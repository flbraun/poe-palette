const { app, dialog, shell } = require('electron')
const semver = require('semver')
const https = require('https')

exports.checkForUpdates = () => {
    const currentVersion = app.getVersion()

    const reqOptions = {
        protocol: 'https:',
        host: 'api.github.com',
        path: '/repos/flbraun/poe-palette/releases/latest',
        headers: {
            'User-Agent': 'flbraun/poe-palette',
        },
    }

    https.get(reqOptions, (resp) => {
        let data = ''

        resp.on('data', (chunk) => {
            data += chunk
        })

        resp.on('end', () => {
            const respData = JSON.parse(data)
            const latestVersion = respData.tag_name
            const releasePage = respData.html_url

            if (semver.lt(semver.coerce(currentVersion), semver.coerce(latestVersion))) {
                let buttonClicked = dialog.showMessageBoxSync(null, {
                    type: 'info',
                    title: 'Update available!',
                    message: 'A new version of PoE Palette is available!',
                    detail: `${latestVersion} is available, you're running ${currentVersion}.\nOpen download page?`,
                    buttons: ['Yes', 'No'],
                })

                if (buttonClicked === 0) {
                    // 0 is index of 'Yes' button
                    shell.openExternal(releasePage)
                    app.quit()
                }
            }
        })
    })
}
