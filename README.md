<img src="https://raw.githubusercontent.com/FBruzzesi/sklearn-smithy/main/docs/img/sksmith-logo.svg" width=150 height=150 align="right">

# Scikit-learn Smithy

A CLI to forge scikit-learn compatible estimator templates with ease.

## Why

Writing a scikit-learn compatible estimators might be harder than expected.

While everyone knows about the `fit` and `predict`, there are other behaviours, methods and attributes that scikit-learn might be expecting from your estimator. These depend on:

- The type of estimator you're writing.
- The signature of the estimator.
- The signature of the `.fit(...)` method.

This tool aims to help you with that by asking you a few questions about your estimator, and then generating the boilerplate code for you, so that you can focus on the core implementation of the estimator, and not on the nitty-gritty details of the scikit-learn API.

Once the core logic is implemented, the estimator should be ready to test against the _somewhat official_ [`parametrize_with_checks`](https://scikit-learn.org/dev/modules/generated/sklearn.utils.estimator_checks.parametrize_with_checks.html#sklearn.utils.estimator_checks.parametrize_with_checks) pytest compatible decorator:

```py
from sklearn.utils.estimator_checks import parametrize_with_checks

@parametrize_with_checks([YourAwesomeRegressor, MoreAwesomeClassifier, EvenMoreAwesomeTransformer])
def test_sklearn_compatible_estimator(estimator, check):
    check(estimator)
```

## Web UI

The tool made it into a [web ui](https://sklearn-smithy.streamlit.app/) powered by streamlit, so that there is no need to install anything locally to try it out.

## Installation

Suggested to install it directly from pypi:

```bash
python -m pip install sklearn-smithy
```

This will make the `smith` command available in your terminal.

## Commands

The `smith` entrypoint offers two commands:

```bash
smith --help
```

```terminal
Usage: smith [OPTIONS] COMMAND [ARGS]...                                                                                                                          
                
Awesome CLI to generate scikit-learn estimator boilerplate code
...
╭─ Commands ──────────────────────────────────────────────────────────────────────────────╮
│ forge     Asks a list of questions to generate a shiny new estimator ✨                │
│ version   Display library version.                                                      │
╰─────────────────────────────────────────────────────────────────────────────────────────╯
```

and as you can already guess, the `forge` command is the one that will generate the boilerplate code for you.

```bash
smith forge --help
```

```terminal
Asks a list of questions to generate a shiny new estimator ✨

Depending on the **estimator type** the additional information could be required:

* if the estimator is linear (classifier or regression)
* if the estimator has a `predict_proba` method (classifier or outlier detector)
* is the estimator has a `decision_function` method (classifier only)

Finally, the following two questions will be prompt:

* if the estimator should have tags (To know more about tags, check the dedicated
    [scikit-learn documentation](https://scikit-learn.org/dev/developers/develop.html#estimator-tags))
* in which file the class should be saved (default is `f'{name.lower()}.py'`)
                                                  
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --name                                                   TEXT                                        name the estimator. [default: None] [required]                                                │
│ *  --estimator-type                                         [classifier|outlier|regressor|transformer]  Estimator type. [default: None] [required]                                                    │
│    --required-params                                        TEXT                                        List of required parameters (comma-separated).                                                │
│    --other-params                                           TEXT                                        List of optional parameters (comma-separated).                                                │
│    --support-sample-weight    --no-support-sample-weight                                                Whether or not `.fit()` does support `sample_weight`. [default: no-support-sample-weight]     │
│    --help                                                                                               Show this message and exit.                                                                   │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Origin story

The idea for this tool originated from [scikit-lego #660](https://github.com/koaning/scikit-lego/pull/660):

> So the story goes as the following:
>
> - The CI/CD fails for scikit-learn==1.5rc1 because of a change in the `check_estimator` internals
> - In the [scikit-learn issue](https://github.com/scikit-learn/scikit-learn/issues/28966) I got a better picture of how to run test for compatible components
> - In particular, in [rolling your own estimator](https://scikit-learn.org/dev/developers/develop.html#rolling-your-own-estimator) suggests to use [`parametrize_with_checks`](https://scikit-learn.org/dev/modules/generated/sklearn.utils.estimator_checks.parametrize_with_checks.html#sklearn.utils.estimator_checks.parametrize_with_checks), and of course I thought "that is a great idea to avoid dealing manually with each test"
> - Say no more, I enter a rabbit hole to refactor all our tests - which would be fine
> - Except that these tests failures helped me figure out a few missing parts in the codebase
