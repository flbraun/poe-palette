import dataclasses
import functools
import http
import json
from typing import Any

from .types import URL
from .utils import DefaultHTTPSession


@dataclasses.dataclass(frozen=True)
class CraftOfExileIndex:
    raw: dict[str, tuple[int, int]]  # (b, bi)

    def match(self, item_name: str) -> tuple[int, int] | None:
        return self.raw.get(item_name, None)


@functools.cache
def get_craftofexile_index(craftofexile_session: DefaultHTTPSession) -> CraftOfExileIndex:
    """
    Downloads current data from Craft of Exile and makes it available as a sort-of index.
    """
    index = {}

    url = 'https://www.craftofexile.com/json/data/main/poec_data.json'
    res = craftofexile_session.get(url)
    assert res.status_code == http.HTTPStatus.OK, f'{res.status_code} {url}'

    # the endpoint returns a JSON string, but its prefixed with some junk that
    # make it invalid JSON. clean that up.
    junk = 'poecd='
    assert res.text.startswith(junk), f'{res.text[:20]}'
    res_parsed = json.loads(res.text[len(junk):])

    item: dict[str, Any]
    for item in res_parsed['bitems']['seq']:
        index[item['name_bitem']] = (int(item['id_base']), int(item['id_bitem']))

    return CraftOfExileIndex(raw=index)


def make_craftofexile_url(b: int, bi: int) -> URL | None:
    """
    b is CoE's internal id for the type of crafting base, e.g. 33 for "Gloves (STR)".
    bi is CoE's internal id for the concrete crafting base, e.g. 7595 for "Spiked Gloves".
    """
    return f'https://www.craftofexile.com/?b={b}&bi={bi}'
