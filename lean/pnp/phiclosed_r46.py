# phiclosed_r46.py (2026-08-08, opus-5) : Φ_q の閉じた形の検算。
# 主張: Φ_q(x) = (1/x)∫_0^x h_q(v)dv - h_q(0),  h_q(v) = (1/φ(q))·log|Φ_q(-e^{-iv})|
#      (Φ_q は q 次の円分多項式)
# これが正しければ「Φ_q ≤ 0」は
#      「円分多項式の log|Φ_q| の、-1 から出発する走査平均が出発点で最大」
# という、部分和問題を一切含まない主張に書き換わる。
import numpy as np, math
from math import gcd
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

NM=300000; nn=np.arange(1,NM+1,dtype=float); sg=(-1.0)**(nn+1)/nn
def ReI(x): return np.where(np.abs(x)<1e-12,1.0,np.sin(x)/np.where(np.abs(x)<1e-12,1.0,x))

def h(q,v):                       # (1/φ(q)) Σ_{r⊥q} log|2cos(v/2 + πr/q)|
    ph=phi(q); s=0.0
    for r in range(1,q+1):
        if gcd(r,q)==1:
            s+=math.log(abs(2*math.cos(v/2.0+math.pi*r/q))+1e-300)
    return s/ph
def h_via_cyclo(q,v):             # (1/φ(q)) log|Φ_q(-e^{-iv})|  を根から
    ph=phi(q); z=complex(math.cos(-v),math.sin(-v)); s=0.0
    for r in range(1,q+1):
        if gcd(r,q)==1:
            zeta=complex(math.cos(2*math.pi*r/q),math.sin(2*math.pi*r/q))
            s+=math.log(abs(-z-zeta)+1e-300)
    return s/ph

print("="*104)
print("[検算] Φ_q(x) = (1/x)∫_0^x h_q(v)dv - h_q(0),  h_q(v)=(1/φ(q))log|Φ_q(-e^{-iv})|")
print("="*104)
for q in (4,6,10,12):
    ph=phi(q); cs=np.array([ram(q,n) for n in range(1,NM+1)],dtype=float)/ph
    R0=float((sg*cs).sum())
    print(f"\n--- q={q}  φ={ph}")
    print(f"    h_q(0)={h(q,0.0):+.6f}   (1/φ)log|Φ_q(-1)|={h_via_cyclo(q,0.0):+.6f}   "
          f"級数の R_q(0)={R0:+.6f}   [3つ一致すべき]")
    print("      x        Φ_q(x)(級数)     Φ_q(x)(閉形式)     差")
    for x in (0.5,1.5,3.0,8.0,20.0,60.0):
        Ph_series=float((sg*cs*ReI(nn*x)).sum())-R0
        m=200000; vs=np.linspace(0.0,x,m+1)
        hv=np.array([h(q,v) for v in vs])
        Ph_closed=float(np.trapezoid(hv,vs))/x - h(q,0.0)
        print(f"    {x:6.2f}    {Ph_series:+.6f}       {Ph_closed:+.6f}      {Ph_series-Ph_closed:+.2e}")
print()
print("  ※ 一致すれば、Problem 10.3 は次の主張に等価:")
print("     『(1/x)∫_0^x log|Φ_q(-e^{-iv})| dv ≤ log|Φ_q(-1)|  (∀x>0)』")
print("     Jensen より円全体の平均は 0(Mahler 測度 1)なので、走査平均は")
print("     log|Φ_q(-1)| から 0 へ単調に落ちる、という形の主張になる。")
