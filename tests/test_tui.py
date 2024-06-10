from pathlib import Path

import pytest
from textual.widgets import Button, Input, Select, Switch

from sksmithy._models import EstimatorType
from sksmithy.tui import ForgeTUI


async def test_smoke() -> None:
    """Basic smoke test."""
    app = ForgeTUI()
    async with app.run_test(size=None) as pilot:
        await pilot.pause()
        assert pilot is not None

        await pilot.pause()
        await pilot.exit(0)


@pytest.mark.parametrize(
    ("name_", "err_msg"),
    [
        ("MightyEstimator", ""),
        ("not-valid-name", "`not-valid-name` is not a valid python class name!"),
        ("class", "`class` is a python reserved keyword!"),
    ],
)
async def test_name(name_: str, err_msg: str) -> None:
    """Test `name` text_input component."""
    app = ForgeTUI()
    async with app.run_test(size=None) as pilot:
        name_comp = pilot.app.query_one("#name", Input)
        name_comp.value = name_
        await pilot.pause()

        assert (not name_comp.is_valid) == bool(err_msg)

        notifications = list(pilot.app._notifications)  # noqa: SLF001
        assert len(notifications) == int(bool(err_msg))

        if notifications:
            assert notifications[0].message == err_msg


async def test_estimator_interaction(estimator: EstimatorType) -> None:
    """Test that all toggle components interact correctly with the selected estimator."""
    app = ForgeTUI()
    async with app.run_test(size=None) as pilot:
        pilot.app.query_one("#estimator", Select).value = estimator.value
        await pilot.pause()

        assert (not pilot.app.query_one("#linear", Switch).disabled) == (
            estimator in {EstimatorType.ClassifierMixin, EstimatorType.RegressorMixin}
        )
        assert (not pilot.app.query_one("#predict_proba", Switch).disabled) == (
            estimator in {EstimatorType.ClassifierMixin, EstimatorType.OutlierMixin}
        )

        assert (not pilot.app.query_one("#decision_function", Switch).disabled) == (
            estimator == EstimatorType.ClassifierMixin
        )

        if estimator == EstimatorType.ClassifierMixin:
            linear = pilot.app.query_one("#linear", Switch)
            linear.value = True

            await pilot.pause()
            assert pilot.app.query_one("#decision_function", Switch).disabled


async def test_valid_params() -> None:
    """Test required and optional params interaction."""
    app = ForgeTUI()
    required_ = "a,b"
    optional_ = "c,d"
    async with app.run_test(size=None) as pilot:
        required_comp = pilot.app.query_one("#required", Input)
        optional_comp = pilot.app.query_one("#optional", Input)

        required_comp.value = required_
        optional_comp.value = optional_

        await required_comp.action_submit()
        await optional_comp.action_submit()
        await pilot.pause(0.01)

        notifications = list(pilot.app._notifications)  # noqa: SLF001
        assert not notifications


@pytest.mark.parametrize(("required_", "optional_"), [("a,b", "a"), ("a", "a,b")])
async def test_duplicated_params(required_: str, optional_: str) -> None:
    app = ForgeTUI()
    msg = "The following parameters are duplicated between required and optional: {'a'}"

    async with app.run_test(size=None) as pilot:
        required_comp = pilot.app.query_one("#required", Input)
        optional_comp = pilot.app.query_one("#optional", Input)

        required_comp.value = required_
        optional_comp.value = optional_

        await required_comp.action_submit()
        await optional_comp.action_submit()
        await pilot.pause()

        forge_btn = pilot.app.query_one("#forge-btn", Button)
        forge_btn.action_press()
        await pilot.pause()

        assert all(msg in n.message for n in pilot.app._notifications)  # noqa: SLF001


async def test_forge_raise() -> None:
    """Test forge button and all of its interactions."""
    app = ForgeTUI()
    async with app.run_test(size=None) as pilot:
        required_comp = pilot.app.query_one("#required", Input)
        optional_comp = pilot.app.query_one("#optional", Input)

        required_comp.value = "a,a"
        optional_comp.value = "b b"

        await required_comp.action_submit()
        await optional_comp.action_submit()
        await pilot.pause()

        forge_btn = pilot.app.query_one("#forge-btn", Button)
        forge_btn.action_press()
        await pilot.pause()

        m1, m2, m3 = (n.message for n in pilot.app._notifications)  # noqa: SLF001

        assert "Found repeated parameters!" in m1
        assert "The following parameters are invalid python identifiers: ('b b',)" in m2

        assert "Name cannot be empty!" in m3
        assert "Estimator cannot be empty!" in m3
        assert "Outfile file cannot be empty!" in m3
        assert "Found repeated parameters!" in m3
        assert "The following parameters are invalid python identifiers: ('b b',)" in m3


@pytest.mark.parametrize("use_binding", [True, False])
async def test_forge(tmp_path: Path, name: str, estimator: EstimatorType, use_binding: bool) -> None:
    """Test forge button and all of its interactions."""
    app = ForgeTUI()
    async with app.run_test(size=None) as pilot:
        name_comp = pilot.app.query_one("#name", Input)
        estimator_comp = pilot.app.query_one("#estimator", Select)
        await pilot.pause()

        output_file_comp = pilot.app.query_one("#output-file", Input)

        name_comp.value = name
        estimator_comp.value = estimator.value

        await pilot.pause()

        output_file = tmp_path / (f"{name.lower()}.py")
        output_file_comp.value = str(output_file)
        await output_file_comp.action_submit()
        await pilot.pause()

        if use_binding:
            await pilot.press("F")
        else:
            forge_btn = pilot.app.query_one("#forge-btn", Button)
            forge_btn.action_press()
        await pilot.pause()

        notification = next(iter(pilot.app._notifications))  # noqa: SLF001

        assert f"Template forged at {output_file!s}" in notification.message
        assert output_file.exists()
