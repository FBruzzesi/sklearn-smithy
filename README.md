# Scikit learn smithy

CLI to forge scikit-learn compatible estimators with ease.

## Why

Writing a scikit-learn compatible estimator is a bit of a hassle. You need to write a lot of boilerplate code to get started. This tool aims to help you with that.

Not only that, but scikit-learn expects certain behaviours, methods and attributes from your estimator depending on:

- The type of estimator you're writing.
- The signature of the estimator.
- The signature of the `.fit(...)` method.

This tool will generate the boilerplate code for you, so you can focus on the implementation logic of your estimator, and not on the nitty-gritty details of the scikit-learn API.

## Example

TODO

## Installation

TODO

## Origin story

The idea for this tool originated from [scikit-lego #660](https://github.com/koaning/scikit-lego/pull/660):

> So the story goes as the following:
>
> - The CI/CD fails for scikit-learn==1.5rc1 because of a change in the `check_estimator` internals
> - In the [scikit-learn issue](https://github.com/scikit-learn/scikit-learn/issues/28966) I got a better picture of how to run test for compatible components
> - In particular, in [rolling your own estimator](https://scikit-learn.org/dev/developers/develop.html#rolling-your-own-estimator) suggests to use [`parametrize_with_checks`](https://scikit-learn.org/dev/modules/generated/sklearn.utils.estimator_checks.parametrize_with_checks.html#sklearn.utils.estimator_checks.parametrize_with_checks), and of course I thought "that is a great idea to avoid dealing manually with each test"
> - Say no more, I enter a rabbit hole to refactor all our tests - which would be fine
> - Except that these tests failures helped me figure out a few missing parts in the codebase
