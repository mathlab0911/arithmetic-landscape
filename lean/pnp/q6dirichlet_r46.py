# q6dirichlet_r46.py (2026-08-08, opus-5) : 2つの確認。
#  (1) 【重大】Φ_q ≤ 0 は q=12 で偽。Jensen から構造的な理由がある(M(q)=1/2 の q すべてで偽)
#  (2) q=6 の場合、問題は Dirichlet 核の形に書き換わる:
#      Φ_6(-e^{-iv}) = 1+e^{-iv}+e^{-2iv}  ⟹ |·| = |sin(3v/2)/sin(v/2)|
#      Problem 10.3(q=6) ⟺ (1/y)∫_0^y log|sin 3u / sin u| du ≤ log 3  (∀y>0)
import numpy as np, math
from math import gcd
def phi(q): return sum(1 for a in range(1,q+1) if gcd(a,q)==1)
def Phi_at(q,z):
    p=1+0j
    for r in range(1,q+1):
        if gcd(r,q)==1:
            p*= (z-complex(math.cos(2*math.pi*r/q),math.sin(2*math.pi*r/q)))
    return p
def h(q,v): return math.log(abs(Phi_at(q,-complex(math.cos(-v),math.sin(-v))))+1e-300)/phi(q)

print("="*100)
print("(1) 【重大】M(q)=1/2 となる q では Φ_q ≤ 0 は Jensen から必ず偽")
print("    Jensen: 円全体での log|Φ_q| の平均 = 0(Mahler 測度 1)。")
print("    出発点 log|Φ_q(-1)| = 0 なら、走査平均は 0 から出て 0 に戻る ⟹ どこかで正")
print("="*100)
print("    q   |Φ_q(-1)|   M(q)      log M(q)    max_x Φ_q(x)(x≤200を掃引)   Φ_q≤0 か")
for q in (4,6,8,10,12,15,18,20,21,24):
    v0=abs(Phi_at(q,-1)); ph=phi(q); M=0.5*v0**(1.0/ph)
    xs=np.linspace(0.05,200,4000); best=-9e9; bx=0
    for x in xs:
        m=4000; vs=np.linspace(0.0,x,m+1)
        hv=np.array([h(q,v) for v in vs]) if q<0 else None
        break
    # 走査平均は累積積分で一気に
    V=200.0; m=400000; vs=np.linspace(0.0,V,m+1)
    hv=np.array([h(q,v) for v in vs])
    cum=np.concatenate([[0.0],np.cumsum((hv[1:]+hv[:-1])/2*(vs[1]-vs[0]))])
    with np.errstate(invalid='ignore',divide='ignore'):
        Phi=np.where(vs>0, cum/np.where(vs>0,vs,1.0)-hv[0], 0.0)
    mx=float(np.nanmax(Phi[1:]))
    print(f"   {q:3d}   {v0:8.4f}   {M:.5f}   {math.log(M):+.5f}      {mx:+.6f}"
          f"                {'YES' if mx<=1e-9 else '★NO(反例)'}")
print()
print("="*100)
print("(2) q=6: Φ_6(-e^{-iv}) = 1+e^{-iv}+e^{-2iv}、|·| = |sin(3v/2)/sin(v/2)| の確認")
print("="*100)
print("      v      |Φ_6(-e^{-iv})|   |sin(3v/2)/sin(v/2)|    差")
for v in (0.3,0.7,1.4,2.2,3.0):
    a=abs(Phi_at(6,-complex(math.cos(-v),math.sin(-v))))
    bq=abs(math.sin(1.5*v)/math.sin(0.5*v))
    print(f"    {v:5.2f}     {a:.8f}         {bq:.8f}        {a-bq:+.2e}")
print()
print("  ⟹ Problem 10.3 の q=6 の場合は、次と等価(部分和問題が完全に消える):")
print("     (1/y)∫_0^y log|sin 3u / sin u| du ≤ log 3   (∀ y>0)")
ys=np.linspace(0.001,60,3000)
uu=np.linspace(1e-9,60,600001)
f=np.log(np.abs(np.sin(3*uu)/np.sin(uu))+1e-300)
cum=np.concatenate([[0.0],np.cumsum((f[1:]+f[:-1])/2*(uu[1]-uu[0]))])
val=np.interp(ys,uu,cum)/ys
print(f"     数値: max over y∈(0,60] の (1/y)∫ = {val.max():.6f}   vs  log 3 = {math.log(3):.6f}"
      f"   → {'OK(超えない)' if val.max()<=math.log(3)+1e-9 else '★超過'}")
