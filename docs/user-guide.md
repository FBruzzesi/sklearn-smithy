# User Guide 📚

As introduced in the [home page](index.md), **sklearn-smithy** is a tool that helps you to forge scikit-learn compatible estimator with ease, and it comes in three flavours.

Let's see how to use each one of them.

## Web UI 🌐

The web UI is available at [sklearn-smithy.streamlit.app](https://sklearn-smithy.streamlit.app/){:target="_blank"} allowing you to interact with the tool directly from your browser.

This option does not require any installation, and it is the most user-friendly way to use the tool if you have access to a browser or do not want to install anything on your machine.

## CLI ⌨️

Once the library is installed, the `smith` CLI (Command Line Interface) will be available and that is the primary way to interact with the `smithy` package.

The CLI provides a main command called `forge`, which will prompt a series of question in the terminal, based on which it will generate the code for the estimator.

!!! warning "Non-interactive mode"
    As any CLI, in principle it would be possible to run it in a non-interactive way, however this is not *fully* supported yet and it comes with some risks and limitations.

    The reason for this is that the validation and the parameters interaction happen while prompting the questions one after the other, meaning that the input to one prompt will follow next.

Let's see an example of how to use `smith forge` command:

<div class="termy">

```console
$ <font color="#4E9A06">smith</font> forge
# 🐍 How would you like to name the estimator?:$ MightyClassifier
# 🎯 Which kind of estimator is it? (classifier, outlier, regressor, transformer, cluster):$ classifier
# 📜 Please list the required parameters (comma-separated) []:$ alpha,beta
# 📑 Please list the optional parameters (comma-separated) []:$ mu,sigma
# 📶 Does the `.fit()` method support `sample_weight`? [y/N]:$ y
# 📏 Is the estimator linear? [y/N]:$ N
# 🎲 Should the estimator implement a `predict_proba` method? [y/N]:$ N
# ❓ Should the estimator implement a `decision_function` method? [y/N]:$ y
# 🧪 We are almost there... Is there any tag you want to add? (comma-separated) []:$ binary_only
# 📂 Where would you like to save the class? [mightyclassifier.py]:$ path/to/file.py
<span style="color: green; font-weight: bold;">Template forged at path/to/file.py </span>
```

</div>

Now the estimator template to be filled will be available at the specified path `path/to/file.py`.

<div class="termy">

```console
$ cat path/to/file.py
import numpy as np

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils import check_X_y
from sklearn.utils.validation import check_is_fitted, check_array
...
```

</div>

## TUI 💻

🚧 WIP
