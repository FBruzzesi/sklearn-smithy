from typing import Annotated

from typer import Option

from sksmithy._callbacks import estimator_callback, name_callback, params_callback, tags_callback
from sksmithy._models import EstimatorType
from sksmithy._prompts import (
    PROMPT_DECISION_FUNCTION,
    PROMPT_ESTIMATOR,
    PROMPT_LINEAR,
    PROMPT_NAME,
    PROMPT_OPTIONAL,
    PROMPT_OUTPUT,
    PROMPT_PREDICT_PROBA,
    PROMPT_REQUIRED,
    PROMPT_SAMPLE_WEIGHT,
    PROMPT_TAGS,
)

name_arg = Annotated[
    str,
    Option(
        prompt=PROMPT_NAME,
        prompt_required=False,
        help="[bold green]Name[/bold green] the estimator.",
        callback=name_callback,
    ),
]

estimator_type_arg = Annotated[
    EstimatorType,
    Option(
        prompt=PROMPT_ESTIMATOR,
        prompt_required=False,
        help="Estimator type.",
        callback=estimator_callback,
    ),
]

required_params_arg = Annotated[
    str,
    Option(
        prompt=PROMPT_REQUIRED,
        help="List of [bold green]required[/bold green] parameters (comma-separated).",
        callback=params_callback,
    ),
]

optional_params_arg = Annotated[
    str,
    Option(
        prompt=PROMPT_OPTIONAL,
        help="List of [bold green]optional[/bold green] parameters (comma-separated).",
        callback=params_callback,
    ),
]

sample_weight_arg = Annotated[
    bool,
    Option(
        is_flag=True,
        prompt=PROMPT_SAMPLE_WEIGHT,
        prompt_required=False,
        help="Whether or not `.fit()` does support [bold green]`sample_weight`[/bold green].",
    ),
]

linear_arg = Annotated[
    bool,
    Option(
        is_flag=True,
        prompt=PROMPT_LINEAR,
        help="Whether or not the estimator is [bold green]linear[/bold green].",
    ),
]

predict_proba_arg = Annotated[
    bool,
    Option(
        is_flag=True,
        prompt=PROMPT_PREDICT_PROBA,
        help="Whether or not the estimator implements [bold green]`predict_proba`[/bold green] method.",
    ),
]

decision_function_arg = Annotated[
    bool,
    Option(
        is_flag=True,
        prompt=PROMPT_DECISION_FUNCTION,
        help="Whether or not the estimator implements [bold green]`decision_function`[/bold green] method.",
    ),
]

tags_arg = Annotated[
    str,
    Option(
        prompt=PROMPT_TAGS,
        prompt_required=False,
        help="List of optional scikit-learn [bold green]tags[/bold green].",
        callback=tags_callback,
    ),
]

output_file_arg = Annotated[
    str,
    Option(
        prompt=PROMPT_OUTPUT,
        help="[bold green]Destination file[/bold green] where to save the boilerplate code.",
    ),
]
