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
    PROMPT_OPTIONAL,
    PROMPT_OUTPUT,
    PROMPT_PREDICT_PROBA,
    PROMPT_REQUIRED,
    PROMPT_SAMPLE_WEIGHT,
    PROMPT_TAGS,
)
from sksmithy.cli import cli

runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert f"sklearn-smithy={__version__}" in result.stdout


@pytest.mark.parametrize("linear", ["y", "N"])
def test_forge_estimator(tmp_path: Path, name: str, estimator: EstimatorType, linear: str) -> None:
    """Tests that prompts are correct for classifier estimator."""
    output_file = tmp_path / (f"{name.lower()}.py")
    assert not output_file.exists()

    _input = "".join(
        [
            f"{name}\n",  # name
            f"{estimator.value}\n",  # estimator_type
            "\n",  # required params
            "\n",  # optional params
            "\n",  # sample weight
            f"{linear}\n" if estimator in {EstimatorType.ClassifierMixin, EstimatorType.RegressorMixin} else "",
            "\n" if estimator in {EstimatorType.ClassifierMixin, EstimatorType.OutlierMixin} else "",  # predict_proba
            "\n"
            if (linear == "N" and estimator == EstimatorType.ClassifierMixin)
            else "",  # decision_function: prompted only if not linear
            "\n",  # tags
            f"{output_file!s}\n",  # output file
        ]
    )

    result = runner.invoke(
        app=cli,
        args=["forge"],
        input=_input,
    )

    assert result.exit_code == 0
    assert output_file.exists()

    # General prompts
    assert all(
        _prompt in result.stdout
        for _prompt in (
            PROMPT_NAME,
            PROMPT_ESTIMATOR,
            PROMPT_REQUIRED,
            PROMPT_OPTIONAL,
            PROMPT_SAMPLE_WEIGHT,
            PROMPT_TAGS,
            f"{PROMPT_OUTPUT} [{name.lower()}.py]",
        )
    )

    # Estimator type specific prompts
    assert (PROMPT_LINEAR in result.stdout) == (
        estimator in {EstimatorType.ClassifierMixin, EstimatorType.RegressorMixin}
    )
    assert (PROMPT_PREDICT_PROBA in result.stdout) == (
        estimator in {EstimatorType.ClassifierMixin, EstimatorType.OutlierMixin}
    )
    assert (PROMPT_DECISION_FUNCTION in result.stdout) == (linear == "N" and estimator == EstimatorType.ClassifierMixin)


@pytest.mark.parametrize(
    ("invalid_name", "name_err_msg"),
    [
        ("class", "Error: `class` is a python reserved keyword!"),
        ("abc-xyz", "Error: `abc-xyz` is not a valid python class name!"),
    ],
)
@pytest.mark.parametrize(
    ("invalid_required", "required_err_msg"),
    [
        ("a-b", "Error: The following parameters are invalid python identifiers: ('a-b',)"),
        ("a,a", "Error: Found repeated parameters!"),
    ],
)
@pytest.mark.parametrize(
    ("invalid_optional", "dupliclated_err_msg"),
    [("a", "Error: The following parameters are duplicated between required and optional: {'a'}")],
)
@pytest.mark.parametrize(
    ("invalid_tags", "tags_err_msg"),
    [("not-a-tag,also-not-a-tag", "Error: The following tags are not available: ('not-a-tag', 'also-not-a-tag').")],
)
def test_forge_invalid_args(
    tmp_path: Path,
    name: str,
    invalid_name: str,
    name_err_msg: str,
    invalid_required: str,
    required_err_msg: str,
    invalid_optional: str,
    dupliclated_err_msg: str,
    invalid_tags: str,
    tags_err_msg: str,
) -> None:
    """Tests that error messages are raised with invalid names."""
    output_file = tmp_path / (f"{name.lower()}.py")
    assert not output_file.exists()

    _input = "".join(
        [
            f"{invalid_name}\n",  # name, invalid attempt
            f"{name}\n",  # name, valid attempt
            "transformer\n"  # type
            f"{invalid_required}\n",  # required params, invalid attempt
            "a,b\n",  # required params, valid attempt
            f"{invalid_optional}\n",  # optional params, invalid attempt
            "c,d\n",  # optional params, valid attempt
            "\n",  # sample_weight
            f"{invalid_tags}\n",  # tags, invalid attempt
            "binary_only\n",  # valid attempt
            f"{output_file!s}\n",
        ]
    )

    result = runner.invoke(
        app=cli,
        args=["forge"],
        input=_input,
    )

    result = runner.invoke(cli, ["forge"], input=_input)

    assert result.exit_code == 0
    assert output_file.exists()

    assert all(
        err_msg in result.stdout for err_msg in (name_err_msg, required_err_msg, dupliclated_err_msg, tags_err_msg)
    )
