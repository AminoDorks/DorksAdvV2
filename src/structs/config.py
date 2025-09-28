from msgspec import (
    Struct,
    field,
    structs
)

__all__ = [
    "Config",
    "ProfileConfig",
    "ThreadConfig"
]

ICON_PATH = "assets/icon.jpg"
THUMBNAIL_PATH = "assets/thumbnail.jpg"
BACKGROUND_PATH = "assets/background.jpg"


class ProfileConfig(Struct, frozen=True):
    nickname: str | None = field(default=None)
    about: str | None = field(default=None)
    icon: str = field(default=ICON_PATH)
    use_antiban: bool = field(name="useAntiban", default=True)


class ThreadConfig(Struct, frozen=True):
    title: str | None = field(default=None)
    description: str | None = field(default=None)
    announcement: str | None = field(default=None)
    thumbnail: str = field(default=THUMBNAIL_PATH)
    background: str = field(default=BACKGROUND_PATH)


class PromoteConfig(Struct, frozen=True):
    delay: int = field(default=2)
    workers: int = field(default=1)
    min_level: int = field(name="minLevel", default=1)
    max_level: int = field(name="maxLevel", default=20)
    min_users_per_thread: int = field(name="minUsersPerThread", default=50)
    max_users_per_community: int = field(
        name="maxUsersPerCommunity",
        default=250
    )
    promote_type: str = field(name="promoteType", default="private-chats")
    profile_config: ProfileConfig = field(
        name="profileConfig",
        default=ProfileConfig()
    )
    thread_config: ThreadConfig = field(
        name="threadConfig",
        default=ThreadConfig()
    )

    def copy(self, **kwargs):
        d = structs.asdict(self)
        d.update(kwargs)
        return type(self)(**d)


class Config(Struct):
    locale: str = field(default="en")
    api_key: str | None = field(name="apiKey", default=None)
    theme: str = field(default="classic")
    promote_config: PromoteConfig = field(
        name="promoteConfig",
        default=PromoteConfig()
    )
