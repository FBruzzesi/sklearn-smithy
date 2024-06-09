import pytest
from streamlit.testing.v1 import AppTest

from sksmithy._models import EstimatorType
from sksmithy.tui import ForgeTUI


@pytest.fixture(params=["MightyEstimator"])
def name(request: pytest.FixtureRequest) -> str:
    return request.param


@pytest.fixture(params=list(EstimatorType))
def estimator(request: pytest.FixtureRequest) -> EstimatorType:
    return request.param


@pytest.fixture(params=[["alpha", "beta"], ["max_iter"], []])
def required(request: pytest.FixtureRequest) -> list[str]:
    return request.param


@pytest.fixture(
    params=[
        ("a,a", "Found repeated parameters!"),
        ("a-a", "The following parameters are invalid python identifiers: ('a-a',)"),
    ]
)
def invalid_required(request: pytest.FixtureRequest) -> tuple[str, str]:
    return request.param


@pytest.fixture(
    params=[
        ("b,b", "Found repeated parameters!"),
        ("b b", "The following parameters are invalid python identifiers: ('b b',)"),
    ]
)
def invalid_optional(request: pytest.FixtureRequest) -> tuple[str, str]:
    return request.param


@pytest.fixture(params=[["mu", "sigma"], []])
def optional(request: pytest.FixtureRequest) -> list[str]:
    return request.param


@pytest.fixture(params=[True, False])
def sample_weight(request: pytest.FixtureRequest) -> bool:
    return request.param


@pytest.fixture(params=[True, False])
def linear(request: pytest.FixtureRequest) -> bool:
    return request.param


@pytest.fixture(params=[True, False])
def predict_proba(request: pytest.FixtureRequest) -> bool:
    return request.param


@pytest.fixture(params=[True, False])
def decision_function(request: pytest.FixtureRequest) -> bool:
    return request.param


@pytest.fixture(params=[["allow_nan", "binary_only"], [], None])
def tags(request: pytest.FixtureRequest) -> list[str] | None:
    return request.param


@pytest.fixture()
def app() -> AppTest:
    return AppTest.from_file("sksmithy/app.py", default_timeout=10)


@pytest.fixture()
def tui() -> ForgeTUI:
    return ForgeTUI()
