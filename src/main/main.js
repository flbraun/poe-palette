const { app, BrowserWindow, ipcMain, shell, globalShortcut, dialog, screen } = require('electron')
const path = require('node:path')
const tray = require('./tray')
const { userSettings } = require('./storage')
const { checkForUpdates } = require('./update')
const { getItemNameFromGame } = require('./clipboard')

app.commandLine.appendSwitch('wm-window-animations-disabled')

// check for updates in background
if (app.isPackaged) {
    checkForUpdates()
}

const toggleWindowVisibility = (win) => {
    if (win.isVisible()) {
        win.hide()
    } else {
        win.show()
    }
}

const panic = (msg) => {
    // call when something non-recoverable happened.
    // displays the message, then exits the application.
    dialog.showMessageBoxSync(null, {
        type: 'error',
        title: 'Fatal Error',
        message: 'A fatal error occured.',
        detail: msg,
        buttons: ['OK'],
    })
    app.quit()
}

const createPaletteWindow = () => {
    const primaryDisplay = screen.getPrimaryDisplay()
    const { width, height } = primaryDisplay.workAreaSize

    const window = new BrowserWindow({
        width: width,
        height: height,
        webPreferences: {
            preload: path.join(__dirname, '..', 'windows', 'palette', 'preload.js'),
        },
        frame: false,
        transparent: true,
        show: false,
        skipTaskbar: true,
    })
    window.loadFile(path.join(__dirname, '..', 'windows', 'palette', 'index.html'))

    // hide the palette window when it loses focus
    window.on('blur', window.hide)

    // automatically open dev tools when in dev mode
    if (!app.isPackaged) window.webContents.openDevTools()

    return window
}

app.whenReady().then(() => {
    console.log('\n----------------------------------------')
    console.log(`PoE Palette v${app.getVersion()}`)
    console.log(`Running Node v${process.versions.node}`)
    console.log(`Running Electron v${process.versions.electron}`)
    console.log(`Running Chromium v${process.versions.chrome}`)
    console.log('----------------------------------------')

    const paletteWindow = createPaletteWindow()

    // create tray and make it toggle the palette window when left-clicked
    tray.createTray(() => toggleWindowVisibility(paletteWindow), paletteWindow)

    // register IPC handlers for messages _from_ the palette renderer
    ipcMain.handle('externalUrlOpen', (event, url) => shell.openExternal(url))
    ipcMain.handle('panic', (event, msg) => panic(msg))
    ipcMain.handle('hideWindow', () => paletteWindow.hide())

    // once the window has finished loading, send the current user settings to the palette renderer
    paletteWindow.webContents.once('did-finish-load', () => {
        paletteWindow.webContents.send('enabledResultTypesChanged', userSettings.getEnabledResultTypes())
        paletteWindow.webContents.send('leagueChanged', userSettings.get('league'))
    })

    // register shortcuts
    const shortcuts = new Map([ // shortcut => callback
        [
            userSettings.get('paletteShortcut'),
            () => toggleWindowVisibility(paletteWindow),
        ],
        [
            userSettings.get('itemOnPaletteShortcut'),
            () => {
                getItemNameFromGame()
                    .then((itemName) => {
                        if (itemName !== null) {
                            paletteWindow.webContents.send('itemOnPalette', itemName)
                            toggleWindowVisibility(paletteWindow)
                        }
                    })
                    .catch((err) => console.error(err))
            },
        ],
    ])
    shortcuts.forEach((value, key) => {
        const ret = globalShortcut.register(key, value)
        if (!ret) {
            panic(`Failed to register shortcut: ${key}`)
        }
    })

    console.log('\nPoE Palette is ready.\n')
})

// propagate focus events to the respective renderer
app.on('browser-window-focus', (event, window) => {
    window.webContents.send('focusGained')
})

app.on('will-quit', () => globalShortcut.unregisterAll())
