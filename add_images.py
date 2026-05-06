import re

with open('report_public.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix existing broken PNG links to SVG
text = text.replace('data/maps/article/lane2_bars.png', 'data/maps/article/lane2_bars.svg')
text = text.replace('data/maps/article/verdict_quadrant.png', 'data/maps/article/verdict_quadrant.svg')

# Insert lane1_dotplot under Part II
if 'lane1_dotplot.svg' not in text:
    target = '## Part II: The 250,000-Map Litmus Test {.new-page}'
    if target in text:
        insert = '\n\n![How skewed each map looks on the partisan-fairness number. Both 2026 maps sit beyond the Alberta line at ~5%; only the minority also crosses the US line at 7%. The further right the dot, the more the map favours the UCP relative to its provincial vote share.](data/maps/article/lane1_dotplot.svg)\n\n'
        text = text.replace(target, target + insert)

# Insert airdrie and calgary/lethbridge images under Part III
if 'figure_airdrie_v3.svg' not in text:
    target = '## Part III: Cracking, Packing, and Draining'
    if target in text:
        insert = '\n\n![The division of Airdrie into four separate districts, diluting its urban voting power.](data/maps/article/figure_airdrie_v3.svg)\n\n'
        text = text.replace(target, target + insert)

if 'Minority_Draining_Lethbridge-West.svg' not in text:
    target2 = '**Lethbridge (4 new hybrids):**'
    if target2 in text:
        insert2 = '\n\n![The draining of Lethbridge into rural peripheries.](scratch/story_proofs/Minority_Draining_Lethbridge-West.svg)\n\n'
        text = text.replace(target2, target2 + insert2)
        
if 'Majority_Cracking_Calgary-Glenmore.svg' not in text:
    target3 = '**Calgary (7 new hybrids):**'
    if target3 in text:
        insert3 = '\n\n![The localized packing in Calgary-Glenmore.](scratch/story_proofs/Majority_Cracking_Calgary-Glenmore.svg)\n\n'
        text = text.replace(target3, target3 + insert3)

with open('report_public.md', 'w', encoding='utf-8') as f:
    f.write(text)
print("Images restored successfully.")
