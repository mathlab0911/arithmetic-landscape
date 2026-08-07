# flatness_r5.py — Theorem 19 exact reconstruction at k=20 + flatness decomposition
# Exact DP over Python bigints. Primes k=20, rho=50% (n=355, T=710).
from fractions import Fraction

P = [3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73]
k = len(P); T = sum(P); n = 355
CSV_LM = 22808; CSV_DEG = 4344  # results_landscape_r1.csv primes k=20 rho=50

def rep_counts(B):
    """exact subset-sum representation counts r_B[m], m=0..sum(B)"""
    tot = sum(B)
    r = [0]*(tot+1); r[0] = 1
    for a in B:
        for m in range(tot, a-1, -1):
            r[m] += r[m-a]
    return r

rA = rep_counts(P)
deg = rA[n]
D = (P[-1]-1)//2  # 36

lm_rec = deg  # d=0 stratum
rows = []
for d in range(1, D+1):
    Id = [a for a in P if a <= 2*d]
    Bd = [a for a in P if a > 2*d]
    N = len(Id); sig = sum(Id)
    rB = rep_counts(Bd)
    def rget(r, m): return r[m] if 0 <= m < len(r) else 0
    over = rget(rB, n+d)
    under = rget(rB, n-d-sig)
    lm_rec += over + under
    # independence approx term: 2 * deg * 2^-N
    approx = Fraction(2*deg, 2**N)
    exact = over + under
    rows.append((d, N, sig, over, under, exact, approx))

print(f"T={T} n={n} deg={deg} (CSV {CSV_DEG}) lm_rec={lm_rec} (CSV {CSV_LM})")
print(f"Theorem19 exact match lm: {lm_rec == CSV_LM}, deg: {deg == CSV_DEG}")

# lm/deg vs W_D = Gamma + a_k/2^k
lmdeg = Fraction(lm_rec, deg)
Gamma = sum(Fraction(a, 2**(j+1)) for j, a in enumerate(P))
W = Gamma + Fraction(P[-1], 2**k)
print(f"lm/deg = {float(lmdeg):.6f}  W_D = {float(W):.6f}  Gamma = {float(Gamma):.6f}")
print(f"Q = (lm/deg)/W_D = {float(lmdeg/W):.6f}")

# per-d decomposition of the deficit
print("\n d  N(d) sigma  over  under  exact  approx   exact/approx")
tot_exact = Fraction(0); tot_approx = Fraction(0)
for (d, N, sig, over, under, exact, approx) in rows:
    ratio = float(Fraction(exact,1)/approx) if approx else float('nan')
    tot_exact += exact; tot_approx += approx
    if d <= 12 or exact > 0:
        print(f"{d:3d} {N:4d} {sig:5d} {over:6d} {under:6d} {exact:6d} {float(approx):9.2f} {ratio:8.4f}")
print(f"sums: exact(d>=1)={float(tot_exact):.1f} approx(d>=1)={float(tot_approx):.1f}")

# flatness epsilon per d: max/min of r_Bd over the exact convolution window
# deg = sum_{J subset Id} r_Bd(n - sigma(J)); window targets = n - sigma(J)
from itertools import combinations
print("\n flatness: d, N, window_width, min r, max r, at n+d, eps=max/min-1 (window incl n+d, n-d-sig)")
for (d, N, sig, over, under, exact, approx) in rows:
    if d > 8: break
    Id = [a for a in P if a <= 2*d]
    Bd = [a for a in P if a > 2*d]
    rB = rep_counts(Bd)
    # all subset sums of Id
    subs = {0}
    for a in Id:
        subs |= {s+a for s in subs}
    targets = sorted({n - s for s in subs} | {n+d, n-d-sig})
    vals = [rB[m] for m in targets if 0 <= m < len(rB)]
    lo, hi = min(vals), max(vals)
    eps = hi/lo - 1 if lo > 0 else float('inf')
    print(f"{d:3d} {N:3d} width={targets[-1]-targets[0]:4d}  {lo}  {hi}  {rB[n+d]}  eps={eps:.4f}")

# where does Q's deficit come from: cumulative exact-vs-approx by d
print("\ncumulative (lm/deg - W) contribution by d:")
cum = Fraction(0)
for (d, N, sig, over, under, exact, approx) in rows:
    cum += Fraction(exact, deg) - approx/deg
    if d in (1,2,3,4,5,6,8,10,15,20,36):
        print(f" d<={d:2d}: {float(cum):+.5f}")
print(f"total (lm/deg - W) = {float(lmdeg - W):+.5f}  (tail term a_k/2^k = {float(Fraction(P[-1],2**k)):.6f})")
