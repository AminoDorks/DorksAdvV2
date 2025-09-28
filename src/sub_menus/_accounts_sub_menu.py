from aminodorksfix.asyncfix import Client
from msgspec import convert
from InquirerPy.base.control import Choice
from asyncio import sleep

from src.structs.login_response import LoginResponse
from src.structs.cache import CachedAccount
from src.interfaces._sub_menu import ISubMenu
from src.ui._ui import UIManager
from src.utils._loader import save_file

from src._constants import (
    CACHE,
    CACHE_PATH,
    CONFIG
)


class AccountsSubMenu(ISubMenu):
    __slots__ = (
        "_ui"
        "_client"
    )

    def __init__(self, ui: UIManager, client: Client) -> None:
        super().__init__()
        self._ui = ui
        self._client = client

    async def __login_with_save(self, email: str, password: str) -> None:
        key = f"{email}-{password}"

        try:
            response = convert(
                await self._client.login(
                    email=email,
                    password=password
                ), type=LoginResponse
            )

            if CACHE.accounts.get(key):
                CACHE.accounts.pop(key)

            CACHE.accounts[key] = CachedAccount(
                device_id=str(self._client.device_id),
                session_id=response.session_id,
                email=email,
                password=password
            )

            save_file(
                path=CACHE_PATH,
                object=CACHE
            )
            self._ui.output_text(
                self._ui.strings.statuses.logged_in.format(email)
            )

        except Exception as e:
            self._ui.output_text(
                f"{self._ui.strings.errors.error_while_logging}: {e}"
            )
        finally:
            await sleep(CONFIG.promote_config.delay)

    async def __add_account(self) -> None:
        await self.__login_with_save(
            email=self._ui.call_input(self._ui.strings.inputs.input_email),
            password=self._ui.call_input(
                self._ui.strings.inputs.input_password
            )
        )

    def __delete_accounts(self) -> None:
        accounts = map(
            lambda account_key: Choice(
                value=account_key,
                name=" ".join(account_key.split("-"))
            ),
            list(CACHE.accounts.keys())
        )

        choices = self._ui.call_checkbox(
            self._ui.strings.choices.select_accounts,
            list(accounts)
        )

        for choice in choices:
            CACHE.accounts.pop(choice)

        save_file(
            path=CACHE_PATH,
            object=CACHE
        )

    async def __refresh_accounts(self) -> None:
        for account_key in list(CACHE.accounts.keys()):
            email, password = account_key.split("-")

            await self.__login_with_save(
                email=email,
                password=password
            )

    async def call_sub_menu(self) -> None:
        match self._ui.call_choices(
            self._ui.strings.choices.select_menu,
            self._ui.strings.menus.accounts
        ):
            case "add-account":
                await self.__add_account()
            case "delete-accounts":
                self.__delete_accounts()
            case "refresh-accounts":
                await self.__refresh_accounts()
