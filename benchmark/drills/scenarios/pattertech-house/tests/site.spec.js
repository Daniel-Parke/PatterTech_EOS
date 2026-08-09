// @ts-check
const { test, expect } = require('@playwright/test');

test('the page loads with its chrome', async ({ page }) => {
  await page.goto('');
  await expect(page).toHaveTitle(/PatterTech/);
  await expect(page.locator('header.chrome')).toBeVisible();
  await expect(page.locator('main#page')).toHaveCount(1);
});

test('nothing scrolls sideways on a phone', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto('');
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - window.innerWidth);
  expect(overflow).toBeLessThanOrEqual(0);
});
