import dataclasses
import functools

from tabulate import tabulate

from .types import URL, NinjaCategory
from .utils import LoggedRequestsSession


ninja_api_endpoint_for_category: dict[NinjaCategory, tuple[str, str]] = {
    # General
    NinjaCategory.CURRENCY: ('https://poe.ninja/api/data/currencyoverview?league=Ancestor&type=Currency', 'currencyTypeName'),  # noqa: E501
    NinjaCategory.FRAGMENTS: ('https://poe.ninja/api/data/currencyoverview?league=Ancestor&type=Fragment', 'currencyTypeName'),  # noqa: E501
    NinjaCategory.TATTOOS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=Tattoo', 'name'),
    NinjaCategory.OMENS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=Omen', 'name'),
    NinjaCategory.DIVINATION_CARDS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=DivinationCard', 'name'),  # noqa: E501
    NinjaCategory.ARTIFACTS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=Artifact', 'name'),
    NinjaCategory.OILS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=Oil', 'name'),
    NinjaCategory.INCUBATORS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=Incubator', 'name'),
    # Equipment & Gems
    NinjaCategory.UNIQUE_WEAPONS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=UniqueWeapon', 'name'),
    NinjaCategory.UNIQUE_ARMOURS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=UniqueArmour', 'name'),
    NinjaCategory.UNIQUE_ACCESSORIES: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=UniqueAccessory', 'name'),  # noqa: E501
    NinjaCategory.UNIQUE_FLASKS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=UniqueFlask', 'name'),
    NinjaCategory.UNIQUE_JEWELS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=UniqueJewel', 'name'),
    NinjaCategory.UNIQUE_RELICS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=UniqueRelic', 'name'),
    NinjaCategory.SKILL_GEMS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=SkillGem', 'name'),
    NinjaCategory.CLUSTER_JEWELS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=ClusterJewel', 'name'),
    # Atlas
    NinjaCategory.MAPS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=Map', 'name'),
    NinjaCategory.BLIGHTED_MAPS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=BlightedMap', 'name'),
    NinjaCategory.BLIGHT_RAVAGED_MAPS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=BlightRavagedMap', 'name'),  # noqa: E501
    NinjaCategory.SCOURGED_MAPS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=ScourgedMap', 'name'),
    NinjaCategory.UNIQUE_MAPS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=UniqueMap', 'name'),
    NinjaCategory.DELIRIUM_ORBS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=DeliriumOrb', 'name'),
    NinjaCategory.INVITATIONS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=Invitation', 'name'),
    NinjaCategory.SCARABS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=Scarab', 'name'),
    NinjaCategory.MEMORIES: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=Memory', 'name'),
    # Crafting
    NinjaCategory.BASE_TYPES: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=BaseType', 'name'),
    NinjaCategory.FOSSILS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=Fossil', 'name'),
    NinjaCategory.RESONATORS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=Resonator', 'name'),
    NinjaCategory.HELMET_ENCHANTS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=HelmetEnchant', 'name'),  # noqa: E501
    NinjaCategory.BEASTS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=Beast', 'name'),
    NinjaCategory.ESSENCES: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=Essence', 'name'),
    NinjaCategory.VIALS: ('https://poe.ninja/api/data/itemoverview?league=Ancestor&type=Vial', 'name'),
}

ninja_url_for_category: dict[NinjaCategory, tuple[str, bool]] = {  # (url, item_name_as_param)
    # General
    NinjaCategory.CURRENCY: ('https://poe.ninja/economy/ancestor/currency', False),
    NinjaCategory.FRAGMENTS: ('https://poe.ninja/economy/ancestor/fragments', False),
    NinjaCategory.TATTOOS: ('https://poe.ninja/economy/ancestor/tattoos', False),
    NinjaCategory.OMENS: ('https://poe.ninja/economy/ancestor/omens', False),
    NinjaCategory.DIVINATION_CARDS: ('https://poe.ninja/economy/ancestor/divination-cards', False),
    NinjaCategory.ARTIFACTS: ('https://poe.ninja/economy/ancestor/artifacts', False),
    NinjaCategory.OILS: ('https://poe.ninja/economy/ancestor/oils', False),
    NinjaCategory.INCUBATORS: ('https://poe.ninja/economy/ancestor/incubators', False),
    # Equipment & Gems
    NinjaCategory.UNIQUE_WEAPONS: ('https://poe.ninja/economy/ancestor/unique-weapons', False),
    NinjaCategory.UNIQUE_ARMOURS: ('https://poe.ninja/economy/ancestor/unique-armours', False),
    NinjaCategory.UNIQUE_ACCESSORIES: ('https://poe.ninja/economy/ancestor/unique-accessories', False),
    NinjaCategory.UNIQUE_FLASKS: ('https://poe.ninja/economy/ancestor/unique-flasks', False),
    NinjaCategory.UNIQUE_JEWELS: ('https://poe.ninja/economy/ancestor/unique-jewels', False),
    NinjaCategory.UNIQUE_RELICS: ('https://poe.ninja/economy/ancestor/unique-relics', False),
    NinjaCategory.SKILL_GEMS: ('https://poe.ninja/economy/ancestor/skill-gems', True),
    NinjaCategory.CLUSTER_JEWELS: ('https://poe.ninja/economy/ancestor/cluster-jewels', True),
    # Atlas
    NinjaCategory.MAPS: ('https://poe.ninja/economy/ancestor/maps', True),
    NinjaCategory.BLIGHTED_MAPS: ('https://poe.ninja/economy/ancestor/blighted-maps', True),
    NinjaCategory.BLIGHT_RAVAGED_MAPS: ('https://poe.ninja/economy/ancestor/blight-ravaged-maps', True),
    NinjaCategory.SCOURGED_MAPS: ('https://poe.ninja/economy/ancestor/scourged-maps', True),
    NinjaCategory.UNIQUE_MAPS: ('https://poe.ninja/economy/ancestor/unique-maps', True),
    NinjaCategory.DELIRIUM_ORBS: ('https://poe.ninja/economy/ancestor/delirium-orbs', False),
    NinjaCategory.INVITATIONS: ('https://poe.ninja/economy/ancestor/invitations', False),
    NinjaCategory.SCARABS: ('https://poe.ninja/economy/ancestor/scarabs', False),
    NinjaCategory.MEMORIES: ('https://poe.ninja/economy/ancestor/memories', True),
    # Crafting
    NinjaCategory.BASE_TYPES: ('https://poe.ninja/economy/ancestor/base-types', True),
    NinjaCategory.FOSSILS: ('https://poe.ninja/economy/ancestor/fossils', False),
    NinjaCategory.RESONATORS: ('https://poe.ninja/economy/ancestor/resonators', False),
    NinjaCategory.HELMET_ENCHANTS: ('https://poe.ninja/economy/ancestor/helmet-enchants', True),
    NinjaCategory.BEASTS: ('https://poe.ninja/economy/ancestor/beasts', False),
    NinjaCategory.ESSENCES: ('https://poe.ninja/economy/ancestor/essences', False),
    NinjaCategory.VIALS: ('https://poe.ninja/economy/ancestor/vials', False),
}


@dataclasses.dataclass(frozen=True)
class NinjaIndex:
    raw: dict[NinjaCategory, set[str]]

    def match(self, item_name: str) -> NinjaCategory | None:
        for category, items in self.raw.items():
            if item_name in items:
                return category

    @property
    def stats(self):
        return {key: len(self.raw[key]) for key in self.raw}

    def print_stats(self):
        print(
            tabulate(
                [[category, length] for category, length in self.stats.items()],
                headers=('ninja category', '# items'),
                tablefmt='outline',
            )
        )


@functools.cache
def get_ninja_index() -> NinjaIndex:
    """
    Downloads current data from ninja and makes it available as a sort-of index.
    """
    session = LoggedRequestsSession()

    index = {}

    for category, endpoint_info in ninja_api_endpoint_for_category.items():
        url, response_attr = endpoint_info

        res = session.get(url)
        assert res.status_code == 200

        res_parsed = res.json()
        index[category] = {line[response_attr] for line in res_parsed['lines']}

    index = NinjaIndex(raw=index)
    index.print_stats()

    return index


def make_ninja_url(item_name: str, base_name: str | None, category: NinjaCategory) -> URL | None:
    base_url, name_as_param = ninja_url_for_category[category]

    if name_as_param:
        return f'{base_url}?name={item_name}'

    if base_name:
        item_name += f' {base_name}'
    item_name = item_name.replace(' ', '-').replace("'", '').lower()
    return f'{base_url}/{item_name}'
