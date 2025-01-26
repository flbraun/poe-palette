import http

from poepalettedata.types import URL, NinjaCategory
from poepalettedata.utils import DefaultHTTPSession


# antiquary has slightly different categoriy names than ninja, map them.
# some ninja categories are not supported by antiquary.
ninja_antiquary_category_map: dict[NinjaCategory, str] = {
    # General
    NinjaCategory.CURRENCY: 'Currency',
    NinjaCategory.FRAGMENTS: 'Fragment',
    # NinjaCategory.TATTOOS
    # NinjaCategory.OMENS
    NinjaCategory.DIVINATION_CARDS: 'Divination',
    NinjaCategory.ARTIFACTS: 'Artifact',
    NinjaCategory.OILS: 'Oil',
    NinjaCategory.INCUBATORS: 'Incubator',
    # Equipment & Gems
    NinjaCategory.UNIQUE_WEAPONS: 'Weapon',
    NinjaCategory.UNIQUE_ARMOURS: 'Armour',
    NinjaCategory.UNIQUE_ACCESSORIES: 'Accessory',
    NinjaCategory.UNIQUE_FLASKS: 'Flask',
    NinjaCategory.UNIQUE_JEWELS: 'Jewel',
    # NinjaCategory.UNIQUE_RELICS
    NinjaCategory.SKILL_GEMS: 'Skill Gem',
    # NinjaCategory.CLUSTER_JEWELS
    # Atlas
    NinjaCategory.MAPS: 'Map',
    NinjaCategory.BLIGHTED_MAPS: 'Blighted Map',
    NinjaCategory.BLIGHT_RAVAGED_MAPS: 'Blight-ravaged Map',
    # NinjaCategory.SCOURGED_MAPS
    NinjaCategory.UNIQUE_MAPS: 'Unique Map',
    NinjaCategory.DELIRIUM_ORBS: 'Delirium Orb',
    # NinjaCategory.INVITATIONS
    NinjaCategory.SCARABS: 'Scarab',
    # NinjaCategory.MEMORIES
    # Crafting
    # NinjaCategory.BASE_TYPES
    NinjaCategory.FOSSILS: 'Fossil',
    NinjaCategory.RESONATORS: 'Resonator',
    NinjaCategory.BEASTS: 'Beast',
    NinjaCategory.ESSENCES: 'Essence',
    NinjaCategory.VIALS: 'Vial',
}


def make_antiquary_url(
    antiquary_session: DefaultHTTPSession,
    league_name: str | None,
    ninja_category: NinjaCategory,
    item_name: str,
) -> URL | None:
    """
    Antiquary identifies items by an internal id, not by their name.
    See https://github.com/PoE-TradeMacro/POE-TradeMacro/issues/702#issuecomment-388828830

    TODO: maybe it's not a good idea to use ninja_category as Ninja may forget about some
    categories after a league is done (e.g. Tattoos), but they will live on in antiquary.
    """
    if not league_name:
        return None

    antiquary_category = ninja_antiquary_category_map.get(ninja_category)
    if antiquary_category is None:
        return None

    antiquary_search_url = f'https://poe-antiquary.xyz/api/macro/{antiquary_category}/{item_name}'
    res = antiquary_session.get(antiquary_search_url)
    assert res.status_code == http.HTTPStatus.OK, f'{res.status_code} {antiquary_search_url}'
    res_parsed = res.json()

    if not res_parsed or len(res_parsed['items']) == 0:
        return None

    if len(res_parsed['items']) == 1:
        item_type_name = res_parsed['itemType']
        item_id = res_parsed['items'][0]['id']
        return f'https://poe-antiquary.xyz/{league_name}/{item_type_name}/{item_name}/{item_id}'

    if len(res_parsed['items']) > 1:
        item_type_name = res_parsed['itemType']
        return f'https://poe-antiquary.xyz/{league_name}/{item_type_name}?name={item_name}'

    return None
