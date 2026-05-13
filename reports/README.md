Published report outputs.

| Directory | Contents |
|---|---|
| `academic/` | Full technical monograph (`report_academic.md`, `report_academic.pdf`) — APA citations, full methodology, statistical appendices |
| `public/` | Plain-language summary (`report_public.md`, `report_public.pdf`) — grade-9 reading level, subject-matter-naive audience |
| `assets/` | Figures, tables, and supporting assets shared across both reports |

## Generating PDFs

```bash
# Rebuild the academic PDF
python analysis/scripts/build_academic_pdf.py

# Rebuild the public PDF
python analysis/scripts/build_pdf.py
```

Both scripts require Chrome or Edge at a standard Windows install path. Output PDFs are written back into the respective subdirectory (`reports/academic/` and `reports/public/`).

## Report discipline

Both reports have a **DOCUMENTED CORRECTIONS** box. Retracted findings go there — never delete silently. When a finding changes: update the relevant section, add a corrections entry, and check `docs/FROZEN_MANIFEST.md` for any URLs that need re-archiving.
