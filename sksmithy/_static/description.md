Writing scikit-learn compatible estimators might be harder than expected.

While everyone knows about the `fit` and `predict`, there are other behaviours, methods and attributes that scikit-learn might be expecting from your estimator depending on:

- The type of estimator you're writing.
- The signature of the estimator.
- The signature of the `.fit(...)` method.

Scikit-learn Smithy to the rescue: this tool aims to help you crafting your own estimator by asking a few questions about it, and then generating the boilerplate code.

In this way you will be able to fully focus on the core implementation logic, and not on nitty-gritty details of the
scikit-learn API.
