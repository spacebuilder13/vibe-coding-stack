# Domain: Analytics

When to load: setting up PostHog, defining events, tracking token costs, observability.

## PostHog (product analytics)

Connector: `posthog` — see `registry/connectors.json`

**Standard 12 event types (from project-insurance):**
1. `session_start` — user opens app
2. `briefing_started` — intake flow begins
3. `briefing_completed` — intake flow done
4. `chat_message_sent` — user sends message
5. `voice_transcription_started` — STT initiated
6. `voice_response_played` — TTS played
7. `doc_uploaded` — file upload
8. `quiz_started` — quiz initiated
9. `quiz_completed` — quiz done
10. `contact_submitted` — email opt-in
11. `session_ended` — user exits
12. `error_occurred` — any error with context

**Setup:**
```js
import posthog from 'posthog-js'
posthog.init(process.env.POSTHOG_API_KEY, { api_host: process.env.POSTHOG_HOST })
posthog.capture('event_name', { property: 'value' })
```

## Token usage ledger (Claude API cost tracking)

Reuse from `project-sandy/api/_lib/token-usage-ledger.js`

Tracks per session:
- Input tokens
- Output tokens
- Model used
- Estimated cost (USD)
- Session ID

Log on every API call. Review weekly to catch runaway costs.

## Ingest v3 observability (from boards/)
- Run manifest — what ran, when, outcome
- Decision trace — router confidence + choices
- Metrics — latency, tokens, corrections
- Eval scores — quality + drift checks

## Anti-patterns
- Tracking everything without a defined event taxonomy
- Ignoring token costs until the bill arrives
- No baseline before A/B testing
- PostHog in Vercel Functions without batching (adds latency)
