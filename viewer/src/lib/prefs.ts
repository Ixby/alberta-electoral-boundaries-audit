// Alberta Electoral Boundary Audit — user preferences (single cookie)
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Cookie: ab_audit_prefs (1 year, SameSite=Strict, path=/)
// Format: pipe-separated key=value pairs, e.g. c=yes|t=dark|i=1|s=alpine-badger-banff
// Keys:   c (consent: yes/no)         t (theme: dark/light)
//         i (intro seen: 1)           s (last share code: word-word-word)

const COOKIE = 'ab_audit_prefs';

function _parse(): Record<string, string> {
	const m = document.cookie.match(/(?:^|;\s*)ab_audit_prefs=([^;]+)/);
	if (!m) return {};
	const out: Record<string, string> = {};
	for (const pair of m[1].split('|')) {
		const eq = pair.indexOf('=');
		if (eq > 0) out[pair.slice(0, eq)] = pair.slice(eq + 1);
	}
	return out;
}

function _write(prefs: Record<string, string>): void {
	const val = Object.entries(prefs).map(([k, v]) => `${k}=${v}`).join('|');
	const exp = new Date();
	exp.setFullYear(exp.getFullYear() + 1);
	document.cookie = `${COOKIE}=${val}; expires=${exp.toUTCString()}; path=/; SameSite=Strict`;
}

function _set(key: string, value: string | null): void {
	const prefs = _parse();
	if (value === null) delete prefs[key];
	else prefs[key] = value;
	_write(prefs);
}

function _get(key: string): string | null {
	return _parse()[key] ?? null;
}

// ── Analytics consent ─────────────────────────────────────────────────────────
export function getStoredConsent(): 'yes' | 'no' | null {
	const v = _get('c');
	return v === 'yes' || v === 'no' ? v : null;
}

export function storeConsent(yes: boolean): void {
	_set('c', yes ? 'yes' : 'no');
}

// ── Theme ─────────────────────────────────────────────────────────────────────
export function getStoredTheme(): 'dark' | 'light' | null {
	const v = _get('t');
	return v === 'dark' || v === 'light' ? v : null;
}

export function storeTheme(theme: 'dark' | 'light'): void {
	_set('t', theme);
}

// ── Intro modal ───────────────────────────────────────────────────────────────
export function hasSeenIntro(): boolean {
	return _get('i') === '1';
}

export function markIntroSeen(): void {
	_set('i', '1');
}

// ── Last share code (session resume) ─────────────────────────────────────────
export function getLastCode(): string | null {
	return _get('s') || null;
}

export function storeLastCode(code: string): void {
	_set('s', code);
}
