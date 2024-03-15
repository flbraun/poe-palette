from collections.abc import Generator

from .leagues import League
from .ninja import get_ninja_index, make_ninja_url
from .trade import make_trade_url
from .types import NinjaCategory
from .utils import DefaultHTTPSession, Entry, make_wiki_url


def get_beasts(league: League) -> Generator[Entry, None, None]:
    with DefaultHTTPSession() as ninja_session:
        index = get_ninja_index(ninja_session, league)

    for beast in index.raw[NinjaCategory.BEASTS]:
        yield Entry(
            display_text=beast,
            wiki_url=make_wiki_url(beast),
            ninja_url=make_ninja_url(league, beast, None, NinjaCategory.BEASTS),
            trade_url=make_trade_url(league, beast),
        )
