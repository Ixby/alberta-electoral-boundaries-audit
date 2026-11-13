# Submission-archive counts behind the IAP review (M2, N2-N6)

Companion to `claims_graded.md`. Copied from the working check file `W_archive.md` (2026-11-02): method, counts, ID lists and borderline lists are unchanged. Only personal names that no claim names were replaced by roles. Verdict lines below are the checker's working labels; the graded verdicts in `claims_graded.md` take precedence (notably N2, graded "cannot be checked as stated" because the minority's base, Lethbridge residents who weighed in, cannot be rebuilt: residence is redacted in the archive). Data only; no gerrymander verdicts. The archive is the Commission's 2025-26 submission archive (R1 = 170 written submissions, R2 = 1,082). IDs `1-NNNN` / `2-NNNN` = EBC-2025-1-NNNN / EBC-2025-2-NNNN. Scripts named below were run from a local scratch folder and are not committed.

---

Started 2026-11-02. Data only; no gerrymander verdicts.

## M2 (IAP p.23) Leduc-Beaumont request and Beaumont objection to Sherwood Park pairing
**Verdict: HOLDS (mostly) for Beaumont residents and Beaumont's mayor; PARTLY for "Leduc residents" and "their mayors" (no City of Leduc resident or mayor found asking for it; Leduc County mayor and Beaumont mayor did).**

Note: IDs below use shorthand `1-NNNN` = EBC-2025-1-NNNN, `2-NNNN` = EBC-2025-2-NNNN.

### Method
- Rounds searched: R1 (170) and R2 (1,082) submission texts plus hansard_r1/hansard_r2.
- Terms: regex `beaumont` (case-insens.) over all text files = 6 R1 + 236 R2 files mention Beaumont; `Leduc` for Leduc-only mentions; `mayor` filtered to Leduc/Beaumont; hansard grep for `Mayor, City of Beaumont`, `Mayor, County of Leduc`, `City of Leduc`.
- Body text taken after "Submission" and before "Terms By clicking". Written submission texts do not reliably show municipality, so "Beaumont resident" is only what the text says (e.g. "our city", "resident of Beaumont") or content (inference).
- "Beaumont-voice objection" = Beaumont named AND text objects to splitting Beaumont / moving part of it into Strathcona-Sherwood Park AND speaks from the Beaumont side (not a Strathcona-Sherwood Park resident writing about Heritage Hills). "Strathcona-side" = writer self-identifies in Strathcona/Sherwood Park or defends Heritage Hills/the existing constituency.
- Script: C:/tmp/ceb_w/beau.py, beau3.py (regex split|divid|fracture|half|two ridings, then manual exclusion list of Strathcona-side/other).
- Interim-report context (inference from texts): R2 objections concern the interim proposal splitting Beaumont along 50 St, east half into Strathcona-Sherwood Park, west half with Leduc-Beaumont.

### Counts
- R2 Beaumont-voice objections to the split / Sherwood Park pairing: **142** (of which 50 explicitly name Strathcona or Sherwood Park; the rest object to the split generally, which in the interim map meant the Sherwood Park pairing (inference)).
- R2 Strathcona-Sherwood Park-side objections to adding Beaumont (not Beaumont people): **79**.
- Other Beaumont mentions (not a position on the pairing, or only a passing mention / general submissions): 15 (2-0092, 0506, 0571, 0572, 0669, 0769, 0826, 0913, 0957, 0978, 0989, 1015, 1025, 1080, 1084; note 0826 and 0913 do object to the Beaumont split but as Edmonton-area planner/other writers, so 2 further objectors outside both groups).
- R2 submissions from Beaumont side that explicitly want Beaumont kept with Leduc / in Leduc-Beaumont: see quotes; e.g. 2-0167 "Please leave the entire city in the Leduc-Beaumont electoral area", 2-0348 "Stay in Leduc-beaumont", 2-0404 (Leduc and Beaumont "grouped in the same electoral boundary").
- Supporters of splitting Beaumont: **0** found in R2 (no Beaumont-voice text endorsing the split).
- R1 (before interim): 1-0144 (Leduc County resident: Leduc, Beaumont, Leduc County "remain in the same electoral district"), 1-0091 ("Put us back into Leduc-Beaumont please"; Beaumont not to go into an Edmonton riding), 1-0016 ("making our area part of Leduc Beaumont or ..."). BORDERLINE/contrary: 1-0086 and 1-0087 (a Leduc writer) asked to SPLIT Leduc-Beaumont into separate Leduc and Beaumont ridings. 1-0138 only a population table.
- Leduc County hearing/written: 2-0175 ("boundaries need to stay within Leduc county"); 2-0519 (Looma/Leduc County communities), 2-0843 (not about this).
- City of Leduc residents asking for Leduc-Beaumont: **none identifiable** in text (inference: text carries no municipality field; 0 mention themselves as City of Leduc residents asking for it).
- Mayors: the City of Beaumont mayor (hearing R2, Edmonton/Jan 20 2026, hansard_r2 ~line 40034): "I am here today on behalf of Beaumont residents and Beaumont city council to respectfully ask that the commission reconsider the interim proposal to divide our city and instead keep Beaumont whole". She said she is in "the Leduc-Beaumont riding currently ... And want to stay there. Absolutely." the Leduc County mayor (hansard_r2 ~line 28156): priority "that the city of Leduc and the city of Beaumont reside together entirely inside ... the current Leduc-Beaumont riding." A former Beaumont mayor, written 2-1070. City of Leduc mayor: not found in any hearing participant list or written text.
- Commission reaction recorded: a Commissioner to the Leduc County mayor: "that Beaumont thing: we got a lot of push-back. It's a hot spot." (hansard_r2).
- Unreadable/scanned: none among Beaumont items other than image-only attachments noted in 2-0178 (a .jpg attachment, not read).

### Beaumont-voice IDs (n=142)
2-0166, 2-0167, 2-0168, 2-0169, 2-0170, 2-0172, 2-0173, 2-0174, 2-0176, 2-0177, 2-0178, 2-0180, 2-0181, 2-0182, 2-0183, 2-0184, 2-0185, 2-0186, 2-0187, 2-0188, 2-0189, 2-0190, 2-0191, 2-0192, 2-0193, 2-0194, 2-0195, 2-0196, 2-0197, 2-0198, 2-0199, 2-0201, 2-0202, 2-0203, 2-0204, 2-0205, 2-0206, 2-0207, 2-0213, 2-0214, 2-0215, 2-0216, 2-0229, 2-0234, 2-0244, 2-0258, 2-0259, 2-0260, 2-0263, 2-0264, 2-0265, 2-0269, 2-0271, 2-0272, 2-0275, 2-0276, 2-0277, 2-0279, 2-0280, 2-0282, 2-0285, 2-0288, 2-0290, 2-0291, 2-0294, 2-0295, 2-0296, 2-0297, 2-0298, 2-0299, 2-0300, 2-0302, 2-0303, 2-0305, 2-0306, 2-0308, 2-0310, 2-0311, 2-0312, 2-0313, 2-0314, 2-0315, 2-0316, 2-0318, 2-0319, 2-0320, 2-0321, 2-0322, 2-0323, 2-0324, 2-0325, 2-0326, 2-0329, 2-0330, 2-0331, 2-0333, 2-0335, 2-0337, 2-0339, 2-0341, 2-0342, 2-0345, 2-0346, 2-0347, 2-0348, 2-0350, 2-0352, 2-0354, 2-0356, 2-0363, 2-0366, 2-0380, 2-0391, 2-0404, 2-0432, 2-0435, 2-0439, 2-0443, 2-0448, 2-0451, 2-0459, 2-0461, 2-0462, 2-0465, 2-0468, 2-0471, 2-0478, 2-0479, 2-0487, 2-0489, 2-0501, 2-0502, 2-0520, 2-0601, 2-0603, 2-0661, 2-0738, 2-0838, 2-0958, 2-0976, 2-1070, 2-1078

### Strathcona-side IDs (n=79)
2-0385, 2-0411, 2-0413, 2-0416, 2-0425, 2-0426, 2-0428, 2-0447, 2-0476, 2-0510, 2-0513, 2-0515, 2-0517, 2-0522, 2-0523, 2-0527, 2-0534, 2-0544, 2-0547, 2-0556, 2-0561, 2-0562, 2-0566, 2-0567, 2-0568, 2-0587, 2-0590, 2-0595, 2-0608, 2-0646, 2-0756, 2-0780, 2-0802, 2-0805, 2-0809, 2-0815, 2-0820, 2-0821, 2-0824, 2-0846, 2-0865, 2-0867, 2-0868, 2-0871, 2-0876, 2-0884, 2-0905, 2-0928, 2-0930, 2-0941, 2-0943, 2-0945, 2-0948, 2-0949, 2-0962, 2-0969, 2-0977, 2-0988, 2-1008, 2-1013, 2-1032, 2-1034, 2-1040, 2-1043, 2-1054, 2-1055, 2-1056, 2-1058, 2-1059, 2-1062, 2-1064, 2-1069, 2-1071, 2-1072, 2-1073, 2-1075, 2-1106, 2-1109, 2-1136

### Quotes
- 2-0167: "Breaking up the City of Beaumont across two electoral areas is the wrong thing to do ... Please leave the entire city in the Leduc-Beaumont electoral area."
- 2-0198: "If it's true that Beaumont will be divided ... with half in Leduc and half in Strathcona county ... I vehemently oppose this idea."
- 2-0277: "We have more in common with Leduc than Strathcona."
### Why
Large, one-sided Beaumont opposition to the Sherwood Park pairing and mayoral requests exist; but the Leduc City half of "Residents of Leduc and Beaumont, as well as their mayors" is not evidenced (Beaumont mayor + Leduc County mayor are). The only R1 Leduc-city-identified submitter asked for a split.

## N2 (minority para 117 and 127) Lethbridge: "over 5:1" / "approximately 75 to 14" to preserve city boundaries
**Verdict: DOES NOT HOLD as a count I can reproduce (lean "partly holds" on direction only). Direction (preserve > hybrid) is right; the margin is not.** Written-submission count: 70 preserve vs 38 hybrid (1.8:1); R2 only 64 vs 33 (1.9:1); self-stated Lethbridge residents 13 vs 8 (1.6:1). Hearing transcripts NOT tallied (see limits).

IDs use shorthand `1-NNNN`/`2-NNNN` = EBC-2025-1-NNNN / EBC-2025-2-NNNN.

### Method
- Rounds: R1 (pre-interim) and R2 (post-interim) written submissions. 150 files contain "lethbridge" (case-insens.), listed in C:/tmp/ceb_w/leth_ids.txt.
- Auto-screen regexes (scripts C:/tmp/ceb_w/leth.py) for preserve phrases (not split|divid, leave/keep Lethbridge, fully/wholly urban, two urban, oppose hybrid, municipal boundary, status quo ...) and hybrid phrases (quad, four-quadrant, regional approach, Lethbridge-Cardston/Livingstone/Little Bow/Taber, portions of Lethbridge, support hybrid ...). Then manual reading of every file to set final labels (labels in C:/tmp/ceb_w/leth_lab.json). Residency regex in leth2.py ("resident of Lethbridge", "live in Lethbridge", Lethbridge West/East resident ...).
- PRESERVE = asks to keep Lethbridge as urban-only divisions / not split into rural-urban hybrids / keep current East-West city boundaries. HYBRID = asks for rural-urban Lethbridge divisions (four-quadrant, regional hybrids, Lethbridge-X). NEUTRAL/NOT ADDRESSED = mentions Lethbridge without a position on hybrid vs urban (e.g. Medicine Hat or Calgary submissions using Lethbridge as comparison; 2-0143, 0144, 0157, 0694, 0714, 0728, 0803, 1020, 1039, 1098, 0929, 0993, 1036, plus boundary-line-only comments 2-0417, 1130, 1138).
- Boundary-line-only note: some R2 Lethbridge-West residents objected to moving their neighbourhood to Lethbridge-East (2-0159, 2-0417); 2-0159 also says it is "good that our overall urban community remains as two urban ridings" so counted PRESERVE; 2-0417 neutral.

### Counts (written submissions, R1+R2)
- PRESERVE: 70 (R1 6, R2 64)
- HYBRID: 38 (R1 5, R2 33)
- Neutral/not addressed: remaining of the 150 (about 42 files).
- Residents (text-stated "I live in Lethbridge / Lethbridge-West" etc., regex; undercount since no municipality field): PRESERVE 13, HYBRID 8. Many HYBRID writers state they are from Coaldale, Taber, Lethbridge County or "southern Alberta" (2-0677, 0678, 0680, 0682, 0683, 0781, 0788, 0794, 0797, 0808 are near-identical "resident of southern Alberta" template letters; 2-0537, 2-0535, 2-0452, 2-1117 are Coaldale-linked). Counting templates once instead of each would lower HYBRID further; PRESERVE also has template clusters (2-0018/0027/0037; 2-0643/0635/0804).
- Borderline items: 2-0014 (counted HYBRID, text argues for "rural influence"), 2-0729 (HYBRID, "regional approach"), 2-0870 (HYBRID, "such as hybrid urban-rural ridings"), 2-0525 (HYBRID weak: "bridge the gap"), 2-0434 and 2-0472 (PRESERVE, general urban-stay-urban), 2-0485 (PRESERVE by inference, Calgary writer saying urban-rural ridings fit outside the largest cities incl. Lethbridge), 1-0121 and 1-0135 (PRESERVE, Lethbridge residents stressing city distinctness without naming hybrids; inference), 1-0125/1-0113 (general urban-stay-urban, Lethbridge named as example).
- Unreadable: no Lethbridge item among the 27 near-empty text files that I could confirm; attachments (e.g. 2-0178-type images) not read. 1-0009 near-empty (14 chars).
- NOT TALLIED: hearing transcripts (hansard_r1 516 and hansard_r2 365 lines mention Lethbridge; R1 Lethbridge hearing at hansard_r1 line ~903). If the minority counted oral presenters too, my written-only count would differ.

### PRESERVE IDs (n=70)
1-0119, 1-0121, 1-0125, 1-0126, 1-0113, 1-0135, 2-0018, 2-0027, 2-0037, 2-0110, 2-0123, 2-0159, 2-0250, 2-0292, 2-0359, 2-0368, 2-0373, 2-0393, 2-0400, 2-0427, 2-0434, 2-0441, 2-0457, 2-0472, 2-0485, 2-0579, 2-0600, 2-0635, 2-0643, 2-0665, 2-0668, 2-0689, 2-0701, 2-0702, 2-0716, 2-0723, 2-0725, 2-0733, 2-0735, 2-0739, 2-0742, 2-0743, 2-0744, 2-0752, 2-0753, 2-0758, 2-0762, 2-0767, 2-0770, 2-0775, 2-0777, 2-0795, 2-0798, 2-0804, 2-0849, 2-0856, 2-0892, 2-0914, 2-1007, 2-1027, 2-1087, 2-1088, 2-1089, 2-1095, 2-1119, 2-1120, 2-1125, 2-1133, 2-1140, 2-0236

### HYBRID IDs (n=38)
1-0101, 1-0140, 1-0142, 1-0146, 1-0182, 2-0014, 2-0422, 2-0438, 2-0440, 2-0463, 2-0529, 2-0537, 2-0552, 2-0658, 2-0676, 2-0677, 2-0678, 2-0680, 2-0682, 2-0683, 2-0696, 2-0729, 2-0774, 2-0781, 2-0788, 2-0794, 2-0797, 2-0808, 2-0870, 2-0888, 2-0891, 2-0937, 2-0982, 2-0991, 2-1014, 2-1019, 2-1063, 2-0525

### Quotes
- 2-0643: "the decision to maintain Lethbridge's electoral divisions without dividing them into rural-urban (hybrid) constituencies."
- 2-0400: "Lethbridge West should remain urban only, as should Lethbridge East."
- 2-0537: "I write to urge the Commission to adopt the four-quadrant hybrid model for Lethbridge and its surrounding rural municipalities."
### Why
Preserve outnumbers hybrid in the archive, but by roughly 2:1 on any cut I tried, nowhere near 5:1 or 75:14; the minority's basis (which rounds, hearings, residents only, deduplication) is not stated so cannot be reconstructed from public sources.

## N3 (minority para 104) "Rebecca Brown was the only resident of Bearspaw who wrote about this issue" [Bearspaw joining a Calgary division]
**Verdict: HOLDS within the readable archive (one self-identified Bearspaw resident). Cannot rule out unreadable R1 items.**

### Method
- Rounds: R1 + R2 text, plus hansard_r1/r2. Regex `bearspaw` (case-insens.): 8 files total: 1-0139, 2-0619, 2-0786, 2-0911, 2-0950, 2-0990, 2-0995, 2-1097. Residency regex over all files: `(i live in (the )?(rocky ?view|bearspaw|watermark|church ranches|glenbow|elbow valley)|resident of (rocky ?view|bearspaw|elbow valley)|live in rocky ?view|...)` and neighbourhood terms (watermark, church ranches, rockland park, glenbow, lynx ridge); Calgary-North West terms. Hearing transcripts grepped for `bearspaw` (R1: 19 lines; R2: ~20 lines) and speaker residence read.
- Counted "resident of Bearspaw" only where the text says "I live in Bearspaw" or equivalent.
### Counts / IDs
- Self-identified Bearspaw residents addressing Bearspaw in/out of Calgary: **1** = EBC-2025-2-0911 (Rebecca Brown: "I live in Bearspaw, a rural area just outside Calgary ... rural areas should remain connected to rural communities rather than ..." and keeping Bearspaw "aligned with other rural areas").
- Others mentioning Bearspaw, none self-identify as living there: 2-0990 (MLA for Calgary-North West; advocates ADDING Bearspaw and Watermark to Calgary-North West); 2-0995 and 2-1097 (Calgary-North West residents; favour the Bearspaw/Watermark/Church Ranches link to Calgary-NW, 2-1097 "such as myself" is a Calgary-NW resident); 2-0786 (Tuscany resident, mentions Bearspaw amenities); 2-0950 (Tuscany resident, Bearspaw school/market); 2-0619 (Bearspaw First Nation mention, unrelated); 1-0139 (Airdrie organisation; would support a Cochrane division "that could include the Bearspaw area").
- Hearing R2 (Calgary, Jan 12 2026, hansard_r2 ~6725-7100): a Calgary-North West hearing witness testified Bearspaw should stay in Cochrane-Springbank; she states "I live in Calgary-North West", so not a Bearspaw resident. Calgary hearing R1 (Jun 2025): Cochrane presenters speak about Bearspaw but live/work in Cochrane. 
- Related: R1 1-0041 is also a "Rebecca Brown" submission (municipality: Rocky View County; general rural-v-urban seat-count message, does NOT mention Bearspaw or joining Calgary). Page 1 is image-only; I read it from the PDF image. Whether same person as 2-0911 is not stated (inference: likely but unverified).
- UNREADABLE (text extraction yielded only headers or empty; page 1 of the printed email is an image): R1: 1-0010, 0012, 0014, 0019, 0025, 0026, 0028, 0031, 0036, 0038, 0041 (read manually as above), 0042 (read manually: not relevant), 0044, 0045, 0047, 0050, 0053, 0054, 0059, 0074, 0083, 0088, 0105, 0122, 0123, 0124, 0131, 0153, 0177, 0185, 0187. R2: 2-0983 (header only), 2-0001 and 2-0119 (partial). These 33-34 items could contain Bearspaw residents; unknown. Any R1/R2 item whose message is in an image-only page is invisible to all counts in this file (limit applies to every claim).
### Quote
- 2-0911: "I believe that rural and urban boundaries should remain distinct and that rural areas should remain connected to rural communities rather than ..." and "Keeping rural areas like Bearspaw aligned with other rural areas ensures effective representation".
### Why
Only one readable submission comes from a self-described Bearspaw resident; the rest are from adjoining Calgary neighbourhoods, an MLA, or Airdrie.

## N4 (minority para 106) "Dividing Springbank was never proposed to the ABEBC"
**Verdict: HOLDS for the readable archive: no written submission or oral remark proposes dividing Springbank between divisions. Caveat on wording: ~12 submissions asked to move all of Springbank into a Calgary division (Calgary-Bow); one hedges "some polls" west of Calgary.**

### Method
- Regex `springbank` over R1+R2 text: 25 files (2 R1, 23 R2). Split regexes over those files: `split|divid|part of springbank|portion of springbank|(east|west|north|south)(ern)? of springbank|springbank (east|west)|(part|portion|half|piece|some|polls?) (of|in) (the )?springbank|split(ting)? (of )?(springbank|rocky view)` -> zero hits that propose dividing Springbank (all hits were unrelated "divide/divider"). Hearings: `springbank` 37 lines R1, 48 lines R2, read in context.
- "Proposed dividing Springbank" = text asks that Springbank be split among two or more divisions.
### Counts / IDs
- Propose dividing Springbank: **0**.
- Propose moving ALL of Springbank into Calgary-Bow/west Calgary (not a division of it): 2-0020 (Calgary-Bow-Springbank), 2-0030, 2-0038 (as fallback add), 2-0051, 2-0586, 2-0588, 2-0731, 2-0747, 2-0749, 2-0759, 2-0800, 2-0920, 2-0990 (MLA), 2-1057; oral: R2 Calgary hearing (a presenter, ~hansard_r2 5378-5413) confirms an MLA proposal to "add Springbank and remove Wildwood" in Calgary-Bow was made after the interim report.
- Borderline: 2-0866 ("extension of the current Calgary-West boundaries to include some polls west of the Calgary proper boundaries, perhaps including Springbank, Elbow Valley, and the Tsuut'ina first nation") - suggests partial inclusion of an area including Springbank, but does not propose splitting the community; counted not-a-division (inference). 2-0383 supports removing Springbank and Elbow Valley from Banff-Kananaskis (whole). 2-1033 about Elbow Valley. 2-0687 cautions against hybrids combining Calgary with Springbank. 2-0429 and 2-1057: Springbank residents opposing Cochrane-Springbank placement.
- Commission-side remark (not a submission): R2 Calgary hearing, a Commissioner: "In the case of Calgary-North West we have a chance to look at Springbank, taking parts of it" (hansard_r2 ~6945; a presenter corrected "I think you mean Bearspaw") - i.e. a Commission question, and about Bearspaw.
- R1 hearings: Springbank mentioned as part of Banff-Kananaskis; "To protect Calgary-Elbow, you have to flood pieces of Springbank" (hansard_r1 ~23764, a speaker discussing a different Calgary-Elbow configuration) - not a proposal to split Springbank.
- Cannot check from public sources: maps in PDF attachments (not text-extractable) might show a boundary through Springbank. IMAGE/ATTACHMENT-ONLY items are unreadable (see N3 list).
### Quotes
- 2-0749: "The community of Springbank shares its primary social and economic identity with Calgary Bow and should be integrated into that constituency" (whole community).
- 2-0759: "Placing Springbank in Cochrane-Springbank severs these bonds".
### Why
No submission asked for a split of Springbank; the proposals were to move the whole community. Where the IAP claim is read as "no one asked for it to be split" it holds; whether a final map divides Springbank is a separate fact I cannot check here.


## N5 (minority para 138) "Not a single submission, to our knowledge, asked for Diamond Valley to be paired with Banff"
**Verdict: HOLDS as worded (zero submissions pair Diamond Valley with Banff). One written submission and one hearing presentation put Diamond Valley in a Canmore-Crowsnest Pass district (Canmore is Banff's neighbour), which is not "Banff" strictly.**

### Method
- Regex `diamond valley|black diamond|turner valley|\bDV\b` over R1+R2 = 29 files (1 R1: 1-0138 data table; 28 R2). Co-occurrence with `banff|canmore|kananaskis|bow valley|mountain (riding|division|corridor)|rocky mountain` within 250 characters; then every non-co-occurring DV file read around its DV mention. Hearings: same regex, windows of +/-8 lines for Banff/Canmore/Kananaskis/Bow Valley.
- "Asked for DV paired with Banff" = text requests a division containing both Diamond Valley and Banff.
### Counts / IDs
- DV with Banff: **0**.
- DV with Canmore (Banff-adjacent) in a south-Rockies corridor district: **2** = written EBC-2025-2-0619 ("Alpine Alberta": "South of Canmore, the foothills communities of Bragg Creek, Diamond Valley, Longview, and Pincher Creek ..."; it proposes separate Canmore-Crowsnest Pass and Rocky Mountain House-Banff districts, so it separates Banff from DV) and the matching hearing presentation (hansard_r2 ~line 10836: "a Canmore-Crowsnest Pass district ... from Canmore to Bragg Creek to Diamond Valley to Crowsnest"; a later R2 remark ~10988: "an MLA that's representing Crowsnest, Canmore, Bragg Creek, Diamond Valley"). BORDERLINE: counted not-Banff.
- DV with Okotoks / Highwood (the opposite): 18 = 2-0012, 2-0021, 2-0024, 2-0045, 2-0050, 2-0052, 2-0053, 2-0062, 2-0233, 2-0269, 2-0560, 2-0741, 2-0761, 2-0784, 2-0789, 2-0807, 2-0836, 2-0839.
- Mention DV with no position on pairing: 2-0236 (Foothills/Okotoks municipal joint letter, objects to DV relocated to High River-Vulcan), 2-0545, 2-0621 (school boards; Okotoks-DV; Banff-Jasper concerns), 2-0365, 2-0410, 2-0908, 2-0994, 1-0138 (data table), 2-1025 (long table).
- Hearing R2: Okotoks/Foothills/DV mayors and reeve jointly proposed an alternate map keeping DV with Okotoks (hansard_r2 ~299-352); a Commissioner (hansard_r2 ~46408): "The ones we heard from preferred if Okotoks would stay in Diamond Valley".
- Unreadable: none directly implicated; the unreadable list in N3 applies to everything.
### Quotes
- 2-0050: "I strongly prefer Okotoks-Diamond Valley, and strongly reject Calgary-Okotoks."
- 2-0789: "Removing Diamond Valley and replacing it with a south Calgary population would destroy the rural make up of our riding."
### Why
Nobody in the archive asks for Diamond Valley with Banff. The only close case is a Canmore-Crowsnest Pass idea; the minority's wording (Banff) survives, but "no one asked for DV in a mountain riding" would not.

## N6 (minority Exec. Summary p.115) "Most of our colleagues' proposed boundaries were also clearly opposed by the vast majority of submissions that the ABEBC received"
**Verdict: DOES NOT HOLD as a blanket statement. By area: Diamond Valley arrangement HOLDS (against clearly dominant); Lethbridge hybrids PARTLY (more against than for, about 65% of positioned submissions, not "vast"); Springbank/Bearspaw into Calgary DOES NOT HOLD (more for than against among those who addressed it); NE Calgary CANNOT BE CHECKED (the majority's four-division plan postdates the archive; interim tallies given).**

### Method
- Majority proposals as described in the IAP majority and minority text (notes in C:/Users/email/AppData/Local/Temp/ceb/notes): (1) Lethbridge: one Lethbridge-only division plus three Lethbridge hybrids (Little Bow, Taber-Warner, Cardston); (2) Springbank/Bearspaw into west-Calgary divisions (Calgary-North West-Bearspaw, Calgary-Bow-Springbank, Calgary-West-Springbank); (3) Banff-Canmore-Diamond Valley (adds Longview/Diamond Valley/Millarville/Priddis/Bragg Creek); (4) NE Calgary four-division plan (Klein, Cross, East, Confluence) discussed as a paper.
- Counts are submissions that address the area. FOR = supports the majority-type outcome, AGAINST = opposes it, NEUTRAL = mentions without a position. Archive total = 1,252 submissions (170 R1 + 1,082 R2); most do not address any of these areas, so "vast majority of submissions" cannot be literally true of any single area (inference).
- The archive predates the IAP; "opposed" here means opposed to the equivalent configuration or the underlying principle (rural/hybrid combination) in the ABEBC round.
- Repo labels: grepped wt-osf for "5.9.4" (hits in analysis/review, findings/sentiment_analysis_completion_report.md, reports/academic/report_academic.md section 5.9.4.x) and sentiment files. Existing LLM-scored labels (data/outputs/submission_sentiment_llm_full_results.csv, 1,110 rows, 620 unique submissions; data/outputs/sentiment_intensity_scores.csv, 452 rows) cover seven OTHER minority configurations (Airdrie 4-way, Nolan Hill-Cochrane, Chestermere, Olds-Three Hills, Red Deer hybrids, St. Albert-Sturgeon, Rocky Mountain House-Banff Park hybrid). None covers Lethbridge, Springbank/Bearspaw, NE Calgary or Diamond Valley, and the repo's own completion report says the full-corpus scan was incomplete. NOT reused; all counts here are my own regex-plus-manual reading.

### 1. Lethbridge hybrids
- AGAINST hybrids (preserve urban-only): 70; FOR hybrids: 38; NEUTRAL/not addressed: about 42 of 150 Lethbridge-mentioning files. Share against among those with a position: 65%. IDs: see the N2 section (same lists).
- The majority plan is partly hybrid, partly urban (one Lethbridge-only seat), so neither camp matches it exactly (inference); some "preserve" writers (e.g. 2-0159) wanted two urban seats, which the majority plan does not give.

### 2. Springbank/Bearspaw into Calgary
- FOR (explicitly wants Springbank and/or Bearspaw in a Calgary division): 19 = 2-0020, 2-0030, 2-0038, 2-0051, 2-0429, 2-0586, 2-0588, 2-0731, 2-0747, 2-0749, 2-0759, 2-0800, 2-0920, 2-0990, 2-0995, 2-1057, 2-1097, 2-0786, 2-0950. Many Springbank/Calgary-Bow letters are near-identical and some come from one MLA's campaign; counting each once would lower this. Borderline: 2-0038 conditional; 2-0866 ("some polls ... perhaps including Springbank") not counted.
- AGAINST (explicitly objects to Springbank/Bearspaw/Rocky View going in with Calgary): 3 = 2-0911, 2-0687, 2-0960. Broader objections to rural areas in Calgary ridings (about the interim's Elbow Valley and Conrich hybrids, so only an inference for Springbank/Bearspaw): 2-0569, 2-1026, 2-1033, 2-1038, 2-1053.
- Hearing (Calgary, Jan 12 2026): a hearing witness (a Calgary-North West resident) against Bearspaw in Calgary-NW; a presenter against Springbank into Calgary-Bow; speakers in favour at hansard_r2 ~13857-13920.
- NEUTRAL: 2-0545, 2-0619, 2-0617 (Springbank hockey community, no position), 2-0383 (supports removing Springbank from Banff-Kananaskis).
- Read: among those who addressed it, FOR outnumbers AGAINST about 19 to 3.

### 3. Banff-Canmore-Diamond Valley
- FOR (DV with Banff/Canmore): 0 strict (DV+Banff); 2 for DV+Canmore (2-0619 and its hearing presentation).
- AGAINST (DV should stay with Okotoks/Highwood, or objects to DV moving): 18 (IDs in N5) + 2-0236 and 2-0621 (joint municipal and school-board positions) = 20. 2-0761, 2-0784, 2-0789 and 2-0807 explicitly object to "removing Diamond Valley".
- NEUTRAL: 2-0545, 2-0365, 2-0410, 2-0908, 2-0994, 1-0138, 2-1025.
- Holds for DV: AGAINST dominates (about 20 against, 0-2 for).

### 4. NE Calgary
- The majority's own Exec Summary says "no improvements to recommend" for NE Calgary and attaches a Durnie/Solberg four-division discussion paper; no submission in the archive can refer to that plan. Verdict for this area: cannot be checked from public sources.
- Interim-round tallies for the NE/E Calgary divisions (Calgary-Cross/Klein/East/Confluence, Conrich, Whitehorn); 47 files mention them; informal reading: supportive of the interim configuration 16 (2-0020, 2-0232, 2-0292, 2-1094, 2-0433, 2-0533, 2-0919, 2-1076, 2-0666, 2-0698, 2-0748, 2-0764, 2-0993, 2-0823, 2-0907, 2-0931); opposed 7 (2-0396, 2-0786, 2-0830, 2-0740, 2-1123, 2-0745, 2-0691); the rest neutral or off-topic (about 24). Borderline: 2-0842 (Whitehorn resident, position unclear, neutral), 2-0933 (keep Rundle, Pineridge together, neutral).
### Quotes
- 2-0749 (FOR Springbank into Calgary-Bow): "The community of Springbank shares its primary social and economic identity with Calgary Bow and should be integrated into that constituency".
- 2-0911 (AGAINST): "rural areas should remain connected to rural communities rather than being absorbed into urban ones".
- 2-0643 (Lethbridge AGAINST hybrids): "maintain Lethbridge's electoral divisions without dividing them into rural-urban (hybrid) constituencies."
### Why
Only the Diamond Valley element (and, by a modest majority of positioned submissions, Lethbridge) runs against the majority's changes; Springbank/Bearspaw drew more support than opposition in the archive, and the NE Calgary plan postdates the archive.

## SUMMARY
- M2: holds for Beaumont (142 Beaumont-voice objections to the split/Sherwood Park pairing, Beaumont mayor and Leduc County mayor asked for Leduc-Beaumont); no City of Leduc resident or mayor found asking for it -> partly holds overall.
- N2: does not hold (as a count): 70 preserve vs 38 hybrid (1.8:1), not 5:1 / 75:14.
- N3: holds (1 self-identified Bearspaw resident: 2-0911), subject to ~34 unreadable items.
- N4: holds (0 propose dividing Springbank; many propose moving the whole community to Calgary).
- N5: holds as worded (0 pair DV with Banff; 2 pair DV with Canmore in a corridor district).
- N6: does not hold as a blanket claim (holds for DV, partly Lethbridge, not Springbank/Bearspaw; NE Calgary cannot be checked).
