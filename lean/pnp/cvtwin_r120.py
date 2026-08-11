# r120b (final): CV-twins.  Pairs of odd sets with IDENTICAL k, mean, variance -- hence
# identical coefficient of variation -- whose gap series differ.  The landscape is then
# measured by full enumeration.  CV predicts no difference; Gamma predicts one.
#
# Positive control (the check that can fail): GAMMA-twins, i.e. pairs with identical
# Gamma but different CV.  If the landscape followed CV these would separate; they must not.
import random, statistics
from fractions import Fraction as F

def Gamma(A):
    A = sorted(A); M = A[-1]
    return 1 + 2*sum(F(1, 2**sum(1 for a in A if a <= 2*d)) for d in range(1, (M-1)//2 + 1))

def cv(A):
    k = len(A); m = sum(A)/k
    return (sum((a-m)**2 for a in A)/k)**0.5 / m

def landscape_ratio(A, halfwidth=20):
    A = list(A); k = len(A); tot = sum(A)
    sums = [0]*(1 << k)
    for S in range(1, 1 << k):
        lo = S & -S; sums[S] = sums[S ^ lo] + A[lo.bit_length()-1]
    out = []
    for n in range(tot//2 - halfwidth, tot//2 + halfwidth + 1):
        lm = deg = 0
        for S in range(1 << k):
            E = abs(sums[S] - n)
            if E == 0: deg += 1
            ok = True
            for i in range(k):
                if abs(sums[S ^ (1 << i)] - n) <= E: ok = False; break
            if ok: lm += 1
        if deg: out.append(lm/deg)
    return statistics.median(out), len(out)

def harvest(K, POOL, trials, seed):
    random.seed(seed)
    b = {}
    for _ in range(trials):
        A = tuple(sorted(random.sample(POOL, K)))
        b.setdefault((sum(A), sum(a*a for a in A)), set()).add(A)
    return b

print("=== CV-twins: same CV by construction, Gamma free ===")
print(f"{'k':>3} {'CV':>10} {'Gamma':>10} {'lm/deg':>9}   set")
rows = []
for K, seed in ((12, 11), (13, 12), (14, 13)):
    b = harvest(K, list(range(1, 120, 2)), 300000, seed)
    best = None
    for _, fam in b.items():
        if len(fam) < 2: continue
        g = sorted((Gamma(A), A) for A in fam)
        sp = g[-1][0] - g[0][0]
        if best is None or sp > best[0]: best = (sp, g[0], g[-1])
    if best is None: continue
    _, (glo, Alo), (ghi, Ahi) = best
    rlo, nlo = landscape_ratio(Alo); rhi, nhi = landscape_ratio(Ahi)
    assert abs(cv(Alo) - cv(Ahi)) < 1e-12, "not a CV twin"
    for A, G, r in ((Alo, glo, rlo), (Ahi, ghi, rhi)):
        print(f"{K:>3} {cv(A):>10.6f} {float(G):>10.4f} {r:>9.3f}   {list(A)}")
    print(f"      -> CV ratio 1.0000 exactly;  Gamma ratio {float(ghi/glo):.3f};"
          f"  lm/deg ratio {rhi/rlo:.3f}   ({nlo},{nhi} targets)")
    rows.append((float(ghi/glo), rhi/rlo))

print()
print("=== positive control: Gamma-twins (same Gamma, CV free) ===")
for K, seed in ((12, 21), (13, 22), (14, 23)):
    random.seed(seed)
    b = {}
    for _ in range(200000):
        A = tuple(sorted(random.sample(list(range(1, 120, 2)), K)))
        b.setdefault(Gamma(A), set()).add(A)
    best = None
    for G, fam in b.items():
        if len(fam) < 2: continue
        c = sorted((cv(A), A) for A in fam)
        sp = c[-1][0] - c[0][0]
        if best is None or sp > best[0]: best = (sp, G, c[0], c[-1])
    if best is None: continue
    _, G, (clo, Alo), (chi, Ahi) = best
    assert Gamma(Alo) == Gamma(Ahi)
    rlo, _ = landscape_ratio(Alo); rhi, _ = landscape_ratio(Ahi)
    print(f"{K:>3} Gamma={float(G):.4f}={G} fixed;  CV {clo:.4f} vs {chi:.4f} "
          f"(ratio {chi/clo:.3f});  lm/deg {rlo:.3f} vs {rhi:.3f} (ratio {rhi/rlo:.3f})")
    # r121 (F22): the control instances must be machine-readable too.  The first version
    # printed the CV-twin sets and only the summary numbers for the Gamma-twins -- so the
    # pair that could have falsified the claim was the one a reader could not reproduce.
    print(f"      low  CV: {list(Alo)}")
    print(f"      high CV: {list(Ahi)}")
