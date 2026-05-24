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
      <p>This tool is a public-interest statistical audit of Alberta's 2023 electoral boundary commission process. It is not a commercial product and does not run advertisements. This policy explains what is collected, by whom, how it is used, and how you can opt out.</p>
    </section>

    <section>
      <h2>The principle</h2>
      <p>Citizens should be able to understand how their government works without worrying that someone is watching over their shoulder. Every design choice in this tool follows from that.</p>

      <h3>Nothing leaves your browser without your consent</h3>
      <p>All data is assembled in your browser first. Nothing is transmitted unless you explicitly clicked <strong>Yes</strong> at the participation prompt <em>and</em> then clicked <strong>Share</strong>. If you clicked <strong>No thanks</strong> — or closed the tab, or shared without consenting — nothing was recorded. These are not policy commitments enforced by honour; they are code paths. <code>recordEvent()</code> and <code>flushTelemetry()</code> both check the consent flag as their first instruction. There is no other path to the database.</p>

      <h3>Individual identification is impossible by design</h3>
      <p>The data we collect is specifically structured to make identifying any individual technically impossible — not merely against the rules. Viewport position is quantized to a 5×5 grid before it leaves your device: all of Alberta divided into 25 cells, each roughly the size of a major city. Zoom is one of four coarse tiers. No timestamps are recorded between events — we capture the sequence of what you looked at, not how long you spent. No raw browser fingerprint is transmitted. No precise coordinates leave your device at any point.</p>
      <p>We are interested in the stories that groups tell — which parts of the map draw attention, which proposals people compare, where the audit lands when people find it worth sharing. We are not interested in you specifically. The architecture is built to make "you specifically" technically unreachable, not merely policy-prohibited.</p>
      <p>If we were ordered by a court to identify a specific person from our data, we could not do it. That is not a promise. It is a structural fact.</p>
    </section>

    <section>
      <h2>What GitHub Pages Collects</h2>
      <p>This site is hosted on GitHub Pages (pages.github.com). GitHub's infrastructure automatically records standard server-access logs when any page is loaded: your IP address, browser user-agent string, referring URL, and request timestamp. We do not receive, access, or control these logs. They are governed exclusively by <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener noreferrer">GitHub's Privacy Statement</a>. We have no relationship with GitHub beyond being a hosting customer.</p>
    </section>

    <section>
      <h2>Participation</h2>
      <p>When the page loads, you are asked one question:</p>
      <blockquote>May we connect anonymous usage data?</blockquote>
      <p>If your browser sends a Do Not Track signal, <strong>No</strong> is pre-selected and the reason is noted. You can change your answer either way.</p>
      <p>If you answer <strong>No</strong>, the data collection system is disabled for your session. Nothing is recorded, including if you later use the share feature.</p>
      <p>If you answer <strong>Yes</strong>, the collection system is armed from that moment forward. The starting map configuration is not collected — we set it and already know it. What we collect is where you end up and how you got there.</p>
      <p>Your answer is saved in a first-party cookie (<code>ab_audit_prefs</code>, one year, SameSite=Strict) alongside your other site preferences (colour theme, whether you have seen the map-tool introduction, and the last map configuration you viewed). On return visits the prompt is skipped and your stored choice is applied immediately. There is no re-asking. No consent is sought at share time. No data is collected retroactively.</p>
    </section>

    <section>
      <h2>Do Not Track</h2>
      <p>If your browser sends <code>DNT: 1</code>, No is pre-selected in the participation prompt and the reason is shown. You can still choose Yes if you want to participate — your explicit choice overrides the browser signal. If you leave the answer at No or decline, nothing is recorded.</p>
      <p>The database enforces this independently of the client. Every write to our database carries a verifiable commitment: the hash of the DNT-handling code deployed to the site, paired with a publicly declared randomness beacon from <a href="https://drand.cloudflare.com" target="_blank" rel="noopener noreferrer">Cloudflare drand</a>. The beacon round is committed to our source repository before data collection is enabled, so no one can retroactively forge a seed that would validate a compromised version of the check.</p>
      <p>If the DNT-handling code is altered, the hash changes, the write is rejected, and the database enters a freeze state — all further writes are blocked until a human operator reviews the discrepancy and re-establishes a valid commitment. The beacon is public and auditable by anyone. There is no way for this check to silently fail.</p>
    </section>

    <section>
      <h2>What We Collect</h2>
      <p>Data is collected only from sessions where participation was confirmed and the session has not been flagged as Do Not Track. Nothing is transmitted until you click Share. If you close the tab without sharing, nothing is recorded.</p>
      <p>When you click Share, the following is written to our database:</p>

      <h3>Ending state</h3>
      <p>The map configuration you arrived at: which map is primary, which overlays are active, which layer toggles are on, which electoral district (if any) is highlighted, and your viewport position and zoom level. This is the meaningful signal — it shows where people land and what they find worth sharing.</p>

      <h3>Flight path</h3>
      <p>The sequence of interactions that led to your ending state. Each step is one of five event types:</p>
      <ul>
        <li><strong>Viewport</strong> — map centre (rounded to ~8 km grid), zoom level (one decimal place), active map, overlays, and layers at that moment</li>
        <li><strong>Map switch</strong> — which map you left and which you moved to</li>
        <li><strong>Overlay toggle</strong> — which overlay was turned on or off</li>
        <li><strong>Layer toggle</strong> — which layer was turned on or off</li>
        <li><strong>ED focus</strong> — which electoral district you clicked</li>
      </ul>
      <p>Steps are numbered in order. No time elapsed between steps is recorded — sequence is captured, pace is not.</p>

      <h3>Feature summary</h3>
      <p>Derived from the flight path in the browser before anything is transmitted: which maps were activated, whether overlays were used, whether layers were changed, which electoral districts were clicked, whether the search and lock features were used.</p>

      <h3>Session context</h3>
      <ul>
        <li>Day of week and hour of day — no full date, no minute</li>
        <li>Browser family and major version, parsed from the user-agent string in the browser — used to catch layout or interaction issues that vary by browser, not to characterize users by browser preference; the raw user-agent string is discarded and never transmitted</li>
        <li>Viewport width and height, rounded to the nearest 100 pixels</li>
        <li>Device class: mobile, tablet, or desktop, derived from viewport width</li>
        <li>Timezone — a value like <em>America/Edmonton</em> shared by millions of people</li>
        <li>Language — a value like <em>en-CA</em> or <em>fr-CA</em></li>
        <li>Approximate region, if you chose to provide it (see below)</li>
        <li>How long you spent on the page before sharing, in one of five tiers: under 1 minute, 1–3 minutes, 3–10 minutes, 10–30 minutes, or 30 minutes or more</li>
        <li>Origin code — if your session began by loading someone else's share code, that code is recorded as the starting point of your session. If your session began from the default configuration, this field is null. This lets us distinguish pure exploration from sessions that build on a prior shared configuration.</li>
      </ul>
    </section>

    <section>
      <h2>Approximate Region (Optional)</h2>
      <p>During the share flow you may be asked whether to include your approximate location. This is separate from the participation consent given on load and is entirely optional.</p>
      <p>If you accept, your browser requests your position via the Geolocation API. Before anything leaves your device, the coordinates are snapped to the nearest 1-degree grid cell — approximately 100 km in Alberta. The raw coordinates are discarded locally. The value transmitted identifies a broad region (Calgary area, Edmonton area, Lethbridge area) without identifying a neighbourhood, street, or address.</p>
    </section>

    <section>
      <h2>Pre-Anonymization</h2>
      <p>All location values — viewport coordinates, zoom level, and optional geolocation — are reduced to their anonymized form in your browser before any data is transmitted. The server never receives a precise value. There is nothing to redact because identifying precision is discarded before it leaves your device.</p>
      <p>No name. No email address. No IP address. No raw user-agent string. No persistent identifier across sessions. An in-memory token stitches your flight-path events into a sequence for the duration of the page load; it is never transmitted and is gone when the tab closes.</p>
    </section>

    <section>
      <h2>What You Can Retrieve</h2>
      <p>Entering a share code into the site returns the map configuration that was saved — the ending state. That is all.</p>
      <p>Your flight path, session context, and feature summary are stored separately and are not retrievable by share code. This is not a restriction enforced by application logic that could be changed; the two records have no shared key. The connection between a specific share code and the telemetry collected in that session does not exist in the database. Neither you nor anyone else can retrieve it, because there is nothing to retrieve.</p>
    </section>

    <section>
      <h2>Three-Word Share Codes</h2>
      <p>Share codes are displayed on screen. They are copied to your clipboard only when you click the Copy button. They are never placed in a URL and never transmitted as part of a link. Browser history, referrer headers, and server logs will not contain the code. Recipients enter the code directly into the site to load the shared map state.</p>
      <p>The most recent code you generated is stored in an encrypted cookie so your map state is restored on your next visit — see Cookies below.</p>
    </section>

    <section>
      <h2>Cookies</h2>
      <p>This site sets one cookie: <code>ab_audit_prefs</code>. It contains four values:</p>
      <ul>
        <li><strong>Consent</strong> — yes or no, as you answered the participation prompt</li>
        <li><strong>Theme</strong> — dark or light, if you toggled it</li>
        <li><strong>Intro seen</strong> — whether you have already dismissed the map intro</li>
        <li><strong>Last map state</strong> — the share code for the map configuration you were last at, so your view is restored on your next visit</li>
      </ul>
      <p>The cookie is encrypted with AES-256-GCM in your browser before it is written. The server never sees the plaintext — the decryption key lives in the client code, not on any server. The cookie is also flagged <code>Secure</code>, meaning it is only transmitted over HTTPS, and <code>SameSite=Strict</code>, meaning it is never sent as part of a cross-site request.</p>
      <p>The last map state is encrypted because it encodes where you were in the map — which proposal you were examining, which layers you had on, where your viewport was positioned. That is your business, not anyone else's. Encrypting it means the cookie is opaque to anyone who might intercept it, log it, or read it off your device.</p>
      <p>The cookie expires after one year. Clearing your cookies removes it.</p>
    </section>

    <section>
      <h2>Data Retention</h2>
      <p>All records are pre-anonymized before storage and contain no personally identifying information. We retain them indefinitely as research data. Aggregate patterns derived from the database are also retained indefinitely.</p>
      <p>If we determine that a record contains PII — which the pre-anonymization architecture is designed to prevent — that record will be encrypted immediately, distilled to non-identifying statistics, and permanently deleted within 30 days.</p>
    </section>

    <section>
      <h2>Your Rights</h2>
      <p>You have the right not to be remembered.</p>
      <ul>
        <li><strong>Answer No</strong> at the participation prompt, and nothing is recorded for your session.</li>
        <li><strong>Enable Do Not Track</strong> in your browser, and No is pre-selected on your behalf.</li>
        <li><strong>Share codes you generate</strong> can be deleted on request. Send the code to <a href="mailto:wconn161@mtroyal.ca">wconn161@mtroyal.ca</a> and we will delete it and confirm in writing.</li>
        <li><strong>Confirmation</strong>: you may request written confirmation that a specific share code exists or does not exist in our database. We cannot search by identity — none was collected.</li>
      </ul>
    </section>

    <section>
      <h2>Contact</h2>
      <p>Will Conner<br>
      <a href="mailto:wconn161@mtroyal.ca">wconn161@mtroyal.ca</a></p>
      <p>This project is independent and is not affiliated with or endorsed by any institution.</p>
      <p>Questions, concerns, and deletion requests are answered within 10 business days.</p>
    </section>

    <section>
      <h2>Policy Updates</h2>
      <p>When this policy changes, the effective date at the top is updated and the change is committed to the <a href="https://github.com/ixby/alberta-electoral-boundaries-audit" target="_blank" rel="noopener noreferrer">public git repository</a>. The commit history is the changelog. Any change that expands what is collected or how it is used is noted in the commit message.</p>
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
    padding-left: 1.4rem;
    margin-bottom: 0.85rem;
  }
  li { margin-bottom: 0.45rem; }

  blockquote {
    border-left: 3px solid #6B35A7;
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
