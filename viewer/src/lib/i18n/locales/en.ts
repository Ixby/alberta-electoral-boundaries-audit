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
				'"Gerrymander" is not a term Canadian courts use. But if it were — in the everyday sense most people mean by it — the evidence in this audit would reasonably support calling the minority proposal, if enacted, a heavily gerrymandered map. Every structural test this audit runs flags the minority proposal; none flag the alternative (the majority proposal).'
		},
		q2: {
			heading: 'What does "gerrymander" mean in Canadian law?',
			body:
				'It doesn\'t. The Canadian test is different: whether the boundaries give voters effective representation under section 3 of the Charter. The minority proposal raises serious questions under that test; only a judge can answer them definitively, and no one has asked one yet.'
		},
		q3: {
			heading: 'What does it mean for Albertans?',
			body:
				"At a 50/50 provincial vote, the audit's measurements place the minority proposal at a structural extreme — fewer than 100 of the 1.01 million neutral comparison maps produce the same kind of seat imbalance. That imbalance matters because at 58 of 87 seats — a two-thirds supermajority — the governing party unlocks extraordinary procedural powers: it can waive standard notice periods and push public bills through multiple legislative stages in a single day, bypassing deliberation checks that normally constrain it. Whether the minority proposal's tilt is large enough to push one party past that 58-seat threshold at vote shares other than 50/50 is a question this audit has not yet tested. Whether the tradeoff itself is acceptable is a question for Albertans, not for this audit."
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
		map: 'Map',
		split: 'The Split',
		litmus: 'Litmus Test',
		crack_pack: 'Crack & Pack',
		impact: 'Impact',
		gerrymanders: 'Gerrymanders',
		november: 'November',
		invisible: 'Invisible',
		retractions: 'Retractions',
		references: 'References',
		resources: 'Resources'
	},
	hero: {
		h1: 'Alberta Electoral Boundary Audit',
		subtitle:
			"Alberta's commission produced two riding maps in 2026. This audit compared them — using the same tests, applied equally to both — to ask whether they treat voters the same way.",
		badge: 'Official Elections Alberta maps — Published May 2026',
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
		btn_aria: 'Open interactive map'
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
		p5: 'The rest of this page walks through what the two proposed maps actually do.'
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
	law: {
		title: 'Legal context — Alberta Electoral Boundary Audit',
		heading: 'The legal context',
		lede: 'Deeper treatment of why "gerrymander" is not the legal vocabulary in Canada, what the Charter section 3 "effective representation" test actually requires, how comparable jurisdictions structure their commissions differently, and what reform pathways exist for Alberta.',
		coming_soon:
			'This route is under active development. The current homepage already names the constitutional frame in Section 7 ("Canada is different — and similar"); the deeper treatment — the Saskatchewan Reference reasoning in full, the standing question for a Charter challenge, and a comparison table of provincial commission structures — lands here as it is drafted. See the editorial scaffold in the project repository under proposals/verdict_and_glossary_draft.md.',
		back: '← Back to the homepage'
	},
	methods: {
		title: 'How we tested — Alberta Electoral Boundary Audit',
		heading: 'How we tested',
		lede: 'Deeper treatment of the 1.01M-plan ReCom ensemble, the five pre-registered structural tests, the targeted-procedure (hill-climbing) test, the sampler cross-validation, and the pre-registration / falsification framework.',
		coming_soon:
			'This route is under active development. The current homepage names the headline numbers in the verdict block and the structural tests in passing; the deeper treatment — the lane-1 vs lane-2 framing, the four statistical measures explained, the five pre-registered structural tests with their pass/fail thresholds, and reproduction instructions — lands here as it is drafted. See the editorial scaffold in the project repository under proposals/verdict_and_glossary_draft.md.',
		back: '← Back to the homepage'
	},
	section7: {
		heading: 'Canada is different — and similar',
		p1: 'Canada belongs to the same family as the U.S., the U.K., and Australia. We elect single members from geographic districts under first-past-the-post. We redraw the lines periodically — federally after each decennial census, provincially on staggered schedules. We inherited the basic machinery from the same Westminster roots. So far, no surprises.',
		p2: 'What sets Canada apart is the test the lines have to pass.',
		p3: 'In American constitutional law, the binding rule is <em>one person, one vote</em> — districts must have populations as nearly equal as practicable, and large departures require strict justification. In Canadian constitutional law, the binding rule is different. Section 3 of the <em>Canadian Charter of Rights and Freedoms</em> guarantees every citizen the right to vote. In <em>Reference re Provincial Electoral Boundaries (Sask.)</em> — the 1991 Saskatchewan Reference, the leading case — the Supreme Court of Canada interpreted that right as a right to <em>effective representation</em>, not a right to mathematical equality of district populations.',
		p4: "That distinction matters. Effective representation allows district populations to vary, sometimes substantially, when there are good reasons: vast rural geographies one MLA cannot reasonably serve at standard population density, communities of interest that should be kept together, minority representation mathematical equality would dilute. The Saskatchewan Reference made that flexibility constitutional. The EBCA's 25% population variance — the rule that protects rural Alberta seats — flows directly from it.",
		p5: 'The catch is that flexibility cuts both ways. If a commission can legitimately depart from population equality for the right reasons, it can also depart from population equality for the wrong ones. Canadian law has no American-style mathematical floor to fall back on. It has the effective-representation test, applied by judges, after the fact, in litigation. Most jurisdictions guard against the wrong reasons with structural protections: federal redistricting commissions are insulated by statute and their recommendations take effect automatically if Parliament does not act on them within a deadline. Quebec uses a permanent independent commission whose work the National Assembly can override only with a two-thirds supermajority. British Columbia operates under a similar default-adopt rule.',
		p6: 'Alberta is the exception. Under the <em>Electoral Boundaries Commission Act</em>, the commission\'s report is a recommendation only — the legislature must vote to enact it. That is normally a formality. In the 2026 cycle, the commission split 3–2 and produced two competing proposals; the legislature created a separate MLA committee, chaired by a Premier-appointed MLA, to choose between them. Nothing in Canadian constitutional law required that committee to exist. Nothing requires its choice to follow the commission\'s process. That is the structural gap this audit is examining.',
		p7: 'So when Canadian courts say "gerrymander" isn\'t their legal vocabulary, they are not saying the underlying concept does not apply here. They are saying the test is different — effective representation, not mathematical equality. Whether the minority proposal meets that test is exactly the question this audit has measured the geometry against, and exactly the question only a judge can answer definitively. The longer legal treatment — the <em>Saskatchewan Reference</em> reasoning in full, the contrast with other provinces, the standing question, and the available reform pathways — lives at <a href="?lang={lang}#section-7">the legal route</a>.'
	}
} as const;
