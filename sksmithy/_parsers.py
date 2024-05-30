from keyword import iskeyword

from sksmithy._models import TagType


def name_parser(name: str | None) -> tuple[str, str]:
    """Validate that `name` is a valid python class name."""
    if name:
        is_valid = name.isidentifier()
        is_kw = iskeyword(name)

        msg = (
            f"`{name}` is not a valid python class name!"
            if not is_valid
            else f"`{name}` is a python reserved keyword!"
            if is_kw
            else ""
        )

        return name, msg
    return "", "Name cannot be empty!"


def params_parser(params: str | None) -> tuple[list[str], str]:
    """Parse and validate that `params` contains valid python names."""
    if params:
        param_list = params.split(",")
        invalid = tuple(p for p in param_list if not p.isidentifier())

        if len(invalid) > 0:
            msg = f"The following parameters are invalid python identifiers: {invalid}"
            return [], msg

        if len(set(param_list)) < len(param_list):
            msg = "Found repeated parameters!"
            return [], msg

        return param_list, ""
    return [], ""


def check_duplicates(required: list[str], optional: list[str]) -> str:
    """Check that there are not duplicates between required and optional params."""
    duplicated_params = set(required).intersection(set(optional))

    return f"The following parameters are duplicated: {duplicated_params}" if duplicated_params else ""


def tags_parser(tags: str) -> tuple[list[str], str]:
    """Parse and validate `tags` by comparing with sklearn list."""
    if tags:
        list_tag = tags.split(",")
        unavailable_tags = tuple(t for t in list_tag if t not in TagType.__members__)
        msg = (
            (
                f"The following tags are not available: {unavailable_tags}."
                "\nPlease check the documentation at https://scikit-learn.org/dev/developers/develop.html#estimator-tags"
                " to know which values are available."
            )
            if len(unavailable_tags)
            else ""
        )
        return list_tag, msg
    return [], ""
