from collections.abc import Callable
from typing import Concatenate, ParamSpec, TypeVar

from typer import BadParameter, CallbackParam, Context

from sksmithy._models import EstimatorType
from sksmithy._parsers import check_duplicates, name_parser, params_parser, tags_parser
from sksmithy._prompts import PROMPT_DECISION_FUNCTION, PROMPT_LINEAR, PROMPT_PREDICT_PROBA

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


def estimator_callback(ctx: Context, param: CallbackParam, value: EstimatorType) -> EstimatorType:
    """`estimator_type` argument callback.

    It dynamically modifies the behaviour of the rest of the prompts based on its value.
    """
    if not ctx.obj:
        ctx.obj = {}

    if param.name in ctx.obj:
        return ctx, param, ctx.obj[param.name]

    linear, predict_proba, decision_function = (
        op for op in ctx.command.params if op.name in {"linear", "predict_proba", "decision_function"}
    )

    match value:
        case EstimatorType.ClassifierMixin | EstimatorType.RegressorMixin:
            linear.prompt = PROMPT_LINEAR
            linear.prompt_required = True
        case _:
            linear.prompt = False
            linear.prompt_required = False

    match value:
        case EstimatorType.ClassifierMixin | EstimatorType.OutlierMixin:
            predict_proba.prompt = PROMPT_PREDICT_PROBA
            predict_proba.prompt_required = True
        case _:
            predict_proba.prompt = False
            predict_proba.prompt_required = False

    # Check if supports decision_function
    match value:
        case EstimatorType.ClassifierMixin:
            decision_function.prompt = PROMPT_DECISION_FUNCTION
            decision_function.prompt_required = True
        case _:
            decision_function.prompt = False
            decision_function.prompt_required = False

    ctx.obj[param.name] = value

    return value
