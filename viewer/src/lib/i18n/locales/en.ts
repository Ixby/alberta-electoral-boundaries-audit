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
		p_howfar: 'A computer drew 1.01 million legal versions of the map at random. One of the two real maps is more one-sided than all but about 1 in 350,000 of them, in the UCP’s favour. The other sits in the normal range.',
		aside_pre: 'You might call a map shaped like that ',
		aside_post: '. That word has no legal meaning in Canada, so we don’t use it as a verdict. We show you what the map does; you judge. For the deeper layers — what the law actually requires, and exactly how we ran the test — see ',
		box_heading: 'What we can and can’t say',
		box_can_1: 'The minority map sits outside what 1.01 million neutral maps produce, in the UCP-favoured direction.',
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
			'This site has been translated by AI. Some content may still appear in English while translations are in progress. If you notice errors or would like to help translate this project, please %s.',
		link_label: 'contact us',
		// {count} is replaced at runtime with the live word count of the
		// English prose, so volunteer translators know the size of the job
		// before raising their hand. Computed, never hardcoded — it stays
		// correct as the prose grows.
		word_count: 'For scale: the English prose runs about {count} words. You are welcome to contribute to all of it or just a portion \u2014 in most cases the work is correcting minor errors the machine made, not translating from scratch.'
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
				'"Gerrymander" is not a term Canadian courts use. But if it were — in the everyday sense most people mean by it — the evidence in this audit would reasonably support calling the <em>minority proposal</em>, if enacted, a heavily gerrymandered map. Four of the five structural tests this audit runs flag the <em>minority proposal</em> and none flag the alternative (the <em>majority proposal</em>); the fifth test is neutral for both.',
			footnote:
				'The "majority" and "minority" names come from a 3–2 split among the Electoral Boundaries Commission (chaired by Justice Miller), which produced two competing proposals rather than a single recommendation. The legislature has since set both aside and referred redistricting to a five-MLA committee chaired by Brandon Lunty (a Premier-appointed MLA); the committee oversees a separate four-person Independent Advisory Panel — two members nominated by the Premier (Hon. Monte Solberg and Darwin Durnie), two by the Leader of the Opposition (Dr. Gerard Kennedy and Brent Robinson) — tasked with producing a new 91-seat boundary proposal before the November 2026 deadline.'
		},
		q2: {
			heading: 'What does "gerrymander" mean in Canadian law?',
			body:
				"There isn't one. The Canadian test is different: whether the boundaries give voters <em>effective representation</em> under section 3 of the Charter. The minority proposal raises serious questions under the effective-representation standard; only a judge can answer them definitively, and no one has asked one yet."
		},
		q3: {
			heading: "What's at stake for Albertans?",
			body:
				"At a 50/50 provincial vote, the audit's measurements place the minority proposal at a structural extreme: fewer than 100 of the 1.01 million neutral comparison maps produce the same kind of seat imbalance. That imbalance matters because at 60 of 89 seats (a two-thirds supermajority) the governing party unlocks extraordinary procedural powers. It can waive standard notice periods and push public bills through multiple legislative stages in a single day, bypassing the deliberation checks the legislature normally relies on. Whether the minority proposal's tilt is large enough to push one party past that 60-seat threshold at vote shares <em>other</em> than 50/50 is a question this audit has not yet tested. Whether that imbalance is acceptable is a question for Albertans, not for this audit."
		},
		cta_law: 'Read the legal context →',
		cta_methods: 'See how we tested →',
		scorecard_h: 'The scorecard',
		scorecard_fig_alt:
			'Scatter plot: efficiency gap on the horizontal axis, count of structural tests failed on the vertical axis. The 2019 enacted map and the 2026 majority map cluster in the safe lower-left corner. The 2026 minority map appears alone in the upper-right outlier region.',
		scorecard_fig_caption:
			'Both lanes on one picture. Horizontal: how skewed the partisan-fairness number is (right = more UCP-favoured). Vertical: how many of five structural-fairness tests the map fails. Bottom-left is the safe corner where neutral procedures routinely land; the upper-right is the outlier region. The 2019 enacted map and the 2026 majority sit in the safe corner. The 2026 minority sits alone in the outlier region.',
		scorecard_intro:
			'Two independent measurements applied to both maps under the same pre-registered thresholds. Structure uses only the shape of the lines — no election results. Numbers tests how the lines convert votes into seats. Both lanes reach the same conclusion.',
		scorecard_close:
			'Two independent measurements, one answer. The convergence is the audit\'s strongest single signal.'
	},
	top_callouts: {
		gerrymander_lead: 'Is the minority map a gerrymander?',
		gerrymander_body: 'On the audit\u2019s joint partisan-bias score, the commission\u2019s minority map sits in the extreme tail of 1,010,000 algorithmically-drawn neutral comparison maps \u2014 approximately 66 of them reach its tipping-point seats@50/50 value, with a dependence-robust joint upper bound of roughly 1&nbsp;in&nbsp;350,000 under that reference distribution. The majority map falls well within normal range.',
		tldr_label: 'TL;DR',
		tldr_p1: 'Alberta\u2019s redistribution commission split 3&ndash;2 in 2026 and produced two different proposed maps. The government set both aside and assigned redistricting to a five-member committee of MLAs (the Lunty committee), expected to report in November 2026. Neither commission map is law.',
		tldr_p2: 'This audit tested both commission maps the same way, using 1,010,000 computer-drawn neutral maps built from the official Elections Alberta shapefiles as a reference point. The majority proposal sits within the neutral range on every pre-registered test. The minority proposal crosses four of five structural tests, and its partisan-fairness seat split at a 50/50 vote is reached by roughly 66 of those 1,010,000 neutral maps \u2014 a dependence-robust joint upper bound of roughly 1 in 350,000 under that reference distribution. The audit\u2019s efficiency-gap metric for the minority sits at the 94th percentile \u2014 <em>near, but below</em>, the audit\u2019s own 95th-percentile threshold.',
		tldr_p3: 'The audit measures outcomes, not intent. When the Lunty committee releases its map, this audit will apply the same tests to it.',
		tldr_footer: 'Pre-registered falsification conditions and retraction commitments are in %s.',
		tldr_footer_link: '\u00a79'
	},
	head: {
		title: 'Alberta Electoral Boundary Audit',
		meta_description:
			"Statistical audit of Alberta's 2026 electoral boundary commission — 1,010,000 neutral maps, official Elections Alberta shapefiles, pre-registered tests."
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
		notes: 'Notes',
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
		november: 'November',
		lunty: 'Lunty',
		invisible: 'Invisible',
		suggestions: 'Reform suggestions',
		retractions: 'Retractions',
		references: 'References',
		resources: 'Resources',
		technical: 'Technical resources'
	},
	hero: {
		h1: 'Alberta Electoral Boundary Audit',
		draft: '(UNPUBLISHED DRAFT — reviewers welcome)',
		subtitle:
			"Alberta's commission produced two riding maps in 2026. This audit compared them — using the same tests, applied equally to both — to ask whether they treat voters the same way.",
		badge: 'Official Elections Alberta maps — Published May 2026',
		cover_note: 'Click to zoom and explore all three boundary proposals simultaneously. Pin the viewport and flip between maps — boundaries shift, voters stay put. Scroll down for the analysis.',
		cover_note_1:
			'This map is the best way in. Click it to zoom and explore. The buttons at the top switch between the minority map, the majority map, and the 2019 enacted boundaries — or layer all three to see exactly where they diverge. <strong>Detail</strong> colours each polling area by how people voted in 2023; <strong>Trend</strong> adds partisan shading by district (blue UCP, orange NDP); <strong>Lines</strong> toggles boundaries on and off. <strong>Find</strong> jumps to any riding by name.',
		cover_note_2:
			"Try locking the viewport and flipping between maps — watch a boundary shift while the voters underneath stay still. The whole question, in one gesture.",
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
			"The minority map's geometry crosses 4 of 5 pre-registered structural thresholds <em>without using any election data at all</em>. The fifth (anchoring) is neutral. The majority crosses 0 of the 4 firing. These tests measure properties of the boundary lines themselves — district shape, municipal anchoring, population spread — and reach the conclusion before any vote is counted.",
		can_2:
			'Separately, when election data is brought in, the minority map sits at the 99.99th percentile of 1.01 million algorithmically-drawn comparison maps held to the same statutory rules. Roughly 66 of those 1.01 million neutral maps reach the same seats@50/50 value. The dependence-robust joint upper bound across the two analytical channels is approximately 1 in 350,000 under that reference distribution (p&nbsp;≤&nbsp;2.80×10<sup>−6</sup>). Two analytical instruments — geometric and statistical — reach the same conclusion in the same direction; the joint bound is the dependence-aware summary of that convergence, not four independent tests reading in agreement.',
		can_3:
			"Three of the configurations the minority proposal contains were flagged in writing by Commission Chair Justice Miller in §5.8.2 of the majority report and Appendix C. The audit's tests were run with no knowledge of his flags and surface the same regions. A third independent instrument — judicial — converges on the same boundaries.",
		cant_1:
			'The audit does <strong>not</strong> establish that any commissioner intended the partisan effects it measures. Boundary geometry cannot reveal intent.',
		cant_2:
			'The audit does <strong>not</strong> predict what the Lunty committee will choose, what the November 2026 vote will be, or how Albertans will react.',
		cant_3:
			'The audit does <strong>not</strong> predict how a court would rule if a Charter challenge were brought against either proposal.',
		cant_4:
			"The audit does <strong>not</strong> claim the dependence-robust bound of approximately 1 in 350,000 (p&nbsp;≤&nbsp;2.80×10<sup>−6</sup>) is the probability that a gerrymander occurred. That number is the tail probability of the minority's geometry under a neutral algorithmic null. It is evidence the neutral null is implausible. It is not a posterior probability of partisan intent — that question requires evidence the geometry cannot supply.",
		cant_5:
			"The audit does <strong>not</strong> tell any individual voter what position to take or what to do with this information. The choice is yours."
	},
	editorial_intro: {
		heading: 'What is redistricting, and why it matters',
		p1: 'Every voter in Alberta lives in an <em>electoral district</em> — a slice of the province that elects one person to the legislature. There are 87 districts. Each district elects one MLA. When you cast a ballot in a provincial election, you are choosing the MLA for the district you live in. For most Albertans, that is the whole connection to the legislature: one MLA, one district, one vote.',
		p2: 'Those district lines are not permanent. People move, neighbourhoods grow, rural areas thin out, cities sprawl. Every eight to ten years, Alberta is supposed to redraw the lines so each district is roughly the right size and reflects the way Albertans actually live now. The body that does the redrawing is the <em>Electoral Boundaries Commission</em> — an independent commission with judges, lawyers, and public members, not politicians.',
		p3: "This is the standard process. This time, the standard process produced something unusual. The commission's five members split 3–2 on what the map should look like, and rather than settling on one recommendation they produced two: a <em>majority proposal</em> (backed by three commissioners) and a <em>minority proposal</em> (backed by two). Both are sitting on the table — and the legislature has set both aside. A separate committee of MLAs chaired by Brandon Lunty — appointed by the Premier for this specific decision — now oversees a four-person Independent Advisory Panel, constituted under Government Motion 37 (passed April 21, 2026), tasked with producing a new 91-seat map. The legislature must approve whatever the committee delivers before November 2026.",
		p4: "Why it matters to you: the lines decide who your MLA is. They decide which neighbourhoods, towns, and concerns get represented together. If your city is split across four MLAs instead of one, no single representative is accountable for the city as a whole. If your community of interest — a small town, a rural region, a downtown core — is divided between districts, your voice on provincial decisions is diluted. The map also shapes which party can form a government, and at what margins. The audit's specific finding (the minority proposal sits at a structural extreme) is the reason you are reading this site, but the broader question is older and applies to every redistricting cycle: do the lines reflect the way Albertans live, or do they shape the politics following?",
		p5: 'The rest of this page walks through what the two proposed maps actually do.',
		key_terms_lead: 'Key terms in this section — click to read:'
	},
	editorial_reflect: {
		heading: 'Interlude: What this means for you and your community',
		intro_p1:
			"Set aside, for a moment, the question of which party gains or loses seats. Politicians and parties tend to frame this as a fight over power concentration in the legislature, and at the legislative scale it is. But power concentration in the legislature is not where you experience these maps. You experience them through three concrete questions about your own district:",
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
			'Communities are not abstract either. A high school\'s catchment area, a chamber of commerce, a faith community, a neighbourhood association — these are real groupings of people with shared local concerns. When a boundary line cuts through them, no single MLA is responsible for the whole. Take Airdrie under the minority proposal: a city of roughly 85,800 people sliced into four electoral districts, each anchored to a different rural hinterland. No single representative is accountable for Airdrie as a city. The same dynamic plays out anywhere a town, neighbourhood, or recognised community of interest is split — the bigger the split, the weaker the representation. The audit measures <em>municipal anchoring</em> (what fraction of each district\'s perimeter follows existing municipal lines), and the minority proposal scores notably lower than the majority on the anchoring test.',
		municipality_h: 'Your municipality.',
		municipality_p:
			"When a city is fractured across many representatives, its ability to bargain on provincial decisions weakens. A council asking for transit funding, a school board negotiating a new school, a mayor lobbying for highway extensions — each of those goes better when the city can point to a few MLAs who owe accountability to the city as a whole. The minority proposal splits Calgary's northwest quadrant across multiple districts whose vote-share patterns suggest <em>packing</em> (concentrating one party's voters into a few high-margin seats) on top of <em>cracking</em> (splitting the other party's voters across many low-margin seats). Whether the pattern is intentional is a question the audit cannot answer — boundary geometry doesn't reveal intent. What it can say is that the four statistical measures flag the same districts the structural tests flag, and that the alternative proposal does not produce the same fingerprint.",
		region_h: 'Your region.',
		region_p1:
			"If you live outside Alberta's cities you have probably noticed political conversations about boundaries always seem to centre the cities. It's a fair complaint, so let's be direct about what this audit does and does not say about rural Alberta.",
		region_p2:
			"What it does <strong>not</strong> say: rural Alberta has too many seats. The EBCA allows district populations to vary by up to 25% so one rural MLA isn't representing a geography the size of southern France. Canadian courts treat the variance as legitimate. Both proposed maps preserve it. Nothing in this audit changes it.",
		region_p3:
			'What it <strong>does</strong> say: in several places on the minority proposal, rural communities are being attached as the <em>tail</em> of a district whose population centre sits in a city. Look at how the minority proposal handles Airdrie — a city of about 85,800 sliced into four districts, each one extended out into a different stretch of rural countryside. The population centre of each new district is the urban slice, not the rural tail. An MLA elected from that kind of district is most likely to live, campaign, and prioritise where the votes are — which means rural communities formerly represented by a dedicated rural MLA become the back half of an urban-led seat. That pattern repeats on the minority proposal in ways it does not on the majority proposal.',
		region_p4:
			"The audit doesn't propose taking seats away from rural Alberta. It asks whether the lines respect the rural communities those seats are meant to represent, or whether rural geography is being used as ballast to absorb urban votes into districts whose centre is somewhere else. If you live in one of those rural tails, the question of which map gets enacted decides whether your MLA represents the rural community you actually live in, or an urban district whose lines happen to include your land.",
		province_h: 'Your province.',
		province_p:
			"The legislature is what you get when you sum every district's answers to the three questions above. If most districts are anchored to communities whose MLAs actually live in them, the legislature represents those communities. If most districts have rural tails attached to urban heads, the legislature represents the heads — and the tails get whatever attention is left over. The partisan question — which party wins a majority — is downstream of that. The supermajority question — whether one party crosses 60 of 89 seats and unlocks procedural shortcuts like waiving notice periods or accelerating bills through multiple stages in a single day — is downstream of <em>that</em>. At a hypothetical 50/50 provincial split, the audit's measurements place the minority proposal at a structural extreme: fewer than 100 of the 1.01 million neutral comparison maps produce the same kind of seat imbalance. Whether that imbalance pushes a party past 60 seats at the vote shares Albertans actually deliver is a question this audit has not yet directly tested; the opening questions at the top of this page are honest about that gap. Whether the answer to any of these questions matters enough to act on is, again, a question for you."
	},
	editorial_history: {
		heading: 'Context: A short history of gerrymandering',
		p1: 'The word comes from 1812. Massachusetts governor Elbridge Gerry signed off on a state-senate map whose districts were so contorted in his party\'s favour that a Boston cartoonist drew one of them as a salamander — wings, claws, a forked tongue. The cartoonist\'s pun, <em>Gerry-mander</em>, stuck. The shape stuck too: two centuries later, the word still means drawing electoral lines to engineer a partisan outcome.',
		p2: 'The term endures because the problem endures. Anywhere voters choose representatives from geographic districts, someone has to draw the lines, and the lines can be drawn many ways. Different countries have arrived at different answers about who should do the drawing and what should constrain them.',
		p3: '<strong>The United States</strong> treats partisan gerrymandering as a problem the federal courts mostly cannot fix. In <em>Rucho v. Common Cause</em> (2019), the U.S. Supreme Court ruled that partisan gerrymanders are "political questions" outside its jurisdiction. Some states (California, Michigan) have responded by creating independent citizen commissions to draw their own lines; others (Texas, North Carolina) have continued to draw openly partisan maps and defended them on the basis that <em>Rucho</em> permits it.',
		p4: "<strong>The United Kingdom</strong> uses four permanent Boundary Commissions — one each for England, Scotland, Wales, and Northern Ireland — staffed by judges and senior civil servants. They redraw lines roughly every eight years against fixed rules (population equality, geographic coherence, respect for local government boundaries). Parliament can in theory reject the commissions' recommendations, but in practice virtually never does; by convention, the commissions' judgment stands.",
		p5: "<strong>Australia</strong> delegates the work to the Australian Electoral Commission, a federal independent agency with full authority over both election administration and boundaries. Redistributions happen automatically when a state's seat count changes or seven years pass since the last one. The commissioners' decisions are reviewable on procedural grounds but not on partisan ones. As in the U.K., gerrymandering as Americans know it is virtually unheard of.",
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
				'An American nickname for an electoral map drawn to favour one party. It has no legal meaning in Canada — no court or law uses it — so this site never uses it as a verdict.'
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
				"A five-MLA Select Special Committee on Electoral Boundaries chaired by Brandon Lunty — a Premier-appointed MLA — established by the Legislative Assembly's Motion 19 (April 16, 2026), which set aside both commission reports. The committee oversees a separate four-person Independent Advisory Panel, constituted under Government Motion 37 (passed April 21, 2026), that draws the actual map; the committee then reports to the Legislature before the November 2026 deadline. Both bodies are separate from the EBC and are not part of the standard EBCA process."
		},
		'advisory-panel': {
			term: 'Independent Advisory Panel',
			definition:
				"The four-person panel appointed by the Lunty committee under clause C(d)(ii) of Government Motion 37 to draw a 91-seat boundary recommendation. The Premier nominated the Hon. Monte Solberg and Darwin Durnie; the Leader of the Opposition nominated Dr. Gerard Kennedy and Brent Robinson. A fifth seat — a sitting or retired judge to serve as chair — went unfilled after Alberta's acting chief justice declined to nominate one."
		},
		ebca: {
			term: 'EBCA',
			definition:
				'The Electoral Boundaries Commission Act — the Alberta law that sets the rules a new map must follow, including how far district populations may vary.'
		},
		ensemble: {
			term: 'The 1.01-million-map test',
			definition:
				'A computer drew 1.01 million legal Alberta maps at random, all following the same rules. A real map counts as unusual when it falls outside what almost all of these neutral maps produce.'
		},
		efficiency_gap: {
			term: 'Efficiency gap',
			definition:
				'A measure of "wasted" votes — votes beyond what a candidate needed to win, plus every vote for a loser — compared between the two parties. A large gap points to a one-sided map.'
		},
		mean_median: {
			term: 'Mean-median gap',
			definition:
				'The gap between a party\'s average vote share across districts and its middle (median) one. A large gap suggests its voters are spread in a way that wastes votes.'
		},
		declination: {
			term: 'Declination',
			definition:
				'A measure of how lopsidedly each party wins its seats — by blowouts or by squeakers. On the minority map it points the same way as the other measures (toward the governing party) after a June 2026 sign correction.'
		},
		seats_5050: {
			term: 'Seats at a tie',
			definition:
				'How many seats each party would win if the province split its vote exactly 50-50. It strips out who actually won and tests the map\'s built-in tilt.'
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
			p5: 'This image is what makes the stakes plain. A province that looks like it votes one way on a standard map is actually a province where most of the people live in areas that vote the other way. Once the population is visible underneath the boundary choices, those choices stop looking random.'
		},
		preliminary: {
			badge: 'PRELIMINARY',
			heading: 'Preliminary findings — pending independent expert review',
			body: 'The statistical tests in this section are being reviewed by independent subject-matter experts before final publication. The full results are shown below for that scrutiny.'
		},
		structural_results: {
			heading: 'Structural audit results — before any statistics:',
			body: 'The majority map crosses <strong>zero of five</strong> pre-registered structural thresholds. The minority map crosses <strong>four of the five</strong>; the fifth (anchoring) is neutral — both maps fall within the 70–85% Canadian norm. These are geometric measurements — population spread, <button class="vocab-term" data-def="how closely a district\'s borders follow pre-existing city and municipal limits, rather than cutting through them" aria-expanded="false">municipal anchoring</button>, Airdrie split count, NW Calgary population excess, and the seven boundary configurations Commission Chair Justice Miller himself flagged in writing (§5.8.2 of the majority report and Appendix C) — requiring no election data and no statistical sampler. The next section tests both maps against 1,010,000 computer-generated neutral maps and reaches the same conclusion through a completely different instrument. Three independent instruments — geometric, judicial, and statistical — converge.'
		},
		clean: {
			heading: "6: When a fair-looking map isn't",
			legal_label: 'A NOTE ON LEGAL TERMINOLOGY',
			legal_body: '"Gerrymandering" has no legal definition in Canadian law. The word is used throughout this report in its everyday political sense — manipulating electoral boundaries for partisan advantage. The legal tests actually applying in Canada are different: whether boundaries provide "effective representation" under s.3 of the <em>Charter of Rights and Freedoms</em> (the constitutional standard the Supreme Court of Canada set in the 1991 <em>Saskatchewan Reference</em>), and whether the commission followed the rules of Alberta\'s <em>Electoral Boundaries Commission Act</em>. The audit\'s findings are evidence bearing on those legal questions. They are not proof of a legally-defined wrong, and this report does not describe them in those terms.',
			intro_p1: "The cleanest single question to ask of any electoral map is this: if the province's vote split exactly evenly between the two main parties, what seat count would the map produce? This holds the electorate constant and asks the map alone what it does.",
			intro_p2: "To answer this, the audit generated 1,010,000 computer-simulated, mathematically neutral Alberta maps. The simulation used the official Elections Alberta shapefiles and held to the exact same statutory rules and geographic boundaries the commission used. The commission's two 2026 maps were then placed into that distribution to see how normal they are. The simulation ran four independent chains of 252,500 steps each, with the base seed drawn from the Cloudflare drand beacon and pre-registered at OSF before execution.",
			howmcmc_label: 'HOW THE SIMULATION WORKS',
			howmcmc_mcmc: '<strong>MCMC (Markov Chain Monte Carlo)</strong> is a method for exploring a large space — here, the space of all legal Alberta maps — by taking random steps from a starting point. Each step proposes a small swap between adjacent districts; if the result stays within the statutory rules, it becomes the new starting point. After enough steps, the visited maps form a representative sample of legal plans. The simulation is seeded from the Cloudflare drand public randomness beacon to prevent any cherry-picking of starting conditions.',
			howmcmc_recom: '<strong>ReCom (Redistricting Compiler)</strong> is the specific algorithm used here. Each step merges two adjacent districts into one region and re-splits it randomly into two new valid districts, preserving contiguity and population balance by construction — so the algorithm never needs to reject an invalid proposal.',
			prereg_label: 'PRE-REGISTRATION',
			prereg_body: "Pre-registration means writing down the exact tests, thresholds, and predicted directions before looking at any data, and locking those commitments into a public time-stamped record. The Open Science Framework (OSF) is the public repository where this audit's commitments are filed. It prevents retrofitting: if a result doesn't emerge cleanly, the threshold cannot be changed after the fact and then presented as always having been the test. All five structural tests and four partisan-fairness metrics in this audit were registered at OSF before any simulation was run.",
			neutral_p: 'In Alberta, the neutral answer is not 50/50. <em>Across 1,010,000 computer-simulated legal Alberta maps, the median map gives the UCP only 44.8% of the seats at 50/50 votes</em> — a typical Alberta map under neutral votes hands the NDP a small seat majority. This is counterintuitive but mechanical: rural UCP voters win their ridings by 60-40 margins (wasting many "extra" UCP votes), while urban NDP voters win their ridings by tighter 51-49 margins (wasting fewer NDP votes per win). At neutrality, NDP comes out ahead on seat efficiency.',
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
			t1_r4_b: '<strong>below 51.7% (fewer than 100 plans reach this value)</strong>',
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
			t2_r1_b: '+0.1% (p15.5)',
			t2_r1_c: '−3.6% (p1)',
			t2_r1_d: '−0.027 (p20)',
			t2_r1_e: '46.1% (p78)',
			t2_r2_a: 'Minority 2026',
			t2_r2_b: '<strong>+4.0% (p94.4)</strong>',
			t2_r2_c: '<strong>+1.0% (p99.98)</strong>',
			t2_r2_d: '<strong>+0.077 (p98.8)</strong>',
			t2_r2_e: '<strong>51.7% (p99.99)</strong>',
			sub1_close: "The majority map sits comfortably inside the normal range on three of four metrics. Its mean-median sits at p1 (= p0.92) in the NDP-favourable direction — an unusual result but pointing the wrong way to help the UCP. The majority map's close adherence to municipal boundaries places NDP-heavy urban cores into their own compact districts, where NDP votes win by efficient margins while UCP rural wins tend to be by larger margins; this mild structural NDP efficiency advantage is what shows up in the mean-median measure. The minority map is in the tail on all four, each pointing in the same partisan direction.",
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
			sub2_close: "Fewer than 100 of 1,010,000 computer-simulated neutral Alberta maps produced a <code>seats@50/50</code> value as high as the minority proposal's. Based on actual recent voting patterns, it would award the UCP 60 seats (compared to 55 in the majority proposal). The majority proposal is the kind of map a neutral procedure routinely generates. The minority proposal is the kind of map you have to specifically aim to draw.",
			sub3_h: 'What this means in plain language',
			sub3_p: 'The minority proposal sits in the extreme tail of the 1,010,000-plan ensemble on three of four partisan-fairness metrics, with the fourth (efficiency gap, +4.0%) at the 94th percentile — <em>near, but below</em>, the audit\'s pre-registered Alberta-calibrated threshold of the 95th. The two joint-test channels share underlying efficiency-gap data and are not statistically independent, so combining their p-values under Fisher\'s method overstates significance. The defensible upper bound from a dependence-robust combination is roughly <strong>one in 350,000</strong> (Bonferroni; p&nbsp;≤&nbsp;2.8×10<sup>−6</sup>). That remains an extreme result, well beyond conventional significance thresholds — but it is reported as a bound, not as four independent instruments reading in agreement.',
			details_summary: "What this p-value means — and what it doesn't",
			details_p1: 'A p-value answers one question: if the map were drawn by a neutral process, how often would we see a result this extreme or more extreme? At the dependence-robust bound p&nbsp;≤&nbsp;2.8×10<sup>−6</sup>, the answer is at most about once in 350,000 trials.',
			details_p2: 'This is a frequentist hypothesis test, not a measurement of intent. It does not say the commission intended to gerrymander, and it does not quantify how unfair the map is in practical terms. It says the boundary pattern is statistically inconsistent with the ReCom neutral-drawing reference distribution — a strong external check, but not a perfect one (it does not enforce every statutory criterion the commission worked under, e.g., s.15(2) tiers and community-of-interest constraints).',
			details_p3: 'The structural test battery (population, splits, anchoring, compactness, signatures) was registered with timestamps before canonical recomputation. The partisan-bias channels (joint Mahalanobis, SZAT, Fisher/Bonferroni combination) are labelled "exploratory" in the audit\'s own §4.3.1 sense: documented in the repository, but not pre-data. The audit reports each channel separately and combines them under the dependence-robust bound rather than presenting them as fully independent confirmatory tests.',
			szat_label: 'SWING-ZONE ALLOCATION TEST (SZAT)',
			szat_body: 'SZAT was designed as a second analytical channel: instead of asking "is this map extreme overall?" it asks "are the specific line choices partisan-neutral?" It works by isolating only the Voting Areas where the minority\'s map differs from the majority\'s — the contested re-draws — and testing whether those particular choices, taken together, shift vote efficiency in one party\'s direction. Because it compares only the points of departure, it automatically controls for everything the two maps share: the same geography, population targets, and statutory rules. Under a standard permutation test SZAT returned p=0.0024; under a block-permutation null that corrects for spatial autocorrelation across adjacent Voting Areas, it returned p≈0.19 — not significant. SZAT is retained as exploratory context but does not survive as a confirmatory channel. The headline rests on the simulation alone. <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/szat_summary.json" rel="noopener">Technical details →</a>',
			two_q: '<strong>The SZAT result.</strong> The 1,010,000-map simulation asks: <em>is this map extreme compared to neutral maps drawn on the same Alberta geography?</em> A second test — the <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/szat_summary.json" rel="noopener">Swing-Zone Allocation Test</a> — asked a different question: <em>are the specific lines on the map partisan-neutral?</em> It works by looking only at the Voting Areas where the minority drew differently from the majority and asking whether those particular choices, taken together, shifted vote efficiency in one party\'s direction. Under standard permutation it returned p=0.0024. Under a block-permutation null — which corrects for spatial autocorrelation among adjacent Voting Areas — it returned p≈0.19. The block-permutation result does not reach significance. The audit therefore reports the simulation result alone as the headline: a dependence-robust upper bound of <strong>1 in 350,000</strong> (p&nbsp;≤&nbsp;2.8×10<sup>−6</sup>), not a Fisher combination of two independent channels.',
			super_lead: 'In an 89-seat legislature, a two-thirds supermajority requires exactly 60 seats. The minority proposal\'s seats@50/50 of 51.7% (p99.99 against the 1,010,000-plan ensemble) sits in the regime where a UCP supermajority becomes statistically reachable on Alberta\'s 2023 geography — but the ensemble null does not enforce every statutory criterion the commission worked under, so this is a strong external check, not a proof that no legally compliant Alberta map could reach this seat count. The structural-lane evidence in Findings 1, 2 and 4 (which does not depend on this null at all) carries most of the weight; the seats@50/50 tail position is the supporting context.',
			super_label: 'WHY A SUPERMAJORITY MATTERS',
			super_body: 'Under Canada\'s Westminster parliamentary system, a simple majority (45 seats) is enough to pass routine laws and budgets. A two-thirds supermajority (60 seats) does more. It lets the governing party invoke "closure" to shut down debate, rewrite procedural rules without opposition consent, and control the composition of every legislative committee. It also insulates the government from internal dissent: even with half a dozen backbenchers crossing the floor, the government still holds a working majority. A simple majority lets you drive the car; a 60-seat supermajority lets you rewrite the traffic laws.',
			super_close: 'The urban-hybridization pattern identified in Lane 2 — urban voters distributed into surrounding rural-edge districts — is the structural mechanism consistent with the 60-seat outcome. The Lane 2 structural finding and the Lane 1 statistical finding converge on the same proposal, the same direction, and the same communities.',
			sub4_h: 'Confirmation from the targeted-procedure test',
			sub4_p: 'To be sure this isn\'t a quirk of the neutral simulation\'s known compactness preference, the audit ran a targeted hill-climbing procedure (<a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">Cannon et al. 2022 — cited and described in the technical report</a>) in both directions: maximising UCP seats and maximising NDP seats. Same number of steps (40,000) in each direction, same statutory constraints, same provincial geometry.',
			t4_col_a: 'Procedure',
			t4_col_b: 'Most-extreme value reached',
			t4_col_c: 'What it tells us',
			t4_r1_a: 'Neutral MCMC, max produced',
			t4_r1_b: 'below 51.7% UCP seats @ 50/50',
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
			sub4_close: "The minority map's 51.7% sits closer to the targeted-UCP ceiling (52.9%) than to the neutral median (44.8%). The majority map's 46.1% sits at the neutral median. Both the 2019 enacted map and the 2026 majority fall comfortably within what neutral procedure routinely produces — different vote shares, same zone of unremarkable outcomes. The majority continues 2019 Alberta practice on the partisan-fairness axis the same way it continues 2019 practice on municipal anchoring (80.0% vs 2019's 75.2%). Two maps drawn under the same Alberta rules, by the same five commissioners, in the same room: one lands where neutral procedures routinely produce, the other lands where you have to specifically aim to land.",
			sub4_quote: '<em>This</em> is the shape of the finding, and it is also the framing a court would actually apply.',
			sub5_h: 'Ruling Out Alternative Explanations',
			sub5_p: 'When presented with a statistical outlier of this magnitude, a rigorous audit must test the standard innocent explanations before treating the pattern as unexplained. The structural data (Lane 2) weighs against each of the standard alternative explanations:',
			defense1: '<strong>The "Natural Political Geography" Defense:</strong> <em>("Urban voters are naturally packed; the map just reflects Alberta\'s geography.")</em> The 1,010,000 simulations already account for Alberta\'s natural geography. The simulation proves: while geography gives the UCP a baseline efficiency advantage, it naturally caps around the 83rd to 90th percentile. The minority map sits at the 99.99th percentile — an extreme outlier <em>even when compared to Alberta\'s naturally skewed baseline</em>.',
			defense2: '<strong>The "Communities of Interest" Defense:</strong> <em>("The odd shapes were drawn to keep specific communities together.")</em> If you are trying to keep communities together, you follow municipal borders. The majority map followed existing city limits 80% of the time. The minority map followed them 72% of the time — both within the 70–85% Canadian norm. What the minority map does do is actively split the unified city of Airdrie into four separate pieces, and place three of its boundary decisions precisely in the urban-edge zones the commission chair flagged as geometrically anomalous — choices not explainable by community-of-interest logic.',
			defense3: '<strong>The "Population Equality" Defense:</strong> <em>("They had to draw weird boundaries to make sure every district had the exact same population.")</em> The minority map is actually much <em>worse</em> at population equality. Its Population Mean Absolute Deviation (MAD) was 4,707 — 48% wider than the majority map\'s 3,180 — placing it at the 99th percentile of the canonical ensemble (only 1 in 100 neutral maps produces a worse spread). It sacrificed population equality to achieve its shape.',
			defense4: '<strong>The "Incompetence or Bad Luck" Defense:</strong> <em>("They just drew a sloppy map and got unlucky with the numbers.")</em> Hitting a 60-seat supermajority configuration while also splitting Airdrie into four pieces and placing three boundaries in the exact zones the commission\'s own chair flagged as anomalous requires precision. The joint dependence-robust upper bound on the probability of accidentally drawing a map this extreme on both analytical channels under the ReCom neutral reference distribution is roughly <strong>1 in 350,000</strong> (p&nbsp;≤&nbsp;2.80×10<sup>−6</sup>). That bound is still extreme — well beyond conventional significance — but it is reported as a bound, not as a precise single probability.',
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
			stakes_fig_alt: 'Scatter plot with efficiency gap on the horizontal axis and count of structural tests failed on the vertical axis. The 2019 enacted map and the majority 2026 map cluster in the safe lower-left corner. The minority 2026 map appears in the upper-right outlier region.',
			stakes_fig_caption: 'The two ways of measuring the two commission proposals, plotted together. Left-to-right: how skewed the proposal looks on the partisan-fairness number — the further right, the more it favours the UCP. Bottom-to-top: how many of five structural-fairness tests the proposal fails — the higher, the worse. The 2019 enacted map sits in the safe corner: low on both. The majority 2026 proposal stays flat at zero structural problems and near-zero partisan skew (+0.1%). The minority 2026 proposal is a structural outlier on every test that distinguishes the two maps (4 of 5; the fifth, anchoring, is neutral for both); its efficiency gap (+4.0%) sits just below the Alberta threshold line.',
			stakes_table_intro: 'The same findings in plain summary form, leading with the structural finding because the cross-validated evidence supports it most strongly:',
			t5_col_b: 'Lane 2: Structure (geometry-only, no votes)',
			t5_col_c: 'Lane 1: Numbers (vote-dependent)',
			t5_r1_a: '<strong>Majority 2026</strong>',
			t5_r1_b: 'clean — crosses <em>no</em> structural threshold',
			t5_r1_c: 'inside the normal range on every metric (<code>seats@50/50</code> 46.1% — p78; efficiency gap +0.1%)',
			t5_r2_a: '<strong>Minority 2026</strong>',
			t5_r2_b: '<strong>crosses 4 of 5 structural thresholds</strong> by a wide margin (anchoring neutral — both maps within Canadian norm)',
			t5_r2_c: 'tail position on three of four partisan-fairness metrics — <code>seats@50/50</code> 51.7% (p99.99, roughly 66 of 1,010,000 reach it); mean-median p99.98; declination p98.8 (UCP-tail); efficiency gap +4.0% (p94.4, <em>near but below</em> the pre-registered 95th-percentile threshold); dependence-robust joint bound p&nbsp;≤&nbsp;2.8×10<sup>−6</sup> (≈ 1 in 350,000)',
			details2_summary: 'Why Lane 2 carries the case — technical detail',
			details2_p: "The audit pre-registered five structural-irregularity tests on April 24, 2026 before the final simulation results were compiled. Anchoring is neutral for both maps; on the remaining four tests the minority crosses every one and the majority crosses none. Those measurements are geometric — they don't depend on any statistical sampler or any vote attribution. <strong>This is the central finding.</strong> Lane 1 (the partisan-fairness numbers) corroborates Lane 2 under canonical official shapefiles: the minority sits in the tail of the 1,010,000-plan ensemble on three of four pre-registered metrics, with efficiency gap at p94.4 (<em>near, but below</em>, the pre-registered 95th-percentile threshold), under a dependence-robust joint upper bound of p&nbsp;≤&nbsp;2.8×10<sup>−6</sup> (≈ 1 in 350,000; replaces an earlier Fisher-combined figure that overstated the joint significance by treating two channels with overlapping data as independent). The question of whether Lane 2's unusual geometry is the specific <em>mechanism</em> behind the Lane 1 numbers was tested and the answer is no — see <a href=\"https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/redist_python_comparison.md\" rel=\"noopener\">findings/redist_python_comparison.md</a>. The Swing-Zone Allocation Test was run on the contested boundary choices; under standard permutation it returned p=0.0024, but under block permutation (correcting for spatial autocorrelation across adjacent Voting Areas) it returned p≈0.19 — not significant. SZAT is retained as exploratory context only. Separately, the mechanism question was tested: whether the boundary shapes themselves — the lasso corridor, the park extension — are the direct cause of the seat swing; they are not. The seat effect comes from how redrawn Voting Area assignments shift vote efficiency across districts, not from the shapes per se. Both lanes flag the minority map; they reach it through independent instruments. Lane 2 carries the case. Lane 1 corroborates without carrying."
		},
		impact: {
			heading: '5: Effects on Representation',
			lanes_label: 'LANE 1 AND LANE 2',
			lanes_body: '<strong>Lane 1 (numbers)</strong> uses election results to test whether the map converts votes into seats fairly — it asks how the map performs across different vote splits. <strong>Lane 2 (structure)</strong> examines only the drawn lines — city splits, population spread, boundary shapes — with no election data at all. Each lane is independent: a map can fail one while passing the other. The minority proposal fails both; the majority passes both.',
			intro: "Lane 1 depends on which election results you score the maps against. Lane 2 does not. The structural evidence is in the maps themselves — drawn lines, split cities, where the boundaries do and don't follow administrative lines that exist for other reasons. On these tests, the two maps are not close.",
			fig_alt: 'Bar chart comparing five structural-fairness tests side by side. The majority map bars sit at zero or well inside safe ranges. The minority map bars cross the threshold on four of the five tests by a wide margin; the fifth (anchoring) is neutral for both maps.',
			fig_caption: 'The five structural-fairness tests, side by side. Teal bars are the majority map; purple bars are the minority map. The dashed line in each row marks the failing threshold. The minority bars cross the threshold on four of the five tests by a wide margin; the fifth (anchoring) is neutral for both maps. The majority bars sit flat at zero or well inside the safe range.',
			table_intro: "The same five tests in tabular form, with each test's threshold stated alongside the result. The bottom row is the audit's <em>summary</em> — the count of tests each map fails out of the five.",
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
			table_r3_a: 'NW Calgary population excess above average',
			table_r3_b: '2.8%',
			table_r3_c: '11.5%',
			table_r3_d: '<strong>UCP</strong> (Packs urban NDP votes)',
			table_r4_a: "Boundaries flagged by the commission's own chair",
			table_r4_b: '0',
			table_r4_c: '3',
			table_r4_d: 'N/A',
			table_r5_a: 'Airdrie split (constraint minimum: 2)',
			table_r5_b: '2 pieces',
			table_r5_c: '4 pieces',
			table_r5_d: '<strong>UCP</strong> (Cracks urban/suburban power)',
			table_r6_a: '<strong>Pre-registered summary</strong> (&ge; 4 of 5 = outlier)',
			table_r6_b: '<strong>0 of 5 fired</strong>',
			table_r6_c: '<strong>4 of 5 fired</strong> (anchoring test neutral — both maps within Canadian norm; remaining 4 tests all fire)',
			table_r6_d: '<strong>UCP</strong>',
			rationales_p: "A separate finding, applied only to the minority: <strong>five of six of the minority commissioners' published rationales fail under independent check</strong>. The test runs against the minority only because the majority did not publish a contested-redraw rationale list — the audit cannot apply it symmetrically, and it is reported here as a single flag rather than as additional rows in the structural-irregularity count. (A seventh redraw the audit had previously listed turned out to rest on a federal-boundary claim untraceable in the minority report; it has been removed rather than left as a weak claim.)",
			chair_appendix_p: 'The audit also tested the chair\'s separate, blanket assertion in Appendix C that the minority\'s seven contested hybrid configurations had <strong>no public support</strong> in the 1,140+ public submissions. A keyword search across the full submission archive (94% machine-parsed, 6% image-only and excluded; methodology and per-configuration evidence at <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/submission_search_findings.md" rel="noopener">findings/submission_search_findings.md</a>) returned a more nuanced picture than either the chair\'s blanket claim or its blanket dismissal: the chair was right on three of seven (Airdrie 4-way split, Calgary–Nolan-Hill–Cochrane hybrid, and the St. Albert minority alternative each lack any documented support), wrong on three of seven (Rocky Mountain House–Banff Park drew an explicit, detailed proposal from at least one Clearwater-area submission plus several aligned ones; Olds–Three-Hills–Didsbury was supported by Beiseker residents in writing; Chestermere drew multiple submissions opposing a Calgary merger that materially align with the minority\'s intent), and partially wrong on one (Red Deer hybrids drew a peri-Red-Deer hybrid proposal from a sitting Red Deer councillor, with directional but not configuration-exact alignment). The chair\'s Appendix C "no public support" sweep is therefore demonstrably overbroad — three of seven are demonstrably false — but it is not invented out of whole cloth, since three of seven do hold up. <strong>This finding cuts against the chair, not against the minority.</strong>',
			summary_p: '<strong>On Lane 2, the majority crosses zero structural thresholds. The minority crosses every one of them by a wide margin.</strong> The count is a raw tally rather than a calibrated family-wise probability — its weight comes from directional unanimity (every firing test pointing the same way), not from a joint null-distribution calculation. The statistical lane (§3) supplies the joint probability through a different instrument.'
		},
		cpd: {
			heading: '4: Cracking, Packing, and Draining',
			vocab_label: 'Three moves, one playbook',
			vocab_packing: "<strong>Packing</strong> means cramming one party's voters into districts the party wins by landslides — each packed ballot still counts, but it contributes nothing beyond victory. Large, lopsided wins. Wasted votes.",
			vocab_cracking: "<strong>Cracking</strong> means splitting a community across multiple districts so it wins none of them outright. A city strong enough to carry two seats gets carved into four, each tethered to a different rural area. Diluted votes. No seat for anyone.",
			vocab_draining: '<strong>Draining</strong> is the spatial companion: packed and cracked districts are placed next to each other so over-concentrated supporters on one side "drain" voting power away from the contested districts nearby. The adjacency pattern amplifies both effects — packing and cracking reinforce each other across district lines.',
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
			anchoring_p: "<strong>Where it departs from municipal lines, it departs at strategically important places.</strong> When electoral maps follow the edge of a city or town, voters recognize where their division begins and ends — the property-tax line, the school-division line, the local-election ward line, and the provincial-election line all coincide. Statistics Canada publishes these boundaries for free. On official Elections Alberta shapefiles, both maps follow municipal lines at comparable overall rates: the majority at 80%, the minority at 72%, both within Canada's 70–85% norm (Quebec: 78%, Ontario: 82%, BC: 71%; comparator commissions documented in the monograph). (The audit's initial provisional analysis showed the minority anchoring at only 15%; the figure did not survive recomputation on official shapefiles — see the correction note below.) The striking observation is not the overall rate but where the minority's departures are concentrated: the three boundaries the commission's own chair flagged as anomalous — Rocky Mountain House–Banff Park <button class=\"ed-trigger\" data-ed-name=\"Rocky Mountain House-Banff Park\">show ↗</button>'s extension into uninhabited national-park land, the Nolan Hill–Cochrane <button class=\"ed-trigger\" data-ed-name=\"Calgary-Nolan Hill-Cochrane\">show ↗</button> lasso corridor, and the Olds–North Airdrie <button class=\"ed-trigger\" data-ed-name=\"Olds-Three Hills-Didsbury\">show ↗</button> reach — are each departures from pre-existing civic geography in the exact urban-edge zones where pairing urban and rural voters most directly affects which party wins the seat.",
			anchoring_followup: 'The minority commissioners gave reasons for each of the three flagged boundaries. For Rocky Mountain House–Banff Park, they cited geographic size, the Highway 22 corridor, and the proximity of First Nations reserves to Rocky Mountain House; the commission chair called the extension into uninhabited national park land "a bad faith effort" to satisfy the area criterion, and the phrase appears in the commission\'s official final report. For Nolan Hill–Cochrane, they cited shared transportation and employment ties between northwest Calgary and Cochrane; Statistics Canada journey-to-work data shows only 35.8% of Cochrane workers travel to Calgary at all, with most working within Cochrane itself. For the Olds–North Airdrie reach, they cited Highway 2 corridor continuity; the audit found the specific Airdrie extension fails on population grounds. Independent check found five of the minority\'s six published sub-rationales fail or only partially hold against primary data.',
			packing_p: "<strong>One area of Calgary is carved up to concentrate NDP voters into larger-than-average divisions.</strong> In Calgary's northwest quadrant <button class=\"ed-trigger\" data-ed-name=\"Calgary-North West-Bearspaw\">show ↗</button>, the minority map's divisions average 11.5% above the province-wide population — versus 2.8% on the majority. The same geographic zone, drawn by the same commission under the same constraints, produces districts a quarter larger on one map than on the other. This fits the structural signature of <em>packing</em>: concentrating one party's voters into fewer, larger districts so each of their ballots weighs less. Packing and <em>cracking</em> (splitting a party's voters thinly across districts they narrowly lose) are the two classic gerrymandering moves; both shrink a party's seat count below its vote share.",
			chair_p: "The commission chair — appointed under the same Act, working from the same submissions — flagged three boundaries on the minority map as geographically anomalous: Rocky Mountain House–Banff Park's extension into uninhabited national park land; the Calgary-Nolan Hill–Cochrane lasso-shaped corridor; the Olds–Three Hills–Didsbury reach into north Airdrie. The majority received zero such flags from the same chair. (The chair's published criticism covers seven boundary configurations in total — four geometric flags in the main report and three in Appendix C. This audit independently confirmed anomalous geometry for three of the four geometric flags; the fourth, Calgary-Foothills-Airdrie West <button class=\"ed-trigger\" data-ed-name=\"Calgary-Foothills-Airdrie West\">show ↗</button>, did not meet the audit's confirmation threshold.) Beyond the chair's geometry flags, the audit's own cracking-signature test (academic §5.3.2) flags the four-way Airdrie split on every criterion — a community split that leaves Airdrie's residents a minority in all four ridings, where the majority's two-way split shows none; Cochrane and Chestermere come up cracking-adjacent. Some of what the audit's math flags, the chair did not. The audit measures the structural effect, not intent."
		},
		litmus: {
			heading: '3: The 1,010,000-Map Litmus Test',
			fig_alt: 'Histogram showing the distribution of efficiency gaps across 1,010,000 neutral Alberta maps. Most maps cluster near zero. The minority commission map (purple line) sits at the 94th percentile (+4.0%), in the shaded right tail. The majority map (teal line) sits at +0.1%, well within the normal range.',
			fig_caption: 'Distribution of <button class="vocab-term" data-def="a measure of how lopsidedly votes are converted into seats — positive values favour the UCP, negative values favour the NDP" aria-expanded="false">efficiency gaps</button> across 1,010,000 neutral Alberta maps drawn from the same geography. Most neutral maps cluster near zero; the shaded right tail marks the top 10%. The minority proposal&rsquo;s +4.0% sits at the 94th <button class="vocab-term" data-def="the percentage of maps that scored lower — p94 means 94 out of 100 neutral maps were less partisan than this" aria-expanded="false">percentile</button> — a region fewer than 6 in 100 neutral maps ever reach. The majority proposal&rsquo;s +0.1% is indistinguishable from what a neutral process typically produces.',
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
			table_r6_b: '46.1% — p78 (normal range)',
			table_r6_c: '51.7% — p99.99 (fewer than 100 of 1,010,000 reach this)',
			table_r6_d: '<strong>UCP</strong>',
			table_r7_a: 'Efficiency Gap (percentile in 1,010,000-map simulation)',
			table_r7_b: '+0.1% — p15.5 (normal range)',
			table_r7_c: '+4.0% — p94.4',
			table_r7_d: '<strong>UCP</strong>',
			table_r8_a: 'Packing-cracking neighbourhood pattern',
			table_r8_b: '6 coupled chain signals',
			table_r8_c: '2 (pre-registered PASS)',
			table_r8_d: 'Neutral — minority achieves partisan effect via hybridization, not adjacency drain (§5.3.5)',
			vocab_label: 'VOCABULARY',
			vocab_eg: "<strong>Efficiency gap.</strong> A single number that measures how lopsidedly a party's votes are translated into seats. Positive numbers favour the UCP; negative favour the NDP. The audit uses ~5% as Alberta's outlier line — the value exceeded by only 5% of the 1,010,000 neutral Alberta-specific simulations. This threshold is not borrowed from US or general literature; a threshold calibrated to another jurisdiction would be wrong because Alberta's natural geography produces a different neutral range.",
			vocab_mm: "<strong>Mean-median difference.</strong> The gap between a party's median district vote share and its mean district vote share. When one party wins many close races, the median sits above the mean — those votes are distributed efficiently. When a party wins many races by large margins, the mean sits above the median — votes are being wasted. A large mean-median gap in one direction flags structural inefficiency in how one side's votes are spread across districts.",
			vocab_percentile: '<strong>Percentile ranking.</strong> In this audit, a "percentile" is a rank within the 1,010,000 neutral simulated maps. "p94" means 94% of neutral maps score lower — the real map is more extreme than 94% of neutral draws. "p99.99" means fewer than 1 in 10,000 neutral maps reach the level.',
			vocab_anchoring: '<strong>Anchoring.</strong> The fraction of an electoral border that lies on a pre-existing administrative line — a city limit, a school-division boundary, a Statistics Canada census line.',
			closing_p1: "The bottom rows depend on election results. The <em>seats@50/50</em> test holds the electorate at perfect parity (UCP and NDP each win exactly half the votes province-wide) and asks how many seats the map awards the UCP. A neutral Alberta map produces a median around 44.8% UCP seats. Alberta's geography — NDP voters concentrated in city cores, UCP voters spread across rural ridings — gives the NDP a small efficiency advantage at neutrality. The majority map at 46.1% sits at the 78th percentile of the 1,010,000-map simulation, well inside the normal range. The minority map at 51.7% sits at the 99.99th percentile: fewer than 100 of 1,010,000 neutral draws reach that value. The <em>efficiency gap</em> number measures how lopsidedly each party's votes get translated into seats. On the official Elections Alberta shapefiles the minority's efficiency gap is +4.0%, placing it at the 94.4th percentile — just below the audit's 95th-percentile outlier line. The opening questions at the top of this page unpack the consequences.",
			closing_p2: "The last row is where the minority map has fewer coupled chain signals than the majority on the neighbour-drain test: 2 against the majority's 6 (and the 2019 enacted map's 5). The audit pre-registered this test before measuring, and the minority's lower count is a genuine pre-registered PASS — the minority does not show the classic pack-and-drain adjacency pattern. It is the single test where the minority numerically outperforms the majority. §5.3.5 of the academic report explains why: the minority achieves its partisan effect through hybridization (city-splitting that internalises packing and cracking within individual EDs), which is invisible to an adjacency-chain test that only measures how packed districts cluster next to cracked ones."
		},
		commission_split: {
			heading: '2: How the Commission Split',
			intro: 'Alberta\'s Electoral Boundary Commission finished its work on March 23, 2026 and could not agree. Three commissioners produced one map; the other two produced a different one. Commission Chair Justice Dallas K. Miller and two opposition-nominated commissioners wrote the majority report; two government-nominated commissioners — Dr. Julian Martin and John D. Evans — wrote the minority report. The split centred on how to draw boundaries in fast-growing urban-edge communities. The majority gave Airdrie two districts; the minority four. The majority drew northwest Calgary\'s divisions close to the provincial average; the minority drew them 11.5% above it. Both maps follow the same statute. Both are legal under the <em>Electoral Boundaries Commission Act</em>. The disagreement was about which specific geographic configurations best served the communities being drawn. Alberta\'s governing party is the United Conservative Party (UCP); its main opposition is the New Democratic Party (NDP). Smaller parties — the Alberta Party, the Liberal Party of Alberta, and others — contest seats too, but their combined provincial vote share has been low enough in recent elections that it does not materially affect the audit\'s partisan-fairness calculations, which are grounded in the 2023 UCP–NDP split. This audit measured both maps using the same methods, applied identically. Three findings stand out.',
			finding1: "<strong>The two maps differ on six things you can measure without looking at any election results:</strong> how evenly people are spread across districts, whether voters are concentrated, how badly cities are cut up, whether borders follow city limits, the shape of the districts, and how many boundaries Commission Chair Justice Miller himself flagged as anomalous in writing (§5.8.2 of the majority report and Appendix C). The minority map differs from the majority on every one of them.",
			finding2: '<strong>Every measured difference moves in the same direction.</strong> Everywhere the two maps diverge — northwest Calgary, Airdrie, urban areas with clear city limits — the minority map draws boundaries that spread NDP votes thinner and let UCP votes count more efficiently. The communities most reshaped by the minority map are the same communities where the NDP is strongest. The audit cannot determine intent. It can measure effect.',
			finding3: '<strong>The process now promoting the minority map is without precedent among the Canadian redistribution cycles this audit reviewed — an assessment political scientist Duane Bratt (Mount Royal University) shared in correspondence with the author.</strong> None of the reviewed provinces lets a cabinet hand redistricting to a committee its own party controls partway through a redistribution cycle. Most provinces either require the legislature to debate the commissioners\' map first, or give the commission\'s map automatic effect unless overridden. Alberta does neither. On April 16, the government set both commission maps aside and assigned the work to an MLA committee a majority of whose members come from the governing United Conservative Party (UCP); the committee\'s full composition and mandate are detailed in §7. Alberta\'s <em>Electoral Boundaries Commission Act</em> requires the legislature to pass a separate Electoral Districts Act to give a commission report legal effect — the commission report itself changes nothing. Most other provinces make a commission\'s report legally effective unless the legislature actively overrides it; Alberta\'s default reverses it, meaning the governing party controls whether any commission map ever becomes law. The government\'s stated justification was to implement Commission Chair Justice Miller\'s Recommendation 5. But Miller had written the recommendation specifically to dissuade the legislature from accepting the minority map, and his majority colleagues did not endorse it. Recommendation 5 was also geographically specific: one additional rural seat south of Edmonton, and one in Clearwater County and western Mountain View County — both far from the fast-growing Calgary and Edmonton urban-edge communities where the commission actually split. It was not an invitation to redesign those contested boundaries. The government adopted the seat count while handing a committee it controls authority over exactly the lines the commission disagreed on.',
			closing: '<strong>The process is its own finding, separate from the maps.</strong>'
		},
		november: {
			heading: '7: The Lunty Committee',
			context_label: 'CONTEXT',
			context_body: ' — This section describes the process that replaced the commission and the legal framework that applies to it. It is not part of the statistical findings. The findings are in §3–§6 above.',
			intro: "Neither commission map is in force. On April 16, 2026 the Legislative Assembly passed Motion 19, setting both aside and referring redistricting to a Select Special Committee of five MLAs — three UCP, two NDP — chaired by Brandon Lunty (UCP, Leduc-Beaumont). The committee itself does not draw the map. It oversees a separate Independent Advisory Panel, constituted under Government Motion 37 (passed April 21, 2026), tasked with producing a 91-seat boundary proposal. Motion 37 contemplated five panel members — a sitting or retired judge as chair, two members nominated by the Premier, and two by the Leader of the Opposition — but Alberta's acting chief justice declined to nominate a judge to the chair, and the panel now operates with the four appointees the committee confirmed: the Hon. Monte Solberg and Darwin Durnie (Premier's nominees) and Dr. Gerard Kennedy and Brent Robinson (Opposition nominees). The committee must deliver its report to the Legislature by November 2, 2026. Unlike the original commission, neither the committee nor the panel is required to hold public hearings; the panel draws on submissions the original commission gathered. When the committee's map is released, this audit will apply the same methodology to evaluate it.",
			h_anomalous: 'Why the Committee Is Anomalous',
			anomalous_p1:
				"Canadian redistricting practice has, since the 1960s, settled on a single model: an independent commission, insulated from government direction, produces boundary recommendations; the legislature may debate them but cannot easily override them without a formal legislative vote. Alberta's statutory process under the <em>Electoral Boundaries Commission Act</em> follows this template — but with one structural difference from most provinces: Alberta's commission report has no automatic legal effect. Under the Act, a separate Electoral Districts Act must be passed by the legislature to give any commission map force of law. This means the government of the day controls not only whether the commission map is debated, but whether it ever becomes law at all. Other Canadian jurisdictions take the opposite default: the commission's recommendations take effect unless the legislature affirmatively votes to override them.",
			anomalous_p2:
				"What the government did in April 2026 has no recorded precedent in post-Confederation redistricting: it allowed a completed, published commission process to conclude — both majority and minority reports filed — and then referred the redistricting task to a five-member committee of MLAs whose majority (three of five) is held by the governing party, without bringing either commission report to a vote. The Lunty committee is not a commission. It has no statutory independence from the government's legislative direction. Its three-member UCP majority mirrors the government's control of the legislature. No other Canadian province has transferred redistricting authority, mid-cycle, to a government-controlled legislative committee after an independent commission had completed its work.",
			h_framework: 'The Constitutional Framework',
			framework_p1:
				'Section 3 of the <em>Charter of Rights and Freedoms</em> — "Every citizen of Canada has the right to vote in an election of members of the House of Commons or of a legislative assembly" — has been interpreted by the Supreme Court of Canada to guarantee not merely the act of casting a ballot but <em>effective representation</em>. The leading authority is <em>Reference re Provincial Electoral Boundaries (Saskatchewan)</em> [1991] 2 SCR 158, in which McLachlin J. (as she then was) wrote for the majority that the purpose of s.3 "is not equality of voting power per se, but the right to effective representation." Population parity is the primary consideration; departures are permitted when justified by community of interest, geography, history, or minority-representation objectives.',
			framework_p2:
				"The Saskatchewan framework does not categorically prohibit partisan considerations in redistricting. What it establishes is that boundary maps must, on the whole, provide effective representation to voters — and that systematic impairment of one identifiable group's ability to elect proportionate representation is the pattern that s.3 challenges target. The audit's statistical and structural findings — the minority map's position at the 99.99th percentile of 1,010,000 neutral draws, its crossing of four of five structural thresholds (the fifth, anchoring, is neutral for both maps), the identified communities affected — are the evidentiary record a s.3 applicant would need to assemble. On the community-of-interest side of that record, the Federal Court's decision in <em>Raîche v. Canada</em> (2004 FC 679) is the leading Canadian authority: the court there required the federal Electoral Boundaries Commission to revisit boundaries that had ignored Acadian community of interest in New Brunswick. The audit's municipal-anchoring measurements and its specific community findings — Airdrie split into four districts, the chair-flagged urban-edge anomalies in northwest Calgary — are the same kind of evidence the Federal Court treated as legally cognizable. Whether that record meets the constitutional threshold is a legal question this audit does not decide; the audit reports the measurement.",
			framework_p3:
				"The committee's legality as a process is a separate question. Alberta's <em>Electoral Boundaries Commission Act</em> does not expressly prohibit the legislature from constituting a parallel redistricting body, because the Act contemplates that the legislature will enact the final boundaries through ordinary legislation regardless. Whether the committee process, if it produces a map with the structural and statistical profile of the minority proposal, could survive a s.3 Charter challenge turns on whether effective representation is achievable under the resulting boundaries — the same test that would apply to any commission-produced map.",
			h_quebec: 'The Quebec Contrast',
			quebec_p1:
				"Quebec offers the comparison most relevant to Alberta's situation. Quebec's Commission de la représentation électorale (CRE) is a permanent, independent electoral boundaries body, not an ad hoc commission constituted per redistribution cycle. The CRE operates continuously and cannot be dissolved or bypassed by cabinet action. Under Quebec's <em>Loi électorale</em>, the National Assembly must adopt the CRE's recommendations unless it votes to deviate — and deviations require a two-thirds majority of all members of the Assembly, not a bare legislative majority. The practical effect is that a governing party cannot, acting alone with its own majority, substitute its preferred map for the commission's. Cross-party agreement is constitutionally required to override the independent body's judgment.",
			quebec_p2:
				"Quebec's model emerged partly from lessons about what happens when redistricting is not insulated from partisan control. The contrast with Alberta's current process — where a majority-controlled committee has replaced the commission's work before the legislature has voted on either commission report — illustrates the structural difference between redistricting systems that assume partisan pressure and design against it, versus systems where that pressure has a clearer path to the outcome.",
			closing:
				"The audit will apply the same tests to the Lunty committee's map when it is released. The constitutional and comparative observations above are contextual; the methodology does not change."
		},
		references: {
			heading: '10: References and Methodology',
			heading_aria: 'Link to references',
			intro:
				'The underlying methodology draws on established political science, statistics, and legal literature. Full citations follow American Political Science Association (APSA) style; court cases follow Canadian legal convention. The complete reference list appears in the <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">technical report</a>. Key sources are listed here.',
			h_academic: 'Academic literature',
			h_cases: 'Court cases',
			h_statutes: 'Statutes'
		},
		resources: {
			heading: '11: Technical Appendix',
			heading_aria: 'Link to technical',
			tag_plain: 'Plain Language',
			plain_label: 'Full public report',
			plain_desc: 'Long-form, with maps, for general readers',
			tag_summary: 'Summary',
			summary_label: 'Summary of findings',
			summary_desc: 'Plain-language overview, explains every concept from scratch',
			tag_academic: 'Academic',
			academic_label: 'Technical report',
			academic_desc: 'Full methods and citations for researchers',
			tag_notebook: 'Notebook',
			notebook_label: 'Interactive notebook',
			notebook_desc: 'Run the charts yourself in your browser, no install needed',
			tag_code: 'Code'
		},
		about_me: {
			heading: 'About me',
			p1: "I'm a student at Mount Royal University. I did this research on my own — it was not assigned as coursework and the university did not commission it. My views are my own and do not represent the university. I have no connection to Elections Alberta, the commission, or any political party.",
			p2: "I have voted for different parties in different elections, across the political spectrum. I'm telling you because my political history could affect how I look at this issue. The main protection against it is the method: I tested both maps the same way, wrote down my predictions before looking at the results, and put everything online so anyone can check my work. I paid for this research myself. If you find something I got wrong, I genuinely want to know.",
			p3: 'Pre-registration records (written before results were examined): <a href="https://osf.io/6pt83" rel="noopener">OSF:6pt83</a>, AsPredicted:#289,469, AsPredicted:#289,451.',
			p4: 'Questions or corrections: <a href="mailto:wconn161@mtroyal.ca">wconn161@mtroyal.ca</a>'
		},
		translation_about: {
			heading: 'About this translation',
			p1: 'You are reading an AI translation, produced by Anthropic\u2019s Fable 5 model and awaiting native-speaker review. The English version is the authoritative text: if anything in this translation is unclear or seems wrong, the English original governs.',
			p2: 'Translation quality matters here in a way it doesn\u2019t on most websites \u2014 this audit makes statistical claims about electoral fairness, and a mistranslated number or a wrongly-hedged sentence misleads in ways that are hard for a reader to detect. Machine translation of civic-statistical prose is genuinely difficult, and errors are likely.',
			p3: 'If you are a native speaker and you spot an error \u2014 or you\u2019d like to review a section properly \u2014 please %s. For scale: the English prose runs about {count} words. You are welcome to take on all of it or just a portion, and in most cases the work is correcting minor errors the machine made rather than translating from scratch \u2014 even reviewing a single section helps.',
			p3_link: 'get in touch'
		},
		retractions: {
			heading: '9: Retractions and Corrections',
			heading_aria: 'Link to retractions',
			conditions_label: 'RETRACTION CONDITIONS',
			conditions_intro:
				'Every finding is pre-committed to a specific falsification condition. If any condition below materialises, the finding it names is retracted publicly within 30 days. The overall directional conclusion — that the minority map sits outside the neutral range on multiple independent tests — is retracted only if at least three of the five tests fail.',
			c1_title: 'Condition 1 — A counter-map exists',
			c1_what: "<em>What gets retracted:</em> The structural finding that the Airdrie four-way split and the three chair-flagged boundaries cannot be explained by the minority's stated community-of-interest rationale.",
			c1_cond:
				"Condition: someone produces a legal Alberta map satisfying the minority's own stated reasons — Airdrie, Cochrane, Nolan Hill, Rocky Mountain House–Banff Park — and anchors on municipal lines at majority-comparable rates. Open challenge at <a href=\"https://github.com/Ixby/alberta-electoral-boundaries-audit/issues/14\" rel=\"noopener\">Issue #14</a>.",
			c2_title: 'Condition 2 — The Neighbour-Drain pre-registered pass is reversed',
			c2_what: '<em>What gets retracted:</em> The Section 3 table entry recording the minority map as a pre-registered PASS on the neighbour-drain adjacency test.',
			c2_cond:
				'Condition: the v2 continuous drain score falls in the extreme upper tail (p &lt; 0.05) of random permutations across the fixed contiguity graph, meaning the pass was a measurement artefact of the v1 binary scoring method rather than a genuine null result.',
			c3_title: 'Condition 3 — A pre-2026 commission document surfaces',
			c3_what: "<em>What gets retracted:</em> The inference that the minority's boundary choices were drafting decisions rather than responses to documented community submissions.",
			c3_cond:
				"Condition: an internal commission document dated before the minority's final boundary choices shows those choices were explicitly driven by community submissions the audit has not seen — not by the six published sub-rationales the audit tested.",
			c4_title: 'Condition 4 — The 2027 election result contradicts the simulation',
			c4_what: "<em>What gets retracted:</em> The Lane 1 finding — that the minority map's seats@50/50 score sits at the 99.99th percentile of 1,010,000 neutral draws.",
			c4_cond:
				'Condition: if the 2027 provincial election is fought on either commission map and the actual partisan seat split contradicts the directional projection from 2023 votes, the Lane 1 percentile findings are revisited against actual results.',
			c5_title: 'Condition 5 — An Alberta court distinguishes the Quebec SCC ruling',
			c5_what: '<em>What gets retracted:</em> The Section 7 procedural argument that the April 16 motion to replace the commission with the Lunty committee sits in the same constitutional class as Quebec\'s 2024 redistricting freeze.',
			c5_cond:
				"Background: on April 22, 2026 — six days after Alberta's April 16 motion — the Supreme Court of Canada upheld, 7–2 and from the bench, a Quebec Court of Appeal ruling that the Legault government's legislative freeze on its redistricting commission violated the Charter's s.3 democratic-representation guarantee. Condition: a court reviewing the Alberta motion finds it constitutionally distinct — for example, because reassigning the work to an MLA committee differs structurally from a legislative freeze, or because Alberta's effective-representation analysis under s.3 comes out differently than Quebec's.",
			corr_label: 'DOCUMENTED CORRECTIONS (canonical recomputation, 2026-05-11)',
			corr_intro:
				"The following early finding did not survive reanalysis against official Elections Alberta shapefiles (received 2026-05-06). It is retained here per the audit's pre-committed policy of never deleting failed findings.",
			corr_municipal:
				"<strong>Municipal anchoring (retracted).</strong> Early analysis using provisional map boundaries showed the minority map anchored to municipal lines only 15% of the time — 4.9&times; below the 70–85% Canadian norm. This figure was an artefact of the provisional (DPG-era) boundary reconstructions. On official Elections Alberta canonical shapefiles, both maps anchor within the Canadian norm: majority 80%, minority 72%. The municipal-anchoring <em>divergence</em> between the two maps is not a signal that survives canonical recomputation. The three boundary anomalies flagged by the commission chair (Rocky Mountain House–Banff Park, Nolan Hill–Cochrane, Olds–North Airdrie) remain and are not affected by this correction."
		},
		suggestions: {
			heading: '8: Suggestions',
			heading_aria: 'Link to section 8',
			intro:
				"This audit ran into two data problems that have nothing to do with the commission's work and everything to do with how Alberta's electoral system is designed. Both are fixable.",
			advance_p1:
				"<strong>About half of all Alberta votes now arrive before election day</strong> — advance polls, mobile polls, special ballots. Elections Alberta reports these results as totals for each electoral division, not by specific Voting Area. This means roughly 395,000 NDP and UCP votes cast in 2023 cannot be pinned to any neighbourhood on a map. They are counted; they just can't be located. Every advance voter is checked against a voters list before receiving their ballot, and the list links each voter to their specific Voting Area. Publishing VA-level advance-vote totals would not require any change to the voting process — only to what EA reports.",
			advance_p2:
				"This affects the commissioners too, not just outside analysts. When a commission decides whether to keep Airdrie whole or split it, whether a corridor between two communities makes sense, whether a proposed boundary divides a natural constituency — those are judgments that depend on knowing where voters live. Commissioners work from the same published dataset as everyone else. Half the geographic signal about the communities they are drawing boundaries around is missing for them as well.",
			lesser_slave_p1:
				'There is at least one community in northern Alberta where this gap is total. In the northern part of the Lesser Slave Lake <button class="ed-trigger" data-ed-name="Lesser Slave Lake">show ↗</button> division, there is a Voting Area covering 4,832 km&#178; — larger than Prince Edward Island — where every single vote in 2023 was cast through Elections Alberta\'s mobile polling team. Those 844 residents\' choices are counted in the divisional total but cannot be pinned to any location on a map. The community is entirely invisible in the published election results.',
			lesser_slave_p2:
				'When the commission initially considered eliminating the Lesser Slave Lake division and merging it into a larger riding, it was working without geographic vote data from those communities. The commission eventually preserved the division — after 80+ public submissions, many from the Indigenous communities in the northern part of the riding — invoking a provincial law that allows ridings with First Nations and M&#233;tis communities to have smaller populations than the provincial average. They got there. But the data they were working with didn\'t show them who was voting in the communities they were deciding to protect.',
			ebca_label: 'SECTION 15(2) EBCA',
			ebca_body:
				"Section 15(2) of Alberta's <em>Electoral Boundaries Commission Act</em> is a discretionary provision that allows commissions to protect undersize ridings — those more than 25% below the provincial population average — when the riding meets at least three of five specific criteria: (a) geographic area exceeding 20,000 km², (b) distance more than 150 km from the Legislature Building by most direct highway route, (c) absence of any town with more than 8,000 residents, (d) presence of an Indian reserve or a Métis settlement, and (e) whether the riding is coterminous with a boundary of the Province of Alberta. The provision is not automatic; the commission must judge whether the criteria are met. Lesser Slave Lake independently meets four of the five.",
			rationale_p1:
				"The interim rationale for eliminating the riding was population: at roughly 27,000 residents, Lesser Slave Lake sits about 45% below the provincial average, approaching the legal floor. This reads as a straightforward application of the rules. It isn't. Alberta law gives commissions explicit discretion to protect undersize ridings when at least three of five specific criteria apply, and Lesser Slave Lake meets four of them independently. Its area is 69,566 km² (criterion a, threshold 20,000 km²). Its nearest boundary is more than 150 km from the Legislature by highway (criterion b). No town in the riding has a population over 8,000 (criterion c). And the riding contains fourteen Indian reserves and M&#233;tis settlements whose communities share a common northern geography, a common dependence on mobile polling to vote at all, and a collective interest in having a representative primarily accountable to northern Alberta (criterion d).",
			rationale_p2:
				"Under the proposed Mackenzie merger, the collective voice would have been permanently absorbed into a riding where the other party wins by more than two to one, not because those communities changed but because the lines around them did. Each of those four criteria is an objective fact about the riding's geography, not a judgment call. Together they describe a constituency the provision was written to protect: remote, large, sparsely populated, and containing communities whose representation interest cannot be read from raw population numbers. You need three to qualify; Lesser Slave Lake has four. Treating the population shortfall as if it compelled elimination misreads the statute. The commission's reversal was the correct application of the law, not a concession to political pressure.",
			banff_p:
				'Here is the other side of the story: while the Indigenous communities in Lesser Slave Lake were fighting to be counted, the dissenting commissioners proposed protecting a different riding by drawing its boundary through Banff National Park, where no one lives. The commission\'s own chair called it "a bad faith effort" to claim the legal protection. The phrase is in the commission\'s official final report. The protection designed for remote communities with Indigenous populations was used, in the minority\'s map, to defend a boundary through uninhabited wilderness. The communities it was designed to help had to fight for it through public submissions. The Lunty committee will face the same §&#x2009;15(2) decision in November — with no statutory requirement to hold public hearings, and no guarantee the 80 submissions reversing the commission\'s interim position will carry the same weight a second time.',
			census_p1:
				"<strong>Alberta should wait for the 2026 census before drawing the next map.</strong> Canada counts its population every ten years. The 2026 census enumeration happens in spring 2026; Statistics Canada releases usable sub-provincial data roughly two years later, in 2027 or 2028. The commission that drew the maps assessed in this audit had to use the 2021 census — already four years old when the maps were drawn, and potentially fourteen years old by the time those boundaries retire. Fast-growing cities like Airdrie and Chestermere will change by 40% or more over that window. Rural communities will shrink. The map will be wrong from the day it is used. A straightforward change to the <em>Electoral Boundaries Commission Act</em> could require that any new commission be appointed only after Statistics Canada releases the most current dissemination-area data from the preceding census. The result: maps that reflect where Albertans actually live, not where they lived a decade ago.",
			census_p2:
				'The Lunty committee is operating under the existing statute, which sets no census-timing requirement, and cannot unilaterally delay past its November 2026 deadline. This recommendation applies to a future amendment to the <em>Electoral Boundaries Commission Act</em>, not to the current process. The tension is real: a committee required to deliver a map by November is working from data already five years old by then — naming the constraint is more useful than pretending it does not exist.',
			closing:
				"Neither of these is a finding about the current commission's maps. They are observations about a system that makes accurate electoral analysis harder than it needs to be. They are offered here as practical suggestions, not conclusions. Both are genuinely fixable, and fixing them would make every future commission — and every future audit — work from better ground."
		}
	},
	editorial_canada: {
		heading: 'Context: Canada is different — and similar',
		p1: 'Canada belongs to the same family as the U.S., the U.K., and Australia. We elect single members from geographic districts under first-past-the-post. We redraw the lines periodically — federally after each decennial census, provincially on staggered schedules. We inherited the basic machinery from the same Westminster roots. So far, no surprises.',
		p2: 'What sets Canada apart is the test the lines have to pass.',
		p3: 'In American constitutional law, the binding rule is <em>one person, one vote</em> — districts must have populations as nearly equal as practicable, and large departures require strict justification. In Canadian constitutional law, the binding rule is different. Section 3 of the <em>Canadian Charter of Rights and Freedoms</em> guarantees every citizen the right to vote. In <em>Reference re Provincial Electoral Boundaries (Sask.)</em> — the 1991 Saskatchewan Reference, the leading case — the Supreme Court of Canada interpreted the right as a right to <em>effective representation</em>, not a right to mathematical equality of district populations.',
		p4: "That distinction matters. Effective representation allows district populations to vary, sometimes substantially, when there are good reasons: vast rural geographies one MLA cannot reasonably serve at standard population density, communities of interest that should be kept together, minority representation that mathematical equality would dilute. The Saskatchewan Reference made that flexibility constitutional. The EBCA's 25% population variance — the rule that protects rural Alberta seats — flows directly from it.",
		p5: 'The catch is that flexibility cuts both ways. If a commission can legitimately depart from population equality for the right reasons, it can also depart from population equality for the wrong ones. Canadian law has no American-style mathematical floor to fall back on. It has the effective-representation test, applied by judges, after the fact, in litigation. Most jurisdictions guard against the wrong reasons with structural protections: federal redistricting commissions are insulated by statute and their recommendations take effect automatically if Parliament does not act on them within a deadline. Quebec uses a permanent independent commission whose work the National Assembly can override only with a two-thirds supermajority. British Columbia operates under a similar default-adopt rule.',
		p6: 'Alberta is the exception. Under the <em>Electoral Boundaries Commission Act</em>, the commission\'s report is a recommendation only — the legislature must vote to enact it. Approval is normally a formality. In the 2026 cycle, the commission split 3–2 and produced two competing proposals; the legislature created a separate MLA committee, chaired by a Premier-appointed MLA, to choose between them. Nothing in Canadian constitutional law required the committee to exist. Nothing requires its choice to follow the commission\'s process. This is the structural gap this audit is examining.',
		p7: 'So when Canadian courts say "gerrymander" isn\'t their legal vocabulary, they are not saying the underlying concept does not apply here. They are saying the test is different — effective representation, not mathematical equality. Whether the minority proposal meets that test is exactly the question this audit has measured the geometry against, and exactly the question only a judge can answer definitively. The <em>Saskatchewan Reference</em> reasoning in full, the contrast with other provinces, the standing question, and the available reform pathways are treated in <a href="#references">the references section below</a>.'
	},
	chrome: {
		back_to_top: 'Back to top',
		license_title: 'Creative Commons Attribution-NonCommercial-ShareAlike 4.0',
		license_alt: 'CC BY-NC-SA 4.0',
		license_aria: 'Creative Commons BY-NC-SA 4.0',
		back_to_stakes: '↑ Back to Stakes',
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
				'In §4, click <em>Show flagged districts on map</em> to highlight the Airdrie split and NW Calgary zone.',
			got_it: 'Got it'
		},
		footer: {
			title: 'Alberta Electoral Boundary Audit — May 2026',
			copyright: '© Will Conner 2026 —',
			text_label: 'Text:',
			code_label: 'Code:',
			translation_label: 'Translations:',
			translation_credit: 'Anthropic Fable 5 (AI) — awaiting native-speaker review'
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
			map_2019: '2019',
			// Mobile segmented-button short labels
			map_minority_short: 'Min',
			map_majority_short: 'Maj',
			map_2019_short: '’19',
			// Search
			search_placeholder: 'Search a district…',
			search_aria: 'Search districts',
			search_clear_aria: 'Clear search',
			search_in: 'in {ed}',
			// Zoom / resolution readout
			zoom_aria: 'Zoom',
			res_prefix: '1 pixel ≈',
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
			lines_note_emphasis: 'deliberate choice by the committee',
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
			poll: 'Poll #{id} · in-person votes',
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
			title: 'Miller — a restored rural seat',
			body: 'This area is on the map because of Justice Dallas Miller, the commission’s chair. In an addendum to the final report, he wrote that if the Legislature would not accept cutting two rural ridings, it should instead add two seats — going from 89 to 91 — and restore them. He pointed to this spot, around Clearwater and western Mountain View counties west of Red Deer, as where one of those rural seats should go. It’s sketched from county lines as a placeholder, not an official boundary, until the next commission redraws the map.'
		},
		flags: {
			'banff-town': {
				title: 'Banff — the town carved out of the park',
				body: "Banff sits inside a federal national park, as a small municipal island. The minority groups the townsite with Canmore — the next town down the Bow Valley — in “Canmore-Kananaskis,” and leaves the uninhabited park as the riding that carries Banff's name. The boundary hugs the town because it's the only populated spot for miles. It looks like a mistake, but it follows real geography."
			},
			'banff-park': {
				title: 'North of Banff — “Rocky Mountain House–Banff Park”',
				body: "“Rocky Mountain House–Banff Park” is one of the minority's proposed ridings, made up largely of uninhabited national park; the town of Banff sits in a neighbouring riding to the south. The minority applied the Electoral Boundaries Commission Act's smaller-population provision to this riding — a choice the commission's chair addressed in the final report."
			},
			'airdrie-split': {
				title: 'Airdrie — split four ways',
				body: "Airdrie's growth and its commute to Calgary (about 76% of out-commuters) could have anchored a single new Airdrie-area seat — the kind the data supports. The minority instead splits the city across four ridings; the population math doesn't require it, and no submission proposed it. On the audit's cracking-signature test this four-way split meets every criterion — Airdrie's residents end up a minority in all four ridings, with no seat the city controls — where the majority's two-way split shows none. This is a community split, invisible to the partisan-fairness tests; the audit measures the structural effect, not intent. (Academic §5.3.2.)"
			},
			'nolan-hill-cochrane': {
				title: 'Calgary-Nolan Hill–Cochrane',
				body: "Cochrane's commute to Calgary could have justified pairing it with the city — but the 2021 journey-to-work data spreads that flow city-wide (about a third of workers; half work within Cochrane) and doesn't point to Nolan Hill. The minority's narrow corridor to the Nolan Hill ward — the shape the chair called a lasso — reaches further than the data, and no submission proposed it. The audit reads this as cracking-adjacent: it thins Cochrane's voice, but Cochrane (about 34,000) is too small for a seat of its own, so it stops short of a formal cracking sign. (Academic §5.3.2.)"
			},
			'olds-airdrie-reach': {
				title: 'Olds–Three Hills–Didsbury — the Airdrie reach',
				body: "A rural riding keeping the Highway 2 towns — Olds, Didsbury, Three Hills — together is well supported; Beiseker-area residents wrote in favour of it. It could have stayed within those communities. The minority's version instead reaches south into the northern edge of Airdrie, an extension the population math doesn't require. The reach is part of how the four-way Airdrie split works — each piece of Airdrie absorbed into a larger rural seat — which the audit reads as part of the cracking pattern. (Academic §5.3.2.)"
			},
			chestermere: {
				title: 'Chestermere — split between two ridings',
				body: "Chestermere's heavy commute to Calgary (86% of out-commuters) could have supported keeping it whole and near the city — which residents who opposed a Calgary merger also wanted. The minority instead slices a southern piece into a specific Calgary district it shares no schools or transit with, and that slice fails the population test. The audit reads the bleed into a Calgary district as cracking-adjacent — a community-of-interest split that thins Chestermere's voice without rising to a formal cracking signature. (Academic §5.3.2, §5.8.4.)"
			},
			'red-deer': {
				title: 'Red Deer — the hybrid ridings',
				body: "Red Deer's regional ties to Blackfalds, Sylvan Lake, Lacombe and Innisfail could have grouped those towns together — a city councillor and residents proposed similar hybrids. The minority's version instead folds parts of the city itself into town-led ridings, thinning urban Red Deer's vote; its “shared schools” rationale also doesn't hold (different school divisions). Folding a city into town-led ridings is the pattern the audit calls hybridization — consistent with cracking, achieving the partisan effect inside the hybrid ridings rather than across them. (Academic §5.3.5.)"
			},
			'st-albert': {
				title: 'St. Albert — competing configurations',
				body: "Either map's version of St. Albert could rest on a reasonable basis. The audit simply found no submission backing the minority's specific alternative — and since citizens rarely name a commission's exact boundaries, it treats the evidence here as thin, not clearly for or against."
			},
			'calgary-zone-a-packing': {
				title: 'Calgary north & east — a packing signature',
				body: "The commission chair didn't flag this one — the audit's own math does. Across Calgary's north and east (the audit's “Zone A,” north and east of the Bow River), the minority map's districts run about 11.5% larger than the provincial average, against 2.8% on the majority map. Packing means concentrating one side's voters into fewer, larger districts, so each of their ballots weighs a little less; Zone A is NDP-competitive, and 13 of its 17 districts were NDP-won in 2023. The audit measures the structural effect, not intent. (Academic §5.3.1.)"
			}
		}
	}
} as const;
