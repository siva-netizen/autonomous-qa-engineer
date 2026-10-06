import { test, expect } from '@playwright/test';

test.describe('Checkout Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Setup: Add item to cart to enable checkout
    await page.goto('/');
    await page.getByTestId('product-card-prod-001').getByRole('button', { name: /add to cart/i }).click();
    await page.getByTestId('cart-link').click();
    await page.getByRole('link', { name: /checkout/i }).click();
  });

  test('TC-CHECKOUT-001: Successful Checkout Flow', async ({ page }) => {
    await page.getByTestId('name-input').fill('John Doe');
    await page.getByTestId('address-input').fill('123 Main St');
    await page.getByTestId('city-input').fill('Anytown');
    await page.getByTestId('zip-input').fill('12345');
    await page.getByTestId('card-input').fill('1234567812345678');
    await page.getByTestId('expiry-input').fill('12/25');
    await page.getByTestId('cvv-input').fill('123');
    await page.getByTestId('submit-order-button').click();
    
    await expect(page).toHaveURL(/.*order-confirmation/);
    await expect(page.getByTestId('order-id')).toContainText('ORD-');
  });

  test('TC-CHECKOUT-002: Checkout Validation Errors', async ({ page }) => {
    await page.getByTestId('submit-order-button').click();
    await expect(page.getByTestId('error-message')).toBeVisible();
  });

  test('TC-CHECKOUT-003: Invalid Payment Format Validation', async ({ page }) => {
    await page.getByTestId('name-input').fill('John Doe');
    await page.getByTestId('card-input').fill('123');
    await page.getByTestId('submit-order-button').click();
    await expect(page.getByTestId('payment-error')).toBeVisible();
  });
});
