import argparse
import dataclasses
import enum
import logging
import string
import urllib.parse
from typing import Any

import humanize
import requests

from .types import URL


class LoggedRequestsSession(requests.Session):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.hooks['response'].append(self.log_response_stats)

    @staticmethod
    def log_response_stats(r: requests.Session, *args, **kwargs) -> None:
        logger = logging.getLogger('http_request')
        logger.info(
            '%s %s %s %s',
            r.url,
            r.status_code,
            f'{int(r.elapsed.total_seconds() * 1000)}ms',
            humanize.naturalsize(len(r.content), binary=True).replace(' ', ''),
        )


@dataclasses.dataclass(frozen=True)
class Entry:
    """
    The final data container that serializes data for the
    electron app to consume.
    """
    display_text: str
    wiki_url: URL | None = None
    poedb_url: URL | None = None
    ninja_url: URL | None = None
    trade_url: URL | None = None
    tool_url: URL | None = None


def make_wiki_url(item_name: str) -> URL:
    item_name = item_name.replace(' ', '_')
    return f'https://www.poewiki.net/wiki/{item_name}'


def make_poedb_url(item_name: str) -> URL:
    item_name = item_name.replace(' ', '_').replace("'", '')
    item_name = urllib.parse.quote(item_name)
    return f'https://poedb.tw/us/{item_name}'


def slugify(text: str) -> str:
    text = text.replace("'", '').replace(' ', '-')
    return text.lower()


class EnumAction(argparse.Action):
    """
    Argparse action for handling Enums.

    Courtesy by Tim on StackOverflow: https://stackoverflow.com/a/60750535
    Slight adaptations to satisfy the project's linter.
    """
    def __init__(self, **kwargs) -> None:
        # Pop off the type value
        enum_type = kwargs.pop('type', None)

        # Ensure an Enum subclass is provided
        if enum_type is None:
            msg = 'type must be assigned an Enum when using EnumAction'
            raise ValueError(msg)
        if not issubclass(enum_type, enum.Enum):
            msg = 'type must be an Enum when using EnumAction'
            raise TypeError(msg)

        # Generate choices from the Enum
        kwargs.setdefault('choices', tuple(e.value for e in enum_type))

        super().__init__(**kwargs)

        self._enum = enum_type

    def __call__(
            self,
            parser: argparse.ArgumentParser,
            namespace: argparse.Namespace,
            values: Any,  # noqa: ANN401
            option_string: str | None = None,
        ) -> None:
        # Convert value back into an Enum
        value = self._enum(values)
        setattr(namespace, self.dest, value)


def is_format_string(str_: str) -> bool:
    """
    Checks if a string is a format string, e.g. "Hello {name}".
    """
    fmter = string.Formatter()
    return next(fmter.parse(str_))[1] is not None
