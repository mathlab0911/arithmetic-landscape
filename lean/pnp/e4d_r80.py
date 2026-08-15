# e4d_r80.py  Rescue: the hypothesis says dev = Q(x)*lambda^2 and lambda(0)=0, so dev(0)=0.
#   Where dev(0) has not yet converged to 0 (finite-size term dev0), the right observable is
#   the CENTRED one:  Qhat_c = (dev(x) - dev(0)) / lambda^2 .  Test all four ensembles with it.
import numpy as np, random, time
from fractions import Fraction
def odd_primes(k):
    out=[]; n=3
    while len(out)<k:
        if all(n%p for p in range(3,int(n**0.5)+1,2)): out.append(n)
        n+=2
    return out
def run(A, rhos):
    A=sorted(A); k=len(A); T=sum(A); S2=sum(a*a for a in A); D=(A[-1]-1)//2
    G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
    ns={r:int(r*T) for r in rhos}; ns[0.5]=T//2
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
    dev={}; lam={}; degs={}
    for r,n in ns.items():
        deg=g(n); degs[r]=deg
        dev[r]=((deg+extra[r])/deg)/G-1.0 if deg>0 else float('nan')
        lam[r]=(T/2.0-n)/(S2/4.0)
    return dev,lam,degs,G,4*T*A[-1]/S2
RHOS=[0.30,0.35,0.40]
PLAN=[("odds ~i",      lambda k:[2*i+1 for i in range(k)],          [100,140,180,220]),
      ("squares ~i^2", lambda k:sorted(set(2*((i*i)//2)+1 for i in range(1,k+1))), [80,110,140,170]),
      ("cubes ~i^3",   lambda k:sorted(set(2*((i**3)//2)+1 for i in range(1,k+1))),[40,50,60,70]),
      ("primes",       odd_primes,                                   [100,140,180,220])]
print("="*116)
print("E4 (centred): Qhat_c = (dev(x) - dev(0)) / lambda^2 .  Collapse in k within each ensemble?")
print("="*116)
for name,f,KS in PLAN:
    print(f"\n  ### {name}")
    print("      x:"+"".join(f"     {0.5-r:.2f}    " for r in RHOS)+"    dev(0)      (4T/S2)N   time")
    st={}
    for k in KS:
        t0=time.time(); dev,lam,degs,G,c=run(f(k),RHOS)
        cells=[]
        for r in RHOS:
            if degs[r]<1e4: cells.append("    ---    "); st[(k,r)]=None; continue
            q=(dev[r]-dev[0.5])/lam[r]**2; st[(k,r)]=q; cells.append(f"{q:10.2f} ")
        print(f"   k={k:4d} "+"".join(cells)+f" {dev[0.5]:+9.2e}   {c:6.3f}   ({time.time()-t0:.1f}s)")
    print("      k-stability over the 3 largest k (max/min):")
    o=[]
    for r in RHOS:
        vs=[st[(k,r)] for k in KS[-3:] if st.get((k,r)) is not None]
        o.append(f"{max(vs)/min(vs):10.2f} " if len(vs)>=2 and min(vs)>0 else "     ---   ")
    print("            "+"".join(o))
print()
print("="*116)
print("Reference: the UNcentred Qhat for the same runs, to show what the centring fixes")
print("="*116)
for name,f,KS in PLAN[2:3]:
    for k in KS:
        dev,lam,degs,G,c=run(f(k),RHOS)
        u=[dev[r]/lam[r]**2 if degs[r]>=1e4 else float('nan') for r in RHOS]
        cc=[(dev[r]-dev[0.5])/lam[r]**2 if degs[r]>=1e4 else float('nan') for r in RHOS]
        print(f"  {name} k={k}:  uncentred {['%.3e'%v for v in u]}   centred {['%.2f'%v for v in cc]}")
