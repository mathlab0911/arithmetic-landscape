"""
r153 -- the corrections to the annealed prediction are a HERMITE expansion in z.

First order came out as 1 - z^2, and 1 - z^2 = -He_2(z).  So

    lm/r = Gamma * ( 1 + He_2(z) Q(0)/sigma^2 + O(sigma^-4) ),

which is not a coincidence of notation: the same Hermite polynomials organise the
Edgeworth expansion of Appendix A.  If the pattern is real, the next term should be a
combination of He_4 and He_2, and the residual after removing the He_2 term should be
proportional to He_4 in z.

Test: R(z) = (lm/r / Gamma - 1 - He_2(z) Q/sigma^2) * sigma^4, and look at R(z)/He_4(z).
Small k on purpose -- the residual is O(sigma^-4), and at k = 30 that is 1e-8, far above
the float64 noise floor of the dynamic program.
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
    tails={j:(subset_counts(A[j:]) if j<k else np.array([1.0])) for j in range(k+1)}
    n=np.arange(T+1)
    for d in range(1,(M-1)//2+1):
        j=sum(1 for a in A if a<=2*d)
        cnt=tails[j]; slow=pref[j]; L=len(cnt)
        t1=n+d; m1=t1<L; lm[m1]+=cnt[t1[m1]]
        t2=n-d-slow; m2=(t2>=0)&(t2<L); lm[m2]+=cnt[t2[m2]]
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

He2 = lambda z: z*z - 1.0
He4 = lambda z: z**4 - 6*z*z + 3.0

print("="*96)
print("is the residual after the He_2 term proportional to He_4 ?")
print("="*96)
for k in (24, 30, 36):
    A=[2*i-1 for i in range(1,k+1)]
    r,lm=lm_profile(A); T=sum(A); mu=T/2.0
    G,Q,s2=gamma_Q_sigma(A); sig=np.sqrt(s2)
    print(f"\n  odd numbers, k={k}:  Gamma={G:.10f}  Q={Q:.5f}  sigma^2={s2:.1f}"
          f"  sigma^-4={s2**-2:.2e}")
    print(f"    {'z':>6s} {'lm/r':>14s} {'He2 term':>12s} {'residual*s^4':>14s}"
          f" {'He4(z)':>9s} {'ratio':>10s}")
    rows=[]
    for z in (0.0,0.4,0.8,1.2,1.6,2.0,2.4):
        n=int(round(mu+z*sig)); w=slice(max(0,n-20),n+21)
        rr,ll=r[w],lm[w]
        if rr.sum()<=0: continue
        val=float(ll.sum()/rr.sum())
        rel=val/G-1.0
        h2=He2(z)*Q/s2
        R=(rel-h2)*s2*s2
        h4=He4(z)
        rows.append((z,R,h4))
        print(f"    {z:6.2f} {val:14.9f} {h2:12.3e} {R:14.4f} {h4:9.3f}"
              f" {R/h4 if abs(h4)>1e-9 else float('nan'):10.3f}")
    rs=[R/h4 for _,R,h4 in rows if abs(h4)>0.3]
    if rs:
        print(f"    ratio over the points with |He4| > 0.3:  mean {np.mean(rs):.3f}"
              f"   spread {np.std(rs)/abs(np.mean(rs))*100:.1f}%")
