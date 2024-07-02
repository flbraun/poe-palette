module.exports = {
    packagerConfig: {
        asar: true,
        prune: true,
        icon: 'assets/mirror',
        ignore: [
            // project files
            '.github',
            '.ruff_cache',
            '.idea',
            '.vscode',
            '.venv',
            'venv',
            '.editorconfig',
            '.eslintrc.json',
            'data/', // Python source code
            'data-.*.json',
            'src/main/.eslintrc.json',
            'src/windows/.eslintrc.json',
            '.gitattributes',
            '.gitignore',
            '.npmrc',
            '.pip-tools.toml',
            '.ruff.toml',
            '.stylelintrc.json',
            'README.md',
            'requirements.in',
            'requirements.txt',
            'requirements-dev.in',
            'requirements-dev.txt',
            // remove unnecessary files from the packaged node_modules, like test, source maps, type files, etc.
            /test/,
            /tests/,
            /\.spec\.js$/,
            /__tests__/,
            /\.test\.js$/,
            /\.map$/,
            /docs/,
            /docs/,
            /examples/,
            /@types/,
            /\.d\.ts$/,
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
