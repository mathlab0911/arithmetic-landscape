# table1_r086.py (2026-08-09, opus-5 round 86) Paper 3, Table 1.
#   Corrected transfer function, evaluated at the MEASURED local log-slope:
#     Phi(l) = 1 + SUM_d 2^{1-N_d} exp(-l^2 s_d/8) cosh(l delta_d),  delta_d = d + sigma_d/2
#   Reported per the new rule (F: "N digits" is meaningless until you say where the signal is):
#   the residual is quoted as a FRACTION OF THE SIGNAL, both raw and centred.
import numpy as np, math
from fractions import Fraction
def odd_primes(k):
    out=[]; n=3
    while len(out)<k:
        if all(n%p for p in range(3,int(n**0.5)+1,2)): out.append(n)
        n+=2
    return out
ENS=[("odds  a_i = 2i-1", lambda k:[2*i+1 for i in range(k)], 220),
     ("squares ~ i^2",    lambda k:sorted(set(2*((i*i)//2)+1 for i in range(1,k+1))), 170),
     ("primes",           odd_primes, 220)]
def measured(A, rhos):
    A=sorted(A);k=len(A);T=sum(A);D=(A[-1]-1)//2
    ns={r:int(r*T) for r in rhos}; ns[0.5]=T//2
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
    out={}
    for r,n in ns.items():
        lt = 0.25*math.log(g(n-2)/g(n+2))
        out[r]=((g(n)+ex[r])/g(n), lt)
    return out
def Phi(A, lam):
    A=sorted(A);k=len(A);D=(A[-1]-1)//2
    tot=1.0;j=0;sig=0;s2s=0
    for d in range(1,D+1):
        while j<k and A[j]<=2*d: sig+=A[j]; s2s+=A[j]*A[j]; j+=1
        w=2.0**(1-j)
        if w<1e-18: break
        de=d+sig/2.0; arg=lam*de
        if abs(arg)>700: break
        tot += w*math.exp(-lam*lam*s2s/8.0)*math.cosh(arg)
    return tot
RH=[0.44,0.42,0.40,0.35,0.30,0.25,0.20]
print("="*118)
print("PAPER 3, TABLE 1 -- corrected transfer function against the measurement")
print("   Phi(lambda) = 1 + SUM 2^{1-N_d} exp(-lambda^2 s_d/8) cosh(lambda delta_d),  lambda = measured local log-slope")
print("="*118)
for nm,f,k in ENS:
    A=sorted(f(k)); m=measured(A,RH)
    G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
    r0,l0=m[0.5]; p0=Phi(A,l0)
    dev0_m=r0/G-1.0; dev0_p=p0/G-1.0
    print(f"\n  ### {nm}   (k={k},  Gamma = {G:.6f},  measured dev(0) = {dev0_m:+.3e})")
    print("     x     lambda      measured      Phi(lambda)    residual    | signal      resid/signal | centred signal  resid/signal")
    for r in RH:
        x=0.5-r; rm,lam=m[r]; pp=Phi(A,lam)
        res=rm-pp; sig_raw=rm-G; sig_ctr=(rm-r0)
        print(f"   {x:.2f} {lam:10.3e}  {rm:12.6f}  {pp:12.6f}  {res:+11.3e} | {sig_raw:+10.3e}  {abs(res/sig_raw)*100:9.2f}% "
              f"| {sig_ctr:+12.3e}  {abs((res-(r0-p0))/sig_ctr)*100:8.2f}%")
print()
print("="*118)
print("SUMMARY for the paper: residual as a fraction of the CENTRED signal (the quantity the theorem is about)")
print("="*118)
print(f"  {'ensemble':<18} " + "".join(f"  x={0.5-r:.2f} " for r in RH))
for nm,f,k in ENS:
    A=sorted(f(k)); m=measured(A,RH)
    G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
    r0,l0=m[0.5]; p0=Phi(A,l0)
    cells=[]
    for r in RH:
        rm,lam=m[r]; pp=Phi(A,lam)
        cells.append(f"  {abs(((rm-pp)-(r0-p0))/(rm-r0))*100:6.2f}%")
    print(f"  {nm:<18} "+"".join(cells))
print()
print("  lambda = 0 identity for the corrected Phi: the weight exp(-lambda^2 s_d/8) is 1 at lambda = 0,")
print("  so Phi(0) = 1 + SUM 2^{1-N_d} = Gamma(A) exactly -- unchanged, and it is paper 1's window identity.")
for nm,f,k in ENS:
    A=sorted(f(k)); G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
    print(f"    {nm:<18} Phi(0) = {Phi(A,0.0):.10f}   Gamma = {G:.10f}   diff = {Phi(A,0.0)-G:+.2e}")
