# ShopDemo Inspection and Baseline

## Target identity

- Repository: `https://github.com/ettaverse/dummy-ecommerce`
- Local path: `./shopdemo/` (ignored by the QA repository)
- Revision: `ac0adf4`
- Runtime: Next.js `16.2.2`, React `19.2.4`, TypeScript, MSW `2.13.1`
- Base URL: `http://localhost:3000`
- Backend: browser-side MSW; no real backend dependency

## Startup

```bash
cd shopdemo
npm install
npm run dev
```

The server started successfully with Next.js/Turbopack and returned HTTP 200 for `/`.

## Routes inspected

| Route | Behavior |
|---|---|
| `/` | Product listing, search, category filter, price sort |
| `/products/:id` | Product detail, stock state, quantity, add-to-cart |
| `/cart` | Cart items, quantity controls, remove, total, checkout link |
| `/checkout` | Shipping/payment validation and order submission |
| `/order-confirmation?orderId=...` | Confirmation and order ID |
| `/login` | Seeded-user authentication and invalid-credential handling |
| `/signup` | New-user validation and in-memory registration |

## Deterministic test data

- 14 products with stable IDs `prod-001` through `prod-014`.
- `prod-001` is Wireless Headphones, priced at `$79.99`, in stock.
- `prod-008` is Wool Beanie and is deliberately out of stock.
- Seeded accounts are defined in `src/data/users.json`; the baseline used `demo@shopdemo.com` / `Demo@123`.
- Cart state is held in the MSW handler and resets when the worker is reloaded.
- Auth tokens are stored in `localStorage` under `shopdemo_auth_token`.

## Stable selectors

The target provides `data-testid` selectors for listing, filters, product details, cart controls, checkout fields/errors, order confirmation, and authentication. The first test uses:

- `product-count`
- `product-card-prod-001`
- `quantity-input`
- `add-to-cart-button`
- `added-notification`
- `cart-count`
- `cart-link`
- `cart-item-cart-1`
- `cart-item-quantity-cart-1`
- `cart-total`

Selectors were verified in the implementation and in a live browser smoke run; they were not guessed.

## Mock API surface

MSW handlers implement:

- `GET /api/products?search=&category=&sort=`
- `GET /api/products/:id`
- `GET /api/cart`
- `POST /api/cart`
- `PATCH /api/cart/:id`
- `DELETE /api/cart/:id`
- `POST /api/checkout`
- `POST /api/auth/signup`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/me`

Checkout validates required shipping fields, email, five-digit ZIP, 16-digit card number, `MM/YY` expiry, and three/four-digit CVV. Successful checkout clears the cart and returns an `ORD-<timestamp>` order ID.

## Live baseline evidence

The real Chromium smoke run passed these nine flows:

1. Product listing: 14 products rendered.
2. Search: `Wireless` returned `prod-001`.
3. Category filter: Electronics returned four products.
4. Price sort: ascending order placed `prod-009` first.
5. Product detail: added two Wireless Headphones.
6. Cart quantity: increased quantity to three; total became `$239.97`.
7. Empty checkout validation: required field errors rendered.
8. Successful checkout: order confirmation and order ID rendered.
9. Invalid login, valid login, and logout succeeded.

Evidence files are ignored local artifacts:

- `artifacts/shopdemo-baseline/home.png`
- `artifacts/shopdemo-baseline/final-signed-out.png`
- `artifacts/shopdemo-baseline/baseline-trace.zip`

The browser reported one `401 Unauthorized` console error during unauthenticated session restoration (`GET /api/auth/me` without a token). This is expected for the signed-out baseline. No network requests failed.

## Target health findings

- `npm run build`: passed; all expected routes compiled and generated.
- `npm run lint`: failed on two React `set-state-in-effect` errors in `CartContext.tsx` and `useProducts.ts`; there were also four image/worker warnings. These are pre-existing target findings, not changes made by the QA repository.
- `npm install`: reported 15 dependency audit findings in the target tree. No automatic fix was applied because dependency upgrades could alter the reproducible target.
- Next.js emitted a workspace-root warning because both the QA repository and ignored target have lockfiles. This does not prevent local execution.

## First executable QA flow

`SHOP-BASELINE-001 / TC-001: Browse and add a product to cart`

```text
Open /
  → assert 14 products
  → open product-card-prod-001
  → set quantity to 2
  → add to cart
  → assert added notification and cart count 2
  → open cart
  → assert item quantity 2 and total $159.98
```

This flow is implemented as a baseline Playwright test in `tests/e2e/shopdemo-baseline.spec.ts`. It executed successfully with `npm run test:e2e -- --project=chromium`: 1 test passed in 1.4 seconds. It is an inspected-target test, not yet an LLM-generated test; generation and execution pipeline integration are the next implementation step.
