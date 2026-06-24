// Annotation pins for the deck.gl explorer. Two kinds:
//   1. "Looks wrong, is faithful" — geography that reads oddly but follows the record.
//   2. Audit-detected packing/cracking signatures — flagged on the strength of the
//      audit's own math (§5.3.1–§5.3.5), independent of what the commission chair
//      flagged. Each carries the grounded "why" and a §-reference shown on hover.
//
// Coordinates are in the explorer's Cartesian projection (EPSG:3401), matching
// the VA/ED geometry.

/** A "looks wrong, is faithful" annotation pin. */
export interface Flag {
	id: string;
	x: number;
	y: number;
	title: string;
	body: string;
}

export const FLAGS: Flag[] = [
	{
		id: 'banff-town',
		x: -57871.8,
		y: -374910.0,
		title: 'Banff — the town carved out of the park',
		body: "Banff sits inside a federal national park, as a small municipal island. The minority groups the townsite with Canmore — the next town down the Bow Valley — in “Canmore-Kananaskis,” and leaves the uninhabited park as the riding that carries Banff's name. The boundary hugs the town because it's the only populated spot for miles. It looks like a mistake, but it follows real geography."
	},
	{
		id: 'banff-park',
		x: -55271.8,
		y: -369910.0,
		title: 'North of Banff — “Rocky Mountain House–Banff Park”',
		body: "“Rocky Mountain House–Banff Park” is one of the minority's proposed ridings, made up largely of uninhabited national park; the town of Banff sits in a neighbouring riding to the south. The minority applied the Electoral Boundaries Commission Act's smaller-population provision to this riding — a choice the commission's chair addressed in the final report."
	},
	{
		id: 'airdrie-split',
		x: 50734.9,
		y: -361975.1,
		title: 'Airdrie — split four ways',
		body: "Airdrie's growth and its commute to Calgary (about 76% of out-commuters) could have anchored a single new Airdrie-area seat — the kind the data supports. The minority instead splits the city across four ridings; the population math doesn't require it, and no submission proposed it. On the audit's cracking-signature test this four-way split meets every criterion — Airdrie's residents end up a minority in all four ridings, with no seat the city controls — where the majority's two-way split shows none. This is a community split, invisible to the partisan-fairness tests; the audit measures the structural effect, not intent. (Academic §5.3.2.)"
	},
	{
		id: 'nolan-hill-cochrane',
		x: 19244.3,
		y: -373751.5,
		title: 'Calgary-Nolan Hill–Cochrane',
		body: "Cochrane's commute to Calgary could have justified pairing it with the city — but the 2021 journey-to-work data spreads that flow city-wide (about a third of workers; half work within Cochrane) and doesn't point to Nolan Hill. The minority's narrow corridor to the Nolan Hill ward — the shape the chair called a lasso — reaches further than the data, and no submission proposed it. The audit reads this as cracking-adjacent: it thins Cochrane's voice, but Cochrane (about 34,000) is too small for a seat of its own, so it stops short of a formal cracking sign. (Academic §5.3.2.)"
	},
	{
		id: 'olds-airdrie-reach',
		x: 50979.2,
		y: -359414.6,
		title: 'Olds–Three Hills–Didsbury — the Airdrie reach',
		body: "A rural riding keeping the Highway 2 towns — Olds, Didsbury, Three Hills — together is well supported; Beiseker-area residents wrote in favour of it. It could have stayed within those communities. The minority's version instead reaches south into the northern edge of Airdrie, an extension the population math doesn't require. The reach is part of how the four-way Airdrie split works — each piece of Airdrie absorbed into a larger rural seat — which the audit reads as part of the cracking pattern. (Academic §5.3.2.)"
	},
	{
		id: 'chestermere',
		x: 64493.7,
		y: -389679.5,
		title: 'Chestermere — split between two ridings',
		body: "Chestermere's heavy commute to Calgary (86% of out-commuters) could have supported keeping it whole and near the city — which residents who opposed a Calgary merger also wanted. The minority instead slices a southern piece into a specific Calgary district it shares no schools or transit with, and that slice fails the population test. The audit reads the bleed into a Calgary district as cracking-adjacent — a community-of-interest split that thins Chestermere's voice without rising to a formal cracking signature. (Academic §5.3.2, §5.8.4.)"
	},
	{
		id: 'red-deer',
		x: 63114.3,
		y: -253265.0,
		title: 'Red Deer — the hybrid ridings',
		body: "Red Deer's regional ties to Blackfalds, Sylvan Lake, Lacombe and Innisfail could have grouped those towns together — a city councillor and residents proposed similar hybrids. The minority's version instead folds parts of the city itself into town-led ridings, thinning urban Red Deer's vote; its “shared schools” rationale also doesn't hold (different school divisions). Folding a city into town-led ridings is the pattern the audit calls hybridization — consistent with cracking, achieving the partisan effect inside the hybrid ridings rather than across them. (Academic §5.3.5.)"
	},
	{
		id: 'st-albert',
		x: 72695.3,
		y: -101273.3,
		title: 'St. Albert — competing configurations',
		body: "Either map's version of St. Albert could rest on a reasonable basis. The audit simply found no submission backing the minority's specific alternative — and since citizens rarely name a commission's exact boundaries, it treats the evidence here as thin, not clearly for or against."
	},
	{
		id: 'calgary-zone-a-packing',
		x: 45500.0,
		y: -380000.0,
		title: 'Calgary north & east — a packing signature',
		body: "The commission chair didn't flag this one — the audit's own math does. Across Calgary's north and east (the audit's “Zone A,” north and east of the Bow River), the minority map's districts run about 11.5% larger than the provincial average, against 2.8% on the majority map. Packing means concentrating one side's voters into fewer, larger districts, so each of their ballots weighs a little less; Zone A is NDP-competitive, and 13 of its 17 districts were NDP-won in 2023. The audit measures the structural effect, not intent. (Academic §5.3.1.)"
	}
];
