import { expect, test } from '@playwright/test';

test('[SHOP-BASELINE-001][TC-001] browse and add a product to cart', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByRole('heading', { name: 'Products' })).toBeVisible();
  await expect(page.getByTestId('product-count')).toHaveText('14 products found');

  await page.getByTestId('product-card-prod-001').click();
  await expect(page).toHaveURL(/\/products\/prod-001$/);
  await expect(page.getByTestId('product-name')).toHaveText('Wireless Headphones');

  await page.getByTestId('quantity-input').fill('2');
  await page.getByTestId('add-to-cart-button').click();

  await expect(page.getByTestId('added-notification')).toBeVisible();
  await expect(page.getByTestId('cart-count')).toHaveText('2');

  await page.getByTestId('cart-link').click();
  await expect(page).toHaveURL(/\/cart$/);
  await expect(page.getByTestId('cart-item-cart-1')).toBeVisible();
  await expect(page.getByTestId('cart-item-quantity-cart-1')).toHaveText('2');
  await expect(page.getByTestId('cart-total')).toHaveText('$159.98');
});
