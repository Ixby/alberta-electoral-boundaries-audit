---
name: Track W — pre-registration platform survey and recommendation
description: Survey of third-party pre-registration platforms for the audit's November 2026 signature-detection checklist. Closes D17 (self-held pre-registration vulnerability) by identifying an external, neutral, time-stamped custodian for the pre-registered tests before the MLA-committee 91-seat map lands 2026-11-02.
forward_dependencies:
  - analysis/v0_1_pre_registration_draft.md (the submission-ready document itself)
  - Track C re-audit of November committee map (executed against the externally-held checklist)
  - report_academic.md §3.11 (baseline scorecard; the pre-registered tests are its forward column)
  - analysis/v0_1_red_team_round_2.md §D17 (vulnerability this closes)
backward_dependencies:
  - analysis/v0_1_track_c_checklist_baseline_scoring.md (test list, thresholds, pass/fail criteria)
  - report_public.md §"What a gerrymander in the 91-seat map would actually look like" (public-facing checklist)
  - report_academic.md §3.7–3.10 (signature-detection methodology)
---

# Track W — pre-registration platform survey and recommendation

**Date:** 2026-04-22
**Purpose:** Select a third-party platform to hold the audit's November 2026 signature-detection checklist as a time-stamped, externally-verifiable pre-registration. Closes D17 (self-held pre-registration vulnerability identified in `analysis/v0_1_red_team_round_2.md`).
**Scope:** Platform survey only. The pre-registration document itself is drafted in `analysis/v0_1_pre_registration_draft.md`; actual submission is reserved for the PO.

---

## What the audit needs from a platform

The November 2026 MLA-committee 91-seat map is due 2026-11-02. The audit's commitment is: a structured checklist of 17 signals (S1–S6 strong, W1–W3 weak, P1–P5 process, X1–X3 supplementary) will be scored on the new map within 72 hours of its release. For the commitment to have methodological force, the checklist must be held by a neutral party before the map lands, and the held version must be recoverable afterward in its original form with a verifiable timestamp.

Required platform features:

1. **Third-party custody.** The platform, not the audit author, holds the pre-registered document. The author cannot alter the held copy after submission.
2. **Time-stamp.** A verifiable submission date. The map is due 2026-11-02; the pre-registration must be dated before that.
3. **Public accessibility after the map lands.** Readers of the November re-audit must be able to retrieve the original pre-registered document and verify the audit did not change its criteria post-hoc.
4. **Support for structured checklist documents.** The audit does not need a clinical-trial CRF template. It needs to post a markdown or PDF document of 10–20 pages with numeric thresholds and pass/fail criteria.
5. **Free or low-cost.** This is a self-funded civic audit, not an institutionally-funded study. Paid-tier platforms are non-starters unless the free tier covers the use case.
6. **Optional: embargo until the map lands.** Not strictly required (the audit's criteria are public already in `report_public.md`), but an embargo lets the audit submit earlier without triggering speculation. The map-release date is not a secret and neither is the audit's methodology, so this is nice-to-have rather than load-bearing.

---

## Platform survey

### OSF (Open Science Framework) Registrations — osf.io

**Operator:** Center for Open Science (501(c)(3), Charlottesville VA). Founded 2013. Widely used in psychology, political science, economics, and other social sciences.

| Feature | OSF |
|---|---|
| Free / open | Yes. Free tier includes unlimited public registrations and 5 GB storage. |
| Third-party custody | Yes. Once a registration is submitted, the content is locked and archived; the author cannot edit the registered version (edits produce a new version with a new timestamp, with the original preserved). |
| Time-stamp | Yes. Each registration gets a permanent URL, a DOI, and a server-side submission timestamp. |
| Public accessibility | Yes by default; private registrations can be embargoed for up to 4 years, then auto-release. |
| Embargo until specific date | Yes. The embargo end-date is configurable; readers see a stub with the DOI and the embargo-end date, and the full document releases automatically on that date (or on demand earlier). |
| Document format | Accepts markdown, PDF, plain text, images, or structured forms. The audit's checklist fits in any of these. OSF also offers registration templates (e.g., PRP-QUANT, Preregistration Template via AsPredicted) but a blank "OSF Preregistration" template accepts arbitrary prose. |
| Political-science fit | Widely used. The *Journal of Politics*, *Political Analysis*, *American Journal of Political Science*, and EGAP (Evidence in Governance and Politics) all reference OSF registrations. |
| Revocation risk | Low. OSF withdrawals leave a tombstone record with the withdrawal reason, not silent deletion. The audit cannot make a pre-registration disappear. |
| Author persistence | OSF accounts are free and tied to email + ORCID. The audit can register without institutional credentials. |

**Drawbacks.** None material for this use case. OSF is the strongest fit.

### AsPredicted — aspredicted.org

**Operator:** Wharton Credibility Lab (University of Pennsylvania). Founded 2015.

| Feature | AsPredicted |
|---|---|
| Free / open | Yes. Free and open to academics and non-academics. |
| Third-party custody | Yes. Registration is locked on submission; the author cannot edit. |
| Time-stamp | Yes. Server-side timestamp, unique URL. |
| Public accessibility | The registration is private by default and becomes public when the author flips a switch (typically at manuscript submission). Unlike OSF, AsPredicted does not support a scheduled auto-release. |
| Embargo until specific date | No scheduled date. The author manually makes the registration public when ready. This requires the author to actively release on 2026-11-02, rather than the platform releasing automatically. |
| Document format | Structured 9-question template only (hypothesis, DV, conditions, analysis plan, outliers and exclusions, sample size, other, name, prior work). No free-form document upload. |
| Political-science fit | Designed for experimental social science. Accepts non-experimental registrations but the 9-question template is framed around experiment design. |
| Revocation risk | Low. |
| Author persistence | Accounts are free, email-based. |

**Drawbacks.** The 9-question structured template is a poor fit for a 17-signal checklist with numeric thresholds, pass/fail criteria, and a scoring table. The audit could shoehorn the checklist into the "other" field, but it would lose the document structure readers need. The manual-release model (no scheduled auto-release) also means a 2026-11-02 embargo requires active hand-release by the author on that date, adding an action item with a hard deadline.

### ClinicalTrials.gov

Not applicable. Medical-trial registry only. The audit is not a medical study and the platform does not accept political-science pre-registrations.

### Registered Reports via journal submission

**Examples:** *Political Analysis* (Oxford; Stage 1 Registered Reports accepted), *Election Law Journal* (Liebert; no formal RR track as of 2026), *Journal of Politics* (no formal RR track), *British Journal of Political Science* (limited RR pilot).

| Feature | Registered Reports |
|---|---|
| Free / open | Typically free to submit. Open-access fees may apply on acceptance. |
| Third-party custody | Yes — the journal's editorial board. This is the gold-standard D17 cure: the scorer and defender are formally separated by an editorial review. |
| Time-stamp | Yes, via journal submission records. Stage 1 acceptance (in-principle acceptance) is publicly recorded on the journal's site. |
| Public accessibility | High once Stage 1 is accepted. Pre-Stage 1, visibility is editor-only. |
| Embargo until specific date | Implicit: the Stage 1 protocol is reviewed and accepted before data collection (map release in this case); Stage 2 publishes the full results after. |
| Document format | Full article structure (intro, methods, analysis plan). More elaborate than a checklist. |
| Political-science fit | *Political Analysis* is the leading outlet. Turnaround is 2–4 months for Stage 1 review. |
| Drawbacks | **Timeline.** The map lands 2026-11-02. Submitting a Stage 1 protocol today (2026-04-22) leaves ~6 months for Stage 1 review, which is feasible but tight. Rejection at Stage 1 consumes time with no fallback. External editorial control also means the audit cannot guarantee which tests the journal accepts in the protocol. |

Registered Reports are the strongest D17 cure in principle (editorial custody is maximally external) but operationally heavier than the audit needs and exposed to journal-timeline risk.

---

## Recommendation

**Primary platform: OSF Registrations.**

OSF satisfies every required feature and most of the nice-to-haves:
- Free, open, institutionally independent.
- Server-side timestamp with permanent DOI.
- Embargo with scheduled auto-release on a specific date — the audit can submit now, set the embargo to 2026-11-02, and the registration auto-releases on the map's due date. If the committee's map slips, the release can be pushed.
- Accepts free-form markdown or PDF, so the 17-signal checklist can be posted in full with numeric thresholds and pass/fail criteria preserved.
- Archives withdrawn registrations as tombstones, preventing silent deletion.
- Widely recognised in political science and adjacent fields.

**Secondary / complementary:** submit the same pre-registration document as a Stage 1 Registered Report to *Political Analysis* if a peer-reviewed custodial layer is desired on top of OSF. The two can coexist: OSF holds the time-stamped version immediately; the journal reviews the same document at its own cadence. This is not required for D17 closure — OSF alone suffices — but is available if the PO wants maximum methodological rigour.

**Rejected alternatives:**
- AsPredicted: the 9-question template does not fit a 17-signal checklist, and manual release on map-release day adds an action item with a hard deadline.
- ClinicalTrials.gov: not applicable.
- Standalone Registered Reports (without OSF): journal-timeline risk. If Stage 1 review is not complete by 2026-11-02, the audit has no time-stamped custody.

---

## D17 closure argument

D17's attack (`analysis/v0_1_red_team_round_2.md`) is: "the audit's November checklist is self-held; the scorer and the defender are the same person." Posting the checklist to OSF before 2026-11-02 closes this vulnerability on three counts:

1. **Custody.** The checklist is held by a 501(c)(3) organisation (Center for Open Science), not by the audit author. COS cannot modify the registered content, and the audit author cannot alter the registered copy after submission.
2. **Timestamp.** The registration carries a server-side submission date, cryptographically unalterable in the OSF archive. A reader of the November re-audit can verify the pre-registration predated the map.
3. **Falsifiability.** The pre-registered document includes explicit "what would falsify the audit's critique" criteria (see the draft document). The audit commits to those criteria before seeing the map, so passing or failing them after the map lands is a verifiable claim, not a post-hoc rationalisation.

D17 is not fully closed until the registration is actually submitted and a DOI assigned. Drafting the document (this task) is Phase 1; submission (PO-held) is Phase 2.

---

## Submission instructions (OSF) — for the PO to execute

The pre-registration draft is `analysis/v0_1_pre_registration_draft.md`. The PO retains submission authority. The steps below assume OSF as the chosen platform per the recommendation above. Estimated wall time for a first-time user: 30–45 minutes.

### Pre-submission checklist

- [ ] Confirm the draft document (`analysis/v0_1_pre_registration_draft.md`) is final. Any edit after OSF submission creates a new version; the original timestamp is preserved but subsequent edits are visible.
- [ ] Confirm author identity: Will Conner, independent civic audit, no institutional affiliation to declare.
- [ ] Decide on the ORCID question. ORCID is free (orcid.org) and an ORCID ID linked to the OSF account strengthens author persistence. Optional but recommended.
- [ ] Decide on the embargo date. Recommended: 2026-11-02 (the committee's stated map release date) with a 14-day fallback to 2026-11-16 if the committee slips. OSF allows the embargo end-date to be adjusted post-submission.
- [ ] Export the draft to PDF for clean archival, in addition to keeping the markdown source. OSF accepts both; PDF is the preferred archival format.

### Step-by-step OSF submission

1. **Create or sign in to an OSF account.**
   - Navigate to `https://osf.io/register` (or `https://osf.io/login`).
   - Use a persistent email (not a temporary address) — OSF uses email as the primary account identifier.
   - If creating a new account, link ORCID during sign-up if available.

2. **Create a new Project.**
   - Click "Create new project" on the OSF dashboard.
   - Title: *Alberta Electoral Boundaries Audit — November 2026 Pre-registered Signature-Detection Checklist*.
   - Description: Paste §1 (Title and metadata) from the pre-registration draft.
   - Storage region: Canada if the option appears (OSF stores in multiple regions); otherwise leave default.
   - Visibility: Private during preparation; will be made public via the registration flow.

3. **Upload the pre-registration document.**
   - In the project's Files tab, upload the PDF export of `analysis/v0_1_pre_registration_draft.md`.
   - Also upload the markdown source for reproducibility.
   - Optional: upload a copy of `analysis/v0_1_track_c_checklist_baseline_scoring.md` as the baseline scorecard referenced in §3.

4. **Start a new Registration.**
   - From the project page, click the "Registrations" tab, then "Add New Registration."
   - Registration template: choose **"OSF Preregistration"** (the general-purpose template). Do not pick PRP-QUANT or the AsPredicted-derived template; the 17-signal checklist does not fit their structured forms.
   - In each template field, either (a) paste the corresponding section from the draft, or (b) write "See attached pre-registration document" and rely on the uploaded PDF as the authoritative content.

5. **Fill the registration metadata.**
   - *Contributors:* Will Conner (primary and corresponding).
   - *License:* CC BY 4.0 (permissive; allows readers to cite and reproduce). Alternative: CC BY-NC 4.0 if the audit prefers a non-commercial restriction.
   - *Keywords:* electoral boundaries, gerrymandering, pre-registration, Alberta, redistricting, political science, signature detection, MCMC ensemble.
   - *Subjects:* Political Science; Social and Behavioral Sciences.
   - *Associated project:* link back to the OSF project created in Step 2.

6. **Configure the embargo.**
   - Select "Enter registration into embargo."
   - Embargo end-date: 2026-11-02 (or later, per the fallback decision in the pre-submission checklist).
   - Embargo content: public stub visible (title, author, DOI, embargo end-date); full document hidden until embargo ends, then auto-released.
   - Note: even under embargo, the server-side submission timestamp is part of the DOI metadata and is verifiable by any reader once the embargo lifts.

7. **Certify and submit.**
   - OSF asks the author to certify: (a) the registration is the author's own work; (b) the registration does not contain protected or confidential information; (c) the author agrees to OSF's terms of service.
   - Submit. OSF assigns a DOI (format: `10.17605/OSF.IO/XXXXX`) and a permanent URL (`https://osf.io/XXXXX`).

8. **Record the DOI.**
   - Copy the assigned DOI into the audit's `README.md` under a "Pre-registration" heading.
   - Reference the DOI in the next update of `report_academic.md` §3.11 and `report_public.md` §"What a gerrymander in the 91-seat map would actually look like."
   - Retain the OSF confirmation email as a secondary timestamp record.

### Optional Phase 3b — Registered Report at *Political Analysis*

If the PO wants an additional, peer-reviewed layer of custody on top of OSF:

1. Navigate to the *Political Analysis* author portal at `academic.oup.com/pan`.
2. Prepare a Stage 1 Registered Report package containing: the pre-registration document (as Methods/Analysis Plan), a brief Introduction (the §2 Background in the draft, expanded slightly for an academic reader), and the Reference list.
3. Submit Stage 1 for editorial review. Review typically takes 8–12 weeks. If accepted in-principle before 2026-11-02, the journal holds Stage 2 (results) for submission after scoring.
4. If not accepted in-principle by 2026-11-02, the audit still has OSF custody — the journal route is additive, not replacement.

### What the PO retains authority over

- Whether to submit at all.
- The embargo end-date.
- The license choice (CC BY 4.0 vs CC BY-NC 4.0).
- Whether to pursue the *Political Analysis* Stage 1 track in parallel.
- Whether to link an ORCID.
- Whether to cross-post the DOI to the audit's repository README before or after the embargo lifts.

This sub-agent has not created an OSF account, submitted the registration, or contacted any journal. The draft document is ready for the PO or parent session to take the steps above.

---

## Data provenance

- OSF feature set: osf.io/registries (as of 2026-04-22); Center for Open Science documentation.
- AsPredicted feature set: aspredicted.org (as of 2026-04-22); Wharton Credibility Lab documentation.
- Registered Reports at *Political Analysis*: Oxford Academic journal pages (as of 2026-04-22).
- D17 vulnerability: `analysis/v0_1_red_team_round_2.md`.
- Checklist content source: `analysis/v0_1_track_c_checklist_baseline_scoring.md` and `report_public.md` §"What a gerrymander in the 91-seat map would actually look like".
