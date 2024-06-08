import sys
from typing import ClassVar

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Input, Rule

from sksmithy.tui._components import (
    DecisionFunction,
    Estimator,
    Linear,
    Name,
    Optional,
    PredictProba,
    Required,
    SampleWeight,
)

if sys.version_info >= (3, 11):  # pragma: no cover
    from typing import Self
else:  # pragma: no cover
    from typing_extensions import Self

SIDEBAR_MSG: str = """
Writing scikit-learn compatible estimators might be harder than expected.

While everyone knows about the `fit` and `predict`, there are other behaviours, methods and attributes that scikit-learn might be expecting from your estimator depending on:

- The type of estimator you're writing.
- The signature of the estimator.
- The signature of the `.fit(...)` method.

Scikit-learn Smithy to the rescue: this tool aims to help you crafting your own estimator by asking a few questions about it, and then generating the boilerplate code.

In this way you will be able to fully focus on the core implementation logic, and not on nitty-gritty details of the scikit-learn API.
"""


class TUI(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH: ClassVar[str] = "../_static/tui.tcss"
    TITLE: ClassVar[str] = "Smithy Forge"

    BINDINGS: ClassVar[list[tuple[str, str, str]]] = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("ctrl+s", "toggle_sidebar", "Sidebar"),
    ]

    show_sidebar = reactive(False)

    def compose(self: Self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(icon="⚒️")
        yield ScrollableContainer(
            Horizontal(Name(), Estimator()),
            Horizontal(Required(), Optional()),
            Horizontal(SampleWeight(), Linear()),
            Horizontal(PredictProba(), DecisionFunction()),
            Rule(),
            Button(),
        )
        # yield Sidebar(classes="-hidden")
        yield Footer()

    def action_toggle_dark(self: Self) -> None:
        """Toggle dark mode."""
        self.dark = not self.dark

    # def action_toggle_sidebar(self) -> None:
    #     sidebar = self.query_one(Sidebar)
    #     self.set_focus(None)
    #     if sidebar.has_class("-hidden"):
    #         sidebar.remove_class("-hidden")
    #     else:
    #         if sidebar.query("*:focus"):
    #             self.screen.set_focus(None)
    #         sidebar.add_class("-hidden")

    @on(Input.Changed, "#name")
    def show_invalid_name(self: Self, event: Input.Changed) -> None:
        if not event.validation_result.is_valid:
            self.name_ = None
            self.notify(
                message=event.validation_result.failure_descriptions[0],
                title="Invalid Name",
                severity="error",
                timeout=5,
            )
        else:
            self.name_ = event.value

    @on(Input.Changed, "#required,#optional")
    def show_invalid_required(self: Self, event: Input.Changed) -> None:
        if not event.validation_result.is_valid:
            if event.input.id == "required":
                self.required_ = None
            else:
                self.optional_ = None

            self.notify(
                message="\n".join(event.validation_result.failure_descriptions),
                title="Invalid Parameter",
                severity="error",
                timeout=5,
            )
        elif event.input.id == "required":
            self.required_ = event.value.split(",")
        else:
            self.optional_ = event.value.split(",")


if __name__ == "__main__":
    tui = TUI()
    tui.run()
