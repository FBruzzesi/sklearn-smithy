import subprocess
from enum import Enum
from importlib import resources
from pathlib import Path
from typing import Annotated, Final

import typer
from jinja2 import Template

app = typer.Typer(
    help="Awesome CLI to generate scikit-learn estimator boilerplate code",
    rich_markup_mode="rich",
)


class EstimatorType(str, Enum):
    """List of possible estimator types."""

    ClassifierMixin = "classifier"
    OutlierMixin = "outlier"
    RegressorMixin = "regressor"
    TransformerMixin = "transformer"


class TagType(str, Enum):
    """List of extra tags.

    Description of each tag is available at https://scikit-learn.org/dev/developers/develop.html#estimator-tags.
    """

    allow_nan = "allow_nan"
    array_api_support = "array_api_support"
    binary_only = "binary_only"
    multilabel = "multilabel"
    multioutput = "multioutput"
    multioutput_only = "multioutput_only"
    no_validation = "no_validation"
    non_deterministic = "non_deterministic"
    pairwise = "pairwise"
    preserves_dtype = "preserves_dtype"
    poor_score = "poor_score"
    requires_fit = "requires_fit"
    requires_positive_X = "requires_positive_X"  # noqa: N815
    requires_y = "requires_y"
    requires_positive_y = "requires_positive_y"
    _skip_test = "_skip_test"
    _xfail_checks = "_xfail_checks"
    stateless = "stateless"
    X_types = "X_types"


TEMPLATE_PATH: Final[Path] = resources.files("skboilerplate") / "template.py.jinja"


# TODO: Add validation with callbacks
# name: no special characters
# required: no dashes or special chars except "_"
# other: no dashes or special chars except "_"
@app.command()
def main(
    name: Annotated[
        str,
        typer.Option(
            prompt="🐍 How would you like to name the estimator?",
            help="[bold green]name[/bold green] the estimator.",
            # callback= ...,
        ),
    ],
    estimator_type: Annotated[
        EstimatorType,
        typer.Option(
            prompt="🎯 Which kind of estimator is it?",
            help="Estimator type.",
        ),
    ],
    required_params: Annotated[
        str,
        typer.Option(
            prompt="📜 Please list the required parameters (comma-separated)",
            help=(
                "List of [bold green]required[/bold green] parameters. "
                "Must be comma-separated valid python variable names."
            ),
        ),
    ] = "",
    other_params: Annotated[
        str,
        typer.Option(
            prompt="📑 Please list the other parameters (comma or space separated)",
            help=(
                "List of [bold green]optional[/bold green] parameters. "
                "Must be comma-separated valid python variable names."
            ),
        ),
    ] = "",
    support_sample_weight: Annotated[
        bool,
        typer.Option(
            prompt="📶 Should the estimator `.fit()` method support `sample_weight`?",
            help="Whether or not the estimator `.fit()` method should support the `sample_weight` argument",
        ),
    ] = False,
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

    output_file = typer.prompt("📂 Where would you like to save the class?", default=f"{name.lower()}.py")

    required = required_params.split(",") if required_params else []  # TODO: Add parser callback
    others = other_params.split(",") if other_params else []  # TODO: Add parser callback
    params = [*required, *others]

    tags = tags.split(",") if tags else None
    unavailable_tags = tuple(t for t in tags if t not in TagType.__members__)

    if len(unavailable_tags):
        msg = (
            f"The following tags are not available: {unavailable_tags}."
            "\nPlease check the documentation at https://scikit-learn.org/dev/developers/develop.html#estimator-tags"
            " to know which values are avaiable."
        )
        raise ValueError(msg)

    values = {
        "name": name,
        "estimator_type": estimator_type.value,
        "mixin": estimator_type.name,
        "linear": is_linear,
        "support_sample_weight": support_sample_weight,
        "required": required,
        "others": others,
        "parameters": params,
        "decision_function": decision_function,
        "predict_proba": predict_proba,
        "tags": tags,
    }

    destination_file = Path(output_file)
    destination_file.parent.mkdir(parents=True, exist_ok=True)

    with TEMPLATE_PATH.open(mode="r") as stream:
        template = Template(stream.read())

    with destination_file.open(mode="w") as destination:
        destination.write(template.render(values))

    subprocess.run(["ruff", "format", str(destination_file), "-q"], check=True)


if __name__ == "__main__":
    app()
