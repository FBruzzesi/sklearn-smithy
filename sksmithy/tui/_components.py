import sys
import webbrowser
from importlib import resources
from pathlib import Path

from result import Err, Ok
from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Grid, Horizontal, ScrollableContainer
from textual.widgets import Button, Collapsible, Input, Markdown, Select, Static, Switch, TextArea

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


SIDEBAR_MSG: str = (resources.files("sksmithy") / "_static" / "description.md").read_text()


class Prompt(Static):
    pass


class Name(Container):
    """Name input component."""

    def compose(self: Self) -> ComposeResult:
        yield Prompt(PROMPT_NAME, classes="label")
        yield Input(placeholder="MightyEstimator", id="name", validators=[NameValidator()])

    @on(Input.Changed, "#name")
    def on_input_change(self: Self, event: Input.Changed) -> None:
        if not event.validation_result.is_valid:  # type: ignore[union-attr]
            self.notify(
                message=event.validation_result.failure_descriptions[0],  # type: ignore[union-attr]
                title="Invalid Name",
                severity="error",
                timeout=5,
            )
        else:
            output_file = self.app.query_one("#output-file", Input)
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
        linear = self.app.query_one("#linear", Switch)
        predict_proba = self.app.query_one("#predict_proba", Switch)
        decision_function = self.app.query_one("#decision_function", Switch)

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
        if not event.validation_result.is_valid:  # type: ignore[union-attr]
            self.notify(
                message="\n".join(event.validation_result.failure_descriptions),  # type: ignore[union-attr]
                title="Invalid Parameter",
                severity="error",
                timeout=5,
            )

        optional = self.app.query_one("#optional", Input).value or ""
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
        if not event.validation_result.is_valid:  # type: ignore[union-attr]
            self.notify(
                message="\n".join(event.validation_result.failure_descriptions),  # type: ignore[union-attr]
                title="Invalid Parameter",
                severity="error",
                timeout=5,
            )

        required = self.app.query_one("#required", Input).value or ""
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
            Switch(id="sample_weight"),
            Prompt(PROMPT_SAMPLE_WEIGHT, classes="label"),
            classes="container",
        )


class Linear(Container):
    """linear switch component."""

    def compose(self: Self) -> ComposeResult:
        yield Horizontal(
            Switch(id="linear"),
            Prompt(PROMPT_LINEAR, classes="label"),
            classes="container",
        )

    @on(Switch.Changed, "#linear")
    def on_switch_changed(self: Self, event: Switch.Changed) -> None:
        decision_function = self.app.query_one("#decision_function", Switch)
        decision_function.disabled = event.value
        decision_function.value = decision_function.value and (not decision_function.disabled)


class PredictProba(Container):
    """predict_proba switch component."""

    def compose(self: Self) -> ComposeResult:
        yield Horizontal(
            Switch(id="predict_proba"),
            Prompt(PROMPT_PREDICT_PROBA, classes="label"),
            classes="container",
        )


class DecisionFunction(Container):
    """decision_function switch component."""

    def compose(self: Self) -> ComposeResult:
        yield Horizontal(
            Switch(id="decision_function"),
            Prompt(PROMPT_DECISION_FUNCTION, classes="label"),
            classes="container",
        )


class ForgeButton(Container):
    """forge button component."""

    def compose(self: Self) -> ComposeResult:
        yield Button(label="Forge ⚒️", id="forge-btn", variant="success")

    @on(Button.Pressed, "#forge-btn")
    def on_forge(self: Self, _: Button.Pressed) -> None:  # noqa: C901
        errors = []

        name_input = self.app.query_one("#name", Input).value
        estimator = self.app.query_one("#estimator", Select).value
        required_params = self.app.query_one("#required", Input).value
        optional_params = self.app.query_one("#optional", Input).value

        sample_weight = self.app.query_one("#linear", Switch).value
        linear = self.app.query_one("#linear", Switch).value
        predict_proba = self.app.query_one("#predict_proba", Switch).value
        decision_function = self.app.query_one("#decision_function", Switch).value

        code_area = self.app.query_one("#code-area", TextArea)
        code_editor = self.app.query_one("#code-editor", Collapsible)

        match name_parser(name_input):
            case Ok(name):
                pass
            case Err(name_error_msg):
                errors.append(name_error_msg)

        match estimator:
            case str(v):
                estimator_type = EstimatorType(v)
            case Select.BLANK:
                errors.append("Estimator cannot be empty!")

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

        if errors:
            self.notify(
                message="\n".join([f"- {e}" for e in errors]),
                title="Invalid inputs!",
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

            code_area.text = forged_template
            code_editor.collapsed = False

            self.notify(
                message="Template forged!",
                title="Success!",
                severity="information",
                timeout=5,
            )


class SaveButton(Container):
    """forge button component."""

    def compose(self: Self) -> ComposeResult:
        yield Button(label="Save 📂", id="save-btn", variant="primary")

    @on(Button.Pressed, "#save-btn")
    def on_save(self: Self, _: Button.Pressed) -> None:
        output_file = self.app.query_one("#output-file", Input).value

        if not output_file:
            self.notify(
                message="Outfile filename cannot be empty!",
                title="Invalid filename!",
                severity="error",
                timeout=5,
            )
        else:
            destination_file = Path(output_file)
            destination_file.parent.mkdir(parents=True, exist_ok=True)

            code = self.app.query_one("#code-area", TextArea).text

            with destination_file.open(mode="w") as destination:
                destination.write(code)

            self.notify(
                message=f"Saved at {destination_file}",
                title="Success!",
                severity="information",
                timeout=5,
            )


class DestinationFile(Container):
    """Destination file input component."""

    def compose(self: Self) -> ComposeResult:
        yield Input(placeholder=PROMPT_OUTPUT, id="output-file")


class ForgeRow(Grid):
    """Row grid for forge."""


class OptionGroup(ScrollableContainer):
    pass


class Sidebar(Container):
    def compose(self: Self) -> ComposeResult:
        yield OptionGroup(Markdown(SIDEBAR_MSG))

    def on_markdown_link_clicked(self: Self, event: Markdown.LinkClicked) -> None:
        # Relevant discussion: https://github.com/Textualize/textual/discussions/3668
        webbrowser.open_new_tab(event.href)
