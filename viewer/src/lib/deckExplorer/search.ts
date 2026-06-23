// Pure ED-name matcher for the deck.gl explorer search box.
//
// Framework-free (no deck.gl, no Svelte, no DOM): turns the generated
// ed_index_<map>.json array into a searchable index and ranks query matches.
// The Svelte component owns the input + dropdown + keyboard nav + fly-to; this
// module just answers "given a query, which districts match and in what order".
//
// Ranking: case-insensitive; prefix matches rank ahead of substring matches;
// within a tier, alphabetical. Empty / whitespace-only query → [].

export interface EdRec {
	name: string;
	cx: number;
	cy: number;
	zoom: number;
	// Set only on community/municipality entries: the 2019 electoral district the
	// place sits in (used for the dropdown subtitle). Absent on district entries.
	ed?: string;
	// Also community-only: the place's OWN centroid (ccx, ccy) and radius in
	// metres (crad), for the distinct community marker. cx/cy/zoom still fly to the
	// containing district; these pinpoint the community within it.
	ccx?: number;
	ccy?: number;
	crad?: number;
}

export interface NameIndex {
	// Records paired with a lower-cased name for cheap, repeated matching.
	entries: { rec: EdRec; lower: string }[];
}

export function buildNameIndex(edIndex: EdRec[]): NameIndex {
	const entries = edIndex.map((rec) => ({ rec, lower: rec.name.toLowerCase() }));
	// Pre-sort alphabetically so the within-tier order falls out for free.
	entries.sort((a, b) => a.rec.name.localeCompare(b.rec.name));
	return { entries };
}

export function matchNames(idx: NameIndex, query: string, limit = 50): EdRec[] {
	const q = query.trim().toLowerCase();
	if (!q) return [];

	const prefix: EdRec[] = [];
	const substr: EdRec[] = [];
	for (const { rec, lower } of idx.entries) {
		if (lower.startsWith(q)) prefix.push(rec);
		else if (lower.includes(q)) substr.push(rec);
	}
	// entries are pre-sorted alphabetically, so each tier is already alphabetical.
	return prefix.concat(substr).slice(0, limit);
}
