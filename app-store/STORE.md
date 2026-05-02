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

---

## Publishing a new app

See `app-store/publish.md` for the full workflow.

Short version:
1. Deploy to Vercel → confirm URL is live
2. `/qa` passes
3. Add row to the table above
4. If it's a PWA: confirm `manifest.json` + service worker are in place
