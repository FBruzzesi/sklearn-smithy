import sys
from pathlib import Path

from result import Err, Ok
from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Grid, Horizontal
from textual.widgets import Button, Input, Select, Static, Switch

from sksmithy._models import EstimatorType
from sksmithy._parsers import check_duplicates, name_parser, params_parser
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
)
from sksmithy._utils import render_template
from sksmithy.tui._validators import NameValidator, ParamsValidator

if sys.version_info >= (3, 11):  # pragma: no cover
    from typing import Self
else:  # pragma: no cover
    from typing_extensions import Self


class Prompt(Static):
    pass


class ForgeRow(Grid):
    pass


class Name(Container):
    """Name input component."""

    def compose(self: Self) -> ComposeResult:
        yield Prompt(PROMPT_NAME, classes="label")
        yield Input(placeholder="MightyEstimator", id="name", validators=[NameValidator()])

    @on(Input.Changed, "#name")
    def on_input_change(self: Self, event: Input.Changed) -> None:
        if not event.validation_result.is_valid:
            self.notify(
                message=event.validation_result.failure_descriptions[0],
                title="Invalid Name",
                severity="error",
                timeout=5,
            )
        else:
            output_file: Input = self.app.query_one("#output_file")
            output_file.value = f"{event.value.lower()}.py"


class Estimator(Container):
    """Estimator select component."""

    def compose(self: Self) -> ComposeResult:
        yield Prompt(PROMPT_ESTIMATOR, classes="label")
        yield Select(
            options=((" ".join(x.capitalize() for x in e.value.split("-")), e.value) for e in EstimatorType),
            id="estimator",
        )

    @on(Select.Changed, "#estimator")
    def on_select_change(self: Self, event: Select.Changed) -> None:
        linear: Switch = self.app.query_one("#linear")
        predict_proba: Switch = self.app.query_one("#predict_proba")
        decision_function: Switch = self.app.query_one("#decision_function")

        linear.disabled = event.value not in {"classifier", "regressor"}
        predict_proba.disabled = event.value not in {"classifier", "outlier"}
        decision_function.disabled = event.value not in {"classifier"}

        linear.value = linear.value and (not linear.disabled)
        predict_proba.value = predict_proba.value and (not predict_proba.disabled)
        decision_function.value = decision_function.value and (not decision_function.disabled)


class Required(Container):
    """Required params input component."""

    def compose(self: Self) -> ComposeResult:
        yield Prompt(PROMPT_REQUIRED, classes="label")
        yield Input(placeholder="alpha,beta", id="required", validators=[ParamsValidator()])

    @on(Input.Submitted, "#required")
    def on_input_change(self: Self, event: Input.Submitted) -> None:
        if not event.validation_result.is_valid:
            self.notify(
                message="\n".join(event.validation_result.failure_descriptions),
                title="Invalid Parameter",
                severity="error",
                timeout=5,
            )

        optional: Input = self.app.query_one("#optional").value or ""
        if (
            optional
            and event.value
            and (
                duplicates_result := check_duplicates(
                    event.value.split(","),
                    optional.split(","),
                )
            )
        ):
            self.notify(
                message=duplicates_result,
                title="Duplicate Parameter",
                severity="error",
                timeout=5,
            )


class Optional(Container):
    """Optional params input component."""

    def compose(self: Self) -> ComposeResult:
        yield Prompt(PROMPT_OPTIONAL, classes="label")
        yield Input(placeholder="mu,sigma", id="optional", validators=[ParamsValidator()])

    @on(Input.Submitted, "#optional")
    def on_optional_change(self: Self, event: Input.Submitted) -> None:
        if not event.validation_result.is_valid:
            self.notify(
                message="\n".join(event.validation_result.failure_descriptions),
                title="Invalid Parameter",
                severity="error",
                timeout=5,
            )

        required: Input = self.app.query_one("#required").value or ""
        if (
            required
            and event.value
            and (
                duplicates_result := check_duplicates(
                    required.split(","),
                    event.value.split(","),
                )
            )
        ):
            self.notify(
                message=duplicates_result,
                title="Duplicate Parameter",
                severity="error",
                timeout=5,
            )


class SampleWeight(Container):
    """sample_weight switch component."""

    def compose(self: Self) -> ComposeResult:
        yield Horizontal(
            Prompt(PROMPT_SAMPLE_WEIGHT, classes="label"),
            Switch(id="sample_weight"),
            classes="container",
        )


class Linear(Container):
    """linear switch component."""

    def compose(self: Self) -> ComposeResult:
        yield Horizontal(
            Prompt(PROMPT_LINEAR, classes="label"),
            Switch(id="linear"),
            classes="container",
        )

    @on(Switch.Changed, "#linear")
    def on_switch_changed(self: Self, event: Switch.Changed) -> None:
        decision_function: Switch = self.app.query_one("#decision_function")
        decision_function.disabled = event.value
        decision_function.value = decision_function.value and (not decision_function.disabled)


class PredictProba(Container):
    """predict_proba switch component."""

    def compose(self: Self) -> ComposeResult:
        yield Horizontal(
            Prompt(PROMPT_PREDICT_PROBA, classes="label"),
            Switch(id="predict_proba"),
            classes="container",
        )


class DecisionFunction(Container):
    """decision_function switch component."""

    def compose(self: Self) -> ComposeResult:
        yield Horizontal(
            Prompt(PROMPT_DECISION_FUNCTION, classes="label"),
            Switch(id="decision_function"),
            classes="container",
        )


class DestinationFile(Container):
    """Destination file input component."""

    def compose(self: Self) -> ComposeResult:
        yield Prompt(PROMPT_OUTPUT, classes="label", id="output_prompt")
        yield Input(placeholder="mightyestimator.py", id="output_file")


class ForgeButton(Container):
    """forge button component."""

    def compose(self: Self) -> ComposeResult:
        yield Button.success(
            label="Forge ⚒️",
            id="forge_btn",
        )

    @on(Button.Pressed, "#forge_btn")
    def on_button_pressed(self: Self, _: Button.Pressed) -> None:
        errors = []

        name_input: str = self.app.query_one("#name").value
        estimator: str | None = self.app.query_one("#estimator").value
        required_params: str = self.app.query_one("#required").value
        optional_params: str = self.app.query_one("#optional").value

        sample_weight: bool = self.app.query_one("#linear").value
        linear: bool = self.app.query_one("#linear").value
        predict_proba: bool = self.app.query_one("#predict_proba").value
        decision_function: bool = self.app.query_one("#decision_function").value

        output_file: str = self.app.query_one("#output_file").value

        match name_parser(name_input):
            case Ok(name):
                pass
            case Err(name_error_msg):
                errors.append(name_error_msg)

        match estimator:
            case str(v):
                estimator_type = EstimatorType(v)
            case Select.BLANK:
                errors.append("Estimator cannot be None")

        match params_parser(required_params):
            case Ok(required):
                required_is_valid = True
            case Err(required_err_msg):
                required_is_valid = False
                errors.append(required_err_msg)

        match params_parser(optional_params):
            case Ok(optional):
                optional_is_valid = True

            case Err(optional_err_msg):
                optional_is_valid = False
                errors.append(optional_err_msg)

        if required_is_valid and optional_is_valid and (msg_duplicated_params := check_duplicates(required, optional)):
            errors.append(msg_duplicated_params)

        if not output_file:
            errors.append("Outfile file cannot be empty")

        if errors:
            self.notify(
                message="\n".join([f"- {e}" for e in errors]),
                title="Invalid inputs",
                severity="error",
                timeout=5,
            )

        else:
            forged_template = render_template(
                name=name,
                estimator_type=estimator_type,
                required=required,
                optional=optional,
                linear=linear,
                sample_weight=sample_weight,
                predict_proba=predict_proba,
                decision_function=decision_function,
                tags=None,
            )

            destination_file = Path(output_file)
            destination_file.parent.mkdir(parents=True, exist_ok=True)

            with destination_file.open(mode="w") as destination:
                destination.write(forged_template)

            self.notify(
                message=f"Template forged at {destination_file}",
                title="Success!",
                severity="information",
                timeout=5,
            )


forge_row = ForgeRow(Static(), Static(), ForgeButton(), DestinationFile(), Static(), Static(), id="forge_row")

# class Version(Static):
#     def render(self: Self) -> RenderableType:
#         return f"Version: [b]{version('sklearn-smithy')}"


# class Sidebar(Container):
#     def compose(self: Self) -> ComposeResult:
#         yield Title("Description")
#         yield Container(MarkdownViewer(SIDEBAR_MSG))
#         yield Version()
