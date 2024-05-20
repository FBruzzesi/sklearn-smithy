from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({"good": "bold green", "bad": "bold red"})
console = Console(theme=custom_theme)
