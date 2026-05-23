# Privacy and Data Retention Policy

**Alberta Electoral Boundary Audit**
Effective: 2026-05-23
Maintained by: Will Conner

---

## Overview

This tool is a public-interest statistical audit of Alberta's 2023 electoral boundary commission process. It is not a commercial product and does not run advertisements. This policy explains what is collected, by whom, how it is used, and how you can opt out.

The principle behind our data practices: observe reliably what we can, find useful patterns, respect the right of every person not to be remembered. Enough information to be useful. Not enough to be snoopy.

---

## What GitHub Pages Collects

This site is hosted on GitHub Pages (pages.github.com). GitHub's infrastructure automatically records standard server-access logs when any page is loaded: your IP address, browser user-agent string, referring URL, and request timestamp. We do not receive, access, or control these logs. They are governed exclusively by GitHub's Privacy Statement (github.com/site/privacy). We have no relationship with GitHub beyond being a hosting customer.

---

## Participation

When the page loads, you are asked one question:

> *May we connect anonymous usage data?*

The default answer is **No**. If your browser sends a Do Not Track signal, No is pre-selected and the reason is noted. You can change your answer either way.

If you answer **No**, the data collection system is disabled for your session. Nothing is recorded, including if you later use the share feature.

If you answer **Yes**, the collection system is armed from that moment forward. The starting map configuration is not collected — we set it and already know it. What we collect is where you end up and how you got there.

There is no re-asking. No consent is sought at share time. No data is collected retroactively.

---

## Do Not Track

If your browser sends `DNT: 1`, No is pre-selected in the participation prompt and the reason is shown. You can still choose Yes if you want to participate — your explicit choice overrides the browser signal. If you leave the answer at No or decline, nothing is recorded.

The database enforces this independently of the client. Every write to our database carries a verifiable commitment: the hash of the DNT-handling code deployed to the site, paired with a publicly declared randomness beacon from Cloudflare drand (drand.cloudflare.com). The beacon round is committed to our source repository before data collection is enabled, so no one can retroactively forge a seed that would validate a compromised version of the check.

If the DNT-handling code is altered, the hash changes, the write is rejected, and the database enters a freeze state — all further writes are blocked until a human operator reviews the discrepancy and re-establishes a valid commitment. The beacon is public and auditable by anyone. There is no way for this check to silently fail.

---

## What We Collect

Data is collected only from sessions where participation was confirmed and the session has not been flagged as Do Not Track. Nothing is transmitted until you click Share. If you close the tab without sharing, nothing is recorded.

When you click Share, the following is written to our database:

**Ending state.** The map configuration you arrived at: which map is primary, which overlays are active, which layer toggles are on, which electoral district (if any) is highlighted, and your viewport position and zoom level. This is the meaningful signal — it shows where people land and what they find worth sharing.

**Flight path.** The sequence of interactions that led to your ending state. Each step is one of five event types:

- *Viewport* — map centre (rounded to ~8 km grid), zoom level (one decimal place), active map, overlays, and layers at that moment
- *Map switch* — which map you left and which you moved to
- *Overlay toggle* — which overlay was turned on or off
- *Layer toggle* — which layer was turned on or off
- *ED focus* — which electoral district you clicked

Steps are numbered in order. No time elapsed between steps is recorded — sequence is captured, pace is not.

**Feature summary.** Derived from the flight path in the browser before anything is transmitted: which maps were activated, whether overlays were used, whether layers were changed, which electoral districts were clicked, whether the search and lock features were used.

**Session context.** Recorded once at share time:

- Day of week and hour of day — no full date, no minute
- Browser family and major version, parsed from the user-agent string in the browser — used to catch layout or interaction issues that vary by browser, not to characterize users by browser preference; the raw user-agent string is discarded and never transmitted
- Viewport width and height, rounded to the nearest 100 pixels
- Device class: mobile, tablet, or desktop, derived from viewport width
- Timezone — a value like *America/Edmonton* shared by millions of people
- Language — a value like *en-CA* or *fr-CA*
- Approximate region, if you chose to provide it (see below)
- How long you spent on the page before sharing, in one of five tiers: under 1 minute, 1–3 minutes, 3–10 minutes, 10–30 minutes, or 30 minutes or more

---

## Approximate Region (Optional)

During the share flow you may be asked whether to include your approximate location. This is separate from the participation consent given on load and is entirely optional.

If you accept, your browser requests your position via the Geolocation API. Before anything leaves your device, the coordinates are snapped to the nearest 1-degree grid cell — approximately 100 km in Alberta. The raw coordinates are discarded locally. The value transmitted identifies a broad region (Calgary area, Edmonton area, Lethbridge area) without identifying a neighbourhood, street, or address.

---

## Pre-Anonymization

All location values — viewport coordinates, zoom level, and optional geolocation — are reduced to their anonymized form in your browser before any data is transmitted. The server never receives a precise value. There is nothing to redact because identifying precision is discarded before it leaves your device.

No name. No email address. No IP address. No raw user-agent string. No persistent identifier across sessions. An in-memory token stitches your flight-path events into a sequence for the duration of the page load; it is never transmitted and is gone when the tab closes.

---

## What You Can Retrieve

Entering a share code into the site returns the map configuration that was saved — the ending state. That is all.

Your flight path, session context, and feature summary are stored separately and are not retrievable by share code. This is not a restriction enforced by application logic that could be changed; the two records have no shared key. The connection between a specific share code and the telemetry collected in that session does not exist in the database. Neither you nor anyone else can retrieve it, because there is nothing to retrieve.

---

## Three-Word Share Codes

Share codes are displayed on screen. They are copied to your clipboard only when you click the Copy button. They are never placed in a URL, never written to a cookie, and never transmitted as part of a link. Browser history, referrer headers, and server logs will not contain the code. Recipients enter the code directly into the site to load the shared map state.

---

## Data Retention

All records are pre-anonymized before storage and contain no personally identifying information. We retain them indefinitely as research data. Aggregate patterns derived from the database are also retained indefinitely.

If we determine that a record contains PII — which the pre-anonymization architecture is designed to prevent — that record will be encrypted immediately, distilled to non-identifying statistics, and permanently deleted within 30 days.

---

## Your Rights

You have the right not to be remembered.

- **Answer No** at the participation prompt, and nothing is recorded for your session.
- **Enable Do Not Track** in your browser, and No is pre-selected on your behalf.
- **Share codes you generate** can be deleted on request. Send the code to wconn161@mtroyal.ca and we will delete it and confirm in writing.
- **Confirmation**: you may request written confirmation that a specific share code exists or does not exist in our database. We cannot search by identity — none was collected.

---

## Contact

Will Conner  
wconn161@mtroyal.ca  
Mount Royal University, Department of Policy Studies  

Questions, concerns, and deletion requests are answered within 10 business days.

---

## Policy Updates

When this policy changes, the effective date at the top is updated and the change is committed to the public git repository (github.com/ixby/alberta-electoral-boundaries-audit). The commit history is the changelog. Any change that expands what is collected or how it is used is noted in the commit message.
