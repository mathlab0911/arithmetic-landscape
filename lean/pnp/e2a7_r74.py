# e2a7_r74.py  端(ρ=0.05, 0.40)で立方から外れる原因の切り分け:
#   ρ↔傾き s の関係は非線形(ρ が中心から遠いと s は線形より速く伸びる)。
#   厳密に s を解いて w = s·N (最大元が感じる傾き、無次元) で書き直すと崩れが直るか。
import math
from fractions import Fraction
def odd_primes(k):
    out=[]; n=3
    while len(out)<k:
        if all(n%p for p in range(3,int(n**0.5)+1,2)): out.append(n)
        n+=2
    return out
def tilt(A, target):
    """Σ a/(1+e^{-s a}) = target を満たす s を Newton 法で解く"""
    s=0.0
    for _ in range(200):
        f=0.0; fp=0.0
        for a in A:
            z=1.0/(1.0+math.exp(-s*a)); f+=a*z; fp+=a*a*z*(1-z)
        d=(f-target)/fp; s-=d
        if abs(d)<1e-15: break
    return s
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
    dev={r:((g(ns[r])+extra[r])/g(ns[r]))/G-1.0 for r in rhos}
    w={r: -tilt(A, ns[r])*A[-1] for r in rhos}     # ρ<1/2 では s<0 なので符号を反転
    return dev, w, A[-1]
RHOS=[0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40]
KS=[80,120,160,180]
print("="*104)
print("【無次元の傾き w = |s|·N】  ρ とは非線形に対応する。線形近似 w≈6(1/2−ρ) との比較")
print("="*104)
print("   k   "+"".join(f"  ρ={r:.2f} " for r in RHOS))
DEV={};W={};NN={}
for k in KS:
    d,w,N=run(k,RHOS); DEV[k]=d; W[k]=w; NN[k]=N
    print(f" {k:3d}  "+"".join(f"{w[r]:8.4f} " for r in RHOS))
print("  線形 "+"".join(f"{6*(0.5-r):8.4f} " for r in RHOS)+"  ← 6(1/2−ρ)")
print()
print("="*104)
print("【F = dev·N² を w の関数として】 F/w³ が一定になるか(端の立ち上がりが直るか)")
print("="*104)
print("   k   "+"".join(f"  ρ={r:.2f} " for r in RHOS))
for k in KS:
    print(f" {k:3d}  "+"".join(f"{DEV[k][r]*NN[k]**2/W[k][r]**3:8.2f} " for r in RHOS))
print()
print("  比較: (1/2−ρ)³ で割った場合(前回の表を再掲・端で 2 倍に暴れていた)")
print("   k   "+"".join(f"  ρ={r:.2f} " for r in RHOS))
for k in KS:
    print(f" {k:3d}  "+"".join(f"{DEV[k][r]*NN[k]**2/(0.5-r)**3/1000:8.2f} " for r in RHOS)+"  (×10³)")
print()
for tag,f in (("F/w³", lambda k,r: DEV[k][r]*NN[k]**2/W[k][r]**3),
              ("F/(1/2−ρ)³", lambda k,r: DEV[k][r]*NN[k]**2/(0.5-r)**3)):
    vs=[f(k,r) for k in KS for r in RHOS]
    print(f"  {tag:12s}: 全体の max/min = {max(vs)/min(vs):6.2f}   中央値 {sorted(vs)[len(vs)//2]:.4g}")
