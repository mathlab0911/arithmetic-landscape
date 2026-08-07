import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv(r"C:\Users\amake\Claude\Projects\study\lean\pnp\results_landscape_r2.csv")
df["lm_over_deg"] = df.lm/df.deg
df["Q"] = df.lm_over_deg/df.gamma   # 1 に収束するか

print("=== Q = (lm/deg)/Gamma : per-k distribution ===")
print(df.groupby(["k","seq"]).Q.agg(["mean","std","min","max"]).round(4).to_string())

print()
print("=== regression lm/deg = a*Gamma + b (random rows) ===")
for k,g in df[df.seq=="random"].groupby("k"):
    a,b,r,p,se = stats.linregress(g.gamma, g.lm_over_deg)
    print(f"k={k}: slope={a:.4f} (se {se:.4f}), intercept={b:.4f}, R^2={r*r:.5f}")

print()
print("=== primes z-scores combined across k (Stouffer, k=8..20) ===")
zs=[]
for k,g in df.groupby("k"):
    P=g[g.seq=="primes"].iloc[0]; R=g[g.seq=="random"]
    z=(P.lm-R.lm.mean())/R.lm.std(ddof=1); zs.append(z)
zs=np.array(zs)
print("z_lm per k:", np.round(zs,3))
print("Stouffer Z (NOT independent across k; indicative only) =", round(zs.sum()/np.sqrt(len(zs)),3))

print()
print("=== empirical p-value: how many of 100 random seeds have lm <= primes' lm? ===")
for k,g in df.groupby("k"):
    P=g[g.seq=="primes"].iloc[0]; R=g[g.seq=="random"]
    c=(R.lm<=P.lm).sum(); cg=(R.gamma<=P.gamma).sum()
    print(f"k={k}: lm rank {c}/100 ; gamma rank {cg}/100")
