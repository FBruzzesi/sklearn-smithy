import subprocess
from enum import Enum
from importlib import resources
from pathlib import Path
from typing import Final, Union

import typer
from jinja2 import Template


class EstimatorType(str, Enum):
    """List of possible estimator types."""

    ClassifierMixin = "classifier"
    OutlierMixin = "outlier"
    RegressorMixin = "regressor"
    TransformerMixin = "transformer"


TEMPLATE_PATH: Final[Path] = resources.files("skboilerplate") / "template.py.jinja"


def main(
    name: str,
    estimator_type: EstimatorType,
    required_params: Union[str, None] = None,  # noqa: UP007
    other_params: Union[str, None] = None,  # noqa: UP007
    support_sample_weight: bool = False,
    linear: bool = False,
    output_file: str = "",
) -> None:
    """Generate boilerplate code given options."""
    with TEMPLATE_PATH.open(mode="r") as stream:
        template = Template(stream.read())

    required = required_params.split(",") if required_params else []
    others = other_params.split(",") if other_params else []
    params = [*required, *others]

    values = {
        "name": name,
        "estimator_type": estimator_type.value,
        "mixin": estimator_type.name,
        "linear": linear,
        "support_sample_weight": support_sample_weight,
        "required": required,
        "others": others,
        "parameters": params,
    }

    destination_file = Path(output_file or f"{name.lower()}.py")
    destination_file.parent.mkdir(parents=True, exist_ok=True)

    with destination_file.open(mode="w") as destination:
        destination.write(template.render(values))

    subprocess.run(["ruff", "format", str(destination_file), "-q"], check=True)


if __name__ == "__main__":
    typer.run(main)
