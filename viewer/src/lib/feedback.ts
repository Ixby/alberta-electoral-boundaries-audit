// Alberta Electoral Boundary Audit — feedback submission client
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Thin client for the `feedback-submit` Supabase Edge Function. The function
// runs with verify_jwt disabled and does its own protection (honeypot, length
// guards, daily-salted IP-hash rate limit, store-first persistence), so the
// browser sends no auth header — exactly like the analytics collector.
//
// Wire shape (must match the function):
//   { message, name?, email?, website?, context? }
// where `website` is the honeypot (must stay empty for real users) and
// `context` is a small object describing where the feedback came from.

import { PUBLIC_SUPABASE_URL } from '$env/static/public';

const ENDPOINT = `${PUBLIC_SUPABASE_URL}/functions/v1/feedback-submit`;

export interface FeedbackInput {
	message: string;
	name?: string;
	email?: string;
	/** Honeypot — bound to a hidden field; real submissions leave it empty. */
	website?: string;
	/** Where the feedback originated: { page, lang, path, ... }. */
	context?: Record<string, unknown>;
}

export type FeedbackResult =
	| { ok: true; id?: string }
	| { ok: false; reason: 'empty' | 'rate' | 'generic' };

/**
 * Submit feedback. Resolves with a tagged result the caller maps to a localized
 * message. Never throws: a network failure resolves to { ok:false, reason:'generic' }.
 */
export async function submitFeedback(input: FeedbackInput): Promise<FeedbackResult> {
	try {
		const res = await fetch(ENDPOINT, {
			method: 'POST',
			headers: { 'content-type': 'application/json' },
			body: JSON.stringify({
				message: input.message,
				name: input.name || undefined,
				email: input.email || undefined,
				website: input.website || undefined,
				context: input.context ?? {}
			})
		});

		if (res.ok) {
			const data = (await res.json().catch(() => ({}))) as { id?: string };
			return { ok: true, id: data.id };
		}
		if (res.status === 429) return { ok: false, reason: 'rate' };
		if (res.status === 400) {
			const data = (await res.json().catch(() => ({}))) as { error?: string };
			if (data.error === 'empty') return { ok: false, reason: 'empty' };
		}
		return { ok: false, reason: 'generic' };
	} catch {
		return { ok: false, reason: 'generic' };
	}
}
