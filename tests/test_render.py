import pytest

from sksmithy._models import EstimatorType
from sksmithy._utils import render_template


@pytest.mark.parametrize("estimator_type", list(EstimatorType))
@pytest.mark.parametrize("required", [["alpha", "beta"], []])
@pytest.mark.parametrize("optional", [["mu", "sigma"], []])
@pytest.mark.parametrize("sample_weight", [True, False])
@pytest.mark.parametrize("linear", [True, False])
@pytest.mark.parametrize("predict_proba", [True, False])
@pytest.mark.parametrize("decision_function", [True, False])
@pytest.mark.parametrize("tags", [["allow_nan", "binary_only"], [], None])
def test_render_template(
    estimator_type: EstimatorType,
    required: list[str],
    optional: list[str],
    sample_weight: bool,
    linear: bool,
    predict_proba: bool,
    decision_function: bool,
    tags: list[str] | None,
) -> None:
    if linear and estimator_type not in {EstimatorType.ClassifierMixin, EstimatorType.RegressorMixin}:
        pytest.skip()
    if predict_proba and estimator_type not in {EstimatorType.ClassifierMixin, EstimatorType.OutlierMixin}:
        pytest.skip()
    if decision_function and estimator_type not in {
        EstimatorType.ClassifierMixin,
    }:
        pytest.skip()

    result = render_template(
        name="MightyEstimator",
        estimator_type=estimator_type,
        required=required,
        optional=optional,
        linear=linear,
        sample_weight=sample_weight,
        predict_proba=predict_proba,
        decision_function=decision_function,
        tags=tags,
    )
    assert "class MightyEstimator" in result
    assert "self.n_features_in_ = X.shape[1]" in result

    match estimator_type:
        case EstimatorType.ClassifierMixin:
            assert "self.classes_ = " in result
            assert "def n_classes_(self)" in result

            if linear:
                assert "ClassifierMixin, BaseEstimator" not in result
                assert "LinearClassifierMixin, BaseEstimator" in result
                assert "def predict(self, X)" not in result
                assert "self.coef_ = ..." in result
                assert "self.intercept_ = ..." in result

            else:
                assert "ClassifierMixin, BaseEstimator" in result
                assert "LinearClassifierMixin, BaseEstimator" not in result
                assert "def predict(self, X)" in result
                assert "self.coef_ = ..." not in result
                assert "self.intercept_ = ..." not in result

            if predict_proba:
                assert "def predict_proba(self, X)" in result
            else:
                assert "def predict_proba(self, X)" not in result

            if decision_function:
                assert "def decision_function(self, X)" in result
            else:
                assert "def decision_function(self, X)" not in result

        case EstimatorType.RegressorMixin:
            if linear:
                assert "RegressorMixin, LinearModel" in result
                assert "RegressorMixin, BaseEstimator" not in result
                assert "def predict(self, X)" not in result
                assert "self.coef_ = ..." in result
                assert "self.intercept_ = ..." in result

            else:
                assert "RegressorMixin, LinearModel" not in result
                assert "RegressorMixin, BaseEstimator" in result
                assert "def predict(self, X)" in result
                assert "self.coef_ = ..." not in result
                assert "self.intercept_ = ..." not in result

        case EstimatorType.OutlierMixin:
            ...
        case EstimatorType.TransformerMixin:
            ...
        case EstimatorType.ClusterMixin:
            ...

    if sample_weight:
        assert "sample_weight = _check_sample_weight(sample_weight)" in result
        assert (
            "def fit(self, X, y, sample_weight=None)" in result
            or "def fit(self, X, y=None, sample_weight=None)" in result
        )

    if tags:
        assert "def _more_tags(self)" in result
