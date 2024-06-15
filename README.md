<img src="https://raw.githubusercontent.com/FBruzzesi/sklearn-smithy/main/docs/img/sksmith-logo.svg" width=150 height=150 align="right">

# Scikit-learn Smithy

Scikit-learn smithy is a tool that helps you to forge scikit-learn compatible estimator with ease.

---

[WebUI](https://sklearn-smithy.streamlit.app/) | [Documentation](https://fbruzzesi.github.io/sklearn-smithy) | [Repository](https://github.com/fbruzzesi/sklearn-smithy) | [Issue Tracker](https://github.com/fbruzzesi/sklearn-smithy/issues)

---

How can you use it?

<details><summary>✅ Directly from the browser via a Web UI. </summary>

- Available at [sklearn-smithy.streamlit.app](https://sklearn-smithy.streamlit.app/)
- It requires no installation.
- Powered by [streamlit](https://streamlit.io/)

<img src="https://raw.githubusercontent.com/FBruzzesi/sklearn-smithy/main/docs/img/webui.png" align="right">

</details>

<details><summary>✅ As a CLI (command line interface) in the terminal.</summary>

- Available via the `smith forge` command.
- It requires [installation](#installation): `python -m pip install sklearn-smithy`
- Powered by [typer](https://typer.tiangolo.com/).

<img src="https://raw.githubusercontent.com/FBruzzesi/sklearn-smithy/main/docs/img/cli.png" align="right">

</details>

<details><summary>✅ As a TUI (terminal user interface) in the terminal.</summary>

- Available via the `smith forge-tui` command.
- It requires installing [extra dependencies](#extra-dependencies): `python -m pip install "sklearn-smithy[textual]"`
- Powered by [textual](https://textual.textualize.io/).

<img src="https://raw.githubusercontent.com/FBruzzesi/sklearn-smithy/main/docs/img/tui.png" align="right">

</details>

All these tools will prompt a series of questions regarding the estimator you want to create, and then it will generate the boilerplate code for you.

## Why ❓

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

### Sanity check

Once the core logic is implemented, the estimator should be ready to test against the _somewhat official_
[`parametrize_with_checks`](https://scikit-learn.org/dev/modules/generated/sklearn.utils.estimator_checks.parametrize_with_checks.html#sklearn.utils.estimator_checks.parametrize_with_checks)
pytest compatible decorator:

```py
from sklearn.utils.estimator_checks import parametrize_with_checks

@parametrize_with_checks([
    YourAwesomeRegressor,
    MoreAwesomeClassifier,
    EvenMoreAwesomeTransformer,
])
def test_sklearn_compatible_estimator(estimator, check):
    check(estimator)
```

and it should be compatible with scikit-learn Pipeline, GridSearchCV, etc.

### Official guide

Scikit-learn documentation on how to
[develop estimators](https://scikit-learn.org/dev/developers/develop.html#developing-scikit-learn-estimators).

## Supported estimators

The following types of scikit-learn estimator are supported:

- ✅ Classifier
- ✅ Regressor
- ✅ Outlier Detector
- ✅ Clusterer
- ✅ Transformer
  - ✅ Feature Selector
- 🚧 Meta Estimator

## Installation

sklearn-smithy is available on [pypi](https://pypi.org/project/sklearn-smithy), so you can install it directly from there:

```bash
python -m pip install sklearn-smithy
```

**Remark:** The minimum Python version required is 3.10.

This will make the `smith` command available in your terminal, and you should be able to run the following:

```bash
smith version
```

> sklearn-smithy=...

### Extra dependencies

To run the TUI, you need to install the `textual` dependency as well:

```bash
python -m pip install "sklearn-smithy[textual]"
```

## User guide 📚

Please refer to the dedicated [user guide](https://fbruzzesi.github.io/sklearn-smithy/user-guide/) documentation section.

## Origin story

The idea for this tool originated from [scikit-lego #660](https://github.com/koaning/scikit-lego/pull/660), which I cannot better explain than quoting the PR description itself:

> So the story goes as the following:
>
> - The CI/CD fails for scikit-learn==1.5rc1 because of a change in the `check_estimator` internals
> - In the [scikit-learn issue](https://github.com/scikit-learn/scikit-learn/issues/28966) I got a better picture of how to run test for compatible components
> - In particular, [rolling your own estimator](https://scikit-learn.org/dev/developers/develop.html#rolling-your-own-estimator) suggests to use [`parametrize_with_checks`](https://scikit-learn.org/dev/modules/generated/sklearn.utils.estimator_checks.parametrize_with_checks.html#sklearn.utils.estimator_checks.parametrize_with_checks), and of course I thought "that is a great idea to avoid dealing manually with each test"
> - Say no more, I enter a rabbit hole to refactor all our tests - which would be fine
> - Except that these tests failures helped me figure out a few missing parts in the codebase
