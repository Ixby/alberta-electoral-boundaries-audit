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

/** Per-map district totals (ed_totals.json, built by analysis/scripts/build_ed_totals.py). */
type EdTotals = Record<string, Record<string, { total: number; anywhere: boolean }>>;

/**
 * A combined-directory row: a district name, which map versions contain it, and
 * each version's 2023 vote total counting all ballots (ed_totals.json; advance,
 * mobile, special and Vote Anywhere ballots are spread over voting areas by
 * election-day vote, so totals on the proposal maps are estimates). `*Votes` is
 * null when the district name isn't on that map.
 */
export interface DirectoryEntry {
	name: string;
	minority: boolean;
	majority: boolean;
	ed2019: boolean;
	minorityVotes: number | null;
	majorityVotes: number | null;
	ed2019Votes: number | null;
}

/** One Recommendation 5 zone (lunty_bounds.json), minus its geometry. */
export interface R5Zone {
	cond: 'a' | 'b' | 'c' | 'd';
	eds: string[];
}

export const prerender = true;

export const load: PageLoad = async ({ fetch }) => {
	const json = async <T>(file: string): Promise<T> =>
		(await fetch(`${base}/mapdata/${file}`)).json() as Promise<T>;

	// All-ballot district totals, the same figures the map explorer's tooltip shows.
	const edTotals = await json<EdTotals>('ed_totals.json');
	function mapTotals(key: string): Map<string, number> {
		return new Map(Object.entries(edTotals[key] ?? {}).map(([ed, r]) => [ed, r.total]));
	}
	function indexNames(rows: EdIndexEntry[]): Set<string> {
		return new Set(rows.map((r) => r.name));
	}

	const [minRows, majRows, ed2019Rows, minTot, majTot, ed2019Tot, r5] = await Promise.all([
		json<EdIndexEntry[]>('ed_index_minority.json'),
		json<EdIndexEntry[]>('ed_index_majority.json'),
		json<EdIndexEntry[]>('ed_index_2019.json'),
		mapTotals('minority'),
		mapTotals('majority'),
		mapTotals('2019'),
		json<{ zones: R5Zone[] }>('lunty_bounds.json')
	]);
	const minority = indexNames(minRows);
	const majority = indexNames(majRows);
	const ed2019 = indexNames(ed2019Rows);

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
			ed2019: ed2019.has(name),
			minorityVotes: minTot.get(name) ?? null,
			majorityVotes: majTot.get(name) ?? null,
			ed2019Votes: ed2019Tot.get(name) ?? null
		}));

	// The four Recommendation 5 areas the map draws, with their district lists.
	const r5Zones: R5Zone[] = r5.zones.map((z) => ({ cond: z.cond, eds: z.eds }));

	return { directory, r5Zones };
};
