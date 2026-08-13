"""
r152 -- the z-dependence tested on the case Part II actually proves: the odd primes.

Part II proves the theorem for the primes AT THE CENTRE, unconditionally.  cor:crossing
speaks about every target, so the primes are the sharpest place to test it: the one family
where the main theorem is not conditional on anything.

Predicted:  (Gamma - lm/r)/Gamma = (1 - z^2) Q(0)/sigma^2,  z = (n - mu)/sigma.
Window occupancy is printed -- a prediction tested on an empty window is not tested.
"""
import numpy as np
from sympy import primerange

def subset_counts(A):
    T=sum(A); dp=np.zeros(T+1); dp[0]=1.0
    for a in A: dp[a:] += dp[:-a]
    return dp

def lm_profile(A):
    """lm and r for every target.  Tails A_{>2d} are built ONCE per distinct threshold,
       from the top down, so the cost is O(k^2 T / 2) rather than O(k) full rebuilds."""
    A=sorted(A); T=sum(A); M=A[-1]; k=len(A)
    r=subset_counts(A); lm=r.copy()
    pref=[0]*(k+1)
    for i,a in enumerate(A): pref[i+1]=pref[i]+a
    tails={}
    for j in range(k):                      # tail A[j:]
        hi=A[j:]
        tails[j]=subset_counts(hi) if hi else np.array([1.0])
    tails[k]=np.array([1.0])
    n=np.arange(T+1)
    js=[sum(1 for a in A if a<=2*d) for d in range(1,(M-1)//2+1)]
    for d,j in enumerate(js, start=1):
        cnt=tails[j]; slow=pref[j]; L=len(cnt)
        t1=n+d; m1=t1<L; lm[m1]+=cnt[t1[m1]]
        t2=n-d-slow; m2=(t2>=0)&(t2<L); lm[m2]+=cnt[t2[m2]]
    return r,lm

def gamma_Q_sigma(A):
    A=sorted(A); M=A[-1]; k=len(A)
    pref=[0]*(k+1); pref2=[0]*(k+1)
    for i,a in enumerate(A): pref[i+1]=pref[i]+a; pref2[i+1]=pref2[i]+a*a
    sig2=pref2[k]/4.0
    G=1.0; S=0.0; j=0
    for d in range(1,(M-1)//2+1):
        while j<k and A[j]<=2*d: j+=1
        w=2.0**-j; G+=2*w
        S+=w*((d+pref[j]/2.0)**2 - pref2[j]/4.0)
    return G, S/G, sig2

GAMMA_P = 5.34928793202265755799135261817
def first_primes(k):
    out=[]
    for p in primerange(3, 10**7):
        out.append(p)
        if len(out)==k: break
    return out

print("="*100)
print("the odd primes: does the crossing at one standard deviation happen there too?")
print("="*100)
for k in (40, 65, 90):
    A=first_primes(k)
    r,lm=lm_profile(A); T=sum(A); mu=T/2.0
    G,Q,s2=gamma_Q_sigma(A); sig=np.sqrt(s2)
    print(f"\n  k={k} odd primes, max={A[-1]}, T={T}")
    print(f"    Gamma={G:.8f}   (Gamma(P)={GAMMA_P:.8f}, diff {G-GAMMA_P:+.2e})")
    print(f"    Q(0)={Q:.4f}   sigma={sig:.1f}   Q/sigma^2={Q/s2:.4e}")
    print(f"    {'z':>6s} {'occ':>7s} {'lm/r':>13s} {'measured dev':>14s} {'predicted':>13s} {'ratio':>7s}")
    for z in (0.0,0.5,0.9,1.0,1.1,1.5,2.0):
        n=int(round(mu+z*sig)); w=slice(max(0,n-20),n+21)
        rr,ll=r[w],lm[w]; occ=int((rr>0).sum())
        if rr.sum()<=0: continue
        val=float(ll.sum()/rr.sum()); dev=(G-val)/G; pred=(1-z*z)*Q/s2
        rat=dev/pred if abs(pred)>1e-14 else float('nan')
        print(f"    {z:6.2f} {f'{occ}/41':>7s} {val:13.8f} {dev:14.3e} {pred:13.3e} {rat:7.3f}")

print()
print("="*100)
print("primes against odd numbers at the same k: which is the annealed answer better for?")
print("="*100)
print(f"  {'k':>5s} {'Q odds':>9s} {'Q primes':>10s} {'s2 odds':>12s} {'s2 primes':>13s}"
      f" {'err odds':>11s} {'err primes':>11s} {'odds/primes':>12s}")
for k in (40,70,110,160,240,360,520):
    O=[2*i-1 for i in range(1,k+1)]; P=first_primes(k)
    Go,Qo,so=gamma_Q_sigma(O); Gp,Qp,sp=gamma_Q_sigma(P)
    eo,ep=Qo/so,Qp/sp
    print(f"  {k:5d} {Qo:9.3f} {Qp:10.3f} {so:12.1f} {sp:13.1f} {eo:11.3e} {ep:11.3e} {eo/ep:12.2f}")

print()
print("="*100)
print("Q(0) for the odd numbers is exact")
print("="*100)
import sympy as sp
d = sp.symbols('d', positive=True, integer=True)
S = sp.summation(((d + d**2/2)**2 - d*(2*d-1)*(2*d+1)/12) * sp.Rational(1,2)**d, (d,1,sp.oo))
print(f"  N_d = d, L_d = d^2, s_d = d(2d-1)(2d+1)/3, delta_d = d + d^2/2")
print(f"  sum_{{d>=1}} 2^-d (delta_d^2 - s_d/4) = {S}   exactly")
print(f"  Gamma(odds) = 3, so Q(0) = {sp.nsimplify(S/3)} = {float(S/3):.10f}")
print(f"  and the relative error of the annealed prediction at the centre is")
print(f"  Q(0)/sigma^2 with sigma^2 = k(4k^2-1)/12, i.e. asymptotically 61/k^3.")
