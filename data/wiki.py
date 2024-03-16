import http
import itertools
import pprint
from collections.abc import Generator

from tabulate import tabulate

from .antiquary import make_antiquary_url
from .craftofexile import get_craftofexile_index, make_craftofexile_url
from .leagues import League
from .ninja import NinjaCategory, get_ninja_index, make_ninja_url
from .trade import automake_trade_url
from .types import Rarity
from .utils import DefaultHTTPSession, Entry, make_poedb_url, make_wiki_url


def iter_wiki_query(wiki_session: DefaultHTTPSession, **cargo_params: dict[str, str]) -> Generator[dict, None, None]:
    page_size = 500
    offset = 0

    while True:
        res = wiki_session.get(
            'https://www.poewiki.net/w/api.php',
            params={
                'action': 'cargoquery',
                'format': 'json',
                'offset': offset,
                'limit': page_size,
                **cargo_params,
            },
        )
        assert res.status_code == http.HTTPStatus.OK

        res_decoded = res.json()
        try:
            result_page = res_decoded['cargoquery']
        except KeyError:
            # unexpected message format, probably the query was bad.
            # print full response for debugging.
            pprint.pprint(res_decoded)
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
KNOWN_NINJA_UNLISTED_NAMES: set[str] = {  # item names that are never listed on ninja
    # non-armour/weapon base types
    'Contract: Bunker',
    'Contract: Laboratory',
    'Contract: Mansion',
    'Contract: Prohibited Library',
    'Contract: Records Office',
    'Contract: Repository',
    "Contract: Smuggler's Den",
    'Contract: Tunnels',
    'Contract: Underbelly',
    'Blueprint: Bunker',
    'Blueprint: Laboratory',
    'Blueprint: Mansion',
    'Blueprint: Prohibited Library',
    'Blueprint: Records Office',
    'Blueprint: Repository',
    "Blueprint: Smuggler's Den",
    'Blueprint: Tunnels',
    'Blueprint: Underbelly',
    'Amethyst Flask',
    'Aquamarine Flask',
    'Basalt Flask',
    'Bismuth Flask',
    'Corundum Flask',
    'Diamond Flask',
    'Gold Flask',
    'Granite Flask',
    'Iron Flask',
    'Jade Flask',
    'Quartz Flask',
    'Quicksilver Flask',
    'Ruby Flask',
    'Sapphire Flask',
    'Silver Flask',
    'Stibnite Flask',
    'Sulphur Flask',
    'Topaz Flask',
    'Colossal Life Flask',
    'Divine Life Flask',
    'Eternal Life Flask',
    'Giant Life Flask',
    'Grand Life Flask',
    'Greater Life Flask',
    'Hallowed Life Flask',
    'Large Life Flask',
    'Medium Life Flask',
    'Sacred Life Flask',
    'Sanctified Life Flask',
    'Small Life Flask',
    'Colossal Mana Flask',
    'Divine Mana Flask',
    'Eternal Mana Flask',
    'Giant Mana Flask',
    'Grand Mana Flask',
    'Greater Mana Flask',
    'Hallowed Mana Flask',
    'Large Mana Flask',
    'Medium Mana Flask',
    'Sacred Mana Flask',
    'Sanctified Mana Flask',
    'Small Mana Flask',
    'Colossal Hybrid Flask',
    'Hallowed Hybrid Flask',
    'Large Hybrid Flask',
    'Medium Hybrid Flask',
    'Sacred Hybrid Flask',
    'Small Hybrid Flask',
    'Candlestick Relic',
    'Censer Relic',
    'Coffer Relic',
    'Papyrus Relic',
    'Processional Relic',
    'Tome Relic',
    'Urn Relic',
    'Large Cluster Jewel',
    'Medium Cluster Jewel',
    'Small Clorster Jewel',
    'Small Cluster Jewel',
    'Breach Ring',  # always drops rare and corrupted
    'Ashscale Talisman',  # always drops rare and corrupted
    'Avian Twins Talisman',  # always drops rare and corrupted
    'Black Maw Talisman',  # always drops rare and corrupted
    'Bonespire Talisman',  # always drops rare and corrupted
    'Breakrib Talisman',  # always drops rare and corrupted
    'Chrysalis Talisman',  # always drops rare and corrupted
    'Clutching Talisman',  # always drops rare and corrupted
    'Deadhand Talisman',  # always drops rare and corrupted
    'Deep One Talisman',  # always drops rare and corrupted
    'Fangjaw Talisman',  # always drops rare and corrupted
    'Hexclaw Talisman',  # always drops rare and corrupted
    'Horned Talisman',  # always drops rare and corrupted
    'Lone Antler Talisman',  # always drops rare and corrupted
    'Longtooth Talisman',  # always drops rare and corrupted
    'Mandible Talisman',  # always drops rare and corrupted
    'Monkey Paw Talisman',  # always drops rare and corrupted
    'Monkey Twins Talisman',  # always drops rare and corrupted
    'Primal Skull Talisman',  # always drops rare and corrupted
    'Rot Head Talisman',  # always drops rare and corrupted
    'Rotfeather Talisman',  # always drops rare and corrupted
    'Spinefuse Talisman',  # always drops rare and corrupted
    'Splitnewt Talisman',  # always drops rare and corrupted
    'Three Hands Talisman',  # always drops rare and corrupted
    'Three Rat Talisman',  # always drops rare and corrupted
    'Undying Flesh Talisman',  # always drops rare and corrupted
    'Wereclaw Talisman',  # always drops rare and corrupted
    'Writhing Talisman',  # always drops rare and corrupted
    "Thief's Trinket",  # always drops rare and corrupted
    # currency (mostly shards)
    'Chaos Orb',  # gold standard, so will never be listed
    "Facetor's Lens",  # price varies by stored experience
    'Alchemy Shard',
    'Alteration Shard',
    'Ancient Shard',
    'Bestiary Orb',
    'Binding Shard',
    'Chaos Shard',
    "Engineer's Shard",
    'Horizon Shard',
    'Imprint',
    'Imprinted Bestiary Orb',
    'Regal Shard',
    'Scroll Fragment',
    'Transmutation Shard',
    "Harbinger's Shard",
    # misc
    'Fine Incubator',  # low-level version of Ornate Incubator
    'Whispering Incubator',  # low-level version Infused Incubator
    "Gemcutter's Incubator",  # superseded by Thaumaturge's Incubator?
    'Pale Court Set',
    'Blood-filled Vessel',
    'Chronicle of Atzoatl',
    'Deadly End',  # The Tower of Ordeals piece
    'Ignominious Fate',  # The Tower of Ordeals piece
    'Victorious Fate',  # The Tower of Ordeals piece
    'Will of Chaos',  # The Tower of Ordeals piece
    'Deregulation Scroll',  # upgrades Harbinger items
    'Electroshock Scroll',  # upgrades Harbinger items
    'Fragmentation Scroll',  # upgrades Harbinger items
    'Haemocombustion Scroll',  # upgrades Harbinger items
    'Specularity Scroll',  # upgrades Harbinger items
    'Time-light Scroll',  # upgrades Harbinger items
    'Ritual Splinter',
    *(  # non-collectable Expedition artifacts
        f'{tier} {faction} Artifact'
        for tier, faction in itertools.product(
            ('Lesser', 'Greater', 'Grand', 'Exceptional'),
            ('Black Scythe', 'Broken Circle', 'Order', 'Sun'),
        )
    ),
}
KNOWN_NINJA_UNLISTED_CLASSES: set[str] = {  # wiki item classes that are never listed on ninja
    'Monster Organ Sample',
    'Voidstone',
    'Captured Soul',
    'Incursion Item',
    'Fishing Rod',
    'Expedition Logbook',
    "Rogue's Brooch",
    "Rogue's Cloak",
    "Rogue's Gear",
    "Rogue's Tool",
    'Heist Target',
    'Labyrinth Key',
    'Labyrinth Trinket',
    'Sanctum Research',
}


def get_items(league: League) -> Generator[Entry, None, None]:
    with (
        DefaultHTTPSession() as wiki_session,
        DefaultHTTPSession() as ninja_session,
        DefaultHTTPSession() as antiquary_session,
        DefaultHTTPSession() as craftofexile_session,
    ):
        ninja_unknown = []
        ninja_index = get_ninja_index(ninja_session, league)
        craftofexile_index = get_craftofexile_index(craftofexile_session)

        for item in iter_wiki_query(
            wiki_session,
            tables='items',
            fields='name,base_item,class,rarity_id,cannot_be_traded_or_modified',
            where='drop_enabled=true AND class != "Hideout Decoration" AND class != "Cosmetic Item" AND class != "Quest Item"',  # noqa: E501
            group_by='name',
        ):
            # unpack result fields
            name, base_item, class_, rarity, tradable = (
                item['title']['name'],
                item['title']['base item'],
                item['title']['class'],
                Rarity(item['title']['rarity id']),
                not bool(int(item['title']['cannot be traded or modified'])),
            )

            if name in WIKI_ITEM_BLACKLIST:
                continue

            ninja_category = ninja_index.match(name)
            is_known = name in KNOWN_NINJA_UNLISTED_NAMES or class_ in KNOWN_NINJA_UNLISTED_CLASSES
            if ninja_category is None and not is_known:
                ninja_unknown.append((name, base_item, class_, rarity.value))

            display_text = name if ninja_category is not NinjaCategory.UNIQUE_MAPS else f'{name} {base_item}'

            entry_kwargs = {
                'display_text': display_text,
                'wiki_url': make_wiki_url(name),
                'poedb_url': make_poedb_url(name),
                'antiquary_url': make_antiquary_url(antiquary_session, league, ninja_category, name),
            }

            if ninja_category is not None and ninja_category != NinjaCategory.CLUSTER_JEWELS:
                entry_kwargs['ninja_url'] = make_ninja_url(league, name, base_item, ninja_category)

            if tradable:
                entry_kwargs['trade_url'] = automake_trade_url(league, ninja_category, name, base_item=base_item)

            craftofexile_ids = craftofexile_index.match(name)
            if craftofexile_ids is not None:
                entry_kwargs['craftofexile_url'] = make_craftofexile_url(*craftofexile_ids)

            yield Entry(**entry_kwargs)

    print(
        tabulate(
            [[*thing] for thing in sorted(ninja_unknown, key=lambda x: x[2])],
            headers=('name', 'base item', 'class', 'rarity id'),
            tablefmt='outline',
        ),
    )
