import re
import time
from importlib import resources
from importlib.metadata import version

from result import Err, Ok

from sksmithy._models import EstimatorType
from sksmithy._parsers import check_duplicates, name_parser, params_parser
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
from sksmithy._utils import render_template

if (st_version := version("streamlit")) and tuple(int(re.sub(r"\D", "", str(v))) for v in st_version.split(".")) < (
    1,
    34,
    0,
):  # pragma: no cover
    st_import_err_msg = (
        f"streamlit>=1.34.0 is required for this module. Found version {st_version}.\nInstall it with "
        '`python -m pip install "streamlit>=1.34.0"` or `python -m pip install "sklearn-smithy[streamlit]"`'
    )
    raise ImportError(st_import_err_msg)

else:  # pragma: no cover
    import streamlit as st

SIDEBAR_MSG: str = (resources.files("sksmithy") / "_static" / "description.md").read_text()


def app() -> None:  # noqa: C901,PLR0912,PLR0915
    """Streamlit App."""
    st.set_page_config(
        page_title="Smithy",
        page_icon="⚒️",
        layout="wide",
        menu_items={
            "Get Help": "https://github.com/FBruzzesi/sklearn-smithy",
            "Report a bug": "https://github.com/FBruzzesi/sklearn-smithy/issues/new",
            "About": """
                Forge your own scikit-learn estimator!

                For more information, please visit the [sklearn-smithy](https://github.com/FBruzzesi/sklearn-smithy)
                repository.
                """,
        },
    )

    st.title("Scikit-learn Smithy ⚒️")
    st.markdown("## Forge your own scikit-learn compatible estimator")

    with st.sidebar:
        st.markdown(SIDEBAR_MSG)

    linear = False
    predict_proba = False
    decision_function = False
    estimator_type: EstimatorType | None = None

    required_is_valid = False
    optional_is_valid = False
    msg_duplicated_params: str | None = None

    if "forged_template" not in st.session_state:
        st.session_state["forged_template"] = ""

    if "forge_counter" not in st.session_state:
        st.session_state["forge_counter"] = 0

    with st.container():  # name and type
        c11, c12 = st.columns(2)

        with c11:  # name
            name_input = st.text_input(
                label=PROMPT_NAME,
                value="MightyEstimator",
                placeholder="MightyEstimator",
                help=(
                    "It should be a valid "
                    "[python identifier](https://docs.python.org/3/reference/lexical_analysis.html#identifiers)"
                ),
                key="name",
            )

            match name_parser(name_input):
                case Ok(name):
                    pass
                case Err(name_error_msg):
                    name = ""
                    st.error(name_error_msg)

        with c12:  # type
            estimator = st.selectbox(
                label=PROMPT_ESTIMATOR,
                options=tuple(e.value for e in EstimatorType),
                format_func=lambda v: " ".join(x.capitalize() for x in v.split("-")),
                index=None,
                key="estimator",
            )

            if estimator:
                estimator_type = EstimatorType(estimator)

    with st.container():  # params
        c21, c22 = st.columns(2)

        with c21:  # required
            required_params = st.text_input(
                label=PROMPT_REQUIRED,
                placeholder="alpha,beta",
                help=(
                    "It should be a sequence of comma-separated "
                    "[python identifiers](https://docs.python.org/3/reference/lexical_analysis.html#identifiers)"
                ),
                key="required",
            )

            match params_parser(required_params):
                case Ok(required):
                    required_is_valid = True
                case Err(required_err_msg):
                    required_is_valid = False
                    st.error(required_err_msg)

        with c22:  # optional
            optional_params = st.text_input(
                label=PROMPT_OPTIONAL,
                placeholder="mu,sigma",
                help=(
                    "It should be a sequence of comma-separated "
                    "[python identifiers](https://docs.python.org/3/reference/lexical_analysis.html#identifiers)"
                ),
                key="optional",
            )

            match params_parser(optional_params):
                case Ok(optional):
                    optional_is_valid = True
                case Err(optional_err_msg):
                    optional_is_valid = False
                    st.error(optional_err_msg)

        if required_is_valid and optional_is_valid and (msg_duplicated_params := check_duplicates(required, optional)):
            st.error(msg_duplicated_params)

    with st.container():  # sample_weight and linear
        c31, c32 = st.columns(2)

        with c31:  # sample_weight
            sample_weight = st.toggle(
                PROMPT_SAMPLE_WEIGHT,
                help="[sample_weight](https://scikit-learn.org/dev/glossary.html#term-sample_weight)",
                key="sample_weight",
            )
        with c32:  # linear
            linear = st.toggle(
                label=PROMPT_LINEAR,
                disabled=(estimator_type not in {EstimatorType.ClassifierMixin, EstimatorType.RegressorMixin}),
                help="Available only if estimator is `Classifier` or `Regressor`",
                key="linear",
            )

    with st.container():  # predict_proba and decision_function
        c41, c42 = st.columns(2)

        with c41:  # predict_proba
            predict_proba = st.toggle(
                label=PROMPT_PREDICT_PROBA,
                disabled=(estimator_type not in {EstimatorType.ClassifierMixin, EstimatorType.OutlierMixin}),
                help=(
                    "[predict_proba](https://scikit-learn.org/dev/glossary.html#term-predict_proba): "
                    "Available only if estimator is `Classifier` or `Outlier`. "
                ),
                key="predict_proba",
            )

        with c42:  # decision_function
            decision_function = st.toggle(
                label=PROMPT_DECISION_FUNCTION,
                disabled=(estimator_type != EstimatorType.ClassifierMixin) or linear,
                help=(
                    "[decision_function](https://scikit-learn.org/dev/glossary.html#term-decision_function): "
                    "Available only if estimator is `Classifier`"
                ),
                key="decision_function",
            )

    st.write("#")  # empty space hack

    with st.container():  # forge button
        _, c52, _, c54 = st.columns([2, 1, 1, 1])

        with c52:
            forge_btn = st.button(
                label="Time to forge 🛠️",
                type="primary",
                disabled=any(
                    [
                        not name,
                        not estimator_type,
                        not required_is_valid,
                        not optional_is_valid,
                        msg_duplicated_params,
                    ]
                ),
                key="forge_btn",
            )
            if forge_btn:
                st.session_state["forge_counter"] += 1
                st.session_state["forged_template"] = render_template(
                    name=name,
                    estimator_type=estimator_type,  # type: ignore[arg-type]  # At this point estimator_type is never None.
                    required=required,
                    optional=optional,
                    linear=linear,
                    sample_weight=sample_weight,
                    predict_proba=predict_proba,
                    decision_function=decision_function,
                )

        with c54, st.popover(label="Download", disabled=not st.session_state["forge_counter"]):
            if name:
                file_name = st.text_input(label="Select filename", value=f"{name.lower()}.py", key="file_name")

                data = st.session_state["forged_template"]
                st.download_button(
                    label="Confirm",
                    type="primary",
                    data=data,
                    file_name=file_name,
                    key="download_btn",
                )

    with st.container():  # code output
        if forge_btn:
            st.toast("Request submitted!")
            progress_text = "Forging in progress ..."
            progress_bar = st.progress(0, text=progress_text)
            # Consider using status component instead
            # https://docs.streamlit.io/develop/api-reference/status/st.status

            for percent_complete in range(100):
                time.sleep(0.002)
                progress_bar.progress(percent_complete + 1, text=progress_text)

            time.sleep(0.2)
            progress_bar.empty()

        if st.session_state["forge_counter"]:
            st.code(st.session_state["forged_template"], language="python", line_numbers=True)


if __name__ == "__main__":
    app()
