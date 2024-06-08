import sys

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
    def compose(self: Self) -> ComposeResult:
        yield Prompt(PROMPT_NAME, classes="label")
        yield Input(placeholder="MightyEstimator", id="name", validators=[NameValidator()])


class Estimator(Container):
    def compose(self: Self) -> ComposeResult:
        yield Prompt(PROMPT_ESTIMATOR, classes="label")
        yield Select(
            options=((" ".join(x.capitalize() for x in e.value.split("-")), e.value) for e in EstimatorType),
            id="estimator",
        )


class Required(Container):
    def compose(self: Self) -> ComposeResult:
        yield Prompt(PROMPT_REQUIRED, classes="label")
        yield Input(placeholder="alpha,beta", id="required", validators=[ParamsValidator()])


class Optional(Container):
    def compose(self: Self) -> ComposeResult:
        yield Prompt(PROMPT_OPTIONAL, classes="label")
        yield Input(placeholder="mu,sigma", id="optional", validators=[ParamsValidator()])


class SampleWeight(Container):
    def compose(self: Self) -> ComposeResult:
        yield Horizontal(
            Prompt(PROMPT_SAMPLE_WEIGHT, classes="label"),
            Switch(id="sample_weight"),
            classes="container",
        )


class Linear(Container):
    def compose(self: Self) -> ComposeResult:
        yield Horizontal(
            Prompt(PROMPT_LINEAR, classes="label"),
            Switch(id="linear"),
            classes="container",
        )


class PredictProba(Container):
    def compose(self: Self) -> ComposeResult:
        yield Horizontal(
            Prompt(PROMPT_PREDICT_PROBA, classes="label"),
            Switch(id="predict_proba"),
            classes="container",
        )


class DecisionFunction(Container):
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
