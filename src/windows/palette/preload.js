const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
    externalUrlOpen: (url) => ipcRenderer.invoke('externalUrlOpen', url),
    panic: (msg) => ipcRenderer.invoke('panic', msg),
    hideWindow: () => ipcRenderer.invoke('hideWindow'),
    onLeagueChanged: (callback) => ipcRenderer.on('leagueChanged', callback),
    onEnabledResultTypesChanged: (callback) => ipcRenderer.on('enabledResultTypesChanged', callback),
    onFocusGained: (callback) => ipcRenderer.on('focusGained', callback),
    onItemOnPalette: (callback) => ipcRenderer.on('itemOnPalette', callback),
})
