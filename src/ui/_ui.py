from base64 import b64decode
from aminodorksfix.asyncfix import Client
from InquirerPy.base.control import Choice

from src.structs.themes import Theme
from src.structs.strings import Strigns

from typing import (
    List,
    Callable
)

from src._constants import (
    CONFIG,
    STRINGS_PATH,
    CONFIG_PATH
)
from src.utils._loader import (
    load_file,
    save_file
)
from src.ui._inquirer import (
    build_input,
    build_select,
    build_path_input,
    build_confirm,
    build_checkbox
)

__all__ = [
    "UIManager"
]


class UIManager:
    __slots__ = (
        "_theme",
        "_strings"
    )

    def __init__(self, theme: Theme) -> None:
        self._theme = theme
        self._strings = load_file(STRINGS_PATH.format(CONFIG.locale), Strigns)

    @property
    def theme(self) -> Theme:
        return self._theme

    @theme.setter
    def theme(self, theme: Theme) -> None:
        self._theme = theme

    @property
    def strings(self) -> Strigns:
        return self._strings

    @strings.setter
    def strings(self, strings: Strigns) -> None:
        self._strings = strings

    def __colorize_text(self, text: str) -> str:
        return f"\033[0;{self.theme.ansiColor}{text}\033[0m"

    def __output_logo(self) -> None:
        print(f"{self.__colorize_text(b64decode(
            self.theme.logo
        ).decode("utf-8"))}\n")

    def output_credits(self):
        print(f"{self.__colorize_text(self.strings.other.credits)}")

    def output_text(self, text: str, elements: List[str] = None) -> None:
        if not elements:
            print(self.__colorize_text(text))
            return

        print(
            "".join(
                [f"{self.__colorize_text(
                    "["
                )}{element}{self.__colorize_text(
                    "]"
                )}" for element in elements]) + f": {self.__colorize_text(
                    text
                )}"
        )

    def call_client(
            self,
            is_rewrite: bool = False,
            device_id: str = None
    ) -> Client:
        if (not CONFIG.api_key) or is_rewrite:
            CONFIG.api_key = build_input(
                message=self.strings.inputs.input_api_key,
                theme=self.theme
            )
            save_file(
                path=CONFIG_PATH,
                object=CONFIG
            )

        return Client(
            api_key=CONFIG.api_key,
            socket_enabled=False,
            deviceId=device_id
        )

    def call_menu(self):
        self.__output_logo()
        select_answer = build_select(
            message=self.strings.choices.select_menu,
            choices=self.strings.menus.main,
            theme=self.theme
        )

        return select_answer

    def call_input(
            self,
            message: str,
            validate: Callable = None,
            default: str = ""
    ) -> str:
        input_answer = build_input(
            message=message,
            theme=self.theme,
            validate=validate,
            default=default
        )

        return input_answer

    def call_file(
            self,
            message: str,
            default: str = ""
    ) -> str:
        input_answer = build_path_input(
            message=message,
            theme=self.theme,
            default=default
        )

        return input_answer

    def call_confirm(self, message: str, default: bool = True) -> bool:
        input_answer = build_confirm(
            message=message,
            theme=self.theme,
            default=default
        )

        return input_answer

    def call_choices(self, message: str, choices: List[Choice]) -> str:
        select_answer = build_select(
            message=message,
            choices=choices,
            theme=self.theme
        )

        return select_answer

    def call_checkbox(
            self,
            message: str,
            choices: List[Choice],
            validate: Callable = None
    ) -> List[str]:
        return build_checkbox(
            message=message,
            theme=self.theme,
            choices=choices,
            validate=validate
        )
