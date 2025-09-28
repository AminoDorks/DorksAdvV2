# type: ignore
# lib forced to do this
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from InquirerPy.validator import PathValidator

from src.structs.themes import Theme

from typing import (
    List,
    Callable
)
from InquirerPy import (
    inquirer,
    get_style
)

__all__ = [
    "build_select"
]


def build_input(
        message: str,
        theme: Theme,
        validate: Callable = None,
        default: str = ""
) -> str:
    answer = inquirer.text(
        message=message,
        style=get_style(
            theme.inquirerStyle
        ),
        validate=validate,
        default=default
    ).execute()

    return answer


def build_select(
        message: str,
        choices: List[Choice],
        theme: Theme
) -> str:
    if not list(filter(lambda choice: isinstance(
        choice, Separator
    ), choices)) \
            and list(filter(lambda choice: choice.value == "main", choices)):
        if len(choices) > 1:
            choices.insert(0, Separator())
        choices.insert(-1, Separator())

    return inquirer.select(
        message=message,
        choices=choices,
        style=get_style(theme.inquirerStyle)
    ).execute()


def build_confirm(
        message: str,
        theme: Theme,
        default: bool = True
) -> bool:
    return inquirer.confirm(
        message=message,
        style=get_style(theme.inquirerStyle),
        default=default
    ).execute()


def build_path_input(
        message: str,
        theme: Theme,
        default: str = ""
):
    return inquirer.filepath(
        message=message,
        style=get_style(theme.inquirerStyle),
        only_files=True,
        validate=PathValidator(is_file=True, message="Input is not a file"),
        default=default
    ).execute()


def build_checkbox(
        message: str,
        theme: Theme,
        choices: List[Choice],
        validate: Callable = None
) -> List[str]:
    return inquirer.checkbox(
        message=message,
        choices=choices,
        style=get_style(theme.inquirerStyle),
        validate=validate
    ).execute()
