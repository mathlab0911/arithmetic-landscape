# window_sens_r13.py — 振幅抽出の窓幅依存を調べる。
# 論文に載せた値(halfwidth=90)が安定か、それとも窓幅の artefact かを判定する。
# 予想: 窓が広いほど遠方で Gaussian 近似が劣化し、DFT が汚染される。
import math, cmath
from resid_r13 import ALLP, rep_counts, SQ

def amp(B, halfwidth, q=6):
    b=len(B); S=sum(B); V0=sum(a*a for a in B)/4.0
    r=rep_counts(B); c=S//2
    N=(2*halfwidth//q)*q
    acc=0j; used=0
    for t in range(N):
        m=c-N//2+t
        if m<0 or m>=len(r) or r[m]==0: continue
        d=m-S/2.0
        lg=b*math.log(2)-0.5*math.log(2*math.pi*V0)-d*d/(2*V0)
        acc+=(r[m]/math.exp(lg)-1.0)*cmath.exp(-2j*math.pi*m/q); used+=1
    return abs((2.0/used)*acc)

print("振幅比 = 実測 / 2(√3/2)^(b+1)   (B = 5 以上の素数, d=2)")
HW=[12,18,24,30,42,60,90,120,180,240]
print("  k   b  " + "".join(f"  hw={h:<4d}" for h in HW))
for k in range(18,33,2):
    B=[a for a in ALLP[:k] if a>4]; b=len(B)
    row=f" {k:3d} {b:3d} "
    for h in HW:
        row += f"  {amp(B,h)/(2*SQ**(b+1)):7.4f}"
    print(row)

print()
print("  σ = √V0(Gaussian の幅)との対比 — 窓が σ に対してどれくらいか")
for k in range(18,33,2):
    B=[a for a in ALLP[:k] if a>4]
    s=math.sqrt(sum(a*a for a in B)/4.0)
    print(f" {k:3d}  sigma = {s:8.2f}   hw=90 は {90/s:.3f}σ,  hw=24 は {24/s:.3f}σ")
