"""Rules for placing the ballots not cast on election day (exploratory, not registered).

Every rule takes one division's voting areas and the division's non-election-day
totals for the two parties, and returns the two parties' placed ballots per
area. Every rule returns exactly the division totals it was given.

  M0  the registered rule (Amendment 12): one party mix for the whole division,
      areas weighted by their election-day two-party votes.   = general(beta=0, lam=0)
  P   the rule studied here: ballots go only to electors who did not vote on
      election day (names on the list minus election-day ballots), lam = 1
      exactly; each area keeps its own election-day lean at strength beta,
      with beta taken from provincial evidence only (BETA_P).  = general(BETA_P, 1)
  M1, M2  older comparison rules, used only in the provincial location tests.

general(beta, lam):
  beta  how much of the area's election-day lean the early voters share
        (0 = none, 1 = all of it, on the log-odds scale)
  lam   how the number of ballots is spread: 0 = like election-day votes,
        1 = like the electors who did not vote on election day
"""
import numpy as np
from scipy.optimize import brentq

BETA_P = 1.0      # value used; estimate and range in outputs/provincial_location_tests.json and robustness.json
LAM_P = 1.0       # fixed by the rule, not estimated
SHRINK_K = 10.0   # pseudo-count: a tiny area's share is pulled toward the division's share before the log-odds step


def _logit(p):
    p = np.clip(p, 0.005, 0.995)
    return np.log(p / (1 - p))


def general(e_n, e_u, gap, A_n, A_u, beta, lam, shrink_k=0.0):
    """G(beta, lam). e_n, e_u: election-day votes per area; gap: electors minus election-day ballots."""
    e_n, e_u, gap = (np.asarray(x, float) for x in (e_n, e_u, gap))
    e = e_n + e_u
    T = A_n + A_u
    if T <= 0 or e.sum() <= 0:
        return np.zeros_like(e), np.zeros_like(e)
    w = e / e.sum()
    g = np.clip(gap, 0, None)
    if lam > 0 and g.sum() > 0:
        w = (1 - lam) * w + lam * g / g.sum()
    P = e_n.sum() / e.sum()
    p = np.where(e + shrink_k > 0, (e_n + shrink_k * P) / np.where(e + shrink_k > 0, e + shrink_k, 1), P)
    x = beta * (_logit(p) - _logit(P))
    target = A_n / T
    if target <= 0:
        q = np.zeros_like(w)
    elif target >= 1:
        q = np.ones_like(w)
    else:
        a = brentq(lambda a: float(np.sum(w / (1 + np.exp(-(a + x)))) - target), -30, 30)
        q = 1 / (1 + np.exp(-(a + x)))
    return T * w * q, T * w * (1 - q)


def m0(e_n, e_u, gap, A_n, A_u):
    return general(e_n, e_u, gap, A_n, A_u, 0.0, 0.0)


def rule_p(e_n, e_u, gap, A_n, A_u, beta=BETA_P):
    return general(e_n, e_u, gap, A_n, A_u, beta, LAM_P, shrink_k=SHRINK_K)


def count_weights_p(gap):
    """P's count side: each area's share of the division's early ballots is its share of election-day non-voters."""
    g = np.clip(np.asarray(gap, float), 0, None)
    return g / g.sum() if g.sum() > 0 else np.full(len(g), 1.0 / len(g))


def allocate_p(t, tot, beta=BETA_P):
    """All 2023 ballots per voting area under P.

    t: build_va_table(); tot: division_totals(). Returns arrays (row order of t):
      ndp, ucp, other   election-day votes plus placed early votes
      placed_ballots    placed early ballots of every kind (valid, declined, rejected), for the turnout check
    Early NDP and UCP ballots follow rule_p; early ballots for other candidates, and declined and rejected
    early ballots, follow P's count side alone (no lean).
    """
    gap = np.nan_to_num(t.gap.values.astype(float), nan=0.0)
    n, u, o = t.e_n.values.copy(), t.e_u.values.copy(), t.e_o.values.copy()
    placed = np.zeros(len(t))
    for ed, ix in t.groupby("ed").indices.items():
        a_n, a_u = rule_p(t.e_n.values[ix], t.e_u.values[ix], gap[ix], float(tot.ndp[ed]), float(tot.ucp[ed]), beta)
        w = count_weights_p(gap[ix])
        n[ix] += a_n
        u[ix] += a_u
        o[ix] += float(tot.other[ed]) * w
        placed[ix] += float(tot.total[ed]) * w
    return {"ndp": n, "ucp": u, "other": o, "placed_ballots": placed}


def m1(e_n, e_u, gap, A_n, A_u):
    """Party-specific: NDP ballots by election-day NDP votes, UCP ballots by election-day UCP votes."""
    e_n, e_u = np.asarray(e_n, float), np.asarray(e_u, float)
    n = A_n * e_n / e_n.sum() if e_n.sum() > 0 else A_n * (e_n + e_u) / (e_n + e_u).sum()
    u = A_u * e_u / e_u.sum() if e_u.sum() > 0 else A_u * (e_n + e_u) / (e_n + e_u).sum()
    return n, u


def m2(e_n, e_u, gap, A_n, A_u):
    return general(e_n, e_u, gap, A_n, A_u, 0.5, 1.0)
