# devsmooth_r18.py (2026-08-08, opus-5 13周目)
# 設計文書 paper2_l3l5_r17.md §2 の判定実験。
#   smooth_d = 2^{-N_d} [ (G(d+)+G(d-)) / <G(d_J)>_J - 2 ],  G(x)=exp(-x^2/(2 V0d))
#   d+ = d + sigma_d/2,  d_J = sigma_d/2 - sigma(J),  V0d = sum_{B_d} a^2 /4
#   DevSmooth = sum_{d>=2} smooth_d      (これを pred に足して obs に寄るか)
# さらに k=36..44 に伸ばして「多項式減衰 vs 指数減衰」で機構を判別する。
import math, cmath
from fractions import Fraction

def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
ALLP=[p for p in primes_upto(20000) if p%2==1]
Z6=cmath.exp(2j*math.pi/6); SQ=math.sqrt(3)/2

def rep_counts(B):
    tot=sum(B); r=[0]*(tot+1); r[0]=1
    for a in B:
        for m in range(tot,a-1,-1): r[m]+=r[m-a]
    return r
def rget(r,m): return r[m] if 0<=m<len(r) else 0

def full(A):
    A=sorted(A); k=len(A); T=sum(A); n=T//2
    deg=rep_counts(A)[n]
    if deg==0: return None
    D=(A[-1]-1)//2
    lm=deg; dev=0.0; devs=0.0
    for d in range(1,D+1):
        Id=[a for a in A if a<=2*d]; Bd=[a for a in A if a>2*d]
        sig=sum(Id); Nd=len(Id); bd=len(Bd)
        rB=rep_counts(Bd)
        lm += rget(rB,n+d)+rget(rB,n-d-sig)
        V0d=sum(a*a for a in Bd)/4.0
        # --- 振動部(既存の Dev) ---
        F=1+0j
        for a in Bd: F*=(1+Z6**a)
        rel=abs(F)/2.0**bd
        if rel>1e-14:
            V6=sum(a*a/(math.cos(math.pi*a/6)**2) for a in Bd)/4.0
            Ad=2.0*rel*math.sqrt(V0d/V6); ph=cmath.phase(F)
            P=1+0j
            for a in Id: P*=(1+cmath.exp(-1j*math.pi*a/3))
            z=(cmath.exp(1j*math.pi*(n+d)/3)+cmath.exp(1j*math.pi*(n-d-sig)/3)
               -2*cmath.exp(1j*math.pi*n/3)*P/2.0**Nd)
            dev += 2.0**(-Nd)*(Ad*cmath.exp(-1j*ph)*z).real
        # --- 平滑部(DevSmooth) ---
        # <G(sigma_d/2 - sigma(J))>_J は I_d の部分和分布 r_{I_d} を DP で作れば O(sum I_d)。
        # 2^{N_d} 個の J を列挙してはいけない(N_d は k まで伸びる)。
        G=lambda x: math.exp(-x*x/(2*V0d))
        dp = d + sig/2.0
        rI = rep_counts(Id) if Id else [1]
        tot = float(2**Nd)
        avg = sum(cnt*G(sig/2.0 - s) for s,cnt in enumerate(rI) if cnt)/tot
        if avg>0:
            devs += 2.0**(-Nd)*((G(dp)+G(-dp))/avg - 2.0)
    G_=sum(Fraction(a,2**(j+1)) for j,a in enumerate(A))
    W=float(G_+Fraction(A[-1],2**k))
    return dict(k=k,deg=deg,lm=lm,lmdeg=lm/deg,W=W,dev=dev,devs=devs)

print("="*112)
print("DevSmooth 判定実験: pred(振動のみ) と pred+DevSmooth を obs = lm/deg - W_D と比べる")
print("="*112)
print("  k     obs         pred(振動)   DevSmooth     pred+DS      pred/obs  (pred+DS)/obs   欠落/obs")
res=[]
for k in range(16,45,2):
    r=full(ALLP[:k])
    if r is None: continue
    obs=r["lmdeg"]-r["W"]; pred=r["dev"]; ds=r["devs"]
    res.append((k,obs,pred,ds))
    print(f" {k:3d} {obs:+11.7f} {pred:+11.7f} {ds:+11.7f} {pred+ds:+11.7f}"
          f"   {pred/obs:8.4f}     {(pred+ds)/obs:8.4f}    {(obs-pred)/obs:+8.4f}")

print()
print("  判定1: (pred+DS)/obs が pred/obs より 1 に近づけば DevSmooth が本命の欠落項。")
b1=[abs(p/o-1) for k,o,p,d in res]; b2=[abs((p+d)/o-1) for k,o,p,d in res]
print(f"          |pred/obs − 1| の平均 = {sum(b1)/len(b1):.4f}")
print(f"          |(pred+DS)/obs − 1| の平均 = {sum(b2)/len(b2):.4f}")

print()
print("  判定2: 欠落 (obs−pred) の減衰型。多項式(〜1/S2)か指数((√3/2)^b)か。")
print("  k    b_2   欠落(obs-pred)   /(√3/2)^b     ×S2         S2")
for k,o,p,d in res:
    B=[a for a in ALLP[:k] if a>4]; b=len(B); S2=sum(a*a for a in B)
    miss=o-p
    print(f" {k:3d} {b:4d}   {miss:+.6e}   {miss/(SQ**b):+.5f}   {miss*S2:+11.2f}  {S2:9d}")
print()
print("  → /(√3/2)^b が一定なら指数型(振動由来)、×S2 が一定なら多項式型(平滑由来)。")
