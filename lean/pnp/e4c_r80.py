# e4c_r80.py  Why does the cube arm blow up? Check the PRIOR question: does lm/deg -> Gamma
#   hold at all for that profile? If the base law fails, the lambda^2 test on it is vacuous.
import numpy as np, math
from fractions import Fraction
def odd_primes(k):
    out=[]; n=3
    while len(out)<k:
        if all(n%p for p in range(3,int(n**0.5)+1,2)): out.append(n)
        n+=2
    return out
S={"odds  a_i=2i-1":       lambda k: [2*i+1 for i in range(k)],
   "squares ~i^2":         lambda k: sorted(set(2*((i*i)//2)+1 for i in range(1,k+1))),
   "cubes ~i^3":           lambda k: sorted(set(2*((i**3)//2)+1 for i in range(1,k+1))),
   "primes":               odd_primes}
def lm_deg(A,n):
    A=sorted(A); k=len(A); T=sum(A); D=(A[-1]-1)//2
    dp=np.zeros(1); dp[0]=1.0; cur=k; extra=0.0
    g=lambda m: dp[m] if 0<=m<len(dp) else 0.0
    for d in range(D,0,-1):
        j=0
        while j<k and A[j]<=2*d: j+=1
        while cur>j:
            cur-=1; a=A[cur]; new=np.zeros(len(dp)+a); new[:len(dp)]=dp; new[a:a+len(dp)]+=dp; dp=new
        extra += g(n+d)+g(T-n+d)
    while cur>0:
        cur-=1; a=A[cur]; new=np.zeros(len(dp)+a); new[:len(dp)]=dp; new[a:a+len(dp)]+=dp; dp=new
    return g(n)+extra, g(n)
print("="*104)
print("Does lm/deg -> Gamma hold AT THE CENTRE (rho=1/2) for each profile?  dev = (lm/deg)/Gamma - 1")
print("="*104)
print(f"  {'profile':<20}" + "".join(f"    k={k:<5d}" for k in (20,30,40,50,60,70)) + "     Gamma")
for nm,f in S.items():
    row=[]
    for k in (20,30,40,50,60,70):
        A=sorted(f(k)); T=sum(A); n=T//2
        G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
        lm,deg=lm_deg(A,n)
        row.append((lm/deg)/G-1.0 if deg>=1e4 else float('nan'))
    print(f"  {nm:<20}"+"".join(f" {v:+10.3e}" for v in row)+f"   {G:8.3f}")
print()
print("  interpretation: for the lambda^2 law to be testable on a profile, dev at the centre")
print("  must already be ~0. If it is not, Gamma itself is not the limit for that profile.")
print()
print("="*104)
print("How many elements are 'small'? N_A(d)=#{a<=2d} at d=2,5,10 -- the quantity the")
print("classification theorem actually sees. A profile with too few small elements has no flatness.")
print("="*104)
print(f"  {'profile':<20}  k=40: N(2) N(5) N(10)     k=70: N(2) N(5) N(10)     largest element")
for nm,f in S.items():
    out=[]
    for k in (40,70):
        A=sorted(f(k)); out.append([sum(1 for a in A if a<=2*d) for d in (2,5,10)])
    A=sorted(f(70))
    print(f"  {nm:<20}      {out[0][0]:3d} {out[0][1]:4d} {out[0][2]:5d}          {out[1][0]:3d} {out[1][1]:4d} {out[1][2]:5d}         {A[-1]}")
