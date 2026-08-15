# c23b_r76.py  判別の精密化: 大域フィットは平均化するので【局所指数】を見る。+ E2b。
import math
from fractions import Fraction
def odd_primes(k):
    out=[]; n=3
    while len(out)<k:
        if all(n%p for p in range(3,int(n**0.5)+1,2)): out.append(n)
        n+=2
    return out
def devs(k, rhos):
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
    return {r:((g(ns[r])+extra[r])/g(ns[r]))/G-1.0 for r in rhos}, A[-1], {r:g(ns[r]) for r in rhos}
RHOS=[0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.42,0.44,0.46]
KS=[120,150,180]
print("="*100)
print("【局所指数】隣接する2点から d logF / d log x を出す(x = 1/2 − ρ)。純冪なら一定")
print("="*100)
S={}
for k in KS:
    dv,N,dg=devs(k,RHOS); S[k]=(dv,N,dg)
    xs=[0.5-r for r in RHOS]; Fs=[dv[r]*N*N for r in RHOS]
    print(f"\n  k={k} (N={N})")
    print("    区間 x       局所指数   F の値      deg")
    for i in range(len(RHOS)-1):
        if Fs[i]<=0 or Fs[i+1]<=0: 
            print(f"   {xs[i]:.3f}→{xs[i+1]:.3f}      (F≤0)   {Fs[i]:9.2f} {Fs[i+1]:9.2f}"); continue
        a=math.log(Fs[i]/Fs[i+1])/math.log(xs[i]/xs[i+1])
        print(f"   {xs[i]:.3f}→{xs[i+1]:.3f}     {a:7.3f}   {Fs[i]:9.2f}   {dg[RHOS[i]]:.3e}")
print()
print("="*100)
print("【窓ごとの c₂,c₃ フィット】中心近く(小 x)だけで見ると係数は正か")
print("="*100)
def fit2(xs,Fs):
    S22=sum(x**4 for x in xs); S23=sum(x**5 for x in xs); S33=sum(x**6 for x in xs)
    b2=sum(F*x**2 for x,F in zip(xs,Fs)); b3=sum(F*x**3 for x,F in zip(xs,Fs))
    det=S22*S33-S23*S23
    return ( b2*S33-b3*S23)/det, (-b2*S23+b3*S22)/det
for k in KS:
    dv,N,_=S[k]
    print(f"\n  k={k}")
    for lo,hi,tag in ((0.04,0.16,"中心近く x∈[0.04,0.16] (ρ=0.34..0.46)"),
                      (0.10,0.25,"中間     x∈[0.10,0.25] (ρ=0.25..0.40)"),
                      (0.20,0.45,"外側     x∈[0.20,0.45] (ρ=0.05..0.30)")):
        sel=[r for r in RHOS if lo<=0.5-r<=hi]
        if len(sel)<3: continue
        xs=[0.5-r for r in sel]; Fs=[dv[r]*N*N for r in sel]
        c2,c3=fit2(xs,Fs)
        print(f"    {tag}:  c₂={c2:9.1f}  c₃={c3:10.1f}  c₂/c₃={c2/c3 if c3 else float('nan'):8.3f}")
print()
print("="*100)
print("【E2b】レート関数の普遍性  D_k(ρ) = Î^素数(ρ) − Î^奇数(ρ),  Î = −(1/k)ln(deg(⌊ρT⌋)/2^k)")
print("="*100)
def degcount(A,n):
    dp=[1]
    for a in A:
        new=[0]*(len(dp)+a)
        for m,c in enumerate(dp):
            if c: new[m]+=c; new[m+a]+=c
        dp=new
    return dp[n] if 0<=n<len(dp) else 0
RB=[0.20,0.30,0.40,0.50]
print("   k  " + "".join(f"   ρ={r:.2f}  " for r in RB) + "  符号")
prev=None
for k in (16,20,24,28,32,36,40,48,56,64):
    P=odd_primes(k); L=[2*i+1 for i in range(k)]
    row=[]; signs=set()
    for r in RB:
        dP=degcount(P,int(r*sum(P))); dL=degcount(L,int(r*sum(L)))
        if dP==0 or dL==0: row.append("   ---   "); continue
        IP=-math.log(dP/2**k)/k; IL=-math.log(dL/2**k)/k
        d=IP-IL; row.append(f"{d:+9.5f}"); signs.add(d>0)
    print(f" {k:3d}  "+"".join(row)+f"   {'一定' if len(signs)==1 else '★混在'}")
