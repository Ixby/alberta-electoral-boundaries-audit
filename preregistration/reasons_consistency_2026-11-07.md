# Consistency of the panel's stated reasons (written before any computation)

> Written 2026-11-07, about 9:50 AM Alberta Time (UTC−6). Unregistered and not blind: the Lethbridge and Banff results, and the quotes already cited ("Lethbridge already has population to spare", "a minor change ... to capture the necessary population", "much more regular polygon shape with straight line boundaries"), are known. Requested by the author on 2026-11-07. GitHub only; no OSF filing. Nothing here says whether any map is a gerrymander or why a line was drawn. A reason applied inconsistently is evidence for the effective-representation and statutory questions, not proof of intent.

## Method

1. **Extract the reasons.** List every reason and general principle the panel majority states for each changed or new division, with verbatim quotes and page references. A reading agent does the extraction, and each quote used is then checked against the page text (`findings/reasons_consistency/stated_reasons.json`). The minority's direct counters are kept beside them.
2. **Test the reasons that can be measured** against the panel's own map. A reason is applied consistently if the panel's map treats comparable cases the same way.
   - **M1, "population to spare":** for every city of 20,000 or more, compute its July 2024 municipal estimate (public OSI file, `data/osi/`) divided by the panel's average division population (53,722). Report the number of divisions holding it and whether it is combined with rural areas. If Lethbridge's ratio is not distinctly above those of cities the panel kept urban, this reason is not applied consistently.
   - **M2, "necessary population":** for Banff-Canmore-Diamond Valley, and for each Lethbridge division, compare the population the panel added or moved with the minimum needed to bring the commission majority's version inside ±25% of the 91-division average (40,292 to 67,153).
   - **M3, "regular shapes":** compare the compactness (Polsby-Popper, lines simplified to 50 m) of each changed panel division with its majority predecessor, the majority division that supplies most of its population. The reason is applied consistently if the divisions the panel defends on shape got more regular, and others did not get markedly less regular without a stated reason.
   - **M4, s.15(2):** check the panel's grants and refusals against the five statutory criteria and against its own stated purpose for s.15(2).
3. **Reasons that cannot be measured** (communities of interest, functional integration, regional representation) are listed with the panel's evidence, the minority's counter, and whether the panel applies the same reasoning to other comparable places in its report.

## Reading

Each check is reported as consistent, inconsistent or not testable, with the numbers and quotes. No overall score is formed.

**Signed:** Claude (acting as session agent), directed by Will Conner
