# ChangeDetection.io watcher — Elections Alberta shapefile release

This document is the setup guide for the **primary detector** in the audit's automation pipeline: a [ChangeDetection.io](https://changedetection.io/) watcher that monitors Elections Alberta's web pages for the release of the official 2026 boundary shapefiles. When the watcher detects a change, it fires a webhook to the audit's GitHub Actions workflow, which automatically runs the audit pipeline against the new files.

The architecture:

```
Elections Alberta web page
        |
        | (polled every 12 hours)
        v
ChangeDetection.io watcher
        |
        | (webhook fires on detected change)
        v
GitHub Actions repository_dispatch event
        |
        v
recompute-on-shapefile-release.yml workflow
        |
        | (runs ~90 min on GitHub-hosted runner)
        v
Draft PR opened with regenerated artefacts
        |
        v
Maintainer reviews, merges, files OSF amendment
```

A scheduled Sunday-06:00-UTC backstop in the GitHub workflow runs the same pipeline weekly even if the watcher is offline or misses a release. The pipeline is idempotent: re-running with the same shapefiles produces the same outputs and doesn't open a new PR.

---

## Prerequisites

You need:

1. A ChangeDetection.io instance. Two options:
   - **Hosted (easier):** sign up at <https://changedetection.io/> ($8.99/mo as of 2026; first watch free for 14 days)
   - **Self-hosted (cheaper, more work):** run it in Docker on a small VPS or home server (config below)
2. A GitHub personal access token (PAT) with `repo` scope, for the watcher's webhook to fire `repository_dispatch` events
3. The audit's GitHub repository (this one) with the workflow file at `.github/workflows/recompute-on-shapefile-release.yml`

---

## Step 1 — Set up ChangeDetection.io

### Option A: Hosted

Sign up at <https://changedetection.io/>. The dashboard appears at `https://lemonade.changedetection.io/` (or whatever subdomain is assigned).

### Option B: Self-hosted (Docker)

```bash
mkdir -p ~/changedetection-data
docker run -d --restart always \
  -p 5000:5000 \
  -v ~/changedetection-data:/datastore \
  --name changedetection \
  ghcr.io/dgtlmoon/changedetection.io:latest
```

Visit `http://localhost:5000` (or your VPS IP) to access the dashboard.

---

## Step 2 — Add the watched pages

Add these three watches to ChangeDetection.io. For each: create a new watch, paste the URL, set the polling interval to **12 hours** (Elections Alberta is unlikely to release files at non-business hours; this minimises poll burden while keeping detection latency bounded).

### Watch 1: Elections Alberta GIS data landing page

- **URL:** `https://www.elections.ab.ca/resource-centre/maps-data/`
- **Trigger:** Any change in the rendered text (default)
- **CSS Filter:** `main` (only watch the main content area; ignores nav/footer changes)
- **Tag:** `elections-alberta-shapefiles`

### Watch 2: Alberta Electoral Boundaries Commission landing page

- **URL:** `https://www.abebc.ca/`
- **Trigger:** Any change in the rendered text
- **CSS Filter:** `main, .content` (depending on the site's actual structure — adjust after first load)
- **Tag:** `elections-alberta-shapefiles`

### Watch 3: Alternate maps-and-GIS-data page (in case Elections Alberta restructures)

- **URL:** `https://www.elections.ab.ca/resources/maps-and-gis-data/`
- **Trigger:** Any change
- **CSS Filter:** `main`
- **Tag:** `elections-alberta-shapefiles`

The polling poller (`analysis/scripts/automation/poll_elections_alberta.py`) keeps this same URL list in sync; if you add/remove a watch here, also update the script's `WATCHED_PAGES` list.

---

## Step 3 — Configure the webhook to fire GitHub Actions

In ChangeDetection.io, go to **Settings → Notifications**. Add a new notification with:

- **Notification URL:**
  ```
  https://api.github.com/repos/Ixby/alberta-electoral-boundaries-audit/dispatches?token=YOUR_GITHUB_PAT
  ```
  Replace `YOUR_GITHUB_PAT` with a [fine-grained personal access token](https://github.com/settings/tokens?type=beta) that has **Contents: read+write** and **Actions: read+write** permissions on this repository.

- **Notification body (JSON):**
  ```json
  {
    "event_type": "elections-alberta-shapefile-released",
    "client_payload": {
      "watch_url": "{{watch_url}}",
      "watch_title": "{{watch_title}}",
      "diff_url": "{{diff_url}}",
      "current_snapshot": "{{current_snapshot}}",
      "majority_url": "MANUAL_FILL_OR_AUTO_DETECT",
      "minority_url": "MANUAL_FILL_OR_AUTO_DETECT"
    }
  }
  ```

- **Request method:** POST
- **Trigger:** **Only fire on tagged watches** (set tag to `elections-alberta-shapefiles` so unrelated watches don't trigger the audit pipeline)

The `majority_url` and `minority_url` fields will need to be filled by the maintainer after the watcher fires (since the watcher detects "the page changed" but doesn't reliably identify which links are the new shapefiles vs old ones still on the page). The poller script `poll_elections_alberta.py` is the auto-detection backstop; if it identifies the files unambiguously, the workflow uses them automatically.

---

## Step 4 — Test the trigger end-to-end

Without waiting for an actual release:

1. In ChangeDetection.io, manually click **"Re-check"** on one of the watches → **"Mark as triggered"** to simulate a detected change
2. Confirm the webhook fires (check the notification log in ChangeDetection.io's UI)
3. Check GitHub Actions — the `recompute-on-shapefile-release.yml` workflow should appear in the run history with trigger source `repository_dispatch`
4. The workflow will fail the "Resolve shapefile inputs" step (since no real URLs were provided), but the trigger chain is verified

Or trigger the workflow directly from the GitHub Actions UI using `workflow_dispatch` and provide test URLs (e.g., the audit's own DPG-reconstructed shapefiles to verify the pipeline runs end-to-end against any input).

---

## Step 5 — Notification of completion

Set the workflow's `NOTIFY_WEBHOOK_URL` repository secret to a Slack/Discord/Teams incoming webhook, an email-relay endpoint, or any URL that accepts a JSON POST with a `{"text": "..."}` body. The workflow's final step posts there when the recompute completes and the draft PR is open.

---

## Operational notes

**Polling frequency.** 12 hours is the recommended interval. Elections Alberta doesn't release files outside business hours, and a 12-hour interval keeps the detection-to-PR latency under 24 hours while minimising load on Elections Alberta's servers (be a polite scraper).

**False positives.** The watcher will fire on any text change on the watched pages, including unrelated content updates (news posts, navigation changes, etc.). The workflow's "Resolve shapefile inputs" step checks for actual `.gpkg`/`.zip` files; if none are found, it exits cleanly without recomputing. False positives are tolerable; false negatives (missing a real release) are why the Sunday backstop exists.

**False negatives.** The watcher might miss a release if Elections Alberta hosts the files on a new URL not in the watch list. The Sunday backstop's poller script (`poll_elections_alberta.py`) traverses each page looking for shapefile links, so even if the page text doesn't change in a way the watcher detects, the backstop still finds new files.

**Cost.** Hosted ChangeDetection.io: $8.99/month. Self-hosted: ~$5/month for a small VPS (DigitalOcean droplet, Vultr, etc.) or free if you have a home server. GitHub Actions: free for public repositories within the 2,000-minute monthly free tier (the recompute uses 90-180 min per run; well inside the budget for the expected one-or-two trigger events per year).

**Maintenance.** Re-verify the watched URLs annually. Elections Alberta has restructured its site twice since 2020; if the URLs in `WATCHED_PAGES` (in `poll_elections_alberta.py`) and in the ChangeDetection.io watches go stale, update both in sync.

---

## What this pipeline does NOT do

- It does **not** auto-merge the draft PR. The maintainer reviews the deltas, updates prose, computes shapefile hashes, and merges manually.
- It does **not** file the OSF pre-registration amendment. The maintainer uploads the amendment to OSF Registrations manually.
- It does **not** publish the updated public report. The maintainer decides whether the deltas warrant re-publication or just an updated PDF.

The pipeline produces evidence; the human signs off on the conclusions. That separation is deliberate — the audit's defensibility depends on every published claim being maintainer-reviewed, not on auto-publishing whatever the pipeline produces.
