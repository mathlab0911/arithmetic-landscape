# qhat_r78.py (2026-08-09, opus-5 78周目) 決定的テスト: 仮説 dev = Q(x)·λ² を【フィット無し】で判定
#   λ = (T/2 − n)/V,  V = S₂/4   (T, S₂ は厳密整数、n = ⌊ρT⌋)
#   仮説が正しければ Q̂ := dev/λ² は (a) k 方向でほぼ一定 (b) x→0 で正の定数 A に外挿できる
import time, math
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
    dev={r:((g(ns[r])+extra[r])/g(ns[r]))/G-1.0 for r in rhos}
    V=S2/4.0
    lam={r:(T/2.0-ns[r])/V for r in rhos}
    return dev,lam,T,S2,A[-1]

RHOS=[0.44,0.42,0.40,0.38,0.35,0.32,0.30,0.25,0.20,0.15,0.10]
KS=[100,140,180,220]
print("="*112)
print("【前提の確認】λ = 4xT/S₂ ≈ 6x/N か。 (4T/S₂)·N が k で一定なら fable の主項が正しい")
print("="*112)
print("    k     N       T          S₂            (4T/S₂)·N")
R={}
for k in KS:
    t0=time.time(); dev,lam,T,S2,N=run(k,RHOS); R[k]=(dev,lam,T,S2,N)
    print(f"  {k:4d} {N:6d} {T:9d} {S2:15d}     {4*T/S2*N:8.4f}    ({time.time()-t0:.1f}s)")
print("                                            ↑ 予言は 6")
print()
print("="*112)
print("【決定的テスト】Q̂(x,k) = dev / λ²   —— 仮説なら k 一定・x→0 で正の定数")
print("="*112)
print("     x    " + "".join(f"   k={k}  " for k in KS) + "   k方向 max/min")
for r in RHOS:
    x=0.5-r
    vals=[R[k][0][r]/R[k][1][r]**2 for k in KS]
    pos=[v for v in vals if v>0]
    mm = f"{max(pos)/min(pos):8.2f}" if len(pos)==len(vals) else "  (負あり)"
    print(f"  {x:.3f}  "+"".join(f"{v:9.1f}" for v in vals)+f"   {mm}")
print()
print("  【生の dev】(符号と大きさの確認)")
print("     x    " + "".join(f"    k={k}    " for k in KS))
for r in RHOS:
    print(f"  {0.5-r:.3f}  "+"".join(f"{R[k][0][r]:+11.3e}" for k in KS))
print()
print("="*112)
print("【x→0 の外挿】Q̂ は正の定数に落ち着くか、それとも 0 を横切るか")
print("="*112)
for k in KS:
    dev,lam,_,_,N=R[k]
    print(f"\n  k={k}: x が小さくなる向きに Q̂ を並べる")
    print("     x    :"+ "".join(f"{0.5-r:8.3f}" for r in reversed(RHOS)))
    print("     Q̂    :"+ "".join(f"{dev[r]/lam[r]**2:8.1f}" for r in reversed(RHOS)))
