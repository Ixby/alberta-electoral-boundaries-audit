# Alberta Redistricting Audit — Moved

This file previously held a single compiled report. After the dual-audience remediation pass, the audit is published in two versions:

- **Public / Media edition:** [report_public.md](report_public.md)
- **Academic / Legal edition:** [report_academic.md](report_academic.md)

Both reports were updated in v0.3 with a red-team findings section at the top — three fortifications (Monte Carlo CI, declination metric, 2019 cross-election check) materially weakened the partisan-bias magnitude claim. The structural findings (population distribution, Calgary zone gap, community splits, visible boundary shapes, procedural concerns) are unchanged by the red-team pass.

See also:

- [Design critique](analysis/v0_1_design_critique.md) — hostile red-team pass against the audit's own methodology
- [Uncertainty analysis](analysis/v0_1_uncertainty_and_shapefile_impact.md) — confidence-interval and shapefile-impact assessment
- [Bias audit](analysis/v0_1_bias_audit.md) — self-audit that identified the class-A bias issues fixed in v0.2

**Author and audit design:** Will Conner, Mount Royal University, BSc Computer Information Systems (4th year student)

Repository: [Ixby/alberta-electoral-boundaries-audit](https://github.com/Ixby/alberta-electoral-boundaries-audit)
