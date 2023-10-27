const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
    externalUrlOpen: (url) => ipcRenderer.invoke('externalUrlOpen', url),
    panic: (msg) => ipcRenderer.invoke('panic', msg),
})