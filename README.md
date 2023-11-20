# PoE Palette
Screen workers love command palettes to quickly access actions in their frequently used programs. As Path of Exile essentially is a second job and has tons of external resources and tools to consult it's time that it gets its own palette!

![demo](https://github.com/flbraun/poe-palette/raw/master/.github/demo.gif)

## Capabilities
- Search for items in the [community wiki](https://www.poewiki.net)
- Search for items in [PoEDB](https://poedb.tw) (opt-in)
- Search for items in [poe.ninja](https://poe.ninja)
- Open the [official trade site](https://www.pathofexile.com/trade) for an item; uses the [bulk item exchange](https://www.pathofexile.com/trade/exchange) when appropriate (e.g. for currency, scarabs)
- Search and open channels of [The Forbidden Trove](https://forbiddentrove.com) Discord server (opt-in; only desktop client supported)
- Open various sites of [PoeStack](https://poestack.com) (e.g. TFT Bulk Tool)

PoE Palette also knows about a hand-curated list of other smaller tools and websites, e.g. [PoELab](https://www.poelab.com), [Vorici Chromatic Calculator](https://siveran.github.io/calc.html), [Timeless Jewel Finder](https://vilsol.github.io/timeless-jewels/tree) and the [Patch Notes Archive](https://www.pathofexile.com/forum/view-forum/patch-notes).

## Installation
1. Download the latest release from the [release page](https://github.com/flbraun/poe-palette/releases).
2. Extract the archive and run the `poe-palette.exe` you will find inside.
   On the first start you will probably be warned that this program will put your computer at risk. This is because the application does not digitally sign its code. As long as you download the official release from the aforementioned release page it is still safe to run!
   Click "More info", then "Run anyway" to proceed.
3. PoE Palette will now start in the background and appear in your system tray.

## Configuration
You can configure the app by right clicking its tray icon (the Mirror of Kalandra).

Here you can choose which type of results should appear in your search results and in which league you are playing. The latter is important for referring you to the correct external resources (e.g. trade links).

## Using the palette
The palette can be opened (and hidden) by pressing the shortcut `Ctrl+P`.

Start typing for what you're looking, e.g. `abberath`. PoE Palette will now perform a fuzzy, case-insensitive search for your terms against its internal index and present you with a list of results.

From here on you can either refine your search, or navigate through the results with the `Up` and `Down` arrow keys. Hitting `Enter` will open the currently highlighted result and close the palette.

### Performing a prefixed search
You may also perform a **prefixed search**. A prefixed search consists of a special prefix (see below) followed by a colon followed by your search term, e.g. `wiki:abberath`. This will limit search results to - in this case - articles in the community wiki. This is very handy when you already know where you want to go, saving you time when navigating through the result list.

The available search prefixes are `wiki`, `poedb`, `ninja`, `trade`, `tft` and `tool`.

Please note that prefixed searches for resources disabled in the configuration will not work!

### Opening the palette for an ingame item
You may also hover over an item in the game and press the shortcut `Ctrl+Shift+P`. The palette will then open prefilled with the item's name. This allows for quickly opening that item in an external resource, e.g. poe.ninja.

## FAQ
#### Search results don't show a PoE Ninja result for my item!
PoE Ninja does not list _every_ item in the game because they pull their data from GGG's public stash API. So, if nobody lists a worthless or exceedingly rare item it does not appear on PoE Ninja, and consequently PoE Palette will not show results for it.
If your item is actually listed on [poe.ninja](https://poe.ninja) please [open an issue](https://github.com/flbraun/poe-palette/issues/new/choose).

#### How can I change the palette shortcuts?
You are able to change the shortcuts for both toggling the palette and the ingame item search, but there currently is no UI for it. You can change them manually by editing poe-palette's config file with a text editor (e.g. Notepad) though.
The config file is located at `%APPDATA&\poe-palette\config.json`. **Please exit PoE Palette before modifying this file.**
Check the [official Electron documentation](https://www.electronjs.org/docs/latest/api/accelerator#available-modifiers) for available key codes and modifiers.

## Contributing
Pull requests are generally welcome! If you want to add new features or substantially change an existing one, please [open an issue](https://github.com/flbraun/poe-palette/issues/new/choose) beforehand so we can align on the required changes.

Apart from the required code changes, please also provide necessary adjustments to public documentation (e.g. this readme, GitHub wiki, etc).
