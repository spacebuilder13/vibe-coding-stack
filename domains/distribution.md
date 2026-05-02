# Domain: Distribution

When to load: brief mentions getting the app to users — SEO, email, content, social, AEO.

## What distribution covers
- **SEO** — search discoverability, prerender, schema markup
- **Email** — transactional (Resend), newsletters, post-session summaries
- **Content** — blog posts, AEO (answer engine optimisation), voice search
- **Social** — sharing, OG tags, WhatsApp previews

## Email — Resend

Connector: `resend` — see `registry/connectors.json`

```js
import { Resend } from 'resend'
const resend = new Resend(process.env.RESEND_API_KEY)

await resend.emails.send({
  from: 'Sandy <sandy@yourdomain.com>',
  to: userEmail,
  subject: 'Your insurance summary',
  html: '<p>Here is your summary...</p>'
})
```

**Domain verification required** — add DNS records in Resend dashboard.
Pattern from supperclubbing: `supperclubbing.in` as verified domain.

**Use cases:**
- Post-session summary (project-insurance pattern)
- Email opt-in confirmation
- Onboarding sequence trigger
- Weekly coaching report (project-sandy pattern)

## SEO — Vite prerender

From supperclubbing — works for React + Vite SPAs:

```js
// vite.config.ts
import { vitePrerenderPages } from './plugins/vite-plugin-prerender-pages'
export default { plugins: [vitePrerenderPages()] }
```

**Blog validation script** (`npm run validate:blog`):
- Checks slugs, hero images, sitemap coverage
- Run before every deploy

## Schema markup (from supperclubbing)

```tsx
// ArticleSchema.tsx
<script type="application/ld+json">{JSON.stringify({
  "@context": "https://schema.org",
  "@type": "Article",
  headline: post.title,
  datePublished: post.date,
  author: { "@type": "Person", name: "spacebuilder13" }
})}</script>
```

Also: `OrganizationSchema.tsx` for brand-level markup.

## AEO (Answer Engine Optimisation)
- Write content as direct answers to questions (for AI search, Perplexity, etc.)
- Lead with the answer, not the preamble
- Use structured headers (H2 = question, body = answer)
- Include schema markup for FAQ, HowTo, Article types

## OG + social tags
```html
<meta property="og:title" content="..." />
<meta property="og:description" content="..." />
<meta property="og:image" content="..." />
<meta property="twitter:card" content="summary_large_image" />
```

## Anti-patterns
- Deploying without OG tags (WhatsApp/Slack previews will be blank)
- SPA without prerender (Google can't index it reliably)
- Email without domain verification (lands in spam)
- Buying backlinks or gaming SEO — build for AEO instead
