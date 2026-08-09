# e2a5_r74.py  【データ崩壊(collapse)テスト】補正の自然な変数は何か。
#  候補: u1=(1/2−ρ)/N (小さい元が感じる傾き)  u2=(1/2−ρ)√k (z値)  u3=(1/2−ρ)/k
#  正しい変数なら dev/(u^α) が k と ρ の両方について一定になるはず。
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
    return {r:((g(ns[r])+extra[r])/g(ns[r]))/G-1.0 for r in rhos}, A[-1], T, sum(a*a for a in A)

RHOS=[0.10,0.15,0.20,0.25,0.30,0.35]
KS=[60,80,100,120,140,160]
D={}; META={}
for k in KS:
    d,N,T,S2 = run(k,RHOS); D[k]=d; META[k]=(N,T,S2)
print("="*108)
print("【E2a-5 データ崩壊テスト】どの変数で書けば k 依存が消えるか")
print("="*108)
cands = [
  ("dev·N²/(1/2−ρ)²   [傾き (1/2−ρ)/N]", lambda k,r: D[k][r]*META[k][0]**2/(0.5-r)**2),
  ("dev·k²/(1/2−ρ)²   [(1/2−ρ)/k]",      lambda k,r: D[k][r]*k**2/(0.5-r)**2),
  ("dev/((1/2−ρ)²k)   [z値 z²=3k(..)²]", lambda k,r: D[k][r]/((0.5-r)**2*k)),
  ("dev·(T/S2)^-2/(1/2−ρ)² [s=4(..)T/S2]",lambda k,r: D[k][r]/((0.5-r)**2*(META[k][1]/META[k][2])**2)),
]
for name,f in cands:
    print(f"\n  ■ {name}")
    print("     k  " + "".join(f"  ρ={r:.2f}   " for r in RHOS) + "   列内変動(max/min)")
    allv=[]
    for k in KS:
        vs=[f(k,r) for r in RHOS]; allv+=vs
        print(f"   {k:3d}  "+"".join(f"{v:9.3g} " for v in vs)+f"   {max(vs)/min(vs):8.2f}")
    print(f"     ⇒ 全体の max/min = {max(allv)/min(allv):8.2f}   "
          f"{'★崩壊している(良い変数)' if max(allv)/min(allv)<3 else '崩壊せず'}")
print()
print("="*108)
print("【最も良い変数での定数】")
print("="*108)
best=min(cands, key=lambda c: max(c[1](k,r) for k in KS for r in RHOS)/min(c[1](k,r) for k in KS for r in RHOS))
print(f"  {best[0]}")
vs=[best[1](k,r) for k in KS for r in RHOS]
print(f"  値の範囲: {min(vs):.4g} 〜 {max(vs):.4g}   中央値 {sorted(vs)[len(vs)//2]:.4g}")
