# floorsearch2_r18.py — 反例が「整数の粒度」の人為物でないかを確認する。
#   小さい k では r の値が数十しかなく、3点が偶然一致して eps=0 になりうる。
#   k を大きくして r の典型値を上げ、比の下限が b とともにどう動くかを見る。
import math, random, statistics

def rep_counts(B):
    tot=sum(B); r=[0]*(tot+1); r[0]=1
    for a in B:
        for m in range(tot,a-1,-1): r[m]+=r[m-a]
    return r
def rget(r,m): return r[m] if 0<=m<len(r) else 0

def eps_ratio(A, d=2):
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
    L=2*math.sqrt(2)*2.0**(-b/2)
    return (hi/lo-1)/L, hi/lo-1, L, b, lo, len(targets)

print("="*104)
print("反例の再検討: k ごとに最小の eps_2/L(b) を局所探索で追い込む")
print("  『r の典型値』も併記 — これが小さいと整数の粒度で eps=0 が起きうる(人為物)")
print("="*104)
print("   k    b   最小 eps_2/L(b)   その eps_2   L(b)        min r   窓の点数   判定")
rng=random.Random(99)
for k in (12,16,20,24,28,32,36):
    hi=max(6*k, 60)
    cands=[x for x in range(1,hi+1,2)]
    bestr=None; bestA=None
    for _ in range(40):
        cur=rng.sample(cands,k)
        r=eps_ratio(cur)
        if r is None: continue
        curr=r[0]
        for _ in range(600):
            A2=list(cur); i=rng.randrange(len(A2))
            v=A2[i]+rng.choice([-6,-4,-2,2,4,6])
            if v<1 or v%2==0 or v in A2: continue
            A2[i]=v
            r2=eps_ratio(A2)
            if r2 and r2[0]<curr: cur,curr = A2,r2[0]
        rr=eps_ratio(cur)
        if rr and (bestr is None or rr[0]<bestr[0]): bestr,bestA = rr,cur
    ratio,eps,L,b,lo,npts = bestr
    verdict = "粒度の疑い" if lo < 200 else ("反例候補" if ratio<0.1 else "床は生きている")
    print(f"  {k:3d} {b:4d}   {ratio:12.5f}   {eps:.4e} {L:.4e} {lo:8d}   {npts:5d}    {verdict}")

print()
print("  判定の読み方: min r(窓内の最小の表現数)が数百未満なら、eps=0 は整数の丸めで起きうる。")
print("  min r が大きいのに比が 0 近くなら、本物の反例。")
