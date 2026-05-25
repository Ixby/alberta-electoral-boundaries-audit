#!/usr/bin/env node
/**
 * sync-check.mjs — flag drift between proposals/verdict_and_glossary_draft.md
 * and viewer/src/lib/i18n/locales/en.ts.
 *
 * The editorial draft (proposal) carries the canonical prose + rationale notes.
 * The locale file carries runtime strings rendered by +page.svelte. The two
 * are maintained in parallel; this script catches accidental drift.
 *
 * What it checks: for each tracked key (see PROBE list), a substantive prose
 * snippet from en.ts should appear inside the proposal markdown. Plain
 * substring match, normalised to strip HTML tags so <em>foo</em> in the
 * locale file matches *foo* / plain "foo" in the proposal.
 *
 * Exit 0 if all probes match. Exit 1 if any miss (also prints a diff line so
 * the maintainer can see which key drifted).
 *
 * Usage: node scripts/sync-check.mjs
 */
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(__dirname, '..', '..');
const proposalPath = resolve(repoRoot, 'proposals/verdict_and_glossary_draft.md');
const localePath = resolve(repoRoot, 'viewer/src/lib/i18n/locales/en.ts');

const proposal = readFileSync(proposalPath, 'utf8');
const locale = readFileSync(localePath, 'utf8');

/**
 * Each probe picks a distinctive phrase from one locale string and checks
 * that the same phrase appears in the proposal. Probes are anchored on
 * substrings that are unlikely to drift accidentally (proper nouns, exact
 * numbers, distinctive phrasing) rather than common words.
 *
 * To add a probe: pick a key from en.ts that is also in the proposal, copy
 * a 6-12 word fragment from the locale string that uniquely identifies it,
 * and add it to PROBES below.
 */
const PROBES = [
	// Opener
	{ key: 'opener.body', anchor: 'Rural, Urban, curious, wonk, journalist, lawyer, academic, politician' },
	{ key: 'opener.body', anchor: 'peer inside the machine' },
	// Verdict
	{ key: 'verdict.q1.body', anchor: 'reasonably support calling the' },
	{ key: 'verdict.q1.footnote', anchor: '"majority" and "minority" names come from a 3–2 split' },
	{ key: 'verdict.q2.body', anchor: 'whether the boundaries give voters' },
	{ key: 'verdict.q3.body', anchor: 'two-thirds supermajority) the governing party unlocks extraordinary procedural powers' },
	// Boundary card
	{ key: 'boundary.heading', anchor: "What this audit can and can't tell you" },
	{ key: 'boundary.can_1', anchor: 'Fewer than 1 in 14.5 million randomly generated comparison maps' },
	// Section 1 (onboarding)
	{ key: 'editorial_intro.heading', anchor: 'What is redistricting, and why it matters' },
	{ key: 'editorial_intro.p1', anchor: 'one MLA, one district, one vote' },
	{ key: 'editorial_intro.p3', anchor: 'split 3–2 on what the map should look like' },
	// Section 5 (ladder)
	{ key: 'editorial_reflect.intro_q1', anchor: 'Where does your MLA live' },
	{ key: 'editorial_reflect.intro_q3', anchor: 'demands of the head dominate the demands of the tails' },
	{ key: 'editorial_reflect.region_p3', anchor: 'rural communities are being attached as the' },
	{ key: 'editorial_reflect.province_p', anchor: 'sum every district\'s answers to the three questions' },
	// Section 6 (history)
	{ key: 'editorial_history.p1', anchor: 'Massachusetts governor Elbridge Gerry' },
	{ key: 'editorial_history.p3', anchor: 'Rucho v. Common Cause' },
	// Section 7 (Canada)
	{ key: 'editorial_canada.p3', anchor: 'Saskatchewan Reference' },
	{ key: 'editorial_canada.p4', anchor: '25% population variance' }
];

/**
 * Normalise text for comparison: strip <em>/<strong> tags, normalise quotes,
 * collapse whitespace. The proposal uses Markdown emphasis (*foo*) and the
 * locale file uses HTML (<em>foo</em>); both should match the same normalised
 * form.
 */
function normalise(s) {
	return s
		.replace(/<\/?em>/g, '')
		.replace(/<\/?strong>/g, '')
		.replace(/\\\*/g, '*') // Markdown-escaped asterisks
		.replace(/\\'/g, "'")
		.replace(/\\"/g, '"')
		.replace(/\s+/g, ' ')
		.trim();
}

const normalisedProposal = normalise(proposal);
const normalisedLocale = normalise(locale);

let failures = 0;
for (const { key, anchor } of PROBES) {
	const a = normalise(anchor);
	const inProposal = normalisedProposal.includes(a);
	const inLocale = normalisedLocale.includes(a);
	if (!inProposal && !inLocale) {
		console.error(`MISS  ${key}: anchor missing from BOTH files — probe is stale, update it`);
		failures++;
	} else if (!inProposal) {
		console.error(`DRIFT ${key}: locale has "${anchor}" but proposal does not`);
		failures++;
	} else if (!inLocale) {
		console.error(`DRIFT ${key}: proposal has "${anchor}" but locale does not`);
		failures++;
	}
}

if (failures === 0) {
	console.log(`OK    ${PROBES.length} probes matched between proposal and locale`);
	process.exit(0);
} else {
	console.error(`\nFAILED  ${failures} of ${PROBES.length} probes drifted.`);
	console.error('Resolve: edit either the proposal (proposals/verdict_and_glossary_draft.md)');
	console.error('or the locale (viewer/src/lib/i18n/locales/en.ts) so the prose matches.');
	process.exit(1);
}
