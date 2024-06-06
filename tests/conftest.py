import pytest

from sksmithy._models import EstimatorType


@pytest.fixture(params=["MightyEstimator"])
def name(request) -> str:
    return request.param


@pytest.fixture(params=list(EstimatorType))
def estimator(request) -> str:
    return request.param


@pytest.fixture(params=[["alpha", "beta"], ["max_iter"], []])
def required(request) -> list[str]:
    return request.param


@pytest.fixture(params=[["mu", "sigma"], []])
def optional(request) -> list[str]:
    return request.param


@pytest.fixture(params=[True, False])
def sample_weight(request) -> bool:
    return request.param


@pytest.fixture(params=[True, False])
def linear(request) -> bool:
    return request.param


@pytest.fixture(params=[True, False])
def predict_proba(request) -> bool:
    return request.param


@pytest.fixture(params=[True, False])
def decision_function(request) -> bool:
    return request.param


@pytest.fixture(params=[["allow_nan", "binary_only"], [], None])
def tags(request) -> list[str] | None:
    return request.param
