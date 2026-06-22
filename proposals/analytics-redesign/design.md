# Analytics Redesign — Design

Status: approved (brainstorm 2026-06-22). Supersedes the consent-gated flight-path telemetry.

## Goal
Answer three questions for the audit site, **without tracking individuals**:
1. **Reach & engagement** — how many people come, how deep they go, do they reach the findings.
2. **Content interest** — which findings / districts / chair-flagged POIs draw attention.
3. **Map-explorer usage** — which maps get compared, how deep people zoom, which districts they inspect, where they drop off.

Explicit **non-goals (v1):** sharing/virality lineage (deprioritized), per-person journeys, A/B testing, real-time.

## Privacy model — cookieless anonymous aggregate
- **No cookies, no localStorage id, no personal data persisted, no consent banner.**
- Unique-visitor counting uses the **Plausible technique**: a **daily-rotating salted hash of `IP + user-agent`**, computed **server-side only** (in the collector), irreversible, and **rotated every day** so a visitor cannot be tracked across days. The IP is never stored.
- Because nothing personal is retained, this is GDPR/PIPEDA-compatible **without consent**. The opt-in gate and the privacy banner are **removed**; the privacy policy is simplified to describe the cookieless aggregate model.

## Architecture
The site is **static** (GitHub Pages) — no server to see the IP — so collection goes through one piece of server-side infra:

```
browser  ──POST event──▶  Supabase Edge Function (collector)  ──▶  Supabase tables
                          (sees IP server-side, daily-hash,         (no IP, no PII)
                           rate-limit, validate, drop bots)
```

- **Collector = a Supabase Edge Function.** The only component that ever sees the IP. It: validates the event against an allow-list of names/props, computes `visitor_hash = sha256(daily_salt + ip + user_agent + 'alberta-audit')`, drops obvious bots, rate-limits, and inserts the anonymized row. `daily_salt` is a random secret rotated daily (a tiny scheduled job or derived from the date + a server secret).
- Browser sends events with `navigator.sendBeacon` (fire-and-forget, survives unload), to the Edge Function URL. No third party.

## Data model
- `analytics_events` — raw anonymized events: `{ id, ts, day (date), event_name (text), props (jsonb), visitor_hash (text), path (text) }`. RLS: **insert only via the Edge Function (service role); no public read.**
- `analytics_daily` — nightly rollup for fast dashboards: per `day` × `event_name` × selected prop dimensions → counts + unique-visitor counts (distinct `visitor_hash`). Built by a scheduled Supabase function (pg_cron) so the dashboard never scans raw rows.
- Retention: raw `analytics_events` pruned after ~60–90 days (rollups kept indefinitely).

## Event taxonomy (allow-listed)
- **Reach/engagement:** `pageview {path}`, `engaged {path, seconds_bucket}` (time-on-page bucket), `scroll_depth {path, pct_bucket}` (did they reach the findings?).
- **Content interest:** `section_view {section_id}` (report findings scrolled into view), `poi_open {id}`, `report_map_link {poi}`.
- **Map usage:** `explorer_open`, `map_toggle {map}`, `zoom_depth {bucket}`, `district_select {name}`, `layer_toggle {layer, on}`.

The deck explorer's existing `logEvent(...)` calls are re-pointed from the `telemetry` table to the new collector (`explorer_open`, `district_select`, `poi_*`).

## Dashboard — private, in-app
- A route (e.g. `/admin/analytics`), **not linked publicly**, **gated by Supabase Auth** (magic-link or password sign-in). RLS on the rollup tables permits reads **only** for the authenticated admin; the public never reads analytics.
- Views from `analytics_daily`: visitors & engagement over time; scroll-depth funnel to the findings; top report sections; explorer usage (map-version comparisons, zoom-depth distribution, most-inspected districts); drop-off.
- Charts rendered in-app from the aggregates (no third-party embed).

## Migration / retirement
1. Stand up the collector + tables + rollup (no UI change yet; verify events flow).
2. Re-point the deck explorer + report instrumentation to the collector.
3. Remove the consent gate, the flight-path machinery (`share.ts` telemetry path, `flushTelemetry`, the 30s interval), and the old `telemetry` table usage. Keep the share-code feature itself (UX), just not its analytics role.
4. Simplify the privacy policy.

## Open decisions for the plan
- `daily_salt` rotation mechanism (pg_cron job writing a secret row vs deriving from date + a Vault secret).
- Exact scroll/engagement thresholds and zoom buckets.
- Dashboard charting approach (hand-rolled SVG vs a tiny lib).
- Branch/merge order relative to `feat/deck-explorer-port` (which re-points `logEvent`).
