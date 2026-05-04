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

---

## Publishing a new app

See `app-store/publish.md` for the full workflow.

Short version:
1. Deploy to Vercel → confirm URL is live
2. `/qa` passes
3. Add row to the table above
4. If it's a PWA: confirm `manifest.json` + service worker are in place
