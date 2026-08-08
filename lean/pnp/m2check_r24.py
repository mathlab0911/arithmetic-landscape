# m2check_r24.py (2026-08-08, opus-5 19周目)
# fable-5 指示書 opus5_報告兼指示書_r23.md 作業1: M2.4 の照合。
#
# 主張(fable-5, paper2_M2_draft.md):
#   主要弧の LCLT に Edgeworth 第1補正を入れると、中心密度の補正因子が
#       1 − S4/(4 S2^2)
#   になる。これが「P2 絶対公式の 0.972」の正体ではないか。【予想】
#
# 検証:
#   deg * sqrt(2 pi V0) / 2^b − 1   と   − S4/(4 S2^2)   を比べる (V0 = S2/4)
#   合格基準(fable-5): k >= 16 で差が 0.5% 以内。
#
# 検証プロトコル:
#   V2b … deg は Seeds.lean と独立に Python の DP で計算し、CSV の deg 列と一致するか照合する
#   V1  … 出力は m2check_r24.log に保存
#   V2c … 比だけでなく生の deg と両辺の値を印字
import math, csv, os

# ---------- Seeds.lean の乱数列を完全再現(LCG、UInt64) ----------
MASK = (1 << 64) - 1
def lcg_next(s): return (s * 6364136223846793005 + 1442695040888963407) & MASK
def rand_odds(k, maxV, seed):
    cands = [n for n in range(maxV + 1) if n >= 3 and n % 2 == 1]
    s = seed & MASK; acc = []
    for _ in range(k):
        if not cands: break
        s = lcg_next(s)
        i = (s >> 33) % len(cands)
        acc.append(cands[i]); cands.pop(i)
    return acc

def is_prime(n):
    if n < 2: return False
    for d in range(2, int(n**0.5) + 1):
        if n % d == 0: return False
    return True
ODDPRIMES = [n for n in range(400) if is_prime(n) and n % 2 == 1]

def rep_counts(B):
    tot = sum(B); r = [0]*(tot+1); r[0] = 1
    for a in B:
        for m in range(tot, a-1, -1): r[m] += r[m-a]
    return r

def deg_of(B):
    """Seeds.lean の invariants と同じ定義: n = total//2、最小エネルギーを達成する部分集合の個数。"""
    r = rep_counts(B); n = sum(B)//2
    best = None; tot = 0
    for m, c in enumerate(r):
        if c == 0: continue
        e = abs(m - n)
        if best is None or e < best: best = e; tot = c
        elif e == best: tot += c
    return tot, best

def moments(B):
    S2 = sum(a*a for a in B); S4 = sum(a**4 for a in B)
    return S2, S4

def lhs_rhs(B):
    b = len(B); S2, S4 = moments(B)
    deg, gs = deg_of(B)
    V0 = S2/4.0
    lhs = deg*math.sqrt(2*math.pi*V0)/(2.0**b) - 1.0
    rhs = -S4/(4.0*S2*S2)
    return deg, gs, lhs, rhs, S2, S4

# ---------- V2b: CSV の deg 列と独立計算が一致するか ----------
print("="*100)
print("[V2b] 独立実装の deg が Seeds.lean(CSV)の deg と一致するか")
print("="*100)
CSV = "results_landscape_r2.csv"
mismatch = 0; checked = 0
if os.path.exists(CSV):
    with open(CSV) as f:
        for row in csv.DictReader(f):
            k = int(row["k"]); seed = int(row["seed"])
            if row["seq"] == "primes":
                B = sorted(ODDPRIMES[:k])
            else:
                maxV = ODDPRIMES[:k][-1]
                B = sorted(rand_odds(k, maxV, (20260807 + seed*2654435761) & MASK))
            if sum(B) != int(row["total"]):
                mismatch += 1; continue
            d, _ = deg_of(B); checked += 1
            if d != int(row["deg"]): mismatch += 1
    print(f"  照合 {checked} 行 / 不一致 {mismatch} 行")
    print("  ⇒ 一致。以降の deg は信頼してよい" if mismatch == 0 else "  ★不一致あり。以降の結論は保留")
else:
    print("  CSV が見つからない")

# ---------- 素数列 ----------
print()
print("="*100)
print("[1] 素数列 k = 8..28")
print("="*100)
print("   k   b     deg        gs   実測 (deg*sqrt(2piV0)/2^b − 1)   予言 (−S4/(4S2^2))     差")
for k in range(8, 29, 2):
    B = sorted(ODDPRIMES[:k]); b = len(B)
    deg, gs, lhs, rhs, S2, S4 = lhs_rhs(B)
    print(f" {k:3d} {b:3d} {deg:11d}   {gs:2d}        {lhs:+11.6f}             {rhs:+11.6f}   {lhs-rhs:+10.6f}")

# ---------- 100シード ----------
print()
print("="*100)
print("[2] ランダム奇数列 100シード(Seeds.lean と同じ列を再現)")
print("="*100)
print("   k    シード数    実測の平均      予言の平均      |差| の平均    |差| の最大")
allrows = []
for k in (8, 12, 16, 18, 20):
    maxV = ODDPRIMES[:k][-1]
    ds = []
    for i in range(100):
        B = sorted(rand_odds(k, maxV, (20260807 + i*2654435761) & MASK))
        if len(B) != k: continue
        deg, gs, lhs, rhs, S2, S4 = lhs_rhs(B)
        ds.append((lhs, rhs))
        allrows.append((k, i, B, deg, lhs, rhs))
    ml = sum(x for x, _ in ds)/len(ds); mr = sum(y for _, y in ds)/len(ds)
    dd = [abs(x-y) for x, y in ds]
    print(f" {k:3d}     {len(ds):4d}     {ml:+11.6f}    {mr:+11.6f}    {sum(dd)/len(dd):10.6f}   {max(dd):10.6f}")

print()
print("  合格基準(fable-5): k >= 16 で差が 0.5% 以内")

# ---------- 差の k 依存 ----------
print()
print("="*100)
print("[3] 差の k 依存 —— 高次項 (S4/S2^2)^2 のスケールで説明できるか(素数列)")
print("="*100)
print("   k      差 D          (S4/S2^2)^2        D / (S4/S2^2)^2")
for k in range(8, 29, 2):
    B = sorted(ODDPRIMES[:k])
    deg, gs, lhs, rhs, S2, S4 = lhs_rhs(B)
    q = (S4/S2**2)**2
    print(f" {k:3d}   {lhs-rhs:+11.6f}     {q:12.8f}      {(lhs-rhs)/q:+10.4f}")
print("  比が一定なら、残差は次の次数 (S4/S2^2)^2 で説明できる。")

# ---------- lm / pred2 ----------
print()
print("="*100)
print("[4] 『0.97 の謎』本体: lm / pred2 は 1 ± 0.01 に入るか")
print("     pred  = Gamma * deg          (論文1 の P2 絶対公式のもとの形)")
print("     pred2 = pred * (1 − S4/(4S2^2))  ではなく、補正は deg 側ではなく")
print("             『Gaussian 予測から deg を出す』側に入るので、ここでは")
print("     lm ≈ Gamma * 2^b/sqrt(2 pi V0) * (1 − S4/(4S2^2)) を見る。")
print("="*100)
def gamma_of(B):
    g = 0.0; p = 1.0
    for x in sorted(B):
        p /= 2.0; g += p*x
    return g
def lm_of(B):
    """Seeds.lean と同じ全数探索(k <= 24 まで)"""
    k = len(B); n = sum(B)//2
    sums = [0]
    for x in B:
        sums = sums + [s+x for s in sums]
    gs = min(abs(s-n) for s in sums)
    lm = 0
    for idx, s in enumerate(sums):
        e = abs(s-n); ok = True
        for i in range(k):
            ns = s - B[i] if (idx >> i) & 1 else s + B[i]
            if abs(ns-n) <= e: ok = False; break
        if ok: lm += 1
    return lm, gs
print("   k     lm        Gamma      lm/(Gamma*deg)   lm/(Gamma*deg*(1−S4/(4S2^2)))")
for k in range(8, 25, 2):
    B = sorted(ODDPRIMES[:k])
    deg, gs, lhs, rhs, S2, S4 = lhs_rhs(B)
    # lm は 2^k 列挙なので k<=24 に限る(Seeds.lean と同じ順序で idx ビットを対応させる)
    sums = [0]
    for x in B: sums = sums + [s+x for s in sums]
    n = sum(B)//2
    gsv = min(abs(s-n) for s in sums)
    lm = 0
    for idx, s in enumerate(sums):
        e = abs(s-n); ok = True
        for i in range(k):
            ns = s - B[i] if (idx >> i) & 1 else s + B[i]
            if abs(ns-n) <= e: ok = False; break
        if ok: lm += 1
    G = gamma_of(B)
    corr = 1.0 + rhs
    print(f" {k:3d} {lm:9d}   {G:9.5f}     {lm/(G*deg):10.5f}          {lm/(G*deg*corr):10.5f}")
print()
print("  注意: 補正 (1−S4/(4S2^2)) は『deg を Gauss 近似から出すとき』の因子である。")
print("        lm/(Gamma*deg) は deg を実測で使っているので、補正を掛けると逆に悪くなるはず。")
print("        『0.97 の謎』が P2 の絶対公式(Gauss 予測で deg を置き換える形)にあるなら、")
print("        [1] の比較で決着する。")
