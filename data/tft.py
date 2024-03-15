import functools
import http
import os
from collections.abc import Generator

import emoji

from .types import URL, LeagueType
from .utils import Entry, LoggedRequestsSession


@functools.cache
def get_channel_list(server_id: str) -> list[dict]:
    session = LoggedRequestsSession()

    url = f'https://discordapp.com/api/v9/guilds/{server_id}/channels'
    headers = {
        'authorization': os.environ['DISCORD_TOKEN'],
    }
    res = session.get(url, headers=headers)
    assert res.status_code == http.HTTPStatus.OK, f'{res.status_code} {url}'

    return res.json()


def get_tft_channels(league_type: LeagueType) -> Generator[Entry, None, None]:
    tft_server_id = '645607528297922560'
    channels = get_channel_list(tft_server_id)

    if league_type == LeagueType.CHALLENGE:
        container_phrases = (
            'Affliction SC Services',
            'Affliction SC Trades',
            'Affliction SC Bulk WTB',
            'Affliction SC Bulk WTS',
        )
    elif league_type == LeagueType.CHALLENGE_HARDCORE:
        container_phrases = ('Affliction Hardcore',)
    elif league_type == LeagueType.STANDARD:
        container_phrases = ('Standard Services', 'Standard Trades', 'Standard Bulk')
    elif league_type == LeagueType.HARDCORE:
        container_phrases = ()  # TFT currently has no Hardcore section
    else:
        raise ValueError(league_type)

    # find the appropriate container channels so we can gather the child channels
    container_channel_ids = {
        channel['id']
        for channel in channels
        if any(phrase.casefold() in channel['name'].casefold() for phrase in container_phrases)
    }

    if container_phrases and not container_channel_ids:
        msg = f'No container channels found for container phrases {container_phrases!r}.'
        raise AssertionError(msg)

    for channel in channels:
        if channel['parent_id'] in container_channel_ids:
            # strip emojis from channel names
            display_text = emoji.replace_emoji(channel['name'], replace='')

            yield Entry(
                display_text=display_text,
                tft_url=make_tft_url(tft_server_id, channel['id']),
            )


def make_tft_url(server_id: str, channel_id: str) -> URL:
    return f'discord://-/channels/{server_id}/{channel_id}'
