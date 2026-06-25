// Alberta Electoral Boundary Audit — user preferences (single encrypted cookie)
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Cookie: ab_audit_prefs (1 week, SameSite=Strict, Secure, path=/)
// Value:  AES-256-GCM ciphertext — base64(iv).base64(ciphertext)
// Plaintext format: pipe-separated key=value pairs, e.g. t=dark|i=1|s=m=minority&cx=0.5&…
// Keys:   t (theme: dark/light)       i (intro seen: 1)
//         s (last share view: a serialized URL query string, e.g. m=minority&f=pois&cx=…)
//         g (GPS region: lat,lng)     l (browser language: e.g. en-CA)
//
// Theme is also mirrored to localStorage['ab_pref_t'] so app.html can prevent
// FOUC synchronously without decrypting the cookie.

const COOKIE = 'ab_audit_prefs';
const KEY_B64 = 'YRQH2/GoqjVopQ+jKyRBKUYHDsnKe/Vg6DDrHHBr0gE=';

let _keyPromise: Promise<CryptoKey> | null = null;
function _importKey(): Promise<CryptoKey> {
	if (!_keyPromise) {
		const raw = Uint8Array.from(atob(KEY_B64), c => c.charCodeAt(0));
		_keyPromise = crypto.subtle.importKey('raw', raw, 'AES-GCM', false, ['encrypt', 'decrypt']);
	}
	return _keyPromise;
}

function _b64enc(buf: ArrayBuffer | Uint8Array): string {
	const bytes = buf instanceof Uint8Array ? buf : new Uint8Array(buf);
	return btoa(String.fromCharCode(...bytes));
}
function _b64dec(s: string): Uint8Array<ArrayBuffer> {
	return Uint8Array.from(atob(s), c => c.charCodeAt(0)) as Uint8Array<ArrayBuffer>;
}

async function _encrypt(text: string): Promise<string> {
	const key = await _importKey();
	const iv  = crypto.getRandomValues(new Uint8Array(12));
	const ct  = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, new TextEncoder().encode(text));
	return `${_b64enc(iv)}.${_b64enc(ct)}`;
}

async function _decrypt(encoded: string): Promise<string | null> {
	const dot = encoded.indexOf('.');
	if (dot < 0) return null;
	try {
		const key = await _importKey();
		const iv  = _b64dec(encoded.slice(0, dot));
		const ct  = _b64dec(encoded.slice(dot + 1));
		const pt  = await crypto.subtle.decrypt({ name: 'AES-GCM', iv }, key, ct);
		return new TextDecoder().decode(pt);
	} catch {
		return null;
	}
}

async function _parse(): Promise<Record<string, string>> {
	const m = document.cookie.match(/(?:^|;\s*)ab_audit_prefs=([^;]+)/);
	if (!m) return {};
	const plain = await _decrypt(decodeURIComponent(m[1]));
	if (!plain) return {};
	const out: Record<string, string> = {};
	for (const pair of plain.split('|')) {
		const eq = pair.indexOf('=');
		if (eq > 0) out[pair.slice(0, eq)] = pair.slice(eq + 1);
	}
	return out;
}

async function _write(prefs: Record<string, string>): Promise<void> {
	const plain = Object.entries(prefs).map(([k, v]) => `${k}=${v}`).join('|');
	const enc   = await _encrypt(plain);
	const exp   = new Date();
	exp.setTime(exp.getTime() + 7 * 24 * 60 * 60 * 1000); // 1 week
	const secure = location.protocol === 'https:' ? '; Secure' : '';
	document.cookie = `${COOKIE}=${encodeURIComponent(enc)}; expires=${exp.toUTCString()}; path=/; SameSite=Strict${secure}`;
}

async function _set(key: string, value: string | null): Promise<void> {
	const prefs = await _parse();
	if (value === null) delete prefs[key];
	else prefs[key] = value;
	await _write(prefs);
}

async function _get(key: string): Promise<string | null> {
	return (await _parse())[key] ?? null;
}

// ── Theme ─────────────────────────────────────────────────────────────────────
export async function getStoredTheme(): Promise<'dark' | 'light' | null> {
	const v = await _get('t');
	return v === 'dark' || v === 'light' ? v : null;
}

export async function storeTheme(theme: 'dark' | 'light'): Promise<void> {
	localStorage.setItem('ab_pref_t', theme);
	await _set('t', theme);
}

// ── Intro modal ───────────────────────────────────────────────────────────────
export async function hasSeenIntro(): Promise<boolean> {
	return (await _get('i')) === '1';
}

export async function markIntroSeen(): Promise<void> {
	await _set('i', '1');
}

// ── Last share view (session resume) ─────────────────────────────────────────
// Stored as a serialized URL query string (see share.ts serializeState).
export async function getLastCode(): Promise<string | null> {
	return (await _get('s')) || null;
}

export async function storeLastCode(code: string): Promise<void> {
	await _set('s', code);
}

// ── GPS region (10 km grid, 0.1° resolution) ──────────────────────────────────
export async function getStoredGps(): Promise<{ lat: number; lng: number } | null> {
	const v = await _get('g');
	if (!v) return null;
	const [lat, lng] = v.split(',').map(Number);
	if (isNaN(lat) || isNaN(lng)) return null;
	return { lat, lng };
}

export async function storeGps(lat: number, lng: number): Promise<void> {
	const rLat = Math.round(lat * 10) / 10;
	const rLng = Math.round(lng * 10) / 10;
	await _set('g', `${rLat},${rLng}`);
}

// ── Browser language ──────────────────────────────────────────────────────────
export async function getStoredLanguage(): Promise<string | null> {
	return (await _get('l')) || null;
}

export async function storeLanguage(lang: string): Promise<void> {
	await _set('l', lang);
}
