import pytest
from textual.widgets import Button, Input, Select, Switch

from sksmithy._models import EstimatorType
from sksmithy.tui import ForgeTUI


async def test_smoke(tui: ForgeTUI) -> None:
    """Basic smoke test."""
    async with tui.run_test() as pilot:
        await pilot.pause()
        assert pilot is not None


@pytest.mark.parametrize(
    ("name_", "err_msg"),
    [
        ("MightyEstimator", ""),
        ("not-valid-name", "`not-valid-name` is not a valid python class name!"),
        ("class", "`class` is a python reserved keyword!"),
    ],
)
async def test_name(tui: ForgeTUI, name_: str, err_msg: str) -> None:
    """Test `name` text_input component."""
    async with tui.run_test(size=None) as pilot:
        await pilot.pause()
        name_comp = tui.query_one("#name", Input)
        name_comp.value = name_

        await pilot.pause(0.01)

        assert (not name_comp.is_valid) == bool(err_msg)

        notifications = list(tui._notifications)  # noqa: SLF001
        assert len(notifications) == int(bool(err_msg))

        if notifications:
            assert notifications[0].message == err_msg


async def test_estimator_interaction(tui: ForgeTUI, estimator: EstimatorType) -> None:
    """Test that all toggle components interact correctly with the selected estimator."""
    async with tui.run_test(size=None) as pilot:
        await pilot.pause()
        tui.query_one("#estimator", Select).value = estimator.value
        await pilot.pause()

        assert (not tui.query_one("#linear", Switch).disabled) == (
            estimator in {EstimatorType.ClassifierMixin, EstimatorType.RegressorMixin}
        )
        assert (not tui.query_one("#predict_proba", Switch).disabled) == (
            estimator in {EstimatorType.ClassifierMixin, EstimatorType.OutlierMixin}
        )

        assert (not tui.query_one("#decision_function", Switch).disabled) == (
            estimator == EstimatorType.ClassifierMixin
        )

        if estimator == EstimatorType.ClassifierMixin:
            linear = tui.query_one("#linear", Switch)
            linear.value = True

            await pilot.pause()
            assert tui.query_one("#decision_function", Switch).disabled


@pytest.mark.parametrize(
    ("required_", "optional_", "err_msg"),
    [
        ("a,b", "c,d", ""),
        ("a,a", "", "Found repeated parameters!"),
        ("", "b,b", "Found repeated parameters!"),
        ("a-a", "", "The following parameters are invalid python identifiers: ('a-a',)"),
        ("", "b b", "The following parameters are invalid python identifiers: ('b b',)"),
        ("a,b", "a", "The following parameters are duplicated between required and optional: {'a'}"),
    ],
)
async def test_params(tui: ForgeTUI, required_: str, optional_: str, err_msg: str) -> None:
    """Test required and optional params interaction."""
    async with tui.run_test(size=None) as pilot:
        required_comp = tui.query_one("#required", Input)
        optional_comp = tui.query_one("#optional", Input)

        required_comp.value = required_
        optional_comp.value = optional_

        await required_comp.action_submit()
        await optional_comp.action_submit()
        await pilot.pause(0.01)

        notifications = list(tui._notifications)  # noqa: SLF001
        assert int(bool(notifications)) == int(bool(err_msg))

        if notifications:
            assert err_msg in "".join(n.message for n in notifications)


async def test_forge(tui: ForgeTUI, name: str, estimator: EstimatorType) -> None:
    """Test forge button and all of its interactions."""
    async with tui.run_test() as pilot:
        await pilot.pause()
        forge_btn = tui.query_one("#forge_btn", Button)
        forge_btn.action_press()
        await pilot.pause()

        notification = next(iter(tui._notifications))  # noqa: SLF001
        assert "Name cannot be empty!" in notification.message
        assert "Estimator cannot be empty!" in notification.message
        assert "Outfile file cannot be empty!" in notification.message

        name_comp = tui.query_one("#name", Input)
        estimator_comp = tui.query_one("#estimator", Select)

        name_comp.value = name
        estimator_comp.value = estimator.value

        forge_btn.action_press()

        await pilot.pause()

        notification = next(iter(tui._notifications))  # noqa: SLF001
        assert f"Template forged at {name.lower()}.py" in notification.message
