from src.structs.config import Config
from src.structs.themes import Themes
from src.structs.cache import Cache
from src.utils._loader import load_file

__all__ = [
    "CONFIG",
    "THEMES",
    "CACHE",
    "COMMUNITIES",
    "API_MIN_LEVEL",
    "API_MAX_LEVEL",
    "MESSAGE",
    "SPAM_UNICODE"
]

CONFIG_PATH = "config.json"
THEMES_PATH = "assets/themes.json"
CACHE_PATH = "cache.json"
STRINGS_PATH = "assets/strings_{}.json"
COMMUNITIES_PATH = "communities.txt"
MESSAGE_PATH = "message.txt"
SPAM_UNICODE_PATH = "assets/unicode.txt"

CONFIG = load_file(CONFIG_PATH, Config)
THEMES = load_file(THEMES_PATH, Themes)
CACHE = load_file(CACHE_PATH, Cache)

COMMUNITIES = set(open(COMMUNITIES_PATH, "r").read().split("\n"))
MESSAGE = open(MESSAGE_PATH, "r", encoding="utf-8").read()
SPAM_UNICODE = open(SPAM_UNICODE_PATH, "r", encoding="utf-8").read()

API_MIN_LEVEL = 0
API_MAX_LEVEL = 21
