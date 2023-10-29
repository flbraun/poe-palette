/* global POEPALETTE_MINISEARCH */

const KEY_CODES = {
    ENTER: 13,
    ARROW_UP: 38,
    ARROW_DOWN: 40,
}

const ICONS = {
    WIKI: '../../assets/wiki.png',
    POEDB: '../../assets/poedb.png',
    NINJA: '../../assets/ninja.png',
    TRADE: '../../assets/trade.png',
    GOTO: '../../assets/goto.png',
}

const resultTypes = ['wiki', 'poedb', 'ninja', 'trade', 'tool']
const specialSearchPrefixes = resultTypes.map(e => `${e}:`)

// register click handlers that hide the window when clicking outside of the palette area
document.getElementsByTagName('body')[0].addEventListener('click', () => {
    window.electronAPI.hideWindow()
})
document.getElementById('palette').addEventListener('click', (event) => {
    event.stopPropagation()
})

const makePalette = (searchInput, resultlist) => {
    let selectedResult = null

    const addResultNode = (icon, text, target) => {
        const image = document.createElement('img')
        image.src = icon
        image.classList.add('icon')

        const label = document.createTextNode(text)

        const result = document.createElement('div')
        result.classList.add('result')
        result.appendChild(image)
        result.appendChild(label)
        result.onclick = (event) => { event.preventDefault(); window.electronAPI.externalUrlOpen(target) }

        resultlist.appendChild(result)
        /* todo highlight terms */
    }

    const navigateResult = (incr) => {
        const resultlen = resultlist.children.length
        if (resultlen == 0) {
            return // there is nothing to navigate through
        }
        const current = Array.prototype.indexOf.call(resultlist.children, selectedResult)

        let next = current + incr
        // honor bounds of resultlist
        if (next < 0) next = 0
        if (next > resultlen - 1) next = resultlen - 1
        // todo: when out of bounds, wrap to top/bottom

        if (selectedResult !== null) {
            selectedResult.classList.remove('focus')
        }
        const nextElem = resultlist.childNodes.item(next)
        nextElem.classList.add('focus')
        selectedResult = nextElem
    }

    searchInput.addEventListener('input', () => {
        // clear previous search results
        resultlist.replaceChildren()

        // prepare search
        let term = searchInput.value.trim()
        let targetedSearch = null  // null or one of resultTypes

        // are we searching for something special? e.g. "ninja:fragment of"
        const targetedSearchesMatched = specialSearchPrefixes.filter(e => term.startsWith(e))
        if (targetedSearchesMatched.length > 0) {
            targetedSearch = targetedSearchesMatched[0].replace(':', '')
            term = term.substring(targetedSearch.length + 1)
        }

        if (term.length === 0) {
            return // no usable term present; don't bother the search index
        }

        // perform search
        const timeName = targetedSearch !== null ? `targeted search (${targetedSearch}) for "${term}"` : `search for "${term}"` // eslint-disable-line max-len
        console.time(timeName)
        const searchresults = POEPALETTE_MINISEARCH.search(term, { prefix: true, fuzzy: 0.2 })
        console.timeEnd(timeName)

        // handle search results
        if (searchresults.length === 0) {
            // no results found, offer wiki search
            addResultNode(ICONS.WIKI, `Search wiki for "${term}"`, `https://www.poewiki.net/index.php?title=Special:Search&search=${term}`) // eslint-disable-line max-len
        } else {
            // render first N search results
            const maxResults = targetedSearch === null ? 5 : 5 * resultTypes.length
            searchresults.slice(0, maxResults).forEach(r => {
                if (
                    [null, 'wiki'].includes(targetedSearch)
                    && Object.prototype.hasOwnProperty.call(r, 'wiki_url')
                    && r.wiki_url !== null
                ) {
                    addResultNode(ICONS.WIKI, r.display_text, r.wiki_url)
                }
                if (
                    [null, 'poedb'].includes(targetedSearch)
                    && Object.prototype.hasOwnProperty.call(r, 'poedb_url')
                    && r.poedb_url !== null
                ) {
                    addResultNode(ICONS.POEDB, r.display_text, r.poedb_url)
                }
                if (
                    [null, 'ninja'].includes(targetedSearch)
                    && Object.prototype.hasOwnProperty.call(r, 'ninja_url')
                    && r.ninja_url !== null
                ) {
                    addResultNode(ICONS.NINJA, r.display_text, r.ninja_url)
                }
                if (
                    [null, 'trade'].includes(targetedSearch)
                    && Object.prototype.hasOwnProperty.call(r, 'trade_url')
                    && r.trade_url !== null
                ) {
                    addResultNode(ICONS.TRADE, `Trade for ${r.display_text}`, r.trade_url)
                }
                if (
                    [null, 'tool'].includes(targetedSearch)
                    && Object.prototype.hasOwnProperty.call(r, 'tool_url')
                    && r.tool_url !== null
                ) {
                    addResultNode(ICONS.GOTO, `Open ${r.display_text}`, r.tool_url)
                }
            })
        }
    })

    searchInput.addEventListener('keydown', (event) => {
        if (event.keyCode == KEY_CODES.ARROW_DOWN) {
            event.preventDefault() // prevents text cursor from jumping around
            navigateResult(1)
        } else if (event.keyCode == KEY_CODES.ARROW_UP) {
            event.preventDefault() // prevents text cursor from jumping around
            navigateResult(-1)
        } else if (event.keyCode == KEY_CODES.ENTER) {
            event.preventDefault()
            if (selectedResult !== null) {
                selectedResult.click()
            }
        }
    })
}

makePalette(document.getElementById('search'), document.getElementById('resultlist'))
