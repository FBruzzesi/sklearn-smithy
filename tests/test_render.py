from sksmithy._models import EstimatorType
from sksmithy._utils import render_template


def test_params(name: str, required: list[str], optional: list[str]) -> None:
    """Tests params (both required and optional) render as expected."""
    result = render_template(
        name=name,
        estimator_type=EstimatorType.ClassifierMixin,
        required=required,
        optional=optional,
        sample_weight=False,
        linear=False,
        predict_proba=False,
        decision_function=False,
        tags=None,
    )

    assert all(f"self.{p} = {p}" in result for p in [*required, *optional])
    assert ("self.n_iter_" in result) == ("max_iter" in [*required, *optional])

    assert ("_required_parameters = " in result) == bool(required)
    # Not able to make a better assert work because of how f-strings render outer and inner strings
    # Here is what I tested assert (f'_required_parameters = {[f"{r}" for r in required]}' in result) == bool(required)
    # but still renders as "_required_parameters = ['a', 'b']" which is not how it is in the file


def test_tags(name: str, tags: list[str] | None) -> None:
    """Tests tags render as expected."""
    result = render_template(
        name=name,
        estimator_type=EstimatorType.ClassifierMixin,
        required=[],
        optional=[],
        sample_weight=False,
        linear=False,
        predict_proba=False,
        decision_function=False,
        tags=tags,
    )

    assert ("def _more_tags(self)" in result) == bool(tags)

    if tags:
        for tag in tags:
            assert f'"{tag}": ...,' in result


def test_common_estimator(name: str, estimator: EstimatorType, sample_weight: bool) -> None:
    """Tests common features are present for all estimators. Includes testing for sample_weight"""
    result = render_template(
        name=name,
        estimator_type=estimator,
        required=[],
        optional=[],
        sample_weight=sample_weight,
        linear=False,
        predict_proba=False,
        decision_function=False,
        tags=None,
    )

    assert f"class {name}" in result
    assert "self.n_features_in_ = X.shape[1]" in result
    assert ("sample_weight = _check_sample_weight(sample_weight)" in result) == sample_weight

    match estimator:
        case EstimatorType.TransformerMixin:
            assert "X = check_array(X, ...)" in result
            assert ("def fit(self, X, y=None, sample_weight=None)" in result) == (sample_weight)
            assert ("def fit(self, X, y=None)" in result) == (not sample_weight)
        case _:
            assert "X, y = check_X_y(X, y, ...)" in result
            assert ("def fit(self, X, y, sample_weight=None)" in result) == (sample_weight)
            assert ("def fit(self, X, y)" in result) == (not sample_weight)


def test_classifier(name: str, linear: bool, predict_proba: bool, decision_function: bool) -> None:
    """Tests classifier specific rendering."""
    estimator_type = EstimatorType.ClassifierMixin

    result = render_template(
        name=name,
        estimator_type=estimator_type,
        required=[],
        optional=[],
        sample_weight=False,
        linear=linear,
        predict_proba=predict_proba,
        decision_function=decision_function,
        tags=None,
    )

    # Classifier specific
    assert "self.classes_ = " in result
    assert "def n_classes_(self)" in result
    assert "def transform(self, X)" not in result

    assert "def transform(self, X)" not in result

    # Linear
    assert ("class MightyEstimator(LinearClassifierMixin, BaseEstimator)" in result) == linear
    assert ("self.coef_ = ..." in result) == linear
    assert ("self.intercept_ = ..." in result) == linear

    assert ("class MightyEstimator(ClassifierMixin, BaseEstimator)" in result) == (not linear)
    assert ("def predict(self, X)" in result) == (not linear)

    # Predict proba
    assert ("def predict_proba(self, X)" in result) == predict_proba

    # Decision function
    assert ("def decision_function(self, X)" in result) == (decision_function and not linear)


def test_regressor(name: str, linear: bool) -> None:
    """Tests regressor specific rendering."""
    estimator_type = EstimatorType.RegressorMixin

    result = render_template(
        name=name,
        estimator_type=estimator_type,
        required=[],
        optional=[],
        sample_weight=False,
        linear=linear,
        predict_proba=False,
        decision_function=False,
        tags=None,
    )

    # Regressor specific
    assert "def transform(self, X)" not in result

    # Linear
    assert ("class MightyEstimator(RegressorMixin, LinearModel)" in result) == linear
    assert ("self.coef_ = ..." in result) == linear
    assert ("self.intercept_ = ..." in result) == linear

    assert ("class MightyEstimator(RegressorMixin, BaseEstimator)" in result) == (not linear)
    assert ("def predict(self, X)" in result) == (not linear)


def test_outlier(name: str, predict_proba: bool) -> None:
    """Tests outlier specific rendering."""
    estimator_type = EstimatorType.OutlierMixin

    result = render_template(
        name=name,
        estimator_type=estimator_type,
        required=[],
        optional=[],
        sample_weight=False,
        linear=False,
        predict_proba=predict_proba,
        decision_function=False,
        tags=None,
    )

    # Outlier specific
    assert "class MightyEstimator(OutlierMixin, BaseEstimator)" in result
    assert "self.offset_" in result
    assert "def score_samples(self, X)" in result
    assert "def decision_function(self, X)" in result
    assert "def predict(self, X)" in result

    assert "def transform(self, X)" not in result

    # Predict proba
    assert ("def predict_proba(self, X)" in result) == predict_proba


def test_transformer(name: str) -> None:
    """Tests transformer specific rendering."""
    estimator_type = EstimatorType.TransformerMixin

    result = render_template(
        name=name,
        estimator_type=estimator_type,
        required=[],
        optional=[],
        sample_weight=False,
        linear=False,
        predict_proba=False,
        decision_function=False,
        tags=None,
    )
    # Transformer specific
    assert "class MightyEstimator(TransformerMixin, BaseEstimator)" in result
    assert "def transform(self, X)" in result
    assert "def predict(self, X)" not in result


def test_cluster(name: str) -> None:
    """Tests cluster specific rendering."""
    estimator_type = EstimatorType.ClusterMixin

    result = render_template(
        name=name,
        estimator_type=estimator_type,
        required=[],
        optional=[],
        sample_weight=False,
        linear=False,
        predict_proba=False,
        decision_function=False,
        tags=None,
    )

    # Cluster specific
    assert "class MightyEstimator(ClusterMixin, BaseEstimator)" in result
    assert "self.labels_ = ..." in result
    assert "def predict(self, X)" in result
