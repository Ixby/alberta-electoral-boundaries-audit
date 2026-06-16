<!--
  Alberta Electoral Boundary Audit — Privacy Policy
  © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
-->
<svelte:head>
  <title>Privacy Policy · Alberta Electoral Boundary Audit</title>
  <meta name="description" content="Privacy and data retention policy for the Alberta Electoral Boundary Audit.">
</svelte:head>

<script lang="ts">
  import { base } from '$app/paths';
</script>

<header>
  <div class="header-inner">
    <a href="{base}/" class="back-link">← Back to audit</a>
    <div class="header-text">
      <div class="site-label">Alberta Electoral Boundary Audit</div>
      <h1>Privacy &amp; Data Retention Policy</h1>
      <p class="meta">Effective: 2026-05-24 · Maintained by Will Conner</p>
    </div>
  </div>
</header>

<main>
  <div class="policy">

    <section>
      <h2>Overview</h2>
      <p>This tool is a public-interest audit of Alberta's 2023 electoral boundary commission process. It is not a commercial product and runs no advertisements. This page explains what data is collected, why, what is never collected, and how you can opt out.</p>
    </section>

    <section>
      <h2>The principle</h2>
      <p>Citizens should be able to understand how their government works without worrying that someone is watching over their shoulder. Every design choice in this tool follows from that.</p>

      <h3>Nothing leaves your browser without your consent</h3>
      <p>All data is assembled in your browser first. Nothing is sent to our database unless you clicked <strong>Yes, I'll help</strong> at the prompt when you first opened MapExplorer. If you clicked <strong>No thanks</strong>, nothing is recorded — not even if you later share a map view.</p>

      <h3>We couldn't identify you even if we tried</h3>
      <p>The data is deliberately blurry. Your map position is rounded to one of 25 large regions before it leaves your browser — each region is roughly the size of a major Alberta city. Zoom level is one of four coarse buckets. We record the sequence of what you looked at, but not how long you spent on anything. No browser fingerprint. No precise coordinates.</p>
      <p>We are interested in the stories that groups tell — which parts of the map draw attention, which proposals people compare, where the audit lands when people find it worth sharing. We are not interested in you specifically. The design makes "you specifically" technically unreachable, not merely against our policy.</p>
      <p>If we were ordered by a court to identify a specific person from our data, we could not do it. That is not a promise. It is a structural fact.</p>

      <h3>See what we see</h3>
      <p>The analytics dashboard shows the actual data we have collected — which districts people clicked, which maps they explored, and the full sequence of each session. Nothing is hidden or summarized away from it.</p>
      <p><a href="{base}/dashboard" class="dashboard-link">Open the analytics dashboard →</a></p>
    </section>

    <section>
      <h2>What GitHub Pages collects</h2>
      <p>This site is hosted on GitHub Pages. GitHub's servers automatically log basic request details when any page loads — your IP address, browser type, referring page, and timestamp. We do not receive or control these logs; they are governed by <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener noreferrer">GitHub's Privacy Statement</a>. We have no relationship with GitHub beyond hosting.</p>
    </section>

    <section>
      <h2>Participation</h2>
      <p>When you open MapExplorer, you see one prompt:</p>
      <blockquote>Help us refine MapExplorer</blockquote>
      <p>If your browser has Do Not Track turned on, <strong>No thanks</strong> is pre-selected and the reason is shown. You can still switch to <strong>Yes, I'll help</strong> if you want.</p>
      <p>If you choose <strong>No thanks</strong>, that is the end of it. Nothing is recorded for your session.</p>
      <p>If you choose <strong>Yes, I'll help</strong>, we begin collecting your exploration path from that moment. Your answer is saved in a cookie so the prompt does not appear again on future visits.</p>
    </section>

    <section>
      <h2>Do Not Track</h2>
      <p>If your browser sends a Do Not Track signal, <strong>No thanks</strong> is pre-selected when you open MapExplorer. You can override it by choosing <strong>Yes, I'll help</strong> — your explicit choice wins.</p>
      <p>We take Do Not Track seriously at the database level too. If the code that handles this signal is ever changed without a corresponding update to our audit trail, our database automatically stops accepting new data until a human reviews the discrepancy. There is no way for this check to fail silently.</p>
    </section>

    <section>
      <h2>What we collect</h2>
      <p>Only collected if you chose <strong>Yes, I'll help</strong>.</p>

      <p>As you explore MapExplorer, we periodically record your exploration path — roughly every 30 seconds. Each step is one of:</p>
      <ul>
        <li>Which electoral district you clicked</li>
        <li>Which map you switched to</li>
        <li>Which data layer you turned on or off</li>
      </ul>
      <p>We record what you looked at, in order — not how long you spent on each thing.</p>

      <p>If you click <strong>Share</strong>, we also save your ending map view (which map is active, which overlays are on, roughly where your viewport is). This goes into a separate table with no link back to your exploration path — so no one can look up a share code and find out how you got there.</p>

      <h3>What we record when you share</h3>
      <ul>
        <li>Which map was active and which others were visible</li>
        <li>Which data layers were on</li>
        <li>Which district (if any) was highlighted</li>
        <li>Roughly where you were on the map and how zoomed in</li>
        <li>Roughly how long you had been on the page (one of five buckets: under 1 min, 1–3, 3–10, 10–30, 30+)</li>
        <li>Browser family (e.g. Chrome, Safari) — raw browser string is discarded</li>
        <li>Screen size, rounded to the nearest 100 pixels</li>
        <li>Device type: phone, tablet, or desktop</li>
        <li>Time zone and language (e.g. America/Edmonton, en-CA)</li>
        <li>Full date and time of the share</li>
        <li>If you loaded someone else's share code first, that code is noted as your starting point</li>
        <li>Your approximate region (10 km grid), if you allowed GPS access when you consented to analytics</li>
      </ul>
    </section>

    <section>
      <h2>Optional: approximate region</h2>
      <p>When you choose <strong>Yes, I'll help</strong>, your browser asks for GPS permission as part of consent. This is entirely optional — you can accept analytics and deny GPS, and that's fine.</p>
      <p>If you allow location access, your browser reads your GPS coordinates and we immediately round them to the nearest tenth of a degree of latitude and longitude — a grid cell roughly 10 km across. The precise coordinates are discarded right there in the browser and never leave your device. What we receive is a broad region like "Calgary area" or "Peace Country."</p>
      <p>If you've already consented but haven't granted GPS, the request may appear silently in the background on your next visit. Denying it has no effect on your participation in analytics.</p>
      <p>Your approximate region is stored in your cookie and included with share events so we can understand which parts of Alberta find the audit most useful.</p>
    </section>

    <section>
      <h2>What we never collect</h2>
      <p>No name. No email. No IP address. No precise location. No raw browser fingerprint. No cross-session identifier — each page load gets a temporary ID that exists only in memory and disappears when you close the tab.</p>
      <p>Everything is rounded or bucketed in your browser before anything is sent. The server never sees a precise value.</p>
    </section>

    <section>
      <h2>Share codes</h2>
      <p>Your cookie always holds a code for your current map view — it is updated continuously as you explore, every few hundred milliseconds. Clicking <strong>Share</strong> reveals that code so you can copy it. Nothing new is generated at that moment; the code was already there.</p>
      <p>Share codes appear on screen and go to your clipboard only when you click Copy. They are never embedded in a URL, so they don't appear in browser history, server logs, or referrer headers. To load someone's shared view, the recipient types the code directly into the site.</p>

      <h3>There are only 19,200 possible codes</h3>
      <p>Share codes represent map configurations, not people. There are exactly 19,200 valid combinations of map, overlays, layers, and viewport region — so two people exploring independently can easily arrive at the same code. This is expected and intentional. When it happens, we record two arrivals at the same map state, which is exactly the signal we're looking for: it tells us that configuration is genuinely interesting, not just a one-off. No two sessions are merged or linked because of a shared code.</p>

      <h3>What can and cannot be linked</h3>
      <p>Share codes and flight paths are impossible to link. They are stored in separate database tables with no shared key — not a privacy policy restriction, an architectural one. There is no query that connects them.</p>
      <p>Web server logs work the same way. When your browser loads this page, GitHub's servers record your IP address. When your flight-path events reach our database, they carry a session identifier — a random string that exists only in your browser's memory for that page load. Your IP address is never stored in our database. The session identifier is never sent to GitHub's servers. The two pieces of information were never associated, so there is nothing to link.</p>
    </section>

    <section>
      <h2>Cookies</h2>
      <p>This site sets one cookie that stores six things:</p>
      <ul>
        <li><strong>Your consent choice</strong> — yes or no</li>
        <li><strong>Colour theme</strong> — dark or light, if you changed it</li>
        <li><strong>Intro dismissed</strong> — so the map introduction doesn't repeat</li>
        <li><strong>Current map view</strong> — updated continuously as you explore, so your view is restored on your next visit</li>
        <li><strong>Approximate region</strong> — your 10 km GPS grid cell, if you allowed location access</li>
        <li><strong>Browser language</strong> — e.g. en-CA, to understand which language communities find the audit</li>
      </ul>
      <p>The cookie is encrypted in your browser before it is written — the server never sees the contents. It is only sent over HTTPS and is never shared with other sites. It expires after one year. You can remove it by clearing your cookies.</p>
      <p>The map view and location data are encrypted because they encode where you were — which proposal you were looking at, which layers were on, where your viewport was. That is your business, not anyone else's.</p>
    </section>

    <section>
      <h2>Data retention</h2>
      <p>All stored records are anonymized before they reach our database. The database is hosted in Canada (ca-central-1). We keep records indefinitely as research data. If we ever found that a record contained identifying information — which the design is built to prevent — we would delete it within 30 days.</p>
    </section>

    <section>
      <h2>Your rights</h2>
      <p>You have the right not to be remembered.</p>
      <ul>
        <li><strong>Choose No thanks</strong> at the prompt and nothing is recorded.</li>
        <li><strong>Turn on Do Not Track</strong> in your browser and No thanks is pre-selected for you.</li>
      </ul>
    </section>

    <section>
      <h2>Contact</h2>
      <p>Will Conner<br>
      <a href="mailto:wconn161@mtroyal.ca">wconn161@mtroyal.ca</a></p>
      <p>Independent research — not affiliated with or endorsed by any institution.</p>
      <p>Questions and deletion requests answered within 10 business days.</p>
    </section>

    <section>
      <h2>Policy updates</h2>
      <p>When this policy changes, the effective date at the top is updated and the change is committed to the <a href="https://github.com/ixby/alberta-electoral-boundaries-audit" target="_blank" rel="noopener noreferrer">public git repository</a>. The commit history is the changelog. Any change that expands what is collected is noted in the commit message.</p>
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
  :global(:root[data-theme="dark"]) header {
    background: #111722;
  }

  .header-inner {
    max-width: 760px;
    margin: 0 auto;
  }

  .back-link {
    display: inline-block;
    color: rgba(255,255,255,0.6);
    text-decoration: none;
    font-size: 0.85rem;
    margin-bottom: 1.1rem;
    transition: color 0.15s;
  }
  .back-link:hover { color: #fff; }

  .site-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: rgba(255,255,255,0.45);
    margin-bottom: 0.35rem;
  }

  h1 {
    font-size: clamp(1.4rem, 4vw, 1.9rem);
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.25;
    margin-bottom: 0.4rem;
  }

  .meta {
    font-size: 0.82rem;
    color: rgba(255,255,255,0.45);
  }

  main {
    padding: 2.5rem clamp(1.2rem, 4vw, 3.5rem) 4rem;
  }

  .policy {
    max-width: 760px;
    margin: 0 auto;
  }

  section {
    margin-bottom: 2.4rem;
    padding-bottom: 2.4rem;
    border-bottom: 1px solid #e0ddd6;
  }
  :global(:root[data-theme="dark"]) section {
    border-bottom-color: #2e3040;
  }
  section:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
  }

  h2 {
    font-size: 1.15rem;
    font-weight: 700;
    color: #1a2e45;
    margin-bottom: 0.8rem;
    letter-spacing: -0.01em;
  }
  :global(:root[data-theme="dark"]) h2 { color: #a8c4e0; }

  h3 {
    font-size: 0.95rem;
    font-weight: 600;
    color: #243b53;
    margin: 1.2rem 0 0.5rem;
  }
  :global(:root[data-theme="dark"]) h3 { color: #8890a4; }

  p { margin-bottom: 0.85rem; }
  p:last-child { margin-bottom: 0; }

  ul {
    padding-inline-start: 1.4rem;
    margin-bottom: 0.85rem;
  }
  li { margin-bottom: 0.45rem; }

  .dashboard-link {
    display: inline-block;
    margin-top: 0.3rem;
    background: #6B35A7;
    color: #fff !important;
    text-decoration: none;
    padding: 0.5rem 1.1rem;
    border-radius: 5px;
    font-size: 0.92rem;
    font-weight: 500;
  }
  .dashboard-link:hover { background: #5a2a90; }

  blockquote {
    border-inline-start: 3px solid #6B35A7;
    padding: 0.5rem 1rem;
    margin: 0.9rem 0;
    background: rgba(107,53,167,0.05);
    border-radius: 0 4px 4px 0;
    font-style: italic;
    color: #333;
  }
  :global(:root[data-theme="dark"]) blockquote {
    background: rgba(107,53,167,0.12);
    color: #c4b8d8;
  }

  code {
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 0.85em;
    background: rgba(0,0,0,0.06);
    padding: 0.1em 0.4em;
    border-radius: 3px;
    color: #1a2e45;
  }
  :global(:root[data-theme="dark"]) code {
    background: rgba(255,255,255,0.08);
    color: #a8c4e0;
  }

  a { color: #1a5276; }
  a:hover { text-decoration: underline; }
  :global(:root[data-theme="dark"]) a { color: #6aaddb; }

  @media (max-width: 600px) {
    h2 { font-size: 1.05rem; }
    main { padding-top: 1.8rem; }
  }
</style>
