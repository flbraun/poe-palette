const { Tray, Menu, app } = require('electron')
const path = require('node:path')
const { userSettings } = require('./storage')

exports.createTray = (leftClickCallback, window) => {
    const tray = new Tray(path.join(__dirname, '..', '..', 'assets', 'mirror.png'))
    tray.setToolTip('PoE Palette')
    tray.on('click', leftClickCallback)
    const contextMenu = Menu.buildFromTemplate([
        { label: `PoE Palette v${app.getVersion()}`, enabled: false },
        { type: 'separator' },
        {
            type: 'checkbox',
            label: 'Wiki',
            checked: userSettings.get('wikiEnabled'),
            click: (menuItem) => {
                userSettings.set('wikiEnabled', menuItem.checked)
                window.webContents.send('enabledResultTypesChanged', userSettings.getEnabledResultTypes())
            },
        },
        {
            type: 'checkbox',
            label: 'PoEDB',
            checked: userSettings.get('poedbEnabled'),
            click: (menuItem) => {
                userSettings.set('poedbEnabled', menuItem.checked)
                window.webContents.send('enabledResultTypesChanged', userSettings.getEnabledResultTypes())
            },
        },
        {
            type: 'checkbox',
            label: 'PoENinja',
            checked: userSettings.get('ninjaEnabled'),
            click: (menuItem) => {
                userSettings.set('ninjaEnabled', menuItem.checked)
                window.webContents.send('enabledResultTypesChanged', userSettings.getEnabledResultTypes())
            },
        },
        {
            type: 'checkbox',
            label: 'Trade',
            checked: userSettings.get('tradeEnabled'),
            click: (menuItem) => {
                userSettings.set('tradeEnabled', menuItem.checked)
                window.webContents.send('enabledResultTypesChanged', userSettings.getEnabledResultTypes())
            },
        },
        {
            type: 'checkbox',
            label: 'TFT',
            checked: userSettings.get('tftEnabled'),
            click: (menuItem) => {
                userSettings.set('tftEnabled', menuItem.checked)
                window.webContents.send('enabledResultTypesChanged', userSettings.getEnabledResultTypes())
            },
        },
        {
            type: 'checkbox',
            label: 'PoE Antiquary',
            checked: userSettings.get('antiquaryEnabled'),
            click: (menuItem) => {
                userSettings.set('antiquaryEnabled', menuItem.checked)
                window.webContents.send('enabledResultTypesChanged', userSettings.getEnabledResultTypes())
            },
        },
        {
            type: 'checkbox',
            label: 'Craft of Exile',
            checked: userSettings.get('craftofexileEnabled'),
            click: (menuItem) => {
                userSettings.set('craftofexileEnabled', menuItem.checked)
                window.webContents.send('enabledResultTypesChanged', userSettings.getEnabledResultTypes())
            },
        },
        {
            type: 'checkbox',
            label: 'Tools',
            checked: userSettings.get('toolsEnabled'),
            click: (menuItem) => {
                userSettings.set('toolsEnabled', menuItem.checked)
                window.webContents.send('enabledResultTypesChanged', userSettings.getEnabledResultTypes())
            },
        },
        { type: 'separator' },
        {
            type: 'radio',
            label: 'Challenge',
            checked: userSettings.get('league') === 'challenge',
            click: () => {
                ;(userSettings.set('league', 'challenge'), window.webContents.send('leagueChanged', 'challenge'))
            },
        },
        {
            type: 'radio',
            label: 'Challenge Hardcore',
            checked: userSettings.get('league') === 'challengehc',
            click: () => {
                ;(userSettings.set('league', 'challengehc'), window.webContents.send('leagueChanged', 'challengehc'))
            },
        },
        {
            type: 'radio',
            label: 'Standard',
            checked: userSettings.get('league') === 'standard',
            click: () => {
                ;(userSettings.set('league', 'standard'), window.webContents.send('leagueChanged', 'standard'))
            },
        },
        {
            type: 'radio',
            label: 'Hardcore',
            checked: userSettings.get('league') === 'hardcore',
            click: () => {
                ;(userSettings.set('league', 'hardcore'), window.webContents.send('leagueChanged', 'hardcore'))
            },
        },
        { type: 'separator' },
        { label: 'Quit', role: 'quit' },
    ])
    tray.setContextMenu(contextMenu)
}
