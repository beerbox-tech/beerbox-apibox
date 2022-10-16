"""
created by: thibault defeyter
created at: 2022/10/21
licene: MIT

beerbox configuration
"""

from os import getenv
from urllib.parse import quote


def get_bool(key: str, default: bool) -> bool:
    """return a boolean value from env variables, default to false"""
    default_value = "true" if default else "false"
    return getenv(key, default_value).lower() == "true"


def get_string(key: str, default: str) -> str:
    """return string value from env variables"""
    return getenv(key, default)


def postgres_url(user: str, password: str, host: str, port: str, database: str) -> str:
    """return a postresql url from user, password, host, port and database"""
    return f"postgresql://{user}:{quote(password)}@{host}:{port}/{database}"


# general config
SERVICE = get_string("SERVICE", "beerbox-backend")
VERSION = get_string("VERSION", "dev")

# identifier generation configuration
IDENTIFIER_ALPHABET = "abcdefghijklmnopqrstuvxyz"
IDENTIFIER_SIZE = 8

# database config
POSTGRES_USERNAME = get_string("POSTGRES_USERNAME", "admin")
POSTGRES_PASSWORD = get_string("POSTGRES_PASSWORD", "admin")
POSTGRES_DATABASE = get_string("POSTGRES_DATABASE", "beerbox")
POSTGRES_HOST = get_string("POSTGRES_HOST", "localhost")
POSTGRES_PORT = get_string("POSTGRES_PORT", "5432")
POSTGRES_ECHO = get_bool("POSTGRES_ECHO", False)
POSTGRES_URL = postgres_url(
    POSTGRES_USERNAME,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DATABASE,
)
