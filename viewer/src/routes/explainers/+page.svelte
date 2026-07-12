<!--
  Alberta Electoral Boundary Audit — The Fourteen Explainers (Appendices A–N)
  © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>

  One appendix per casing on the main page. Each owns exactly one concept and
  walks a fixed arc: name the confusion, build the concept with one concrete
  example, send the reader back to the casing able to read its number unaided,
  close with what the concept cannot tell you. Content mirrors the appendices
  of reports/public/report_public.md — keep the two in sync.
  English-only for now — content is pending author review before translation.
-->
<svelte:head>
  <title>The Fourteen Explainers · Alberta Electoral Boundary Audit</title>
  <meta name="description" content="Fourteen short explainers — one per evidence casing in the Alberta Electoral Boundary Audit: cracking, packing, neutral ensembles, the prosecutor's fallacy, conventions versus law, and more.">
</svelte:head>

<script lang="ts">
  import { base } from '$app/paths';
</script>

<header>
  <div class="header-inner">
    <a href="{base}/" class="back-link">← Back to audit</a>
    <div class="header-text">
      <div class="site-label">Alberta Electoral Boundary Audit</div>
      <h1>The Fourteen Explainers</h1>
      <p class="meta">Appendices A–N · one concept each · English only for now</p>
    </div>
  </div>
</header>

<main>
  <div class="content">

    <p class="standfirst">
      Each casing in the audit links to one appendix here. Each appendix owns exactly one
      concept, starts from the honest confusion, builds the idea with one concrete example,
      sends you back to the casing's number able to read it unaided — and ends with what the
      concept <em>cannot</em> tell you. They can be read in any order.
    </p>

    <section id="appendix-a">
      <h2>Appendix A — What "cracking" actually does to a vote</h2>
      <p class="confusion"><em>The confusion:</em> "Airdrie voters still vote. Nobody took their ballots. How does drawing lines 'dilute' anything?"</p>
      <p>Imagine a town of 40,000 that mostly votes Orange, sitting in a region that mostly votes Blue. Give the town its own riding and it elects an Orange MLA: 40,000 people, one seat, a voice. Now slice the town into four pieces and staple each piece to a chunk of Blue countryside. In each new riding the town's 10,000 voters face 30,000 rural voters. Orange loses all four. Same voters, same ballots, zero seats. Nothing was stolen from any individual voter; what was taken is the <em>community's</em> ability to elect anyone. That is cracking. The mirror move, packing (Appendix C), stuffs a group into as few ridings as possible so it wins those overwhelmingly and nothing else.</p>
      <p>Now re-read Casing 1: 85,805 people, four ridings, a minority in every one — and the same commission's other draft shows two ridings were enough to satisfy the law.</p>
      <p class="limit"><em>The limit:</em> cracking describes an effect, not a motive. A split can happen because someone wanted dilution — or because other constraints crowded the map. The geometry alone cannot say which.</p>
      <p class="back-anchor"><a href="{base}/#casing-1">↩ Back to Casing 1</a></p>
    </section>

    <section id="appendix-b">
      <h2>Appendix B — Shape analysis, and what s.15(2) protection is for</h2>
      <p class="confusion"><em>The confusion:</em> "All electoral districts look weird. Why do these three shapes matter?"</p>
      <p>Districts follow geography, so lumpy is normal. What shape analysis looks for is <em>work</em> — a boundary doing something no ordinary constraint explains. A corridor that lassoes one neighbourhood into a distant district. An arm reaching into a city's edge. A line extended through land where nobody lives. Alberta's law has a special provision, section 15(2), that lets up to four districts fall below the normal population floor — written for remote districts with strong community ties, like northern ridings serving Indigenous communities across vast distances. Extending a boundary through uninhabited national park to qualify a district for that protection is what the commission's own chair called "a bad faith effort": using a rule written for people who live far apart to protect a line where no one lives at all.</p>
      <p>Now re-read Casing 2: three shapes, flagged by the process's own chair, independently confirmed by tests that had no stake in his fight.</p>
      <p class="limit"><em>The limit:</em> a strange shape is a question, not an answer. One of these shapes has a real, creditable logic underneath — the Banff townsite's placement with Canmore — and the chair's objection survives it anyway, because it was aimed at the empty-park extension the placement does not touch.</p>
      <p class="back-anchor"><a href="{base}/#casing-2">↩ Back to Casing 2</a></p>
    </section>

    <section id="appendix-c">
      <h2>Appendix C — Packing, in a three-district toy example</h2>
      <p class="confusion"><em>The confusion:</em> "Bigger districts have more voters. So what? Everyone still gets one vote."</p>
      <p>Take 12,000 voters, 7,000 Orange and 5,000 Blue, split into three districts of 4,000. Draw them evenly and Orange wins all three. Now redraw: cram 4,000 Orange voters into one district (Orange wins it 100–0), and spread the remaining 3,000 Orange across two districts of 4,000 where Blue's 5,000 give it the edge in both. Same 12,000 voters, same 7,000 Orange majority — but now Orange holds one seat and Blue holds two. That is packing: your opponents' votes get warehoused where they pile up as surplus, wasted on margins they didn't need. The tell is district <em>size and concentration</em>: opponents' districts run big and deep, yours run lean and efficient.</p>
      <p>Now re-read Casing 3: in the one Calgary zone where 13 of 17 districts vote NDP, the minority's districts run 11.5% over the provincial average; the majority's, drawn in the same room, run 2.8%.</p>
      <p class="limit"><em>The limit:</em> oversized districts can also come from honest guesses about growth, or from keeping a community whole. Size asymmetry is the signature packing leaves — and also the signature several innocent choices leave.</p>
      <p class="back-anchor"><a href="{base}/#casing-3">↩ Back to Casing 3</a></p>
    </section>

    <section id="appendix-d">
      <h2>Appendix D — What MAD measures, and why the band exists</h2>
      <p class="confusion"><em>The confusion:</em> "Population Mean Absolute Deviation — is this just statistics for 'the districts aren't identical'?"</p>
      <p>Almost. Every district can't hold exactly the same number of people — communities come in awkward sizes. MAD asks: on average, how far does each district stray from the ideal share? A MAD of 3,180 means districts miss the ideal by about 3,180 people on average; 4,707 means the misses average half again larger. The law tolerates straying — Alberta allows ±25% — because respecting real communities is worth some inequality. That's the bargain: deviation is the currency, and you spend it to buy things like whole towns and sensible boundaries. Which is what makes Casing 4 pointed: the minority map spends 48% more of that currency than the majority — and Casing 1 shows it <em>didn't</em> buy Airdrie's wholeness with it.</p>
      <p>Now re-read Casing 4: wider spread than 99 of every 100 neutral maps, on the one value the statute actually quantifies.</p>
      <p class="limit"><em>The limit:</em> the law ranks nothing inside the band. "Spent more deviation" is an observation about priorities, not a violation — every district on both maps is legal.</p>
      <p class="back-anchor"><a href="{base}/#casing-4">↩ Back to Casing 4</a></p>
    </section>

    <section id="appendix-e">
      <h2>Appendix E — How a data artifact fooled us, and how it was caught</h2>
      <p class="confusion"><em>The confusion:</em> "You published 15%, then said 72%. Why should I trust any of your other numbers?"</p>
      <p>Because of <em>why</em> the number changed. Early in the audit, no official digital boundaries existed for the proposed maps — only PDF images in the commission's reports. The audit traced those images into approximate digital boundaries. Tracing is lossy: a boundary that actually runs along a city limit can end up drawn a few hundred metres off, and a metric that asks "does this border follow the municipal line?" then answers <em>no</em> for borders that really do. Multiply that across a whole map and you manufacture a dramatic, false signal. The day Elections Alberta released official shapefiles, the audit re-ran everything. Most findings survived. This one died, and was retracted in place — the corrections section preserves it permanently.</p>
      <p>Now re-read Casing 5: the retraction is not a stain on the method. It <em>is</em> the method — the same recomputation that killed this finding is what makes the surviving ones credible.</p>
      <p class="limit"><em>The limit:</em> one honest retraction doesn't certify everything else; reproducibility does. Every surviving number can be regenerated from public data and public code, which is the only guarantee worth having.</p>
      <p class="back-anchor"><a href="{base}/#casing-5">↩ Back to Casing 5</a></p>
    </section>

    <section id="appendix-f">
      <h2>Appendix F — The what-if machine, and how to read a percentile</h2>
      <p class="confusion"><em>The confusion:</em> "A million computer maps? A percentile of a simulation? What does that even mean?"</p>
      <p>You can't judge whether a map is unusual without knowing what usual looks like — and for electoral maps, nobody gets to see the alternatives. So the audit built them. An algorithm starts from a legal map and makes a long chain of random legal edits: merge two neighbouring districts, re-split them a random valid way, repeat — 252,500 times over, in four independent chains, 1,010,000 maps in all. No vote data is consulted while drawing; the machine cannot favour anyone because it cannot see anyone. Then you take the real map, measure it, and ask: out of the million neutral maps, how many score this high? If 500,000 do, your map is ordinary. If 66 do, your map is the kind of map that neutral drawing produces 66 times in a million tries.</p>
      <p>Now re-read Casing 6: the majority map at the 78th percentile — ordinary. The minority at the 99.99th — 66 matches in 1,010,000.</p>
      <p class="limit"><em>The limit:</em> the machine respects population and contiguity but not every statutory nicety a real commission weighs, so its percentiles measure distance from <em>neutral drawing</em>, not from <em>everything a lawful commission might do</em>. And a percentile is a distance, not a verdict.</p>
      <p class="back-anchor"><a href="{base}/#casing-6">↩ Back to Casing 6</a></p>
    </section>

    <section id="appendix-g">
      <h2>Appendix G — The efficiency gap, in one worked example</h2>
      <p class="confusion"><em>The confusion:</em> "One number that captures gerrymandering? That sounds too convenient."</p>
      <p>It is, slightly — which is why it gets a threshold and a miss in this report. The idea: every vote that doesn't help win a seat is "wasted" — all votes cast for losers, plus winners' votes beyond the 50%-plus-one they needed. In a fair map both parties waste about equally. The efficiency gap is the difference in wasted votes, as a share of all votes. Suppose in a 100-vote district Orange wins 90–10: Orange wasted 39 (surplus beyond 51), Blue wasted 10 (all losers). Packed and cracked maps make one party waste systematically more. Positive gaps favour conservatives in this report's sign convention; the audit's Alberta calibration line (~4.1%) is the level only 5% of the million neutral maps cross.</p>
      <p>Now re-read Casing 7: minority at +4.0%, 94th percentile — below the audit's own pre-registered line, reported as the miss it is.</p>
      <p class="limit"><em>The limit:</em> the efficiency gap compresses a whole map into one number, and one number can't distinguish a gerrymander from geography being lumpy. That's why this audit uses four metrics and a locked threshold — and keeps the miss on the books.</p>
      <p class="back-anchor"><a href="{base}/#casing-7">↩ Back to Casing 7</a></p>
    </section>

    <section id="appendix-h">
      <h2>Appendix H — The prosecutor's fallacy, in plain language</h2>
      <p class="confusion"><em>The confusion:</em> "One in 357,000 that this map is innocent. That's the finding, right?"</p>
      <p>No — and the difference matters enough to have a name. The number says: <em>if</em> a neutral process drew Alberta's map, the chance it would look like the minority map is at most one in 357,000. That is P(this evidence, given innocence). It is not P(innocence, given this evidence) — and swapping them is the prosecutor's fallacy. Classic example: a suspect matches a DNA profile found at a scene, and the profile occurs in one in a million people. "One in a million chance he's innocent"? Wrong. In a city of ten million, about ten people match; on the DNA alone, the suspect is one of ten — a 90% chance <em>someone else</em> matches too. The rarity of the evidence under innocence is not the probability of innocence, because you also need to know how many innocent ways the evidence could arise.</p>
      <p>Now re-read Casing 8: the audit states the number it can defend — the rarity of the map under neutral drawing — and refuses the swap that would turn it into a verdict.</p>
      <p class="limit"><em>The limit:</em> refusing the fallacy costs the audit its most quotable sentence, and that cost is deliberate. Rarity is evidence. It is not, and never becomes, proof of intent.</p>
      <p class="back-anchor"><a href="{base}/#casing-8">↩ Back to Casing 8</a></p>
    </section>

    <section id="appendix-i">
      <h2>Appendix I — What a sampler is, and why swapping it matters</h2>
      <p class="confusion"><em>The confusion:</em> "You checked your simulation with… another simulation? How is that a check?"</p>
      <p>Because the two machines are built differently, and artifacts don't usually survive a change of machinery. Any map-drawing algorithm has quirks — the standard one (ReCom) has a documented lean toward compact, tidy districts, which could in principle exaggerate how extreme a sprawling real map looks. So the audit swapped the engine: a variant that grows districts from random spanning <em>forests</em> instead of trees, with measurably different internal behaviour, registered publicly (OSF he53s) before a single map was drawn with it, seeds derived from a public randomness beacon anyone can verify. If the minority's tail position were an artifact of the first engine's quirks, the second engine would move it. It moved less than one percentile point on every metric — a pre-registered ROBUST verdict. The audit also reports the check that <em>failed</em>: the claim that Act I's flagged geometry is the specific mechanism behind the seat numbers did not survive testing, and was dropped.</p>
      <p>Now re-read Casing 9: three attacks, two survived, one claim honestly lost.</p>
      <p class="limit"><em>The limit:</em> robustness rules out tooling artifacts. It cannot rule in design — a genuinely extreme map is genuinely extreme whatever produced it.</p>
      <p class="back-anchor"><a href="{base}/#casing-9">↩ Back to Casing 9</a></p>
    </section>

    <section id="appendix-j">
      <h2>Appendix J — Why neighbours voting alike breaks naive statistics</h2>
      <p class="confusion"><em>The confusion:</em> "A test gave p = 0.0024 and you threw it away? That looks like hiding a result."</p>
      <p>The opposite — it's correcting one. Many tests assume observations are independent, like separate coin flips. Voting areas aren't: neighbouring areas share demographics, incomes, histories — they vote alike. Treating 100 clustered areas as 100 independent flips is really more like 20 informative observations wearing 100 coats, and it makes coincidences look impossible when they're merely uncommon. The fix is to build a null that preserves the clustering — shuffle <em>blocks</em> of neighbouring areas together rather than each area separately — and ask the question again. The audit's swing-zone test looked significant under the naive null (p = 0.0024) and unremarkable under the corrected one (p ≈ 0.19). When the honest null disagrees with the flattering one, you keep the honest null and retire the result.</p>
      <p>Now re-read Casing 10: two of the audit's own instruments retired, one pre-registered test the minority map outright passed.</p>
      <p class="limit"><em>The limit:</em> the correction shows the <em>boundary-choice</em> signal doesn't stand — it says nothing against the ensemble findings, which never assumed independence in the first place.</p>
      <p class="back-anchor"><a href="{base}/#casing-10">↩ Back to Casing 10</a></p>
    </section>

    <section id="appendix-k">
      <h2>Appendix K — How to check a stated reason against public data</h2>
      <p class="confusion"><em>The confusion:</em> "Commissioners are the experts. Who is an audit to grade their reasons?"</p>
      <p>Nobody special — and that's the point: the check requires no special access. The minority report says Cochrane residents "move fluidly" into Calgary; Statistics Canada's journey-to-work tables (free, public) show about a third of Cochrane's workers commute into Calgary while roughly half work in Cochrane — a real tie, and one that says nothing about the specific Nolan Hill corridor drawn. The report implies shared schools link Red Deer and Sylvan Lake; the two towns' school-division boundaries (also public) put them in different divisions. Each check follows the same recipe: take the stated reason, find the public dataset that would show it, and see whether the <em>particular line drawn</em> is the line the data supports. Five of six checked rationales fail that last step — the tie is real, the line is not the one the tie points to.</p>
      <p>Now re-read Casing 11 — and notice the audit retracted one of its own seven claims by the same standard, when the source couldn't be located.</p>
      <p class="limit"><em>The limit:</em> a rationale that fails checking proves the <em>stated</em> reason doesn't fit. It cannot reveal the real one — sloppiness and pretext leave identical paperwork.</p>
      <p class="back-anchor"><a href="{base}/#casing-11">↩ Back to Casing 11</a></p>
    </section>

    <section id="appendix-l">
      <h2>Appendix L — How commissioners are appointed, and what nomination implies</h2>
      <p class="confusion"><em>The confusion:</em> "Government-nominated commissioners drew the government-favouring map. Case closed, surely?"</p>
      <p>Alberta's commission is built from nominations: a chair, plus commissioners nominated from government and opposition sides — a design that assumes partisan perspectives and balances them, betting that a mixed room converges on one defensible map. For decades the bet paid: commissions signed consensus reports. This cycle the room split along its nomination lines, and the government's nominees produced the statistical outlier. That correlation is real and worth recording. It is also exactly where the inference must stop. Nominated commissioners are not agents; no evidence in this audit's record shows the government directed, coordinated with, or even knew the shape of its nominees' map before filing. History is full of nominees who disappointed their nominators. The correlation invites a question — it cannot answer it, and the audit's instruments cut against the chair's side too when the data went that way, which is what symmetric measurement means.</p>
      <p>Now re-read Casing 12: the split is the anomaly; the provenance is the question mark, not the answer.</p>
      <p class="limit"><em>The limit:</em> appointment provenance is context, never proof. Treating it as proof is the same fallacy as Appendix H, wearing a political coat.</p>
      <p class="back-anchor"><a href="{base}/#casing-12">↩ Back to Casing 12</a></p>
    </section>

    <section id="appendix-m">
      <h2>Appendix M — The Act's process, commission to committee, end to end</h2>
      <p class="confusion"><em>The confusion:</em> "How can the legislature just… take over redistricting? Isn't the commission's map the map?"</p>
      <p>No — and this is the load-bearing surprise of the whole episode. Under Alberta's <em>Electoral Boundaries Commission Act</em>, the commission proposes; only the Legislative Assembly disposes. The commission's final report — hearings, submissions, revisions and all — is advice. It has no legal effect until the Assembly enacts a map, and the Act places almost no constraints on what the Assembly does instead: no minimum debate, no notice period, no obligation to prefer the commission's work, no hearing requirement for whatever process follows. Section 12 lets the Assembly refer the work onward — which is what Motion 19 did, to a select committee. Select committees of the Assembly are composed of MLAs; independence was excluded by the choice of vehicle itself, lawfully. Every previous cycle, the Assembly's restraint — not the statute — was what kept politicians' hands off the pen.</p>
      <p>Now re-read Casing 13: sixteen communities of hearings replaced by a body required to hold none. All of it inside the Act.</p>
      <p class="limit"><em>The limit:</em> this appendix explains what the law permits. Whether what the law permits is what Albertans should accept is a political question — the one the November tests are built to inform.</p>
      <p class="back-anchor"><a href="{base}/#casing-13">↩ Back to Casing 13</a></p>
    </section>

    <section id="appendix-n">
      <h2>Appendix N — Conventions versus law, and how norms erode</h2>
      <p class="confusion"><em>The confusion:</em> "If politicians drawing their own districts violates our deepest electoral norm, how can it be legal?"</p>
      <p>Because Canada's constitution runs on two operating systems. One is law: written, justiciable, enforced by courts. The other is convention: unwritten rules of political behaviour — binding in practice, invisible to a courtroom. The Supreme Court described the divide in the 1981 Patriation Reference: courts may <em>recognize</em> a convention and will still decline to <em>enforce</em> it, because conventions are policed politically — by opposition, press, and voters — not judicially. Independent boundary commissions live on the convention side. Sixty years of practice, in every province and federally, built the rule that politicians do not draw their own ridings; no statute anywhere makes that rule mandatory. Which means the guardrail's entire strength was that governments kept choosing to honour it. A norm violated once, without consequence, is weaker for every government that follows — of any party.</p>
      <p>Now re-read Casing 14: real violation, fully documented, judicially irrelevant — all three at once.</p>
      <p class="limit"><em>The limit:</em> "unenforceable" is a statement about courts, not about consequences. Conventions are enforced at elections, by people who know what was done. Reports like this one exist so they know.</p>
      <p class="back-anchor"><a href="{base}/#casing-14">↩ Back to Casing 14</a></p>
    </section>

    <p class="footer-note">
      Content mirrors the appendices of the
      <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/public/report_public.md" rel="noopener">full public report</a>.
      English only for now, pending author review before translation.
    </p>

  </div>
</main>

<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :global(body) {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 17px;
    line-height: 1.65;
    color: #1a1a1a;
    background: #f9f7f2;
  }
  :global(:root[data-theme="dark"] body) {
    color: #dde2ed;
    background: #1e1f26;
  }

  header {
    background: #1a2e45;
    color: #fff;
    padding: 2rem clamp(1.2rem, 4vw, 3.5rem);
  }
  :global(:root[data-theme="dark"]) header { background: #111722; }

  .header-inner { max-width: 760px; margin: 0 auto; }

  .back-link {
    display: inline-block;
    color: rgba(255,255,255,0.6);
    text-decoration: none;
    font-size: 0.85rem;
    margin-bottom: 1.1rem;
    padding: 4px 0;
    transition: color 0.15s;
  }
  .back-link:hover { color: #fff; }

  .site-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: rgba(255,255,255,0.55);
    margin-bottom: 0.35rem;
  }

  h1 { font-size: clamp(1.5rem, 4vw, 2.1rem); line-height: 1.2; }

  .meta { font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-top: 0.5rem; }

  main { padding: 2.2rem clamp(1.2rem, 4vw, 3.5rem) 4rem; }

  .content { max-width: 760px; margin: 0 auto; }

  .standfirst {
    font-size: 1.08rem;
    line-height: 1.7;
    margin-bottom: 2rem;
    color: #333;
  }
  :global(:root[data-theme="dark"]) .standfirst { color: #c4cad8; }

  section { margin-bottom: 2.6rem; }

  h2 {
    font-size: 1.22rem;
    line-height: 1.35;
    margin-bottom: 0.8rem;
    padding-top: 0.5rem;
  }

  p { margin-bottom: 0.9rem; }

  .confusion { color: #555; }
  :global(:root[data-theme="dark"]) .confusion { color: #a8b0c0; }

  .limit {
    border-inline-start: 3px solid #b8860b;
    padding: 0.4rem 0 0.4rem 0.9rem;
    color: #444;
  }
  :global(:root[data-theme="dark"]) .limit { color: #b8c0d0; }

  .back-anchor { font-size: 0.9rem; }
  .back-anchor a, a { color: #1a5c8f; }
  :global(:root[data-theme="dark"]) a { color: #7db3e0; }

  .footer-note {
    margin-top: 3rem;
    padding-top: 1.2rem;
    border-top: 1px solid rgba(128,128,128,0.3);
    font-size: 0.85rem;
    color: #666;
  }
  :global(:root[data-theme="dark"]) .footer-note { color: #98a0b0; }
</style>
