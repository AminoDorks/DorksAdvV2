from googletrans import Translator
from itertools import chain
from re import findall

from src.ui._ui import UIManager

from asyncio import (
    gather,
    create_task,
    sleep,
    Semaphore
)
from typing import (
    Dict,
    List
)
from aminodorksfix.asyncfix import (
    Client,
    SubClient
)
from aminodorksfix.lib.util.objects import (
    Community,
    CommunityList,
    UserProfileCountList
)
from aminodorksfix.lib.util.exceptions import (
    InvalidCodeOrLink,
    YouAreBanned
)

from src.utils._utils import (
    nullabelize,
    match_invite_code
)
from src._constants import (
    CONFIG,
    CACHE,
    COMMUNITIES,
    MESSAGE,
    SPAM_UNICODE
)

__all__ = [
    "Promoter"
]


class Promoter:
    __slots__ = (
        "_client",
        "_ui",
        "_messages",
        "_icon_binary",
        "_thumbnail_binary",
        "_background_binary",
        "_icon",
        "_all_invited_users",
        "_all_created_threads",
        "_all_added_communities"
    )

    _translator: Translator = Translator()

    def __init__(self, client: Client, ui: UIManager) -> None:
        self._client = client
        self._ui = ui
        self._messages = {}
        self._icon = None
        self._all_invited_users = 0
        self._all_created_threads = 0
        self._all_added_communities = 0

    @staticmethod
    def __level_is_valid(level: int) -> bool:
        return level >= CONFIG.promote_config.min_level and \
            level <= CONFIG.promote_config.max_level

    @classmethod
    def __get_filtered_users(
        cls,
        excluded_ids: List[str],
        responses: List[UserProfileCountList]
    ) -> List[str]:
        users = list(map(lambda response: response.json.get(
            "userProfileList", []
        ), responses))

        user_dicts = list(map(lambda user: {
            "user_id": user["uid"],
            "level": user["level"]
            }, list(chain.from_iterable(
                users
            )
        )))

        filtered_user_dicts = list(
            filter(
                lambda user_id: (
                    user_id["user_id"] not in excluded_ids
                    and cls.__level_is_valid(user_id["level"])
                ),
                user_dicts,
            )
        )

        return list(map(
            lambda user_id: user_id["user_id"],
            filtered_user_dicts
        ))

    @classmethod
    async def __get_translated_text(cls) -> Dict[str, str]:
        languages = {}
        local_message = MESSAGE
        finded_urls = findall(r"https?://[^\s]+", local_message)

        for index, url in enumerate(finded_urls, 0):
            local_message = local_message.replace(url, f"@{index}")

        for language in ["en", "ru", "ar", "de", "fr", "pt"]:
            text = (await cls._translator.translate(
                text=local_message,
                dest=language
            )).text

            for index, url in enumerate(finded_urls, 0):
                text = text.replace(f"@{index}", url).replace(
                    f"@ {index}", url
                )

            languages[language] = text

        return languages

    async def __create_thread(
            self,
            sub_client: SubClient,
            message: str,
            users: List[str]
    ) -> None:
        try:
            thread = await sub_client.start_chat(
                userId=users,
                message=message
            )
            announcement = nullabelize(
                CONFIG.promote_config.thread_config.announcement
            )

            await sub_client.edit_chat(
                chatId=str(thread.chatId),
                announcement=announcement,
                pinAnnouncement=True if announcement else False,
                title=nullabelize(CONFIG.promote_config.thread_config.title),
                content=nullabelize(
                    CONFIG.promote_config.thread_config.description
                ),
                icon=self._icon
            )
            await sub_client.edit_chat(
                chatId=str(thread.chatId),
                viewOnly=True
            )
            await sub_client.edit_chat(
                chatId=str(thread.chatId),
                backgroundImage=open(
                    CONFIG.promote_config.thread_config.background,
                    "rb"
                )
            )
            self._ui.output_text(
                text=self._ui.strings.statuses.thread_created.format(
                    len(users)
                ),
                elements=[str(sub_client.comId), str(thread.chatId)]
            )
            self._all_invited_users += len(users)
            self._all_created_threads += 1
        except Exception as e:
            self._ui.output_text(
                self._ui.strings.errors.error_while_creating_thread + str(e),
                [str(sub_client.comId)]
            )
        finally:
            await sleep(CONFIG.promote_config.delay)

    async def __safe_get_users(self, sub_client: SubClient) -> List[List[str]]:
        staff = [
            *(await sub_client.get_all_users(type="leaders")).profile.userId,
            *(await sub_client.get_all_users(type="curators")).profile.userId,
        ]
        online_users_count = (await sub_client.get_online_users()).json.get(
            "userProfileCount", 0
        )

        all_users = self.__get_filtered_users(staff, await gather(*[
            sub_client.get_online_users(start=start, size=start + 100)
            for start in range(
                0,
                min(
                    online_users_count,
                    CONFIG.promote_config.max_users_per_community
                ),
                100
            )
        ]))

        if len(all_users) >= CONFIG.promote_config.max_users_per_community:
            filtered_all_users = all_users[
                :CONFIG.promote_config.max_users_per_community
            ]

            return [filtered_all_users[
                i: i + CONFIG.promote_config.min_users_per_thread
                ] for i in range(
                0, len(filtered_all_users
                       ), CONFIG.promote_config.min_users_per_thread)]

        tasks = [
            sub_client.get_all_users(
                type="recent",
                start=start,
                size=start + 100
            )
            for start in range(
                0,
                CONFIG.promote_config.max_users_per_community - len(
                    all_users
                ) + 100, 100)
        ]

        all_users.extend(
            self.__get_filtered_users(staff, await gather(*tasks))
        )

        filtered_all_users = list(set(
            all_users
        ))[:CONFIG.promote_config.max_users_per_community]

        return [filtered_all_users[
                i: i + CONFIG.promote_config.min_users_per_thread
                ] for i in range(
                0, len(filtered_all_users
                       ), CONFIG.promote_config.min_users_per_thread)]

    async def __promote_threads(
            self,
            sub_client: SubClient,
            language: str
    ) -> None:
        try:
            users_to_promote = await self.__safe_get_users(sub_client)
            message = self._messages[language]

            for users_group in users_to_promote:
                await self.__create_thread(
                    sub_client=sub_client,
                    message=message,
                    users=users_group
                )
            self._all_added_communities += 1
        except Exception as e:
            self._ui.output_text(
                self._ui.strings.errors.error_while_creating_thread + str(e),
                [str(sub_client.comId)]
            )
        finally:
            await sleep(CONFIG.promote_config.delay)

    async def __edit_profile(self, sub_client: SubClient) -> None:
        try:
            await sub_client.edit_profile(
                nickname=nullabelize(
                    CONFIG.promote_config.profile_config.nickname
                ),
                content=SPAM_UNICODE if (
                    CONFIG.promote_config.profile_config.use_antiban
                ) else nullabelize(CONFIG.promote_config.profile_config.about),
                icon=open(
                    CONFIG.promote_config.profile_config.icon,
                    "rb"
                )
            )
            self._ui.output_text(
                self._ui.strings.statuses.profile_edited,
                [str(sub_client.comId)]
            )

        except Exception as e:
            self._ui.output_text(
                self._ui.strings.errors.error_while_editing_profile + str(e),
                [str(sub_client.comId)]
            )
        finally:
            await sleep(CONFIG.promote_config.delay)

    async def __safe_get_community(
            self,
            community_list: CommunityList,
            link: str
    ) -> Community | None:
        try:
            community_from_link = (await self._client.get_from_code(
                link
            )).json["extensions"]["community"]
        except Exception:
            return

        community_object = await self._client.get_community_info(
            community_from_link["ndcId"]
        )

        if community_object.comId in community_list.comId:
            return community_object

        try:
            await self._client.join_community(
                str(community_object.comId)
            )
        except YouAreBanned:
            return
        except InvalidCodeOrLink:
            invite_code = match_invite_code(str(community_object.description))
            if not invite_code:
                return

            try:
                await self._client.join_community(
                    comId=str(community_object.comId),
                    invitationCode=invite_code.split(
                        "http://aminoapps.com/invite/"
                    )[1]
                )
            except Exception:
                return
            return community_object
        finally:
            await sleep(CONFIG.promote_config.delay)

    async def __community_worker(
            self,
            semaphore: Semaphore,
            community_list: CommunityList,
            link: str
    ) -> None:
        async with semaphore:
            community = await self.__safe_get_community(
                community_list=community_list,
                link=link
            )

            if not community:
                self._ui.output_text(
                    self._ui.strings.errors.error_while_joining_community,
                    [link]
                )
                return

            self._ui.output_text(
                self._ui.strings.statuses.community_joined,
                [str(community.comId)]
            )

            sub_client = SubClient(
                comId=community.comId,
                profile=self._client.profile  # type: ignore
            )

            await self.__edit_profile(sub_client)
            await self.__promote_threads(
                sub_client=sub_client,
                language=str(community.primaryLanguage)
            )
            try:
                await self._client.leave_community(str(community.comId))
            except Exception:
                pass

    async def start(self) -> None:
        semaphore = Semaphore(CONFIG.promote_config.workers)

        if not self._messages:
            self._messages = await self.__get_translated_text()

        for account in CACHE.accounts.values():
            self._client = self._ui.call_client(
                device_id=account.device_id
            )

            try:
                await self._client.login_sid(
                    SID=account.session_id
                )
                self._ui.output_text(
                    self._ui.strings.statuses.logged_in.format(
                        self._client.profile.json["nickname"]  # type: ignore
                    )
                )
            except Exception as e:
                self._ui.output_text(
                    f"{self._ui.strings.errors.error_while_logging} {e}"
                )
            community_list = await self._client.sub_clients(
                start=0,
                size=100
            )

            try:
                self._icon = await self._client.upload_media(
                    file=open(
                        CONFIG.promote_config.thread_config.thumbnail,
                        "rb"
                    ),
                    fileType="image"
                )
            except:  # noqa: E722
                pass

            await gather(*[
                create_task(self.__community_worker(
                    semaphore=semaphore,
                    community_list=community_list,
                    link=link
                )) for link in COMMUNITIES
            ])

        self._ui.output_text(self._ui.strings.statuses.promote_results)
        for value, caption in zip([
            self._all_invited_users,
            self._all_created_threads,
            self._all_added_communities
        ], [
            self._ui.strings.statuses.invited_users,
            self._ui.strings.statuses.created_threads,
            self._ui.strings.statuses.added_communities
        ]):
            self._ui.output_text(
                text=str(value),
                elements=[caption]
            )
        self._ui.call_input(self._ui.strings.inputs.input_enter_to_exit)
