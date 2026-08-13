"""
r151 -- the correction at a GENERAL target, and the prediction it makes.

prop:correction is stated at the centre.  The theorem is "for every target", so redo the
layer expansion at n with z = (n - mu)/sigma.  The two offsets are no longer symmetric:

  z_d^+ = (z sigma + delta_d)/sigma_d,   z_d^- = (z sigma - delta_d)/sigma_d,

and phi(z_d^+) + phi(z_d^-) = 2 phi(z) exp(-[z^2 s_d/4 + delta_d^2]/(2 sigma_d^2))
                                       cosh(z sigma delta_d / sigma_d^2).
Expanding to first order in 1/sigma^2, with cosh ~ 1 + z^2 delta_d^2/(2 sigma^2):

    lm/r  =  Gamma * ( 1 - (1 - z^2) Q(0)/sigma^2 )  +  o(sigma^-2).

THE PREDICTION.  The correction carries a factor (1 - z^2).  It VANISHES at z = +-1 -- one
standard deviation from the centre -- and CHANGES SIGN beyond, so lm/r should sit BELOW
Gamma inside one sigma and ABOVE it outside.  Nothing in the annealed picture suggests a
crossing; if it is there, the expansion is describing something real.
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
    A=sorted(A); M=A[-1]; sig2=sum(a*a for a in A)/4.0
    G=1.0; S=0.0
    for d in range(1,(M-1)//2+1):
        low=[a for a in A if a<=2*d]
        N=len(low); L=sum(low); s=sum(a*a for a in low)
        w=2.0**-N; G+=2*w; S+=w*((d+L/2.0)**2 - s/4.0)
    return G, S/G, sig2

print("="*96)
print("lm/r against Gamma as a function of z = (n - mu)/sigma")
print("prediction:  (Gamma - lm/r)/Gamma  =  (1 - z^2) Q(0)/sigma^2")
print("="*96)
for k, kind in ((90,'odds'), (60,'odds'), (40,'sqrt32')):
    if kind=='odds': A=[2*i-1 for i in range(1,k+1)]
    else:
        A,last=[],-1
        for i in range(1,k+1):
            a=2*int((i**1.5)/2)+1
            while a<=last: a+=2
            A.append(a); last=a
    r,lm=lm_profile(A); T=sum(A); mu=T/2.0
    G,Q,s2=gamma_Q_sigma(A); sig=np.sqrt(s2)
    print(f"\n  {kind}, k={k}:  Gamma={G:.6f}  Q(0)={Q:.3f}  sigma={sig:.1f}"
          f"  Q/sigma^2={Q/s2:.3e}")
    print(f"    {'z':>6s} {'n':>8s} {'lm/r':>12s} {'measured dev':>14s} {'predicted':>13s} {'ratio':>7s}")
    for z in (0.0, 0.5, 0.9, 1.0, 1.1, 1.5, 2.0, 2.5):
        n=int(round(mu + z*sig)); w=slice(max(0,n-20), n+21)
        rr,ll=r[w],lm[w]
        if rr.sum()<=0: continue
        val=float(ll.sum()/rr.sum()); dev=(G-val)/G; pred=(1-z*z)*Q/s2
        rat = dev/pred if abs(pred)>1e-14 else float('nan')
        print(f"    {z:6.2f} {n:8d} {val:12.6f} {dev:14.3e} {pred:13.3e} {rat:7.3f}")
