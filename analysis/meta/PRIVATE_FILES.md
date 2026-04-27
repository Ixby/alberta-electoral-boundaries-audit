# Private Files

The following files exist locally but are excluded from this repository via `.gitignore`.
They are stored in `private/` or other gitignored locations.

## Moved to `private/` (2026-04-23)

| Original path | Reason |
|---|---|
| `migration.md` | Session handoff log / token tracking — internal |
| `CLAUDE.md` | AI session bootstrap — internal tool |
| `v1_2_gerrymander_audit_prompt.md` | Claude execution prompt — internal tool |
| `report_public.md` | Build scaffold for magazine PDF — not a standalone science output |
| `report_public.pdf` | Magazine PDF — kept private |
| `analysis/v0_1_duane_bratt_outreach_email.md` | Draft personal outreach email |
| `analysis/live_tasks.md` | Live session task tracker |
| `analysis/v0_1_elections_alberta_shapefile_request.md` | FOIP correspondence with Elections Alberta |
| `analysis/url_archival_log.md` | URL archival execution log |

## Deleted (2026-04-23)

- `analysis/v0_1_three_map_partisan_comparison.html` — generated output, regenerable
- `data/reference/polling_338_historical/alberta_landing_raw.html` — scraping cache
- `data/reference/polling_338_historical/riding_1001_w20230529.html` … `riding_1087_w20230529.html` (87 files) — scraping cache

## Red team consolidation (2026-04-23)

23 red team files consolidated into `analysis/methodology/red_team_consolidated.md`:
- `analysis/red_team/` (14 files) — untracked, deleted after merge
- `analysis/v0_1_science_red_team_*.md` (3 files) — untracked, deleted after merge
- `analysis/reports/design_critique.md` — untracked, deleted after merge
- `analysis/methodology/editorial_pass_log.md` — untracked, deleted after merge
- `historical/v0_1_red_team_academic_discredit.md` — tracked, untracked + deleted after merge
- `historical/v0_1_red_team_round_2.md` — tracked, untracked + deleted after merge
- `historical/v0_2_final_redteam.md` — tracked, untracked + deleted after merge
- `historical/v1_2_prompt_redteam.md` — tracked, untracked + deleted after merge
