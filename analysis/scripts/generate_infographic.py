"""One-page PNG infographic of the 2026 Alberta Electoral Boundaries audit results."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

# ── palette ──────────────────────────────────────────────────────────────────
NAVY    = '#1B2A4A'
RED     = '#C0392B'
GREEN   = '#1E8449'
AMBER   = '#CA6F1E'
BLUE    = '#1A5276'
MBLUE   = '#2980B9'
LBLUE   = '#D6EAF8'
LRED    = '#FADBD8'
LGREEN  = '#D5F5E3'
LAMBER  = '#FDEBD0'
GRAY    = '#7F8C8D'
DARK    = '#2C3E50'
BG      = '#F4F6F7'
WHITE   = '#FFFFFF'
LGRAY   = '#ECF0F1'
PURPLE  = '#6C3483'
LPURP   = '#E8DAEF'


def clear_ax(ax, bg=WHITE, edge=NAVY, lw=1.5):
    ax.set_facecolor(bg)
    for sp in ax.spines.values():
        sp.set_edgecolor(edge)
        sp.set_linewidth(lw)
    ax.set_xticks([])
    ax.set_yticks([])


def t(ax, x, y, s, fs=10, c=DARK, ha='center', va='center',
      bold=False, italic=False):
    ax.text(x, y, s, fontsize=fs, color=c, ha=ha, va=va,
            fontweight='bold' if bold else 'normal',
            fontstyle='italic' if italic else 'normal',
            transform=ax.transAxes)


def fpatch(ax, x, y, w, h, fc, ec, lw=1.2, radius=0.02):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f'round,pad={radius}',
                       facecolor=fc, edgecolor=ec, linewidth=lw,
                       transform=ax.transAxes, clip_on=False)
    ax.add_patch(p)


fig = plt.figure(figsize=(20, 27), dpi=150, facecolor=BG)

# ── HEADER ───────────────────────────────────────────────────────────────────
ah = fig.add_axes([0.02, 0.962, 0.96, 0.034])
clear_ax(ah, bg=NAVY, edge=NAVY)
t(ah, 0.5, 0.68, 'COMPUTATIONAL FORENSIC AUDIT: 2026 ALBERTA ELECTORAL BOUNDARIES',
  fs=17, c=WHITE, bold=True)
t(ah, 0.5, 0.18,
  'Will Conner · Mount Royal University · 2026-05-07 · MGGG ReCom Ensemble · CC0 1.0 Universal',
  fs=9, c='#BDC3C7')

# ── BIG RESULT ───────────────────────────────────────────────────────────────
ar = fig.add_axes([0.02, 0.887, 0.96, 0.068])
clear_ax(ar, bg=RED, edge=RED)
t(ar, 0.5, 0.78, 'MINORITY MAP — FISHER COMBINED NEUTRAL-NULL PROBABILITY',
  fs=12, c='#FADBD8', bold=True)
t(ar, 0.5, 0.44, 'p = 1.55 × 10⁻⁸   ·   once in 64 million neutral random draws',
  fs=21, c=WHITE, bold=True)
t(ar, 0.5, 0.11, 'Fisher T = 42.148  ·  χ²(df=4)  ·  Channels 1 + 2 combined',
  fs=9.5, c='#F1948A', italic=True)

# ── CHANNEL CARDS ────────────────────────────────────────────────────────────
# Channel 1
c1 = fig.add_axes([0.02, 0.72, 0.30, 0.158])
clear_ax(c1, bg=LRED, edge=RED, lw=2)
t(c1, 0.5, 0.94, 'CHANNEL 1', fs=11, c=RED, bold=True)
t(c1, 0.5, 0.83, 'Partisan Joint Tail (Mahalanobis)', fs=9.5, c=DARK, italic=True)
c1.axhline(0.775, xmin=0.03, xmax=0.97, color='#F1948A', lw=0.8)
t(c1, 0.04, 0.74, 'Map', fs=7.5, c=GRAY, ha='left')
t(c1, 0.60, 0.74, 'Mahal.', fs=7.5, c=GRAY, ha='center')
t(c1, 0.97, 0.74, 'Verdict', fs=7.5, c=GRAY, ha='right')

rows_c1 = [
    ('Minority 2026', '6.11', '1.60×10⁻⁷', RED,   '✗ OUTLIER'),
    ('Majority 2026', '2.69', '0.125',       GREEN, '✓ within null'),
    ('2019 Enacted',  '3.56', '0.013',       AMBER, '~ moderate'),
]
yy = 0.64
for nm, mh, pv, col, verd in rows_c1:
    t(c1, 0.04, yy, nm,   fs=8.5, c=DARK,  ha='left')
    t(c1, 0.60, yy, mh,   fs=8.5, c=col,   ha='center', bold=True)
    t(c1, 0.97, yy, verd, fs=8,   c=col,   ha='right',  bold=True)
    yy -= 0.145

t(c1, 0.5, 0.19, 'Ensemble centre: moderately UCP-favourable', fs=8, c=GRAY, italic=True)
t(c1, 0.5, 0.09, '(mean EG = +0.016 — natural geographic sorting)', fs=7.5, c=GRAY, italic=True)

# Channel 2
c2 = fig.add_axes([0.355, 0.72, 0.30, 0.158])
clear_ax(c2, bg=LRED, edge=RED, lw=2)
t(c2, 0.5, 0.94, 'CHANNEL 2', fs=11, c=RED, bold=True)
t(c2, 0.5, 0.83, 'Swing-Zone Allocation Test (SZAT)', fs=9.5, c=DARK, italic=True)
c2.axhline(0.775, xmin=0.03, xmax=0.97, color='#F1948A', lw=0.8)

stats_c2 = [
    ('SZAT score (EG difference)',    '+0.03917',   MBLUE),
    ('Null 97.5th percentile',        '+0.03693',   MBLUE),
    ('Bootstrap N / seed',            '10k / 23687475', GRAY),
    ('Bootstrap p-value',             '0.0044',     RED),
    ('Swing-zone VAs',                '2,108 of 4,765', DARK),
]
yy = 0.70
for lbl, val, col in stats_c2:
    t(c2, 0.04, yy, lbl, fs=8, c=DARK, ha='left')
    t(c2, 0.97, yy, val, fs=8, c=col,  ha='right',
      bold=(col == RED))
    yy -= 0.115

c2.axhline(0.155, xmin=0.03, xmax=0.97, color='#F1948A', lw=0.8)
t(c2, 0.5, 0.09, 'H₀ rejected at α = 0.05', fs=10, c=RED, bold=True)

# Channel 3
c3 = fig.add_axes([0.69, 0.72, 0.30, 0.158])
clear_ax(c3, bg=LGREEN, edge=GREEN, lw=2)
t(c3, 0.5, 0.94, 'CHANNEL 3', fs=11, c=GREEN, bold=True)
t(c3, 0.5, 0.83, 'Neighbour-Drain Label-Shuffle Null', fs=9.5, c=DARK, italic=True)
c3.axhline(0.775, xmin=0.03, xmax=0.97, color='#A9DFBF', lw=0.8)
t(c3, 0.04, 0.74, 'Map',     fs=7.5, c=GRAY, ha='left')
t(c3, 0.51, 0.74, 'drain',   fs=7.5, c=GRAY, ha='center')
t(c3, 0.73, 0.74, 'z',       fs=7.5, c=GRAY, ha='center')
t(c3, 0.97, 0.74, 'p',       fs=7.5, c=GRAY, ha='right')

rows_c3 = [
    ('Minority 2026', '0.00618', '−1.37', '0.134', GREEN,
     '  within null — does not contribute to Fisher'),
    ('Majority 2026', '0.00018', '−2.92', '<.0001', AMBER,
     '  anomalously clean (inverted finding)'),
]
yy = 0.63
for nm, dr, z, pv, col, note in rows_c3:
    t(c3, 0.04, yy,      nm, fs=8,   c=DARK, ha='left')
    t(c3, 0.51, yy,      dr, fs=8,   c=col,  ha='center')
    t(c3, 0.73, yy,       z, fs=8,   c=col,  ha='center')
    t(c3, 0.97, yy,      pv, fs=8,   c=col,  ha='right')
    t(c3, 0.04, yy-0.09, note, fs=7.5, c=col, ha='left', italic=True)
    yy -= 0.23

# ── PARTISAN METRICS TABLE ────────────────────────────────────────────────────
am = fig.add_axes([0.02, 0.555, 0.455, 0.155])
clear_ax(am, bg=WHITE, edge=NAVY, lw=1.5)
t(am, 0.5, 0.95, 'MINORITY MAP: PARTISAN METRICS vs NEUTRAL ENSEMBLE', fs=11, c=NAVY, bold=True)
t(am, 0.5, 0.875,
  '50,000-plan ensemble  ·  2 chains × 25k steps  ·  base_seed = 1432864451',
  fs=8, c=GRAY, italic=True)
am.axhline(0.835, xmin=0.02, xmax=0.98, color=NAVY,    lw=1.2)
am.axhline(0.800, xmin=0.02, xmax=0.98, color='#BDC3C7', lw=0.7)

COL = [0.03, 0.38, 0.57, 0.74, 0.89]
for x, h in zip(COL, ['Metric', 'Observed', 'Ens. Mean', 'Pctile', 'Marg. p']):
    t(am, x, 0.818, h, fs=8, c=NAVY, ha='left', bold=True)

mdata = [
    ('Efficiency Gap',  '+0.0402', '+0.0160', 'p95.9',   '0.0413'),
    ('Mean-Median',     '+0.0104', '−0.0197', 'p99.992', '0.0001'),
    ('Declination',     '−0.0770', '−0.0021', 'p0.4',    '0.0042'),
    ('Seats @ 50/50',   '+0.5169', '+0.4523', 'p100.0',  '<0.0001'),
    ('Population MAD',  '3,938',   '—',       'p98.9',   '—'),
]
yy = 0.748
for i, (met, obs, emn, pct, mp) in enumerate(mdata):
    if i % 2 == 0:
        am.axhspan(yy - 0.078, yy + 0.022, xmin=0.01, xmax=0.99,
                   facecolor=LGRAY, alpha=0.55)
    t(am, COL[0], yy-0.028, met, fs=8.5, c=DARK,   ha='left')
    t(am, COL[1], yy-0.028, obs, fs=8.5, c=RED,    ha='left', bold=True)
    t(am, COL[2], yy-0.028, emn, fs=8.5, c=GRAY,   ha='left')
    t(am, COL[3], yy-0.028, pct, fs=8.5, c=RED,    ha='left', bold=True)
    mp_col = RED if mp not in ('—', '0.125', '0.013') else GRAY
    t(am, COL[4], yy-0.028, mp, fs=8.5, c=mp_col, ha='left')
    yy -= 0.130

# ── JUSTIFICATION TESTS ───────────────────────────────────────────────────────
aj = fig.add_axes([0.50, 0.555, 0.49, 0.155])
clear_ax(aj, bg=WHITE, edge=RED, lw=1.5)
t(aj, 0.5, 0.95, 'POPULATION JUSTIFICATION TESTS — ALL 5 UNFORCED', fs=11, c=RED, bold=True)
t(aj, 0.5, 0.875,
  'Can contested minority configurations be forced by population math or area law?',
  fs=8, c=GRAY, italic=True)
aj.axhline(0.835, xmin=0.02, xmax=0.98, color='#F1948A', lw=0.8)

jtests = [
    ('T1', 'Olds-Three Hills-Didsbury',
     'Rural sum 43,691 within band without Airdrie slice'),
    ('T2', 'Rocky Mtn House–Banff Park',
     '2019 predecessor 24,468 km² — park extension not load-bearing'),
    ('T3', 'Airdrie 4-way split',
     '2-way split arithmetically sufficient'),
    ('T4', 'Red Deer 4 districts',
     '2 districts are the minimum — achieved by majority'),
    ('T5', 'Chestermere into Calgary-Peigan',
     'Ches+Strathmore+Wheatland = 45,240 (viable standalone)'),
]
yy = 0.785
for t_id, name, note in jtests:
    t(aj, 0.02, yy,       f'✗ {t_id}', fs=9,   c=RED,  ha='left', bold=True)
    t(aj, 0.13, yy,       name,         fs=8.5, c=DARK, ha='left')
    t(aj, 0.13, yy-0.065, note,         fs=7.5, c=GRAY, ha='left', italic=True)
    yy -= 0.148

# ── ADDITIONAL CHANNELS ───────────────────────────────────────────────────────
aa = fig.add_axes([0.02, 0.395, 0.96, 0.148])
clear_ax(aa, bg=WHITE, edge=NAVY, lw=1.5)
t(aa, 0.5, 0.96, 'ADDITIONAL CHANNELS — CANONICAL RERUN 2026-05-07', fs=11, c=NAVY, bold=True)
aa.axhline(0.90, xmin=0.02, xmax=0.98, color='#BDC3C7', lw=0.8)

# Population MAD panel
fpatch(aa, 0.02, 0.06, 0.29, 0.80, LRED,   RED)
t(aa, 0.165, 0.82, 'Population MAD', fs=10, c=RED, bold=True)
t(aa, 0.165, 0.68, 'Minority MAD = 3,938 persons', fs=9, c=DARK)
t(aa, 0.165, 0.56, 'Majority MAD = 2,827 persons', fs=9, c=DARK)
t(aa, 0.165, 0.43, 'Minority p98.9  ·  Majority p16.7', fs=9.5, c=RED, bold=True)
t(aa, 0.165, 0.28, 'Consistent with deliberate over/underloading', fs=8, c=GRAY, italic=True)
t(aa, 0.165, 0.17, 'of partisan constituencies', fs=8, c=GRAY, italic=True)

# Reock proxy panel
fpatch(aa, 0.355, 0.06, 0.29, 0.80, LGREEN, GREEN)
t(aa, 0.500, 0.82, 'Reock Proxy (Compactness)', fs=10, c=GREEN, bold=True)
t(aa, 0.500, 0.68, 'Minority p0.1  ·  Majority p0.9', fs=9, c=DARK)
t(aa, 0.500, 0.53, 'Both maps MORE compact than ensemble', fs=9.5, c=GREEN, bold=True)
t(aa, 0.500, 0.37, 'NULL FINDING', fs=10, c=GREEN, bold=True)
t(aa, 0.500, 0.26, 'Expected for commission maps constrained', fs=8, c=GRAY, italic=True)
t(aa, 0.500, 0.16, 'by community-of-interest and municipal lines', fs=8, c=GRAY, italic=True)

# Municipal anchoring panel
fpatch(aa, 0.69, 0.06, 0.29, 0.80, LAMBER, AMBER)
t(aa, 0.835, 0.82, 'Municipal Anchoring', fs=10, c=AMBER, bold=True)
t(aa, 0.835, 0.68, 'Minority 4.9× below comparator norm', fs=9, c=DARK)
t(aa, 0.835, 0.55, 'Direction: supports gerrymander', fs=9.5, c=AMBER, bold=True)
t(aa, 0.835, 0.37, 'Not computable to p-value:', fs=8.5, c=GRAY, italic=True)
t(aa, 0.835, 0.27, 'Canadian comparator distribution', fs=8.5, c=GRAY, italic=True)
t(aa, 0.835, 0.17, 'too thin for statistical null', fs=8.5, c=GRAY, italic=True)

# ── DPG + MAJORITY SUMMARY ────────────────────────────────────────────────────
ad = fig.add_axes([0.02, 0.287, 0.455, 0.098])
clear_ax(ad, bg=LBLUE, edge=BLUE, lw=1.5)
t(ad, 0.5, 0.88, 'DPG v11 GEOMETRY VALIDATION', fs=10, c=BLUE, bold=True)
t(ad, 0.5, 0.70, 'T1–T5 thresholds pre-registered before canonical shapefile receipt', fs=8.5, c=DARK)
t(ad, 0.5, 0.55, 'Symmetric-difference match: 99.9994%  ·  4,765 VAs  ·  pop 4,262,572', fs=9, c=GREEN, bold=True)
t(ad, 0.5, 0.35, 'AsPredicted #289,449  ·  OSF: osf.io/w2s8k', fs=8.5, c=BLUE)
t(ad, 0.5, 0.18, 'COMPLETE', fs=9, c=GREEN, bold=True)

am2 = fig.add_axes([0.50, 0.287, 0.49, 0.098])
clear_ax(am2, bg=LGREEN, edge=GREEN, lw=1.5)
t(am2, 0.5, 0.88, 'MAJORITY MAP — ALL CHANNELS WITHIN NEUTRAL NULL', fs=10, c=GREEN, bold=True)
maj_lines = [
    ('✓', 'Ch1 Mahalanobis p = 0.125 — within null on all four partisan metrics'),
    ('✓', 'Ch3 drain_score anomalously clean (z = −2.92, p < 0.0001, inverted finding)'),
    ('✓', 'Population MAD at p16.7  ·  Reock proxy null (same as minority — expected)'),
    ('~', '2019 enacted: moderate UCP lean (Mahal p = 0.013) — consistent with geography'),
]
yy = 0.74
for icon, line in maj_lines:
    col = GREEN if icon == '✓' else AMBER
    t(am2, 0.02, yy, f'{icon}  {line}', fs=8, c=col, ha='left')
    yy -= 0.18

# ── PRE-REGISTRATION CHAIN ────────────────────────────────────────────────────
ap = fig.add_axes([0.02, 0.172, 0.96, 0.105])
clear_ax(ap, bg=LPURP, edge=PURPLE, lw=1.5)
t(ap, 0.5, 0.94,
  'PRE-REGISTRATION CHAIN — ALL FOUR SUBMITTED 2026-05-06/07  ·  CC0 1.0 Universal',
  fs=10, c=PURPLE, bold=True)
ap.axhline(0.86, xmin=0.02, xmax=0.98, color='#C39BD3', lw=0.8)

pregs = [
    ('#289,449', 'osf.io/w2s8k',
     'DPG v11 geometry validation', 'COMPLETE', GREEN),
    ('#289,451', 'osf.io/r3zm7',
     'Neighbour-Drain label-shuffle null', 'COMPLETE — minority within null', GREEN),
    ('#289,455', 'osf.io/qsgy8',
     'Lunty 91-seat forensic scorecard', 'PRE-REGISTERED — pending Nov 2026', AMBER),
    ('#289,469', 'osf.io/6pt83',
     'SZAT bootstrap null', 'COMPLETE — H₀ rejected p = 0.0044', GREEN),
]
xs = [0.01, 0.26, 0.51, 0.76]
for i, (num, osf, title, status, col) in enumerate(pregs):
    cx = xs[i] + 0.115
    t(ap, cx, 0.75, num,    fs=9,   c=PURPLE, bold=True)
    t(ap, cx, 0.60, osf,    fs=8.5, c=MBLUE)
    t(ap, cx, 0.44, title,  fs=8,   c=DARK)
    t(ap, cx, 0.24, status, fs=8,   c=col,    bold=True)
    if i < 3:
        ap.axvline(xs[i] + 0.245, ymin=0.10, ymax=0.90, color='#C39BD3', lw=0.8)

# ── VERDICT FOOTER ────────────────────────────────────────────────────────────
av = fig.add_axes([0.02, 0.025, 0.96, 0.138])
clear_ax(av, bg=NAVY, edge=NAVY, lw=0)
t(av, 0.5, 0.88, 'AUDIT VERDICT', fs=13, c='#AED6F1', bold=True)
t(av, 0.5, 0.70,
  "The minority map's four-dimensional partisan feature vector sits at Mahalanobis distance 6.11 from",
  fs=10, c=WHITE)
t(av, 0.5, 0.57,
  'the neutral-draw ensemble centre. Combined with SZAT, the joint neutral-null probability is 1 in 64 million.',
  fs=10, c=WHITE)
t(av, 0.5, 0.40,
  'The majority map is within the neutral null on all executed channels.',
  fs=11, c='#A9DFBF', bold=True)
t(av, 0.5, 0.22,
  'Phase 2 pre-registered — within 72 hours of the November 2026 Lunty committee map tabling,',
  fs=9, c='#AED6F1', italic=True)
t(av, 0.5, 0.10,
  'the 91-seat forensic scorecard (AsPredicted #289,455 / osf.io/qsgy8) will be executed against it.',
  fs=9, c='#AED6F1', italic=True)

# ── SAVE ─────────────────────────────────────────────────────────────────────
out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                   'infographic.png')
fig.savefig(out, dpi=150, bbox_inches='tight', facecolor=BG, edgecolor='none')
print(f'Saved: {out}')
