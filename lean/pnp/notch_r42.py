# notch_r42.py (2026-08-08, opus-5 42周目) : fable-5 r41 の決定的テスト。
# q=10 の切れ込みの脇の高さ(r40 実測: -0.393/-0.379/-0.355)が Lemma 8.0' の式から出るか。
#
# 予言: 5 は 10 と互いに素でないので剰余類分解から外れる。よって
#   (1/b)log|G(2π/10+t)| = (1/b)log|sin(5t/2)| + ((b-1)/b)[ log M(10) + Φ₁₀(Nt) ]
# ここで Φ₁₀ は q=6 と同じ作り(Ramanujan和 c₁₀(n)/φ(10) × 窓 W、B'=B\{5} で厳密計算)。
# 脇の局所最大を予言側で求め、実測と比べる。自由パラメータなし。
import numpy as np, math
from math import gcd
def primes_upto(n):
    s=np.ones(n+1,bool); s[:2]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]: s[i*i::i]=False
    return np.nonzero(s)[0]
PR=primes_upto(200000)
def mobius(n):
    r=1;m=n
    for p in range(2,int(n**0.5)+1):
        if m%p==0:
            m//=p
            if m%p==0: return 0
            r=-r
    if m>1: r=-r
    return r
def ram(q,n):
    g=gcd(n,q); return sum(d*mobius(q//d) for d in range(1,g+1) if g%d==0)
def phi(q): return sum(1 for a in range(1,q+1) if gcd(a,q)==1)
def M(q):
    t=0.0;c=0
    for a in range(1,q):
        if gcd(a,q)==1:
            t+=math.log(abs(1+complex(math.cos(2*math.pi*a/q),math.sin(2*math.pi*a/q))));c+=1
    return 0.5*math.exp(t/c)

NMAX=4000; q=10; ph=phi(q); lM=math.log(M(q))
coef=np.array([((-1.0)**(n+1)/n)*ram(q,n)/ph for n in range(1,NMAX+1)])
nn=np.arange(1,NMAX+1,dtype=np.float64)

print("="*100)
print("[決定的テスト] q=10 の切れ込みの脇の高さ — Lemma 8.0' の式から出るか")
print("  予言 = (1/b)log|sin(5t/2)| + ((b-1)/b)[log M(10) + Φ₁₀(Nt)]   (自由パラメータなし)")
print(f"  log M(10) = {lM:+.5f}")
print("="*100)
print("   k    b     実測の脇の高さ   予言の脇の高さ    差      | −(3/2)log b/b | log M(10)+その")
for k in (40,60,100,140):
    A=PR[PR%2==1][:k]; B=A[A>4].astype(np.float64); b=len(B); N=float(B.max())
    Bp=B[B!=5.0]                                   # B' = B \ {5}
    def Phi(ts):
        out=np.zeros(len(ts))
        for i,t in enumerate(ts):
            W=np.cos(np.outer(nn*t,Bp)).sum(axis=1)/len(Bp)
            out[i]=float((coef*W).sum())
        W0=np.cos(np.outer(nn*0.0,Bp)).sum(axis=1)/len(Bp)
        return out-float((coef*W0).sum())          # Φ(0)=0 に正規化
    c=2*math.pi/q
    xs=np.linspace(0.02,3.0,150); ts=xs/N
    # 実測
    meas=np.zeros(len(ts))
    for i0 in range(0,b,40):
        meas+=np.log(np.abs(np.cos(np.outer(B[i0:i0+40],c+ts)/2.0))+1e-300).sum(axis=0)
    meas/=b
    # 予言
    pred=(np.log(np.abs(np.sin(5*ts/2.0))))/b + ((b-1)/b)*(lM+Phi(ts))
    im, ip = int(np.argmax(meas)), int(np.argmax(pred))
    law=-1.5*math.log(b)/b
    print(f"  {k:3d} {b:4d}      {meas[im]:+.5f}        {pred[ip]:+.5f}     {meas[im]-pred[ip]:+.5f}"
          f" |   {law:+.5f}    |  {lM+law:+.5f}")
print()
print("  ※ 実測の脇の高さは r40 の peakscan(600万点)と独立に、この掃引で再計算している(V2-b)")
