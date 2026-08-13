"""
r150 -- the FIRST CORRECTION to the annealed prediction, in closed form.

At the centre n = T/2, the layer at offset d contributes, by the local CLT applied to
B_d = {a > 2d} (which has m_d = k - N_d elements, half-mean mu_d, half-variance
sigma_d^2 = sigma^2 - s_d/4 where s_d = sum of a^2 over a <= 2d):

    layer_d / r  =  2^{-N_d} * (sigma/sigma_d) * exp(-delta_d^2 / (2 sigma_d^2)),
    delta_d = d + L_d/2,   L_d = sum of a over a <= 2d.

Both signs of the offset give the same delta_d at the centre, so

    lm/r  =  1 + 2 sum_d 2^{-N_d} (sigma/sigma_d) exp(-delta_d^2/(2 sigma_d^2)).

Expanding to first order in 1/sigma^2:  (sigma/sigma_d) ~ 1 + s_d/(8 sigma^2) and
exp(...) ~ 1 - delta_d^2/(2 sigma^2), so the layer factor is 1 - (delta_d^2/2 - s_d/8)/sigma^2
and

    lm/r  ~  Gamma * (1 - Q(0)/sigma^2),
    Q(0) = Gamma^{-1} sum_d 2^{-N_d} (delta_d^2 - s_d/4) ,

which is EXACTLY the quantity Part III already tabulates in the counterexample section.
So the annealed prediction's relative error should be Q(0)/sigma^2, and (H) -- the
boundedness of sum 2^{-N_d} delta_d^2 -- is precisely the condition that keeps the
numerator from growing.  Test it against the exact DP.
"""
import numpy as np

def subset_counts(A):
    T=sum(A); dp=np.zeros(T+1); dp[0]=1.0
    for a in A: dp[a:] += dp[:-a]
    return dp

def lm_profile(A):
    A=sorted(A); T=sum(A); M=A[-1]
    r=subset_counts(A); lm=r.copy(); cache={}
    for d in range(1,(M-1)//2+1):
        j=sum(1 for a in A if a<=2*d)
        if j not in cache:
            hi=A[j:]; cache[j]=(subset_counts(hi) if hi else np.array([1.0]), sum(A[:j]))
        cnt,slow=cache[j]; L=len(cnt); n=np.arange(T+1)
        t1=n+d; m1=t1<L; lm[m1]+=cnt[t1[m1]]
        t2=n-d-slow; m2=(t2>=0)&(t2<L); lm[m2]+=cnt[t2[m2]]
    return r,lm

def gamma_Q_sigma(A):
    A=sorted(A); M=A[-1]
    sig2=sum(a*a for a in A)/4.0
    G=1.0; S=0.0
    for d in range(1,(M-1)//2+1):
        low=[a for a in A if a<=2*d]
        N=len(low); L=sum(low); s=sum(a*a for a in low)
        w=2.0**-N; G+=2*w
        S+=w*((d+L/2.0)**2 - s/4.0)
    return G, S/G, sig2

def profile(kind,k):
    if kind=='odds': return [2*i-1 for i in range(1,k+1)]
    if kind=='sqrt32':
        A,last=[],-1
        for i in range(1,k+1):
            a=2*int((i**1.5)/2)+1
            while a<=last: a+=2
            A.append(a); last=a
        return A
    if kind=='alpha12':
        c=4.0*np.sqrt(k); A,last=[],-1
        for i in range(1,k+1):
            a=2*int(c*np.sqrt(i)/2)+1
            while a<=last: a+=2
            A.append(a); last=a
        return A

print("="*100)
print("predicted relative error  Q(0)/sigma^2   against the exact computation")
print("="*100)
print(f"  {'profile':>8s} {'k':>4s} {'Gamma':>10s} {'Q(0)':>12s} {'sigma^2':>12s}"
      f" {'predicted':>11s} {'measured':>11s} {'ratio':>7s}")
for kind in ('odds','sqrt32','alpha12'):
    for k in (20,30,40,55,70,90):
        A=profile(kind,k)
        r,lm=lm_profile(A); T=sum(A); c=T//2; w=slice(c-20,c+21)
        rr,ll=r[w],lm[w]; m=rr>0
        val=float((ll[m]/rr[m]).mean())
        G,Q,s2=gamma_Q_sigma(A)
        pred=Q/s2; meas=(G-val)/G
        print(f"  {kind:>8s} {k:4d} {G:10.5f} {Q:12.4f} {s2:12.1f} {pred:11.6f}"
              f" {meas:11.6f} {meas/pred if pred else 0:7.3f}")
    print()

print("="*100)
print("the extremal case the formula points at: a translated block {2m+1, ..., 2m+2k-1}")
print("all elements of size ~ 2m, so N_d = 0 for every d < m and Q(0) is as large as it")
print("can be relative to Gamma.  Predicted relative error ~ 1/(6k), the slowest decay")
print("any family of distinct odd integers can produce.")
print("="*100)
print(f"  {'m':>5s} {'k':>4s} {'Gamma':>10s} {'Q(0)':>12s} {'sigma^2':>12s} {'pred':>10s}"
      f" {'measured':>10s} {'ratio':>7s} {'k*pred':>8s}")
for k in (12, 18, 24, 30, 36):
    m = k
    A = [2*m+1+2*i for i in range(k)]
    r, lm = lm_profile(A); T=sum(A); c=T//2; w=slice(max(0,c-20), c+21)
    rr, ll = r[w], lm[w]; msk = rr>0
    val = float((ll[msk]/rr[msk]).mean())
    G,Q,s2 = gamma_Q_sigma(A); pred=Q/s2; meas=(G-val)/G
    print(f"  {m:5d} {k:4d} {G:10.4f} {Q:12.2f} {s2:12.1f} {pred:10.6f}"
          f" {meas:10.6f} {meas/pred:7.3f} {k*pred:8.4f}")
print()
print("  k*pred settling means the error is Theta(1/k) for this family: slow, and still")
print("  going to zero.  The formula therefore says the annealed prediction survives every")
print("  family of distinct odd integers, with 1/k the worst rate available -- because")
print("  Q(0) ~ m^2/6 and sigma^2 ~ k m^2, so the m cancels and only 1/k is left.")



def stats(A, halfwidth=40):
    r, lm = lm_profile(A); T=sum(A); c=T//2
    w = slice(max(0,c-halfwidth), c+halfwidth+1)
    rr, ll = r[w], lm[w]
    nz = int((rr>0).sum())
    return (float(ll.sum()/rr.sum()) if rr.sum()>0 else None), nz, 2*halfwidth+1

print("="*104)
print("r-weighted ratio (the value at a typical ground state), and how full the window is")
print("="*104)
print(f"  {'family':>10s} {'k':>4s} {'window':>9s} {'Gamma':>10s} {'lm/r':>10s}"
      f" {'measured':>10s} {'predicted':>10s} {'ratio':>7s}")
for kind in ('odds','sqrt32','alpha12'):
    for k in (30,55,90):
        A=profile(kind,k); val,nz,tot=stats(A); G,Q,s2=gamma_Q_sigma(A)
        meas=(G-val)/G; pred=Q/s2
        print(f"  {kind:>10s} {k:4d} {f'{nz}/{tot}':>9s} {G:10.5f} {val:10.5f}"
              f" {meas:10.6f} {pred:10.6f} {meas/pred:7.3f}")
print()
for k in (12,18,24,30,36,44):
    m=k; A=[2*m+1+2*i for i in range(k)]
    val,nz,tot=stats(A); G,Q,s2=gamma_Q_sigma(A)
    meas=(G-val)/G; pred=Q/s2
    print(f"  {'block':>10s} {k:4d} {f'{nz}/{tot}':>9s} {G:10.5f} {val:10.5f}"
          f" {meas:10.6f} {pred:10.6f} {meas/pred:7.3f}")
print()
print("  the window occupancy column is the diagnostic: where it is far below full, the")
print("  unweighted mean of ratios was averaging over an atypical subset of targets.")
