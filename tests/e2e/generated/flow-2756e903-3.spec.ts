import { test, expect } from '@playwright/test';
test('generated smoke', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/.+/);
});
