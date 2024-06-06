import pytest

from sksmithy._models import EstimatorType


@pytest.fixture(params=["MightyEstimator"])
def name(request: pytest.FixtureRequest) -> str:
    return request.param


@pytest.fixture(params=list(EstimatorType))
def estimator(request: pytest.FixtureRequest) -> EstimatorType:
    return request.param


@pytest.fixture(params=[["alpha", "beta"], ["max_iter"], []])
def required(request: pytest.FixtureRequest) -> list[str]:
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
