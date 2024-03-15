const Store = require('electron-store')

const setdefault = (store, key, value) => {
    if (!store.has(key)) {
        store.set(key, value)
    }
}

const userSettingsSchema = {
    wikiEnabled: { type: 'boolean' },
    poedbEnabled: { type: 'boolean' },
    ninjaEnabled: { type: 'boolean' },
    tradeEnabled: { type: 'boolean' },
    tftEnabled: { type: 'boolean' },
    antiquaryEnabled: { type: 'boolean' },
    toolsEnabled: { type: 'boolean' },
    league: {
        type: 'string',
        enum: ['challenge', 'challengehc', 'standard', 'hardcore'],
    },
    paletteShortcut: { type: 'string' },
    itemOnPaletteShortcut: { type: 'string' },
}

const userSettings = new Store({ userSettingsSchema })
setdefault(userSettings, 'wikiEnabled', true)
setdefault(userSettings, 'poedbEnabled', false)
setdefault(userSettings, 'ninjaEnabled', true)
setdefault(userSettings, 'tradeEnabled', true)
setdefault(userSettings, 'tftEnabled', false)
setdefault(userSettings, 'antiquaryEnabled', false)
setdefault(userSettings, 'toolsEnabled', true)
setdefault(userSettings, 'league', 'challenge')
setdefault(userSettings, 'paletteShortcut', 'CommandOrControl+P')
setdefault(userSettings, 'itemOnPaletteShortcut', 'CommandOrControl+Shift+P')
userSettings.getEnabledResultTypes = () => {
    const enabled = []
    if (userSettings.get('wikiEnabled')) enabled.push('wiki')
    if (userSettings.get('poedbEnabled')) enabled.push('poedb')
    if (userSettings.get('ninjaEnabled')) enabled.push('ninja')
    if (userSettings.get('tradeEnabled')) enabled.push('trade')
    if (userSettings.get('tftEnabled')) enabled.push('tft')
    if (userSettings.get('antiquaryEnabled')) enabled.push('antiquary')
    if (userSettings.get('toolsEnabled')) enabled.push('tools')
    return enabled
}
console.log(`userSettings located at ${userSettings.path}`)

exports.userSettings = userSettings
