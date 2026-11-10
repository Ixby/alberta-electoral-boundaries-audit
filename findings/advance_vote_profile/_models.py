"""Allocation rules for ballots not cast on election day (exploratory, not registered).

Every rule takes one division's small areas and the division's non-election-day
totals for the two parties, and returns the two parties' allocated ballots per
area. Every rule returns exactly the division totals it was given.

Names used in the write-up:
  M0  current audit rule: one party mix for the whole division, areas weighted
      by their election-day two-party count.              = general(beta=0, lam=0)
  M1  party-specific: each party's ballots follow that party's own election-day
      votes.
  M2  turnout gap: areas weighted by electors who did not vote on election day,
      party mix half way between the division mix and the area's own lean.
                                                          = general(beta=0.5, lam=1)
  G(beta, lam)  the general family that contains M0 and M2 and is fitted to data.
      beta: how much of the area's election-day lean the non-election-day
            voters share (0 = none, 1 = all of it, on the log-odds scale);
      lam:  how the *number* of ballots is spread: 0 = like election-day votes,
            1 = like the electors who did not vote on election day.
"""
import numpy as np
from scipy.optimize import brentq


def _logit(p):
    p = np.clip(p, 0.005, 0.995)
    return np.log(p / (1 - p))


def general(e_n, e_u, gap, A_n, A_u, beta, lam, shrink_k=0.0, w_extra=None):
    """G(beta, lam). e_n, e_u: election-day votes per area; gap: electors minus election-day ballots.

    shrink_k: pseudo-count pulling a tiny area's share toward the division share before the log-odds step.
    w_extra: optional (weights, mix) to blend a third volume pattern (used for location-informed variants).
    """
    e_n, e_u, gap = (np.asarray(x, float) for x in (e_n, e_u, gap))
    e = e_n + e_u
    T = A_n + A_u
    if T <= 0 or e.sum() <= 0:
        return np.zeros_like(e), np.zeros_like(e)
    w = e / e.sum()
    g = np.clip(gap, 0, None)
    if lam > 0 and g.sum() > 0:
        w = (1 - lam) * w + lam * g / g.sum()
    if w_extra is not None:
        wx, mix = w_extra
        w = (1 - mix) * w + mix * wx / wx.sum()
    P = e_n.sum() / e.sum()
    p = np.where(e + shrink_k > 0, (e_n + shrink_k * P) / np.where(e + shrink_k > 0, e + shrink_k, 1), P)
    x = beta * (_logit(p) - _logit(P))
    target = A_n / T
    if target <= 0:
        q = np.zeros_like(w)
    elif target >= 1:
        q = np.ones_like(w)
    else:
        f = lambda a: float(np.sum(w / (1 + np.exp(-(a + x)))) - target)
        a = brentq(f, -30, 30)
        q = 1 / (1 + np.exp(-(a + x)))
    return T * w * q, T * w * (1 - q)


def m0(e_n, e_u, gap, A_n, A_u):
    return general(e_n, e_u, gap, A_n, A_u, 0.0, 0.0)


def m1(e_n, e_u, gap, A_n, A_u):
    """Party-specific: NDP ballots by election-day NDP votes, UCP ballots by election-day UCP votes."""
    e_n, e_u = np.asarray(e_n, float), np.asarray(e_u, float)
    n = A_n * e_n / e_n.sum() if e_n.sum() > 0 else A_n * (e_n + e_u) / (e_n + e_u).sum()
    u = A_u * e_u / e_u.sum() if e_u.sum() > 0 else A_u * (e_n + e_u) / (e_n + e_u).sum()
    return n, u


def m2(e_n, e_u, gap, A_n, A_u):
    return general(e_n, e_u, gap, A_n, A_u, 0.5, 1.0)
