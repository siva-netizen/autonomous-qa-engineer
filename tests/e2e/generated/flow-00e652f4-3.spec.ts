import { test, expect } from '@playwright/test';

test.describe('ShopDemo Cart Functionality (REQ-RA-001)', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('TC-CART-001: Add single product to cart', async ({ page }) => {
    await page.getByTestId('product-card-prod-001').click();
    await page.getByTestId('quantity-input').fill('1');
    await page.getByTestId('add-to-cart-button').click();
    await expect(page.getByTestId('added-notification')).toBeVisible();
    await expect(page.getByTestId('cart-count')).toHaveText('1');
  });

  test('TC-CART-002: Verify cart total calculation for multiple items', async ({ page }) => {
    // Setup: Add 2 units
    await page.getByTestId('product-card-prod-001').click();
    await page.getByTestId('quantity-input').fill('2');
    await page.getByTestId('add-to-cart-button').click();
    
    await page.getByTestId('cart-link').click();
    await expect(page.getByTestId('cart-item-quantity-cart-1')).toHaveValue('2');
    await expect(page.getByTestId('cart-total')).toContainText('$159.98');
  });

  test('TC-CART-004: Update quantity in cart', async ({ page }) => {
    // Setup: Add 1 unit
    await page.getByTestId('product-card-prod-001').click();
    await page.getByTestId('add-to-cart-button').click();
    
    await page.getByTestId('cart-link').click();
    await page.getByTestId('cart-item-quantity-cart-1').fill('3');
    await expect(page.getByTestId('cart-total')).toContainText('$239.97');
  });
});
