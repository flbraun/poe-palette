from collections.abc import Generator

from poepalettedata.ninja import get_ninja_index, make_ninja_url
from poepalettedata.trade import make_trade_url
from poepalettedata.types import NinjaCategory
from poepalettedata.utils import Config, Entry, make_wiki_url


def get_beasts(config: Config) -> Generator[Entry]:
    index = get_ninja_index(config.ninja_api_league_name)

    for beast in index.raw[NinjaCategory.BEASTS]:
        yield Entry(
            display_text=beast,
            wiki_url=make_wiki_url(beast),
            ninja_url=make_ninja_url(config.ninja_website_league_name, beast, None, NinjaCategory.BEASTS),
            trade_url=make_trade_url(config.trade_league_name, beast),
        )
