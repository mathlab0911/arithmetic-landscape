# c23_r76.py (2026-08-09, opus-5 76周目) fable ご指示の判別フィット
#   F(ρ) = dev·N²  を  F = c₂·x² + c₃·|x|³   (x = 1/2 − ρ) で同時フィットし、
#   c₂/c₃ と両者の k 安定性を見る。c₂ ≈ 0 なら純 |x|³(非解析的)⟹ 歪度系でなく端・最大元系。
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
    return {r:((g(ns[r])+extra[r])/g(ns[r]))/G-1.0 for r in rhos}, A[-1], {r:g(ns[r]) for r in rhos}

def fit2(xs, Fs):
    """F = c2 x² + c3 x³ の最小二乗(切片なし)"""
    S22=sum(x**4 for x in xs); S23=sum(x**5 for x in xs); S33=sum(x**6 for x in xs)
    b2=sum(F*x**2 for x,F in zip(xs,Fs)); b3=sum(F*x**3 for x,F in zip(xs,Fs))
    det=S22*S33-S23*S23
    c2=( b2*S33 - b3*S23)/det; c3=(-b2*S23 + b3*S22)/det
    pred=[c2*x**2+c3*x**3 for x in xs]
    mF=sum(Fs)/len(Fs); ss=sum((F-mF)**2 for F in Fs)
    r2=1-sum((F-p)**2 for F,p in zip(Fs,pred))/ss
    return c2,c3,r2,pred

RHOS=[0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40]
KS=[80,100,120,140,160,180]
DATA={}
for k in KS:
    dev,N,degs = run(k,RHOS); DATA[k]=(dev,N,degs)

print("="*104)
print("【判別フィット】F(ρ)=dev·N² を  F = c₂x² + c₃|x|³  (x=1/2−ρ) で同時フィット")
print("="*104)
for label,use in (("全点 ρ=0.05..0.40", RHOS), ("中央域のみ ρ=0.10..0.35", RHOS[1:-1])):
    print(f"\n  ■ {label}")
    print("     k     c₂         c₃        c₂/c₃     R²      c₂x²の寄与率(x=0.3)")
    for k in KS:
        dev,N,_=DATA[k]
        xs=[0.5-r for r in use]; Fs=[dev[r]*N*N for r in use]
        c2,c3,r2,_=fit2(xs,Fs)
        x=0.30; share=c2*x*x/(c2*x*x+c3*x**3) if (c2*x*x+c3*x**3)!=0 else float('nan')
        print(f"   {k:3d} {c2:10.1f} {c3:10.1f} {c2/c3 if c3 else float('nan'):9.4f} {r2:8.5f}   {share*100:6.1f}%")
print()
print("="*104)
print("【比較】単独モデルの当てはまり(どちらか一方だけで足りるか)")
print("="*104)
print("     k   |  純 x² のみ R²  |  純 |x|³ のみ R²  |  両方 R²")
for k in KS:
    dev,N,_=DATA[k]; use=RHOS[1:-1]
    xs=[0.5-r for r in use]; Fs=[dev[r]*N*N for r in use]
    mF=sum(Fs)/len(Fs); ss=sum((F-mF)**2 for F in Fs)
    def r2_pow(p):
        c=sum(F*x**p for x,F in zip(xs,Fs))/sum(x**(2*p) for x in xs)
        return 1-sum((F-c*x**p)**2 for x,F in zip(xs,Fs))/ss
    _,_,r2b,_=fit2(xs,Fs)
    print(f"   {k:3d}  |   {r2_pow(2):9.5f}   |    {r2_pow(3):9.5f}     |  {r2b:9.5f}")
print()
print("  【生値】F(ρ) = dev·N²(参照用)")
print("     k    N   "+"".join(f"  ρ={r:.2f} " for r in RHOS))
for k in KS:
    dev,N,_=DATA[k]
    print(f"   {k:3d} {N:5d}  "+"".join(f"{dev[r]*N*N:8.1f} " for r in RHOS))
