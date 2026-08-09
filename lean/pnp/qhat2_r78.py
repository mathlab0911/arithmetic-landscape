# qhat2_r78.py  Q̂ の k→∞ 外挿と Q̂(x)=A(1+γx²) の係数抽出、+ E2b 頑健性(参照列3本)
import math
from fractions import Fraction
def odd_primes(k):
    out=[]; n=3
    while len(out)<k:
        if all(n%p for p in range(3,int(n**0.5)+1,2)): out.append(n)
        n+=2
    return out
def run(k, rhos):
    A=odd_primes(k); T=sum(A); S2=sum(a*a for a in A); D=(A[-1]-1)//2
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
    V=S2/4.0
    return ({r:((g(ns[r])+extra[r])/g(ns[r]))/G-1.0 for r in rhos},
            {r:(T/2.0-ns[r])/V for r in rhos}, A[-1])
RHOS=[0.40,0.38,0.35,0.32,0.30,0.25,0.20]
KS=[100,140,180,220]
Q={};NS={}
for k in KS:
    dv,lam,N=run(k,RHOS); NS[k]=N
    for r in RHOS: Q[(k,r)]=dv[r]/lam[r]**2
print("="*100)
print("【Q̂ の k→∞ 外挿】残差の形を 1/N と 1/log N の両方で当てて、頑健かを見る")
print("="*100)
print("     x    " + "".join(f"  k={k} " for k in KS) + "  外挿(1/N)  外挿(1/logN)  差")
EXT={}
for r in RHOS:
    x=0.5-r; ys=[Q[(k,r)] for k in KS]
    def extrap(f):
        xs=[f(NS[k]) for k in KS]; n=len(xs)
        mx=sum(xs)/n; my=sum(ys)/n
        b=sum((a-mx)*(y-my) for a,y in zip(xs,ys))/sum((a-mx)**2 for a in xs)
        return my+b*(0-mx)
    e1=extrap(lambda N:1.0/N); e2=extrap(lambda N:1.0/math.log(N))
    EXT[x]=(e1+e2)/2
    print(f"  {x:.3f}  "+"".join(f"{v:7.1f}" for v in ys)+f"   {e1:8.1f}   {e2:9.1f}   {abs(e1-e2):5.1f}")
print()
print("="*100)
print("【Q̂∞(x) = A(1 + γx²) の当てはめ】(2案の外挿の平均を使用)")
print("="*100)
for lo,hi,tag in ((0.19,0.31,"x∈[0.20,0.30] 信頼域"),(0.19,0.41,"x∈[0.20,0.40] 拡大")):
    xs=[x for x in EXT if lo<=x<=hi]; ys=[EXT[x] for x in xs]
    # Q = A + Aγ x²  の線形回帰 (説明変数 x²)
    u=[x*x for x in xs]; n=len(u); mu=sum(u)/n; my=sum(ys)/n
    b=sum((a-mu)*(y-my) for a,y in zip(u,ys))/sum((a-mu)**2 for a in u)
    A0=my-b*mu; gam=b/A0
    r2=1-sum((y-(A0+b*a))**2 for a,y in zip(u,ys))/sum((y-my)**2 for y in ys)
    print(f"  {tag}: A = {A0:7.2f}   γ = {gam:6.2f}   R² = {r2:.5f}   (点数 {n})")
print()
print("  fable の理論候補 ΔV/V = −27/5 = −5.40 との比較:")
print("   ⇒ 実測 γ は【正】。符号が逆。値の大きさも 1.5 倍程度違う")
print()
print("="*100)
print("【E2b 頑健性】参照列を3本にして D_k(ρ) の符号・単調性を確認 (ρ=0.50)")
print("="*100)
def degcount(A,n):
    dp=[1]
    for a in A:
        new=[0]*(len(dp)+a)
        for m,c in enumerate(dp):
            if c: new[m]+=c; new[m+a]+=c
        dp=new
    return dp[n] if 0<=n<len(dp) else 0
import random
def refs(k):
    random.seed(20260809+k)
    P=odd_primes(k)
    return {"奇数 1,3,5,…":[2*i+1 for i in range(k)],
            "等差 5,11,17,…":[5+6*i for i in range(k)],
            "ランダム奇数(P と同レンジ)":sorted(random.sample(range(3,P[-1]+1,2),k))}
print("   k  " + "".join(f"  {t:<22s}" for t in ("奇数列","等差 6n+5","ランダム奇数"))+"  符号")
for k in (16,24,32,40,48,56):
    P=odd_primes(k); dP=degcount(P,int(0.5*sum(P))); IP=-math.log(dP/2**k)/k
    row=[]; sg=set()
    for t,L in refs(k).items():
        dL=degcount(L,int(0.5*sum(L)))
        if dL==0: row.append("        ---          "); continue
        d=IP-(-math.log(dL/2**k)/k); row.append(f"{d:+21.6f}"); sg.add(d>0)
    print(f" {k:3d}  "+"".join(row)+f"   {'全部正' if sg=={True} else ('全部負' if sg=={False} else '★混在')}")
