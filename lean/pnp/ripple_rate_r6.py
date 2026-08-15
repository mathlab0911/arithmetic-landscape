# ripple_rate_r6.py — P6 の予測レート sqrt(3)/2 = 0.86603 と実測の突き合わせ
# ripple_d(k) ~ C * lambda^k を log 線形回帰で当てる(k >= 14 の安定域)
import math

# flatness_sweep_r6.log の値をそのまま転記(k=8..24)
K = [8,10,12,14,16,18,20,22,24]
ripple = {
 1:[0.0940,0.0454,0.0106,0.0137,0.0059,0.0051,0.0033,0.0023,0.0017],
 2:[1.1970,0.8439,0.6199,0.4642,0.4072,0.2580,0.1930,0.1454,0.1086],
 3:[1.6418,1.0388,0.8291,0.6253,0.5470,0.3467,0.2540,0.1952,0.1439],
 4:[1.8020,1.2774,0.8493,0.6386,0.5518,0.3504,0.2606,0.1971,0.1445],
 5:[1.8020,1.2774,0.8493,0.6386,0.5518,0.3504,0.2606,0.1971,0.1445],
 6:[2.3077,1.3171,1.1958,0.7670,0.6616,0.4154,0.3642,0.2480,0.1967],
}
epsP = {
 2:[1.0000,0.7500,0.3684,0.3125,0.1827,0.1518,0.1104,0.0734,0.0570],
 3:[float('nan'),0.3333,0.8571,0.3200,0.2386,0.1944,0.1462,0.1112,0.0789],
 4:[float('nan'),2.0000,6.0000,0.5833,0.6944,0.4122,0.2987,0.2283,0.1573],
}
epsR = {  # ランダム列の中央値
 2:[0.5000,0.1429,0.0556,0.0300,0.0166,0.0072,0.0030,0.0016,0.0007],
 3:[2.0000,0.7500,0.2778,0.1389,0.0526,0.0148,0.0099,0.0023,0.0010],
}

def fit(ks, vs):
    ks = [k for k, v in zip(ks, vs) if v == v and v > 0]
    ys = [math.log(v) for v in vs if v == v and v > 0]
    n = len(ks)
    mk = sum(ks)/n; my = sum(ys)/n
    num = sum((k-mk)*(y-my) for k, y in zip(ks, ys))
    den = sum((k-mk)**2 for k in ks)
    slope = num/den
    # R^2
    pred = [my + slope*(k-mk) for k in ks]
    ss_res = sum((y-p)**2 for y, p in zip(ys, pred))
    ss_tot = sum((y-my)**2 for y in ys)
    return math.exp(slope), 1 - ss_res/ss_tot

TARGET = math.sqrt(3)/2
print(f"P6 の予測減衰レート sqrt(3)/2 = {TARGET:.5f}  (1ステップ k->k+1 あたり)")
print()
print("--- mod 6 リップル振幅の減衰レート lambda (k>=14 でフィット) ---")
print("  d   lambda    R^2     予測との比")
for d in sorted(ripple):
    ks = [k for k in K if k >= 14]
    vs = [v for k, v in zip(K, ripple[d]) if k >= 14]
    lam, r2 = fit(ks, vs)
    print(f" {d:2d}  {lam:.5f}  {r2:.4f}   {lam/TARGET:.4f}")

print()
print("--- 素数列の平坦性 eps_d の減衰レート (k>=14) ---")
for d in sorted(epsP):
    ks = [k for k in K if k >= 14]
    vs = [v for k, v in zip(K, epsP[d]) if k >= 14]
    lam, r2 = fit(ks, vs)
    print(f" d={d}: lambda={lam:.5f}  R^2={r2:.4f}   予測との比={lam/TARGET:.4f}")

print()
print("--- ランダム列の平坦性 eps_d の減衰レート (k>=14、比較用) ---")
for d in sorted(epsR):
    ks = [k for k in K if k >= 14]
    vs = [v for k, v in zip(K, epsR[d]) if k >= 14]
    lam, r2 = fit(ks, vs)
    print(f" d={d}: lambda={lam:.5f}  R^2={r2:.4f}   (素数より速い = 算術的障害がない)")
