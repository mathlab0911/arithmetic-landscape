#!/usr/bin/env python3
"""
r088 / task 1 of spec_t3rigid_r087 §5.1 :  verify  lem:kappa   |G~(th)| <= |G(th)|^kappa .

Three independent layers of the check:
  (A) the elementary inequality it rests on:      1 - t*y  <=  (1-y)^t   (t,y in [0,1]) ?
  (B) the per-symbol consequence:                 1 - t*y  <=  (1-y)^kappa ?
  (C) the product statement on a minor-arc grid:  log|G~| <= kappa*log|G| ?
  (D) repair candidate (additive form):           |G~|^2 <= exp(-t_min * sum_a sin^2(pi a th))
"""
import math
import numpy as np

TWO_PI = 2.0 * math.pi


# ---------------------------------------------------------------- ensembles
def sieve(m):
    s = np.ones(m + 1, bool); s[:2] = False
    for i in range(2, int(m ** .5) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.nonzero(s)[0]


def ensemble(name, k):
    if name == 'odds':
        return np.arange(1, 2 * k, 2, dtype=np.int64)
    if name == 'squares':
        return (np.arange(1, k + 1, dtype=np.int64)) ** 2
    if name == 'primes':
        p = sieve(20 * k + 200)
        return p[1:k + 1].astype(np.int64)          # first k odd primes
    raise ValueError(name)


# ---------------------------------------------------------------- the tilt
def tilt(A, rho):
    """s > 0 solving  sum_a a/(1+e^{s a}) = rho * T   (rho < 1/2)."""
    T = float(A.sum()); tgt = rho * T
    a = A.astype(float)
    lo, hi = 0.0, 1.0
    while (a / (1.0 + np.exp(hi * a))).sum() > tgt:
        hi *= 2.0
        if hi > 1e6:
            raise RuntimeError('no bracket')
    for _ in range(200):
        mid = .5 * (lo + hi)
        if (a / (1.0 + np.exp(mid * a))).sum() > tgt:
            lo = mid
        else:
            hi = mid
    return .5 * (lo + hi)


# ---------------------------------------------------------------- (A) & (B)
def check_elementary(kappa=0.18):
    ys = np.linspace(0.0, 1.0, 2001)
    out = []
    for t in (0.18, 0.30, 0.50, 0.70, 0.90, 1.00):
        rhsA = np.power(1.0 - ys, t)               # (1-y)^t
        rhsB = np.power(1.0 - ys, kappa)           # (1-y)^kappa
        lhs = 1.0 - t * ys
        out.append((t,
                    float((rhsA - lhs).min()),     # <0  => claim (A) false
                    float(ys[np.argmin(rhsA - lhs)]),
                    float((rhsB - lhs).min()),     # <0  => claim (B) false
                    float(ys[np.argmin(rhsB - lhs)])))
    return out


# ---------------------------------------------------------------- (C) & (D)
def check_product(name, k, rho, ngrid=20001, seed=0):
    A = ensemble(name, k)
    s = tilt(A, rho)
    p = 1.0 / (1.0 + np.exp(s * A.astype(float)))
    t = 4.0 * p * (1.0 - p)
    kappa = float(t.min())

    rng = np.random.default_rng(seed)
    # theta grid: uniform sweep away from the main arc, plus random points,
    # plus deliberately chosen near-rational points (the minor-arc heartland).
    th = np.concatenate([
        np.linspace(1e-3, 0.5, ngrid),
        rng.random(ngrid) * 0.5,
        np.array([j / q + 1e-6 for q in (3, 5, 6, 7, 11, 13, 101, 1009)
                  for j in range(1, q) if j / q < 0.5]),
    ])

    a = A.astype(float)
    worst = -np.inf; worst_th = None; slack_min = np.inf
    viol = 0; tot = 0
    dmin_add = np.inf
    for chunk in np.array_split(th, max(1, len(th) // 400)):
        ph = TWO_PI * np.outer(chunk, a)                       # (m,k)
        y = np.sin(ph / 2.0) ** 2                              # sin^2(pi a th)
        # untilted:  |G| = prod |cos(pi a th)|
        c2 = np.clip(1.0 - y, 1e-300, None)
        logG = 0.5 * np.log(c2).sum(axis=1)
        # tilted:    |G~|^2 = prod (1 - t_a y)
        logGt = 0.5 * np.log(np.clip(1.0 - t[None, :] * y, 1e-300, None)).sum(axis=1)
        d = logGt - kappa * logG          # >0  => claim (C) violated
        tot += len(chunk); viol += int((d > 1e-12).sum())
        i = int(np.argmax(d))
        if d[i] > worst:
            worst = float(d[i]); worst_th = float(chunk[i])
        slack_min = min(slack_min, float((-d).min()))
        # (D) additive repair:  2*log|G~| <= -t_min * sum y
        dmin_add = min(dmin_add, float((-t.min() * y.sum(axis=1) - 2 * logGt).min()))
    return dict(name=name, k=k, rho=rho, s=s, kappa=kappa,
                pmin=float(p.min()), sN=s * float(A.max()),
                viol=viol, tot=tot, worst=worst, worst_th=worst_th,
                slack_min=slack_min, add_slack=dmin_add)


if __name__ == '__main__':
    print('=' * 74)
    print('(A) is  1 - t*y <= (1-y)^t  true?   [min over y of RHS-LHS; <0 means FALSE]')
    print('=' * 74)
    print(f"{'t':>6} {'min[(1-y)^t-(1-ty)]':>22} {'at y':>8} "
          f"{'min[(1-y)^.18-(1-ty)]':>24} {'at y':>8}")
    for t, mA, yA, mB, yB in check_elementary():
        print(f'{t:6.2f} {mA:22.6f} {yA:8.3f} {mB:24.6f} {yB:8.3f}')

    print()
    print('=' * 74)
    print('(C) pointwise product test on a minor-arc theta grid')
    print('=' * 74)
    print(f"{'ens':>8} {'k':>5} {'rho':>5} {'s':>10} {'kappa':>7} {'s*N':>7} "
          f"{'viol/tot':>14} {'max(logG~-k logG)':>18}")
    res = []
    for nm, k in (('odds', 200), ('squares', 150), ('primes', 200)):
        for rho in (0.4, 0.2):
            r = check_product(nm, k, rho)
            res.append(r)
            print(f"{r['name']:>8} {r['k']:5d} {r['rho']:5.2f} {r['s']:10.3e} "
                  f"{r['kappa']:7.4f} {r['sN']:7.3f} "
                  f"{r['viol']:6d}/{r['tot']:<7d} {r['worst']:18.3f}")
    print()
    print('(D) additive repair  2log|G~| <= -t_min*sum sin^2 : min slack over grid')
    for r in res:
        print(f"   {r['name']:>8} rho={r['rho']:.2f}  min slack = {r['add_slack']:.6f}"
              f"   ({'OK' if r['add_slack'] >= -1e-9 else 'FAILS'})")
