<!--
  Alberta Electoral Boundary Audit — How the Maps Were Tested
  © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>

  Rewritten 2026-07-13 as the grade-8 walkthrough of every test and statistic
  (author directive). Replaces the prior version, which carried three stale or
  retracted claims: "1 in 714,000" (pre-C10 parametric p), "66 of 1,010,000"
  (pre-C10 exceedance count), and "zero in 1,010,000 is an assumption-free
  statement" (the exact framing retracted in the 2026-07-10 dependence-honesty
  correction — autocorrelated chains mean 0 exceedances honestly supports far
  less). Also fixes the quarter-scale --n-steps 252500 reproduce command.

  Content grounded in: data/outputs/simulation_real_map_scores_canonical.json,
  data/outputs/simulated_ensemble_percentiles_canonical.csv,
  data/outputs/simulation_convergence_diagnostics_canonical.json,
  reports/academic/report_academic.md (C10-C13 era), reports/public/report_public.md.
  Every number here must match those artifacts; update them together.
  English-only for now — content is pending author review before translation.

  Voice target: Flesch-Kincaid grade ~8. Short sentences. Everyday analogies.
-->
<svelte:head>
  <title>How the Maps Were Tested · Alberta Electoral Boundary Audit</title>
  <meta name="description" content="Every test and statistic in the audit, explained in plain language: the million-map what-if machine, the five structural tests, the four fairness measures, p-values, and the tests that died.">
</svelte:head>

<script lang="ts">
  import { base } from '$app/paths';
</script>

<header>
  <div class="header-inner">
    <a href="{base}/" class="back-link">← Back to audit</a>
    <div class="header-text">
      <div class="site-label">Alberta Electoral Boundary Audit</div>
      <h1>How the Maps Were Tested</h1>
      <p class="meta">Every test and every statistic, in plain language · English only for now · Every number reproducible from the public repository</p>
    </div>
  </div>
</header>

<main>
  <div class="content">

    <p class="standfirst">
      The whole audit rests on one simple idea. If you want to know whether a map is unusual,
      draw a million maps that could not be biased — a computer draws them, and it never sees
      a single vote — then check where the real maps land among them. This page walks through
      that idea and every test built on it. No formulas. If you can read a weather forecast,
      you can read this.
    </p>

    <nav class="toc" aria-label="Page contents">
      <a href="#what-if">The what-if machine</a>
      <a href="#percentile">How to read a percentile</a>
      <a href="#structural">The five structural tests</a>
      <a href="#fairness">The four fairness measures</a>
      <a href="#odds">What the odds mean</a>
      <a href="#died">The tests that died</a>
      <a href="#break">Trying to break our own result</a>
      <a href="#prereg">Promises made in advance</a>
      <a href="#reproduce">Run it yourself</a>
    </nav>

    <section id="what-if">
      <h2>The what-if machine: 1,010,000 neutral maps</h2>
      <p>
        A computer drew <strong>1,010,000 legal Alberta maps</strong>. Each one follows the same
        two hard rules the real commission followed: every district holds close to the same
        number of people (within 25% of the average), and every district is one connected piece.
      </p>
      <p>
        How does a computer draw a map? One small step at a time. Take two districts that share
        a border. Merge them into one blob. Split the blob back into two new legal districts,
        at random. Repeat, 1,010,000 times, saving the map after each step. The method is called
        ReCom, and it is the standard tool in this field.
      </p>
      <p>
        The key fact: <strong>the computer never sees a vote.</strong> It does not know where NDP
        or UCP voters live. So if a neutral map still leans one way, that lean comes from
        Alberta's geography alone — and if a real map leans much further than nearly all the
        neutral ones, geography can no longer be the explanation.
      </p>
      <p>Three honesty points about the machine:</p>
      <ul>
        <li>
          <strong>The dice were rolled in public.</strong> The random seed was not picked by the
          author. It comes from a public randomness beacon (Cloudflare's "drand"), like a
          lottery draw broadcast live. It was locked in before the official map files existed.
          Anyone can recompute it.
        </li>
        <li>
          <strong>Four separate runs agree.</strong> The million maps came from four independent
          runs, each starting differently. All four settled on the same picture. The standard
          checks for this (used across the field) pass with room to spare.
        </li>
        <li>
          <strong>The machine is not a perfect referee.</strong> It follows the two hard rules,
          but not every soft rule real commissions honour — like keeping communities together.
          Real commission maps are actually tidier than most neutral maps. The audit says this
          plainly everywhere the machine's numbers appear.
        </li>
      </ul>
    </section>

    <section id="percentile">
      <h2>How to read a percentile</h2>
      <p>
        Line up all 1,010,000 neutral maps from least UCP-leaning to most UCP-leaning. Now
        place a real map in the line. Its <strong>percentile</strong> is just its position:
        "78th percentile" means it leans further than 78 out of every 100 neutral maps. That is
        unremarkable — a bit above the middle of the pack.
      </p>
      <p>
        "99.99th percentile" is different. It means the map out-leans virtually every neutral
        map in the line — in this audit, all but <strong>69 of the 1,010,000</strong>. Height
        works the same way: a man at the 78th percentile is a bit tall; a man at the 99.99th
        percentile is about seven feet.
      </p>
    </section>

    <section id="structural">
      <h2>The five structural tests (no votes needed)</h2>
      <p>
        Before any simulation, the audit measured the drawn lines themselves. Five tests, all
        locked in before the results were known. Each compares the two commission maps directly.
      </p>
      <ul>
        <li>
          <strong>1. Population spread.</strong> How far do districts drift from the ideal size?
          On the commission's own tables, the majority map's typical drift is 3,180 people; the
          minority map's is 4,707 — about half again wider. Wider drift means votes count less
          equally.
        </li>
        <li>
          <strong>2. Calgary crowding.</strong> In north-east and central Calgary, the minority
          map's districts run 11.5% bigger than the provincial average. The majority's run 2.8%
          bigger. Bigger districts mean each vote inside them weighs less — and this zone votes
          heavily NDP. The pattern is called <em>packing</em>.
        </li>
        <li>
          <strong>3. The Airdrie split.</strong> The law forces Airdrie into at least two
          districts. The majority map uses two. The minority map cuts the city into four pieces,
          each attached to different outside territory. Splitting a community thin is called
          <em>cracking</em>.
        </li>
        <li>
          <strong>4. The chair's flags.</strong> The commission's own chair publicly flagged
          boundaries as geographically strange. Three of his flags land on the minority map.
          Zero land on the majority map.
        </li>
        <li>
          <strong>5. Following city limits (the test that died).</strong> Early data suggested
          the minority map ignored municipal lines. Official map files killed that finding:
          both maps follow city limits at normal Canadian rates (80% and 72%). The audit keeps
          the dead test on display instead of deleting it.
        </li>
      </ul>
      <p>
        Score: the minority map crosses all four live thresholds. The majority map crosses none.
      </p>
    </section>

    <section id="fairness">
      <h2>The four fairness measures (votes added)</h2>
      <p>
        Now add the 2023 votes and ask: how does each map turn votes into seats? Four standard
        measures, each checked against the million neutral maps.
      </p>
      <ul>
        <li>
          <strong>1. Seats at a tied vote.</strong> The most intuitive test. Pretend the
          province votes exactly 50/50 and count each side's seats. On Alberta's geography a
          typical neutral map gives the UCP about 44.8% of seats at a tie — city NDP votes are
          used a little more efficiently, so a tie naturally favours the NDP slightly. The
          majority map gives the UCP 46.1% — 78th percentile, ordinary. The minority map gives
          the UCP <strong>51.7%</strong> — a majority of seats while tied in votes. Only 69 of
          the 1,010,000 neutral maps do better for the UCP. For scale, a procedure told to
          <em>deliberately</em> maximize UCP seats reached 52.9%. The minority map sits closer
          to that engineered ceiling than to the neutral middle.
        </li>
        <li>
          <strong>2. The efficiency gap.</strong> Every vote is either needed to win a seat or
          "wasted" — cast for a loser, or piled onto a winner beyond what victory required.
          This measure compares how fast each party's votes are wasted. The majority map scores
          +0.1% — essentially nothing. The minority scores +4.0% in the UCP's favour — the
          94.5th percentile, just <em>under</em> the audit's pre-set alarm line at the 95th.
          This is the one measure that did not fire, and the audit reports it as a miss.
        </li>
        <li>
          <strong>3. The mean-median gap.</strong> Compare a party's average district result
          with its middle district result. When the two drift apart, votes are being bunched
          into blowouts somewhere. The minority map's gap favours the UCP more than 99.9% of
          neutral maps. The majority's gap leans the other way — mildly NDP-efficient — which
          matches how tidy commission maps behave on Alberta's geography.
        </li>
        <li>
          <strong>4. Declination.</strong> A geometry reading of win margins: does the map treat
          the two parties' wins alike, or does it bend at the 50% line? The minority map bends
          in the UCP's favour more than 98.8% of neutral maps. The majority map reads normal.
          (An early version of this measure had its sign flipped by a coding error; the
          correction is documented, not erased.)
        </li>
      </ul>
      <p>
        Score: three of four fire on the minority map, all in the same direction, and the fourth
        lands just under the line — also in the same direction. The majority map is ordinary on
        all four.
      </p>
    </section>

    <section id="odds">
      <h2>What "1 in 568,000" means — and why the audit doubled its margin</h2>
      <p>
        Combine the four fairness measures into one score and ask: how often does neutral
        drawing produce a profile as extreme as the minority map's? The answer is about
        <strong>1 in 1.1 million</strong>. But the audit does not quote that number. It quotes
        <strong>1 in 568,000</strong> — exactly half as impressive. Here is why.
      </p>
      <p>
        The audit looked for a signal in two different places: this combined score, and a second
        test on the specific boundary choices. Looking in two places gives luck two chances.
        Think of lottery tickets: buy two, and your odds of holding a winner double. So before
        quoting the odds, the audit doubles them against itself. That way, "you had two tries"
        is already paid for.
      </p>
      <p>
        The doubling has one more virtue: it needs no assumptions. It holds whether the two
        tests are related or not. An earlier version of this audit combined the two tests with
        a method that <em>assumed</em> they were unrelated, and got "1 in 15 million." The two
        tests share the same vote data, so that assumption was wrong, and the number was
        retired. What is left is the number a hostile statistician could not beat down.
      </p>
      <p>
        One caution the audit repeats everywhere: these odds measure how unusual the
        <em>map</em> is. They are not the odds that anyone acted with intent. A rare map could
        still, in principle, be honest work. The odds say only this: routine drafting does not
        produce this map.
      </p>
    </section>

    <section id="died">
      <h2>The tests that died</h2>
      <p>
        Three findings did not survive, and all three stay in print. That is on purpose: an
        audit that only shows you its wins is advertising.
      </p>
      <ul>
        <li>
          <strong>The city-limits test</strong> died when official map files replaced early
          traced ones. The scary early number was an artifact of the tracing.
        </li>
        <li>
          <strong>The boundary-choices test (SZAT)</strong> looked significant until the audit
          corrected it for a simple fact: neighbouring places vote alike. Treating neighbours
          as independent flatters the result. After the correction, the test showed nothing.
          It was retired.
        </li>
        <li>
          <strong>The "1 in 15 million" figure</strong> assumed two tests were unrelated when
          they were not. Retired and replaced by the cautious 1 in 568,000.
        </li>
      </ul>
    </section>

    <section id="break">
      <h2>Trying to break our own result</h2>
      <p>
        Before trusting the headline, the audit attacked it three ways.
      </p>
      <ul>
        <li>
          <strong>Swap the engine.</strong> Rerun everything with a completely different
          map-drawing algorithm (a spanning-forest method, promised in public before running).
          Every result moved by less than one percentile point. The finding survived.
        </li>
        <li>
          <strong>Swap the software.</strong> An independent implementation in a different
          programming language was tried on early data and behaved unstably; on official files
          the question became moot — no plans from either implementation reach the minority
          map's value.
        </li>
        <li>
          <strong>Test the mechanism — and fail.</strong> The audit guessed that the strange
          shapes from the structural tests were the direct cause of the seat advantage. That
          guess failed its test. The shapes and the seat lean point at the same map, but the
          shapes are not the engine. The audit says so.
        </li>
      </ul>
    </section>

    <section id="prereg">
      <h2>Promises made in advance</h2>
      <p>
        The strongest defence against fooling yourself is to write your predictions down before
        you look. The audit locked its tests, thresholds, and predicted directions into public,
        time-stamped registrations (on the Open Science Framework) — and locked its random
        seeds to a public beacon — before the official map files were released. When a locked
        prediction missed, it stayed a miss. The same locked tests will be run, unchanged, on
        the committee's new map when it lands in November 2026. The audit also names which of
        its results are <em>exploratory</em> (seeds locked, but the exact test combination
        chosen later) versus fully pre-registered. The headline odds are exploratory; the
        November scorecard is the fully pre-registered test.
      </p>
    </section>

    <section id="reproduce">
      <h2>Run it yourself</h2>
      <p>
        Every number on this site comes from a script in the public repository run against
        committed data. The full recipe is in
        <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/docs/REPRODUCING.md" rel="noopener">REPRODUCING.md</a>;
        the short version:
      </p>
      <pre><code>git clone https://github.com/Ixby/alberta-electoral-boundaries-audit.git
cd alberta-electoral-boundaries-audit
git lfs install &amp;&amp; git lfs pull
pip install -r requirements.txt

# regenerate the 1,010,000-map ensemble (long-running; checkpointed;
# --n-steps is the TOTAL across 4 chains)
python analysis/scripts/mcmc_ensemble_canonical.py --n-steps 1010000

# score the real maps against the ensemble
python analysis/scripts/joint_outlier_score_canonical.py</code></pre>
      <p>
        A hosted notebook version runs in the browser via
        <a href="https://colab.research.google.com/github/Ixby/alberta-electoral-boundaries-audit/blob/master/notebooks/alberta_audit_explorer.ipynb" rel="noopener">Google Colab</a>.
        The full methodology — including every retraction and correction along the way — is in
        the <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">academic monograph</a>.
      </p>
      <p class="cross-ref">
        Companion pages: <a href="{base}/law">What the law asks of an electoral map</a> ·
        <a href="{base}/explainers">The fourteen explainers (Appendices A–N)</a>, one for each
        casing in the main report.
      </p>
    </section>

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

  h1 {
    font-size: clamp(1.4rem, 4vw, 1.9rem);
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.25;
    margin-bottom: 0.4rem;
  }

  .meta { font-size: 0.82rem; color: rgba(255,255,255,0.55); }

  main { padding: 2.2rem clamp(1.2rem, 4vw, 3.5rem) 4rem; }
  .content { max-width: 760px; margin: 0 auto; }

  .standfirst {
    font-size: 1.06rem;
    color: #3a3a38;
    border-inline-start: 3px solid #1a2e45;
    padding-inline-start: 1rem;
    margin-bottom: 1.6rem;
  }
  :global(:root[data-theme="dark"]) .standfirst {
    color: #b9c0d0;
    border-inline-start-color: #4a6690;
  }

  .toc {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem 0.9rem;
    font-size: 0.88rem;
    margin-bottom: 2.2rem;
    padding: 0.7rem 0.9rem;
    background: rgba(26, 46, 69, 0.05);
    border-radius: 6px;
  }
  :global(:root[data-theme="dark"]) .toc { background: rgba(255,255,255,0.05); }
  .toc a { text-decoration: none; }
  .toc a:hover { text-decoration: underline; }

  section { margin-bottom: 2.4rem; scroll-margin-top: 1.5rem; }

  h2 {
    font-size: 1.22rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
    letter-spacing: -0.01em;
  }

  p { margin-bottom: 0.9rem; }

  ul { margin: 0 0 0.9rem 1.4rem; }
  li { margin-bottom: 0.7rem; }

  a { color: #1a5276; }
  :global(:root[data-theme="dark"]) a { color: #7fb3d5; }

  .cross-ref { font-size: 0.92rem; color: #55554f; }
  :global(:root[data-theme="dark"]) .cross-ref { color: #9aa3b5; }

  pre {
    background: #14181f;
    color: #d8dee9;
    padding: 1rem 1.2rem;
    border-radius: 8px;
    overflow-x: auto;
    font-size: 0.84rem;
    line-height: 1.55;
    margin-bottom: 0.9rem;
  }
  code { font-family: ui-monospace, SFMono-Regular, "Cascadia Mono", Consolas, monospace; }
</style>
