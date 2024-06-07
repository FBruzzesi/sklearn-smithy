# User Guide

As introduced in the [home page](index.md), **sklearn-smithy** is a tool that helps you to forge scikit-learn compatible estimator with ease, and it comes in three flavours.

Let's see how to use each one of them.

## Web UI 🌐

## CLI ⌨️

Once the library is installed, the `smith` CLI (Command Line Interface) will be available and that is the primary way to interact with the `smithy` package.

The CLI provides a main command called `forge`, which will prompt a series of question in the terminal, based on which it will generate the code for the estimator.

```bash
smith forge
```

TODO: Enter example GIF

!!! warning "Non-interactive mode"
    As any CLI, in principle it would be possible to run it in a non-interactive way, however this is not *fully* supported yet and it comes with some risks and limitations.

    The reason for this is that the validation and the parameters interaction happen while prompting the questions one after the other, meaning that the input to one prompt will follow next.

## TUI 💻

🚧 WIP
