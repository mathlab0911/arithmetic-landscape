# e4_r80.py (2026-08-09, opus-5 80th round) E4 cross-ensemble test.
#   Prediction to be falsified: (4T/S2)*N -> 6 for odds/primes/random, -> 7 for cubes.
#   General: for a profile a_i ~ i^alpha, 4TN/S2 -> 4(2alpha+1)/(alpha+1).
#   Then: does Qhat_ens = dev / lambda_ens^2 collapse in k WITHIN each ensemble?
import numpy as np, random, math
from fractions import Fraction

def odd_primes(k):
    out=[]; n=3
    while len(out)<k:
        if all(n%p for p in range(3,int(n**0.5)+1,2)): out.append(n)
        n+=2
    return out
def seq_odds(k):  return [2*i+1 for i in range(k)]
def seq_cubes(k): return sorted(set(2*((i**3)//2)+1 for i in range(1,k+1)))
def seq_rand(k,seed):
    random.seed(seed); P=odd_primes(k)
    return sorted(random.sample(range(1,P[-1]+2,2), k))

def lm_deg(A, ns):
    """exact int64 DP (safe while 2^k < 9.2e18, i.e. k <= 62).
       lm(n) = deg(n) + sum_{d>=1} [ r_{B_d}(n+d) + r_{B_d}(T-n+d) ],  B_d = {a>2d}"""
    A=sorted(A); k=len(A); T=sum(A); D=(A[-1]-1)//2
    dp=np.zeros(1,dtype=np.int64); dp[0]=1; cur=k
    extra={n:0 for n in ns}
    def g(m): return int(dp[m]) if 0<=m<len(dp) else 0
    for d in range(D,0,-1):
        j=0
        while j<k and A[j]<=2*d: j+=1
        while cur>j:
            cur-=1; a=A[cur]
            new=np.zeros(len(dp)+a,dtype=np.int64)
            new[:len(dp)]=dp; new[a:a+len(dp)]+=dp; dp=new
        for n in ns: extra[n]+= g(n+d)+g(T-n+d)
    while cur>0:
        cur-=1; a=A[cur]
        new=np.zeros(len(dp)+a,dtype=np.int64)
        new[:len(dp)]=dp; new[a:a+len(dp)]+=dp; dp=new
    return {n:(g(n)+extra[n], g(n)) for n in ns}, T

ENS={"odds 1,3,..,2k-1": seq_odds,
     "cubes 2*floor(i^3/2)+1": seq_cubes,
     "primes 3,5,7,..": odd_primes,
     "random odd (seed 1)": lambda k: seq_rand(k,1)}
print("="*104)
print("E4 STEP 1 -- the profile-dependent prediction:  (4T/S2)*N  should be 6, 7, 6, 6")
print("="*104)
print(f"  {'ensemble':<26}"+"".join(f"  k={k:<4d}" for k in (16,24,32,40,48))+"   predicted")
for name,f in ENS.items():
    row=[]
    for k in (16,24,32,40,48):
        A=sorted(f(k)); T=sum(A); S2=sum(a*a for a in A); N=A[-1]
        row.append(4*T*N/S2)
    pred = 7 if "cubes" in name else 6
    print(f"  {name:<26}"+"".join(f" {v:7.3f}" for v in row)+f"      {pred}")
print()
print("  (for a_i ~ i^alpha the limit is 4(2a+1)/(a+1): alpha=1 -> 6, alpha=3 -> 7)")
print()
print("="*104)
print("E4 STEP 2 -- correctness checks per ensemble: reflection lm(n)=lm(T-n) must hold exactly")
print("="*104)
for name,f in ENS.items():
    ok=True; det=[]
    for k in (16,24,32):
        A=sorted(f(k)); T=sum(A); n=int(0.30*T)
        r,_=lm_deg(A,[n,T-n])
        good = r[n]==r[T-n]; ok &= good
        det.append(f"k={k}:{'OK' if good else 'FAIL'}")
    print(f"  {name:<26} "+"  ".join(det)+f"   -> {'PASS' if ok else '*** FAIL ***'}")

print()
print("="*112)
print("E4 STEP 3 -- the actual test: does Qhat_ens = dev / lambda_ens^2 collapse in k WITHIN each ensemble?")
print("   dev = (lm/deg)/Gamma(A) - 1,  lambda_ens = (T/2 - n)/V,  V = S2/4,  all from the sequence's own T,S2")
print("="*112)
import time
RHOS=[0.25,0.30,0.35,0.40]
KS=[16,20,24,28,32,36,40]
for name,f in ENS.items():
    print(f"\n  ### {name}")
    A0=sorted(f(16)); G0=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A0)))
    print(f"      x=1/2-rho:"+"".join(f"   {0.5-r:.2f}   " for r in RHOS)+"      Gamma      (4T/S2)N")
    store={}
    for k in KS:
        t0=time.time(); A=sorted(f(k)); T=sum(A); S2=sum(a*a for a in A); N=A[-1]
        G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
        ns=[int(r*T) for r in RHOS]
        res,_=lm_deg(A,ns)
        cells=[]
        for r,n in zip(RHOS,ns):
            lm,deg=res[n]
            if deg<10**4: cells.append("   ---    "); store[(k,r)]=None; continue
            dev=(lm/deg)/G-1.0; lam=(T/2.0-n)/(S2/4.0)
            q=dev/lam**2; store[(k,r)]=q; cells.append(f"{q:9.2f} ")
        print(f"   k={k:3d}  "+"".join(cells)+f"  {G:8.3f}   {4*T*N/S2:7.3f}  ({time.time()-t0:.1f}s)")
    print("      k-stability (max/min over k, using k>=24):")
    line=[]
    for r in RHOS:
        vs=[store[(k,r)] for k in KS if k>=24 and store.get((k,r)) is not None]
        line.append(f"{max(vs)/min(vs):9.2f} " if len(vs)>=3 and min(vs)>0 else "    ---   ")
    print("             "+"".join(line))
