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
	}
} as const;
