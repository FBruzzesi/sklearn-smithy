from keyword import iskeyword

from typer import BadParameter

from sksmithy._logger import console
from sksmithy._models import TagType


def name_callback(name: str) -> str:
    """Validate if `name` is a valid python class name."""
    valid = name.isidentifier()
    kw = iskeyword(name)

    if not valid:
        msg = f"{name} is not a valid class name in python"
        raise BadParameter(msg)
    if kw:
        msg = f"{name} is a valid class name, but also a python keyword"
        console.print(msg, style="bad")

    return name


def args_callback(params: str) -> str:
    """Validate if `params` contains valid python names."""
    if params:
        param_list = params.split(",")
        invalid = tuple(p for p in param_list if not p.isidentifier())

        if len(invalid) > 0:
            msg = f"The following parameters are invalid python identifiers: {invalid}"
            raise BadParameter(msg)
    return params


def parse_tags(tags: str) -> list[str]:
    """Parse and validate `tags`."""
    if tags:
        list_tag = tags.split(",")
        unavailable_tags = tuple(t for t in list_tag if t not in TagType.__members__)

        if len(unavailable_tags):
            msg = (
                f"The following tags are not available: {unavailable_tags}."
                "\nPlease check the documentation at https://scikit-learn.org/dev/developers/develop.html#estimator-tags"
                " to know which values are avaiable."
            )
            raise BadParameter(msg)
        return list_tag
    return []
