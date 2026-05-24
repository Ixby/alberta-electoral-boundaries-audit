# Privacy and Data Retention Policy

**Alberta Electoral Boundary Audit**
Effective: 2026-05-24
Maintained by: Will Conner

---

## Overview

This tool is a public-interest audit of Alberta's 2023 electoral boundary commission process. It is not a commercial product and runs no advertisements. This page explains what data is collected, why, what is never collected, and how you can opt out.

---

## The principle

Citizens should be able to understand how their government works without worrying that someone is watching over their shoulder. Every design choice in this tool follows from that.

### Nothing leaves your browser without your consent

All data is assembled in your browser first. Nothing is sent to our database unless you clicked **Yes, I'll help** at the prompt when you first opened MapExplorer. If you clicked **No thanks**, nothing is recorded — not even if you later share a map view.

### We couldn't identify you even if we tried

The data is deliberately blurry. Your map position is rounded to one of 25 large regions before it leaves your browser — each region is roughly the size of a major Alberta city. Zoom level is one of four coarse buckets. We record the sequence of what you looked at, but not how long you spent on anything. No browser fingerprint. No precise coordinates.

We are interested in the stories that groups tell — which parts of the map draw attention, which proposals people compare, where the audit lands when people find it worth sharing. We are not interested in you specifically. The design makes "you specifically" technically unreachable, not merely against our policy.

If we were ordered by a court to identify a specific person from our data, we could not do it. That is not a promise. It is a structural fact.

---

## What GitHub Pages collects

This site is hosted on GitHub Pages. GitHub's servers automatically log basic request details when any page loads — your IP address, browser type, referring page, and timestamp. We do not receive or control these logs; they are governed by GitHub's Privacy Statement (docs.github.com/en/site-policy). We have no relationship with GitHub beyond hosting.

---

## Participation

When you open MapExplorer, you see one prompt: *Help us refine MapExplorer*.

If your browser has Do Not Track turned on, **No thanks** is pre-selected and the reason is shown. You can still switch to **Yes, I'll help** if you want.

If you choose **No thanks**, that is the end of it. Nothing is recorded for your session.

If you choose **Yes, I'll help**, we begin collecting your exploration path from that moment. Your answer is saved in a cookie so the prompt does not appear again on future visits.

---

## Do Not Track

If your browser sends a Do Not Track signal, **No thanks** is pre-selected when you open MapExplorer. You can override it — your explicit choice wins.

We take Do Not Track seriously at the database level too. If the code that handles this signal is ever changed without a corresponding update to our audit trail, our database automatically stops accepting new data until a human reviews the discrepancy. There is no way for this check to fail silently.

---

## What we collect

Only collected if you chose **Yes, I'll help**.

As you explore MapExplorer, we periodically record your exploration path — roughly every 30 seconds. Each step is one of:

- Which electoral district you clicked
- Which map you switched to
- Which data layer you turned on or off

We record what you looked at, in order — not how long you spent on each thing.

If you click **Share**, we also save your ending map view (which map is active, which overlays are on, roughly where your viewport is). This goes into a separate table with no link back to your exploration path — so no one can look up a share code and find out how you got there.

### What we record when you share

- Which map was active and which others were visible
- Which data layers were on
- Which district (if any) was highlighted
- Roughly where you were on the map and how zoomed in
- Roughly how long you had been on the page (one of five buckets: under 1 min, 1–3, 3–10, 10–30, 30+)
- Browser family (e.g. Chrome, Safari) — raw browser string is discarded
- Screen size, rounded to the nearest 100 pixels
- Device type: phone, tablet, or desktop
- Time zone and language (e.g. America/Edmonton, en-CA)
- Full date and time of the share
- If you loaded someone else's share code first, that code is noted as your starting point

---

## Optional: approximate region

When you share, you may be asked if you want to include your approximate location. This is entirely optional and separate from the main consent.

If you say yes, your browser fetches your GPS coordinates and we immediately round them to the nearest degree of latitude and longitude — a grid cell roughly 100 km across. The precise coordinates are discarded right there in the browser and never leave your device. What we receive is a broad region like "Calgary area" or "Peace Country."

---

## See what we see

The analytics dashboard shows the actual data we have collected — which districts people clicked, which maps they explored, and the full sequence of each session. Nothing is hidden or summarized away from it.

→ [Open the analytics dashboard](../dashboard)

---

## What we never collect

No name. No email. No IP address. No precise location. No raw browser fingerprint. No cross-session identifier — each page load gets a temporary ID that exists only in memory and disappears when you close the tab.

Everything is rounded or bucketed in your browser before anything is sent. The server never sees a precise value.

---

## Share codes

Share codes appear on screen and go to your clipboard only when you click Copy. They are never embedded in a URL, so they don't appear in browser history, server logs, or referrer headers. To load someone's shared view, the recipient types the code directly into the site.

Your most recent share code is stored in a cookie so your map view is restored on your next visit.

### There are only 19,200 possible codes

Share codes represent map configurations, not people. There are exactly 19,200 valid combinations of map, overlays, layers, and viewport region — so two people exploring independently can easily arrive at the same code. This is expected and intentional. When it happens, we record two arrivals at the same map state, which is exactly the signal we're looking for: it tells us that configuration is genuinely interesting, not just a one-off. No two sessions are merged or linked because of a shared code.

### What can and cannot be linked

Share codes and flight paths are impossible to link. They are stored in separate database tables with no shared key — not a privacy policy restriction, an architectural one. There is no query that connects them.

Web server logs work the same way. When your browser loads this page, GitHub's servers record your IP address. When your flight-path events reach our database, they carry a session identifier — a random string that exists only in your browser's memory for that page load. Your IP address is never stored in our database. The session identifier is never sent to GitHub's servers. The two pieces of information were never associated, so there is nothing to link.

---

## Cookies

This site sets one cookie that stores four things:

- **Your consent choice** — yes or no
- **Colour theme** — dark or light, if you changed it
- **Intro dismissed** — so the map introduction doesn't repeat
- **Last map view** — so your view is restored on your next visit

The cookie is encrypted in your browser before it is written — the server never sees the contents. It is only sent over HTTPS and is never shared with other sites. It expires after one year. You can remove it by clearing your cookies.

The last map view is encrypted because it encodes where you were in the map — which proposal you were looking at, which layers were on, where your viewport was. That is your business, not anyone else's.

---

## Data retention

All stored records are anonymized before they reach our database. We keep them indefinitely as research data. If we ever found that a record contained identifying information — which the design is built to prevent — we would delete it within 30 days.

---

## Your rights

You have the right not to be remembered.

- **Choose No thanks** at the prompt and nothing is recorded.
- **Turn on Do Not Track** in your browser and No thanks is pre-selected for you.
- **Delete a share code** by emailing it to wconn161@mtroyal.ca — we will delete it and confirm.
- **Confirm a share code exists or not** by emailing the same address. We cannot search by identity because none was collected.

---

## Contact

Will Conner
wconn161@mtroyal.ca

Independent research — not affiliated with or endorsed by any institution.

Questions and deletion requests answered within 10 business days.

---

## Policy updates

When this policy changes, the effective date at the top is updated and the change is committed to the public git repository (github.com/ixby/alberta-electoral-boundaries-audit). The commit history is the changelog. Any change that expands what is collected is noted in the commit message.
