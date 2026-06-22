// Alberta Electoral Boundary Audit — client-side analytics SDK
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Cookieless, anonymous, fire-and-forget analytics. Every event is POSTed to the
// `analytics-collect` Supabase Edge Function, which validates it against a strict
// allow-list, drops bots, and server-side-hashes IP+UA into a daily-rotating
// visitor hash. The browser sends NO identifying information — just the event
// name, an optional top-level `path`, and an optional `props` object whose keys
// the server filters down to the allow-listed set for that event.
//
// Wire shape (must match the collector's allow-list EXACTLY):
//   { event_name, path?, props? }
// where `path` is the TOP-LEVEL envelope field (the collector reads body.path,
// never props.path) and `props` carries the per-event dimensions:
//   pageview        { }                              + path
//   engaged         { seconds_bucket }               + path
//   scroll_depth    { pct_bucket }                   + path
//   section_view    { section_id }
//   poi_open        { id }
//   report_map_link { poi }
//   explorer_open   { }
//   map_toggle      { map }
//   zoom_depth      { bucket }
//   district_select { name }
//   layer_toggle    { layer, on }
//
// Everything here is browser-only and never throws: during SSR / prerender
// `track` no-ops, and every network failure is swallowed. There is no consent
// gate — the privacy model is the server-side cookieless aggregate, so no
// personal data ever leaves the browser.

import { browser } from '$app/environment';
import { PUBLIC_SUPABASE_URL } from '$env/static/public';

const COLLECTOR = `${PUBLIC_SUPABASE_URL}/functions/v1/analytics-collect`;

// ── Core send ────────────────────────────────────────────────────────────────
// Fire-and-forget. Prefers navigator.sendBeacon (survives page unload, the case
// `engaged` cares about) and falls back to fetch with keepalive. No auth / apikey
// header is needed — the collector runs with verify_jwt disabled. Never throws.

export function track(event_name: string, props?: Record<string, unknown>, path?: string): void {
	if (!browser) return;
	try {
		const body = JSON.stringify({ event_name, props, path });
		// sendBeacon is the primary path: it is queued by the browser and survives
		// the document being torn down (pagehide / visibilitychange→hidden), which
		// is exactly when the `engaged` event fires.
		if (typeof navigator !== 'undefined' && typeof navigator.sendBeacon === 'function') {
			const blob = new Blob([body], { type: 'application/json' });
			if (navigator.sendBeacon(COLLECTOR, blob)) return;
		}
		// Fallback: keepalive fetch so an in-flight request can still complete past
		// unload. Swallow every rejection — analytics must never surface an error.
		void fetch(COLLECTOR, {
			method: 'POST',
			headers: { 'content-type': 'application/json' },
			body,
			keepalive: true
		}).catch(() => {});
	} catch {
		// Any synchronous failure (serialization, missing APIs) is swallowed.
	}
}

// ── Convenience ──────────────────────────────────────────────────────────────

export function pageview(path: string = browser ? location.pathname : '/'): void {
	track('pageview', undefined, path);
}

// ── Pure bucketing helpers (unit-tested) ─────────────────────────────────────

// Scroll depth → coarse milestone bucket. Reports the highest milestone the user
// has reached: <25 → 0 (not a milestone), then 25 / 50 / 75 / 100.
export function scrollPctBucket(pct: number): number {
	if (pct >= 100) return 100;
	if (pct >= 75) return 75;
	if (pct >= 50) return 50;
	if (pct >= 25) return 25;
	return 0;
}

// Visible seconds-on-page → coarse engagement bucket. Floors to the largest
// threshold not exceeding `s`: 0 / 5 / 15 / 30 / 60 / 120 / 300.
const SECONDS_THRESHOLDS = [5, 15, 30, 60, 120, 300] as const;
export function secondsBucket(s: number): number {
	let bucket = 0;
	for (const t of SECONDS_THRESHOLDS) {
		if (s >= t) bucket = t;
		else break;
	}
	return bucket;
}

// Tile level (0–10) → small human label for the zoom-depth distribution. The
// explorer's tile level is the discrete zoom signal already computed each paint.
export function zoomBucket(level: number): string {
	if (level <= 1) return 'province';
	if (level <= 3) return 'region';
	if (level <= 5) return 'city';
	if (level <= 7) return 'district';
	return 'street';
}

// ── Engagement instrumentation ───────────────────────────────────────────────
// Sets up scroll-depth milestones + accumulated-visible-time reporting for a
// page. Returns a cleanup fn that detaches listeners and flushes nothing (the
// engaged event is flushed by the unload listeners themselves). Safe no-op in SSR.

export function initEngagement(path: string): () => void {
	if (!browser) return () => {};

	// ── Scroll depth: fire each crossed milestone once ──────────────────────────
	const firedBuckets = new Set<number>();
	function scrollPct(): number {
		const doc = document.documentElement;
		const scrollable = doc.scrollHeight - doc.clientHeight;
		if (scrollable <= 0) return 100; // page shorter than viewport → fully seen
		return Math.min(100, Math.round(((window.scrollY || 0) / scrollable) * 100));
	}
	function onScroll(): void {
		const bucket = scrollPctBucket(scrollPct());
		if (bucket > 0 && !firedBuckets.has(bucket)) {
			firedBuckets.add(bucket);
			track('scroll_depth', { pct_bucket: bucket }, path);
		}
	}

	// ── Engaged time: accumulate seconds the page is actually visible ───────────
	let accumulatedMs = 0;
	let lastVisibleAt: number | null =
		document.visibilityState === 'visible' ? Date.now() : null;
	let engagedFired = false;

	function accumulate(): void {
		if (lastVisibleAt !== null) {
			accumulatedMs += Date.now() - lastVisibleAt;
			lastVisibleAt = null;
		}
	}
	function flushEngaged(): void {
		accumulate();
		const seconds = Math.round(accumulatedMs / 1000);
		const bucket = secondsBucket(seconds);
		// Only report once per page life, and only when a meaningful bucket is hit,
		// so a hidden-on-arrival tab doesn't emit a 0-second engaged event.
		if (engagedFired || bucket <= 0) return;
		engagedFired = true;
		track('engaged', { seconds_bucket: bucket }, path);
	}
	function onVisibility(): void {
		if (document.visibilityState === 'hidden') {
			flushEngaged();
		} else if (lastVisibleAt === null) {
			lastVisibleAt = Date.now();
		}
	}

	window.addEventListener('scroll', onScroll, { passive: true });
	document.addEventListener('visibilitychange', onVisibility);
	window.addEventListener('pagehide', flushEngaged);
	// Fire an initial scroll check (covers short pages / restored scroll position).
	onScroll();

	return () => {
		window.removeEventListener('scroll', onScroll);
		document.removeEventListener('visibilitychange', onVisibility);
		window.removeEventListener('pagehide', flushEngaged);
	};
}

// ── Section visibility ───────────────────────────────────────────────────────
// Fire `section_view {section_id}` the first time each named element scrolls into
// view. Returns a cleanup fn. Safe no-op in SSR and where IntersectionObserver is
// unavailable.

export function observeSections(ids: string[]): () => void {
	if (!browser || typeof IntersectionObserver === 'undefined') return () => {};

	const seen = new Set<string>();
	const observer = new IntersectionObserver(
		(entries) => {
			for (const entry of entries) {
				if (!entry.isIntersecting) continue;
				const id = entry.target.id;
				if (id && !seen.has(id)) {
					seen.add(id);
					track('section_view', { section_id: id });
					observer.unobserve(entry.target);
				}
			}
		},
		{ threshold: 0.25 }
	);

	for (const id of ids) {
		const el = document.getElementById(id);
		if (el) observer.observe(el);
	}

	return () => observer.disconnect();
}
