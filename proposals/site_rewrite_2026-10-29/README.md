# Main-page rewrite, 2026-10-29

**Status:** accepted by the author for implementation; implemented in the PR that adds this folder. Publication waits on the author's read.

The main page was rebuilt around three questions (what happened, how, how we know) and ends on the November test. The fourteen-item evidence log moved, in full, to `/evidence`; the reform suggestions moved to `/fixes`. The smoking-gun metaphor is gone.

| File | What it is |
|---|---|
| `rewrite_draft.md` | The accepted text, with a source comment after every paragraph (`en.ts` key, legal-memo row, or `[verify]`) |
| `section_review.md` | Every section of the old page: its job in the old story and the new one, a prose verdict, keep / change / move / cut |
| `cut_add_change.md` | The three lists behind the restructure |
| `legal_framework.md` | What the Constitution and Alberta law require of districts and the process; citation table with verification status |
| `gen_home.py` | Generates the `home.*` strings in `en.ts` and the matching main-page markup from the draft in one pass, so keys and markup cannot drift |

Open checks before publishing are listed in the PR description. The working review is the "Audit Site Proposals" document (shared separately).
