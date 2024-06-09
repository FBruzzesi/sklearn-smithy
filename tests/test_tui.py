import pytest

from textual.widgets import Input
from sksmithy.tui import ForgeTUI



async def test_smoke(tui: ForgeTUI) -> None:
    """Basic smoke test."""
    async with tui.run_test() as pilot:
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

    async with tui.run_test() as pilot:
        name = tui.query_one("#name", Input)
        name.value = name_

        # assert app.error[0].value == err_msg
        assert (not name.is_valid) == bool(err_msg)
        await pilot.pause()
        notifications = list(tui._notifications)
        assert len(notifications) == int(bool(err_msg))

        if notifications:
            assert notifications[0].message == err_msg

# def test_estimator_interaction(app: AppTest, estimator: EstimatorType) -> None:
#     """Test that all toggle components interact correctly with the selected estimator."""
#     app.run()
#     app.selectbox(key="estimator").select(estimator.value).run()

#     assert (not app.toggle(key="linear").disabled) == (
#         estimator in {EstimatorType.ClassifierMixin, EstimatorType.RegressorMixin}
#     )
#     assert (not app.toggle(key="predict_proba").disabled) == (
#         estimator in {EstimatorType.ClassifierMixin, EstimatorType.OutlierMixin}
#     )
#     assert (not app.toggle(key="decision_function").disabled) == (estimator == EstimatorType.ClassifierMixin)

#     if estimator == EstimatorType.ClassifierMixin:
#         app.toggle(key="linear").set_value(True).run()

#         assert app.toggle(key="decision_function").disabled


# @pytest.mark.parametrize(
#     ("required_", "optional_", "err_msg"),
#     [
#         ("a,b", "c,d", ""),
#         ("a,a", "", "Found repeated parameters!"),
#         ("", "b,b", "Found repeated parameters!"),
#         ("a-a", "", "The following parameters are invalid python identifiers: ('a-a',)"),
#         ("", "b b", "The following parameters are invalid python identifiers: ('b b',)"),
#         ("a,b", "a", "The following parameters are duplicated between required and optional: {'a'}"),
#     ],
# )
# def test_params(
#     app: AppTest, name: str, estimator: EstimatorType, required_: str, optional_: str, err_msg: str
# ) -> None:
#     """Test required and optional params interaction."""
#     app.run()
#     app.text_input(key="name").input(name).run()
#     app.selectbox(key="estimator").select(estimator.value).run()

#     app.text_input(key="required").input(required_).run()
#     app.text_input(key="optional").input(optional_).run()

#     if err_msg:
#         assert app.error[0].value == err_msg
#         # Forge button gets disabled if any error happen
#         assert app.button(key="forge_btn").disabled
#     else:
#         assert not app.error
#         assert not app.button(key="forge_btn").disabled


# def test_forge(app: AppTest, name: str, estimator: EstimatorType) -> None:
#     """Test forge button and all of its interactions.

#     Remark that there is no way of testing `popover` or `download_button` components (yet).
#     """
#     app.run()
#     assert app.button(key="forge_btn").disabled
#     assert app.session_state["forge_counter"] == 0

#     app.text_input(key="name").input(name).run()
#     app.selectbox(key="estimator").select(estimator.value).run()
#     assert not app.button(key="forge_btn").disabled
#     assert not app.code

#     app.button(key="forge_btn").click().run()
#     assert app.session_state["forge_counter"] == 1
#     assert app.code is not None
