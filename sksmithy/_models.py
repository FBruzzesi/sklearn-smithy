from enum import Enum


class EstimatorType(str, Enum):
    """List of possible estimator types."""

    ClassifierMixin = "classifier"
    OutlierMixin = "outlier"
    RegressorMixin = "regressor"
    TransformerMixin = "transformer"
    ClusterMixin = "cluster"


class TagType(str, Enum):
    """List of extra tags.

    Description of each tag is available at https://scikit-learn.org/dev/developers/develop.html#estimator-tags.
    """

    allow_nan = "allow_nan"
    array_api_support = "array_api_support"
    binary_only = "binary_only"
    multilabel = "multilabel"
    multioutput = "multioutput"
    multioutput_only = "multioutput_only"
    no_validation = "no_validation"
    non_deterministic = "non_deterministic"
    pairwise = "pairwise"
    preserves_dtype = "preserves_dtype"
    poor_score = "poor_score"
    requires_fit = "requires_fit"
    requires_positive_X = "requires_positive_X"  # noqa: N815
    requires_y = "requires_y"
    requires_positive_y = "requires_positive_y"
    _skip_test = "_skip_test"
    _xfail_checks = "_xfail_checks"
    stateless = "stateless"
    X_types = "X_types"
