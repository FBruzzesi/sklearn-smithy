import sys
from collections.abc import Callable
from typing import ClassVar

from result import Err, Ok, Result
from textual.validation import ValidationResult, Validator

from sksmithy._parsers import name_parser, params_parser

if sys.version_info >= (3, 11):  # pragma: no cover
    from typing import Self
else:  # pragma: no cover
    from typing_extensions import Self


class _BaseValidator(Validator):
    parser: ClassVar[Callable[..., Result]]

    def validate(self: Self, value: str) -> ValidationResult:
        match self.parser(value):
            case Ok(_):
                return self.success()
            case Err(msg):
                return self.failure(msg)


class NameValidator(_BaseValidator):
    parser = name_parser


class ParamsValidator(_BaseValidator):
    parser = params_parser


# class DuplicateParamValidator(Validator):
#     def validate(self, value: str)  -> ValidationResult:
#         required = self.required_
#         optional = self.optional_
#         result = check_duplicates(required, optional)
#         return self.failure(result) if result else self.success()
