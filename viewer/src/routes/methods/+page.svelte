<!--
  Alberta Electoral Boundary Audit — How the Maps Were Tested
  © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>

  Content grounded in: data/outputs/simulation_real_map_scores_canonical.json,
  data/outputs/simulated_ensemble_percentiles_canonical.csv,
  findings/joint_empirical_bound_verification.json (2026-07-08/09 verification
  runs), reports/academic/report_academic.md §4.3.3 / §5.4.9 / §5.4.10, and the
  public report's vocabulary boxes. Every number here must match those
  artifacts; update them together. English-only for now — content is pending
  author review before translation.
-->
<svelte:head>
  <title>How the Maps Were Tested · Alberta Electoral Boundary Audit</title>
  <meta name="description" content="The audit's methodology in plain language: the 1,010,000-map neutral ensemble, the four partisan-fairness metrics, what they can and cannot show, and how to reproduce every number.">
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
      <p class="meta">Plain-language companion · English only for now · Every number reproducible from the public repository</p>
    </div>
  </div>
</header>

<main>
  <div class="content">

    <p class="standfirst">
      The audit's central instrument is a simple idea: if you want to know whether a map is
      unusual, draw a million maps that <em>couldn't</em> be biased — because a computer drew
      them with no knowledge of where anyone votes for whom — and see where the real maps land
      among them. This page explains that instrument, the four fairness measurements taken with
      it, what the results can and cannot support, and how to re-run all of it yourself.
    </p>

    <section id="ensemble">
      <h2>The ensemble: 1,010,000 neutral maps</h2>
      <p>
        The audit generated <strong>1,010,000 neutral Alberta maps</strong> — four independent
        chains of 252,500 each — using the ReCom algorithm (DeFord, Duchin &amp; Solomon 2021)
        as implemented in the open-source GerryChain library. Each neutral map divides the same
        official Elections Alberta geography into 89 contiguous districts within the same ±25%
        population band the real commission worked under. The algorithm never sees a vote total
        while drawing, so any partisan lean a neutral map has comes from Alberta's geography
        alone.
      </p>
      <p>
        Three design choices matter for trusting the result:
      </p>
      <ul>
        <li>
          <strong>The randomness is publicly verifiable.</strong> The random seed (1432864451)
          was not chosen by the author: it is derived by hashing a published round of the
          Cloudflare/League of Entropy "drand" public randomness beacon — a value no one can
          influence or select after the fact. Anyone can recompute it.
        </li>
        <li>
          <strong>The chains demonstrably converged.</strong> Four independent chains starting
          from different random walks agree with each other: the Gelman–Rubin diagnostic on the
          full run is below even the strict 1.01 recommendation on all four metrics, with
          effective sample sizes of roughly 1,400–1,700 per metric after accounting for
          autocorrelation.
        </li>
        <li>
          <strong>The headline does not depend on a statistical model.</strong> The minority
          map's joint fairness profile was compared against every one of the 1,010,000 neutral
          maps directly: not one reaches it. That count — zero in 1,010,000 — is an
          assumption-free statement. The parametric figure the audit reports (about 1 in
          714,000) is the <em>more conservative</em> of the two.
        </li>
      </ul>
      <div class="honesty-box">
        <strong>What the ensemble is not.</strong> The neutral maps satisfy contiguity and the
        population band, but they do not enforce everything a real commission honours — the
        s.15(2) criteria, communities of interest, municipal coherence. The audit therefore
        calls its baseline a "ReCom-typical" null, not a "commission-typical" one, and reads
        every tail position against that unconstrained distribution. Both real maps are, for
        instance, more compact and more municipally anchored than almost all neutral maps —
        exactly what you would expect from commission work. A constraint-enforcing ensemble is
        listed as future work in the monograph. Note also the audit's own classification: the
        headline statistic is <em>exploratory</em> — the random seeds were publicly committed
        before the official shapefiles existed, but the specific test combination was not
        registered in advance. The prospectively pre-registered confirmatory test is the
        November 2026 committee-map scorecard (OSF: qsgy8).
      </div>
    </section>

    <section id="efficiency-gap">
      <h2>Efficiency gap</h2>
      <p>
        Every vote is either needed to win a seat or "wasted" — cast for a loser, or piled onto
        a winner's surplus. The efficiency gap totals each party's wasted votes and expresses
        the difference as a share of all votes. A positive value in this audit means the map
        wastes NDP votes faster than UCP votes — a UCP-favourable tilt.
      </p>
      <p>
        Because Alberta's geography is not neutral (the neutral maps themselves average a
        mildly UCP-favourable gap), the audit calibrates its outlier line to Alberta rather
        than borrowing the US literature's 7% threshold (which no court has adopted): the line
        sits at <strong>+4.1%</strong>, the value only 5% of the 1,010,000 neutral maps exceed.
        On official shapefiles the majority map scores <strong>+0.1%</strong> (15th percentile
        — utterly ordinary) and the minority <strong>+4.0%</strong> (94th percentile — near,
        but below, the line). The efficiency gap is the one partisan metric on which the
        minority map is <em>not</em> flagged, and the audit reports it that way.
      </p>
    </section>

    <section id="mean-median">
      <h2>Mean–median gap</h2>
      <p>
        Take a party's vote share in each of the 89 districts; compare the average with the
        median. When a party wins its seats efficiently (many narrow wins), the median sits
        above the mean; when its votes are packed into blowouts, the mean is dragged away from
        the median. The gap between the two is a compact skew detector.
      </p>
      <p>
        Here the two 2026 maps split in opposite directions. The minority map's mean–median of
        <strong>+1.0%</strong> is more UCP-favourable than 99.98% of neutral maps. The majority
        map sits at the other tail (−3.6%, more NDP-lean than almost all neutral maps) — an
        outlier the audit attributes to the ReCom-typical null rather than to drawing choices:
        real commission maps preserve rural low-NDP districts that unconstrained neutral maps
        merge and dissolve, and the monograph applies that discount symmetrically to both maps'
        tail readings.
      </p>
    </section>

    <section id="declination">
      <h2>Declination</h2>
      <p>
        Declination (Warrington 2018) reads the geometry of a map's win margins. Line the 89
        districts up by one party's vote share and look at the picture on either side of the
        50% line: declination measures the angle between the two halves — how differently the
        map treats each party's wins. A map treating both sides alike scores near zero; a map
        that bends at the 50% line does not. In this audit's sign convention, positive
        declination favours the UCP.
      </p>
      <p>
        The minority map's declination of <strong>+0.077</strong> lands at the 98.8th
        percentile of the neutral ensemble — a flagged UCP-favourable outlier. The majority's
        (−0.027) sits at the 20th percentile, inside the normal range. One transparency note
        the audit keeps in print: an early version computed this metric with a swapped sign, and
        the correction (Amendment 10, June 2026) is documented in the monograph rather than
        erased — under the corrected convention all four partisan metrics point the same
        direction on the minority map.
      </p>
    </section>

    <section id="seats-50-50">
      <h2>Seats at a 50/50 vote</h2>
      <p>
        The most intuitive test: swing the province-wide vote to an exact 50/50 tie and count
        the seats the map hands each side. It isolates what the <em>map</em> contributes to an
        outcome, with the electorate held perfectly neutral. On Alberta's geography a typical
        neutral map gives the UCP about <strong>44.8%</strong> of seats at a tie — city-core
        NDP concentration confers a small natural efficiency edge at parity.
      </p>
      <p>
        The majority map scores <strong>46.1%</strong> — 78th percentile, unremarkable. The
        minority map scores <strong>51.7%</strong> (46 of 89 seats — a majority for the UCP
        while tied in votes): higher than all but <strong>66 of the 1,010,000</strong> neutral
        maps, at the very edge of the ensemble's ceiling of 51.72%. For scale: a targeted
        hill-climbing procedure told to <em>deliberately maximize</em> UCP seats under the same
        constraints reached 52.9%. The minority map sits closer to that engineered ceiling than
        to the neutral median. Two honest caveats travel with this result: real electorates are
        never a uniform 50/50, so this measures the map's contribution rather than predicting
        any election; and the neutral baseline is the ReCom-typical null described
        <a href="#ensemble">above</a>.
      </p>
    </section>

    <section id="reproduce">
      <h2>Reproduce it yourself</h2>
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

# regenerate the 1,010,000-map ensemble (long-running; checkpointed)
python analysis/scripts/mcmc_ensemble_canonical.py --n-steps 252500

# score the real maps and verify the headline against every plan
python analysis/scripts/joint_outlier_score_canonical.py
python analysis/scripts/verify_joint_empirical_bound.py</code></pre>
      <p>
        A hosted notebook version runs in the browser via
        <a href="https://colab.research.google.com/github/Ixby/alberta-electoral-boundaries-audit/blob/master/notebooks/alberta_audit_explorer.ipynb" rel="noopener">Google Colab</a>.
        Registrations, seeds, and amendment history are indexed in the monograph's §4.3.3; the
        full methodology, including every retraction and correction the audit has made along
        the way, is in the
        <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">academic monograph</a>.
      </p>
      <p class="cross-ref">
        Companion page: <a href="{base}/law">What the law asks of an electoral map</a> — how
        these measurements relate to the <em>Charter</em> and Alberta's boundary statute.
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
    margin-bottom: 2.2rem;
  }
  :global(:root[data-theme="dark"]) .standfirst {
    color: #b9c0d0;
    border-inline-start-color: #4a6690;
  }

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

  .honesty-box {
    background: rgba(26, 46, 69, 0.06);
    border-inline-start: 3px solid #7B2D3E;
    padding: 0.9rem 1.1rem;
    border-radius: 0 6px 6px 0;
    font-size: 0.95rem;
    margin-bottom: 0.9rem;
  }
  :global(:root[data-theme="dark"]) .honesty-box {
    background: rgba(255, 255, 255, 0.05);
  }

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
