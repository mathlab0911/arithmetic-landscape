# q0g_r084.py  Both suspects are dead (lambda_d^eff = lambda_true for every d), so the factor is
#   NOT in the slope. It must be in the magnitude P_d.  Candidate, derived:
#     P_d/r_B(n) = 2^{-N_d} sqrt(V/V_d) exp(-delta^2/2V_d) exp(u^2/2V - u^2/2V_d) 2cosh(lambda delta)
#   with V_d = (S2 - s_d)/4, s_d = SUM_{a<=2d} a^2.  The x-dependent exponential contributes
#     u^2(1/2V - 1/2V_d) = -u^2 s_d/(8V^2) = -lambda^2 s_d/8   (using u = lambda V)
#   so the coefficient of lambda^2 in the increment becomes  delta_d^2 - s_d/4,  NOT delta_d^2.
#     ==>  Q(0) = (1/Gamma) SUM 2^{-N_d} ( delta_d^2 - s_d/4 )
import numpy as np, math
from fractions import Fraction
def odd_primes(k):
    out=[]; n=3
    while len(out)<k:
        if all(n%p for p in range(3,int(n**0.5)+1,2)): out.append(n)
        n+=2
    return out
ENS={"odds":lambda k:[2*i+1 for i in range(k)],
     "squares":lambda k:sorted(set(2*((i*i)//2)+1 for i in range(1,k+1))),
     "primes":odd_primes,
     "cubes":lambda k:sorted(set(2*((i**3)//2)+1 for i in range(1,k+1)))}
def closed(A):
    A=sorted(A);k=len(A);S2=sum(a*a for a in A);D=(A[-1]-1)//2
    G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
    old=new=0.0; j=0; sig=0; s2s=0
    for d in range(1,D+1):
        while j<k and A[j]<=2*d: sig+=A[j]; s2s+=A[j]*A[j]; j+=1
        w=2.0**(-j)
        if w<1e-18: break
        de=d+sig/2.0
        old+=w*de*de; new+=w*(de*de - s2s/4.0)
    return old/G, new/G
def measure(A,rho=0.40):
    A=sorted(A);k=len(A);T=sum(A);D=(A[-1]-1)//2
    G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
    ns={rho:int(rho*T),0.5:T//2}
    dp=np.zeros(1);dp[0]=1.0;cur=k;ex={r:0.0 for r in ns}
    g=lambda m: dp[m] if 0<=m<len(dp) else 0.0
    for d in range(D,0,-1):
        j=0
        while j<k and A[j]<=2*d: j+=1
        while cur>j:
            cur-=1;a=A[cur];nw=np.zeros(len(dp)+a);nw[:len(dp)]=dp;nw[a:a+len(dp)]+=dp;dp=nw
        for r,n in ns.items(): ex[r]+=g(n+d)+g(T-n+d)
    while cur>0:
        cur-=1;a=A[cur];nw=np.zeros(len(dp)+a);nw[:len(dp)]=dp;nw[a:a+len(dp)]+=dp;dp=nw
    n=ns[rho]; lt=0.25*math.log(g(n-2)/g(n+2))
    d0=(g(ns[0.5])+ex[0.5])/g(ns[0.5])/G-1.0
    dv=(g(n)+ex[rho])/g(n)/G-1.0
    return (dv-d0)/lt**2
print("="*104)
print("THE CORRECTED CLOSED FORM:   Q(0) = (1/Gamma) SUM 2^{-N_d} ( delta_d^2 - s_d/4 )")
print("="*104)
print(f"  {'ensemble':<10} {'k':>5} {'measured':>11} {'old (delta^2)':>15} {'ratio':>8}   {'new (-s_d/4)':>14} {'ratio':>8}")
for nm,f in ENS.items():
    if nm=="cubes":
        o,nw=closed(f(70)); print(f"  {'cubes':<10} {70:>5} {'(n/a)':>11} {o:15.1f} {'—':>8}   {nw:14.1f} {'—':>8}")
        continue
    k=220 if nm in ("odds","primes") else 170
    A=sorted(f(k)); m=measure(A); o,nw=closed(A)
    print(f"  {nm:<10} {k:>5} {m:11.3f} {o:15.3f} {m/o:8.4f}   {nw:14.3f} {m/nw:8.4f}")
print()
print("="*104)
print("k-dependence of the new ratio (the old one converged to 0.873-0.882, not to 1)")
print("="*104)
print(f"  {'ensemble':<10}"+"".join(f"     k={k:<5d}" for k in (100,140,180,220)))
for nm in ("odds","squares","primes"):
    row=[]
    for k in (100,140,180,220):
        kk=170 if (nm=="squares" and k>170) else k
        A=sorted(ENS[nm](kk)); m=measure(A); o,nw=closed(A); row.append(m/nw)
    print(f"  {nm:<10}"+"".join(f"  {v:10.5f}" for v in row))
