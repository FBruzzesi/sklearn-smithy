import subprocess
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Final

import typer
from jinja2 import Template

from sksmithy._arguments import (
    estimator_type_arg,
    name_arg,
    other_params_arg,
    required_params_arg,
    support_sample_weight_arg,
)
from sksmithy._callbacks import parse_tags
from sksmithy._logger import console
from sksmithy._models import EstimatorType

app = typer.Typer(
    help="Awesome CLI to generate scikit-learn estimator boilerplate code",
    rich_markup_mode="rich",
)


TEMPLATE_PATH: Final[Traversable] = resources.files("sksmithy") / "template.py.jinja"


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
    other_params: other_params_arg = "",
    support_sample_weight: support_sample_weight_arg = False,
) -> None:
    """Asks a list of questions to generate a shiny new estimator ✨

    Depending on the **estimator type** the additional information could be required:

    * if the estimator is linear (classifier or regression)

    * if the estimator has a `predict_proba` method (classifier or outlier detector)

    * is the estimator has a `decision_function` method (classifier only)

    Finally, the following two questions will be prompt:

    * if the estimator should have tags (To know more about tags, check the dedicated
        [scikit-learn documentation](https://scikit-learn.org/dev/developers/develop.html#estimator-tags)

    * in which file the class should be saved (default is `f'{name.lower()}.py'`)
    """
    # Check if linear
    match estimator_type:
        case EstimatorType.ClassifierMixin | EstimatorType.RegressorMixin:
            is_linear = typer.confirm("📏 Is the estimator linear?")
        case _:
            is_linear = False

    # Check if supports predict_proba
    match estimator_type:
        case EstimatorType.ClassifierMixin | EstimatorType.OutlierMixin:
            predict_proba = typer.confirm("🎲 Should the estimator have a `predict_proba` method?")
        case _:
            predict_proba = False

    # Check if supports decision_function
    match estimator_type:
        case EstimatorType.ClassifierMixin:
            decision_function = typer.confirm("❓ Should the estimator have a `decision_function` method?")
        case _:
            decision_function = False

    tags = typer.prompt(
        "🧪 We are almost there... Are there any tag you want to add? (comma or space separated)\n"
        "To know more about tags, check the documentation at:\n"
        "https://scikit-learn.org/dev/developers/develop.html#estimator-tags",
        default="",
    )
    tags = parse_tags(tags)

    output_file = typer.prompt("📂 Where would you like to save the class?", default=f"{name.lower()}.py")

    required = required_params.split(",")
    other = other_params.split(",")
    params = [*required, *other]

    values = {
        "name": name,
        "estimator_type": estimator_type.value,
        "mixin": estimator_type.name,
        "linear": is_linear,
        "support_sample_weight": support_sample_weight,
        "required": required,
        "others": other,
        "parameters": params,
        "decision_function": decision_function,
        "predict_proba": predict_proba,
        "tags": tags,
    }

    with TEMPLATE_PATH.open(mode="r") as stream:
        template = Template(stream.read())

    try:
        destination_file = Path(output_file)
        destination_file.parent.mkdir(parents=True, exist_ok=True)

        with destination_file.open(mode="w") as destination:
            destination.write(template.render(values))

        subprocess.run(["ruff", "format", str(destination_file), "-q"], check=True)

        console.print(f"Template forged at {destination_file}", style="good")

    except Exception as e:  # noqa: BLE001
        console.print(f"Failed to forge template due to the following exception: {e}", style="bad")


if __name__ == "__main__":
    app()
