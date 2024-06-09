import numpy as np

from sklearn.base import BaseEstimator
from sklearn.feature_selection import SelectorMixin
from sklearn.utils import check_X_y
from sklearn.utils.validation import check_is_fitted, check_array


class MightyEstimator(SelectorMixin, BaseEstimator):
    """MightyEstimator estimator.

    ...
    """

    def fit(self, X, y=None):
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
        X = check_array(X, ...)  # TODO: Fill in `check_array` arguments

        self.n_features_in_ = X.shape[1]

        ...  # TODO: Implement fit logic

        self.selected_features_ = ...  # TODO: Indexes of selected features
        self.support_ = np.isin(
            np.arange(0, self.n_features_in_),  # all_features
            self.selected_features_,
        )

        return self

    def _get_support_mask(self, X):
        """Get the boolean mask indicating which features are selected.

        Returns
        -------
        support : boolean array of shape [# input features]
            An element is True iff its corresponding feature is selected for retention.
        """

        check_is_fitted(self)
        return self.support_
