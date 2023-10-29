const { Tray, Menu, app } = require('electron')
const path = require('node:path')
const { userSettings } = require('./storage')

exports.createTray = (leftClickCallback) => {
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
            click: (menuItem) => userSettings.set('wikiEnabled', menuItem.checked),
        },
        {
            type: 'checkbox',
            label: 'PoEDB',
            checked: userSettings.get('poedbEnabled'),
            click: (menuItem) => userSettings.set('poedbEnabled', menuItem.checked),
        },
        {
            type: 'checkbox',
            label: 'PoENinja',
            checked: userSettings.get('ninjaEnabled'),
            click: (menuItem) => userSettings.set('ninjaEnabled', menuItem.checked),
        },
        {
            type: 'checkbox',
            label: 'TFT',
            checked: userSettings.get('tftEnabled'),
            click: (menuItem) => userSettings.set('tftEnabled', menuItem.checked),
        },
        {
            type: 'checkbox',
            label: 'Tools',
            checked: userSettings.get('toolsEnabled'),
            click: (menuItem) => userSettings.set('toolsEnabled', menuItem.checked),
        },
        { type: 'separator' },
        {
            type: 'radio',
            label: 'Challenge',
            checked: userSettings.get('league') === 'challenge',
            click: () => userSettings.set('league', 'challenge'),
        },
        {
            type: 'radio',
            label: 'Challenge Hardcore',
            checked: userSettings.get('league') === 'challengehc',
            click: () => userSettings.set('league', 'challengehc'),
        },
        {
            type: 'radio',
            label: 'Standard',
            checked: userSettings.get('league') === 'standard',
            click: () => userSettings.set('league', 'standard'),
        },
        {
            type: 'radio',
            label: 'Hardcore',
            checked: userSettings.get('league') === 'hardcore',
            click: () => userSettings.set('league', 'hardcore'),
        },
        { type: 'separator' },
        { label: 'Toggle visibility', click: leftClickCallback },
        { type: 'separator' },
        { label: 'Quit', role: 'quit' },
    ])
    tray.setContextMenu(contextMenu)
}
