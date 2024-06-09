import sys

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Input, Select, Static, Switch

from sksmithy._models import EstimatorType
from sksmithy._prompts import (
    PROMPT_DECISION_FUNCTION,
    PROMPT_ESTIMATOR,
    PROMPT_LINEAR,
    PROMPT_NAME,
    PROMPT_OPTIONAL,
    PROMPT_PREDICT_PROBA,
    PROMPT_REQUIRED,
    PROMPT_SAMPLE_WEIGHT,
)
from sksmithy.tui._validators import NameValidator, ParamsValidator

if sys.version_info >= (3, 11):  # pragma: no cover
    from typing import Self
else:  # pragma: no cover
    from typing_extensions import Self


class Prompt(Static):
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
            # TODO: Update filename component


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

    @on(Input.Changed, "#required")
    def on_input_change(self: Self, event: Input.Changed) -> None:
        if not event.validation_result.is_valid:
            self.notify(
                message="\n".join(event.validation_result.failure_descriptions),
                title="Invalid Parameter",
                severity="error",
                timeout=5,
            )

        # TODO: Add check for duplicates with optional


class Optional(Container):
    """Optional params input component."""

    def compose(self: Self) -> ComposeResult:
        yield Prompt(PROMPT_OPTIONAL, classes="label")
        yield Input(placeholder="mu,sigma", id="optional", validators=[ParamsValidator()])

    @on(Input.Changed, "#optional")
    def on_input_change(self: Self, event: Input.Changed) -> None:
        if not event.validation_result.is_valid:
            self.notify(
                message="\n".join(event.validation_result.failure_descriptions),
                title="Invalid Parameter",
                severity="error",
                timeout=5,
            )
        # TODO: Add check for duplicates with required


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
    def on_switch_changed(self, event: Switch.Changed) -> None:
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


# class Version(Static):
#     def render(self: Self) -> RenderableType:
#         return f"Version: [b]{version('sklearn-smithy')}"


# class Sidebar(Container):
#     def compose(self: Self) -> ComposeResult:
#         yield Title("Description")
#         yield Container(MarkdownViewer(SIDEBAR_MSG))
#         yield Version()
