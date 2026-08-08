# floorsearch_r18.py (2026-08-08, opus-5 13周目)
# prob:window-floor の反例探索。
#   L(b) = 2*sqrt2*2^{-b/2} は R_c(大域)の下界。eps_d(窓)はこれに縛られない。
#   eps_2 / L(b) が 1 を大きく下回る奇数列があるか、系統的に探す。
#   見つかれば「窓版の床は存在しない」= fable-5 は証明を試みなくてよい。
import math, random

def rep_counts(B):
    tot=sum(B); r=[0]*(tot+1); r[0]=1
    for a in B:
        for m in range(tot,a-1,-1): r[m]+=r[m-a]
    return r
def rget(r,m): return r[m] if 0<=m<len(r) else 0

def eps_ratio(A, d=2):
    """eps_d / L(b_d) を返す。deg=0 なら None。"""
    A=sorted(A); T=sum(A); n=T//2
    Id=[a for a in A if a<=2*d]; Bd=[a for a in A if a>2*d]
    if not Bd: return None
    b=len(Bd); sig=sum(Id); rB=rep_counts(Bd)
    subs=[0]
    for a in Id: subs = subs + [s+a for s in subs]
    targets=sorted(set([n-s for s in subs]+[n+d, n-d-sig]))
    vals=[rget(rB,m) for m in targets]
    lo,hi=min(vals),max(vals)
    if lo<=0: return None
    eps=hi/lo-1
    L=2*math.sqrt(2)*2.0**(-b/2)
    return eps/L, eps, L, b

print("="*100)
print("prob:window-floor 反例探索 —  eps_2 / L(b) が 1 を大きく下回る奇数列を探す")
print("="*100)

best=[]
def try_seq(name, A):
    r=eps_ratio(A)
    if r is None: return
    ratio,eps,L,b = r
    best.append((ratio,name,eps,L,b,tuple(A)))

# 族1: ランダム奇数列(範囲・長さを振る)
rng=random.Random(20260808)
for k in range(12,33,2):
    for hi in (2*k, 4*k, 8*k, 16*k):
        cands=[x for x in range(1,hi+1,2)]
        if len(cands)<k: continue
        for _ in range(60):
            try_seq(f"rand k={k} hi={hi}", rng.sample(cands,k))

# 族2: 剰余を固定(mod 4 の位相を極端にする)
for k in range(12,33,2):
    try_seq(f"all 1 mod4 k={k}", [1+4*i for i in range(k)])
    try_seq(f"all 3 mod4 k={k}", [3+4*i for i in range(k)])
    try_seq(f"consec odd k={k}", [1+2*i for i in range(k)])
    try_seq(f"1mod4 half k={k}", [1+4*i for i in range(k//2)]+[3+4*i for i in range(k-k//2)])

# 族3: 等差・幾何・素数まわり
for k in range(12,33,2):
    try_seq(f"3+6i k={k}", [3+6*i for i in range(k)])
    try_seq(f"5+6i k={k}", [5+6*i for i in range(k)])
    try_seq(f"1+6i k={k}", [1+6*i for i in range(k)])

# 族4: 局所探索 — 比の小さい列から1要素ずつ変えて下げにいく
best.sort()
seeds=[b[5] for b in best[:30]]
for seed in seeds:
    cur=list(seed); r=eps_ratio(cur)
    if r is None: continue
    curr=r[0]
    for _ in range(400):
        A2=list(cur)
        i=rng.randrange(len(A2))
        delta=rng.choice([-4,-2,2,4,6,-6])
        v=A2[i]+delta
        if v<1 or v%2==0 or v in A2: continue
        A2[i]=v
        r2=eps_ratio(A2)
        if r2 and r2[0]<curr:
            cur, curr = A2, r2[0]
    try_seq(f"local-opt k={len(cur)}", cur)

best.sort()
print("  最小の 20 件(比が小さいほど床を破っている):")
print("   eps_2/L(b)    eps_2        L(b)      b   列(先頭8項)                     名前")
for ratio,name,eps,L,b,A in best[:20]:
    head=",".join(str(x) for x in sorted(A)[:8])
    print(f"  {ratio:9.4f}  {eps:.4e} {L:.4e} {b:3d}  {head:<32} {name}")

print()
rs=[x[0] for x in best]
rs.sort()
import statistics
print(f"  探索総数 {len(rs)} 件。最小 {rs[0]:.4f} / 5%点 {rs[len(rs)//20]:.4f} / 中央値 {statistics.median(rs):.4f} / 最大 {rs[-1]:.4f}")
print(f"  比が 0.5 未満: {sum(1 for x in rs if x<0.5)} 件 / 0.3 未満: {sum(1 for x in rs if x<0.3)} 件 / 0.1 未満: {sum(1 for x in rs if x<0.1)} 件")
print()
print("  判定: 比が 0.1 を大きく下回る列が構成できれば『窓版の床は無い』の証拠。")
print("        下限が 0.3〜0.5 あたりで止まるなら、窓版も同スケールで成り立つ可能性が高い。")
