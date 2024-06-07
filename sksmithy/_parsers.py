from keyword import iskeyword

from result import Err, Ok, Result

from sksmithy._models import TagType


def name_parser(name: str | None) -> Result[str, str]:
    """Validate that `name` is a valid python class name.

    The parser returns `Err(...)` if:

    - `name` is not a valid python identifier
    - `name` is a python reserved keyword
    - `name` is empty

    Otherwise it returns `Ok(name)`.
    """
    if name:
        if not name.isidentifier():
            msg = f"`{name}` is not a valid python class name!"
            return Err(msg)
        if iskeyword(name):
            msg = f"`{name}` is a python reserved keyword!"
            return Err(msg)
        return Ok(name)
    msg = "Name cannot be empty!"
    return Err(msg)


def params_parser(params: str | None) -> Result[list[str], str]:
    """Parse and validate that `params` contains valid python names.

    The parser first splits params on commas to get a list of strings. Then it returns `Err(...)` if:

    - any element in the list is not a valid python identifier
    - any element is repeated more than once

    Otherwise it returns `Ok(params.split(","))`.
    """
    param_list: list[str] = params.split(",") if params else []
    invalid = tuple(p for p in param_list if not p.isidentifier())

    if len(invalid) > 0:
        msg = f"The following parameters are invalid python identifiers: {invalid}"
        return Err(msg)

    if len(set(param_list)) < len(param_list):
        msg = "Found repeated parameters!"
        return Err(msg)

    return Ok(param_list)


def check_duplicates(required: list[str], optional: list[str]) -> str | None:
    """Check that there are not duplicates between required and optional params."""
    duplicated_params = set(required).intersection(set(optional))
    return (
        f"The following parameters are duplicated between required and optional: {duplicated_params}"
        if duplicated_params
        else None
    )


def tags_parser(tags: str) -> Result[list[str], str]:
    """Parse and validate `tags` by comparing with sklearn list.

    The parser first splits tags on commas to get a list of strings. Then it returns `Err(...)` if any of the tag is not
    in the scikit-learn supported list.

    Otherwise it returns `Ok(tags.split(","))`
    """
    list_tag: list[str] = tags.split(",") if tags else []

    unavailable_tags = tuple(t for t in list_tag if t not in TagType.__members__)
    if len(unavailable_tags):
        msg = (
            f"The following tags are not available: {unavailable_tags}."
            "\nPlease check the official documentation at "
            "https://scikit-learn.org/dev/developers/develop.html#estimator-tags"
            " to know which values are available."
        )

        return Err(msg)

    return Ok(list_tag)
