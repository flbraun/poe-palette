import dataclasses
import functools
import http
import logging
from typing import TypeAlias

from poepalettedata.types import URL, NinjaCategory
from poepalettedata.utils import DefaultHTTPSession


logger = logging.getLogger(__name__)

ninja_api_endpoint_for_category: dict[NinjaCategory, tuple[str, str]] = {  # (url_template, response_key)
    # General
    NinjaCategory.CURRENCY: (
        'https://poe.ninja/api/data/currencyoverview?league={league}&type=Currency',
        'currencyTypeName',
    ),
    NinjaCategory.FRAGMENTS: (
        'https://poe.ninja/api/data/currencyoverview?league={league}&type=Fragment',
        'currencyTypeName',
    ),
    NinjaCategory.RUNES: ('https://poe.ninja/api/data/itemoverview?league={league}&type=KalguuranRune', 'name'),
    NinjaCategory.TATTOOS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=Tattoo', 'name'),
    NinjaCategory.OMENS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=Omen', 'name'),
    NinjaCategory.DIVINATION_CARDS: (
        'https://poe.ninja/api/data/itemoverview?league={league}&type=DivinationCard',
        'name',
    ),
    NinjaCategory.ARTIFACTS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=Artifact', 'name'),
    NinjaCategory.OILS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=Oil', 'name'),
    NinjaCategory.INCUBATORS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=Incubator', 'name'),
    # Equipment & Gems
    NinjaCategory.UNIQUE_WEAPONS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=UniqueWeapon', 'name'),
    NinjaCategory.UNIQUE_ARMOURS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=UniqueArmour', 'name'),
    NinjaCategory.UNIQUE_ACCESSORIES: (
        'https://poe.ninja/api/data/itemoverview?league={league}&type=UniqueAccessory',
        'name',
    ),
    NinjaCategory.UNIQUE_FLASKS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=UniqueFlask', 'name'),
    NinjaCategory.UNIQUE_JEWELS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=UniqueJewel', 'name'),
    NinjaCategory.UNIQUE_RELICS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=UniqueRelic', 'name'),
    NinjaCategory.SKILL_GEMS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=SkillGem', 'name'),
    NinjaCategory.CLUSTER_JEWELS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=ClusterJewel', 'name'),
    # Atlas
    NinjaCategory.MAPS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=Map', 'name'),
    NinjaCategory.BLIGHTED_MAPS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=BlightedMap', 'name'),
    NinjaCategory.BLIGHT_RAVAGED_MAPS: (
        'https://poe.ninja/api/data/itemoverview?league={league}&type=BlightRavagedMap',
        'name',
    ),
    NinjaCategory.SCOURGED_MAPS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=ScourgedMap', 'name'),
    NinjaCategory.UNIQUE_MAPS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=UniqueMap', 'name'),
    NinjaCategory.DELIRIUM_ORBS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=DeliriumOrb', 'name'),
    NinjaCategory.INVITATIONS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=Invitation', 'name'),
    NinjaCategory.SCARABS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=Scarab', 'name'),
    NinjaCategory.MEMORIES: ('https://poe.ninja/api/data/itemoverview?league={league}&type=Memory', 'name'),
    # Crafting
    NinjaCategory.BASE_TYPES: ('https://poe.ninja/api/data/itemoverview?league={league}&type=BaseType', 'name'),
    NinjaCategory.FOSSILS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=Fossil', 'name'),
    NinjaCategory.RESONATORS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=Resonator', 'name'),
    NinjaCategory.BEASTS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=Beast', 'name'),
    NinjaCategory.ESSENCES: ('https://poe.ninja/api/data/itemoverview?league={league}&type=Essence', 'name'),
    NinjaCategory.VIALS: ('https://poe.ninja/api/data/itemoverview?league={league}&type=Vial', 'name'),
}

ninja_url_for_category: dict[NinjaCategory, tuple[str, bool]] = {  # (url_template, item_name_as_param)
    # General
    NinjaCategory.CURRENCY: ('https://poe.ninja/economy/{league}/currency', False),
    NinjaCategory.FRAGMENTS: ('https://poe.ninja/economy/{league}/fragments', False),
    NinjaCategory.RUNES: ('https://poe.ninja/economy/{league}/kalguuran-runes', False),
    NinjaCategory.TATTOOS: ('https://poe.ninja/economy/{league}/tattoos', False),
    NinjaCategory.OMENS: ('https://poe.ninja/economy/{league}/omens', False),
    NinjaCategory.DIVINATION_CARDS: ('https://poe.ninja/economy/{league}/divination-cards', False),
    NinjaCategory.ARTIFACTS: ('https://poe.ninja/economy/{league}/artifacts', False),
    NinjaCategory.OILS: ('https://poe.ninja/economy/{league}/oils', False),
    NinjaCategory.INCUBATORS: ('https://poe.ninja/economy/{league}/incubators', False),
    # Equipment & Gems
    NinjaCategory.UNIQUE_WEAPONS: ('https://poe.ninja/economy/{league}/unique-weapons', False),
    NinjaCategory.UNIQUE_ARMOURS: ('https://poe.ninja/economy/{league}/unique-armours', False),
    NinjaCategory.UNIQUE_ACCESSORIES: ('https://poe.ninja/economy/{league}/unique-accessories', False),
    NinjaCategory.UNIQUE_FLASKS: ('https://poe.ninja/economy/{league}/unique-flasks', False),
    NinjaCategory.UNIQUE_JEWELS: ('https://poe.ninja/economy/{league}/unique-jewels', False),
    NinjaCategory.UNIQUE_RELICS: ('https://poe.ninja/economy/{league}/unique-relics', False),
    NinjaCategory.SKILL_GEMS: ('https://poe.ninja/economy/{league}/skill-gems', True),
    NinjaCategory.CLUSTER_JEWELS: ('https://poe.ninja/economy/{league}/cluster-jewels', True),
    # Atlas
    NinjaCategory.MAPS: ('https://poe.ninja/economy/{league}/maps', True),
    NinjaCategory.BLIGHTED_MAPS: ('https://poe.ninja/economy/{league}/blighted-maps', True),
    NinjaCategory.BLIGHT_RAVAGED_MAPS: ('https://poe.ninja/economy/{league}/blight-ravaged-maps', True),
    NinjaCategory.SCOURGED_MAPS: ('https://poe.ninja/economy/{league}/scourged-maps', True),
    NinjaCategory.UNIQUE_MAPS: ('https://poe.ninja/economy/{league}/unique-maps', True),
    NinjaCategory.DELIRIUM_ORBS: ('https://poe.ninja/economy/{league}/delirium-orbs', False),
    NinjaCategory.INVITATIONS: ('https://poe.ninja/economy/{league}/invitations', False),
    NinjaCategory.SCARABS: ('https://poe.ninja/economy/{league}/scarabs', False),
    NinjaCategory.MEMORIES: ('https://poe.ninja/economy/{league}/memories', True),
    # Crafting
    NinjaCategory.BASE_TYPES: ('https://poe.ninja/economy/{league}/base-types', True),
    NinjaCategory.FOSSILS: ('https://poe.ninja/economy/{league}/fossils', False),
    NinjaCategory.RESONATORS: ('https://poe.ninja/economy/{league}/resonators', False),
    NinjaCategory.BEASTS: ('https://poe.ninja/economy/{league}/beasts', False),
    NinjaCategory.ESSENCES: ('https://poe.ninja/economy/{league}/essences', False),
    NinjaCategory.VIALS: ('https://poe.ninja/economy/{league}/vials', False),
}

RawNinjaIndex: TypeAlias = dict[NinjaCategory, set[str]]


@dataclasses.dataclass(frozen=True)
class NinjaIndex:
    raw: RawNinjaIndex

    def match(self, item_name: str) -> NinjaCategory | None:
        for category, items in self.raw.items():
            if item_name in items:
                return category
        return None

    @property
    def stats(self) -> dict[NinjaCategory, int]:
        return {key: len(self.raw[key]) for key in self.raw}

    def log_stats(self) -> None:
        logger.info('PoE Ninja index stats:')
        for category, length in self.stats.items():
            logger.info('%(category)s: %(length)d', {'category': str(category), 'length': length})


@functools.cache
def get_ninja_index(api_league_name: str) -> NinjaIndex:
    """
    Downloads current data from ninja and makes it available as a sort-of index.
    """
    raw: RawNinjaIndex = {}

    for category, endpoint_info in ninja_api_endpoint_for_category.items():
        url_template, response_attr = endpoint_info
        url = url_template.format(league=api_league_name)

        res = DefaultHTTPSession().get(url)
        assert res.status_code == http.HTTPStatus.OK, f'{res.status_code} {url}'

        res_parsed = res.json()
        raw[category] = {line[response_attr] for line in res_parsed['lines']}

    index: NinjaIndex = NinjaIndex(raw=raw)
    index.log_stats()

    return index


def make_ninja_url(
    website_league_name: str,
    item_name: str,
    base_name: str | None,
    category: NinjaCategory,
) -> URL | None:
    base_url_template, name_as_param = ninja_url_for_category[category]
    base_url = base_url_template.format(league=website_league_name)

    if name_as_param:
        return f'{base_url}?name={item_name}'

    if base_name:
        item_name += f' {base_name}'
    item_name = item_name.replace(' ', '-').replace("'", '').lower()
    return f'{base_url}/{item_name}'
