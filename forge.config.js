module.exports = {
    packagerConfig: {
        asar: true,
        icon: 'assets/mirror',
        ignore: [
            // Python source code
            '^/data($|/)',
            // misc dev stuff
            '^/.github($|/)',
            '^/.idea($|/)',
            '^/.ruff_cache($|/)',
            '^/.vscode($|/)',
            '^/.venv($|/)',
            '^/venv($|/)',
            '^/.editorconfig$',
            '^/.eslintrc.json$',
            '^/src/main/.eslintrc.json$',
            '^/src/renderer/.eslintrc.json$',
            '^/.gitattributes$',
            '^/.gitignore$',
            '^/.npmrc$',
            '^/.ruff.toml$',
            '^/.stylelintrc.json$',
            '^/README.md$',
            '^/requirements.txt$',
            '^/requirements-dev.txt$',
        ],
    },
    rebuildConfig: {},
    makers: [
        {
            name: '@electron-forge/maker-zip',
            platforms: ['win32'],
        },
    ],
    plugins: [
        {
            name: '@electron-forge/plugin-auto-unpack-natives',
            config: {},
        },
    ],
}
