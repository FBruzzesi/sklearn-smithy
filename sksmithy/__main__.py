from pathlib import Path

import typer

from sksmithy._arguments import (
    decision_function_arg,
    estimator_type_arg,
    linear_arg,
    name_arg,
    optional_params_arg,
    output_file_arg,
    predict_proba_arg,
    required_params_arg,
    sample_weight_arg,
    tags_arg,
)
from sksmithy._logger import console
from sksmithy._utils import render_template

app = typer.Typer(
    help="Awesome CLI to generate scikit-learn estimator boilerplate code",
    rich_markup_mode="rich",
    rich_help_panel="Customization and Utils",
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
    linear: linear_arg = False,
    predict_proba: predict_proba_arg = False,
    decision_function: decision_function_arg = False,
    tags: tags_arg = "",
    output_file: output_file_arg = "",
) -> None:
    """Generate a new shiny scikit-learn compatible estimator ✨

    Depending on the estimator type the following additional information could be required:

    * if the estimator is linear (classifier or regression)
    * if the estimator has a `predict_proba` method (classifier or outlier detector)
    * is the estimator has a `decision_function` method (classifier only)

    Finally, the following two questions will be prompt:

    * if the estimator should have tags (To know more about tags, check the dedicated scikit-learn documentation
        at https://scikit-learn.org/dev/developers/develop.html#estimator-tags
    * in which file the class should be saved (default is `f'{name.lower()}.py'`)
    """
    forged_template = render_template(
        name=name,
        estimator_type=estimator_type,
        required=required_params,  # type: ignore[arg-type]  # Callback transforms it into `list[str]`
        optional=optional_params,  # type: ignore[arg-type]  # Callback transforms it into `list[str]`
        linear=linear,
        sample_weight=sample_weight,
        predict_proba=predict_proba,
        decision_function=decision_function,
        tags=tags,  # type: ignore[arg-type]  # Callback transforms it into `list[str]`
    )

    destination_file = Path(output_file)
    destination_file.parent.mkdir(parents=True, exist_ok=True)

    with destination_file.open(mode="w") as destination:
        destination.write(forged_template)

    console.print(f"Template forged at {destination_file}", style="good")


if __name__ == "__main__":
    app()
