// English — source of truth.
// Mirrors the editorial content in proposals/verdict_and_glossary_draft.md.
export default {
	selector: {
		label: 'Choose language'
	},
	disclaimer: {
		text:
			'This site has been translated by AI. Some content may still appear in English while translations are in progress. If you notice errors or would like to help translate this project, please %s.',
		link_label: 'contact us'
	},
	opener: {
		heading: "Who's this for?",
		body:
			"Us. All of us. Rural, Urban, curious, wonk, journalist, lawyer, academic, politician — all of us. Because it impacts all of us. Whether or not you like the party in power, what the split commission produced has never been done before. And it's given us the opportunity to peer inside the machine in ways we never could before. Now we can establish a baseline — a series of tests, and everything that comes after can be graded on it. Let me show you what I found."
	},
	verdict: {
		q1: {
			heading: 'Is the proposed map a gerrymander?',
			body:
				'"Gerrymander" is not a term Canadian courts use. But if it were — in the everyday sense most people mean by it — the evidence in this audit would reasonably support calling the <em>minority proposal</em>, if enacted, a heavily gerrymandered map. Every structural test this audit runs flags the <em>minority proposal</em>; none flag the alternative (the <em>majority proposal</em>).',
			footnote:
				'The "majority" and "minority" names come from a 3–2 split among the Electoral Boundaries Commission (chaired by Justice Miller), which produced two competing proposals rather than a single recommendation. A separate MLA committee chaired by Brandon Lunty — a Premier-appointed MLA — is now choosing between them before the November 2026 deadline.'
		},
		q2: {
			heading: 'What does "gerrymander" mean in Canadian law?',
			body:
				"It doesn't. The Canadian test is different: whether the boundaries give voters <em>effective representation</em> under section 3 of the Charter. The minority proposal raises serious questions under that test; only a judge can answer them definitively, and no one has asked one yet."
		},
		q3: {
			heading: 'What does it mean for Albertans?',
			body:
				"At a 50/50 provincial vote, the audit's measurements place the minority proposal at a structural extreme — fewer than 100 of the 1.01 million neutral comparison maps produce the same kind of seat imbalance. That imbalance matters because at 58 of 87 seats — a two-thirds supermajority — the governing party unlocks extraordinary procedural powers: it can waive standard notice periods and push public bills through multiple legislative stages in a single day, bypassing deliberation checks that normally constrain it. Whether the minority proposal's tilt is large enough to push one party past that 58-seat threshold at vote shares <em>other</em> than 50/50 is a question this audit has not yet tested. Whether the tradeoff itself is acceptable is a question for Albertans, not for this audit."
		},
		cta_law: 'Read the legal context →',
		cta_methods: 'See how we tested →'
	},
	head: {
		title: 'Alberta Electoral Boundary Audit',
		meta_description:
			"Statistical audit of Alberta's 2026 electoral boundary commission — 1,010,000 neutral maps, official Elections Alberta shapefiles, pre-registered tests."
	},
	nav: {
		home_aria: 'Back to top',
		theme_aria: 'Toggle dark/light mode',
		theme_title: 'Toggle dark mode',
		nav_aria: 'Toggle navigation',
		drawer_top: '↑ Top',
		verdict: 'Verdict',
		why: 'Why?',
		map: 'Map',
		split: 'The Split',
		litmus: 'Litmus Test',
		crack_pack: 'Crack & Pack',
		for_you: 'For You',
		impact: 'Impact',
		history: 'History',
		canada: 'Canada',
		gerrymanders: 'Gerrymanders',
		november: 'November',
		lunty: 'Lunty',
		invisible: 'Invisible',
		suggestions: 'Suggestions',
		retractions: 'Retractions',
		references: 'References',
		resources: 'Resources',
		technical: 'Technical'
	},
	hero: {
		h1: 'Alberta Electoral Boundary Audit',
		subtitle:
			"Alberta's commission produced two riding maps in 2026. This audit compared them — using the same tests, applied equally to both — to ask whether they treat voters the same way.",
		badge: 'Official Elections Alberta maps — Published May 2026',
		cover_note: 'Click to zoom and explore all three boundary proposals simultaneously. Pin the viewport and flip between maps — boundaries shift, voters stay put. Scroll down for the analysis.',
		cover_note_1:
			'This map is the best way in. Click it to zoom and explore. The buttons at the top switch between the minority map, the majority map, and the 2019 enacted boundaries — or layer all three to see exactly where they diverge. <strong>Detail</strong> colours each polling area by how people voted in 2023; <strong>Trend</strong> adds partisan shading by district (blue UCP, orange NDP); <strong>Lines</strong> toggles boundaries on and off. <strong>Find</strong> jumps to any riding by name.',
		cover_note_2:
			"Try locking the viewport and flipping between maps — watch a boundary shift while the voters underneath stay still. That's the whole question in one gesture.",
		cover_note_3:
			"When you're done exploring, scroll down for the summary. For the full technical analysis, see the Resources section. All data is official Elections Alberta shapefiles and other government and open-source records.",
		image_alt:
			'Alberta electoral district maps — minority commission proposal, coloured by 2023 vote',
		map_hint: 'Click to explore interactively',
		btn_title: 'Click to open interactive map',
		btn_aria: 'Click to explore interactively'
	},
	boundary: {
		heading: "What this audit can and can't tell you",
		can_1:
			'Fewer than 1 in 14.5 million randomly generated comparison maps produced patterns as extreme as the minority proposal on all four statistical measures combined.',
		can_2:
			'The minority proposal fails 5 of 5 pre-registered structural tests. The majority proposal fails 0 of 5.',
		can_3:
			'These results are consistent with maps that produce strong partisan effects, and inconsistent with what the random comparison set produces.',
		cant_1:
			'The audit does <strong>not</strong> establish that any commissioner intended the partisan effects it measures. Boundary geometry cannot reveal intent.',
		cant_2:
			'The audit does <strong>not</strong> predict what the Lunty committee will choose, what the November 2026 vote will be, or how Albertans will react.',
		cant_3:
			'The audit does <strong>not</strong> predict how a court would rule if a Charter challenge were brought against either proposal.',
		cant_4:
			"The audit does <strong>not</strong> tell any individual voter what position to take or what to do with this information. That's yours to decide."
	},
	section1: {
		heading: 'What is redistricting and why should you care?',
		p1: 'Every voter in Alberta lives in an <em>electoral district</em> — a slice of the province that elects one person to the legislature. There are 87 districts. Each district elects one MLA. When you cast a ballot in a provincial election, you are choosing the MLA for the district you live in. That is the entire connection most Albertans have to the legislature: one MLA, one district, one vote.',
		p2: 'Those district lines are not permanent. People move, neighbourhoods grow, rural areas thin out, cities sprawl. Every eight to ten years, Alberta is supposed to redraw the lines so each district is roughly the right size and reflects the way Albertans actually live now. The body that does the redrawing is the <em>Electoral Boundaries Commission</em> — an independent commission with judges, lawyers, and public members, not politicians.',
		p3: "That is the standard process. This time, the standard process produced something unusual. The commission's five members split 3–2 on what the map should look like, and rather than settling on one recommendation they produced two: a <em>majority proposal</em> (backed by three commissioners) and a <em>minority proposal</em> (backed by two). Both are sitting on the table. A separate committee of MLAs chaired by Brandon Lunty — appointed by the Premier for this specific decision — is choosing between them. The legislature must approve whichever one survives that committee before November 2026.",
		p4: "Why it matters to you: the lines decide who your MLA is. They decide which neighbourhoods, towns, and concerns get represented together. If your city is split across four MLAs instead of one, no single representative is accountable for the city as a whole. If your community of interest — a small town, a rural region, a downtown core — is divided between districts, your voice on provincial decisions is diluted. The map also shapes which party can form a government, and at what margins. The audit's specific finding (that the minority proposal sits at a structural extreme) is the reason you are reading this site, but the broader question is older and applies to every redistricting cycle: do the lines reflect the way Albertans live, or do they shape the politics that follow?",
		p5: 'The rest of this page walks through what the two proposed maps actually do.',
		key_terms_lead: 'Key terms in this section — click to read:'
	},
	section5: {
		heading: 'What this means for you and your community',
		intro_p1:
			"Set aside, for a moment, the question of which party gains or loses seats. Politicians and parties tend to frame this as a fight over power concentration in the legislature, and at that scale it is. But power concentration in the legislature is not where you experience these maps. You experience them through three concrete questions about your own district:",
		intro_q1: 'Where does your MLA live?',
		intro_q2: 'Are they invested in your community?',
		intro_q3: 'Will the demands of the head dominate the demands of the tails?',
		intro_p2:
			'Every other framing — partisan advantage, supermajority threshold, statistical extreme — eventually points back to those three. The five rungs below walk through how each proposed map answers them, at five scales.',
		you_h: 'You.',
		you_p:
			"Your electoral district decides who represents you in the legislature. Right now you live in one of 87 districts. Under both proposed maps you may live in a different one — possibly with a different MLA, possibly anchored to different neighbouring communities. If you don't know what district you're in right now, or who your MLA is, you're not alone: most Albertans couldn't name their MLA. But the boundary lines are not abstract. They decide whose phone number is on your local representative's office wall, whose neighbourhood petition gets your name attached to it, whose concerns your MLA hears about first. The postal-code lookup on this site shows which district you sit in under each proposal. If your district changes, your representative changes — and your representative's relationship to your community changes with it.",
		community_h: 'Your community.',
		community_p:
			'Communities are not abstract either. A high school\'s catchment area, a chamber of commerce, a faith community, a neighbourhood association — these are real groupings of people with shared local concerns. When a boundary line cuts through them, no single MLA is responsible for the whole. Take Airdrie under the minority proposal: a city of about 74,000 people sliced into four electoral districts, each anchored to a different rural hinterland. No single representative is accountable for Airdrie as a city. The same dynamic plays out anywhere a town, neighbourhood, or recognised community of interest is split — the bigger the split, the weaker the representation. The audit measures <em>municipal anchoring</em> (what fraction of each district\'s perimeter follows existing municipal lines), and the minority proposal scores notably lower than the majority on that test.',
		municipality_h: 'Your municipality.',
		municipality_p:
			"When a city is fractured across many representatives, its ability to bargain on provincial decisions weakens. A council asking for transit funding, a school board negotiating a new school, a mayor lobbying for highway extensions — each of those goes better when the city can point to a few MLAs who owe accountability to the city as a whole. The minority proposal splits Calgary's northwest quadrant across multiple districts whose vote-share patterns suggest <em>packing</em> (concentrating one party's voters into a few high-margin seats) on top of <em>cracking</em> (splitting the other party's voters across many low-margin seats). Whether the pattern is intentional is a question the audit cannot answer — boundary geometry doesn't reveal intent. What it can say is that the four statistical measures flag the same districts that the structural tests flag, and that the alternative proposal does not produce the same fingerprint.",
		region_h: 'Your region.',
		region_p1:
			"If you live outside Alberta's cities you have probably noticed that political conversations about boundaries always seem to centre the cities. That's a fair complaint, so let's be direct about what this audit does and does not say about rural Alberta.",
		region_p2:
			"What it does <strong>not</strong> say: that rural Alberta has too many seats. The EBCA allows district populations to vary by up to 25% so that one rural MLA isn't representing a geography the size of southern France. Canadian courts treat that variance as legitimate. Both proposed maps preserve it. Nothing in this audit changes that.",
		region_p3:
			'What it <strong>does</strong> say: in several places on the minority proposal, rural communities are being attached as the <em>tail</em> of a district whose population centre sits in a city. Look at how the minority proposal handles Airdrie — a city of about 74,000 sliced into four districts, each one extended out into a different stretch of rural countryside. The population centre of each new district is the urban slice, not the rural tail. An MLA elected from that kind of district is most likely to live, campaign, and prioritise where the votes are — which means rural communities formerly represented by a dedicated rural MLA become the back half of an urban-led seat. That pattern repeats on the minority proposal in ways it does not on the majority proposal.',
		region_p4:
			"The audit doesn't propose taking seats away from rural Alberta. It asks whether the lines respect the rural communities those seats are meant to represent, or whether rural geography is being used as ballast to absorb urban votes into districts whose centre is somewhere else. If you live in one of those rural tails, the question of which map gets enacted decides whether your MLA represents the rural community you actually live in, or an urban district whose lines happen to include your land.",
		province_h: 'Your province.',
		province_p:
			"The legislature is what you get when you sum every district's answers to the three questions above. If most districts are anchored to communities whose MLAs actually live in them, the legislature represents those communities. If most districts have rural tails attached to urban heads, the legislature represents the heads — and the tails get whatever attention is left over. The partisan question — which party wins a majority — is downstream of that. The supermajority question — whether one party crosses 58 of 87 seats and unlocks procedural shortcuts like waiving notice periods or accelerating bills through multiple stages in a single day — is downstream of <em>that</em>. At a hypothetical 50/50 provincial split, the audit's measurements place the minority proposal at a structural extreme: fewer than 100 of the 1.01 million neutral comparison maps produce the same kind of seat imbalance. Whether that imbalance pushes a party past 58 seats at the vote shares Albertans actually deliver is a question this audit has not yet directly tested; the verdict at the top of this page is honest about the gap. Whether the answer to any of these questions matters enough to act on is, again, a question for you."
	},
	section6: {
		heading: 'A short history of gerrymandering',
		p1: 'The word comes from 1812. Massachusetts governor Elbridge Gerry signed off on a state-senate map whose districts were so contorted to favour his party that a Boston cartoonist drew one of them as a salamander — wings, claws, a forked tongue. The cartoonist\'s pun, <em>Gerry-mander</em>, stuck. The shape stuck too: two centuries later, the word still means drawing electoral lines to engineer a partisan outcome.',
		p2: 'The term endures because the problem endures. Anywhere voters choose representatives from geographic districts, someone has to draw the lines, and the lines can be drawn many ways. Different countries have arrived at different answers about who should do the drawing and what should constrain them.',
		p3: '<strong>The United States</strong> treats partisan gerrymandering as a problem the federal courts mostly cannot fix. In <em>Rucho v. Common Cause</em> (2019), the U.S. Supreme Court ruled that partisan gerrymanders are "political questions" outside its jurisdiction. Some states (California, Michigan) have responded by creating independent citizen commissions to draw their own lines; others (Texas, North Carolina) have continued to draw openly partisan maps and defended them on the basis that <em>Rucho</em> permits it.',
		p4: "<strong>The United Kingdom</strong> uses four permanent Boundary Commissions — one each for England, Scotland, Wales, and Northern Ireland — staffed by judges and senior civil servants. They redraw lines roughly every eight years against fixed rules (population equality, geographic coherence, respect for local government boundaries). Parliament can in theory reject the commissions' recommendations, but in practice virtually never does; the convention is that the commissions' judgment stands.",
		p5: "<strong>Australia</strong> delegates the work to the Australian Electoral Commission, a federal independent agency with full authority over both election administration and boundaries. Redistributions happen automatically when a state's seat count changes or seven years pass since the last one. The commissioners' decisions are reviewable on procedural grounds but not on partisan ones. Like the U.K., the result is that gerrymandering as Americans know it is virtually unheard of.",
		p6: 'These three cases bracket the spectrum: courts staying out (U.S.), independent commissions with strong parliamentary deference (U.K.), and a permanent independent agency with full authority (Australia). Canada sits somewhere different again — which is what the next section takes up.'
	},
	glossary: {
		more_link: 'Learn more →',
		'electoral-district': {
			term: 'Electoral district (ED)',
			definition:
				'The geographic area that elects one member to the provincial legislature. Often shortened to "ED" after first use. Each ED has one MLA. (The word "riding" usually refers to federal districts; in the provincial context the proper term is electoral district.)'
		},
		riding: {
			term: 'Riding',
			definition:
				'In Canadian usage, this most often refers to a federal electoral district. The Alberta provincial equivalent is called an "electoral district" (ED). The audit uses the provincial term throughout.'
		},
		mla: {
			term: 'MLA',
			definition:
				'Member of the Legislative Assembly — the person elected from one electoral district to represent it in the Alberta legislature.'
		},
		ucp: {
			term: 'UCP',
			definition:
				"United Conservative Party — Alberta's current governing provincial party. Formed in 2017 from the merger of the Progressive Conservatives and the Wildrose Party; has held government since 2019."
		},
		ndp: {
			term: 'NDP',
			definition:
				"New Democratic Party (Alberta NDP) — Alberta's current official opposition. The Alberta NDP held government from 2015 to 2019."
		},
		gerrymander: {
			term: 'Gerrymander',
			definition:
				'A map drawn so that one political party wins more seats than its share of the vote would suggest. The word comes from an 1812 Massachusetts district shaped like a salamander. It is not a legal term in Canada, but the concept is widely studied.'
		},
		cracking: {
			term: 'Cracking',
			definition:
				"A gerrymandering technique that splits a voting bloc across many districts so it never reaches a majority in any single one. For example, dividing a city across four ridings so its voters are outnumbered in each."
		},
		packing: {
			term: 'Packing',
			definition:
				"A gerrymandering technique that concentrates one party's voters into a small number of districts. The party wins those districts overwhelmingly but \"wastes\" many votes — leaving fewer of its voters available to compete in other districts."
		},
		draining: {
			term: 'Draining',
			definition:
				"A term this audit uses for a follow-on effect of cracking and packing: the wasted votes those techniques produce get pushed into strategically chosen places, altering the political character of nearby electoral districts. It is the audit's own framing rather than an established concept in the redistricting literature — the audit tests for the effect and finds results consistent with it, but treats it as exploratory rather than a settled methodology."
		},
		anchoring: {
			term: 'Anchoring',
			definition:
				'How firmly the proposed boundaries follow existing municipal lines (city limits, town boundaries). A highly anchored map mostly respects those lines; a loosely anchored map departs from them often — especially at politically meaningful spots, which is a structural warning sign.'
		},
		'charter-s3': {
			term: 'Section 3 of the Charter',
			definition:
				'The section of the Canadian Charter of Rights and Freedoms that guarantees citizens the right to vote. Canadian courts have interpreted it not as a strict "one person, one vote" rule but as a right to "effective representation."'
		},
		'effective-representation': {
			term: 'Effective representation',
			definition:
				"The standard Canadian courts apply when judging electoral boundaries. It means voters should have a meaningful voice — not just numerical equality of riding populations, but also recognition of community ties, geography, and minority representation. The leading statement is from the Supreme Court of Canada's 1991 Saskatchewan Reference."
		},
		ebc: {
			term: 'Electoral Boundaries Commission (EBC)',
			definition:
				"The body that draws Alberta's provincial electoral boundaries under the EBCA. The 2026 commission was chaired by Justice Miller and split 3–2 among its commissioners, producing two competing proposals (the majority and minority proposals) rather than a single recommendation."
		},
		'lunty-committee': {
			term: 'Lunty committee',
			definition:
				"An MLA committee chaired by Brandon Lunty — an MLA appointed by the Premier — that is choosing between the EBC's majority and minority proposals before the November 2026 deadline. The committee is separate from the EBC; the legislature created it for this specific decision and it is not part of the standard EBCA process."
		},
		ebca: {
			term: 'EBCA',
			definition:
				'The Alberta Electoral Boundaries Commission Act — the law that governs how electoral boundaries are drawn in the province. It sets up the commission, the public-hearing process, and the rules for when a new map takes effect.'
		},
		fsa: {
			term: 'Forward sortation area (FSA)',
			definition:
				'The first three characters of a Canadian postal code (the letter-digit-letter part). About 270 FSAs cover Alberta. Most fall entirely within a single electoral district.'
		}
	},
	body: {
		section_link_aria: 'Link to section',
		the_map: {
			heading: '1: The Map',
			p1: 'The cover map is the best single image in this audit. Here is how to read it.',
			p2: "Alberta is divided into 4,765 Voting Areas — small geographic zones Elections Alberta uses to count polling-station ballots. Each one is coloured by how people in it actually voted in 2023: orange where NDP votes are concentrated, blue where UCP votes are concentrated. But the colour only becomes dark and saturated where a lot of people live. A Voting Area that covers hundreds of square kilometres of parkland or farmland stays pale — nearly invisible. The map lights up where people are, and fades where they aren't.",
			p3: 'This is very different from the Alberta you see on election night. Most election maps colour entire ridings solid blue or orange based on who won. Rural ridings are geographically large and the UCP wins most of them, so election-night Alberta looks like a wall of blue with small orange pockets in Edmonton and Calgary. The cover map uses the same votes and the same geography — but shows them weighted by where people actually live. What appears is a province where most of the population is concentrated in a dense arc of cities, and those cities vote very differently from the rural map that normally represents them.',
			p4: "The boundary lines drawn over the colour are the minority commission's 89 proposed electoral districts — the map this audit ends up critiquing. The audit's work is to ask what those lines do to the people underneath them.",
			p5: 'For me personally, this was the image that made the stakes clear. A province that looks like it votes one way on a standard map is actually a province where most of the people live in areas that vote the other way. Once you can see the population underneath the boundary choices, those choices stop looking random.'
		},
		structural_results: {
			heading: 'Structural audit results — before any statistics:',
			body: 'The majority map crosses <strong>zero of five</strong> pre-registered structural thresholds. The minority map crosses <strong>all five</strong>. These are geometric measurements — population spread, <button class="vocab-term" data-def="how closely a district\'s borders follow pre-existing city and municipal limits, rather than cutting through them" aria-expanded="false">municipal anchoring</button>, Airdrie split count, NW Calgary population excess, and chair-flagged boundary anomalies — that require no election data and no statistical sampler. The next section tests both maps against 1,010,000 computer-generated neutral maps and reaches the same conclusion through a completely different instrument.'
		},
		cpd: {
			heading: '4: Cracking, Packing, and Draining',
			vocab_label: 'Three moves, one playbook',
			vocab_packing: "<strong>Packing</strong> means cramming one party's voters into districts that party wins by landslides — each packed ballot still counts, but it contributes nothing beyond victory. Large, lopsided wins. Wasted votes.",
			vocab_cracking: "<strong>Cracking</strong> means splitting a community across multiple districts so it wins none of them outright. A city strong enough to carry two seats gets carved into four, each tethered to a different rural area. Diluted votes. No seat for anyone.",
			vocab_draining: '<strong>Draining</strong> is the spatial companion: packed and cracked districts are placed next to each other so that over-concentrated supporters on one side "drain" voting power away from the contested districts nearby. The adjacency pattern amplifies both effects — packing and cracking reinforce each other across district lines.',
			vocab_disclaimer: 'All three can occur without any explicit partisan intent. What the audit measures is whether the pattern — and its statistical magnitude — is consistent with what a neutral map-drawing process produces. <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md#5-results" rel="noopener">Full methodology at §5 of the technical report.</a>',
			fig_alt: 'Map showing the division of Airdrie into four separate districts under the minority map',
			fig_caption: 'The division of Airdrie into four separate districts under the minority map, diluting its urban voting power.',
			intro: 'The five commissioners worked from the same statutory rules, the same provincial geography, the same archive of 1,140 public submissions, and the same demographic data. Their two competing drafts agree on most of Alberta. Where the drafts diverge, they diverge on choices someone in the room had to make. Three of those choices are worth seeing as choices, not numbers.',
			airdrie_p: "<strong>It splits the City of Airdrie into four pieces.</strong> The law caps each electoral division at one-and-a-quarter times the provincial average, so Airdrie needs at least two divisions. The majority map gives it two. The minority gives it four — north to Calgary-Nolan Hill-Cochrane, east to Airdrie East, west to Calgary-Foothills-Airdrie West, and centre-south to Calgary-Airdrie — each one stapled to a different rural or Calgary-edge district. An Airdrie resident with a question for her MLA has to know which quarter of the city she lives in before she can call the right office. Her neighbours two blocks over will give her three different answers. The PTA at her child's school cannot send a single delegation to one MLA on a school-funding question; they have to coordinate four delegations to four offices, each MLA primarily accountable to a different rural or suburban constituency. The minor-hockey association, the food bank, the Chamber of Commerce — every organization that operates citywide now operates across four provincial ridings.",
			airdrie_callout_label: 'WHY AIRDRIE MATTERS',
			airdrie_callout_p1: 'Airdrie is the largest Alberta city without its own MLA. At 85,805 people (2024 municipal census) it is bigger than Red Deer; it has one council, one tax bill, one school division — every civic system treats it as a unit.',
			airdrie_callout_p2: 'Splitting it across four provincial divisions — Calgary-Airdrie, Calgary-Foothills-Airdrie West, Calgary-Nolan Hill-Cochrane, and Airdrie East — each primarily identified with a different surrounding jurisdiction, removes Airdrie from the political map at the level of government that draws it. The city has 85,805 residents and zero seats in the legislature where a majority of voters call the place home.',
			airdrie_callout_p3: 'A four-way split is invisible to every partisan-fairness test except the one that asks: can a voter find their MLA?',
			airdrie_callout_summary: 'Both maps are legal. The four-way split is a choice.',
			airdrie_btn: 'Show flagged districts on map',
			anchoring_p: "<strong>Where it departs from municipal lines, it departs at strategically important places.</strong> When electoral maps follow the edge of a city or town, voters recognize where their division begins and ends — the property-tax line, the school-division line, the local-election ward line, and the provincial-election line all coincide. Statistics Canada publishes these boundaries for free. On official Elections Alberta shapefiles, both maps follow municipal lines at comparable overall rates: the majority at 80%, the minority at 72%, both within Canada's 70–85% norm (Quebec: 78%, Ontario: 82%, BC: 71%; comparator commissions documented in the monograph). (The audit's initial provisional analysis showed the minority anchoring at only 15%; that figure did not survive recomputation on official shapefiles — see the correction note below.) The striking observation is not the overall rate but where the minority's departures are concentrated: the three boundaries the commission's own chair flagged as anomalous — Rocky Mountain House–Banff Park <button class=\"ed-trigger\" data-ed-name=\"Rocky Mountain House-Banff Park\">show ↗</button>'s extension into uninhabited national-park land, the Nolan Hill–Cochrane <button class=\"ed-trigger\" data-ed-name=\"Calgary-Nolan Hill-Cochrane\">show ↗</button> lasso corridor, and the Olds–North Airdrie <button class=\"ed-trigger\" data-ed-name=\"Olds-Three Hills-Didsbury\">show ↗</button> reach — are each departures from pre-existing civic geography in the exact urban-edge zones where pairing urban and rural voters most directly affects which party wins the seat.",
			anchoring_followup: 'The minority commissioners gave reasons for each of the three flagged boundaries. For Rocky Mountain House–Banff Park, they cited geographic size, the Highway 22 corridor, and the proximity of First Nations reserves to Rocky Mountain House; the commission chair called the extension into uninhabited national park land "a bad faith effort" to satisfy the area criterion, and that phrase appears in the commission\'s official final report. For Nolan Hill–Cochrane, they cited shared transportation and employment ties between northwest Calgary and Cochrane; Statistics Canada journey-to-work data shows only 35.8% of Cochrane workers travel to Calgary at all, with most working within Cochrane itself. For the Olds–North Airdrie reach, they cited Highway 2 corridor continuity; the audit found the specific Airdrie extension fails on population grounds. Independent check found five of the minority\'s six published sub-rationales fail or only partially hold against primary data.',
			packing_p: "<strong>One area of Calgary is carved up to concentrate NDP voters into larger-than-average divisions.</strong> In Calgary's northwest quadrant <button class=\"ed-trigger\" data-ed-name=\"Calgary-North West-Bearspaw\">show ↗</button>, the minority map's divisions average 11.5% above the province-wide population — versus 2.8% on the majority. The same geographic zone, drawn by the same commission under the same constraints, produces districts a quarter larger on one map than on the other. This is <em>packing</em>: concentrating one party's voters into fewer, larger districts so each of their ballots weighs less. Packing and <em>cracking</em> (splitting a party's voters thinly across districts they narrowly lose) are the two classic gerrymandering moves; both shrink a party's seat count below its vote share.",
			chair_p: "The commission chair — appointed under the same Act, working from the same submissions — flagged three boundaries on the minority map as geographically anomalous: Rocky Mountain House–Banff Park's extension into uninhabited national park land; the Calgary-Nolan Hill–Cochrane lasso-shaped corridor; the Olds–Three Hills–Didsbury reach into north Airdrie. The majority received zero such flags from the same chair. (The chair's published criticism covers seven boundary configurations in total — four geometric flags in the main report and three in Appendix C. This audit independently confirmed anomalous geometry for three of the four geometric flags; the fourth, Calgary-Foothills-Airdrie West <button class=\"ed-trigger\" data-ed-name=\"Calgary-Foothills-Airdrie West\">show ↗</button>, did not meet the audit's confirmation threshold.)"
		},
		litmus: {
			heading: '3: The 1,010,000-Map Litmus Test',
			fig_alt: 'Histogram showing the distribution of efficiency gaps across 250,000 neutral Alberta maps. Most maps cluster near zero. The minority commission map (purple line) sits at the 94th percentile (+3.96%), in the shaded right tail. The majority map (teal line) sits at +0.04%, well within the normal range.',
			fig_caption: 'Distribution of <button class="vocab-term" data-def="a measure of how lopsidedly votes are converted into seats — positive values favour the UCP, negative values favour the NDP" aria-expanded="false">efficiency gaps</button> across 250,000 neutral Alberta maps drawn from the same geography. Most neutral maps cluster near zero; the shaded right tail marks the top 10%. The minority proposal&rsquo;s +3.96% sits at the 94th <button class="vocab-term" data-def="the percentage of maps that scored lower — p94 means 94 out of 100 neutral maps were less partisan than this" aria-expanded="false">percentile</button> — a region fewer than 6 in 100 neutral maps ever reach. The majority proposal&rsquo;s +0.04% is indistinguishable from what a neutral process typically produces.',
			table_intro: "The table compares the two maps. The first five rows use no election results — they're properties of the lines themselves. The last two depend on how votes were attributed to each district.",
			table_col_measured: 'What was measured',
			table_col_majority: 'Majority map',
			table_col_minority: 'Minority map',
			table_col_direction: 'Direction / Beneficiary',
			table_r1_a: 'Population spread across districts (tighter is better)',
			table_r1_b: '3,180',
			table_r1_c: '4,707 — 48% wider',
			table_r1_d: 'Structural (Reduces vote equality)',
			table_r2_a: 'NW Calgary population excess above average',
			table_r2_b: '2.8%',
			table_r2_c: '11.5%',
			table_r2_d: '<strong>UCP</strong> (Packs urban NDP votes)',
			table_r3_a: 'Airdrie split',
			table_r3_b: '2 divisions',
			table_r3_c: '4 divisions',
			table_r3_d: '<strong>UCP</strong> (Cracks urban/suburban power)',
			table_r4_a: 'Borders that follow existing municipal lines',
			table_r4_b: '80% — within norm',
			table_r4_c: '72% — within norm',
			table_r4_d: 'N/A — both within Canadian norm (70–85%)',
			table_r5_a: 'Boundaries flagged by the commission chair',
			table_r5_b: '0',
			table_r5_c: '3',
			table_r5_d: 'N/A',
			table_r6_a: 'Seats at 50/50 votes (percentile in 1,010,000-map simulation)',
			table_r6_b: '46.1% — p83 (normal range)',
			table_r6_c: '51.7% — p99.99 (fewer than 100 of 1,010,000 reach this)',
			table_r6_d: '<strong>UCP</strong>',
			table_r7_a: 'Efficiency Gap (percentile in 1,010,000-map simulation)',
			table_r7_b: '+0.04% — p15.5 (normal range)',
			table_r7_c: '+3.96% — p94.4',
			table_r7_d: '<strong>UCP</strong>',
			table_r8_a: 'Packing-cracking neighbourhood pattern',
			table_r8_b: '6 coupled chain signals',
			table_r8_c: '2 (pre-registered PASS)',
			table_r8_d: 'Neutral — minority achieves partisan effect via hybridization, not adjacency drain (§5.3.5)',
			vocab_label: 'VOCABULARY',
			vocab_eg: "<strong>Efficiency gap.</strong> A single number that measures how lopsidedly a party's votes are translated into seats. Positive numbers favour the UCP; negative favour the NDP. The audit uses ~5% as Alberta's outlier line — the value exceeded by only 5% of the 1,010,000 neutral Alberta-specific simulations. This threshold is not borrowed from US or general literature; a threshold calibrated to another jurisdiction would be wrong because Alberta's natural geography produces a different neutral range.",
			vocab_mm: "<strong>Mean-median difference.</strong> The gap between a party's median district vote share and its mean district vote share. When one party wins many close races, the median sits above the mean — those votes are distributed efficiently. When a party wins many races by large margins, the mean sits above the median — votes are being wasted. A large mean-median gap in one direction flags structural inefficiency in how one side's votes are spread across districts.",
			vocab_percentile: '<strong>Percentile ranking.</strong> In this audit, a "percentile" is a rank within the 1,010,000 neutral simulated maps. "p94" means 94% of neutral maps score lower — the real map is more extreme than 94% of neutral draws. "p99.99" means fewer than 1 in 10,000 neutral maps reach that level.',
			vocab_anchoring: '<strong>Anchoring.</strong> The fraction of an electoral border that lies on a pre-existing administrative line — a city limit, a school-division boundary, a Statistics Canada census line.',
			closing_p1: "The bottom rows depend on election results. The <em>seats@50/50</em> test holds the electorate at perfect parity (UCP and NDP each win exactly half the votes province-wide) and asks how many seats the map awards the UCP. A neutral Alberta map produces a median around 44.8% UCP seats — Alberta's geography (NDP voters concentrated in city cores, UCP voters spread across rural ridings) gives the NDP a small efficiency advantage at neutrality. The majority map at 46.1% sits at the 83rd percentile of the 1,010,000-map simulation (normal range). The minority map at 51.7% is at the 99.99th percentile — fewer than 100 of 1,010,000 neutral draws reach that value. The <em>efficiency gap</em> number measures how lopsidedly each party's votes get translated into seats; on the official Elections Alberta shapefiles the minority's efficiency gap is +3.96%, placing it at the 94.4th percentile — just below the audit's 95th-percentile outlier line. The verdict section unpacks the consequences.",
			closing_p2: "The last row is where the minority map has fewer coupled chain signals than the majority on the neighbour-drain test: 2 against the majority's 6 (and the 2019 enacted map's 5). The audit pre-registered this test before measuring, and the minority's lower count is a genuine pre-registered PASS — the minority does not show the classic pack-and-drain adjacency pattern. It is the single test where the minority numerically outperforms the majority. §5.3.5 of the academic report explains why: the minority achieves its partisan effect through hybridization (city-splitting that internalises packing and cracking within individual EDs), which is invisible to an adjacency-chain test that only measures how packed districts cluster next to cracked ones."
		},
		commission_split: {
			heading: '2: How the Commission Broke',
			intro: 'Alberta\'s Electoral Boundary Commission finished its work on March 23, 2026 and could not agree. Three commissioners produced one map; the other two produced a different one. Commission Chair Justice Dallas K. Miller and two opposition-nominated commissioners wrote the majority report; two government-nominated commissioners — Dr. Julian Martin and John D. Evans — wrote the minority report. The split centred on how to draw boundaries in fast-growing urban-edge communities: the majority gave Airdrie two districts, the minority four; the majority drew northwest Calgary\'s divisions close to the provincial average size, the minority drew them 11.5% above it. Both maps follow the same statute; the disagreement was about which specific geographic configurations best served the communities being drawn. Both are legal under the <em>Electoral Boundaries Commission Act</em>. The governing party is the United Conservative Party (UCP); its main opposition is the New Democratic Party (NDP). Alberta also has smaller parties — the Alberta Party, the Liberal Party of Alberta, and others — that contest seats but whose combined provincial vote share has remained low enough in recent elections that they do not materially affect the audit\'s partisan-fairness calculations, which are grounded in the 2023 UCP–NDP vote split. This audit measured both maps using the same methods, applied identically. Three findings stand out.',
			finding1: '<strong>The two maps differ on six things you can measure without looking at any election results:</strong> how evenly people are spread across districts, whether voters are concentrated, how badly cities are cut up, whether borders follow city limits, the shape of the districts, and how many boundaries the commission\'s own chair flagged as anomalous. The minority map differs from the majority on every one of them.',
			finding2: '<strong>Every measured difference cuts the same way.</strong> Everywhere the two maps diverge — northwest Calgary, Airdrie, urban areas with clear city limits — the minority map draws boundaries that spread NDP votes thinner and let UCP votes count more efficiently. The communities most reshaped by the minority map are the same communities where the NDP is strongest. The audit cannot determine intent. It can measure effect.',
			finding3: '<strong>The process now promoting the minority map has no precedent in Canada.</strong> No other province lets a cabinet hand redistricting to a committee its own party controls partway through a redistribution cycle. Most provinces either require the legislature to debate the commissioners\' map first, or give the commission\'s map automatic effect unless overridden. Alberta does neither. On April 16, the government set both commission maps aside and assigned the work to a five-member committee of MLAs (Members of the Legislative Assembly), three from the governing United Conservative Party (UCP). Alberta\'s <em>Electoral Boundaries Commission Act</em> requires the legislature to pass a separate Electoral Districts Act to give a commission report legal effect — the commission report itself changes nothing. Most other provinces make a commission\'s report legally effective unless the legislature actively overrides it; Alberta\'s default reverses that, meaning the governing party controls whether any commission map ever becomes law. The government\'s stated justification was to implement Commission Chair Justice Miller\'s Recommendation 5. But Miller had written that recommendation specifically to dissuade the legislature from accepting the minority map, and his majority colleagues did not endorse it. Recommendation 5 was also geographically specific: one additional rural seat south of Edmonton, and one in Clearwater County and western Mountain View County — both far from the fast-growing Calgary and Edmonton urban-edge communities where the commission actually split. It was not an invitation to redesign those contested boundaries. The government adopted the seat count while handing a committee it controls authority over exactly the lines the commission disagreed on.',
			closing: '<strong>The process is its own finding, separate from the maps.</strong>'
		},
		november: {
			heading: '7: The Lunty Committee',
			context_label: 'CONTEXT',
			context_body: ' — This section describes the process that replaced the commission and the legal framework that applies to it. It is not part of the statistical findings. The findings are in §3–§6 above.',
			intro: "Neither commission map is in force. The government set both aside in April 2026 and referred redistricting to a Special Select Committee of five MLAs — three UCP, two NDP — chaired by Brandon Lunty (UCP, Leduc-Beaumont). The committee itself does not draw the map; it oversees a separate advisory panel of five appointees (government-appointed chair, two UCP nominees, two NDP nominees) tasked with producing a 91-seat boundary proposal. The committee must deliver its report to the Legislature by November 2, 2026. Unlike the original commission, neither the committee nor the advisory panel is required to hold public hearings; the panel draws on submissions the original commission gathered. The all-party committee sought a retired or sitting judge to chair the advisory panel; Alberta's acting chief justice declined to nominate one. When the committee's map is released, this audit will apply the same methodology to evaluate it.",
			h_anomalous: 'Why the Committee Is Anomalous',
			anomalous_p1:
				"Canadian redistricting practice has, since the 1960s, settled on a single model: an independent commission, insulated from government direction, produces boundary recommendations; the legislature may debate them but cannot easily override them without a formal legislative vote. Alberta's statutory process under the <em>Electoral Boundaries Commission Act</em> follows this template — but with one structural difference from most provinces: Alberta's commission report has no automatic legal effect. Under the Act, a separate Electoral Districts Act must be passed by the legislature to give any commission map force of law. That means the government of the day controls not only whether the commission map is debated, but whether it ever becomes law at all. Other Canadian jurisdictions take the opposite default: the commission's recommendations take effect unless the legislature affirmatively votes to override them.",
			anomalous_p2:
				"What the government did in April 2026 has no recorded precedent in post-Confederation redistricting: it allowed a completed, published commission process to conclude — both majority and minority reports filed — and then referred the redistricting task to a five-member committee of MLAs whose majority (three of five) is held by the governing party, without bringing either commission report to a vote. The Lunty committee is not a commission. It has no statutory independence from the government's legislative direction. Its three-member UCP majority mirrors the government's control of the legislature. No other Canadian province has transferred redistricting authority, mid-cycle, to a government-controlled legislative committee after an independent commission had completed its work.",
			h_framework: 'The Constitutional Framework',
			framework_p1:
				'Section 3 of the <em>Charter of Rights and Freedoms</em> — "Every citizen of Canada has the right to vote in an election of members of the House of Commons or of a legislative assembly" — has been interpreted by the Supreme Court of Canada to guarantee not merely the act of casting a ballot but <em>effective representation</em>. The leading authority is <em>Reference re Provincial Electoral Boundaries (Saskatchewan)</em> [1991] 2 SCR 158, in which McLachlin J. (as she then was) wrote for the majority that the purpose of s.3 "is not equality of voting power per se, but the right to effective representation." Population parity is the primary consideration; departures are permitted when justified by community of interest, geography, history, or minority-representation objectives.',
			framework_p2:
				"The Saskatchewan framework does not categorically prohibit partisan considerations in redistricting. What it establishes is that boundary maps must, on the whole, provide effective representation to voters — and that systematic impairment of one identifiable group's ability to elect proportionate representation is the pattern that s.3 challenges target. The audit's statistical and structural findings — the minority map's position at the 99.99th percentile of 1,010,000 neutral draws, its crossing of all five structural thresholds, the identified communities affected — are the evidentiary record a s.3 applicant would need to assemble. Whether that record meets the constitutional threshold is a legal question this audit does not decide; the audit reports the measurement.",
			framework_p3:
				"The committee's legality as a process is a separate question. Alberta's <em>Electoral Boundaries Commission Act</em> does not expressly prohibit the legislature from constituting a parallel redistricting body, because the Act contemplates that the legislature will enact the final boundaries through ordinary legislation regardless. Whether the committee process, if it produces a map with the structural and statistical profile of the minority proposal, could survive a s.3 Charter challenge turns on whether effective representation is achievable under the resulting boundaries — the same test that would apply to any commission-produced map.",
			h_quebec: 'The Quebec Contrast',
			quebec_p1:
				"Quebec offers the comparison most relevant to Alberta's situation. Quebec's Commission de la représentation électorale (CRE) is a permanent, independent electoral boundaries body, not an ad hoc commission constituted per redistribution cycle. The CRE operates continuously and cannot be dissolved or bypassed by cabinet action. Under Quebec's <em>Loi électorale</em>, the National Assembly must adopt the CRE's recommendations unless it votes to deviate — and deviations require a two-thirds majority of all members of the Assembly, not a bare legislative majority. The practical effect is that a governing party cannot, acting alone with its own majority, substitute its preferred map for the commission's. Cross-party agreement is constitutionally required to override the independent body's judgment.",
			quebec_p2:
				"Quebec's model emerged partly from lessons about what happens when redistricting is not insulated from partisan control. The contrast with Alberta's current process — where a majority-controlled committee has replaced the commission's work before the legislature has voted on either commission report — illustrates the structural difference between redistricting systems that assume partisan pressure and design against it, versus systems where that pressure has a clearer path to the outcome.",
			closing:
				"The audit will apply the same tests to the Lunty committee's map when it is released. The constitutional and comparative observations above are contextual; the methodology does not change."
		}
	},
	section7: {
		heading: 'Canada is different — and similar',
		p1: 'Canada belongs to the same family as the U.S., the U.K., and Australia. We elect single members from geographic districts under first-past-the-post. We redraw the lines periodically — federally after each decennial census, provincially on staggered schedules. We inherited the basic machinery from the same Westminster roots. So far, no surprises.',
		p2: 'What sets Canada apart is the test the lines have to pass.',
		p3: 'In American constitutional law, the binding rule is <em>one person, one vote</em> — districts must have populations as nearly equal as practicable, and large departures require strict justification. In Canadian constitutional law, the binding rule is different. Section 3 of the <em>Canadian Charter of Rights and Freedoms</em> guarantees every citizen the right to vote. In <em>Reference re Provincial Electoral Boundaries (Sask.)</em> — the 1991 Saskatchewan Reference, the leading case — the Supreme Court of Canada interpreted that right as a right to <em>effective representation</em>, not a right to mathematical equality of district populations.',
		p4: "That distinction matters. Effective representation allows district populations to vary, sometimes substantially, when there are good reasons: vast rural geographies one MLA cannot reasonably serve at standard population density, communities of interest that should be kept together, minority representation mathematical equality would dilute. The Saskatchewan Reference made that flexibility constitutional. The EBCA's 25% population variance — the rule that protects rural Alberta seats — flows directly from it.",
		p5: 'The catch is that flexibility cuts both ways. If a commission can legitimately depart from population equality for the right reasons, it can also depart from population equality for the wrong ones. Canadian law has no American-style mathematical floor to fall back on. It has the effective-representation test, applied by judges, after the fact, in litigation. Most jurisdictions guard against the wrong reasons with structural protections: federal redistricting commissions are insulated by statute and their recommendations take effect automatically if Parliament does not act on them within a deadline. Quebec uses a permanent independent commission whose work the National Assembly can override only with a two-thirds supermajority. British Columbia operates under a similar default-adopt rule.',
		p6: 'Alberta is the exception. Under the <em>Electoral Boundaries Commission Act</em>, the commission\'s report is a recommendation only — the legislature must vote to enact it. That is normally a formality. In the 2026 cycle, the commission split 3–2 and produced two competing proposals; the legislature created a separate MLA committee, chaired by a Premier-appointed MLA, to choose between them. Nothing in Canadian constitutional law required that committee to exist. Nothing requires its choice to follow the commission\'s process. That is the structural gap this audit is examining.',
		p7: 'So when Canadian courts say "gerrymander" isn\'t their legal vocabulary, they are not saying the underlying concept does not apply here. They are saying the test is different — effective representation, not mathematical equality. Whether the minority proposal meets that test is exactly the question this audit has measured the geometry against, and exactly the question only a judge can answer definitively. The <em>Saskatchewan Reference</em> reasoning in full, the contrast with other provinces, the standing question, and the available reform pathways are treated in <a href="#references">the references section below</a>.'
	}
} as const;
