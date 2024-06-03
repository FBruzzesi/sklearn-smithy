<img src="https://raw.githubusercontent.com/FBruzzesi/sklearn-smithy/main/docs/img/sksmith-logo.svg" width=150 height=150 align="right">

# Scikit-learn Smithy

Scikit-learn smithy is a tool that helps you to forge scikit-learn compatible estimator templates with ease.

How can you use it?

- ✅ From a [web UI](https://sklearn-smithy.streamlit.app/) powered by [streamlit](https://streamlit.io/).
- ✅ As a CLI (command line interface): `smith forge` command (see [installation](#installation) and [commands](#available-cli-commands)).
- 🚧 As a TUI (terminal user interface): We are not there yet!

## Why ❓

Writing a scikit-learn compatible estimators might be harder than expected.

While everyone knows about the `fit` and `predict`, there are other behaviours, methods and attributes that
scikit-learn might be expecting from your estimator depending on:

- The type of estimator you're writing.
- The signature of the estimator.
- The signature of the `.fit(...)` method.

Scikit-learn Smithy to the rescue: this tool aims to help you crafting your own estimator by asking a few
questions about it, and then generating the boilerplate code.

In this way you will be able to fully focus on the core implementation logic, and not on nitty-gritty details
of the scikit-learn API.

Once the core logic is implemented, the estimator should be ready to test against the _somewhat official_ [`parametrize_with_checks`](https://scikit-learn.org/dev/modules/generated/sklearn.utils.estimator_checks.parametrize_with_checks.html#sklearn.utils.estimator_checks.parametrize_with_checks) pytest compatible decorator:

```py
from sklearn.utils.estimator_checks import parametrize_with_checks

@parametrize_with_checks([YourAwesomeRegressor, MoreAwesomeClassifier, EvenMoreAwesomeTransformer])
def test_sklearn_compatible_estimator(estimator, check):
    check(estimator)
```

## Installation

To use the tool from the terminal, we suggest to install it directly from pypi:

```bash
python -m pip install sklearn-smithy
```

This will make the `smith` command available in your terminal.

## Available CLI commands

The `smith` entrypoint offers two commands:

```bash
smith --help
```

```terminal
Usage: smith [OPTIONS] COMMAND [ARGS]...                                                                                                                          
                
Awesome CLI to generate scikit-learn estimator boilerplate code
...
╭─ Commands ─────────────────────────────────────────────────────────────────────────────╮
│ forge     Generate a new shiny scikit-learn compatible estimator ✨                    │
│ version   Display library version.                                                     │
╰────────────────────────────────────────────────────────────────────────────────────────╯
```

and as you can already guess, the `forge` command is the one that will generate the boilerplate code for you.

```bash
smith forge --help
```

```terminal
Generate a new shiny scikit-learn compatible estimator ✨

Depending on the estimator type the following additional information could be required:

* if the estimator is linear (classifier or regression)
* if the estimator has a `predict_proba` method (classifier or outlier detector)
* is the estimator has a `decision_function` method (classifier only)

Finally, the following two questions will be prompt:

* if the estimator should have tags (To know more about tags, check the dedicated scikit-learn documentation
    at https://scikit-learn.org/dev/developers/develop.html#estimator-tags
* in which file the class should be saved (default is `f'{name.lower()}.py'`)                                                                                                                                                    
                                                                                                                                                                                                                                                                     
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --name                                           TEXT                                                Name of the estimator [default: None] [required]                                              │
│ *  --estimator-type                                 [classifier|outlier|regressor|transformer|cluster]  Estimator type [default: None] [required]                                                     │
│    --required-params                                TEXT                                                List of (comma-separated) required parameters                                                 │
│    --optional-params                                TEXT                                                List of  (comma-separated) optional parameters                                                │
│    --sample-weight        --no-sample-weight                                                            Whether or not `.fit()` supports `sample_weight` [default: no-sample-weight]                  │
│    --linear               --no-linear                                                                   Whether or not the estimator is linear [default: no-linear]                                   │
│    --predict-proba        --no-predict-proba                                                            Whether or not the estimator implements `predict_proba` method [default: no-predict-proba]    │
│    --decision-function    --no-decision-function                                                        Whether or not the estimator implements `decision_function` method                            │
│                                                                                                         [default: no-decision-function]                                                               │
│    --tags                                           TEXT                                                List of optional extra scikit-learn tags                                                      │
│    --output-file                                    TEXT                                                Destination file where to save the boilerplate code                                           │
│    --help                                                                                               Show this message and exit.                                                                   │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Origin story

The idea for this tool originated from [scikit-lego #660](https://github.com/koaning/scikit-lego/pull/660), which I cannot better explain than quoting the PR description:

> So the story goes as the following:
>
> - The CI/CD fails for scikit-learn==1.5rc1 because of a change in the `check_estimator` internals
> - In the [scikit-learn issue](https://github.com/scikit-learn/scikit-learn/issues/28966) I got a better picture of how to run test for compatible components
> - In particular, in [rolling your own estimator](https://scikit-learn.org/dev/developers/develop.html#rolling-your-own-estimator) suggests to use [`parametrize_with_checks`](https://scikit-learn.org/dev/modules/generated/sklearn.utils.estimator_checks.parametrize_with_checks.html#sklearn.utils.estimator_checks.parametrize_with_checks), and of course I thought "that is a great idea to avoid dealing manually with each test"
> - Say no more, I enter a rabbit hole to refactor all our tests - which would be fine
> - Except that these tests failures helped me figure out a few missing parts in the codebase
