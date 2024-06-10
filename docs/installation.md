# Installation ✨

sklearn-smithy is available on [pypi](https://pypi.org/project/sklearn-smithy){:target="_blank"}, so you can install it directly from there:

```bash
python -m pip install sklearn-smithy
```

!!! warning
    The minimum Python version required is 3.10.

This will make the `smith` command available in your terminal, and you should be able to run the following:

```bash
smith version
```

> sklearn-smithy=...

## Extra dependencies

To run the TUI, you need to install the `textual` dependency as well:

```bash
python -m pip install "sklearn-smithy[textual]"
```

## Other installation methods

=== "pip + source/git"

    ```bash
    python -m pip install git+https://github.com/FBruzzesi/sklearn-smithy.git
    ```

=== "local clone"

    ```bash
    git clone https://github.com/FBruzzesi/sklearn-smithy.git
    cd sklearn-smithy
    python -m pip install .
    ```
