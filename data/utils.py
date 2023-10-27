import dataclasses
import logging
import urllib.parse

import humanize
import requests

from .types import URL


class LoggedRequestsSession(requests.Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hooks['response'].append(self._log_response_stats)

    def _log_response_stats(self, r, *args, **kwargs):
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
    text = text.lower()
    return text
