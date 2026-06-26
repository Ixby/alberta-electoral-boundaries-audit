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

/** Per-VA properties (va_props.json) — parallel-indexed to valabels_*.json. */
interface VaProp {
	votes?: number;
}

/**
 * A combined-directory row: a district name, which map versions contain it, and
 * each version's IN-PERSON vote total (sum of the district's voting-area votes;
 * advance/special ballots are not attributed per VA, so these are election-day
 * totals only). `*Votes` is null when the district name isn't on that map.
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

export const prerender = true;

export const load: PageLoad = async ({ fetch }) => {
	const json = async <T>(file: string): Promise<T> =>
		(await fetch(`${base}/mapdata/${file}`)).json() as Promise<T>;

	// Per-VA in-person vote counts, parallel-indexed to each map's VA→district
	// label array. Summing votes by district label yields the in-person ED total.
	const vaProps = await json<VaProp[]>('va_props.json');
	async function mapTotals(file: string): Promise<Map<string, number>> {
		const labels = await json<string[]>(file); // index = VA position → district name
		const tot = new Map<string, number>();
		for (let i = 0; i < labels.length; i++) {
			const ed = labels[i];
			if (ed) tot.set(ed, (tot.get(ed) ?? 0) + (vaProps[i]?.votes ?? 0));
		}
		return tot;
	}
	function indexNames(rows: EdIndexEntry[]): Set<string> {
		return new Set(rows.map((r) => r.name));
	}

	const [minRows, majRows, ed2019Rows, minTot, majTot, ed2019Tot] = await Promise.all([
		json<EdIndexEntry[]>('ed_index_minority.json'),
		json<EdIndexEntry[]>('ed_index_majority.json'),
		json<EdIndexEntry[]>('ed_index_2019.json'),
		mapTotals('valabels_minority.json'),
		mapTotals('valabels_majority.json'),
		mapTotals('valabels_2019.json')
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

	return { directory };
};
