from typing import Annotated

from typer import Option

from sksmithy._callbacks import args_callback, name_callback
from sksmithy._models import EstimatorType
from sksmithy._prompts import PROMPT_ESTIMATOR, PROMPT_NAME, PROMPT_OPTIONAL, PROMPT_REQUIRED, PROMPT_SAMPLE_WEIGHT

name_arg = Annotated[
    str,
    Option(
        prompt=PROMPT_NAME,
        help="[bold green]Name[/bold green] the estimator.",
        callback=name_callback,
    ),
]

estimator_type_arg = Annotated[
    EstimatorType,
    Option(
        prompt=PROMPT_ESTIMATOR,
        help="Estimator type.",
    ),
]

required_params_arg = Annotated[
    str,
    Option(
        prompt=PROMPT_REQUIRED,
        help=("List of [bold green]required[/bold green] parameters (comma-separated)."),
        callback=args_callback,
    ),
]
optional_params_arg = Annotated[
    str,
    Option(
        prompt=PROMPT_OPTIONAL,
        help=("List of [bold green]optional[/bold green] parameters (comma-separated)."),
        callback=args_callback,
    ),
]

support_sample_weight_arg = Annotated[
    bool,
    Option(
        prompt=PROMPT_SAMPLE_WEIGHT,
        help="Whether or not `.fit()` does support [bold green]`sample_weight`[/bold green].",
    ),
]
