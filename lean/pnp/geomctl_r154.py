import numpy as np
from itertools import combinations
exec(open('geom_r154.py').read().split('print("="*104)')[0])

print("CONTROL 1: brute force against the DP, same family")
for k in (8,10,12):
    A=[2**i+1 for i in range(1,k+1)]; T=sum(A); c=T//2
    r,lm=lm_profile(A)
    bad=0; checked=0
    for n in range(c-5, c+6):
        lmb=rb=0
        for mask in range(1<<k):
            s=sum(A[i] for i in range(k) if mask>>i & 1); D=abs(s-n)
            if D==0: rb+=1
            ok=True
            for i in range(k):
                t=s-A[i] if (mask>>i & 1) else s+A[i]
                if abs(t-n)<=D: ok=False; break
            if ok: lmb+=1
        if rb==0: continue
        checked+=1
        if lmb!=round(lm[n]) or rb!=round(r[n]): bad+=1
    print(f"  k={k:3d}: {checked} targets with r>0, {bad} disagreements")

print()
print("CONTROL 2: other targets and a second family")
for label, gen in (("a_i = 2^i + 1", lambda i: 2**i+1), ("a_i = 2^i - 1", lambda i: 2**i-1)):
    print(f"\n  {label}")
    print(f"    {'k':>3s} {'Gamma':>9s} {'z=0':>10s} {'z=0.5':>10s} {'z=1':>10s} {'z=1.5':>10s} {'z=0 / Gamma':>12s}")
    for k in (8, 11, 14, 17):
        A=sorted(set(a for a in (gen(i) for i in range(1,k+1)) if a%2==1))
        if len(A)<k or sum(A)>600_000: continue
        r,lm=lm_profile(A); T=sum(A); G,Q,s2=gamma_Q_sigma(A); sig=np.sqrt(s2); mu=T/2.0
        vals=[]
        for z in (0,0.5,1.0,1.5):
            n=int(round(mu+z*sig)); w=slice(max(0,n-20),n+21)
            rr,ll=r[w],lm[w]
            vals.append(float(ll.sum()/rr.sum()) if rr.sum()>0 else float('nan'))
        print(f"    {k:3d} {G:9.4f} {vals[0]:10.4f} {vals[1]:10.4f} {vals[2]:10.4f} {vals[3]:10.4f} {vals[0]/G:12.4f}")
