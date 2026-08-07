# figures_r9.py (2026-08-08) — 論文用の図を PDF(ベクタ)で生成する。
#   fig_flatness.pdf   : eps_d(k) の指数減衰、素数 vs ランダム、予測レート sqrt(3)/2
#   fig_convergence.pdf: Q = (lm/deg)/W_D の k 依存(ランダムは100シードの平均±SD、素数は厳密値)
# 数値はすべてこのスクリプト内で再計算する(論文の表と同じ手順)。
import math, random
from fractions import Fraction
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["DejaVu Serif"],
    "font.size": 9, "axes.linewidth": 0.7,
    "xtick.direction": "in", "ytick.direction": "in",
    "xtick.major.width": 0.7, "ytick.major.width": 0.7,
    "legend.frameon": False, "pdf.fonttype": 42,
})

def primes_upto(n):
    s = [True]*(n+1); s[0]=s[1]=False
    for i in range(2, int(n**0.5)+1):
        if s[i]:
            for j in range(i*i, n+1, i): s[j]=False
    return [i for i in range(n+1) if s[i]]

ALLP = [p for p in primes_upto(2000) if p % 2 == 1]

def rep_counts(B):
    tot = sum(B); r = [0]*(tot+1); r[0] = 1
    for a in B:
        for m in range(tot, a-1, -1):
            r[m] += r[m-a]
    return r

def rget(r, m): return r[m] if 0 <= m < len(r) else 0

def analyze(A, dmax=6):
    A = sorted(A); k = len(A); T = sum(A); n = T // 2
    rA = rep_counts(A); deg = rA[n]
    if deg == 0: return None
    D = (A[-1]-1)//2
    lm = deg; eps = {}
    for d in range(1, D+1):
        Id = [a for a in A if a <= 2*d]
        Bd = [a for a in A if a > 2*d]
        sig = sum(Id); rB = rep_counts(Bd)
        lm += rget(rB, n+d) + rget(rB, n-d-sig)
        if d <= dmax:
            subs = {0}
            for a in Id: subs |= {s+a for s in subs}
            targets = sorted({n - s for s in subs} | {n+d, n-d-sig})
            vals = [rget(rB, m) for m in targets]
            lo, hi = min(vals), max(vals)
            eps[d] = (hi/lo - 1) if lo > 0 else float('inf')
    Gamma = sum(Fraction(a, 2**(j+1)) for j, a in enumerate(A))
    W = Gamma + Fraction(A[-1], 2**k)
    return dict(k=k, deg=deg, lm=lm, W=float(W), Q=float(Fraction(lm, deg)/W), eps=eps)

KS = list(range(8, 25, 2))
print("computing primes ...")
prim = {k: analyze(ALLP[:k]) for k in KS}

print("computing random (20 seeds per k) ...")
rnd_eps, rnd_Q = {}, {}
for k in KS:
    A = ALLP[:k]; maxV = A[-1]
    cands = [x for x in range(3, maxV+1, 2)]
    rng = random.Random(20260808 + k); rows = []; tries = 0
    while len(rows) < 20 and tries < 300:
        tries += 1
        res = analyze(sorted(rng.sample(cands, k)), dmax=4)
        if res: rows.append(res)
    def med(vals):
        v = sorted(vals); return v[len(v)//2] if v else float('nan')
    rnd_eps[k] = {d: med([r["eps"][d] for r in rows if d in r["eps"]]) for d in (2, 3)}
    rnd_Q[k] = med([r["Q"] for r in rows])

# ---------------- Figure 1: flatness decay ----------------
fig, ax = plt.subplots(figsize=(5.0, 3.4))
SQ = math.sqrt(3)/2
styles = {2: ("o", "#1f4e79"), 3: ("s", "#2e75b6"), 4: ("^", "#8faadc")}
for d, (mk, col) in styles.items():
    xs = [k for k in KS if d in prim[k]["eps"] and prim[k]["eps"][d] not in (0, float('inf'))]
    ys = [prim[k]["eps"][d] for k in xs]
    ax.semilogy(xs, ys, marker=mk, color=col, ms=4, lw=1.1, label=f"primes, $d={d}$")
for d, col in ((2, "#c00000"), (3, "#e8a0a0")):
    xs = [k for k in KS if rnd_eps[k][d] not in (0, float('inf')) and rnd_eps[k][d] == rnd_eps[k][d]]
    ys = [rnd_eps[k][d] for k in xs]
    ax.semilogy(xs, ys, marker="v", color=col, ms=4, lw=1.1, ls="--", label=f"random, $d={d}$")
# reference slope (sqrt3/2)^k anchored at the primes d=2 point at k=16
anchor_k, anchor_y = 16, prim[16]["eps"][2]
xs = list(range(14, 25))
ax.semilogy(xs, [anchor_y * SQ**(x-anchor_k) for x in xs], color="0.35", lw=0.9, ls=":",
            label=r"slope $(\sqrt{3}/2)^{k}$")
ax.set_xlabel("$k$ (number of terms)")
ax.set_ylabel(r"flatness $\varepsilon_d(k)$")
ax.set_xticks(KS)
ax.legend(ncol=2, fontsize=7.5, loc="lower left")
ax.grid(True, which="major", lw=0.3, color="0.85")
fig.tight_layout()
fig.savefig("fig_flatness.pdf")
print("wrote fig_flatness.pdf")

# ---------------- Figure 2: convergence of Q ----------------
df = pd.read_csv(r"results_landscape_r2.csv")
df["Gamma_W"] = df.gamma  # gamma column already holds Gamma (tail term negligible)
df["Q100"] = (df.lm/df.deg)/df.gamma
seed_stats = (df[df.seq == "random"].groupby("k").Q100.agg(["mean", "std"]))

fig, ax = plt.subplots(figsize=(5.0, 3.4))
ax.axhline(1.0, color="0.4", lw=0.8, ls="--")

ks = list(seed_stats.index)
ax.errorbar(ks, seed_stats["mean"], yerr=seed_stats["std"],
            marker="o", ms=4, lw=1.1, capsize=3, color="#c00000",
            label="random, 100 seeds (mean $\\pm$ s.d.)")

ax.plot(KS, [prim[k]["Q"] for k in KS], marker="s", ms=4, lw=1.1,
        color="#1f4e79", label="primes (exact)")
ax.plot(KS, [rnd_Q[k] for k in KS], marker="v", ms=3.5, lw=0.9, ls=":",
        color="#e08080", label="random median (exact, 20 seeds)")

ax.set_xlabel("$k$ (number of terms)")
ax.set_ylabel(r"$Q = (\mathrm{lm}/\deg)\,/\,W_D$")
ax.set_xticks(KS)
ax.set_ylim(0.5, 1.7)
ax.legend(fontsize=7.5, loc="upper right")
ax.grid(True, which="major", lw=0.3, color="0.85")
fig.tight_layout()
fig.savefig("fig_convergence.pdf")
print("wrote fig_convergence.pdf")

# ---------------- printed cross-check against the logged tables ----------------
print("\n=== cross-check (should match flatness_sweep_r6.log / analyze_r2b.log) ===")
print(" k   Q(primes)   eps2(P)   eps3(P)   eps2(R)med")
for k in KS:
    p = prim[k]
    print(f"{k:3d} {p['Q']:10.5f} {p['eps'].get(2,float('nan')):9.4f} "
          f"{p['eps'].get(3,float('nan')):9.4f} {rnd_eps[k][2]:11.4f}")
print("\n100-seed Q stats (mean, sd):")
print(seed_stats.round(4).to_string())
