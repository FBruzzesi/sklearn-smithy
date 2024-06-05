from sksmithy._models import EstimatorType
from sksmithy._utils import render_template


def test_render_classifier(
    name: str,
    required: list[str],
    optional: list[str],
    sample_weight: bool,
    linear: bool,
    predict_proba: bool,
    decision_function: bool,
    tags: list[str] | None,
) -> None:
    estimator_type = EstimatorType.ClassifierMixin

    result = render_template(
        name=name,
        estimator_type=estimator_type,
        required=required,
        optional=optional,
        sample_weight=sample_weight,
        linear=linear,
        predict_proba=predict_proba,
        decision_function=decision_function,
        tags=tags,
    )
    # All
    assert "self.n_features_in_ = X.shape[1]" in result
    assert all(f"self.{p} = {p}" in result for p in [*required, *optional])

    assert ("self.n_iter_" in result) == ("max_iter" in [*required, *optional])
    assert "X, y = check_X_y(X, y, ...)" in result

    # Classifier specific
    assert "self.classes_ = " in result
    assert "def n_classes_(self)" in result
    assert "def transform(self, X)" not in result

    # Sample weight
    assert ("sample_weight = _check_sample_weight(sample_weight)" in result) == sample_weight
    assert ("def fit(self, X, y)" in result) == (not sample_weight)
    assert ("def fit(self, X, y, sample_weight=None)" in result) == (sample_weight)

    # Linear
    assert ("class MightyEstimator(LinearClassifierMixin, BaseEstimator)" in result) == linear
    assert ("self.coef_ = ..." in result) == linear
    assert ("self.intercept_ = ..." in result) == linear

    assert ("class MightyEstimator(ClassifierMixin, BaseEstimator)" not in result) == linear
    assert ("def predict(self, X)" not in result) == linear

    # Predict proba
    assert ("def predict_proba(self, X)" in result) == predict_proba

    # Decision function
    assert ("def decision_function(self, X)" in result) == (decision_function and not linear)

    # Tags
    assert ("def _more_tags(self)" in result) == bool(tags)


def test_render_regressor(
    name: str,
    required: list[str],
    optional: list[str],
    sample_weight: bool,
    linear: bool,
) -> None:
    estimator_type = EstimatorType.RegressorMixin

    result = render_template(
        name=name,
        estimator_type=estimator_type,
        required=required,
        optional=optional,
        sample_weight=sample_weight,
        linear=linear,
        predict_proba=False,
        decision_function=False,
        tags=None,
    )
    # All
    assert "self.n_features_in_ = X.shape[1]" in result
    assert all(f"self.{p} = {p}" in result for p in [*required, *optional])
    assert ("self.n_iter_" in result) == ("max_iter" in [*required, *optional])
    assert "X, y = check_X_y(X, y, ...)" in result

    # Regressor specific
    assert "def transform(self, X)" not in result

    # Sample weight
    assert ("sample_weight = _check_sample_weight(sample_weight)" in result) == sample_weight
    assert ("def fit(self, X, y)" in result) == (not sample_weight)
    assert ("def fit(self, X, y, sample_weight=None)" in result) == sample_weight

    # Linear
    assert ("class MightyEstimator(RegressorMixin, LinearModel)" in result) == linear
    assert ("self.coef_ = ..." in result) == linear
    assert ("self.intercept_ = ..." in result) == linear

    assert ("class MightyEstimator(RegressorMixin, BaseEstimator)" not in result) == linear
    assert ("def predict(self, X)" not in result) == linear


def test_render_outlier(
    name: str,
    required: list[str],
    optional: list[str],
    sample_weight: bool,
    predict_proba: bool,
) -> None:
    estimator_type = EstimatorType.OutlierMixin

    result = render_template(
        name=name,
        estimator_type=estimator_type,
        required=required,
        optional=optional,
        sample_weight=sample_weight,
        linear=False,
        predict_proba=predict_proba,
        decision_function=False,
        tags=None,
    )
    # All
    assert "self.n_features_in_ = X.shape[1]" in result
    assert all(f"self.{p} = {p}" in result for p in [*required, *optional])
    assert ("self.n_iter_" in result) == ("max_iter" in [*required, *optional])
    assert "X, y = check_X_y(X, y, ...)" in result

    # Outlier specific
    assert "class MightyEstimator(OutlierMixin, BaseEstimator)" in result
    assert "self.offset_" in result
    assert "def score_samples(self, X)" in result
    assert "def decision_function(self, X)" in result
    assert "def predict(self, X)" in result
    assert "def transform(self, X)" not in result

    # Sample weight
    assert ("sample_weight = _check_sample_weight(sample_weight)" in result) == sample_weight
    assert ("def fit(self, X, y)" in result) == (not sample_weight)
    assert ("def fit(self, X, y, sample_weight=None)" in result) == sample_weight

    # Predict proba
    assert ("def predict_proba(self, X)" in result) == predict_proba


def test_render_transformer(
    name: str,
    required: list[str],
    optional: list[str],
    sample_weight: bool,
) -> None:
    estimator_type = EstimatorType.TransformerMixin

    result = render_template(
        name=name,
        estimator_type=estimator_type,
        required=required,
        optional=optional,
        sample_weight=sample_weight,
        linear=False,
        predict_proba=False,
        decision_function=False,
        tags=None,
    )
    # All
    assert "self.n_features_in_ = X.shape[1]" in result
    assert all(f"self.{p} = {p}" in result for p in [*required, *optional])
    assert ("self.n_iter_" in result) == ("max_iter" in [*required, *optional])
    assert "X, y = check_X_y(X, y, ...)" not in result
    assert "X = check_array(X, ...)" in result

    # Transformer specific
    assert "class MightyEstimator(TransformerMixin, BaseEstimator)" in result
    assert "def transform(self, X)" in result
    assert "def predict(self, X)" not in result

    # Sample weight
    assert ("sample_weight = _check_sample_weight(sample_weight)" in result) == sample_weight
    assert ("def fit(self, X, y=None)" in result) == (not sample_weight)
    assert ("def fit(self, X, y=None, sample_weight=None)" in result) == (sample_weight)


def test_render_cluster(
    name: str,
    required: list[str],
    optional: list[str],
    sample_weight: bool,
) -> None:
    estimator_type = EstimatorType.ClusterMixin

    result = render_template(
        name=name,
        estimator_type=estimator_type,
        required=required,
        optional=optional,
        sample_weight=sample_weight,
        linear=False,
        predict_proba=False,
        decision_function=False,
        tags=None,
    )
    # All
    assert "self.n_features_in_ = X.shape[1]" in result
    assert all(f"self.{p} = {p}" in result for p in [*required, *optional])
    assert ("self.n_iter_ = ..." in result) == ("max_iter" in [*required, *optional])
    assert "X, y = check_X_y(X, y, ...)" in result

    # Cluster specific
    assert "class MightyEstimator(ClusterMixin, BaseEstimator)" in result
    assert "self.labels_ = ..." in result
    assert "def predict(self, X)" in result

    # Sample weight
    assert ("sample_weight = _check_sample_weight(sample_weight)" in result) == sample_weight
    assert ("def fit(self, X, y)" in result) == (not sample_weight)
    assert ("def fit(self, X, y, sample_weight=None)" in result) == (sample_weight)
