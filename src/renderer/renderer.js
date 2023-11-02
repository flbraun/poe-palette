/* global MiniSearch */

const POEPALETTE_MINISEARCH = new MiniSearch({
    fields: ['display_text'],
    storeFields: ['display_text', 'wiki_url', 'poedb_url', 'ninja_url', 'trade_url', 'tool_url'],
})

const init_minisearch = async (league) => {
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
}

window.electronAPI.onLeagueChanged((event, league) => init_minisearch(league))
