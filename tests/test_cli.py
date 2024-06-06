from pathlib import Path

import pytest
from typer.testing import CliRunner

from sksmithy import __version__
from sksmithy._models import EstimatorType
from sksmithy._prompts import (
    PROMPT_DECISION_FUNCTION,
    PROMPT_ESTIMATOR,
    PROMPT_LINEAR,
    PROMPT_NAME,
    PROMPT_PREDICT_PROBA,
)
from sksmithy.cli import app

runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert f"sklearn-smithy={__version__}" in result.stdout


@pytest.mark.parametrize("linear", ["y", "N"])
def test_forge_default(tmp_path: Path, name: str, estimator: EstimatorType, linear: str) -> None:
    """Tests that prompts are correct for classifier estimator."""

    _input = "".join(
        [
            f"{name}\n",  # name
            f"{estimator.value}\n",  # estimator_type
            f"{linear}\n" if estimator in {EstimatorType.ClassifierMixin, EstimatorType.RegressorMixin} else "",
            "\n" if estimator in {EstimatorType.ClassifierMixin, EstimatorType.OutlierMixin} else "",  # predict_proba
            "\n"
            if (linear == "N" and estimator == EstimatorType.ClassifierMixin)
            else "",  # decision_function: prompted only if linear is False
        ]
    )

    output_file = tmp_path / (f"{name.lower()}.py")

    # fmt: off
    result = runner.invoke(
        app=app,
        # By specifying arguments here it is easier to control for the others above.
        # However, this means that prompts are not appearing in the console.
        args=[
            "forge",
            "--required-params", "",
            "--optional-params", "",
            "--no-sample-weight",
            "--tags", "",
            "--output-file", str(output_file)
        ],
        input=_input,
    )
    # fmt: on

    assert result.exit_code == 0

    # General prompts
    assert PROMPT_NAME in result.stdout
    assert PROMPT_ESTIMATOR in result.stdout
    # assert PROMPT_REQUIRED in result.stdout
    # assert PROMPT_OPTIONAL in result.stdout
    # assert PROMPT_SAMPLE_WEIGHT in result.stdout
    # assert PROMPT_TAGS in result.stdout
    # assert f"{PROMPT_OUTPUT} [{name.lower()}.py]" in result.stdout
    assert output_file.exists

    # Estimator type specific prompts
    assert (PROMPT_LINEAR in result.stdout) == (
        estimator in {EstimatorType.ClassifierMixin, EstimatorType.RegressorMixin}
    )
    assert (PROMPT_PREDICT_PROBA in result.stdout) == (
        estimator in {EstimatorType.ClassifierMixin, EstimatorType.OutlierMixin}
    )
    assert (PROMPT_DECISION_FUNCTION in result.stdout) == (linear == "N" and estimator == EstimatorType.ClassifierMixin)


@pytest.mark.parametrize(
    ("invalid_name", "err_msg"),
    [
        ("class", "Error: `class` is a python reserved keyword!"),
        ("abc-xyz", "Error: `abc-xyz` is not a valid python class name!"),
    ],
)
def test_forge_invalid_name(tmp_path: Path, name: str, invalid_name: str, err_msg: str) -> None:
    """Tests that error messages are raised with invalid names."""

    output_file = tmp_path / (f"{name.lower()}.py")
    input_output_file = f"{output_file!s}\n"

    _input = "".join(
        [
            f"{invalid_name}\n",  # name, invalid attempt
            f"{name}\n",  # name, valid attempt
            "transformer\n",  # estimator_type
            "\n",  # required params
            "\n",  # optional params
            "\n",  # sample_weight
            "",  # linear
            "",  # predict_proba
            "",  # decision_function
            "\n",  # tags
            input_output_file,  # output file
        ]
    )

    result = runner.invoke(app, ["forge"], input=_input)

    assert result.exit_code == 0
    assert err_msg in result.stdout


@pytest.mark.parametrize(
    ("invalid_required", "err_msg"),
    [
        ("a-b", "Error: The following parameters are invalid python identifiers: ('a-b',)"),
        ("a,a", "Error: Found repeated parameters!"),
    ],
)
def test_forge_invalid_params(tmp_path: Path, name: str, invalid_required: str, err_msg: str) -> None:
    """Tests that error messages are raised with invalid parameters."""

    output_file = tmp_path / (f"{name.lower()}.py")
    input_output_file = f"{output_file!s}\n"

    _input = "".join(
        [
            f"{name}\n",  # name
            "transformer\n",  # estimator_type
            f"{invalid_required}\n",  # required param, invalid attempt
            "a,b\n",  # required params
            "\n",  # optional params
            "\n",  # sample_weight
            "",  # linear
            "",  # predict_proba
            "",  # decision_function
            "\n",  # tags
            input_output_file,  # output file
        ]
    )

    result = runner.invoke(app, ["forge"], input=_input)

    assert result.exit_code == 0
    assert err_msg in result.stdout


def test_forge_duplicated_params(tmp_path: Path, name: str) -> None:
    """Tests that error messages are raised with duplicated parameters."""

    output_file = tmp_path / (f"{name.lower()}.py")
    input_output_file = f"{output_file!s}\n"

    _input = "".join(
        [
            f"{name}\n",  # name
            "transformer\n",  # estimator_type
            "a,b\n",  # required params
            "a\n",  # optional params, invalid attempt
            "c,d\n",  # optional params, valid attempt
            "\n",  # sample_weight
            "",  # linear
            "",  # predict_proba
            "",  # decision_function
            "\n",  # tags
            input_output_file,  # output file
        ]
    )

    result = runner.invoke(app, ["forge"], input=_input)

    assert result.exit_code == 0
    assert "Error: The following parameters are duplicated between required and optional: {'a'}" in result.stdout
