# Sensitivity Analysis

This document reports the structural robustness of the core redistricting findings under systematic parameter variation. A hallmark of forensic gerrymandering detection is that the qualitative finding must survive reasonable perturbations of the procedural constraints. 

## Parameter Sweep Matrix

| Parameter | Baseline | Low | High | Result Stability |
|-----------|----------|-----|------|------------------|
| Population deviation (±) | 0.25 | 0.15 | 0.30 | `seats@50/50`: 48.31% → 47.7%–48.6% |
| Ensemble size | 250,000 | 100,000 | 2,000,000 | Percentile: p98.5 → p98.1–p98.9 |
| Buffer distance | 200m | 100m | 400m | Adjacent pairs: 127 → 124–131 |
| Vote Apportionment | v0.9 Topology | 70/30 Blend | 80/20 Blend | Direction held (Minority > Majority) |

## Key Findings

1. **Population Deviation Tolerance**: Under tighter statutory constraints (±15%), the ReCom ensemble median shifts slightly, but the minority map's 48.31% reading remains an extreme upper-tail outlier (p98+). 
2. **Ensemble Saturation**: The 250,000-sample size accurately captures the extreme tail. Scaling to 2,000,000 draws mathematically bounds the top end (identifying the "converged ceiling" at 51.72%), and the minority map's rank placement remains highly stable.
3. **Geometric Robustness**: Variations in buffering for intersection-detection (200m baseline) marginally alter adjacency-graph connectivity but do not open or close enough pathways to meaningfully affect the Markov chain's steady-state distribution.

**Conclusion**: All parameter perturbations preserve the qualitative finding. The minority map's fortification signature is structurally embedded and invariant to the procedural parameters of the evaluation apparatus.
