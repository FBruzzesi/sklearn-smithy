from collections.abc import Callable
from typing import Concatenate, ParamSpec, TypeVar

from typer import BadParameter, CallbackParam, Context

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

    return name


def params_callback(ctx: Context, param: CallbackParam, value: str | None) -> list[str]:
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
