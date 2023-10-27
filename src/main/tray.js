const { Tray, Menu, app } = require('electron')
const path = require('node:path')

exports.createTray = (leftClickCallback) => {
    const tray = new Tray(path.join(__dirname, '..', '..', 'assets', 'mirror.png'))
    tray.setToolTip('PoE Palette')
    tray.on('click', leftClickCallback)
    const contextMenu = Menu.buildFromTemplate([
        { label: `PoE Palette v${app.getVersion()}`, enabled: false },
        { type: 'separator' },
        { type: 'checkbox', label: 'Wiki', checked: true },
        { type: 'checkbox', label: 'PoEDB', checked: true },
        { type: 'checkbox', label: 'PoENinja', checked: true },
        { type: 'checkbox', label: 'TFT', checked: true },
        { type: 'checkbox', label: 'Tools', checked: true },
        { type: 'separator' },
        { type: 'radio', label:'Challenge', checked: true },
        { type: 'radio', label:'Challenge Hardcore' },
        { type: 'radio', label:'Standard' },
        { type: 'radio', label:'Hardcore' },
        { type: 'separator' },
        { label: 'Toggle visibility', click: leftClickCallback },
        { type: 'separator' },
        { label: 'Quit', role: 'quit' },
    ])
    tray.setContextMenu(contextMenu)
}
