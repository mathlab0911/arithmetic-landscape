# l8check_r44.py (2026-08-08, opus-5 44周目) : fable-5 r43 の作業2+自主監査。
#  (A) 8.0'(i) の誤差上界 |diff| ≤ E*(1+2πN|nt|) が数値で成立するか (n と t を振る)
#  (B) Φ_q ≤ 0 を「上界として使う」ための明示的な尾の評価が、どの x から Φ<0 を証明するか。
#      その x は L5b 包絡の到達点(x≈1.5)と繋がるか。
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
def Mq(q):
    t=0.0;c=0
    for a in range(1,q):
        if gcd(a,q)==1:
            t+=math.log(abs(1+complex(math.cos(2*math.pi*a/q),math.sin(2*math.pi*a/q))));c+=1
    return 0.5*math.exp(t/c)

print("="*104)
print("(A) 8.0'(i) の誤差上界 |T_{r,n} - (1/φ(q))Σ_p e(pnt)| ≤ E*(1 + 2πN|nt|) の数値確認")
print("    E* = sup_{u≤N} |#{p≤u,p≡r} - #{p≤u}/φ(q)|  を実測して使う")
print("="*104)
k=140; q=6; ph=phi(q)
A=PR[PR%2==1][:k]; B=A[A>4].astype(np.int64); b=len(B); N=int(B.max())
print(f"  k={k} b={b} N={N} q={q} φ(q)={ph}")
print("      r    n     x=Nt     |実測の差|    上界 E*(1+2πN|nt|)   比    判定")
worst=0.0
for r in (1,5):
    Bp=B[B%q==r]
    # E* を実測
    us=np.sort(B); F=np.cumsum((us%q==r).astype(float)); G=np.cumsum(np.ones(len(us)))
    Estar=float(np.max(np.abs(F-G/ph)))
    for n in (1,3,17,60):
        for x in (0.5,2.0,10.0):
            t=x/N
            lhs=abs(np.exp(1j*n*t*Bp).sum() - np.exp(1j*n*t*B).sum()/ph)
            ub=Estar*(1+2*math.pi*N*abs(n*t))
            ratio=lhs/ub
            worst=max(worst,ratio)
            print(f"    {r:3d} {n:4d}  {x:7.2f}   {lhs:10.4f}    {ub:14.2f}   {ratio:.4f}  "
                  f"{'OK' if ratio<=1 else '★破れ'}")
print(f"  → E*(実測) = {Estar:.3f}、最悪比 = {worst:.4f}  ⇒ "
      f"{'上界は全ケースで成立' if worst<=1 else '★上界が破れた'}")

print()
print("="*104)
print("(B) Φ_6(x) を「上界」として使うための明示的な尾の評価")
print("    Φ_q(x) = -log(2M(q)) + R(x),  R(x) = Σ_n ((-1)^{n+1}/n)(c_q(n)/φ(q)) Re Ĩ(nx)")
print("    素朴な上界: |R(x)| ≤ (q/φ(q))·(2/x)·Σ 1/n² = (q/φ(q))(π²/3)/x   (x ≥ 2)")
print("="*104)
NM=200000
cs=np.array([ram(q,n) for n in range(1,NM+1)],dtype=float)/ph
sg=np.array([(-1.0)**(n+1)/n for n in range(1,NM+1)])
nn=np.arange(1,NM+1,dtype=float)
def Itil(x):  # Re Ĩ(x) = sin x / x
    return np.where(np.abs(x)<1e-12, 1.0, np.sin(x)/np.where(np.abs(x)<1e-12,1.0,x))
lim=-math.log(2*Mq(q))
crude_c=(q/ph)*(math.pi**2/3)
print(f"  -log(2M(6)) = {lim:+.5f}   (Φ の x→∞ 極限)   素朴上界の定数 = {crude_c:.3f}")
print("      x      Φ_6(x)(級数)   |R(x)|(実測)  素朴上界 C/x   素朴上界で Φ<0 と言えるか")
xs=[1.0,1.5,2.0,2.5,4.0,8.0,16.0,36.0,72.0,120.0]
for x in xs:
    R=float((sg*cs*Itil(nn*x)).sum())
    Phi=lim*(-1)+0  # placeholder
    Phi=-lim+R if False else (R-lim)   # Φ = R - log(2M) ... 下で確認
    ok = "YES" if crude_c/x < lim else "no"
    print(f"    {x:6.1f}    {R-lim:+.5f}      {abs(R):.5f}      {crude_c/x:8.4f}      {ok}")
print()
print(f"  ⇒ 素朴上界が Φ<0 を保証するのは x > C/(-log(2M(6))) = {crude_c/lim:.1f} から。")
print(f"     L5b 包絡の到達点は x ≈ 1.5。**その間 [1.5, {crude_c/lim:.0f}] は級数の実測でしか押さえられていない。**")
