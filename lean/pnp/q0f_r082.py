# q0f_r082.py  Final question: is the common factor ~0.876 a real constant, or does it drift to 1 with k?
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
def Qtrue(A, rho=0.40):
    A=sorted(A);k=len(A);T=sum(A);D=(A[-1]-1)//2
    G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
    ns={rho:int(rho*T), 0.5:T//2}
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
    # predicted Q(0)
    S2=sum(a*a for a in A); s=0.0; j=0; sig=0
    for d in range(1,D+1):
        while j<k and A[j]<=2*d: sig+=A[j]; j+=1
        w=2.0**(-j)
        if w<1e-18: break
        s+=w*(d+sig/2.0)**2
    return (dv-d0)/lt**2, s/G
print("="*96)
print("k-dependence of  Qhat_c(lambda_true) / Q(0)_predicted   (measured at x=0.10)")
print("="*96)
print(f"  {'ensemble':<10}"+"".join(f"    k={k:<5d}" for k in (60,100,140,180,220)))
for nm,f in ENS.items():
    row=[]
    for k in (60,100,140,180,220):
        if nm=="squares" and k>170: k=170
        try:
            q,p=Qtrue(f(k)); row.append(q/p)
        except Exception as e: row.append(float('nan'))
    print(f"  {nm:<10}"+"".join(f"  {v:9.5f}" for v in row))
print()
print("  If these sit on a constant, the mismatch is a normalisation factor to be found.")
print("  If they climb toward 1, it is finite size and (**) needs no correction.")
