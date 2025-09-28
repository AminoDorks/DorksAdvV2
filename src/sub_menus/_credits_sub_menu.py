from src.interfaces._sub_menu import ISubMenu
from src.ui._ui import UIManager


class CreditsSubMenu(ISubMenu):
    __slots__ = ("_ui")

    def __init__(self, ui: UIManager) -> None:
        super().__init__()
        self._ui = ui

    async def call_sub_menu(self) -> None:
        self._ui.output_credits()
        self._ui.call_choices(
            self._ui.strings.choices.select_menu,
            self._ui.strings.menus.credits
        )
