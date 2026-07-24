# JR Smoke Zone — AI chat Worker

A tiny Cloudflare Worker that lets the website's chat bot talk to Claude, **without ever
putting the Anthropic API key in the public website**. The key lives as a Worker secret.

The site works **without** this Worker — the chat bot falls back to its built-in
deterministic answers. This Worker just upgrades it to real AI conversation.

- `worker.js` — the proxy. Origin allowlist, rate limit, turn/length caps, a
  tobacco-retailer system prompt, and a regex backstop that drops any price/guarantee.
- `wrangler.jsonc` — config. No secrets in it.

## What it costs
- **Cloudflare Worker:** free tier (100k requests/day) — free.
- **Claude API:** ~1–3¢ per conversation (model: Claude Haiku 4.5). Needs an Anthropic
  API account with prepaid credits. **Set a monthly spend cap** in the Anthropic Console.

## Deploy (one time, ~10 min)

You need: an Anthropic API key (console.anthropic.com → API keys) with a few dollars of
credit, and Node installed.

```bash
cd worker
npm i -g wrangler            # or: npx wrangler ...
wrangler login              # opens Cloudflare in your browser (use the account that owns jrsmokezone.com)
wrangler secret put ANTHROPIC_API_KEY   # paste your Anthropic key when prompted (never goes in git)
wrangler deploy             # prints the Worker URL, e.g. https://jrsmokezone-chat.<sub>.workers.dev
```

Then in the **Anthropic Console → Limits**, set a monthly **spend cap** (e.g. $10) so a
bad day can never surprise-bill you.

## Turn it on
Give the Worker URL to Claude Code (or set it yourself): in `build.py`, set
`WORKER = "https://jrsmokezone-chat.<sub>.workers.dev"`, then `python3 build.py`,
bump `CHATV`, and `git push origin master`. Until `WORKER` is set, the bot stays on its
free deterministic answers.

## Optional: rate limiting (recommended)
```bash
wrangler kv namespace create RATE_KV
```
Paste the returned id into `wrangler.jsonc` (uncomment the `kv_namespaces` block), then
`wrangler deploy` again. Caps each visitor IP to 20 messages / 10 min.

## Test
```bash
curl -s https://jrsmokezone-chat.<sub>.workers.dev/chat \
  -H 'content-type: application/json' -H 'origin: https://jrsmokezone.com' \
  -d '{"messages":[{"role":"user","content":"what are your hours?"}]}'
```
Should return `{"reply":"..."}`. A request with no/other `origin` returns 403 (that's the gate).

## Guardrails baked in
- **Origin allowlist** — only jrsmokezone.com / www / the github.io fallback may call it.
- **Price/guarantee backstop** — any reply with a dollar figure or "guarantee" is replaced
  with a "call for pricing" line, even if the model is jailbroken.
- **System prompt** — 21+ only, no health/medical claims, not a dispensary, not e-commerce,
  no invented stock/reviews.
- **Caps** — 16 turns, 1000 chars/message, optional 20 msgs/10min per IP.
