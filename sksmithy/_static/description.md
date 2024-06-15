# Description

Writing scikit-learn compatible estimators might be harder than expected.

While everyone knows about the `fit` and `predict`, there are other behaviours, methods and attributes that
scikit-learn might be expecting from your estimator depending on:

- The type of estimator you're writing.
- The signature of the estimator.
- The signature of the `.fit(...)` method.

Scikit-learn Smithy to the rescue: this tool aims to help you crafting your own estimator by asking a few
questions about it, and then generating the boilerplate code.

In this way you will be able to fully focus on the core implementation logic, and not on nitty-gritty details
of the scikit-learn API.

## Sanity check

Once the core logic is implemented, the estimator should be ready to test against the _somewhat official_
[`parametrize_with_checks`](https://scikit-learn.org/dev/modules/generated/sklearn.utils.estimator_checks.parametrize_with_checks.html#sklearn.utils.estimator_checks.parametrize_with_checks)
pytest compatible decorator.

## Official guide

Scikit-learn documentation on how to
[develop estimators](https://scikit-learn.org/dev/developers/develop.html#developing-scikit-learn-estimators).
