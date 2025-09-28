from msgspec import (
    Struct,
    field
)

__all__ = [
    "LoginResponse"
]


class LoginResponse(Struct):
    session_id: str = field(name="sid")
