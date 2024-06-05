import pytest
from result import Err, Ok, is_err, is_ok

from sksmithy._parsers import check_duplicates, name_parser, params_parser, tags_parser


@pytest.mark.parametrize(
    ("name", "checker"),
    [
        ("valid_name", is_ok),
        ("ValidName", is_ok),
        ("123Invalid", is_err),
        ("class", is_err),
        ("", is_err),
    ],
)
def test_name_parser(name: str, checker: callable) -> None:
    result = name_parser(name)
    assert checker(result)


@pytest.mark.parametrize(
    ("params", "checker", "expected"),
    [
        (None, is_ok, []),
        ("a,b,c", is_ok, ["a", "b", "c"]),
        ("123a,b c,x", is_err, "The following parameters are invalid python identifiers: ('123a', 'b c')"),
        ("a,a,b", is_err, "Found repeated parameters!"),
    ],
)
def test_params_parser(params: str, checker: callable, expected: str) -> None:
    result = params_parser(params)
    assert checker(result)

    match result:
        case Ok(value):
            assert value == expected
        case Err(msg):
            assert msg == expected


@pytest.mark.parametrize(
    ("required", "optional", "expected"),
    [
        (["a", "b"], ["c", "d"], None),
        ([], ["c", "d"], None),
        ([], [], None),
        (["a", "b"], ["b", "c"], "The following parameters are duplicated between required and optional: {'b'}"),
    ],
)
def test_check_duplicates(required: list[str], optional: list[str], expected: str) -> None:
    result = check_duplicates(required, optional)
    assert result == expected


@pytest.mark.parametrize(
    ("tags", "checker", "expected"),
    [
        ("allow_nan,binary_only", is_ok, ["allow_nan", "binary_only"]),
        ("", is_ok, []),
        ("some_madeup_tag", is_err, "The following tags are not available: ('some_madeup_tag',)"),
    ],
)
def test_tags_parser(tags: str, checker: callable, expected: str) -> None:
    result = tags_parser(tags)
    assert checker(result)
    match result:
        case Ok(value):
            assert value == expected
        case Err(msg):
            assert msg.startswith(expected)
