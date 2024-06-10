<img src="https://raw.githubusercontent.com/FBruzzesi/sklearn-smithy/main/docs/img/sksmith-logo.svg" width=150 height=150 align="right">

# Scikit-learn Smithy

Scikit-learn smithy is a tool that helps you to forge scikit-learn compatible estimator with ease.

How can you use it?

- [x] Directly from the browser via our [web UI](https://sklearn-smithy.streamlit.app/){:target="_blank"} ([more info](user-guide.md/#web-ui))
- [x] As a CLI (command line interface) in your terminal via the `smith forge` command ([more info](user-guide.md/#cli))
- [x] As a TUI (terminal user interface) in your terminal via the `smith-tui` command ([more info](user-guide.md/#tui))

!!! info
  
    All these tools will prompt a series of questions regarding the estimator you want to create, and then it will generate the boilerplate code for you.

## Supported estimators

The following types of scikit-learn estimator are supported:

- [x] Classifier
- [x] Regressor
- [x] Outlier Detector
- [x] Clusterer
- [x] Transformer
    - [x] Feature Selector
- [ ] Meta Estimator

## Origin story

The idea for this tool originated from [scikit-lego #660](https://github.com/koaning/scikit-lego/pull/660){:target="_blank"}, which I cannot better explain than quoting the PR description itself:

> So the story goes as the following:
>
> - The CI/CD fails for scikit-learn==1.5rc1 because of a change in the `check_estimator` internals
> - In the [scikit-learn issue](https://github.com/scikit-learn/scikit-learn/issues/28966){:target="_blank"} I got a better picture of how to run test for compatible components
> - In particular, [rolling your own estimator](https://scikit-learn.org/dev/developers/develop.html#rolling-your-own-estimator){:target="_blank"} suggests to use [`parametrize_with_checks`](https://scikit-learn.org/dev/modules/generated/sklearn.utils.estimator_checks.parametrize_with_checks.html#sklearn.utils.estimator_checks.parametrize_with_checks){:target="_blank"}, and of course I thought "that is a great idea to avoid dealing manually with each test"
> - Say no more, I enter a rabbit hole to refactor all our tests - which would be fine
> - Except that these tests failures helped me figure out a few missing parts in the codebase
