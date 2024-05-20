from typing import Annotated

from typer import Option

from sksmithy._callbacks import args_callback, name_callback
from sksmithy._models import EstimatorType

name_arg = Annotated[
    str,
    Option(
        prompt="🐍 How would you like to name the estimator?",
        help="[bold green]name[/bold green] the estimator.",
        callback=name_callback,
    ),
]

estimator_type_arg = Annotated[
    EstimatorType,
    Option(
        prompt="🎯 Which kind of estimator is it?",
        help="Estimator type.",
    ),
]

required_params_arg = Annotated[
    str,
    Option(
        prompt="📜 Please list the required parameters (comma-separated)",
        help=("List of [bold green]required[/bold green] parameters (comma-separated)."),
        callback=args_callback,
    ),
]
other_params_arg = Annotated[
    str,
    Option(
        prompt="📑 Please list the other parameters (comma separated)",
        help=("List of [bold green]optional[/bold green] parameters (comma-separated)."),
        callback=args_callback,
    ),
]

support_sample_weight_arg = Annotated[
    bool,
    Option(
        prompt="📶 Does the `.fit()` method support `sample_weight`?",
        help="Whether or not `.fit()` does support [bold green]`sample_weight`[/bold green].",
    ),
]
