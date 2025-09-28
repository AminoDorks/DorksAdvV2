from os import system

from src.ui._ui import UIManager
from src.sub_menus._promote_sub_menu import PromoteSubMenu
from src.sub_menus._accounts_sub_menu import AccountsSubMenu
from src.sub_menus._settings_sub_menu import SettingsSubMenu
from src.sub_menus._credits_sub_menu import CreditsSubMenu

from src._constants import (
    CONFIG,
    THEMES
)

__all__ = [
    "Bot"
]


class Bot:
    __slots__ = (
        "_client",
        "_sub_menus"
    )

    _ui: UIManager = UIManager(getattr(THEMES, CONFIG.theme))

    def __init__(self) -> None:
        self._client = self._ui.call_client()
        self._sub_menus = {
            "promote": PromoteSubMenu(self._ui, self._client),
            "accounts": AccountsSubMenu(self._ui, self._client),
            "settings": SettingsSubMenu(self._ui, self._client),
            "credits": CreditsSubMenu(self._ui)
        }

    async def run(self):
        while True:
            system("cls || clear")
            await self._sub_menus[self._ui.call_menu()].call_sub_menu()
