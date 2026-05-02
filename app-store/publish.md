# Publish Workflow

How to go from a deployed app to a registered entry in the app store.

## Step 1: Verify the deploy

- [ ] URL is live and loads correctly
- [ ] No console errors on load
- [ ] Auth flow works (if applicable)
- [ ] Mobile viewport correct (375px minimum)
- [ ] `/qa` has passed

## Step 2: PWA setup (for save-to-homescreen)

Every app in the store should be a PWA. Minimum viable PWA:

```json
// public/manifest.json
{
  "name": "App Name",
  "short_name": "ShortName",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#FBFAF6",
  "theme_color": "#1B1A17",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

```html
<!-- In <head> -->
<link rel="manifest" href="/manifest.json" />
<meta name="theme-color" content="#1B1A17" />
<meta name="mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="default" />
```

Icons needed: 192×192 and 512×512 PNG. Generate from the app's logo.

## Step 3: Register in STORE.md

Add a row to `app-store/STORE.md`:

```
| App Name | https://your-app.vercel.app | One-line description (struggling moment → what it does) | YYYY-MM-DD |
```

## Step 4: Update BUILD.md checklist

Mark the final checklist item in `BUILD.md`:
- [x] `app-store/STORE.md` updated

## Step 5: Commit

```bash
git add app-store/STORE.md BUILD.md
git commit -m "publish: register [App Name] in app store"
```

## App store shell (coming)

A PWA shell at `app-store/pwa-shell/` will render STORE.md as a browseable app grid with:
- Google Auth (Supabase)
- App tiles with icon, name, description
- "Add to homescreen" flow for each app
- Search/filter by domain
