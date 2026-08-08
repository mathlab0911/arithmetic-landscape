# profile_r42.py (2026-08-08, opus-5 42周目) : fable-5 r41 作業1。Lemma 8.0' のプロファイル照合。
#
# 予言(自由パラメータなし)。恒等式
#   (1/b)log|G(θ)| = -log2 + Σ_n ((-1)^{n+1}/n) (1/b) Re S(n),  S(n)=Σ_{p∈B} e^{i n p θ}
# で θ = 2πj/q + t とし、剰余類分解 + 「既約類での等分布が t 振動と分離する」を仮定すると
#   (1/b) Re S(n) ≈ (c_q(n)/φ(q)) · Re W(nt),   W(x) = (1/b) Σ_{p∈B} e^{i p x}
# よって
#   P(t) := Σ_{n≤nmax} ((-1)^{n+1}/n) (c_q(n)/φ(q)) Re W(nt)
#   予言される峰からの落ち込み = P(t) - P(0)
# W は B から厳密に計算する(fable の Ĩ の平滑版を使わない)ので、
# 検証されるのは「等分布が t 振動と分離する」という核心の主張だけになる。
import numpy as np, math
from math import gcd

def primes_upto(n):
    s=np.ones(n+1,bool); s[:2]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]: s[i*i::i]=False
    return np.nonzero(s)[0]
PRIMES=primes_upto(200000)

def mobius(n):
    r=1; m=n
    for p in range(2,int(n**0.5)+1):
        if m%p==0:
            m//=p
            if m%p==0: return 0
            r=-r
    if m>1: r=-r
    return r
def ramanujan(q,n):
    g=gcd(n,q); s=0
    for d in range(1,g+1):
        if g%d==0: s+=d*mobius(q//d)
    return s
def phi(q): return sum(1 for a in range(1,q+1) if gcd(a,q)==1)

def setup(k,d=2):
    A=PRIMES[PRIMES%2==1][:k]; B=A[A>2*d].astype(np.float64)
    return B,len(B),float(B.max())

def logG(B,th):                       # 厳密な (1/b)log|G|
    return float(np.log(np.abs(np.cos(np.outer(B,th)/2.0))+1e-300).sum(axis=0)[0])/len(B) \
           if np.ndim(th)==0 else None

def logG_vec(B,ths, chunk=40):
    out=np.zeros(len(ths))
    for i in range(0,len(B),chunk):
        out+=np.log(np.abs(np.cos(np.outer(B[i:i+chunk],ths)/2.0))+1e-300).sum(axis=0)
    return out/len(B)

def P_of_t(B,q,ts,nmax):
    b=len(B); ph=phi(q)
    cs=np.array([ramanujan(q,n) for n in range(1,nmax+1)],dtype=np.float64)/ph
    sgn=np.array([(-1.0)**(n+1)/n for n in range(1,nmax+1)])
    coef=sgn*cs
    n=np.arange(1,nmax+1,dtype=np.float64)
    out=np.zeros(len(ts))
    for i,t in enumerate(ts):
        # W(nt) = (1/b) Σ_p e^{i p n t}   を n ごとに
        ang=np.outer(n*t,B)                     # nmax x b
        W=np.cos(ang).sum(axis=1)/b
        out[i]=float((coef*W).sum())
    return out

print("="*104)
print("[作業1] Lemma 8.0' のプロファイル照合 — q=6、自由パラメータなし")
print("  縦軸: 峰からの落ち込み (1/b)log|G(2π/6+t)| - (1/b)log|G(2π/6)|")
print("  比較: 予言 P(t)-P(0)   (P は Ramanujan和 c_6(n)/φ(6) × 厳密な窓 W(nt) の級数)")
print("="*104)
NMAX=4000
for k in (40,60,100,140):
    B,b,N=setup(k); q=6; c=2*math.pi/q
    xs=np.concatenate([np.linspace(0.0,6.0,25)[1:], np.linspace(7.0,40.0,12)])   # x = N t
    ts=xs/N
    meas=logG_vec(B,c+ts)-logG_vec(B,np.array([c]))[0]
    pred=P_of_t(B,q,ts,NMAX); pred=pred-P_of_t(B,q,np.array([0.0]),NMAX)[0]
    err=meas-pred
    viol=int(np.sum(meas>pred+1e-9))
    print(f"\n--- k={k} b={b} N={N:.0f}  nmax={NMAX}")
    print("      x=Nt    実測落ち込み   予言        差(実測-予言)")
    for i in range(0,len(xs),3):
        print(f"    {xs[i]:7.2f}   {meas[i]:+.5f}    {pred[i]:+.5f}    {err[i]:+.5f}")
    print(f"    → 最大絶対誤差 {np.abs(err).max():.5f} / RMS {np.sqrt((err**2).mean()):.5f}"
          f" / 予言が上界を破った点 {viol}/{len(xs)}")
