#!/usr/bin/env python3
"""
r090 / lem:eta part (b):  is  eta  at  theta = a/q  equal to  mu(q)/phi(q) ?

Ramanujan-sum prediction.  S_A(a/q) = SUM_{(r,q)=1} e(ra/q) pi(N;q,r)
                                    ~ (b/phi(q)) c_q(a) = (b/phi(q)) mu(q)   for (a,q)=1.
So  Re S_A(a/q)/b -> mu(q)/phi(q),  whose maximum over q >= 3 is  +1/2, attained
UNIQUELY at q = 6  (mu(q)=+1 and phi(q)=2 together force q=6).
That is the additive twin of paper 2's  sup_q M(q) = sqrt(3)/2  at q = 6.

Falsifier stated before running: if the measured Re S_A(a/q)/b does not track
mu(q)/phi(q) to within finite-size drift, the mechanism is wrong and rem:sixagain
stays a numerical coincidence.
"""
import math
import numpy as np


def sieve(m):
    s = np.ones(m + 1, bool); s[:2] = False
    for i in range(2, int(m ** .5) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.nonzero(s)[0]


def mobius(n):
    r, p, out = n, 2, 1
    while p * p <= r:
        if r % p == 0:
            r //= p
            if r % p == 0:
                return 0
            out = -out
        p += 1
    return -out if r > 1 else out


def phi(n):
    r, p, out = n, 2, n
    while p * p <= r:
        if r % p == 0:
            while r % p == 0:
                r //= p
            out -= out // p
        p += 1
    if r > 1:
        out -= out // r
    return out


for NMAX in (10 ** 5, 10 ** 6, 10 ** 7):
    P = sieve(NMAX)[1:].astype(float)          # odd primes
    b = len(P)
    print('=' * 78)
    print(f'odd primes up to {NMAX:,}   (b = {b:,})')
    print(f"  {'q':>4} {'a':>3} {'Re S_A(a/q)/b':>15} {'mu(q)/phi(q)':>14} "
          f"{'diff':>11}  {'mu':>3} {'phi':>4}")
    worst_q, worst_v = None, -np.inf
    for q in range(2, 17):
        mu, ph = mobius(q), phi(q)
        pred = mu / ph
        a = 1
        while math.gcd(a, q) != 1:
            a += 1
        meas = float(np.cos(2 * math.pi * a * P / q).sum() / b)
        if meas > worst_v:
            worst_v, worst_q = meas, q
        star = '   <-- worst' if q == 6 else ''
        print(f'  {q:4d} {a:3d} {meas:15.6f} {pred:14.6f} {meas - pred:11.2e}  '
              f'{mu:3d} {ph:4d}{star}')
    print(f'  max over 2 <= q <= 16 :  q = {worst_q}, value {worst_v:.6f}'
          f'   (prediction: q=6, 0.5)')
