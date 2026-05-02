# Domain: LLM

When to load: using Claude API, choosing models, managing costs, prompt caching.

## Model routing (default)

| Task | Model | Approx cost |
|------|-------|-------------|
| Routing, classification, simple edits | `claude-haiku-4-5-20251001` | ~$0.0008/1K input |
| Most work — code, analysis, writing | `claude-sonnet-4-6` | ~$0.003/1K input |
| Deep architecture, hard reasoning | `claude-opus-4-6` | ~$0.015/1K input |

Default to Sonnet. Use Haiku for routing steps. Use Opus only when the problem genuinely requires deep reasoning.
**Expected savings from routing: ~51% vs uniform Sonnet.**

## Prompt caching

Use for: SOUL.md, HEARTBEAT.md, STACK.md — stable context that doesn't change mid-session.
- Cache write: 1.25x base input price (5-min) or 2x (1-hour)
- Cache read: 0.1x base input price (**90% savings**)
- Break-even: 1 read (5-min cache), 2 reads (1-hour cache)

## Tiered context loading (76% token reduction)

- **Tier 0** (~650 tokens, always loaded, cached): SOUL.md + HEARTBEAT.md + STACK.md
- **Tier 1** (load per session): AGENTS.md + PROGRAM.md + BUILD.md
- **Tier 2** (load per domain when routed): `domains/<name>.md`
- **Tier 3** (fetch JIT when executing): `registry/*.json`, skill bodies

Never load all domains upfront. Route first, then load.

## Shared Claude client (reuse from project-sandy)

```js
// api/_lib/anthropic.js
import Anthropic from '@anthropic-ai/sdk'
const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY })

export async function chat({ model = 'claude-sonnet-4-6', system, messages, maxTokens = 1024 }) {
  return client.messages.create({ model, system, messages, max_tokens: maxTokens })
}
```

## Standard API route pattern

```js
// api/chat-generate.js
export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end()
  const { message, sessionId } = req.body
  // validate, call Claude, log tokens, return
}
```

## LLM output validation
- Validate structure (JSON schema), not content
- Never write unvalidated LLM output to database
- Use confidence tags for uncertain spans
- Evaluator-optimizer loop when quality matters

## Anthropic agent patterns (reference)
1. **Augmented LLM** — retrieval + tools + memory (default)
2. **Prompt chaining** — sequential steps, each builds on last
3. **Routing** — classify input → specialized downstream
4. **Parallelization** — independent subtasks run simultaneously
5. **Orchestrator-workers** — orchestrator delegates, workers execute
6. **Evaluator-optimizer** — generator + reviewer in loop

Start simple. Add orchestration only when simpler approach fails.

## Anti-patterns
- Using Opus for tasks Haiku can handle
- Loading all context upfront instead of JIT
- No token ledger — flying blind on costs
- Trusting LLM output without schema validation
- Autonomous loops without a human gate
