from collections.abc import Generator

from .ninja import NinjaCategory
from .utils import Entry


all_tools = [
    # PoEStack
    Entry(display_text='PoeStack', tool_url='https://poestack.com/'),
    Entry(display_text='PoeStack - Stash View', tool_url='https://poestack.com/poe/stash-view?league=Ancestor'),
    Entry(display_text='PoeStack - Pricing', tool_url='https://poestack.com/pricing'),
    Entry(display_text='PoeStack - TFT Bulk Tool', tool_url='https://poestack.com/tft/bulk-tool?league=Ancestor'),
    Entry(display_text='PoeStack - TFT Compasses', tool_url='https://poestack.com/tft/live-search?tag=compasses'),
    Entry(display_text='PoeStack - TFT Five Ways', tool_url='https://poestack.com/tft/live-search?tag=five-ways'),
    # PoELab
    Entry(display_text='PoELab - Normal', tool_url='https://www.poelab.com/gtgax'),
    Entry(display_text='PoELab - Cruel', tool_url='https://www.poelab.com/r8aws'),
    Entry(display_text='PoELab - Merciless', tool_url='https://www.poelab.com/riikv'),
    Entry(display_text='PoELab - Eternal', tool_url='https://www.poelab.com/wfbra'),
    # PoENinja
    Entry(display_text='PoE Ninja - Builds', tool_url='https://poe.ninja/builds/ancestor'),
    Entry(display_text='PoE Ninja - Streamers', tool_url='https://poe.ninja/builds/streamers'),
    *[
        Entry(
            display_text=f'PoE Ninja - {category.value}',
            tool_url=f'https://poe.ninja/economy/ancestor/{category.value.lower().replace(" ", "-")}',
        )
        for category in NinjaCategory
    ],
    # misc
    Entry(display_text='Craft of Exile', tool_url='https://www.craftofexile.com/'),
    Entry(display_text='PoEDB', tool_url='https://poedb.tw/us'),
    Entry(display_text='PoEDB - Modifiers', tool_url='https://poedb.tw/us/Modifiers'),
    Entry(display_text='PoE Antiquary', tool_url='https://poe-antiquary.xyz'),
    Entry(display_text='Vorici Chromatic Calculator', tool_url='https://siveran.github.io/calc.html'),
    Entry(display_text='Path of Exile Regex', tool_url='https://poe.re/'),
    Entry(display_text='GGG Tracker', tool_url='https://gggtracker.com/'),
    Entry(display_text='Official Trade Site', tool_url='https://www.pathofexile.com/trade/search/Ancestor'),
    Entry(display_text='Patch Notes Archive', tool_url='https://www.pathofexile.com/forum/view-forum/patch-notes'),
    Entry(display_text='Maxroll Passive Tree Planner', tool_url='https://maxroll.gg/poe/poe-passive-tree/'),
    Entry(display_text='Maxroll Atlas Tree Planner', tool_url='https://maxroll.gg/poe/poe-atlas-tree/'),
    Entry(display_text='Large Cluster Jewel Calculator', tool_url='https://theodorejbieber.github.io/PoEClusterJewelCalculator/'),
    Entry(display_text='Timeless Jewel Finder', tool_url='https://vilsol.github.io/timeless-jewels/tree'),
]


def get_tools() -> Generator[Entry, None, None]:
    yield from all_tools
