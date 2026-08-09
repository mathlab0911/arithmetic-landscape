# e2a3_r74.py  E2a を大きい k へ: B_d を d 降順に【増分構築】して配列1本で回す(メモリ O(T))
import time
from fractions import Fraction
def odd_primes(k):
    out=[]; n=3
    while len(out)<k:
        if all(n%p for p in range(3,int(n**0.5)+1,2)): out.append(n)
        n+=2
    return out
def run(k, rhos):
    A=odd_primes(k); T=sum(A); D=(A[-1]-1)//2
    G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
    ns={r:int(r*T) for r in rhos}
    dp=[1]; cur=k                      # B_d = A[cur:]、いまは空集合
    extra={r:0 for r in rhos}
    g=lambda m: dp[m] if 0<=m<len(dp) else 0
    for d in range(D,0,-1):
        j=0
        while j<k and A[j]<=2*d: j+=1  # B_d = A[j:]
        while cur>j:                   # d が下がる ⟹ B_d は増える
            cur-=1; a=A[cur]
            new=[0]*(len(dp)+a)
            for m,c in enumerate(dp):
                if c: new[m]+=c; new[m+a]+=c
            dp=new
        for r in rhos:
            n=ns[r]; extra[r]+= g(n+d)+g(T-n+d)
    while cur>0:                       # 全体集合まで伸ばして deg を取る
        cur-=1; a=A[cur]
        new=[0]*(len(dp)+a)
        for m,c in enumerate(dp):
            if c: new[m]+=c; new[m+a]+=c
        dp=new
    out={}
    for r in rhos:
        deg=g(ns[r]); out[r]=(deg+extra[r], deg)
    return out,G,T

RHOS=[0.20,0.30,0.40,0.50]
print("="*104)
print("【E2a-3】大きい k での剛性の確認(ρ=0.20 まで含む)。判定子 spread = max_ρ ratio − min_ρ ratio")
print("="*104)
print("   k     T    " + "".join(f"  ρ={r:.2f}  " for r in RHOS) + "   spread   max|r−1|  (時間)")
res={}
for k in (40,52,64,76,88,100):
    t0=time.time(); out,G,T=run(k,RHOS)
    vals=[]; cells=[]
    for r in RHOS:
        lm,deg=out[r]
        if deg<10**4: cells.append("  ---   ")
        else:
            v=(lm/deg)/G; vals.append(v); cells.append(f"{v:8.5f}")
    sp=max(vals)-min(vals); mx=max(abs(v-1) for v in vals); res[k]=(sp,mx)
    print(f" {k:3d} {T:6d}  "+"".join(cells)+f"  {sp:.6f} {mx:.6f}  ({time.time()-t0:.1f}s)")
print()
ks=sorted(res)
print("   k       : "+" ".join(f"{k:9d}" for k in ks))
print("   spread  : "+" ".join(f"{res[k][0]:9.6f}" for k in ks))
print("   max|r−1|: "+" ".join(f"{res[k][1]:9.6f}" for k in ks))
import math
print()
print("   参考: 論文2 の予言する減衰 (√3/2)^k との比較(比が一定なら同じレート)")
print("   k       : "+" ".join(f"{k:9d}" for k in ks))
print("   (√3/2)^k: "+" ".join(f"{(math.sqrt(3)/2)**k:9.2e}" for k in ks))
print("   max|r−1|/(√3/2)^k: "+" ".join(f"{res[k][1]/((math.sqrt(3)/2)**k):9.1f}" for k in ks))
