import sys
from importlib import metadata, resources
from typing import ClassVar

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Button, Collapsible, Footer, Header, Rule, Static, TextArea

from sksmithy.tui._components import (
    DecisionFunction,
    DestinationFile,
    Estimator,
    ForgeButton,
    ForgeRow,
    Linear,
    Name,
    Optional,
    PredictProba,
    Required,
    SampleWeight,
    SaveButton,
    Sidebar,
)

if sys.version_info >= (3, 11):  # pragma: no cover
    from typing import Self
else:  # pragma: no cover
    from typing_extensions import Self


class ForgeTUI(App):
    """Textual app to forge scikit-learn compatible estimators."""

    CSS_PATH: ClassVar[str] = str(resources.files("sksmithy") / "_static" / "tui.tcss")
    TITLE: ClassVar[str] = "Scikit-learn Smithy ⚒️"  # type: ignore[misc]

    BINDINGS: ClassVar = [
        ("ctrl+d", "toggle_sidebar", "Description"),
        ("L", "toggle_dark", "Light/Dark mode"),
        ("F", "forge", "Forge"),
        ("ctrl+s", "save", "Save"),
        ("E", "app.quit", "Exit"),
    ]

    show_sidebar = reactive(False)  # noqa: FBT003

    def on_mount(self: Self) -> None:
        """Compose on mount.

        Q: is this needed???
        """
        self.compose()

    def compose(self: Self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Container(
            Header(icon=f"v{metadata.version('sklearn-smithy')}"),
            ScrollableContainer(
                Horizontal(Name(), Estimator()),
                Horizontal(Required(), Optional()),
                Horizontal(SampleWeight(), Linear()),
                Horizontal(PredictProba(), DecisionFunction()),
                Rule(),
                ForgeRow(
                    Static(),
                    ForgeButton(),
                    SaveButton(),
                    DestinationFile(),
                ),
                Rule(),
                Collapsible(
                    TextArea(
                        text="",
                        language="python",
                        theme="vscode_dark",
                        show_line_numbers=True,
                        tab_behavior="indent",
                        id="code-area",
                    ),
                    title="Code Editor",
                    collapsed=True,
                    id="code-editor",
                ),
            ),
            Sidebar(classes="-hidden"),
            Footer(),
        )

    def action_toggle_dark(self: Self) -> None:  # pragma: no cover
        """Toggle dark mode."""
        self.dark = not self.dark

    def action_toggle_sidebar(self: Self) -> None:  # pragma: no cover
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
        forge_btn = self.query_one("#forge-btn", Button)
        forge_btn.press()

    def action_save(self: Self) -> None:
        """Press save button."""
        save_btn = self.query_one("#save-btn", Button)
        save_btn.press()


if __name__ == "__main__":  # pragma: no cover
    tui = ForgeTUI()
    tui.run()
