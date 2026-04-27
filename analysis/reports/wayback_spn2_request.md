---
name: Wayback SPN2 authenticated-archival request
description: Draft request and self-serve runbook for obtaining authenticated Save Page Now 2 access from the Internet Archive, to close the 6–8 remaining unarchived URLs flagged in analysis/url_archival_log.md. Includes the self-serve path (IA S3 keys, no support request needed) and a fallback support email if quotas remain insufficient.
forward_dependencies:
  - analysis/url_archival_log.md (retry pass once auth is in hand)
  - FROZEN_MANIFEST.md (update snapshot columns after successful pass)
backward_dependencies:
  - analysis/url_archival_log.md (lists the unarchived URLs)
---

# Wayback SPN2 authenticated-archival request

**Status:** Draft. PO action required.

## What "SPN2 Bearer token" actually is

The Internet Archive does not issue per-request Bearer tokens for Save Page Now 2. SPN2 authenticates via the same S3-compatible access key and secret that every archive.org account can generate from its own account settings. "Authenticated SPN2" in this project's logs means using those S3 keys in the `Authorization` header; the quota for authenticated requests is materially higher than the anonymous IP-wide limit that blocked the Chrome-based retry.

## Self-serve path (recommended first)

Ten-minute task. No support ticket needed.

1. Create or sign in to an archive.org account at `https://archive.org/account/signup`.
2. Go to `https://archive.org/account/s3.php` and copy the `access` key and `secret` shown. These are your SPN2 credentials.
3. Export them to environment variables locally:
   ```
   set IA_ACCESS_KEY=<access>
   set IA_SECRET_KEY=<secret>
   ```
4. The retry pass can then send each POST to `https://web.archive.org/save` with the header:
   ```
   Authorization: LOW <access>:<secret>
   ```
5. Quota under authentication is ~4 captures per second with burst allowance, well above what 8 URLs need.

Once keys are in hand, the next session can re-spawn the archival sub-agent from the prompt preserved in `analysis/url_archival_log.md`, this time with the `Authorization` header populated.

## Fallback: support email (if self-serve quota still blocks)

Only send if the authenticated retry still hits a cap (unlikely for 8 URLs, but the fallback is documented here so the decision does not have to be re-made under time pressure).

**To:** `info@archive.org` (general) or `spn@archive.org` (Save Page Now team, if reachable)

**Subject:** Research-tier SPN2 rate limit — Canadian electoral boundary commission archival project (8 URLs)

Dear Internet Archive team,

I am a fourth-year Mount Royal University BSc student running a non-partisan academic audit of the Alberta Electoral Boundaries Commission's 2025–26 proposals. The audit depends on a durable third-party archival record of a set of commission and Elections Alberta pages, many of which are slated to come down after the commission's November 2026 report.

Using the CDX API and anonymous Save Page Now, I have successfully archived 19 of 27 priority URLs. The remaining 6–8 URLs hit an IP-wide anonymous-SPN rate cap during a retry pass and have not been preserved. I have an archive.org account with S3 access keys configured; before attempting a full authenticated retry, I wanted to confirm two things:

1. Whether a standard authenticated SPN2 pass is appropriate for a research-archival use of this scale, or whether you would prefer I request a research-tier elevation before running the pass.
2. Whether there is a documented ceiling on authenticated captures per day, so I can pace the request set accordingly.

The specific URLs are commission-proposal PDFs, public-submission portal pages, and Elections Alberta landing pages — all public, all already intended for preservation on archive.org's own terms. A full list is available on request.

Thank you for the service you provide; this work would not be possible without it.

Best,

Will Conner
BSc Computer Information Systems, 4th year
Mount Royal University
Calgary, Alberta, Canada
[email address]

GitHub: `https://github.com/Ixby/alberta-electoral-boundaries-audit`

## URL list (for either path)

The unarchived URLs are catalogued in `analysis/url_archival_log.md` under the "Chrome-based retry pass — 0 new captures" section. Pull the list from that file at run-time; do not duplicate it here (single source of truth).

## Decision point for PO

- **Fast path (recommended):** spend 10 minutes on self-serve, then next session re-spawns the archival sub-agent with credentials in env vars.
- **Formal path:** send the support email above and wait for reply. Adds a few days; only worth it if the self-serve path fails.

## Note on archive.ph as backup

`archive.ph` is used in some of the existing snapshots and requires no authentication. It is not as authoritative as the Internet Archive for academic or legal citation, but it is a credible secondary custody record. The retry pass should attempt IA first; fall back to archive.ph for any URL that IA still refuses.
