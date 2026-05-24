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
	}
} as const;
