<script lang="ts">
  import { onMount } from 'svelte';
  import { base } from '$app/paths';
  import { init } from '$lib/mapEngine';

  onMount(() => {
    init(base);
  });
</script>

<header>
  <div class="header-inner">
    <div class="header-text">
      <h1>Alberta Electoral Boundary Audit</h1>
      <p class="subtitle">Alberta's commission produced two riding maps in 2026. This audit compared them — using the same tests, applied equally to both — to ask whether they treat voters the same way.</p>
      <span class="badge">Official Elections Alberta maps &mdash; May 2026</span>
      <p class="cover-note">The map at right is the minority commission's 2026 proposal &mdash; the one that sits furthest from the neutral ensemble in statistical testing. Each riding is coloured by its 2023 vote: blue for UCP-leaning districts, orange for NDP-leaning. Colour intensity reflects where people actually live: bright and saturated in dense urban cores, pale and faded in sparse rural areas.</p>
    </div>
    <a href="#" id="zoom-trigger" title="Click to zoom" style="cursor:zoom-in; display:inline-block;">
      <img src="images/cover_art.png" alt="Alberta electoral district maps — minority commission proposal, coloured by 2023 vote" class="header-image">
    </a>
  </div>
</header>

<nav>
  <a href="#section-1">1: Map</a>
  <a href="#section-2">2: The Split</a>
  <a href="#section-3">3: Litmus Test</a>
  <a href="#section-4">4: Crack &amp; Pack</a>
  <a href="#section-5">5: Impact</a>
  <a href="#section-6">6: Gerrymanders</a>
  <a href="#section-7">7: November</a>
  <a href="#section-8">8: Invisible</a>
  <a href="#resources">Resources</a>
  <a href="#retractions">Retractions</a>
  <a href="#references">References</a>
</nav>

<div class="container">

  <div style="padding: 1.5rem 0 0.5rem;">
    <div class="callout" style="background:#F0EBF8; border-left-color:#6B35A7; font-size:1.05rem; padding:0.9rem 1rem; margin-bottom:0.8rem;">
      <p style="margin:0;"><strong>Bottom line:</strong> The commission&rsquo;s minority map would occur by chance in fewer than 1&nbsp;in&nbsp;14.5&nbsp;million randomly drawn maps. The majority map falls well within normal range.</p>
    </div>
    <div class="callout" style="background: #D0EEEA; border-left-color: #1A7A6E; font-size: 1.02rem; line-height: 1.65;">
      <p style="margin:0 0 0.6rem;"><strong>TL;DR</strong></p>
      <p style="margin:0 0 0.6rem;">Alberta's redistribution commission split 3&ndash;2 in 2026 and produced two different proposed maps. The government set both aside and assigned redistricting to a five-member committee of MLAs (the Lunty committee), expected to report in November 2026. Neither commission map is law.</p>
      <p style="margin:0 0 0.6rem;">This audit tested both commission maps the same way, using 1,010,000 computer-drawn neutral maps built from the official Elections Alberta shapefiles as a reference point. The majority proposal sits within the neutral range on every pre-registered test. The minority proposal crosses four of five structural tests, and its partisan-fairness seat split at a 50/50 vote is reached by fewer than 100 of those neutral maps &mdash; a joint probability of roughly 1 in 15 million under a neutral drawing process.</p>
      <p style="margin:0;">The audit measures outcomes, not intent. When the Lunty committee releases its map, this audit will apply the same tests to it.</p>
    </div>
  </div>

  <section id="section-1">
    <h2>1: The Map</h2>
    <p>The cover map is the best single image in this audit. Here is how to read it.</p>
    <p>Alberta is divided into 4,765 Voting Areas — small geographic zones Elections Alberta uses to count polling-station ballots. Each one is coloured by how people in it actually voted in 2023: orange where NDP votes are concentrated, blue where UCP votes are concentrated. But the colour only becomes dark and saturated where a lot of people live. A Voting Area that covers hundreds of square kilometres of parkland or farmland stays pale — nearly invisible. The map lights up where people are, and fades where they aren't.</p>
    <p>This is very different from the Alberta you see on election night. Most election maps colour entire ridings solid blue or orange based on who won. Rural ridings are geographically large and the UCP wins most of them, so election-night Alberta looks like a wall of blue with small orange pockets in Edmonton and Calgary. The cover map uses the same votes and the same geography — but shows them weighted by where people actually live. What appears is a province where most of the population is concentrated in a dense arc of cities, and those cities vote very differently from the rural map that normally represents them.</p>
    <p>The boundary lines drawn over the colour are the minority commission's 89 proposed electoral districts — the map this audit ends up critiquing. The audit's work is to ask what those lines do to the people underneath them.</p>
    <p>For me personally, this was the image that made the stakes clear. A province that looks like it votes one way on a standard map is actually a province where most of the people live in areas that vote the other way. Once you can see the population underneath the boundary choices, those choices stop looking random.</p>
  </section>

  <section id="section-2">
    <h2>2: How the Commission Broke</h2>
    <p>Alberta's Electoral Boundary Commission finished its work on March 23, 2026 and could not agree. Three commissioners produced one map; the other two produced a different one. Commission Chair Justice Dallas K. Miller and two opposition-nominated commissioners wrote the majority report; two government-nominated commissioners — Dr. Julian Martin and John D. Evans — wrote the minority report. The split centred on how to draw boundaries in fast-growing urban-edge communities: the majority gave Airdrie two districts, the minority four; the majority drew northwest Calgary's divisions close to the provincial average size, the minority drew them 11.5% above it. Both maps follow the same statute; the disagreement was about which specific geographic configurations best served the communities being drawn. Both are legal under the <em>Electoral Boundaries Commission Act</em>. The governing party is the United Conservative Party (UCP); its main opposition is the New Democratic Party (NDP). Alberta also has smaller parties — the Alberta Party, the Liberal Party of Alberta, and others — that contest seats but whose combined provincial vote share has remained low enough in recent elections that they do not materially affect the audit's partisan-fairness calculations, which are grounded in the 2023 UCP–NDP vote split. This audit measured both maps using the same methods, applied identically. Three findings stand out.</p>
    <ol style="margin: 0.8rem 0 0.9rem 1.4rem;">
      <li style="margin-bottom: 0.6rem;"><strong>The two maps differ on six things you can measure without looking at any election results:</strong> how evenly people are spread across districts, whether voters are concentrated, how badly cities are cut up, whether borders follow city limits, the shape of the districts, and how many boundaries the commission's own chair flagged as anomalous. The minority map differs from the majority on every one of them.</li>
      <li style="margin-bottom: 0.6rem;"><strong>The direction runs against the places where the governing party is weakest.</strong> Calgary's northwest quadrant, the City of Airdrie, urban areas with established municipal boundaries — the communities most affected by the minority map's structural differences are the same ones where the governing party's opponents are strongest. The audit cannot determine intent. It can measure effect.</li>
      <li style="margin-bottom: 0.6rem;"><strong>The process now promoting the minority map has no precedent in Canada.</strong> No other province lets a cabinet hand redistricting to a committee its own party controls partway through a redistribution cycle. Most provinces either require the legislature to debate the commissioners' map first, or give the commission's map automatic effect unless overridden. Alberta does neither. On April 16, the government set both commission maps aside and assigned the work to a five-member committee of MLAs (Members of the Legislative Assembly), three from the governing United Conservative Party (UCP). Alberta's <em>Electoral Boundaries Commission Act</em> requires the legislature to pass a separate Electoral Districts Act to give a commission report legal effect — the commission report itself changes nothing. Most other provinces make a commission's report legally effective unless the legislature actively overrides it; Alberta's default reverses that, meaning the governing party controls whether any commission map ever becomes law. The government's stated justification was to implement Commission Chair Justice Miller's Recommendation 5, which proposed a 91-seat legislature; but Miller had written that recommendation specifically to dissuade the legislature from adopting the minority map, and noted his majority colleagues did not endorse it — the government adopted the seat-count while replacing the map-drawing itself with a committee it controls.</li>
    </ol>
    <p><strong>The process is its own finding, separate from the maps.</strong></p>
  </section>

  <div class="callout" style="background:#EAF3FF; border-left-color:#2B5BA1; margin:0.5rem 0 1rem;">
    <p style="margin:0 0 0.4rem;"><strong>Structural audit results — before any statistics:</strong></p>
    <p style="margin:0;">The majority map crosses <strong>zero of five</strong> pre-registered structural thresholds. The minority map crosses <strong>all five</strong>. These are geometric measurements — population spread, <abbr title="how closely a district's borders follow pre-existing city and municipal limits, rather than cutting through them">municipal anchoring</abbr>, Airdrie split count, NW Calgary population excess, and chair-flagged boundary anomalies — that require no election data and no statistical sampler. The next section tests both maps against 1,010,000 computer-generated neutral maps and reaches the same conclusion through a completely different instrument.</p>
  </div>

  <section id="section-3">
    <h2>3: The 1,010,000-Map Litmus Test</h2>

    <figure style="margin:1.2rem 0;text-align:center;">
      <img src="images/lane1_dotplot.svg" alt="Histogram showing the distribution of efficiency gaps across 250,000 neutral Alberta maps. Most maps cluster near zero. The minority commission map (purple line) sits at the 94th percentile (+4.0%), in the shaded right tail. The majority map (teal line) sits at +0.1%, well within the normal range." style="max-width: 100%; border: 1px solid #ddd; border-radius: 4px; background: #fff; padding: 0.5rem;">
      <figcaption style="font-size: 0.82rem; color: #666; margin-top: 0.4rem;">Distribution of <abbr title="a measure of how lopsidedly votes are converted into seats — positive values favour the UCP, negative values favour the NDP">efficiency gaps</abbr> across 250,000 neutral Alberta maps drawn from the same geography. Most neutral maps cluster near zero; the shaded right tail marks the top 10%. The minority proposal&rsquo;s +4.0% sits at the 94th <abbr title="the percentage of maps that scored lower — p94 means 94 out of 100 neutral maps were less partisan than this">percentile</abbr> — a region fewer than 6 in 100 neutral maps ever reach. The majority proposal&rsquo;s +0.1% is indistinguishable from what a neutral process typically produces.</figcaption>
    </figure>

    <p>The table compares the two maps. The first five rows use no election results — they're properties of the lines themselves. The last two depend on how votes were attributed to each district.</p>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>What was measured</th>
            <th>Majority map</th>
            <th>Minority map</th>
            <th>Direction / Beneficiary</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Population spread across districts (tighter is better)</td>
            <td class="normal">3,180</td>
            <td class="flag">4,707 — 48% wider</td>
            <td>Structural (Reduces vote equality)</td>
          </tr>
          <tr>
            <td>NW Calgary population excess above average</td>
            <td class="normal">2.8%</td>
            <td class="flag">11.5%</td>
            <td><strong>UCP</strong> (Packs urban NDP votes)</td>
          </tr>
          <tr>
            <td>Airdrie split</td>
            <td class="normal">2 divisions</td>
            <td class="flag">4 divisions</td>
            <td><strong>UCP</strong> (Cracks urban/suburban power)</td>
          </tr>
          <tr>
            <td>Borders that follow existing municipal lines</td>
            <td>80% — within norm</td>
            <td>72% — within norm</td>
            <td>N/A — both within Canadian norm (70–85%)</td>
          </tr>
          <tr>
            <td>Boundaries flagged by the commission chair</td>
            <td class="normal">0</td>
            <td class="flag">3</td>
            <td>N/A</td>
          </tr>
          <tr>
            <td>Seats at 50/50 votes (percentile in 1,010,000-map simulation)</td>
            <td class="normal">46.1% — p83 (normal range)</td>
            <td class="flag">51.7% — p99.99 (fewer than 100 of 1,010,000 reach this)</td>
            <td><strong>UCP</strong></td>
          </tr>
          <tr>
            <td>Compactness-Weighted Efficiency Gap</td>
            <td class="normal">+1.5%</td>
            <td class="flag">-2.4%</td>
            <td><strong>UCP</strong> (via irregular shapes)</td>
          </tr>
          <tr>
            <td>Packing-cracking neighbourhood pattern</td>
            <td>6 coupled chain signals</td>
            <td class="normal">2 (pre-registered PASS)</td>
            <td>Neutral — minority achieves partisan effect via hybridization, not adjacency drain (§5.3.5)</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="callout">
      <p><strong>VOCABULARY</strong></p>
      <p><strong>Efficiency gap.</strong> A single number that measures how lopsidedly a party's votes are translated into seats. Positive numbers favour the UCP; negative favour the NDP. The audit uses ~5% as Alberta's outlier line — the value exceeded by only 5% of the 1,010,000 neutral Alberta-specific simulations. This threshold is not borrowed from US or general literature; a threshold calibrated to another jurisdiction would be wrong because Alberta's natural geography produces a different neutral range.</p>
      <p><strong>Mean-median difference.</strong> The gap between a party's median district vote share and its mean district vote share. When one party wins many close races, the median sits above the mean — those votes are distributed efficiently. When a party wins many races by large margins, the mean sits above the median — votes are being wasted. A large mean-median gap in one direction flags structural inefficiency in how one side's votes are spread across districts.</p>
      <p><strong>Percentile ranking.</strong> In this audit, a "percentile" is a rank within the 1,010,000 neutral simulated maps. "p94" means 94% of neutral maps score lower — the real map is more extreme than 94% of neutral draws. "p99.99" means fewer than 1 in 10,000 neutral maps reach that level.</p>
      <p><strong>Anchoring.</strong> The fraction of an electoral border that lies on a pre-existing administrative line — a city limit, a school-division boundary, a Statistics Canada census line.</p>
    </div>

    <p>The bottom rows depend on election results. The <em>seats@50/50</em> test holds the electorate at perfect parity (UCP and NDP each win exactly half the votes province-wide) and asks how many seats the map awards the UCP. A neutral Alberta map produces a median around 44.8% UCP seats — Alberta's geography (NDP voters concentrated in city cores, UCP voters spread across rural ridings) gives the NDP a small efficiency advantage at neutrality. The majority map at 46.1% sits at the 83rd percentile of the 1,010,000-map simulation (normal range). The minority map at 51.7% is at the 99.99th percentile — fewer than 100 of 1,010,000 neutral draws reach that value. The <em>efficiency gap</em> number measures how lopsidedly each party's votes get translated into seats; on the official Elections Alberta shapefiles the minority's efficiency gap is +4.0%, placing it at the 94th percentile — just below the audit's 95th-percentile outlier line. The verdict section unpacks the consequences.</p>

    <p>The last row is where the minority map has fewer coupled chain signals than the majority on the neighbour-drain test: 2 against the majority's 6 (and the 2019 enacted map's 5). The audit pre-registered this test before measuring, and the minority's lower count is a genuine pre-registered PASS — the minority does not show the classic pack-and-drain adjacency pattern. It is the single test where the minority numerically outperforms the majority. §5.3.5 of the academic report explains why: the minority achieves its partisan effect through hybridization (city-splitting that internalises packing and cracking within individual EDs), which is invisible to an adjacency-chain test that only measures how packed districts cluster next to cracked ones.</p>
  </section>

  <section id="section-4">
    <h2>4: Cracking, Packing, and Draining</h2>

    <figure style="margin:1.2rem 0;text-align:center;">
      <img src="images/figure_airdrie_v3.svg" alt="Map showing the division of Airdrie into four separate districts under the minority map" style="max-width: 100%; border: 1px solid #ddd; border-radius: 4px; background: #fff; padding: 0.5rem;">
      <figcaption style="font-size: 0.82rem; color: #666; margin-top: 0.4rem;">The division of Airdrie into four separate districts under the minority map, diluting its urban voting power.</figcaption>
    </figure>

    <p>The five commissioners worked from the same statutory rules, the same provincial geography, the same archive of 1,140 public submissions, and the same demographic data. Their two competing drafts agree on most of Alberta. Where the drafts diverge, they diverge on choices someone in the room had to make. Three of those choices are worth seeing as choices, not numbers.</p>

    <p><strong>It splits the City of Airdrie into four pieces.</strong> The law caps each electoral division at one-and-a-quarter times the provincial average, so Airdrie needs at least two divisions. The majority map gives it two. The minority gives it four — north to Calgary-Nolan Hill-Cochrane, east to Airdrie East, west to Calgary-Foothills-Airdrie West, and centre-south to Calgary-Airdrie — each one stapled to a different rural or Calgary-edge district. An Airdrie resident with a question for her MLA has to know which quarter of the city she lives in before she can call the right office. Her neighbours two blocks over will give her three different answers. The PTA at her child's school cannot send a single delegation to one MLA on a school-funding question; they have to coordinate four delegations to four offices, each MLA primarily accountable to a different rural or suburban constituency. The minor-hockey association, the food bank, the Chamber of Commerce — every organization that operates citywide now operates across four provincial ridings.</p>

    <div class="callout">
      <p><strong>WHY AIRDRIE MATTERS</strong></p>
      <p>Airdrie is the largest Alberta city without its own MLA. At 85,805 people (2024 municipal census) it is bigger than Red Deer; it has one council, one tax bill, one school division — every civic system treats it as a unit.</p>
      <p>Splitting it across four provincial divisions — Calgary-Airdrie, Calgary-Foothills-Airdrie West, Calgary-Nolan Hill-Cochrane, and Airdrie East — each primarily identified with a different surrounding jurisdiction, removes Airdrie from the political map at the level of government that draws it. The city has 85,805 residents and zero seats in the legislature where a majority of voters call the place home.</p>
      <p>A four-way split is invisible to every partisan-fairness test except the one that asks: can a voter find their MLA?</p>
    </div>

    <div class="callout">
      Both maps are legal. The four-way split is a choice.
    </div>

    <p><strong>Where it departs from municipal lines, it departs at strategically important places.</strong> When electoral maps follow the edge of a city or town, voters recognize where their division begins and ends — the property-tax line, the school-division line, the local-election ward line, and the provincial-election line all coincide. Statistics Canada publishes these boundaries for free. On official Elections Alberta shapefiles, both maps follow municipal lines at comparable overall rates: the majority at 80%, the minority at 72%, both within Canada's 70–85% norm (Quebec: 78%, Ontario: 82%, BC: 71%; comparator commissions documented in the monograph). (The audit's initial provisional analysis showed the minority anchoring at only 15%; that figure did not survive recomputation on official shapefiles — see the correction note below.) The striking observation is not the overall rate but where the minority's departures are concentrated: the three boundaries the commission's own chair flagged as anomalous — Rocky Mountain House–Banff Park's extension into uninhabited national-park land, the Nolan Hill–Cochrane lasso corridor, and the Olds–North Airdrie reach — are each departures from pre-existing civic geography in the exact urban-edge zones where pairing urban and rural voters most directly affects which party wins the seat.</p>

    <p>The minority commissioners gave reasons for each of the three flagged boundaries. For Rocky Mountain House–Banff Park, they cited geographic size, the Highway 22 corridor, and the proximity of First Nations reserves to Rocky Mountain House; the commission chair called the extension into uninhabited national park land "a bad faith effort" to satisfy the area criterion, and that phrase appears in the commission's official final report. For Nolan Hill–Cochrane, they cited shared transportation and employment ties between northwest Calgary and Cochrane; Statistics Canada journey-to-work data shows only 35.8% of Cochrane workers travel to Calgary at all, with most working within Cochrane itself. For the Olds–North Airdrie reach, they cited Highway 2 corridor continuity; the audit found the specific Airdrie extension fails on population grounds. Independent check found five of the minority's six published sub-rationales fail or only partially hold against primary data.</p>

    <p><strong>One area of Calgary is carved up to concentrate NDP voters into larger-than-average divisions.</strong> In Calgary's northwest quadrant, the minority map's divisions average 11.5% above the province-wide population — versus 2.8% on the majority. The same geographic zone, drawn by the same commission under the same constraints, produces districts a quarter larger on one map than on the other. This is <em>packing</em>: concentrating one party's voters into fewer, larger districts so each of their ballots weighs less. Packing and <em>cracking</em> (splitting a party's voters thinly across districts they narrowly lose) are the two classic gerrymandering moves; both shrink a party's seat count below its vote share.</p>

    <p>The commission chair — appointed under the same Act, working from the same submissions — flagged three boundaries on the minority map as geographically anomalous: Rocky Mountain House–Banff Park's extension into uninhabited national park land; the Calgary-Nolan Hill–Cochrane lasso-shaped corridor; the Olds–Three Hills–Didsbury reach into north Airdrie. The majority received zero such flags from the same chair. (The chair's published criticism covers seven boundary configurations in total — four geometric flags in the main report and three in Appendix C. This audit independently confirmed anomalous geometry for three of the four geometric flags; the fourth, Calgary-Foothills-Airdrie West, did not meet the audit's confirmation threshold.)</p>
  </section>

  <section id="section-5">
    <h2>5: The Impact on the Ground</h2>

    <div class="callout">
      <p><strong>LANE 1 AND LANE 2</strong></p>
      <p><strong>Lane 1 (numbers)</strong> uses election results to test whether the map converts votes into seats fairly — it asks how the map performs across different vote splits. <strong>Lane 2 (structure)</strong> examines only the drawn lines — city splits, population spread, boundary shapes — with no election data at all. Each lane is independent: a map can fail one while passing the other. The minority proposal fails both; the majority passes both.</p>
    </div>

    <p>Lane 1 depends on which election results you score the maps against. Lane 2 does not. The structural evidence is in the maps themselves — drawn lines, split cities, where the boundaries do and don't follow administrative lines that exist for other reasons. On these tests, the two maps are not close.</p>

    <figure style="margin:1.2rem 0;text-align:center;">
      <img src="images/lane2_bars.svg" alt="Bar chart comparing five structural-fairness tests side by side. The majority map bars sit at zero or well inside safe ranges. The minority map bars cross every threshold by a wide margin." style="max-width: 100%; border: 1px solid #ddd; border-radius: 4px; background: #fff; padding: 0.5rem;">
      <figcaption style="font-size: 0.82rem; color: #666; margin-top: 0.4rem;">The five structural-fairness tests, side by side. Teal bars are the majority map; purple bars are the minority map. The dashed line in each row marks the failing threshold. The minority bars cross every threshold by a wide margin. The majority bars sit flat at zero or well inside the safe range.</figcaption>
    </figure>

    <p>The same five tests in tabular form, with each test's threshold stated alongside the result. The bottom row is the audit's <em>summary</em> — the count of tests each map fails out of the five.</p>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Test</th>
            <th>Majority map</th>
            <th>Minority map</th>
            <th>Direction / Beneficiary</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Border follows existing municipal lines (70–85% Canadian norm)</td>
            <td class="normal">80% — within norm</td>
            <td>72% — within norm</td>
            <td>N/A — both within Canadian norm</td>
          </tr>
          <tr>
            <td>Population spread (tighter is better)</td>
            <td class="normal">3,180</td>
            <td class="flag">4,707 — 48% wider</td>
            <td>Structural (Reduces vote equality)</td>
          </tr>
          <tr>
            <td>NW Calgary population excess above average</td>
            <td class="normal">2.8%</td>
            <td class="flag">11.5%</td>
            <td><strong>UCP</strong> (Packs urban NDP votes)</td>
          </tr>
          <tr>
            <td>Boundaries flagged by the commission's own chair</td>
            <td class="normal">0</td>
            <td class="flag">3</td>
            <td>N/A</td>
          </tr>
          <tr>
            <td>Airdrie split (constraint minimum: 2)</td>
            <td class="normal">2 pieces</td>
            <td class="flag">4 pieces</td>
            <td><strong>UCP</strong> (Cracks urban/suburban power)</td>
          </tr>
          <tr>
            <td><strong>Pre-registered summary</strong> (&ge; 4 of 5 = outlier)</td>
            <td class="normal"><strong>0 of 5 fired</strong></td>
            <td class="flag"><strong>4 of 5 fired</strong> (anchoring test neutral — both maps within Canadian norm; remaining 4 tests all fire)</td>
            <td><strong>UCP</strong></td>
          </tr>
        </tbody>
      </table>
    </div>

    <p>A separate finding — applied only to the minority because the minority is the map whose contested redraws are public (the majority did not publish a contested-redraw rationale list; the seven-rationale audit cannot be applied symmetrically and is reported as a single flag, not as additional rows in the structural-irregularity count) — is that <strong>five of six of the minority commissioners' published rationales fail under independent check</strong>. (A seventh redraw the audit had previously listed turned out to rest on a federal-boundary claim that cannot be located in the minority report; it has been removed rather than left as a weak claim.)</p>

    <p>The audit also tested the chair's separate, blanket assertion in Appendix C that the minority's seven contested hybrid configurations had <strong>no public support</strong> in the 1,140+ public submissions. A keyword search across the full submission archive (94% machine-parsed, 6% image-only and excluded; methodology and per-configuration evidence at <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/submission_search_findings.md" rel="noopener">findings/submission_search_findings.md</a>) returned a more nuanced picture than either the chair's blanket claim or its blanket dismissal: the chair was right on three of seven (Airdrie 4-way split, Calgary–Nolan-Hill–Cochrane hybrid, and the St. Albert minority alternative each lack any documented support), wrong on three of seven (Rocky Mountain House–Banff Park drew an explicit, detailed proposal from at least one Clearwater-area submission plus several aligned ones; Olds–Three-Hills–Didsbury was supported by Beiseker residents in writing; Chestermere drew multiple submissions opposing a Calgary merger that materially align with the minority's intent), and partially wrong on one (Red Deer hybrids drew a peri-Red-Deer hybrid proposal from a sitting Red Deer councillor, with directional but not configuration-exact alignment). The chair's Appendix C "no public support" sweep is therefore demonstrably overbroad — three of seven are demonstrably false — but it is not invented out of whole cloth, since three of seven do hold up. <strong>This finding cuts against the chair, not against the minority.</strong></p>

    <p><strong>On Lane 2, the majority crosses zero structural thresholds. The minority crosses every one of them by a wide margin.</strong></p>
  </section>

  <section id="section-6">
    <h2>6: How &#8220;Clean Gerrymanders&#8221; Work</h2>

    <div class="callout">
      <p><strong>A NOTE ON LEGAL TERMINOLOGY</strong></p>
      <p>"Gerrymandering" has no legal definition in Canadian law. The word is used throughout this report in its everyday political sense — manipulating electoral boundaries for partisan advantage. The legal tests that actually apply in Canada are different: whether boundaries provide "effective representation" under s.3 of the <em>Charter of Rights and Freedoms</em> (the constitutional standard the Supreme Court of Canada set in the 1991 <em>Saskatchewan Reference</em>), and whether the commission followed the rules of Alberta's <em>Electoral Boundaries Commission Act</em>. The audit's findings are evidence bearing on those legal questions. They are not proof of a legally-defined wrong, and this report does not describe them that way.</p>
    </div>

    <p>The cleanest single question to ask of any electoral map is this: if the province's vote split exactly evenly between the two main parties, what seat count would the map produce? This holds the electorate constant and asks the map alone what it does.</p>

    <p>To answer this, the audit generated 1,010,000 computer-simulated, mathematically neutral Alberta maps (4 independent chains &times; 252,500 steps, base seed from Cloudflare drand beacon, pre-registered at OSF before execution) using the official Elections Alberta shapefiles, holding to the exact same statutory rules and geographic boundaries the commission used. We then placed the commission's two 2026 maps into that distribution to see how normal they are.</p>

    <div class="callout">
      <p><strong>HOW THE SIMULATION WORKS</strong></p>
      <p><strong>MCMC (Markov Chain Monte Carlo)</strong> is a method for exploring a large space — here, the space of all legal Alberta maps — by taking random steps from a starting point. Each step proposes a small swap between adjacent districts; if the result stays within the statutory rules, it becomes the new starting point. After enough steps, the visited maps form a representative sample of legal plans. The simulation is seeded from the Cloudflare drand public randomness beacon to prevent any cherry-picking of starting conditions.</p>
      <p><strong>ReCom (Redistricting Compiler)</strong> is the specific algorithm used here. Each step merges two adjacent districts into one region and re-splits it randomly into two new valid districts, preserving contiguity and population balance by construction — so the algorithm never needs to reject an invalid proposal.</p>
    </div>

    <div class="callout">
      <p><strong>PRE-REGISTRATION</strong></p>
      <p>Pre-registration means writing down the exact tests, thresholds, and predicted directions before looking at any data, and locking those commitments into a public time-stamped record. The Open Science Framework (OSF) is the public repository where this audit's commitments are filed. It prevents retrofitting: if a result doesn't emerge cleanly, the threshold cannot be changed after the fact and then presented as always having been the test. All five structural tests and four partisan-fairness metrics in this audit were registered at OSF before any simulation was run.</p>
    </div>

    <p>In Alberta, the neutral answer is not 50/50. <em>Across 1,010,000 computer-simulated legal Alberta maps, the median map gives the UCP only 44.8% of the seats at 50/50 votes</em> — a typical Alberta map under neutral votes hands the NDP a small seat majority. This is counterintuitive but mechanical: rural UCP voters win their ridings by 60-40 margins (wasting many "extra" UCP votes), while urban NDP voters win their ridings by tighter 51-49 margins (wasting fewer NDP votes per win). At neutrality, NDP comes out ahead on seat efficiency.</p>

    <p>The full distribution from the canonical 1,010,000-map simulation:</p>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Where the map sits</th>
            <th>UCP seats at 50/50 votes</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Median Alberta map</td>
            <td class="normal">44.8% — NDP slight seat majority</td>
          </tr>
          <tr>
            <td>95th-percentile map</td>
            <td>47.1%</td>
          </tr>
          <tr>
            <td>99th-percentile map</td>
            <td>48.4%</td>
          </tr>
          <tr>
            <td><strong>Maximum across 1,010,000 maps</strong></td>
            <td class="flag"><strong>below 51.7% (fewer than 100 plans reach this value)</strong></td>
          </tr>
        </tbody>
      </table>
    </div>

    <p>A note on seat counts. The 2026 commission maps each have <strong>89</strong> districts; the audit's computer simulation runs on the <strong>87</strong>-district 2019 map (its starting substrate); the November Lunty committee will produce <strong>91</strong>. All percentages are seat <em>shares</em>, comparable across these denominators. The simulation uses the 2019 map as its starting point because the ReCom algorithm needs a legally enacted map to propose swaps from — the 2019 map is the last enacted Alberta electoral map. Using either commission proposal as the substrate would be circular: we would be measuring whether a map is extreme compared to maps derived from itself.</p>

    <p>The results — placing the three real maps in this distribution — point to a specific, surgical pattern of boundary drawing.</p>

    <h3>All four statistical measures fire simultaneously</h3>

    <p>When the official Elections Alberta shapefiles are used, the minority map is a statistical outlier on every partisan-fairness metric — not just the tipping-point one.</p>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Map</th>
            <th>Efficiency gap</th>
            <th>Mean-median</th>
            <th><a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener" title="Declination measures the angular difference between the seats-votes curve for each party. Negative values favour the UCP; positive favour the NDP.">Declination</a></th>
            <th>Seats at 50/50</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Majority 2026</td>
            <td class="normal">+0.1% (p15)</td>
            <td>&#8722;3.6% (p2)</td>
            <td>+0.027 (p81)</td>
            <td class="normal">46.1% (p83)</td>
          </tr>
          <tr>
            <td>Minority 2026</td>
            <td class="flag"><strong>+4.0% (p94)</strong></td>
            <td class="flag"><strong>+1.0% (p99.98)</strong></td>
            <td class="flag"><strong>&#8722;0.077 (p1.2)</strong></td>
            <td class="flag"><strong>51.7% (p99.99)</strong></td>
          </tr>
        </tbody>
      </table>
    </div>

    <p>The majority map sits comfortably inside the normal range on three of four metrics. Its mean-median sits at p2 in the NDP-favourable direction — an unusual result but pointing the wrong way to help the UCP. The majority map's close adherence to municipal boundaries places NDP-heavy urban cores into their own compact districts, where NDP votes win by efficient margins while UCP rural wins tend to be by larger margins; this mild structural NDP efficiency advantage is what shows up in the mean-median measure. The minority map is in the tail on all four, each pointing in the same partisan direction.</p>

    <h3>The 50/50 tipping point: fewer than 100 of 1,010,000 neutral maps reach it</h3>

    <p>The tipping-point metric is the most intuitive: if the province split exactly 50/50 between the two parties, how many seats does each map give the UCP?</p>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Map</th>
            <th>UCP seats at 50/50 votes</th>
            <th>Where it sits</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>2019 enacted</td>
            <td class="normal">46.0%</td>
            <td class="normal">83rd percentile — inside the normal range</td>
          </tr>
          <tr>
            <td><strong>Majority 2026</strong></td>
            <td class="normal"><strong>46.1%</strong></td>
            <td class="normal"><strong>83rd percentile — well within bounds</strong></td>
          </tr>
          <tr>
            <td><strong>Minority 2026</strong></td>
            <td class="flag"><strong>51.7% (46 seats)</strong></td>
            <td class="flag"><strong>99.99th percentile — fewer than 100 of 1,010,000 neutral draws reach this</strong></td>
          </tr>
        </tbody>
      </table>
    </div>

    <p>Fewer than 100 of 1,010,000 computer-simulated neutral Alberta maps produced a <code>seats@50/50</code> value as high as the minority proposal's. Based on actual recent voting patterns, it would award the UCP 60 seats (compared to 55 in the majority proposal). The majority proposal is the kind of map a neutral procedure routinely generates. The minority proposal is the kind of map you have to specifically aim to draw.</p>

    <h3>What this means in plain language</h3>

    <p>The official shapefiles reveal a map that is statistically extreme in the same partisan direction on all four measures at once. The joint probability of a neutral drawing process producing a map this extreme across all four measures simultaneously is roughly one in 15 million (p&nbsp;=&nbsp;6.87&times;10<sup>&#8722;8</sup>, <a href="https://osf.io/6pt83" rel="noopener">pre-registered Fisher combined test</a>). That is not a rounding error or a measurement artefact — it is the same answer from four independent statistical instruments read in the same room.</p>

    <details style="margin:0.8rem 0 1rem; border-left:3px solid #bbb; padding:0.4rem 0 0.4rem 0.9rem;">
      <summary style="cursor:pointer; font-weight:600; color:#444; font-size:0.93rem; user-select:none;">What this p-value means — and what it doesn&rsquo;t</summary>
      <div style="margin-top:0.6rem; font-size:0.92rem; line-height:1.6; color:#333;">
        <p style="margin:0 0 0.5rem;">A p-value answers one question: if the map were drawn by a neutral process, how often would we see a result this extreme or more extreme? At p&nbsp;=&nbsp;6.87&times;10<sup>&#8722;8</sup>, the answer is about once in 14.5 million trials.</p>
        <p style="margin:0 0 0.5rem;">This is a frequentist hypothesis test, not a measurement of intent. It does not say the commission intended to gerrymander, and it does not quantify how unfair the map is in practical terms. It says the boundary pattern is statistically inconsistent with a neutral drawing process — the same conclusion a randomized audit would reach regardless of who drew the map or why.</p>
        <p style="margin:0;">The test was pre-registered before the data were analyzed (<a href="https://osf.io/w2s8k" rel="noopener">OSF registration w2s8k</a>). The pre-registration specifies the null hypothesis, the metrics, and the rejection threshold in advance, so the result cannot be attributed to choosing a favorable framing after seeing the numbers.</p>
      </div>
    </details>

    <div class="callout">
      <p><strong>SWING-ZONE ALLOCATION TEST (SZAT)</strong></p>
      <p>SZAT is the audit's second independent test, and it asks a different question from the simulation: not "is this map extreme overall?" but "are the specific line choices partisan-neutral?" It works by isolating only the Voting Areas where the minority's map differs from the majority's — the contested re-draws — and testing whether those particular choices, taken together, shift vote efficiency in one party's direction. Because it compares only the points of departure, it automatically controls for everything the two maps share: the same geography, population targets, and statutory rules. <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/szat_summary.json" rel="noopener">Technical details and bootstrap results &rarr;</a></p>
    </div>

    <p><strong>Two questions, one answer.</strong> The 1,010,000-map simulation asks: <em>is this map extreme compared to neutral maps drawn on the same Alberta geography?</em> A second, separate test — called the <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/szat_summary.json" rel="noopener">Swing-Zone Allocation Test</a> — asks a different question: <em>are the specific lines on the map partisan-neutral?</em> It works by looking only at the Voting Areas where the minority drew differently from the majority and asking whether those particular choices, taken together, shifted vote efficiency in one party's direction. Because it compares only the places where the two maps differ, it automatically controls for everything they share — the same provincial geography, the same population targets, the same statutory rules. Both questions return the same answer. That is why the one-in-15-million figure is a combined result rather than a single test: it is two independent lines of evidence converging.</p>

    <p>This explains why the minority proposal had to be such an extreme statistical outlier (p99.99) against 1,010,000 neutral simulations. In an 89-seat legislature, a two-thirds supermajority requires exactly 60 seats. You do not hit the 60-seat supermajority threshold by drawing natural, community-respecting boundaries; you have to surgically force the map to get there.</p>

    <div class="callout">
      <p><strong>WHY A SUPERMAJORITY MATTERS</strong></p>
      <p>Under Canada's Westminster parliamentary system, a simple majority (45 seats) is enough to pass routine laws and budgets. But securing a two-thirds supermajority (60 seats) grants a government near-absolute control. It allows the ruling party to effortlessly invoke "closure" to shut down debate, rewrite the rules of the legislature without opposition consent, and completely dominate all legislative committees. More importantly, it makes a Premier mathematically bulletproof to internal revolts — even if half a dozen backbenchers cross the floor, the government retains absolute control. A simple majority lets you drive the car; a 60-seat supermajority lets you rewrite the traffic laws.</p>
    </div>

    <p>By strategically diluting urban voters into surrounding rural-edge districts (the "urban hybridization" pattern identified in Lane 2), the minority proposal engineers the exact structural firewall needed to secure those 60 seats. The Lane 2 structural finding and the Lane 1 statistical finding converge on the same proposal, the same direction, and the same communities.</p>

    <h3>Confirmation from the targeted-procedure test</h3>

    <p>To be sure this isn't a quirk of the neutral simulation's known compactness preference, the audit ran a targeted hill-climbing procedure (<a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">Cannon et al. 2022 — cited and described in the technical report</a>) in both directions: maximising UCP seats and maximising NDP seats. Same number of steps (40,000) in each direction, same statutory constraints, same provincial geometry.</p>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Procedure</th>
            <th>Most-extreme value reached</th>
            <th>What it tells us</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Neutral MCMC, max produced</td>
            <td>below 51.7% UCP seats @ 50/50</td>
            <td>The natural ceiling under neutral drawing</td>
          </tr>
          <tr>
            <td>Neutral MCMC, min produced</td>
            <td>~39% UCP seats @ 50/50</td>
            <td>The natural floor under neutral drawing</td>
          </tr>
          <tr>
            <td>Targeted hill-climb, UCP-maximizing</td>
            <td class="flag"><strong>52.9%</strong></td>
            <td>What a procedure deliberately aiming for UCP advantage can reach</td>
          </tr>
          <tr>
            <td>Targeted hill-climb, NDP-maximizing</td>
            <td><strong>37.9%</strong></td>
            <td>What a procedure deliberately aiming for NDP advantage can reach (below the neutral floor)</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p>The minority map's 51.7% sits closer to the targeted-UCP ceiling (52.9%) than to the neutral median (44.8%). The majority map's 46.1% sits at the neutral median. Both the 2019 enacted map and the 2026 majority fall comfortably within what neutral procedure routinely produces — different vote shares, same zone of unremarkable outcomes. The majority continues 2019 Alberta practice on the partisan-fairness axis the same way it continues 2019 practice on municipal anchoring (80.0% vs 2019's 75.2%). Two maps drawn under the same Alberta rules, by the same five commissioners, in the same room: one lands where neutral procedures routinely produce, the other lands where you have to specifically aim to land.</p>

    <p><em>That</em> is the shape of the finding, and it is also the framing a court would actually apply.</p>

    <h3>Ruling Out Alternative Explanations</h3>

    <p>When presented with a statistical outlier of this magnitude, a rigorous audit must rule out innocent explanations before attributing these patterns to deliberate design. The structural data (Lane 2) systematically dismantles the standard alternative defenses:</p>

    <ol style="margin: 0.8rem 0 0.9rem 1.4rem;">
      <li style="margin-bottom: 0.6rem;"><strong>The "Natural Political Geography" Defense:</strong> <em>("Urban voters are naturally packed; the map just reflects Alberta's geography.")</em> The 1,010,000 simulations already account for Alberta's natural geography. The simulation proves that while geography gives the UCP a baseline efficiency advantage, it naturally caps around the 83rd to 90th percentile. The minority map sits at the 99.99th percentile — an extreme outlier <em>even when compared to Alberta's naturally skewed baseline</em>.</li>
      <li style="margin-bottom: 0.6rem;"><strong>The "Communities of Interest" Defense:</strong> <em>("The odd shapes were drawn to keep specific communities together.")</em> If you are trying to keep communities together, you follow municipal borders. The majority map followed existing city limits 80% of the time. The minority map followed them 72% of the time — both within the 70–85% Canadian norm. What the minority map does do is actively split the unified city of Airdrie into four separate pieces, and place three of its boundary decisions precisely in the urban-edge zones the commission chair flagged as geometrically anomalous — choices that cannot be explained by community-of-interest logic.</li>
      <li style="margin-bottom: 0.6rem;"><strong>The "Population Equality" Defense:</strong> <em>("They had to draw weird boundaries to make sure every district had the exact same population.")</em> The minority map is actually much <em>worse</em> at population equality. Its Population Mean Absolute Deviation (MAD) was 4,707 — 48% wider than the majority map's 3,180 — placing it at the 99th percentile of the canonical ensemble (only 1 in 100 neutral maps produces a worse spread). It sacrificed population equality to achieve its shape.</li>
      <li style="margin-bottom: 0.6rem;"><strong>The "Incompetence or Bad Luck" Defense:</strong> <em>("They just drew a sloppy map and got unlucky with the numbers.")</em> Hitting exactly 60 seats for a supermajority while also splitting Airdrie into four pieces and placing three boundaries in the exact zones the commission's own chair flagged as anomalous requires surgical precision. The joint probability of accidentally drawing a map that hits the extreme statistical tail across four independent partisan metrics simultaneously is roughly <strong>1 in 15 million</strong> (p&nbsp;=&nbsp;6.87&times;10<sup>&#8722;8</sup>). You cannot blunder your way into the 99.99th percentile.</li>
    </ol>

    <p>What the data shows is that the minority proposal worsened both population parity and community coherence relative to what the same five commissioners produced simultaneously under identical statutory rules. The audit does not determine what the minority commissioners intended — boundary geometry cannot reveal intent — but the structural departure from both the neutral ensemble and the majority proposal's output stands regardless of intention.</p>

    <h3>A note on the R cross-validation</h3>

    <p>An earlier version of this audit (using approximated rather than official shapefiles) cross-validated the Python ReCom ensemble against the R <code>redist</code> package's Sequential Monte Carlo sampler. That cross-check produced unstable results: across three runs with the same nominal seed, the fraction of plans reaching the old minority value (48.3% on the approximated geometry) was 5.6%, then 28%, then 58% — a sampler-convergence failure, not a discovery. The full write-up is at <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/redist_python_comparison.md" rel="noopener">findings/redist_python_comparison.md</a>.</p>

    <p>With official Elections Alberta shapefiles, the minority map's <code>seats@50/50</code> rises to 51.7% — a value fewer than 100 of 1,010,000 neutral plans reach. The R cross-validation question becomes moot: zero plans from either sampler reach the canonical value at comparable sample sizes.</p>

    <p><strong>The asymmetry around 50/50 is more telling than the inversion itself.</strong> A precision sweep of the seat-vote curve at 0.01-percentage-point resolution finds the minority map keeps the UCP at or above the 45-seat legislative-majority threshold down to a UCP provincial vote share of about <strong>49.7%</strong>. That is technically a vote-seat inversion — the UCP would form government on the minority map while losing the popular vote by 0.3 percentage points — but 0.3 points is well within ordinary polling noise, so on its own this is not a dramatic finding. What <em>is</em> dramatic is the contrast: on the <strong>majority</strong> map, the UCP would need to <em>win</em> the popular vote by about 4 percentage points to reach the same 45-seat threshold. Both maps face the same Alberta geography and the same statutory rules; the gap between them — 0.3pp vs +4pp — is structural difference, not noise.</p>

    <p>This is the structural-bias finding the audit holds with confidence. It is geometry-only; it does not depend on any election result; it does not move when polls do.</p>

    <p><strong>One caveat the audit takes seriously.</strong> A real electorate is not a uniform 50/50. Voters can swamp any map's structural lean with enough swing — a particularly upset or inspired electorate will tip the result regardless of how the boundaries are drawn. The 50/50 test isolates <em>the map's contribution to the outcome</em>, not the outcome itself. What it shows is what the map does when the electorate doesn't decide for it.</p>
  </section>

  <section id="section-7">
    <h2>7: What Happens in November</h2>

    <p>Neither commission map is in force. The government set both aside in April 2026 and referred redistricting to the Lunty committee. That committee — five MLAs, three from the governing UCP — is expected to release its proposed boundaries in November 2026. When it does, this audit will apply the same methodology to evaluate it. What follows is the evaluation of the two commission proposals.</p>

    <p>The audit's central finding is geometric. <strong>Lane 2 — the structural-irregularity scorecard — is the foundation; Lane 1 is the proof that the geometry is doing partisan work.</strong></p>

    <p>The chart below puts both lanes on a single picture. The horizontal axis is Lane 1 (the partisan-fairness efficiency gap, where further right means more UCP-favoured); the vertical axis is Lane 2 (the count of structural-fairness tests the proposal fails, out of five, where higher means more structural problems). The bottom-left corner is "clean on both lanes." The top-right corner is "out of bounds on both lanes."</p>

    <figure style="margin:1.2rem 0;text-align:center;">
      <img src="images/verdict_quadrant.svg" alt="Scatter plot with efficiency gap on the horizontal axis and count of structural tests failed on the vertical axis. The 2019 enacted map and the majority 2026 map cluster in the safe lower-left corner. The minority 2026 map appears in the upper-right outlier region." style="max-width: 100%; border: 1px solid #ddd; border-radius: 4px; background: #fff; padding: 0.5rem;">
      <figcaption style="font-size: 0.82rem; color: #666; margin-top: 0.4rem;">The two ways of measuring the two commission proposals, plotted together. Left-to-right: how skewed the proposal looks on the partisan-fairness number — the further right, the more it favours the UCP. Bottom-to-top: how many of five structural-fairness tests the proposal fails — the higher, the worse. The 2019 enacted map sits in the safe corner: low on both. The majority 2026 proposal stays flat at zero structural problems and near-zero partisan skew (+0.1%). The minority 2026 proposal is a structural outlier on all five tests; its efficiency gap (+4.0%) sits just below the Alberta threshold line.</figcaption>
    </figure>

    <p>The same verdict in plain summary form, leading with the structural finding because that is what the cross-validated evidence supports most strongly:</p>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th></th>
            <th>Lane 2: Structure (geometry-only, no votes)</th>
            <th>Lane 1: Numbers (vote-dependent)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Majority 2026</strong></td>
            <td class="normal">clean — crosses <em>no</em> structural threshold</td>
            <td class="normal">inside the normal range on every metric (<code>seats@50/50</code> 46.1% — p83; efficiency gap +0.1%)</td>
          </tr>
          <tr>
            <td><strong>Minority 2026</strong></td>
            <td class="flag"><strong>crosses 4 of 5 structural thresholds</strong> by a wide margin (anchoring neutral — both maps within Canadian norm)</td>
            <td class="flag">statistical outlier on all four partisan-fairness measures simultaneously — <code>seats@50/50</code> 51.7% (p99.99, fewer than 100 of 1,010,000 reach it); efficiency gap +4.0% (p94); all four pre-registered; Fisher combined p&nbsp;=&nbsp;6.87&times;10<sup>&#8722;8</sup></td>
          </tr>
        </tbody>
      </table>
    </div>

    <p><strong>Why Lane 2 carries the case.</strong> The audit pre-registered five structural-irregularity tests on April 24, 2026 before the final simulation results were compiled. The minority crosses every one; the majority crosses none. Those measurements are geometric — they don't depend on any statistical sampler or any vote attribution. Lane 1 (the partisan-fairness numbers) corroborates Lane 2 strongly under canonical official shapefiles: the minority is a statistical outlier on all four pre-registered metrics simultaneously, with a joint neutral-null probability of p&nbsp;=&nbsp;6.87&times;10<sup>&#8722;8</sup> (pre-registered Fisher combined test — a method that combines four independent test results into a single probability by multiplying their individual tail probabilities; the combined figure is far smaller than any single test's because all four point the same direction; OSF <a href="https://osf.io/6pt83" rel="noopener">6pt83</a>). The question of whether Lane 2's unusual geometry is the specific <em>mechanism</em> behind the Lane 1 numbers was tested and the answer is no — see <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/redist_python_comparison.md" rel="noopener">findings/redist_python_comparison.md</a>. The Swing-Zone Allocation Test shows the contested boundary choices are partisan-skewed, but the tested question was whether the boundary shapes themselves — the lasso corridor, the park extension — are the direct cause of the seat swing; they are not. The seat effect comes from how redrawn Voting Area assignments shift vote efficiency across districts, not from the shapes per se. Both lanes flag the minority map; they reach that conclusion through independent instruments. Lane 2 is the central finding. Lane 1 corroborates without carrying.</p>


  </section>

  <section id="section-8">
    <h2>8: The Invisible Part</h2>

    <p>This audit ran into two data problems that have nothing to do with the commission and everything to do with how Alberta's electoral system is designed. Both are fixable.</p>

    <p><strong>Elections Alberta already has the data to tell us where advance voters live — it just doesn't publish it.</strong> About half of all Alberta votes are now cast before election day — advance polls, mobile polls, special ballots. Elections Alberta reports these results as totals for each electoral division, not by specific Voting Area. That means roughly 395,000 NDP and UCP votes cast in 2023 cannot be pinned to any neighbourhood on a map. They are counted; they just can't be located. This is not a technical problem. Every advance voter is checked against a voters list before receiving their ballot, and that list links each voter to their specific Voting Area. The information exists at the moment of voting. Elections Alberta simply does not retain or publish that link in its results. No change to the voting process is required — only a change to what EA reports from data it already holds.</p>

    <p>This affects the commissioners too, not just outside analysts. When a commission decides whether to keep Airdrie whole or split it, whether a corridor between two communities makes sense, whether a proposed boundary divides a natural constituency — those are judgments that depend on knowing where voters live. Commissioners work from the same published dataset as everyone else. Half the geographic signal about the communities they are drawing boundaries around is missing for them as well.</p>

    <p>There is at least one community in northern Alberta where this gap is total. In the northern part of the Lesser Slave Lake division, there is a Voting Area covering 4,832 km&#178; — larger than Prince Edward Island — where every single vote in 2023 was cast through Elections Alberta's mobile polling team. Those 844 residents' choices are counted in the divisional total but cannot be pinned to any location on a map. That community is entirely invisible in the published election results.</p>

    <p>When the commission initially considered eliminating the Lesser Slave Lake division and merging it into a larger riding, it was working without geographic vote data from those communities. The commission eventually preserved the division — after 80+ public submissions, many from the Indigenous communities in the northern part of the riding — invoking a provincial law that allows ridings with First Nations and M&#233;tis communities to have smaller populations than the provincial average. They got there. But the data they were working with didn't show them who was voting in the communities they were deciding to protect.</p>

    <div class="callout">
      <p><strong>SECTION 15(2) EBCA</strong></p>
      <p>Section 15(2) of Alberta's <em>Electoral Boundaries Commission Act</em> is a discretionary provision that allows commissions to protect undersize ridings — those more than 25% below the provincial population average — when the riding meets at least three of five specific criteria: (a) geographic area exceeding 20,000 km², (b) distance more than 150 km from the Legislature Building by most direct highway route, (c) absence of any town with more than 8,000 residents, (d) presence of an Indian reserve or a Métis settlement, and (e) whether the riding is coterminous with a boundary of the Province of Alberta. The provision is not automatic; the commission must judge whether the criteria are met. Lesser Slave Lake independently meets four of the five.</p>
    </div>

    <p>The interim rationale for eliminating the riding was population: at roughly 27,000 residents, Lesser Slave Lake sits about 45% below the provincial average, approaching the legal floor. That reads as a straightforward application of the rules. It isn't. Alberta law gives commissions explicit discretion to protect undersize ridings when at least three of five specific criteria apply — and Lesser Slave Lake meets four of them independently. Its area is 69,566 km² (criterion a — threshold 20,000 km²). Its nearest boundary is more than 150 km from the Legislature by highway (criterion b). No town in the riding has a population over 8,000 (criterion c). And the riding contains fourteen Indian reserves and M&#233;tis settlements whose communities share a common northern geography, a common dependence on mobile polling to vote at all, and a collective interest in having a representative primarily accountable to northern Alberta (criterion d). Under the proposed Mackenzie merger, that collective voice would have been permanently absorbed into a riding where the other party wins by more than two to one — not because those communities changed, but because the lines around them did. Each of those four criteria is an objective fact about the riding's geography, not a judgment call. Together they describe a constituency the provision was written to protect: remote, large, sparsely populated, and containing communities whose representation interest cannot be read from raw population numbers. You need three to qualify; Lesser Slave Lake has four. Treating the population shortfall as if it compelled elimination misreads the statute. The commission's reversal was the correct application of the law, not a concession to political pressure.</p>

    <p>Here is the other side of that story: while the Indigenous communities in Lesser Slave Lake were fighting to be counted, the dissenting commissioners proposed protecting a different riding by drawing its boundary through Banff National Park, where no one lives. The commission's own chair called that "a bad faith effort" to claim the legal protection. That phrase is in the commission's official final report. The protection designed for remote communities with Indigenous populations was used, in the minority's map, to defend a boundary through uninhabited wilderness. The communities it was designed to help had to fight for it through public submissions. The Lunty committee will face the same §&#x2009;15(2) decision in November — with no statutory requirement to hold public hearings, and no guarantee that the 80 submissions that reversed the commission's interim position will carry the same weight a second time.</p>

    <p><strong>Alberta should wait for the 2026 census before drawing the next map.</strong> Canada counts its population every ten years. The 2026 census enumeration happens in spring 2026; Statistics Canada releases usable sub-provincial data roughly two years later, in 2027 or 2028. The commission that drew the maps assessed in this audit had to use the 2021 census — already four years old when the maps were drawn, and potentially fourteen years old by the time those boundaries retire. Fast-growing cities like Airdrie and Chestermere will change by 40% or more over that window. Rural communities will shrink. The map will be wrong from the day it is used. A straightforward change to the <em>Electoral Boundaries Commission Act</em> could require that any new commission be appointed only after Statistics Canada releases the most current dissemination-area data from the preceding census. The result: maps that reflect where Albertans actually live, not where they lived a decade ago.</p>

    <p>The Lunty committee is operating under the existing statute, which sets no census-timing requirement, and cannot unilaterally delay past its November 2026 deadline. This recommendation applies to a future amendment to the <em>Electoral Boundaries Commission Act</em>, not to the current process. The tension is real: a committee required to deliver a map by November is working from data that will already be five years old — naming that constraint is more useful than pretending it does not exist.</p>

    <p>Neither of these is a finding about the current commission's maps. They are observations about a system that makes accurate electoral analysis harder than it needs to be. They are offered here as practical suggestions, not conclusions. Both are genuinely fixable, and fixing them would make every future commission — and every future audit — work from better ground.</p>
  </section>

  <section id="resources">
    <h2>Reports and resources</h2>

    <ul class="links-list">
      <li>
        <span class="tag">Plain Language</span>
        <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/public/report_public.pdf">Full public report</a> &mdash; Long-form, with maps, for general readers
      </li>
      <li>
        <span class="tag">Summary</span>
        <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/docs/FINDINGS_BRIEF.md">Summary of findings</a> &mdash; Plain-language overview, explains every concept from scratch
      </li>
      <li>
        <span class="tag">Academic</span>
        <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md">Technical report</a> &mdash; Full methods and citations for researchers
      </li>
      <li>
        <span class="tag">Notebook</span>
        <a href="https://colab.research.google.com/github/Ixby/alberta-electoral-boundaries-audit/blob/master/notebooks/alberta_audit_explorer.ipynb" rel="noopener">Interactive notebook</a> &mdash; Run the charts yourself in your browser, no install needed
      </li>
      <li>
        <span class="tag">Code</span>
        <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit" rel="noopener">github.com/Ixby/alberta-electoral-boundaries-audit</a>
      </li>
    </ul>
  </section>

  <section id="retractions">
    <h2>Retractions and Corrections</h2>

    <div class="callout warning">
      <p><strong>RETRACTION CONDITIONS</strong></p>
      <p>The audit's findings are pre-committed to falsifiability. Retractions apply per-finding. If any condition below materialises, the specific finding it relates to is retracted publicly within 30 days. The overall verdict (directional consistency across multiple independent tests) is retracted only if at least three of the tests fail.</p>
      <ol style="margin: 0.6rem 0 0 1.4rem;">
        <li style="margin-bottom: 0.5rem;"><strong>A counter-map exists.</strong> Someone produces a legal Alberta map satisfying the minority's own community-of-interest reasons (Airdrie, Cochrane, Nolan Hill, Rocky Mountain House–Banff Park) <em>and</em> anchoring on municipal boundaries at majority-comparable rates. Open challenge — <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/issues/14" rel="noopener">Issue #14</a> on the audit's GitHub repository.</li>
        <li style="margin-bottom: 0.5rem;"><strong>The Neighbour-Drain Pass fails the label-shuffling null.</strong> If the v2 continuous drain score (Phase B of <code>drain_v2_plan.md</code>) falls in the extreme upper tail (p &lt; 0.05) of random permutations across the fixed contiguity graph, the "pre-registered pass" is retracted and reclassified as a detected spatial signature.</li>
        <li style="margin-bottom: 0.5rem;"><strong>A pre-2026 internal commission document surfaces.</strong> Showing the minority's choices were a deliberate response to documented community submissions rather than drafting choices.</li>
        <li style="margin-bottom: 0.5rem;"><strong>The 2027 election result, fought on either of these maps, contradicts the percentile readings.</strong> If the partisan-fairness direction the audit projects from 2023 votes turns out to be wrong on actual votes, the Lane 1 finding gets revisited.</li>
        <li style="margin-bottom: 0.5rem;"><strong>The Quebec 2026 Supreme Court ruling is materially distinguished by an Alberta court.</strong> (On April 22, 2026 — six days after Alberta's April 16 motion — the Supreme Court of Canada upheld, 7–2 and from the bench, a Quebec Court of Appeal ruling that the Legault government's 2024 legislative freeze on its own redistricting commission violated the Charter's democratic-representation guarantee under s.3. The SCC held that a legislature cannot block independent commission redistricting work to preserve specific regional outcomes — the same class of argument the Alberta minority commissioners advance for retaining certain ridings. Whether Alberta's structure — reassigning redistricting to an MLA committee rather than freezing a commission outright — is constitutionally distinguishable from Quebec's is the open question.) If a court reviewing the April 16 Alberta motion finds the Alberta situation is constitutionally distinct from Quebec's — for example, because the Lunty committee is structured differently from a legislative-freeze law, or because Alberta's effective-representation analysis differs from Quebec's — the audit's procedural critique of the motion weakens.</li>
      </ol>
    </div>

    <div class="callout warning">
      <p><strong>DOCUMENTED CORRECTIONS (canonical recomputation, 2026-05-11)</strong></p>
      <p>The following early finding did not survive reanalysis against official Elections Alberta shapefiles (received 2026-05-06). It is retained here per the audit's pre-committed policy of never deleting failed findings.</p>
      <p><strong>Municipal anchoring (retracted).</strong> Early analysis using provisional map boundaries showed the minority map anchored to municipal lines only 15% of the time — 4.9&times; below the 70–85% Canadian norm. This figure was an artefact of the provisional (DPG-era) boundary reconstructions. On official Elections Alberta canonical shapefiles, both maps anchor within the Canadian norm: majority 80%, minority 72%. The municipal-anchoring <em>divergence</em> between the two maps is not a signal that survives canonical recomputation. The three boundary anomalies flagged by the commission chair (Rocky Mountain House–Banff Park, Nolan Hill–Cochrane, Olds–North Airdrie) remain and are not affected by this correction.</p>
    </div>
  </section>

  <section id="references">
    <h2>References &amp; Methodology</h2>

    <p>While this report summarizes the audit for a general audience, the underlying methodology relies on established political science and legal literature on electoral boundary design. Key references include:</p>

    <ul style="margin: 0.8rem 0 0.9rem 1.4rem; line-height: 1.7;">
      <li style="margin-bottom: 0.5rem;"><strong>Chen, Jowei, and Jonathan Rodden. 2013.</strong> "Unintentional Gerrymandering: Political Geography and Electoral Bias in Legislatures." <em>Quarterly Journal of Political Science</em> 8(3): 239–269. (Establishes the framework for evaluating how "natural packing" of urban voters interacts with neutrally drawn boundaries).</li>
      <li style="margin-bottom: 0.5rem;"><strong>Courtney, John C. 2001.</strong> <em>Commissioned Ridings: Designing Canada's Electoral Districts</em>. Montreal and Kingston: McGill-Queen's University Press. (The foundational text on the history and structural norms of independent Canadian boundary commissions).</li>
    </ul>
  </section>

  <section>
    <h2>About me</h2>
    <p style="font-size:0.9rem; color:#444;">
      I'm a student at Mount Royal University. I did this research on my own &mdash; it was not assigned as coursework and the university did not commission it. My views are my own and do not represent the university. I have no connection to Elections Alberta, the commission, or any political party.
    </p>
    <p style="font-size:0.9rem; color:#444;">
      I have supported parties on all sides of the political spectrum depending on the election. I'm telling you that because my political history could affect how I look at this issue. The main protection against that is the method: I tested both maps the same way, wrote down my predictions before looking at the results, and put everything online so anyone can check my work. I paid for this research myself. If you find something I got wrong, I genuinely want to know.
    </p>
    <p style="font-size:0.9rem; color:#444;">
      Pre-registration records (written before results were examined): <a href="https://osf.io/6pt83" rel="noopener">OSF:6pt83</a>, AsPredicted:#289,469, AsPredicted:#289,451.
    </p>
    <p style="font-size:0.9rem; color:#444;">
      Questions or corrections: <a href="mailto:wconn161@mtroyal.ca">wconn161@mtroyal.ca</a>
    </p>
  </section>

</div><!-- /.container -->

<!-- Zoom overlay -->
<div id="zoom-overlay" aria-modal="true" role="dialog" aria-label="Map zoom viewer" style="display:none;">
  <button id="zoom-close" title="Close (Esc)">&times;</button>
  <div id="zoom-instructions">
    <div class="zi-row zi-level"><span class="zi-key">Zoom</span> <span id="zoom-pct">100%</span></div>
    <div class="zi-divider"></div>
    <div class="zi-row"><span class="zi-key">Scroll</span> zoom in / out</div>
    <div class="zi-row"><span class="zi-key">Drag</span> pan</div>
    <div class="zi-row"><span class="zi-key">Dbl-click</span> reset</div>
    <div class="zi-row"><span class="zi-key">Esc</span> close</div>
  </div>
  <div id="top-bar">
    <div class="tb-group">
      <button class="tb-btn tb-map-primary" data-map="minority">Min</button>
      <button class="tb-btn" data-map="majority">Maj</button>
      <button class="tb-btn" data-map="2019">2019</button>
    </div>
    <div class="tb-sep"></div>
    <div class="tb-group">
      <button class="tb-btn tb-layer-on" data-layer="vote">Vote</button>
      <button class="tb-btn tb-layer-on" data-layer="ed-fill">Fill</button>
      <button class="tb-btn tb-layer-on" data-layer="ed-lines">Lines</button>
    </div>
    <div class="tb-sep"></div>
    <button class="tb-btn" data-layer="lock">Lock</button>
    <div class="tb-sep"></div>
    <button class="tb-btn" data-anomaly="airdrie">Anomaly</button>
  </div>
  <div id="zoom-stage">
    <object id="zoom-obj" type="image/svg+xml" data="images/cover_art_minority_hires.svg"
      title="Alberta electoral district map — full resolution"></object>
  </div>
  <div id="ed-tooltip"></div>
  <div id="ed-callout" aria-live="polite">
    <button id="ec-close">&times;</button>
    <div id="ec-header">
      <div id="ec-name"></div>
      <div id="ec-context">2026 minority proposal &middot; 2023 election results</div>
    </div>
    <div id="ec-bar"><div id="ec-ucp-bar"></div><div id="ec-ndp-bar"></div></div>
    <div id="ec-split">
      <div class="ec-party ec-ucp">
        <span class="ec-pct" id="ec-ucp-pct"></span>
        <span class="ec-party-name">UCP</span>
        <span class="ec-votes" id="ec-ucp-votes"></span>
      </div>
      <div class="ec-party ec-ndp">
        <span class="ec-pct" id="ec-ndp-pct"></span>
        <span class="ec-party-name">NDP</span>
        <span class="ec-votes" id="ec-ndp-votes"></span>
      </div>
    </div>
    <div id="ec-meta">
      <span id="ec-total-votes"></span>
      <span class="ec-dot">&middot;</span>
      <span id="ec-va-count"></span>
      <span class="ec-dot">&middot;</span>
      <span id="ec-pop"></span>
    </div>
    <div id="ec-compare"></div>
  </div>
</div>

<footer>
  <div class="container">
    Alberta Electoral Boundary Audit &mdash; May 2026<br>
    <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit">github.com/Ixby/alberta-electoral-boundaries-audit</a>
  </div>
</footer>

<!-- Map onboarding modal — shown once per session via sessionStorage; logic in mapEngine.ts -->
<div id="map-intro-modal" style="display:none;">
  <div id="map-intro-inner">
    <h3>How to use the map</h3>
    <ul>
      <li><strong>Min / Maj / 2019</strong> &mdash; switch which commission map you&rsquo;re viewing as the primary layer</li>
      <li><strong>Vote</strong> &mdash; show 2023 election results as partisan colour in each district</li>
      <li><strong>Fill</strong> &mdash; colour districts by their assigned boundaries</li>
      <li><strong>Lines</strong> &mdash; show or hide district boundary edges</li>
      <li><strong>Lock</strong> &mdash; prevent the map from auto-panning when you click a district</li>
      <li><strong>Anomaly</strong> &mdash; highlight the four Airdrie districts and the NW Calgary zone the audit flagged as structurally unusual</li>
    </ul>
    <p><strong>Try this:</strong> Click <em>Anomaly</em> to highlight the boundary anomalies, then click any highlighted district to see its vote data and how it compares across all three maps.</p>
    <button id="map-intro-close">Got it</button>
  </div>
</div>

<style>
  :global {
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-size: 17px;
      line-height: 1.65;
      color: #1a1a1a;
      background: #f9f7f2;
    }

    a { color: #1a5276; }
    a:hover { text-decoration: underline; }

    header {
      background: #1a2e45;
      color: #fff;
      padding: 2.5rem 2rem 2rem;
    }

    .header-inner {
      max-width: 1100px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      gap: 2.5rem;
    }

    .header-text {
      flex: 1;
      min-width: 0;
    }

    header h1 {
      font-size: clamp(1.4rem, 4vw, 2.1rem);
      font-weight: 700;
      letter-spacing: -0.01em;
      line-height: 1.3;
      margin-bottom: 0.5rem;
    }

    header .subtitle {
      font-size: 1rem;
      opacity: 0.78;
    }

    header .badge {
      display: inline-block;
      margin-top: 1rem;
      padding: 0.25rem 0.75rem;
      border: 1px solid rgba(255,255,255,0.4);
      border-radius: 3px;
      font-size: 0.82rem;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: rgba(255,255,255,0.85);
    }

    .header-image {
      flex-shrink: 0;
      max-height: 600px;
      width: auto;
      display: block;
    }

    .cover-note {
      font-size: 0.78rem;
      opacity: 0.62;
      margin-top: 0.85rem;
      line-height: 1.5;
      max-width: 380px;
    }

    nav {
      background: #243b53;
      padding: 0.55rem 1rem;
      text-align: center;
      font-size: 0.88rem;
      position: sticky;
      top: 0;
      z-index: 100;
    }

    nav a {
      color: #a8c7e8;
      margin: 0 0.8rem;
      text-decoration: none;
    }

    nav a:hover { color: #fff; text-decoration: underline; }
    nav a.active { color: #fff; border-bottom: 2px solid rgba(255,255,255,0.6); padding-bottom: 1px; }

    .container {
      max-width: 820px;
      margin: 0 auto;
      padding: 0 1.2rem;
    }

    section { padding: 2.2rem 0 1.8rem; border-bottom: 1px solid #ddd; scroll-margin-top: 50px; }
    section:last-of-type { border-bottom: none; }

    h2 {
      font-size: 1.25rem;
      font-weight: 700;
      margin-bottom: 0.9rem;
      color: #1a2e45;
    }

    h3 {
      font-size: 1rem;
      font-weight: 600;
      margin: 1.3rem 0 0.4rem;
      color: #243b53;
    }

    p { margin-bottom: 0.9rem; }

    .lead {
      font-size: 1.08rem;
      line-height: 1.7;
      color: #333;
    }

    /* Findings cards */
    .findings-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 1rem;
      margin: 1.2rem 0;
    }

    .card {
      background: #f5f5f5;
      border: 1px solid #ddd;
      border-radius: 5px;
      padding: 1.1rem 1.1rem 1rem;
    }

    .card .label {
      font-size: 0.78rem;
      font-weight: 600;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: #666;
      margin-bottom: 0.3rem;
    }

    .card .number {
      font-size: 1.9rem;
      font-weight: 700;
      line-height: 1.1;
      margin-bottom: 0.25rem;
    }

    .card .number.neutral { color: #1a5276; }
    .card .number.flag    { color: #6B35A7; }

    .card .description {
      font-size: 0.86rem;
      color: #555;
      line-height: 1.5;
    }

    /* Summary table */
    .table-wrap { overflow-x: auto; margin: 1.2rem 0; }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
      background: #fff;
      border: 1px solid #ccc;
      border-radius: 4px;
      overflow: hidden;
    }

    th {
      background: #1a2e45;
      color: #fff;
      font-weight: 600;
      padding: 0.55rem 0.8rem;
      text-align: left;
    }

    td {
      padding: 0.5rem 0.8rem;
      border-top: 1px solid #e8e8e8;
      vertical-align: top;
    }

    tr:hover td { background: #f4f6f8; }

    td.flag { color: #6B35A7; font-weight: 600; }
    td.normal { color: #1A7A6E; }

    /* Callout box */
    .callout {
      background: #eaf1f8;
      border-left: 4px solid #1a5276;
      padding: 0.9rem 1.1rem;
      border-radius: 0 4px 4px 0;
      margin: 1.1rem 0;
      font-size: 0.94rem;
    }

    .callout.warning {
      background: #fdfbe4;
      border-left-color: #b7950b;
    }

    /* Links section */
    .links-list {
      list-style: none;
      padding: 0;
    }

    .links-list li {
      padding: 0.4rem 0;
      border-bottom: 1px solid #e8e8e8;
      font-size: 0.94rem;
    }

    .links-list li:last-child { border-bottom: none; }

    .links-list .tag {
      display: inline-block;
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      padding: 0.1rem 0.4rem;
      border-radius: 3px;
      background: #dce6f0;
      color: #1a3550;
      margin-right: 0.4rem;
      vertical-align: middle;
    }

    footer {
      background: #1a2e45;
      color: rgba(255,255,255,0.7);
      padding: 1.6rem 1.5rem;
      text-align: center;
      font-size: 0.82rem;
      margin-top: 1rem;
    }

    footer a { color: rgba(255,255,255,0.85); }

    @media (max-width: 700px) {
      .header-inner { flex-direction: column; gap: 1.5rem; }
      .header-image { max-height: 300px; }
    }

    @media (max-width: 540px) {
      .findings-grid { grid-template-columns: 1fr; }
    }

#zoom-overlay {
    position: fixed; inset: 0; z-index: 9000;
    background: rgba(0,0,0,0.92);
  }
  #zoom-stage {
    position: absolute; inset: 0;
    overflow: hidden;
    cursor: grab;
    touch-action: none;
  }
  #zoom-stage.dragging { cursor: grabbing; }
  #zoom-obj {
    position: absolute; display: block; border: 0;
  }
  #zoom-close {
    position: fixed; top: 1rem; right: 1.4rem; z-index: 9001;
    background: none; border: none;
    color: #fff; font-size: 2.4rem; line-height: 1;
    cursor: pointer; opacity: 0.7;
    transition: opacity 0.15s;
  }
  #zoom-close:hover { opacity: 1; }
  #zoom-instructions {
    position: fixed; bottom: 1.2rem; right: 1.2rem; z-index: 9001;
    background: rgba(0,0,0,0.55); border: 1px solid rgba(255,255,255,0.15);
    border-radius: 6px; padding: 0.55rem 0.8rem;
    color: rgba(255,255,255,0.75); font-size: 0.75rem;
    line-height: 1.7; pointer-events: none;
    backdrop-filter: blur(4px);
  }
  .zi-row { display: flex; align-items: baseline; gap: 0.5rem; }
  .zi-key {
    display: inline-block; min-width: 5.2em;
    font-weight: 700; color: #fff;
    font-size: 0.72rem; letter-spacing: 0.03em;
  }
  .zi-level { margin-bottom: 0.25rem; }
  #zoom-pct { font-weight: 700; color: #fff; font-variant-numeric: tabular-nums; }
  .zi-divider {
    border-top: 1px solid rgba(255,255,255,0.15);
    margin: 0.35rem 0;
  }
  #ed-tooltip {
    display: none; position: fixed; z-index: 9002;
    background: rgba(10,10,10,0.88);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 6px; padding: 0.45rem 0.7rem;
    color: #fff; font-size: 0.76rem; line-height: 1.65;
    pointer-events: none; backdrop-filter: blur(4px);
    white-space: nowrap;
  }
  #ed-tooltip strong { display: block; font-size: 0.8rem; margin-bottom: 0.1rem; }
  /* ── Unified top bar ─────────────────────────────────────────────────────── */
  #top-bar {
    position: absolute;
    top: 10px; left: 10px; right: 52px;
    z-index: 9002;
    display: flex; align-items: center; gap: 5px; flex-wrap: wrap;
    background: rgba(10,12,18,0.88);
    border-radius: 10px; padding: 5px 8px;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.07);
  }
  .tb-group { display: flex; gap: 4px; align-items: center; }
  .tb-sep { width: 1px; height: 16px; background: rgba(255,255,255,0.12); margin: 0 2px; flex-shrink: 0; }
  .tb-btn {
    background: transparent;
    border: 1px solid rgba(255,255,255,0.12);
    color: rgba(255,255,255,0.35);
    font-size: 0.64rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;
    padding: 5px 10px; border-radius: 6px; cursor: pointer;
    transition: background 0.13s, color 0.13s, border-color 0.13s;
    white-space: nowrap;
    -webkit-tap-highlight-color: transparent;
    touch-action: manipulation;
  }
  .tb-btn:hover { border-color: rgba(255,255,255,0.25); color: rgba(255,255,255,0.65); }
  .tb-btn[data-map="minority"].tb-map-primary  { background: rgba(107,53,167,0.4); border-color: #6B35A7; color: #d4b0ff; }
  .tb-btn[data-map="majority"].tb-map-primary  { background: rgba(26,122,110,0.4); border-color: #1A7A6E; color: #8eecd8; }
  .tb-btn[data-map="2019"].tb-map-primary      { background: rgba(80,80,80,0.35);  border-color: #888;   color: #fff; }
  .tb-btn[data-map="minority"].tb-map-overlay  { border-color: rgba(107,53,167,0.7); color: rgba(180,130,255,0.8); }
  .tb-btn[data-map="majority"].tb-map-overlay  { border-color: rgba(26,122,110,0.7); color: rgba(100,210,185,0.8); }
  .tb-btn[data-map="2019"].tb-map-overlay      { border-color: rgba(160,160,160,0.6); color: rgba(210,210,210,0.8); }
  .tb-btn.tb-layer-on { background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.3); color: rgba(255,255,255,0.9); }
  .tb-btn[data-layer="lock"].tb-layer-on { background: rgba(255,200,0,0.12); border-color: rgba(255,200,0,0.45); color: rgba(255,210,60,0.95); }
  @media (max-width: 700px) { #zoom-instructions { display: none; } }
  /* Touch tap callout — bottom-anchored panel */
  #ed-callout {
    position: fixed; z-index: 9003;
    left: 0; right: 0; bottom: 0;
    background: rgba(12,14,20,0.97);
    border-top: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px 18px 0 0;
    padding: 1.1rem 1.4rem 1.8rem;
    backdrop-filter: blur(10px);
    color: #fff;
    pointer-events: none;
    transform: translateY(100%);
    transition: transform 0.22s cubic-bezier(0.4, 0, 0.2, 1);
  }
  #ed-callout.ec-visible { transform: translateY(0); pointer-events: auto; }
  #ec-close {
    position: absolute; top: 0.55rem; right: 0.9rem;
    background: none; border: none;
    color: rgba(255,255,255,0.45); font-size: 1.5rem; line-height: 1;
    cursor: pointer; padding: 0.2rem 0.4rem;
  }
  #ec-close:hover { color: #fff; }
  #ec-header { margin-bottom: 0.85rem; }
  #ec-name { font-size: 1.05rem; font-weight: 600; letter-spacing: 0.01em; }
  #ec-context { font-size: 0.72rem; color: rgba(255,255,255,0.4); margin-top: 0.15rem; }
  #ec-bar {
    display: flex; height: 10px; border-radius: 5px;
    overflow: hidden; margin-bottom: 0.55rem;
  }
  #ec-ucp-bar { background: #142e94; }
  #ec-ndp-bar { background: #e86310; }
  #ec-split {
    display: flex; justify-content: space-between;
    margin-bottom: 0.8rem;
  }
  .ec-party { display: flex; flex-direction: column; gap: 0.1rem; }
  .ec-party.ec-ndp { text-align: right; }
  .ec-pct { font-size: 1.15rem; font-weight: 700; font-variant-numeric: tabular-nums; }
  .ec-ucp .ec-pct { color: #6b8fd4; }
  .ec-ndp .ec-pct { color: #e8934a; }
  .ec-party-name { font-size: 0.7rem; color: rgba(255,255,255,0.5); letter-spacing: 0.06em; text-transform: uppercase; }
  .ec-votes { font-size: 0.75rem; color: rgba(255,255,255,0.55); font-variant-numeric: tabular-nums; }
  #ec-meta {
    font-size: 0.75rem; color: rgba(255,255,255,0.38);
    display: flex; gap: 0.4rem; flex-wrap: wrap; align-items: center;
  }
  .ec-dot { opacity: 0.4; }
  #ec-compare {
    display: none; flex-wrap: wrap; align-items: center;
    gap: 0.5rem; margin-top: 0.65rem;
    padding-top: 0.55rem; border-top: 1px solid rgba(255,255,255,0.1);
    font-size: 0.72rem;
  }
  .ec-cmp-header { color: rgba(255,255,255,0.35); text-transform: uppercase; letter-spacing: 0.06em; font-size: 0.65rem; }
  .ec-cmp-item { display: flex; align-items: center; gap: 0.25rem; }
  .ec-cmp-label {
    font-size: 0.63rem; font-weight: 700; letter-spacing: 0.05em;
    text-transform: uppercase; color: rgba(255,255,255,0.38);
    border: 1px solid rgba(255,255,255,0.18); border-radius: 3px;
    padding: 0.05rem 0.35rem;
  }
  .ec-cmp-val { color: rgba(255,255,255,0.7); font-variant-numeric: tabular-nums; }
  .ec-cmp-unique { color: rgba(255,180,60,0.75); font-style: italic; font-size: 0.68rem; }

  /* Anomaly button */
  .tb-btn[data-anomaly].tb-layer-on {
    background: rgba(255,140,0,0.15);
    border-color: rgba(255,165,0,0.55);
    color: rgba(255,180,30,0.95);
  }

  /* Map onboarding modal */
  #map-intro-modal {
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.58);
    z-index: 500;
    align-items: center;
    justify-content: center;
  }
  #map-intro-inner {
    background: #1a1a2e;
    color: #e0e0e0;
    border-radius: 8px;
    padding: 1.5rem;
    max-width: 430px;
    width: 90%;
    font-size: 0.92rem;
    line-height: 1.6;
    box-shadow: 0 4px 28px rgba(0,0,0,0.55);
  }
  #map-intro-inner h3 { margin: 0 0 0.8rem; font-size: 1.1rem; color: #fff; }
  #map-intro-inner ul { margin: 0 0 0.8rem; padding-left: 1.2rem; }
  #map-intro-inner li { margin-bottom: 0.4rem; }
  #map-intro-inner p { margin: 0 0 1rem; }
  #map-intro-close {
    background: #6B35A7;
    border: none;
    color: #fff;
    padding: 0.5rem 1.4rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.92rem;
    font-weight: 600;
  }
  #map-intro-close:hover { background: #7f46c0; }
  }
</style>
