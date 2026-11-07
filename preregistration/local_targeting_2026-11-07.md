# Signs of local targeting in the panel's changes (written before any computation)

> Written 2026-11-07, about 9:40 AM Alberta Time (UTC−6), before any figure below has been computed. Unregistered and not blind. Requested by the author on 2026-11-07. The author's message used a coined political label for local gerrymandering; the audit uses neutral terms. All ballots are primary. Nothing here says whether any map is a gerrymander or why any line was drawn.

The question is whether the panel's changes, relative to the commission majority's map, fall on competitive seats more than chance would suggest, and whether their effect on margins runs one way.

## A. Were competitive seats more likely to be changed?

- **Unit:** each of the commission majority's 89 divisions.
- **Changed:** no panel division has exactly the same voting areas.
- **Groups:** competitive (2023 all-ballots margin within 10 points) against the rest, and NDP-won against UCP-won.
- **Test:** Fisher's exact test, two-sided.
- **Confound, stated now:** the two restorations force a cascade through rural central Alberta, where seats are safe UCP, so changed divisions are not a random sample. A difference in rates does not by itself show targeting.

## B. Which way did the changes move margins?

- **Matching:** each panel division that differs from the majority's is matched to the majority division supplying most of its 2021 population.
- **Reported:** each pair's margin change (NDP minus UCP, all ballots), and the count, among pairs within 10 points on either map, moving toward the UCP and toward the NDP.
- **Test:** a two-sided sign test on those counts.

## C. Where did the moved voters' NDP votes go?

- **The voters:** those in voting areas that change division.
- **Where they came from:** were they in a seat the NDP won, nearly won (lost by under 10), or lost by 10 or more on the majority's map?
- **Where they went:** the same three categories on the panel's map.
- **Reported:** the full transition table of NDP votes.
- **Read as cracking:** the share that moves from won or near-won seats into seats lost by 10 or more.

## Afterwards

All comparisons go into the ledger (`findings/test_ledger/`) with the multiple-testing correction.

**Signed:** Claude (acting as session agent), directed by Will Conner
