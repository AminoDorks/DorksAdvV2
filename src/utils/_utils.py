from re import search

__all__ = [
    "match_invite_code",
    "nullabelize"
]


def match_invite_code(content: str) -> str | None:
    matches = search(
        pattern=r"http://aminoapps\.com/invite/[a-zA-Z0-9]+",
        string=content
    )

    if matches:
        return matches.group(0)


def nullabelize(value: str | None) -> str | None:
    return None if not value or value == "" else value
