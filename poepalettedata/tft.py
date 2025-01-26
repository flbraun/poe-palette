import functools
import http
import logging
from collections.abc import Generator

import emoji

from poepalettedata.types import URL
from poepalettedata.utils import Config, DefaultHTTPSession, Entry, get_secret


logger = logging.getLogger(__name__)


@functools.cache
def get_channel_list(server_id: str) -> list[dict[str, str]]:
    url = f'https://discordapp.com/api/v9/guilds/{server_id}/channels'
    headers = {
        'authorization': get_secret('DISCORD_AUTH_TOKEN'),
    }
    res = DefaultHTTPSession().get(url, headers=headers)
    assert res.status_code == http.HTTPStatus.OK, f'{res.status_code} {url}'

    data: list[dict[str, str]] = res.json()  # typing incomplete, but all leaf values we care about are strings
    return data


def get_tft_channels(config: Config) -> Generator[Entry]:
    if not config.tft_channel_groups:
        logger.info('No TFT channel groups configured; skipping')
        return

    tft_server_id = '645607528297922560'
    channels = get_channel_list(tft_server_id)

    # find the appropriate channel groups so we can gather the child channels
    channel_group_ids = {
        channel['id']
        for channel in channels
        if any(phrase.casefold() in channel['name'].casefold() for phrase in config.tft_channel_groups)
    }

    if not channel_group_ids:
        logger.error(
            'No channel groups found for %(channel_groups)r.',
            {'channel_groups': config.tft_channel_groups},
        )
        return

    for channel in channels:
        if channel['parent_id'] in channel_group_ids:
            # strip emojis from channel names
            display_text = emoji.replace_emoji(channel['name'], replace='')

            yield Entry(
                display_text=display_text,
                tft_url=make_tft_url(tft_server_id, channel['id']),
            )


def make_tft_url(server_id: str, channel_id: str) -> URL:
    return f'discord://-/channels/{server_id}/{channel_id}'
