<!--
  Alberta Electoral Boundary Audit — What the Law Asks of an Electoral Map
  © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>

  Content grounded in reports/academic/report_academic.md §2 (legal-context
  literature review, corrected 2026-06-12 per T1.7 referee findings), §5.1.4–
  §5.1.5 (EBCA §15(2) statutory text and eligibility audit), and the public
  report's legal-terminology box. Every citation below appears in those
  verified sections; do not add case law here without verifying it there first.
  English-only for now — content is pending author review before translation.
-->
<svelte:head>
  <title>What the Law Asks · Alberta Electoral Boundary Audit</title>
  <meta name="description" content="How Canadian law evaluates an electoral map: Charter s.3 effective representation, the Saskatchewan Reference, and Alberta's Electoral Boundaries Commission Act — and how this audit's evidence relates to those tests.">
</svelte:head>

<script lang="ts">
  import { base } from '$app/paths';
</script>

<header>
  <div class="header-inner">
    <a href="{base}/" class="back-link">← Back to audit</a>
    <div class="header-text">
      <div class="site-label">Alberta Electoral Boundary Audit</div>
      <h1>What the Law Asks of an Electoral Map</h1>
      <p class="meta">Plain-language companion · English only for now · Not legal advice</p>
    </div>
  </div>
</header>

<main>
  <div class="content">

    <p class="standfirst">
      This audit measures maps. Courts judge them. The two jobs are related but not the same,
      and this page explains the difference: what Canadian law actually asks of an electoral
      boundary, which questions belong to a court rather than to a statistician, and where the
      audit's evidence fits. The audit itself takes no position on any legal conclusion —
      it reports what the data show and stops there.
    </p>

    <section id="why-not-gerrymander">
      <h2>Why this audit never rules "gerrymander"</h2>
      <p>
        "Gerrymandering" is used throughout the audit in its everyday political sense —
        manipulating electoral boundaries for partisan advantage. But in Canadian law the word
        has no legal definition. There is no statute to violate by "gerrymandering" and no
        court test with that name. A map cannot be found guilty of a category that does not
        exist, which is one reason the audit refuses to issue that verdict no matter what the
        numbers say.
      </p>
      <p>
        The American contrast is worth a moment, because most of this audit's statistical tools
        — the efficiency gap, neutral map ensembles — were invented for American fights. In the
        US, partisan gerrymandering is at least a named claim. But the US Supreme Court shut
        the federal courthouse door in <em>Rucho v. Common Cause</em>, 588 U.S. 684 (2019),
        holding that federal courts lack "judicially discernible and manageable standards" to
        judge such claims. The same metrics remain live in some US state courts — most
        prominently <em>League of Women Voters v. Commonwealth</em>, 178 A.3d 737 (Pa. 2018).
      </p>
      <p>
        Canada took a different path. Instead of a gerrymandering test, Canadian law asks two
        answerable questions. Does the map deliver <a href="#effective-representation">effective
        representation</a> under section 3 of the <em>Charter</em>? And did the commission
        comply with <a href="#ebca">its governing statute</a>? The audit's findings are
        evidence a court could weigh inside those two inquiries — inputs, not a verdict on
        either. And statistics cannot read minds: boundary geometry can show what a map
        <em>does</em>, never what its drafters <em>intended</em>.
      </p>
    </section>

    <section id="effective-representation">
      <h2>The constitutional test: effective representation</h2>
      <p>
        Section 3 of the <em>Charter of Rights and Freedoms</em> guarantees citizens the right
        to vote. In <em>Reference re Provincial Electoral Boundaries (Saskatchewan)</em>,
        [1991] 2 SCR 158 — the audit calls it the <em>Saskatchewan Reference</em> — the Supreme
        Court of Canada held that what s.3 protects in boundary-drawing is not one-person-one-vote
        arithmetic but <strong>effective representation</strong>.
      </p>
      <p>
        Writing for the majority, McLachlin J. explained (at para. 33) that "relative parity of
        voting power" is the starting point. But it must be weighed against permissible
        deviations for geography, community history, community interests and minority
        representation. The Court deliberately set no bright-line tolerance. A deviation from
        strict population equality is constitutionally defensible <em>if the non-numeric
        factors justify it</em>.
      </p>
      <p>
        Two consequences follow, and both cut against overreading this audit's numbers:
      </p>
      <ul>
        <li>
          <strong>Partisan asymmetry alone does not make a map unconstitutional.</strong> Under
          the case law reviewed in the monograph, a statistical tilt must be paired with
          something more — population deviations not justified by geography or community of
          interest, or evidence the neutral factors were invoked to rationalize a partisan
          outcome rather than to serve their statutory purpose. The audit's structural lane
          (population spread, city splits, chair-flagged boundaries) exists precisely because
          the law asks about that pairing.
        </li>
        <li>
          <strong>Courts defer to commissions.</strong> The standard is a deferential
          "reasonable commission" review, not a search for the best possible map. In
          <em>Raîche v. Canada (Attorney General)</em>, 2004 FC 679 — the closest reviewed case
          to a boundary challenge on community-of-interest grounds — the Federal Court found
          <em>no</em> Charter s.3 violation. The violations it did find were statutory (the
          federal boundary statute's community-of-interest duty), and the remedy was referral
          back to the commission, not boundaries struck down. It is a trial-level decision on
          the federal statute — persuasive, not binding, for any Alberta challenge.
        </li>
      </ul>
      <p>
        Where does the audit sit in that framework? Its measurements — how far each map's
        partisan metrics sit from a million neutral alternatives, how population variance is
        distributed, where boundaries depart from municipal lines — are inputs a court could
        weigh in the effective-representation analysis. No metric, and no combination of
        metrics, is a proxy for the test's outcome. When the audit reports that several
        indicators point the same way, that is a statement about an empirical pattern, not a
        legal conclusion.
      </p>
    </section>

    <section id="ebca">
      <h2>The statute: Alberta's Electoral Boundaries Commission Act</h2>
      <p>
        Alberta's commissions are governed by the <em>Electoral Boundaries Commission Act</em>,
        RSA 2000, c. E-3 (the EBCA). Three of its rules matter most for reading this audit.
      </p>
      <p>
        <strong>The population band.</strong> As a general rule, each proposed electoral
        division must stay within ±25% of the provincial average population. Both 2026
        proposals comply: apart from the three divisions each map protects under the s.15(2)
        exception described next, every district sits inside the band, and the largest
        deviation on the high side (+24.06%, in the minority map) comes within a point of the
        cap without crossing it. Inside that generous band the commission has wide discretion —
        the audit's population findings (the minority's 48%-wider spread, the NE/central
        Calgary crowding) all describe choices made <em>within</em> the legal band. Legal and
        unusual are different questions.
      </p>
      <p>
        <strong>The s.15(2) exception.</strong> For at most four divisions, the population may
        fall as much as 50% below the average — if the commission is of the opinion that at
        least three of these five criteria exist:
      </p>
      <ul class="criteria">
        <li>area over 20,000 km² (or total surveyed area over 15,000 km²);</li>
        <li>more than 150 km from the Legislature Building to the division's nearest boundary, by the most direct highway;</li>
        <li>no town in the division over 8,000 people;</li>
        <li>the division contains an Indian reserve or a Métis settlement;</li>
        <li>part of the boundary runs along Alberta's provincial border.</li>
      </ul>
      <p>
        The provision is permissive: meeting the criteria makes a division eligible, but never
        obliges the commission to use the allowance. Both 2026 maps invoke s.15(2) for three
        divisions each. The audit re-checked all six invocations under the corrected statutory
        thresholds and found every one eligible. The controversy the audit documents is not
        eligibility but a drawing choice. The minority's Rocky Mountain House–Banff Park
        division picks up one qualifying criterion — the provincial-border one — only by
        extending through uninhabited national-park land. The commission chair criticized that
        choice in the official report, even though the division qualifies without it.
      </p>
      <p>
        <strong>What a commission report is — and is not.</strong> Under the EBCA, the
        commission's report has no legal effect by itself. Boundaries change only when the
        Legislative Assembly passes a separate Electoral Districts Act. Most provinces make a
        commission's map effective unless the legislature actively overrides it. Alberta's
        default is reversed — the governing party controls whether any commission map becomes
        law. Section 12 of the Act also permits referring a commission's recommendations to a
        legislative committee, with no statutory minimum notice or public-comment period. That
        is the door the government used on April 16, 2026. It set both commission maps aside
        and assigned the work to a committee whose majority comes from the governing party, due
        to report by November 2, 2026. The audit documents that process choice as a finding
        about procedure — separate from, and additional to, anything the maps' geometry shows.
      </p>
      <p class="cross-ref">
        The full legal analysis — including the case-law review, the commission-deference
        literature, and the procedural comparison with other provinces — is in the academic
        monograph, §2 and §5.9, at
        <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">the audit repository</a>.
      </p>
    </section>

    <section>
      <h2>The audit's standing rule</h2>
      <p>
        Every version of this audit carries the same discipline: it may report what the tests
        show, and it may say how unusual a map is against a neutral baseline, but it does not
        declare any map a gerrymander, does not infer intent from geometry, and does not
        pronounce on constitutional or statutory compliance. Those are questions for courts,
        commissions, and readers — with the audit's evidence on the table.
      </p>
      <p class="cross-ref">
        Companion page: <a href="{base}/methods">How the maps were tested</a> — the ensemble,
        the four fairness metrics, and how to reproduce every number.
      </p>
      <p class="disclaimer">
        This page is a plain-language companion to the audit, written for orientation. It is
        not legal advice, and nothing here should be relied on as a legal opinion.
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

  .disclaimer {
    font-size: 0.88rem;
    font-style: italic;
    color: #6b6b65;
    border-top: 1px solid rgba(128,128,128,0.25);
    padding-top: 0.9rem;
  }
  :global(:root[data-theme="dark"]) .disclaimer { color: #8891a8; }
</style>
