"""
r163 -- reconciling 4 against 7 before (hrate-b) is registered (fable-5, r162 §2.3).

opus reported lm/r near 7 over 8 <= k <= 18; fable measured a median of 4.000 at
k = 10, 12, 14.  Both readings agree that the value is BOUNDED while Gamma = k+2 diverges,
but a conjecture cannot be registered on a quantity whose definition is not pinned.

Finding 1 -- the gap is a STATISTIC, not a window.
  r-weighted   sum lm / sum r   = the ratio at a typical GROUND STATE          ~ 7
  median/mean of lm(n)/r(n)     = the ratio at a typical REPRESENTABLE TARGET  ~ 4
They differ by about 1.8 because in this lacunary family lm/r is larger exactly where r is
larger, so weighting by r is not a neutral choice.

Finding 2 -- "pinned at 4.000" does not survive the range.
  median: 4.0 for k = 10..16, then 5.0, 4.5, 4.0, 5.0 at k = 17..20.
  mean:   3.89 -> 4.52 over the same range, drifting upward.
  implied effective depth D_eff moves between 2 and 4; it is not the constant 2.
So the effective-depth reading describes k <= 16 well and is not a fixed truncation.
(F26/F27: extend the range until the hypotheses are distinguishable.)
"""
import numpy as np
def subset_counts(A):
    T=sum(A); dp=np.zeros(T+1); dp[0]=1.0
    for a in A: dp[a:] += dp[:-a]
    return dp
def lm_profile(A):
    A=sorted(A); T=sum(A); M=A[-1]; k=len(A)
    r=subset_counts(A); lm=r.copy()
    pref=[0]*(k+1)
    for i,a in enumerate(A): pref[i+1]=pref[i]+a
    n=np.arange(T+1); dmax=(M-1)//2
    bounds=[]; d0=1; j=0
    while d0<=dmax:
        while j<k and A[j]<=2*d0: j+=1
        d1 = dmax if j>=k else min(dmax,(A[j]-1)//2)
        bounds.append((d0,d1,j)); d0=d1+1
    for d0,d1,j in bounds:
        cnt = subset_counts(A[j:]) if j<k else np.array([1.0])
        C=np.concatenate(([0.0],np.cumsum(cnt))); L=len(cnt)
        def blk(lo,hi):
            lo=np.clip(lo,0,L); hi=np.clip(hi+1,0,L); return C[hi]-C[lo]
        lm += blk(n+d0,n+d1)
        lm += blk(n-d1-pref[j], n-d0-pref[j])
    return r,lm
def gamma_partial(A, D):
    return 1 + 2*sum(2.0**(-sum(1 for a in A if a <= 2*d)) for d in range(1, D+1))

print("="*94)
print("does the pointwise value stay pinned at 4?  extending past fable's k <= 14")
print("="*94)
A20=[2**i+1 for i in range(1,21)]
print("  Gamma(D) partial sums:", ", ".join(f"D={D}:{gamma_partial(A20,D):.3f}" for D in (1,2,3,4,6,8)))
print()
print(f"  {'k':>3s} {'Gamma=k+2':>9s} {'median':>9s} {'mean':>8s} {'r-wtd':>8s} {'implied D_eff':>13s}")
for k in range(10, 21):
    A=[2**i+1 for i in range(1,k+1)]
    if sum(A) > 2_500_000:
        print(f"  {k:3d}  skipped (T={sum(A)})"); continue
    r,lm=lm_profile(A); T=sum(A); c=T//2
    w=slice(max(0,c-20), c+21); rr,ll=r[w],lm[w]; m=rr>0
    med=float(np.median(ll[m]/rr[m])); mean=float((ll[m]/rr[m]).mean()); rw=float(ll.sum()/rr.sum())
    Deff=None
    for D in range(1,60):
        if gamma_partial(A,D) >= med-1e-9: Deff=D; break
    print(f"  {k:3d} {k+2.0:9.1f} {med:9.4f} {mean:8.4f} {rw:8.4f} {str(Deff):>13s}")
