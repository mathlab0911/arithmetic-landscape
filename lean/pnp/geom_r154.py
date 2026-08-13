"""
r154 -- hunting the counterexample the correction formula points at.

rem:correctionH settled prob:hrate for clean powers: distinctness forces sigma^2 ~ k^3
while Q(0) ~ k^{3(1-alpha)}, so the ratio is k^{-3alpha} -> 0 for every alpha > 0.  The
formula also says where to look for failure: Q(0)/sigma^2 must be forced UP, and that needs
a family growing faster than any power, so that the top layer's delta_d^2 (of order a_k^2)
beats sigma^2 (of order a_k^2 / 4) without the 2^{-N_d} damping catching it.

Geometric family a_i = 2^i + 1 (odd, distinct, and NOT super-increasing beyond i = 3, so
the subset sums genuinely overlap and r > 1 at many targets).

If lm/r fails to approach Gamma here, that is the first profile where the annealed count is
provably wrong -- which the paper itself says is worth more than a proof of the conjecture.
"""
import numpy as np

def subset_counts(A):
    T=sum(A); dp=np.zeros(T+1); dp[0]=1.0
    for a in A: dp[a:] += dp[:-a]
    return dp

def lm_profile(A):
    """lm and r for every target.

    N_d is constant on blocks of d, so within a block the layer contributes a SLIDING SUM
    of the tail counts -- computable from a prefix sum in O(T) per block instead of O(T)
    per value of d.  For the odd numbers M = 2k and the difference is cosmetic; for a
    geometric family M is exponential in k and the naive loop does not finish.
    """
    A=sorted(A); T=sum(A); M=A[-1]; k=len(A)
    r=subset_counts(A); lm=r.copy()
    pref=[0]*(k+1)
    for i,a in enumerate(A): pref[i+1]=pref[i]+a
    n=np.arange(T+1)
    dmax=(M-1)//2
    bounds=[]                          # (d0, d1, j) blocks on which N_d = j
    d0=1; j=0
    while d0<=dmax:
        while j<k and A[j]<=2*d0: j+=1
        d1 = dmax if j>=k else min(dmax, (A[j]-1)//2)
        bounds.append((d0,d1,j)); d0=d1+1
    for d0,d1,j in bounds:
        cnt = subset_counts(A[j:]) if j<k else np.array([1.0])
        C = np.concatenate(([0.0], np.cumsum(cnt)))       # C[i] = sum of cnt[:i]
        L = len(cnt)
        def block(lo, hi):                                 # sum cnt[lo..hi], clipped
            lo=np.clip(lo,0,L); hi=np.clip(hi+1,0,L)
            return C[hi]-C[lo]
        lm += block(n+d0, n+d1)
        lm += block(n-d1-pref[j], n-d0-pref[j])
    return r,lm

def gamma_Q_sigma(A):
    A=sorted(A); M=A[-1]; k=len(A)
    pref=[0]*(k+1); pref2=[0]*(k+1)
    for i,a in enumerate(A): pref[i+1]=pref[i]+a; pref2[i+1]=pref2[i]+a*a
    sig2=pref2[k]/4.0; G=1.0; S=0.0; j=0
    for d in range(1,(M-1)//2+1):
        while j<k and A[j]<=2*d: j+=1
        w=2.0**-j; G+=2*w; S+=w*((d+pref[j]/2.0)**2 - pref2[j]/4.0)
    return G, S/G, sig2

print("="*104)
print("geometric family a_i = 2^i + 1 : does lm/r still approach Gamma?")
print("="*104)
print(f"  {'k':>3s} {'max':>7s} {'T':>8s} {'Gamma':>12s} {'Q(0)':>13s} {'sigma^2':>13s}"
      f" {'Q/sigma^2':>11s} {'occ':>7s} {'lm/r':>12s} {'lm/r / Gamma':>13s}")
for k in range(6, 19):
    A=[2**i+1 for i in range(1,k+1)]
    T=sum(A)
    if T > 3_000_000: break
    r,lm=lm_profile(A); mu=T/2.0
    G,Q,s2=gamma_Q_sigma(A)
    c=int(round(mu)); w=slice(max(0,c-20), c+21)
    rr,ll=r[w],lm[w]; occ=int((rr>0).sum())
    if rr.sum()<=0:
        print(f"  {k:3d} {A[-1]:7d} {T:8d} {G:12.5f} {Q:13.3f} {s2:13.1f} {Q/s2:11.4f}"
              f" {f'{occ}/41':>7s}   window empty")
        continue
    val=float(ll.sum()/rr.sum())
    print(f"  {k:3d} {A[-1]:7d} {T:8d} {G:12.5f} {Q:13.3f} {s2:13.1f} {Q/s2:11.4f}"
          f" {f'{occ}/41':>7s} {val:12.5f} {val/G:13.5f}")
print()
print("  Q/sigma^2 is the predicted relative error.  Where it is of order 1 the expansion")
print("  has no business being accurate, and the question is whether lm/r/Gamma leaves 1.")

print()
print("="*104)
print("CONTROL 1: brute force.  Enumerate all 2^k subsets and count strict local minima")
print("directly from the definition, for the same family.  The DP must agree exactly.")
print("="*104)
from itertools import combinations
def brute_lm_r(A, n):
    lm=r=0
    k=len(A)
    for mask in range(1<<k):
        S=[A[i] for i in range(k) if mask>>i & 1]
        s=sum(S); D=abs(s-n)
        if D==0: r+=1
        ok=True
        for i in range(k):
            t=s-A[i] if (mask>>i & 1) else s+A[i]
            if abs(t-n)<=D: ok=False; break
        if ok: lm+=1
    return lm,r
for k in (8,10,12):
    A=[2**i+1 for i in range(1,k+1)]; T=sum(A); c=T//2
    r,lm=lm_profile(A)
    bad=0; checked=0
    for n in range(c-6, c+7):
        bl,br = brute_lm_r(A,n)
        if br==0: continue
        checked+=1
        if bl!=round(lm[n]) or br!=round(r[n]): bad+=1
    print(f"  k={k:3d}: {checked} targets with r>0 compared, {bad} disagreements with brute force")

print()
print("="*104)
print("CONTROL 2: several target regions, not just the centre, and a second family")
print("="*104)
for label, gen in (("a_i = 2^i + 1", lambda i: 2**i+1),
                   ("a_i = 2^i - 1", lambda i: 2**i-1),
                   ("a_i = 3^i + 2*(i%2)", lambda i: 3**i + 2*(i%2))):
    print(f"\n  {label}")
    print(f"    {'k':>3s} {'Gamma':>9s} {'lm/r @z=0':>11s} {'@z=0.5':>10s} {'@z=1':>10s}"
          f" {'@z=1.5':>10s} {'ratio z=0':>10s}")
    for k in (8, 11, 14):
        A=sorted(set(a for a in (gen(i) for i in range(1,k+1)) if a%2==1))
        if len(A)<k or sum(A)>3_000_000: continue
        r,lm=lm_profile(A); T=sum(A); G,Q,s2=gamma_Q_sigma(A); sig=np.sqrt(s2); mu=T/2.0
        vals=[]
        for z in (0,0.5,1.0,1.5):
            n=int(round(mu+z*sig)); w=slice(max(0,n-20),n+21)
            rr,ll=r[w],lm[w]
            vals.append(float(ll.sum()/rr.sum()) if rr.sum()>0 else float('nan'))
        print(f"    {k:3d} {G:9.4f} {vals[0]:11.4f} {vals[1]:10.4f} {vals[2]:10.4f}"
              f" {vals[3]:10.4f} {vals[0]/G:10.4f}")
