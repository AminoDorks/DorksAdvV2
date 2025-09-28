from msgspec import Struct

from typing import (
    Any,
    TypeVar,
    Type
)
from msgspec.json import (
    encode,
    decode,
    format
)

__all__ = [
    "load_file",
    "save_file"
]

T = TypeVar("T", bound=Struct)


def load_file(path: str, type: Type[T]) -> T:
    try:
        return decode(
            open(
                path,
                "r",
                encoding="utf-8"
            ).read(), type=type
        )
    except FileNotFoundError:
        object = type()
        with open(path, "w") as file:
            file.write(encode(object).decode("utf-8"))
        return object


def save_file(path: str, object: Any) -> None:
    with open(path, "w", encoding="utf-8") as file:
        file.write(format(encode(object), indent=4).decode("utf-8"))
