const { keyboard, Key } = require('@nut-tree-fork/nut-js')
const { clipboard } = require('electron')

keyboard.config.autoDelayMs = 5

const ITEM_NAME_LINE = 2 // 0-based
const POLL_MAX_MS = 1000

const extractItemName = (text) => {
    const lines = text.split(/\r?\n|\r|\n/g)
    if (!text.startsWith('Item Class:') || lines.length < ITEM_NAME_LINE + 1) {
        return null
    }
    return lines[ITEM_NAME_LINE]
}

exports.getItemNameFromGame = async () => {
    const clipboardBackup = clipboard.readText()

    // send Ctrl+C to copy the ingame item into the clipboard
    await keyboard.pressKey(Key.LeftControl, Key.C)
    await keyboard.releaseKey(Key.LeftControl, Key.C)

    // check the clipboard for an item name to appear
    const started = new Date()
    while (new Date() - started < POLL_MAX_MS) {
        const itemName = extractItemName(clipboard.readText())
        if (itemName !== null) {
            console.log(`Found item "${itemName}" in clipboard after ${new Date() - started}ms`)
            // restore original clipboard content before returning
            clipboard.writeText(clipboardBackup)
            return itemName
        }
    }

    // restore original clipboard content before throwing
    clipboard.writeText(clipboardBackup)
    throw new Error(`Timeout of ${POLL_MAX_MS}ms exceeded when waiting for item to appear in clipboard`)
}
