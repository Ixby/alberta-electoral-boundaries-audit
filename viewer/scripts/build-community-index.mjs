// Alberta Electoral Boundary Audit — community→ED search index builder
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Builds static/mapdata/community_index_2019.json so the explorer search can
// accept a municipality / community name (e.g. "Country Hills") and fly the user
// to the 2019 electoral district that contains it (e.g. Calgary-Beddington).
//
// The 2019 map is the fixed cross-reference — it is only about orienting people;
// the majority/minority proposals shift around that anchor. Derived entirely from
// already-committed, canonical-derived data:
//   - va_props.community     the community (the near/in feature's data)
//   - va_muni.json           the municipality (build_va_municipality.py)
//   - valabels_2019.json     each VA's 2019 electoral district
//   - ed_index_2019.json     that district's centroid + fit-zoom
//
// A distinct PLACE is (community, municipality): one community name in two
// municipalities (e.g. a "Glenwood" neighbourhood in Edmonton vs the Village of
// Glenwood) becomes two entries. When a name is ambiguous across municipalities
// it is shown with the municipality in brackets — "Glenwood (Edmonton)" — while
// the place whose municipality IS its own name stays bare.
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const dir = resolve(dirname(fileURLToPath(import.meta.url)), '../static/mapdata');
const read = (f) => JSON.parse(readFileSync(resolve(dir, f), 'utf8'));

const vaProps = read('va_props.json'); // [{ id, community, ... }]
const labels2019 = read('valabels_2019.json'); // [edName, ...] by VA id
const edIndex = read('ed_index_2019.json'); // [{ name, cx, cy, zoom }]
const muniPath = resolve(dir, 'va_muni.json');
const vaMuni = existsSync(muniPath) ? read('va_muni.json') : []; // [muniName, ...] by VA id
const geomPath = resolve(dir, 'community_geom_2019.json');
// { "community muni": [ccx, ccy, crad] } — each place's own centroid + radius (m).
const placeGeom = existsSync(geomPath) ? read('community_geom_2019.json') : {};

const edByName = new Map(edIndex.map((e) => [e.name, e]));
const edNameSet = new Set(edIndex.map((e) => e.name));

// place key "community|municipality" -> { community, muni, edCounts: Map }
const places = new Map();
for (const va of vaProps) {
	const community = String(va.community ?? '').trim();
	if (!community) continue;
	const ed = labels2019[va.id];
	if (!ed || !edByName.has(ed)) continue;
	const muni = String(vaMuni[va.id] ?? '').trim();
	const key = community + '|' + muni;
	let p = places.get(key);
	if (!p) {
		p = { community, muni, edCounts: new Map() };
		places.set(key, p);
	}
	p.edCounts.set(ed, (p.edCounts.get(ed) || 0) + 1);
}

// How many distinct municipalities does each community name appear in?
const muniCountByName = new Map();
for (const { community, muni } of places.values()) {
	let s = muniCountByName.get(community);
	if (!s) {
		s = new Set();
		muniCountByName.set(community, s);
	}
	s.add(muni);
}

const out = [];
for (const { community, muni, edCounts } of places.values()) {
	if (edNameSet.has(community)) continue; // already an ED entry — no dupes
	// Dominant 2019 ED for this place (most VAs); ties break to first seen.
	let bestEd = null;
	let best = -1;
	for (const [ed, c] of edCounts) {
		if (c > best) {
			best = c;
			bestEd = ed;
		}
	}
	const e = edByName.get(bestEd);
	// Bracket the municipality only when the bare name is ambiguous across
	// municipalities AND the municipality differs from the community itself
	// (so the Village of Glenwood stays "Glenwood", not "Glenwood (Glenwood)").
	const ambiguous = (muniCountByName.get(community)?.size ?? 1) > 1;
	const name = ambiguous && muni && muni !== community ? `${community} (${muni})` : community;
	// The place's own centroid + radius (m) for the distinct community marker;
	// fly-to (cx/cy/zoom) stays the ED so the user lands in district context.
	const g = placeGeom[community + '|' + muni];
	// k: the place key, for looking up its outline (community_outlines_2019.json).
	const entry = { name, ed: bestEd, k: community + '|' + muni, cx: e.cx, cy: e.cy, zoom: e.zoom };
	if (g) {
		entry.ccx = g[0];
		entry.ccy = g[1];
		entry.crad = g[2];
	}
	out.push(entry);
}
// Collapse any exact-duplicate display names that still resolve identically.
const seen = new Set();
const deduped = out.filter((r) => {
	const k = r.name + '|' + r.ed;
	if (seen.has(k)) return false;
	seen.add(k);
	return true;
});
deduped.sort((a, b) => a.name.localeCompare(b.name));

writeFileSync(resolve(dir, 'community_index_2019.json'), JSON.stringify(deduped));
console.log(`Wrote community_index_2019.json: ${deduped.length} places (municipality data: ${vaMuni.length ? 'yes' : 'NO — names not bracketed'})`);
