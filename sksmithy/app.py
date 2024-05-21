# streamlit run sksmithy/app.py
import re
import time
from importlib.metadata import version

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
from sksmithy._utils import render_template

if (st_version := version("streamlit")) and tuple(int(re.sub(r"\D", "", str(v))) for v in st_version.split(".")) < (
    1,
    34,
    0,
):  # pragma: no cover
    msg = (
        f"streamlit>=1.34.0 is required for this module. Found version {st_version}.\nInstall it with "
        '`python -m pip install "streamlit>=1.34.0"` or `python -m pip install "sklearn-smithy[streamlit]"`',
    )
    raise ImportError(msg)

else:  # pragma: no cover
    import streamlit as st

st.set_page_config(
    page_title="Smithy",
    page_icon="⚒️",
    layout="wide",
    menu_items={
        "Get Help": "https://github.com/FBruzzesi/sklearn-smithy",
        "Report a bug": "https://github.com/FBruzzesi/sklearn-smithy/issues/new",
        # "About": "# This is a header. This is an *extremely* cool app!"
    },
)

st.title("Scikit-learn Smithy ⚒️")
st.markdown("## Forge your own scikit-learn compatible estimator")

with st.sidebar:
    st.markdown("""
        # Why ❓

        Writing a scikit-learn compatible estimators might be harder than expected.

        While everyone knows about the `fit` and `predict`, there are other behaviours, methods and attributes that
        scikit-learn might be expecting from your estimator. These depend on:

        - The type of estimator you're writing.
        - The signature of the estimator.
        - The signature of the `.fit(...)` method.

        This tool aims to help you with that by asking you a few questions about your estimator, and then generating the
        boilerplate code for you, so that you can focus on the core implementation of the estimator,
        and not on the nitty-gritty details of the scikit-learn API.

        Once the core logic is implemented, the estimator should be ready to test against the _somewhat official_
        [`parametrize_with_checks`](https://scikit-learn.org/dev/modules/generated/sklearn.utils.estimator_checks.parametrize_with_checks.html#sklearn.utils.estimator_checks.parametrize_with_checks)
        pytest compatible decorator.
    """)

estimator_type = None
sample_weights = False
linear = False
predict_proba = False
decision_function = False

with st.container():
    c11, c12 = st.columns(2)

    with c11:
        name = st.text_input(
            label=PROMPT_NAME,
            placeholder="MightyEstimator",
        )

        if name and not name.isidentifier():
            msg_invalid_name = f"`{name}` is not a valid python class name"
            st.error(msg_invalid_name)

    with c12:
        estimator = st.selectbox(
            label=PROMPT_ESTIMATOR,
            options=("classifier", "regressor", "outlier", "transformer"),
            format_func=lambda x: x.capitalize(),
            index=None,
        )

        if estimator:
            estimator_type = EstimatorType(estimator)

with st.container():
    c21, c22 = st.columns(2)

    with c21:
        required_params = st.text_input(label=PROMPT_REQUIRED, placeholder="alpha,beta")

        if required_params:
            required = required_params.split(",")
            invalid_required = tuple(p for p in required if not p.isidentifier())

            if len(invalid_required) > 0:
                msg_invalid_required = f"The following parameters are invalid python identifiers: {invalid_required}"
                st.error(msg_invalid_required)
        else:
            required = []

    with c22:
        optional_params = st.text_input(label=PROMPT_OPTIONAL, placeholder="mu,sigma")

        if optional_params:
            optional = optional_params.split(",")
            invalid_optional = tuple(p for p in optional if not p.isidentifier())

            if len(invalid_optional) > 0:
                msg_invalid_optional = f"The following parameters are invalid python identifiers: {invalid_optional}"
                st.error(msg_invalid_optional)
        else:
            optional = []


with st.container():
    c31, c32 = st.columns(2)

    with c31:
        sample_weight = st.toggle(PROMPT_SAMPLE_WEIGHT)
    with c32:
        linear = st.toggle(
            label=PROMPT_LINEAR,
            disabled=(estimator_type not in {EstimatorType.ClassifierMixin, EstimatorType.RegressorMixin}),
            help="Available only if estimator is `Classifier` or `Regressor`",
        )

with st.container():
    c41, c42 = st.columns(2)
    with c41:
        predict_proba = st.toggle(
            label=PROMPT_PREDICT_PROBA,
            disabled=(estimator_type not in {EstimatorType.ClassifierMixin, EstimatorType.OutlierMixin}),
            help="Available only if estimator is `Classifier` or `Outlier`",
        )
    with c42:
        decision_function = st.toggle(
            label=PROMPT_DECISION_FUNCTION,
            disabled=(estimator_type != EstimatorType.ClassifierMixin),
            help="Available only if estimator is `Classifier`",
        )

st.write("#")  # Empty space hack

with st.container():
    _, c52, _ = st.columns([2, 1, 2])

    with c52:
        forge_btn = (
            st.button(
                label="Time to forge 🛠️",
                type="primary",
                disabled=(name is None) or (estimator_type is None),
            )
            or False
        )

with st.container():
    if forge_btn:
        st.toast("Request submitted!")
        progress_text = "Forging in progress ..."
        progress_bar = st.progress(0, text=progress_text)
        # Consider using status component instead
        # https://docs.streamlit.io/develop/api-reference/status/st.status

        for percent_complete in range(100):
            time.sleep(0.002)
            progress_bar.progress(percent_complete + 1, text=progress_text)

        forged_template = render_template(
            name=name,
            estimator_type=estimator_type,
            required=required,
            optional=optional,
            linear=linear,
            sample_weight=sample_weight,
            predict_proba=predict_proba,
            decision_function=decision_function,
        )

        st.code(forged_template, language="python", line_numbers=True)

        time.sleep(1.0)
        progress_bar.empty()
