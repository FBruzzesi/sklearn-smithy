import numpy as np

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils import check_X_y
from sklearn.utils.validation import check_is_fitted, check_array


class MightyEstimator(ClassifierMixin, BaseEstimator):
    """MightyEstimator estimator.

    ...
    """

    def fit(self, X, y):
        """
        Fit MightyEstimator estimator.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,) or (n_samples, n_targets)
            Target values.

        Returns
        -------
        self : MightyEstimator
            Fitted MightyEstimator estimator.
        """
        X, y = check_X_y(X, y, ...)  # TODO: Fill in `check_X_y` arguments

        self.n_features_in_ = X.shape[1]
        self.classes_ = np.unique(y)

        ...  # TODO: Implement fit logic

        return self

    def predict(self, X):
        """Predict X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The data to predict.

        Returns
        -------
        Prediction array.
        """

        check_is_fitted(self)
        X = check_array(X, ...)  # TODO: Fill in `check_array` arguments

        if X.shape[1] != self.n_features_in_:
            msg = f"X has {X.shape[1]} features but the estimator was fitted on {self.n_features_in_} features."
            raise ValueError(msg)

        y_pred = ...  # TODO: Implement predict logic

        return y_pred

    @property
    def n_classes_(self):
        """Number of classes."""
        return len(self.classes_)
