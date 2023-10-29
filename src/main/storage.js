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
    tftEnabled: { type: 'boolean' },
    toolsEnabled: { type: 'boolean' },
    league: {
        type: 'string',
        enum: ['challenge', 'challengehc', 'standard', 'hardcore'],
    },
}

const userSettings = new Store({ userSettingsSchema })
setdefault(userSettings, 'wikiEnabled', true)
setdefault(userSettings, 'poedbEnabled', false)
setdefault(userSettings, 'ninjaEnabled', true)
setdefault(userSettings, 'tftEnabled', false)
setdefault(userSettings, 'toolsEnabled', true)
setdefault(userSettings, 'league', 'challenge')
console.log(`userSettings located at ${userSettings.path}`)

exports.userSettings = userSettings
