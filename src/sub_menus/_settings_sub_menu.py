from aminodorksfix.asyncfix import Client

from src.structs.strings import Strigns
from src.interfaces._sub_menu import ISubMenu
from src.ui._ui import UIManager

from src.utils._loader import (
    save_file,
    load_file
)
from src._constants import (
    CONFIG,
    THEMES,
    CONFIG_PATH,
    STRINGS_PATH
)


class SettingsSubMenu(ISubMenu):
    __slots__ = (
        "_ui",
        "_client"
    )

    def __init__(self, ui: UIManager, client: Client) -> None:
        super().__init__()
        self._ui = ui
        self._client = client

    def __change_api_key(self) -> None:
        self._client = self._ui.call_client(True)

    def __change_theme(self) -> None:
        CONFIG.theme = self._ui.call_choices(
            message=self._ui.strings.choices.select_theme,
            choices=self._ui.strings.themes
        )
        self._ui.theme = getattr(THEMES, CONFIG.theme)
        save_file(
            path=CONFIG_PATH,
            object=CONFIG
        )

    def __change_language(self) -> None:
        choice = self._ui.call_choices(
            message=self._ui.strings.choices.select_language,
            choices=self._ui.strings.languages
        )

        self._ui.strings = load_file(STRINGS_PATH.format(choice), Strigns)
        CONFIG.locale = choice
        save_file(
            path=CONFIG_PATH,
            object=CONFIG
        )

    async def call_sub_menu(self) -> None:
        match self._ui.call_choices(
            self._ui.strings.choices.select_menu,
            self._ui.strings.menus.settings
        ):
            case "change-api-key":
                self.__change_api_key()
            case "change-theme":
                self.__change_theme()
            case "change-language":
                self.__change_language()
            case _:
                pass
