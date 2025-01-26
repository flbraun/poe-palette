from collections.abc import Generator

from poepalettedata.types import NinjaCategory
from poepalettedata.utils import Config, Entry, is_format_string


tool_data = [
    # PoELab
    {'display_text': 'PoELab - Normal', 'tool_url': 'https://www.poelab.com/gtgax'},
    {'display_text': 'PoELab - Cruel', 'tool_url': 'https://www.poelab.com/r8aws'},
    {'display_text': 'PoELab - Merciless', 'tool_url': 'https://www.poelab.com/riikv'},
    {'display_text': 'PoELab - Eternal', 'tool_url': 'https://www.poelab.com/wfbra'},
    # PoENinja
    {'display_text': 'PoE Ninja - Builds', 'tool_url': 'https://poe.ninja/builds/{ninja_website_league_name}'},
    {'display_text': 'PoE Ninja - Streamers', 'tool_url': 'https://poe.ninja/builds/streamers'},
    *[
        {
            'display_text': f'PoE Ninja - {category.value}',
            'tool_url': f'https://poe.ninja/economy/{{ninja_website_league_name}}/{category.value.lower().replace(" ", "-")}',  # noqa: E501
        }
        for category in NinjaCategory
    ],
    # misc
    {'display_text': 'Craft of Exile', 'tool_url': 'https://www.craftofexile.com/'},
    {'display_text': 'PoEDB', 'tool_url': 'https://poedb.tw/us'},
    {'display_text': 'PoEDB - Modifiers', 'tool_url': 'https://poedb.tw/us/Modifiers'},
    {'display_text': 'Vorici Chromatic Calculator', 'tool_url': 'https://siveran.github.io/calc.html'},
    {'display_text': 'Path of Exile Regex', 'tool_url': 'https://poe.re/'},
    {'display_text': 'GGG Tracker', 'tool_url': 'https://gggtracker.com/'},
    {'display_text': 'Official Trade Site', 'tool_url': 'https://www.pathofexile.com/trade/search/{trade_league_name}'},
    {'display_text': 'Patch Notes Archive', 'tool_url': 'https://www.pathofexile.com/forum/view-forum/patch-notes'},
    {'display_text': 'Maxroll Passive Tree Planner', 'tool_url': 'https://maxroll.gg/poe/poe-passive-tree/'},
    {'display_text': 'Maxroll Atlas Tree Planner', 'tool_url': 'https://maxroll.gg/poe/poe-atlas-tree/'},
    {
        'display_text': 'Large Cluster Jewel Calculator',
        'tool_url': 'https://theodorejbieber.github.io/PoEClusterJewelCalculator/',
    },
    {'display_text': 'Timeless Jewel Finder', 'tool_url': 'https://vilsol.github.io/timeless-jewels/tree'},
]


def get_tools(config: Config) -> Generator[Entry]:
    for data in tool_data:
        url_template = data['tool_url']
        if is_format_string(url_template):
            data['tool_url'] = url_template.format(
                ninja_website_league_name=config.ninja_website_league_name,
                trade_league_name=config.trade_league_name,
            )

        yield Entry(**data)
