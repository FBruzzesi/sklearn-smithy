import nox
from nox.sessions import Session

nox.options.default_venv_backend = "uv"
nox.options.reuse_venv = True

PYTHON_VERSIONS = ["3.10", "3.11", "3.12"]


@nox.session(python=PYTHON_VERSIONS)  # type: ignore[misc]
@nox.parametrize("pre", [False, True])
def pytest_coverage(session: Session, pre: bool) -> None:
    """Run pytest coverage across different python versions."""
    pkg_install = [".[all]"]
    test_install = ["-r", "requirements/test.txt"]

    if pre:
        pkg_install.append("--pre")
        test_install.append("--pre")

    session.install(*pkg_install)
    session.install(*test_install)

    session.run("pytest", "tests", "--cov=sksmithy", "--cov=tests", "--cov-fail-under=90", "--numprocesses=auto")
