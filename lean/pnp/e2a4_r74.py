# e2a4_r74.py  E2a の【補正則】を測る。剛性は確定したので、次は「1 への近づき方」の形。
#   仮説: ratio(ρ,k) − 1  ≈  C · (1/2 − ρ)^α / k^β
import time, math
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
    dp=[1]; cur=k; extra={r:0 for r in rhos}
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
    return {r:((g(ns[r])+extra[r]), g(ns[r])) for r in rhos}, G, T, A[-1]

RHOS=[0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45]
KS=[60,80,100,120,140]
print("="*112)
print("【E2a-4】補正則  ratio(ρ,k) − 1  の形。剛性は確定済みなので、1 への近づき方を測る")
print("="*112)
print("   k    N=a_k    T    " + "".join(f"  ρ={r:.2f}   " for r in RHOS))
data={}
for k in KS:
    t0=time.time(); out,G,T,N = run(k,RHOS)
    cells=[]
    for r in RHOS:
        lm,deg=out[r]
        if deg<10**4: cells.append("   ---    ")
        else:
            v=(lm/deg)/G-1.0; data[(k,r)]=v; cells.append(f"{v:+9.2e} ")
    print(f" {k:3d} {N:6d} {T:7d}  "+"".join(cells)+f"  ({time.time()-t0:.1f}s)")
print()
print("="*112)
print("【ρ 依存の形】固定 k で  log(ratio−1)  vs  log(1/2−ρ)  の傾き α")
print("="*112)
for k in KS:
    xs=[];ys=[]
    for r in RHOS:
        v=data.get((k,r))
        if v is not None and v>0: xs.append(math.log(0.5-r)); ys.append(math.log(v))
    if len(xs)>=4:
        n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
        a=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
        ss=sum((y-my)**2 for y in ys); rs=1-sum((y-(my+a*(x-mx)))**2 for x,y in zip(xs,ys))/ss
        print(f"   k={k:3d}: α = {a:6.3f}   (R²={rs:.4f}, 点数={n})")
print()
print("="*112)
print("【k 依存の形】固定 ρ で  log(ratio−1)  vs  log k  の傾き −β")
print("="*112)
for r in RHOS:
    xs=[];ys=[]
    for k in KS:
        v=data.get((k,r))
        if v is not None and v>0: xs.append(math.log(k)); ys.append(math.log(v))
    if len(xs)>=4:
        n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
        b=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
        ss=sum((y-my)**2 for y in ys); rs=1-sum((y-(my+b*(x-mx)))**2 for x,y in zip(xs,ys))/ss
        print(f"   ρ={r:.2f}: β = {-b:6.3f}   (R²={rs:.4f}, 点数={n})")
print()
print("  【注意 V3】点数が少ないので指数は当てない。上は『形の見当』であって主張ではない。")
