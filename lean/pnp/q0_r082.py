# q0_r082.py (2026-08-09, opus-5 round 82) Verify fable's closed form for Q(0).
#   (*)  ratio(lambda) = 1 + SUM_d 2^{-N_d} e^{-delta_d^2/2V} * 2 cosh(lambda delta_d),  delta_d = d + sigma_d/2
#   (**) Q(0) = (1/Gamma) SUM_d 2^{-N_d} (d + sigma_d/2)^2
#   Expanding cosh one more order also predicts the x-dependence:
#        Qhat_c(x) = Q(0) * (1 + lambda^2 * R4/12),  R4 = SUM 2^{-N_d} delta^4 / SUM 2^{-N_d} delta^2
#   That second prediction is a far stronger test than the single number, so it is included.
import numpy as np, math
from fractions import Fraction
def odd_primes(k):
    out=[]; n=3
    while len(out)<k:
        if all(n%p for p in range(3,int(n**0.5)+1,2)): out.append(n)
        n+=2
    return out
ENS={"odds ~i":    lambda k:[2*i+1 for i in range(k)],
     "squares ~i^2":lambda k:sorted(set(2*((i*i)//2)+1 for i in range(1,k+1))),
     "primes":      odd_primes,
     "cubes ~i^3":  lambda k:sorted(set(2*((i**3)//2)+1 for i in range(1,k+1)))}

def series(A):
    """returns Gamma, S1 = SUM 2^-N_d, S2 = SUM 2^-N_d delta^2, S4 = SUM 2^-N_d delta^4,
       plus the Gaussian factors, evaluated over d = 1..D with D = (max-1)/2"""
    A=sorted(A); k=len(A); T=sum(A); V=sum(a*a for a in A)/4.0; D=(A[-1]-1)//2
    G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
    s1=s2=s4=0.0; s1g=s2g=0.0; j=0; sig=0; rows=[]
    minfac=1.0
    for d in range(1,D+1):
        while j<k and A[j]<=2*d: sig+=A[j]; j+=1
        w=2.0**(-j); delta=d+sig/2.0; fac=math.exp(-delta*delta/(2*V))
        s1+=w; s2+=w*delta**2; s4+=w*delta**4
        s1g+=w*fac; s2g+=w*fac*delta**2
        if w*delta*delta>1e-12: minfac=min(minfac,fac)
        if d<=8: rows.append((d,j,sig,delta,w,w*delta*delta,fac))
    return dict(G=G,S1=s1,S2=s2,S4=s4,S1g=s1g,S2g=s2g,T=T,V=V,D=D,rows=rows,minfac=minfac,k=k)

print("="*112)
print("ITEM 2 -- the lambda=0 identity:  1 + SUM 2^{1-N_d} = Gamma(A) ?   (this is paper 1's window identity)")
print("     and how big are the Gaussian factors e^{-delta^2/2V} that (*) carries alongside")
print("="*112)
print(f"  {'ensemble':<14} {'k':>4} {'1+2*S1':>12} {'Gamma(A)':>12} {'diff':>11}   {'1+2*S1g':>12} {'rel.err from':>14}")
print(f"  {'':<14} {'':>4} {'':>12} {'':>12} {'':>11}   {'(with e^-..)':>12} {'the factors':>14}")
for nm,f in ENS.items():
    k = 220 if "cube" not in nm and "square" not in nm else (170 if "square" in nm else 70)
    r=series(f(k))
    a=1+2*r['S1']; b=1+2*r['S1g']
    print(f"  {nm:<14} {k:>4} {a:12.6f} {r['G']:12.6f} {a-r['G']:11.2e}   {b:12.6f} {abs(b-a)/a:14.2e}")
print("\n  (the identity is exact up to the (2D+1)/2^k tail of Theorem B; the Gaussian factors are")
print("   the size shown in the last column -- negligible where the weights are not.)")

print()
print("="*112)
print("ITEM 1/3 -- the closed form (**) per ensemble, with partial sums")
print("="*112)
PRED={}
for nm,f in ENS.items():
    k = 220 if nm in ("odds ~i","primes") else (170 if "square" in nm else 70)
    r=series(f(k)); q0=r['S2']/r['G']; R4=r['S4']/r['S2']
    PRED[nm]=(q0,R4,r)
    print(f"\n  ### {nm}   (k={k}, Gamma={r['G']:.5f}, V={r['V']:.4g}, D={r['D']})")
    print(f"      d   N_d   sigma_d       delta_d      2^-N_d     2^-N_d*delta^2   e^{{-d^2/2V}}")
    for (d,Nd,sig,delta,w,term,fac) in r['rows']:
        print(f"    {d:3d} {Nd:5d} {sig:9d} {delta:13.2f} {w:11.3e} {term:15.4f}   {fac:.6f}")
    print(f"      ...  total SUM 2^-N_d delta^2 = {r['S2']:.4f}")
    print(f"      ==> Q(0) = {r['S2']:.4f} / {r['G']:.5f} = **{q0:.3f}**       R4/12 (x-dependence) = {R4/12:.4g}")

print()
print("="*112)
print("ITEM 1 -- measured Qhat_c extrapolated to x->0, and the comparison")
print("="*112)
def measure(A, rhos):
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
    out={}
    dev={r:((g(n)+extra[r])/g(n))/G-1.0 for r,n in ns.items()}
    for r,n in ns.items():
        if r==0.5: continue
        lam=(T/2.0-n)/(S2/4.0)
        out[0.5-r]=((dev[r]-dev[0.5])/lam**2, lam)
    return out
RH=[0.30,0.35,0.40,0.42,0.44]
print(f"  {'ensemble':<14} " + "".join(f"  x={0.5-r:.2f}  " for r in RH) + "   A (even fit)  measured/predicted")
for nm in ("odds ~i","squares ~i^2","primes"):
    k = 220 if nm in ("odds ~i","primes") else 170
    m=measure(ENS[nm](k), RH)
    xs=sorted(m); qs=[m[x][0] for x in xs]
    # even fit Q = A + B x^2 (least squares on x^2)
    u=[x*x for x in xs]; n=len(u); mu=sum(u)/n; my=sum(qs)/n
    B=sum((a-mu)*(y-my) for a,y in zip(u,qs))/sum((a-mu)**2 for a in u); A0=my-B*mu
    q0p=PRED[nm][0]
    print(f"  {nm:<14} "+"".join(f"{m[x][0]:9.2f} " for x in xs)+f"   {A0:10.2f}     {A0/q0p:8.4f}")
    print(f"  {'':<14} predicted Q(0) = {q0p:.3f};  predicted B/A = R4/12·(T/V)²·... see next block")
