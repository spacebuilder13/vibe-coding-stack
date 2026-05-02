# Domain: Legal

When to load: app handles user data, payments, health/financial advice, or is public-facing.

## Minimum viable legal for a web app

Every public-facing app needs:
1. **Privacy Policy** — what data you collect, how you use it, how to delete it
2. **Terms of Service** — what users can and can't do, liability limits
3. **Cookie consent** — if using analytics (PostHog) or tracking cookies

## Privacy Policy — minimum content

```
What we collect: [email, session data, usage events, voice recordings if applicable]
Why we collect it: [to provide the service]
How long we keep it: [session duration / 30 days / user deletion on request]
Third parties: [Anthropic (Claude API), ElevenLabs (voice), PostHog (analytics), Supabase (auth)]
Your rights: [access, correction, deletion — email us at ...]
Contact: [your email]
```

## India-specific compliance

| Requirement | Rule |
|-------------|------|
| **DPDP Act 2023** | Consent before collecting personal data. Data minimisation. Right to erasure. |
| **IT Act 2000** | Intermediary rules if user-generated content. |
| **GST on digital services** | 18% GST applies to SaaS/digital products sold in India |
| **Financial advice disclaimer** | "This is not SEBI-registered investment advice" — required for any financial tool |
| **Insurance disclaimer** | "This is not IRDAI-registered insurance advice" — required (see project-insurance pattern) |
| **Consumer Protection Act** | Refund policy must be disclosed before purchase |

## Financial / insurance advisory disclaimer (from project-insurance)

```
Sandy is an AI tool for information purposes only.
It is not registered with IRDAI or SEBI.
No recommendations constitute financial or insurance advice.
Consult a registered advisor before making decisions.
```

## Healthcare disclaimer (if applicable)

```
This tool does not provide medical advice.
Consult a qualified healthcare professional for any health concerns.
```

## Cookie consent (minimal)

```js
// Show banner on first visit, store consent in localStorage
if (!localStorage.getItem('cookie-consent')) {
  showCookieBanner() // "We use analytics to improve the product. Accept / Decline"
}
// Only init PostHog after consent
if (localStorage.getItem('cookie-consent') === 'accepted') {
  posthog.init(...)
}
```

## GDPR (if serving EU users)

- Explicit consent before data collection
- Right to erasure: `DELETE /api/user/delete` route required
- Data processing agreement with Anthropic/Supabase/PostHog
- No data transfer outside EU without safeguards (standard contractual clauses)

## Checklist (per app)
- [ ] Privacy policy page at `/privacy`
- [ ] Terms page at `/terms`
- [ ] Cookie consent on analytics init
- [ ] Financial/insurance/health disclaimer if applicable
- [ ] Refund policy visible before checkout (if payments)
- [ ] GSTIN displayed on invoices (if B2B India)

## Anti-patterns
- Launching a financial or health tool without disclaimers
- Collecting email without a privacy policy link
- Enabling PostHog/analytics without cookie consent
- Storing voice recordings without explicit consent and a deletion mechanism
