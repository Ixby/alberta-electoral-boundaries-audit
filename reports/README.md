<!--
© Will Conner 2026 | CC BY-NC-SA 4.0 <https://creativecommons.org/licenses/by-nc-sa/4.0/>
Data: Elections Alberta (public domain) | https://ixby.github.io
-->
> **Backward:**
> - (none — index/README for the reports/ directory)
>
> **Forward:**
> - (leaf — directory index; reviewer-facing navigation)

Published report outputs.

| Directory | Contents |
|---|---|
| `academic/` | Full technical monograph (`report_academic.md`, `report_academic.pdf`) — APA citations, full methodology, statistical appendices |
| `public/` | Plain-language summary (`report_public.md`) — plain-language, subject-matter-naive audience (published as markdown only; PDF retired 2026-07-11) |
| `assets/` | Figures, tables, and supporting assets shared across both reports |

## Generating PDFs

```bash
# Rebuild the academic PDF
python analysis/scripts/build_academic_pdf.py
```

The script requires Chrome or Edge at a standard Windows install path; output is written to `reports/academic/`. The public report has no PDF build — it is published as markdown only.

## Report discipline

Both reports have a **DOCUMENTED CORRECTIONS** box. Retracted findings go there — never delete silently. When a finding changes: update the relevant section, add a corrections entry, and check `docs/FROZEN_MANIFEST.md` for any URLs that need re-archiving.