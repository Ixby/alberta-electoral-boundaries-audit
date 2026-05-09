"""Infographic v2 — 1920 × 1080, laptop-optimised, 4-colour semantic palette."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# ── Palette: 4 semantic roles ─────────────────────────────────────────────
NAVY  = '#1B2A4A'   # chrome: header, footer, borders, section titles
RED   = '#B03A2E'   # alarm:  outlier / rejected null
GREEN = '#1A7A3C'   # clear:  within null / pass
WHITE = '#FFFFFF'   # neutral: card backgrounds
LGRAY = '#E9EAEC'   # page background + alternating table rows

# Derived tints (background fills only — same semantic meaning as parent)
LRED  = '#FAEAE9'
LGRN  = '#E9F5EC'

# Text
DARK  = '#1C2833'   # primary body text
GRAY  = '#6B7280'   # secondary / annotations
NAVY2 = '#5D6D7E'   # footnote text (softer navy)

GAP = 0.007  # inter-panel gap in figure coords




def run():
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=LGRAY)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)


    # ── helpers ───────────────────────────────────────────────────────────────────
    def P(l, b, w, h, bg=WHITE, ec=NAVY, lw=1.0):
        a = fig.add_axes([l, b, w, h])
        a.set_facecolor(bg)
        for s in a.spines.values():
            s.set_edgecolor(ec)
            s.set_linewidth(lw)
        a.set_xticks([]); a.set_yticks([])
        return a


    def T(a, x, y, s, fs=10, c=DARK, ha='center', va='center',
          bold=False, italic=False):
        a.text(x, y, s, fontsize=fs, color=c, ha=ha, va=va,
               fontweight='bold' if bold else 'normal',
               fontstyle='italic' if italic else 'normal',
               transform=a.transAxes)


    def HL(a, y, x0=0.03, x1=0.97, c='#C8CACC', lw=0.8):
        a.axhline(y, xmin=x0, xmax=x1, color=c, linewidth=lw)


    # ── HEADER ───────────────────────────────────────────────────────────────────
    h = P(0, 0.900, 1, 0.100, bg=NAVY, ec=NAVY)
    T(h, 0.5, 0.68,
      'COMPUTATIONAL FORENSIC AUDIT  ·  2026 ALBERTA ELECTORAL BOUNDARIES',
      fs=20, c=WHITE, bold=True)
    T(h, 0.5, 0.22,
      'Will Conner  ·  Mount Royal University  ·  2026-05-07  ·  MGGG ReCom  ·  50,000-plan neutral ensemble  ·  CC0 1.0',
      fs=9.5, c='#A0AAB4')

    # ── HERO STAT ────────────────────────────────────────────────────────────────
    r = P(0, 0.800, 1, 0.100, bg=RED, ec=RED)
    T(r, 0.5, 0.83,
      'MINORITY MAP  ·  FISHER COMBINED NEUTRAL-NULL PROBABILITY',
      fs=11, c='#FCEAE9', bold=True)
    T(r, 0.5, 0.45, 'p  =  1.55 × 10⁻⁸',
      fs=38, c=WHITE, bold=True)
    T(r, 0.5, 0.09,
      'once in 64 million neutral random draws   ·   Fisher T = 42.148   ·   Channels 1 + 2 combined',
      fs=12, c='#FCEAE9')

    # ── CHANNEL CARDS (3 columns) ────────────────────────────────────────────────
    _CW = (0.98 - 2 * GAP) / 3  # channel card width — right edge = 0.01 + 3*CW + 2*GAP = 0.990
    _CB = 0.520  # channel bottom
    _CH = 0.262  # channel height


    def chan(col, bg, ec):
        return P(0.01 + col * (_CW + GAP), _CB, _CW, _CH, bg=bg, ec=ec, lw=1.5)


    # — Channel 1: Mahalanobis —
    c1 = chan(0, LRED, RED)
    T(c1, 0.5, 0.945, 'CHANNEL 1', fs=13, c=RED, bold=True)
    T(c1, 0.5, 0.858, 'Partisan Joint Tail  ·  Mahalanobis distance',
      fs=9.5, c=DARK, italic=True)
    HL(c1, 0.808, c='#E0B0AC')

    T(c1, 0.03, 0.760, 'Map',      fs=8.5, c=GRAY, ha='left',   bold=True)
    T(c1, 0.53, 0.760, 'Mahal.',   fs=8.5, c=GRAY, ha='center', bold=True)
    T(c1, 0.73, 0.760, 'Joint p',  fs=8.5, c=GRAY, ha='center', bold=True)
    T(c1, 0.97, 0.760, 'Result',   fs=8.5, c=GRAY, ha='right',  bold=True)
    HL(c1, 0.718, c='#E0E0E0')

    rows_c1 = [
        ('Minority 2026', '6.11', '1.60 × 10⁻⁷', RED,   'OUTLIER'),
        ('Majority 2026', '2.69', '0.125',                        GREEN, 'within null'),
        ('2019 Enacted',  '3.56', '0.013',                        GRAY,  'moderate'),
    ]
    yy = 0.634
    for nm, mh, pv, col, verd in rows_c1:
        T(c1, 0.03, yy, nm,   fs=10,  c=DARK, ha='left')
        T(c1, 0.53, yy, mh,   fs=10,  c=col,  ha='center', bold=(col != GRAY))
        T(c1, 0.73, yy, pv,   fs=9,   c=col,  ha='center')
        T(c1, 0.97, yy, verd, fs=9.5, c=col,  ha='right',  bold=(col != GRAY))
        yy -= 0.178

    HL(c1, 0.245, c='#E0B0AC', lw=0.6)
    T(c1, 0.5, 0.165, 'Ensemble centre: mean EG = +0.016 (natural geographic sorting)',
      fs=8.5, c=GRAY, italic=True)
    T(c1, 0.5, 0.068, '#289,449  ·  osf.io/w2s8k  ·  COMPLETE', fs=8, c=NAVY2, italic=True)

    # — Channel 2: SZAT —
    c2 = chan(1, LRED, RED)
    T(c2, 0.5, 0.945, 'CHANNEL 2', fs=13, c=RED, bold=True)
    T(c2, 0.5, 0.858, 'Swing-Zone Allocation Test  ·  SZAT bootstrap',
      fs=9.5, c=DARK, italic=True)
    HL(c2, 0.808, c='#E0B0AC')

    rows_c2 = [
        ('SZAT score (EG difference)',   '+0.03917'),
        ('Null 97.5th percentile',       '+0.03693'),
        ('Bootstrap N / seed',           '10,000 / 23,687,475'),
        ('Swing-zone VAs',               '2,108 of 4,765'),
    ]
    yy = 0.720
    for lbl, val in rows_c2:
        T(c2, 0.04, yy, lbl, fs=10, c=DARK, ha='left')
        T(c2, 0.97, yy, val, fs=10, c=DARK, ha='right')
        yy -= 0.120

    HL(c2, 0.295, c='#E0B0AC', lw=1.0)
    T(c2, 0.5, 0.205, 'Bootstrap p = 0.0044   ·   H₀ rejected at α = 0.05',
      fs=13, c=RED, bold=True)
    T(c2, 0.5, 0.068, '#289,469  ·  osf.io/6pt83  ·  COMPLETE', fs=8, c=NAVY2, italic=True)

    # — Channel 3: Drain (null) —
    c3 = chan(2, LGRN, GREEN)
    T(c3, 0.5, 0.945, 'CHANNEL 3', fs=13, c=GREEN, bold=True)
    T(c3, 0.5, 0.858, 'Neighbour-Drain Label-Shuffle Null',
      fs=9.5, c=DARK, italic=True)
    HL(c3, 0.808, c='#9ACBA8')

    T(c3, 0.03, 0.760, 'Map',          fs=8.5, c=GRAY, ha='left',   bold=True)
    T(c3, 0.44, 0.760, 'drain_score',  fs=8.5, c=GRAY, ha='center', bold=True)
    T(c3, 0.68, 0.760, 'z',            fs=8.5, c=GRAY, ha='center', bold=True)
    T(c3, 0.82, 0.760, 'p',            fs=8.5, c=GRAY, ha='center', bold=True)
    T(c3, 0.97, 0.760, 'Result',       fs=8.5, c=GRAY, ha='right',  bold=True)
    HL(c3, 0.718, c='#E0E0E0')

    rows_c3 = [
        ('Minority 2026', '0.00618', '−1.37', '0.134',    GREEN,  'within null'),
        ('Majority 2026', '0.00018', '−2.92', '< 0.0001', GRAY, 'anom. clean'),
    ]
    yy = 0.625
    for nm, dr, z, pv, col, verd in rows_c3:
        T(c3, 0.03, yy, nm,   fs=10,  c=DARK, ha='left')
        T(c3, 0.44, yy, dr,   fs=10,  c=col,  ha='center')
        T(c3, 0.68, yy, z,    fs=10,  c=col,  ha='center')
        T(c3, 0.82, yy, pv,   fs=10,  c=col,  ha='center')
        T(c3, 0.97, yy, verd, fs=9.5, c=col,  ha='right', bold=True)
        yy -= 0.22

    HL(c3, 0.268, c='#9ACBA8', lw=0.6)
    T(c3, 0.5, 0.185, 'Does not contribute to Fisher (minority within null)',
      fs=9.5, c=GRAY, italic=True)
    T(c3, 0.5, 0.068, '#289,451  ·  osf.io/r3zm7  ·  COMPLETE', fs=8, c=NAVY2, italic=True)

    # ── "HOW TO READ" STRIP ───────────────────────────────────────────────────────
    strip = P(0.01, 0.787, 0.98, 0.010, bg='#DDE2E8', ec='#DDE2E8', lw=0)
    T(strip, 0.5, 0.50,
      'Each channel is an independent statistical test against the same 50,000-plan neutral ensemble — '
      'a map drawn by unbiased random redistricting.  Significance on multiple independent channels is the audit’s evidentiary standard.',
      fs=8.5, c='#3D4F5C', italic=True)

    # ── DATA ROW (metrics table + justification tests) ────────────────────────────
    _DB = 0.287  # data row bottom
    _DH = 0.226  # data row height

    # — Partisan metrics table —
    am = P(0.01, _DB, 0.454, _DH, bg=WHITE, ec=NAVY, lw=1.2)
    T(am, 0.5, 0.960, 'MINORITY MAP: PARTISAN METRICS vs NEUTRAL ENSEMBLE',
      fs=12, c=NAVY, bold=True)
    T(am, 0.5, 0.896,
      '50,000 plans  ·  2 chains × 25,000 steps  ·  base_seed = 1432864451',
      fs=8.5, c=GRAY, italic=True)

    HL(am, 0.858, c=NAVY, lw=1.0)
    COLS = [0.03, 0.38, 0.58, 0.76, 0.91]
    for x, hd in zip(COLS, ['Metric', 'Observed', 'Ens. Mean', 'Pctile', 'Marg. p']):
        T(am, x, 0.826, hd, fs=9.5, c=NAVY, ha='left', bold=True)
    HL(am, 0.798, c='#D0D3D6')

    mdata = [
        ('Efficiency Gap',  '+0.0402', '+0.0160', 'p95.9',    '0.0413'),
        ('Mean-Median',     '+0.0104', '−0.0197', 'p99.992', '0.0001'),
        ('Declination',     '−0.0770', '−0.0021', 'p0.4', '0.0042'),
        ('Seats @ 50/50', '+0.5169', '+0.4523', 'p100.0', '<0.0001'),
        ('Population MAD', '3,938', '—', 'p98.9', '—'),
    ]
    yy = 0.748
    for i, (met, obs, emn, pct, mp) in enumerate(mdata):
        if i % 2 == 0:
            am.axhspan(yy - 0.112, yy + 0.020, xmin=0.01, xmax=0.99,
                       facecolor=LGRAY, alpha=0.8)
        T(am, COLS[0], yy - 0.042, met, fs=10, c=DARK,  ha='left')
        T(am, COLS[1], yy - 0.042, obs, fs=10, c=RED,   ha='left', bold=True)
        T(am, COLS[2], yy - 0.042, emn, fs=10, c=GRAY,  ha='left')
        T(am, COLS[3], yy - 0.042, pct, fs=10, c=RED,   ha='left', bold=True)
        pc = RED if mp not in ('—',) else GRAY
        T(am, COLS[4], yy - 0.042, mp,  fs=10, c=pc,    ha='left')
        yy -= 0.152

    T(am, 0.5, 0.042,
      'Declination at p0.4 = 0.4th percentile in the UCP-favour tail (more extreme than 99.6% of plans)',
      fs=8.5, c=GRAY, italic=True)

    # — Justification tests —
    aj = P(0.471, _DB, 0.519, _DH, bg=WHITE, ec=RED, lw=1.2)
    T(aj, 0.5, 0.960, 'POPULATION JUSTIFICATION TESTS  —  ALL 5 UNFORCED',
      fs=12, c=RED, bold=True)
    T(aj, 0.5, 0.896,
      'Can the contested configurations be forced by population math or area law (s. 15(2))?',
      fs=8.5, c=GRAY, italic=True)
    HL(aj, 0.858, c='#E0B0AC', lw=1.0)

    jtests = [
        ('T1', 'Olds-Three Hills-Didsbury',
         'Rural sum of 43,691 within band without Airdrie slice'),
        ('T2', 'Rocky Mtn House–Banff Park',
         '2019 predecessor 24,468 km² — park extension not load-bearing'),
        ('T3', 'Airdrie 4-way split',
         'Arithmetic supports 2-way split; majority achieves this'),
        ('T4', 'Red Deer 4 districts',
         '2 districts are the minimum — achieved by majority'),
        ('T5', 'Chestermere → Calgary-Peigan',
         'Ches. + Strathmore + Wheatland = 45,240 (viable standalone)'),
    ]
    yy = 0.825
    for t_id, name, note in jtests:
        T(aj, 0.02, yy,         f'✗ FAIL', fs=9.5, c=RED,  ha='left', bold=True)
        T(aj, 0.165, yy,        name,                 fs=10,  c=DARK, ha='left', bold=True)
        T(aj, 0.165, yy - 0.065, note,                fs=8.5, c=GRAY, ha='left', italic=True)
        yy -= 0.162

    # ── ADDITIONAL CHANNELS ROW ───────────────────────────────────────────────────
    _ACB = 0.112  # additional channels bottom
    _ACH = 0.163  # additional channels height


    def addchan(col, bg, ec):
        return P(0.01 + col * (_CW + GAP), _ACB, _CW, _ACH, bg=bg, ec=ec, lw=1.2)


    ap1 = addchan(0, LRED,  RED)
    T(ap1, 0.5, 0.882, 'Population MAD  ·  Channel 4', fs=11, c=RED, bold=True)
    T(ap1, 0.5, 0.678, 'Minority 3,938 persons   ·   Majority 2,827 persons', fs=9.5, c=DARK)
    T(ap1, 0.5, 0.478, 'Minority p98.9   ·   Majority p16.7', fs=12, c=RED, bold=True)
    T(ap1, 0.5, 0.265, 'Consistent with deliberate constituency over- and under-loading',
      fs=9, c=GRAY, italic=True)
    T(ap1, 0.5, 0.100, 'Direction: supports gerrymander', fs=9.5, c=RED)

    ap2 = addchan(1, LGRN, GREEN)
    T(ap2, 0.5, 0.882, 'Reock Proxy  ·  Compactness', fs=11, c=GREEN, bold=True)
    T(ap2, 0.5, 0.678, 'Minority p0.1   ·   Majority p0.9', fs=9.5, c=DARK)
    T(ap2, 0.5, 0.478, 'Both maps more compact than ensemble', fs=12, c=GREEN, bold=True)
    T(ap2, 0.5, 0.280, 'NULL FINDING — expected for commission maps', fs=9, c=GRAY, italic=True)
    T(ap2, 0.5, 0.100, 'constrained by COI + municipal boundaries', fs=9, c=GRAY, italic=True)

    ap3 = addchan(2, LGRN, GREEN)
    T(ap3, 0.5, 0.882, 'Majority Map  ·  All Channels Within Null', fs=11, c=GREEN, bold=True)
    T(ap3, 0.5, 0.678,
      '✓  Ch1 Mahalanobis p = 0.125   ·   ✓  Pop MAD at p16.7',
      fs=9.5, c=GREEN)
    T(ap3, 0.5, 0.490,
      '✓  Reock null (expected — same COI constraint applies)',
      fs=9.5, c=GREEN)
    T(ap3, 0.5, 0.290,
      '≈  2019 enacted: Mahal p = 0.013  (consistent with geography)',
      fs=9, c=GRAY, italic=True)
    T(ap3, 0.5, 0.100,
      'Ch3: majority drain score anomalously clean (z = −2.92, inverted)',
      fs=8.5, c=GRAY, italic=True)

    # ── FINDINGS ─────────────────────────────────────────────────────────────────
    av = P(0, 0.028, 1, 0.080, bg=NAVY, ec=NAVY, lw=0)
    T(av, 0.5, 0.770,
      "The minority map’s four-dimensional partisan feature vector sits at "
      "Mahalanobis distance 6.11 from the neutral-draw ensemble centre. "
      "Combined with SZAT, the joint neutral-null probability is 1 in 64 million. "
      "All five population justification tests fail.",
      fs=11, c=WHITE)
    T(av, 0.5, 0.280,
      "The majority map is within the neutral null on all channels.  "
      "Phase 2 pre-registered — pending receipt of the November 2026 Lunty committee 91-seat map.",
      fs=10, c='#A0AAB4')

    # ── FOOTER ────────────────────────────────────────────────────────────────────
    af = P(0, 0, 1, 0.026, bg='#D0D4D8', ec='#D0D4D8', lw=0)
    T(af, 0.5, 0.50,
      'Pre-registered:  #289,449 osf.io/w2s8k  ·  #289,451 osf.io/r3zm7  ·  '
      '#289,455 osf.io/qsgy8  ·  #289,469 osf.io/6pt83'
      '   │   gerrychain 0.3.2 · ReCom · ±25% pop · '
      '4,765 VAs · EPSG:3400',
      fs=8, c='#3D4F5C')

    # ── SAVE ─────────────────────────────────────────────────────────────────────
    out = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'infographic_v2.png')
    fig.savefig(out, dpi=120, facecolor=LGRAY, edgecolor='none')
    print(f'Saved: {out}')


if __name__ == "__main__":
    run()
