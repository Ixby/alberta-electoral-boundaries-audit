// English — source of truth.
// Mirrors the editorial content in proposals/stakes_and_glossary_draft.md.
export default {
	selector: {
		label: 'Choose language'
	},
	verdict: {
		headline: 'Alberta is redrawing its electoral map.',
		p_what: 'Every so often the province redraws its ridings — the local areas that each elect one MLA. Where the lines fall decides who you vote with, and who represents you in the legislature.',
		p_split: 'This time, the panel doing the redraw split. It produced two competing maps — and this audit tests both of them.',
		p_question: 'We tested both maps for one question: is either one shaped to favour a party — even if no one set out to do that?',
		p_answer: 'One of the two is. The other looks normal.',
		p_howfar: 'A computer drew 1.01 million legal versions of the map at random. One of the two real maps is more one-sided than all but about 1 in 568,000 of them, in the UCP’s favour. The other sits in the normal range.',
		aside_pre: 'You might call a map shaped like that ',
		aside_post: '. That word has no legal meaning in Canada, so we don’t use it as a verdict. We show you what the map does; you judge. For the deeper layers — what the law actually requires, and exactly how we ran the test — see ',
		box_heading: 'What we can and can’t say',
		box_can_1: 'The minority map sits outside what 1.01 million neutral maps produce, in the UCP’s favour.',
		box_can_2: 'All four partisan-fairness measures point the same way.',
		box_cant_1: 'That any commissioner intended this — the audit reads outcomes, not motives.',
		box_cant_2: 'That the map “is” a gerrymander — that isn’t a category Canadian law recognizes.',
		box_cant_3: 'How a court would rule, or what the committee will choose.',
		law_link: 'Law',
		methods_link: 'Methods'
	},
	why_redrawn: {
		heading: 'Why this happens — and why it touches you',
		p1: 'Alberta is divided into 87 ridings. Each one elects a single MLA to the legislature. Your riding decides who that person is, which neighbourhoods get grouped with yours, and whose concerns your MLA hears first.',
		p2: 'The lines don’t stay fixed. As people move and cities grow, some ridings end up with far more voters than others, so the province redraws the map every few years to keep them roughly even. A panel of commissioners does the drawing, working from rules set out in law: districts have to be close in population, stay in one piece, and keep real communities together where they can.',
		p3: 'That’s the normal process. This time it broke down. The commissioners couldn’t agree, and split into two camps, each with its own map. Then a committee of MLAs set both of those maps aside and began drawing its own, larger one. A legislative committee overriding the commission like that is rare.',
		p4: 'A line on a map decides whose vote counts for what. It can keep a community’s voters together, or scatter them across several districts where their numbers no longer add up to much. It can keep some races close and put others out of reach. None of that shows on the surface; it is set by where the boundaries fall.'
	},
	two_maps: {
		heading: 'Two maps — and who drew them',
		p1: 'When the commission split, it didn’t produce one map with a dissent attached. It produced two complete, competing maps. Both are legal. They just draw the lines differently.',
		p2: 'A boundary commission has five members. The Chief Justice of Alberta names the chair — the neutral seat, here held by Dallas K. Miller, a former Court of King’s Bench judge. The party in government names two members; the opposition names two.',
		p3: 'This commission divided three to two. The chair and the two opposition-appointed members backed one map — the majority report, because most of the commission signed it. The two government-appointed members backed the other — the minority report.',
		p4: 'The map the audit flags as the more one-sided is the minority report — the one the two government-appointed members drew. The audit can’t show whether they meant to, and doesn’t try. It shows what the map does.',
		p5: 'The cover map at the top of this page lets you compare them yourself. Flip between the two proposals and today’s map, find your own riding, and watch which neighbourhoods get grouped together or split apart.',
		p6: 'A committee of MLAs has since set both maps aside to draw its own, due later in 2026 — a move this site looks at on the Law page. These two remain the audit’s clearest test case, and the same tests will apply to whatever the committee produces.'
	},
	disclaimer: {
		text:
			'AI translated this site. Some of it may still appear in English while the translations are in progress. If you notice errors or would like to help translate this project, please %s.',
		link_label: 'contact us',
		// {count} is replaced at runtime with the live word count of the
		// English prose, so volunteer translators know the size of the job
		// before raising their hand. Computed, never hardcoded — it stays
		// correct as the prose grows.
		word_count: 'For scale: the English prose runs about {count} words. You are welcome to take on all of it or just a part. In most cases the work is fixing small errors the machine made, not translating from scratch.'
	},
	// Opening epigraph: a real exchange that frames how to read the cover map and
	// states the project's ethic before any finding. The commenter is anonymized
	// ("a reader"); the author's reply is a faithful paraphrase of the original.
	epigraph: {
		heading: 'On reading this map',
		reader:
			"Land doesn't vote. Colouring the map this way only makes rural Alberta look bigger than it is. Leave the empty land empty.",
		reader_label: 'a reader',
		author_p1:
			"Fair \u2014 and that is exactly what the map does. It is built from Elections Alberta's own geometry and counts, at the only resolution they keep: how many people voted in each voting area, and how. The colour runs on a spectrum between the two parties, and its depth follows population \u2014 which is why the cities glow and the open country stays pale.",
		author_p2:
			"The land west of Ponoka is pure white: no polling station, no one recorded living or voting there. It is blank precisely because land doesn't vote. The aim is not to interpret the data, only to let it speak at the grain it was recorded in \u2014 and to leave you a little wiser than you came.",
		author_label: 'the author',
		ethic:
			'That is the commitment behind the whole audit: map the system, and let the data speak for itself \u2014 no more than it allows.'
	},
	opener: {
		heading: "Who's this for?",
		body:
			"Us. All of us. Rural, Urban, curious, wonk, journalist, lawyer, academic, politician — all of us. Because it impacts all of us. Whether or not you like the party in power, what the split commission produced has never been done before. And it's given us the opportunity to peer inside the machine in ways we never could before. Now we can establish a baseline — a series of tests, and everything that comes after can be graded on it. Let me show you what I found."
	},
	stakes: {
		q1: {
			heading: 'Is the proposed map a gerrymander?',
			body:
				'"Gerrymander" is not a term Canadian courts use, and this audit does not apply it as a verdict. What the audit can say is narrower and factual: four of the five structural tests it runs flag the <em>minority proposal</em> and none flag the alternative (the <em>majority proposal</em>); the fifth test is neutral for both. Whether that pattern amounts to what people informally mean by a "gerrymander" is a judgment this audit leaves to the reader.',
			footnote:
				'The "majority" and "minority" names come from a 3–2 split among the Electoral Boundaries Commission (chaired by Justice Miller), which produced two competing proposals rather than a single recommendation. The legislature has since set both aside and referred redistricting to a six-MLA committee chaired by Brandon Lunty (a UCP MLA); the committee oversees a separate four-person Independent Advisory Panel — two members nominated by the Premier (Hon. Monte Solberg and Darwin Durnie), two by the Leader of the Opposition (Dr. Gerard Kennedy and Brent Robinson) — tasked with producing a new 91-seat boundary proposal before the November 2026 deadline.'
		},
		q2: {
			heading: 'What does "gerrymander" mean in Canadian law?',
			body:
				"There isn't one. The Canadian test is different: whether the boundaries give voters <em>effective representation</em> under section 3 of the Charter. The minority proposal raises serious questions under the effective-representation standard; only a judge can answer them definitively, and no one has asked one yet."
		},
		q3: {
			heading: "What's at stake for Albertans?",
			body:
				"At a 50/50 provincial vote, the audit's measurements place the minority proposal at a structural extreme: fewer than 100 of the 1.01 million neutral comparison maps produce the same kind of seat imbalance. That imbalance matters because a 60-of-89 majority leaves only a token opposition and is effectively immune to internal dissent — not because it crosses any special threshold (Alberta's Assembly has no two-thirds rule; the same procedural powers are available to a bare majority). Whether the minority proposal's tilt is large enough to push one party past that 60-seat threshold at vote shares <em>other</em> than 50/50 is a question this audit has not yet tested. Whether that imbalance is acceptable is a question for Albertans, not for this audit."
		},
		cta_law: 'Read the legal context →',
		cta_methods: 'See how we tested →',
		scorecard_h: 'The scorecard',
		scorecard_fig_alt:
			'Scatter plot: efficiency gap on the horizontal axis, count of structural tests failed on the vertical axis. The 2019 enacted map and the 2026 majority map cluster in the safe lower-left corner. The 2026 minority map sits alone at upper right, on the four-of-five structural line and just short of the dashed ~4.1% efficiency-gap line. The 2019 map is labelled 0 of 4 run: the Calgary zone test was never run on it.',
		scorecard_fig_caption:
			'Both lanes on one picture. Horizontal: how skewed the partisan-fairness number is (right = more UCP-favoured). Vertical: how many of five structural-fairness tests the map fails. Bottom-left is the safe corner where neutral procedures routinely land; the upper-right is the outlier region. The 2019 enacted map and the 2026 majority sit in the safe corner (the 2019 map was scored on four of the tests; the Calgary zone test was never run on it). The 2026 minority sits alone in the outlier region.',
		scorecard_intro:
			'Two independent measurements applied to both maps under the same pre-registered thresholds. Structure uses only the shape of the lines — no election results. Numbers tests how the lines convert votes into seats. Both lanes reach the same conclusion.',
		scorecard_close:
			'Two independent measurements, one answer. The convergence is the audit\'s strongest single signal.'
	},
	top_callouts: {
		gerrymander_lead: 'Is the minority map a gerrymander?',
		gerrymander_body: 'On the audit\u2019s joint partisan-bias score, the commission\u2019s minority map sits in the extreme tail of 1,010,000 algorithmically-drawn neutral comparison maps \u2014 approximately 69 of them reach its seat share at a tied vote, and the odds of its combined profile under neutral drawing are at most roughly 1&nbsp;in&nbsp;568,000. The majority map falls well within normal range.',
		tldr_label: 'TL;DR',
		tldr_p1: 'Alberta’s commission split, the government took the pen, and a six-MLA committee (the Lunty committee) reports in November 2026. Neither commission map is law.',
		tldr_p2: 'This audit tested both commission maps the same way, against 1,010,000 computer-drawn neutral maps built from official Elections Alberta files. The majority proposal looks like the maps neutral drawing routinely produces \u2014 it passes every pre-registered test. The minority proposal crosses four of five structural tests, and at a tied 50/50 vote only about 69 of the 1,010,000 neutral maps award as many seats as it does. The odds that a neutral process produces its overall fairness profile work out to about 1 in 568,000 \u2014 and that figure is a deliberately cautious ceiling, not a precise estimate. One measure, the efficiency gap, landed just under the audit\u2019s pre-set line; it is reported as a miss.',
		tldr_p3: 'The audit measures outcomes, not intent. When the Lunty committee releases its map, this audit will apply the same tests to it.',
		tldr_footer: 'Pre-registered falsification conditions and retraction commitments are in %s.',
		tldr_footer_link: 'Retractions and Corrections'
	},
	picture: {
		heading: 'The picture, before the proof',
		lead:
			'Three maps, two ways of measuring. One dot is not like the others. This picture is the audit\u2019s whole case in one image \u2014 and right now you have no way to judge whether it means anything. The lines on it are not laws. The corner is not a courtroom. By the end of this page you will know exactly what this picture can prove, and exactly what it cannot. The log comes back to it at the end.'
	},
	head: {
		title: "Alberta's Electoral Map, Audited",
		meta_description:
			"Alberta's 2026 boundary commission filed two maps. One looks normal; the other favours the UCP further than nearly every one of 1,010,000 neutral maps. The 91-seat map that followed, drafted by an advisory panel under a committee of MLAs, is scored here against tests fixed in advance."
	},
	nav: {
		skip_to_content: 'Skip to content',
		home_aria: 'Back to top',
		theme_aria: 'Toggle dark/light mode',
		theme_title: 'Toggle dark mode',
		nav_aria: 'Open table of contents',
		drawer_top: '↑ Top',
		route_story: 'Story',
		route_law: 'Law',
		route_methods: 'Methods',
		// Compact landmarks shown on the sticky bar
		stakes: 'Stakes',
		findings: 'Findings',
		history: 'History',
		reform: 'Reform',
		// Drawer group headings
		group_overview: 'Overview',
		group_audit: 'The audit',
		group_context: 'Context',
		group_forward: 'Going forward',
		group_apparatus: 'Apparatus',
		// Drawer entries
		why: 'Why does this matter?',
		map: 'The map at a glance',
		split: 'How the commission broke',
		litmus: '1,010,000-Map Litmus Test',
		crack_pack: 'Cracking, packing, draining',
		for_you: 'What this means for you',
		impact: 'Impact on the ground',
		gerrymanders: 'Clean gerrymanders',
		history_full: 'A history of gerrymandering',
		canada: "Canada's different",
		lunty: 'Lunty',
		suggestions: 'Reform suggestions',
		smoking_gun: 'The smoking gun',
		picture: 'The picture',
		act1: 'Act I: The map',
		act2: 'Act II: The simulation',
		act3: 'Act III: The conduct',
		revisited: 'The scorecard, revisited',
		explainers: 'Explainers A\u2013N',
		retractions: 'Retractions',
		authors_view: "The author's view",
		references: 'References',
		technical: 'Technical resources',
		feedback: 'Send feedback',
		// New main-page sections (2026-10-29 rewrite)
		happened: 'What happened',
		does: 'What the map does',
		law: 'What the law requires',
		system: 'How the committee got the job',
		know: 'How we know',
		test: 'The November test',
		mind: 'What would change my mind',
		evidence: 'The full record',
		fixes: 'Fixes for next time',
		// Shared site header (every page)
		bar_aria: 'Site',
		bar_home: 'Main page',
		bar_evidence: 'Full record',
		bar_explorer: 'Map explorer',
		bar_norms: 'Norms',
		bar_explainers: 'Explainers',
		bar_fixes: 'Fixes',
		bar_feedback: 'Feedback',
		group_this_page: 'On this page',
		group_pages: 'Pages'
	},
	hero: {
		h1: 'Laws, Norms, & Statistics: An Audit of the 2026 Alberta Electoral Boundaries Commission Reports',
		subtitle:
			"Alberta's commission produced two competing riding maps in 2026. I ran the same tests on both and asked one question: do they treat voters the same way?",
		badge: 'Commission maps, final report March 2026',
		cover_note: 'Click to zoom in and explore all three boundary maps at once: both commission proposals and the map in force today. Pin the viewport and flip between maps. The boundaries shift; the voters stay put. Scroll down for the analysis.',
		cover_note_1:
			'This map is the best way in. Click it to zoom and explore. The buttons at the top switch between the minority map, the majority map and the 2019 enacted boundaries, or layer all three to see exactly where they part ways. <strong>Detail</strong> colours each polling area by how people voted in 2023. <strong>Trend</strong> adds party shading by district (blue UCP, orange NDP). <strong>Lines</strong> turns boundaries on and off. <strong>Find</strong> jumps to any riding by name.',
		cover_note_2:
			"Lock the viewport and flip between maps. Watch a boundary move while the voters underneath stay still. The whole question, in one gesture.",
		cover_note_3:
			"When you're done exploring, scroll down for the summary. The full technical analysis is in the Resources section. All of the data comes from official Elections Alberta shapefiles and other government and open-source records.",
		image_alt:
			'Alberta electoral district map — minority commission proposal, coloured by 2023 vote',
		map_hint: 'Click to explore interactively',
		btn_title: 'Click to open interactive map',
		btn_aria: 'Click to explore interactively'
	},
	boundary: {
		heading: "What this audit can and can't tell you",
		can_1:
			"The minority map's geometry crosses 4 of 5 pre-registered structural thresholds <em>without using any election data at all</em>. The fifth (anchoring) is neutral. The majority crosses 0 of the 4 firing. These tests measure properties of the boundary lines themselves — district shape, municipal anchoring, population spread — and reach the conclusion before any vote is counted.",
		can_2:
			'Separately, when election data is brought in, the minority map sits at the 99.99th percentile of 1.01 million algorithmically-drawn comparison maps matched on population balance and contiguity (the ensemble enforces those two requirements, not every statutory criterion such as communities of interest). Roughly 69 of those 1.01 million neutral maps reach the same seat share at a tied vote. Counting both analytical channels, the odds of this profile under neutral drawing are at most about 1 in 568,000. Two analytical instruments — geometric and statistical — reach the same conclusion, favouring the same party; the joint bound is the dependence-aware summary of that convergence, not four independent tests reading in agreement.',
		can_3:
			"Three of the configurations the minority proposal contains were flagged in writing by Commission Chair Justice Miller in the majority report's response to the minority (final report, pp. 62–63). The audit's tests were run with no knowledge of his flags and surface the same regions. Because Justice Miller chaired the commission and signed the majority report, these are the chair's own criticisms — corroborating, not a fully independent third instrument — but the audit's blind tests landing on the same regions is still striking.",
		cant_1:
			'The audit does <strong>not</strong> establish that any commissioner intended the partisan effects it measures. Boundary geometry cannot reveal intent.',
		cant_2:
			'The audit does <strong>not</strong> predict what the Lunty committee will choose, what the November 2026 vote will be, or how Albertans will react.',
		cant_3:
			'The audit does <strong>not</strong> predict how a court would rule if a Charter challenge were brought against either proposal.',
		cant_4:
			"The audit does <strong>not</strong> claim the dependence-robust bound of approximately 1 in 568,000 (p&nbsp;≤&nbsp;1.76×10<sup>−6</sup>) is the probability that a gerrymander occurred. That number is the tail probability of the minority's geometry under a neutral algorithmic null. It is evidence the neutral null is implausible. It is not a posterior probability of partisan intent — that question requires evidence the geometry cannot supply.",
		cant_5:
			"The audit does <strong>not</strong> tell any individual voter what position to take or what to do with this information. The choice is yours."
	},
	editorial_intro: {
		heading: 'What is redistricting, and why it matters',
		p1: 'Every voter in Alberta lives in an <em>electoral district</em> — a slice of the province that elects one person to the legislature. There are 87 districts. Each district elects one MLA. When you cast a ballot in a provincial election, you are choosing the MLA for the district you live in. For most Albertans, that is the whole connection to the legislature: one MLA, one district, one vote.',
		p2: 'Those district lines are not permanent. People move, neighbourhoods grow, rural areas thin out, cities sprawl. Every eight to ten years, Alberta is supposed to redraw the lines so each district is roughly the right size and reflects the way Albertans actually live now. The body that does the redrawing is the <em>Electoral Boundaries Commission</em> — an independent commission with judges, lawyers, and public members, not politicians.',
		p3: "This is the standard process. This time, the standard process produced something unusual. The commission's five members split 3–2 on what the map should look like, and rather than settling on one recommendation they produced two: a <em>majority proposal</em> (backed by three commissioners) and a <em>minority proposal</em> (backed by two). Both are sitting on the table. On April 21, 2026 the Legislative Assembly passed Government Motion 37, setting both aside and referring redistricting to a six-MLA Select Special Committee chaired by Brandon Lunty (a UCP MLA). The committee oversees a separate four-person Independent Advisory Panel, constituted under the same motion, tasked with producing a new 91-seat map; the committee must deliver its report to the legislature by November 2, 2026.",
		p4: "Why it matters to you: the lines decide who your MLA is. They decide which neighbourhoods, towns, and concerns get represented together. If your city is split across four MLAs instead of one, no single representative is accountable for the city as a whole. If your community of interest — a small town, a rural region, a downtown core — is divided between districts, your voice on provincial decisions is diluted. The map also shapes which party can form a government, and at what margins. The audit's specific finding (the minority proposal sits at a structural extreme) is the reason you are reading this site, but the broader question is older and applies to every redistricting cycle: do the lines reflect the way Albertans live, or do they shape the politics following?",
		p5: 'The rest of this page walks through what the two proposed maps actually do.',
		key_terms_lead: 'Key terms in this section — click to read:'
	},
	editorial_reflect: {
		heading: 'Interlude: What this means for you and your community',
		intro_p1:
			"The log pauses here. Which party gains or loses seats is the legislature's problem — it is not where you experience these maps. You experience them through three concrete questions about your own district:",
		intro_q1: 'Where does your MLA live?',
		intro_q2: 'Are they invested in your community?',
		intro_q3: 'Will the demands of the district\'s urban head dominate its rural tails?',
		intro_p2:
			'Every other framing — partisan advantage, supermajority threshold, statistical extreme — eventually points back to those three. The five rungs below walk through how each proposed map answers them, at five scales.',
		you_h: 'You.',
		you_p:
			"Your electoral district decides who represents you in the legislature. Right now you live in one of 87 districts. Under both proposed maps you may live in a different one — possibly with a different MLA, possibly anchored to different neighbouring communities. If you don't know what district you're in right now, or who your MLA is, you're not alone: most Albertans couldn't name their MLA. But the boundary lines are not abstract. They decide whose phone number is on your local representative's office wall, whose neighbourhood petition gets your name attached to it, whose concerns your MLA hears about first. The map explorer on this site — search for your community by name — shows which district you sit in under each proposal. If your district changes, your representative changes — and your representative's relationship to your community changes with it.",
		community_h: 'Your community.',
		community_p:
			'Communities are not abstract either. A high school\'s catchment area, a chamber of commerce, a faith community, a neighbourhood association — these are real groupings of people with shared local concerns. When a boundary line cuts through them, no single MLA is responsible for the whole. Casing 1 is the extreme case: Airdrie, one city in four pieces, no single representative accountable for it. The same dynamic plays out anywhere a town, neighbourhood, or recognised community of interest is split — the bigger the split, the weaker the representation. (On the broader measure of how faithfully each map follows municipal lines overall, both proposals sit inside the Canadian norm — Casing 5 records the finding that dissolved.)',
		municipality_h: 'Your municipality.',
		municipality_p:
			"When a city is fractured across many representatives, its ability to bargain on provincial decisions weakens. A council asking for transit funding, a school board negotiating a new school, a mayor lobbying for highway extensions — each of those goes better when the city can point to a few MLAs who owe accountability to the city as a whole. The minority proposal splits Calgary's north, east, and central districts across multiple divisions whose vote-share patterns suggest <em>packing</em> (concentrating one party's voters into a few high-margin seats) on top of <em>cracking</em> (splitting the other party's voters across many low-margin seats). Whether the pattern is intentional is a question the audit cannot answer — boundary geometry doesn't reveal intent. What it can say is that the four statistical measures flag the same districts the structural tests flag, and that the alternative proposal does not produce the same fingerprint.",
		region_h: 'Your region.',
		region_p1:
			"If you live outside Alberta's cities you have probably noticed political conversations about boundaries always seem to centre the cities. It's a fair complaint, so let's be direct about what this audit does and does not say about rural Alberta.",
		region_p2:
			"What it does <strong>not</strong> say: rural Alberta has too many seats. The EBCA allows district populations to vary by up to 25% so one rural MLA isn't representing a geography the size of southern France. Canadian courts treat the variance as legitimate. Both proposed maps preserve it. Nothing in this audit changes it.",
		region_p3:
			'What it <strong>does</strong> say: in several places on the minority proposal, rural communities are being attached as the <em>tail</em> of a district whose population centre sits in a city. Look at Casing 1\'s Airdrie split again, this time from the rural side: three of its four districts extend out into a different stretch of rural countryside, and in each the population centre is the urban slice, not the rural tail. An MLA elected from that kind of district is most likely to live, campaign, and prioritise where the votes are — which means rural communities formerly represented by a dedicated rural MLA become the back half of an urban-led seat. That pattern repeats on the minority proposal in ways it does not on the majority proposal.',
		region_p4:
			"The audit doesn't propose taking seats away from rural Alberta. It asks whether the lines respect the rural communities those seats are meant to represent, or whether rural geography is being used as ballast to absorb urban votes into districts whose centre is somewhere else. If you live in one of those rural tails, the question of which map gets enacted decides whether your MLA represents the rural community you actually live in, or an urban district whose lines happen to include your land.",
		province_h: 'Your province.',
		province_p:
			"The legislature is what you get when you sum every district's answers to the three questions above. If most districts are anchored to communities whose MLAs actually live in them, the legislature represents those communities. If most districts have rural tails attached to urban heads, the legislature represents the heads — and the tails get whatever attention is left over. The partisan question — which party wins a majority — is downstream of that. The large-majority question — whether one party crosses 60 of 89 seats, a margin that makes a government effectively immune to floor-crossings and leaves an opposition too small to sustain scrutiny — is downstream of <em>that</em>. At a hypothetical 50/50 provincial split, the audit's measurements place the minority proposal at a structural extreme: fewer than 100 of the 1.01 million neutral comparison maps produce the same kind of seat imbalance. Whether that imbalance pushes a party past 60 seats at the vote shares Albertans actually deliver is a question this audit has not yet directly tested — an honest gap in the record. Whether the answer to any of these questions matters enough to act on is, again, a question for you."
	},
	editorial_history: {
		heading: 'Context: A short history of gerrymandering',
		p1: 'The word comes from 1812. Massachusetts governor Elbridge Gerry signed off on a state-senate map whose districts were so contorted in his party\'s favour that a Boston cartoonist drew one of them as a salamander — wings, claws, a forked tongue. The cartoonist\'s pun, <em>Gerry-mander</em>, stuck. The shape stuck too: two centuries later, the word still means drawing electoral lines to engineer a partisan outcome.',
		p2: 'The term endures because the problem endures. Anywhere voters choose representatives from geographic districts, someone has to draw the lines, and the lines can be drawn many ways. Different countries have arrived at different answers about who should do the drawing and what should constrain them.',
		p3: '<strong>The United States</strong> treats partisan gerrymandering as a problem the federal courts mostly cannot fix. In <em>Rucho v. Common Cause</em> (2019), the U.S. Supreme Court ruled that partisan gerrymanders are nonjusticiable "political questions" the federal courts will not resolve. Some states (California, Michigan) have responded by creating independent citizen commissions to draw their own lines; others (Texas, North Carolina) have continued to draw openly partisan maps and defended them on the basis that <em>Rucho</em> permits it.',
		p4: "<strong>The United Kingdom</strong> uses four permanent Boundary Commissions — one each for England, Scotland, Wales, and Northern Ireland — staffed by judges and senior civil servants. They redraw lines roughly every eight years against fixed rules (population equality, geographic coherence, respect for local government boundaries). Since the Parliamentary Constituencies Act 2020, their final recommendations take effect automatically by Order in Council, with no parliamentary vote required — Parliament's former power to reject them was removed.",
		p5: "<strong>Australia</strong> delegates the work to the Australian Electoral Commission, a federal independent agency with full authority over both election administration and boundaries. Redistributions happen automatically when a state's seat count changes or seven years pass since the last one. The commissioners' decisions are reviewable on procedural grounds but not on partisan ones. As in the U.K., gerrymandering as Americans know it is virtually unheard of.",
		p6: 'These three cases bracket the spectrum: courts staying out (U.S.), independent commissions with strong parliamentary deference (U.K.), and a permanent independent agency with full authority (Australia). Canada sits somewhere different again — which is what the next section takes up.'
	},
	glossary: {
		more_link: 'Learn more →',
		'electoral-district': {
			term: 'Electoral district (ED)',
			definition:
				'The geographic area that elects one member to the provincial legislature, often shortened to "ED" after first use. Each ED has one MLA. (The word "riding" usually refers to federal districts. Alberta\'s statutes call a provincial one an electoral division.)'
		},
		riding: {
			term: 'Riding',
			definition:
				'In Canada, the word most often means a federal electoral district. Alberta\'s statutes call the provincial equivalent an "electoral division". This site calls it a riding, a district or a division interchangeably.'
		},
		mla: {
			term: 'MLA',
			definition:
				'Member of the Legislative Assembly: the person one electoral district elects to represent it in the Alberta legislature.'
		},
		ucp: {
			term: 'UCP',
			definition:
				"United Conservative Party, Alberta's governing provincial party today. It formed in 2017 when the Progressive Conservatives and the Wildrose Party merged, and it has held government since 2019."
		},
		ndp: {
			term: 'NDP',
			definition:
				"New Democratic Party (Alberta NDP), Alberta's official opposition today. It held government from 2015 to 2019."
		},
		gerrymander: {
			term: 'Gerrymander',
			definition:
				'Drawing electoral boundaries to give a party an advantage. The word comes from an 1812 Massachusetts map. Canadian law has no offence by that name. That limits what a court will call it, not whether it happens. The closest legal test is effective representation under section 3 of the Charter.'
		},
		cracking: {
			term: 'Cracking',
			definition:
				"A gerrymandering technique: split a voting bloc across many districts so it never reaches a majority in any single one. Divide a city across four ridings, for example, and its voters are outnumbered in each."
		},
		packing: {
			term: 'Packing',
			definition:
				"A gerrymandering technique: crowd one party's voters into a small number of districts. The party wins those districts overwhelmingly but \"wastes\" many votes, and fewer of its voters are left to compete in other districts."
		},
		draining: {
			term: 'Draining',
			definition:
				"This audit's term for a follow-on effect of cracking and packing. The wasted votes those techniques produce get pushed into strategically chosen places, where they alter the political character of nearby electoral districts. The framing is the audit's own, not an established concept in the redistricting literature. The audit tests for the effect and finds results consistent with it, but treats it as exploratory, not as a settled methodology."
		},
		anchoring: {
			term: 'Anchoring',
			definition:
				'How firmly the proposed boundaries follow existing municipal lines, such as city limits and town boundaries. A highly anchored map mostly respects those lines. A loosely anchored map often departs from them. On the 2026 commission maps the test did not separate the two: both sit close to the 2019 map\'s 75%.'
		},
		'charter-s3': {
			term: 'Section 3 of the Charter',
			definition:
				'The section of the Canadian Charter of Rights and Freedoms that guarantees citizens the right to vote. Canadian courts read it not as a strict "one person, one vote" rule but as a right to "effective representation."'
		},
		'effective-representation': {
			term: 'Effective representation',
			definition:
				"The standard Canadian courts apply when they judge electoral boundaries. It means voters should have a meaningful voice. Equal riding populations are part of that, but so is recognition of community ties, geography and minority representation. The leading statement is from the Supreme Court of Canada's 1991 Saskatchewan Reference."
		},
		ebc: {
			term: 'Electoral Boundaries Commission (EBC)',
			definition:
				"The body that draws Alberta's provincial electoral boundaries under the EBCA. Justice Miller chaired the 2026 commission. Its commissioners split 3–2 and produced two competing proposals, the majority and minority proposals. Under s.9 of the Act, the majority's report is the commission's report."
		},
		'lunty-committee': {
			term: 'Lunty committee',
			definition:
				"The Select Special Committee on Electoral Boundaries: six MLAs, four UCP and two NDP, chaired by UCP MLA Brandon Lunty. Government Motion 37 (introduced April 16, passed April 21, 2026) created it after the Assembly set both commission maps aside. It oversaw an Independent Advisory Panel that drew a 91-seat proposal, and it had to send the panel's report to the Legislature by November 2, 2026. On October 28 it voted 3–2 to end its review without observations. It sits outside the standard commission process. No law required it to hold public hearings, and it held none."
		},
		'advisory-panel': {
			term: 'Independent Advisory Panel',
			definition:
				"The panel the Lunty committee engaged under Government Motion 37 to draw a 91-seat proposal. The Premier nominated the Hon. Monte Solberg and Darwin Durnie. The Leader of the Opposition nominated Dr. Gerard Kennedy and Brent Robinson. Alberta's acting chief justice declined to help find a judge to chair it, and retired Court of Appeal justice Brian O'Ferrall was later named chair. The panel drafted the map and reported on October 22, 2026. The committee reviews it and sends it to the Assembly, where the government's majority decides."
		},
		ebca: {
			term: 'EBCA',
			definition:
				'The Electoral Boundaries Commission Act — the Alberta law that sets the rules a new map must follow, including how far district populations may vary.'
		},
		ensemble: {
			term: 'The 1.01-million-map test',
			definition:
				'A computer drew 1.01 million Alberta maps with 87 districts each, step by step, under population and contiguity rules. All of them follow the same rules, and the computer never sees a vote, which is what makes them neutral. A real map counts as unusual when it falls outside what almost all of these maps produce.'
		},
		efficiency_gap: {
			term: 'Efficiency gap',
			definition:
				'A measure of "wasted" votes, compared between the two parties. A vote is wasted if it goes to a loser, or if it goes to a winner beyond what the win needed. A large gap points to a one-sided map.'
		},
		mean_median: {
			term: 'Mean-median gap',
			definition:
				'Take a party\'s vote share in each district. The mean-median gap is the distance between the average of those shares and the middle (median) one. A large gap suggests its voters are spread in a way that wastes votes.'
		},
		declination: {
			term: 'Declination',
			definition:
				'A measure of how lopsidedly each party wins its seats: by blowouts or by squeakers. After a June 2026 sign correction, it points the same way on the minority map as the other measures do, toward the governing party.'
		},
		seats_5050: {
			term: 'Seats at a tie',
			definition:
				'How many seats each party would win if the province split its vote exactly 50-50. It strips out who actually won and tests the map\'s built-in tilt.'
		},
		fsa: {
			term: 'Forward sortation area (FSA)',
			definition:
				'The first three characters of a Canadian postal code (the letter-digit-letter part). About 150 FSAs cover Alberta.'
		}
	},
	// Main page, rewrite of 2026-10-29 (proposals/site_rewrite_2026-10-29).
	// Generated from the accepted draft together with its markup in +page.svelte.
	home: {
		hero: {
			h1: "Alberta's Electoral Map, Audited",
			subtitle: "Alberta's boundary commission split in 2026 and filed two maps. I set both beside 1.01 million maps a computer drew with no stake in who wins. The majority's map sits among them. The minority's leans to the UCP further than almost any of them.",
			status: "The next map, with 91 seats, comes from an advisory panel that a committee of MLAs oversees. The committee had to send it to the Assembly by Monday, November 2, 2026. It becomes law only if MLAs pass a bill. I'll score it within 72 hours of its release.",
			week: "<strong>This week.</strong> The rules that decide the November verdict were fixed in June 2026, before the panel's map was made public, and <a href=\"https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/preregistration/november_2026_scoring_spec.md\" rel=\"noopener\">they're dated in the project's repository</a>. Three side tests and the choice of comparison set were added October 29–31, after opposition MLAs had described parts of the map at a committee meeting. I'll publish the scores whichever way they point. The first check is against the one recommendation the government cited: <a href=\"#recommendation-5\">Recommendation 5</a>.",
		},
		happened: {
			h: "What happened",
			p1: "Every so often Alberta redraws its ridings, the districts that each send one MLA to the Legislature. Where the lines fall can decide who wins.",
			p2: "On March 23, 2026 the independent commission doing the redraw split three to two and filed two maps. Both fit the Act's numeric rules. The majority argued the minority's map would likely fail the Charter's test; no court has ruled. The chair and the two commissioners nominated by the opposition wrote the majority map. The two commissioners nominated by the government wrote the minority map (<a href=\"https://www.assembly.ab.ca/about/news-and-announcements/2025/03/28/electoral-boundaries-commission-to-soon-begin-consultations\" rel=\"noopener\">Legislative Assembly of Alberta, March 28, 2025</a>). Same rules, same data, same 1,345 public submissions. Two maps.",
			p3: "The majority map looks like what a neutral process draws. The minority map doesn't:",
			li1: "It splits Airdrie, a city of 85,805, into four districts. Outside Airdrie East, which holds more than half the city, Airdrie's residents are outnumbered.",
			li2: "In north-east and central Calgary, its seventeen districts run 11.5% above the provincial average population. On 2023's votes the NDP wins eight of them.",
			li3: "Split the vote dead even and it hands the UCP 51.7% of the seats (46 of 89). Only 69 of 1,010,000 computer-drawn maps give more, and all 69 give 45 of 87 (51.72%), a hair above it.",
			li4: "Replay the 2023 election-day vote and the UCP takes 60 of 89 seats. On the majority map, 55.",
			p4: "The Assembly adopted neither map. On April 21 it passed Government Motion 37, which handed the job to the Select Special Committee on Electoral Boundaries, six MLAs with a UCP majority. An advisory panel under the committee drew a 91-seat map and reported on October 22. The panel itself split: its report includes a minority opinion. On October 28 the committee voted 3–2 to end its review without observations. It held no public hearings on the map and released no draft for the public to comment on. It had to send the panel's report to the Assembly by November 2. The map becomes law only if MLAs pass a bill.",
			box_h: "What I can say, and what I can't",
			can1: "On the four fairness measures combined, the minority map sits further out than all 1.01 million neutral maps, in the UCP's favour. Taken one at a time, three of the four put it deep in the UCP's tail.",
			can2: "All four partisan-fairness measures lean the same way.",
			cant1: "That any commissioner meant to do this. My tests measure what a map does. They can't show motive.",
			cant2: "That the government directed its nominees. I found no evidence of coordination. Appointing someone is not evidence of it.",
			cant3: "That the pattern will happen again. The map that has it was never enacted. November will show whether it comes back.",
			cant4: "How a court would rule, or what the Assembly will enact.",
			p5: "<strong>On the word.</strong> Gerrymandering means drawing lines to give a party an advantage. You recognise it by what a map does, and by what is known about how it was drawn. Canadian law has no offence by that name, so a court won't rule on gerrymandering as such. That doesn't mean it can't happen here. The closest legal test is effective representation under section 3 of the Charter, covered below.",
			p6: "<strong>Reading the cover map.</strong> The cover colours Alberta's 4,765 voting areas by how people in each one voted in 2023: orange where NDP votes are concentrated, blue where UCP votes are. The colour deepens only where lots of people live, so a voting area spread over hundreds of square kilometres of parkland stays pale. West of Ponoka the land is pure white, because it has no polling station and nobody was recorded living or voting there. The lines on top are the minority map's 89 proposed districts. <a href=\"__BASE__/explorer\">Open the map explorer</a> to switch between all three: the minority map, the majority map and the map in force today.",
		},
		does: {
			h: "What the minority map does",
			p1: "The two commission maps agree on most of Alberta. Where they differ, here is what the minority map chose, and what each choice does.",
			h3_1: "One city, four districts",
			p2: "Airdrie has 85,805 people (2024 municipal census), one city council. The law caps each district at one-and-a-quarter times the provincial average, so Airdrie needs at least two districts. The majority map gives it two.",
			p3: "The minority map gives it four: north to Olds-Three Hills-Didsbury, east to Airdrie East, west to Calgary-Foothills-Airdrie West, and centre-south to Calgary-Airdrie. Airdrie East takes more than half the city, and nine in ten of its people are Airdrie residents. Nearly all the rest of the city goes to the two Calgary-edge districts, where Calgary residents outnumber Airdrie's. The north piece holds about 350 people. Splitting a community so thinly that it can't decide any of its seats is called cracking. The split clears the first bar of my cracking test (exploratory: I wrote its rules in the same session that first ran it): more pieces than the city's size requires. It fails the second, that Airdrie's residents be outnumbered in every piece, because of Airdrie East. By the test's own rule, that is no cracking signature. The majority's two-way split fails both bars.",
			p4: "On the minority map, the test doesn't flag the city as a whole. But the part of Airdrie outside Airdrie East, about 45% of the city, is outnumbered in every district it lands in, which is what cracking describes. No registered test scores that part on its own. Airdrie would have four MLAs. Most of the voters who elect three of them live outside Airdrie.",
			h3_2: "Bigger districts in north-east and central Calgary",
			p5: "In Calgary's north-east and central districts, the minority map's seventeen average 11.5% above the provincial average population. The majority's average 2.8%. A bigger district means each vote in it counts for less, so this is a finding about equal population. Putting one party's voters into fewer, larger districts is called packing, but my packing test doesn't detect it here. On 2023's votes the NDP wins eight of the seventeen, and their average winning margin is 15.0 points, 12.6 below the provincial average; the test needs margins 15 points above it. The test is exploratory: I wrote its rules in the same session that first ran it.",
			h3_3: "Districts further from equal size",
			p6: "Equal district populations are the one value Alberta's law puts a number on. By the commission's own population tables, the minority map's districts across the province miss the ideal size by 4,707 people on average. On the majority map, 3,180. The minority's spread is 48% wider. On 2021 census numbers the gap narrows: the two maps' average deviations are almost the same, though the minority's typical district is still further from equal (3,938 against 2,827). The usual defence of odd lines is that they were needed to balance populations. On the numbers the commission itself used, that defence doesn't work here.",
			h3_4: "Rural tails on urban districts",
			p7: "Still, I'm not saying rural Alberta has too many seats. The Act lets district populations vary by up to 25%, so one rural MLA doesn't have to cover an area the size of southern France. Both maps use that room.",
			p8: "But in several places the minority map ties rural communities to a district whose population centre is in a city.",
			h3_5: "Three boundaries the majority called out",
			p9: "The commission's majority, the chair among them, flagged four of the minority's boundaries as geographically anomalous, among them these three:",
			li1: "the Rocky Mountain House–Banff Park extension into uninhabited national-park land;",
			li2: "the lasso-shaped corridor of Calgary-Nolan Hill–Cochrane;",
			li3: "the reach of Olds–Three Hills–Didsbury into north Airdrie.",
			p10: "The flags come from the majority's reply to the minority, so you would expect them to criticise only the minority. So I checked all four against the published maps myself, and three of them hold up.",
			p11: "The majority called the park extension \"a bad faith effort\" to claim a population protection, section 15(2), that is written for remote communities where people actually live. My check undercuts that charge: the division qualifies under s.15(2) even without the extension. The Banff townsite is a separate question: putting it with Canmore makes sense as a community of interest, because the town sits inside a national park it can't grow into. Its objection to the empty-park extension still stands. The townsite's placement doesn't affect it.",
			h3_6: "The seat advantage",
			p12: "Split the province-wide vote dead even, and this is the UCP's share of seats on each map:",
			li4: "the median neutral map gives 44.8%, less than an even share, for a reason covered below;",
			li5: "the majority map gives 46.1%, the 78th percentile;",
			li6: "the minority map gives 51.7% (46 of 89), the 99.99th percentile. Only 69 of 1,010,000 neutral maps exceed it, all with 45 of 87 seats (51.72%), a hair above.",
			p13: "On the minority map the UCP keeps the 45 seats it needs for a majority even if its vote share falls to about 49.2%. On the majority map it would need to win the popular vote by about 9 points. Replay the 2023 election-day vote and the minority map gives it 60 of 89 seats. On the majority map, 55.",
			p14: "Sixty seats is a two-thirds majority. In Alberta, that unlocks no special power. The Assembly decides every question by a simple majority of the votes cast. A simple majority can already pass laws and budgets, cut debate short with a programming motion, change the rules of the House and set every committee's membership, which the rules keep in proportion to seats. Conventions don't need a supermajority either: a simple majority set this one aside. Sixty seats would give the government a cushion. A few floor-crossings couldn't threaten it, and a smaller opposition would have fewer members to keep up committee scrutiny.",
			p15: "None of the minority map's choices breaks the Act's numeric rules. The majority argued the map would likely fail the Charter's test of effective representation; no court has ruled. The Act allows splitting cities, and every district on both maps sits inside the ±25% band, apart from three on each that use the s.15(2) exception for remote divisions. Canadian law has no rule against partisan advantage as such. Its test is whether voters get effective representation.",
		},
		law: {
			h: "What the law requires, and what it doesn't",
			h3_1: "The Constitution",
			p1: "Section 3 of the Charter gives every citizen the right to vote. The Supreme Court of Canada reads it as a right to effective representation. Roughly equal voting power is the starting point, a \"prime condition\", but strict equality isn't required. A district can be bigger or smaller for a real reason, such as geography, community history, shared local interests or a minority community's voice. The difference has to be justified.",
			p2: "Courts give legislatures a lot of room here. They ask whether reasonable people, applying those principles, could have drawn the lines this way. And no government can switch the right off: the notwithstanding clause doesn't apply to section 3.",
			p3: "Courts have also looked at how a map gets made. In 2017 Nova Scotia's Court of Appeal found the province's map violated section 3, because the government had directed its independent commission to change course and the final map didn't reflect the commission's own view. The court added that a legislature may still draw a map itself.",
			p4: "In 2026 the Supreme Court of Canada struck down a Quebec law that paused Quebec's commission to protect ridings in the Gaspésie (<em>Quebec (AG) v. Lalande</em>, 2026 SCC 13, 7–2, reasons May 1). Quebec could have protected them more narrowly. The law had passed unanimously. That didn't save it. On June 12, 2026 Quebec's National Assembly passed its own 127-seat map.",
			h3_2: "Alberta's statute",
			p5: "The <em>Electoral Boundaries Commission Act</em> sets the commission's rules:",
			li1: "<strong>Who sits.</strong> A chair appointed by cabinet from eligible roles that include judges. Four non-MLA members, two nominated by the Premier and two by the Opposition, appointed by the Speaker.",
			li2: "<strong>Hearings.</strong> Public hearings before and after its draft map.",
			li3: "<strong>Deadlines.</strong> A draft within seven months, and a final report within five months after that.",
			li4: "<strong>Seats.</strong> 91. The Act said 89 when the commission drew its maps. Bill 32, introduced April 23, 2026, raised it to 91.",
			li5: "<strong>Population.</strong> Every division within 25% of the average. Up to four remote divisions may go as low as 50% below, if the commission finds at least three of five criteria met.",
			li6: "<strong>Factors.</strong> The commission must consider effective representation, and may weigh growth, communities of interest, geography and other factors.",
			p6: "Both commission maps fit inside these rules.",
			h3_3: "What the law doesn't require",
			p7: "Most of that rulebook is addressed to \"the Commission\". Read plainly, it doesn't bind the Legislature or a committee of MLAs unless the committee's motion adopts it. Government Motion 37 is public, but I've read only the clauses quoted on the committee's page and in its October 28 transcript. None of those adopts the rulebook, and I haven't checked the rest.",
			li7: "The Legislature doesn't have to adopt a commission's map. A report becomes law only if MLAs pass a bill.",
			li8: "I found no provision that requires a committee of MLAs to hold hearings, be independent, publish a draft or explain its choices. Government Motion 37 reportedly says the review is expedited and does not require public hearings.",
			li9: "Recommendation 5, which the government cited, binds no one.",
			li10: "Elections Alberta says it needs at least a year and a half to prepare new ridings. That's a planning need. No law makes it a deadline.",
			li11: "Courts don't review a law while it's being made. A challenge can only come after a boundaries law passes.",
			h3_4: "What happened in 1992",
			p8: "In 1992 Alberta's commission could not agree. Its final report was five separate reports, one from each commissioner. In July 1992 the Assembly passed Motion 24 and handed the work to a Select Special Committee of MLAs chaired by Bob Bogle. The Opposition refused to appoint members, so four Progressive Conservative MLAs drew the map. Alberta voted on it in the 1993 election.",
			p9: "In 1994 the Court of Appeal let that map stand. The 2026 commission's account says the court found it did not rise to the level of Charter condemnation, but called for “a gradual and steady” change (final report, Appendix D, p. 281). Secondary accounts add that the court criticised how the map was made: the committee's members couldn't explain several of its boundaries, one of the smallest districts was Bogle's own, and a proper review was needed before the Legislature's term ran out. I haven't read the judgment itself. In 1995 the Legislature amended the Act and changed how commissions are appointed. Alberta used that process from then until 2026.",
			h3_5: "What this means in November",
			p10: "The new map, once enacted, can still be challenged in court. It faces the same test as any map: effective representation, with every population gap justified. Reasons matter. Secondary accounts say Alberta's Court of Appeal criticised the last committee-drawn map for not giving them. I'm scoring the map and the process. Whether it's constitutional is for a court to say.",
		},
		system: {
			h: "How the committee got the job",
			p1: "Before the committee took over, the commission did its work in public. It held hearings in sixteen communities. It received 1,345 written submissions. And after more than 80 of them, it reversed its plan to remove Lesser Slave Lake.",
			p2: "Four weeks after the split, Government Motion 37 (introduced April 16) created the Select Special Committee on Electoral Boundaries, with six MLAs:",
			li1: "four UCP: Brandon Lunty (chair), de Jonge, Sawyer and Wiebe;",
			li2: "two NDP: Ganley and Gray.",
			p3: "The committee oversees an Independent Advisory Panel, which drafts the 91-seat proposal. In June the committee appointed four panel members: the Hon. Monte Solberg and Darwin Durnie, nominated by the Premier, and Dr. Gerard Kennedy and Brent Robinson, nominated by the Opposition.",
			p4: "Alberta's acting chief justice declined the committee's request to help find a judge to chair the panel, citing \"the irregularity of this process\". The Alberta branch of the Canadian Bar Association declined to take part, and so did the Law Society of Alberta. Retired Court of Appeal justice Brian O'Ferrall was later named chair. The panel advises. The committee's MLAs review its report and send it to the Assembly, where MLAs decide. The panel reported to the committee on October 22. At the committee's October 28 meeting, its UCP members voted 3–2 to end the review of the panel's report before NDP motions on it were considered, and voted down 3–2 an NDP motion to disclose what the panel and its consultants were paid (<a href=\"https://docs.assembly.ab.ca/LADDAR_files/docs/committees/ceb/legislature_31/session_2/20261028_1030_01_ceb.pdf\" target=\"_blank\" rel=\"noopener noreferrer\">committee transcript</a>, pp. CEB-72 and CEB-74). The committee also defeated an NDP motion to publish whom the panel consulted; a UCP member cited privileged legal advice and the panel's independence (p. CEB-75). NDP members said the panel took no public submissions. The committee held no further meetings, and had to send the panel's report to the Assembly by November 2.",
			p5: "In May, Duane Bratt, Professor of Political Science at Mount Royal University, described the process to me as without precedent in Canada. He's right. 1992 isn't the same thing.",
			p6: "In 1992 the commission couldn't agree. Five commissioners filed five reports, and none had a majority behind it. In 2026 a majority signed one, and under the Act a majority report is the commission's report. Government Motion 37 set it aside anyway. That is the part with no precedent.",
			p7: "On the floor, the government presented its route as following the commission: \"We are adopting the recommendations from the report\" (Government House Leader, Hansard, April 16, 2026). The opposition called it \"retaliation against the independent Electoral [Boundaries Commission].\" The report itself doesn't fully support the government's claim. The majority did say two more seats would have given more effective representation (final report, p. 58), and Recommendation 5 itself says its change “would need to be studied by an all-party Select Special Committee or other equivalent Legislative Committee” (p. 66). But the majority asked the Legislature to adopt its 89-seat map. The one recommendation that proposed 91 seats now came from the chair alone.",
			p8: "Every step was lawful. But this time the MLAs who oversee the map will also run in it. And nothing stops a future government, of any party, from citing this cycle as precedent.",
			h3_1: "Recommendation 5: what the government cited",
			p9: "To justify handing the job to a committee, the government cited one recommendation in the commission's report. So that recommendation is the first thing to check when the panel's map comes out. The chair, Justice Dallas Miller, wrote Recommendation 5 alone, in an addendum to the majority report. He was \"reasonably certain\" that with 91 seats no division outside Edmonton and Calgary would be lost, and added: \"My majority colleagues do not agree with me on this point. That is why I am alone in making this recommendation\" (final report, p. 66). He also stated its purpose: it \"is formulated for the express purpose of dissuading the Legislature from accepting the minority report.\"",
			p10: "It's a fallback, and a specific one. If the Legislature wouldn't accept the majority's choice to remove two divisions outside Edmonton and Calgary, the chair asked it to amend the <em>Electoral Divisions Act</em> from 89 seats to 91, restore those two divisions, and keep \"the rest of the province as we propose\" (the majority map) \"to the extent possible.\" Restoring the two divisions should:",
			li3: "<strong>(a) Leave Airdrie and the south alone.</strong> No change to any division in Airdrie, or with any land south of Airdrie's southern city limit, except Drumheller-Stettler. On the majority map that is 41 divisions: both Airdrie seats, all 28 Calgary seats, and the 11 divisions around and south of Calgary.",
			li4: "<strong>(b) Leave north Edmonton alone.</strong> No change to any Edmonton division north of the North Saskatchewan River: 11 divisions on the majority map.",
			li5: "<strong>(c) Put south Edmonton back.</strong> Every Edmonton division south of the river returns to the commission's October 2025 interim map, the draft it published for comment before the final split. The committee may add Nisku to Edmonton-South East if it wants Leduc and Beaumont back in one division. That is 10 divisions.",
			li6: "<strong>(d) Consider a Clearwater seat.</strong> Consider restoring a division made mostly of Clearwater County and western Mountain View County, with s.15(2) status. This is the only restored seat the recommendation places. It names no place for the second.",
			p11: "Together, the conditions rule out most of the ground the commission split over. Airdrie, Calgary, Cochrane and Chestermere, home to the four-way Airdrie split and the Calgary-edge hybrids, all fall under condition (a). Red Deer and St. Albert are covered only by the softer clause, \"to the extent possible.\" A map that reopens Airdrie or Calgary may still be lawful. But it isn't the map Recommendation 5 describes. Government Motion 37 itself reportedly lets the panel apply the recommendation \"subject to any modifications the independent advisory panel considers necessary.\" The <a href=\"__BASE__/explorer\">map explorer</a> outlines the area under each of the four conditions, and each one's pin says whether Recommendation 5 changes it or leaves it alone.",
		},
		know: {
			h: "How we know",
			h3_1: "How the neutral maps were drawn",
			p1: "A computer drew 1,010,000 Alberta maps from the official Elections Alberta files, each with 87 districts, the 2019 map's count, all inside the population band and in one piece. The method, ReCom, is the standard one in this field. It merges two neighbouring districts, splits the result at random into two new legal ones, and repeats. The computer never sees a vote. That is what makes these maps neutral. Where a real map's numbers fall among the million shows how unusual it is. Neutral maps drawn at 89 districts, the commission maps' size, show the same lean (those results are still preliminary).",
			p2: "Some of my commitments are filed on the Open Science Framework, the first on May 6, 2026. The random seeds come from a public randomness beacon. I fixed them in the code on April 27, before the official map files arrived; the record of that is a commit in my own repository, not an OSF registration. <a href=\"__BASE__/methods\">The Methods page</a> labels each finding pre-registered or exploratory.",
			h3_2: "In Alberta, neutral is not 50/50",
			p3: "Rural UCP voters win their ridings by wide margins, like 60-40, and those margins waste a lot of extra votes. Urban NDP voters win theirs by closer margins, like 51-49. So when the vote splits dead even, the median neutral map gives the UCP only 44.8% of seats. That is the baseline both maps are measured against.",
			h3_3: "The results, side by side",
			table1_h1: "Test",
			table1_h2: "Majority map",
			table1_h3: "Minority map",
			table1_r1c1: "Follows municipal lines (2019 map: 75%)",
			table1_r1c2: "80%",
			table1_r1c3: "72%",
			table1_r2c1: "Population spread from ideal size (commission tables)",
			table1_r2c2: "3,180",
			table1_r2c3: "4,707: 48% wider",
			table1_r3c1: "NE/central Calgary districts above provincial average",
			table1_r3c2: "2.8%",
			table1_r3c3: "11.5%",
			table1_r4c1: "Boundaries flagged in the commission's majority report",
			table1_r4c2: "0",
			table1_r4c3: "4 (3 confirmed)",
			table1_r5c1: "Airdrie split (legal minimum: 2)",
			table1_r5c2: "2 pieces",
			table1_r5c3: "4 by territory; 3 by people (≥2%)",
			table1_r6c1: "<strong>Structural summary</strong> (tests failed, of 5; each test compares the two commission maps)",
			table1_r6c2: "<strong>0 of 5</strong>",
			table1_r6c3: "<strong>4 of 5</strong> (the fifth, anchoring, is neutral for both maps)",
			table1_r7c1: "UCP seat share at a tied vote (neutral median 44.8%)",
			table1_r7c2: "46.1% (78th percentile)",
			table1_r7c3: "51.7% (99.99th percentile; 69 of 1,010,000 exceed it)",
			table1_r8c1: "Mean-median gap",
			table1_r8c2: "1st percentile: an outlier, but leaning the NDP's way, the wrong direction to help the UCP",
			table1_r8c3: "deeper in the tail than 99.97% of neutral maps, leaning the UCP's way",
			table1_r9c1: "Declination (a second lopsidedness measure)",
			table1_r9c2: "22nd percentile: inside the normal range",
			table1_r9c3: "deeper in the tail than 98.8%, leaning the UCP's way",
			table1_r10c1: "Efficiency gap (pre-set line about +4.1%)",
			table1_r10c2: "+0.1% (16.5th percentile)",
			table1_r10c3: "+4.0% (94.5th percentile): a miss",
			table1_r11c1: "UCP seats on 2023 votes",
			table1_r11c2: "55 of 89",
			table1_r11c3: "60 of 89",
			table1_r12c1: "Odds of this profile under neutral drawing",
			table1_r12c2: "n/a",
			table1_r12c3: "about 1 in 568,000 (a model estimate; no neutral map matched)",
			p4: "The structural tests behind the summary row need no election results. I wrote all five down on April 24, 2026, after both maps were public. The record is a dated commit in the project's repository; nothing was registered publicly on the OSF until May 6. Three can be read straight off the commission's report, so treat them as checks of the report, not predictions. The 2019 enacted map, still in force today, sits beside the majority, at a 46.0% tied-vote seat share (78th percentile as registered; 65th once neutral maps that tie it are counted).",
			fig_caption: "Partisan skew runs left to right; failed structural tests run bottom to top. The 2019 map and the 2026 majority map sit in the safe corner (the 2019 map fails none of the four tests run on it; the Calgary zone test was never run on it). The minority map sits alone, on the structural line and just short of the partisan one.",
			h3_4: "What \"1 in 568,000\" means",
			p5: "The chance that a neutral process produces the minority map's combined profile across the four fairness measures is about 1 in 568,000 (p ≤ 1.76×10⁻⁶, a Bonferroni-corrected, dependence-robust upper bound). I looked in two places, so I doubled the raw figure. No neutral map matched the profile, so the figure comes from a statistical model, not a count. A more cautious version of the model gives about 1 in 450,000.",
			p6: "That figure isn't the probability that the map is innocent. Treating it that way is the prosecutor's fallacy. A map this rare can still come from unusual but honest judgment. My claim is only that ordinary drafting variation isn't a plausible explanation.",
			h3_5: "Checking with a second method",
			p7: "I swapped the simulation's engine for a structurally different one, a spanning-forest sampler registered in advance at OSF (he53s) and run on 2026-07-10. The minority's percentile on every metric stayed within a point of the main run. That smaller run can't measure a shift that fine (its margin is about two points), so the honest reading is no change it could detect. A separate implementation, the R redist package, also found zero plans reaching the minority's value.",
			h3_6: "Limits of the simulation",
			p8: "The simulation enforces population and contiguity, keeping each district in a single piece, but not every rule the commission weighed (s.15(2), community of interest, municipal anchoring). It's a strong outside check, not a list of every map a lawful commission might draw. The structural tests describe how the two commission maps differ; the simulation is what says how unusual the minority map is. The tied-vote test has a limit too: it isolates what a map contributes on its own. A big enough swing in a real election can still outweigh any map's lean.",
			h3_7: "What didn't hold up",
			p9: "Some tests came back against my findings. They stay on the page.",
			li1: "<strong>The anchoring test came back neutral.</strong> The minority map follows municipal lines 72% of the time and the majority 80%. The 2019 map, drawn by the last commission, scores 75% on the same measure.",
			li2: "<strong>The efficiency gap missed.</strong> The minority came in at +4.0%, the 94.5th percentile. The pre-registered line was the 95th (about +4.1%), so I report it as a miss.",
			li3: "<strong>The mechanism test failed.</strong> I tested whether the flagged shapes produce the seat advantage. On my test, they don't. The shapes and the seat numbers point at the same map, but the link between them didn't hold up.",
			li4: "<strong>The minority passed one test outright.</strong> On neighbour-drain, which looks for packed districts next to thin-margin ones, it shows 1 coupled signal, against the majority's 2 and the 2019 map's 5.",
			li5: "<strong>Two statistics don't hold up.</strong> The Swing-Zone Allocation Test falls from p = 0.0024 to p ≈ 0.19 once corrected for neighbouring areas voting alike, so it is exploratory only. Combining it with the ensemble test, as Fisher's method does, assumes the two are independent. They aren't, so I don't use that combined figure.",
			h3_8: "Both sides tested",
			p10: "I ran the main measurable accusations from each side, plus one hypothesis of my own, through the same tests. None of these checks was set up in advance, so they are exploratory. Every number behind them is public.",
			table2_h1: "The accusation",
			table2_h2: "Who made it",
			table2_h3: "What I found",
			table2_r1c1: "Four of the minority's boundaries are geometrically anomalous",
			table2_r1c2: "The majority (final report, pp. 62–63)",
			table2_r1c3: "Largely confirmed: three of the four geometric flags hold up on the published maps; the fourth's highway-corridor link is defensible",
			table2_r2c1: "The minority's changes in five places had \"no public support\"",
			table2_r2c2: "The majority (final report, pp. 59, 62)",
			table2_r2c3: "Overbroad: right on three of five, partly wrong on two",
			table2_r3c1: "The park extension was \"a bad faith effort\" to claim s.15(2) protection",
			table2_r3c2: "The majority (final report, p. 10)",
			table2_r3c3: "Undercut: the division qualifies under s.15(2) even without the flagged extension",
			table2_r4c1: "The majority \"delete[s] or mangle[s] rural electoral divisions\"",
			table2_r4c2: "The minority (p. 356)",
			table2_r4c3: "Reversed: the minority keeps fewer rural-anchored divisions (23 vs 28, against 2019's 31) and absorbs more into city-named districts (7 vs 3)",
			table2_r5c1: "The majority \"decline[d] to use\" the ±25% flexibility in rural Alberta",
			table2_r5c2: "The minority (p. 356)",
			table2_r5c3: "Supported: majority rural divisions average −6.0% deviation (4 below −10%); the minority's average −12.2% (11 below −10%)",
			table2_r6c1: "\"Substantial and consistent testimony\" for hybrids was ignored",
			table2_r6c2: "The minority (p. 356)",
			table2_r6c3: "Overbroad: support was configuration-specific, documented for three of seven hybrid configurations and absent for three",
			table2_r7c1: "The majority's rural districts are engineered corridors of isolation",
			table2_r7c2: "My own counter-hypothesis (T3.2)",
			table2_r7c3: "Not supported: the geographic explanation held, and the majority cleared",
			p11: "The minority's published reasons for its contested lines mostly fail on public data: four of six don't survive an independent check, and a fifth holds only in part. Usually the general claim is true and the specific line isn't. About 71% of Cochrane's out-commuters work somewhere in Calgary (a third of all its workers). That says nothing about the Nolan Hill neighbourhood the corridor reaches. The majority published no such list, so this check only runs one way. Taken together, the minority's two rural charges against the majority describe two different approaches. More but fuller rural divisions on the majority map. Fewer but lighter ones on the minority map.",
			h3_9: "Who did this",
			p12: "I'm the only author, a self-funded student at Mount Royal University, and I've voted for and donated to both conservative and progressive provincial parties (more under About me). Findings that went against what I expected stay on the record, and every number can be reproduced from public code, public data and random seeds fixed in the code before the analysis ran.",
			h3_10: "The full record",
			p13: "All fourteen findings are on <a href=\"__BASE__/evidence\">the full record</a>, each with its numbers, what it could show, what Canadian practice expects and what the law does with it. Each one links to a short explainer on <a href=\"__BASE__/explainers\">the explainers page</a>.",
		},
		test: {
			h: "The November test",
			p1: "The committee had to send the panel's 91-seat map to the Assembly by November 2, 2026. The rules that decide the verdict were fixed in June 2026, before the panel's map was made public; the <a href=\"https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/preregistration/november_2026_scoring_spec.md\" rel=\"noopener\">scoring rules</a> are dated in the project's repository. Three extra tests reported beside them, and the choice of comparison set, were added October 29–31, after opposition MLAs had described parts of the panel's map at the committee's October 28 meeting. I'll publish the scores within 72 hours of the map's release, whichever way they point.",
			p2: "<strong>The process.</strong> Were public hearings held? Was a draft released? Are the advisory panel's members and terms of reference published? Is the record behind the map public? NDP members said the panel took no public submissions, and the committee defeated a motion to publish whom the panel consulted, so I can only score the reasons for the map's lines from what the panel's report publishes. The process also gets its own nine-feature scorecard, registered on the OSF (u47bq) and shown on <a href=\"__BASE__/norms#measurable\">the norms page</a>.",
			p3: "<strong>Recommendation 5.</strong> Test X1 scores the panel's map against the commission chair's four conditions, one at a time:",
			li1: "(a), (b) and (c) pass if the map leaves those divisions as described.",
			li2: "(d) asks only that a Clearwater seat be considered, so it's scored on evidenced consideration. It passes if the map contains the division, or if the committee's or the panel's published report names the option and gives a reason, tied to the Act's factors, for adopting or declining it. With no other public record of how the map was made, those reports are the only record that counts. Silence or boilerplate fails.",
			p4: "X1 passes only if all four do. Condition (c) needs the commission's interim map, which isn't in the project's files; if I can't get it when scoring begins, I'll report (c) as not scored. I'll also report a strict reading, which fails (d) unless the seat exists. Recommendation 5 binds no one in law. What X1 tests is whether the map delivers what the government cited.",
			p5: "<strong>The map.</strong> Where does it land on every measure on this page, against the same million-map distribution and under the same pre-registered thresholds?",
			p6: "<strong>What each outcome means.</strong> If the panel's map repeats the minority map's pattern on the partisan measures, drawn by different people, under different constraints, on a different timeline, the partisan finding is replicated. The structural tests add little, because they match the minority's pattern on 93.5% of neutral 91-seat maps. If it lands inside the neutral bands, the finding stays an isolated observation about one map that was never enacted, and I'll say so here. Either way, the arithmetic is public. You can check it yourself.",
		},
		mind: {
			h: "What would change my mind",
			p1: "Each load-bearing finding has a written condition that would retract it. Most were set on April 24, 2026; later findings got theirs when they were added. If one is met, I'll publish the retraction. The project's written rule is within 48 hours of the condition becoming known.",
			li1: "<strong>Someone shows the trade-off was forced.</strong> If anyone shows that no legal Alberta map can satisfy the minority's own stated reasons for Airdrie, Cochrane, Nolan Hill and Rocky Mountain House–Banff Park while following municipal lines about as often as the majority's, I'll retract the finding that those boundaries can't be explained by their stated reasons. A map that does both would strengthen the finding instead. The challenge is open at <a href=\"https://github.com/Ixby/alberta-electoral-boundaries-audit/issues/14\" rel=\"noopener\">Issue #14</a>.",
			li2: "<strong>A document shows the reasons came first.</strong> If an internal commission document, dated before the minority's final choices, shows those choices were driven by community submissions I haven't seen, I'll retract the inference that they were drafting decisions.",
			li3: "<strong>The neighbour-drain pass turns out to be an artefact.</strong> If the continuous version of that score falls in the extreme upper tail (p < 0.05) of random permutations, I'll withdraw the minority's pass.",
			li4: "<strong>An election contradicts the simulation.</strong> Neither commission map will be used in 2027, so this can't be tested on them. If the 2027 election, on whatever map is enacted, gives a seat split that contradicts the projection from 2023 votes on that map, I'll revisit the simulation's percentile findings against the actual results.",
			li5: "<strong>A court distinguishes <em>Lalande</em>.</strong> In <em>Quebec (AG) v. Lalande</em>, 2026 SCC 13, the Supreme Court struck down Quebec's law pausing its commission, and Quebec then legislated its own map. If a court reviewing Alberta's route finds it constitutionally different, for example because handing a finished commission's work to an MLA committee isn't the same as freezing a commission mid-process, I'll retract the argument on <a href=\"__BASE__/norms\">the norms page</a> that the two belong in the same class.",
			p2: "The November map can also weaken the overall conclusion, as described above. I correct mistakes in public. I don't delete them. Every correction is listed in the <a href=\"https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md\" rel=\"noopener\">academic report's Documented Corrections section</a>.",
		},
		authors: {
			h: "The author's view",
			p1: "Everything above is the audit. This section is my opinion. Delete it and no number on this page changes.",
			p2: "Two facts are hard to explain innocently. The commissioners the government nominated drew a map that neutral map-drawing almost never produces: fewer than a hundred in a million draws lean that far. And when the commission split instead of endorsing that map, the government moved the job to a committee its own MLAs control.",
			p3: "Each fact, on its own, has an innocent explanation. A commissioner can be eccentric in good faith, and a legislature can lose patience with a split commission. Put the two facts in order, though, and the innocent explanations get harder to hold.",
			p4: "What worries me is that no law was broken. I checked, and that checking is most of what this audit is. The Act makes the commission's report advisory. It sets no notice period, and requires no draft, hearings or consultation before the Legislature acts. The protection was a convention, not a law, and a convention binds only a government that chooses to follow it. In 1995, after its 1992 committee, Alberta changed how commissions are appointed.",
			p5: "The committee that replaced the commission has a government majority and a government chair. It has an advisory panel, chaired by a retired judge who was appointed after the province's acting chief justice declined to help find one. The panel only advises. The MLAs vote, and they will run in the districts they approve. The map won't have a public hearing before it's final.",
			p6: "This government has set a convention aside before. Its first bill, as written, would have let cabinet rewrite laws without the Legislature, and that power was removed only after public outcry. Its own ethics commissioner found the Premier breached the conflicts law by pressing her attorney general about a criminal case. It passed a law letting cabinet repeal local bylaws and trigger the removal of elected councillors. When a court paused one of its laws in June 2025, it invoked the notwithstanding clause that December. Apart from the ethics breach, each of those moves was lawful, and each set aside a convention to get past an independent check.",
			p7: "I also worry about what the map buys. Replay the 2023 election-day vote and the minority map gives the UCP sixty seats of eighty-nine. Sixty seats would protect a government from floor-crossings and leave fewer opposition members to keep up scrutiny in committee. I'd worry about that in anyone's hands.",
			p8: "I could be wrong, and I've set out how you'd know. The panel's map had to go to the Assembly by November 2, and the rules that decide its verdict were fixed in June, before it was made public. If it lands inside the neutral range, my suspicion has taken real damage, and this site will say so within 72 hours of its release. I committed to that before I knew the answer.",
			signed: "— Will Conner",
		},
		fixes: {
			h: "Fixes for next time",
			p1: "Two problems make every audit of Alberta's maps harder than it needs to be. First, about half of all votes now come in before election day, and Elections Alberta reports them by division rather than by voting area. So roughly 810,000 NDP and UCP votes cast in 2023 can't be pinned to the voting area where they were cast. Second, commissions draw from census data that's already years old by the time a map takes effect. Both problems can be fixed. <a href=\"__BASE__/fixes\">The proposals page</a> explains how.",
		},
	},

	fixes: {
		page_title: 'Fixes for next time · Alberta Electoral Boundary Audit',
		h1: 'Fixes for next time',
		meta: 'Plain-language companion · what would make the next map easier to check',
		back: '← Back to the audit'
	},
	evidence: {
		page_title: "The full record · Alberta Electoral Boundary Audit",
		h1: "The full record",
		meta: "Plain-language companion · the fourteen findings in full",
		intro: "Every finding behind the main page, in full: what was found, what it could show, what Canadian practice expects, and its limits, including what the law does with it. Most of them weigh the majority’s map against the minority’s: the commission split, and each side filed a map of its own. Read the page as a log: the findings that ran against the audit stay right beside the ones that support it.",
		back: "← Back to the audit",
		group_map: "On the map: what the lines do",
		group_sim: "In the simulation: how rare each map is",
		group_conduct: "In the conduct: what the people in the process did",
		beat_found: "What we found",
		beat_show: "What it could show",
		beat_context: "Context",
		beat_canada: "What Canadian practice expects",
		beat_law: "Limits and the law",
		explainer: "Explainer",
		e1: "Airdrie: one city of 85,805, four districts",
		e2: "The three boundaries the majority called out and our tests confirmed",
		e3: "North-east and central Calgary: larger districts on the minority map",
		e4: "Equal population: the minority map is worse at the one thing the law actually measures",
		e5: "Municipal anchoring: both maps close to the 2019 map",
		e6: "At a tied vote, only 69 of 1,010,000 neutral maps give the UCP more seats than the minority’s, and only by a hair",
		e7: "The test that missed",
		e8: "One in 568,000, and what that number is not",
		e9: "We tried to knock down our own result",
		e10: "The signals that pointed the other way",
		e11: "Four of six reasons don’t survive checking",
		e12: "The commission that couldn’t sign one map, and what each side charged",
		e13: "The process that answered the public, and what replaced it",
		e14: "The independent-commission norm, set aside",
	},
	body: {
		section_link_aria: 'Link to section',
		the_map: {
			heading: '1: The Map',
			heading2: 'The map on the cover',
			p1: 'The cover map is the best single image in this audit. Here is how to read it.',
			p2: "Alberta is divided into 4,765 Voting Areas — small geographic zones Elections Alberta uses to count polling-station ballots. Each one is coloured by how people in it actually voted in 2023: orange where NDP votes are concentrated, blue where UCP votes are concentrated. But the colour only becomes dark and saturated where a lot of people live. A Voting Area that covers hundreds of square kilometres of parkland or farmland stays pale — nearly invisible. The map lights up where people are, and fades where they aren't.",
			p3: 'This is very different from the Alberta you see on election night. Most election maps colour entire ridings solid blue or orange based on who won. Rural ridings are geographically large and the UCP wins most of them, so election-night Alberta looks like a wall of blue with small orange pockets in Edmonton and Calgary. The cover map uses the same votes and the same geography — but shows them weighted by where people actually live. What appears is a province where most of the population is concentrated in a dense arc of cities, and those cities vote very differently from the rural map that normally represents them.',
			p4: "The boundary lines drawn over the colour are the minority commission's 89 proposed electoral districts — the map this audit ends up critiquing. The audit's work is to ask what those lines do to the people underneath them.",
			p5: 'This image is what makes the stakes plain. A province that looks like it votes one way on a standard map is actually a province where most of the people live in areas that vote the other way. Once the population is visible underneath the boundary choices, those choices stop looking random.'
		},
		preliminary: {
			badge: 'PRELIMINARY',
			heading: 'Preliminary findings — pending independent expert review',
			body: 'Independent subject-matter experts are reviewing the statistical tests in this section before final publication. The full results sit below, open to that scrutiny.'
		},
		structural_results: {
			heading: 'Structural audit results — before any statistics:',
			body: 'The majority map crosses <strong>zero of five</strong> pre-registered structural thresholds. The minority map crosses <strong>four of the five</strong>; the fifth (anchoring) is neutral — both maps fall within the 70–85% Canadian norm. These are geometric measurements — population spread, <button class="vocab-term" data-def="how closely a district\'s borders follow pre-existing city and municipal limits, rather than cutting through them" aria-expanded="false">municipal anchoring</button>, Airdrie split count, NE/central Calgary population excess, and the seven boundary configurations Commission Chair Justice Miller himself flagged in writing (majority report, pp. 59 and 62–63) — requiring no election data and no statistical sampler. The next section tests both maps against 1,010,000 computer-drawn neutral maps and reaches the same conclusion through a completely different instrument. Two independent instruments — geometric and statistical — converge, and both land on the regions the commission chair criticized in writing.'
		},
		clean: {
			heading: "6: When a fair-looking map isn't",
			legal_label: 'A NOTE ON LEGAL TERMINOLOGY',
			legal_body: '"Gerrymandering" has no legal definition in Canadian law. The word is used throughout this report in its everyday political sense — manipulating electoral boundaries for partisan advantage. The legal tests actually applying in Canada are different: whether boundaries provide "effective representation" under s.3 of the <em>Charter of Rights and Freedoms</em> (the constitutional standard the Supreme Court of Canada set in the 1991 <em>Saskatchewan Reference</em>), and whether the commission followed the rules of Alberta\'s <em>Electoral Boundaries Commission Act</em>. The audit\'s findings are evidence bearing on those legal questions. They are not proof of a legally-defined wrong, and this report does not describe them in those terms.',
			intro_p1: "The cleanest single question to ask of any electoral map is this: if the province's vote split exactly evenly between the two main parties, what seat count would the map produce? This holds the electorate constant and asks the map alone what it does.",
			intro_p2: "To answer this, the audit generated 1,010,000 computer-drawn, mathematically neutral Alberta maps. The simulation used the official Elections Alberta shapefiles on the commission's geography, holding every plan to the same population-balance (±25%) and contiguity requirements — the two criteria the algorithm enforces, not every statutory factor (it does not, for example, enforce communities of interest), so the comparison set is best read as population-and-contiguity-neutral rather than fully statute-compliant. The commission's two 2026 maps were then placed into that distribution to see how normal they are. The simulation ran four independent chains of 252,500 steps each, with the base seed drawn from the Cloudflare drand beacon and pre-registered at OSF before execution.",
			howmcmc_label: 'HOW THE SIMULATION WORKS',
			howmcmc_mcmc: 'Merge two neighbouring districts, split the blob back into two new legal ones at random, repeat a million times, saving the map each step. That is the whole machine. The step-by-step walkthrough — and every other test on this page, in plain language — is on <a href="__BASE__/methods">the Methods page</a>.',
			howmcmc_recom: 'The algorithm is called ReCom — the standard tool of the field — and it preserves the two hard legal rules (population balance, contiguity) by construction.',
			prereg_label: 'PRE-REGISTRATION',
			prereg_body: "Pre-registration means writing the tests, thresholds, and predicted directions down in a public, time-stamped record before looking at the data — so a threshold cannot be quietly moved after the answer arrives. This audit's commitments are filed on the Open Science Framework, its random seeds were locked to a public beacon before the official map files existed, and each finding is labelled pre-registered or exploratory accordingly. The full accounting of which is which is on <a href='__BASE__/methods'>the Methods page</a>.",
			neutral_p: 'In Alberta, the neutral answer is not 50/50. <em>Across 1,010,000 computer-drawn legal Alberta maps, the median map gives the UCP only 44.8% of the seats at 50/50 votes</em> — a typical Alberta map under neutral votes hands the NDP a small seat majority. This is counterintuitive but mechanical: rural UCP voters win their ridings by 60-40 margins (wasting many "extra" UCP votes), while urban NDP voters win their ridings by tighter 51-49 margins (wasting fewer NDP votes per win). At neutrality, NDP comes out ahead on seat efficiency.',
			full_dist: 'The full distribution from the canonical 1,010,000-map simulation:',
			t1_col_a: 'Where the map sits',
			t1_col_b: 'UCP seats at 50/50 votes',
			t1_r1_a: 'Median Alberta map',
			t1_r1_b: '44.8% — NDP slight seat majority',
			t1_r2_a: '95th-percentile map',
			t1_r2_b: '47.1%',
			t1_r3_a: '99th-percentile map',
			t1_r3_b: '48.4%',
			t1_r4_a: '<strong>Maximum across 1,010,000 maps</strong>',
			t1_r4_b: '<strong>51.72% (69 of 1,010,000 plans exceed the minority\'s 51.69%)</strong>',
			seat_count_note: 'A note on seat counts. The 2026 commission maps each have <strong>89</strong> districts; the audit\'s computer simulation runs on the <strong>87</strong>-district 2019 map (its starting substrate); the November Lunty committee will produce <strong>91</strong>. All percentages are seat <em>shares</em>, comparable across these denominators. The simulation uses the 2019 map as its starting point because the ReCom algorithm needs a legally enacted map to propose swaps from — the 2019 map is the last enacted Alberta electoral map. Using either commission proposal as the substrate would be circular: we would be measuring whether a map is extreme compared to maps derived from itself.',
			pattern_intro: 'The results — placing the three real maps in this distribution — point to a specific, surgical pattern of boundary drawing.',
			sub1_h: 'All four statistical measures fire simultaneously',
			sub1_p: 'When the official Elections Alberta shapefiles are used, the minority map is a statistical outlier on every partisan-fairness metric — not just the tipping-point one.',
			t2_col_a: 'Map',
			t2_col_b: 'Efficiency gap',
			t2_col_c: 'Mean-median',
			t2_col_d: '<a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener" title="Declination measures the angular difference between the seats-votes curve for each party. Negative values favour the NDP; positive favour the UCP.">Declination</a>',
			t2_col_e: 'Seats at 50/50',
			t2_r1_a: 'Majority 2026',
			t2_r1_b: '+0.1% (p16.5)',
			t2_r1_c: '−3.6% (p1)',
			t2_r1_d: '−0.027 (p21.8)',
			t2_r1_e: '46.1% (p78.5)',
			t2_r2_a: 'Minority 2026',
			t2_r2_b: '<strong>+4.0% (p94.5)</strong>',
			t2_r2_c: '<strong>+1.0% (p99.97)</strong>',
			t2_r2_d: '<strong>+0.077 (p98.8)</strong>',
			t2_r2_e: '<strong>51.7% (p99.99)</strong>',
			sub1_close: "The majority map sits comfortably inside the normal range on three of four metrics. Its mean-median sits at p1 (= p0.99) in the NDP-favourable direction — an unusual result but pointing the wrong way to help the UCP. The majority map's close adherence to municipal boundaries places NDP-heavy urban cores into their own compact districts, where NDP votes win by efficient margins while UCP rural wins tend to be by larger margins; this mild structural NDP efficiency advantage is what shows up in the mean-median measure. The minority map is in the tail on all four, each pointing in the same partisan direction.",
			sub2_h: 'The 50/50 tipping point: fewer than 100 of 1,010,000 neutral maps reach it',
			sub2_p: 'The tipping-point metric introduced above — UCP seats at a 50/50 provincial vote — is the most intuitive way to compare the three maps.',
			t3_col_a: 'Map',
			t3_col_b: 'UCP seats at 50/50 votes',
			t3_col_c: 'Where it sits',
			t3_r1_a: '2019 enacted',
			t3_r1_b: '46.0%',
			t3_r1_c: '78th percentile — inside the normal range',
			t3_r2_a: '<strong>Majority 2026</strong>',
			t3_r2_b: '<strong>46.1%</strong>',
			t3_r2_c: '<strong>78th percentile — well within bounds</strong>',
			t3_r3_a: '<strong>Minority 2026</strong>',
			t3_r3_b: '<strong>51.7% (46 seats)</strong>',
			t3_r3_c: '<strong>99.99th percentile — fewer than 100 of 1,010,000 neutral draws reach this</strong>',
			sub2_close: "Fewer than 100 of 1,010,000 computer-drawn neutral Alberta maps produced a <code>seats@50/50</code> value as high as the minority proposal's. Based on actual recent voting patterns, it would award the UCP 60 seats (compared to 55 in the majority proposal). The majority proposal is the kind of map a neutral procedure routinely generates. The minority proposal is the kind of map you have to specifically aim to draw.",
			sub3_h: 'What this means in plain language',
			sub3_p: 'The minority proposal sits in the extreme tail of the 1,010,000-plan ensemble on three of four partisan-fairness metrics, with the fourth (efficiency gap, +4.0%) at the 94.5th percentile — <em>near, but below</em>, the audit\'s pre-registered Alberta-calibrated threshold of the 95th. The two joint-test channels share underlying efficiency-gap data and are not statistically independent, so combining their p-values under Fisher\'s method overstates significance. The defensible upper bound from a dependence-robust combination is roughly <strong>one in 568,000</strong> (Bonferroni; p&nbsp;≤&nbsp;1.76×10<sup>−6</sup>). That remains an extreme result, well beyond conventional significance thresholds — but it is reported as a bound, not as four independent instruments reading in agreement.',
			details_summary: "What this p-value means — and what it doesn't",
			details_p1: 'A p-value answers one question: if the map were drawn by a neutral process, how often would we see a result this extreme or more extreme? At the dependence-robust bound p&nbsp;≤&nbsp;1.76×10<sup>−6</sup>, the answer is at most about once in 568,000 trials.',
			details_p2: 'This is a frequentist hypothesis test, not a measurement of intent. It does not say the commission intended to gerrymander, and it does not quantify how unfair the map is in practical terms. It says the boundary pattern is statistically inconsistent with the ReCom neutral-drawing reference distribution — a strong external check, but not a perfect one (it does not enforce every statutory criterion the commission worked under, e.g., s.15(2) tiers and community-of-interest constraints).',
			details_p3: 'The structural test battery (population, splits, anchoring, compactness, signatures) was registered with timestamps before canonical recomputation (<a href="https://osf.io/w2s8k" rel="noopener">OSF registration w2s8k</a>). The partisan-bias channels (joint Mahalanobis, SZAT, Fisher/Bonferroni combination) are labelled "exploratory" in the audit\'s own §4.3.1 sense: documented in the repository, but not pre-data. The audit reports each channel separately and combines them under the dependence-robust bound rather than presenting them as fully independent confirmatory tests.',
			szat_label: 'SWING-ZONE ALLOCATION TEST (SZAT)',
			szat_body: 'SZAT was designed as a second analytical channel: instead of asking "is this map extreme overall?" it asks "are the specific line choices partisan-neutral?" It works by isolating only the Voting Areas where the minority\'s map differs from the majority\'s — the contested re-draws — and testing whether those particular choices, taken together, shift vote efficiency in one party\'s direction. Because it compares only the points of departure, it automatically controls for everything the two maps share: the same geography, population targets, and statutory rules. Under a standard permutation test SZAT returned p=0.0024; under a block-permutation null that corrects for spatial autocorrelation across adjacent Voting Areas, it returned p≈0.19 — not significant. SZAT is retained as exploratory context but does not survive as a confirmatory channel. The headline rests on the simulation alone. <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/szat_summary.json" rel="noopener">Technical details →</a>',
			two_q: '<strong>The SZAT result.</strong> The 1,010,000-map simulation asks: <em>is this map extreme compared to neutral maps drawn on the same Alberta geography?</em> A second test — the <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/szat_summary.json" rel="noopener">Swing-Zone Allocation Test</a> — asked a different question: <em>are the specific lines on the map partisan-neutral?</em> It works by looking only at the Voting Areas where the minority drew differently from the majority and asking whether those particular choices, taken together, shifted vote efficiency in one party\'s direction. Under standard permutation it returned p=0.0024. Under a block-permutation null — which corrects for spatial autocorrelation among adjacent Voting Areas — it returned p≈0.19. The block-permutation result does not reach significance. The audit therefore reports the simulation result alone as the headline: a dependence-robust upper bound of <strong>1 in 568,000</strong> (p&nbsp;≤&nbsp;1.76×10<sup>−6</sup>), not a Fisher combination of two independent channels.',
			super_lead: 'In an 89-seat legislature, a two-thirds supermajority requires exactly 60 seats. The minority proposal’s tied-vote seat share of 51.7% — a level only 69 of the 1,010,000 neutral maps reach — sits in the regime where a UCP supermajority becomes statistically reachable on Alberta’s 2023 geography. But the simulation does not enforce every statutory criterion the commission worked under, so this is a strong external check, not proof that no legally compliant Alberta map could reach this seat count. Act I’s structural evidence, which does not depend on the simulation at all, carries most of the weight; the tied-vote tail position is the supporting context.',
			super_label: 'WHY A LARGE MAJORITY MATTERS',
			super_body: 'Under Canada\'s Westminster system, Alberta\'s Assembly has no two-thirds threshold that unlocks special powers: a governing majority — even a bare one — can already pass laws and budgets, invoke "closure" to end debate, change the rules of the House, and set the membership of every committee. What a very large majority changes is margin and durability, not the menu of powers. A government holding 60 of 89 seats is effectively immune to internal dissent — a handful of floor-crossings cannot threaten it — and faces an opposition too small to force recorded divisions or sustain committee scrutiny. The concern here is the concentration of seats and the thinning of effective opposition, not a procedural threshold being crossed.',
			super_close: 'The urban-hybridization pattern identified in Act I — urban voters distributed into surrounding rural-edge districts — is consistent with the 60-seat outcome, though the audit’s direct test of whether that geometry is the specific mechanism came back negative and is reported as a failure (Casing 9). The structural and statistical findings converge on the same proposal and the same communities — and they agree on who benefits.',
			sub4_h: 'Confirmation from the targeted-procedure test',
			sub4_p: 'To be sure this isn\'t a quirk of the neutral simulation\'s known compactness preference, the audit ran a targeted hill-climbing procedure (<a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">Cannon et al. 2022 — cited and described in the technical report</a>) in both directions: maximising UCP seats and maximising NDP seats. Same number of steps (40,000) in each direction, same statutory constraints, same provincial geometry.',
			t4_col_a: 'Procedure',
			t4_col_b: 'Most-extreme value reached',
			t4_col_c: 'What it tells us',
			t4_r1_a: 'Neutral MCMC, max produced',
			t4_r1_b: '51.72% UCP seats @ 50/50 (69 of 1,010,000 plans exceed the minority\'s 51.69%)',
			t4_r1_c: 'The natural ceiling under neutral drawing',
			t4_r2_a: 'Neutral MCMC, min produced',
			t4_r2_b: '~39% UCP seats @ 50/50',
			t4_r2_c: 'The natural floor under neutral drawing',
			t4_r3_a: 'Targeted hill-climb, UCP-maximizing',
			t4_r3_b: '<strong>52.9%</strong>',
			t4_r3_c: 'What a procedure deliberately aiming for UCP advantage can reach',
			t4_r4_a: 'Targeted hill-climb, NDP-maximizing',
			t4_r4_b: '<strong>37.9%</strong>',
			t4_r4_c: 'What a procedure deliberately aiming for NDP advantage can reach (below the neutral floor)',
			sub4_close: "The minority map's 51.7% sits closer to the targeted-UCP ceiling (52.9%) than to the neutral median (44.8%). The majority map's 46.1% sits much nearer the neutral median, at the 78th percentile. Both the 2019 enacted map and the 2026 majority fall comfortably within what neutral procedure routinely produces — different vote shares, same zone of unremarkable outcomes. The majority continues 2019 Alberta practice on the partisan-fairness axis the same way it continues 2019 practice on municipal anchoring (80.0% vs 2019's 75.1%). Two maps drawn under the same Alberta rules, by the same five commissioners, in the same room: one lands where neutral procedures routinely produce, the other lands where you have to specifically aim to land.",
			sub4_quote: '<em>This</em> is the shape of the finding, and it is also the framing a court would actually apply.',
			sub5_h: 'Ruling Out Alternative Explanations',
			sub5_p: 'When presented with a statistical outlier of this magnitude, a rigorous audit must test the standard innocent explanations before treating the pattern as unexplained. The structural data (Lane 2) weighs against each of the standard alternative explanations:',
			defense1: '<strong>The "Natural Political Geography" Defense:</strong> <em>("Urban voters are naturally packed; the map just reflects Alberta\'s geography.")</em> The 1,010,000 simulations already account for Alberta\'s natural geography. Geography does give the UCP a baseline efficiency advantage — but the two real comparison maps show where that advantage naturally tops out: both the 2019 enacted map and the 2026 majority sit at the 78th percentile on the tipping-point metric, and the 2019 map\'s highest placement on any partisan measure is the low 90s (declination, 91st percentile). The minority map sits at the 99.99th percentile — an extreme outlier <em>even when compared to Alberta\'s naturally skewed baseline</em>.',
			defense2: '<strong>The "Communities of Interest" Defense:</strong> <em>("The odd shapes were drawn to keep specific communities together.")</em> If you are trying to keep communities together, you follow municipal borders. The majority map followed existing city limits 80% of the time. The minority map followed them 72% of the time — both within the 70–85% Canadian norm. What the minority map does do is actively split the unified city of Airdrie into four separate pieces, and place three of its boundary decisions precisely in the urban-edge zones the commission chair flagged as geometrically anomalous — choices not explainable by community-of-interest logic.',
			defense3: '<strong>The "Population Equality" Defense:</strong> <em>("They had to draw weird boundaries to make sure every district had the exact same population.")</em> On the commission\'s own population tables the minority map is <em>worse</em> at population equality: its Population Mean Absolute Deviation (MAD) was 4,707, 48% wider than the majority map\'s 3,180. On 2021 census numbers the two maps\' mean deviations are almost the same, and the minority\'s median deviation is wider (3,938 against 2,827). That median spread sits at the 99th percentile of neutral maps balanced to within ±12.5%, but at the bottom of the range when neutral maps may use the statute\'s full ±25%.',
			defense4: '<strong>The "Incompetence or Bad Luck" Defense:</strong> <em>("They just drew a sloppy map and got unlucky with the numbers.")</em> Hitting a 60-seat supermajority configuration while also splitting Airdrie into four pieces and placing three boundaries in the exact zones the commission\'s own chair flagged as anomalous requires precision. The joint dependence-robust upper bound on the probability of accidentally drawing a map this extreme on both analytical channels under the ReCom neutral reference distribution is roughly <strong>1 in 568,000</strong> (p&nbsp;≤&nbsp;1.76×10<sup>−6</sup>). That bound is still extreme — well beyond conventional significance — but it is reported as a bound, not as a precise single probability.',
			sub5_close: 'What the data shows is that the minority proposal worsened both population parity and community coherence relative to what the same five commissioners produced simultaneously under identical statutory rules. The audit does not determine what the minority commissioners intended — boundary geometry cannot reveal intent — but the structural departure from both the neutral ensemble and the majority proposal\'s output stands regardless of intention.',
			sub6_h: 'A note on the R cross-validation',
			sub6_p1: 'An earlier version of this audit (using approximated rather than official shapefiles) cross-validated the Python ReCom ensemble against the R <code>redist</code> package\'s Sequential Monte Carlo sampler. The cross-check produced unstable results: across three runs with the same nominal seed, the fraction of plans reaching the old minority value (48.3% on the approximated geometry) was 5.6%, then 28%, then 58% — a sampler-convergence failure, not a discovery. The full write-up is at <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/redist_python_comparison.md" rel="noopener">findings/redist_python_comparison.md</a>.',
			sub6_p2: 'With official Elections Alberta shapefiles, the minority map\'s <code>seats@50/50</code> rises to 51.7% — a value fewer than 100 of 1,010,000 neutral plans reach. The R cross-validation question becomes moot: zero plans from either sampler reach the canonical value at comparable sample sizes.',
			sub6_asymm: '<strong>The asymmetry around 50/50 is more telling than the inversion itself.</strong> A precision sweep of the seat-vote curve at 0.01-percentage-point resolution finds the minority map keeps the UCP at or above the 45-seat legislative-majority threshold down to a UCP provincial vote share of about <strong>49.7%</strong>. This is technically a vote-seat inversion — the UCP would form government on the minority map while losing the popular vote by 0.3 percentage points — but 0.3 points is well within ordinary polling noise, so on its own this is not a dramatic finding. What <em>is</em> dramatic is the contrast: on the <strong>majority</strong> map, the UCP would need to <em>win</em> the popular vote by about 4 percentage points to reach the same 45-seat threshold. Both maps face the same Alberta geography and the same statutory rules; the gap between them — 0.3pp vs +4pp — is structural difference, not noise.',
			sub6_close: 'This is the structural-bias finding the audit holds with confidence. It is geometry-only; it does not depend on any election result; it does not move when polls do.',
			sub6_caveat: '<strong>One caveat the audit takes seriously.</strong> A real electorate is not a uniform 50/50. Voters can swamp any map\'s structural lean with enough swing — a particularly upset or inspired electorate will tip the result regardless of how the boundaries are drawn. The 50/50 test isolates <em>the map\'s contribution to the outcome</em>, not the outcome itself. What it shows is what the map does when the electorate doesn\'t decide for it.',
			sub7_h: 'The bottom line',
			sub7_p1: 'The audit\'s central finding is geometric. <strong>Lane 2 — the structural-irregularity scorecard — is the foundation; Lane 1 is the proof that the geometry is doing partisan work.</strong>',
			sub7_p2: 'The chart below puts both lanes on a single picture. The horizontal axis is Lane 1 (the partisan-fairness efficiency gap, where further right means more UCP-favoured); the vertical axis is Lane 2 (the count of structural-fairness tests the proposal fails, out of five, where higher means more structural problems).',
			stakes_fig_alt: 'Scatter plot with efficiency gap on the horizontal axis and count of structural tests failed on the vertical axis. The 2019 enacted map and the majority 2026 map cluster in the safe lower-left corner. The minority 2026 map appears in the upper-right outlier region. The 2019 map is labelled 0 of 4 run: the Calgary zone test was never run on it.',
			stakes_fig_caption: 'The two ways of measuring the two commission proposals, plotted together. Left-to-right: how skewed the proposal looks on the partisan-fairness number — the further right, the more it favours the UCP. Bottom-to-top: how many of five structural-fairness tests the proposal fails — the higher, the worse. The 2019 enacted map sits in the safe corner: low on both (it fails none of the four tests run on it; the Calgary zone test was never run on it). The majority 2026 proposal stays flat at zero structural problems and near-zero partisan skew (+0.1%). The minority 2026 proposal is a structural outlier on every test that distinguishes the two maps (4 of 5; the fifth, anchoring, is neutral for both); its efficiency gap (+4.0%) sits just below the Alberta threshold line.',
			stakes_table_intro: 'The same findings in plain summary form, leading with the structural finding because the cross-validated evidence supports it most strongly:',
			t5_col_b: 'Structure — Act I (geometry only, no votes; the academic report’s “Lane 2”)',
			t5_col_c: 'Numbers — Act II (vote-dependent; “Lane 1”)',
			t5_r1_a: '<strong>Majority 2026</strong>',
			t5_r1_b: 'clean — crosses <em>no</em> structural threshold',
			t5_r1_c: 'inside the normal range on every measure (tied-vote seat share 46.1%, 78th percentile; efficiency gap +0.1%)',
			t5_r2_a: '<strong>Minority 2026</strong>',
			t5_r2_b: '<strong>crosses 4 of 5 structural thresholds</strong> by a wide margin (anchoring neutral — both maps within Canadian norm)',
			t5_r2_c: 'extreme tail on three of four fairness measures — tied-vote seat share 51.7% (only 69 of 1,010,000 neutral maps reach it); two further measures past the 98.8th and 99.9th percentiles; efficiency gap +4.0% (<em>near but below</em> the pre-set line — a reported miss); combined odds under neutral drawing about 1 in 568,000',
			details2_summary: 'Why the structural act carries the case — technical detail',
			details2_p: "The audit pre-registered five structural-irregularity tests on April 24, 2026, before the final simulation results were compiled. Anchoring is neutral for both maps; of the remaining four, the minority crosses every one and the majority crosses none. Those measurements are geometric — no statistical sampler, no vote data. <strong>This is the central finding.</strong> The simulation corroborates it: the minority sits in the extreme tail on three of four fairness measures, with the fourth (the efficiency gap) just under the pre-set line at the 94.5th percentile, and combined odds of about 1 in 568,000 under neutral drawing — the deliberately cautious ceiling explained in Casing 8. Two honesty notes live in the casings: the flagged boundary shapes themselves are <em>not</em> the direct mechanism of the seat swing — that claim failed its test and the failure is reported (Casing 9; full write-up at <a href='https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/redist_python_comparison.md' rel='noopener'>findings/redist_python_comparison.md</a>) — and the Swing-Zone Allocation Test did not survive its corrected null and is exploratory only (Casing 10). The structural act carries the case; the numbers corroborate without carrying."
		},
		impact: {
			heading: '5: Effects on Representation',
			lanes_label: 'LANE 1 AND LANE 2',
			lanes_body: '<strong>Lane 1 (numbers)</strong> uses election results to test whether the map turns votes into seats fairly: it asks how the map performs across different vote splits. <strong>Lane 2 (structure)</strong> looks only at the drawn lines — city splits, population spread, boundary shapes — and uses no election data at all. Each lane is independent: a map can fail one and pass the other. The minority proposal fails both. The majority passes both.',
			intro: "Lane 1 depends on which election results you score the maps against. Lane 2 does not. Its structural evidence lives in the maps themselves: the drawn lines, the split cities, the places where boundaries follow, or don't follow, administrative lines that exist for other reasons. On these tests the two maps are not close.",
			fig_alt: 'Bar chart comparing four structural-fairness tests side by side, plus a summary score panel. The majority map bars sit at zero or well inside safe ranges. Three of the five panels have a failing line (dashed red): NE/central Calgary crowding, the boundaries the commission\'s majority flagged that the audit confirmed (three of its four), and the summary scorecard. On those three, the minority bar crosses the line and the majority bar stays inside it. The population-spread and Airdrie panels have no failing line; population spread shows the majority at 3,180 and the minority at 4,707 people from the ideal district size. The fifth test, municipal anchoring, was neutral for both maps — both close to the 2019 map\'s 75% — so it is not plotted; the summary panel scores the minority 4 of 5 with anchoring counted as neutral.',
			fig_caption: 'The four structural-fairness tests, side by side, plus a summary score panel. Teal bars are the majority map; purple bars are the minority map. A dashed line appears where a test has a failing threshold: NE/central Calgary crowding, the boundaries the commission\'s majority flagged that the audit confirmed (three of its four), and the summary scorecard. The minority bar crosses every failing line shown. The majority bar never does. The population-spread and Airdrie panels have no failing line — population spread shows the majority at 3,180 and the minority at 4,707 people from the ideal district size. The fifth test, municipal anchoring, was neutral for both maps — both close to the 2019 map\'s 75% — so it is not plotted here; the summary panel scores the minority 4 of 5 with anchoring counted as neutral.',
			table_intro: "The same five tests as a table, each test's threshold set beside its result. The bottom row is the audit's <em>summary</em>: how many of the five tests each map fails.",
			table_col_test: 'Test',
			table_col_majority: 'Majority map',
			table_col_minority: 'Minority map',
			table_col_direction: 'Direction / Beneficiary',
			table_r1_a: 'Border follows existing municipal lines (70–85% Canadian norm)',
			table_r1_b: '80% — within norm',
			table_r1_c: '72% — within norm',
			table_r1_d: 'N/A — both within Canadian norm',
			table_r2_a: 'Population spread (tighter is better)',
			table_r2_b: '3,180',
			table_r2_c: '4,707 — 48% wider',
			table_r2_d: 'Structural (Reduces vote equality)',
			table_r3_a: 'NE/central Calgary population excess above average',
			table_r3_b: '2.8%',
			table_r3_c: '11.5%',
			table_r3_d: '<strong>UCP</strong> (Packs urban NDP votes)',
			table_r4_a: "Boundaries flagged by the commission's own chair",
			table_r4_b: '0',
			table_r4_c: '4 (3 confirmed by the audit)',
			table_r4_d: 'N/A',
			table_r5_a: 'Airdrie split (constraint minimum: 2)',
			table_r5_b: '2 pieces',
			table_r5_c: '4 by territory; 3 by people (≥2%)',
			table_r5_d: '<strong>UCP</strong> (Cracks urban/suburban power)',
			table_r6_a: '<strong>Pre-registered summary</strong> (&ge; 4 of 5 = outlier)',
			table_r6_b: '<strong>0 of 5 fired</strong>',
			table_r6_c: '<strong>4 of 5 fired</strong> (anchoring test neutral — both maps within Canadian norm; remaining 4 tests all fire)',
			table_r6_d: '<strong>UCP</strong>',
			rationales_p: "A separate finding, for the minority alone: <strong>five of six of the minority commissioners' published rationales fail under independent check</strong>. The test runs against the minority only because the majority published no list of rationales for contested redraws. The audit cannot apply it to both maps alike, so it is reported here as a single flag, not as extra rows in the structural-irregularity count.",
			chair_appendix_p: 'The audit also tested a separate, blanket assertion in the majority report, which the chair signed: that the minority\'s changes in five places (Airdrie, Cochrane, Chestermere, Red Deer and St. Albert) had <strong>no public support</strong> in the 1,345 public submissions (final report, pp. 59 and 62). A keyword search across the full submission archive (93.4% machine-parsed, 6.6% image-only and excluded; methodology and per-configuration evidence at <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/submission_search_findings.md" rel="noopener">findings/submission_search_findings.md</a>) turned up a more nuanced picture than either the majority\'s blanket claim or a blanket dismissal of it. The majority was right on three of the five: the Airdrie 4-way split, the Calgary–Nolan-Hill–Cochrane hybrid and the St. Albert minority alternative each lack any documented support. It was wrong on Chestermere, which drew multiple submissions opposing a Calgary merger, which materially align with the minority\'s intent. And it was partly wrong on Red Deer: the Red Deer hybrids drew a peri-Red-Deer hybrid proposal from a sitting Red Deer councillor, aligned in direction but not in exact configuration. Two configurations the majority attacked on other grounds also drew support: Rocky Mountain House–Banff Park drew an explicit, detailed proposal from at least one Clearwater-area submission, plus several aligned ones, and Beiseker residents supported Olds–Three-Hills–Didsbury in writing. So the majority\'s "no public support" sweep is demonstrably overbroad, but it is not invented out of whole cloth, since three of the five do hold up. <strong>This finding cuts against the majority, not against the minority.</strong>',
			summary_p: '<strong>On Lane 2, the majority crosses zero structural thresholds. The minority crosses four of the five, by a wide margin.</strong> The count is a raw tally. It is not a calibrated family-wise probability. Its weight comes from directional unanimity — every test that fires points the same way — not from a joint null-distribution calculation. The statistical lane (§3) supplies the joint probability, through a different instrument.'
		},
		cpd: {
			heading: '4: Cracking, Packing, and Draining',
			vocab_label: 'Three moves, one playbook',
			vocab_packing: "<strong>Packing</strong> means cramming one party's voters into districts the party wins by landslides. Each packed ballot still counts, but once the seat is won it adds nothing more. Large, lopsided wins. Wasted votes.",
			vocab_cracking: "<strong>Cracking</strong> means splitting a community across several districts so it wins none of them outright. A city strong enough to carry two seats gets carved into four, and in three of them its people are outnumbered. Diluted votes. One seat where there could be two.",
			vocab_draining: '<strong>Draining</strong> is the companion move, played out on the map: packed and cracked districts sit side by side, so over-concentrated supporters on one side "drain" voting power away from the contested districts next door. That adjacency, the way the districts touch, amplifies both effects. Packing and cracking reinforce each other across district lines.',
			vocab_disclaimer: 'All three can happen without any explicit partisan intent. What the audit measures is whether the pattern, and its statistical size, is consistent with what a neutral map-drawing process produces. <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md#5-results" rel="noopener">Full methodology at §5 of the technical report.</a>',
			fig_alt: "Two bars showing how each map divides Airdrie's residents, drawn to scale. Majority: Airdrie-West holds 50.6% of the city and Airdrie-East 49.4%, and both divisions are mostly Airdrie. Minority: Airdrie East holds 54.7% of the city and is 89.6% Airdrie; Calgary-Airdrie holds 24.0% and Calgary-Foothills-Airdrie West 20.9%, and both are mostly Calgary; Olds-Three Hills-Didsbury takes about 350 people.",
			fig_caption: "How each map divides Airdrie's people. The majority gives the city two divisions, both mostly Airdrie. The minority gives it one, Airdrie East, with 54.7% of the city, and puts most of the rest in two Calgary-majority divisions.",
			intro: 'The five commissioners worked from the same statutory rules, the same provincial geography, the same archive of 1,345 public submissions, the same demographic data. Their two competing drafts agree on most of Alberta. Where the drafts part, they part on choices someone in the room had to make. Three of those choices are worth seeing as choices. Not numbers.',
			airdrie_p: "<strong>It splits the City of Airdrie into four pieces.</strong> The law caps each electoral division at one-and-a-quarter times the provincial average, so Airdrie needs at least two divisions. The majority map gives it two. The minority gives it four: north to Olds-Three Hills-Didsbury, east to Airdrie East, west to Calgary-Foothills-Airdrie West, centre-south to Calgary-Airdrie. The north piece holds about 350 people, so three of the four hold at least 2% of the city. Only Airdrie East is mostly Airdrie; each other piece is stapled to a Calgary-edge or rural district. An Airdrie resident with a question for her MLA has to know which part of the city she lives in before she can call the right office. Her neighbours two blocks over will give her three different answers. The PTA at her child's school cannot send a single delegation to one MLA on a school-funding question. It has to coordinate four delegations to four offices, and three of those MLAs answer first to voters outside Airdrie. The minor-hockey association, the food bank, the Chamber of Commerce: every organization that works citywide now works across four provincial ridings.",
			airdrie_callout_label: 'WHY AIRDRIE MATTERS',
			airdrie_callout_p1: 'Airdrie has 85,805 people (2024 municipal census). One council, one tax bill, one school division: every civic system treats it as a unit.',
			airdrie_callout_p2: 'Split it across four provincial divisions — Calgary-Airdrie, Calgary-Foothills-Airdrie West, Olds-Three Hills-Didsbury and Airdrie East — and three of them are identified mainly with a neighbouring jurisdiction. The city has 85,805 residents, and one seat in the legislature where a majority of voters call the place home. The majority map gives it two.',
			airdrie_callout_p3: 'A four-way split is invisible to every partisan-fairness test except the one that asks: can a voter find their MLA?',
			airdrie_callout_summary: 'Both maps are legal. The four-way split is a choice.',
			airdrie_btn: 'Show flagged districts on map',
			anchoring_p: "<strong>Where it departs from municipal lines, it departs at strategically important places.</strong> When an electoral map follows the edge of a city or town, voters can tell where their division begins and ends: the property-tax line, the school-division line, the local-election ward line and the provincial-election line all fall in the same place. Statistics Canada publishes these boundaries for free. On official Elections Alberta shapefiles, both maps follow municipal lines at comparable overall rates — the majority at 80%, the minority at 72% — and both sit within Canada's 70–85% norm (Quebec: 78%, Ontario: 82%, BC: 71%; comparator commissions documented in the monograph). (The audit's first, provisional analysis showed the minority anchoring at only 15%; that figure did not survive recomputation on official shapefiles — see the correction note below.) What stands out is not the overall rate. It is where the minority's departures cluster. The three boundaries the commission's own chair flagged as anomalous — Rocky Mountain House–Banff Park <button class=\"ed-trigger\" data-ed-name=\"Rocky Mountain House-Banff Park\">show ↗</button>'s extension into uninhabited national-park land, the Nolan Hill–Cochrane <button class=\"ed-trigger\" data-ed-name=\"Calgary-Nolan Hill-Cochrane\">show ↗</button> lasso corridor, and the Olds–North Airdrie <button class=\"ed-trigger\" data-ed-name=\"Olds-Three Hills-Didsbury\">show ↗</button> reach — each break from pre-existing civic geography, in the exact urban-edge zones where pairing urban and rural voters most directly affects which party wins the seat.",
			anchoring_followup: 'The minority commissioners gave reasons for each of the three flagged boundaries. For Rocky Mountain House–Banff Park, they cited geographic size, the Highway 22 corridor, and how close First Nations reserves sit to Rocky Mountain House. The commission chair called the extension into uninhabited national park land "a bad faith effort" to satisfy the area criterion, and the phrase appears in the commission\'s official final report. For Nolan Hill–Cochrane, they cited shared transportation and employment ties between northwest Calgary and Cochrane. Statistics Canada journey-to-work data shows only 35.8% of Cochrane workers travel to Calgary at all; most work within Cochrane itself. For the Olds–North Airdrie reach, they cited Highway 2 corridor continuity. The audit found the specific Airdrie extension fails on population grounds. Checked independently against primary data, five of the minority\'s six published sub-rationales fail or only partly hold.',
			packing_p: "<strong>One area of Calgary is carved up to concentrate NDP voters into larger-than-average divisions.</strong> In Calgary's north, east, and central districts <button class=\"ed-trigger\" data-ed-name=\"Calgary-North West-Bearspaw\">show ↗</button>, the minority map's divisions average 11.5% above the provincial average. On the majority, 2.8%. The same geographic zone, drawn by the same commission under the same constraints, produces districts about 8.5% larger on one map than on the other. That fits the structural signature of <em>packing</em>: crowding one party's voters into fewer, larger districts, so each of their ballots weighs less. Packing and <em>cracking</em> (spreading a party's voters thinly across districts they narrowly lose) are the two classic gerrymandering moves. Both shrink a party's seat count below its vote share.",
			chair_p: "The commission chair — appointed under the same Act, working from the same submissions — flagged four boundaries on the minority map as geographically anomalous, among them these three: Rocky Mountain House–Banff Park's extension into uninhabited national park land; the lasso-shaped Calgary-Nolan Hill–Cochrane corridor; the Olds–Three Hills–Didsbury reach into north Airdrie. The same chair gave the majority zero such flags. (In all, the chair's published criticism covers seven boundary configurations: the four geometric flags, plus three places named only in the majority report's claim that the minority's changes lacked public support. This audit independently confirmed anomalous geometry for three of the four geometric flags. The fourth, Calgary-Foothills-Airdrie West <button class=\"ed-trigger\" data-ed-name=\"Calgary-Foothills-Airdrie West\">show ↗</button>, did not meet the audit's confirmation threshold.) Beyond the chair's geometry flags, the audit's own cracking-signature test (academic §5.3.2) does not flag the four-way Airdrie split. It is a community split that leaves Airdrie's residents a minority in three of the four ridings, which together hold nearly half the city, but the test needs them outnumbered in all four, and Airdrie East is mostly Airdrie. Chestermere comes up cracking-adjacent; Cochrane, kept whole and about two-thirds of its riding, does not. Some of what the audit's math flags, the chair did not. The audit measures the structural effect. Not intent."
		},
		litmus: {
			heading: '3: The 1,010,000-Map Litmus Test',
			fig_alt: 'Histogram showing the distribution of efficiency gaps across 1,010,000 neutral Alberta maps. Nine in ten fall between about −1% and +4%. The minority commission map (purple line) sits at the 94.5th percentile (+4.0%), just short of the dashed outlier line where the shaded right tail begins. The majority map (teal line) sits at +0.1%, well within the normal range.',
			fig_caption: 'Distribution of <button class="vocab-term" data-def="a measure of how lopsidedly votes are converted into seats — positive values favour the UCP, negative values favour the NDP" aria-expanded="false">efficiency gaps</button> across 1,010,000 neutral Alberta maps drawn from the same geography. Nine in ten neutral maps fall between about −1% and +4%. The shaded right tail marks the top 5%. The minority proposal&rsquo;s +4.0% sits at the 94.5th <button class="vocab-term" data-def="the percentage of maps that scored lower — p94 means 94 out of 100 neutral maps were less partisan than this" aria-expanded="false">percentile</button> — a region fewer than 6 in 100 neutral maps ever reach. The majority proposal&rsquo;s +0.1% is indistinguishable from what a neutral process typically produces.',
			table_intro: "The table sets the two maps side by side. The first five rows use no election results; they are properties of the lines themselves. The last three depend on how votes were attributed to each district.",
			table_col_measured: 'What was measured',
			table_col_majority: 'Majority map',
			table_col_minority: 'Minority map',
			table_col_direction: 'Direction / Beneficiary',
			table_r1_a: 'Population spread across districts (tighter is better)',
			table_r1_b: '3,180',
			table_r1_c: '4,707 — 48% wider',
			table_r1_d: 'Structural (Reduces vote equality)',
			table_r2_a: 'NE/central Calgary population excess above average',
			table_r2_b: '2.8%',
			table_r2_c: '11.5%',
			table_r2_d: '<strong>UCP</strong> (Packs urban NDP votes)',
			table_r3_a: 'Airdrie split',
			table_r3_b: '2 divisions',
			table_r3_c: '4 by territory; 3 by people (≥2%)',
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
			table_r6_b: '46.1% — p78 (normal range)',
			table_r6_c: '51.7% — p99.99 (fewer than 100 of 1,010,000 reach this)',
			table_r6_d: '<strong>UCP</strong>',
			table_r7_a: 'Efficiency Gap (percentile in 1,010,000-map simulation)',
			table_r7_b: '+0.1% — p16.5 (normal range)',
			table_r7_c: '+4.0% — p94.5',
			table_r7_d: '<strong>UCP</strong>',
			table_r8_a: 'Packing-cracking neighbourhood pattern',
			table_r8_b: '2 coupled chain signals',
			table_r8_c: '1 (pre-registered PASS)',
			table_r8_d: 'Neutral — minority achieves partisan effect via hybridization, not adjacency drain (§5.3.5)',
			vocab_label: 'VOCABULARY',
			vocab_eg: "<strong>Efficiency gap.</strong> A single number for how lopsidedly a party's votes turn into seats. Positive numbers favour the UCP; negative, the NDP. The audit draws Alberta's outlier line at ~4.1%: the value exceeded by only 5% of the 1,010,000 neutral Alberta-specific simulations. That threshold is not borrowed from US or general literature. A threshold calibrated to another jurisdiction would be wrong here, because Alberta's natural geography produces a different neutral range.",
			vocab_mm: "<strong>Mean-median difference.</strong> The gap between a party's median district vote share and its mean district vote share. When one party wins many close races, the median sits above the mean: those votes are spread efficiently. When a party wins many races by large margins, the mean sits above the median: votes are being wasted. A large mean-median gap in one direction flags structural inefficiency in how one side's votes are spread across districts.",
			vocab_percentile: '<strong>Percentile ranking.</strong> In this audit, a "percentile" is a rank within the 1,010,000 neutral simulated maps. "p94" means 94% of neutral maps score lower: the real map is more extreme than 94% of neutral draws. "p99.99" means fewer than 1 in 10,000 neutral maps reach that level.',
			vocab_anchoring: '<strong>Anchoring.</strong> The fraction of an electoral border that lies on a pre-existing administrative line — a city limit, a school-division boundary, a Statistics Canada census line.',
			closing_p1: "The bottom rows depend on election results. The <em>seats@50/50</em> test holds the electorate at perfect parity — the UCP and NDP each win exactly half the votes province-wide — and asks how many seats the map hands the UCP. Neutral Alberta maps produce a median around 44.8% UCP seats. Alberta's geography, with NDP voters concentrated in city cores and UCP voters spread across rural ridings, gives the NDP a small efficiency advantage at neutrality. The majority map, at 46.1%, sits at the 78th percentile of the 1,010,000-map simulation: well inside the normal range. The minority map, at 51.7%, sits at the 99.99th percentile. Fewer than 100 of 1,010,000 neutral draws reach that value. The <em>efficiency gap</em> measures how lopsidedly each party's votes turn into seats. On the official Elections Alberta shapefiles the minority's efficiency gap is +4.0%, at the 94.5th percentile: just below the audit's 95th-percentile outlier line. The opening questions at the top of this page unpack the consequences.",
			closing_p2: "The last row cuts the other way. On the neighbour-drain test the minority map has fewer coupled chain signals than the majority: 1 against the majority's 2 (and the 2019 enacted map's 5). The audit pre-registered this test before measuring, and the minority's lower count is a genuine pre-registered PASS. The minority does not show the classic pack-and-drain adjacency pattern. It is the single test where the minority numerically outperforms the majority. §5.3.5 of the academic report explains why. The minority gets its partisan effect through hybridization — city-splitting that internalises packing and cracking within individual electoral divisions (EDs) — and an adjacency-chain test, which only measures how packed districts cluster next to cracked ones, cannot see it."
		},
		commission_split: {
			heading: '2: How the Commission Split',
			intro: 'Alberta\'s Electoral Boundary Commission finished its work on March 23, 2026 and could not agree. Three commissioners produced one map; the other two produced a different one. Commission Chair Justice Dallas K. Miller and two opposition-nominated commissioners wrote the majority report; two government-nominated commissioners — Dr. Julian Martin and John D. Evans — wrote the minority report. The split centred on how to draw boundaries in fast-growing urban-edge communities. The majority gave Airdrie two districts; the minority four. The majority drew north/east/central Calgary\'s divisions close to the provincial average; the minority drew them 11.5% above it. Both maps follow the same statute. Both are legal under the <em>Electoral Boundaries Commission Act</em>. The disagreement was about which specific geographic configurations best served the communities being drawn. Alberta\'s governing party is the United Conservative Party (UCP); its main opposition is the New Democratic Party (NDP). Smaller parties — the Alberta Party, the Liberal Party of Alberta, and others — contest seats too, but their combined provincial vote share has been low enough in recent elections that it does not materially affect the audit\'s partisan-fairness calculations, which are grounded in the 2023 UCP–NDP split. This audit measured both maps using the same methods, applied identically. Four findings stand out.',
			finding1: "<strong>The two maps differ on six things you can measure without looking at any election results:</strong> how evenly people are spread across districts, whether voters are concentrated, how badly cities are cut up, whether borders follow city limits, the shape of the districts, and how many boundaries Commission Chair Justice Miller himself flagged as anomalous in writing (§5.8.2 of the majority report and Appendix C). The minority map differs from the majority on every one of them.",
			finding2: '<strong>Every measured difference favours the same party.</strong> Everywhere the two maps diverge — north and east Calgary, Airdrie, urban areas with clear city limits — the minority map draws boundaries that spread NDP votes thinner and let UCP votes count more efficiently. The communities most reshaped by the minority map are the same communities where the NDP is strongest. The audit cannot determine intent. It can measure effect.',
			finding3: '<strong>The process that replaced the commission had one precedent among the Canadian redistribution cycles this audit reviewed: Alberta\'s own, in 1992.</strong> None of the reviewed provinces hands redistricting, partway through a cycle, to a committee the governing party controls. Most require the legislature to debate the commission\'s map first, or give that map automatic effect unless the legislature overrides it. Alberta does neither. A commission report here changes nothing until the legislature passes a separate <em>Electoral Divisions Act</em>, so the governing party decides whether any commission map becomes law. On April 21 the Assembly used that power: Government Motion 37, passed 44 to 36, set both commission maps aside and gave the work to an MLA committee with a UCP majority. The government\'s stated justification was the chair\'s Recommendation 5. What that recommendation actually asks is set out next.',
			finding4:
				'<strong>The statistical finding survives an independent change of simulation machinery.</strong> Forest-ReCom Phase A (100 k) yields percentile ranks within ±5 pp of canonical ReCom on every partisan metric — the pre-registered robustness check (OSF <a href="https://osf.io/he53s/" rel="noopener">he53s</a>, executed 2026-07-10; every metric moved by less than one percentile point). Details in Casing 9.',
			closing: '<strong>The process is its own finding, separate from the maps.</strong>'
		},
		november: {
			heading: 'The Lunty Committee',
			context_label: 'CONTEXT',
			context_body: ' — This section describes the process that replaced the commission and the legal framework that applies to it. It is not part of the statistical findings. The findings are in the fourteen casings above.',
			intro: "Neither commission map is in force. On April 21, 2026 the Legislative Assembly passed Government Motion 37, setting both aside and referring redistricting to a Select Special Committee of six MLAs — four UCP, two NDP — chaired by Brandon Lunty (UCP, Leduc-Beaumont). The committee itself does not draw the map. It oversees a separate Independent Advisory Panel, constituted under the same motion, tasked with producing a 91-seat boundary proposal.",
			intro_b:
				"Motion 37 contemplated five panel members — a sitting or retired judge as chair, two members nominated by the Premier, and two by the Leader of the Opposition — but Alberta's acting chief justice declined to nominate a judge to the chair. The panel operates with the four appointees the committee confirmed — the Hon. Monte Solberg and Darwin Durnie (Premier's nominees) and Dr. Gerard Kennedy and Brent Robinson (Opposition nominees) — under a chair appointed later: retired Court of Appeal justice Brian O'Ferrall (sourcing in Casing 13 above). The committee must deliver its report to the Legislature by November 2, 2026. Unlike the original commission, neither the committee nor the panel is required to hold public hearings; the panel draws on submissions the original commission gathered. When the committee's map is released, this audit will apply the same methodology to evaluate it.",
			r5_h: 'Recommendation 5: the yardstick the government chose',
			r5_p1:
				'The government justified taking the pen by pointing to one recommendation in the commission\'s report. That makes it the first thing to check when the committee\'s map lands, due November 2. Recommendation 5 was written by one commissioner, the chair, Justice Dallas Miller, in an addendum to the majority report: “My majority colleagues do not agree with me on this point. That is why I am alone in making this recommendation” (final report, p. 66). He also stated its purpose. It “is formulated for the express purpose of dissuading the Legislature from accepting the minority report.”',
			r5_p2:
				'It is a fallback, and it is specific. If the Legislature would not accept the majority\'s choice to remove two divisions outside Edmonton and Calgary, the chair asked it to amend the <em>Electoral Divisions Act</em> from 89 seats to 91, restore those two divisions, and keep “the rest of the province as we propose” (the majority map) “to the extent possible.” An all-party committee would study it. Restoring the two divisions should:',
			r5_a: '<strong>(a) Leave Airdrie and the south alone.</strong> No change to any division in Airdrie, or with any land south of Airdrie\'s southern city limit, except Drumheller-Stettler. On the majority map that is 41 divisions: both Airdrie seats, all 28 Calgary seats, and the 11 divisions around and south of Calgary.',
			r5_b: '<strong>(b) Leave north Edmonton alone.</strong> No change to any Edmonton division north of the North Saskatchewan River: 11 divisions on the majority map.',
			r5_c: '<strong>(c) Put south Edmonton back.</strong> Every Edmonton division south of the river returns to the commission\'s interim map of October 2025, the draft it published for public comment before the final split. The committee may add Nisku to Edmonton-South East if it wants Leduc and Beaumont back in one division. That is 10 divisions on the majority map.',
			r5_d: '<strong>(d) Consider a Clearwater seat.</strong> Consider restoring a division made mostly of Clearwater County and western Mountain View County, with s. 15(2) status. This is the only restored seat the recommendation places. It names no place for the second.',
			r5_p3:
				'Read together, the conditions close off most of the ground the commission split over. Airdrie, Calgary, Cochrane and Chestermere, home to the four-way Airdrie split and the Calgary-edge hybrids, all fall inside condition (a). Red Deer and St. Albert are covered only by the softer clause: keep the majority map “to the extent possible.” A map that reopens Airdrie or Calgary may still be lawful. It is not the map Recommendation 5 describes. The <a href="__BASE__/explorer">map explorer</a> outlines all four under <em>EBC ’26 Annotations</em>; each area’s pin says whether Recommendation 5 changes it or leaves it alone.',
			r5_test:
				'<strong>How it is scored.</strong> The audit\'s November checklist carries this as test X1 (academic report §5.5): the committee\'s map must meet all four conditions. Failing any one means Government Motion 37 did not implement the proposal the government cited.',
			h_anomalous: 'Why the Committee Is Anomalous',
			anomalous_p1:
				"Canadian redistricting practice has, since the 1960s, settled on a single model: an independent commission, insulated from government direction, produces boundary recommendations; the legislature may debate them but cannot easily override them without a formal legislative vote. Alberta's statutory process under the <em>Electoral Boundaries Commission Act</em> follows this template — but with one structural difference from some other jurisdictions: Alberta's commission report has no automatic legal effect. Under the Act, a separate Electoral Divisions Act must be passed by the legislature to give any commission map force of law. This means the government of the day controls not only whether the commission map is debated, but whether it ever becomes law at all. Other Canadian jurisdictions take the opposite default: the commission's recommendations take effect unless the legislature affirmatively votes to override them.",
			anomalous_p2:
				"What the government did in April 2026 had a precedent in Alberta itself: in 1992 a deadlocked commission's work went to a committee of MLAs. This time it allowed a completed, published commission process to conclude — both majority and minority reports filed — and then referred the redistricting task to a six-member committee of MLAs whose majority (four of six) is held by the governing party, without bringing either commission report to a vote. The Lunty committee is not a commission. It has no statutory independence from the government's legislative direction. Its four-member UCP majority mirrors the government's control of the legislature. No other Canadian province has transferred redistricting authority, mid-cycle, to a government-controlled legislative committee after an independent commission had completed its work.",
			h_framework: 'The Constitutional Framework',
			framework_p1:
				'Section 3 of the <em>Charter of Rights and Freedoms</em> — "Every citizen of Canada has the right to vote in an election of members of the House of Commons or of a legislative assembly" — has been interpreted by the Supreme Court of Canada to guarantee not merely the act of casting a ballot but <em>effective representation</em>. The leading authority is <em>Reference re Provincial Electoral Boundaries (Saskatchewan)</em> [1991] 2 SCR 158, in which McLachlin J. (as she then was) wrote for the majority that the purpose of s.3 "is not equality of voting power per se, but the right to effective representation." Population parity is the primary consideration; departures are permitted when justified by community of interest, geography, history, or minority-representation objectives.',
			framework_p2:
				"The Saskatchewan framework does not categorically prohibit partisan considerations in redistricting. What it establishes is that boundary maps must, on the whole, provide effective representation to voters — and that systematic impairment of one identifiable group's ability to elect proportionate representation is the pattern that s.3 challenges target. The audit's statistical and structural findings — the minority map's position at the 99.99th percentile of 1,010,000 neutral draws, its crossing of four of five structural thresholds (the fifth, anchoring, is neutral for both maps), the identified communities affected — are the evidentiary record a s.3 applicant would need to assemble. On the community-of-interest side of that record, the Federal Court's decision in <em>Raîche v. Canada</em> (2004 FC 679) is the leading Canadian authority: the court there required the federal Electoral Boundaries Commission to revisit boundaries that had ignored Acadian community of interest in New Brunswick. The audit's municipal-anchoring measurements and its specific community findings — Airdrie split into four districts, the chair-flagged urban-edge anomalies in northwest Calgary — are the same kind of evidence the Federal Court treated as legally cognizable. Whether that record meets the constitutional threshold is a legal question this audit does not decide; the audit reports the measurement.",
			framework_p3:
				"The committee's legality as a process is a separate question. Alberta's <em>Electoral Boundaries Commission Act</em> does not expressly prohibit the legislature from constituting a parallel redistricting body, because the Act contemplates that the legislature will enact the final boundaries through ordinary legislation regardless. Whether the committee process, if it produces a map with the structural and statistical profile of the minority proposal, could survive a s.3 Charter challenge turns on whether effective representation is achievable under the resulting boundaries — the same test that would apply to any commission-produced map.",
			h_quebec: 'The Quebec Contrast',
			quebec_p1:
				"Quebec offers the comparison most relevant to Alberta's situation. Quebec's Commission de la représentation électorale (CRE) is a permanent, independent electoral boundaries body, not an ad hoc commission constituted per redistribution cycle. The CRE operates continuously and cannot be dissolved or bypassed by cabinet action. Under Quebec's <em>Loi électorale</em>, the CRE establishes the final electoral map itself: the National Assembly debates the commission's report and hears representations, but does not vote to adopt or override it — within ten days of that debate the commission sets the boundaries, which are published in the Gazette officielle. The practical effect is that a governing party cannot, acting alone with its own majority, substitute its preferred map for the commission's; on the delimitation itself, the independent body has the last word.",
			quebec_p2:
				"Quebec's model emerged partly from lessons about what happens when redistricting is not insulated from partisan control. The contrast with Alberta's current process — where a majority-controlled committee has replaced the commission's work before the legislature has voted on either commission report — illustrates the structural difference between redistricting systems that assume partisan pressure and design against it, versus systems where that pressure has a clearer path to the outcome.",
			closing:
				"The audit will apply the same tests to the Lunty committee's map when it is released. The constitutional and comparative observations above are contextual; the methodology does not change.",
			process_scorecard:
				'The map is only half of what gets scored in November. The process gets its own instrument: a nine-feature scorecard — hearings, published drafts, arm\'s-length drafting, and the rest of what the sixty-year norm guaranteed — published in draft on <a href="__BASE__/norms#measurable">the norms page</a>. Four of the committee\'s failing cells are features it can still add before it reports.'
		},
		casings: {
			frame_h: 'The Smoking Gun',
			frame_p1:
				'You came here looking for a smoking gun. This report does not have one. It cannot have one — and why it cannot is the most important thing we found.',
			frame_cast:
				'Alberta’s 2025–26 Electoral Boundaries Commission finished its work on March 23, 2026, and could not agree. Three commissioners signed one map. The other two — the two the government nominated — signed a different one. Both maps are legal under the <em>Electoral Boundaries Commission Act</em>. Four weeks later, on April 21, the Legislative Assembly set both maps aside and handed the pen to a committee of six MLAs: four of them from the governing United Conservative Party (UCP), with a UCP member in the chair. That committee’s map is due November 2, 2026.',
			frame_p2:
				'We measured both commission maps, and the process around them, every way we knew how. What we found is not a gun. It is casings: fourteen pieces of evidence, each one real, each one measured, each of which would count for something in a courtroom — and none of which, alone or together, can legally prove the conclusion they invite. A spent casing on the ground proves a gun existed and was fired. It cannot prove whose hand was on it. That gap between evidence and proof is not a loophole we failed to close. In Canada, it is the system as written. That, too, is a finding.',
			frame_p3: 'So this report is built like an evidence log. Each casing gets the same five questions, in the same order, every time:',
			beat_found: 'What we found',
			beat_found_d: 'the evidence, with its number.',
			beat_show: 'What it could show',
			beat_show_d: 'the conclusion you will be tempted to draw, stated at full strength.',
			beat_experts: 'What the experts say',
			beat_experts_d: 'how this kind of evidence is treated in places that do fight about it in court.',
			beat_canada: 'What Canadian practice expects',
			beat_canada_d: 'the norm.',
			beat_gun: 'Why it isn\u2019t a smoking gun',
			beat_gun_d: 'the specific reason, under Canadian law, this evidence proves less than it seems to.',
			frame_p4:
				'Each of the eight legal reasons is different. By the fourteenth casing you will have learned, one piece at a time, how Canadian boundary law really works — and why every casing in this log ends the same way.',
			frame_p5:
				'Two casings in the log point the wrong way for our own story, and both are reported in full: one test that stopped telling the maps apart when better data arrived, and one lane where the minority map did better than the majority. A report that never loses an argument with itself isn\u2019t checking. Failed and null tests are part of the record.',
			frame_coi:
				"One more thing belongs in the log before the first casing: the author's own prior. He has voted for and donated to both conservative and progressive provincial parties in Alberta. For about 27 years he has also worked as a contract election officer for Elections Alberta, election by election, administering the vote on election day; nothing in this audit comes from that work. Three findings that ran against his expectation are kept in this log anyway, and every number reproduces from public code, public data, and random seeds committed in public before the analysis ran.",
			frame_lenses:
				'This episode has three lenses, and each has its own companion page: <a href="__BASE__/law">what the law asks</a>, <a href="__BASE__/norms">what the norms ask</a>, and <a href="__BASE__/methods">how the maps were tested</a>. The log below draws on all three.',
			frame_p1b:
				'Or maybe you came for something simpler. You heard Alberta is fighting over its electoral map, and you want to know what the fight is about. The short version: where district lines fall decides whose votes add up to a seat and whose scatter. Alberta was redrawing its ridings, the districts that each elect an MLA. The independent commission doing the work split into two camps and filed two competing maps on March 23, 2026 — both legal under the Act, both signed. Four weeks later the government set both aside and handed the pen to a committee its own party controls, a move Alberta last made in 1992. The fight is over what that committee will draw this November, and whether anyone could tell if it were drawn unfairly. This audit exists so that someone can tell.',
			frame_routes:
				'Two ways in, then. If you came to learn the fight, start with the picture just below, then the map on the cover; the interlude midway down brings it to your own street. Each of the episode\'s three lenses has its own plain-language page: <a href="__BASE__/law">the law</a>, <a href="__BASE__/norms">the norms</a>, <a href="__BASE__/methods">the statistics</a>. If you came for the gun, the log starts at Casing 1: fourteen casings, five questions each, every one ending the same way.',
			refrain: 'A casing, not a gun.',
			refrain_not_even: 'Not even a casing. We logged it anyway.',
			c2_refrain: 'An accusation in the official record — a casing, not a gun.',
			c3_refrain: 'Two casings now, still no gun.',
			c4_refrain: 'Three casings now, still no gun.',
			c6_refrain: 'Sixty-nine of 1,010,000 — a casing, not a gun.',
			c8_refrain: 'One in 568,000 — a casing, not a verdict.',
			c11_refrain: 'Bad reasons for a lawful line — a casing, not a gun.',
			c13_refrain: 'Lawful, every step — a casing, not a gun.',
			know_more: 'Know more',
			act1_h: 'Act I: What the Map Does',
			act1_intro:
				'Act I walks the lines themselves. No election results, no simulation: just geometry anyone can check against a paper map. The two drafts were drawn in the same room, by five commissioners working from the same statutory rules, the same provincial geography, the same archive of 1,345 public submissions and the same demographic data. They agree on most of Alberta. Where they part ways, they part on choices someone in the room had to make.',
			act1_table_h: 'Act I in one picture',
			act1_table_close:
				'On Act I\u2019s tests, the majority crosses zero of the discriminating structural thresholds, the ones that tell the maps apart. The minority crosses every discriminating one: four of four, with the fifth, which does not tell the maps apart, shown rather than hidden. These measurements are geometric. They need no statistical sampler and no vote data. We pre-registered all five on April 24, 2026, fixing them in writing before the final simulation results were compiled.',
			c1_title: 'Casing 1 — A city of 85,805 with one seat of its own',
			c1_found:
				'The minority map splits the City of Airdrie into four pieces. Airdrie has 85,805 people (2024 municipal census), one council and one tax bill. Its council and city services treat it as a unit. The law caps each electoral division at one-and-a-quarter times the provincial average, so Airdrie needs at least two divisions. The majority map gives it two. The minority gives it four: north to Olds-Three Hills-Didsbury, east to Airdrie East, west to Calgary-Foothills-Airdrie West, and centre-south to Calgary-Airdrie. Airdrie East takes more than half the city, and nine in ten of its people are Airdrie residents. Nearly all the rest of the city is stapled to two Calgary-edge districts, where Calgary residents outnumber Airdrie’s. The north piece holds about 350 people. Our cracking test (academic report §5.3.2), a test whose rules we wrote down in the same session we first ran it, so it counts as exploratory, sets a first bar: more pieces than the city’s size requires. The split clears it. It fails the second, that Airdrie’s residents be outnumbered in every piece, because of Airdrie East. By the test’s own rule, that is no cracking signature. The majority’s two-way split fails both bars.',
			c1_show:
				'For the part of the city outside Airdrie East, the minority’s split is the textbook definition of cracking: splitting a community so thinly that it decides nothing. An Airdrie resident with a question for her MLA has to know which part of the city she lives in before she can call the right office. The PTA at her child’s school cannot send a single delegation to one MLA on a school-funding question. It has to coordinate four delegations to four offices, and three of those MLAs answer first to voters outside Airdrie. If you wanted to dilute a fast-growing, politically contested city, this is what it would look like.',
			c1_experts:
				'Community splitting is one of the primary red flags in the redistricting literature, because it is one of the two mechanical moves by which lines turn votes into fewer seats. The other is packing, its mirror. A four-way split is invisible to every partisan-fairness statistic except the one that asks: can a voter find their MLA?',
			c1_canada:
				'Canadian commissions treat municipal integrity — keeping a city whole — as a core anchor for community of interest, the shared ties the law asks boundary bodies to weigh. Splitting a city this size in two is routine. Splitting it four ways, leaving nearly half its residents outnumbered, is not. And the same commission’s majority map proves a two-way split was available, on the same geography.',
			c1_gun:
				'The <em>Electoral Boundaries Commission Act</em> allows municipalities to be split. Community of interest is one factor among several the Act lists, and it does not bind. The Supreme Court of Canada\u2019s <em>Saskatchewan Reference</em>, the leading case on effective representation, tells courts to defer to how boundary bodies weigh those factors. Our review found no Canadian decision striking down a map for splitting a city. Both maps are legal. The four-way split is a choice, and under Canadian law, choices inside the statute\u2019s wide lanes belong to the drawer. <em>(Legal lesson 1: the statute\u2019s factors are discretionary, and courts defer.)</em>',
			c1_app: 'what \u201ccracking\u201d actually does to a vote',
			c2_title: 'Casing 2 — The three boundaries the chair called out',
			c2_found:
				'The commission’s majority (the chair and two commissioners), appointed under the same Act as the minority and working from the same submissions, signed a report that flags four boundaries on the minority map as geographically anomalous, among them these three: the Rocky Mountain House–Banff Park extension into uninhabited national-park land; the lasso-shaped corridor of Calgary-Nolan Hill–Cochrane; and the reach of Olds–Three Hills–Didsbury into north Airdrie. That report, the commission’s official final report, calls the park extension “a bad faith effort” to claim a population protection written for remote communities where people actually live. The majority raised zero such flags against its own map. That is not an independent verdict between the two maps: criticism running only against the other side is what you would expect. What gives the flags weight is our own geometric tests, which score both maps by the same rules. They confirmed anomalous geometry for three of the majority’s four geometric flags. (The fourth, Calgary-Foothills-Airdrie West, did not meet our confirmation threshold; the report’s published criticism covers seven boundary configurations in total.)',
			c2_show:
				'The commission’s majority, the chair among them, accused its colleagues in the official report of a bad-faith use of s.15(2). Our check undercuts the charge: the district qualifies without the park. The accusation shows how deep the split ran, not that the protection was gamed.',
			c2_experts:
				'Spotting a gerrymander — lines drawn for a party’s advantage — began with bizarre shapes, and corridors and uninhabited extensions are the classic signatures. In fairness, the Banff arrangement has a defensible geography under the odd name and the odd shape. The town of Banff sits inside a federal park it cannot grow into, and grouping the townsite with Canmore has sound community-of-interest logic. Our Banff analysis credits that two-sided story in full. It also tests the charge itself, and undercuts it: without the empty-park extension, the district still meets four of the five criteria for that protection (s.15(2) of the Act), so it never depended on the park. What the townsite’s placement cannot explain is why the line runs out into the park at all.',
			c2_banff_link: 'See Banff on the map',
			c2_canada:
				'Commissioners disagree in their reports all the time. A commission majority accusing colleagues of bad faith in the official final report is rare. We know of no other instance, though we have not searched past reports systematically.',
			c2_gun:
				'The majority’s words are opinion, inside a report with no legal force. “Bad faith” in a commission report is an accusation, not a ruling: no tribunal ever weighed it. Under the Act, both reports became advisory the moment they were filed — advice, and only advice. The legislature could set them both aside. It did. <em>(Legal lesson 2: commission reports bind no one — the legislature holds the pen.)</em>',
			c2_app: 'shape analysis and what s.15(2) protection is for',
			c3_title: 'Casing 3 — One zone of Calgary, drawn 11.5% too big',
			c3_found:
				'Take a single zone of Calgary. Same commission, same constraints — and on one map its districts come out about 8.5% larger than on the other. In the city’s north-east and central districts, the minority map’s seventeen divisions hold on average 11.5% more people than the provincial average. The majority’s hold 2.8% more. That is a finding about equal population. It is not a packing signature. Our packing test (academic report §5.3.1) also needs the zone’s NDP-won districts to be won by wide margins, at least 15 points above the provincial average. On 2023’s votes the NDP wins eight of the minority map’s seventeen, by an average of 15.0 points: 12.6 below the provincial average of 27.6. The test fails, so no packing signature is detected. We wrote its rules in the same sitting that first ran it, so the test was exploratory from the start.',
			c3_show:
				'A larger district means each ballot in it weighs less, whoever casts it. Crowding one party’s voters into fewer, larger districts is called packing, and with cracking (finding 1) it is one of the two classic gerrymandering moves. Here the size gap is real, but the wide winning margins that would mark packing are not there.',
			c3_experts:
				'Packing and cracking are the mechanism behind essentially every partisan-gerrymandering case ever argued in a United States court. Oversized districts exactly where one party\u2019s voters cluster: that is the pattern the detection research is built to find.',
			c3_canada:
				'Some spread from the average is normal inside the legal band, but Canadian commissions justify it with community-of-interest reasons. The minority\u2019s published reasons for this zone are among those that fail an independent check. See finding 11.',
			c3_gun:
				'Every one of those districts sits inside the Act\u2019s \u00b125% population band, and Canadian law has no cause of action — no grounds to sue — for partisan effect. Section 3 of the Charter protects citizens\u2019 effective representation: a meaningful voice, not just equal numbers. It does not promise parties that votes will turn into seats in proportion, and no Canadian court has read it that way. <em>(Legal lesson 3: inside the band, size asymmetry is lawful discretion — partisan effect is not a recognized legal harm.)</em>',
			c3_app: 'packing in a three-district toy example',
			c4_title: 'Casing 4 — Worse at the one thing the law actually measures',
			c4_found:
				'Take each district, measure how far its population sits from an equal share, and average the gaps: that is the mean absolute deviation, or MAD. On the commission’s own population tables, the minority map’s districts stray further from equal than the majority’s — a MAD of 4,707 people against 3,180, 48% wider. On 2021 census numbers the gap is smaller. The two maps’ mean deviations are almost the same, while the minority’s median deviation (the gap for the district in the middle of the pack) is still wider: 3,938 against 2,827. Against neutral maps — drawn by computer, with no stake in who wins — that balance each district to within ±12.5%, that median spread sits at the 99th percentile, wider than nearly all of them. Against neutral maps allowed the statute’s full ±25%, both commission maps sit at the bottom of the range.',
			c4_show:
				'Vote equality — every vote weighing the same — is the one value the statute measures in every district, and on the commission’s own figures the minority map gives up more of it than the majority drawn beside it. The common defence — “they had to draw weird boundaries to equalize population” — runs backwards here. The minority map is the less equal of the two.',
			c4_experts:
				'In every formal model of redistricting, equal population is the constraint that comes first. Spread this wide, on a map drawn at the same time as a tighter one, is a cost signal: evidence that other goals outranked the statute\u2019s central value.',
			c4_canada:
				'Canadian commissions treat the deviation band as a limit, not a budget. In Alberta, the commission itself sees “a clear historic trend” “towards greater emphasis on voter parity” (final report, p. 24).',
			c4_gun:
				'The statute’s one population rule is the ±25% band, with room for up to four remote divisions to sit as much as 50% below average (s.15(2)). Each map uses three of those four exceptions, and no district on either map breaks the rule. Inside the band, the law does not rank maps. A wider spread and a tighter one are legally the same. <em>(Legal lesson 4: the statute has one population rule, and the minority map complies with it.)</em>',
			c4_app: 'what MAD measures and why the band exists',
			c5_title: 'Casing 5 — The casing that dissolved when we picked it up',
			c5_found:
				'How often does a district line follow a city or town boundary? The majority map does it 80% of the time and the minority 72%. The 2019 map, drawn by the last commission, does it 75% of the time. This test does not separate the two maps.',
			c5_show: 'When a district boundary follows a city or town line, the property-tax line, the school-division line and the provincial-election line all match, and voters can tell where their district begins and ends. On that measure the two maps look alike.',
			c5_experts:
				'This is what an artifact looks like: a signal made by the tools, not by the map. Provisional tracings manufactured it, and the real map files erased it. That lesson in method is why we re-ran everything on the official shapefiles the day Elections Alberta released them.',
			c5_canada:
				'Nothing. No Canadian statute or practice guide requires any particular anchoring rate. The 70–85% norm describes what commissions do; it does not prescribe what they must do.',
			c5_gun:
				'It settles nothing either way. Both maps sit close to the 2019 map, and the Act sets no anchoring threshold.',
			c5_app: 'what municipal anchoring measures, and what it can\u2019t show',
			act2_h: 'Act II: What the Simulation Sees',
			act2_intro_p1:
				'Act I needed nothing but the lines. Act II asks a harder question: how unusual are these maps, next to what a process with no agenda would draw? To answer it, we had a computer draw 1,010,000 mathematically neutral Alberta maps (4 independent chains \u00d7 252,500 steps, base seed from the Cloudflare drand public randomness beacon, pre-registered at OSF before execution). It used the official Elections Alberta shapefiles and held to the same statutory rules and geographic boundaries the commission used. Think of the simulation as a \u201cwhat-if machine\u201d: what would Alberta\u2019s maps look like if nobody was trying to do anything? Set a real map inside that crowd, and its percentile \u2014 its place in the line \u2014 tells you how far out into the tail, the rare end, it sits.',
			act2_intro_p2:
				'One fact about Alberta makes every number below readable. In this province, neutral is not 50/50. Split the province-wide vote exactly evenly, and the median of the 1,010,000 neutral maps — the middle of the pack — gives the UCP only 44.8% of seats. Why? Rural UCP voters win their ridings by wide 60-40 margins, wasting many \u201cextra\u201d votes, while urban NDP voters win theirs by tighter 51-49 margins and waste fewer. Left alone, Alberta\u2019s natural political geography mildly favours the NDP\u2019s seat efficiency. Keep that baseline in mind. It is what the maps below are measured against.',
			c6_title: 'Casing 6 — Fewer than 100 maps in 1,010,000',
			c6_found:
				'Set the real maps in a crowd: maps a computer drew with no stake in who wins. Split the vote dead even, 50/50, and ask each map how many seats it hands the UCP. Across the million neutral maps the median answer is 44.8%, and the ceiling is 51.72%: 45 of 87 seats, because the neutral maps have 87 districts, the 2019 count. Only 69 of the 1,010,000 go past the minority map’s 51.69% (46 of 89), and all 69 sit at that ceiling. The 2019 enacted map sits at 46.0% (78th percentile, or the 65th once tied maps are counted as ties), the 2026 majority at 46.1% (78th percentile). The minority sits at 51.7%: the 99.99th percentile, at the far edge of the crowd. Two other pre-registered fairness measures agree. On each, the minority map lands deeper in the tail than 98 to 99.9 per cent of the neutral maps, all leaning the same way — toward the UCP. What does that mean in seats? Replay the 2023 election-day vote and the minority map’s geometry gives the UCP 60 of 89 seats. On the majority map, 55.',
			c6_found2:
				'How far can \u201caiming\u201d go? To find out, we also ran a targeted hill-climbing search — the standard tool for exploring biased-but-legal maps, which nudges a map step by step toward a chosen party — in both directions, 40,000 steps each, same constraints, same geometry. The minority map\u2019s 51.7% sits closer to the deliberately aimed UCP ceiling (52.9%) than to the neutral median (44.8%). The majority map\u2019s 46.1% sits much nearer the neutral median, at the 78th percentile. And around 50/50 the lopsidedness is starker than the number alone. A precision sweep finds that the minority map keeps the UCP at or above the 45-seat majority threshold down to a UCP vote share of about 49.7%: the UCP could lose the popular vote by 0.3 points and still form government. On the majority map, the UCP would need to win the popular vote by about 4 points to reach the same threshold. Same geography, same rules. The gap between the two maps is structural, not noise.',
			c6_show:
				'Neutral processes essentially never produce a map like the minority’s. The majority map is the kind of map a neutral procedure turns out routinely. The minority map is the kind you have to aim to draw.',
			c6_experts:
				'Ensemble outlier analysis — testing a real map against a crowd of neutral ones — is the state of the art in redistricting statistics. It is the method US courts found persuasive in the state cases that struck maps down. Three of four pre-registered metrics in the extreme tail, all four leaning the same way: that is a strong outlier profile. And the \u201cit\u2019s just Alberta\u2019s natural geography\u201d defence is already answered inside the method, because the simulation runs on Alberta\u2019s natural geography. That geography\u2019s baseline advantage tops out where the 2019 map and the 2026 majority sit: the 78th percentile, with the 2019 map\u2019s highest placement on any partisan measure in the low 90s. Against Alberta\u2019s naturally skewed baseline, the minority sits at the 99.99th percentile.',
			c6_canada:
				'No Canadian commission has ever been required to test its map against a neutral ensemble, a computer-drawn crowd like ours. Here we are importing a standard the process itself never had to meet. That is exactly why the result is informative, and exactly why it binds nobody.',
			c6_gun:
				'Two limits, one legal and one statistical. Legal: as far as our review found, no Canadian court has yet weighed ensemble evidence. In the United States, the Supreme Court held in <em>Rucho v. Common Cause</em> (2019) that even strong statistical evidence of partisan gerrymandering is not for federal courts to police. A percentile is a description, not a threshold crossed. Statistical: the ensemble respects population and contiguity (each district a single connected piece), but it does not enforce every statutory criterion the commission worked under (the s.15(2) exception for remote divisions, community of interest, municipal anchoring). So its percentiles measure extremity against that reference distribution, not against “everything a legally compliant commission might have drawn.” Nor does it match the commission maps’ size: its maps have 87 districts, theirs 89. A run that draws 89 districts and holds the s.15(2) divisions where the commission put them still places the minority past the 98th percentile on the three measures where it sits in the far tail; the full same-size comparison is not final yet. A strong outside check; not a perfect one. One further honest limit: a real electorate is not frozen at 50/50. With a big enough swing, voters can swamp any map’s structural lean. The 50/50 test isolates the map’s contribution to the outcome, not the outcome itself. <em>(Legal lesson 5: the best evidence type in the field has no legal home in Canada.)</em>',
			c6_app: 'how the what-if machine works and how to read a percentile',
			c7_title: 'Casing 7 — The test that missed',
			c7_found:
				'That leaves the fourth partisan-fairness metric, the efficiency gap: a single number for how lopsidedly a party’s votes turn into seats, built from wasted votes (the votes a winner had beyond what was needed, plus every vote cast for a loser). For the minority map it came in at +4.0%, the 94.5th percentile. Our pre-registered outlier line is the 95th percentile (about +4.1% on Alberta’s simulated distribution). It missed. It leans toward the UCP, but it falls below the line, and every table in this report shows it that way. The majority map’s efficiency gap is +0.1% (16.5th percentile).',
			c7_show: 'On its own, almost nothing. That is exactly why it is in the log.',
			c7_experts:
				'Near-misses are what an honest battery of tests naturally produces. If every test in a report fires, a reader should grow more suspicious of the auditor than of the map. This one missed, and it stays a miss. (The efficiency gap’s proposed US threshold, about 7%, is an academic proposal no court has adopted.)',
			c7_canada: 'Nothing. No Canadian body uses the efficiency gap at all.',
			c7_gun:
				'We do not claim it as evidence at all. This entry is here to show the record was counted honestly. Pre-registration cuts both ways: the same locked line that gives the other metrics their force makes this one a miss. And a miss it stays. <em>(Epistemic lesson: the threshold was set before the answer was known — so the answer is allowed to be \u201cno.\u201d)</em>',
			c7_refrain: 'A casing, not a gun — and this one we do not even fire.',
			c7_app: 'the efficiency gap in one worked example',
			c8_title: 'Casing 8 — One in 568,000, and what that number is not',
			c8_found:
				'Picture a drawing process with no agenda. How likely is it to produce the minority map’s combined four-metric profile? The chance is bounded at about one in 568,000. That is a deliberately cautious ceiling: we doubled our own margin to cover the second analytical channel we examined (the Swing-Zone Allocation Test, finding 10). Why double it, rather than quote the stronger single-test number? Because we gave ourselves two chances to find something rare — two channels, two chances for luck to look like a signal — so the odds are multiplied by two before they are quoted. The doubling holds no matter how the two channels relate. The four measures inside the simulation count as one look, not four, because they are combined into a single joint score before any probability is computed. On that joint score no neutral map lands as far out as the minority’s, so the chance cannot be counted from the crowd. It comes from a curve fitted to the crowd, which matches it closely except near the edge, where the real crowd runs slightly thicker (academic report, Appendix G). (For the technical record: p ≤ 1.76×10⁻⁶, a Bonferroni-corrected, dependence-robust upper bound.)',
			c8_show:
				'You will want this number to mean “the probability the map is innocent.” It is our strongest single number, and the pull to read it that way is enormous.',
			c8_experts:
				'The number is well defined, and defensible as what it actually is: the probability of the map\u2019s measured profile turning up under a neutral drawing process. In statistics, confusing P(evidence given innocence) with P(innocence given evidence) has a name, the prosecutor\u2019s fallacy, and it has sent innocent people to prison. This report refuses the swap. How rare the map is under the neutral null — the no-agenda baseline — is not the probability of wrongdoing once the evidence is in (what statisticians call the posterior). For that you would need things no one has, like the base rate of eccentric-but-sincere drafting.',
			c8_canada:
				'No Canadian legal standard takes in a number like this. There is no threshold for it to cross, because the law never defined one.',
			c8_gun:
				'A one-in-568,000 map can still, in principle, come from unusual but honest judgment. The number measures how far outside neutral practice the map sits. It cannot see motive, and this report will not pretend it can. What we do claim is the weaker statement, and it is well supported: routine drafting variation is not a plausible explanation for this profile. What the explanation is, we put in your hands. <em>(Legal-epistemic lesson: no probability of a map is a probability of intent.)</em>',
			c8_app: 'the prosecutor\u2019s fallacy in plain language',
			c9_title: 'Casing 9 — We tried to shoot our own result down',
			c9_found:
				'We mounted three attacks on our own headline, the minority map’s place at the far edge of the crowd. The results were mixed, and all are reported in full. First, the sampler swap: we replaced the simulation’s mathematical engine with a structurally different one (a spanning-forest sampler, pre-registered at OSF as registration he53s and executed 2026-07-10), and the tail position survived. Every metric’s percentile moved by less than one point, a pre-registered ROBUST verdict on all four. Second, the software swap: an independent implementation (the R redist package) also finds zero plans reaching the minority’s value at comparable sample sizes. Third, the mechanism test, and here our claim failed. We tested whether the odd shapes on the map (the corridors, the park extension) are the specific mechanism producing the seat advantage in the simulation. If they were, the neutral maps that hand the UCP more seats should be less compact than the rest. They are slightly more compact. Both kinds of evidence point at the same map and lean the same way, but the claim that the shapes are the mechanism did not survive its falsification test, the test built to knock it down. The report says so.',
			c9_show: 'The outlier belongs to the map, not to our tools.',
			c9_experts:
				'Holding up across samplers and implementations is what separates a finding from an artifact. Publishing your own failed falsification is what separates an audit from advocacy.',
			c9_canada: 'Nobody requires any of this. We imposed it on ourselves, in writing, before running it.',
			c9_gun:
				'Ruling out artifacts is not ruling in design. Surviving every attack we could mount establishes that the map is genuinely, robustly extreme. It says nothing about why. <em>(Epistemic lesson: robustness strengthens the description, never the accusation.)</em>',
			c9_app: 'what a sampler is and why swapping it matters',
			c10_title: 'Casing 10 — The signals that pointed the other way',
			c10_found:
				'Two entries in the log do not help our story. Both are reported. One the minority passed outright. The neighbour-drain test looks for the classic adjacency pattern, where packed districts sit right beside thin-margin ones. The minority shows 1 coupled chain signal against the majority’s 2 (and the 2019 enacted map’s 5): a pass, and one of the few tests where the minority beats the majority on the numbers. We specified the test on April 24 and registered it on the OSF on May 6, after a provisional pass on approximate boundaries. The pass is real but narrow. Our reading (academic report §5.3.5) is that the minority gets its partisan effect through hybridization — splitting cities into districts that mix urban and rural voters inside single ridings — and an adjacency test cannot see that, because the packing and cracking happen within districts rather than between them. That is a reading, not a tested result, and it is not what finding 9’s failed test was about: that test asked about the shapes of the lines, not about which voters they put together. One we retired. The Swing-Zone Allocation Test asked whether swing-zone voting areas were allocated to districts in a partisan pattern. It looked significant (p = 0.0024) until we corrected its null, the baseline of chance it is measured against, for spatial clustering: neighbouring voting areas vote alike, which violates the test’s assumption that each area is independent. After the correction it returns p ≈ 0.19, not significant, and on 2026-06-13 it was retired to exploratory status.',
			c10_show:
				'As first computed, the retired test suggested the specific boundary choices — not just the overall map — were partisan-loaded. After correction, it suggests nothing.',
			c10_experts:
				'Spatial autocorrelation — neighbours resembling neighbours — is the classic way redistricting statistics fool their own makers, and correcting for it is the method working as intended. A drain-test pass alongside tail results elsewhere is not a contradiction. It is a fingerprint: it tells you which mechanism this map does not use.',
			c10_canada: 'Not applicable. These are our own instruments.',
			c10_gun:
				"One of these was our own instrument failing, not the map’s, and the other points in the map’s favour. Both are in the record because a record that keeps only the convenient entries is not a record. <em>(Epistemic lesson, stated twice in this report on purpose: the null can win.)</em>",
			c10_refrain: 'Two retired, one pass for the other side. We logged them anyway.',
			c10_app: 'why neighbours voting alike breaks naive statistics',
			act3_h: 'Act III: What People Did',
			act3_intro:
				'Acts I and II measured paper. Act III reads conduct: what the people in and around the process wrote, claimed and chose. In court, conduct is usually where questions of intent get answered. Watch what happens to it here.',
			c11_title: 'Casing 11 — Five of six reasons don\u2019t survive checking',
			c11_found:
				'Lines can be measured. So can the reasons people give for them. The minority commissioners published reasons for their contested redraws. Four of the six fail an independent check, and a fifth holds only in part. The point is not that the minority’s reasoning is invented. In most of these cases the general claim is true, and a boundary honouring it could have been drawn. What the data does not reach is the particular line the minority actually drew. Take Calgary-Nolan Hill–Cochrane, which the minority defends on the idea that Cochrane residents “move fluidly” into Calgary. Statistics Canada’s 2021 journey-to-work data shows about 71 percent of Cochrane’s out-commuters work somewhere in Calgary (a third of all its workers), while roughly half of its workers stay within Cochrane: a real city-to-city tie, but one that says nothing about the Nolan Hill neighbourhood the corridor actually reaches. Airdrie’s commute to Calgary (about 76 percent of its out-commuters) and its rapid growth are both real, and could have supported a new Airdrie-area seat. Neither requires splitting the city four ways. Chestermere sends 86 percent of its out-commuters to Calgary, and shares a Catholic school division with Calgary, but not a public one or a transit system with the specific Calgary district the minority slices part of it into. The pairing of Red Deer with Sylvan Lake holds in part: 54 percent of Sylvan Lake’s out-commuters work in Red Deer, and one Catholic school division serves both, though their public divisions differ.',
			c11_note:
				'Checked only against the minority, because the minority is the map whose contested redraws are public. The majority did not publish a list of reasons for contested redraws, so the check cannot be applied to both sides alike; it is reported as a single flag.',
			c11_show:
				'Reasons that do not survive checking look like rationalizations: reasons found after the line, not before. In each case the evidence pointed to a boundary the minority could have drawn. The line it drew is a different one.',
			c11_experts:
				'Setting a stated reason beside what the evidence supports is pretext analysis, a test of whether the reason is a cover. It is exactly how US courts probe intent in the gerrymandering cases they do hear. Reasons that fail on public data are the standard tell.',
			c11_canada:
				'Commissions publish reasons precisely so the public can weigh them. Reasons that collapse against free, public Statistics Canada data defeat the point of publishing them.',
			c11_gun:
				'No Canadian law requires a commissioner’s reasons to survive an independent check, and a failed reason fits sloppiness as easily as pretext. Courts reviewing boundaries ask whether the outcome denies effective representation, not whether the reasoning in the file was tidy. <em>(Legal lesson 6: bad reasons for a lawful line are still a lawful line.)</em>',
			c11_app: 'how to check a stated reason against public data',
			c12_title: 'Casing 12 — The commission that couldn\u2019t sign one map',
			c12_found:
				'The commission split: two final reports, two incompatible 89-seat maps, filed the same day. The three-commissioner majority included the chair. The two-commissioner minority — the commissioners the government nominated (<a href="https://www.assembly.ab.ca/about/news-and-announcements/2025/03/28/electoral-boundaries-commission-to-soon-begin-consultations" rel="noopener">Legislative Assembly of Alberta, March 28, 2025</a>; <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/evidence/legislature/assembly_news_ebc_appointed_2025-03-28.html" rel="noopener">archived copy</a>) — produced the map every previous finding describes. Our instruments cut both ways across that divide. The majority report asserted that the minority’s changes in five places (Airdrie, Cochrane, Chestermere, Red Deer and St. Albert) had no public support in the 1,345 submissions (final report, pp. 59 and 62). We keyword-searched the full archive (93.4% machine-parsed) and found the majority right on three of the five and partly wrong on two, Chestermere and Red Deer, which drew some aligned submissions. Two configurations the majority attacked on other grounds, Rocky Mountain House–Banff Park and Olds–Three Hills–Didsbury, also had documented public support. The blanket claim is demonstrably overbroad. That finding cuts against the majority, not the minority, and it is in this log for exactly that reason. The criticism also ran the other way, and the log records that too. The minority report charges the majority with an “inclination to delete or mangle rural electoral divisions and, in effect, reduce effective rural representation” (minority report, p. 356). Our one majority-targeted structural counter-test to date asked whether the majority’s rural districts are engineered corridors of isolation. It came back supporting the innocent, geographic explanation (exploratory; the design and its limits are published). Then, the same day the charge surfaced, we counted the rural divisions themselves (exploratory; hypotheses frozen in the script before it ran; every classified name published). The count turns the charge around. Against 2019’s 31 rural-anchored divisions, the majority has 28: it absorbs three into city-named districts, merges six into three and adds three new ones. The minority has 23: it absorbs seven and merges two into one. A stricter version of the classifier gives the same order. Both maps thin rural representation relative to 2019, and that is the true core of the charge. But on the measure the accusation itself names, the minority map does more of what it accuses the majority of. The same page makes a second charge that can be measured: that the majority declined to use the Act’s ±25% flexibility in rural Alberta, a flexibility the minority insists is “not a benign allowance for errors in mapmaking” but “a deliberate instruction”. That one holds. The majority’s rural divisions average 6% below the provincial mean, with only four drawn more than 10% light. The minority’s average 12% below, with eleven drawn more than 10% light. Tested together, the two charges describe two design philosophies, not one vice: more-but-fuller rural divisions on the majority, fewer-but-lighter on the minority. Both directions of every cut are in the log.',
			c12_show:
				'A process designed to converge produced two answers, and the outlier map came from the government’s nominees.',
			c12_experts:
				'Who appointed whom is standard evidence in institutional-capture analysis. It carries weight only when the instruments are applied to both sides alike, which is why our correction of the chair matters as much as our findings against the minority.',
			c12_canada:
				'One map per commission is the norm, even when a commissioner dissents. The Act does plan for a split, but only to say whose report counts: when there is more than one, the majority’s is the commission’s report (s.9). It says nothing about a split this sharp, with the majority accusing colleagues of bad faith in the report itself.',
			c12_gun:
				'Nomination is not instruction. We found no evidence of coordination between the government and its nominees, and none can be inferred from appointment alone. Commissioners, whoever named them, have gone their own way before. <em>(Epistemic lesson: provenance raises the question; it cannot answer it.)</em>',
			c12_app: 'how commissioners are appointed and what nomination does and doesn\u2019t imply',
			ledger_h: 'Both sides, tested — the accusations ledger',
			ledger_intro:
				'Every accusation each side put in writing, run through the same tests, each result reported where it fell. This ledger is not a scorecard. Nothing in it gets added up: some rows land on the minority, some on the majority, some on the chair. The only score in this report is the five locked tests above. None of these checks was set up ahead of time the way those five were, so they carry less weight. Every number and name behind them is public.',
			ledger_col_a: 'The accusation',
			ledger_col_b: 'Who made it',
			ledger_col_c: 'Where it landed',
			ledger_r1_a: 'Three of the minority\'s boundaries are geometrically anomalous',
			ledger_r1_b: 'The chair (majority report)',
			ledger_r1_c: 'Largely confirmed — the audit\'s blind tests independently confirmed three of the chair\'s four geometric flags; the fourth fell below threshold',
			ledger_r2_a: 'The minority\'s changes in five places had \u201cno public support\u201d',
			ledger_r2_b: 'The majority (final report, pp. 59, 62)',
			ledger_r2_c: 'Overbroad — right on three of five, wrong on one, partially wrong on one',
			ledger_r3_a: 'The park extension was \u201ca bad faith effort\u201d to claim s.15(2) protection',
			ledger_r3_b: 'The chair (final report, p. 10)',
			ledger_r3_c: 'Undercut — the division qualifies under s.15(2) even without the flagged extension',
			ledger_r4_a: 'The majority \u201cdelete[s] or mangle[s] rural electoral divisions\u201d',
			ledger_r4_b: 'The minority (p. 356)',
			ledger_r4_c: 'Reversed — the minority keeps fewer rural-anchored divisions (23 vs 28, against 2019\'s 31) and absorbs more into city-named districts (7 vs 3)',
			ledger_r5_a: 'The majority \u201cdecline[d] to use\u201d the \u00b125% flexibility in rural Alberta',
			ledger_r5_b: 'The minority (p. 356)',
			ledger_r5_c: 'Supported — majority rural divisions average \u22126.0% deviation (4 below \u221210%); the minority\'s average \u221212.2% (11 below \u221210%)',
			ledger_r6_a: '\u201cSubstantial and consistent testimony\u201d for hybrids was ignored',
			ledger_r6_b: 'The minority (p. 356)',
			ledger_r6_c: 'Overbroad — support was configuration-specific: documented for three of seven hybrid configurations, absent for three',
			ledger_r7_a: 'The majority\'s rural districts are engineered corridors of isolation',
			ledger_r7_b: 'The audit\'s own counter-hypothesis (T3.2)',
			ledger_r7_c: 'Not supported — the geographic explanation held; the majority cleared',
			ledger_close:
				'Neither side\'s accusations survived intact, and neither side\'s map escaped a hit. On the floor of the legislature, no one criticized the majority report at all. The government wrapped its motion in the majority chair\'s own recommendation; the opposition demanded the report\'s adoption. The written charges against the majority exist only in the minority\'s own pages. That is why we had to test them ourselves.',
			c13_title: 'Casing 13 — When the process might have answered, it was replaced',
			c13_found:
				"The commission held hearings in sixteen communities, received 1,345 written submissions, and after 80-plus of them reversed its plan to remove Lesser Slave Lake: a system visibly responding to what the public said. Four weeks after its split reports arrived, that system was replaced. Government Motion 37, introduced April 16 and passed April 21, 2026, set both reports aside. It created a Select Special Committee of six MLAs — four UCP, two NDP, chaired by UCP MLA Brandon Lunty — to oversee a 91-seat map, which it had to send to the Assembly by November 2, 2026 (<a href=\"https://www.assembly.ab.ca/assembly-business/committees/ceb\" rel=\"noopener\">committee page</a>). The committee was not required to hold public hearings, and, as <a href=\"https://www.cbc.ca/news/canada/edmonton/alberta-boundaries-committee-motion-9.7172743\" rel=\"noopener\">CBC reported</a> it would, it held none on the map. No draft was released for public challenge. The map was drawn by an Independent Advisory Panel, <a href=\"https://www.cbc.ca/news/canada/edmonton/alberta-boundaries-panel-legislative-committee-elections-9.7187435\" rel=\"noopener\">chaired by retired Court of Appeal justice Brian O’Ferrall</a>, which reported on October 22; the panel itself split. On October 28 the committee voted 3–2 to end its review without observations. The Assembly decides whether the map becomes law. On the floor, the government presented the takeover as faithfulness to the commission — “We are adopting the recommendations from the report” (Government House Leader, Hansard, April 16, 2026) — while the opposition described the same motion as presenting the “minority report in slow motion.” Against the majority report itself, that claim of faithfulness reads narrower. The majority did say two more seats would have given more effective representation (p. 58), and Recommendation 5 itself calls for an all-party select committee (p. 66). But the majority asked the Legislature to adopt its 89-seat map. Its own seat-count fix was aimed at future commissions. And the one recommendation that did propose 91 seats now was the chair’s alone: “My majority colleagues do not agree with me on this point.”",
			c13_show:
				'When the independent route failed to deliver a usable answer, the government took the pen. And the vehicle it chose removed every mechanism by which the public could contest what it writes before it becomes law.',
			c13_experts:
				'The design gives up two transparency features the redistricting research treats as protective: published drafts and public hearings. Its panel is built like the commission, two nominees from each side and a retired judge as chair, but a committee with a government majority oversees it, and MLAs send the result to the Assembly. Civil-liberties observers (<a href="https://ccla.org/press-release/ccla-sounds-the-alarm-over-the-politicization-of-albertas-electoral-map/" rel="noopener">CCLA</a>) raised the concern about politicization independently of this audit.',
			c13_canada:
				"The norm at stake is the deepest in modern Canadian redistribution: politicians do not draw their own districts. When MLAs last drew Alberta’s map, in 1992 (finding 14), the Court of Appeal let it stand in 1994 (secondary accounts say it faulted the committee for being unable to explain several of its boundaries; we have not read the judgment), and in 1995 the Act was amended to change how commissions are appointed. Our November tests (on the main page) measure the committee’s process against exactly the features it is not required to provide.",
			c13_gun:
				'Every step is lawful. The Act makes the commission\u2019s reports advisory. It sets no minimum notice or comment period, and it imposes no hearing or draft-release requirement on what follows. Under parliamentary sovereignty the legislature may lawfully do precisely what it did. <em>(Legal lesson 7: the process that could have created accountability is optional — and opting out is legal.)</em>',
			c13_app: 'the Act\u2019s process from commission to committee, end to end',
			c14_title: 'Casing 14 — The sixty-year norm, set aside in an afternoon',
			c14_found:
				"Canada spent roughly sixty years building independent boundary commissions. They were the institutional answer, since the federal reform era of the 1960s, to the once-routine practice of governing parties drawing their own ridings. In May, Duane Bratt, Professor of Political Science at Mount Royal University, described the process to the author as without precedent in Canada. That stands. Alberta handed a map to MLAs once before, in 1992, but that commission had deadlocked: five commissioners, five reports, no majority. In 2026 the commission did not deadlock. A majority signed a report, which the Act treats as the commission’s report, and it was set aside anyway. In some jurisdictions a commission’s map takes effect unless the legislature overrides it. In Alberta, it takes a bill.",
			c14_show:
				'The opposition named the move on the floor: “retaliation against the independent Electoral [Boundaries Commission].” The injury is not one map. It is the demonstration that the guardrail was a convention, a habit and not a law — and conventions bind only governments that consent to be bound. Nothing prevents the next government, of any party, from citing this cycle as precedent.',
			c14_experts:
				'Research comparing jurisdictions treats independent commissions as the single most protective institutional feature against gerrymandering. Removing the institution matters more than any one boundary it might have drawn.',
			c14_canada:
				"The federal process and the provinces use arm’s-length commissions, with exceptions: Alberta in 1992, and Quebec, whose National Assembly legislated its own 127-seat map in June 2026 after the Supreme Court struck down its pause of the commission. Alberta’s 2026 cycle departed from that standard by simple majority vote.",
			c14_gun:
				"Constitutional conventions bind politically, but courts will not enforce them; the Supreme Court said as much in the 1981 Patriation Reference. That does not put the process beyond the courts’ reach. In 2017 Nova Scotia’s Court of Appeal found a map unconstitutional because the government had stifled its commission’s independent view. In 2026 the Supreme Court struck down Quebec’s law pausing its commission (<em>Quebec (AG) v. Lalande</em>, 2026 SCC 13). What a court reviews is the enacted map, under section 3. <em>(Legal lesson 8: norms are not law, but how a map is made can still matter in court.)</em>",
			c14_app: 'conventions versus law, and how norms erode',
			rev_h: 'The Scorecard, Revisited',
			rev_p1:
				'Fourteen casings. No gun. Now go back to the picture from the top of this page — you can read it now.',
			rev_p2:
				'The horizontal axis is one of Act II’s four fairness measures: the efficiency gap, more UCP-favoured the further right you go. The vertical axis is Act I’s count of discriminating structural tests failed, the tests that tell the maps apart. The 2019 map and the 2026 majority sit in the quiet corner: near-zero skew, zero structural flags. The minority sits alone. Four of four structural flags. An efficiency gap just under the line we set in advance. And, off this chart’s axes, a tied-vote seat count that only 69 of 1,010,000 neutral maps exceed, and a 60-of-89 seat outcome on recent voting patterns. The two acts converge on the same map and the same communities. The specific claim that the geometry is the mechanism failed its test (Casing 9), yet both acts still agree on who benefits.',
			rev_litany_intro: 'Now run this instrument itself through the same five questions, one last time.',
			rev_found:
				'A scorecard: the best instrument I could build to draw fourteen casings together into something that can be stated, checked, and falsified. Five pre-registered structural tests: the minority crosses every discriminating one, the majority none, the fifth, which does not tell them apart, on display. Four partisan-fairness metrics against 1,010,000 neutral maps: three in the extreme tail, one reported miss.',
			rev_show:
				'The closest thing to a gerrymandering signal that can exist under Alberta law and Canadian norms: a checkable way of saying \u201cthis map is the kind of map that aiming produces,\u201d with every threshold set before any answer was known.',
			rev_experts:
				'When intent cannot be seen, the field reads maps with combined batteries of outlier tests. Pre-registration is what keeps them honest.',
			rev_canada:
				'Nothing. No Canadian institution scores maps this way. That is exactly why we had to build one.',
			rev_gun:
				'Its thresholds are our own calibrations, not legal lines. Alberta is one province with one split commission: a sample size of one. And no pile of casings ever becomes a gun, because the gap between \u201cextreme\u201d and \u201cdeliberate\u201d is not statistical. It is the gap the law chose to leave open.',
			rev_refrain: 'A casing, not a gun. But this casing fires again in November.',
			playbook_h: 'What running the play again would look like',
			playbook_p1:
				'This report cannot prove a gerrymander; the word has no legal home here. What it can do is say, in advance and in public, exactly what the signature looks like, and then say whether the November map carries it. Our November tests were registered (OSF, registration qsgy8) before the committee\u2019s map existed. The registration\u2019s own name for the check is the Lunty test, and it is the confirmatory counterpart to everything above. The signature has two halves. Process: were public hearings held; was a draft released; are the advisory panel\u2019s members and terms of reference published; does the map honour the recommendation the government cited when it took the pen? Outcome: where the map lands on every metric in this report, against the same million-map distribution, under the same pre-registered thresholds.',
			playbook_p2:
				'Suppose the committee\u2019s map repeats the minority\u2019s signature, though drawn by different people, under different constraints, on a different timeline. Then the structural finding above earns confirmatory status. If it lands inside the neutral bands, the finding stands as an isolated observation about one map that was never enacted, and this report will say exactly that. The scoring runs within 72 hours of the map\u2019s release, whichever way it points. That commitment was registered before anyone knew the answer. Pass or fail, you will not have to trust our judgment. Only our arithmetic, which is public, seeded from a public beacon, and reproducible by anyone.',
			appendices_note:
				'Every casing above links to a lettered explainer — one concept each, from \u201cthis is confusing\u201d to \u201cnow I understand\u201d — on the companion page:',
			appendices_link: 'The fourteen explainers (Appendices A–N)'
		},
		authors_view: {
			heading: "The Author's View",
			heading_aria: "Link to the author's view",
			preamble:
				'Everything else on this page is the audit. Pre-registered tests. Documented corrections. Evidence you can check without trusting me. Delete this section and not one number changes. This section is not a finding. It is an opinion — signed, severable, and mine.',
			p1: 'The audit cannot prove intent. I have kept that discipline on every page above. This page is where I set it down.',
			p2: 'Start with the two facts I cannot make innocent. Government-nominated commissioners drew a map that neutral map-drawing almost never produces — fewer than a hundred matches in a million draws. And when the commission split rather than endorse it, the government did not ask why. It took the pen.',
			p3: 'Each fact has an innocent reading. A commissioner can be eccentric in good faith. A legislature can lose patience with deadlock. But put the facts in sequence and the innocent readings strain. A government wanted a certain kind of map. The independent route did not deliver one. A route was found that would.',
			p4: 'Here is what alarms me. It is not that a law was broken. No law was broken — I checked, and that checking is most of what this audit is. The statute makes the commission’s report advisory. It sets no notice period. It requires no draft, no hearings, no consultation. Every step of the takeover was legal. That is the alarm. The guardrail was never law. It was a habit — and habits only bind governments that choose to keep them.',
			p5: 'Look at what the habit used to buy. The commission held hearings in sixteen communities. It read 1,345 written submissions. It changed its mind in public, because the public gave it reasons to. The committee that replaced it is six MLAs: four government, two opposition, government chair. No rule required an independent voice at that table, and none sits there. There is an advisory panel — chaired, to its credit, by a retired judge. But advisers advise. The votes belong to the MLAs, and the map they draw is the map they will run in. It will face no public hearing. No draft will be released for the public to contest. It arrives finished.',
			p6: 'And this government has been here before. Its first bill, as written, would have let cabinet rewrite laws without the legislature. That power was stripped — after the outcry, not before. Its own ethics commissioner found the Premier breached the conflicts law by pressing her attorney general about a criminal case, and called interference with the administration of justice “a threat to democracy.” It passed a law letting cabinet repeal local bylaws and trigger the removal of elected councillors. And when a court paused one of its laws in December 2025, it invoked the notwithstanding clause; within a week the injunction was gone. Every one of those moves was lawful. Every one spent a norm to get past an independent check. Redrawing the electoral map through a committee the government controls is not a departure. It is the pattern, applied to elections.',
			p7: 'Political scientists have names for governments that keep the letter of the law while hollowing out the norms beneath it. The gentlest is <em>democratic backsliding</em>. The literature is blunt about how it works. Democracies rarely die of coups anymore. They die of this — one lawful, norm-breaking step at a time, each with a plausible reason, none of them illegal.',
			p8: 'Canada spent sixty years building one norm above the rest: politicians do not draw their own districts. Voters choose their representatives. Not the reverse. In April 2026, Alberta set that norm aside in an afternoon, by a vote of 44 to 36.',
			p9: 'I worry about what the map buys. On recent voting patterns, the minority map’s geometry yields sixty seats of eighty-nine. That is not a mandate. It is insulation — from floor-crossings, from committees, from any opposition large enough to sustain scrutiny. I would worry about that insulation in any hands. I worry more in the hands of a government that has just shown me, in this very file, what it does with procedural control when a process threatens to answer back.',
			p10: 'I could be wrong. Unlike most opinions about this government, mine ships with the terms of its own destruction. The committee’s map is due November 2. The tests were locked before it existed. Were hearings held. Are the advisers named, their terms of reference published. Does the map honour the recommendation used to justify the takeover. Where does it land against a million neutral maps. If it lands inside the neutral bands, my suspicion took real damage — and this site will say so within seventy-two hours, because I committed to that before I knew the answer. That is the difference between an opinion and an accusation. An opinion tells you what would change it.',
			signed: '— Will Conner',
			sources:
				'<em>Sources for this section.</em> The ethics finding is from the Ethics Commissioner’s report, <a href="https://www.ethicscommissioner.ab.ca/media/3124/allegations-involving-premier-danielle-smith-may-17-2023.pdf" rel="noopener">Allegations Involving Premier Danielle Smith (May 17, 2023)</a>: “In my opinion, Premier Smith contravened s.3 of the Conflicts of Interest Act in her interaction with the Minister of Justice and Attorney General.” The Sovereignty Act’s original cabinet powers and their removal: <a href="https://www.cbc.ca/news/canada/edmonton/alberta-sovereignty-act-1.6678407" rel="noopener">CBC, December 2022</a>. Bill 20’s cabinet powers over councillors and bylaws: <a href="https://www.cbc.ca/news/canada/edmonton/alberta-bill-gives-cabinet-power-to-remove-municipal-councillors-change-or-repeal-bylaws-1.7185346" rel="noopener">CBC, April 2024</a> and the <a href="https://rmalberta.com/wp-content/uploads/2025/10/Bill-20-Member-Resource-Branded.pdf" rel="noopener">RMA analysis of the act as passed</a>. The notwithstanding-clause invocation and the injunction’s end: <a href="https://www.cbc.ca/news/canada/edmonton/alberta-government-notwithstanding-clause-bills-9.6983786" rel="noopener">CBC, December 2025</a> and <a href="https://egale.ca/awareness/egale-v-alberta-healthcare/" rel="noopener">Egale Canada’s case timeline</a>. The committee’s structure, the advisory panel, and its judicial chair: <a href="https://www.cbc.ca/news/canada/edmonton/alberta-boundaries-committee-motion-9.7172743" rel="noopener">CBC, April 2026</a> and <a href="https://www.cbc.ca/news/canada/edmonton/alberta-boundaries-panel-legislative-committee-elections-9.7187435" rel="noopener">CBC, May 2026</a>; the commission’s sixteen-community hearings and 1,345 written submissions are from its final report (p. 14). The committee’s creation (Government Motion 37, passed April 21, 2026) and its six members: the <a href="https://www.assembly.ab.ca/assembly-business/committees/ceb" rel="noopener">Legislative Assembly’s committee page</a>. The acting chief justice’s refusal: <a href="https://bowislandcommentator.com/news/2026/05/28/chief-justice-cites-integrity-issues-refuses-to-suggest-electoral-boundaries-chair/" rel="noopener">Southern Alberta Newspapers, May 2026</a>. The 1992 committee and the 1995 amendment: <a href="https://albertaviews.ca/knowing-draw-line/" rel="noopener">Alberta Views</a> and <a href="https://docs.assembly.ab.ca/LADDAR_files/docs/bills/bill/legislature_23/session_3/19950213_bill-020.pdf" rel="noopener">Bill 20 (1995)</a>. The ensemble and seat figures are this audit’s own, sourced throughout the report above.'
		},
		references: {
			heading: 'References and Methodology',
			heading_aria: 'Link to references',
			intro:
				'The method draws on established literature in political science, statistics and law. Full citations follow American Political Science Association (APSA) style; court cases follow Canadian legal convention. The complete reference list is in the <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">technical report</a>. The key sources are here.',
			h_academic: 'Academic literature',
			h_cases: 'Court cases',
			h_statutes: 'Statutes'
		},
		resources: {
			heading: 'Reports and code',
			heading_aria: 'Link to technical',
			tag_plain: 'Plain Language',
			plain_label: 'Full public report',
			plain_desc: 'Long-form, with maps, for general readers',
			tag_summary: 'Summary',
			summary_label: 'Summary of findings',
			summary_desc: 'Plain-language overview that explains every concept from scratch',
			tag_academic: 'Academic',
			academic_label: 'Technical report',
			academic_desc: 'Full methods and citations for researchers',
			tag_notebook: 'Notebook',
			notebook_label: 'Interactive notebook',
			notebook_desc: 'Run the charts yourself, in your browser, with nothing to install',
			tag_code: 'Code'
		},
		about_me: {
			heading: 'About me',
			p1: "I'm a student at Mount Royal University. I did this research on my own: it was not assigned as coursework, and the university did not commission it. My views are my own and do not represent the university. I've worked as a contract election officer for Elections Alberta for about 27 years, election by election, administering the vote on election day. I'm not under contract now; I last worked at a recent election. I've had no other employment with Elections Alberta and have no knowledge of its work beyond those tasks. Nothing in this audit comes from that work; every input is public. This research is my own, not Elections Alberta's, and does not speak for it. I have no connection to the commission. I've voted for and donated to both conservative and progressive provincial parties in Alberta as an adult.",
			p2: "My political history could affect how I look at this issue, and the main protection against that is the method. I tested both maps the same way, registered my tests in public, time-stamped records, labelled every finding pre-registered or exploratory, and put everything online so anyone can check my work. I paid for this research myself. If you find something I got wrong, I want to know.",
			p3: 'Seed-commitment and pre-registration records: <a href="https://osf.io/6pt83" rel="noopener">OSF:6pt83</a>, AsPredicted:#289,469, AsPredicted:#289,451 — the random seeds come from a public beacon and were fixed in the code on April 27, 2026, before the official shapefiles arrived (the record is a repository commit, not an OSF registration); the neighbour-drain test (#289,451) was specified on April 24 and registered on the OSF on May 6, after a provisional pass on approximate boundaries; the others were filed alongside exploratory analysis.',
			p4: 'Questions or corrections: '
		},
		translation_about: {
			heading: 'About this translation',
			p1: 'You are reading an AI translation. Anthropic\u2019s Fable 5 model produced it, and it is still awaiting review by a native speaker. The English version is the authoritative text: if anything in this translation is unclear or seems wrong, the English original governs.',
			p2: 'Translation quality matters here in a way it doesn\u2019t on most websites. This audit makes statistical claims about electoral fairness, and a mistranslated number or a wrongly hedged sentence misleads in ways a reader will find hard to detect. Machine translation of civic-statistical prose is genuinely difficult. Errors are likely.',
			p3: 'If you are a native speaker and you spot an error \u2014 or you\u2019d like to review a section properly \u2014 please %s. For scale: the English prose runs about {count} words. You are welcome to take on all of it, or just a portion. In most cases the work is correcting minor errors the machine made, not translating from scratch, and even reviewing a single section helps.',
			p3_link: 'get in touch'
		},
		retractions: {
			heading: 'Retractions and Corrections',
			heading_aria: 'Link to retractions',
			conditions_label: 'RETRACTION CONDITIONS',
			conditions_intro:
				'Every finding is pre-committed to a specific falsification condition. If any condition below materialises, the finding it names is retracted publicly within 30 days. The overall directional conclusion — that the minority map sits outside the neutral range on multiple independent tests — is retracted under the methodology\'s pre-committed compound condition: at least three of the six independent structural dimensions reversing direction.',
			c1_title: 'Condition 1 — The trade-off is shown to be forced',
			c1_what: "<em>What gets retracted:</em> The structural finding that the Airdrie four-way split and the three chair-flagged boundaries cannot be explained by the minority's stated community-of-interest rationale.",
			c1_cond:
				"Condition: someone shows that no legal Alberta map can satisfy the minority's own stated reasons — Airdrie, Cochrane, Nolan Hill, Rocky Mountain House–Banff Park — while anchoring on municipal lines at majority-comparable rates. A counter-map that does both would strengthen the finding instead (Amendment 5, Part 22). On the official boundaries this condition is moot: both maps already anchor on municipal lines above its 60% bar (minority 71.8%, majority 80.0%). Open challenge at <a href=\"https://github.com/Ixby/alberta-electoral-boundaries-audit/issues/14\" rel=\"noopener\">Issue #14</a>.",
			c2_title: 'Condition 2 — The Neighbour-Drain pre-registered pass is reversed',
			c2_what: '<em>What gets retracted:</em> The Casing 10 entry recording the minority map as a pre-registered PASS on the neighbour-drain adjacency test.',
			c2_cond:
				'Condition: the v2 continuous drain score falls in the extreme upper tail (p &lt; 0.05) of random permutations across the fixed contiguity graph, meaning the pass was a measurement artefact of the v1 binary scoring method rather than a genuine null result.',
			c3_title: 'Condition 3 — A pre-2026 commission document surfaces',
			c3_what: "<em>What gets retracted:</em> The inference that the minority's boundary choices were drafting decisions rather than responses to documented community submissions.",
			c3_cond:
				"Condition: an internal commission document dated before the minority's final boundary choices shows those choices were explicitly driven by community submissions the audit has not seen — not by the six published sub-rationales the audit tested.",
			c4_title: 'Condition 4 — The 2027 election result contradicts the simulation',
			c4_what: "<em>What gets retracted:</em> The simulation finding — that at a tied vote the minority map awards a seat share only 69 of 1,010,000 neutral draws exceed.",
			c4_cond:
				'Condition: if the 2027 provincial election is fought on either commission map and the actual partisan seat split contradicts the directional projection from 2023 votes, the simulation\'s percentile findings are revisited against actual results.',
			c5_title: 'Condition 5 — An Alberta court distinguishes the Quebec SCC ruling',
			c5_what: '<em>What gets retracted:</em> The procedural argument in the Lunty Committee section that Government Motion 37, which replaced the commission with the Lunty committee, sits in the same constitutional class as Quebec\'s 2024 redistricting freeze.',
			c5_cond:
				"Background: on April 22, 2026 — the day after Alberta passed Government Motion 37 — the Supreme Court of Canada upheld, 7–2 and from the bench, a Quebec Court of Appeal ruling that the Legault government's legislative freeze on its redistricting commission violated the Charter's s.3 democratic-representation guarantee. Condition: a court reviewing the Alberta motion finds it constitutionally distinct — for example, because reassigning the work to an MLA committee differs structurally from a legislative freeze, or because Alberta's effective-representation analysis under s.3 comes out differently than Quebec's.",
			corr_label: 'DOCUMENTED CORRECTIONS (canonical recomputation, 2026-05-11)',
			corr_light_label: 'CORRECTIONS',
			corr_light_intro:
				'This audit corrects in public and deletes nothing. The structural test that changed on the official boundaries is told in full at Casing 5; the two statistical tests that did not hold up, at Casings 8 and 10. The complete ledger of every correction — what changed, when, and why — is kept in the <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">academic report\u2019s DOCUMENTED CORRECTIONS section</a>.',
			corr_intro:
				"The following early finding did not survive reanalysis against official Elections Alberta shapefiles (received 2026-05-06). It is retained here per the audit's pre-committed policy of never deleting failed findings.",
			corr_municipal:
				"<strong>Municipal anchoring.</strong> Early draft analysis using provisional map boundaries showed the minority map anchored to municipal lines only 15% of the time — 4.9&times; below the 70–85% Canadian norm. This figure was an artefact of the provisional (DPG-era) boundary reconstructions. On official Elections Alberta canonical shapefiles, both maps anchor within the Canadian norm: majority 80%, minority 72%. The municipal-anchoring <em>divergence</em> between the two maps is not a signal that survives canonical recomputation. The three boundary anomalies flagged by the commission chair (Rocky Mountain House–Banff Park, Nolan Hill–Cochrane, Olds–North Airdrie) remain and are not affected by this correction."
		},
		suggestions: {
			heading: 'Suggestions',
			heading_aria: 'Link to suggestions',
			resume:
				'The opinion is over; the log resumes. Three pieces of housekeeping remain: what would make the next audit easier, the conditions under which this one retracts itself, and the paper trail.',
			intro:
				"This audit ran into two data problems that have nothing to do with the commission's work and everything to do with how Alberta's electoral system is designed. Both are fixable.",
			advance_p1:
				"<strong>About half of all Alberta votes now arrive before election day</strong>: advance polls, mobile polls, special ballots. Elections Alberta reports these results as totals for each electoral division, not by specific Voting Area. So roughly 810,000 NDP and UCP votes cast in 2023 cannot be pinned to any neighbourhood on a map. They are counted. They just can't be located. Every advance voter is checked against a voters list before receiving a ballot, and that list links each voter to a specific Voting Area. Publishing advance-vote totals by Voting Area would mean sorting advance ballots by area at the count, combining small areas to protect secrecy: a change to counting, not to how people vote.",
			advance_p2:
				"This matters most to people auditing a map. Commissions rightly draw from population, not votes, and the census already tells them where people live. But turnout by area would show which communities a map's districts actually reach, and as far as the public record shows, commissioners see the same published results as everyone else.",
			lesser_slave_p1:
				'In at least one community in northern Alberta, this gap is total. In the northern part of the Lesser Slave Lake <button class="ed-trigger" data-ed-name="Lesser Slave Lake">show ↗</button> division sits a Voting Area covering 4,832 km&#178; — more than four-fifths the size of Prince Edward Island, home to 844 people at the 2021 census — where no vote in 2023 was cast at an election-day poll: every vote went into the division-wide advance, mobile or special-ballot totals. Those votes are counted in the divisional total, but they cannot be pinned to any location on a map. In the published election results, the community is entirely invisible.',
			lesser_slave_p2:
				'When the commission first considered eliminating the Lesser Slave Lake division and merging it into a larger riding, it was working without geographic vote data from those communities. In the end it preserved the division. That came after 80+ public submissions, many from the Indigenous communities in the northern part of the riding, and it invoked s. 15(2) of the <em>Electoral Boundaries Commission Act</em>, the protection for remote ridings set out below. They got there. But the published results couldn\'t show how many people in those communities voted.',
			ebca_label: 'SECTION 15(2) EBCA',
			ebca_body:
				"Section 15(2) of Alberta's <em>Electoral Boundaries Commission Act</em> is a discretionary provision that allows commissions to protect undersize ridings — those more than 25% below the provincial population average — when the riding meets at least three of five specific criteria: (a) an area over 20,000 km², or a surveyed area over 15,000 km², (b) a distance of more than 150 km from the Legislature Building to the riding's nearest boundary by the most direct highway route, (c) absence of any town with more than 8,000 residents, (d) presence of an Indian reserve or a Métis settlement, and (e) part of the riding's boundary running along a boundary of the Province of Alberta. Up to four ridings may be protected this way, to as much as 50% below the average. The provision is not automatic; the commission must judge whether the criteria are met.",
			rationale_p1:
				"The interim rationale for eliminating the riding was population. At roughly 27,000 residents, Lesser Slave Lake had barely half the provincial average population: right at the legal floor. That reads like a straightforward application of the rules. It isn't. The law gives commissions discretion here, and Lesser Slave Lake meets four of the five criteria independently. Its area is 69,566 km² (criterion a, threshold 20,000 km²). Its nearest boundary is more than 150 km from the Legislature by highway (criterion b). No town in the riding has a population over 8,000 (criterion c). And the riding contains fourteen Indian reserves and M&#233;tis settlements whose communities share a common northern geography and a collective interest in having a representative primarily accountable to northern Alberta (criterion d).",
			rationale_p2:
				"Under the interim plan, which merged Lesser Slave Lake with Peace River into one riding called Mackenzie, that collective voice would have been folded into the largest riding in the province. Not because those communities changed. Because the lines around them did. Each of those four criteria is an objective fact about the riding's geography, not a judgment call. Together they describe a constituency the provision was written to protect: remote, large, sparsely populated, and home to communities whose interest in representation cannot be read from raw population numbers. You need three to qualify. Lesser Slave Lake has four. The shortfall did not force elimination. Section 15(2) let the commission keep the riding once it added people: the final report brought in Big Lakes County, Swan Hills and part of Woodlands County, lifting it to 45% below the average. The commission's own words for its first plan: \"we erred.\"",
			banff_p:
				'Here is the other side of the story. All five commissioners agreed to the interim plan that removed Lesser Slave Lake, and both final maps protected it under s.&#x2009;15(2). The minority also used s.&#x2009;15(2) for Rocky Mountain House–Banff Park, which it extended into the uninhabited part of Banff National Park. The commission\'s majority, its own chair among them, called that "a bad faith effort" to claim the legal protection; the phrase is in the commission\'s official final report. The audit\'s check undercuts that charge: the division qualifies under s.&#x2009;15(2) even without the extension. Still, in the minority\'s map, a protection written for remote communities where people live was stretched over empty parkland. The 91-seat map that followed was drafted by an advisory panel under the Lunty committee. Section&#x2009;15(2) binds the commission; it bound the panel only if Government Motion 37 adopted it. No statute required public hearings on that map, and none were held.',
			census_p1:
				"<strong>The other problem is timing. Alberta should wait for the 2026 census before drawing the next map.</strong> Canada counts its population every five years. The 2026 census was taken in May 2026, and its first results are due in February 2027. The commission that drew the maps assessed in this audit had to start from the 2021 census, updated to a July 2024 provincial estimate: a count already four years old when the maps were drawn, and potentially fourteen years old by the time those boundaries retire. Fast-growing cities like Airdrie and Chestermere will change by 40% or more over that window. Rural communities will shrink. The map will be wrong from the day it is used. A straightforward change to the <em>Electoral Boundaries Commission Act</em> could require that any new commission be appointed only after Statistics Canada releases the most current dissemination-area data from the preceding census. The result: maps that reflect where Albertans actually live. Not where they lived a decade ago.",
			census_p2:
				'The Lunty committee worked under the existing statute, which sets no census-timing requirement, and it could not delay past its November 2, 2026 deadline on its own. This recommendation applies to a future amendment to the <em>Electoral Boundaries Commission Act</em>, not to the current process. The tension is real. The 91-seat map was drawn from a census five years old by the time it was delivered. Naming the constraint is more useful than pretending it does not exist.',
			closing:
				"Neither data problem is a finding about the current commission's maps. They are observations about a system that makes accurate electoral analysis harder than it needs to be, offered here as practical suggestions, not conclusions. Both are genuinely fixable. Fixing them would put every future commission, and every future audit, on better ground."
		}
	},
	editorial_canada: {
		heading: 'Context: Canada is different — and similar',
		p1: 'Canada belongs to the same family as the U.S., the U.K., and Australia. We elect single members from geographic districts under first-past-the-post. We redraw the lines periodically — federally after each decennial census, provincially on staggered schedules. We inherited the basic machinery from the same Westminster roots. So far, no surprises.',
		p2: 'What sets Canada apart is the test the lines have to pass.',
		p3: 'In American constitutional law, the binding rule is <em>one person, one vote</em> — districts must have populations as nearly equal as practicable, and large departures require strict justification. In Canadian constitutional law, the binding rule is different. Section 3 of the <em>Canadian Charter of Rights and Freedoms</em> guarantees every citizen the right to vote. In <em>Reference re Provincial Electoral Boundaries (Sask.)</em> — the 1991 Saskatchewan Reference, the leading case — the Supreme Court of Canada interpreted the right as a right to <em>effective representation</em>, not a right to mathematical equality of district populations.',
		p4: "That distinction matters. Effective representation allows district populations to vary, sometimes substantially, when there are good reasons: vast rural geographies one MLA cannot reasonably serve at standard population density, communities of interest that should be kept together, minority representation that mathematical equality would dilute. The Saskatchewan Reference made that flexibility constitutional. The EBCA's 25% population variance — the rule that protects rural Alberta seats — flows directly from it.",
		p5: 'The catch is that flexibility cuts both ways. If a commission can legitimately depart from population equality for the right reasons, it can also depart from population equality for the wrong ones. Canadian law has no American-style mathematical floor to fall back on. It has the effective-representation test, applied by judges, after the fact, in litigation. Most jurisdictions guard against the wrong reasons with structural protections: federally, redistribution commissions are insulated by statute and their boundaries take effect through a representation order, without a parliamentary vote to adopt them. Quebec goes furthest — its permanent independent commission establishes the final map itself, with no Assembly vote to adopt or override it. Even British Columbia, whose Legislative Assembly does vote to approve the commission\'s proposals and enact them in legislation, treats adopting the independent commission\'s work as the norm rather than substituting a map of its own.',
		p6: 'Alberta is the exception. Under the <em>Electoral Boundaries Commission Act</em>, the commission\'s report is a recommendation only — the legislature must vote to enact it. Approval is normally a formality. In the 2026 cycle, the commission split 3–2 and produced two competing proposals; the legislature created a separate MLA committee, chaired by a UCP MLA, to choose between them. Nothing in Canadian constitutional law required the committee to exist. Nothing requires its choice to follow the commission\'s process. This is the structural gap this audit is examining.',
		p7: 'So when Canadian courts say "gerrymander" isn\'t their legal vocabulary, they are not saying the underlying concept does not apply here. They are saying the test is different — effective representation, not mathematical equality. Whether the minority proposal meets that test is exactly the question this audit has measured the geometry against, and exactly the question only a judge can answer definitively. The <em>Saskatchewan Reference</em> reasoning in full, the contrast with other provinces, the standing question, and the available reform pathways are treated in <a href="#references">the references section below</a>.'
	},
	chrome: {
		back_to_top: 'Back to top',
		license_title: 'Creative Commons Attribution-NonCommercial-ShareAlike 4.0',
		license_alt: 'CC BY-NC-SA 4.0',
		license_aria: 'Creative Commons BY-NC-SA 4.0',
		back_to_stakes: '↑ Back to Stakes',
		back_to_picture: '↑ Back to the picture',
		lightbox: {
			fig_aria: 'Figure enlarged view',
			fig_close_aria: 'Close enlarged figure (Esc)',
			map_aria: 'Map zoom viewer',
			map_close_aria: 'Close map viewer',
			close_title: 'Close (Esc)'
		},
		participation: {
			heading: 'Help us refine MapExplorer',
			body:
				"As you explore, we track which maps and districts you visit and periodically send the data to our research database. Sharing a view also saves where you ended up. The goal: understand what's useful and make the tool better.",
			no_collect:
				"We never collect your name, IP address, or precise location. Everything is anonymized in your browser before it leaves. We couldn't identify you from the data even if ordered to.",
			dnt:
				'Your browser has Do Not Track enabled. No is pre-selected on your behalf. You can still choose Yes.',
			no_thanks: 'No thanks',
			yes_help: "Yes, I'll help",
			privacy_policy: 'Privacy policy'
		},
		share: {
			button: 'Share',
			button_title: 'Share or load a map configuration',
			dialog_aria: 'Share map configuration',
			close_aria: 'Close share panel',
			share_label: 'Share this configuration',
			share_hint:
				'Type this code into any browser running the audit to load this configuration. The code is never placed in a URL.',
			load_label: 'Load a configuration',
			load_btn: 'Load',
			load_placeholder: 'alpine-eagle-banff',
			copy: 'Copy',
			copied: 'Copied!',
			copy_failed: 'Failed',
			unrecognised: 'Unrecognised code — check spelling.'
		},
		map: {
			minority: 'Minority',
			majority: 'Majority',
			current: 'Current',
			wasted: 'Wasted',
			wasted_title: 'Efficiency-gap contribution per district',
			partisan: 'Partisan',
			partisan_title:
				'Colour each district by partisan outcome (UCP blue / NDP orange)',
			borders: 'Borders',
			flagged: 'Flagged',
			flagged_title:
				'All 7 configurations flagged by commission chair Justice Miller — switches to minority map automatically',
			help_aria: 'Map help',
			help_title: 'How to use the map',
			pin_aria: 'Pin Map',
			pin_title: 'Pin Map — prevent auto-pan on district click',
			search_aria: 'Find an electoral district',
			search_placeholder: 'Find district…',
			zoom_aria: 'Map zoom',
			clear_aria: 'Clear district selection',
			clear_title: 'Clear selection',
			va_hint: 'Click within this district to see polling station results',
			va_close_aria: 'Close polling station detail',
			va_close_title: 'Close',
			object_title: 'Alberta electoral district map — full resolution',
			ea_credit: 'Map data:',
			cc_title: 'Text content: CC BY-NC-SA 4.0',
			cc_alt: 'Creative Commons BY-NC-SA 4.0',
			// Engine-internal strings (callouts, errors, loading) — injected into
			// the framework-free map engine via setEngineStrings() at init and on
			// every language switch.
			votes_suffix: 'votes',
			total_votes_suffix: 'total votes',
			pop_prefix: 'Pop.',
			voting_areas_suffix: 'voting areas',
			other_maps: 'Other maps',
			unique_boundary: 'Boundary unique to this map',
			in_person_votes: 'in-person votes (excl. Vote Anywhere)',
			load_error_generic: 'Could not load the boundary map. Try reloading the page.',
			load_error_map: 'Could not load the {key} map — check your connection.',
			context_minority: '2026 minority proposal · 2023 election results',
			context_majority: '2026 majority proposal · 2023 election results',
			context_2019: '2019 enacted boundaries · 2023 election results',
			tag_min: 'Min',
			tag_maj: 'Maj',
			tag_2019: '2019',
			dev_notice:
				'Map Explorer is under continuous live development and may sometimes break. If something looks wrong, come back in a few days — the issue will likely be resolved. Suggestions are welcome: %s.',
			dev_notice_email_label: 'email me',
			dev_notice_dismiss: 'Dismiss development notice',
			skel_1: 'Loading Map Explorer…',
			skel_2: 'drawing Alberta…',
			skel_3: 'crunching the numbers…',
			skel_4: 'counting every vote…',
			skel_5: 'plotting the boundaries…',
			skel_6: 'almost there…'
		},
		map_intro: {
			heading: 'How to use the map',
			click_district: 'Click any district',
			click_district_desc: 'see 2023 election results and snap to it',
			click_within: 'Click within a selected district',
			click_within_desc:
				'see individual polling station results (colour = vote split)',
			dblclick: 'Double-click a district',
			dblclick_desc:
				'zoom to fill screen; double-click empty space to zoom out',
			layers_primary: 'Minority / Majority / Current',
			layers_primary_desc: 'switch the active boundary map',
			layers_data: 'Partisan / Wasted / Borders',
			layers_data_desc: 'toggle data layers',
			search: 'Find district',
			search_desc: 'jump by name; arrow keys pan, + / − zoom',
			escape: 'Escape',
			escape_desc: 'close this viewer',
			s4_tip:
				'In §4, click <em>Show flagged districts on map</em> to highlight the Airdrie split and NE/central Calgary zone.',
			got_it: 'Got it'
		},
		footer: {
			title: 'Alberta Electoral Boundary Audit — November 2026',
			copyright: '© Will Conner 2026 —',
			text_label: 'Text:',
			code_label: 'Code:',
			translation_label: 'Translations:',
			translation_credit: 'Anthropic Fable 5 (AI) — awaiting native-speaker review',
			data_credit:
				'Map data: secondary highways from the National Road Network, © Statistics Canada (Open Government Licence – Canada); other roads & water © OpenStreetMap contributors (ODbL); boundaries & results © Elections Alberta.'
		}
	},
	// deck.gl Map Explorer (DeckExplorer.svelte + deckExplorer/pois.ts). This is a
	// separate component from the framework-free engine under body.map / body.share.
	explorer: {
		controls: {
			// Desktop control panel header
			panel_title: 'Map controls',
			close_aria: 'Close map',
			// Map-version buttons
			map_version_hdr: 'Map version',
			map_version_hint: '· click to toggle',
			map_toggle_title: 'Toggle this map on/off',
			map_minority: 'Minority',
			map_majority: 'Majority',
			map_2019: 'Official',
			// Mobile segmented-button short labels
			map_minority_short: 'Min',
			map_majority_short: 'Maj',
			map_2019_short: 'Offic',
			// Search
			search_placeholder: 'Search a district…',
			search_aria: 'Search districts',
			search_clear_aria: 'Clear search',
			search_in: 'in {ed}',
			// Zoom / resolution readout
			zoom_aria: 'Zoom',
			res_prefix: '1 pixel ≈',
			// Boundary-line provenance tag beside the resolution readout: yellow
			// (overview) flags the official lines; blue (detail) the computed lines.
			zoom_official: '(Official)',
			zoom_computed: '(Computed)',
			// Overlays / layer toggles
			overlays_hdr: 'Community Interest Overlays',
			layer_highways: 'Highways',
			layer_water: 'Rivers & lakes',
			layer_annotations: "EBC '26 Annotations",
			// Mobile icon-bar aria labels
			mobile_map_version_aria: 'Map version',
			mobile_search_aria: 'Search districts',
			mobile_layers_aria: 'Map layers',
			mobile_info_aria: 'About the boundary lines',
			mobile_share_aria: 'Share this view',
			mobile_close_aria: 'Close map',
			// Language switcher (integrated into the map control bar / panel)
			lang_aria: 'Change language',
			lang_hdr: 'Language',
			// "Reading the lines" note (desktop + mobile info popover)
			lines_note_title: 'Reading the lines',
			lines_note_lead: 'Every odd shape or split line is a',
			lines_note_emphasis: 'deliberate choice by a commission',
			lines_note_tail:
				'— not a data error. Lines follow the edges of polling areas; where two maps agree they sit on the same line, where they split apart the proposals genuinely disagree.'
		},
		share: {
			button: 'Share this view',
			heading: 'Share this view',
			copy: 'Copy link',
			copied: 'Copied',
			help: 'This link captures your current map, overlays, and view.',
			open_heading: 'Open a shared link',
			open_placeholder: 'Paste a share link…',
			open_btn: 'Open',
			err_empty: 'Paste a share link',
			err_invalid: 'Not a valid share link'
		},
		tip: {
			total_votes: 'total votes',
			// Per-VA counts are election-day (in-person) votes only — advance/special
			// ballots are not attributed per voting area (per Elections Alberta).
			inperson_votes: 'in-person votes',
			ed_total: 'District total: {n} votes',
			ed_total_eday: 'District total: {n} (election-day)',
			poll: 'Poll #{id}',
			ucp_pct: 'UCP {u}%',
			ndp_pct: 'NDP {n}%',
			unassigned: '(unassigned)',
			where_in: 'in {community}',
			where_near: 'near {community}',
			note_sparse:
				"A sparsely populated area — with few votes cast here, the colour stays close to the map's neutral baseline.",
			note_no_votes:
				"No votes were recorded here, so this area shows the map's neutral baseline tone.",
			no_one_title: 'No one votes here',
			no_one_body:
				"No polling division covers this spot — nobody is recorded living or voting here, so it stays the map's neutral tone.",
			flag_link: 'Click to zoom in'
		},
		miller: {
			// Condition (d). Conditions (a)–(c) are the nested objects below; the
			// explorer picks the key from each zone's `cond` in lunty_bounds.json.
			// locked_hint is appended on the map only (not the text version).
			locked_hint: 'Nothing inside this outline moves under Recommendation 5.',
			title: 'Recommendation 5(d): the rural seat to restore',
			body: 'Justice Dallas Miller, the commission’s chair, wrote that if the Legislature would not accept losing two rural ridings, it should go from 89 seats to 91 and restore them. This is the one place he named for a restored seat: a riding made mostly of Clearwater County and western Mountain View County, with s. 15(2) status (the rule that lets a large, remote riding have far fewer people than average). He asked that it be considered, not required. The outline is approximate: Clearwater County plus the part of Mountain View County that sat in the 2019 Rimbey-Rocky Mountain House-Sundre riding. It lies wholly north of Airdrie and takes no land from any riding conditions (a) or (b) protect. He named no place for the second seat.',
			a: {
				title: 'Recommendation 5(a): no change from Airdrie south',
				body: 'The chair’s Recommendation 5 says restoring the two rural seats should not touch any riding in Airdrie, or with land south of Airdrie’s southern city limit, except Drumheller-Stettler. That is {n} ridings, every Calgary seat among them, that should match the majority map line for line. Airdrie and Calgary are where the commission split most sharply; this condition keeps them as the majority drew them.'
			},
			b: {
				title: 'Recommendation 5(b): no change in north Edmonton',
				body: 'Recommendation 5 says restoring the two rural seats should not touch any Edmonton riding north of the North Saskatchewan River. That is {n} ridings that should match the majority map. Beverly-Clareview crosses the river; about two-thirds of it is on the north bank, so it is counted here.'
			},
			c: {
				title: 'Recommendation 5(c): south Edmonton goes back to the draft',
				body: 'Recommendation 5 says every Edmonton riding south of the North Saskatchewan River should return to the commission’s October 2025 interim map, the draft it published for comment before the final split. One option is allowed: adding Nisku to Edmonton-South East, to put Leduc and Beaumont back in one riding. This outline marks the {n} majority-map ridings that would change. It does not show the interim lines themselves.'
			}
		},
		flags: {
			'banff-town': {
				title: 'Banff — the town carved out of the park',
				body: "Banff sits inside a federal national park, as a small municipal island. The minority groups the townsite with Canmore — the next town down the Bow Valley — in “Canmore-Kananaskis,” and leaves the uninhabited park as the riding that carries Banff's name. The boundary hugs the town because it's the only populated spot for miles. It looks like a mistake, but it follows real geography."
			},
			'banff-park': {
				title: 'North of Banff — “Rocky Mountain House–Banff Park”',
				body: "“Rocky Mountain House–Banff Park” is one of the minority's proposed ridings, made up largely of uninhabited national park; the town of Banff sits in a neighbouring riding to the south. The minority applied the Electoral Boundaries Commission Act's smaller-population provision to this riding — a choice the commission's majority called \"a bad faith effort\" in the final report. The audit's check undercuts that charge: the riding qualifies for the provision even without the park extension."
			},
			'airdrie-split': {
				title: 'Airdrie — split four ways',
				body: "Airdrie's growth and its commute to Calgary (about 76% of out-commuters) could have anchored a single new Airdrie-area seat — the kind the data supports. The minority instead splits the city across four ridings; the population math doesn't require it, and no submission proposed it. On the audit's cracking-signature test this four-way split stops short of a formal signature: outside Airdrie East, which holds more than half the city, Airdrie's residents end up a minority, but the test needs them outnumbered in every piece. This is a community split, invisible to the partisan-fairness tests; the audit measures the structural effect, not intent. (Academic §5.3.2.)"
			},
			'nolan-hill-cochrane': {
				title: 'Calgary-Nolan Hill–Cochrane',
				body: "Cochrane's commute to Calgary could have justified pairing it with the city — but the 2021 journey-to-work data spreads that flow city-wide (about a third of workers; half work within Cochrane) and doesn't point to Nolan Hill. The minority's narrow corridor to the Nolan Hill ward — in one of two districts the commission's majority said \"look strange\" — reaches further than the data, and no submission proposed it. The audit's cracking test does not flag it: Cochrane stays whole and makes up about two-thirds of the riding, and at about 34,000 it is too small for a seat of its own. (Academic §5.3.2.)"
			},
			'olds-airdrie-reach': {
				title: 'Olds–Three Hills–Didsbury — the Airdrie reach',
				body: "A rural riding keeping the Highway 2 towns — Olds, Didsbury, Three Hills — together is well supported; Beiseker-area residents wrote in favour of it. It could have stayed within those communities. The minority's version instead reaches south into the northern edge of Airdrie, an extension the population math doesn't require. The reach is part of how the four-way Airdrie split works — a thinly settled strip of the city, about 350 people, absorbed into a larger rural seat — which the audit reads as part of the cracking pattern. (Academic §5.3.2.)"
			},
			chestermere: {
				title: 'Chestermere — split between two ridings',
				body: "Chestermere's heavy commute to Calgary (86% of out-commuters) could have supported keeping it whole and near the city — which residents who opposed a Calgary merger also wanted. The minority instead slices a southern piece into a specific Calgary district it shares no schools or transit with, and that slice fails the population test. The audit counts the bleed into a Calgary district as a community-of-interest split that thins Chestermere's voice; it did not score it on the cracking test. (Academic §5.8.4; justification tests, Test 5.)"
			},
			'red-deer': {
				title: 'Red Deer — the hybrid ridings',
				body: "Red Deer's regional ties to Blackfalds, Sylvan Lake, Lacombe and Innisfail could have grouped those towns together — a city councillor and residents proposed similar hybrids. The minority's version instead folds parts of the city itself into town-led ridings, thinning urban Red Deer's vote. Folding a city into town-led ridings is the pattern the audit calls hybridization — consistent with cracking, achieving the partisan effect inside the hybrid ridings rather than across them. (Academic §5.3.5.)"
			},
			'st-albert': {
				title: 'St. Albert — competing configurations',
				body: "Either map's version of St. Albert could rest on a reasonable basis. The audit simply found no submission backing the minority's specific alternative — and since citizens rarely name a commission's exact boundaries, it treats the evidence here as thin, not clearly for or against."
			},
			'calgary-zone-a-packing': {
				title: 'Calgary north & east — larger districts, no packing signature',
				body: "The commission's majority didn't flag this one — the audit's own math does. Across Calgary's north and east (the audit's “Zone A,” north and east of the Bow River), the minority map's districts run about 11.5% larger than the provincial average, against 2.8% on the majority map, so each ballot there weighs a little less. That is a population-equality finding. It is not a packing signature: on 2023's votes the NDP would win 8 of the zone's 17 districts, by margins below the provincial average, and the audit's packing test needs margins well above it. The audit measures the structural effect, not intent. (Academic §5.3.1.)"
			}
		},
		text: {
			page_title: 'Text version — Alberta Electoral Boundary Audit map',
			intro:
				'This is the text version of the audit’s interactive map. It carries the same information as the visual map, written out so it can be read with a screen reader. It leads with the boundaries the audit flagged, then lists every district and which of the three maps includes it.',
			link_map: 'Open the interactive map',
			link_report: 'Read the full report',
			link_to_text: 'Open the accessible text version of this map',
			toc_heading: 'On this page',
			toc_summary: 'Short summary',
			toc_flagged: 'Flagged boundaries',
			toc_r5: 'Recommendation 5 areas',
			toc_directory: 'District directory',
			summary_heading: 'Short summary',
			summary_p1:
				'The audit compares three maps of Alberta’s electoral districts: the commission’s minority proposal, its majority proposal, and the 2019 enacted map that is in force today.',
			summary_p2:
				'On five structural tests committed to the repository on April 24, after provisional runs on approximate boundaries but before the official files arrived, the majority map crosses none of the thresholds and the minority map crosses four. These tests need no election results. The separate statistical results compare each map against a large set of computer-drawn neutral maps.',
			summary_p3:
				'The sections below explain nine specific boundaries the audit flagged, then list every district. This page describes the statistical and structural position only. It does not reach a legal conclusion about any map.',
			flagged_heading: 'Flagged boundaries',
			flagged_lead:
				'The audit flagged nine boundaries. Some look unusual but faithfully follow real geography; others are flagged by the audit’s own measurements, though none meets the audit’s formal packing or cracking test. Each is explained below, with a section reference to the academic report where it applies.',
			r5_heading: 'Recommendation 5 areas',
			r5_lead:
				'The government cited the commission chair’s Recommendation 5 when it handed the map to an MLA committee. The recommendation sets four conditions for a 91-seat map, three of them tied to districts on the majority map. Each area the map draws is described below, with the majority-map districts it covers.',
			r5_districts: 'Majority-map districts in this area:',
			directory_heading: 'District directory',
			directory_lead:
				'This table lists every district name that appears on any of the three maps, in alphabetical order. For each name it shows whether that name is part of the minority proposal, the majority proposal, and the 2019 enacted map. District names differ between the maps, so some rows appear on only one or two of them. The table shows names, map membership and each district’s election-day vote total — for population figures and test results, see the full report.',
			directory_totals_note:
				'Each figure is the district’s in-person (election-day) vote total on that map — the sum of its polls. Advance and special ballots are not attributed per voting area, so they are not included here; for full results see the report. A dash (—) means the district name does not appear on that map.',
			col_district: 'District',
			col_minority: 'Minority proposal',
			col_majority: 'Majority proposal',
			col_2019: 'Official map',
			present_yes: 'Yes',
			present_no: 'No',
			methodology_note:
				'This page is a static, text-only equivalent of the interactive map. It is built from the same district data and the same boundary annotations.',
			skip_to_main: 'Skip to main content',
			back_to_map: 'Back to the interactive map'
		}
	},
	// Public feedback form (/feedback route + footer links).
	feedback: {
		nav_link: 'Send feedback',
		page_title: 'Send feedback',
		meta_description:
			'Share a correction, question, or suggestion about the Alberta Electoral Boundary Audit.',
		heading: 'Send feedback',
		intro:
			'Spotted an error, have a question, or want to suggest an improvement? This goes straight to the author. Name and email are optional — leave an email only if you would like a reply.',
		name_label: 'Name',
		name_optional: 'optional',
		name_placeholder: 'Your name',
		email_label: 'Email',
		email_optional: 'optional',
		email_placeholder: 'you@example.com',
		email_hint: 'Only used to reply to you. Never shared, never added to any list.',
		message_label: 'Message',
		message_required: 'required',
		message_placeholder: 'What would you like to tell us?',
		submit: 'Send feedback',
		submitting: 'Sending…',
		success_title: 'Thank you',
		success_body:
			'Your feedback has been received. If you left an email address and your message calls for a reply, you will hear back.',
		send_another: 'Send another',
		error_empty: 'Please enter a message before sending.',
		error_rate: 'You have sent several messages recently. Please try again in a little while.',
		error_generic: 'Something went wrong sending your feedback. Please try again in a moment.',
		privacy_note:
			'Your message is stored securely in Canada and used only to improve this audit. See the {privacy} for details.',
		privacy_link_text: 'privacy policy',
		back_to_report: 'Back to the report',
		back_to_map: 'Back to the map explorer'
	},
	// Reader-facing prose of the standalone pages (explainers, methods, norms,
	// law, privacy policy) and the main page's reference list. Strings that
	// carry markup are rendered with {@html}; __BASE__ is replaced with the
	// deploy base path at render time.
	pages: {
		explainers: {
			head_title: 'The Fourteen Explainers · Alberta Electoral Boundary Audit',
			head_description: "Fourteen short explainers — one per finding in the Alberta Electoral Boundary Audit: cracking, packing, neutral ensembles, the prosecutor's fallacy, conventions versus law, and more.",
			back: '← Back to audit',
			site_label: 'Alberta Electoral Boundary Audit',
			h1: 'The Fourteen Explainers',
			meta: 'Appendices A–N · one concept each',
			standfirst: "Each finding in the audit links to one appendix here, and each appendix owns exactly one concept. It starts from the honest confusion. It builds the idea with one concrete example. It sends you back to the finding's number able to read it unaided. And it ends with what the concept <em>cannot</em> tell you. Read them in any order.",
			appendix_a: {
				heading: 'Appendix A — What "cracking" actually does to a vote',
				confusion: '<em>The confusion:</em> "Airdrie voters still vote. Nobody took their ballots. How does drawing lines \'dilute\' anything?"',
				p1: "Imagine a town of 40,000 that mostly votes Orange, sitting in a region that mostly votes Blue. Give the town its own riding, a district with its own seat in the Legislature, and it elects an Orange MLA: 40,000 people, one seat, a voice. Now slice the town into four pieces and staple each piece to a chunk of Blue countryside. In each new riding the town's 10,000 voters face 30,000 rural voters. Orange loses all four. Same voters, same ballots, zero seats. Nothing was stolen from any single voter. What was taken is the <em>community's</em> ability to elect anyone. That is cracking. Its mirror move is packing (Appendix C): stuff a group into as few ridings as possible, so it wins those by landslides and nothing else.",
				p2: "Now re-read finding 1: 85,805 people, four ridings, a minority in three of them. The fourth, Airdrie East, keeps more than half the city together, so by the audit's own (exploratory) rule this is no cracking signature. Outside it, the pieces do what the imagined town's pieces did. The same commission's other map shows two ridings were enough to satisfy the law.",
				limit: '<em>The limit:</em> cracking describes an effect, not a motive. A split can happen because someone wanted dilution. It can also happen because other constraints crowded the map. The geometry alone cannot say which.',
				back_anchor: '<a href="__BASE__/evidence#casing-1">↩ Back to finding 1</a>'
			},
			appendix_b: {
				heading: 'Appendix B — Shape analysis, and what s.15(2) protection is for',
				confusion: '<em>The confusion:</em> "All electoral districts look weird. Why do these three shapes matter?"',
				p1: 'Districts follow geography, so lumpy is normal. Shape analysis looks for <em>work</em>: a boundary doing something no ordinary constraint explains. A corridor that lassoes one neighbourhood into a distant district. An arm reaching into a city\'s edge. A line extended through land where nobody lives. Alberta\'s law has a special provision, section 15(2), that lets up to four districts fall below the normal population floor. It was written for remote districts with strong community ties, like northern ridings serving Indigenous communities across vast distances. Extending a boundary through uninhabited national park so a district qualifies for that protection is what the commission\'s majority, the chair among them, called "a bad faith effort": a rule written for people who live far apart, used to protect a line where no one lives at all. The audit\'s check undercuts the charge: the district qualifies even without the extension.',
				p2: "Now re-read finding 2: three shapes, flagged by the commission's own majority. Tests that had no stake in its fight confirm the odd geometry, and undercut the alleged motive.",
				limit: "<em>The limit:</em> a strange shape is a question, not an answer. One of these shapes has a real, creditable logic underneath: the Banff townsite's placement with Canmore. The majority's objection survives it anyway. It was aimed at the empty-park extension, and the placement does not touch that.",
				back_anchor: '<a href="__BASE__/evidence#casing-2">↩ Back to finding 2</a>'
			},
			appendix_c: {
				heading: 'Appendix C — Packing, in a three-district toy example',
				confusion: '<em>The confusion:</em> "Bigger districts have more voters. So what? Everyone still gets one vote."',
				p1: "Everyone does. Size is a clue to how those votes are grouped. Take 12,000 voters, 7,000 Orange and 5,000 Blue, split into three districts of 4,000. Draw them evenly and Orange wins all three. Now redraw. Cram 4,000 Orange voters into one district (Orange wins it 100–0). Spread the remaining 3,000 Orange across two districts of 4,000, where Blue's 5,000 give it the edge in both. Same 12,000 voters, same 7,000 Orange majority. Now Orange holds one seat and Blue holds two. That is packing: your opponents' votes get warehoused where they pile up as surplus, wasted on margins they didn't need. The tell is district <em>size and concentration</em>. Opponents' districts run big and deep. Yours run lean and efficient.",
				p2: "Now re-read finding 3: in one Calgary zone, the minority's seventeen districts run 11.5% over the provincial average. The majority's, drawn in the same room, run 2.8%. That is the size half of the pattern. The other half is missing: on 2023's votes the NDP wins eight of the seventeen, by margins below the provincial average, so the audit's packing test does not detect packing.",
				limit: '<em>The limit:</em> oversized districts can also come from honest guesses about growth, or from keeping a community whole. Size asymmetry is the signature packing leaves. Several innocent choices leave it too.',
				back_anchor: '<a href="__BASE__/evidence#casing-3">↩ Back to finding 3</a>'
			},
			appendix_d: {
				heading: 'Appendix D — What MAD measures, and why the band exists',
				confusion: '<em>The confusion:</em> "Population Mean Absolute Deviation — is this just statistics for \'the districts aren\'t identical\'?"',
				p1: "Almost. Districts can't all hold exactly the same number of people; communities come in awkward sizes. MAD asks a plain question: on average, how far does each district stray from the ideal share? The majority map's MAD of 3,180 means its districts miss the ideal by about 3,180 people on average. The minority's 4,707 means its misses average half again larger. The law tolerates straying, inside a band (Alberta allows ±25%), because respecting real communities is worth some inequality. That's the bargain. Deviation is the currency, and you spend it to buy things like whole towns and sensible boundaries. That is what gives finding 4 its point: on the commission's own tables, the minority map spends 48% more of that currency than the majority. On 2021 census counts the three maps' spreads come out almost the same. And finding 1 shows it <em>didn't</em> buy Airdrie's wholeness with it.",
				p2: 'Now re-read finding 4: the wider spread of the two, on the one value the statute actually quantifies. Against neutral maps held to ±12.5% (maps a computer drew without seeing a single vote; Appendix F), the minority\'s spread, measured at the middle district, is wider than 99 of every 100. Against neutral maps allowed the law\'s full ±25%, both maps are more equal than almost all of them.',
				limit: '<em>The limit:</em> the law ranks nothing inside the band. "Spent more deviation" is an observation about priorities, not a violation. Every district on both maps is legal.',
				back_anchor: '<a href="__BASE__/evidence#casing-4">↩ Back to finding 4</a>'
			},
			appendix_e: {
				heading: "Appendix E — What municipal anchoring measures, and what it can't show",
				confusion: '<em>The confusion:</em> "Why count how often a boundary follows a city or town line?"',
				p1: "Because that is where people already know they live. When a district boundary runs along a municipal boundary, the property-tax line, the school-division line, the local ward line and the provincial-election line coincide. A voter can tell which district they are in without a map. The test measures how much of each map's district boundary length runs within 500 metres of a Statistics Canada municipal boundary. Alberta's 2019 map, drawn by the last commission, scores 75% on that measure. The majority map scores 80%. The minority scores 72%. Both sit close to the 2019 map, so on overall rates the test does not separate them.",
				p2: "Now re-read finding 5: the rate is ordinary on both maps, and close to the 2019 map's. The test does not separate them.",
				limit: '<em>The limit:</em> the anchoring rate is a norm, not a rule. The Act sets no threshold. And a departure can have a good reason, such as a suburb that has grown across a city limit.',
				back_anchor: '<a href="__BASE__/evidence#casing-5">↩ Back to finding 5</a>'
			},
			appendix_f: {
				heading: 'Appendix F — The what-if machine, and how to read a percentile',
				confusion: '<em>The confusion:</em> "A million computer maps? A percentile of a simulation? What does that even mean?"',
				p1: 'You can\'t judge whether a map is unusual without knowing what usual looks like. For electoral maps, nobody gets to see the alternatives. So the audit built them. An algorithm starts from a valid map and makes a long chain of random valid edits. Merge two neighbouring districts. Re-split them a random valid way. Repeat: 252,500 times over, in four independent chains, 1,010,000 maps in all. No vote data is consulted while drawing. The machine cannot favour anyone because it cannot see anyone, and that is what "neutral" means here. Then you take the real map, measure it, and ask: out of the million neutral maps, how many score this high? If 500,000 do, your map is ordinary. If 69 do, your map is the kind of map neutral drawing produces 69 times in 1,010,000 tries. One caution: neighbouring maps in the chain are near-copies, so the million maps are worth closer to 1,400 independent draws, and the exact rank is less precise than it looks.',
				p2: 'Now re-read finding 6: the majority map at the 78th percentile — ordinary. The minority at the 99.99th — 69 in 1,010,000 score higher.',
				limit: '<em>The limit:</em> the machine respects population and contiguity (each district a single connected piece), but not every statutory nicety a real commission weighs. So its percentiles measure distance from <em>neutral drawing</em>, not from <em>everything a lawful commission might do</em>. And a percentile is a distance, not a verdict.',
				back_anchor: '<a href="__BASE__/evidence#casing-6">↩ Back to finding 6</a>'
			},
			appendix_g: {
				heading: 'Appendix G — The efficiency gap, in one worked example',
				confusion: '<em>The confusion:</em> "One number that captures gerrymandering? That sounds too convenient."',
				p1: 'It is, slightly. That is why it gets a threshold, and a miss, in this report. The idea: every vote that doesn\'t help win a seat is "wasted." That means all votes cast for losers, plus winners\' votes beyond the 50%-plus-one they needed. In a fair map both parties waste about equally. The efficiency gap is the difference in wasted votes, as a share of all votes. Suppose Orange wins a 100-vote district 90–10. Orange wasted 39, its surplus beyond 51. Blue wasted 10, all of them votes for the loser. Packed and cracked maps make one party waste systematically more. In this report\'s sign convention, positive gaps favour conservatives. The audit\'s Alberta calibration line (~4.1%) is the level only 5% of the million neutral maps cross.',
				p2: "Now re-read finding 7: minority at +4.0%, 94.5th percentile. That is below the audit's own pre-registered line, locked in public in advance, and it is reported as the miss it is.",
				limit: "<em>The limit:</em> the efficiency gap compresses a whole map into one number, and one number can't tell a gerrymander from lumpy geography. That's why this audit uses four metrics and a locked threshold. And it keeps the miss on the books.",
				back_anchor: '<a href="__BASE__/evidence#casing-7">↩ Back to finding 7</a>'
			},
			appendix_h: {
				heading: "Appendix H — The prosecutor's fallacy, in plain language",
				confusion: '<em>The confusion:</em> "One in 568,000 that this map is innocent. That\'s the finding, right?"',
				p1: 'No, and the difference matters enough to have a name. The number says this: <em>if</em> a neutral process drew Alberta\'s map, the chance it would look like the minority map is about one in 568,000 under the audit\'s model. That is P(this evidence, given innocence). It is not P(innocence, given this evidence). Swapping them is the prosecutor\'s fallacy. The classic example: a suspect matches a DNA profile found at a scene, and the profile occurs in one in a million people. "One in a million chance he\'s innocent"? Wrong. In a city of ten million, about ten people match. On the DNA alone, the suspect is one of ten — a 90% chance <em>someone else</em> is the source. The rarity of the evidence under innocence is not the probability of innocence. You also need to know how many innocent ways the evidence could arise.',
				p2: 'Now re-read finding 8: the audit states the number it can defend — the rarity of the map under neutral drawing — and refuses the swap that would turn it into a verdict.',
				limit: '<em>The limit:</em> refusing the fallacy costs the audit its most quotable sentence, and that cost is deliberate. Rarity is evidence. It is not, and never becomes, proof of intent.',
				back_anchor: '<a href="__BASE__/evidence#casing-8">↩ Back to finding 8</a>'
			},
			appendix_i: {
				heading: 'Appendix I — What a sampler is, and why swapping it matters',
				confusion: '<em>The confusion:</em> "You checked your simulation with… another simulation? How is that a check?"',
				p1: "Because the two machines are built differently, and artifacts (results made by a machine's quirks rather than by the map) don't usually survive a change of machinery. Any map-drawing algorithm, or sampler, has quirks. The standard one, ReCom, has a documented lean toward compact, tidy districts, which could in principle exaggerate how extreme a sprawling real map looks. So the audit swapped the engine. The replacement grows districts from random spanning <em>forests</em> instead of trees, with measurably different internal behaviour. It was registered publicly (OSF he53s) before a single map was drawn with it, and its seeds were derived from a public randomness beacon anyone can verify. If the minority's tail position were an artifact of the first engine's quirks, the second engine would move it. It moved less than one percentile point on every metric, within the run's own margin of error (the run fell short of its sample target): a pre-registered ROBUST verdict. The audit also reports the check that <em>failed</em>. The claim that the minority map's flagged geometry is the specific mechanism behind the seat numbers did not survive testing, and was dropped.",
				p2: 'Now re-read finding 9: three attacks, two survived, one claim honestly lost.',
				limit: '<em>The limit:</em> robustness rules out tooling artifacts. It cannot rule in design. A genuinely extreme map is genuinely extreme, whatever produced it.',
				back_anchor: '<a href="__BASE__/evidence#casing-9">↩ Back to finding 9</a>'
			},
			appendix_j: {
				heading: 'Appendix J — Why neighbours voting alike breaks naive statistics',
				confusion: '<em>The confusion:</em> "A test gave p = 0.0024 and you threw it away? That looks like hiding a result."',
				p1: "The opposite: it's correcting one. Many tests assume observations are independent, like separate coin flips. Voting areas aren't. Neighbouring areas share demographics, incomes, histories. They vote alike. Treating 100 clustered areas as 100 independent flips is really more like 20 informative observations wearing 100 coats, and it makes coincidences look impossible when they're merely uncommon. The fix is to build a null (a picture of what chance alone would produce) that preserves the clustering. Shuffle <em>blocks</em> of neighbouring areas together rather than each area separately, and ask the question again. The audit's swing-zone test of boundary choices looked significant under the naive null (p = 0.0024) and unremarkable under the corrected one (p ≈ 0.19). When the honest null disagrees with the flattering one, you keep the honest null. And you retire the result.",
				p2: "Now re-read finding 10: two of the audit's own instruments retired, one pre-registered test the minority map outright passed.",
				limit: "<em>The limit:</em> the correction shows the <em>boundary-choice</em> signal doesn't stand. It says nothing against the ensemble findings from the computer-drawn maps, which never assumed independence in the first place.",
				back_anchor: '<a href="__BASE__/evidence#casing-10">↩ Back to finding 10</a>'
			},
			appendix_k: {
				heading: 'Appendix K — How to check a stated reason against public data',
				confusion: '<em>The confusion:</em> "Commissioners are the experts. Who is an audit to grade their reasons?"',
				p1: 'Nobody special, and that\'s the point: the check requires no special access. The minority report says Cochrane residents "move fluidly" into Calgary. Statistics Canada\'s journey-to-work tables (free, public) show about a third of Cochrane\'s workers commute into Calgary, while roughly half work in Cochrane. A real tie, and one that says nothing about the specific Nolan Hill corridor drawn. The report says rural residents "go to school" in the city. For Red Deer and Sylvan Lake that holds in part: the public school divisions differ, but one Catholic division serves both, and 54% of Sylvan Lake\'s out-commuters work in Red Deer. Each check follows the same recipe. Take the stated reason. Find the public dataset that would show it. See whether the <em>particular line drawn</em> is the line the data supports. Four of six checked rationales fail that last step, and a fifth holds only in part. The tie is real; the line is not the one the tie points to.',
				limit: "<em>The limit:</em> a rationale that fails checking proves the <em>stated</em> reason doesn't fit. It cannot reveal the real one. Sloppiness and pretext leave identical paperwork.",
				back_anchor: '<a href="__BASE__/evidence#casing-11">↩ Back to finding 11</a>'
			},
			appendix_l: {
				heading: 'Appendix L — How commissioners are appointed, and what nomination implies',
				confusion: '<em>The confusion:</em> "Government-nominated commissioners drew the government-favouring map. Case closed, surely?"',
				p1: "Not closed. Start with who sits in the room. Alberta's commission is built from nominations: a chair, plus commissioners nominated from government and opposition sides. This time the Premier nominated the two who wrote the minority report (<a href=\"https://www.assembly.ab.ca/about/news-and-announcements/2025/03/28/electoral-boundaries-commission-to-soon-begin-consultations\" rel=\"noopener\">Legislative Assembly of Alberta, March 28, 2025</a>). The design assumes partisan perspectives and balances them. It bets that a mixed room converges on one defensible map. For two decades after 1995 the bet paid: even when a commissioner dissented, each commission sent the Assembly one map. This cycle the room split along its nomination lines, and the government's nominees produced the statistical outlier. That correlation is real and worth recording. It is also exactly where the inference must stop. Nominated commissioners are not agents. No evidence in this audit's record shows the government directed, coordinated with, or even knew the shape of its nominees' map before filing. At the committee's October 28 meeting the Opposition Leader alleged that maps presented at the commission's hearings \"were created by the government\" and matched the minority's maps in style (committee transcript, p. CEB-71). That is an allegation; the audit has not verified it. History is full of nominees who disappointed their nominators. The correlation invites a question. It cannot answer it. And the audit's instruments cut against the majority too when the data went that way. That is what symmetric measurement means.",
				p2: 'Now re-read finding 12: the split is the anomaly; the provenance, who nominated whom, is the question mark, not the answer.',
				limit: '<em>The limit:</em> appointment provenance is context, never proof. Treating it as proof is the same fallacy as Appendix H, wearing a political coat.',
				back_anchor: '<a href="__BASE__/evidence#casing-12">↩ Back to finding 12</a>'
			},
			appendix_m: {
				heading: "Appendix M — The Act's process, commission to committee, end to end",
				confusion: '<em>The confusion:</em> "How can the legislature just… take over redistricting? Isn\'t the commission\'s map the map?"',
				p1: "No. This is the load-bearing surprise of the whole episode. Under Alberta's <em>Electoral Boundaries Commission Act</em>, the commission proposes; only the Legislative Assembly disposes. The commission's final report — hearings, submissions, revisions and all — is advice. It has no legal effect until the Assembly enacts a map. And the Act places no constraints on what the Assembly does instead: no minimum debate, no notice period, no obligation to prefer the commission's work, no hearing requirement for whatever process follows. Nothing in the Act stops the Assembly from sending the work elsewhere. That is what Government Motion 37 did, sending it to a select committee. Recommendation 5 itself proposed an all-party select committee for a two-seat fix; Motion 37 used that vehicle for a wider redraw. Select committees of the Assembly are composed of MLAs, so the choice of vehicle kept the decision out of independent hands. An advisory panel drafted the map; the committee reviewed it and sent it to the Assembly, where MLAs decide. Lawfully. In every cycle since the Act was amended in 1995, the Assembly's restraint, not the statute, was what kept politicians' hands off the pen. In 1992 there was no commission report to honour: the commission deadlocked, five commissioners filing five reports, and a committee of MLAs drew the map. Secondary accounts say the Court of Appeal faulted that committee in 1994 for being unable to explain several of its boundaries; the audit has not read the judgment.",
				p2: 'Now re-read finding 13: sixteen communities of hearings replaced by a body not required to hold any. All of it inside the Act.',
				limit: '<em>The limit:</em> this appendix explains what the law permits. Whether what the law permits is what Albertans should accept is a political question — the one the November tests on the main page are built to inform.',
				back_anchor: '<a href="__BASE__/evidence#casing-13">↩ Back to finding 13</a>'
			},
			appendix_n: {
				heading: 'Appendix N — Conventions versus law, and how norms erode',
				confusion: '<em>The confusion:</em> "If politicians drawing their own districts violates our deepest electoral norm, how can it be legal?"',
				p1: "Because Canada's constitution runs on two operating systems. One is law: written, justiciable (a court can rule on it), enforced by courts. The other is convention: unwritten rules of political behaviour, binding in practice, invisible to a courtroom. The Supreme Court described the divide in the 1981 Patriation Reference. Courts may <em>recognize</em> a convention and will still decline to <em>enforce</em> it, because conventions are policed politically — by opposition, press, and voters — not judicially. In Alberta, a boundary commission's map lives on the convention side. Sixty years of practice, federally and then province by province, built the rule that politicians do not draw their own ridings. Alberta's Act does not make that rule mandatory. So the guardrail's entire strength was that governments kept choosing to honour it. A norm set aside once, without consequence, is weaker for every government that follows. Of any party.",
				p2: 'Now re-read finding 14: a documented departure from long practice, which the opposition calls a violation, and no convention a court will enforce — all at once. A court can still review the map the process produces.',
				limit: '<em>The limit:</em> "unenforceable" is a statement about courts, not about consequences. Conventions are enforced at elections, by people who know what was done. Reports like this one exist so they know.',
				back_anchor: '<a href="__BASE__/evidence#casing-14">↩ Back to finding 14</a>'
			},
			footer_note: 'Content mirrors the appendices of the <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/public/report_public.md" rel="noopener">full public report</a>.'
		},
		methods: {
			head_title: 'How the Maps Were Tested · Alberta Electoral Boundary Audit',
			head_description: 'Every test and statistic in the audit, explained in plain language: the million-map what-if machine, the five structural tests, the four fairness measures, p-values, and the tests that died.',
			back: '← Back to audit',
			site_label: 'Alberta Electoral Boundary Audit',
			h1: 'How the Maps Were Tested',
			meta: 'Every test and every statistic, in plain language · Every number reproducible from the public repository',
			standfirst: 'The whole audit rests on one simple idea. Want to know whether a map is unusual? Draw a million maps that could not be biased. A computer draws them, and it never sees a single vote. Then check where the real maps land among them. This page walks through that idea and every test built on it. No formulas. If you can read a weather forecast, you can read this.',
			toc: {
				aria: 'Page contents',
				what_if: 'The what-if machine',
				percentile: 'How to read a percentile',
				structural: 'The five structural tests',
				fairness: 'The four fairness measures',
				odds: 'What the odds mean',
				died: 'The tests that died',
				break: 'Trying to break our own result',
				prereg: 'Promises made in advance',
				reproduce: 'Run it yourself'
			},
			what_if: {
				heading: 'The what-if machine: 1,010,000 neutral maps',
				p1: 'A computer drew <strong>1,010,000 valid Alberta maps</strong>, each with 87 districts, the 2019 map\'s count. Each one follows the same two hard rules the real commission followed: every district holds close to the same number of people (within 25% of the average; each drawing step aims for 12.5%), and every district is one connected piece.',
				p2: 'How does a computer draw a map? One small step at a time. Take two districts that share a border. Merge them into one blob. Split the blob back into two new legal districts, at random. Repeat, 1,010,000 times, saving the map after each step. The method is called ReCom, and it is the standard tool in this field.',
				p3: "The key fact: <strong>the computer never sees a vote.</strong> It does not know where NDP or UCP voters live. So if a neutral map still leans one way, that lean comes from Alberta's geography alone. And if a real map leans much further than nearly all the neutral ones, geography and the two hard rules alone become a poor explanation.",
				p4: 'Four honesty points about the machine:',
				li1: '<strong>The dice came from a public source.</strong> The random seed (the starting number behind every random choice) combines a published value from a public randomness beacon ("drand", run by the League of Entropy, a group that includes Cloudflare) with a fixed label. The beacon value (round 5,500,000) was public in October 2025, so it can\'t date the seed. The author fixed the label in code on April 27, 2026, before the official map files arrived on May 6; the record is a commit in the project\'s repository, not an OSF registration. Anyone can recompute it.',
				li2: '<strong>Four separate runs agree.</strong> The million maps came from four independent runs, each starting differently. All four settled on the same picture. The standard checks for this (used across the field) pass with room to spare.',
				li3: '<strong>A note on seat counts.</strong> The 2026 commission maps have 89 districts each. The simulated maps have 87, the size of the 2019 map, the last legally enacted one. The panel\'s November map has 91. Seats on this site are given as <em>shares</em>, so the three sizes can be set side by side. The fit is close, not exact: the audit labels these cross-size comparisons and is checking them against simulated maps of the same size.',
				li4: "<strong>The machine is not a perfect referee.</strong> It follows the two hard rules, but not every soft rule real commissions honour, like keeping communities together. Real commission maps are actually tidier than most neutral maps. The audit names this limit plainly everywhere the machine's numbers appear."
			},
			percentile: {
				heading: 'How to read a percentile',
				p1: 'Line up all 1,010,000 neutral maps from least UCP-leaning to most UCP-leaning. Now place a real map in the line. Its <strong>percentile</strong> is just its position: "78th percentile" means it leans further than 78 out of every 100 neutral maps. That is unremarkable: a bit above the middle of the pack.',
				p2: '"99.99th percentile" is different. It means the map out-leans virtually every neutral map in the line — in this audit, all but <strong>69 of the 1,010,000</strong>. Height works the same way. A man at the 78th percentile is a bit tall. A man at the 99.99th percentile stands about six foot eight.'
			},
			structural: {
				heading: 'The five structural tests (no election results needed)',
				p1: 'Not every test needs the machine. The audit also measured the drawn lines themselves. Five tests, committed to the repository on April 24, after the commission\'s reports were public and after provisional runs on approximate boundaries, but before the official map files arrived. They are not on the OSF. Each compares the two commission maps directly.',
				li1: "<strong>1. Population spread.</strong> How far do districts drift from the ideal size? On the commission's own tables, the majority map's average drift is 3,180 people. The minority map's is 4,707, about half again wider. Wider drift means votes count less equally. On 2021 census counts, though, the three maps' average drift comes out almost the same.",
				li2: "<strong>2. Calgary crowding.</strong> In north-east and central Calgary, the minority map's districts run 11.5% bigger than the provincial average. The majority's run 2.8% bigger. Bigger districts mean each vote inside them weighs less. Crowding one party's voters into fewer, larger districts is called <em>packing</em>, but the audit's packing test doesn't detect it here: on 2023's votes the NDP wins eight of the zone's seventeen districts, by margins below the provincial average.",
				li3: '<strong>3. The Airdrie split.</strong> The law forces Airdrie into at least two districts. The majority map uses two. The minority map cuts the city into four pieces (three holding at least 2% of its people), each attached to different outside territory. Splitting a community thin is called <em>cracking</em>. The split crosses this test\'s line, but not the audit\'s separate cracking test (exploratory): Airdrie East keeps more than half the city together, and nine in ten of its people are Airdrie residents.',
				li4: "<strong>4. The chair's flags.</strong> The commission's majority, the chair among them, publicly flagged boundaries as geographically strange. Four of its flags land on the minority map, and the audit's own geometry check confirmed three. Zero land on the majority map.",
				li5: '<strong>5. Following city limits (the test that died).</strong> Both maps follow city limits about as often as the 2019 map\'s 75% (80% and 72%), so this test cannot tell them apart. The audit keeps the dead test on display instead of deleting it.',
				p2: 'Score: the minority map crosses all four live thresholds. The majority map crosses none.'
			},
			fairness: {
				heading: 'The four fairness measures (votes added)',
				p1: 'Now add the 2023 election-day votes and ask: how does each map turn votes into seats? Four standard measures, each checked against the million neutral maps.',
				li1: "<strong>1. Seats at a tied vote.</strong> The most intuitive test. Pretend the province votes exactly 50/50 and count each side's seats. On Alberta's geography a typical neutral map gives the UCP about 44.8% of seats at a tie. City NDP votes are used a little more efficiently, so a tie naturally favours the NDP slightly. The majority map gives the UCP 46.1%: 78th percentile, ordinary. The minority map gives the UCP <strong>51.7%</strong>, a majority of seats while tied in votes. Only 69 of the 1,010,000 neutral maps do better for the UCP. For scale, a procedure told to <em>deliberately</em> maximize UCP seats reached 52.9%. The minority map sits closer to that engineered ceiling than to the neutral middle.",
				li2: '<strong>2. The efficiency gap.</strong> Every vote is either needed to win a seat or "wasted" — cast for a loser, or piled onto a winner beyond what victory required. This measure compares how fast each party\'s votes are wasted. The majority map scores +0.1%: essentially nothing. The minority scores +4.0% in the UCP\'s favour, the 94.5th percentile, just <em>under</em> the audit\'s pre-set alarm line at the 95th. This is the one measure that did not fire. The audit reports it as a miss.',
				li3: "<strong>3. The mean-median gap.</strong> Compare a party's average district result with its middle district result. When the two drift apart, votes are being bunched into blowouts somewhere. The minority map's gap favours the UCP more than 99.9% of neutral maps. The majority's gap leans the other way, toward the NDP, further than 99% of neutral maps. The audit reports that outlier; it has no tested explanation.",
				li4: "<strong>4. Declination.</strong> A geometry reading of win margins: does the map treat the two parties' wins alike, or does it bend at the 50% line? The minority map bends further in the UCP's favour than about 98.8% of neutral maps. The majority map reads normal.",
				p2: 'Score: three of four fire on the minority map, all in the same direction. The fourth lands just under the line, pointing the same way. The majority map is ordinary on three. On the fourth, the mean-median gap, it is an outlier toward the NDP.'
			},
			odds: {
				heading: 'What "1 in 568,000" means — and why the audit doubled its margin',
				p1: "Combine the four fairness measures into one score and ask: how often does neutral drawing produce a profile as extreme as the minority map's? None of the 1,010,000 neutral maps did. A statistical model fitted to them estimates about <strong>1 in 1.1 million</strong>: an extrapolation, not a count. The audit does not quote that number. It quotes <strong>1 in 568,000</strong> — exactly half as impressive. A more cautious version, which allows for near-copies in the chain, gives about 1 in 450,000. Here is why the audit doubles.",
				p2: 'The audit looked for a signal in two different places: this combined score, and a second test on the specific boundary choices. Looking in two places gives luck two chances. Think of lottery tickets: buy two, and your odds of holding a winner double. So before quoting the odds, the audit doubles them against itself. That way, "you had two tries" is already paid for.',
				p3: 'The doubling has one more virtue: it holds whether the two tests are related or not. It does not remove the model\'s own assumptions, which is why the more cautious figure is given too.',
				p4: 'One caution the audit repeats everywhere: these odds measure how unusual the <em>map</em> is. They are not the odds that anyone acted with intent. A rare map could still, in principle, be honest work. The odds say only this: neutral drawing almost never produces this map.'
			},
			died: {
				heading: 'The tests that died',
				p1: 'Two tests failed, and both stay on this page. That is on purpose: an audit that only shows you its wins is advertising.',
				li1: '<strong>The city-limits test</strong>, last of the structural tests, found nothing to separate the maps: both follow municipal lines about as often as the 2019 map (75%).',
				li2: '<strong>The boundary-choices test (SZAT)</strong> looked significant until the audit corrected it for a simple fact: neighbouring places vote alike. Treating neighbours as independent flatters the result. After the correction, the test showed nothing. It was retired.'
			},
			break: {
				heading: 'Trying to break our own result',
				p1: 'Before trusting the headline, the audit attacked it three ways.',
				li1: '<strong>Swap the engine.</strong> Rerun the four fairness measures with a structurally different map-drawing algorithm (a spanning-forest method, promised in public before running). Every result moved by less than one percentile point, within the run\'s own margin of error; the run fell short of its sample target. The finding survived.',
				li2: "<strong>Swap the software.</strong> A different sampler, in the R language, drew 5,000 maps; none reached the minority map's value.",
				li3: '<strong>Test the mechanism — and fail.</strong> The audit guessed that the strange shapes from the structural tests were the direct cause of the seat advantage. That guess failed its test. The shapes and the seat lean point at the same map, but the shapes are not the engine. The audit says so.'
			},
			prereg: {
				heading: 'Promises made in advance',
				p1: "The strongest defence against fooling yourself is to write your predictions down before you look. The audit wrote its tests, thresholds, and predicted directions into time-stamped records: commits in its public repository and, from May 6, 2026, registrations on the Open Science Framework. Its random seeds were fixed in the code on April 27, before the official map files arrived; that record is a repository commit, not an OSF registration. The first OSF registrations came about six hours after the files arrived, and the audit's records say which came after. When a locked prediction missed, it stayed a miss. The May 6 registration predicted the minority map would favour the NDP and spread population less, built on a mistake about who nominated whom; both predictions missed. The rules that decide the November verdict were fixed in June 2026 and will be run, unchanged, on the panel's 91-seat map. The audit also names which of its results are <em>exploratory</em> (seeds locked, but the exact test combination chosen later) and which are pre-registered. The headline odds are exploratory. The November verdict rules were fixed in advance; they are dated in the repository, not on the OSF."
			},
			reproduce: {
				heading: 'Run it yourself',
				p1: 'Every number from the audit\'s analysis comes from a script in the public repository run against committed data. The full recipe is in <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/docs/REPRODUCING.md" rel="noopener">REPRODUCING.md</a>; the short version:',
				p2: 'A hosted notebook version runs in the browser via <a href="https://colab.research.google.com/github/Ixby/alberta-electoral-boundaries-audit/blob/master/notebooks/alberta_audit_explorer.ipynb" rel="noopener">Google Colab</a>. The full methodology — including every correction along the way — is in the <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">academic monograph</a>.',
				cross_ref: 'Companion pages: <a href="__BASE__/law">What the law asks of an electoral map</a> · <a href="__BASE__/norms">What the norms ask</a> · <a href="__BASE__/explainers">The fourteen explainers (Appendices A–N)</a>, one for each finding in the main report.'
			}
		},
		norms: {
			head_title: 'What the Norms Ask · Alberta Electoral Boundary Audit',
			head_description: "The third lens on Alberta's 2026 boundary episode: where the politicians-don't-draw-their-own-districts norm came from, what it bought, the case for setting it aside, and who is actually accusing whom of what.",
			back: '← Back to audit',
			site_label: 'Alberta Electoral Boundary Audit',
			h1: 'What the Norms Ask of an Electoral Map',
			meta: 'Plain-language companion · Not a verdict on anyone',
			standfirst: 'Alberta\'s boundary episode has three lenses. The <a href="__BASE__/law">law</a> asks what is legal. The <a href="__BASE__/methods">statistics</a> ask what is unusual. The third lens asks what is customary, and custom is the contested ground. "The government broke a sixty-year norm" is not a neutral measurement. It is the heart of the opposition\'s accusation. So this page does not just recite the norms. It cross-examines them: where they came from, what they are for, what the case for setting them aside actually is, and what remains once the rhetoric on both sides is cleared away.',
			the_norm: {
				heading: 'The norm, stated plainly',
				p1: "Politicians do not draw their own districts. Canada spent roughly sixty years building that rule, not as a law but as a practice. Since the federal reform era of the 1960s, the federal process and the provinces moved to arm's-length boundary commissions, with exceptions including Alberta in 1992 and Quebec in 2026. The person who will run in a district does not hold the pen that draws it.",
				p2: "The norm exists because of what came before it. Governing parties once routinely drew their own ridings, and the conflict of interest is not subtle. A map-drawer who must win under the map has every reason to draw it in his own favour, and no one watching can tell an honest line from a self-serving one. The commission model does not make maps perfect. It makes the drawer's interest separable from the outcome. That is what lets everyone else trust the result."
			},
			what_it_bought: {
				heading: 'What the norm bought, in this very cycle',
				p1: 'The 2025–26 commission is the norm\'s own best exhibit. It held hearings in sixteen communities. It received 1,345 written submissions. It published an interim proposal, took criticism, and reversed itself on the strength of eighty-plus submissions. That is the system visibly responding to public input. Whatever else the commission failed at, the process around it worked exactly as designed: in public, on the record, and answerable to what citizens said.'
			},
			the_departure: {
				heading: 'The departure: the map goes to a committee of MLAs',
				p1: "In April 2026, weeks after the split commission filed two incompatible maps, the Legislative Assembly set both aside. Government Motion 37, passed April 21, handed the work to a committee of six MLAs, four from the governing party, chaired by a government member. The committee was not required to hold public hearings, and it held none. An advisory panel drew the map and reported on October 22. On October 28 the committee voted 3–2 to end its review without observations. No draft was published for public challenge, and NDP members said the panel took no public submissions.",
				p2: "In May, Duane Bratt, Professor of Political Science at Mount Royal University, described the move to the author as without precedent in Canada. That stands. Alberta's own 1992 committee is a different case. That commission deadlocked, the Opposition refused to take part in the committee that followed, and in 1994 the Court of Appeal let the map stand. Secondary accounts say it faulted the committee for being unable to explain several of its boundaries; the audit has not read the judgment. The Act was amended in 1995. In 2026 a commission majority signed a report, which the Act treats as the commission's report, and it was set aside anyway. What it <em>means</em> is where the argument starts."
			},
			steel_man: {
				heading: 'The case for setting the norm aside — taken seriously',
				p1: "An audit that only rehearses one side's outrage is not checking anything. So take the government's side at full strength. Build its strongest case, the steel-man, before testing it:",
				li1: "<strong>The commission failed at its one job.</strong> The commission model promises a single arm's-length answer. This commission delivered two incompatible maps and a majority publicly accusing colleagues of bad faith. When the independent route splits, someone has to decide. The statute says who.",
				li2: "<strong>The statute gives the legislature the pen by design.</strong> Under Alberta's Act, a commission report has no legal force. Boundaries change only when the Assembly passes an Electoral Divisions Act. Government Motion 37 used a door the law built on purpose. Nothing was smuggled.",
				li3: '<strong>Elected members answer to voters; commissioners answer to no one.</strong> The oldest argument for legislative control is accountability. An MLA who draws a self-serving map can be voted out. A commissioner cannot.',
				li4: '<strong>The committee is not a purely partisan instrument.</strong> Two of its six members are opposition MLAs. An advisory panel drafted the proposal. That panel included two opposition nominees and was chaired by a retired Court of Appeal justice. It split: its report includes a minority opinion.',
				li5: "<strong>The government cited the chair's own recommendation.</strong> Its stated justification for the committee's 91-seat mandate was Recommendation 5, written by the commission chair himself, which says its change “would need to be studied by an all-party Select Special Committee or other equivalent Legislative Committee.” And it told the House exactly that: “We are adopting the recommendations from the report.”"
			},
			where_it_bends: {
				heading: 'Where the steel-man bends',
				p1: 'Each of those points is real. The documented record also pushes back on each:',
				li1: 'The split explains <em>replacing</em> the maps. It does not explain <em>removing the public</em>. Recommendation 5 itself proposed an all-party select committee for a two-seat fix; Motion 37 used that vehicle for a wider redraw. A hearing requirement, a published draft, or a binding panel would have answered the split too. The chosen vehicle forfeits each transparency feature the comparative literature treats as protective. The split forced none of those forfeits.',
				li2: '"The statute allows it" is the law lens, and it is answered there: the Act sets no rule for what the Assembly does if it does not approve a commission\'s report. The norms question is different. Some jurisdictions make a commission\'s map effective <em>unless</em> the legislature overrides it. Alberta\'s reversed default means the governing party always controls whether any commission map becomes law. Lawful and customary are different questions.',
				li3: 'The accountability argument proves too much. It argues against boundary commissions everywhere. Yet Canadian jurisdictions — and the UK, and Australia — moved the other way, with rare exceptions such as Alberta in 1992 and Quebec in 2026, precisely because election-time accountability is weak protection against a map designed to shape those same elections.',
				li4: "The panel drafts; a government-majority committee reviews and forwards; the Assembly's majority decides. Bipartisan advice with a government-controlled decision is a different institution from an independent commission. The difference is exactly the norm at issue.",
				li5: "Recommendation 5's author wrote it to dissuade the legislature from adopting the minority map, and his majority colleagues did not endorse it. It is also specific. It leaves Airdrie, Calgary and everything south of them exactly as the majority drew them (Drumheller-Stettler alone excepted), the very lines the commission split over, and nothing in the committee's mandate holds the committee to those lines. Citing a recommendation against its author's stated purpose is a documented tension, not a resolved one.",
				li6: 'The other document the government read onto the floor of the House — page 58 of the majority report — laments the two-seat cap. But the remedy attached to it is for the Legislature to give <em>future commissions</em> the power to set seat counts. The motion took that latitude now, for a committee of MLAs, while declining the report’s operative request: adopt the 89-seat map.'
			},
			whose_accusation: {
				heading: 'Whose accusation is it?',
				p1: 'Here is the separation this page exists to make: fact from judgment. The following are documented facts. The departure happened, and it has no Canadian precedent. The transparency features were forfeited. The commission\'s majority called one minority boundary a "bad faith effort" in a public statutory document. The Canadian Civil Liberties Association publicly <a href="https://ccla.org/press-release/ccla-sounds-the-alarm-over-the-politicization-of-albertas-electoral-map/" rel="noopener">raised the politicization concern</a>. The opposition voted against the motion. And the accusations run both ways. The minority report charges the majority with “an inclination to delete or mangle rural electoral divisions and, in effect, reduce effective rural representation” — rural representation being, in the minority\'s own words, “not merely a question of numbers; it is a question of access, voice, and practical governability” (p. 356). The audit found that charge and tested it the same day (exploratory; the hyphen-robust classifier and every classified name are published with the finding). The direction reverses. The minority map keeps fewer rural-anchored divisions than the majority (23 vs 28 against 2019\'s 31) and absorbs more of 2019\'s rural divisions into city-named districts (seven vs three). Both maps thin rural representation relative to 2019, so the charge\'s core observation is real. But on the measure the accusation names, it lands on its author. Its companion charge, that the majority declined to use the Act\'s ±25% flexibility for rural Alberta, was tested the same day and holds. The majority drew its rural divisions near population parity; the minority drew them light. One charge reversed, one supported, both published. The audit discounts the majority\'s flags on the minority map because they come from one side of a split commission. The same discount applies here too, in both directions.',
				p2: "The following is <em>not</em> a documented fact. It is a political judgment: that the departure was illegitimate. That judgment depends on how much deference the norm deserved in the face of a split commission, and reasonable people weigh that differently. The audit documents the departure and its costs. It does not carry the opposition's conclusion, and nothing in the audit's statistics can carry it either. A number can say a map is rare. It cannot say a process was wrong."
			},
			norms_vs_law: {
				heading: 'Norms are not law — and one place turned the norm into law',
				p1: 'Could a court enforce the norm? Not while it stays a norm. Constitutional conventions, the unwritten rules of political behaviour, bind politically, not judicially. The Supreme Court said so in the 1981 Patriation Reference, and courts have held that line since: a court may name a convention and will still decline to enforce it. That gap, between what is customary and what is compellable, is where this entire episode lives.',
				p2: "Quebec shows the other choice: it wrote the norm into law. Its boundary commission is permanent and independent, and on the map itself the commission ordinarily has the last word. When Quebec's government tried to freeze its commission by legislation, the courts <em>did</em> act, because a law was now in play. On April 22, 2026, the Supreme Court of Canada upheld, 7–2 and from the bench, the ruling that the freeze violated the Charter's democratic-representation guarantee. Its reasons followed on May 1 (<em>Quebec (AG) v. Lalande</em>, 2026 SCC 13). Where the norm was written into law, it became enforceable. Alberta's norm never was, and so it wasn't. The contrast cuts both ways, though. Even in Quebec, on June 12, 2026, the National Assembly passed its own 127-seat map."
			},
			measurable: {
				heading: 'The process scorecard: making the norms question measurable',
				p1: "Rhetoric about norms is cheap in both directions. The audit's answer is a third scorecard. The structural tests and the statistics measure the maps. This scorecard measures the <em>process</em>, on nine protective features the sixty-year practice guaranteed. Each is a yes-or-no question answerable from public documents, and the same nine score every process this audit examines.",
				table: {
					head: {
						feature: 'Protective feature',
						commission: 'Commission process',
						committee: 'Committee process (as constituted)'
					},
					arms_length_drafting: {
						feature: "Arm's-length drafting",
						commission: 'Yes',
						committee: "Partial — the panel drafts; a government-majority committee reviews and forwards it; the Assembly decides"
					},
					public_hearings_before: {
						feature: 'Public hearings before adoption',
						commission: 'Yes — sixteen communities',
						committee: 'No — none held on the map'
					},
					draft_published_challenge: {
						feature: 'Draft published for challenge',
						commission: 'Yes — interim proposal revised in public',
						committee: 'No — none published'
					},
					new_public_submissions: {
						feature: 'New public submissions accepted',
						commission: 'Yes — 1,345 received',
						committee: "No — none taken; the panel had access to the commission's archive"
					},
					demonstrated_responsiveness: {
						feature: 'Demonstrated responsiveness',
						commission: 'Yes — reversed itself on 80+ submissions',
						committee: 'Pending'
					},
					neutral_chair_deciding: {
						feature: 'Neutral chair of the deciding body',
						commission: 'Yes — a judge, appointed by cabinet',
						committee: 'No — a government MLA chairs the reviewing committee, and the Assembly\'s majority decides; the retired judge chairs only the panel'
					},
					opposition_deciding_body: {
						feature: 'Opposition in the deciding body',
						commission: 'Yes — two of five',
						committee: 'Yes — two of six'
					},
					published_reasons_contested: {
						feature: 'Published reasons for contested choices',
						commission: 'Yes — both reports',
						committee: 'Pending'
					},
					precedent_conformity: {
						feature: 'Precedent conformity',
						commission: 'Yes',
						committee: 'No — no Canadian precedent; Alberta\'s 1992 committee followed a deadlocked commission'
					},
					count: {
						feature: 'Count',
						commission: '9 of 9',
						committee: '1 Yes · 1 Partial · 5 No · 2 Pending'
					}
				},
				p2: "One more way to see this scorecard: it is the <em>third axis</em>. The audit's chart plots every map on two dimensions: structure and statistics. All three maps plotted so far (the majority, the minority and the current map) were drawn by commission processes that score nine of nine here, so the third axis has had nothing to separate. The November map will be the first point in the audit's history with a different process score behind it.",
				p3: "Read the table honestly, in both directions. The commission scores nine of nine <em>by construction</em>. The criteria describe the institution the norm built, and the commission was that institution. The informative part was the committee's to decide. Four of its No and Pending cells were features it could have added before it reported: hearings, a published draft, new submissions, and the responsiveness they make possible. It added none of them. On October 28 it voted 3–2 to end its review without observations, and it held no further meetings.",
				draft_note: 'Status matters here: this scorecard\'s criteria, sources, and predicted directions are <a href="https://osf.io/u47bq/" rel="noopener">registered on the OSF (u47bq, July 14, 2026)</a> — frozen in July 2026, months before the committee reported. It was written mid-episode by an author whose earlier findings you have just read — a bias risk the <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/preregistration/lane3_process_scorecard_draft.md" rel="noopener">registered document</a> discloses rather than hides. Signed errata (Amendment 5, Part 25, November 1, before any committee map was seen) correct some of its facts, such as the committee\'s size. They change no criterion or verdict, and the OSF text is unchanged. Applied backward to the commission, it is description, not prediction. When the panel\'s map lands, the same locked map tests run unchanged — and this scorecard rates the process that produced it. At that point the norms debate stops being a shouting match about tradition and becomes a scored comparison: did the committee behave like the institution it replaced?'
			},
			audits_standing_rule: {
				heading: "The audit's standing rule",
				p1: 'Same rule as everywhere else on this site. The audit documents what happened, how rare it is, and who claimed what. Whether the norm deserved to survive the split — and what its setting-aside should cost at the ballot box, if anything — belongs to readers and voters. Not to a statistical audit.',
				cross_ref: 'Companion pages: <a href="__BASE__/law">What the law asks of an electoral map</a> · <a href="__BASE__/methods">How the maps were tested</a>',
				disclaimer: 'This page is a plain-language companion to the audit, written for orientation. It is not legal advice, and it is not a verdict on any person or party.'
			}
		},
		law: {
			head_title: 'What the Law Asks · Alberta Electoral Boundary Audit',
			head_description: "How Canadian law evaluates an electoral map: Charter s.3 effective representation, the Saskatchewan Reference, and Alberta's Electoral Boundaries Commission Act — and how this audit's evidence relates to those tests.",
			back: '← Back to audit',
			site_label: 'Alberta Electoral Boundary Audit',
			h1: 'What the Law Asks of an Electoral Map',
			meta: 'Plain-language companion · Not legal advice',
			standfirst: "This audit measures maps. Courts judge them. The two jobs are related, but they are not the same, and this page walks through the difference: what Canadian law actually asks of an electoral boundary, which questions belong to a court rather than to a statistician, and where the audit's evidence fits. The audit itself takes no position on any legal conclusion. It reports what the data show, and it stops there.",
			why_not_gerrymander: {
				heading: 'Why this audit never rules "gerrymander"',
				p1: 'The audit uses "gerrymandering" throughout in its everyday political sense: manipulating electoral boundaries for partisan advantage. But in Canadian law the word has no legal definition. There is no statute to violate by "gerrymandering" and no court test with that name. A map cannot be found guilty of a category that does not exist. That is one reason the audit refuses to issue that verdict, no matter what the numbers say.',
				p2: 'The American contrast is worth a moment, because most of this audit\'s statistical tools — the efficiency gap, neutral map ensembles (large sets of computer-drawn maps) — were invented for American fights. In the US, partisan gerrymandering is at least a named claim. But the US Supreme Court shut the federal courthouse door in <em>Rucho v. Common Cause</em>, 588 U.S. 684 (2019), holding that federal courts lack "judicially discernible and manageable standards" to judge such claims. The same metrics remain live in some US state courts, most prominently in <em>League of Women Voters v. Commonwealth</em>, 178 A.3d 737 (Pa. 2018).',
				p3: 'Canada took a different path. Instead of a gerrymandering test, Canadian law asks two answerable questions. Does the map deliver <a href="#effective-representation">effective representation</a> under section 3 of the <em>Charter</em>? And did the commission comply with <a href="#ebca">its governing statute</a>? The audit\'s findings are evidence a court could weigh inside those two inquiries. Inputs, not a verdict on either. And statistics cannot read minds: boundary geometry can show what a map <em>does</em>, never what its drafters <em>intended</em>.'
			},
			effective_representation: {
				heading: 'The constitutional test: effective representation',
				p1: 'Section 3 of the <em>Charter of Rights and Freedoms</em> guarantees citizens the right to vote. In <em>Reference re Provincial Electoral Boundaries (Saskatchewan)</em>, [1991] 2 SCR 158 — the audit calls it the <em>Saskatchewan Reference</em> — the Supreme Court of Canada held that what s.3 protects in boundary-drawing is not one-person-one-vote arithmetic but <strong>effective representation</strong>.',
				p2: 'Writing for the majority, McLachlin J. explained that "relative parity of voting power" is the starting point. But it must be weighed against permissible deviations for geography, community history, community interests and minority representation. The Court deliberately set no bright-line tolerance, no fixed number for how far a district may stray. A deviation from strict population equality is constitutionally defensible <em>if the non-numeric factors justify it</em>.',
				p3: "Two consequences follow, and both cut against overreading this audit's numbers:",
				li1: "<strong>Partisan asymmetry alone does not make a map unconstitutional.</strong> Under the case law reviewed in the audit's academic monograph, a statistical tilt must be paired with something more — population deviations not justified by geography or community of interest, or evidence those same factors were invoked to rationalize a partisan outcome rather than to serve their statutory purpose. The audit's structural tests (population spread, city splits, boundaries the commission's majority flagged) exist precisely because the law asks about that pairing.",
				li2: '<strong>Courts defer to commissions.</strong> The standard is a deferential "reasonable commission" review, not a search for the best possible map. In <em>Raîche v. Canada (Attorney General)</em>, 2004 FC 679 — the closest reviewed case to a boundary challenge on community-of-interest grounds — the Federal Court found <em>no</em> Charter s.3 violation. The violations it did find were statutory (the federal boundary statute\'s community-of-interest duty). The court set aside the commission\'s decision for the districts in dispute and suspended its ruling for a year, and the fix came through Parliament. It is a trial-level decision on the federal statute: persuasive, not binding, for any Alberta challenge.',
				p4: "Where does the audit sit in that framework? Its measurements are inputs a court could weigh in the effective-representation analysis: how far each map's partisan metrics sit from a million neutral alternatives, how population variance is distributed, where boundaries depart from municipal lines. No metric, and no combination of metrics, is a proxy for the test's outcome. When the audit reports that several indicators point the same way, that is a statement about an empirical pattern. It is not a legal conclusion."
			},
			ebca: {
				heading: "The statute: Alberta's Electoral Boundaries Commission Act",
				p1: "Alberta's commissions are governed by the <em>Electoral Boundaries Commission Act</em>, RSA 2000, c. E-3 (the EBCA). Three of its rules matter most for reading this audit.",
				p2: "<strong>The population band.</strong> As a general rule, each proposed electoral division must stay within ±25% of the provincial average population. Both 2026 proposals comply. Apart from the three divisions each map protects under the s.15(2) exception described next, every district sits inside the band. The largest deviation on the high side (+24.06%, in the minority map) comes within a point of the cap without crossing it. Inside that generous band the commission has wide discretion, and the audit's population findings (the minority's population spread, 48% wider than the majority's on the commission's own tables, and the NE/central Calgary crowding) all describe choices made <em>within</em> the legal band. On 2021 census counts, the three maps' average deviations come out almost the same. Legal and unusual are different questions.",
				p3: '<strong>The s.15(2) exception.</strong> For at most four divisions, the population may fall as much as 50% below the average — if the commission is of the opinion that at least three of these five criteria exist:',
				criterion1: 'area over 20,000 km² (or total surveyed area over 15,000 km²);',
				criterion2: "more than 150 km from the Legislature Building to the division's nearest boundary, by the most direct highway;",
				criterion3: 'no town in the division over 8,000 people;',
				criterion4: 'the division contains an Indian reserve or a Métis settlement;',
				criterion5: "part of the boundary runs along Alberta's provincial border.",
				p4: "The provision is permissive: meeting the criteria makes a division eligible, but never obliges the commission to use the allowance. Both 2026 maps invoke s.15(2) for three divisions each. The audit checked all six invocations against the statutory thresholds and found every one eligible. The controversy the audit documents is not eligibility. It is a drawing choice. The minority's Rocky Mountain House–Banff Park division picks up one qualifying criterion, the provincial-border one, only by extending through uninhabited national-park land. On that choice, the commission's own final report (March 23, 2026, p. 10) speaks for itself. The majority commissioners write:",
				quote: '"They propose to retain an electoral division of \'Rocky Mountain House-Banff Park\' by artificially extending its boundary to the province\'s western border with British Columbia (taking part of Banff National Park, where no one lives), which is a bad faith effort to ensure it can be protected under s. 15(2) of the Act."',
				p5: 'That characterization — including the phrase "bad faith" — belongs to the three majority commissioners, the chair among them, and was made in a public statutory document. It is not the audit\'s. The audit\'s own analysis found the division qualifies under s.15(2) even without the extension. Quoting them records what the primary source says. It does not record what any commissioner intended.',
				p6: "<strong>What a commission report is — and is not.</strong> Under the EBCA, the commission's report has no legal effect by itself. Boundaries change only when the Legislative Assembly passes a separate Electoral Divisions Act. Some jurisdictions make a commission's map effective unless the legislature actively overrides it. Alberta's default is reversed: the governing party controls whether any commission map becomes law. The Act's rules on hearings, deadlines and the ±25% band are addressed to the commission. Nothing in the Act governs what the Assembly does instead, and it sets no minimum notice or public-comment period. Government Motion 37, passed April 21, 2026, set both commission maps aside. It handed the work to a committee of six MLAs, four from the governing party, which had to report by November 2, 2026. Alberta handed a map to MLAs once before, in 1992. That commission had deadlocked; this one had not. In 1994 the Court of Appeal upheld the 1992 map; secondary accounts say it faulted the committee for being unable to explain several of its boundaries, though the audit has not read the judgment. The audit documents the motion's process choice as a finding about procedure, separate from and additional to anything the maps' geometry shows.",
				cross_ref: 'The full legal analysis — including the case-law review, the commission-deference literature, and the procedural comparison with other provinces — is in the academic monograph, §2 and §5.9, at <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">the audit repository</a>.'
			},
			audits_standing_rule: {
				heading: "The audit's standing rule",
				p1: "Every version of this audit carries the same rule. It may report what the tests show. It may say how unusual a map is against a neutral baseline. But it does not declare any map a gerrymander, does not infer intent from geometry, and does not pronounce on constitutional or statutory compliance. Those are questions for courts, commissions, and readers, with the audit's evidence on the table.",
				cross_ref: 'Companion pages: <a href="__BASE__/methods">How the maps were tested</a> — every test and statistic in plain language — and <a href="__BASE__/norms">What the norms ask</a> — the third lens, on custom and its cross-examination.',
				disclaimer: 'This page is a plain-language companion to the audit, written for orientation. It is not legal advice, and nothing here should be relied on as a legal opinion.'
			}
		},
		privacy_policy: {
			head_title: 'Privacy Policy · Alberta Electoral Boundary Audit',
			head_description: 'Privacy and data retention policy for the Alberta Electoral Boundary Audit.',
			back: '← Back to audit',
			site_label: 'Alberta Electoral Boundary Audit',
			h1: 'Privacy & Data Retention Policy',
			meta: 'Effective: 2026-11-03 · Maintained by Will Conner',
			overview: {
				heading: 'Overview',
				p1: "This tool is a public-interest audit of Alberta's 2025–26 electoral boundary commission process. It is not a commercial product and runs no advertisements. This page explains what the analytics measure, what they never collect, and why none of it can be tied back to you. It also says what the feedback form keeps.",
				p2: 'The short version: the site uses cookieless, aggregate analytics. There is no tracking cookie, no advertising, no cross-site profiling, and no identifier that follows you. Because the analytics store nothing personal, there is no consent banner to click through — the privacy protection is built into how the measurement works, not bolted on as a prompt.'
			},
			how_analytics_work: {
				heading: 'How the analytics work',
				p1: 'When a page loads or you interact with the map, the site sends a small, anonymous event to a counting service we run. Each event is just the name of what happened — for example, "page viewed" or "district selected" — plus a few coarse details about the action. The event carries no name, no email, no account, and no identifier stored on your device.',
				p2: 'To count how many distinct people visited on a given day without identifying anyone, the counting service combines your network address and browser type and runs them through a one-way cryptographic hash together with a secret that changes every day. The result is a short code that lets us tell two visits apart <em>within</em> a single day, and nothing more. The original address is never stored — only the hash is. Because the secret rotates daily, the same visitor produces a different code tomorrow, so no one can follow a visitor across days. When a new day\'s secret is made, the old one is deleted. After that, no one can work backwards from a code to a person.',
				p3: 'We are interested in the picture that visitors paint as a group — which findings get read, which maps get opened, which districts draw attention. We are not interested in you specifically, and the measurement is built so that "you specifically" is not something the data can express.'
			},
			measured: {
				heading: 'What is measured',
				p1: 'The analytics record aggregate, anonymous events such as:',
				li1: 'Page views',
				li2: 'How far down a page people scroll, in coarse bands (25%, 50%, 75%, 100%)',
				li3: 'Roughly how long the page was actively on screen, in coarse time buckets',
				li4: 'Which finding sections come into view as people read',
				li5: 'Which maps are opened in the explorer, and which districts are selected',
				li6: 'Which map layers are turned on or off, and roughly how far in people zoom',
				li7: 'Which points of interest or report links are opened',
				li8: 'A coarse picture of your setup — screen-size band (such as phone, tablet, or desktop), form factor, and browser family (such as Chrome, Safari, or Firefox). The analytics never store your exact screen dimensions or full browser identification string.',
				li9: 'A one-time snapshot of how the map explorer performed when it first drew — for example, the load time in coarse bands and a rounded memory figure. This helps us tell whether the explorer is fast enough on real devices. The numbers are deliberately banded, not exact, so they describe a device class rather than a device.',
				p2: "Each of these is stored as a separate event that carries no identifier except that day's code, and is reported only in aggregate. There is no per-person profile, no session replay, and nothing that links one day's visits to the next. We see totals and distributions, not people."
			},
			never_collected: {
				heading: 'What the analytics never collect',
				p1: 'The analytics collect no name, no email and no account. No advertising identifier. No stored IP address — your network address is hashed with a daily-rotating secret and immediately discarded; only the daily code is kept, and it changes every day. No raw browser fingerprint. No cross-day or cross-site identifier. No precise location. No cookie or browser-storage identifier that marks you as a returning visitor for analytics purposes.'
			},
			github_pages_collects: {
				heading: 'What GitHub Pages collects',
				p1: 'This site is hosted on GitHub Pages. GitHub\'s servers automatically log basic request details when any page loads — your IP address, browser type, referring page, and timestamp. We do not receive or control these logs; they are governed by <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener noreferrer">GitHub\'s Privacy Statement</a>. We have no relationship with GitHub beyond hosting. The analytics described above run separately and never store your IP address.'
			},
			share_codes: {
				heading: 'Share links',
				p1: 'The map explorer has a Share feature. It writes your current map view — which maps are on, which overlays are showing, roughly where your viewport sits — into the page\'s web address, and Copy link puts that address on your clipboard so you can send it to someone. The link describes a map configuration, not a person. Two people who arrive at the same view independently get the same link; that is expected, and nothing in it ties them together.',
				p2: "Because the view lives in the address, it goes wherever web addresses go: into your browser history, and to GitHub's servers when someone opens the link. The analytics never see it. They record only which page was viewed, not the view in its address.",
				p3: 'Nothing is saved when you share. The link carries the whole view itself, so no database is needed to make it work, and we keep no record of who shared what. Copying a link sends nothing to the analytics.'
			},
			cookies_browser_storage: {
				heading: 'Cookies and browser storage',
				p1: 'The analytics use no cookie and no browser-storage identifier. Nothing about the measurement marks you as a returning visitor.',
				p2: 'The site does set one small <strong>functional</strong> cookie to remember your own preferences between visits. It is not used for analytics or tracking, and it never leaves your browser in readable form. It stores:',
				li1: '<strong>Colour theme</strong> — dark or light, if you changed it',
				li2: "<strong>Intro dismissed</strong> — so the map introduction doesn't repeat",
				li3: '<strong>Current map view</strong> — so your last view is restored if you come back within ten minutes',
				li4: '<strong>Browser language</strong> — so the site can show your preferred language',
				p3: "This cookie holds only the preferences above — no personal or identifying information. Its contents are scrambled with a key that ships inside the page, so the stored value is not human-readable; because that key is public, treat this as tamper-resistance rather than true secrecy. It is sent only over HTTPS, is never shared with other sites, and you can remove it at any time by clearing your cookies. The site is served as static files, so nothing on the server side reads it. Your colour theme is also mirrored to your browser's local storage so the correct theme can be applied instantly on load, before anything flickers; that value too is purely functional and never sent anywhere. If you choose a language, local storage keeps that choice the same way."
			},
			data_retention: {
				heading: 'Data retention',
				p1: 'The analytics records are anonymous by construction: the only identifier in them is the daily code described above. They are stored on infrastructure hosted in Canada (ca-central-1) and kept as research data. If we ever found that a record contained identifying information — which the design is built to prevent — we would delete it within 30 days.'
			},
			your_choices: {
				heading: 'Your choices',
				p1: 'Because the analytics collect nothing personal, there is nothing to opt out of and no consent prompt to manage. If you would still prefer to send no analytics events at all, a content blocker or a browser that blocks the request to the counting service will stop them, and the site will work exactly the same. You can also clear the functional preferences cookie at any time through your browser.'
			},
			contact: {
				heading: 'Contact',
				p1: 'Will Conner — independent research, not affiliated with or endorsed by any institution.',
				p2: 'The feedback form is separate from the analytics. It stores your message, the page and language you sent it from, and your name and email only if you give them. To limit repeat sending, it checks a hash of your network address made with a daily-changing secret. Messages are kept on the same Canadian infrastructure as the analytics records. Questions, corrections, and deletion requests, including deletion of a message you sent: please use the <a href="__BASE__/feedback">feedback form</a>. Requests are answered within 10 business days.'
			},
			policy_updates: {
				heading: 'Policy updates',
				p1: 'When this policy changes, the effective date at the top is updated and the change is committed to the <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit" target="_blank" rel="noopener noreferrer">public git repository</a>. The commit history is the changelog. Any change that expands what is collected is noted in the commit message.'
			}
		},
		home: {
			references: {
				academic: {
					commission_2026: '<strong>Alberta Electoral Boundaries Commission. 2026.</strong> <em>2025–26 Electoral Boundaries Commission Final Report (Majority and Minority)</em>. Government of Alberta.',
					chen_rodden_2013: '<strong>Chen, Jowei, and Jonathan Rodden. 2013.</strong> "Unintentional Gerrymandering: Political Geography and Electoral Bias in Legislatures." <em>Quarterly Journal of Political Science</em> 8(3): 239–269.',
					courtney_2001: "<strong>Courtney, John C. 2001.</strong> <em>Commissioned Ridings: Designing Canada's Electoral Districts</em>. Montreal and Kingston: McGill-Queen's University Press.",
					deford_duchin_solomon_2021: '<strong>DeFord, Daryl, Moon Duchin, and Justin Solomon. 2021.</strong> "Recombination: A Family of Markov Chains for Redistricting." <em>Harvard Data Science Review</em> 3(1). (The ReCom algorithm used to generate the 1,010,000-map ensemble.)',
					gelman_king_1994: '<strong>Gelman, Andrew, and Gary King. 1994.</strong> "A Unified Method of Evaluating Electoral Systems and Redistricting Plans." <em>American Journal of Political Science</em> 38(2): 514–554.',
					katz_king_rosenblatt_2020: '<strong>Katz, Jonathan N., Gary King, and Elizabeth Rosenblatt. 2020.</strong> "Theoretical Foundations and Empirical Evaluations of Partisan Fairness in District-Based Democracies." <em>American Political Science Review</em> 114(1): 164–178.',
					pal_2015: '<strong>Pal, Michael. 2015.</strong> "The Fractured Right to Vote." <em>McGill Law Journal</em> 61(2): 231–274. (Canadian constitutional framework for electoral boundaries.)',
					stephanopoulos_mcghee_2015: '<strong>Stephanopoulos, Nicholas O., and Eric M. McGhee. 2015.</strong> "Partisan Gerrymandering and the Efficiency Gap." <em>University of Chicago Law Review</em> 82(2): 831–900. (Source of the efficiency gap measure used throughout.)'
				},
				cases: {
					saskatchewan_reference: '<em>Reference re Provincial Electoral Boundaries (Saskatchewan)</em>, [1991] 2 SCR 158. (The leading Supreme Court of Canada authority on the constitutional standard for electoral boundary drawing.)',
					raiche: '<em>Raîche v. Canada (Attorney General)</em>, 2004 FC 679. (Federal Court; leading Canadian authority on community-of-interest evidence in electoral boundary disputes.)',
					rucho: "<em>Rucho v. Common Cause</em>, 139 S. Ct. 2484 (2019). (U.S. Supreme Court; establishes the non-justiciability of partisan gerrymandering claims in federal courts — context for why Canada's s.3 effective-representation standard differs.)"
				},
				statutes: {
					ebca: '<em>Electoral Boundaries Commission Act</em>, RSA 2000, c E-3.'
				}
			}
		}
	}
} as const;
