import sys
from collections.abc import Callable
from typing import ClassVar, TypeVar

from result import Err, Ok, Result
from textual.validation import ValidationResult, Validator

from sksmithy._parsers import name_parser, params_parser

if sys.version_info >= (3, 11):  # pragma: no cover
    from typing import Self
else:  # pragma: no cover
    from typing_extensions import Self

T = TypeVar("T")
R = TypeVar("R")


class _BaseValidator(Validator):
    parser: ClassVar[Callable[[T], Result[R, str]]]

    def validate(self: Self, value: str) -> ValidationResult:
        match self.parser(value):
            case Ok(_):
                return self.success()
            case Err(msg):
                return self.failure(msg)


class NameValidator(_BaseValidator):
    @staticmethod
    def parser(value: str) -> Result[str, str]:
        return name_parser(value)


class ParamsValidator(_BaseValidator):
    @staticmethod
    def parser(value: str) -> Result[list[str], str]:
        return params_parser(value)


# class DuplicateParamValidator(Validator):
#     def validate(self, value: str)  -> ValidationResult:
#         required = self.required_
#         optional = self.optional_
#         result = check_duplicates(required, optional)
#         return self.failure(result) if result else self.success()
