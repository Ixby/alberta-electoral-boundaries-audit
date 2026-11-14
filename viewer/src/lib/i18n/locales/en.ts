// English — source of truth.
// Mirrors the editorial content in proposals/stakes_and_glossary_draft.md.
export default {
	selector: {
		label: 'Choose language'
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
	stakes: {
		q1: {
			heading: 'Is the proposed map a gerrymander?',
			body:
				'"Gerrymander" is not a term Canadian courts use, and this audit does not apply it as a verdict. What the audit can say is narrower and factual: four of the five structural tests it runs flag the <em>minority proposal</em> and none flag the alternative (the <em>majority proposal</em>); the fifth test is neutral for both. Whether that pattern amounts to what people informally mean by a "gerrymander" is a judgment this audit leaves to the reader.',
			footnote:
				'The "majority" and "minority" names come from a 3–2 split among the Electoral Boundaries Commission (chaired by Justice Miller), which produced two competing proposals rather than a single recommendation. The legislature has since set both aside and referred redistricting to a six-MLA committee chaired by Brandon Lunty (a UCP MLA); the committee oversees a separate five-member Independent Advisory Panel — a chair, retired Court of Appeal justice Brian O\'Ferrall, plus two members nominated by the Premier (Hon. Monte Solberg and Darwin Durnie) and two by the Leader of the Opposition (Dr. Gerard Kennedy and Brent Robinson) — tasked with producing a new 91-seat boundary proposal before the November 2026 deadline.'
		},
		scorecard_h: 'The scorecard',
		scorecard_fig_alt:
			'Scatter plot. Across: efficiency gap. Up: number of structural tests flagged. The 2019 map and the commission majority\'s map sit together at lower left. The commission minority\'s map sits alone at upper right, on the four-of-five line and just short of the dashed efficiency-gap line at about 4.1%. The 2019 map is marked 0 of 4 run.',
		scorecard_intro:
			'Two independent measurements applied to both maps under the same pre-registered thresholds. Structure uses only the shape of the lines — no election results. Numbers tests how the lines convert votes into seats. Both lanes reach the same conclusion.',
	},
	head: {
		title: "Alberta's Electoral Map, Audited",
		meta_description:
			'A proposed 91-riding map for Alberta is before the Legislature. I checked it, and the commission\'s two maps before it, against tests written down in advance. On provisional results, the new map does not repeat the lean toward the UCP found in the commission minority\'s map.'
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
		route_methods: 'How I checked',
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
		crack_pack: 'Cracking and packing',
		for_you: 'What this means for you',
		impact: 'Impact on the ground',
		gerrymanders: 'Clean gerrymanders',
		history_full: 'A history of gerrymandering',
		canada: "Canada's different",
		lunty: 'Lunty',
		suggestions: 'Reform suggestions',
		smoking_gun: 'Evidence, not proof',
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
		happened: 'The commission\'s two maps',
		does: 'What the map does',
		law: 'What the law requires',
		system: 'Who drew the maps',
		know: 'How I checked',
		test: 'The November test',
		november: 'The panel\'s map, checked',
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
		group_pages: 'Pages',
		answer: 'The short answer'
	},
	hero: {
		h1: 'Laws, Norms, & Statistics: An Audit of the 2026 Alberta Electoral Boundaries Commission Reports',
		subtitle:
			"Alberta's commission produced two competing riding maps in 2026. I ran the same tests on both and asked one question: do they treat voters the same way?",
		badge: 'Cover: the commission\'s minority map (final report, March 2026)',
		cover_note: 'Click the map to zoom in. Switch between the commission\'s two maps and the 2019 map, the one in use today. Pin the view and flip between them. The lines move. The voters stay put. The panel\'s new map is not in the explorer yet.',
		image_alt:
			'Alberta electoral district map — minority commission proposal, coloured by 2023 vote',
		map_hint: 'Click to explore interactively',
		btn_title: 'Click to open interactive map',
		btn_aria: 'Click to explore interactively'
	},
	glossary: {
		more_link: 'Learn more →',
		'electoral-district': {
			term: 'Electoral division',
			definition:
				'The name Alberta\'s laws give a riding. On this site it shows up only in names and quotes. Everywhere else, it\'s riding.'
		},
		riding: {
			term: 'Riding',
			definition:
				'The area that elects one MLA. Alberta\'s laws call it an electoral division. This site says riding, except in names and quotes.'
		},
		mla: {
			term: 'MLA',
			definition:
				'Member of the Legislative Assembly: the person one riding elects to represent it in Alberta\'s Legislature.'
		},
		ucp: {
			term: 'UCP',
			definition:
				'The United Conservative Party, Alberta\'s governing party. It formed in 2017, when the Progressive Conservatives and the Wildrose Party merged, and it has held government since 2019.'
		},
		ndp: {
			term: 'NDP',
			definition:
				'The New Democratic Party (Alberta NDP), the official opposition. It held government from 2015 to 2019.'
		},
		gerrymander: {
			term: 'Gerrymandering',
			definition:
				'Drawing lines to give a party an advantage. The word comes from an 1812 map in Massachusetts. Canadian law has no offence by that name. That limits what a court will call it. Whether it happens is another matter. The closest legal test is effective representation under section 3 of the Charter. This audit measures what a map does, and it calls no map a gerrymander.'
		},
		cracking: {
			term: 'Cracking',
			definition:
				'Splitting a group of voters across many ridings so they never make up a majority in any one. Divide a city among four ridings, for example, and its voters can be outnumbered in each.'
		},
		packing: {
			term: 'Packing',
			definition:
				'Crowding one party\'s voters into a few ridings. The party wins those ridings by huge margins but "wastes" many votes, and fewer of its voters are left to compete elsewhere.'
		},
		anchoring: {
			term: 'Anchoring',
			definition:
				'How much of a map\'s boundaries run along existing city and town lines. A well-anchored map mostly follows them. This test couldn\'t tell the 2026 commission maps apart: both sit close to the 2019 map\'s 75%.'
		},
		'charter-s3': {
			term: 'Section 3 of the Charter',
			definition:
				'The part of the Canadian Charter of Rights and Freedoms that gives citizens the right to vote. Canadian courts read it as a right to "effective representation". On that reading, "one person, one vote" is not a strict rule.'
		},
		'effective-representation': {
			term: 'Effective representation',
			definition:
				'The standard Canadian courts use to judge electoral maps. It means every voter should have a real voice. Ridings of equal population are part of that. So are community ties, geography and the representation of minorities. The leading statement is the Supreme Court of Canada\'s 1991 Saskatchewan Reference.'
		},
		ebc: {
			term: 'The commission',
			definition:
				'The independent Electoral Boundaries Commission, which draws Alberta\'s ridings under the Act. In 2026 it had a chair, Justice Miller, and four members: two nominated by the Premier and two by the Leader of the Opposition. It held hearings in sixteen communities and published a draft map in October 2025. On March 23, 2026 it filed its final report, split 3 to 2. That is why there were two maps. The chair and the two members the Opposition nominated signed the majority map. The two the Premier nominated signed the minority map. Under s.9 of the Act, the majority\'s report is the commission\'s report. The Assembly set both maps aside.'
		},
		'lunty-committee': {
			term: 'The committee',
			definition:
				'The Select Special Committee on Electoral Boundaries: six MLAs, four UCP and two NDP, chaired by UCP MLA Brandon Lunty. Government Motion 37 created it after the Assembly set both commission maps aside. The motion was put on notice April 16 and moved, debated and passed on April 21, 2026. The committee appointed the panel and oversaw its work. No law required it to hold public hearings, and it held none. On October 28 it voted 3 to 2 to end its review without observations. On November 2, 2026 it sent the panel\'s report to the Assembly.'
		},
		'advisory-panel': {
			term: 'The panel',
			definition:
				'The Independent Advisory Panel, which the committee appointed under Government Motion 37 to draw a 91-riding map. Its chair, retired Court of Appeal justice Brian O\'Ferrall, was the Premier\'s nominee; the committee named him on June 2, 2026. On June 9 it named four members: the Hon. Monte Solberg and Darwin Durnie, nominated by the Premier, and Dr. Gerard Kennedy and Brent Robinson, nominated by the Leader of the Opposition (committee report, p. 9). The panel reported on October 22, 2026, and it split too: its report includes a minority opinion with an alternative map (paragraph 167). MLAs decide whether the panel\'s map becomes law.'
		},
		ebca: {
			term: 'EBCA',
			definition:
				'The Electoral Boundaries Commission Act, the Alberta law that sets the rules a new map must follow. A riding may have up to 25% more or fewer people than average. Under s.15(2), up to four remote ridings may have as many as 50% fewer, if each meets at least three of five tests in the Act.'
		},
		ensemble: {
			term: 'Computer-drawn maps',
			definition:
				'1,010,000 maps of Alberta that a computer drew from the same 4,765 voting areas, each with 87 ridings. Each riding stays near the same population and in one piece. The computer never sees a vote. So the maps show what a map drawn with no aim looks like, and that is all this site means when it calls them neutral. A real map counts as unusual when it falls outside what almost all of them produce.'
		},
		efficiency_gap: {
			term: 'Efficiency gap',
			definition:
				'The two parties\' wasted votes, compared. A vote is wasted when it goes to a loser, or to a winner beyond what the win needed. A large gap points to a one-sided map. On this site a positive gap favours the UCP.'
		},
		mean_median: {
			term: 'Mean-median gap',
			definition:
				'Take a party\'s vote share in each riding. The mean-median gap is the distance between the average of those shares and the middle one. A large gap suggests the party\'s voters are spread in a way that wastes votes.'
		},
		declination: {
			term: 'Declination',
			definition:
				'How one-sided each party\'s wins are: blowouts or narrow wins. On the commission minority\'s map it points toward the UCP, the same way as the other measures.'
		},
		seats_5050: {
			term: 'The 50-50 test (seats at a tie)',
			definition:
				'A tie, staged on paper: every riding\'s vote moves by the same amount until the province splits exactly 50-50, and then the seats are counted. That sets aside who actually won and measures the lean built into the map itself. In a tie, a typical computer-drawn Alberta map gives the UCP 44.8% of the seats, because the UCP\'s rural wins are wider than the NDP\'s city wins.'
		},
		fsa: {
			term: 'Forward sortation area (FSA)',
			definition:
				'The first three characters of a Canadian postal code (letter, digit, letter). About 150 FSAs cover Alberta.'
		},
		percentile: {
			term: 'Percentile',
			definition: 'Where a real map ranks among the computer-drawn maps. A map at the 78th percentile leans further toward the UCP than 78 of every 100 of them. One at the 99.99th leans further than all but about 1 in 10,000.'
		},
		hybrid: {
			term: 'Hybrid riding',
			definition: 'A riding that joins part of a city to rural or small-town areas. When this site counts ridings that cross a city limit, a riding crosses one if 5% to 95% of its people live in the city.'
		},
		election_day: {
			term: 'Election-day ballots',
			definition: 'Ballots cast at a polling station on election day. Elections Alberta reports them for each voting area, so the audit knows where they were cast.'
		},
		all_ballots: {
			term: 'All ballots',
			definition: 'Every 2023 ballot, early ones included: advance, mobile and special ballots, and Vote Anywhere. About half were not cast on election day. Those are reported only for each old riding, so where they fall inside a new riding is an estimate. The registered rule, rule P (Amendment 14), places them only among people who did not vote on election day, using Alberta data only. The older rule, which spreads them in step with election-day votes, is kept as a check. Since November 7, 2026, every vote-based test is reported on all ballots, with election-day results kept beside them. The one exception is the combined odds figure, which exists only on election-day ballots. Both changes, rule P and the switch to all ballots, were <strong>not blind</strong>: each was made after some all-ballots results had been seen.'
		},
		reconstruction: {
			term: 'Reconstruction',
			definition: 'The panel\'s map lines, rebuilt from the pages of its report, because the official map files are not public yet. The first two accuracy checks failed: 49.0%, then 13.8% of voting areas landed in the wrong riding, against a 10% limit. The third check passed. It was a repeat run on pages already seen, so it does not count as a fresh test of accuracy. That makes every result for the panel\'s map <strong>provisional</strong>: it may change when the official files come out. A seat is <strong>too close to call</strong> when its winning margin is smaller than the votes in the voting areas that a differing line cuts through.'
		}
	},
	// Main page, rewrite of 2026-10-29 (proposals/site_rewrite_2026-10-29).
	// Generated from the accepted draft together with its markup in +page.svelte.
	home: {
		hero: {
			kicker: 'Alberta Gerrymander:',
			h1: "Alberta's new 91-riding map is mostly fair. How it got made is the real story.",
			subtitle: 'A commission split and filed two maps. One leaned toward the UCP further than almost any map a computer drew without seeing a vote. The Legislature adopted neither and handed the job to a committee of MLAs. The map that came out of that is before the Legislature now. This is what it does, how it got here, and how I checked.',
			status: 'Where it stands. An advisory panel drew the new map, and a committee of six MLAs sent it to the Legislature on Monday, November 2, 2026. On November 4 the Assembly voted 45 to 36 to concur in it and to urge the government to introduce a bill. It isn\'t law unless a bill passes. The official map files still aren\'t public, so my results for it are provisional. When those files come out, I\'ll score them within 72 hours.',
			week: "<strong>This week.</strong> The rules that decide the November verdict were written down in June 2026, and <a href=\"https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/preregistration/november_2026_scoring_spec.md\" rel=\"noopener\">they're dated in the project's repository</a>. Three side tests and the choice of comparison set were added October 29–31, after opposition MLAs had described parts of the map at a committee meeting. Seven amendments followed on November 2–7, after the panel's report was tabled; the last three were written after results had been seen. The provisional scores are in the November section below. The first check is against the one recommendation the government cited: <a href=\"#recommendation-5\">Recommendation 5</a>.",
		},
		happened: {
			h: 'The commission\'s two maps',
			p1: 'Every so often Alberta redraws its ridings. A riding is the patch of the province that elects one MLA, and where its edges fall can decide who wins. This time three bodies handled the map, in this order: the commission, the committee and the panel.',
			p2: '<strong>First, the commission.</strong> The Electoral Boundaries Commission is independent. A judge chairs it, and it has four other members: two nominated by the Premier and two by the Opposition. On March 23, 2026 it split 3 to 2. The chair and the Opposition\'s two nominees signed the majority map. The Premier\'s two nominees signed the minority map (<a href="https://www.assembly.ab.ca/about/news-and-announcements/2025/03/28/electoral-boundaries-commission-to-soon-begin-consultations" rel="noopener">Legislative Assembly of Alberta, March 28, 2025</a>). Both maps fit the Act\'s number rules. The majority argued the minority\'s map would likely fail the Charter\'s test. No court has ruled.',
			p3: 'The majority map looks like what you get when you draw with no aim. On the measures that use votes, the minority map doesn\'t. Here is where the two part ways. The first two points compare the maps with each other; the last two use votes.',
			li1: 'The minority map splits Airdrie four ways. Outside Airdrie East, the city\'s residents are outnumbered in every riding they land in.',
			li2: 'It makes ridings in north-east and central Calgary bigger, so a vote there counts for a little less.',
			li3: 'Split the vote exactly 50-50 and on the minority map the UCP still wins 46 of the 89 seats (51.7%). That is a majority of seats without a majority of votes. Only 69 of 1,010,000 computer-drawn maps give more, and all 69 give 45 of 87 (51.72%), just above it.',
			li4: 'Replay the 2023 election on election-day ballots and the minority map gives the UCP 60 of 89 seats; the majority map, 55. Count all ballots and the registered count is 57 and 48. The older way of placing early ballots, kept as a check, gives 55 and 48. Both counts are partly an estimate, because early ballots have to be placed inside the new ridings.',
			p4: '<strong>Then, the committee.</strong> The Legislature adopted neither map. It handed the job to a committee of MLAs instead.',
			box_h: "What I can say, and what I can't",
			can1: 'I can say the commission\'s minority map sits far outside what the computer drew. Put four fairness measures together and none of the 1,010,000 maps is as far out in the UCP\'s favour; on a rank-based version, seven are. Taken one at a time, three of the four put it at the far edge (election-day ballots).',
			can2: 'All four of those measures lean the same way: toward the UCP.',
			cant1: "That any commissioner meant to do this. A test can measure what a map does. It can't show motive.",
			cant2: "That the government directed its nominees. I found no evidence of coordination, and appointing someone isn't evidence of it.",
			cant3: 'That the pattern will come back. The map that has it was never enacted, and on provisional results the panel\'s map doesn\'t repeat it.',
			cant4: "How a court would rule, or what the Assembly will enact.",
			p5: '<strong>About the word in the title.</strong> Gerrymandering means drawing the lines to give a party an advantage. Both sides used the word on the floor of the Legislature on November 4, 2026, and it is the name this fight goes by. That is why it is in the title. Canadian law has no offence by that name, so no court will rule on gerrymandering as such. That doesn\'t mean it can\'t happen here. I measure what maps do. I don\'t call any of them a gerrymander.',
			p6: '<strong>Reading the cover map.</strong> Each of Alberta\'s 4,765 voting areas is coloured by its 2023 vote: orange for NDP, blue for UCP. The colour is deep only where many people live, so wide, empty areas stay pale. Land with no polling station and no recorded voters is white. The lines are the commission minority\'s 89 proposed ridings. <a href="__BASE__/explorer">Open the map explorer</a> to switch maps.',
		},
		does: {
			h: "What the minority map does",
			p1: "The two commission maps agree on most of Alberta. Where they differ, here is what the minority map chose, and what each choice does.",
			h3_1: "One city, four districts",
			p2: '<strong>Airdrie has to be split.</strong> It has 85,805 people (2024 municipal census) and one city council. The law caps each riding at one and a quarter times the provincial average, and Airdrie is over the cap. So it needs at least two ridings. The majority map gives it two.',
			p3: 'The minority map gives it four. Airdrie East takes more than half the city. Most of the rest goes to two ridings shared with Calgary, where Calgary residents outnumber Airdrie\'s. About 350 people go to a rural riding. Airdrie would have four MLAs. Most of the voters who elect three of them live outside Airdrie. Splitting a community so thinly that it can\'t decide any seat has a name: cracking. I tested for it. The test was added later: I wrote its rules in the same session that first ran it. It needs Airdrie\'s residents outnumbered in every piece. In Airdrie East they are not, so by the test\'s own rule this is not cracking. The majority map\'s two-way split is not cracking either.',
			p4: "On the minority map, the test doesn't flag the city as a whole. But the part of Airdrie outside Airdrie East, about 45% of the city, is outnumbered in every riding it lands in, which is what cracking describes. No registered test scores that part on its own.",
			h3_2: "Bigger districts in north-east and central Calgary",
			p5: '<strong>Calgary\'s north-east and centre.</strong> The more people in your riding, the less your one vote counts. On the minority map, the seventeen ridings here average 11.5% more people than the provincial average. On the majority map the figure is 2.8%. (On a literal reading of how the zone is defined, the figures are 8.5% to 8.9% against 1.3% to 1.6%. The zone\'s list has a history: it was first written as NDP-competitive ridings against UCP-dominant ones, and later described by geography, with the same ridings.) Crowding one party\'s voters into a few lopsided wins is called packing. I tested for that too, and the test does not find it: the NDP wins eight of the seventeen by margins below the provincial average. Like the Airdrie test, it was written in the same session that first ran it.',
			h3_3: "Districts further from equal size",
			p6: '<strong>Are the minority map\'s ridings closer to equal?</strong> Equal populations are the one value the law puts a number on. I checked on the commission\'s own tables, where the minority map\'s ridings miss the ideal size by 4,707 people on average. The majority\'s miss by 3,180. On 2021 census numbers the averages are close, but the minority map\'s middle riding is still further off (3,938 against 2,827). So on the numbers the commission itself used, the defence that odd lines were needed to balance populations does not work here.',
			h3_4: "Rural tails on urban districts",
			p7: "Still, I'm not saying rural Alberta has too many seats. The Act lets district populations vary by up to 25%, so one rural MLA doesn't have to cover an area the size of southern France. Both maps use that room.",
			p8: '<strong>Part city, part country.</strong> A hybrid riding joins part of a city to rural areas. Count a riding as hybrid when 5% to 95% of its people live in the city, and the minority map has six at Calgary\'s city limit. The majority map has none.',
			h3_5: "Three boundaries the majority called out",
			p9: "The commission's majority, the chair among them, flagged four of the minority's boundaries as geographically anomalous, among them these three:",
			li1: "the Rocky Mountain House–Banff Park extension into uninhabited national-park land;",
			li2: "the lasso-shaped corridor of Calgary-Nolan Hill–Cochrane;",
			li3: "the reach of Olds–Three Hills–Didsbury into north Airdrie.",
			p10: "The flags come from the majority's reply to the minority, so you would expect them to criticise only the minority. So I checked all four against the published maps myself, and three of them hold up.",
			p11: "The majority called the park extension \"a bad faith effort\" to claim a population protection, section 15(2), that is written for remote communities where people actually live. My check undercuts that charge: the division qualifies under s.15(2) even without the extension. The Banff townsite is a separate question: putting it with Canmore makes sense as a community of interest, because the town sits inside a national park it can't grow into. The majority's objection to the empty-park extension still stands. The townsite's placement doesn't affect it.",
			h3_6: "The seat advantage",
			p12: "Split the province-wide vote dead even, and this is the UCP's share of seats on each map:",
			li4: "the median neutral map gives 44.8%, less than an even share, for a reason covered below;",
			li5: "the majority map gives 46.1%, the 78th percentile;",
			li6: "the minority map gives 51.7% (46 of 89), the 99.99th percentile. Only 69 of 1,010,000 neutral maps exceed it, all with 45 of 87 seats (51.72%), a hair above.",
			p13: '<strong>What it takes to win a majority.</strong> I took the 2023 election-day ballots and shifted every riding\'s vote by the same amount, to see how much of the vote the UCP needs on each map. On the minority map it keeps the 45 seats it needs for a majority even if its share of the UCP and NDP vote falls to about 49.2%, a little under half. On the majority map it would need to win that vote by about 9 points.',
			p14: 'Does the size of a majority matter? On 2023 election-day ballots, the commission\'s minority map gives the UCP 60 of 89 seats, a two-thirds majority. On all 2023 ballots, the registered count gives 57, which is not. The older rule for placing early ballots, kept as a check, gives 55. (Where early ballots belong inside the new ridings is an estimate.) In Alberta, two-thirds unlocks no special power. The Assembly decides every question by a simple majority of the votes cast. A simple majority can already pass laws and budgets. It can put a time limit on debate, change the rules of the House, and set every committee\'s membership, which the rules keep in proportion to seats. Conventions, the unwritten rules of politics, need no supermajority either: a simple majority set aside the practice of leaving the map to an independent commission. A majority that size would give a government a cushion. A few MLAs crossing the floor could not threaten it. And a smaller opposition would have fewer members to keep up the work on committees.',
			p15: 'Courts do not review a law while it is being made. Once a new map becomes law, someone can challenge it in court. It would face the same test as any map: effective representation, with every population gap justified. As I read the law, Canada has no rule against partisan advantage as such. The question is whether voters get effective representation. The commission\'s minority map shows how far apart the two can be. None of its choices breaks the Act\'s number rules, and the Act allows splitting cities. The commission\'s majority argued that the map would likely fail the Charter test. No court has ruled on that.',
		},
		law: {
			h: "What the law requires, and what it doesn't",
			h3_1: 'How a map is made can matter too',
			p1: 'Section 3 of the Charter gives every citizen the right to vote. The Supreme Court of Canada reads that as a right to effective representation. In plain terms, your vote should count for roughly as much as a vote in any other riding. There is room for real reasons such as geography or community, as long as each gap is justified. Canadian law has no rule against partisan advantage as such.',
			p2: 'No government can switch this right off. The notwithstanding clause lets a legislature set some Charter rights aside for a time. It does not apply to section 3.',
			p3: 'Courts have also looked at how a map gets made. In 2017 Nova Scotia\'s Court of Appeal found that the province\'s map broke section 3. The government had told its independent commission to change course, so the final map did not reflect the commission\'s own view. The court added that a legislature may still draw a map itself.',
			p4: 'To protect ridings in the Gaspésie, a Quebec law paused the province\'s commission. It passed unanimously. That did not save it. In 2026 the Supreme Court of Canada struck it down (<em>Quebec (AG) v. Lalande</em>, 2026 SCC 13, decided 7 to 2, reasons May 1). Quebec could have protected those ridings in a narrower way. On June 12, 2026, Quebec\'s National Assembly passed its own 127-seat map.',
			h3_2: 'The rules in brief',
			p5: 'The Act sets these rules for the commission:',
			li1: '<strong>Who sits.</strong> Cabinet chooses the chair from a list of eligible roles that includes judges. The Speaker appoints four members who are not MLAs: two nominated by the Premier and two by the Opposition.',
			li2: "<strong>Hearings.</strong> It must hold public hearings before its draft map, and again after.",
			li3: '<strong>Deadlines.</strong> It has seven months to produce a draft map, then five more for its final report.',
			li4: '<strong>Seats.</strong> 91. The Act said 89 when the commission drew its maps. Bill 32, introduced April 23, 2026, raised the number to 91.',
			li5: '<strong>Population.</strong> Every riding has to sit within 25% of the average. Up to four remote ridings may go as low as 50% below average, if the commission finds that at least three of five tests are met. Both rules are explained below.',
			li6: '<strong>Factors.</strong> The commission must consider effective representation. It may also weigh growth, communities of interest, geography and other factors.',
			p6: 'Both commission maps fit inside these rules. Two of the rules need a closer look: the population band, and the exception for remote ridings.',
			h3_3: 'What the law does not require',
			p7: 'On April 21, 2026, Government Motion 37 set both commission maps aside. It handed the work to a committee of six MLAs, four of them from the governing party, with a report due by November 2, 2026. The committee then appointed an advisory panel to draw the map. The motion gave the panel the Act\'s population rules and its list of factors, nearly word for word: the 25% band, the exception for up to four remote ridings, and effective representation first. It left out the hearings. The review was to be expedited, which means done quickly, with no requirement to hold public hearings (Votes and Proceedings, April 21, 2026). As for the Act, most of its rules are addressed to "the Commission". Read plainly, they do not bind the Legislature or a committee of MLAs.',
			li7: 'The Legislature doesn\'t have to adopt a commission\'s map. A map becomes law only if MLAs pass a bill.',
			li8: 'I found no provision that requires a committee of MLAs to hold hearings, be independent, publish a draft or explain its choices.',
			li9: 'Recommendation 5, the one recommendation the government cited, binds no one.',
			li10: 'Elections Alberta says it needs at least a year and a half to prepare for new ridings. That is a planning need. No law makes it a deadline.',
			li11: "Courts don't review a law while it's being made. A challenge can only come after a boundaries law passes.",
			h3_4: "Alberta handed the map to MLAs once before, in 1992",
			p8: 'In 1992 Alberta\'s commission could not agree. Its final report was five separate reports, one from each commissioner. In July 1992 the Assembly passed Motion 24 and handed the work to a Select Special Committee of MLAs chaired by Bob Bogle. The Opposition refused to name members, so four Progressive Conservative MLAs drew the map. Alberta voted on it in the 1993 election. The 2026 commission did not deadlock. A majority signed its report, and the report was set aside anyway.',
			p9: 'In 1994 the Court of Appeal let the 1992 map stand. I have not read the judgment itself, so this account of it comes from others. The 2026 commission\'s report says the court found that the map did not rise to the level of Charter condemnation, but called for “a gradual and steady” change (final report, Appendix D, p. 282). Other published accounts add that the court criticised how the map was made. The committee\'s members could not explain several of its boundaries. One of the smallest ridings was Bogle\'s own. And a proper review was needed before the Legislature\'s term ran out. In 1995 the Legislature amended the Act and changed how commissions are appointed. Alberta used that process from then until 2026.',
			h3_5: 'If the new map is challenged',
			p10: 'Once a new map becomes law, it can be challenged in court. The test is the same as for any map: effective representation, with every population gap justified. Reasons matter. I score the map and the process. Whether it is constitutional is for a court to say.',
		},
		system: {
			h: 'Who drew the maps',
			p1: 'The commission worked in public. It held hearings in sixteen communities and received 1,345 written submissions. It had planned to remove the Lesser Slave Lake riding. Many asked it not to (the minority report counts at least 56), and it dropped the plan.',
			p2: "That came four weeks after the split. Government Motion 37 was put on notice on April 16, then moved, debated and passed on April 21. It created the Select Special Committee on Electoral Boundaries, with six MLAs:",
			li1: "four UCP: Brandon Lunty (chair), de Jonge, Sawyer and Wiebe;",
			li2: "two NDP: Ganley and Gray.",
			p3: '<strong>Last, the panel.</strong> The committee appointed an Independent Advisory Panel to draw a 91-seat map. The Premier nominated its chair, retired Court of Appeal justice Brian O\'Ferrall, and two of its members, the Hon. Monte Solberg and Darwin Durnie. The Opposition nominated the other two, Dr. Gerard Kennedy and Brent Robinson (committee report, p. 9). The panel split too: its minority offered an alternative map. The panel only advises. MLAs decide.',
			p4: 'On May 6, 2026, before the panel\'s chair was named, Alberta\'s acting chief justice wrote to the committee. The courts, she said, would not circulate its request for a judge or give any input on the choice of chair. Her reason: "the irregularity of this process". She added that this passed no judgment on the legislation. The Alberta branch of the Canadian Bar Association then declined too. Both letters are reproduced in the Opposition members\' part of the committee\'s report (pp. 15–16). The panel only advises. The committee\'s MLAs review its report and send it to the Assembly, where MLAs decide. At the committee\'s October 28 meeting, its UCP members voted 3–2 to end the review of the panel\'s report before NDP motions on it were considered. They also voted 3–2 against an NDP motion to disclose what the panel and its consultants were paid (<a href="https://docs.assembly.ab.ca/LADDAR_files/docs/committees/ceb/legislature_31/session_2/20261028_1030_01_ceb.pdf" target="_blank" rel="noopener noreferrer">committee transcript</a>, pp. CEB-73 and CEB-74). The committee defeated an NDP motion to publish whom the panel consulted. A UCP member cited privileged legal advice and the panel\'s independence (p. CEB-75). The committee did not meet again. It had to send the panel\'s report to the Assembly by November 2.',
			p5: "In May, Duane Bratt, Professor of Political Science at Mount Royal University, described the process to me, in private correspondence, as without precedent in Canada. I later found Alberta's 1992 committee. I don't think it is the same thing, and that distinction is mine, not his.",
			p6: "In 1992 the commission couldn't agree. Five commissioners filed five reports, and none had a majority behind it. In 2026 a majority signed one, and under the Act a majority report is the commission's report. Government Motion 37 set it aside anyway. I found no precedent for that part.",
			p7: "On the floor, the government presented its route as following the commission: \"We are adopting the recommendations from the report\" (Government House Leader, Hansard, April 16, 2026). The opposition called it \"retaliation against the independent Electoral [Boundaries Commission].\" The report itself doesn't fully support the government's claim. The majority did say two more seats would have given more effective representation (final report, p. 58), and Recommendation 5 itself says its change “would need to be studied by an all-party Select Special Committee or other equivalent Legislative Committee” (p. 66). But the majority asked the Legislature to adopt its 89-seat map. The one recommendation that proposed 91 seats now came from the chair alone.",
			p8: 'As I read the Act, nothing in it forbids these steps, and no court has ruled on them. But this time the MLAs who oversee the map will also run in it. And a future government of any party can point to this as a precedent.',
			h3_1: 'Recommendation 5: the one the government cited',
			p9: 'To justify giving the job to a committee, the government cited one recommendation in the commission\'s report: Recommendation 5. One person wrote it: the commission\'s chair, Justice Dallas Miller, in an addendum to the majority report. He was "reasonably certain" that with 91 seats no riding outside Edmonton and Calgary would be lost. He added: "My majority colleagues do not agree with me on this point. That is why I am alone in making this recommendation" (final report, p. 66). He also said why he wrote it: it "is formulated for the express purpose of dissuading the Legislature from accepting the minority report." So it was the first thing I checked the panel\'s map against. The result for each part is below.',
			p10: 'It is a fallback, and a narrow one. The commission\'s majority removed two ridings outside Edmonton and Calgary. If the Legislature would not accept that, the chair asked it to change the <em>Electoral Divisions Act</em> from 89 seats to 91, bring those two ridings back, and keep "the rest of the province as we propose" (the majority map) "to the extent possible." Bringing back the two ridings should:',
			li3: '<strong>(a) Leave Airdrie and the south alone.</strong> Change no riding in Airdrie, and none with land south of Airdrie\'s southern city limit, except Drumheller-Stettler. On the majority map that is 41 ridings: both Airdrie seats, all 28 Calgary seats, and the 11 ridings around and south of Calgary. <strong>Result: not met.</strong> The panel\'s map changes 10 of the 41. By their names on the majority map, they are Calgary-Bow, Calgary-West-Elbow Valley, Canmore-Banff, Cochrane-Springbank, High River-Vulcan-Siksika, Lethbridge-East, Lethbridge-West, Livingstone-Macleod, Okotoks-Diamond Valley and Taber-Cardston.',
			li4: '<strong>(b) Leave north Edmonton alone.</strong> Change no Edmonton riding north of the North Saskatchewan River: 11 ridings on the majority map. <strong>Result: met.</strong> All 11 are unchanged.',
			li5: '<strong>(c) Put south Edmonton back.</strong> Every Edmonton riding south of the river goes back to the commission\'s October 2025 draft map, the one it published for comment before the final split. The committee may add Nisku to Edmonton-South East if it wants Leduc and Beaumont back in one riding. That is 10 ridings. <strong>Result: not scored.</strong> My check needs the draft map\'s lines, and no file of them exists. The draft\'s population table matches 9 of the 10 to the person, and the tenth is the Nisku option. That is strong evidence, not proof, that the panel followed it.',
			li6: '<strong>(d) Consider a Clearwater seat.</strong> Consider bringing back a riding made mostly of Clearwater County and western Mountain View County, with s.15(2) status. That is the Act\'s exception that lets up to four remote ridings have as many as 50% fewer people than average. This is the only restored seat the recommendation places. It names no place for the second. <strong>Result: adopted.</strong> Rocky Mountain House-Sundre has 61% of its people in that area.',
			p11: 'On my check, the panel\'s map does not meet Recommendation 5, because it fails condition (a). These results are provisional: the official map files are not public yet, so I rebuilt the panel\'s lines from its report. Airdrie, Calgary, Cochrane and Chestermere all fall under condition (a). That is where the commission\'s minority split Airdrie four ways and drew ridings that join parts of Calgary to the countryside. Red Deer and St. Albert are covered only by the softer clause, "to the extent possible." Together, the conditions cover most of the ground the commission split over. A map that reopens Airdrie or Calgary may still be lawful. But it is not the map Recommendation 5 describes. Motion 37 itself lets the panel apply the recommendation "subject to any modifications the independent advisory panel considers necessary." The <a href="__BASE__/explorer">map explorer</a> outlines the area under each of the four conditions, and each one\'s pin says whether Recommendation 5 changes it or leaves it alone.',
		},
		know: {
			h: 'How I checked',
			h3_1: 'Maps drawn by a computer',
			p1: 'Say a map leans toward a party. Leans compared with what? Compared with 1,010,000 maps of Alberta that a computer drew from the official files, each with 87 ridings, the 2019 number. In every one, each riding is close to the same population and in one piece. The computer never sees a vote, so these maps show what lines drawn with no aim look like. That is all “neutral” means here. Maps drawn with 89 ridings show the same lean; those results are provisional.',
			p2: 'Where is all of this written down? In two places. Most of it is in dated commits in the project\'s public repository. Some is also registered on the Open Science Framework (OSF), a public site that time-stamps research plans. Note the order: the first OSF registration was filed on May 6, 2026, about six hours after the official map files arrived, and the records say which came after.',
			h3_2: 'Why a tie does not mean half the seats',
			p3: 'Rural UCP voters win their ridings by wide margins, about 70-30. Urban NDP voters win by closer ones, about 60-40. So in a 50-50 tie the typical computer-drawn map gives the UCP only 44.8% of seats. That is the starting point.',
			h3_3: 'Four results, side by side',
			table1_h1: 'Measure',
			table1_h2: 'Commission majority map',
			table1_h3: 'Commission minority map',
			table1_r1c1: 'Follows city and town lines (2019 map: 75%)',
			table1_r1c2: "80%",
			table1_r1c3: "72%",
			table1_r2c1: 'Average miss from the ideal riding size, in people (commission\'s tables)',
			table1_r2c2: "3,180",
			table1_r2c3: '4,707: 48% bigger',
			table1_r3c1: 'North-east and central Calgary ridings: people above the provincial average',
			table1_r3c2: "2.8% (1.3% to 1.6% on a literal reading of the zone rule)",
			table1_r3c3: "11.5% (8.5% to 8.9% on a literal reading of the zone rule)",
			table1_r4c1: 'Boundaries the commission\'s majority report flagged as odd',
			table1_r4c2: "0",
			table1_r4c3: '4 (3 confirmed by my check)',
			table1_r5c1: 'Pieces of Airdrie (the law requires at least 2)',
			table1_r5c2: "2 pieces",
			table1_r5c3: '4 by area; 3 counting only pieces with at least 2% of its people',
			table1_r6c1: '<strong>Structural summary</strong> (five dated tests; four of them measure the minority map against the majority map, so the majority cannot fail those)',
			table1_r6c2: "<strong>the yardstick</strong> for four of the five",
			table1_r6c3: '<strong>differs from the majority on 4</strong> (the fifth, city and town lines, separates neither map)',
			table1_r7c1: 'UCP share of seats if the vote splits 50-50 (typical computer-drawn map: 44.8%)',
			table1_r7c2: "46.1% (78th percentile)",
			table1_r7c3: '51.7% (99.99th percentile: only 69 of 1,010,000 give more)',
			table1_r8c1: 'Mean-median gap (election-day ballots)',
			table1_r8c2: '1st percentile: far out, but toward the NDP, the wrong way to help the UCP',
			table1_r8c3: 'further out than 99.97% of computer-drawn maps, toward the UCP',
			table1_r9c1: 'Declination, another measure of one-sided wins (election-day ballots)',
			table1_r9c2: "22nd percentile: inside the normal range",
			table1_r9c3: 'further out than 98.8%, toward the UCP',
			table1_r10c1: 'Efficiency gap, a count of wasted votes (line set in advance: about +4.1%)',
			table1_r10c2: "+0.1% (16.5th percentile)",
			table1_r10c3: '+4.0% (94.5th percentile): just under the line, so a miss',
			table1_r11c1: "UCP seats on 2023 votes (election-day ballots; all ballots)",
			table1_r11c2: "55 of 89; 48 of 89",
			table1_r11c3: '60 of 89; 57 of 89 (the all-ballots count is an estimate: 55 on the older rule, kept as a check)',
			table1_r12c1: 'How rare the map is on all four fairness measures together',
			table1_r12c2: 'Not unusual (about 1 in 10; election-day ballots)',
			table1_r12c3: 'Rarer than 1 in 10,000: a model estimate, not a bound (election-day ballots)',
			p4: 'I wrote four of the five down on April 24, 2026, after I had measured both maps on provisional boundaries. The next day I added the Airdrie split, and the rule that 4 of 5 counts as a match. The record is a dated commit in the project\'s repository. Nothing was registered on the OSF until May 6. Three of the tests can be read straight off the commission\'s report, so treat them as checks of the report, not predictions.',
			fig_caption: 'Left to right: how far each map leans toward the UCP on the efficiency gap. Bottom to top: how many structural tests flag it. The 2019 map and the commission majority\'s map sit in the lower-left corner. The 2019 map is flagged on none of the four tests run on it; the Calgary zone test was never run on it. The minority map sits alone, on the structural line and just short of the efficiency-gap line.',
			h3_4: 'What the odds mean',
			p5: 'Take all four measures together. How often would drawing that never sees votes produce the minority map\'s mix of results? Rarer than 1 in 10,000, whichever way I computed it. On the published measure there is nothing to count: no computer-drawn map is as far out (on a rank-based version, seven are). So the figure comes from a statistical model. It is a model estimate, not a bound. It uses election-day ballots. No all-ballots version exists, because the computer-drawn maps\' all-ballots scores are not in the repository.',
			p6: 'That figure is not the chance the map was drawn in good faith. A map this rare can still come from unusual but honest choices. My claim is narrower: drawing that follows the rules and never sees votes almost never produces it.',
			h3_5: "Checking with a second method",
			p7: 'What the three checks show: I found no sign that the map\'s far-out position comes from my tools, though the engine swap was too small to be conclusive. None of the checks says why the map was drawn as it was.',
			h3_6: 'What the computer-drawn maps leave out',
			p8: 'The computer-drawn maps are a strong outside check, not a list of every map a lawful commission might draw. The computer keeps every riding near the same population and in one piece. It does not follow every rule the commission weighed: the s.15(2) exception, which lets up to four remote ridings be much smaller; community of interest; and following city and town lines. The structural tests say how the two commission maps differ. The computer-drawn maps say how unusual a map is. The 50-50 test has a limit too. It shows what a map adds on its own. In a real election, a big enough swing in votes can outweigh any map\'s lean.',
			h3_7: "What didn't hold up",
			p9: "Some tests came back against my findings. They stay on the page.",
			li1: '<strong>Town and city lines settled nothing.</strong> The minority map follows them 72% of the time and the majority map 80%. The 2019 map, drawn by the last commission, scores 75%. So the test came back neutral: it can\'t tell the two maps apart.',
			li2: '<strong>The efficiency gap fell just short.</strong> I set the line in advance: the 95th percentile, about +4.1%. The minority map came in at +4.0%, the 94.5th percentile. Close doesn\'t count, so I report it as a miss.',
			li3: '<strong>The test of whether the odd shapes cause the seat advantage couldn\'t be run.</strong> No computer-drawn map in its planned run reaches the minority map\'s seats, so there was nothing to compare. The link between the shapes and the seats is untested.',
			h3_8: "Both sides tested",
			p10: "Each side of the commission accused the other in writing. The majority said the minority's changes in five places had “no public support”. The minority said the majority “delete[s] or mangle[s] rural electoral divisions”. I ran the main measurable accusations from each side, plus one hypothesis of my own, through the same tests. None of these checks was set up in advance, so they are exploratory. Every number behind them is public.",
			table2_h1: "The accusation",
			table2_h2: "Who made it",
			table2_h3: "What I found",
			table2_r1c1: "Four of the minority's boundaries are geometrically anomalous",
			table2_r1c2: "The majority (final report, pp. 62–63)",
			table2_r1c3: "Largely confirmed: three of the four geometric flags hold up on the published maps; the fourth's highway-corridor link is defensible",
			table2_r2c1: "The minority's changes in five places had \"no public support\"",
			table2_r2c2: "The majority (final report, pp. 59, 62)",
			table2_r2c3: 'Nearly right. Right at Cochrane and St. Albert, where no record asks for what the minority drew. Wrong by one to three records elsewhere: Airdrie 1 against 10 for the majority’s arrangement, Red Deer 1 against 20, Chestermere 3 against 6. Every posted submission and hearing presentation was read in full; counts are records, not people.',
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
			table2_r6c3: 'Not scored as a whole. The full read counted requests in named places, not testimony about mixed city-and-rural ridings in general. In Lethbridge, 38 records ask for the city to be joined to the country around it, as the minority drew, and 93 for two ridings inside the city, as the majority drew.',
			table2_r7c1: "The majority's rural districts are engineered corridors of isolation",
			table2_r7c2: "My own counter-hypothesis (T3.2)",
			table2_r7c3: "Not supported: the geographic explanation held, and the majority cleared",
			p11: "Checked against public data, the minority's published reasons for its contested lines hold up unevenly. The count depends on the rule. Counting only the reasons the minority actually stated, none of the six is contradicted and four are supported only in part. Counting my own arithmetic on whether population forced each line, four of the lines were not forced; the minority did not claim they were. Usually the general claim is true and the specific line isn't. About 71% of Cochrane's out-commuters work somewhere in Calgary (a third of all its workers). That says nothing about the Nolan Hill neighbourhood the corridor reaches. The majority's report gives checkable reasons for its own contested choices too (final report, PDF pp. 44–60). I tested only the minority's stated reasons and did not test the majority's, so this check runs one way. Taken together, the minority's two rural charges against the majority describe two different approaches. More but fuller rural divisions on the majority map. Fewer but lighter ones on the minority map.",
			h3_9: "Who did this",
			p12: 'I\'m the only author, a self-funded student at Mount Royal University. I\'ve voted for and donated to both conservative and progressive provincial parties. Findings that went against me stay on the record, and every number can be rebuilt from public code, data and recorded random seeds.',
			h3_10: "The full record",
			p13: 'All fifteen findings are in <a href="__BASE__/evidence">the full record</a>, with short <a href="__BASE__/explainers">explainers</a>.',
		},
		test: {
			h: 'The tests on the panel\'s map',
			p1: "The committee had to send the panel's 91-seat map to the Assembly by November 2, 2026. The rules that decide the verdict were written down in June 2026; the <a href=\"https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/preregistration/november_2026_scoring_spec.md\" rel=\"noopener\">scoring rules</a> are dated in the project's repository. Three extra tests reported beside them, and the choice of comparison set, were added October 29–31, after opposition MLAs had described parts of the panel's map at the committee's October 28 meeting. Seven amendments followed on November 2–7, after the panel's report was tabled (see the November section below). I'll publish the scores on the official map files within 72 hours of their release, whichever way they point.",
			p2: "<strong>The process.</strong> Were public hearings held? Was a draft released? Are the advisory panel's members and terms of reference published? Is the record behind the map public? NDP members said the panel took no public submissions, and the committee defeated a motion to publish whom the panel consulted, so I can only score the reasons for the map's lines from what the panel's report publishes. The process also gets its own nine-feature scorecard, registered on the OSF (u47bq) and shown on <a href=\"__BASE__/norms#measurable\">the norms page</a>.",
			p3: '<strong>The one recommendation the government cited.</strong> That is Recommendation 5, from the commission\'s chair. It sets four conditions, and a second test, X1, checked the panel\'s map against them. Each condition was scored on its own:',
			li1: '(a) failed. Of the 41 ridings from Airdrie south, the panel\'s map changes 10. (b) passed, 11 of 11. (c) was not scored, because the commission\'s October 2025 interim map is not in the project\'s files. All three work the same way: a condition passes if the map leaves its ridings as the recommendation describes.',
			li2: '(d) passed: the map has a Clearwater seat. Rocky Mountain House-Sundre has 61% of its people in the Clearwater County and western Mountain View County area. The condition asks only that such a seat be considered. It passes if the map has that riding, or if the committee\'s or the panel\'s published report names the option and gives a reason, tied to the Act\'s factors, for taking it or not. With no other public record of how the map was made, those reports are the only record that counts. Silence or boilerplate fails.',
			p4: 'X1 passes only if all four conditions pass. (a) failed, so X1 was not met, whatever (c) would have shown. Recommendation 5 binds no one in law. What X1 tests is whether the map delivers what the government cited. By that test, it does not.',
			p5: "<strong>The map.</strong> Where does it land on every measure on this page, against the same million-map distribution and under the pre-registered thresholds (on all ballots, two of those lines were set afresh: Amendments 12 and 14)?",
			p6: '<strong>The main test.</strong> In June 2026, before the panel\'s map was public, I wrote down how I would check it (<a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/preregistration/november_2026_scoring_spec.md" rel="noopener">the scoring rules</a>). The test asked one thing, in two halves: does the panel\'s map repeat the pattern in the commission minority\'s map? On the lines, 3 or more of 5 structural flags would count as a match. On the votes, 2 or more of 4 fairness flags in the UCP\'s direction would count. The result, on 2023 election-day ballots: 2 of 5 and 1 of 4. Neither half matches. The votes half carries the weight, because a later check, not set in advance, found that the structural half adds little on its own. Of computer-drawn 91-riding maps balanced only to the Act\'s ±25% band, 93.5% match the minority\'s structural pattern. That rate was not measured on maps balanced more tightly; on the main set, balanced to ±12.5%, the first of those tests alone flags 25.3%. The result is provisional, because it uses my reconstruction of the map. I will rerun every test on the official map files within 72 hours of their release, and post the result whichever way it points.',
		},
		november: {
			h: "November: the panel's map, checked",
			note: 'These results are provisional, and here is why. The official map files are not public, so I rebuilt the panel\'s lines from its report. I call that my reconstruction. It failed its first two accuracy checks: 49.0% of voting areas landed in the wrong riding, then 13.8%, against a 10% limit. A rule change (Amendment 10) allowed a third try. That one passed, but only as a repeat run on pages already seen, not as a fresh test. I will rerun everything on the official files.',
			p1: '<strong>The tests set in advance.</strong> I ran them on November 4. Their rules were amended eight times from November 2 to 10. Four amendments came before I scored the panel\'s map. Four came after I had seen results (<code>findings/pre_registration_amendment_log.md</code>).',
			li1: '<strong>How the lines are drawn:</strong> 2 of 5 flags. A match with the commission minority\'s map needed 3. Not repeated.',
			li2: '<strong>How votes turn into seats:</strong> 1 of 4 flags. A match needed 2. Not present. The one flag is the 50-50 test, which counts seats when the vote splits evenly. On that test the panel\'s map sits at the 98.8th percentile: higher than 98.8 in every 100 computer-drawn maps, on election-day ballots. The other three measures sit in the normal range.',
			li3: '<strong>Recommendation 5,</strong> the one the government cited, asked that 41 ridings be left alone. The panel changed 10 of them, so the map does not follow it on my registered test.',
			p2: 'So on this provisional reading, the panel\'s map does not carry the commission minority map\'s pattern. Not in how its lines are drawn, and not in how it turns votes into seats.',
			p3: '<strong>Which ballots count (November 7 and 10).</strong> On the 2019 map, election-day ballots alone elect 57 UCP members. The real 2023 result was 49. What election-day ballots leave out is about half of 2023\'s ballots: the early ones, cast in advance, by mobile poll, by special ballot or anywhere. Elections Alberta reports those only for each old riding. Early ballots leaned 6.2 points more NDP than election-day ballots, and more NDP in 83 of 87 ridings. So I changed the rule after seeing some results (Amendment 12): every vote-based test uses all ballots, with election-day results kept beside them. That change was not blind. Where early ballots fall inside a new riding is an estimate. The registered rule, rule P, places them only among people who did not vote on election day, using Alberta data only. It is Amendment 14, signed on November 10 and filed on the OSF. I chose it after I had seen its effect on the maps, so it is not blind either. The older rule from Amendment 12 is kept as a check.',
			li4: "<strong>The panel's map</strong> gets the same counts on both kinds of ballots and under both rules: 2 of 5 and 1 of 4.",
			li5: '<strong>The commission minority\'s map,</strong> on all ballots under rule P, comes out at 57 seats to 32. Two Calgary seats are narrow, won by 401 and 68 modelled votes. On the same ballots and rule, its efficiency gap is +5.64%, above the line of +2.15%. Only 192 of 1,010,000 computer-drawn maps reach that gap, the 99.98th percentile. It has 4 of 5 flags on how the lines are drawn and 4 of 4 on how votes turn into seats. One of the five line tests is not counted under rule P, because its score proved unreliable; the academic report has the detail. The commission majority\'s map has 0 of 5 and 0 of 4. On the older rule, kept as a check, the minority\'s gap is +2.55% against a line of +1.39%, its seats 55 to 34, and its flags 5 of 5 and 4 of 4. The check for too few close seats has not been run under rule P. This does not reopen <a href="__BASE__/evidence#casing-7">finding 7</a>.',
			li6: '<strong>Comparison sets rerun (November 8 and 10).</strong> I reran every set of computer-drawn maps under rule P, the main 1,010,000 included. 32 of 36 runs drew the same maps as before. The four from a second sampler did not, and I left them out, as Amendment 13 requires. That amendment too was written after results were seen. On the older rule, the smaller sets were rerun on November 8. Two runs that did not repeat exactly were left out, and the only flag in those sets is the city-versus-rest test in the narrowest set.',
			p4: '<strong>What the newer checks found.</strong> These checks look at what the panel’s changes do. All of them use my reconstruction of the panel’s map. I rebuilt it from the panel’s report because the official map files are not public yet, so every result here is provisional. The reconstruction failed its first two accuracy checks (49.0%, then 13.8% of voting areas placed wrong, against a 10% limit). The third passed only as a repeat run on pages already seen. None of these checks was registered, and most were planned after related results were known. For each one except the count of city-limit crossings, a plan was committed to the repository together with the results. That the plan was written first rests on my word. The test ledger records all of this (<code>findings/test_ledger/README.md</code>).',
			li7: '<strong>What the panel’s changes do to seats.</strong> The panel minority’s alternative map (paragraph 167 of the panel’s report) undoes the changes south of Airdrie. Against it, the panel’s map gives the NDP 2 fewer seats on election-day ballots. On all ballots the answer depends on how early ballots, those not cast on election day, are placed inside each riding. On the registered rule P, both maps give the UCP 50, so there is no difference: the panel’s Banff-Canmore-Diamond Valley goes to the NDP, by 1,276 modelled votes. On the older rule, kept as a check, the panel’s map gives the UCP 51 seats and the alternative map 50, so the NDP has 1 fewer. Every seat that differs is too close to call on the reconstruction: its winning margin is smaller than the votes in the voting areas that a differing line cuts through. The direction is the same in the 2015, 2019 and 2023 elections, and over most of a 10-point swing either way (<code>findings/iap_para167/</code>, <code>findings/six_signals/</code>).',
			li8: '<strong>Against computer-drawn maps,</strong> the panel’s map sits near the middle on election-day ballots: UCP seats at the 43rd percentile, and the efficiency gap at the 48th. On those measures the alternative map sits nearer the edge. On the 50-50 test, which counts seats when the vote splits evenly, the panel’s map sits higher: at the 90th to 97th percentile against computer-drawn maps that also have 91 ridings. On that test it is the panel’s map, not the alternative, that is nearer the edge.',
			li9: '<strong>Lethbridge.</strong> The panel’s map splits the city four ways. I had the computer redraw the region many times, without votes and respecting city limits. Those redraws split Lethbridge two ways in 51% of cases, three ways in 48%, and four ways in 0.9%. The panel’s map puts 45% of the city’s NDP voters in seats the NDP loses by 10 points or more, and the competitive second city seat is gone. Against the redraws, that sits at the 93rd percentile, just inside the line set in advance (<code>findings/hybrid_regions/</code>). How strongly the redraws keep cities whole matters. Past commission maps imply a city-limit weight between 0.52 and 0.66; the redraws above use 0.5. At 0.52 the panel’s map is at the 93rd percentile. At 0.66, the weight that matches the 2026 commission majority’s own map, it is at the 97th, beyond the line (<code>findings/city_weight/</code>). Those weights were measured on redraws of the whole province. They are assumed to mean the same in a redraw of one region, and that has not been checked.',
			li10: '<strong>Where moved voters went.</strong> The panel’s changes move some NDP votes between ridings. Of those, 14,199 go from a seat the NDP wins or nearly wins into one it loses by 10 points or more. Another 3,152 go the other way. Most of it, about 10,000, comes from Lethbridge, and about 3,700 from Edmonton-Beaumont into Leduc-Beaumont. The Banff change adds little. The panel did not change NDP-held or competitive seats more often than others. It changed them less often (<code>findings/local_targeting/</code>). Computer redraws of the south and central region find the panel’s layout there ordinary and the commission majority’s the unusual one, partly because of how the redraws are built. So much of this flow is a move away from an unusual starting point.',
			li11: '<strong>City limits in past maps.</strong> Here a riding counts as crossing a city limit when 5% to 95% of its people live in the city. A riding that reaches past the limit but holds almost only city residents is not counted. At Calgary’s limit, the 2010 and 2017 maps and the commission majority’s map have none, and the 2003 map had three. The panel’s map has two (the Springbank ridings). The commission minority’s had six. At Edmonton’s limit, the 2003, 2010 and 2017 maps had none. The commission majority’s map and the panel’s each have two, and the minority’s three (<code>findings/city_weight/big_city_lines.json</code>).',
			li12: '<strong>Rural voters.</strong> In Lethbridge County, the number of rural residents placed in mostly-city ridings goes from 0 on the commission majority’s map to 8,138 on the panel’s. Rocky View County goes from 4 pieces to 6. On the check’s own measure, one of the panel’s changes overrides a rural preference on 2023 votes: Edmonton-Nisku, which holds about 7,000 rural residents (<code>findings/rural_voice/</code>).',
			li13: '<strong>Which population the comparisons use.</strong> The computer-drawn maps balance 2021 census population. The real maps were drawn on 2024 estimates. Calgary and Edmonton grew faster, so on 2024 figures they hold about two seats’ worth more people (51.4 seats’ worth, against 49.5). On each map’s own published figures, city ridings hold 9 to 10 points more people than the rest, beyond what the 2021 figures show. For the panel’s map, the gap is +13.4% on its own figures, against +4.3% on 2021 figures. That limits every city comparison in this record. A rerun of the computer-drawn maps on 2024 figures is proposed (<code>findings/population_basis/</code>).',
			li13b: '<strong>Every changed region.</strong> Each group of ridings the panel changed was redrawn many times without reference to party, at each map’s own number of seats. The panel’s layouts sit inside the normal range in every region, on every measure. The commission majority’s layout of the south and central region is the unusual one. It packs more NDP votes into wide wins (Lethbridge-West and Canmore-Banff) than any of the redraws (50,000, drawn each of two ways), and puts fewer in lopsided losses. Part of that is built in. The redraws keep every riding within 25% of the region’s average and have no remote-riding exception, so none can hold a riding as small as the majority’s Canmore-Banff or the panel’s Rocky Mountain House-Sundre. Even Lethbridge-West on its own packs more NDP votes than 95% of the redraws do across the whole region, both ways. The panel’s changes lower that packing (<code>findings/changed_districts/</code>).',
			li14: '<strong>All of it together.</strong> The newer checks made 132 percentile comparisons, plus 11 other tests. Of the comparisons, 12 fall beyond the 5th or 95th percentile: 8 for the panel’s map and the alternative map, and 4 for the commission majority’s layout of the south. Run enough tests and some will land at the edge by chance. After correcting for the number of tests, none of the 12 holds up.',
			reasons: '<strong>The panel\'s own reasons</strong> (<a href="__BASE__/evidence#casing-15">finding 15</a>). The panel said Lethbridge “already has population to spare”, yet it split the city four ways. Red Deer, about the same size, kept two city ridings. Banff\'s riding was at most about 1,300 people short. The panel added 8,901. In Lethbridge and Banff, the reasons I could check do not hold. Where a change moves no seat, they mostly hold. Against its own minority\'s alternative map, the panel\'s map gives the NDP 2 fewer seats on election-day ballots. On all ballots, under the registered rule P, there is no difference. On the older rule for early ballots, kept as a check, it gives 1 fewer. Each seat that differs is too close to call: its margin is smaller than the votes in the areas where the two lines differ.',
			more: '<strong>The newer checks</strong> came after November 4 and were not set in advance. They look at seats, Lethbridge, city limits and rural voters. Of 132 comparisons, 12 fall outside the usual range. None holds up once the number of tests is counted. The checks are in <a href="__BASE__/evidence#newer-checks">the full record</a>, after finding 15.'
		},
		mind: {
			h: "What would change my mind",
			p1: 'Each main finding has a written condition that would withdraw it, most set on April 24, 2026. If one is met, I will publish the retraction within 30 days of learning of it, as the project\'s rule says.',
			li1: '<strong>Someone shows the trade-off was forced.</strong> If no legal map can meet the minority\'s stated reasons at Airdrie, Cochrane, Nolan Hill and Rocky Mountain House–Banff Park while following town and city lines as often as the majority map, I\'ll retract the finding that those reasons don\'t explain those lines. The challenge is open at <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/issues/14" rel="noopener">Issue #14</a>.',
			li2: "<strong>A document shows the reasons came first.</strong> If an internal commission document, dated before the minority's final choices, shows those choices were driven by community submissions I haven't seen, I'll retract the inference that they were drafting decisions.",
			li3: '<strong>The neighbour-drain test.</strong> I have retired this test as unreliable, so I no longer claim the minority map passed it. This condition no longer applies.',
			li4: '<strong>An election contradicts the computer-drawn maps.</strong> If the 2027 election, on whatever map becomes law, gives a seat split that contradicts what 2023 votes predict on that map, I\'ll revisit the percentile findings.',
			li5: '<strong>A court sets <em>Lalande</em> apart.</strong> The Supreme Court struck down Quebec\'s law pausing its commission (<em>Quebec (AG) v. Lalande</em>, 2026 SCC 13). If a court finds Alberta\'s route different in law, I\'ll retract the argument on <a href="__BASE__/norms">the norms page</a> that the two belong together.',
			p2: 'The panel\'s map could have weakened my conclusion. On provisional results it does not repeat the pattern, so the pattern stays a finding about one map, never enacted. I correct mistakes in public and don\'t delete them (<a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">technical report, Documented Corrections</a>).',
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
			p8: "I could be wrong, and I've set out how you'd know. The panel's map went to the Assembly on November 2, and the rules that decide its verdict were fixed in June, before it was made public. If it lands inside the neutral range, my suspicion has taken real damage, and this site will say so within 72 hours of its release. I committed to that before I knew the answer.",
			signed: "— Will Conner",
		},
		fixes: {
			h: 'Two fixes for next time',
			p1: 'Two problems make Alberta\'s maps harder to check. About half of all votes are cast before election day, and Elections Alberta reports them only by riding, so about 810,000 UCP and NDP votes from 2023 can\'t be traced to a voting area. And maps are drawn from census counts that are years old by the time they take effect. <a href="__BASE__/fixes">The fixes page</a> shows how to fix both.',
		},
		answer: {
			h: 'The short answer',
			p1: '<strong>On my fairness tests, the new map mostly passes.</strong> I fixed the tests in advance. On them, the panel\'s 91-seat map does not repeat the lean toward the UCP that I found in one of the commission\'s maps. It sets off 2 of 5 flags on how its lines are drawn, where a match needed 3 of 5. It sets off 1 of 4 on how it turns votes into seats, where a match needed 2 of 4. One caution: the official map files aren\'t public yet, so I rebuilt the lines from the panel\'s report, and these results are provisional.',
			p2: '<strong>But there are issues. Three of them.</strong> <em>The 50-50 test.</em> Picture the province splitting its vote exactly in half. (I get there by shifting every riding\'s vote by the same amount.) Then count seats. On the panel\'s map the UCP wins 44 of 91, or 48.35%. That is under half. But maps a computer draws without seeing a vote usually give the UCP fewer still in a tie, 44.8% for the typical one, because rural UCP wins are wider than urban NDP wins. 48.35% is more than 98.8 in every 100 of those maps give, on 2023 election-day ballots. Against maps with the same 91 ridings, it is more than 90 to 97 in 100. <em>Lethbridge and Banff.</em> The panel gave population reasons for its lines there, and the reasons don\'t match the panel\'s own numbers. Set those changes beside the alternative map the panel\'s own minority drew, and on 2023 election-day ballots they cost the NDP two seats. Count all ballots and the registered rule P gives none; the older rule for placing early ballots, kept as a check, gives one. Each seat that differs is too close to call: the winning margin is smaller than the votes along the lines in question. <em>Recommendation 5.</em> It is the one recommendation the government cited. On the floor, the government presented its route as following the commission: "We are adopting the recommendations from the report" (Government House Leader, Hansard, April 16, 2026). Recommendation 5 asked that the 41 ridings in Airdrie and south of it stay as the commission\'s majority drew them. The panel\'s map changes 10 of them. Motion 37 let the panel modify the recommendation, and the recommendation binds no one in law. But this is not the map it describes.',
			p3: '<strong>The map that started it.</strong> In March 2026 the independent commission split 3 to 2 and filed two maps. I had a computer draw 1,010,000 maps without seeing a vote, and held both commission maps up against them. The majority\'s map looks like the million. The minority\'s map leans toward the UCP further than almost any of them. Split the vote 50-50 and only 69 of them give the UCP a larger share of seats, and only by a hair.',
			p4: '<strong>How the new map was made.</strong> The commission held public hearings and published a draft. The committee and its panel did neither: no public hearings on the new map, and no draft. As I read the law, nothing forbids that. It does depart from a practice Canada spent about sixty years building: an independent body draws the map, at arm\'s length from the MLAs who will run in it. That practice provided nine safeguards. On <a href="__BASE__/norms#measurable">my scorecard</a>, the committee\'s process has 2 of them, has 1 in part, and lacks 6.',
			next: '<strong>What happens now.</strong> On November 4, 2026 the Assembly voted 45 to 36 to concur in the panel\'s map and to urge the government to introduce a bill (<a href="https://docs.assembly.ab.ca/LADDAR_files/docs/hansards/han/legislature_31/session_2/20261104_1330_01_han.pdf" rel="noopener">Hansard</a>, p. 2116). The map becomes law only if a bill passes, and a court challenge can come only after that. In the same debate the Leader of the Opposition called it "a map that is clearly gerrymandered, that is clearly illegal, that is clearly unconstitutional" (p. 2101). No court has ruled on any of it. When the official files are out, I\'ll rerun every test within 72 hours and post the result here, whichever way it points.'
		},
		bodies: {
			t1: '<strong>March 23, 2026.</strong> The commission splits 3 to 2 and files two maps.',
			t2: '<strong>April 21.</strong> Government Motion 37 sets both maps aside and creates the committee of six MLAs.',
			t3: '<strong>June 2 and 9.</strong> The committee appoints the panel: first its chair, then four members.',
			t4: '<strong>October 22.</strong> The panel reports its 91-seat map. On October 28 the committee votes 3 to 2 to end its review without adding any observations of its own.',
			t5: '<strong>November 2.</strong> The committee sends the panel\'s report to the Legislature. Next, MLAs decide whether to pass a bill.'
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
		meta: 'The fifteen findings in full, in plain language',
		intro: 'In March 2026 the commission split 3 to 2, so its majority and its minority each filed a map. Most of the findings below compare those two maps. Finding 15 checks the panel that drew the new 91-riding map. (A riding is the area that elects one MLA.) Every finding behind the main page is here in full. Each says what I found. Nearly all then say what it might suggest and what’s normal in Canada, and close on why it isn’t proof, including what the law does with it. Read the page as a log. The findings that cut against the audit sit right beside the ones that support it.',
		back: "← Back to the audit",
		group_map: 'The lines: what each map does on the ground',
		group_sim: 'Against computer-drawn maps: how unusual each map is',
		group_conduct: 'The people: what each body did and said',
		beat_found: 'What I found',
		beat_show: 'What it might suggest',
		beat_context: 'What experts say',
		beat_canada: 'What’s normal in Canada',
		beat_law: 'Why it isn’t proof',
		explainer: "Explainer",
		e1: 'The minority map splits Airdrie, a city of 85,805, into four ridings',
		e2: 'The majority flagged four of the minority’s boundaries as odd, and my tests confirm three',
		e3: 'In north-east and central Calgary, the minority map’s ridings hold more people',
		e4: 'The minority map is less equal in population, the one thing the law measures',
		e5: 'Both maps follow city and town lines about as often as the 2019 map does',
		e6: 'With the vote split 50-50, the minority map gives the UCP a larger share of seats than all but 69 of 1,010,000 computer-drawn maps',
		e7: 'The efficiency gap: past its line on all ballots, just short on election-day ballots',
		e8: 'Between 1 in 20,000 and 1 in 570,000: the odds of a map like the minority’s, and the misreading they invite',
		e9: 'I tried to knock down my own result: one check held, one was too small to settle it, and one could not be run',
		e10: 'Three tests retired',
		e11: 'Six of the minority’s stated reasons, checked against public data',
		e12: 'The commission split 3 to 2, and I tested each side’s charges against the other',
		e13: 'The commission kept the Lesser Slave Lake riding after the public weighed in; the process that replaced it held no hearings',
		e14: 'One motion set aside the norm that an independent body draws the map',
		e15: 'In Lethbridge and Banff, the panel’s reasons I could check do not hold up against its own numbers',
		sides_h: 'The commission’s majority and minority: their charges, put to the same tests',
		newer_h: 'The newer checks on the panel’s map, provisional and not set in advance',
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
			sub2_close: "Fewer than 100 of 1,010,000 computer-drawn neutral Alberta maps produced a <code>seats@50/50</code> value as high as the minority proposal's. On 2023 election-day ballots it would award the UCP 60 seats (55 on the majority proposal); on all ballots, 57 and 48 (55 and 48 on the older way of placing early ballots, kept as a check). The majority proposal is the kind of map a neutral procedure routinely generates. The minority proposal is the kind of map you have to specifically aim to draw.",
			sub3_h: 'What this means in plain language',
			sub3_p: 'The minority proposal sits in the extreme tail of the 1,010,000-plan ensemble on three of four partisan-fairness metrics, with the fourth (efficiency gap, +4.0%) at the 94.5th percentile — <em>near, but below</em>, the audit\'s pre-registered Alberta-calibrated threshold of the 95th. A statistical model gives an estimate <strong>between about 1 in 20,000 and 1 in 570,000, depending on the model</strong>. That remains an extreme result, well beyond conventional significance thresholds — but it is a model estimate, not four independent instruments reading in agreement.',
			details_summary: "What this p-value means — and what it doesn't",
			details_p1: 'A p-value answers one question: if the map were drawn by a neutral process, how often would we see a result this extreme or more extreme? On the audit\'s model estimates, the answer is between about once in 20,000 and once in 570,000 trials, depending on the model.',
			details_p2: 'This is a frequentist hypothesis test, not a measurement of intent. It does not say the commission intended to gerrymander, and it does not quantify how unfair the map is in practical terms. It says the boundary pattern is statistically inconsistent with the ReCom neutral-drawing reference distribution — a strong external check, but not a perfect one (it does not enforce every statutory criterion the commission worked under, e.g., s.15(2) tiers and community-of-interest constraints).',
			details_p3: 'The structural test battery (population, splits, anchoring, compactness, signatures) was registered with timestamps before canonical recomputation (<a href="https://osf.io/w2s8k" rel="noopener">OSF registration w2s8k</a>). The partisan-bias channel (the joint Mahalanobis score) is labelled "exploratory" in the audit\'s own §4.3.1 sense: documented in the repository, but not pre-data.',
			super_lead: 'In an 89-seat legislature, a two-thirds supermajority requires exactly 60 seats. The minority proposal’s tied-vote seat share of 51.7% — a level only 69 of the 1,010,000 neutral maps reach — sits in the regime where a UCP supermajority becomes statistically reachable on Alberta’s 2023 geography. But the simulation does not enforce every statutory criterion the commission worked under, so this is a strong external check, not proof that no legally compliant Alberta map could reach this seat count. Act I’s structural evidence, which does not depend on the simulation at all, carries most of the weight; the tied-vote tail position is the supporting context.',
			super_label: 'WHY A LARGE MAJORITY MATTERS',
			super_body: 'Under Canada\'s Westminster system, Alberta\'s Assembly has no two-thirds threshold that unlocks special powers: a governing majority — even a bare one — can already pass laws and budgets, invoke "closure" to end debate, change the rules of the House, and set the membership of every committee. What a very large majority changes is margin and durability, not the menu of powers. A government holding 60 of 89 seats is effectively immune to internal dissent — a handful of floor-crossings cannot threaten it — and faces an opposition too small to force recorded divisions or sustain committee scrutiny. The concern here is the concentration of seats and the thinning of effective opposition, not a procedural threshold being crossed.',
			super_close: 'The urban-hybridization pattern identified in Act I — urban voters distributed into surrounding rural-edge districts — is consistent with the 60-seat outcome, though the audit’s direct test of whether that geometry is the specific mechanism could not be run on its final data (Finding 9). The structural and statistical findings converge on the same proposal and the same communities — and they agree on who benefits.',
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
			defense1: '<strong>The "Natural Political Geography" Defence:</strong> <em>("Urban voters are naturally packed; the map just reflects Alberta\'s geography.")</em> The 1,010,000 simulations already account for Alberta\'s natural geography. Geography does give the UCP a baseline efficiency advantage — but the two real comparison maps show where that advantage naturally tops out: both the 2019 enacted map and the 2026 majority sit at the 78th percentile on the tipping-point metric, and the 2019 map\'s highest placement on any partisan measure is the low 90s (declination, 91st percentile). The minority map sits at the 99.99th percentile — an extreme outlier <em>even when compared to Alberta\'s naturally skewed baseline</em>.',
			defense2: '<strong>The "Communities of Interest" Defence:</strong> <em>("The odd shapes were drawn to keep specific communities together.")</em> If you are trying to keep communities together, you follow municipal borders. The majority map followed existing city limits 80% of the time. The minority map followed them 72% of the time — both within the 70–85% Canadian norm. What the minority map does do is actively split the unified city of Airdrie into four separate pieces, and place three of its boundary decisions precisely in the urban-edge zones the commission chair flagged as geometrically anomalous — choices not explainable by community-of-interest logic.',
			defense3: '<strong>The "Population Equality" Defence:</strong> <em>("They had to draw weird boundaries to make sure every district had the exact same population.")</em> On the commission\'s own population tables the minority map is <em>worse</em> at population equality: its Population Mean Absolute Deviation (MAD) was 4,707, 48% wider than the majority map\'s 3,180. On 2021 census numbers the two maps\' mean deviations are almost the same, and the minority\'s median deviation is wider (3,938 against 2,827). That median spread sits at the 99th percentile of neutral maps balanced to within ±12.5%, but at the bottom of the range when neutral maps may use the statute\'s full ±25%.',
			defense4: '<strong>The "Incompetence or Bad Luck" Defence:</strong> <em>("They just drew a sloppy map and got unlucky with the numbers.")</em> Hitting a 60-seat supermajority configuration while also splitting Airdrie into four pieces and placing three boundaries in the exact zones the commission\'s own majority flagged as anomalous requires precision. A statistical model puts the probability of accidentally drawing a map this extreme under the ReCom neutral reference distribution <strong>between about 1 in 20,000 and 1 in 570,000, depending on the model</strong>. That is still extreme — well beyond conventional significance — but it is a model estimate, not a precise single probability.',
			sub5_close: 'What the data shows is that the minority proposal worsened both population parity and community coherence relative to what the same five commissioners produced simultaneously under identical statutory rules. The audit does not determine what the minority commissioners intended — boundary geometry cannot reveal intent — but the structural departure from both the neutral ensemble and the majority proposal\'s output stands regardless of intention.',
			sub6_h: 'A note on the R cross-validation',
			sub6_p1: 'An earlier version of this audit (using approximated rather than official shapefiles) cross-validated the Python ReCom ensemble against the R <code>redist</code> package\'s Sequential Monte Carlo sampler. The cross-check produced unstable results: across three runs with the same nominal seed, the fraction of plans reaching the old minority value (48.3% on the approximated geometry) was 5.6%, then 28%, then 58% — a sampler-convergence failure, not a discovery. The full write-up is at <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/redist_python_comparison.md" rel="noopener">findings/redist_python_comparison.md</a>.',
			sub6_p2: 'With official Elections Alberta shapefiles, the minority map\'s <code>seats@50/50</code> rises to 51.7% — a value fewer than 100 of 1,010,000 neutral plans reach. The R cross-validation question becomes moot: zero plans from either sampler reach the canonical value at comparable sample sizes.',
			sub6_asymm: '<strong>The asymmetry around 50/50 is starker than the number alone.</strong> A precision sweep of the seat-vote curve at 0.01-percentage-point resolution finds the minority map keeps the UCP at or above the 45-seat legislative-majority threshold down to about <strong>49.2%</strong> of the two-party vote: the UCP could lose it by about 1.6 points and still form government. On the <strong>majority</strong> map, the UCP would need to <em>win</em> it by about 9 points to reach the same threshold. Both maps face the same Alberta geography and the same statutory rules; the gap between them is structural, not noise.',
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
			t5_r2_c: 'extreme tail on three of four fairness measures — tied-vote seat share 51.7% (only 69 of 1,010,000 neutral maps reach it); two further measures past the 98.8th and 99.9th percentiles; efficiency gap +4.0% (<em>near but below</em> the pre-set line — a reported miss); combined odds under neutral drawing between about 1 in 20,000 and 1 in 570,000',
			details2_summary: 'Why the structural act carries the case — technical detail',
			details2_p: "The audit wrote down five structural-irregularity tests on April 24, 2026, before the final simulation results were compiled. Anchoring is neutral for both maps; of the remaining four, the minority crosses every one and the majority crosses none. Those measurements are geometric — no statistical sampler, no vote data. <strong>This is the central finding.</strong> The simulation corroborates it: the minority sits in the extreme tail on three of four fairness measures, with the fourth (the efficiency gap) just under the pre-set line at the 94.5th percentile, and combined odds between about 1 in 20,000 and 1 in 570,000 under neutral drawing — a model estimate, explained in Finding 8. One honesty note lives in the findings: whether the flagged boundary shapes themselves are the direct mechanism of the seat swing is untested — the planned test could not be run on the final data (Finding 9; full write-up at <a href='https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/redist_python_comparison.md' rel='noopener'>findings/redist_python_comparison.md</a>). The structural act carries the case; the numbers corroborate without carrying."
		},
		impact: {
			heading: '5: Effects on Representation',
			lanes_label: 'LANE 1 AND LANE 2',
			lanes_body: '<strong>Lane 1 (numbers)</strong> uses election results to test whether the map turns votes into seats fairly: it asks how the map performs across different vote splits. <strong>Lane 2 (structure)</strong> looks only at the drawn lines — city splits, population spread, boundary shapes — and uses no election data at all. Each lane is independent: a map can fail one and pass the other. The minority proposal fails both. The majority passes both.',
			intro: "Lane 1 depends on which election results you score the maps against. Lane 2 does not. Its structural evidence lives in the maps themselves: the drawn lines, the split cities, the places where boundaries follow, or don't follow, administrative lines that exist for other reasons. On these tests the two maps are not close.",
			fig_alt: 'Bar chart with five panels: four tests of how the lines are drawn, plus a summary score. Teal bars are the majority map and purple bars the minority map. Three panels have a dashed red failing line: north-east and central Calgary crowding, the boundaries the majority flagged that my tests confirmed, and the summary score. On all three, the purple bar crosses the line and the teal bar stays inside it.',
			fig_caption: 'The minority map’s purple bar crosses every dashed failing line on this chart. The majority map’s teal bar never does. The chart sets four tests of how the lines are drawn side by side, plus a summary score. A dashed line marks a failing level where a test has one: north-east and central Calgary crowding, the boundaries the commission’s majority flagged that my tests confirmed (three of its four), and the summary score. The population-spread and Airdrie panels have no failing line. Population spread puts the majority at 3,180 people from the ideal riding size and the minority at 4,707. A fifth test, how often lines follow city and town limits, is not plotted. Both maps sit close to the 2019 map’s 75%, so that test counts as neutral, and the summary scores the minority 4 of 5.',
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
			chair_appendix_p: 'The audit also tested a separate, blanket assertion in the majority report, which the chair signed: that the minority\'s changes in five places (Airdrie, Cochrane, Chestermere, Red Deer and St. Albert) had <strong>no public support</strong> in the 1,345 public submissions (final report, pp. 59 and 62). A keyword search across the full submission archive (1,252 of the 1,345 submissions had text a machine could read; methodology and per-configuration evidence at <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/submission_search_findings.md" rel="noopener">findings/submission_search_findings.md</a>) turned up a more nuanced picture than either the majority\'s blanket claim or a blanket dismissal of it. The majority was right on four of the five: the Airdrie 4-way split, the Calgary–Nolan-Hill–Cochrane hybrid, the Red Deer hybrids and the St. Albert minority alternative each lack any documented support. It was partly wrong on Chestermere, where three submissions support the minority\'s arrangement and three oppose it. Two configurations the majority attacked on other grounds also drew support: Rocky Mountain House–Banff Park drew an explicit, detailed proposal from at least one Clearwater-area submission, plus several aligned ones, and Beiseker residents supported Olds–Three-Hills–Didsbury in writing. So the majority\'s "no public support" sweep is demonstrably overbroad, but it is not invented out of whole cloth, since four of the five do hold up. <strong>This finding cuts against the majority, not against the minority.</strong>',
			summary_p: '<strong>On Lane 2, the majority crosses zero structural thresholds. The minority crosses four of the five, by a wide margin.</strong> The count is a raw tally. It is not a calibrated family-wise probability. Its weight comes from directional unanimity — every test that fires points the same way — not from a joint null-distribution calculation. The statistical lane (§3) supplies the joint probability, through a different instrument.'
		},
		cpd: {
			heading: '4: Cracking and Packing',
			vocab_label: 'Two moves, one playbook',
			vocab_packing: "<strong>Packing</strong> means cramming one party's voters into districts the party wins by landslides. Each packed ballot still counts, but once the seat is won it adds nothing more. Large, lopsided wins. Wasted votes.",
			vocab_cracking: "<strong>Cracking</strong> means splitting a community across several districts so it wins none of them outright. A city strong enough to carry two seats gets carved into four, and in three of them its people are outnumbered. Diluted votes. One seat where there could be two.",
			vocab_disclaimer: 'Both can happen without any explicit partisan intent. What the audit measures is whether the pattern, and its statistical size, is consistent with what a neutral map-drawing process produces. <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md#5-results" rel="noopener">Full methodology at §5 of the technical report.</a>',
			fig_alt: 'Two bars, drawn to scale, showing how each map divides Airdrie’s people. Majority: Airdrie-West holds 50.6% of the city and Airdrie-East 49.4%, and both ridings are mostly Airdrie. Minority: Airdrie East holds 54.7% of the city and is 89.6% Airdrie; Calgary-Airdrie holds 24.0% and Calgary-Foothills-Airdrie West 20.9%, and both are mostly Calgary; Olds-Three Hills-Didsbury takes about 350 people.',
			fig_caption: 'How each map divides Airdrie’s people. The majority map gives the city two ridings, both mostly Airdrie. The minority map gives it one, Airdrie East, with 54.7% of the city. It puts most of the rest in two ridings that are mostly Calgary.',
			intro: 'The five commissioners worked from the same statutory rules, the same provincial geography, the same archive of 1,345 public submissions, the same demographic data. Their two competing drafts agree on most of Alberta. Where the drafts part, they part on choices someone in the room had to make. Three of those choices are worth seeing as choices. Not numbers.',
			airdrie_p: "<strong>It splits the City of Airdrie into four pieces.</strong> The law caps each electoral division at one-and-a-quarter times the provincial average, so Airdrie needs at least two divisions. The majority map gives it two. The minority gives it four: north to Olds-Three Hills-Didsbury, east to Airdrie East, west to Calgary-Foothills-Airdrie West, centre-south to Calgary-Airdrie. The north piece holds about 350 people, so three of the four hold at least 2% of the city. Only Airdrie East is mostly Airdrie; each other piece is stapled to a Calgary-edge or rural district. An Airdrie resident with a question for her MLA has to know which part of the city she lives in before she can call the right office. Her neighbours two blocks over will give her three different answers. The PTA at her child's school cannot send a single delegation to one MLA on a school-funding question. It has to coordinate four delegations to four offices, and three of those MLAs answer first to voters outside Airdrie. The minor-hockey association, the food bank, the Chamber of Commerce: every organization that works citywide now works across four provincial ridings.",
			airdrie_callout_label: 'WHY AIRDRIE MATTERS',
			airdrie_callout_p1: 'Airdrie has 85,805 people (2024 municipal census). One council, one tax bill, one school division: every civic system treats it as a unit.',
			airdrie_callout_p2: 'Split it across four provincial divisions — Calgary-Airdrie, Calgary-Foothills-Airdrie West, Olds-Three Hills-Didsbury and Airdrie East — and three of them are identified mainly with a neighbouring jurisdiction. The city has 85,805 residents, and one seat in the legislature where a majority of voters call the place home. The majority map gives it two.',
			airdrie_callout_p3: 'A four-way split is invisible to every partisan-fairness test except the one that asks: can a voter find their MLA?',
			airdrie_callout_summary: 'Both maps are legal. The four-way split is a choice.',
			airdrie_btn: 'Show flagged districts on map',
			anchoring_p: "<strong>Where it departs from municipal lines, it departs at strategically important places.</strong> When an electoral map follows the edge of a city or town, voters can tell where their division begins and ends: the property-tax line, the local-election ward line and the provincial-election line all fall in the same place, and often the school-division line too. Statistics Canada publishes these boundaries for free. On official Elections Alberta shapefiles, both maps follow municipal lines at comparable overall rates — the majority at 80%, the minority at 72% — and both sit within Canada's 70–85% norm (Quebec: 78%, Ontario: 82%, BC: 71%; comparator commissions documented in the monograph). (The audit's first, provisional analysis showed the minority anchoring at only 15%; that figure did not survive recomputation on official shapefiles — see the correction note below.) What stands out is not the overall rate. It is where the minority's departures cluster. The three boundaries the commission's own majority, the chair among them, flagged as anomalous — Rocky Mountain House–Banff Park <button class=\"ed-trigger\" data-ed-name=\"Rocky Mountain House-Banff Park\">show ↗</button>'s extension into uninhabited national-park land, the Nolan Hill–Cochrane <button class=\"ed-trigger\" data-ed-name=\"Calgary-Nolan Hill-Cochrane\">show ↗</button> lasso corridor, and the Olds–North Airdrie <button class=\"ed-trigger\" data-ed-name=\"Olds-Three Hills-Didsbury\">show ↗</button> reach — each break from pre-existing civic geography, in the exact urban-edge zones where pairing urban and rural voters most directly affects which party wins the seat.",
			anchoring_followup: 'The minority commissioners gave reasons for each of the three flagged boundaries. For Rocky Mountain House–Banff Park, they cited geographic size, the Highway 22 corridor, and how close First Nations reserves sit to Rocky Mountain House. The commission chair called the extension into uninhabited national park land "a bad faith effort" to satisfy the area criterion, and the phrase appears in the commission\'s official final report. For Nolan Hill–Cochrane, they cited shared transportation and employment ties between northwest Calgary and Cochrane. Statistics Canada journey-to-work data shows only 35.8% of Cochrane workers travel to Calgary at all; most work within Cochrane itself. For the Olds–North Airdrie reach, they cited Highway 2 corridor continuity. The audit found the specific Airdrie extension fails on population grounds. Checked independently against primary data, five of the minority\'s six published sub-rationales fail or only partly hold.',
			packing_p: "<strong>One area of Calgary is carved up to concentrate NDP voters into larger-than-average divisions.</strong> In Calgary's north, east, and central districts <button class=\"ed-trigger\" data-ed-name=\"Calgary-North West-Bearspaw\">show ↗</button>, the minority map's divisions average 11.5% above the provincial average. On the majority, 2.8%. The same geographic zone, drawn by the same commission under the same constraints, produces districts about 8.4% larger on one map than on the other. That fits the structural signature of <em>packing</em>: crowding one party's voters into fewer, larger districts, so each of their ballots weighs less. Packing and <em>cracking</em> (spreading a party's voters thinly across districts they narrowly lose) are the two classic gerrymandering moves. Both shrink a party's seat count below its vote share.",
			chair_p: "The commission chair — appointed under the same Act, working from the same submissions — flagged four boundaries on the minority map as geographically anomalous, among them these three: Rocky Mountain House–Banff Park's extension into uninhabited national park land; the lasso-shaped Calgary-Nolan Hill–Cochrane corridor; the Olds–Three Hills–Didsbury reach into north Airdrie. The same chair gave the majority zero such flags. (In all, the chair's published criticism covers seven boundary configurations: the four geometric flags, plus three places named only in the majority report's claim that the minority's changes lacked public support. This audit independently confirmed anomalous geometry for three of the four geometric flags. The fourth, Calgary-Foothills-Airdrie West <button class=\"ed-trigger\" data-ed-name=\"Calgary-Foothills-Airdrie West\">show ↗</button>, did not meet the audit's confirmation threshold.) Beyond the chair's geometry flags, the audit's own cracking-signature test (academic §5.3.2) does not flag the four-way Airdrie split. It is a community split that leaves Airdrie's residents a minority in three of the four ridings, which together hold nearly half the city, but the test needs them outnumbered in all four, and Airdrie East is mostly Airdrie. Chestermere comes up cracking-adjacent; Cochrane, kept whole and about two-thirds of its riding, does not. Some of what the audit's math flags, the chair did not. The audit measures the structural effect. Not intent."
		},
		litmus: {
			heading: '3: The 1,010,000-Map Litmus Test',
			fig_alt: 'Histogram of the efficiency gap across 1,010,000 computer-drawn Alberta maps. Nine in ten fall between about −1% and +4%. The minority map (purple line) sits at +4.0%, the 94.5th percentile, just short of the dashed line where the shaded right edge begins. The majority map (teal line) sits at +0.1%, well inside the normal range.',
			fig_caption: 'This is how the <button class="vocab-term" data-def="how unevenly votes turn into seats; positive values favour the UCP, negative values favour the NDP" aria-expanded="false">efficiency gap</button> spreads across 1,010,000 computer-drawn Alberta maps, made from the same voting areas as the real maps and scored on 2023 election-day ballots. Nine in ten fall between about −1% and +4%. The shaded right edge marks the top 5%. The minority map’s +4.0% stops just short of it, at the 94.5th <button class="vocab-term" data-def="where a map ranks among the computer-drawn maps: the 94th percentile means 94 in 100 of them lean less toward the UCP" aria-expanded="false">percentile</button>: fewer than 6 in 100 computer-drawn maps reach that far. The majority map’s +0.1% looks like what a neutral process usually produces.',
			table_intro: "The table sets the two maps side by side. The first five rows use no election results; they are properties of the lines themselves. The last two depend on how votes were attributed to each district.",
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
			vocab_label: 'VOCABULARY',
			vocab_eg: "<strong>Efficiency gap.</strong> A single number for how lopsidedly a party's votes turn into seats. Positive numbers favour the UCP; negative, the NDP. The audit draws Alberta's outlier line at ~4.1%: the value exceeded by only 5% of the 1,010,000 neutral Alberta-specific simulations. That threshold is not borrowed from US or general literature. A threshold calibrated to another jurisdiction would be wrong here, because Alberta's natural geography produces a different neutral range.",
			vocab_mm: "<strong>Mean-median difference.</strong> The gap between a party's median district vote share and its mean district vote share. When one party wins many close races, the median sits above the mean: those votes are spread efficiently. When a party wins many races by large margins, the mean sits above the median: votes are being wasted. A large mean-median gap in one direction flags structural inefficiency in how one side's votes are spread across districts.",
			vocab_percentile: '<strong>Percentile ranking.</strong> In this audit, a "percentile" is a rank within the 1,010,000 neutral simulated maps. "p94" means 94% of neutral maps score lower: the real map is more extreme than 94% of neutral draws. "p99.99" means fewer than 1 in 10,000 neutral maps reach that level.',
			vocab_anchoring: '<strong>Anchoring.</strong> The fraction of an electoral border that lies on a pre-existing administrative line — a city limit, a school-division boundary, a Statistics Canada census line.',
			closing_p1: "The bottom rows depend on election results. The <em>seats@50/50</em> test holds the electorate at perfect parity — the UCP and NDP each win exactly half the votes province-wide — and asks how many seats the map hands the UCP. Neutral Alberta maps produce a median around 44.8% UCP seats. Alberta's geography, with NDP voters concentrated in city cores and UCP voters spread across rural ridings, gives the NDP a small efficiency advantage at neutrality. The majority map, at 46.1%, sits at the 78th percentile of the 1,010,000-map simulation: well inside the normal range. The minority map, at 51.7%, sits at the 99.99th percentile. Fewer than 100 of 1,010,000 neutral draws reach that value. The <em>efficiency gap</em> measures how lopsidedly each party's votes turn into seats. On the official Elections Alberta shapefiles the minority's efficiency gap is +4.0%, at the 94.5th percentile: just below the audit's 95th-percentile outlier line. The opening questions at the top of this page unpack the consequences.",
		},
		commission_split: {
			heading: '2: How the Commission Split',
			intro: 'Alberta\'s Electoral Boundary Commission finished its work on March 23, 2026 and could not agree. Three commissioners produced one map; the other two produced a different one. Commission Chair Justice Dallas K. Miller and two opposition-nominated commissioners wrote the majority report; two government-nominated commissioners — Dr. Julian Martin and John D. Evans — wrote the minority report. The split centred on how to draw boundaries in fast-growing urban-edge communities. The majority gave Airdrie two districts; the minority four. The majority drew north/east/central Calgary\'s divisions close to the provincial average; the minority drew them 11.5% above it. Both maps follow the same statute. Both are legal under the <em>Electoral Boundaries Commission Act</em>. The disagreement was about which specific geographic configurations best served the communities being drawn. Alberta\'s governing party is the United Conservative Party (UCP); its main opposition is the New Democratic Party (NDP). Smaller parties — the Alberta Party, the Liberal Party of Alberta, and others — contest seats too, but their combined provincial vote share has been low enough in recent elections that it does not materially affect the audit\'s partisan-fairness calculations, which are grounded in the 2023 UCP–NDP split. This audit measured both maps using the same methods, applied identically. Four findings stand out.',
			finding1: "<strong>The two maps differ on six things you can measure without looking at any election results:</strong> how evenly people are spread across districts, whether voters are concentrated, how badly cities are cut up, whether borders follow city limits, the shape of the districts, and how many boundaries the commission's majority, the chair among them, flagged as anomalous in writing (final report, pp. 62–63). The minority map differs from the majority on every one of them.",
			finding2: '<strong>Every measured difference favours the same party.</strong> Everywhere the two maps diverge — north and east Calgary, Airdrie, urban areas with clear city limits — the minority map draws boundaries that spread NDP votes thinner and let UCP votes count more efficiently. The communities most reshaped by the minority map are the same communities where the NDP is strongest. The audit cannot determine intent. It can measure effect.',
			finding3: '<strong>The process that replaced the commission had one precedent among the Canadian redistribution cycles this audit reviewed: Alberta\'s own, in 1992.</strong> None of the reviewed provinces hands redistricting, partway through a cycle, to a committee the governing party controls. Like most provinces, Alberta requires the legislature to act before a commission\'s map takes effect; Quebec is an exception. A commission report here changes nothing until the legislature passes a separate <em>Electoral Divisions Act</em>, so the governing party decides whether any commission map becomes law. On April 21 the Assembly used that power: Government Motion 37, passed 44 to 36, set both commission maps aside and gave the work to an MLA committee with a UCP majority. The government\'s stated justification was the chair\'s Recommendation 5. What that recommendation actually asks is set out next.',
			finding4:
				'<strong>The statistical finding survives an independent change of simulation machinery.</strong> Forest-ReCom Phase A (100 k) yields percentile ranks within ±5 pp of canonical ReCom on every partisan metric — the pre-registered robustness check (OSF <a href="https://osf.io/he53s/" rel="noopener">he53s</a>, executed 2026-07-10; every metric moved by less than one percentile point). Details in Finding 9.',
			closing: '<strong>The process is its own finding, separate from the maps.</strong>'
		},
		november: {
			heading: 'The Lunty Committee',
			context_label: 'CONTEXT',
			context_body: ' — This section describes the process that replaced the commission and the legal framework that applies to it. It is not part of the statistical findings. The findings are in the fifteen findings above.',
			intro: "Neither commission map is in force. On April 21, 2026 the Legislative Assembly passed Government Motion 37, setting both aside and referring redistricting to a Select Special Committee of six MLAs — four UCP, two NDP — chaired by Brandon Lunty (UCP, Leduc-Beaumont). The committee itself does not draw the map. It oversees a separate Independent Advisory Panel, constituted under the same motion, tasked with producing a 91-seat boundary proposal.",
			intro_b:
				"Motion 37 contemplated five panel members — a chair (a post-secondary president, a judge or retired judge, or someone of similar stature), two members nominated by the Premier, and two by the Leader of the Opposition. The committee appointed retired Court of Appeal justice Brian O'Ferrall as chair on June 2, 2026, on the Premier's nomination, and on June 9 the four other members — the Hon. Monte Solberg and Darwin Durnie (Premier's nominees) and Dr. Gerard Kennedy and Brent Robinson (Opposition nominees) (committee report, p. 9). The committee must deliver its report to the Legislature by November 2, 2026. Unlike the original commission, neither the committee nor the panel is required to hold public hearings; the panel draws on submissions the original commission gathered. When the committee's map is released, this audit will apply the same methodology to evaluate it.",
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
				"The Saskatchewan framework does not categorically prohibit partisan considerations in redistricting. What it establishes is that boundary maps must, on the whole, provide effective representation to voters: relative parity of voting power is a prime condition of effective representation, and departures from it may be justified where they give more effective representation, taking into account factors such as geography, community history, community interests and minority representation. The audit's statistical and structural findings — the minority map's position at the 99.99th percentile of 1,010,000 neutral draws, its crossing of four of five structural thresholds (the fifth, anchoring, is neutral for both maps), the identified communities affected — are the evidentiary record a s.3 applicant would need to assemble. On the community-of-interest side of that record, the Federal Court's decision in <em>Raîche v. Canada</em> (2004 FC 679) is the leading Canadian authority: the court there required the federal Electoral Boundaries Commission to revisit boundaries that had ignored Acadian community of interest in New Brunswick. The audit's municipal-anchoring measurements and its specific community findings — Airdrie split into four districts, the chair-flagged urban-edge anomalies in northwest Calgary — are the same kind of evidence the Federal Court treated as legally cognizable. Whether that record meets the constitutional threshold is a legal question this audit does not decide; the audit reports the measurement.",
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
			frame_h: 'Evidence, not proof',
			frame_p1:
				'You may have come here looking for proof that a map was rigged. This report does not have it. It cannot have it — and why it cannot is the most important thing we found.',
			frame_cast:
				'Alberta’s 2025–26 Electoral Boundaries Commission finished its work on March 23, 2026, and could not agree. Three commissioners signed one map. The other two — the two the government nominated — signed a different one. Both maps are legal under the <em>Electoral Boundaries Commission Act</em>. Four weeks later, on April 21, the Legislative Assembly set both maps aside and handed the pen to a committee of six MLAs: four of them from the governing United Conservative Party (UCP), with a UCP member in the chair. That committee’s map is due November 2, 2026.',
			frame_p2:
				'We measured both commission maps, and the process around them, every way we knew how. What we found is fifteen findings, each one real, each one measured, each of which would count for something in a courtroom — and none of which, alone or together, can legally prove the conclusion they invite. Evidence that a map has a partisan effect is not evidence of who intended it, or why. That gap between evidence and proof is not a loophole we failed to close. In Canada, it is the system as written. That, too, is a finding.',
			frame_p3: 'So this report is built like an evidence log. Each finding gets the same five questions, in the same order, every time:',
			beat_found: 'What we found',
			beat_found_d: 'the evidence, with its number.',
			beat_show: 'What it could show',
			beat_show_d: 'the conclusion you will be tempted to draw, stated at full strength.',
			beat_experts: 'What the experts say',
			beat_experts_d: 'how this kind of evidence is treated in places that do fight about it in court.',
			beat_canada: 'What Canadian practice expects',
			beat_canada_d: 'the norm.',
			beat_gun: 'Why it isn\u2019t proof',
			beat_gun_d: 'the specific reason, under Canadian law, this evidence proves less than it seems to.',
			frame_p4:
				'Each of the eight legal reasons is different. By the fifteenth finding you will have learned, one piece at a time, how Canadian boundary law really works — and why every finding in this log ends the same way.',
			frame_p5:
				'Two findings in the log point the wrong way for our own story, and both are reported in full: one test that stopped telling the maps apart when better data arrived, and one lane where the minority map did better than the majority. A report that never loses an argument with itself isn\u2019t checking. Failed and null tests are part of the record.',
			frame_coi:
				"One more thing belongs in the log before the first finding: the author's own prior. He has voted for and donated to both conservative and progressive provincial parties in Alberta. For about 27 years he has also worked as a contract election officer for Elections Alberta, election by election, administering the vote on election day; nothing in this audit comes from that work. Three findings that ran against his expectation are kept in this log anyway, and every number reproduces from public code, public data, and random seeds committed in public before the analysis ran.",
			frame_lenses:
				'This episode has three lenses, and each has its own companion page: <a href="__BASE__/law">what the law asks</a>, <a href="__BASE__/norms">what the norms ask</a>, and <a href="__BASE__/methods">how the maps were tested</a>. The log below draws on all three.',
			frame_p1b:
				'Or maybe you came for something simpler. You heard Alberta is fighting over its electoral map, and you want to know what the fight is about. The short version: where district lines fall decides whose votes add up to a seat and whose scatter. Alberta was redrawing its ridings, the districts that each elect an MLA. The independent commission doing the work split into two camps and filed two competing maps on March 23, 2026 — both legal under the Act, both signed. Four weeks later the government set both aside and handed the pen to a committee its own party controls, a move Alberta last made in 1992. The fight is over what that committee will draw this November, and whether anyone could tell if it were drawn unfairly. This audit exists so that someone can tell.',
			frame_routes:
				'Two ways in, then. If you came to learn the fight, start with the picture just below, then the map on the cover; the interlude midway down brings it to your own street. Each of the episode\'s three lenses has its own plain-language page: <a href="__BASE__/law">the law</a>, <a href="__BASE__/norms">the norms</a>, <a href="__BASE__/methods">the statistics</a>. If you came for the evidence, the log starts at Finding 1: fifteen findings, five questions each, every one ending the same way.',
			refrain: 'Evidence, not proof.',
			refrain_not_even: 'Not even evidence against the map. We logged it anyway.',
			c2_refrain: 'An accusation in the official record, not a finding of any tribunal.',
			c3_refrain: 'Two findings now, still no proof.',
			c4_refrain: 'Three findings now, still no proof.',
			c6_refrain: 'Sixty-nine of 1,010,000 — evidence, not proof.',
			c8_refrain: 'Odds this long — evidence, not a verdict.',
			c11_refrain: 'Bad reasons for a lawful line are still a lawful line.',
			c13_refrain: 'Nothing in the Act forbids it, as the audit reads it.',
			know_more: 'Know more',
			act1_h: 'Act I: What the Map Does',
			act1_intro:
				'Act I walks the lines themselves. No election results, no simulation: just geometry anyone can check against a paper map. The two drafts were drawn in the same room, by five commissioners working from the same statutory rules, the same provincial geography, the same archive of 1,345 public submissions and the same demographic data. They agree on most of Alberta. Where they part ways, they part on choices someone in the room had to make.',
			act1_table_h: 'Act I in one picture',
			act1_table_close:
				'On Act I\u2019s tests, the majority crosses zero of the discriminating structural thresholds, the ones that tell the maps apart. The minority crosses every discriminating one: four of four, with the fifth, which does not tell the maps apart, shown rather than hidden. These measurements are geometric. They need no statistical sampler and no vote data. We wrote four of the five down on April 24, 2026, in a dated repository commit, after measuring both maps on provisional boundaries, and added the Airdrie split the next day.',
			c1_title: 'Finding 1 — A city of 85,805 with one seat of its own',
			c1_found:
				'Airdrie is one city, with one council and one tax bill. Its 85,805 people (2024 municipal census) share one set of city services. The law caps each riding at one and a quarter times the provincial average, so Airdrie needs at least two ridings. The majority map gives it two. The minority map gives it four. About 350 people in the north go to Olds-Three Hills-Didsbury. The east goes to Airdrie East, which holds more than half the city. The west goes to Calgary-Foothills-Airdrie West and the centre-south to Calgary-Airdrie, and in both of those, Calgary residents outnumber Airdrie’s. I tested the split for cracking: splitting a community so thinly that it decides nothing (academic report §5.3.2). I wrote that test’s rules in the same session I first ran it, so it counts as added later. To count as cracking, a split has to clear two bars. The first is more pieces than the city’s size requires, and the minority’s split clears it. The second is that Airdrie’s residents are outnumbered in every piece. In Airdrie East they are not: nine in ten of its people live in Airdrie. So by the test’s own rule, the minority’s split is not cracking. The majority’s two-way split clears neither bar.',
			c1_show:
				'Outside Airdrie East, the minority’s split is cracking as the textbook defines it. Picture an Airdrie resident with a question for her MLA. Before she can call the right office, she has to know which part of the city she lives in. The parents’ group at her child’s school can’t send one delegation to one MLA. It has to send four, to four offices, and three of those MLAs answer first to voters who don’t live in Airdrie. If you wanted to weaken the voice of a fast-growing, hard-fought city, this is what it would look like.',
			c1_experts:
				'Community splitting is one of the primary red flags in the redistricting literature, because it is one of the two mechanical moves by which lines turn votes into fewer seats. The other is packing, its mirror. A four-way split is invisible to every partisan-fairness statistic except the one that asks: can a voter find their MLA?',
			c1_canada:
				'Splitting a city this size in two is routine. Splitting it four ways, with nearly half its people outnumbered, is not. Canadian commissions treat keeping a city whole as a core part of community of interest: the shared ties the law asks boundary drawers to weigh. And the same commission’s majority map shows that a two-way split was possible on the same ground.',
			c1_gun:
				'I found no Canadian decision that struck down a map for splitting a city. The <em>Electoral Boundaries Commission Act</em> allows cities to be split. Community of interest is one factor among several the Act lists, and it does not bind. The leading case on effective representation, the Supreme Court’s <em>Saskatchewan Reference</em>, tells courts to defer to how boundary drawers weigh those factors. Both maps are likely legal under the Act, though that is debated. Whether either is constitutional is a question for a court, and no court has ruled. The four-way split is a choice, and under Canadian law, choices inside the Act’s wide limits belong to whoever draws the map. <em>(Legal lesson 1: the Act’s factors are left to judgment, and courts defer.)</em>',
			c1_app: 'what \u201ccracking\u201d actually does to a vote',
			c2_title: 'Finding 2 — The three boundaries the chair called out',
			c2_found:
				'The majority wrote the commission’s official final report. In it, they call the minority’s park extension “a bad faith effort” to claim a population exception, s.15(2), written for remote communities where people actually live. The extension is the Rocky Mountain House-Banff Park riding’s reach into empty national-park land. It is one of four minority boundaries the report flags as odd on the map. Two more are the lasso-shaped corridor of Calgary-Nolan Hill-Cochrane and the reach of Olds-Three Hills-Didsbury into north Airdrie. The majority is the chair and two members. They were appointed under the same Act as the minority and worked from the same submissions. They raised no such flags against their own map. On its own, that proves little. You would expect criticism to run only at the other side. What gives the flags weight is a check of my own: shape tests that score both maps by the same rules. They confirmed odd shapes for three of the majority’s four flags. The fourth, Calgary-Foothills-Airdrie West, did not meet my bar. (The report’s published criticism covers seven boundary arrangements in all.)',
			c2_show:
				'The bad-faith charge is one I could test. Without the empty park land, the riding still meets four of the five tests for the remote-riding exception, s.15(2), so it qualifies without the park. My check undercuts the charge. Still, the chair was among those who made it, against colleagues on the same commission. That shows how deep the split ran. It does not show that the exception was gamed.',
			c2_experts:
				'Spotting a gerrymander, lines drawn to give a party an advantage, began with strange shapes. Corridors and reaches into empty land are the classic signs. In fairness, the Banff arrangement has a sound geography behind its odd name and odd shape. The town of Banff sits inside a federal park it cannot grow into, and grouping it with Canmore makes sense as a community. My Banff analysis gives that side of the story full credit. What the town’s placement cannot explain is why the line runs out into the park at all.',
			c2_banff_link: 'See Banff on the map',
			c2_canada:
				'Commissioners disagree in their reports all the time. A commission majority accusing its colleagues of bad faith in the official final report is rare. I know of no other case, though I have not searched past reports one by one.',
			c2_gun:
				'The words “bad faith” are the majority’s opinion, in a report with no legal force. They are a charge, and no tribunal ever weighed it. Under the Act, both reports were advice, and only advice, from the moment they were filed. The Legislature could set them both aside. It did. <em>(Legal lesson 2: commission reports bind no one. The Legislature holds the pen.)</em>',
			c2_app: 'shape analysis and what s.15(2) protection is for',
			c3_title: 'Finding 3 — One zone of Calgary, drawn 11.5% too big',
			c3_found:
				'On the minority map, the seventeen ridings in one zone of Calgary, its north-east and centre, hold on average 11.5% more people than the provincial average. On the majority map, drawn by the same commission under the same rules, the zone’s ridings hold 2.8% more. So on one map they come out about 8.4% larger than on the other. The zone’s lists of ridings were first written, on April 22, as ridings where the NDP is competitive against ridings the UCP dominates. They were later described by geography, with the same ridings in each list. Read that geographic rule literally and the figures are 8.5% to 8.9% for the minority and 1.3% to 1.6% for the majority. That gap is a finding about equal population. It isn’t packing. Packing means crowding one party’s voters into a few ridings it wins by wide margins. My packing test (academic report §5.3.1) checks the margins. On 2023’s votes, the NDP wins eight of the minority map’s seventeen, by an average of 15.0 points. That is 12.6 below the provincial average of 27.6. The test needs the NDP’s wins there to run at least 15 points above that average, so it finds no packing. As with the Airdrie test, I wrote its rules in the same sitting I first ran it, so it has counted as added later from the start.',
			c3_show:
				'A bigger riding means each ballot in it counts for a little less, whoever casts it. Size is one sign of packing. With cracking (finding 1), packing is one of the two classic gerrymandering moves. Here the size gap is real. The wide winning margins that would mark packing are not there.',
			c3_experts:
				'Packing and cracking are the mechanism behind essentially every partisan-gerrymandering case ever argued in a United States court. Oversized districts exactly where one party\u2019s voters cluster: that is the pattern the detection research is built to find.',
			c3_canada:
				'Some spread from the average is normal inside the legal limits. But Canadian commissions back it with community-of-interest reasons. The minority’s published reasons for this zone are among those checked in finding 11.',
			c3_gun:
				'Every one of those ridings sits inside the Act’s limit of 25% above or below the average. Canadian law gives no grounds to sue over a map’s effect on parties. Section 3 of the Charter protects each citizen’s effective representation: a real voice, which equal numbers alone don’t guarantee. It does not promise parties that votes will turn into seats in proportion, and no Canadian court has read it that way. <em>(Legal lesson 3: inside the limits, a size gap is a lawful choice. Harm to a party is not a harm the law recognizes.)</em>',
			c3_app: 'packing in a three-riding example',
			c4_title: 'Finding 4 — Worse at the one thing the law actually measures',
			c4_found:
				'On the commission’s own population tables, the minority map’s ridings miss an equal share by 4,707 people on average. The majority map’s miss by 3,180. That makes the minority’s gap 48% wider. The measure is called the mean absolute deviation, or MAD: the average of every riding’s distance from an equal share. On 2021 census numbers the difference shrinks, and the two maps’ average gaps come out almost the same. But on those numbers the minority map’s median gap, for the riding in the middle of the pack, is still wider: 3,938 people against 2,827. I held that median up against maps a computer drew without ever seeing a vote, each riding kept within 12.5% of the average. The minority’s median gap sits at the 99th percentile: wider than 99 in 100 of them. Against computer-drawn maps allowed the Act’s full 25%, both commission maps land at the low end of the range, where the gaps are smallest.',
			c4_show:
				'When a map’s lines look odd, the usual defence is that they were needed to even out population. On the minority map that defence runs backwards. The Act measures one value in every riding: equal votes, each one weighing the same. On the commission’s own figures, the minority map gives up more of it than the majority map drawn beside it. The minority map is the less equal of the two.',
			c4_experts:
				'In every formal model of redistricting, equal population is the constraint that comes first. Spread this wide, on a map drawn at the same time as a tighter one, is a cost signal: evidence that other goals outranked the statute\u2019s central value.',
			c4_canada:
				'Canadian commissions treat the allowed spread as a limit, not a budget to spend. In Alberta, the commission itself sees “a clear historic trend” “towards greater emphasis on voter parity”, that is, on equal votes (final report, p. 24).',
			c4_gun:
				'No riding on either map breaks the Act’s one population rule, a limit of 25% above or below the average. Up to four remote ridings may sit as much as 50% below the average (s.15(2)), and each map uses three of those four. Inside the limit, the law does not rank maps. A wider spread and a tighter one are the same in law. <em>(Legal lesson 4: the Act has one population rule, and the minority map follows it.)</em>',
			c4_app: 'what MAD measures, and why the law lets ridings differ in size',
			c5_title: 'Finding 5 — The finding that dissolved when we picked it up',
			c5_found:
				'I counted how often a riding line follows a city or town boundary. The majority map does it 80% of the time and the minority map 72%. The 2019 map, drawn by the last commission and still in use, sits between them at 75%. On this test the two commission maps cannot be told apart.',
			c5_show: 'When a riding line follows a city or town line, the property-tax line and the election line match, and often the school-division line too. Voters can tell where their riding begins and ends. On that measure the two maps look alike.',
			c5_experts:
				'This is what an artefact looks like: a signal made by the tools, not by the map. Provisional tracings manufactured it, and the real map files erased it. That lesson in method is why we re-ran everything on the official shapefiles the day Elections Alberta released them.',
			c5_canada:
				'Nothing. No Canadian statute or practice guide requires any particular anchoring rate. The 70–85% norm describes what commissions do; it does not prescribe what they must do.',
			c5_gun:
				'It settles nothing either way. Both maps sit close to the 2019 map, and the Act sets no minimum for this.',
			c5_app: 'what following town and city lines measures, and what it can’t show',
			act2_h: 'Act II: What the Simulation Sees',
			act2_intro_p1:
				'Act I needed nothing but the lines. Act II asks a harder question: how unusual are these maps, next to what a process with no agenda would draw? To answer it, we had a computer draw 1,010,000 mathematically neutral Alberta maps (4 independent chains \u00d7 252,500 steps, base seed from a public randomness beacon, fixed in the code on April 27, 2026 by the git record). It used the official Elections Alberta shapefiles and held to the same statutory rules and geographic boundaries the commission used. Think of the simulation as a \u201cwhat-if machine\u201d: what would Alberta\u2019s maps look like if nobody was trying to do anything? Set a real map inside that crowd, and its percentile \u2014 its place in the line \u2014 tells you how far out into the tail, the rare end, it sits.',
			act2_intro_p2:
				'One fact about Alberta makes every number below readable. In this province, neutral is not 50/50. Split the province-wide vote exactly evenly, and the median of the 1,010,000 neutral maps — the middle of the pack — gives the UCP only 44.8% of seats. Why? Rural UCP voters win their ridings by wide margins, about 70-30 on average, wasting many \u201cextra\u201d votes, while urban NDP voters win theirs by tighter margins, about 60-40, and waste fewer. Left alone, Alberta\u2019s natural political geography mildly favours the NDP\u2019s seat efficiency. Keep that baseline in mind. It is what the maps below are measured against.',
			c6_title: 'Finding 6 — Fewer than 100 maps in 1,010,000',
			c6_found:
				'If the whole province’s vote split exactly in half, the commission’s minority map would give the UCP 46 of its 89 seats, or 51.69%. To see how unusual that is, I tried the same even split on 1,010,000 maps a computer drew without ever seeing a vote. Those maps have 87 ridings, the number on the 2019 map. The middle one gives the UCP 44.8% of the seats. The highest any of them reaches is 51.72%, which is 45 of 87 seats. Only 69 of the 1,010,000 give the UCP more than the minority map does, and all 69 sit at that same value, 51.72%. That puts the minority map at the 99.99th percentile: further out than all but about 1 in 10,000. The commission’s majority map gives the UCP 46.1%. That is the 78th percentile, an ordinary result. The 2019 map, still in use today, gives the UCP 46.0%: the 65th percentile, or the 78th if every map that ties it is counted below it. For the minority map, two other fairness measures that were set in advance point the same way, toward the UCP. On the mean-median gap, it sits further out than 99.97% of the computer-drawn maps. On declination, it sits further out than 98.8%. Replay the 2023 election using only ballots cast on election day, and the minority map gives the UCP 60 of 89 seats, against 55 on the majority map. On all 2023 ballots, which every vote-based test on this site uses, the registered count gives 57 and 48. That count is partly an estimate. About half of 2023’s ballots were cast before election day, and Elections Alberta reports them only for each old riding. So I have to place them inside the new ridings by a rule. The registered rule, rule P, places them only among people who did not vote on election day, using Alberta data only. The older rule, kept as a check, gives 55 and 48. The whole difference is two Calgary seats on the minority map, Calgary-Edgemont and Calgary-Glenmore. Rule P gives both to the UCP, by 401 and 68 modelled votes. No seat moves across the range of early-voter lean the Alberta data allow. That range covers only the lean, though, so it understates the real uncertainty. Rule P is Amendment 14, signed on November 10, 2026. It was chosen after its effect on the maps was known, so it is not blind.',
			c6_found2:
				'How far can \u201caiming\u201d go? To find out, we also ran a targeted hill-climbing search — the standard tool for exploring biased-but-legal maps, which nudges a map step by step toward a chosen party — in both directions, 40,000 steps each, same constraints, same geometry. The minority map\u2019s 51.7% sits closer to the deliberately aimed UCP ceiling (52.9%) than to the neutral median (44.8%). The majority map\u2019s 46.1% sits much nearer the neutral median, at the 78th percentile. And around 50/50 the lopsidedness is starker than the number alone. A precision sweep finds that the minority map keeps the UCP at or above the 45-seat majority threshold down to about 49.2% of the two-party vote: the UCP could lose it by about 1.6 points and still form government. On the majority map, the UCP would need to win it by about 9 points to reach the same threshold. Same geography, same rules. The gap between the two maps is structural, not noise.',
			c6_show:
				'Neutral drawing almost never produces a map like the minority’s. The majority map is the kind a neutral process turns out all the time. The minority map is the kind you have to aim to draw.',
			c6_experts:
				'Ensemble outlier analysis — testing a real map against a crowd of neutral ones — is the state of the art in redistricting statistics. It is the method US courts found persuasive in the state cases that struck maps down. Three of four pre-registered metrics in the extreme tail, all four leaning the same way: that is a strong outlier profile. And the \u201cit\u2019s just Alberta\u2019s natural geography\u201d defence is already answered inside the method, because the simulation runs on Alberta\u2019s natural geography. That geography\u2019s baseline advantage tops out where the 2019 map and the 2026 majority sit: the 78th percentile, with the 2019 map\u2019s highest placement on any partisan measure in the low 90s. Against Alberta\u2019s naturally skewed baseline, the minority sits at the 99.99th percentile.',
			c6_canada:
				'No Canadian commission has ever had to test its map against computer-drawn maps like these. I am holding the process to a standard it never had to meet. That is why the result tells you something, and why it binds no one.',
			c6_gun:
				'As far as I found, no Canadian court has yet weighed evidence like this. In the United States, the Supreme Court held in <em>Rucho v. Common Cause</em> (2019) that even strong statistical evidence of partisan gerrymandering is not for federal courts to police. A percentile describes where a map sits. It is not a line a map crosses. The statistics have a limit too. The computer-drawn maps keep every riding near the same population and in one piece. They do not follow every rule the commission weighed: the s.15(2) exception for remote ridings, community of interest, and following town and city lines. So the percentiles measure how far out a map is against these maps. They do not measure it against every map a lawful commission might have drawn. These maps also have 87 ridings, where the commission’s have 89. A run that draws 89 ridings, and keeps the s.15(2) ridings where the commission put them, still puts the minority map past the 98th percentile on the three measures where it sits at the far edge. That same-size comparison is still provisional. It is a strong outside check, not a perfect one. And real elections are not split 50-50. A big enough swing in votes can outweigh any map’s lean. The 50-50 test shows what the map adds on its own. It does not show who would win. <em>(Legal lesson 5: the best kind of evidence in this field has no legal home in Canada.)</em>',
			c6_app: 'how the computer draws its maps, and how to read a percentile',
			c7_title: 'Finding 7 — The test that missed',
			c7_found:
				'That leaves the fourth fairness measure, the efficiency gap. It boils a map down to one number for how unevenly each party’s votes turn into seats. It counts wasted votes: every vote for a loser, and every vote a winner got beyond what it needed. A positive gap favours the UCP. On all 2023 ballots, under the registered rule P, the minority map’s gap is +5.64%, above the line of +2.15%. Only 192 of 1,010,000 computer-drawn maps reach a gap that large. On election-day ballots, the count this test was first set on, the gap is +4.0%, at the 94.5th percentile. The line I set in advance there is the 95th percentile, about +4.1%, so on those ballots the minority map just missed. The majority map’s gap on election-day ballots is +0.1%, at the 16.5th percentile.',
			c7_show: 'On its own, almost nothing. That is why it is in the record.',
			c7_experts:
				'Near-misses are what an honest battery of tests naturally produces. If every test in a report fires, a reader should grow more suspicious of the auditor than of the map. This one missed, and it stays a miss. (The efficiency gap’s proposed US threshold, about 7%, is an academic proposal no court has adopted.)',
			c7_canada: 'Nothing. No Canadian body uses the efficiency gap at all.',
			c7_gun:
				'On all ballots, under rule P, the efficiency gap is past its line and counts as one of the minority map’s four fairness flags. On election-day ballots it stays a miss, and I report that too. Setting the line in advance cuts both ways. <em>(On November 7, 2026, I registered a change that moved every vote-based test to all 2023 ballots. I wrote that change after I had seen the all-ballots results, the minority map’s included, so it was not blind. Rule P, the rule for placing early ballots inside each riding, followed on November 10 as Amendment 14. It is not blind either: I chose it after I had seen its effect. On the older rule, kept as a check, the line is +1.39% and the gap +2.55%, also above it. See <a href="#november">the panel’s map, on the main page</a>.)</em> <em>(Lesson about evidence: the line was set before the answer was known, so the answer was allowed to be “no.”)</em>',
			c7_refrain: 'Evidence, not proof — and this one we do not even claim.',
			c7_app: 'the efficiency gap in one worked example',
			c8_title: 'Finding 8 — The odds, and what that number is not',
			c8_found:
				'Here I put a figure on one chance: that drawing with no aim produces a map like the minority’s on all four fairness measures at once. It comes out between about 1 in 20,000 and about 1 in 570,000, depending on how the figure is worked out. Each figure is a model estimate on election-day ballots, not a bound. The four measures are combined into one score before any odds are worked out, so they count as one look, not four. On that combined score, none of the 1,010,000 computer-drawn maps sits as far out as the minority’s, so there is nothing to count. The odds come from a curve fitted to those maps. Where the curve can be checked, it undercounts: there are 1.2 to 3 times as many far-out maps as it predicts. That means the true chance is probably higher than the model says. The published model gives about 1 in 570,000 (p ≈ 8.84×10⁻⁷, doubled to ≈ 1.77×10⁻⁶). The doubling is a cautious allowance, not a correction for a stated set of tests. Other fair choices give other figures. A more cautious curve gives about 1 in 449,000. A rank-based version gives 1 in 238,000, and on that score 7 of the 1,010,000 computer-drawn maps reach the minority map’s distance. Dropping one of two measures that come close to counting the same thing twice gives 1 in 97,000. A second, smaller run with a different drawing engine gives 1 in 20,000. No all-ballots version exists, because the computer-drawn maps’ all-ballots scores are not in the repository.',
			c8_show:
				'You will want this number to mean “the chance the map is innocent.” It is my strongest single number, and the pull to read it that way is strong.',
			c8_experts:
				'Statisticians have a name for this mistake: the prosecutor’s fallacy. It mixes up “the chance of this evidence if innocent” with “the chance of innocence given this evidence”, and it has sent innocent people to prison. The number here is well defined. It is the chance that a map with this profile turns up when maps are drawn with no aim. This record refuses the swap. How rare the map is among maps drawn with no aim is not the chance of wrongdoing. To get that, you would need things no one has, such as how often honest drawers produce odd maps.',
			c8_canada:
				'No Canadian legal standard uses a number like this. There is no line for it to cross, because the law never set one.',
			c8_gun:
				'A map this rare can still, in principle, come from unusual but honest judgment. The number measures how far outside neutral drawing the map sits. It cannot see motive, and I will not pretend it can. What I do claim is the weaker statement, and it is well supported: drawing that follows the rules and never looks at votes almost never produces this profile. The explanation, I leave to you. <em>(Lesson about law and evidence: the odds of a map are not the odds of intent.)</em>',
			c8_app: 'the prosecutor\u2019s fallacy in plain language',
			c9_title: 'Finding 9 — We tried to knock down our own result',
			c9_found:
				'I made three attempts to knock down my own main result: the minority map’s place at the far edge of the computer-drawn maps. The results were mixed, and all of them are reported. First, I swapped the drawing engine, the method that makes the computer-drawn maps, for a different kind: a spanning-forest sampler, registered at OSF as he53s and run on 2026-07-10. Every measure’s percentile moved by less than one point, which meets the registered rule for a “robust” result on all four. But the run fell far short of the sample size it registered. So I read it as inconclusive at this run size. I do not read it as a finding that the result is robust. This far out at the edge, a fraction of a point matters: on the new engine, more than ten times as many maps reach the minority’s seat value as on the main run. So the swap shows the map stays far out, though not exactly how far. Second, I swapped the software. An independent program, the R redist package, drew 5,000 maps, and none reached the minority’s value. On that smaller run the majority map sits just above the 95th percentile; on the main run, at the 78th. Third, the mechanism test could not be run. I planned to test whether the odd shapes (the corridors, the park extension) are what produce the seat advantage. If they were, computer-drawn maps that give the UCP as many seats as the minority map does should be less compact than the rest. But none of the 5,000 maps reaches the minority’s seat value, so there is nothing to compare. At the lower cutoff I first used, only 3 maps qualify, and they are slightly <em>less</em> compact than the rest (about 0.227 against 0.232 on a standard compactness score). That is too few to show anything. Both kinds of evidence point at the same map and lean the same way. Whether the shapes are the cause is untested.',
			c9_show: 'The far-out result belongs to the map, not to my tools.',
			c9_experts:
				'Holding up across samplers and implementations is what separates a finding from an artefact. Reporting what you could not test is what separates an audit from advocacy.',
			c9_canada: 'Nobody requires any of this. We imposed it on ourselves, in writing, before running it.',
			c9_gun:
				'Ruling out a quirk of the tools is not ruling in design. The engine and software swaps found no sign that the map’s far-out place comes from the tools, though the engine run was too small to be conclusive. They say nothing about why the map is that way. <em>(Lesson about evidence: checks like these strengthen the description, never the accusation.)</em>',
			c9_app: 'what a sampler is and why swapping it matters',
			c10_title: 'Finding 10 — Three tests retired',
			c10_found:
				'Three exploratory tests have been retired and are not used on this site: a test of boundary choices in swing areas, a test of how packed and close ridings sit side by side, and a method for combining tests. Each proved unreliable when checked. One of them had recorded a pass for the minority map, so retiring it removes a point in that map\'s favour, and I say so here. The full record is in the <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">academic report</a>.',
			act3_h: 'Act III: What People Did',
			act3_intro:
				'Acts I and II measured paper. Act III reads conduct: what the people in and around the process wrote, claimed and chose. In court, conduct is usually where questions of intent get answered. Watch what happens to it here.',
			c11_title: 'Finding 11 — Six reasons, checked',
			c11_found:
				'The minority defends Calgary-Nolan Hill-Cochrane on the idea that Cochrane residents “move fluidly” into Calgary. Statistics Canada’s 2021 commuting data show that about 71% of Cochrane’s out-of-town commuters work somewhere in Calgary. That is a third of all its workers. About half of its workers stay in Cochrane. That is a real tie between two places. It says nothing about Nolan Hill, the Calgary neighbourhood the corridor reaches. Lines can be measured, and so can the reasons given for them. The minority commissioners published reasons for their disputed lines. I checked six, the Cochrane reason among them, and the count depends on the rule. Counting only reasons the minority actually stated, none is contradicted, and four are supported only in part. Counting my own arithmetic on whether population forced the line, four of the lines were not forced. The minority did not claim they were. This is not a finding that the minority made up its reasons. In most of these cases the general claim is true, and a line that honoured it could have been drawn. What the data do not reach is the particular line the minority drew. Airdrie’s commute to Calgary (about 76% of those who commute out) and its fast growth are both real. They could have supported a new Airdrie-area seat. Neither requires splitting the city four ways. Chestermere sends 86% of its out-of-town commuters to Calgary. It shares a Catholic school division with Calgary, but not a public one, and it shares no transit system with the Calgary riding the minority puts part of it in. The pairing of Red Deer with Sylvan Lake holds in part: 54% of Sylvan Lake’s out-of-town commuters work in Red Deer, and one Catholic school division serves both, though their public divisions differ.',
			c11_note:
				"Checked only against the minority. The majority’s report also gives checkable reasons for its own contested choices (final report, PDF pp. 44–60; for example, it kept Airdrie-West 12.4% under average on a growth projection). The audit tested only the minority’s stated reasons and did not test the majority’s. The check is reported as a single flag.",
			c11_show:
				'Reasons that fail a check look like reasons found after the line was drawn, not before. Where my arithmetic shows a line was not forced, population pointed to a line the minority could have drawn. The minority drew a different one.',
			c11_experts:
				'Setting a stated reason beside what the evidence supports is pretext analysis, a test of whether the reason is a cover. It is exactly how US courts probe intent in the gerrymandering cases they do hear. Reasons that fail on public data are the standard tell.',
			c11_canada:
				'Commissions publish reasons so the public can weigh them. Reasons that do not reach the line actually drawn leave the public unable to weigh that line.',
			c11_gun:
				'No Canadian law requires a commissioner’s reasons to pass an outside check, and a failed reason fits carelessness as easily as a cover story. Courts that review boundaries ask whether the result denies effective representation, not whether the reasons on file were tidy. <em>(Legal lesson 6: bad reasons for a lawful line are still a lawful line.)</em>',
			c11_app: 'how to check a stated reason against public data',
			c12_title: 'Finding 12 — The commission that couldn\u2019t sign one map',
			c12_found:
				'The commission split. It filed two final reports and two different 89-seat maps on the same day. The majority of three included the chair. The minority of two were the members the government nominated (<a href="https://www.assembly.ab.ca/about/news-and-announcements/2025/03/28/electoral-boundaries-commission-to-soon-begin-consultations" rel="noopener">Legislative Assembly of Alberta, March 28, 2025</a>; <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/evidence/legislature/assembly_news_ebc_appointed_2025-03-28.html" rel="noopener">archived copy</a>). They drew the map the earlier findings describe. My checks cut both ways across that divide. The majority report said the minority’s changes in five places had no public support in the 1,345 submissions (final report, pp. 59 and 62). The five are Airdrie, Cochrane, Chestermere, Red Deer and St. Albert. To check, I had AI agents working under my direction read every posted public record in full: 1,339 written submissions and 349 hearing presentations, 1,688 in all. Counts are records, not people: a campaign letter sent 20 times counts 20 times. People wrote before either final map existed, so a match means a request matches what a map does. It does not mean anyone endorsed that map. At Cochrane and St. Albert the majority is right: no record asks for what the minority drew there. In the other three places it is wrong, by one to three records. At Airdrie, 1 record asks for what only the minority drew, against 10 for what only the majority drew. At Red Deer it is 1 against 20, and at Chestermere 3 against 6. So in three places of five the claim is close without being exact. That cuts against the majority, not the minority, and it is in this record for that reason. The criticism also ran the other way, and the record holds that too. The minority report charges the majority with an “inclination to delete or mangle rural electoral divisions and, in effect, reduce effective rural representation” (minority report, p. 356). My one test aimed at the majority’s map so far asked whether its rural ridings are corridors built to isolate rural voters. It came back supporting the innocent, geographic explanation (added later; the design and its limits are published). Then, the same day the charge came to light, I counted the rural ridings themselves (added later; the hypotheses were fixed in the script before it ran, and every name it sorted is published). The count turns the charge around. The 2019 map has 31 rural-based ridings. The majority map has 28: it folds three into city-named ridings, merges six into three, and adds three new ones. The minority map has 23: it folds in seven and merges two into one. A stricter version of the sort gives the same order. Both maps thin rural representation compared with 2019, and that is the true core of the charge. But on the measure the charge itself names, the minority map does more of what it accuses the majority of. The same page makes a second charge that can be measured: that the majority declined to use the Act’s 25% flexibility in rural Alberta. The minority calls that flexibility “not a benign allowance for errors in mapmaking” but “a deliberate instruction”. That charge holds. The majority’s rural ridings average 6% below the provincial average, and only four are more than 10% below it. The minority’s average 12% below, and eleven are more than 10% below. Taken together, the two charges describe two ways of designing a map, not one fault: more but fuller rural ridings on the majority map, fewer but smaller ones on the minority map. Both directions of every check are in the record.',
			c12_show:
				'A process built to reach agreement produced two answers, and the far-out map came from the government’s nominees.',
			c12_experts:
				'Who appointed whom is standard evidence in institutional-capture analysis. It carries weight only when the instruments are applied to both sides alike, which is why our correction of the majority matters as much as our findings against the minority.',
			c12_canada:
				'One map per commission is the norm, even when a member dissents. The Act does plan for a split, but only to say whose report counts: when there is more than one, the majority’s is the commission’s report (s.9). It says nothing about a split this sharp, with the majority accusing colleagues of bad faith in the report itself.',
			c12_gun:
				'Being nominated is not being instructed. I found no evidence of coordination between the government and its nominees, and none can be inferred from the appointment alone. Commissioners, whoever named them, have gone their own way before. <em>(Lesson about evidence: who appointed someone raises the question; it cannot answer it.)</em>',
			c12_app: 'how commissioners are chosen, and what a nomination tells you',
			ledger_h: 'Both sides, tested — the accusations ledger',
			ledger_intro:
				'Every accusation each side put in writing, run through the same tests, each result reported where it fell. This ledger is not a scorecard. Nothing in it gets added up: some rows land on the minority, some on the majority. The only score in this report is the five locked tests above. None of these checks was set up ahead of time the way those five were, so they carry less weight. Every number and name behind them is public.',
			ledger_col_a: 'The accusation',
			ledger_col_b: 'Who made it',
			ledger_col_c: 'Where it landed',
			ledger_r1_a: 'Three of the minority\'s boundaries are geometrically anomalous',
			ledger_r1_b: 'The majority (final report, pp. 62–63)',
			ledger_r1_c: 'Largely confirmed — the audit\'s blind tests independently confirmed three of the majority\'s four geometric flags; the fourth fell below threshold',
			ledger_r2_a: 'The minority\'s changes in five places had \u201cno public support\u201d',
			ledger_r2_b: 'The majority (final report, pp. 59, 62)',
			ledger_r2_c: 'Mostly right — right on four of five, partly wrong on Chestermere',
			ledger_r3_a: 'The park extension was \u201ca bad faith effort\u201d to claim s.15(2) protection',
			ledger_r3_b: 'The majority (final report, p. 10)',
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
			c13_title: 'Finding 13 — When the process might have answered, it was replaced',
			c13_found:
				'The commission held hearings in sixteen communities and received 1,345 written submissions. After many of them (the minority report counts at least 56), it dropped its plan to remove the Lesser Slave Lake riding. That is a system visibly answering the public. Four weeks after its split reports arrived, that system was replaced. Government Motion 37 set both reports aside. It was put on notice April 16, then moved, debated and passed, all on April 21, 2026. It created the Select Special Committee on Electoral Boundaries: six MLAs, four UCP and two NDP, chaired by UCP MLA Brandon Lunty (<a href="https://www.assembly.ab.ca/assembly-business/committees/ceb" rel="noopener">committee page</a>). The committee\'s job was to oversee a 91-seat map and send it to the Assembly by November 2, 2026. Nothing required it to hold public hearings. As <a href="https://www.cbc.ca/news/canada/edmonton/alberta-boundaries-committee-motion-9.7172743" rel="noopener">CBC reported</a> it would, it held none on the map, and no draft was released for the public to challenge. The map itself was drawn by the Independent Advisory Panel, <a href="https://www.cbc.ca/news/canada/edmonton/alberta-boundaries-panel-legislative-committee-elections-9.7187435" rel="noopener">chaired by retired Court of Appeal justice Brian O’Ferrall</a> (appointed on the Premier’s nomination; committee report, p. 9). The panel reported on October 22, and it split too. On October 28 the committee voted 3 to 2 to end its review without adding observations of its own. On November 4, 2026, the Assembly voted 45 to 36 to concur in the map and to urge the government to introduce a bill. The map becomes law only when a bill passes. Back in April, in the Assembly, the government had presented the takeover as faithful to the commission: “We are adopting the recommendations from the report” (Government House Leader, Hansard, April 16, 2026). The opposition called the same motion the “minority report in slow motion.” I checked that claim of faithfulness against the majority report. It holds up only in part. The majority did say two more seats would have given more effective representation (p. 58), and Recommendation 5 itself calls for an all-party select committee (p. 66). But the majority asked the Legislature to adopt its 89-seat map. Its own fix for the seat count was aimed at future commissions. And the one recommendation that proposed 91 seats for this cycle was the chair’s alone: “My majority colleagues do not agree with me on this point.”',
			c13_show:
				'When the independent route did not deliver a usable answer, the government took the pen. The route it chose removed every way the public could contest the map before it becomes law.',
			c13_experts:
				'Published drafts and public hearings are two features that redistricting research treats as protective. The route that replaced the commission gives up both. Its panel is built like the commission, with two nominees from each side and a retired judge as chair (named on the Premier’s nomination). But a committee with a government majority oversees the panel, and MLAs send its map to the Assembly. Independently of this audit, civil-liberties observers (<a href="https://ccla.org/press-release/ccla-sounds-the-alarm-over-the-politicization-of-albertas-electoral-map/" rel="noopener">CCLA</a>) raised the concern that politics was entering the process.',
			c13_canada:
				'In modern Canadian redistricting, the deepest norm is that politicians do not draw their own ridings. The last time MLAs drew Alberta’s map, in 1992, the courts let it stand. In 1995 the Act was changed to alter how commissions are appointed (finding 14; the full story is on the law page). On the main page, my tests of the panel’s map measure the committee’s process against exactly the features it is not required to provide.',
			c13_gun:
				'As I read the Act, nothing in it forbids any of these steps, and no court has ruled on them. The Act makes the commission’s reports advice only. It sets no minimum time for notice or comment, and it requires no hearings and no draft for what follows. On my reading, the Legislature’s power to make law as it sees fit (parliamentary sovereignty) lets it do what it did. <em>(Legal lesson 7: the process that could have created accountability is optional, and on my reading, opting out is legal.)</em>',
			c13_app: 'the Act\u2019s process from commission to committee, end to end',
			c14_title: 'Finding 14 — The sixty-year norm, set aside in an afternoon',
			c14_found:
				'Canada spent about sixty years building independent boundary commissions. Since the federal reforms of the 1960s, they have been its answer to an old habit: governing parties drawing their own ridings. In May, Duane Bratt, Professor of Political Science at Mount Royal University, told me in private correspondence that this process was without precedent in Canada. Later I found Alberta’s 1992 committee. Alberta had handed a map to MLAs once before, in 1992, but that commission had deadlocked: five commissioners, five reports, no majority. In 2026 the commission did not deadlock. A majority signed a report, which the Act treats as the commission’s report, and it was set aside anyway. That distinction is mine, not Professor Bratt’s. In Quebec a commission’s map takes effect without the National Assembly’s final approval. In Alberta, as in most provinces, it takes a bill (<em>Lalande</em>, dissent, para. 31).',
			c14_show:
				'In the Assembly, the opposition named the move: “retaliation against the independent Electoral [Boundaries Commission].” The harm here is not one map. It is the proof that the guardrail was a convention, a habit and not a law. Conventions bind only governments that agree to be bound. Nothing stops the next government, of any party, from citing this cycle as a precedent.',
			c14_experts:
				'Research comparing jurisdictions treats independent commissions as the single most protective institutional feature against gerrymandering. Removing the institution matters more than any one boundary it might have drawn.',
			c14_canada:
				'The federal process and the provinces have their maps drawn by commissions at arm’s length from politicians, with exceptions. Alberta in 1992 was one. Quebec is another: in June 2026 its National Assembly passed its own 127-seat map, after the Supreme Court struck down the province’s pause of the commission. Alberta’s 2026 cycle left that standard by a simple majority vote.',
			c14_gun:
				'Constitutional conventions bind politically, but courts will not enforce them. The Supreme Court said so in the 1981 Patriation Reference. That does not put the process beyond the courts’ reach. In 2017 Nova Scotia’s Court of Appeal found a map unconstitutional because the government had stifled its commission’s independent view. In 2026 the Supreme Court struck down Quebec’s law pausing its commission (<em>Quebec (AG) v. Lalande</em>, 2026 SCC 13). What a court reviews is the map once it is law, under section 3 of the Charter. <em>(Legal lesson 8: norms are not law, but how a map is made can still matter in court.)</em>',
			c14_app: 'conventions versus law, and how norms erode',
			c15_title:
				"Finding 15 — The panel’s reasons, checked against its own map",
			c15_note:
				'<em>The quotes and populations here are the panel’s own. Where this finding uses the map’s lines, they come from my reconstruction, rebuilt from the panel’s report, because the panel’s map has not been released as an official map file yet. Those parts are provisional.</em>',
			c15_found:
				'The panel published reasons for its changes to the commission majority’s map, so I gave them the test finding 11 gave the commission minority’s. Does the panel apply each reason the same way to similar places, and do its own numbers support it? Where a change moves no seat, mostly yes. Calgary-West-Springbank really is the “much more regular polygon shape” the panel promised. The two changes that do move a seat on election-day ballots are Lethbridge and Banff. There, the reasons I could check do not hold up. (On all ballots, under the registered rule P for placing early ballots, no seat moves. Under the older rule, kept as a check, only the Banff change moves a seat. See <a href="#november">the panel’s map, on the main page</a>.)',
			c15_p1:
				'<strong>“Lethbridge already has population to spare,”</strong> the panel says, adding that the towns around the city are too small for ridings of their own. Its main reason for its southern changes is “better regional representation of the people of southern Alberta”. The panel itself pairs Lethbridge with Red Deer. Only two Alberta cities have no riding reaching past their limits, it notes, and “Those two cities are Lethbridge and Red Deer.” The two are close in size. On the province’s 2024 estimates, Red Deer has 113,145 people and Lethbridge 111,776, room for about two ridings each, Red Deer slightly more. The panel moves only a small edge of Red Deer into a rural riding, about 1,300 people into Blackfalds-Innisfail, and keeps the rest of the city in two city ridings. Lethbridge it splits four ways: one city riding and three that mix city and rural voters.',
			c15_p2:
				'<strong>The panel’s own test</strong> says a mixed city-and-rural riding is justified if it “reflects a genuine community of interest or is needed to achieve population-compliance.” In Lethbridge, population did not require it. The commission majority’s map met the legal limits in the south without mixing Lethbridge voters into rural ridings. Its two Lethbridge ridings sat 7.0% and 1.0% above the panel’s own average of 53,722. The rural ridings around the city sat between 6.7% below and 2.3% above it. The panel’s report names the other way to meet the limits: larger rural ridings. So the split is needed only once the panel chooses smaller rural ridings. That leaves community of interest. The panel argues it. The panel’s minority disputes it: “Its residents and leaders clearly want two MLAs.”',
			c15_p3:
				'<strong>Cochrane and Okotoks</strong> get ridings of their own, under the panel’s rule that growing mid-size places deserve “dedicated representation”. Lethbridge, a larger city, goes from two ridings of its own to one.',
			c15_p4:
				'<strong>Canmore-Banff was 331 people short</strong> of the floor for an ordinary riding, as the commission majority drew it. The Act forbids an ordinary riding more than 25% below the average. After a small transfer the whole panel agreed on, it was at most about 1,300 short. The panel added 8,901, in what it calls “a minor change ... to capture the necessary population”. It gives other reasons too, which I did not test: keeping the Bow Valley, Kananaskis Country and the foothills together as one mountain-and-foothills community, and giving Okotoks its own MLA.',
			c15_p5:
				'<strong>“Urban with urban residents”</strong> is how the panel describes the mix in its Springbank ridings. In 2021 the Springbank parts held about 40 to 70 people per square kilometre. The Calgary parts of the same ridings held about 1,500 to 1,900.',
			c15_show:
				'A reason used in one place but not in a similar one may not be the real reason. In Lethbridge and Banff, the two changes that move a seat on election-day ballots, the panel’s population reasons do not match its own numbers. Its other reasons there, regional representation and community of interest, are disputed, and I did not test them. Against the panel minority’s alternative map, those changes cost the NDP two seats on 2023 election-day ballots. On all ballots they cost none under the registered rule P for early ballots, and one under the older rule, kept as a check. Each seat that differs is too close to call. Of the NDP votes the panel’s changes move, 14,199 go from a seat the NDP wins or nearly wins into one it loses by 10 points or more, and 3,152 go the other way. That is about four and a half to one.',
			c15_experts:
				"Checking whether stated reasons are applied evenly is the core of pretext analysis, the same method described in Finding 11. A reason that holds everywhere it is used is evidence of a principle. A reason that holds only where it helps one side is the classic sign of a rationale found after the line was drawn.",
			c15_canada:
				'Commissions and panels publish reasons so the public and the Legislature can weigh them. A reason is meant to apply the same way from one end of the map to the other. This panel’s reasons can be checked against its own numbers.',
			c15_gun:
				'Ridings are drawn by deliberate choice, and an uneven reason fits several explanations. The judgment may have shifted between sections of the report. There may be a community tie the numbers cannot see, or a partisan purpose. The statistics can say that the Lethbridge split is rare among computer-drawn maps that respect city limits: about 1 in 100. But it is one of 12 such flags among 132 comparisons, and none of them holds up after correcting for the number of tests. Where the split puts the city’s voters is not extreme by the rule I set in advance. Nor is the split extreme next to small changes to the panel’s own map. Computer redraws of the south and central region find the panel’s layout there ordinary. Much of the four-and-a-half-to-one flow above is a move away from the commission majority’s layout, which those redraws find unusual, partly because they cannot draw a riding as small as its Canmore-Banff (<a href="#newer-checks">the newer checks, below</a>). What the statistics cannot say is why the line was drawn. A court would ask whether the result denies effective representation. It would not ask whether the reasons were tidy. <em>(Legal lesson 6 again: bad reasons for a lawful line are still a lawful line. But they are the right place to look.)</em>',
			c15_app: "how to check a stated reason against public data",
			rev_h: 'The Scorecard, Revisited',
			rev_p1:
				'Fifteen findings. No proof. Now go back to the picture from the top of this page — you can read it now.',
			rev_p2:
				'The horizontal axis is one of Act II’s four fairness measures: the efficiency gap, more UCP-favoured the further right you go. The vertical axis is Act I’s count of discriminating structural tests failed, the tests that tell the maps apart. The 2019 map and the 2026 majority sit in the quiet corner: near-zero skew, zero structural flags. The minority sits alone. Four of four structural flags. An efficiency gap just under the line we set in advance. And, off this chart’s axes, a tied-vote seat count that only 69 of 1,010,000 neutral maps exceed, and a 60-of-89 seat outcome on recent voting patterns. The two acts converge on the same map and the same communities. Whether the geometry is the mechanism could not be tested on the final data (Finding 9), yet both acts agree on who benefits.',
			rev_litany_intro: 'Now run this instrument itself through the same five questions, one last time.',
			rev_found:
				'A scorecard: the best instrument I could build to draw the first fourteen findings together into something that can be stated, checked, and falsified. Five pre-registered structural tests: the minority crosses every discriminating one, the majority none, the fifth, which does not tell them apart, on display. Four partisan-fairness metrics against 1,010,000 neutral maps: three in the extreme tail, one reported miss.',
			rev_show:
				'The closest thing to a gerrymandering signal that can exist under Alberta law and Canadian norms: a checkable way of saying \u201cthis map is the kind of map that aiming produces,\u201d with every threshold set before any answer was known.',
			rev_experts:
				'When intent cannot be seen, the field reads maps with combined batteries of outlier tests. Pre-registration is what keeps them honest.',
			rev_canada:
				'Nothing. No Canadian institution scores maps this way. That is exactly why we had to build one.',
			rev_gun:
				'Its thresholds are our own calibrations, not legal lines. Alberta is one province with one split commission: a sample size of one. And no pile of findings ever becomes proof, because the gap between \u201cextreme\u201d and \u201cdeliberate\u201d is not statistical. It is the gap the law chose to leave open.',
			rev_refrain:
				'This scorecard ran again in November, on the panel\u2019s map. The result is in <a href="#november">November: the panel\u2019s map, checked</a>.',
			playbook_h: 'What running the play again would look like',
			playbook_p1:
				'This report cannot prove a gerrymander; the word has no legal home here. What it can do is say, in advance and in public, exactly what the signature looks like, and then say whether the November map carries it. Our November tests were written down in June 2026 and amended in late October and November, some after results had been seen. The registration\u2019s own name for the check is the Lunty test, and it is the confirmatory counterpart to everything above. The signature has two halves. Process: were public hearings held; was a draft released; are the advisory panel\u2019s members and terms of reference published; does the map honour the recommendation the government cited when it took the pen? Outcome: where the map lands on every metric in this report, against the same million-map distribution, under the same pre-registered thresholds.',
			playbook_p2:
				'Suppose the committee\u2019s map repeats the minority\u2019s signature, though drawn by different people, under different constraints, on a different timeline. Then the structural finding above earns confirmatory status. If it lands inside the neutral bands, the finding stands as an isolated observation about one map that was never enacted, and this report will say exactly that. The scoring runs within 72 hours of the map\u2019s release, whichever way it points. That commitment was registered before anyone knew the answer. Pass or fail, you will not have to trust our judgment. Only our arithmetic, which is public, seeded from a public beacon, and reproducible by anyone.',
			appendices_note:
				'The findings above link to lettered explainers — one concept each, from \u201cthis is confusing\u201d to \u201cnow I understand\u201d — on the companion page:',
			appendices_link: 'The thirteen explainers (Appendices A–N)'
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
			p10: 'I could be wrong. Unlike most opinions about this government, mine ships with the terms of its own destruction. The panel’s map went to the Assembly on November 2. The tests were locked before it existed. Were hearings held. Are the advisers named, their terms of reference published. Does the map honour the recommendation used to justify the takeover. Where does it land against a million neutral maps. If it lands inside the neutral bands, my suspicion took real damage — and this site will say so within seventy-two hours, because I committed to that before I knew the answer. That is the difference between an opinion and an accusation. An opinion tells you what would change it.',
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
			p1: 'I\'m a student at Mount Royal University. I did this research on my own. It was not coursework, and the university did not commission it. My views are my own, not the university\'s. For about 27 years I have worked for Elections Alberta as a contract election officer, election by election, running the vote on election day. I am not under contract at present; I last worked at a recent election. I have had no other job with Elections Alberta, and I know nothing of its work beyond those tasks. Nothing in this audit comes from that work. Elections Alberta supplied the commission maps\' boundary files on request, and they are republished in the project\'s repository. Every other input is a public download. This research is mine, not Elections Alberta\'s, and does not speak for it. I have no connection to the commission. As an adult I\'ve voted for and donated to both conservative and progressive provincial parties in Alberta.',
			p2: "My political history could affect how I look at this issue, and the main protection against that is the method. I tested both maps the same way, registered my tests in public, time-stamped records, labelled every finding pre-registered or exploratory, and put everything online so anyone can check my work. I paid for this research myself. If you find something I got wrong, I want to know.",
			p3: 'The records: <a href="https://osf.io/6pt83" rel="noopener">OSF:6pt83</a>, AsPredicted #289,469 and AsPredicted #289,451. The random seeds come from a public beacon. The main simulation\'s seed was fixed in the code on April 27, 2026, before the official map files arrived; the record is a repository commit, not an OSF registration. The swing-zone test\'s seed was committed on May 6 together with that test\'s first results, so no record fixes it before a result existed. The neighbour-drain test (#289,451) was written down on April 24 and registered on the OSF on May 6, after a provisional pass on approximate boundaries. The others were filed alongside exploratory analysis.',
			p4: 'Questions or corrections: '
		},
		translation_about: {
			heading: 'About this translation',
			p1: 'You are reading a machine translation, made with AI. It has not yet been reviewed by a native speaker. The English version is the authoritative text: if anything in this translation is unclear or seems wrong, the English original governs.',
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
			c2_title: 'Condition 2 — Retired',
			c2_what: 'This condition concerned the neighbour-drain test. I have retired that test as unreliable, so I no longer claim the minority map passed it, and the condition no longer applies.',
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
				'This audit corrects in public and deletes nothing. The structural test that changed on the official boundaries is told in full at Finding 5; the two statistical tests that did not hold up, at Findings 8 and 10. The complete ledger of every correction — what changed, when, and why — is kept in the <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">academic report\u2019s DOCUMENTED CORRECTIONS section</a>.',
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
				'Early votes that no map can place, and census counts years out of date. Neither is the commission\'s doing. Both are built into the system and can be fixed.',
			advance_p1:
				'<strong>If you voted before election day in 2023, your ballot was counted, but no map can show which part of your riding it came from.</strong> About half of Alberta\'s votes are now cast that way, at advance polls, at mobile polls and by special ballot. Elections Alberta reports them only as totals for each riding. It does not report them for each voting area, the small areas a riding is made of. That leaves about 810,000 NDP and UCP votes from that election with no neighbourhood on the map. Yet every advance voter is checked against a voters list before getting a ballot, and that list ties each voter to a voting area. To report advance votes by voting area, the count would sort advance ballots by area, joining small areas together to keep each vote secret. Nobody would vote any differently. Only the count would change.',
			advance_p2:
				'The gap matters most to anyone who checks a map, as this audit does. Commissions are right to draw from population and leave votes aside, and the census already tells them where people live. But turnout by area would show which communities a map\'s ridings really reach. As far as the public record shows, commissioners see the same published results as everyone else.',
			lesser_slave_p1:
				'Take one voting area in the north of the Lesser Slave Lake <button class="ed-trigger" data-ed-name="Lesser Slave Lake">show ↗</button> riding. It covers 4,832 km&#178;, more than four-fifths the size of Prince Edward Island, and at the 2021 census it was home to 844 people. In 2023, not one vote there was cast at an election-day poll. Every vote went into the riding-wide totals for advance, mobile and special ballots. Those votes count in the riding\'s total. They cannot be placed on a map. In the published results, the community that lives there does not appear at all. So in at least one community in northern Alberta, the gap is total.',
			lesser_slave_p2:
				'When the commission first planned to remove the Lesser Slave Lake riding and merge it into a larger one, it had no vote data by place for those communities. At least 56 public submissions, by the minority report’s count, said the region is one community of interest. Some, such as submission EBC-2025-2-0028, wrote about the riding\'s small northern Indigenous communities. After that, the commission kept the riding, under s. 15(2) of the <em>Electoral Boundaries Commission Act</em>, the exception for remote ridings set out below. The communities got there. Even then, the published results could not show how many of their people voted.',
			ebca_label: 'SECTION 15(2) EBCA',
			ebca_body:
				'Section 15(2) of Alberta\'s <em>Electoral Boundaries Commission Act</em> lets a commission protect a small riding, one with more than 25% fewer people than the provincial average. The riding must meet at least three of five tests: (a) an area over 20,000 km², or a surveyed area over 15,000 km²; (b) more than 150 km from the Legislature Building to the riding\'s nearest boundary, by the most direct highway route; (c) no town with more than 8,000 people; (d) an Indian reserve or a Métis settlement in the riding; and (e) part of the riding\'s boundary running along Alberta\'s border. Up to four ridings may be protected this way, down to 50% below average. The protection is not automatic. The commission must judge whether the tests are met, and it may choose not to use it.',
			rationale_p1:
				'With about 27,000 people, Lesser Slave Lake had about half the provincial average, right at the legal floor. The commission\'s first plan removed the riding for that reason. It looks like a plain use of the rules. It is not. Here the law lets a commission choose. Lesser Slave Lake meets three of the five tests, the number the Act asks for. Its area is 69,566 km² (test a: over 20,000 km²). No town in it has more than 8,000 people (test c). It contains Indian reserves and M&#233;tis settlements (test d). Those communities share a northern geography and a common interest in an MLA who answers mainly to northern Alberta. Test b asks for more than 150 km from the Legislature to the riding\'s nearest boundary by highway. On my road model it is not met: for the riding as both final maps draw it, the model gives 134 km.',
			rationale_p2:
				'The commission\'s own words for its first plan were "we erred." That plan merged Lesser Slave Lake with Peace River into one riding called Mackenzie. It would have folded those communities\' shared voice into the largest riding in the province. The communities had not changed. The lines around them had. The riding\'s small population did not force its removal. Section 15(2) let the commission keep it once it added people, and the final report added Big Lakes County, Swan Hills and part of Woodlands County, bringing the riding to 45% below average. Together, the three tests the riding meets describe a large, thinly settled riding, home to communities whose stake in representation does not show in raw population counts. The commission\'s final report counted four tests met. On my road model it is three, which is still enough.',
			banff_p:
				'All five commissioners agreed to the first plan, the one that removed Lesser Slave Lake. Both final maps then protected the riding under s.&#x2009;15(2). The minority also used s.&#x2009;15(2) for Rocky Mountain House–Banff Park, a riding it stretched into the empty part of Banff National Park. In the official final report, the commission\'s majority, its own chair among them, called that "a bad faith effort". My check undercuts the charge: the riding qualifies under s.&#x2009;15(2) even without the park land. Still, on the minority\'s map, an exception meant for remote places where people live was stretched over empty parkland. The 91-seat map that came next was drawn by an advisory panel, overseen by a committee of MLAs. Section&#x2009;15(2) binds the commission. As I read Government Motion 37, it gave the panel the same exception. No law required public hearings on the panel\'s map, and none were held.',
			census_p1:
				'The other problem is timing. On the audit\'s population estimates, the 2019 riding of Airdrie-East grew by about 30% between the 2021 census and mid-2025, while Athabasca-Barrhead-Westlock grew by about 6%. Alberta grows fast, and not evenly. Yet the commission whose maps this audit checks had to start from the 2021 census, brought up to July 2024 with a provincial estimate. That count was already four years old when the maps were drawn. A map drawn from old counts is out of date from the day it is first used. <strong>Alberta should wait for the 2026 census before drawing the next map.</strong> Canada counts its people every five years. The 2026 census was taken in May 2026, and its first results are due in February 2027. A simple change to the <em>Electoral Boundaries Commission Act</em> could make the wait the rule. It could require that a new commission be appointed only after Statistics Canada releases the newest small-area data from the latest census. Then the maps would show where Albertans live now.',
			census_p2:
				'The 91-seat map was drawn from a census that was five years old when the map was delivered. The committee worked under the existing law, which sets no rule on census timing, and it could not delay past its November 2, 2026 deadline on its own. So this proposal is for next time: a future change to the <em>Electoral Boundaries Commission Act</em>. It asks nothing of the current process. The tension is real, and it is more useful to name it than to pretend it is not there.',
			closing:
				'Neither data problem is a finding about the commission\'s maps. Both are about a system that makes checking a map harder than it needs to be, and both can be fixed. If advance ballots were reported by voting area, and each new map started from the newest census, every future commission, and every future audit, would stand on firmer ground. These are practical suggestions. I don\'t offer them as conclusions.'
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
			body: 'Justice Dallas Miller, the commission’s chair, named one place for a restored seat, and this is it: a riding made mostly of Clearwater County and western Mountain View County, with s. 15(2) status, the rule that lets a large, remote riding have far fewer people than average. He wrote that if the Legislature would not accept losing two rural ridings, it should go from 89 seats to 91 and restore them. He asked that it be considered. He did not require it. For the second seat he named no place. The outline here is approximate: Clearwater County plus the part of Mountain View County that sat in the 2019 Rimbey-Rocky Mountain House-Sundre riding. It lies wholly north of Airdrie, and none of its land comes from a riding that condition (a) or (b) protects.',
			a: {
				title: 'Recommendation 5(a): no change from Airdrie south',
				body: 'Airdrie and Calgary are where the commission split most sharply, and this condition keeps them as the majority drew them. Under the chair’s Recommendation 5, restoring the two rural seats should not touch any riding in Airdrie, or with land south of Airdrie’s southern city limit, except Drumheller-Stettler. That is {n} ridings, every Calgary seat among them. Each should match the majority map line for line.'
			},
			b: {
				title: 'Recommendation 5(b): no change in north Edmonton',
				body: 'In Edmonton the line is the North Saskatchewan River. Recommendation 5 says restoring the two rural seats should not touch any Edmonton riding north of it, so {n} ridings should match the majority map. Beverly-Clareview crosses the river. About two-thirds of it is on the north bank, so I count it here.'
			},
			c: {
				title: 'Recommendation 5(c): south Edmonton goes back to the draft',
				body: 'Every Edmonton riding south of the North Saskatchewan River should return to the commission’s October 2025 interim map, Recommendation 5 says. That was the draft the commission published for comment, before the final split. The recommendation allows one option: adding Nisku to Edmonton-South East, to put Leduc and Beaumont back in one riding. The outline marks the {n} majority-map ridings that would change. It doesn’t show the interim lines themselves.'
			}
		},
		flags: {
			'banff-town': {
				title: 'Banff — the town carved out of the park',
				body: "Banff sits inside a federal national park, a small municipal island. The commission minority groups the townsite with Canmore, the next town down the Bow Valley, in “Canmore-Kananaskis.” It leaves the uninhabited park to the riding that carries Banff's name. The boundary hugs the town because it's the only populated spot for miles. It looks like a mistake, but it follows real geography."
			},
			'banff-park': {
				title: 'North of Banff — “Rocky Mountain House–Banff Park”',
				body: 'Much of “Rocky Mountain House–Banff Park” is national park where few people live. The town of Banff is in the riding to the south. For this riding the commission minority used the Act\'s remote-riding exception, section 15(2), which lets up to four ridings have far fewer people than average. The commission\'s majority called this “a bad faith effort” in the final report. My check undercuts that charge: the riding qualifies for the exception even without the park. In a full read of the public submissions, 13 records ask for the park to join the Rocky Mountain House riding, as the minority drew it, and 2 ask for the majority\'s Bow Valley riding. For the riding\'s core, Clearwater County, Rocky Mountain House and Sundre together, 36 ask for what the minority drew and none for what only the majority drew.'
			},
			'airdrie-split': {
				title: 'Airdrie — split four ways',
				body: 'The commission minority splits Airdrie across four ridings, and the city\'s population does not require that. Airdrie\'s growth and its commute to Calgary (about 76% of out-commuters) could have anchored a single new Airdrie-area seat. In a full read of the public submissions, 1 record asks for something like the minority\'s split, and 10 ask for what the majority drew. I ran the split through the cracking test. Cracking means splitting a community so thinly that it can\'t decide any of its seats. This split stops short of that. Outside Airdrie East, which holds more than half the city, Airdrie\'s residents are outnumbered, but the test needs them outnumbered in every piece. The fairness tests that use votes cannot see a split like this. I measure what a split does. Why it was drawn is a question my tests can\'t reach. (Technical report, section 5.3.2.)'
			},
			'nolan-hill-cochrane': {
				title: 'Calgary-Nolan Hill–Cochrane',
				body: 'The commission minority runs a narrow corridor from Cochrane to the Nolan Hill ward in Calgary. The riding is one of two the commission\'s majority said “look strange”. Cochrane\'s commute to Calgary could have justified pairing it with the city. But the 2021 journey-to-work data spreads that commute across the whole city, and it doesn\'t point toward Nolan Hill. About a third of Cochrane\'s workers commute into Calgary, and half work within Cochrane. The corridor reaches further than the data. In a full read of the public submissions, no record asks for Cochrane to be joined to northwest Calgary, and 7 ask for what the majority drew. Still, the cracking test does not flag it. Cochrane stays whole and makes up about two-thirds of the riding, and at about 34,000 people it is too small for a seat of its own. (Technical report, section 5.3.2.)'
			},
			'olds-airdrie-reach': {
				title: 'Olds–Three Hills–Didsbury — the Airdrie reach',
				body: 'About 350 people on the thinly settled northern edge of Airdrie go into a large rural riding on the commission minority\'s map. That strip is part of how the four-way Airdrie split works. The rural riding itself has public support. It keeps Olds, Didsbury and Three Hills together, along with Crossfield, Irricana and Beiseker. In a full read of the submissions, 29 records ask for that riding as the commission minority drew it, and 6 for the majority\'s version. It could have stayed within those communities. Instead the minority\'s version reaches south into Airdrie, which the population does not require. No record mentions that reach. By my own cracking test, the Airdrie split is not cracking. (Technical report, section 5.3.2.)'
			},
			chestermere: {
				title: 'Chestermere — split between two ridings',
				body: 'The commission minority puts a southern slice of Chestermere into a Calgary riding it shares no schools or transit with. That slice fails the population test. Chestermere\'s heavy commute to Calgary (86% of out-commuters) could have supported keeping the city whole and close to Calgary. In a full read of the public submissions, 3 records ask for a link with Calgary, as the minority drew, and 6 ask for what the majority drew. I count the slice as a split of a community, one that thins Chestermere\'s voice. I did not score it on the cracking test. (Technical report, section 5.8.4; reason checks, test 5.)'
			},
			'red-deer': {
				title: 'Red Deer — the hybrid ridings',
				body: 'Parts of Red Deer itself are folded into ridings led by Blackfalds, Sylvan Lake, Lacombe and Innisfail on the commission minority\'s map. That thins urban Red Deer\'s vote. The city\'s ties to those towns could have grouped the towns together instead. In a full read of the public submissions, 1 record asks for something like the minority\'s version: a letter asking for the city to be split into “3-4 separate ridings” with nearby towns. Against that, 20 ask for two ridings inside the city, as the majority drew.'
			},
			'st-albert': {
				title: 'St. Albert — competing configurations',
				body: 'In a full read of the public submissions, 22 records ask to keep the pattern both maps keep for St. Albert: one riding inside the city and one shared with Sturgeon County. No record asks for the commission minority\'s change (part of the city in Lac Ste. Anne-Parkland), and none asks for the majority\'s change. Either map\'s version could rest on a reasonable basis. The submissions give no clear signal for either map here.'
			},
			'calgary-zone-a-packing': {
				title: 'Calgary north and east — larger ridings, no packing signature',
				body: 'On the minority map, Calgary\'s ridings north and east of the Bow River average about 11.5% more people than the provincial average. On the majority map the figure is 2.8%. So each ballot there counts for a little less. That is a finding about equal population. The commission\'s majority raised it in words (final report, pp. 10 and 63), and I put a number on it; the area is my “Zone A”. The zone does not meet the packing test. Packing means crowding one party\'s voters into a few ridings it wins by huge margins. On 2023 votes the NDP would win 8 of the zone\'s 17 ridings, but by margins below the provincial average, and the test needs margins well above it. The numbers show what the map does. They can\'t show why. (Technical report, section 5.3.1.)'
			}
		},
		text: {
			page_title: 'Text version — Alberta Electoral Boundary Audit map',
			intro:
				'The map explorer in words, for screen readers: the boundaries I flagged, then every riding and which maps have it. The panel\'s 91-riding map isn\'t here yet.',
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
				'The explorer shows three maps of Alberta\'s ridings: the commission\'s minority map, its majority map, and the 2019 map, the one in use today. The panel\'s 91-riding map, the one before the Legislature, is left out because its official map files are not public. My provisional results for it are on the main page.',
			summary_p2:
				'Five structural tests look only at the lines. None of them uses an election result. I wrote them down on April 24 and 25, after trial runs on approximate boundaries and before the official files arrived. Four of the five compare the minority map with the majority map. They describe how the two differ, and they don\'t pass or fail the majority map. On four of five comparisons, the minority map differs from the majority map. A separate set of tests uses votes, and holds each map up against 1,010,000 maps a computer drew without seeing a vote.',
			summary_p3:
				'Further down, each of the nine boundaries I flagged gets its own note, and then every riding is listed. This page says what the measurements show. It reaches no legal conclusion about any map.',
			flagged_heading: 'Flagged boundaries',
			flagged_lead:
				'Nine boundaries made my list. Some look odd on the map and turn out to follow real geography. Others stand out on my own measurements, though none meets the formal packing or cracking test. The notes below cite a section of the technical report where one applies. The counts of public submissions come from a full read of all 1,688 public records: 1,339 written submissions and 349 hearing presentations. AI agents did the reading, under my direction. The counts are of records, not people, and a campaign letter counts each time it was sent.',
			r5_heading: 'Recommendation 5 areas',
			r5_lead:
				'The government cited the commission chair\'s Recommendation 5 when it gave the map to a committee of MLAs. The recommendation sets four conditions for a 91-seat map, and three of them name ridings on the majority map. Each area follows, with the majority-map ridings it covers.',
			r5_districts: 'Majority-map districts in this area:',
			directory_heading: 'District directory',
			directory_lead:
				'Every riding name on any of the three maps is here, in alphabetical order. Names change from map to map, so some rows appear on only one or two. Each row shows whether the name is on the minority map, the majority map and the 2019 map, and on each map that has it, the riding\'s 2023 vote total counting all ballots. For populations and test results, see the full report.',
			directory_totals_note:
				'A dash (—) means the riding name is not on that map. Every other figure is the riding\'s 2023 vote total on that map, counting all ballots. Elections Alberta reports advance, mobile and special ballots only for each 2023 riding as a whole. These totals spread them over that riding\'s voting areas in proportion to the election-day votes each area cast. That is the older rule, kept as a check. So each old riding\'s total matches the official result, but how it splits between new ridings is an estimate. The registered rule, rule P, places early ballots only among people who did not vote on election day, so it splits some of them differently. The full record gives its results.',
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
			head_title: 'The Thirteen Explainers · Alberta Electoral Boundary Audit',
			head_description: 'Thirteen short explainers on the findings of the Alberta Electoral Boundary Audit, in plain words: cracking, packing, computer-drawn maps, the prosecutor\'s fallacy, conventions and law, and more.',
			back: '← Back to audit',
			site_label: 'Alberta Electoral Boundary Audit',
			h1: 'The Thirteen Explainers',
			meta: 'Appendices A to N · one idea each',
			standfirst: 'Partway through a finding you may meet a term like "percentile" before you have seen it explained. The findings link here for that moment. Each explainer takes one idea. It starts from the question a fair reader might ask and builds the idea with one simple example. Then it sends you back to the finding, so you can read its number on your own. It ends with what the idea <em>can\'t</em> tell you. Read them in any order.',
			appendix_a: {
				heading: 'Appendix A — Cracking, or how a town can vote and elect no one',
				confusion: '<em>The question:</em> "Airdrie voters still vote. Nobody took their ballots. How can drawing lines \'dilute\' anything?"',
				p1: 'Picture a town of 40,000 that mostly votes Orange, in a region that mostly votes Blue. Give the town its own riding, the area that elects one MLA, and it elects an Orange MLA. Those 40,000 people have a seat and a voice. Now split the town into four pieces. Join each piece to a chunk of Blue countryside. In each new riding, 10,000 town voters face 30,000 rural voters. Orange loses all four. The voters are the same and so are the ballots, but the seat is gone. No single voter lost anything. What the <em>town</em> lost is the power to elect anyone. That is cracking. Its opposite is packing (Appendix C): crowd a group into as few ridings as you can, so it wins those by huge margins and nothing else.',
				p2: 'Finding 1 is about Airdrie, a city of 85,805. The commission\'s minority map splits it into four ridings, and Airdrie\'s people are outnumbered in three of them. The fourth, Airdrie East, keeps more than half the city together. That one riding is why my cracking test does not find the cracking pattern here. I count the test as added later rather than set in advance. Outside Airdrie East, the pieces do what the town\'s pieces did above. The same commission\'s other map shows that two ridings were enough to meet the law.',
				limit: '<em>What it can\'t tell you:</em> why. Cracking names what lines do to a town\'s vote. Someone may have wanted to weaken that vote, or other rules may have crowded the map. The lines alone can\'t say which.',
				back_anchor: '<a href="__BASE__/evidence#casing-1">↩ Back to finding 1 in the full record</a>'
			},
			appendix_b: {
				heading: 'Appendix B — Odd shapes, and who the remote-riding exception is for',
				confusion: '<em>The question:</em> "All ridings look strange. Why do these three shapes matter?"',
				p1: 'One riding on the commission\'s minority map runs its line out through a national park, across land where almost no one lives. Lumpy shapes are normal, because ridings follow rivers, roads and town lines. What I look for is a line doing a job no ordinary rule explains, such as a narrow strip that pulls one neighbourhood into a distant riding, or an arm that reaches into the edge of a city. The park line matters because of a special rule. Section 15(2) of Alberta\'s law, the remote-riding exception, lets up to four ridings have far fewer people than usual. Past commissions have described it as being for remote ridings that are huge and thinly settled, most of them in the north. The commission\'s majority, the chair among them, charged that the park line was drawn in bad faith, to make the riding qualify: a rule written for people who live far apart, used to protect a line where almost no one lives. My check undercuts that charge. The riding qualifies even without the extension.',
				p2: 'The three shapes in finding 2 were flagged by the commission\'s own majority. Tests with no stake in that fight confirm that the shapes are odd. They also undercut the motive the majority charged.',
				limit: '<em>What it can\'t tell you:</em> a strange shape only asks a question. One of these shapes has a real logic behind it that deserves credit: the Banff townsite is placed with Canmore. The townsite\'s placement does not touch the majority\'s objection, which was aimed at the line through the empty park. That objection still stands.',
				back_anchor: '<a href="__BASE__/evidence#casing-2">↩ Back to finding 2 in the full record</a>'
			},
			appendix_c: {
				heading: 'Appendix C — Packing, or how the side with more votes can win fewer seats',
				confusion: '<em>The question:</em> "Bigger ridings have more voters. So what? Everyone still gets one vote."',
				p1: 'Everyone does. But the size of a riding is a clue to how its votes are grouped. Take 12,000 voters, 7,000 Orange and 5,000 Blue, in three ridings of 4,000 each. Mixed evenly, Orange wins all three. Now redraw. One riding gets 4,000 Orange voters, and Orange wins it 100 to 0. The other 3,000 Orange voters are spread over the two ridings left, and Blue\'s 5,000 voters now win both. It is the same 12,000 voters, and Orange still has more of them. Now it holds one seat and Blue holds two. That is packing. One side\'s votes get piled up where they win by far more than they need, and the extra votes are wasted. The sign to look for is <em>size and depth</em>: one side\'s ridings run big and safe, while the other side\'s run lean and close.',
				p2: 'In finding 3\'s zone of Calgary, the north-east and centre, the commission\'s minority map has seventeen ridings, and they average 11.5% more people than the provincial average. The majority\'s ridings in the same zone, drawn in the same room, average 2.8% more. That is the size half of the pattern. The depth half is missing. On 2023\'s votes the NDP wins eight of the seventeen, by margins below the provincial average, so my packing test does not find packing.',
				limit: '<em>What it can\'t tell you:</em> big ridings can also come from honest guesses about growth, or from keeping a community whole. Packing leaves ridings of uneven size. So do several innocent choices.',
				back_anchor: '<a href="__BASE__/evidence#casing-3">↩ Back to finding 3 in the full record</a>'
			},
			appendix_d: {
				heading: 'Appendix D — MAD: how far ridings stray from equal, and how far the law lets them',
				confusion: '<em>The question:</em> "Population mean absolute deviation? Is that just a fancy way to say the ridings aren\'t identical?"',
				p1: 'Nearly. Towns don\'t come in riding-sized pieces, so ridings can\'t all hold exactly the same number of people. The mean absolute deviation, or MAD, measures one plain thing: on average, how far each riding is from an equal share. On the commission\'s own population tables, the majority map\'s MAD is 3,180, so its ridings miss an equal share by about 3,180 people on average. The minority map\'s MAD is 4,707. Its misses are about half again as large. The law lets ridings differ by up to 25% above or below the average, because keeping real communities whole is worth some inequality. Think of that range as a budget. A map spends some of the equal share to keep towns whole and lines sensible. The minority map spends 48% more of that budget than the majority, as finding 4 shows. On 2021 census counts, the two maps\' average misses come out almost the same. And finding 1 shows the minority map <em>didn\'t</em> spend it on keeping Airdrie whole.',
				p2: 'Back in finding 4, the two maps sit side by side on the one thing the Act puts a number on, and the minority\'s ridings stray further from an equal share. The finding also sets both against computer-drawn maps, drawn without seeing a single vote (Appendix F). Against those held to 12.5% above or below the average, the minority\'s spread, measured at the middle riding, is wider than 99 of every 100. Against those allowed the law\'s full 25%, both commission maps are more equal than almost all of them.',
				limit: '<em>What it can\'t tell you:</em> which map the law prefers. The law ranks nothing inside the range, and every riding on both maps is within the law. "Spent more of the budget" is a note about priorities. It is not a breach.',
				back_anchor: '<a href="__BASE__/evidence#casing-4">↩ Back to finding 4 in the full record</a>'
			},
			appendix_e: {
				heading: 'Appendix E — Knowing your riding without a map',
				confusion: '<em>The question:</em> "Why count how often a riding\'s line follows a city or town line?"',
				p1: 'Because those are the lines people already know. When your riding\'s line runs along your town\'s line, you can tell which riding you are in without a map. The election line matches the tax line and the ward line there, and often the school line too. The test measures how much of each map\'s riding lines run within 500 metres of a town or city line, using Statistics Canada\'s boundaries. The 2019 map, drawn by the last commission and in use today, scores 75%. The commission\'s majority map scores 80%, and the minority map 72%. Both are close to the 2019 map.',
				p2: 'On finding 5\'s test, the two maps can\'t be told apart. Both follow town and city lines at an ordinary rate, close to the 2019 map\'s.',
				limit: '<em>What it can\'t tell you:</em> following town lines is a custom that no rule requires. The Act sets no minimum. And a riding can leave a town line for a good reason, such as a suburb that has grown past a city limit.',
				back_anchor: '<a href="__BASE__/evidence#casing-5">↩ Back to finding 5 in the full record</a>'
			},
			appendix_f: {
				heading: 'Appendix F — Reading a percentile among computer-drawn maps',
				confusion: '<em>The question:</em> "A million computer maps? A percentile of a simulation? What does that even mean?"',
				p1: 'At a checkup, a child\'s height is ranked against a chart of other children the same age. A map can be ranked in a similar way. You can\'t tell if it is unusual without knowing what usual looks like, and with electoral maps nobody ever sees the other maps that could have been drawn. So I made them. A computer program starts from a valid map. Then it makes a long chain of small random changes, each one valid. It joins two neighbouring ridings, then splits them again a different way. It repeats that 252,500 times, in four separate chains, for 1,010,000 maps in all. The program never sees a vote while it draws. It can\'t favour anyone because it can\'t see anyone. That is all "neutral" means here. Then I take the real map, score it, and count how many of the 1,010,000 computer-drawn maps score this high. If 500,000 do, the real map is ordinary. If 69 do, neutral drawing turns out a map that scores this high 69 times in 1,010,000 tries. That is a percentile: where a map ranks among the computer-drawn maps, the way the child ranks on the chart. One caution. Each map in a chain is a small change from the one before, so maps next to each other are near-copies. The 1,010,000 maps are worth about 1,000 truly separate maps (roughly 900 to 1,300, depending on the measure). So the exact rank is less precise than it looks.',
				p2: 'Finding 6 runs the 50-50 test. It splits the vote exactly in half, counting 2023 election-day ballots, and counts the UCP\'s seats on each map. The commission\'s majority map sits at the 78th percentile, an ordinary result. The minority map sits at the 99.99th percentile, further out than all but about 1 in 10,000. Only 69 of the 1,010,000 maps give the UCP more seats than it does.',
				limit: '<em>What it can\'t tell you:</em> the computer-drawn maps keep each riding near the same population and in one piece. They do not weigh every fine point of the Act that a real commission weighs. So a percentile measures how far a map is from <em>neutral drawing</em>. It does not measure how far the map is from <em>every map a lawful commission might draw</em>. It is a distance, and it rules on nothing. Nor does it claim that real ridings are drawn at random. The computer-drawn maps are only what a real map is compared with.',
				back_anchor: '<a href="__BASE__/evidence#casing-6">↩ Back to finding 6 in the full record</a>'
			},
			appendix_g: {
				heading: 'Appendix G — The efficiency gap, counted in wasted votes',
				confusion: '<em>The question:</em> "One number that captures gerrymandering? That sounds too easy."',
				p1: 'It is, a little. That is why this audit set a line for it in advance, and why its miss is reported. Start with one riding of 100 votes, which Orange wins 90 to 10. Orange needed 51, so 39 of its votes did no work. Blue\'s 10 all went to the loser. Votes like these are called "wasted": every vote for a loser, plus a winner\'s votes beyond the 50% plus one it needed. On a fair map both parties waste about the same number. The efficiency gap is the difference between the two parties\' wasted votes, as a share of all votes. Packed and cracked maps make one party waste more, riding after riding. On this site a positive gap favours the UCP. My line for Alberta is about +4.1%. Only 5% of the 1,010,000 computer-drawn maps go past it.',
				p2: 'Finding 7 reports the miss. Counting 2023 election-day ballots, the commission\'s minority map has a gap of +4.0%, at the 94.5th percentile. My line, a rule I wrote down in advance, is the 95th percentile. The map falls below it, so it is reported as a miss. The all-ballots score is given in finding 7.',
				limit: '<em>What it can\'t tell you:</em> the efficiency gap squeezes a whole map into one number. One number can\'t tell a gerrymander from lumpy geography. That is why this audit uses four measures and a line fixed in advance. And it keeps the miss on the record.',
				back_anchor: '<a href="__BASE__/evidence#casing-7">↩ Back to finding 7 in the full record</a>'
			},
			appendix_h: {
				heading: 'Appendix H — The prosecutor\'s fallacy, in plain words',
				confusion: '<em>The question:</em> "A one in 570,000 chance that this map is innocent. That\'s the finding, right?"',
				p1: 'No. A DNA match shows why. A suspect matches a DNA profile found at a crime scene, and one person in a million has that profile. That can sound like a one in a million chance he\'s innocent. It isn\'t. In a city of ten million, about ten people match. On the DNA alone, the suspect is one of ten. That is a 90% chance that <em>someone else</em> is the source. How rare the evidence is, if he is innocent, is not the chance he is innocent. You also need to know how many innocent ways the evidence could come about. The difference between those two, how rare the evidence is and how likely innocence is, matters so much that it has a name. Mixing them up is the prosecutor\'s fallacy. The audit\'s number invites the same mix-up. <em>If</em> neutral drawing made Alberta\'s map, a map like the commission\'s minority map would turn up somewhere between about once in 20,000 tries and once in 570,000, counting 2023 election-day ballots. The range depends on how the statistical model is set up. The computer-drawn maps reach that far out rarely or never, so the figure comes from the model, not a count. It is a model estimate, not a bound. Like the DNA figure, it is the chance of the evidence if the map is innocent. It is not the chance the map is innocent, given the evidence.',
				p2: 'Now go back to finding 8, and read it the way you would read the DNA figure. The audit states the number it can defend: how rare the map is under neutral drawing. It refuses the swap that would turn that number into a ruling.',
				limit: '<em>What it can\'t tell you:</em> refusing the fallacy costs the audit its most quotable sentence, and that cost is deliberate. Rarity is evidence. It is not proof of intent, and it never becomes proof.',
				back_anchor: '<a href="__BASE__/evidence#casing-8">↩ Back to finding 8 in the full record</a>'
			},
			appendix_i: {
				heading: 'Appendix I — What a sampler is, and why swapping it matters',
				confusion: '<em>The question:</em> "You checked your simulation with another simulation? How is that a check?"',
				p1: 'Because the two programs are built differently. A kitchen scale that reads heavy will read heavy every time you weigh the flour on it. A scale built another way can catch the error. Every program that draws maps has quirks of its own. A result that comes from a program\'s quirks, rather than from the map, does not usually survive a change of program. The program that draws maps for a study like this is called a sampler. The standard one, ReCom, is known to lean toward compact, tidy ridings. In theory, that could make a sprawling real map look more extreme than it is. So I swapped the engine. The new one grows ridings a different way, from random "forests" instead of "trees", and it behaves differently inside. I registered it publicly (OSF he53s) before it drew any map of the run that counts. Only a 500-step software test came first. The new engine\'s random starting numbers came from a public source that anyone can check. If the minority map\'s far-out position came from the first engine\'s quirks, the second engine would move it. It moved by less than one percentile point on every measure. That meets the rule I set in advance for calling the result robust. But the run drew far fewer usable maps than I had planned, so I read it as inconclusive at this run size. And this far out, a fraction of a point is a big change. The check shows that the map stays far out, not exactly how far. One more check could not be run at all, and I report it anyway. It would test whether the odd shapes (the corridors, the park extension) are what produce the extra seats. That needs computer-drawn maps that reach the minority map\'s seat count, and the separate 5,000-map run has none. So that claim is untested, and I do not make it.',
				p2: 'Finding 9 records the three ways I tried to knock down my own result. The engine swap pointed the same way but was too small to settle it. A second check, set out in the finding, held up. The test of the odd shapes could not be run.',
				limit: '<em>What it can\'t tell you:</em> checks like these can rule out a result made by the tools. They cannot show that anyone designed the map. A truly extreme map is truly extreme, whatever produced it.',
				back_anchor: '<a href="__BASE__/evidence#casing-9">↩ Back to finding 9 in the full record</a>'
			},
			appendix_k: {
				heading: 'Appendix K — How to check a stated reason against public data',
				confusion: '<em>The question:</em> "Commissioners are the experts. Who is an audit to grade their reasons?"',
				p1: 'Nobody special, and that\'s the point. The check needs no special access. Start with Cochrane. The commission\'s minority report says Cochrane residents "move fluidly" into Calgary. Statistics Canada\'s free journey-to-work tables show about a third of Cochrane\'s workers commute into Calgary, while about half work in Cochrane. That is a real tie. But it says nothing about Nolan Hill, the strip of Calgary that Cochrane\'s riding reaches into. The report also says rural residents "go to school" in the city. For Red Deer and Sylvan Lake that holds in part. The two have different public school divisions, but one Catholic division serves both. And 54% of Sylvan Lake\'s workers who leave town to work go to Red Deer. Each check follows the same recipe. Take the stated reason. Find the public data that would show it. Then ask whether the <em>particular line drawn</em> is the line the data supports. I checked six reasons, and the count depends on the rule. Judged on the grounds the minority stated, none is contradicted, and four are supported only in part. On a separate test of whether population forced the line, four of the lines were not forced. The tie is real. The line is not the one the tie points to.',
				limit: '<em>What it can\'t tell you:</em> a reason that fails the check shows that the <em>stated</em> reason doesn\'t fit. It can\'t reveal the real one. Carelessness and a pretext leave the same paperwork.',
				back_anchor: '<a href="__BASE__/evidence#casing-11">↩ Back to finding 11 in the full record</a>'
			},
			appendix_l: {
				heading: 'Appendix L — How commissioners are chosen, and what a nomination tells you',
				confusion: '<em>The question:</em> "The commissioners the government nominated drew the map that favours the government. Case closed, surely?"',
				p1: 'Not closed. The Premier did nominate the two members who wrote the minority report (Legislative Assembly of Alberta, notice of March 28, 2025), and their map is the one that sits far outside the range of the computer-drawn maps. That link is real and worth recording. It is also exactly where the reasoning must stop. A nominee is not an agent. Nothing in this audit\'s record shows that the government directed its nominees, worked with them, or even knew the shape of their map before it was filed. Nominations are how the room is built. Alberta\'s commission has a chair, plus members nominated by the government side and the opposition side. The design expects partisan views and balances them. It bets that a mixed room will settle on one map it can defend. From 1995 to 2017 the bet paid. Even when a member dissented, each commission sent the Assembly one map. This time the room split along the lines of who nominated whom. The committee is the group of MLAs who oversaw the new map. At its October 28 meeting, the Opposition Leader alleged that maps presented at the commission\'s hearings "were created by the government" and matched the style of the minority\'s maps (committee transcript, p. CEB-71). That is an allegation, and I have not checked it. History is full of nominees who let down the people who nominated them. The link raises a question. It can\'t answer it. My tests also cut against the majority, where the data went that way. That is what measuring both sides the same way means.',
				p2: 'Now go back to finding 12. The split is what stands out there. Who nominated whom stays a question mark, and the finding treats it as one.',
				limit: '<em>What it can\'t tell you:</em> who made an appointment is context, never proof. Treating it as proof is the same mistake as in Appendix H, dressed in political clothes.',
				back_anchor: '<a href="__BASE__/evidence#casing-12">↩ Back to finding 12 in the full record</a>'
			},
			appendix_m: {
				heading: 'Appendix M — How the Act works, from commission to committee',
				confusion: '<em>The question:</em> "How can the Legislature just take over the redraw? Isn\'t the commission\'s map the map?"',
				p1: 'No. This is the surprise the whole story rests on. Under Alberta\'s <em>Electoral Boundaries Commission Act</em>, the commission proposes and only the Assembly, Alberta\'s elected MLAs, decides. The commission\'s final report is advice, hearings and all. It has no legal effect until the Assembly passes a map into law. And the Act puts no limits on what the Assembly does instead. There is no minimum debate and no notice period. There is no duty to prefer the commission\'s work, and no duty to hold hearings in whatever process comes next. Nothing in the Act stops the Assembly from sending the work elsewhere. On April 21, 2026, Government Motion 37 did just that. It created the committee: six MLAs, four UCP and two NDP. Recommendation 5 had itself proposed an all-party committee of MLAs, for a fix to two seats. Motion 37 used that kind of committee for a much wider redraw. Because the committee is made of MLAs, the decision left independent hands. The panel, an advisory panel the committee appointed, drew the new map. The committee sent it to the Assembly on November 2, 2026. Two days later the Assembly voted 45 to 36 to concur in it and to urge the government to introduce a bill. It becomes law only when a bill passes. As I read the Act, nothing in it forbids any of this, and no court has ruled on it. In every cycle since 1995, the Assembly left the commissions\' lines alone, changing at most a few names. That restraint kept politicians\' hands off the pen. The Act did not: it lets the Assembly pass a map "with alterations". In 1992 there was no single commission report to honour: the commission deadlocked, with five members filing five reports, and a committee of MLAs drew the map. The Law page tells that story.',
				p2: 'Now go back to finding 13. The commission held hearings in sixteen communities. The body that replaced it did not have to hold any, and held none on the map. As I read the Act, none of that is forbidden either.',
				limit: '<em>What it can\'t tell you:</em> this explainer says what the law allows. Whether Albertans should accept what the law allows is a political question. The November tests on the main page are built to inform it.',
				back_anchor: '<a href="__BASE__/evidence#casing-13">↩ Back to finding 13 in the full record</a>'
			},
			appendix_n: {
				heading: 'Appendix N — Conventions and law, and how a custom wears away',
				confusion: '<em>The question:</em> "If politicians drawing their own ridings breaks our deepest election custom, how can it be legal?"',
				p1: 'Because Canada\'s constitution runs on two kinds of rules, and only one of them is law. The other works more like a lineup. No law makes you wait your turn, yet people do, and they notice who doesn\'t. Law is written down, and a court can rule on it and enforce it. A convention is an unwritten rule of political conduct. It binds in practice, but no court enforces it. The Supreme Court set out the difference in the 1981 Patriation Reference. A court may <em>recognize</em> a convention and still refuse to <em>enforce</em> it. Conventions are policed by politics: by the opposition, the press and voters. In Alberta, an independent commission\'s map sits on the convention side. About sixty years of practice, first federally and then province by province, built the rule that politicians do not draw their own ridings. In Quebec a commission\'s map normally takes effect without the National Assembly\'s final approval, though in June 2026 the Assembly passed a map of its own. In Alberta, as in most provinces, it takes a bill. Alberta\'s Act does not make the rule binding. So here the rule\'s whole strength was that governments kept choosing to follow it. A custom set aside once, at no cost, is weaker for every government that follows. Of any party.',
				p2: 'Now go back to finding 14, which finds three things at once. The break from long practice is documented, and the opposition calls it a violation. No court will enforce the convention. And a court can still review the map that the process produces, once it becomes law.',
				limit: '<em>What it can\'t tell you:</em> "a court won\'t enforce it" is a statement about courts, not about consequences. Conventions are enforced at elections, by people who know what was done. Reports like this one exist so that they know.',
				back_anchor: '<a href="__BASE__/evidence#casing-14">↩ Back to finding 14 in the full record</a>'
			},
			footer_note: 'These explainers match the appendices of the <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/public/report_public.md" rel="noopener">full public report</a>.'
		},
		methods: {
			head_title: 'How I Checked the Maps · Alberta Electoral Boundary Audit',
			head_description: 'Every test and number in the audit, explained in plain words: the 1,010,000 computer-drawn maps, the structural tests, the four fairness measures, the odds, the tests that failed, and the words used on this site.',
			back: '← Back to audit',
			site_label: 'Alberta Electoral Boundary Audit',
			h1: 'How I Checked the Maps',
			meta: 'Every test and every number, in plain words · Every number can be rerun from the public repository',
			standfirst: 'To tell whether a map is unusual, you need something to measure it against. I use 1,010,000 maps a computer drew without ever seeing a vote, and I check where each real map lands among them. That simple idea sits under the audit\'s main result, and this page explains every test behind the audit in plain words. There are no formulas here. If you can read a weather forecast, you can read this.',
			toc: {
				aria: 'Page contents',
				what_if: 'The computer-drawn maps',
				percentile: 'How to read a percentile',
				structural: 'The five structural tests',
				fairness: 'The four fairness measures',
				odds: 'What the odds mean',
				died: 'The tests that failed',
				break: 'Trying to knock down my own result',
				prereg: 'Promises made in advance',
				reproduce: 'Run it yourself',
				ballots: 'Election-day ballots and all ballots',
				november: 'The tests on the panel\'s map',
				words: 'Words used on this site'
			},
			what_if: {
				heading: '1,010,000 computer-drawn maps',
				p1: 'The computer\'s building blocks are the same 4,765 voting areas the real maps use. From them it drew <strong>1,010,000 Alberta maps</strong>, each with 87 ridings, the number on the 2019 map. Every one follows the two hard rules the commission followed. Each riding holds close to the same number of people: within 25% of the average, and each drawing step aims for 12.5%. And each riding is one connected piece.',
				p2: 'To draw them I used ReCom, the standard tool in this field. It works one small step at a time. It picks two ridings that share a border and merges them into one. Then it splits that area into two new legal ridings, at random. It does this 1,010,000 times, saving the map after each step.',
				p3: 'One fact matters most: <strong>the computer never sees a vote.</strong> It does not know where UCP or NDP voters live. That is the only sense in which this site calls these maps neutral. So if a computer-drawn map still leans one way, the lean comes from where Albertans live and from the two rules. If a real map leans much further than nearly all of them, geography and the rules alone become a poor explanation.',
				p4: 'Four things tell you how far to trust these maps:',
				li1: 'Anyone can recompute the seed, the starting number behind every random choice the computer made. <strong>The random numbers came from a public source.</strong> The seed joins a published value from a public randomness beacon (drand, run by the League of Entropy, a group that includes Cloudflare) with a fixed label. The beacon value (round 5,500,000) was public in October 2025, so it cannot date the seed. I fixed the label in the code on April 27, 2026, before the official map files arrived on May 6. The record of that is a commit in the project\'s repository, not an OSF registration. On May 12, 2026, I rewrote the repository\'s history to remove personal information, so the date on that commit is not third-party evidence.',
				li2: 'The maps came from four separate runs, each with its own start. <strong>All four settled on the same picture.</strong> The big count is less than it looks, though. Each map is only one small step from the one before, so the maps are not all independent of each other. Together they are worth about 1,000 independent maps (roughly 900 to 1,300, depending on the measure).',
				li3: '<strong>Not every map has 87 ridings.</strong> The commission\'s two maps have 89 ridings each. The computer-drawn maps have 87, the size of the 2019 map, the last one passed into law. The panel\'s map has 91. So this site gives seats as <em>shares</em>, which lets the three sizes sit side by side. The fit is close, not exact. Where a comparison crosses sizes, I label it. I also check it against computer-drawn maps of the same size, and those same-size results are provisional.',
				li4: 'Real commission maps are tidier than most computer-drawn maps. The computer follows the two hard rules, but not every softer rule a real commission weighs, like keeping communities together. <strong>So these maps are not a perfect referee</strong>, and I name this limit wherever their numbers appear.'
			},
			percentile: {
				heading: 'How to read a percentile',
				p1: 'Line up all 1,010,000 computer-drawn maps, from the one that leans least toward the UCP to the one that leans most. Then place a real map in the line. Its <strong>percentile</strong> is its place in that line. The 78th percentile means it leans further than 78 of every 100 computer-drawn maps. That is ordinary: a bit above the middle.',
				p2: 'Near the far end of that line sits the commission minority\'s map. Split the vote 50-50, and it gives the UCP more seats than all but <strong>69 of the 1,010,000</strong>. That is the 99.99th percentile. A map there leans further than all but about 1 in 10,000 computer-drawn maps.'
			},
			structural: {
				heading: 'The five structural tests (no votes needed)',
				p1: 'Some things about a map show in its lines alone, with no votes and no computer-drawn maps. I measured those with five structural tests. Each one compares the two commission maps directly.',
				li1: '<strong>1. Population spread.</strong> On the commission\'s own tables, the majority map\'s ridings miss the ideal size by 3,180 people on average. The minority map\'s miss by 4,707, about half again as much. A bigger miss means votes count less equally. On 2021 census counts, though, the three maps\' average miss comes out almost the same.',
				li2: '<strong>2. Crowding in Calgary.</strong> In north-east and central Calgary, the minority map\'s ridings hold 11.5% more people than the provincial average. The majority map\'s hold 2.8% more. (On a literal reading of the zone\'s stated geographic rule, the minority map\'s figure is 8.5% to 8.9% and the majority map\'s is 1.3% to 1.6%.) In a bigger riding, each vote weighs less. Crowding one party\'s voters into fewer, bigger ridings is called <em>packing</em>. I tested for it here, and my packing test does not detect it: on 2023\'s votes the NDP wins eight of the zone\'s seventeen ridings, by margins below the provincial average.',
				li3: '<strong>3. The Airdrie split.</strong> The minority map splits Airdrie into four pieces, three of them holding at least 2% of its people, and joins each piece to different land outside the city. The law makes Airdrie hold at least two ridings, and the majority map uses two. Splitting a community thin is called <em>cracking</em>. The minority map\'s split crosses this test\'s line. It does not cross my separate cracking test, which is exploratory: Airdrie East keeps more than half the city together, and nine in ten of its people live in Airdrie.',
				li4: '<strong>4. The chair\'s flags.</strong> The commission\'s majority, the chair among them, called some boundaries geographically odd in its report. Four of those flags fall on the minority map. None fall on the majority map. I ran the four through my own geometry check, and it confirmed three.',
				li5: '<strong>5. Following city and town lines.</strong> Both maps follow them about as often as the 2019 map does, which is 75% (the majority 80%, the minority 72%). So this test cannot tell the maps apart. It failed, and it stays on the page.',
				p2: 'The majority map cannot fail four of these five tests, because those four measure the minority map against it. The other one, the Airdrie split, is measured against the legal minimum of two, which the majority map meets. The minority map differs from the majority map on four of the five. The test on city and town lines separates neither.'
			},
			fairness: {
				heading: 'The four fairness measures (votes added)',
				p1: 'The structural tests read only the lines. These four standard measures add the votes and ask how each map turns them into seats. Each one is checked against the 1,010,000 computer-drawn maps. Every figure in this section uses 2023 election-day ballots, the count these tests were first set on. The rerun on all ballots is in the section "Election-day ballots and all ballots" below.',
				li1: '<strong>1. The 50-50 test.</strong> Shift every riding\'s vote by the same amount until the province splits exactly 50-50, then count each party\'s seats. On a typical computer-drawn Alberta map, half the votes does not bring half the seats. It gives the UCP 44.8% of the seats in a tie, because the UCP\'s rural wins are wider than the NDP\'s city wins. The majority map gives the UCP 46.1%: the 78th percentile, ordinary. The 2019 map gives 46.0%: the 65th percentile (or the 78th, as first registered, if every map that ties it is counted below it). The minority map gives the UCP <strong>51.7%</strong> (46 of 89 seats). That is a majority of seats on a tied vote, and only 69 of the 1,010,000 computer-drawn maps give the UCP more. For scale, one seeded run of a method told to <em>deliberately</em> win the UCP as many seats as it could reached 52.9% (46 of 87 seats). Nothing shows that is the most possible.',
				li2: '<strong>2. The efficiency gap.</strong> Every vote either helps win a seat or is "wasted": cast for a loser, or piled onto a winner beyond what the win needed. This measure compares the two parties\' wasted votes, and a positive gap favours the UCP. The majority map scores +0.1%, close to nothing. The minority map scores +4.0%, the 94.5th percentile. I had set the line in advance at the 95th percentile, about +4.1%, so the minority map lands just <em>under</em> it. It is the one measure that did not flag, and I report it as a miss.',
				li3: '<strong>3. The mean-median gap.</strong> Compare a party\'s average riding result with its middle riding result. When the two drift apart, votes are being bunched into blowouts somewhere. The minority map\'s gap favours the UCP more than 99.97% of computer-drawn maps. This measure also turned up an outlier on the other side: the majority map\'s gap leans toward the NDP, further than 99% of them. I report that too, and I have no tested explanation for it.',
				li4: '<strong>4. Declination.</strong> This reads the winning margins: does the map treat the two parties\' wins alike, or does it bend at the 50% mark? The minority map bends further in the UCP\'s favour than 98.8% of computer-drawn maps. The majority map reads normal.',
				p2: 'Add it up. Three of the four flag the minority map, all in the same direction, toward the UCP. The fourth points the same way but stops just under the line. The majority map is ordinary on three. On the fourth, the mean-median gap, it is an outlier toward the NDP.'
			},
			odds: {
				heading: 'What the odds mean, and why I doubled them',
				p1: 'Combine the four fairness measures into one score. How often would maps drawn without votes produce a result as extreme as the minority map\'s? On the published score, none of the 1,010,000 computer-drawn maps does. With nothing to count, the answer comes from a statistical model. It is <strong>a model estimate, not a bound</strong>: not a count, and not a guaranteed limit. The model can be built several defensible ways, and the answer depends on the choice: between about <strong>1 in 20,000</strong> and <strong>1 in 570,000</strong>. On every version the map is far out at the edge. The model first published gives the top of the range. A version that allows for near-copies among the maps gives about 1 in 449,000. A rank-based version gives 1 in 238,000, and on it seven computer-drawn maps reach the minority map. Dropping one of two measures that nearly repeat each other gives 1 in 97,000. A second, smaller sampler gives 1 in 20,000. All of them use election-day ballots. There is no all-ballots version, because the neutral maps\' all-ballots scores are not in the repository. The published figure is double the model\'s raw estimate of about 1 in 1.1 million. Here is why.',
				p2: 'Looking for a signal in more than one place gives luck more than one chance. Think of lottery tickets: buy two, and your odds of holding a winner double. So before quoting the odds, I doubled them against myself. The doubling is a cautious allowance, not a correction for a stated set of tests.',
				p3: 'The doubling does not remove the model\'s own assumptions. That is why a range is given.',
				p4: 'One caution I repeat everywhere: these odds measure how unusual the <em>map</em> is. They are not the odds that anyone meant to tilt it. A rare map could still, in principle, be honest work. The odds say only this: drawing without votes almost never produces this map.'
			},
			died: {
				heading: 'The tests that failed',
				p1: 'Some of my tests came back empty. They are listed here on purpose. An audit that shows only its wins is advertising.',
				li1: '<strong>The city-limits test</strong>, the last of the structural tests, could not tell the two commission maps apart. Each follows city and town lines about as often as the 2019 map does (75%).',
				li2: '<strong>Three exploratory tests</strong> were retired as unreliable and are not used on this site. The record is in <a href="__BASE__/evidence#casing-10">finding 10</a> and the academic report.'
			},
			break: {
				heading: 'Trying to knock down my own result',
				p1: 'Before I trusted the main result, I went after it three ways, looking for a flaw. What came back was mixed, and all three are reported here.',
				li1: '<strong>Swap the engine.</strong> On July 10, 2026 I reran the four fairness measures with a different way of drawing maps, a spanning-forest sampler registered in advance on the OSF (he53s). Every percentile moved by less than one point, which meets the rule I set for calling the result robust. I don\'t claim that, though. The run fell far short of its planned size, and its margin is about two points, so at this run size I read it as inconclusive. It shows the map stays far out. It does not show exactly how far. On this engine the combined odds come to about 1 in 20,000.',
				li2: '<strong>Swap the software.</strong> I had a separate program, the redist package in the R language, draw 5,000 maps. None reached the minority map\'s value. The majority map came out higher on that smaller run, just above the 95th percentile; on the main run it sits at the 78th.',
				li3: '<strong>Test the cause.</strong> The odd shapes the structural tests found and the seat lean point at the same map. I wanted to test whether the shapes are what produce the seat advantage. That test needs computer-drawn maps that reach the minority map\'s seat count. The 5,000-map run has none, so it could not be run. At the lower cutoff I first used, only 3 maps qualify. They are slightly less compact than the rest, but 3 maps are too few to show anything. Whether the shapes cause the lean is untested.'
			},
			prereg: {
				heading: 'Promises made in advance',
				p1: 'The May 6 registration predicted that the minority map would favour the NDP and spread population less. It was built on a mistake about who nominated whom, and both predictions missed. The best defence against fooling yourself is to write your predictions down before you look, so I wrote my tests into time-stamped records, each with its line and the direction I expected. A prediction set in advance that missed stays a miss, like those two. The rules that decide the result on the panel\'s map were written down in June 2026 and are dated in the repository, not on the OSF. Three side tests, and the choice of which computer-drawn maps to compare against, were added October 29 to 31, after opposition MLAs had described parts of the map at the committee\'s October 28 meeting. Seven amendments followed on November 2 to 7, after the panel\'s report was tabled. Amendments 7 to 10 came before any of the panel\'s map was scored; 11 to 13 came after results had been seen. I also say which results were <em>set in advance</em> (pre-registered) and which were <em>added later</em> (exploratory: the seeds were locked, but the exact combination of tests was chosen later). The headline odds were added later.'
			},
			reproduce: {
				heading: 'Run it yourself',
				p1: 'You can rerun every number in my analysis yourself. Each one comes from a script in the public repository, run on committed data. The full recipe is in <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/docs/REPRODUCING.md" rel="noopener">REPRODUCING.md</a>. The short version:',
				p2: 'If you\'d rather not install anything, a notebook version runs in your browser on <a href="https://colab.research.google.com/github/Ixby/alberta-electoral-boundaries-audit/blob/master/notebooks/alberta_audit_explorer.ipynb" rel="noopener">Google Colab</a>. The full method, with every correction along the way, is in the <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">academic report</a>.',
				cross_ref: 'Related pages: <a href="__BASE__/law">What the law says</a> · <a href="__BASE__/norms">What the norms ask</a> · <a href="__BASE__/explainers">The explainers (Appendices A to N)</a>, which the findings link to.'
			},
			ballots: {
				heading: 'Election-day ballots and all ballots',
				p1: 'On the 2019 map, election-day ballots alone elect 57 UCP and 30 NDP members. All ballots elect 49 and 38, which is the real 2023 result. Those are the two counts of the 2023 vote on this site, and as the 2019 map shows, they can give different results. Each figure says which one it uses. <strong>Election-day ballots</strong> are the ones cast at a polling station on election day: 932,164 of them, 896,644 for the UCP or the NDP. Elections Alberta reports them for each voting area, so I know where they were cast. <strong>All ballots</strong> adds the early ballots: advance, mobile and special ballots, and Vote Anywhere. That makes 1,764,915 ballots, 1,706,304 of them for the UCP or the NDP. Since November 7, 2026, every vote-based test uses all ballots, with the election-day result kept beside it. That change was <strong>not blind</strong>: I made it after I had seen the all-ballots results for the panel\'s map and both commission maps.',
				p2: 'Early ballots are the hard part. Of the 1,706,304 UCP and NDP ballots, 809,660, about 47%, were not cast on election day, and Elections Alberta reports them only as a total for each old riding. Where a new line cuts through an old riding, I have to estimate which side each early ballot belongs on. So an all-ballots seat count on a new map is an estimate, and it depends on how early ballots are placed. One fact holds under any placement rule: across the province, early ballots leaned 6.2 points more NDP than election-day ballots, and more NDP in 83 of 87 ridings. The registered rule is rule P (Amendment 14, signed November 10, 2026). It is <strong>not blind</strong> either: I chose it after I had seen its effect on the maps. Rule P places early ballots only among people on the list who did not vote on election day, and lets each area keep its own election-day lean. It uses Alberta data only. On all ballots under rule P, UCP against NDP, the commission minority\'s map comes out 57-32 (efficiency gap +5.64%) and the commission majority\'s 48-41 (−2.83%). The panel\'s map, as I rebuilt it, comes out 50-41, the paragraph 167 map 50-41 and the 2019 map 49-38. On the minority\'s map, Calgary-Edgemont and Calgary-Glenmore go to the UCP by 401 and 68 modelled votes. On the panel\'s map, Banff-Canmore-Diamond Valley goes to the NDP by 1,276. No seat moves across the range of early-voter lean the Alberta data allow. That range covers only the lean, though, so it understates the real uncertainty. Against the 1,010,000 computer-drawn maps, scored the same way, the minority map\'s efficiency gap ranks at the 99.98th percentile. The majority map ranks at the 18th, the panel\'s map at the 18th and the 2019 map at the 21st. Of the 36 rescored runs, 32 drew the same maps as before; four runs from a second sampler did not, and were left out. The older rule (Amendment 12) is kept as a check. It spreads early ballots over the old riding\'s voting areas in step with each area\'s election-day votes. On it the minority\'s map is 55-34 (efficiency gap +2.55%), the majority\'s 48-41 (−2.70%), the panel\'s map 51-40, the paragraph 167 map 50-41 and the 2019 map 49-38. It also puts more early ballots in 26 polling stations than they have people who did not vote on election day. Where this site gives an all-ballots count, rule P\'s is the registered one and the older rule\'s is a check.'
			},
			words: {
				heading: 'Words used on this site'
			}
		},
		norms: {
			head_title: 'What the Norms Ask · Alberta Electoral Boundary Audit',
			head_description: 'What custom asks of Alberta\'s 2026 electoral map: the rule that MLAs do not draw their own ridings, where it came from, the best case for setting it aside, and how the process scored.',
			back: '← Back to audit',
			site_label: 'Alberta Electoral Boundary Audit',
			h1: 'What the Norms Ask of an Electoral Map',
			meta: 'A plain-language guide · Not a ruling on anyone',
			standfirst: '"The government broke a sixty-year norm" is not a measurement. It is the heart of the Opposition\'s charge. The <a href="__BASE__/law">law</a> asks what is allowed, and the <a href="__BASE__/methods">numbers</a> ask what is unusual. This page asks the third question running through the audit, and it is the one people fight over: what is customary, meaning what Canada has come to expect of how a map gets made. So I don\'t just list the norms here. I test them: where they came from, what they are for, the best case for setting them aside, and what is left once each side\'s rhetoric is cleared away.',
			the_norm: {
				heading: 'The norm: politicians don\'t draw their own ridings',
				p1: 'The person who will run in a riding does not hold the pen that draws it. That is the norm: an unwritten rule, kept by practice, not by law. Canada spent about sixty years building it. From the federal reforms of the 1960s on, Ottawa and the provinces moved the job to boundary commissions that work at arm\'s length from the politicians. There were exceptions, including Alberta in 1992 and Quebec in 2026.',
				p2: 'Governing parties once drew their own ridings as a matter of routine, and the norm exists because of that. The conflict of interest is plain. Someone who has to win under a map has every reason to draw it in their own favour, and no one watching can tell an honest line from a self-serving one. A commission doesn\'t make maps perfect. What a commission adds is distance between the person who draws the lines and the person who gains from them. That distance is what lets everyone else trust the result.'
			},
			what_it_bought: {
				heading: 'What the norm delivered this time',
				p1: 'Alberta\'s commission, which worked in 2025 and 2026, published a draft map, heard the criticism, and changed its mind. It had planned to remove the riding of Lesser Slave Lake. After many submissions (the minority report counts at least 56), it dropped the plan. That is the system answering the public where everyone can see it, and this commission shows the norm at its best. It held hearings in sixteen communities and received 1,345 written submissions, by its own count. Whatever else the commission got wrong, the process around it worked as designed. It was public and on the record, and it answered to what Albertans said.'
			},
			the_departure: {
				heading: 'The break: MLAs take over the map',
				p1: 'In March 2026 the commission split 3 to 2 and filed two maps. On April 21, 2026, the Assembly set both aside. Government Motion 37 gave the job to a committee of six MLAs: four UCP and two NDP, chaired by UCP MLA Brandon Lunty. The committee appointed an advisory panel of five, chaired by a retired Court of Appeal justice, to draw a 91-riding map. The committee did not have to hold public hearings, and it held none. The panel reported on October 22. No draft was published for the public to challenge. NDP members said the panel took no public submissions.',
				p2: 'In May, Duane Bratt, Professor of Political Science at Mount Royal University, described the move to me, in private correspondence, as without precedent in Canada. I later found one earlier case, Alberta\'s own, in 1992. I treat it as a different case, and that distinction is mine, not his. In 1992 the commission could not agree on a map, and MLAs drew one; the <a href="__BASE__/law#ebca">law page</a> tells that story in full. In 2026 a majority of the commission signed a report, which the Act treats as the commission\'s report. It was set aside anyway. What that <em>means</em> is where the argument starts.'
			},
			steel_man: {
				heading: 'The best case for setting the norm aside',
				p1: 'A check that only repeats one side\'s outrage is not checking anything. So here is the government\'s case at its strongest, put as well as I can put it, before I test it:',
				li1: '<strong>The commission failed at its one job.</strong> A commission is meant to give one answer, at arm\'s length. This one gave two maps that could not both be used, and its majority publicly accused the minority of bad faith. When the independent route splits, someone has to decide. The law says who.',
				li2: 'Under Alberta\'s Act, a commission\'s report has no legal force. Ridings change only when the Assembly passes an <em>Electoral Divisions Act</em>. Motion 37 used a door the law built, and nothing was smuggled in. <strong>The law gives the Legislature the pen, on purpose.</strong>',
				li3: 'An MLA who draws a self-serving map can be voted out. A commissioner cannot. <strong>MLAs answer to voters; commissioners answer to no one.</strong> Accountability is the oldest argument for letting the Legislature control the map.',
				li4: '<strong>Two of the committee\'s six members are NDP MLAs</strong>, so the committee is not purely partisan. An advisory panel drew the map. A retired Court of Appeal justice chaired that panel, and two of its members were nominated by the Opposition. The panel split too: its report includes a minority opinion.',
				li5: 'The government\'s stated reason for giving the committee a 91-seat job was Recommendation 5, <strong>written by the commission\'s chair himself</strong>. That recommendation says its change “would need to be studied by an all-party Select Special Committee or other equivalent Legislative Committee” (p. 66). And the government told the Legislature exactly that: “We are adopting the recommendations from the report” (Government House Leader, Hansard, April 16, 2026).'
			},
			where_it_bends: {
				heading: 'Where that case gives way',
				p1: 'Each of those points is real. The record also pushes back on each one:',
				li1: 'The split explains <em>replacing</em> the maps. It does not explain <em>shutting out the public</em>. Recommendation 5 proposed an all-party committee to study a two-seat fix. Motion 37 used that kind of committee for a much wider redraw. A rule requiring hearings, a published draft, or a panel whose map was final would also have settled the split. The route chosen gives up every openness safeguard that studies comparing countries treat as protective. The split forced none of those losses.',
				li2: '"The law allows it" is a question for the law page, and it is answered there: the Act sets no rule for what the Assembly does if it does not approve a commission\'s report. The norms question is different. In Quebec a commission\'s map takes effect without the National Assembly\'s final approval. In Alberta, as in most provinces, it takes a bill, so the governing party always controls whether any commission map becomes law. What is lawful and what is customary are different questions.',
				li3: 'The accountability argument proves too much. It is an argument against boundary commissions everywhere. Yet Canada, the UK and Australia moved the other way, with rare exceptions such as Alberta in 1992 and Quebec in 2026. They did so because elections are weak protection against a map designed to shape those same elections.',
				li4: 'The panel drafts. A committee with a government majority reviews the draft and sends it on. The Assembly\'s majority decides. Advice from both sides, with the decision in the government\'s hands, is a different thing from an independent commission. That difference is the norm at issue.',
				li5: 'The chair wrote Recommendation 5 to talk the Legislature out of adopting the minority map, and his majority colleagues did not endorse it. It is also narrow. It leaves Airdrie, Calgary and everything south of them as the majority drew them, except Drumheller-Stettler. Those are the very lines the commission split over, and nothing in the committee\'s mandate held it to them. Citing a recommendation against its author\'s stated purpose leaves a tension on the record. It does not resolve it.',
				li6: 'The government also read page 58 of the majority report into the record. That page regrets the cap on the number of seats. But the remedy it proposes is for the Legislature to let <em>future commissions</em> set the number of seats. Motion 37 took that freedom in this cycle, for a committee of MLAs, while turning down the report\'s actual request: adopt the 89-seat map.'
			},
			whose_accusation: {
				heading: 'Whose charge is it?',
				p1: 'This page exists to separate fact from judgment. First, the documented facts. The break happened. I found no earlier case of a commission\'s majority report being set aside; Alberta\'s 1992 committee followed a commission with no majority. The openness safeguards were given up. In a public report the law requires, the commission\'s majority called one minority boundary a "bad faith effort". That is the majority\'s charge, and my own check undercuts it (finding 2 in the full record). The Canadian Civil Liberties Association publicly <a href="https://ccla.org/press-release/ccla-sounds-the-alarm-over-the-politicization-of-albertas-electoral-map/" rel="noopener">raised the concern that the map was being politicized</a>. The Opposition voted against the motion. And the charges run both ways. The minority report charges “the Majority’s inclination to delete or mangle rural electoral divisions and, in effect, reduce effective rural representation”. Rural representation, in the minority\'s own words, is “not merely a question of numbers; it is a question of access, voice, and practical governability” (p. 356). I tested that charge the day I found it. The test wasn\'t set in advance; I added it later, and its method and every riding\'s label are published with the finding. It came back the other way. The minority map keeps fewer ridings centred on rural areas than the majority map does: 23 against 28, where the 2019 map has 31. It also folds more of the 2019 map\'s rural ridings into ridings named for cities, seven against three. Both maps thin rural representation compared with 2019, so the charge\'s core observation is real. On the measure the charge names, though, it lands on its author. The companion charge, tested the same day, holds up. It says the majority would not use the Act\'s room to let a riding sit up to 25% below or above the average population, room that could give rural ridings fewer people. The majority drew its rural ridings near the average. The minority drew them with fewer people. So one charge reversed and the other held, and both results are published. I discount the majority\'s complaints about the minority map because they come from one side of a split commission. The same discount applies here, in both directions.',
				p2: 'What follows is <em>not</em> a documented fact. It is a political judgment: that the break was illegitimate. That judgment turns on how much respect the norm deserved once the commission had split, and reasonable people weigh that differently. I document the break and what it cost. I do not adopt the Opposition\'s conclusion, and nothing in the audit\'s statistics can carry it either. A number can say a map is rare. It cannot say a process was wrong.'
			},
			norms_vs_law: {
				heading: 'Norms are not law. Quebec wrote this one into law.',
				p1: 'Could a court enforce the norm? Not while it stays a norm. Unwritten rules of political conduct, which lawyers call constitutional conventions, bind politicians, not courts. The Supreme Court said so in the 1981 Patriation Reference, and courts have held that line since: a court may name a convention and still decline to enforce it. That gap, between what is customary and what a court can order, is where this whole episode lives.',
				p2: 'Quebec shows the other choice. It wrote the norm into law: its boundary commission is permanent and independent. When Quebec\'s government passed a law to pause its commission, the courts <em>did</em> act, because a law was then in play. On April 22, 2026, the Supreme Court of Canada upheld, 7 to 2 and ruling from the bench, the finding that the pause broke the voting rights in section 3 of the Charter. Its reasons followed on May 1 (<em>Quebec (AG) v. Lalande</em>, 2026 SCC 13). Where the norm was written into law, a court could enforce it. Alberta\'s norm was never written into law, so no court can enforce it as a norm. A court can still review a boundaries law once one passes. The contrast cuts both ways, though. Even in Quebec, on June 12, 2026, the National Assembly passed a law setting its own 127-seat map.'
			},
			measurable: {
				heading: 'The process scorecard: putting the norms question to a test',
				p1: 'Talk about norms is cheap on both sides. My answer is a third scorecard. It turns the norms debate from a shouting match about tradition into a scored comparison: did the committee act like the institution it replaced? The tests and statistics elsewhere on this site measure the maps. This scorecard measures the <em>process</em>, on nine safeguards that the sixty-year practice provided. Each is a yes-or-no question that public documents can answer, and the same nine score every process this audit examines.',
				table: {
					head: {
						feature: 'Safeguard',
						commission: 'The commission\'s process',
						committee: 'The committee\'s process (as set up)'
					},
					arms_length_drafting: {
						feature: 'Drawn at arm\'s length from MLAs',
						commission: 'Yes',
						committee: 'Partly: the panel draws; a committee with a government majority reviews the map and sends it on; the Assembly decides'
					},
					public_hearings_before: {
						feature: 'Public hearings before the map is adopted',
						commission: 'Yes: in sixteen communities',
						committee: 'No: none held on the map'
					},
					draft_published_challenge: {
						feature: 'A draft published for the public to challenge',
						commission: 'Yes: a draft map, revised in public',
						committee: 'No: none published'
					},
					new_public_submissions: {
						feature: 'New public submissions accepted',
						commission: 'Yes: 1,345 received, by the commission\'s count',
						committee: 'No: none taken; the panel had access to the commission\'s archive'
					},
					demonstrated_responsiveness: {
						feature: 'Shown to respond to the public',
						commission: 'Yes: changed its plan after many submissions (at least 56, by the minority report\'s count)',
						committee: 'No: ruled out by design, with no hearings, no draft and no new submissions'
					},
					neutral_chair_deciding: {
						feature: 'A neutral chair for the body that decides',
						commission: 'Yes: a judge, appointed by cabinet',
						committee: 'No: a government MLA chairs the committee that reviews the map, and the Assembly\'s majority decides; the retired judge chairs only the panel'
					},
					opposition_deciding_body: {
						feature: 'The Opposition in the body that decides',
						commission: 'Yes: two of five members nominated by the Opposition',
						committee: 'Yes: two of six members are NDP MLAs'
					},
					published_reasons_contested: {
						feature: 'Published reasons for disputed choices',
						commission: 'Yes: both reports',
						committee: 'Yes: the panel\'s report gives reasons for each change'
					},
					precedent_conformity: {
						feature: 'Follows precedent',
						commission: 'Yes',
						committee: 'No: I found no earlier case of a commission\'s majority report being set aside; Alberta\'s 1992 committee followed a commission that could not agree'
					},
					count: {
						feature: 'Total',
						commission: '9 of 9 (by design)',
						committee: '2 Yes · 1 Partly · 6 No'
					}
				},
				p2: 'The panel\'s map is the first in the audit with a different process score behind it. The audit\'s chart places each map on two dimensions: how its lines are drawn, and how it turns votes into seats. This scorecard adds a third. All three maps on that chart so far (the commission\'s majority and minority maps and the 2019 map) came from commission processes, which score nine of nine here by design, so the third dimension has had nothing to tell apart.',
				p3: 'Read the table fairly, in both directions. The commission scores nine of nine <em>by design</em>. The safeguards describe the institution the norm built, and the commission was that institution. The telling part was up to the committee. Four of its No answers were safeguards it could have added before it reported: hearings, a published draft, new submissions, and the response to the public that those make possible. It added none of them. It ended its review on October 28 and held no further meetings.',
				draft_note: 'The scorecard\'s safeguards, sources and expected directions were <a href="https://osf.io/u47bq/" rel="noopener">registered on the OSF (u47bq, July 14, 2026)</a>, a public site that dates and freezes a research plan. That was months before the committee reported. But I wrote the scorecard partway through the episode, after the findings you have just read. That is a risk of bias, and the <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/preregistration/lane3_process_scorecard_draft.md" rel="noopener">registered document</a> says so openly. Signed corrections (Amendment 5, Part 25, November 1, before any committee map was seen) fix some of its facts, such as the committee\'s size. They change no safeguard and no result, and the OSF text is unchanged. Applied backward to the commission, the scorecard describes; it does not predict. With the panel\'s map tabled, the map tests run as written in June and amended in November, and this scorecard rates the process that produced the map.'
			},
			audits_standing_rule: {
				heading: "The audit's standing rule",
				p1: 'The same rule holds everywhere on this site. The audit records what happened and how rare it is, and it notes who claimed what. Whether the norm deserved to survive the split is for readers and voters to decide, and so is what setting it aside should cost at the ballot box, if anything. A statistical audit doesn\'t get a vote.',
				cross_ref: 'Related pages: <a href="__BASE__/law">What the law says</a> · <a href="__BASE__/methods">How I checked</a>',
				disclaimer: 'This page is a plain-language guide to the audit. It is not legal advice, and it is not a ruling on any person or party.'
			}
		},
		law: {
			head_title: 'What the Law Asks · Alberta Electoral Boundary Audit',
			head_description: 'What Canadian law asks of an electoral map, as this audit understands it: the Charter\'s right to effective representation, Alberta\'s Electoral Boundaries Commission Act, and where the audit\'s evidence fits.',
			back: '← Back to audit',
			site_label: 'Alberta Electoral Boundary Audit',
			h1: 'What the Law Says About Alberta\'s Riding Maps',
			meta: 'A plain-language guide · Not legal advice',
			standfirst: 'An electoral map divides the province into ridings, and each riding elects one MLA. This audit measures maps. Courts judge them, and I keep the two jobs apart. This page sets out what Canadian law asks of a map, as I understand it, and where my evidence fits. The audit itself takes no position on any legal conclusion. It reports what the data show, and it stops there.',
			why_not_gerrymander: {
				heading: 'Why the audit never calls a map a gerrymander',
				p1: 'On this site, "gerrymandering" has its everyday meaning: drawing lines to give a party an advantage. As I understand Canadian law, the word has no legal definition. No law forbids "gerrymandering" by name, and no court test uses the word. So a court cannot find a map guilty of it. That is one reason the audit never calls any map a gerrymander, whatever the numbers show.',
				p2: 'Most of the statistical tools I used come from American court fights. The efficiency gap, which compares the votes each party wastes, is one. Another is a large set of computer-drawn maps to compare a real map against. In the United States, partisan gerrymandering is at least a named legal claim. But in <em>Rucho v. Common Cause</em>, 588 U.S. 684 (2019), the US Supreme Court closed the federal courts to it. Federal judges, it held, have no clear, workable standard for judging such claims. Some US state courts still use the same measures. The best-known case is <em>League of Women Voters v. Commonwealth</em>, 178 A.3d 737 (Pa. 2018).',
				p3: 'Canada took a different path. Instead of a gerrymandering test, Canadian law asks two questions a court can answer. Does the map give voters <a href="#effective-representation">effective representation</a> under section 3 of the <em>Charter</em>? And did the commission follow <a href="#ebca">the law that governs it</a>? My findings are evidence a court could weigh on those two questions. They do not answer either one. Statistics also cannot read minds. The lines can show what a map <em>does</em>, never what the people who drew it <em>intended</em>.'
			},
			effective_representation: {
				heading: 'The Charter test: effective representation',
				p1: 'Section 3 of the <em>Charter of Rights and Freedoms</em> gives every citizen the right to vote. The leading case on maps is <em>Reference re Provincial Electoral Boundaries (Saskatchewan)</em>, [1991] 2 SCR 158. This site calls it the <em>Saskatchewan Reference</em>. In it, the Supreme Court of Canada held that when ridings are drawn, section 3 protects <strong>effective representation</strong>. It does not demand that every riding hold exactly the same number of people.',
				p2: 'Justice McLachlin wrote for the majority of the Court. Roughly equal voting power comes first, she explained. But it can give way to other things: geography, community history, shared local interests, and the voice of minority groups. The Court set no fixed limit on how far a riding may stray from the average. A riding may be bigger or smaller than average <em>if those other reasons justify it</em>.',
				p3: 'As I read the case law, two things follow. Both are reasons not to read too much into my numbers:',
				li1: '<strong>A lean toward one party is not enough, on its own, to make a map unconstitutional.</strong> In the cases reviewed in the audit\'s academic report, a lean had to come with something more. It could be gaps in riding population that geography or community do not justify. Or it could be evidence that those reasons were used as cover for a party\'s gain instead of for their real purpose. That is why I also tested how a map\'s lines are drawn. I measured how much riding sizes vary and how cities are split, and I checked the boundaries the commission\'s majority flagged.',
				li2: 'A court does not look for the best possible map. It asks whether reasonable people, applying the right principles, could have drawn these lines. <strong>Courts defer to the people who draw the map</strong>, and they give legislatures and commissions a lot of room. The closest case on community ties is <em>Raîche v. Canada (Attorney General)</em>, 2004 FC 679. The Federal Court found <em>no</em> breach of section 3 there. What it did find was that the federal commission had broken the federal boundaries law\'s duty to respect communities of interest. The court set aside the commission\'s decision for the ridings in dispute and delayed its ruling by a year, and Parliament made the fix. That was a lower-court ruling on a federal law. An Alberta court may find it persuasive, but it does not have to follow it.',
				p4: 'I held each real map up against 1,010,000 maps a computer drew from the same voting areas, without ever seeing a vote. A court asking about effective representation could weigh those comparisons. It could weigh my other measurements too: how population varies from riding to riding, and where lines leave town and city limits. No score, and no mix of scores, decides the legal test. When I report that several measures point the same way, I am describing a pattern in the data. That is not a legal conclusion.'
			},
			ebca: {
				heading: 'Alberta\'s law: the Electoral Boundaries Commission Act',
				p1: 'Alberta\'s commissions work under the <em>Electoral Boundaries Commission Act</em>, RSA 2000, c. E-3. This page calls it the Act. The Act calls a riding an electoral division.',
				p2: 'On the commission\'s minority map, the most populous riding holds 24.06% more people than the provincial average. That is within a point of the limit set by <strong>the population band</strong>, but not past it. As a general rule, each riding\'s population must be within 25% of the provincial average, above or below. Both of the commission\'s 2026 maps meet that rule: apart from the three ridings each map protects under the remote-riding exception, every riding sits inside the band. A band that wide leaves the commission a lot of freedom. My population findings describe choices made <em>inside</em> the legal band. On the commission\'s own tables, riding sizes on the minority map are spread 48% wider than on the majority map. On 2021 census counts, though, the average gap from the ideal size comes out almost the same on all three maps. Another finding is the crowding of north-east and central Calgary. Whether a map is legal and whether it is unusual are different questions.',
				p3: '<strong>The remote-riding exception, section 15(2),</strong> lets up to four ridings have as many as 50% fewer people than average. The commission must be of the opinion that at least three of these five tests are met:',
				criterion1: 'an area over 20,000 km² (or a surveyed area over 15,000 km²);',
				criterion2: 'more than 150 km from the Legislature Building to the riding\'s nearest boundary, by the most direct highway route;',
				criterion3: 'no town in the riding with more than 8,000 people;',
				criterion4: 'an Indian reserve or a Métis settlement in the riding;',
				criterion5: 'part of the riding\'s boundary runs along Alberta\'s border.',
				p4: 'The exception is a choice. A riding that meets the tests is eligible for it, but the commission is never forced to use it. Each of the commission\'s 2026 maps uses it for three ridings. I checked all six against the tests in the Act and found every one eligible. So the dispute is about how one riding was drawn. Eligibility is not the question. The minority\'s Rocky Mountain House–Banff Park riding meets one test, the provincial-border one, only because it runs through national-park land where no one lives. The commission\'s own final report (March 23, 2026, p. 10) records what the majority commissioners said about that choice:',
				quote: '"They propose to retain an electoral division of \'Rocky Mountain House-Banff Park\' by artificially extending its boundary to the province\'s western border with British Columbia (taking part of Banff National Park, where no one lives), which is a bad faith effort to ensure it can be protected under s. 15(2) of the Act."',
				p5: 'Those words, "bad faith" included, belong to the three majority commissioners, one of them the chair. They wrote them in an official report that the Act requires. They are not the audit\'s words. My own check found that the riding qualifies for the exception even without the park land. Quoting the report records what it says. It does not record what any commissioner intended.',
				p6: 'Under the Act, a commission\'s report is <strong>not law by itself</strong>. The lines change only when the Legislative Assembly passes a separate bill, an Electoral Divisions Act. In Quebec a commission\'s map normally takes effect without the National Assembly\'s final approval, though in June 2026 the Assembly passed a map of its own. In Alberta, as in most provinces, it takes a bill, so the governing party decides whether any commission map becomes law. The Act\'s rules on hearings, deadlines and the 25% band are addressed to the commission. As I read it, nothing in the Act governs what the Assembly does instead. It sets no minimum notice and no period for public comment.',
				cross_ref: 'The academic report in <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">the audit repository</a> has the full legal analysis, in sections 2 and 5.9. It reviews the case law and the writing on how courts defer to commissions, and it compares how other provinces make their maps.'
			},
			audits_standing_rule: {
				heading: "The audit's standing rule",
				p1: 'Every version of this audit keeps the same rule. It may report what the tests show, and how unusual a map is next to maps a computer drew with no aim. It does not call any map a gerrymander, and it does not guess at intent from the shape of the lines. Nor does it rule on whether a map meets the Constitution or the Act. Those questions belong to courts, commissions and readers, with the audit\'s evidence in front of them.',
				cross_ref: 'Companion pages: <a href="__BASE__/methods">How I checked</a> explains every test and number in plain words. <a href="__BASE__/norms">What the norms ask</a> covers the unwritten rules for how maps get made, and the strongest case against my reading of them.',
				disclaimer: 'This page is a plain-language guide to the audit. It is not legal advice. Do not rely on anything here as a legal opinion.'
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
				p3: "This cookie holds only the preferences above — no personal or identifying information. Its contents are scrambled with a key that ships inside the page, so the stored value is not human-readable; because that key is public, treat this as tamper-resistance rather than true secrecy. It is sent only over HTTPS, is never shared with other sites, and expires one year after it was last saved. You can remove it at any time by clearing your cookies. The site is served as static files, so nothing on the server side reads it. Your colour theme is also mirrored to your browser's local storage so the correct theme can be applied instantly on load, before anything flickers; that value too is purely functional and never sent anywhere. If you choose a language, local storage keeps that choice the same way."
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
				p2: "The feedback form is separate from the analytics. When you send a message, the page sends your message, your name and email only if you give them, the language you were reading in, the address of the feedback page, and the address of the page you came from if your browser reports one. As with any web request, your browser also sends its identification string and your network address. To limit repeat sending, the service checks a hash of your network address made with a daily-changing secret. Messages are kept on the same Canadian infrastructure as the analytics records. Questions, corrections, and deletion requests, including deletion of a message you sent: please use the <a href=\"__BASE__/feedback\">feedback form</a>. Requests are answered within 10 business days."
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
					raiche: '<em>Raîche v. Canada (Attorney General)</em>, 2004 FC 679. (Federal Court, trial level; the closest reviewed case on community of interest in an electoral boundary dispute.)',
					rucho: "<em>Rucho v. Common Cause</em>, 139 S. Ct. 2484 (2019). (U.S. Supreme Court. It held that partisan gerrymandering claims cannot be decided in federal courts. It is cited here for contrast with Canada's s.3 effective-representation standard.)"
				},
				statutes: {
					ebca: '<em>Electoral Boundaries Commission Act</em>, RSA 2000, c E-3.'
				}
			}
		}
	}
} as const;
