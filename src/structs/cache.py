from typing import Dict

from msgspec import (
    Struct,
    field
)

__all__ = [
    "CachedAccount",
    "Cache"
]


class CachedAccount(Struct):
    device_id: str = field(name="deviceId")
    session_id: str = field(name="sid")
    email: str
    password: str


class Cache(Struct):
    accounts: Dict[str, CachedAccount] = field(default={})
