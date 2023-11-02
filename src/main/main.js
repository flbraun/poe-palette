const { app, BrowserWindow, ipcMain, shell, globalShortcut, dialog } = require('electron')
const path = require('node:path')
const tray = require('./tray')
const { userSettings } = require('./storage')

app.commandLine.appendSwitch('wm-window-animations-disabled')

const createWindow = (width, height) => {
    const win = new BrowserWindow({
        width: width,
        height: height,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
        },
        frame: false,
        transparent: true,
        show: false,
        skipTaskbar: true,
    })
    win.loadFile(path.join(__dirname, '..', 'renderer', 'index.html'))

    // automatically open dev tools when in dev mode
    if (!app.isPackaged) win.webContents.openDevTools()

    return win
}

const toggleWindowVisibility = (win) => {
    if (win.isVisible()) {
        win.hide()
    } else {
        win.show()
    }
}

const panic = (window, msg) => {
    // call when something non-recoverable happened.
    // displays the message, then exits the application.
    dialog.showMessageBoxSync(window, {
        type: 'error',
        title: 'Fatal Error',
        message: 'A fatal error occured.',
        detail: msg,
        buttons: ['OK'],
    })
    app.quit()
}

app.whenReady().then(() => {
    const { screen } = require('electron')
    const primaryDisplay = screen.getPrimaryDisplay()
    const { width, height } = primaryDisplay.workAreaSize

    console.log(`PoE Palette v${app.getVersion()}`)
    console.log(`Running Node v${process.versions.node}`)
    console.log(`Running Electron v${process.versions.electron}`)
    console.log(`Running Chromium v${process.versions.chrome}`)
    console.log(`Screen dimensions: ${width}x${height} px`)

    const window = createWindow(width, height)
    tray.createTray(() => toggleWindowVisibility(window))
    // hide the palette window when it loses focus
    window.on('blur', window.hide)

    ipcMain.handle('externalUrlOpen', (event, url) => shell.openExternal(url))
    ipcMain.handle('panic', (event, msg) => panic(window, msg))
    ipcMain.handle('hideWindow', () => window.hide())
    ipcMain.handle('getSelectedLeague', () => userSettings.get('league'))

    const shortcut = 'CommandOrControl+P'
    const ret = globalShortcut.register(shortcut, () => toggleWindowVisibility(window))
    if (!ret) {
        panic(window, `Failed to register shortcut: ${shortcut}`)
    }
})

app.on('will-quit', () => globalShortcut.unregisterAll())
