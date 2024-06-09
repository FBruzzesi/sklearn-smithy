import subprocess
from importlib import resources
from pathlib import Path
from typing import Final

from jinja2 import Template

from sksmithy._models import EstimatorType

TEMPLATE_PATH: Final[Path] = Path(str(resources.files("sksmithy") / "_static" / "template.py.jinja"))


def render_template(
    name: str,
    estimator_type: EstimatorType,
    required: list[str],
    optional: list[str],
    linear: bool = False,
    sample_weight: bool = False,
    predict_proba: bool = False,
    decision_function: bool = False,
    tags: list[str] | None = None,
) -> str:
    """
    Render a template using the provided parameters.

    This is achieved in a two steps process:

    - Render the jinja template using the input values.
    - Format the string using ruff formatter.

    !!! warning

        This function **does not** validate that arguments are necessarely compatible with each other.
        For instance, it could be possible to pass `estimator_type = EstimatorType.RegressorMixin` and
        `predict_proba = True` which makes no sense as combination, but it would not raise an error.

    Parameters
    ----------
    name
        The name of the template.
    estimator_type
        The type of the estimator.
    required
        The list of required parameters.
    optional
        The list of optional parameters.
    linear
        Whether or not the estimator is linear.
    sample_weight
        Whether or not the estimator supports sample weights in `.fit()`.
    predict_proba
        Whether or not the estimator should implement `.predict_proba()` method.
    decision_function
        Whether or not the estimator should implement `.decision_function()` method.
    tags
        The list of scikit-learn extra tags.

    Returns
    -------
    str : The rendered and formatted template as a string.
    """
    values = {
        "name": name,
        "estimator_type": estimator_type.value,
        "mixin": estimator_type.name,
        "required": required,
        "optional": optional,
        "parameters": [*required, *optional],
        "linear": linear,
        "sample_weight": sample_weight,
        "predict_proba": predict_proba,
        "decision_function": decision_function,
        "tags": tags,
    }

    with TEMPLATE_PATH.open(mode="r") as stream:
        template = Template(stream.read()).render(values)

    return subprocess.check_output(["ruff", "format", "-"], input=template, encoding="utf-8")
