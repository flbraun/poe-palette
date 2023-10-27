import json
from urllib.parse import quote

from .ninja import NinjaCategory
from .types import URL
from .utils import slugify


bulk_tradable_ninja_categories: set[NinjaCategory] = {
    NinjaCategory.CURRENCY,
    NinjaCategory.FRAGMENTS,
    NinjaCategory.TATTOOS,
    NinjaCategory.ARTIFACTS,
    NinjaCategory.OILS,
    NinjaCategory.INCUBATORS,
    NinjaCategory.MAPS,
    NinjaCategory.BLIGHTED_MAPS,
    NinjaCategory.BLIGHT_RAVAGED_MAPS,
    NinjaCategory.SCOURGED_MAPS,
    NinjaCategory.DELIRIUM_ORBS,
    NinjaCategory.SCARABS,
    NinjaCategory.FOSSILS,
    NinjaCategory.RESONATORS,
    NinjaCategory.BEASTS,
    NinjaCategory.ESSENCES,
}


def automake_trade_url(category: NinjaCategory, item_name: str, base_item: str | None = None) -> URL:
    # NinjaCategory is a good (but not perfect) indicator of whether an item is bulk tradable.
    if category in bulk_tradable_ninja_categories:
        if category in {
            NinjaCategory.MAPS,
            NinjaCategory.BLIGHTED_MAPS,
            NinjaCategory.BLIGHT_RAVAGED_MAPS,
            NinjaCategory.SCOURGED_MAPS,
        }:
            item_name = f'{item_name} Tier 16'
        return make_bulk_trade_url(item_name)

    if base_item:
        trade_type, trade_name = base_item, item_name
    else:
        trade_type, trade_name = item_name, None
    return make_trade_url(trade_type, name=trade_name)


def make_trade_url(type_: str, name: str | None = None) -> URL:
    # do not change the order of the keys carelessly! the trade site is very sensitive about them.
    query = {
        'query': {
            'status': {'option': 'online'},
            'type': type_,
            'stats': [{'type': 'and', 'filters': []}],
        },
        'sort': {'price': 'asc'},
    }

    if name:
        query['query']['name'] = name

    query_quoted = quote(json.dumps(query))
    return f'https://www.pathofexile.com/trade/search/Ancestor?q={query_quoted}'


def make_bulk_trade_url(name: str) -> URL:
    query = {
        'exchange': {
            'status': {'option': 'online'},
            'have': ['divine', 'chaos'],
            'want': [slugify(name)],
        }
    }

    query_quoted = quote(json.dumps(query))
    return f'https://www.pathofexile.com/trade/exchange/Ancestor?q={query_quoted}'
