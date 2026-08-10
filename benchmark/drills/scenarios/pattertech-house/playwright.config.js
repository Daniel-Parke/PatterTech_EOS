// @ts-check
const { defineConfig, devices } = require('@playwright/test');
const { pathToFileURL } = require('node:url');
const path = require('node:path');

// No server: the site is static files, so the tests open them directly.
const baseURL = pathToFileURL(path.join(__dirname, 'index.html')).href;

module.exports = defineConfig({
  testDir: './tests',
  use: {
    baseURL,
    ...devices['Desktop Chrome'],
  },
  reporter: [['list']],
});
