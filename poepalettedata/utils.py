import dataclasses
import functools
import logging
import os
import pathlib
import string
import tempfile
import urllib.parse
from typing import TYPE_CHECKING, Any, Literal

import humanize
import requests
import requests.cookies

from poepalettedata.types import URL


if TYPE_CHECKING:
    from _typeshed import Incomplete
    from requests.sessions import (
        _Auth,
        _Cert,
        _Data,
        _Files,
        _HeadersUpdateMapping,
        _HooksInput,
        _Params,
        _TextMapping,
        _Timeout,
        _Verify,
    )


@dataclasses.dataclass(frozen=True)
class Config:
    league_type: Literal['challenge', 'challengehc', 'standard', 'hardcore']
    ninja_api_league_name: str
    ninja_website_league_name: str
    trade_league_name: str
    tft_channel_groups: list[str] = dataclasses.field(default_factory=list)
    antiquary_league_name: str | None = None
    upload: bool = False
    publish: bool = False

    @property
    def data_file(self) -> pathlib.Path:
        location = pathlib.Path(tempfile.gettempdir()) / 'poepalettedata' / 'datafiles'
        location.mkdir(parents=True, exist_ok=True)
        return location / f'data-{self.league_type}.json'


class DefaultHTTPSession(requests.Session):
    """
    The default HTTP session for this project.
    Automatically logs requests and response stats, and sets a default user agent so other
    community services can identify us.
    """

    def __init__(
        self,
        default_user_agent: str | None = 'PoE Palette Scraper (https://github.com/flbraun/poe-palette)',
    ) -> None:
        super().__init__()

        self.default_user_agent = default_user_agent
        self.hooks['response'].append(self.log_response_stats)

    @staticmethod
    def log_response_stats(r: requests.Response, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        logger = logging.getLogger('http_request')
        logger.info(
            '%s %s %s %s',
            r.url,
            r.status_code,
            f'{int(r.elapsed.total_seconds() * 1000)}ms',
            humanize.naturalsize(len(r.content), binary=True).replace(' ', ''),
        )

    def request(  # noqa: PLR0913, PLR0917
        self,
        method: str | bytes,
        url: str | bytes,
        params: '_Params | None' = None,
        data: '_Data | None' = None,
        headers: '_HeadersUpdateMapping | None' = None,
        cookies: 'requests.cookies.RequestsCookieJar | _TextMapping | None' = None,
        files: '_Files | None' = None,
        auth: '_Auth | None' = None,
        timeout: '_Timeout | None' = None,
        allow_redirects: bool = True,  # noqa: FBT001, FBT002
        proxies: '_TextMapping | None' = None,
        hooks: '_HooksInput | None' = None,
        stream: bool | None = None,  # noqa: FBT001
        verify: '_Verify | None' = None,
        cert: '_Cert | None' = None,
        json: 'Incomplete | None' = None,
    ) -> requests.Response:
        if self.default_user_agent is not None:
            if headers is None:
                headers = {}
            if not headers.get('User-Agent'):
                headers['User-Agent'] = self.default_user_agent  # type: ignore[index]
        return super().request(
            method,
            url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
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
    tft_url: URL | None = None
    tool_url: URL | None = None
    antiquary_url: URL | None = None
    craftofexile_url: URL | None = None


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


def is_format_string(str_: str) -> bool:
    """
    Checks if a string is a format string, e.g. "Hello {name}".
    """
    fmter = string.Formatter()
    parsed = tuple(fmter.parse(str_))
    if parsed:
        return parsed[0][1] is not None
    return False


class UnknownSecretError(Exception):
    """
    Raised when a secret is not found.
    """

    def __init__(self, secret_name: str) -> None:
        super().__init__(f'Unknown secret: {secret_name}')


@functools.cache
def get_secret(secret_name: str) -> str:
    """
    Retrieves a secret from the environment.
    """
    if secret_name not in os.environ:
        raise UnknownSecretError(secret_name)
    return os.environ[secret_name]
