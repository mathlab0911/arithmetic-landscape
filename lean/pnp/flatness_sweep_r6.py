# flatness_sweep_r6.py (2026-08-08, opus-5 6周目)
# 目的: 5周目の予想 P6(平坦性 eps_d(k) は k について指数減衰、機構は mod 6 リップル)を
#       k = 8..24 の厳密 DP で実測する。素数列 vs ランダム奇数列。
# 出力: eps_d(k) の表、減衰比、Q=(lm/deg)/W_D の k 依存、r_{B_d} の mod 6 リップル振幅。
from fractions import Fraction
import random

def primes_upto(n):
    s = [True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]

ALLP = [p for p in primes_upto(2000) if p % 2 == 1]

def rep_counts(B):
    tot = sum(B); r = [0]*(tot+1); r[0] = 1
    for a in B:
        for m in range(tot, a-1, -1):
            r[m] += r[m-a]
    return r

def rget(r, m): return r[m] if 0 <= m < len(r) else 0

def analyze(A, dmax=8):
    """A: 昇順の奇数列。定理19で lm/deg を厳密再構成し、eps_d を測る。"""
    A = sorted(A); k = len(A); T = sum(A); n = T // 2
    rA = rep_counts(A); deg = rA[n]
    if deg == 0:
        return None
    D = (A[-1]-1)//2
    lm = deg
    eps = {}
    ripple = {}
    for d in range(1, D+1):
        Id = [a for a in A if a <= 2*d]
        Bd = [a for a in A if a > 2*d]
        sig = sum(Id)
        rB = rep_counts(Bd)
        lm += rget(rB, n+d) + rget(rB, n-d-sig)
        if d <= dmax:
            subs = {0}
            for a in Id: subs |= {s+a for s in subs}
            targets = sorted({n - s for s in subs} | {n+d, n-d-sig})
            vals = [rget(rB, m) for m in targets]
            lo, hi = min(vals), max(vals)
            eps[d] = (hi/lo - 1) if lo > 0 else float('inf')
            # mod 6 リップル: 窓の中心付近 +-30 で r_B を mod 6 の剰余類ごとに平均
            lo_m, hi_m = max(0, n-30), min(len(rB)-1, n+30)
            cls = {c: [] for c in range(6)}
            for m in range(lo_m, hi_m+1):
                cls[m % 6].append(rB[m])
            means = [sum(v)/len(v) if v else 0 for v in cls.values()]
            mu = sum(means)/6
            ripple[d] = (max(means)-min(means))/mu if mu > 0 else float('nan')
    Gamma = sum(Fraction(a, 2**(j+1)) for j, a in enumerate(A))
    W = Gamma + Fraction(A[-1], 2**k)
    Q = Fraction(lm, deg) / W
    return dict(k=k, T=T, n=n, deg=deg, lm=lm, Gamma=float(Gamma), W=float(W),
                lmdeg=float(Fraction(lm, deg)), Q=float(Q), eps=eps, ripple=ripple)

print("=== 素数列: k = 8..24 ===")
print(" k    deg      lm     lm/deg    W_D       Q       eps1     eps2     eps3     eps4     eps6")
prim = {}
for k in range(8, 25, 2):
    A = ALLP[:k]
    r = analyze(A)
    prim[k] = r
    e = r["eps"]
    print(f"{k:3d} {r['deg']:8d} {r['lm']:9d} {r['lmdeg']:8.4f} {r['W']:8.4f} {r['Q']:8.5f}"
          f" {e.get(1,float('nan')):8.4f} {e.get(2,float('nan')):8.4f} {e.get(3,float('nan')):8.4f}"
          f" {e.get(4,float('nan')):8.4f} {e.get(6,float('nan')):8.4f}")

print()
print("=== eps_d(k) の減衰比 eps_d(k+2)/eps_d(k)  (P6予想: (sqrt3/2)^2 = 0.75) ===")
print(" d " + "".join(f"  {k}->{k+2}" for k in range(8, 23, 2)))
for d in range(1, 7):
    row = f"{d:2d} "
    for k in range(8, 23, 2):
        a, b = prim[k]["eps"].get(d), prim[k+2]["eps"].get(d)
        row += f" {b/a:8.4f}" if (a and b and a > 0) else "      n/a"
    print(row)

print()
print("=== mod 6 リップル振幅 (r_Bd の剰余類別平均の最大-最小 / 平均) ===")
print(" k " + "".join(f"     d={d}" for d in range(1, 7)))
for k in range(8, 25, 2):
    print(f"{k:3d} " + "".join(f" {prim[k]['ripple'].get(d, float('nan')):8.4f}" for d in range(1, 7)))

print()
print("=== ランダム奇数列(同じ値域 [3, a_k]、各 k で20シード)との比較 ===")
print(" k   eps1(P)  eps1(R)med  eps2(P)  eps2(R)med  eps3(P)  eps3(R)med   Q(P)     Q(R)med")
for k in range(8, 25, 2):
    A = ALLP[:k]; maxV = A[-1]
    cands = [x for x in range(3, maxV+1, 2)]
    rows = []
    rnd = random.Random(20260808 + k)
    tries = 0
    while len(rows) < 20 and tries < 200:
        tries += 1
        R = sorted(rnd.sample(cands, k))
        res = analyze(R, dmax=3)
        if res: rows.append(res)
    def med(f):
        v = sorted(f(r) for r in rows)
        return v[len(v)//2] if v else float('nan')
    P = prim[k]
    print(f"{k:3d} {P['eps'][1]:9.4f} {med(lambda r: r['eps'][1]):10.4f}"
          f" {P['eps'][2]:9.4f} {med(lambda r: r['eps'][2]):10.4f}"
          f" {P['eps'][3]:9.4f} {med(lambda r: r['eps'][3]):10.4f}"
          f" {P['Q']:9.5f} {med(lambda r: r['Q']):9.5f}")
