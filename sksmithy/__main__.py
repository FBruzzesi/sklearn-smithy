from pathlib import Path

import typer

from sksmithy._arguments import (
    estimator_type_arg,
    name_arg,
    optional_params_arg,
    required_params_arg,
    sample_weight_arg,
)
from sksmithy._callbacks import parse_tags
from sksmithy._logger import console
from sksmithy._models import EstimatorType
from sksmithy._prompts import PROMPT_DECISION_FUNCTION, PROMPT_LINEAR, PROMPT_OUTPUT, PROMPT_PREDICT_PROBA, PROMPT_TAGS
from sksmithy._utils import render_template

app = typer.Typer(
    help="Awesome CLI to generate scikit-learn estimator boilerplate code",
    rich_markup_mode="rich",
)


@app.command()
def version() -> None:
    """Display library version."""
    from importlib import metadata

    __version__ = metadata.version("sklearn-smithy")
    console.print(f"sklearn-smithy {__version__}", style="good")


@app.command()
def forge(
    name: name_arg,
    estimator_type: estimator_type_arg,
    required_params: required_params_arg = "",
    optional_params: optional_params_arg = "",
    sample_weight: sample_weight_arg = False,
) -> None:
    """Asks a list of questions to generate a shiny new estimator ✨

    Depending on the **estimator type** the additional information could be required:

    * if the estimator is linear (classifier or regression)

    * if the estimator has a `predict_proba` method (classifier or outlier detector)

    * is the estimator has a `decision_function` method (classifier only)

    Finally, the following two questions will be prompt:

    * if the estimator should have tags (To know more about tags, check the dedicated
        [scikit-learn documentation](https://scikit-learn.org/dev/developers/develop.html#estimator-tags))

    * in which file the class should be saved (default is `f'{name.lower()}.py'`)
    """
    required = required_params.split(",") if required_params else []
    optional = optional_params.split(",") if optional_params else []

    duplicated_params = set(required).intersection(set(optional))
    if duplicated_params:
        msg_duplicated_params = f"The following parameters are duplicated: {duplicated_params}"
        raise typer.BadParameter(msg_duplicated_params)

    # Check if linear
    match estimator_type:
        case EstimatorType.ClassifierMixin | EstimatorType.RegressorMixin:
            linear = typer.confirm(PROMPT_LINEAR)
        case _:
            linear = False

    # Check if supports predict_proba
    match estimator_type:
        case EstimatorType.ClassifierMixin | EstimatorType.OutlierMixin:
            predict_proba = typer.confirm(PROMPT_PREDICT_PROBA)
        case _:
            predict_proba = False

    # Check if supports decision_function
    match estimator_type:
        case EstimatorType.ClassifierMixin:
            decision_function = typer.confirm(PROMPT_DECISION_FUNCTION)
        case _:
            decision_function = False

    tags = typer.prompt(PROMPT_TAGS, default="")
    tags = parse_tags(tags)

    output_file = typer.prompt(PROMPT_OUTPUT, default=f"{name.lower()}.py")

    forged_template = render_template(
        name=name,
        estimator_type=estimator_type,
        required=required,
        optional=optional,
        linear=linear,
        sample_weight=sample_weight,
        predict_proba=predict_proba,
        decision_function=decision_function,
        tags=tags,
    )

    try:
        destination_file = Path(output_file)
        destination_file.parent.mkdir(parents=True, exist_ok=True)

        with destination_file.open(mode="w") as destination:
            destination.write(forged_template)

        console.print(f"Template forged at {destination_file}", style="good")

    except Exception as e:  # noqa: BLE001
        console.print(f"Failed to forge template due to the following exception: {e}", style="bad")


if __name__ == "__main__":
    app()
