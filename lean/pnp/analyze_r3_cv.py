# 先行研究 Alyahya-Rowe (PPSN 2014) との差分チェック:
# 彼らは「局所最適数は重みの変動係数 CV と強い負の相関」と報告。
# 我々の Gamma が CV の言い換えでないかを、同じ100シードデータで検定する。
import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv(r"C:\Users\amake\Claude\Projects\study\lean\pnp\results_landscape_r2.csv")
df["mean"] = df.total/df.k
df["var"]  = df.sumsq/df.k - df["mean"]**2
df["cv"]   = np.sqrt(df["var"])/df["mean"]
df["lm_over_deg"] = df.lm/df.deg

def partial(x, y, z):
    """z を除いた x,y の偏相関"""
    rx = x - np.polyval(np.polyfit(z, x, 1), z)
    ry = y - np.polyval(np.polyfit(z, y, 1), z)
    return stats.pearsonr(rx, ry)

print("=== corr with lm (random, 100 seeds/k) ===")
for k, g in df[df.seq=="random"].groupby("k"):
    r_cv,  p_cv  = stats.pearsonr(g.cv, g.lm)
    r_gam, p_gam = stats.pearsonr(g.gamma, g.lm)
    r_cg,  _     = stats.pearsonr(g.cv, g.gamma)
    pr_g, pp_g = partial(g.gamma.values, g.lm.values, g.cv.values)      # CV を除いた Gamma
    pr_c, pp_c = partial(g.cv.values,    g.lm.values, g.gamma.values)   # Gamma を除いた CV
    print(f"k={k:2d}  corr(CV,lm)={r_cv:+.4f}  corr(G,lm)={r_gam:+.4f}  corr(CV,G)={r_cg:+.4f} | "
          f"partial(G,lm|CV)={pr_g:+.4f} (p={pp_g:.1e})  partial(CV,lm|G)={pr_c:+.4f} (p={pp_c:.1e})")

print()
print("=== corr with lm/deg (これが Gamma の本命) ===")
for k, g in df[df.seq=="random"].groupby("k"):
    r_cv,_  = stats.pearsonr(g.cv, g.lm_over_deg)
    r_gam,_ = stats.pearsonr(g.gamma, g.lm_over_deg)
    pr_g,pp_g = partial(g.gamma.values, g.lm_over_deg.values, g.cv.values)
    pr_c,pp_c = partial(g.cv.values, g.lm_over_deg.values, g.gamma.values)
    print(f"k={k:2d}  corr(CV,lm/deg)={r_cv:+.4f}  corr(G,lm/deg)={r_gam:+.4f} | "
          f"partial(G|CV)={pr_g:+.4f} (p={pp_g:.1e})  partial(CV|G)={pr_c:+.4f} (p={pp_c:.1e})")

print()
print("=== 素数列の CV と Gamma(ランダム平均との比較)===")
for k, g in df.groupby("k"):
    P = g[g.seq=="primes"].iloc[0]; R = g[g.seq=="random"]
    zc = (P.cv - R.cv.mean())/R.cv.std(ddof=1)
    zg = (P.gamma - R.gamma.mean())/R.gamma.std(ddof=1)
    print(f"k={k:2d}  prime CV={P.cv:.4f} (z={zc:+.3f})   prime Gamma={P.gamma:.4f} (z={zg:+.3f})")
