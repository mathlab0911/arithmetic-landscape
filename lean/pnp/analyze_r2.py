import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv(r"C:\Users\amake\Claude\Projects\study\lean\pnp\results_landscape_r2.csv")
df["pred"] = 2**df.k * df.gamma * np.sqrt(2.0/(np.pi*df.sumsq))
df["ratio"] = df.lm/df.pred
df["lm_over_deg"] = df.lm/df.deg

out = []
for k, g in df.groupby("k"):
    P = g[g.seq == "primes"].iloc[0]
    R = g[g.seq == "random"]
    r, p = stats.pearsonr(R.gamma, R.lm)
    rs, ps = stats.spearmanr(R.gamma, R.lm)
    # 残差相関: lm/pred が Γ に依存しないか(公式が Γ 依存を吸収できているか)
    z_lm = (P.lm - R.lm.mean())/R.lm.std(ddof=1)
    z_gam = (P.gamma - R.gamma.mean())/R.gamma.std(ddof=1)
    out.append(dict(
        k=k,
        prime_gamma=round(P.gamma,4), rand_gamma_mean=round(R.gamma.mean(),4),
        rand_gamma_sd=round(R.gamma.std(ddof=1),4), z_gamma=round(z_gam,3),
        prime_lm=int(P.lm), rand_lm_mean=round(R.lm.mean(),1),
        rand_lm_sd=round(R.lm.std(ddof=1),1), z_lm=round(z_lm,3),
        pearson_gamma_lm=round(r,4), pearson_p=f"{p:.2e}",
        spearman=round(rs,4), spearman_p=f"{ps:.2e}",
        prime_ratio=round(P.ratio,4), rand_ratio_mean=round(R.ratio.mean(),4),
        rand_ratio_sd=round(R.ratio.std(ddof=1),4),
        prime_lm_over_deg=round(P.lm_over_deg,3),
        rand_lm_over_deg_mean=round(R.lm_over_deg.mean(),3),
        rand_lm_over_deg_sd=round(R.lm_over_deg.std(ddof=1),3),
    ))
S = pd.DataFrame(out)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 50)
print("=== per-k summary (random: 100 seeds) ===")
print(S.to_string(index=False))

print()
print("=== P2 absolute formula: lm/pred over ALL rows ===")
print(df.groupby(["k","seq"]).ratio.agg(["mean","std","min","max"]).round(4).to_string())

print()
print("=== lm/deg vs gamma (all random rows pooled per k) ===")
for k, g in df[df.seq=="random"].groupby("k"):
    r,p = stats.pearsonr(g.gamma, g.lm_over_deg)
    print(f"k={k}: corr(gamma, lm/deg) = {r:.4f} (p={p:.2e}); mean lm/deg={g.lm_over_deg.mean():.3f} vs mean gamma={g.gamma.mean():.3f}")

print()
print("=== residual check: does lm/pred still depend on gamma? ===")
for k, g in df[df.seq=="random"].groupby("k"):
    r,p = stats.pearsonr(g.gamma, g.ratio)
    print(f"k={k}: corr(gamma, lm/pred) = {r:.4f} (p={p:.2e})")

print()
print("=== control: corr(lm, sumsq) and partial view ===")
for k, g in df[df.seq=="random"].groupby("k"):
    r1,_ = stats.pearsonr(g.sumsq, g.lm)
    print(f"k={k}: corr(sumsq, lm) = {r1:.4f}; corr(gamma, sumsq) = {stats.pearsonr(g.gamma,g.sumsq)[0]:.4f}")

print()
print("=== gs / deg sanity ===")
print(df.groupby(["k","seq"]).gs.agg(["mean","max"]).to_string())
