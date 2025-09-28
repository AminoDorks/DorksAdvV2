from typing import List
from InquirerPy.base.control import Choice

from msgspec import (
    Struct,
    field
)

__all__ = [
    "Strigns"
]


class Inputs(Struct):
    input_api_key: str = field(name="inputApiKey")
    input_min_level: str = field(name="inputMinLevel")
    input_max_level: str = field(name="inputMaxLevel")
    input_min_users_per_thread: str = field(name="inputMinUsersPerThread")
    input_max_users_per_community: str = field(
        name="inputMaxUsersPerCommunity"
    )
    input_profile_nickname: str = field(name="inputProfileNickname")
    input_profile_about: str = field(name="inputProfileAbout")
    input_profile_icon: str = field(name="inputProfileIcon")
    input_use_antiban: str = field(name="inputUseAntiban")
    input_thread_title: str = field(name="inputThreadTitle")
    input_thread_description: str = field(name="inputThreadDescription")
    input_thread_announcement: str = field(name="inputThreadAnnouncement")
    input_thread_thumbnail: str = field(name="inputThreadThumbnail")
    input_thread_background: str = field(name="inputThreadBackground")
    input_delay: str = field(name="inputDelay")
    input_workers: str = field(name="inputWorkers")
    input_email: str = field(name="inputEmail")
    input_password: str = field(name="inputPassword")
    input_enter_to_exit: str = field(name="inputEnterToExit")


class Choices(Struct):
    select_menu: str = field(name="selectMenu")
    select_theme: str = field(name="selectTheme")
    select_language: str = field(name="selectLanguage")
    select_promote_type: str = field(name="selectPromoteType")
    select_accounts: str = field(name="selectAccounts")


class Menus(Struct):
    main: List[Choice]
    promote: List[Choice]
    accounts: List[Choice]
    settings: List[Choice]
    credits: List[Choice]


class Statuses(Struct):
    logged_in: str = field(name="loggedIn")
    community_joined: str = field(name="communityJoined")
    profile_edited: str = field(name="profileEdited")
    thread_created: str = field(name="threadCreated")
    promote_results: str = field(name="promoteResults")
    invited_users: str = field(name="invitedUsers")
    created_threads: str = field(name="createdThreads")
    added_communities: str = field(name="addedCommunities")


class Errors(Struct):
    error_while_logging: str = field(name="errorWhileLogging")
    error_while_joining_community: str = field(
        name="errorWhileJoiningCommunity"
    )
    error_while_editing_profile: str = field(name="errorWhileEditingProfile")
    error_while_creating_thread: str = field(name="errorWhileCreatingThread")


class Other(Struct):
    credits: str


class Strigns(Struct):
    inputs: Inputs
    choices: Choices
    statuses: Statuses
    errors: Errors
    menus: Menus
    themes: List[Choice]
    languages: List[Choice]
    promote_types: List[Choice] = field(name="promoteTypes")
    other: Other
