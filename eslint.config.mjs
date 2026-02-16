import { includeIgnoreFile } from '@eslint/compat'
import js from '@eslint/js'
import { defineConfig, globalIgnores } from 'eslint/config'
import globals from 'globals'
import { fileURLToPath } from 'node:url'

const gitignorePath = fileURLToPath(new URL('.gitignore', import.meta.url))

export default defineConfig([
    includeIgnoreFile(gitignorePath), // never lint files matched by .gitignore
    globalIgnores(['**/*.min.*js']), // never lint minified files
    {
        files: ['**/*.{js,cjs}'],
        plugins: { js },
        extends: ['js/recommended'],
        languageOptions: {
            ecmaVersion: 'latest',
            sourceType: 'commonjs',
            globals: { ...globals.node },
        },
    },
    {
        files: ['**/*.mjs'],
        plugins: { js },
        extends: ['js/recommended'],
        languageOptions: {
            ecmaVersion: 'latest',
            sourceType: 'module',
            globals: { ...globals.node },
        },
    },
    {
        // electron renderer files
        files: ['src/windows/**/*.js'],
        plugins: { js },
        extends: ['js/recommended'],
        languageOptions: {
            ecmaVersion: 'latest',
            sourceType: 'script',
            globals: { ...globals.browser },
        },
    },
])
