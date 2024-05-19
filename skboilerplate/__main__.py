from jinja2 import Template
from typer import Typer, Option
from importlib import resources
from pathlib import Path

file_path: Path = resources.files("skboilerplate") / "template.py.jinja"  # type: ignore

with open(file_path, "r") as stream:
    template = Template(stream.read())


values = {
    "name": "RandomRegressor",
    "regressor": True,
    "classifier": True,
    "linear": True,
    "support_sample_weight": True,
    "required": ["k"],
    "parameters": ["k", "alpha", "beta", "max_iter"],
}

with open(f"xyz.py", "w") as destination:
    destination.write(template.render(values))
