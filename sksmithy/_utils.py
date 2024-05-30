import subprocess
from importlib import resources
from pathlib import Path
from typing import Final

from jinja2 import Template

from sksmithy._models import EstimatorType

TEMPLATE_PATH: Final[Path] = Path(str(resources.files("sksmithy") / "template.py.jinja"))


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

    Parameters
    ----------
    name: The name of the template.
    estimator_type : The type of the estimator.
    required : A list of required parameters.
    optional : A list of optional parameters.
    linear : Whether the estimator is linear or not
    sample_weight : Whether the estimator supports sample weights in `.fit()` or not
    predict_proba : Whether the estimator will have a `.predict_proba()` method or not.
    decision_function : Whether the estimator will have `.decision_function()` method or not.
    tags : A list of scikit-learn extra tags.

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
