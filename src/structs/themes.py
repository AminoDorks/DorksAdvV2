from msgspec import Struct


__all__ = [
    "Themes",
    "Theme"
]


class Theme(Struct):
    logo: str
    ansiColor: str
    inquirerStyle: dict


class Themes(Struct):
    classic: Theme
    sunlight: Theme
    grass: Theme
    purple: Theme
