import { test, expect } from '@playwright/test';

test.describe('ShopDemo Cart and Checkout', () => {
  test('TC-CART-001: Update and Remove Cart Items', async ({ page }) => {
    await page.goto('/products/prod-001');
    await page.getByTestId('add-to-cart-button').click();
    await page.goto('/cart');
    
    const quantityInput = page.getByTestId('cart-item-quantity-cart-1');
    await quantityInput.fill('3');
    await expect(page.getByTestId('cart-total')).toContainText('$239.97');
    
    await page.getByRole('button', { name: /remove/i }).click();
    await expect(page.getByText(/your cart is empty/i)).toBeVisible();
  });

  test('TC-CHECKOUT-001: Checkout Field Validation', async ({ page }) => {
    await page.goto('/products/prod-001');
    await page.getByTestId('add-to-cart-button').click();
    await page.goto('/checkout');
    
    await page.getByRole('button', { name: /submit/i }).click();
    await expect(page.getByTestId('error-email')).toBeVisible();
    await expect(page.getByTestId('error-zip')).toBeVisible();
  });

  test('TC-CHECKOUT-002: Successful Order Submission', async ({ page }) => {
    await page.goto('/products/prod-001');
    await page.getByTestId('add-to-cart-button').click();
    await page.goto('/checkout');
    
    await page.getByLabel(/email/i).fill('test@example.com');
    await page.getByLabel(/zip/i).fill('12345');
    await page.getByLabel(/card/i).fill('1234567812345678');
    await page.getByLabel(/expiry/i).fill('12/25');
    await page.getByLabel(/cvv/i).fill('123');
    
    await page.getByRole('button', { name: /submit/i }).click();
    await expect(page).toHaveURL(/.*order-confirmation/);
    await expect(page.getByTestId('order-id')).toBeVisible();
  });
});
