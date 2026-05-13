"""Infographic v3 — 1920×1080, redesigned for readability; canonical values throughout.

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# ── Palette ───────────────────────────────────────────────────────────────────
NAVY  = '#1B2A4A'
RED   = '#B03A2E'
AMBER = '#B07A2E'   # below-threshold / marginal findings
GREEN = '#1A7A3C'
WHITE = '#FFFFFF'
LGRAY = '#ECEEF1'   # page background

LRED  = '#FBF0EF'
LAMB  = '#FDF6EE'
LGRN  = '#EFF7F1'

DARK  = '#1C2833'
GRAY  = '#5A6A78'
NAVY2 = '#5D6D7E'

GAP = 0.010


def run():
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=LGRAY)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    def P(l, b, w, h, bg=WHITE, ec=NAVY, lw=1.0):
        a = fig.add_axes([l, b, w, h])
        a.set_facecolor(bg)
        for s in a.spines.values():
            s.set_edgecolor(ec)
            s.set_linewidth(lw)
        a.set_xticks([]); a.set_yticks([])
        return a

    def T(a, x, y, s, fs=11, c=DARK, ha='center', va='center',
          bold=False, italic=False):
        a.text(x, y, s, fontsize=fs, color=c, ha=ha, va=va,
               fontweight='bold' if bold else 'normal',
               fontstyle='italic' if italic else 'normal',
               transform=a.transAxes)

    def HL(a, y, x0=0.03, x1=0.97, c='#C8CACC', lw=0.7):
        a.axhline(y, xmin=x0, xmax=x1, color=c, linewidth=lw)

    # ── HEADER ────────────────────────────────────────────────────────────────
    h = P(0, 0.922, 1, 0.078, bg=NAVY, ec=NAVY)
    T(h, 0.5, 0.68,
      'COMPUTATIONAL FORENSIC AUDIT  ·  2026 ALBERTA ELECTORAL BOUNDARIES',
      fs=21, c=WHITE, bold=True)
    T(h, 0.5, 0.18,
      'Will Conner  ·  Mount Royal University  ·  2026-05-11  '
      '·  MGGG ReCom  ·  250,000-plan neutral ensemble  ·  CC0 1.0',
      fs=10, c='#A0AAB4')

    # ── HERO STAT ─────────────────────────────────────────────────────────────
    r = P(0, 0.822, 1, 0.100, bg=RED, ec=RED)
    T(r, 0.5, 0.840,
      'MINORITY MAP  ·  FISHER COMBINED NEUTRAL-NULL PROBABILITY',
      fs=12, c='#FCEAE9', bold=True)
    T(r, 0.5, 0.460, 'p  =  8.71 × 10⁻⁹',
      fs=40, c=WHITE, bold=True)
    T(r, 0.5, 0.095,
      'once in 115 million neutral random draws   ·   '
      'Fisher T = 43.36   ·   Channels 1 + 2 combined  (Ch3 within null)',
      fs=11, c='#FCEAE9')

    # ── CHANNEL CARDS (3 cols) ─────────────────────────────────────────────
    _CW = (0.980 - 2 * GAP) / 3
    _CB = 0.495
    _CH = 0.315

    def chan(col, bg, ec):
        return P(0.010 + col * (_CW + GAP), _CB, _CW, _CH, bg=bg, ec=ec, lw=1.5)

    # — Channel 1: Mahalanobis —
    c1 = chan(0, LRED, RED)
    T(c1, 0.5, 0.950, 'CHANNEL 1', fs=14, c=RED, bold=True)
    T(c1, 0.5, 0.882, 'Partisan Joint Tail  ·  Mahalanobis distance',
      fs=10.5, c=DARK, italic=True)
    HL(c1, 0.840, c='#E0B0AC', lw=1.0)

    for x, hd in zip([0.04, 0.54, 0.75, 0.97],
                     ['Map', 'Mahal. D', 'Joint p', 'Result']):
        ha = 'left' if x == 0.04 else ('right' if x == 0.97 else 'center')
        T(c1, x, 0.798, hd, fs=10, c=GRAY, ha=ha, bold=True)
    HL(c1, 0.762, c='#D0D0D0', lw=0.5)

    rows_c1 = [
        ('Minority 2026', '6.11', '1.60 × 10⁻⁷', RED,   'OUTLIER'),
        ('Majority 2026', '2.69', '0.125',          GREEN, 'within null'),
        ('2019 Enacted',  '3.56', '0.013',          GRAY,  'moderate'),
    ]
    yy = 0.692
    for nm, mh, pv, col, verd in rows_c1:
        T(c1, 0.04, yy, nm,   fs=11.5, c=DARK,  ha='left')
        T(c1, 0.54, yy, mh,   fs=11.5, c=col,   ha='center', bold=(col != GRAY))
        T(c1, 0.75, yy, pv,   fs=10,   c=col,   ha='center')
        T(c1, 0.97, yy, verd, fs=10.5, c=col,   ha='right',  bold=(col != GRAY))
        yy -= 0.178

    HL(c1, 0.255, c='#E0B0AC', lw=0.5)
    T(c1, 0.5, 0.178, 'Ensemble centre: mean EG +0.016 (natural geographic sorting)',
      fs=9.5, c=GRAY, italic=True)
    T(c1, 0.5, 0.078, '#289,449  ·  osf.io/w2s8k  ·  PRE-REGISTERED',
      fs=9, c=NAVY2, italic=True)

    # — Channel 2: SZAT —
    c2 = chan(1, LRED, RED)
    T(c2, 0.5, 0.950, 'CHANNEL 2', fs=14, c=RED, bold=True)
    T(c2, 0.5, 0.882, 'Swing-Zone Allocation Test  ·  bootstrap',
      fs=10.5, c=DARK, italic=True)
    HL(c2, 0.840, c='#E0B0AC', lw=1.0)

    rows_c2 = [
        ('SZAT score (EG difference)',  '+0.03917'),
        ('Null 97.5th percentile',      '+0.03693'),
        ('Bootstrap N / seed',          '10,000 / 23,687,475'),
        ('Swing-zone VAs',              '2,108 of 4,765'),
    ]
    yy = 0.768
    for lbl, val in rows_c2:
        T(c2, 0.04, yy, lbl, fs=11, c=DARK, ha='left')
        T(c2, 0.97, yy, val, fs=11, c=DARK, ha='right')
        yy -= 0.118

    HL(c2, 0.316, c='#E0B0AC', lw=1.0)
    T(c2, 0.5, 0.222, 'Bootstrap p = 0.0024   ·   H₀ rejected at α = 0.05',
      fs=13.5, c=RED, bold=True)
    T(c2, 0.5, 0.078, '#289,469  ·  osf.io/6pt83  ·  PRE-REGISTERED',
      fs=9, c=NAVY2, italic=True)

    # — Channel 3: Drain (null) —
    c3 = chan(2, LGRN, GREEN)
    T(c3, 0.5, 0.950, 'CHANNEL 3', fs=14, c=GREEN, bold=True)
    T(c3, 0.5, 0.882, 'Neighbour-Drain Label-Shuffle Null',
      fs=10.5, c=DARK, italic=True)
    HL(c3, 0.840, c='#9ACBA8', lw=1.0)

    for x, hd in zip([0.04, 0.42, 0.62, 0.78, 0.97],
                     ['Map', 'drain score', 'z', 'p', 'Result']):
        ha = 'left' if x == 0.04 else ('right' if x == 0.97 else 'center')
        T(c3, x, 0.798, hd, fs=10, c=GRAY, ha=ha, bold=True)
    HL(c3, 0.762, c='#D0D0D0', lw=0.5)

    rows_c3 = [
        ('Minority 2026', '0.00618', '−1.37', '0.134',    GREEN, 'within null'),
        ('Majority 2026', '0.00018', '−2.92', '< 0.0001', GRAY,  'anom. clean'),
    ]
    yy = 0.680
    for nm, dr, z, pv, col, verd in rows_c3:
        T(c3, 0.04, yy, nm,   fs=11.5, c=DARK, ha='left')
        T(c3, 0.42, yy, dr,   fs=11,   c=col,  ha='center')
        T(c3, 0.62, yy, z,    fs=11,   c=col,  ha='center')
        T(c3, 0.78, yy, pv,   fs=11,   c=col,  ha='center')
        T(c3, 0.97, yy, verd, fs=10.5, c=col,  ha='right', bold=True)
        yy -= 0.200

    HL(c3, 0.272, c='#9ACBA8', lw=0.5)
    T(c3, 0.5, 0.192, 'Ch3 minority within null — does not contribute to Fisher',
      fs=10, c=GRAY, italic=True)
    T(c3, 0.5, 0.078, '#289,451  ·  osf.io/r3zm7  ·  PRE-REGISTERED',
      fs=9, c=NAVY2, italic=True)

    # ── HOW-TO-READ STRIP ─────────────────────────────────────────────────────
    strip = P(0.010, 0.480, 0.980, 0.013, bg='#DDE2E8', ec='#DDE2E8', lw=0)
    T(strip, 0.5, 0.50,
      'Each channel is an independent test against the same 250,000-plan neutral ensemble.  '
      'Significance on multiple independent channels is the audit\'s evidentiary standard.',
      fs=9.5, c='#3D4F5C', italic=True)

    # ── DATA ROW ──────────────────────────────────────────────────────────────
    _DB = 0.195
    _DH = 0.283

    # Left panel — Partisan metrics (canonical values)
    am = P(0.010, _DB, 0.455, _DH, bg=WHITE, ec=NAVY, lw=1.2)
    T(am, 0.5, 0.964, 'MINORITY MAP  ·  PARTISAN METRICS vs NEUTRAL ENSEMBLE',
      fs=12.5, c=NAVY, bold=True)
    T(am, 0.5, 0.906,
      '250,000 plans  ·  2-chain ReCom  ·  base_seed = 1432864451',
      fs=9.5, c=GRAY, italic=True)
    HL(am, 0.875, c=NAVY, lw=0.8)

    COLS = [0.03, 0.36, 0.55, 0.73, 0.91]
    for x, hd in zip(COLS, ['Metric', 'Observed', 'Ens. Mean', 'Pctile', 'Marg. p']):
        T(am, x, 0.842, hd, fs=10.5, c=NAVY, ha='left', bold=True)
    HL(am, 0.812, c='#D0D3D6', lw=0.5)

    # Canonical values: EG p94.2 (below threshold, AMBER); Seats@50/50 p>99.9
    mdata = [
        ('Efficiency Gap†', '+0.040', '+0.016', 'p94.2',  '0.058',  AMBER),
        ('Mean-Median',     '+0.010', '−0.020', 'p99.99', '< 0.001', RED),
        ('Declination',     '−0.077', '−0.002', 'p0.4',   '0.004',   RED),
        ('Seats @ 50/50',   '+0.517', '+0.452', 'p>99.9', '< 0.001', RED),
        ('Pop. MAD',        '3,938',  '—',      'p98.9',  '—',       RED),
    ]
    yy = 0.762
    for i, (met, obs, emn, pct, mp, col) in enumerate(mdata):
        if i % 2 == 0:
            am.axhspan(yy - 0.096, yy + 0.030, xmin=0.01, xmax=0.99,
                       facecolor=LGRAY, alpha=0.65)
        T(am, COLS[0], yy - 0.030, met, fs=11,   c=DARK, ha='left')
        T(am, COLS[1], yy - 0.030, obs, fs=11,   c=col,  ha='left', bold=True)
        T(am, COLS[2], yy - 0.030, emn, fs=11,   c=GRAY, ha='left')
        T(am, COLS[3], yy - 0.030, pct, fs=11,   c=col,  ha='left',
          bold=(col in (RED,)))
        mp_c = col if mp != '—' else GRAY
        T(am, COLS[4], yy - 0.030, mp,  fs=11,   c=mp_c, ha='left')
        yy -= 0.144

    T(am, 0.03, 0.044,
      '† EG p94.2 — below p95 individual threshold (retracted); '
      'all four metrics still feed the joint Mahalanobis score.',
      fs=8.5, c=AMBER, ha='left', italic=True)

    # Right panel — Non-partisan structural signals
    ns = P(0.473, _DB, 0.517, _DH, bg=WHITE, ec=RED, lw=1.2)
    T(ns, 0.5, 0.964, 'NON-PARTISAN STRUCTURAL SIGNALS',
      fs=12.5, c=RED, bold=True)
    T(ns, 0.5, 0.906,
      'Four surviving signals, all minority more irregular',
      fs=9.5, c=GRAY, italic=True)
    HL(ns, 0.875, c='#E0B0AC', lw=0.8)

    sigs = [
        ('Population dispersion (MAD)',   'Minority 48% wider than majority',   '✓'),
        ('Calgary zone asymmetry',        'Minority 12.2%  ·  Majority 0.4%',   '✓'),
        ('Airdrie fragmentation',         'Minority 4-way  ·  Majority 2-way',   '✓'),
        ('Chair-flagged anomalies',       '3 minority  ·  0 majority',           '✓'),
        ('Municipal anchoring',           'Both within Canadian norm (70–85%)',  '—'),
    ]
    yy = 0.828
    for sig, desc, mark in sigs:
        col = RED if mark == '✓' else GRAY
        bg  = LRED if mark == '✓' else '#F5F6F7'
        ns.axhspan(yy - 0.104, yy + 0.028, xmin=0.01, xmax=0.99,
                   facecolor=bg, alpha=0.45)
        T(ns, 0.04, yy - 0.014, sig,  fs=10.5, c=col,  ha='left', bold=(mark == '✓'))
        T(ns, 0.04, yy - 0.070, desc, fs=9.5,  c=GRAY, ha='left', italic=True)
        T(ns, 0.97, yy - 0.038, mark + (' FIRES' if mark == '✓' else ' not reproduced'),
          fs=10.5, c=col, ha='right', bold=(mark == '✓'))
        yy -= 0.148

    # ── CONCLUSION BAR ────────────────────────────────────────────────────────
    av = P(0, 0.055, 1, 0.138, bg=NAVY, ec=NAVY, lw=0)
    T(av, 0.5, 0.740,
      "The minority map’s four-metric partisan vector sits at Mahalanobis distance 6.11 from the ensemble centre.  "
      "Combined with SZAT, the joint neutral-null probability is 1 in 115 million.  "
      "Four non-partisan structural signals all run in the same direction.",
      fs=11.5, c=WHITE)
    T(av, 0.5, 0.298,
      'This audit records what public data show.  It does not reach a legal conclusion on gerrymandering.  '
      'Phase 2 pre-registered — pending the November 2026 Lunty committee 91-seat map.',
      fs=10, c='#A8B4C0', italic=True)

    # ── FOOTER ────────────────────────────────────────────────────────────────
    af = P(0, 0, 1, 0.053, bg='#CDD1D6', ec='#CDD1D6', lw=0)
    T(af, 0.5, 0.660,
      'Pre-registered:  #289,449 osf.io/w2s8k  ·  #289,451 osf.io/r3zm7  '
      '·  #289,455 osf.io/qsgy8  ·  #289,469 osf.io/6pt83',
      fs=9.5, c='#3D4F5C')
    T(af, 0.5, 0.255,
      'gerrychain 0.3.2 · ReCom · ±25% pop tolerance · 4,765 Vote Areas · EPSG:3400 · Data: Elections Alberta',
      fs=9, c='#5A6A78')

    # ── SAVE ──────────────────────────────────────────────────────────────────
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for out in [
        os.path.join(base, 'infographic_v3.png'),
        os.path.join(base, 'outputs', 'assets', 'infographic_v3.png'),
    ]:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        fig.savefig(out, dpi=120, facecolor=LGRAY, edgecolor='none')
        print(f'Saved: {out}')


if __name__ == '__main__':
    run()
