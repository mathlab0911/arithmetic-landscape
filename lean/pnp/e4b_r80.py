# e4b_r80.py  E4 redone at k where the test can actually discriminate.
#   r78 already showed Qhat for primes only settles at k >~ 100. k=16..40 was an order of
#   magnitude too small; the spec (and my execution of it) contradicted our own data.
#   Switch to float64 DP (validated against exact int64) so that large k is reachable.
import numpy as np, random, math, time
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

def lm_deg(A, ns, dt=np.float64):
    A=sorted(A); k=len(A); T=sum(A); D=(A[-1]-1)//2
    dp=np.zeros(1,dtype=dt); dp[0]=1; cur=k
    extra={n:0.0 for n in ns}
    def g(m): return dp[m] if 0<=m<len(dp) else dt(0)
    for d in range(D,0,-1):
        j=0
        while j<k and A[j]<=2*d: j+=1
        while cur>j:
            cur-=1; a=A[cur]
            new=np.zeros(len(dp)+a,dtype=dt); new[:len(dp)]=dp; new[a:a+len(dp)]+=dp; dp=new
        for n in ns: extra[n]+= float(g(n+d))+float(g(T-n+d))
    while cur>0:
        cur-=1; a=A[cur]
        new=np.zeros(len(dp)+a,dtype=dt); new[:len(dp)]=dp; new[a:a+len(dp)]+=dp; dp=new
    return {n:(float(g(n))+extra[n], float(g(n))) for n in ns}

print("="*100); print("VALIDATION: float64 DP vs exact int64 DP (k=40, primes and cubes)"); print("="*100)
for nm,f in (("primes",odd_primes),("cubes",seq_cubes),("odds",seq_odds)):
    A=sorted(f(40)); T=sum(A); ns=[int(0.30*T)]
    a=lm_deg(A,ns,np.int64); b=lm_deg(A,ns,np.float64)
    ra=a[ns[0]][0]/a[ns[0]][1]; rb=b[ns[0]][0]/b[ns[0]][1]
    print(f"  {nm:8s}: lm/deg exact={ra:.12f}  float={rb:.12f}   rel.diff={abs(ra-rb)/ra:.2e}")
print()
print("="*112)
print("E4 (redone): Qhat_ens = dev/lambda_ens^2 at k where the ripple has cleared")
print("="*112)
RHOS=[0.30,0.35,0.40]
PLAN={"odds 1,3,..":            (seq_odds,  [60,100,140,180,220]),
      "cubes ~i^3":             (seq_cubes, [30,40,50,60,70]),
      "primes":                 (odd_primes,[60,100,140,180,220]),
      "random odd (med 3 seed)":(None,      [60,100,140,180,220])}
for name,(f,KS) in PLAN.items():
    print(f"\n  ### {name}")
    print("      x = 1/2-rho:"+"".join(f"    {0.5-r:.2f}   " for r in RHOS)+"    Gamma    (4T/S2)N   time")
    store={}
    for k in KS:
        t0=time.time()
        if f is None:
            qs=[]
            for sd in (1,2,3):
                A=sorted(seq_rand(k,sd)); T=sum(A); S2=sum(a*a for a in A); N=A[-1]
                G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
                ns=[int(r*T) for r in RHOS]; res=lm_deg(A,ns)
                qs.append([( (res[n][0]/res[n][1])/G-1.0 )/(((T/2.0-n)/(S2/4.0))**2)
                           if res[n][1]>=1e4 else None for r,n in zip(RHOS,ns)])
            row=[sorted(v[i] for v in qs if v[i] is not None) for i in range(len(RHOS))]
            cells=[]; 
            for i,c in enumerate(row):
                if len(c)<2: cells.append("   ---    "); store[(k,RHOS[i])]=None
                else: m=c[len(c)//2]; store[(k,RHOS[i])]=m; cells.append(f"{m:9.2f} ")
            print(f"   k={k:4d} "+"".join(cells)+f"   (3 seeds, median)      ({time.time()-t0:.1f}s)")
            continue
        A=sorted(f(k)); T=sum(A); S2=sum(a*a for a in A); N=A[-1]
        G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
        ns=[int(r*T) for r in RHOS]; res=lm_deg(A,ns)
        cells=[]
        for r,n in zip(RHOS,ns):
            lm,deg=res[n]
            if deg<1e4: cells.append("   ---    "); store[(k,r)]=None; continue
            q=((lm/deg)/G-1.0)/(((T/2.0-n)/(S2/4.0))**2); store[(k,r)]=q; cells.append(f"{q:9.2f} ")
        print(f"   k={k:4d} "+"".join(cells)+f"  {G:8.3f}  {4*T*N/S2:7.3f}   ({time.time()-t0:.1f}s)")
    print("      k-stability (max/min over the two largest k):")
    out=[]
    for r in RHOS:
        vs=[store[(k,r)] for k in KS[-3:] if store.get((k,r)) is not None]
        out.append(f"{max(vs)/min(vs):9.2f} " if len(vs)>=2 and min(vs)>0 else "    ---   ")
    print("             "+"".join(out))
