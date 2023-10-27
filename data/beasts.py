from collections.abc import Generator

from .ninja import get_ninja_index, make_ninja_url
from .trade import make_trade_url
from .types import NinjaCategory
from .utils import Entry, make_wiki_url


def get_beasts() -> Generator[Entry, None, None]:
    index = get_ninja_index()

    for beast in index.raw[NinjaCategory.BEASTS]:
        yield Entry(
            display_text=beast,
            wiki_url=make_wiki_url(beast),
            ninja_url=make_ninja_url(beast, None, NinjaCategory.BEASTS),
            trade_url=make_trade_url(beast),
        )
