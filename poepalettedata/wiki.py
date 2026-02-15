import http
import logging
import typing

from poepalettedata.antiquary import make_antiquary_url
from poepalettedata.craftofexile import get_craftofexile_index, make_craftofexile_url
from poepalettedata.ninja import get_ninja_index, make_ninja_url
from poepalettedata.trade import automake_trade_url
from poepalettedata.types import URL, NinjaCategory, Rarity
from poepalettedata.utils import Config, DefaultHTTPSession, Entry, make_poedb_url, make_wiki_url


if typing.TYPE_CHECKING:
    from collections.abc import Generator
    from typing import Any

logger = logging.getLogger(__name__)


def iter_wiki_query(wiki_session: DefaultHTTPSession, **cargo_params: str) -> Generator[dict[str, Any]]:
    page_size = 500
    offset = 0

    while True:
        res = wiki_session.get(
            'https://www.poewiki.net/w/api.php',
            params={
                'action': 'cargoquery',
                'format': 'json',
                'offset': str(offset),
                'limit': str(page_size),
                **cargo_params,
            },
        )
        assert res.status_code == http.HTTPStatus.OK

        res_decoded = res.json()
        try:
            result_page = res_decoded['cargoquery']
        except KeyError:
            # unexpected message format, probably the query was bad.
            # log full response for debugging.
            logger.exception('unexpected response from wiki: %s', res_decoded)
            raise
        result_page_len = len(result_page)

        yield from result_page

        # partial page indicates that there won't be a next page; stop crawling
        if result_page_len < page_size:
            break

        offset += result_page_len


WIKI_ITEM_BLACKLIST: set[str] = {  # items to completely ignore when importing from wiki (e.g. test data)
    'Тест',
    'Test',
    '{{subst:PAGENAME}}',
    "Booby Lady's Gloves",
    'His Judgement',  # seems to be in game files, but smells fishy
}


def get_items(config: Config) -> Generator[Entry]:
    with (
        DefaultHTTPSession() as wiki_session,
        DefaultHTTPSession() as antiquary_session,
    ):
        ninja_index = get_ninja_index(config.ninja_api_league_name)
        craftofexile_index = get_craftofexile_index()

        for item in iter_wiki_query(
            wiki_session,
            tables='items',
            fields='name,base_item,class,rarity_id,cannot_be_traded_or_modified',
            where='drop_enabled=true AND class != "Hideout Decoration" AND class != "Cosmetic Item" AND class != "Quest Item"',  # noqa: E501
            group_by='name',
        ):
            # unpack result fields
            name, base_item, _, _, tradable = (
                item['title']['name'],
                item['title']['base item'],
                item['title']['class'],
                Rarity(item['title']['rarity id']),
                not bool(int(item['title']['cannot be traded or modified'])),
            )

            if name in WIKI_ITEM_BLACKLIST:
                continue

            ninja_category = ninja_index.match(name)

            display_text = name if ninja_category is not NinjaCategory.UNIQUE_MAPS else f'{name} {base_item}'

            entry_kwargs: dict[str, URL | None] = {
                'wiki_url': make_wiki_url(name),
                'poedb_url': make_poedb_url(name),
            }

            if ninja_category is not None:
                if ninja_category != NinjaCategory.CLUSTER_JEWELS:
                    entry_kwargs['ninja_url'] = make_ninja_url(
                        config.ninja_website_league_name,
                        name,
                        base_item,
                        ninja_category,
                    )

                entry_kwargs['antiquary_url'] = make_antiquary_url(
                    antiquary_session,
                    config.antiquary_league_name,
                    ninja_category,
                    name,
                )

                if tradable:
                    entry_kwargs['trade_url'] = automake_trade_url(
                        config.trade_league_name,
                        ninja_category,
                        name,
                        base_item=base_item,
                    )

            craftofexile_ids = craftofexile_index.match(name)
            if craftofexile_ids is not None:
                entry_kwargs['craftofexile_url'] = make_craftofexile_url(*craftofexile_ids)

            yield Entry(display_text, **entry_kwargs)
