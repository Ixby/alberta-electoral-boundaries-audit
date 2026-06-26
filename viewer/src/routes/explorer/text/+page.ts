// Alberta Electoral Boundary Audit — accessible text version of the map explorer.
// Prerender-friendly data load: fetch the three district indexes through the
// SvelteKit-provided `fetch` so their contents are INLINED into the prerendered
// HTML. The route is fully static — no WebGL, no map-state coupling.
//
// © Will Conner 2026
// Text/content: CC BY-NC-SA 4.0 <https://creativecommons.org/licenses/by-nc-sa/4.0/>
// Code: GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
import { base } from '$app/paths';
import type { PageLoad } from './$types';

/** One entry in a map-version district index (ed_index_*.json). */
interface EdIndexEntry {
	name: string;
	cx: number;
	cy: number;
	zoom: number;
}

/** A combined-directory row: a district name plus which map versions contain it. */
export interface DirectoryEntry {
	name: string;
	minority: boolean;
	majority: boolean;
	ed2019: boolean;
}

export const prerender = true;

export const load: PageLoad = async ({ fetch }) => {
	async function names(file: string): Promise<Set<string>> {
		const res = await fetch(`${base}/mapdata/${file}`);
		const rows = (await res.json()) as EdIndexEntry[];
		return new Set(rows.map((r) => r.name));
	}

	const [minority, majority, ed2019] = await Promise.all([
		names('ed_index_minority.json'),
		names('ed_index_majority.json'),
		names('ed_index_2019.json')
	]);

	// Distinct district names across all three maps. Names differ between
	// versions (e.g. 2019 "Airdrie-Cochrane" vs the proposals' "Airdrie-East"),
	// so the union is larger than any single map's ~89 entries — that is correct.
	const allNames = new Set<string>([...minority, ...majority, ...ed2019]);

	const directory: DirectoryEntry[] = [...allNames]
		.sort((a, b) => a.localeCompare(b))
		.map((name) => ({
			name,
			minority: minority.has(name),
			majority: majority.has(name),
			ed2019: ed2019.has(name)
		}));

	return { directory };
};
