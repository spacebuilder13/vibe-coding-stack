# Domain: Payments

When to load: brief mentions billing, subscriptions, checkout, or paid features.

## Choose your gateway

| Gateway | Use when |
|---------|---------|
| **Razorpay** | India-first — UPI, cards, netbanking, wallets. Best for INR. |
| **Stripe** | International — global cards, Apple Pay, subscriptions. USD/multi-currency. |

For India-first apps: **Razorpay by default**.
For international or SaaS: **Stripe**.

## Razorpay

Connector: `razorpay` — see `registry/connectors.json`

```js
// Server: create order
const Razorpay = require('razorpay')
const rzp = new Razorpay({ key_id: process.env.RAZORPAY_KEY_ID, key_secret: process.env.RAZORPAY_KEY_SECRET })
const order = await rzp.orders.create({ amount: 49900, currency: 'INR', receipt: 'receipt_001' }) // amount in paise

// Client: open checkout
const rzpCheckout = new window.Razorpay({
  key: process.env.RAZORPAY_KEY_ID,
  order_id: order.id,
  handler: (response) => { /* verify on server */ }
})
rzpCheckout.open()
```

**Webhook verification:**
```js
const crypto = require('crypto')
const expectedSignature = crypto.createHmac('sha256', process.env.RAZORPAY_WEBHOOK_SECRET)
  .update(req.rawBody).digest('hex')
if (expectedSignature !== req.headers['x-razorpay-signature']) return res.status(400).end()
```

## Stripe

Connector: `stripe` — see `registry/connectors.json`

```js
import Stripe from 'stripe'
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY)

// Create checkout session
const session = await stripe.checkout.sessions.create({
  payment_method_types: ['card'],
  line_items: [{ price: 'price_xxx', quantity: 1 }],
  mode: 'subscription',
  success_url: `${YOUR_DOMAIN}/success`,
  cancel_url: `${YOUR_DOMAIN}/cancel`,
})
```

**Webhook verification:**
```js
const event = stripe.webhooks.constructEvent(req.rawBody, req.headers['stripe-signature'], process.env.STRIPE_WEBHOOK_SECRET)
```

## Standard payment API routes
- `POST /api/payment/create-order` — create Razorpay order or Stripe session
- `POST /api/payment/verify` — verify payment signature
- `POST /api/payment/webhook` — handle async events (subscription renewed, failed, etc.)

## Subscription states to handle
- `active` — user is paying, grant access
- `past_due` — payment failed, grace period
- `canceled` — revoke access
- `trialing` — free trial, track expiry

## Legal requirements (India)
- Display price inclusive of GST
- Provide invoice with GSTIN if B2B
- Refund policy must be visible before checkout
- Auto-renewal must be disclosed clearly

## Anti-patterns
- Verifying payment on client-side only (trivially bypassable)
- Not validating webhook signatures
- Storing card data (use Stripe/Razorpay tokenization — never touch raw card numbers)
- No idempotency keys on order creation (causes double-charges on retries)
