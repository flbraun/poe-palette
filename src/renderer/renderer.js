/* global MiniSearch */

const POEPALETTE_MINISEARCH = new MiniSearch({
    fields: ['display_text'],
    storeFields: [
        'display_text',
        'wiki_url',
        'poedb_url',
        'ninja_url',
        'trade_url',
        'tft_url',
        'antiquary_url',
        'tool_url',
    ],
})

let currentLeague
let dataTimestamp

const initMinisearch = async (league) => {
    currentLeague = league

    const url = `https://d2zmd9bpiyaqin.cloudfront.net/data-${league}.json`
    console.log(`loading search data from ${url}`)

    const response = await fetch(url)
    if (response.status !== 200) {
        window.electronAPI.panic(`Failed to download index data from ${url} (HTTP status ${response.status})`)
        return
    }
    let content
    try {
        content = await response.json()
    } catch(error) {
        window.electronAPI.panic(`Failed to parse index data from ${url} (${error.message})`)
        return
    }

    POEPALETTE_MINISEARCH.removeAll()
    console.time('search index building')
    POEPALETTE_MINISEARCH.addAll(content.data)
    console.timeEnd('search index building')
    console.log(`search index size: ${POEPALETTE_MINISEARCH.termCount}`)

    dataTimestamp = Date.parse(response.headers.get('last-modified'))
}

window.electronAPI.onLeagueChanged((event, league) => initMinisearch(league))

const checkForDataUpdates = async () => {
    const url = `https://d2zmd9bpiyaqin.cloudfront.net/data-${currentLeague}.json`

    const response = await fetch(url, { method: 'HEAD' })
    if (response.status !== 200) {
        window.electronAPI.panic(
            `Failed to check for data updates at ${url} (HTTP status ${response.status})`,
        )
        return
    }

    const lastModified = Date.parse(response.headers.get('last-modified'))

    if (lastModified > dataTimestamp) {
        console.log(`New data available at ${url}, reinitializing search index`)
        initMinisearch(currentLeague)
    } else {
        console.log(`No new data available at ${url}`)
    }
}

setInterval(checkForDataUpdates, 15 * 60 * 1000) // check every 15 minutes
