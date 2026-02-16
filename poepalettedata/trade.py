import json
from typing import Any
from urllib.parse import quote

from poepalettedata.types import URL, NinjaCategory
from poepalettedata.utils import slugify


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

bulk_trade_tokens: dict[str, str] = {
    'Orb of Alteration': 'alt',
    'Orb of Fusing': 'fusing',
    'Orb of Alchemy': 'alch',
    'Chaos Orb': 'chaos',
    "Gemcutter's Prism": 'gcp',
    'Exalted Orb': 'exalted',
    'Chromatic Orb': 'chrome',
    "Jeweller's Orb": 'jewellers',
    "Engineer's Orb": 'engineers',
    'Orb of Chance': 'chance',
    "Cartographer's Chisel": 'chisel',
    'Orb of Scouring': 'scour',
    'Blessed Orb': 'blessed',
    'Orb of Regret': 'regret',
    'Regal Orb': 'regal',
    'Divine Orb': 'divine',
    'Vaal Orb': 'vaal',
    'Orbs of Annulment': 'annul',
    'Wisdom Scroll': 'wisdom',
    "Armourer's Scrap": 'scrap',
    "Blacksmith's Whetstone": 'whetstone',
    "Glassblower's Bauble": 'bauble',
    'Orb of Transmutation': 'transmute',
    'Orb of Augmentation': 'aug',
    'Mirror of Kalandra': 'mirror',
    'Eternal Orb': 'eternal',
    "Facetor's Lens": 'facetors',
    'Blessing of Xoph': 'blessing-xoph',
    'Blessing of Tul': 'blessing-tul',
    'Blessing of Esh': 'blessing-esh',
    'Blessing of Uul-Netol': 'blessing-uul-netol',
    'Blessing of Chayula': 'blessing-chayula',
    # Exotic Currency
    'Orb of Dominance': 'mavens-orb',
    'Wild Crystallised Lifeforce': 'wild-lifeforce',
    'Vivid Crystallised Lifeforce': 'vivid-lifeforce',
    'Primal Crystallised Lifeforce': 'primal-lifeforce',
    'Sacred Crystallised Lifeforce': 'sacred-lifeforce',
    # Shards & Splinters
    'Splinter of Xoph': 'splinter-xoph',
    'Splinter of Tul': 'splinter-tul',
    'Splinter of Esh': 'splinter-esh',
    'Splinter of Uul-Netol': 'splinter-uul',
    'Splinter of Chayula': 'splinter-chayula',
    # Fragments & Sets
    'Sacrifice at Dusk': 'dusk',
    'Sacrifice at Midnight': 'mid',
    'Sacrifice at Dawn': 'dawn',
    'Sacrifice at Noon': 'noon',
    'Mortal Grief': 'grief',
    'Mortal Rage': 'rage',
    'Mortal Hope': 'hope',
    'Mortal Ignorance': 'ign',
    'Fragment of the Hydra': 'hydra',
    'Fragment of the Phoenix': 'phoenix',
    'Fragment of the Minotaur': 'minot',
    'Fragment of the Chimera': 'chimer',
    'Offering to the Goddess': 'offer',
    'Tribute to the Goddess': 'offer-tribute',
    'Gift to the Goddess': 'offer-gift',
    'Dedication to the Goddess': 'offer-dedication',
    'Unrelenting Timeless Eternal Emblem': 'uber-timeless-eternal-emblem',
    'Unrelenting Timeless Karui Emblem': 'uber-timeless-karui-emblem',
    'Unrelenting Timeless Vaal Emblem': 'uber-timeless-vaal-emblem',
    'Unrelenting Timeless Templar Emblem': 'uber-timeless-templar-emblem',
    'Unrelenting Timeless Maraketh Emblem': 'uber-timeless-maraketh-emblem',
    "Maven's Invitation: The Atlas": 'the-atlas',
    "Maven's Invitation: The Formed": 'the-formed',
    "Maven's Invitation: The Twisted": 'the-twisted',
    "Maven's Invitation: The Forgotten": 'the-forgotten',
    "Maven's Invitation: The Hidden": 'the-hidden',
    "Maven's Invitation: The Feared": 'the-feared',
    "Maven's Invitation: The Elderslayers": 'the-elderslayers',
}


def automake_trade_url(league_name: str, category: NinjaCategory, item_name: str, base_item: str | None = None) -> URL:
    # NinjaCategory is a good (but not perfect) indicator of whether an item is bulk tradable.
    if category in bulk_tradable_ninja_categories:
        if category in {
            NinjaCategory.MAPS,
            NinjaCategory.BLIGHTED_MAPS,
            NinjaCategory.BLIGHT_RAVAGED_MAPS,
            NinjaCategory.SCOURGED_MAPS,
        }:
            item_name = f'{item_name} Tier 16'
        return make_bulk_trade_url(league_name, item_name)

    if base_item:
        trade_type, trade_name = base_item, item_name
    else:
        trade_type, trade_name = item_name, None
    return make_trade_url(league_name, trade_type, name=trade_name)


def make_trade_url(league_name: str, type_: str, name: str | None = None) -> URL:
    # do not change the order of the keys carelessly! the trade site is very sensitive about them.
    query: dict[str, dict[str, Any]] = {
        'query': {
            'status': {'option': 'securable'},
            'type': type_,
            'stats': [{'type': 'and', 'filters': []}],
        },
        'sort': {'price': 'asc'},
    }

    if name:
        query['query']['name'] = name

    query_quoted = quote(json.dumps(query))
    return f'https://www.pathofexile.com/trade/search/{league_name}?q={query_quoted}'


def make_bulk_trade_url(league_name: str, name: str) -> URL:
    c, div = bulk_trade_tokens['Chaos Orb'], bulk_trade_tokens['Divine Orb']

    if name == 'Divine Orb':
        have = [c]
    elif name == 'Chaos Orb':
        have = [div]
    else:
        have = [c, div]

    # bulk trade utilizes a token alias instead of the actual name.
    # most of the time that token is just the slugified name.
    # there are some exceptions (mostly for older items), e.g. "Orb of Alteration" -> "alt".
    want = bulk_trade_tokens.get(name, slugify(name))

    query = {
        'exchange': {
            'status': {'option': 'online'},
            'have': have,
            'want': [want],
        },
    }

    query_quoted = quote(json.dumps(query))
    return f'https://www.pathofexile.com/trade/exchange/{league_name}?q={query_quoted}'
