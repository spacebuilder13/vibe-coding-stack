# App Store

Personal web app catalog. Each app is a PWA — save to homescreen on Android/iOS.
Auth: Google login via Supabase.

---

## Apps

| Name | URL | Description | Added |
|------|-----|-------------|-------|
| Sandy — Insurance Advisor | https://project-insurance.vercel.app/insurance-day1 | India's first no-commission AI insurance advisor. Intake + conversation + briefing. | 2026-04-28 |
| Supperclubbing | https://supperclubbing.vercel.app | Supper club signup, management, and marketing blog. | 2026-04-28 |
| Project OB — BPS Advisory | https://project-ob.vercel.app | Financial advisory dashboard for Bansali Packing Services. | 2026-04-28 |
| CoinQuest — Expense Tracker | https://rawcdn.githack.com/spacebuilder13/vibe-coding-stack/88afcfaf5304f16218da68f757e5b1f74a03236e/apps/expense-tracker/index.html | Gamified daily expense tracker — log expenses, earn XP, unlock 20 achievements, get weekly insights. | 2026-05-04 |
| Jain Menu | https://jain-menu.vercel.app | Daily Jain recipe picker. Weather + novelty + price scored. 3 options daily with YT shorts. WhatsApp share to cook. | 2026-05-03 |
| Om Shanti × ZMS | https://project-om-shanti.vercel.app | B2B partnership landing + sample Om Shanti Finserv advisory site. NLM-grounded M1. | 2026-05-24 |
| Max Spare — AI Discovery Hub | https://project-max-spare.vercel.app | Zen discovery hub for Asia's largest seal manufacturer. 10 opportunity modules + live chat. Passphrase-gated; all data illustrative. | 2026-05-31 |
| OSF Phase 1 — Pod | https://zms-osf-phase-1.vercel.app | Insurance cases gallery + harness field guide for Utsav + Pooja. `/learn` `/cases` `/campaign`. | 2026-06-15 |
| OSF Client Deck | https://findow-phase1.vercel.app | Password-gated Phase 1 narrative deck. `project-om-shanti/apps/findow-phase1`. | 2026-06-17 |
| Project Royale | https://project-royale.vercel.app | Operations blueprint for rotogravure printing + pouch packaging. Passphrase-gated external V1. | 2026-06-17 |
| Ember — case study | https://ember.atomships.space | One Ember door on atomships.space. Role: living case study / S&A understanding. Live site still Smart Container until later. Repo: spacebuilder13/ember-ecosystem. Vercel atomships-ember. Public + noindex. | 2026-08-14 |
| Ember — community hub | https://project-ember-ten.vercel.app | Linked client prototype (recipes, plan, shop) — not an atomships subdomain. Kitchen: spacebuilder13/project-ember apps/hub. Vercel project-ember. Public + noindex. | 2026-08-25 |
| BDV — engagement brief | https://bdv.atomships.space | Passphrase-gated 3-day brief for Harsh × Yash. Static HTML, public + noindex. Kitchen: spacebuilder13/atomships. Until DNS: https://atomships-bdv.vercel.app | 2026-08-15 |
| Spaceships & Atoms — homepage | https://atomships.space | Public noindex film. Static HTML. Kitchen: spacebuilder13/atomships apps/www. Until DNS: https://atomships-www.vercel.app | 2026-08-16 |

---

## Publishing a new app

See `app-store/publish.md` for the full workflow.

Short version:
1. Deploy to Vercel → confirm URL is live
2. `/qa` passes
3. Add row to the table above
4. If it's a PWA: confirm `manifest.json` + service worker are in place
