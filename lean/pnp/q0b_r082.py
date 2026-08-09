# q0b_r082.py  Direct test of (*) with no expansion and no extrapolation:
#   predict ratio(x) termwise and compare with the measured lm/deg.
#   Also test the refined model that keeps V_d = (S2 - s_d)/4 instead of V.
import numpy as np, math
from fractions import Fraction
def odd_primes(k):
    out=[]; n=3
    while len(out)<k:
        if all(n%p for p in range(3,int(n**0.5)+1,2)): out.append(n)
        n+=2
    return out
ENS={"odds ~i":     lambda k:[2*i+1 for i in range(k)],
     "squares ~i^2": lambda k:sorted(set(2*((i*i)//2)+1 for i in range(1,k+1))),
     "primes":       odd_primes}
def measured(A, rhos):
    A=sorted(A); k=len(A); T=sum(A); S2=sum(a*a for a in A); D=(A[-1]-1)//2
    ns={r:int(r*T) for r in rhos}
    dp=np.zeros(1); dp[0]=1.0; cur=k; extra={r:0.0 for r in ns}
    g=lambda m: dp[m] if 0<=m<len(dp) else 0.0
    for d in range(D,0,-1):
        j=0
        while j<k and A[j]<=2*d: j+=1
        while cur>j:
            cur-=1; a=A[cur]; new=np.zeros(len(dp)+a); new[:len(dp)]=dp; new[a:a+len(dp)]+=dp; dp=new
        for r,n in ns.items(): extra[r]+= g(n+d)+g(T-n+d)
    while cur>0:
        cur-=1; a=A[cur]; new=np.zeros(len(dp)+a); new[:len(dp)]=dp; new[a:a+len(dp)]+=dp; dp=new
    return {r:(g(ns[r])+extra[r])/g(ns[r]) for r in ns}, T, S2
def predict(A, u, refined):
    """(*) evaluated termwise. u = T/2 - n. refined=True keeps V_d and the sqrt prefactor."""
    A=sorted(A); k=len(A); T=sum(A); S2=sum(a*a for a in A); V=S2/4.0; D=(A[-1]-1)//2
    tot=1.0; j=0; sig=0; s2s=0
    for d in range(1,D+1):
        while j<k and A[j]<=2*d: sig+=A[j]; s2s+=A[j]*A[j]; j+=1
        w=2.0**(-j)
        if w<1e-18: break
        delta=d+sig/2.0
        Vd = (S2-s2s)/4.0 if refined else V
        pre = math.sqrt(V/Vd) if refined else 1.0
        ex  = -delta*delta/(2*Vd) + (u*u)/(2*V) - (u*u)/(2*Vd) if refined else -delta*delta/(2*V)
        arg = u*delta/Vd
        if arg>700: break
        tot += w*pre*math.exp(ex)*2*math.cosh(arg)
    return tot
print("="*112)
print("DIRECT TEST of (*) -- no expansion, no extrapolation.  measured lm/deg  vs  predicted ratio")
print("="*112)
RH=[0.44,0.42,0.40,0.35,0.30,0.25,0.20]
for nm,f in ENS.items():
    k = 220 if nm in ("odds ~i","primes") else 170
    A=sorted(f(k)); meas,T,S2=measured(A,RH); V=S2/4.0
    G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
    print(f"\n  ### {nm}  (k={k}, Gamma={G:.5f})")
    print("      x     lambda      measured      (*) plain     ratio      (*) refined   ratio")
    for r in RH:
        n=int(r*T); u=T/2.0-n; x=0.5-r; lam=u/V
        p0=predict(A,u,False); p1=predict(A,u,True); m=meas[r]
        print(f"   {x:.2f}  {lam:9.3e}  {m:12.6f}  {p0:12.6f}  {m/p0:8.5f}  {p1:12.6f}  {m/p1:8.5f}")
print()
print("="*112)
print("Same thing expressed as the centred observable, so it is comparable with r080")
print("   Qhat_c = (dev(x)-dev(0))/lambda^2,   dev = ratio/Gamma - 1")
print("="*112)
for nm,f in ENS.items():
    k = 220 if nm in ("odds ~i","primes") else 170
    A=sorted(f(k)); meas,T,S2=measured(A,RH+[0.5]); V=S2/4.0
    G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
    d0=meas[0.5]/G-1.0; p0c=predict(A,0.0,False)/G-1.0
    print(f"\n  ### {nm}   measured dev(0) = {d0:+.4e}   (*) dev(0) = {p0c:+.4e}")
    print("      x       Qhat_c measured   Qhat_c from (*)    meas/pred")
    for r in RH:
        n=int(r*T); u=T/2.0-n; x=0.5-r; lam=u/V
        qm=((meas[r]/G-1.0)-d0)/lam**2
        qp=((predict(A,u,False)/G-1.0)-p0c)/lam**2
        print(f"   {x:.2f}   {qm:15.3f}   {qp:15.3f}   {qm/qp:11.5f}")
