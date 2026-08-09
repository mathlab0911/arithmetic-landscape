# q0e_r082.py  Candidate for the slip: lambda is DEFINED as u/V (the Gaussian slope), but the
#   object the layers actually couple to is the TRUE local log-slope of r_B at n.
#   Measure  lambda_true = (1/2) log( r_B(n-1)/r_B(n+1) )  and redo Qhat_c with it.
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
     "primes":odd_primes}
def full(A, rhos):
    A=sorted(A);k=len(A);T=sum(A);S2=sum(a*a for a in A);V=S2/4.0;D=(A[-1]-1)//2
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
        # the sequences are all odd, so r_B is supported on one parity class: step by 2
        lt=0.5*math.log(g(n-2)/g(n+2))/2.0 if g(n-2)>0 and g(n+2)>0 else float('nan')
        out[r]=((g(n)+ex[r])/g(n), (T/2.0-n)/V, lt)
    return out,T,V
def predQ0(A):
    A=sorted(A);k=len(A);T=sum(A);S2=sum(a*a for a in A);V=S2/4.0;D=(A[-1]-1)//2
    G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
    s=0.0;j=0;sig=0
    for d in range(1,D+1):
        while j<k and A[j]<=2*d: sig+=A[j]; j+=1
        w=2.0**(-j)
        if w<1e-18: break
        s+=w*(d+sig/2.0)**2
    return s/G
RH=[0.44,0.42,0.40,0.35,0.30]
print("="*112)
print("Is the coupling variable u/V, or the TRUE local log-slope of r_B?")
print("="*112)
for nm,f in ENS.items():
    k=220 if nm in ("odds","primes") else 170
    A=sorted(f(k)); m,T,V=full(A,RH)
    G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A))); q0=predQ0(A)
    d0=m[0.5][0]/G-1.0
    print(f"\n  ### {nm}  (k={k})   predicted Q(0) = {q0:.3f}")
    print("      x    lam=u/V     lam_true    ratio    Qhat_c(u/V)  Qhat_c(true)   true/pred")
    for r in RH:
        rat,lam,lt=m[r]; x=0.5-r; dev=rat/G-1.0
        qa=(dev-d0)/lam**2; qb=(dev-d0)/lt**2
        print(f"   {x:.2f}  {lam:10.3e} {lt:10.3e}  {lt/lam:7.4f}  {qa:11.3f}  {qb:11.3f}   {qb/q0:9.5f}")
