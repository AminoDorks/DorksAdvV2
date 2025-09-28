from aminodorksfix.asyncfix import Client

from src.interfaces._sub_menu import ISubMenu
from src.ui._ui import UIManager
from src.utils._promoter import Promoter
from src._constants import CONFIG
from src.utils._loader import save_file

from src.structs.config import (
    ProfileConfig,
    ThreadConfig
)
from src._constants import (
    API_MAX_LEVEL,
    API_MIN_LEVEL,
    CONFIG_PATH
)


class PromoteSubMenu(ISubMenu):
    __slots__ = (
        "_ui",
        "_client"
    )

    def __init__(self, ui: UIManager, client: Client) -> None:
        super().__init__()
        self._ui = ui
        self._client = client

    async def __promote_start(self) -> None:
        await Promoter(
            client=self._client,
            ui=self._ui
        ).start()

    def __promote_types(self) -> None:
        CONFIG.promote_config = CONFIG.promote_config.copy(
            promote_type=self._ui.call_choices(
                message=self._ui.strings.choices.select_promote_type,
                choices=self._ui.strings.promote_types
            )
        )
        save_file(
            path=CONFIG_PATH,
            object=CONFIG
        )

    def __edit_promoted_users(self) -> None:
        CONFIG.promote_config = CONFIG.promote_config.copy(
            min_level=int(
                self._ui.call_input(
                    message=self._ui.strings.inputs.input_min_level,
                    validate=lambda x: (
                        x.isdigit() and int(
                            x
                        ) <= CONFIG.promote_config.max_level and int(
                            x
                        ) > API_MIN_LEVEL
                    ),
                    default=str(CONFIG.promote_config.min_level)
                )
            )
        )

        CONFIG.promote_config = CONFIG.promote_config.copy(
            max_level=int(
                self._ui.call_input(
                    message=self._ui.strings.inputs.input_max_level,
                    validate=lambda x: (
                        x.isdigit() and int(
                            x
                        ) >= CONFIG.promote_config.min_level and int(
                            x
                        ) < API_MAX_LEVEL
                    ),
                    default=str(CONFIG.promote_config.max_level)
                )
            ),
            min_users_per_thread=int(
                self._ui.call_input(
                    message=self._ui.strings.inputs.input_min_users_per_thread,
                    validate=lambda x: x.isdigit() and int(x) > 0 and int(
                        x
                    ) < 100,
                    default=str(CONFIG.promote_config.min_users_per_thread)
                )
            ),
            max_users_per_community=int(
                self._ui.call_input(
                    message=(
                        self._ui.strings.inputs.input_max_users_per_community
                    ),
                    validate=lambda x: x.isdigit() and int(
                        x
                    ) >= 100,
                    default=str(CONFIG.promote_config.max_users_per_community)
                )
            )
        )
        save_file(
            path=CONFIG_PATH,
            object=CONFIG
        )

    def __edit_profile(self) -> None:
        profile_config = ProfileConfig(
            nickname=self._ui.call_input(
                message=self._ui.strings.inputs.input_profile_nickname,
                default=CONFIG.promote_config.profile_config.nickname or ""
            ),
            about=self._ui.call_input(
                message=self._ui.strings.inputs.input_profile_about,
                default=CONFIG.promote_config.profile_config.about or ""
            ),
            icon=self._ui.call_file(
                message=self._ui.strings.inputs.input_profile_icon,
                default=CONFIG.promote_config.profile_config.icon
            ),
            use_antiban=self._ui.call_confirm(
                message=self._ui.strings.inputs.input_use_antiban,
                default=CONFIG.promote_config.profile_config.use_antiban
            )
        )

        CONFIG.promote_config = CONFIG.promote_config.copy(
            profile_config=profile_config
        )
        save_file(
            path=CONFIG_PATH,
            object=CONFIG
        )

    def __edit_thread(self) -> None:
        thread_config = ThreadConfig(
            title=self._ui.call_input(
                message=self._ui.strings.inputs.input_thread_title,
                default=CONFIG.promote_config.thread_config.title or ""
            ),
            description=self._ui.call_input(
                message=self._ui.strings.inputs.input_thread_description,
                default=CONFIG.promote_config.thread_config.description or ""
            ),
            announcement=self._ui.call_input(
                message=self._ui.strings.inputs.input_thread_announcement,
                default=CONFIG.promote_config.thread_config.announcement or ""
            ),
            thumbnail=self._ui.call_file(
                message=self._ui.strings.inputs.input_thread_thumbnail,
                default=CONFIG.promote_config.thread_config.thumbnail
            ),
            background=self._ui.call_file(
                message=self._ui.strings.inputs.input_thread_background,
                default=CONFIG.promote_config.thread_config.background
            )
        )

        CONFIG.promote_config = CONFIG.promote_config.copy(
            thread_config=thread_config
        )
        save_file(
            path=CONFIG_PATH,
            object=CONFIG
        )

    def __edit_delay(self) -> None:
        CONFIG.promote_config = CONFIG.promote_config.copy(
            delay=int(
                self._ui.call_input(
                    message=self._ui.strings.inputs.input_delay,
                    validate=lambda x: x.isdigit() and int(x) > 0,
                    default=str(CONFIG.promote_config.delay)
                )
            )
        )
        save_file(
            path=CONFIG_PATH,
            object=CONFIG
        )

    def __edit_workers(self) -> None:
        CONFIG.promote_config = CONFIG.promote_config.copy(
            workers=int(
                self._ui.call_input(
                    message=self._ui.strings.inputs.input_workers,
                    validate=lambda x: x.isdigit() and int(x) > 0,
                    default=str(CONFIG.promote_config.workers)
                )
            )
        )
        save_file(
            path=CONFIG_PATH,
            object=CONFIG
        )

    async def call_sub_menu(self) -> None:
        match self._ui.call_choices(
            self._ui.strings.choices.select_menu,
            self._ui.strings.menus.promote
        ):
            case "start":
                await self.__promote_start()
            case "promote-types":
                self.__promote_types()
            case "edit-promoted-users":
                self.__edit_promoted_users()
            case "edit-profile":
                self.__edit_profile()
            case "edit-thread":
                self.__edit_thread()
            case "edit-delay":
                self.__edit_delay()
            case "edit-workers":
                self.__edit_workers()
            case _:
                pass
