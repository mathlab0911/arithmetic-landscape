# e2a6_r74.py  崩壊が確認できた変数 dev·N² について、(a) k 独立性の定量化 (b) ρ の形
import math
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
    ns={r:int(r*T) for r in rhos}; dp=[1]; cur=k; extra={r:0 for r in rhos}
    g=lambda m: dp[m] if 0<=m<len(dp) else 0
    for d in range(D,0,-1):
        j=0
        while j<k and A[j]<=2*d: j+=1
        while cur>j:
            cur-=1; a=A[cur]; new=[0]*(len(dp)+a)
            for m,c in enumerate(dp):
                if c: new[m]+=c; new[m+a]+=c
            dp=new
        for r in rhos: n=ns[r]; extra[r]+= g(n+d)+g(T-n+d)
    while cur>0:
        cur-=1; a=A[cur]; new=[0]*(len(dp)+a)
        for m,c in enumerate(dp):
            if c: new[m]+=c; new[m+a]+=c
        dp=new
    return {r:((g(ns[r])+extra[r])/g(ns[r]))/G-1.0 for r in rhos}, A[-1]
RHOS=[0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40]
KS=[80,100,120,140,160,180]
D={};NN={}
for k in KS: D[k],NN[k]=run(k,RHOS)
print("="*106)
print("【F = dev × N²】(N = a_k = 最大元)。行が k、列が ρ。k で一定なら崩壊")
print("="*106)
print("   k    N   "+"".join(f"  ρ={r:.2f}  " for r in RHOS))
for k in KS:
    print(f" {k:3d} {NN[k]:5d} "+"".join(f"{D[k][r]*NN[k]**2:9.1f}" for r in RHOS))
print()
print("  列ごとの k 方向の変動 (k≥80 の max/min):")
print("   ρ    : "+" ".join(f"{r:8.2f}" for r in RHOS))
print("   変動 : "+" ".join(f"{max(D[k][r]*NN[k]**2 for k in KS)/min(D[k][r]*NN[k]**2 for k in KS):8.2f}"
                            if min(D[k][r]*NN[k]**2 for k in KS)>0 else "     ---" for r in RHOS))
print()
print("="*106)
print("【ρ の形】F(ρ) = C·(1/2−ρ)^α の指数 α(各 k で独立にフィット)")
print("="*106)
for k in KS:
    xs=[];ys=[]
    for r in RHOS:
        v=D[k][r]*NN[k]**2
        if v>0: xs.append(math.log(0.5-r)); ys.append(math.log(v))
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    a=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
    C=math.exp(my-a*mx)
    rs=1-sum((y-(my+a*(x-mx)))**2 for x,y in zip(xs,ys))/sum((y-my)**2 for y in ys)
    print(f"   k={k:3d}:  α = {a:6.3f}   C = {C:8.1f}   R² = {rs:.5f}   (点数 {n})")
print()
print("  【立方(α=3)を仮定したときの C = F/(1/2−ρ)³ の一定性】")
print("   k    "+"".join(f"  ρ={r:.2f}  " for r in RHOS))
for k in KS:
    print(f" {k:3d}  "+"".join(f"{D[k][r]*NN[k]**2/(0.5-r)**3:9.0f}" for r in RHOS))
