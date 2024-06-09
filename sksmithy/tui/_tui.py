import sys
from importlib import resources
from typing import ClassVar

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Rule

from sksmithy.tui._components import (
    DecisionFunction,
    Estimator,
    Linear,
    Name,
    Optional,
    PredictProba,
    Required,
    SampleWeight,
    Sidebar,
    forge_row,
)

if sys.version_info >= (3, 11):  # pragma: no cover
    from typing import Self
else:  # pragma: no cover
    from typing_extensions import Self


class ForgeTUI(App):
    """Textual app to forge scikit-learn compatible estimators."""

    CSS_PATH: ClassVar[str] = str(resources.files("sksmithy") / "_static" / "tui.tcss")
    TITLE: ClassVar[str] = "Smithy Forge"  # type: ignore[misc]

    BINDINGS: ClassVar = [
        ("ctrl+d", "toggle_sidebar", "Description"),
        ("L", "toggle_dark", "Light/Dark mode"),
        ("F", "forge", "Forge"),
        ("E", "app.quit", "Exit"),
    ]

    show_sidebar = reactive(False)  # noqa: FBT003

    def compose(self: Self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Container(
            Header(icon="⚒️"),
            ScrollableContainer(
                Horizontal(Name(), Estimator()),
                Horizontal(Required(), Optional()),
                Horizontal(SampleWeight(), Linear()),
                Horizontal(PredictProba(), DecisionFunction()),
                Rule(),
                forge_row,
                Rule(),
            ),
            Sidebar(classes="-hidden"),
            Footer(),
        )

    def action_toggle_dark(self: Self) -> None:
        """Toggle dark mode."""
        self.dark = not self.dark

    def action_toggle_sidebar(self: Self) -> None:
        """Toggle sidebar component."""
        sidebar = self.query_one(Sidebar)
        self.set_focus(None)

        if sidebar.has_class("-hidden"):
            sidebar.remove_class("-hidden")
        else:
            if sidebar.query("*:focus"):
                self.screen.set_focus(None)
            sidebar.add_class("-hidden")

    def action_forge(self: Self) -> None:
        """Press forge button."""
        forge_btn = self.query_one("#forge_btn", Button)
        forge_btn.press()


if __name__ == "__main__":
    tui = ForgeTUI()
    tui.run()
