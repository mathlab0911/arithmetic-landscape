# q0c_r082.py  The one decision-relevant question: does the residual dev_meas - dev_(*) shrink
#   with k (finite-size) or stay put (a missing term in the derivation)?
import numpy as np, math
from fractions import Fraction
def odd_primes(k):
    out=[]; n=3
    while len(out)<k:
        if all(n%p for p in range(3,int(n**0.5)+1,2)): out.append(n)
        n+=2
    return out
ENS={"odds":lambda k:[2*i+1 for i in range(k)], "primes":odd_primes}
def measured(A,rhos):
    A=sorted(A);k=len(A);T=sum(A);S2=sum(a*a for a in A);D=(A[-1]-1)//2
    ns={r:int(r*T) for r in rhos}
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
    return {r:(g(ns[r])+ex[r])/g(ns[r]) for r in ns},T,S2
def predict(A,u):
    A=sorted(A);k=len(A);T=sum(A);S2=sum(a*a for a in A);V=S2/4.0;D=(A[-1]-1)//2
    tot=1.0;j=0;sig=0
    for d in range(1,D+1):
        while j<k and A[j]<=2*d: sig+=A[j]; j+=1
        w=2.0**(-j)
        if w<1e-18: break
        delta=d+sig/2.0; arg=u*delta/V
        if arg>700: break
        tot+=w*math.exp(-delta*delta/(2*V))*2*math.cosh(arg)
    return tot
RH=[0.40,0.30,0.20]
print("="*108)
print("Residual  D(x) := dev_measured - dev_(*)   as a function of k.  Shrinking => finite size.")
print("="*108)
for nm,f in ENS.items():
    print(f"\n  ### {nm}")
    print("      k    " + "".join(f"    x={0.5-r:.2f}        " for r in RH))
    print("           " + "".join("   D(x)      D/lam^2 " for r in RH))
    for k in (60,100,140,180,220):
        A=sorted(f(k)); meas,T,S2=measured(A,RH); V=S2/4.0
        G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
        cells=[]
        for r in RH:
            n=int(r*T); u=T/2.0-n; lam=u/V
            dm=meas[r]/G-1.0; dp_=predict(A,u)/G-1.0; D=dm-dp_
            cells.append(f" {D:+9.2e} {D/lam**2:+9.2f} ")
        print(f"   {k:4d}   "+"".join(cells))
print()
print("  If D/lambda^2 is roughly k-independent, the missing term scales the same way as the")
print("  signal and is a structural omission; if it decays, it is a finite-size effect.")
print()
print("="*108)
print("Cube arm (item 3): partial sums of (**) -- the explanation of the r080 failure")
print("="*108)
A=sorted(set(2*((i**3)//2)+1 for i in range(1,71))); k=len(A); S2=sum(a*a for a in A); V=S2/4.0
G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
j=0;sig=0;acc=0.0;marks=[1,2,4,8,16,32,64,128,256,1024,4096,16384,65536,171500]
D=(A[-1]-1)//2
for d in range(1,D+1):
    while j<k and A[j]<=2*d: sig+=A[j]; j+=1
    acc += 2.0**(-j)*(d+sig/2.0)**2
    if d in marks: print(f"   d <= {d:7d}:  N_d={j:2d}  sigma_d={sig:9d}  partial SUM = {acc:16.1f}   Q(0) so far = {acc/G:14.1f}")
print(f"\n   final Q(0)_cubes = {acc/G:.1f}   (odds 23.2, primes 57.0, squares 1022)")
print("   the series does not converge in any useful sense at k=70 -- N_d stays tiny for a long time,")
print("   so 2^{-N_d} never damps the growing delta_d^2. That is exactly the starvation seen in r080.")
