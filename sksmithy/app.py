# streamlit run sksmithy/app.py

import re
from importlib.metadata import version

from sksmithy._models import EstimatorType
from sksmithy._prompts import PROMPT_ESTIMATOR, PROMPT_NAME, PROMPT_OPTIONAL, PROMPT_REQUIRED

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
    page_icon="🔨",
    layout="wide",
    menu_items={
        "Get Help": "https://github.com/FBruzzesi/sklearn-smithy",
        "Report a bug": "https://github.com/FBruzzesi/sklearn-smithy/issues/new",
        # "About": "# This is a header. This is an *extremely* cool app!"
    },
)

st.title("Scikit-learn Smithy 🔨")
st.markdown("## Forge your own scikit-learn compatible estimator")

with st.sidebar:
    st.markdown("""
        # Guide

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

    with c22:
        optional_params = st.text_input(label=PROMPT_OPTIONAL, placeholder="mu,sigma")

        if optional_params:
            optional = optional_params.split(",")
            invalid_optional = tuple(p for p in optional if not p.isidentifier())

            if len(invalid_optional) > 0:
                msg_invalid_optional = f"The following parameters are invalid python identifiers: {invalid_optional}"
                st.error(msg_invalid_optional)


with st.container():
    if estimator_type:
        match estimator_type:
            case EstimatorType.ClassifierMixin | EstimatorType.RegressorMixin:
                linear = ...  # PROMPT_LINEAR
            case _:
                linear = False

        # Check if supports predict_proba
        match estimator_type:
            case EstimatorType.ClassifierMixin | EstimatorType.OutlierMixin:
                predict_proba = ...  # PROMPT_PREDICT_PROBA
            case _:
                predict_proba = False

        # Check if supports decision_function
        match estimator_type:
            case EstimatorType.ClassifierMixin:
                decision_function = ...  # PROMPT_DECISION_FUNCTION
            case _:
                decision_function = False

# with st.container():
#     tags = typer.prompt(PROMPT_TAGS, default="")
#     tags = parse_tags(tags)
