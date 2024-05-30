from collections.abc import Callable
from typing import Concatenate, ParamSpec, TypeVar

from typer import BadParameter, CallbackParam, Context

from sksmithy._models import EstimatorType
from sksmithy._parsers import check_duplicates, name_parser, params_parser, tags_parser

T = TypeVar("T")
R = TypeVar("R")
PS = ParamSpec("PS")


def _parse_wrapper(
    ctx: Context,
    param: CallbackParam,
    value: T,
    parser: Callable[Concatenate[T, PS], tuple[R, str]],
    *args: PS.args,
    **kwargs: PS.kwargs,
) -> tuple[Context, CallbackParam, R]:
    """Wrap a parser to handle 'caching' logic."""
    if not ctx.obj:
        ctx.obj = {}

    if param.name in ctx.obj:
        return ctx, param, ctx.obj[param.name]

    result, msg = parser(value, *args, **kwargs)

    if msg:
        raise BadParameter(msg)

    ctx.obj[param.name] = result
    return ctx, param, result


def name_callback(ctx: Context, param: CallbackParam, value: str) -> str:
    """`name` argument callback."""
    *_, name = _parse_wrapper(ctx, param, value, name_parser)

    all_options = ctx.command.params
    output_file_option = next(opt for opt in all_options if opt.name == "output_file")
    output_file_option.default = f"{name.lower()}.py"

    return name


def params_callback(ctx: Context, param: CallbackParam, value: str) -> list[str]:
    """`required-params` and `optional-params` arguments callback."""
    ctx, param, parsed_params = _parse_wrapper(ctx, param, value, params_parser)

    if param.name == "optional_params" and (
        msg := check_duplicates(
            required=ctx.params["required_params"],
            optional=parsed_params,
        )
    ):
        del ctx.obj[param.name]
        raise BadParameter(msg)

    return parsed_params


def tags_callback(ctx: Context, param: CallbackParam, value: str) -> list[str]:
    """`tags` argument callback."""
    *_, parsed_value = _parse_wrapper(ctx, param, value, tags_parser)
    return parsed_value


def estimator_callback(ctx: Context, param: CallbackParam, estimator: EstimatorType) -> str:
    """`estimator_type` argument callback.

    It dynamically modifies the behaviour of the rest of the prompts based on its value.
    """
    if not ctx.obj:
        ctx.obj = {}

    if param.name in ctx.obj:
        return ctx.obj[param.name]

    linear, predict_proba, decision_function = (
        op for op in ctx.command.params if op.name in {"linear", "predict_proba", "decision_function"}
    )

    match estimator:
        case EstimatorType.ClassifierMixin | EstimatorType.RegressorMixin:
            pass
        case _:
            linear.prompt = False  # type: ignore[attr-defined]
            linear.prompt_required = False  # type: ignore[attr-defined]

    match estimator:
        case EstimatorType.ClassifierMixin | EstimatorType.OutlierMixin:
            pass
        case _:
            predict_proba.prompt = False  # type: ignore[attr-defined]
            predict_proba.prompt_required = False  # type: ignore[attr-defined]

    match estimator:
        case EstimatorType.ClassifierMixin:
            pass
        case _:
            decision_function.prompt = False  # type: ignore[attr-defined]
            decision_function.prompt_required = False  # type: ignore[attr-defined]

    ctx.obj[param.name] = estimator.value

    return estimator.value
