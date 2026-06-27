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
      <p class="meta">Effective: 2026-06-24 · Maintained by Will Conner</p>
    </div>
  </div>
</header>

<main>
  <div class="policy">

    <section>
      <h2>Overview</h2>
      <p>This tool is a public-interest audit of Alberta's 2023 electoral boundary commission process. It is not a commercial product and runs no advertisements. This page explains what is measured, what is never collected, and why none of it can be tied back to you.</p>
      <p>The short version: the site uses cookieless, aggregate analytics. There is no tracking cookie, no advertising, no cross-site profiling, and no identifier that follows you. Because nothing personal is stored, there is no consent banner to click through — the privacy protection is built into how the measurement works, not bolted on as a prompt.</p>
    </section>

    <section>
      <h2>How the analytics work</h2>
      <p>When a page loads or you interact with the map, the site sends a small, anonymous event to a counting service we run. Each event is just the name of what happened — for example, "page viewed" or "district selected" — plus a few coarse details about the action. The event carries no name, no email, no account, and no identifier stored on your device.</p>
      <p>To count how many distinct people visited on a given day without identifying anyone, the counting service combines your network address and browser type and runs them through a one-way cryptographic hash together with a secret that changes every day. The result is a short code that lets us tell two visits apart <em>within</em> a single day, and nothing more. The original address is never stored — only the hash is. Because the secret rotates daily, the same visitor produces a different code tomorrow, so there is no way to follow anyone across days or to work backwards from a code to a person.</p>
      <p>We are interested in the picture that visitors paint as a group — which findings get read, which maps get opened, which districts draw attention. We are not interested in you specifically, and the measurement is built so that "you specifically" is not something the data can express.</p>
    </section>

    <section>
      <h2>What is measured</h2>
      <p>The analytics record aggregate, anonymous events such as:</p>
      <ul>
        <li>Page views</li>
        <li>How far down a page people scroll, in coarse bands (25%, 50%, 75%, 100%)</li>
        <li>Roughly how long the page was actively on screen, in coarse time buckets</li>
        <li>Which finding sections come into view as people read</li>
        <li>Which maps are opened in the explorer, and which districts are selected</li>
        <li>Which map layers are turned on or off, and roughly how far in people zoom</li>
        <li>Which points of interest or report links are opened</li>
        <li>A coarse picture of your setup — screen-size band (such as phone, tablet, or desktop), form factor, and browser family (such as Chrome, Safari, or Firefox). We never store your exact screen dimensions or full browser identification string.</li>
        <li>A one-time snapshot of how the map explorer performed when it first drew — for example, the load time in coarse bands and a rounded memory figure. This helps us tell whether the explorer is fast enough on real devices. The numbers are deliberately banded, not exact, so they describe a device class rather than a device.</li>
      </ul>
      <p>Every one of these is stored only in aggregate. There is no per-person profile, no session replay, and no record of an individual's path through the site. We see totals and distributions, not people.</p>
    </section>

    <section>
      <h2>What is never collected</h2>
      <p>No name. No email. No account. No advertising identifier. No stored IP address — your network address is hashed with a daily-rotating secret and immediately discarded; only the short-lived daily code is kept. No raw browser fingerprint. No cross-day or cross-site identifier. No precise location. No cookie or browser-storage identifier that marks you as a returning visitor for analytics purposes.</p>
    </section>

    <section>
      <h2>What GitHub Pages collects</h2>
      <p>This site is hosted on GitHub Pages. GitHub's servers automatically log basic request details when any page loads — your IP address, browser type, referring page, and timestamp. We do not receive or control these logs; they are governed by <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener noreferrer">GitHub's Privacy Statement</a>. We have no relationship with GitHub beyond hosting. The analytics described above run separately and never receive your IP address.</p>
    </section>

    <section>
      <h2>Share codes</h2>
      <p>The map explorer has a Share feature. It turns your current map view — which map is active, which overlays and layers are on, roughly where your viewport sits — into a short three-word code you can copy and send to someone. There are exactly 19,200 valid codes, because a code represents a map configuration, not a person. Two people who arrive at the same view independently get the same code; that is expected and carries no link between them.</p>
      <p>Share codes appear on screen and go to your clipboard only when you click Copy. They are never embedded in a URL, so they don't appear in browser history, server logs, or referrer headers. To open someone's shared view, the recipient types the code directly into the site.</p>
      <p>When you generate a share code, the map configuration it encodes is saved to our database so the link keeps working. That saved record is a map state — not a person, not a path, and not joined to the analytics. It contains no identifier for you.</p>
    </section>

    <section>
      <h2>Cookies and browser storage</h2>
      <p>The analytics use no cookie and no browser-storage identifier. Nothing about the measurement marks you as a returning visitor.</p>
      <p>The site does set one small <strong>functional</strong> cookie to remember your own preferences between visits. It is not used for analytics or tracking, and it never leaves your browser in readable form. It stores:</p>
      <ul>
        <li><strong>Colour theme</strong> — dark or light, if you changed it</li>
        <li><strong>Intro dismissed</strong> — so the map introduction doesn't repeat</li>
        <li><strong>Current map view</strong> — so your last view is restored on your next visit</li>
        <li><strong>Browser language</strong> — so the site can show your preferred language</li>
      </ul>
      <p>This cookie holds only the preferences above — no personal or identifying information. Its contents are scrambled with a key that ships inside the page, so the stored value is not human-readable; because that key is public, treat this as tamper-resistance rather than true secrecy. It is sent only over HTTPS, is never shared with other sites, and you can remove it at any time by clearing your cookies. The site is served as static files, so nothing on the server side reads it. Your colour theme is also mirrored to your browser's local storage so the correct theme can be applied instantly on load, before anything flickers; that value too is purely functional and never sent anywhere.</p>
    </section>

    <section>
      <h2>Data retention</h2>
      <p>The analytics records are aggregate and anonymous by construction, with no identifier to retain. They are stored on infrastructure hosted in Canada (ca-central-1) and kept as research data. If we ever found that a record contained identifying information — which the design is built to prevent — we would delete it within 30 days.</p>
    </section>

    <section>
      <h2>Your choices</h2>
      <p>Because nothing personal is collected, there is nothing to opt out of and no consent prompt to manage. If you would still prefer to send no analytics events at all, a content blocker or a browser that blocks the request to the counting service will stop them, and the site will work exactly the same. You can also clear the functional preferences cookie at any time through your browser.</p>
    </section>

    <section>
      <h2>Contact</h2>
      <p>Will Conner — independent research, not affiliated with or endorsed by any institution.</p>
      <p>Questions, corrections, and deletion requests: please use the <a href="{base}/feedback">feedback form</a>. Requests are answered within 10 business days.</p>
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

  p { margin-bottom: 0.85rem; }
  p:last-child { margin-bottom: 0; }

  ul {
    padding-inline-start: 1.4rem;
    margin-bottom: 0.85rem;
  }
  li { margin-bottom: 0.45rem; }

  em { font-style: italic; }

  a { color: #1a5276; }
  a:hover { text-decoration: underline; }
  :global(:root[data-theme="dark"]) a { color: #6aaddb; }

  @media (max-width: 600px) {
    h2 { font-size: 1.05rem; }
    main { padding-top: 1.8rem; }
  }
</style>
