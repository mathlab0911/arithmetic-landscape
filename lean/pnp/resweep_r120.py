# r120: the definition change moves every Gamma in paper 1's experiment tables.
# The instances are reproducible from Seeds.lean's LCG, so recompute rather than rescale.
#
# POSITIVE CONTROL FIRST: this reimplementation must reproduce the `gamma` column of
# results_landscape_r2.csv (old definition) for all 505 rows before any new number is used.
import csv, os, statistics
from fractions import Fraction as F

M64 = (1 << 64) - 1
def lcg(s): return (s * 6364136223846793005 + 1442695040888963407) & M64

def odd_primes(k):
    out, n = [], 3
    while len(out) < k:
        if all(n % d for d in range(2, int(n**0.5) + 1)): out.append(n)
        n += 2
    return out

def rand_odds(k, maxV, seed):
    cands = [n for n in range(3, maxV + 1) if n % 2 == 1]
    s, acc = seed, []
    for _ in range(k):
        if not cands: break
        s = lcg(s)
        i = (s >> 33) % len(cands)
        acc.append(cands.pop(i))
    return acc

def gamma_old(A):                       # sum a_j 2^-j, ascending
    A = sorted(A); return sum(F(a, 2**(j+1)) for j, a in enumerate(A))
def gamma_new(A):                       # layer form
    A = sorted(A); M = A[-1]
    return 1 + 2*sum(F(1, 2**sum(1 for a in A if a <= 2*d)) for d in range(1, (M-1)//2 + 1))
def cv(A):
    k = len(A); m = sum(A)/k
    return (sum((a-m)**2 for a in A)/k)**0.5 / m

CSV = '/sessions/friendly-laughing-cerf/mnt/study/lean/pnp/results_landscape_r2.csv'
rows = list(csv.DictReader(open(CSV)))
print(f"rows in results_landscape_r2.csv: {len(rows)}")

data, worst = [], 0.0
for r in rows:
    k, seed = int(r['k']), int(r['seed'])
    A = odd_primes(k) if r['seq'] == 'primes' else \
        rand_odds(k, odd_primes(k)[-1], (20260807 + seed * 2654435761) & M64)
    A = sorted(A)
    assert len(A) == k and sum(A) == int(r['total']), (r['seq'], k, seed, sum(A), r['total'])
    d = abs(float(gamma_old(A)) - float(r['gamma'])); worst = max(worst, d)
    data.append(dict(seq=r['seq'], k=k, seed=seed, A=A, lm=int(r['lm']), deg=int(r['deg']),
                     g_old=float(gamma_old(A)), g_new=float(gamma_new(A)), cv=cv(A)))
print(f"POSITIVE CONTROL: sums match on all rows; worst |gamma_recomputed - gamma_in_csv| "
      f"= {worst:.3e}  (float32-ish print precision in the CSV)")
assert worst < 1e-5, "reimplementation does not reproduce the recorded instances"

def pear(x, y):
    n = len(x); mx, my = sum(x)/n, sum(y)/n
    sx = sum((a-mx)**2 for a in x)**0.5; sy = sum((b-my)**2 for b in y)**0.5
    return sum((a-mx)*(b-my) for a, b in zip(x, y))/(sx*sy)
def partial(x, y, z):
    rxy, rxz, ryz = pear(x, y), pear(x, z), pear(y, z)
    return (rxy - rxz*ryz)/(((1-rxz**2)*(1-ryz**2))**0.5)
def linreg(x, y):
    n = len(x); mx, my = sum(x)/n, sum(y)/n
    sxx = sum((a-mx)**2 for a in x); sxy = sum((a-mx)*(b-my) for a, b in zip(x, y))
    b1 = sxy/sxx; b0 = my - b1*mx
    yh = [b0 + b1*a for a in x]
    ssr = sum((b-h)**2 for b, h in zip(y, yh)); sst = sum((b-my)**2 for b in y)
    se = (ssr/(n-2)/sxx)**0.5
    return b1, se, b0, 1 - ssr/sst

for tag in ('g_old', 'g_new'):
    print()
    print(f"===== Table 'Q' with Gamma = {tag} =====")
    print(f"{'k':>3} {'mean Q':>8} {'s.d.':>8} {'slope a':>9} {'(s.e.)':>8} "
          f"{'intercept':>10} {'R^2':>8} {'corr(G,lm)':>11}")
    for k in (8, 12, 16, 18, 20):
        R = [d for d in data if d['k'] == k and d['seq'] == 'random']
        G = [d[tag] for d in R]; LD = [d['lm']/d['deg'] for d in R]; LM = [d['lm'] for d in R]
        Q = [a/b for a, b in zip(LD, G)]
        b1, se, b0, r2 = linreg(G, LD)
        print(f"{k:>3} {statistics.mean(Q):>8.3f} {statistics.stdev(Q):>8.4f} {b1:>9.3f} "
              f"{se:>8.3f} {b0:>10.3f} {r2:>8.5f} {pear(G, LM):>11.3f}")

print()
print("===== Table 'cv' (correlations and partials) =====")
print(f"{'k':>3} {'corr(CV,lm)':>12} {'corr(G,lm)':>11} {'corr(CV,G)':>11} "
      f"{'part(G,lm|CV)':>14} {'part(CV,lm|G)':>14}   [Gamma = new]")
for k in (8, 12, 16, 18, 20):
    R = [d for d in data if d['k'] == k and d['seq'] == 'random']
    C = [d['cv'] for d in R]; G = [d['g_new'] for d in R]; LM = [float(d['lm']) for d in R]
    print(f"{k:>3} {pear(C,LM):>12.3f} {pear(G,LM):>11.3f} {pear(C,G):>11.3f} "
          f"{partial(G,LM,C):>14.3f} {partial(C,LM,G):>14.3f}")
print("  (old-Gamma column, for comparison)")
for k in (8, 12, 16, 18, 20):
    R = [d for d in data if d['k'] == k and d['seq'] == 'random']
    C = [d['cv'] for d in R]; G = [d['g_old'] for d in R]; LM = [float(d['lm']) for d in R]
    print(f"{k:>3} {pear(C,LM):>12.3f} {pear(G,LM):>11.3f} {pear(C,G):>11.3f} "
          f"{partial(G,LM,C):>14.3f} {partial(C,LM,G):>14.3f}")

print()
print("===== lm/deg partials at k=20 =====")
for tag in ('g_old', 'g_new'):
    R = [d for d in data if d['k'] == 20 and d['seq'] == 'random']
    C = [d['cv'] for d in R]; G = [d[tag] for d in R]; LD = [d['lm']/d['deg'] for d in R]
    print(f"  {tag}: partial(Gamma, lm/deg | CV) = {partial(G,LD,C):+.4f}   "
          f"partial(CV, lm/deg | Gamma) = {partial(C,LD,G):+.4f}")

print()
print("===== primes: Gamma(P_k) under both definitions =====")
print(f"{'k':>3} {'old':>12} {'new':>12} {'lm/deg':>10} {'rand mean new':>14} {'z(new)':>8}")
for k in (8, 12, 16, 18, 20):
    P = [d for d in data if d['k'] == k and d['seq'] == 'primes'][0]
    R = [d for d in data if d['k'] == k and d['seq'] == 'random']
    gr = [d['g_new'] for d in R]
    z = (P['g_new'] - statistics.mean(gr))/statistics.stdev(gr)
    print(f"{k:>3} {P['g_old']:>12.4f} {P['g_new']:>12.4f} {P['lm']/P['deg']:>10.3f} "
          f"{statistics.mean(gr):>14.4f} {z:>8.3f}")
