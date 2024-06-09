from sksmithy.tui._tui import ForgeTUI


def forge_tui() -> None:
    """Entrypoint function."""
    tui = ForgeTUI()
    tui.run()


if __name__ == "__main__":
    forge_tui()
