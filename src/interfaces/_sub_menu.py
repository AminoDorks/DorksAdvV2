from abc import (
    ABC,
    abstractmethod
)

from src.ui._ui import UIManager


class ISubMenu(ABC):
    _ui: UIManager

    @abstractmethod
    async def call_sub_menu(self) -> None:
        ...
