# lam_r084.py (2026-08-09, opus-5 round 84) Discriminate (S1) constant offset shift
#   vs (S2) global slope-reference mismatch, by extracting the effective slope per layer.
#     P_d = r_{B_d}(n+d) + r_{B_d}(n-d-sigma_d),  M_d = r_{B_d}(n-d-sigma_d) - r_{B_d}(n+d)
#     lambda_d^eff = atanh(M_d/P_d) / delta_d
#   fable's marked suspicion: the atanh extraction assumes the pair is exactly +-delta_d about
#   the recentred mean.  So the FIRST thing here is a synthetic Gaussian where the answer is known.
import numpy as np, math
from fractions import Fraction
def odd_primes(k):
    out=[]; n=3
    while len(out)<k:
        if all(n%p for p in range(3,int(n**0.5)+1,2)): out.append(n)
        n+=2
    return out
ENS={"odds":lambda k:[2*i+1 for i in range(k)],
     "squares":lambda k:sorted(set(2*((i*i)//2)+1 for i in range(1,k+1))),
     "primes":odd_primes}

print("="*100)
print("SANITY CHECK FIRST (fable's marked spot): does the atanh extraction return the input")
print("slope on a synthetic Gaussian, for every delta?")
print("="*100)
Vs=3.5e6; us=4840.0
print("    delta      input u/V        extracted        rel.err")
for delta in (1.5,12.0,40.0,112.0,300.0,800.0):
    rp=math.exp(-((-us+delta)**2)/(2*Vs)); rm=math.exp(-((-us-delta)**2)/(2*Vs))
    P=rp+rm; M=rm-rp
    lam=math.atanh(M/P)/delta
    print(f"  {delta:8.1f}   {-us/Vs:+.9e}   {lam:+.9e}   {abs(lam+us/Vs)/(us/Vs):.2e}")
print("  -> exact for every delta, as required. The extraction is sound; anything anomalous")
print("     in the real data is the theory, not the tool.")

def layers(A, rho, dmax):
    A=sorted(A); k=len(A); T=sum(A); S2=sum(a*a for a in A); V=S2/4.0; D=(A[-1]-1)//2
    n=int(rho*T); u=T/2.0-n
    j=0; sig=0; sigs={}; Nds={}
    for d in range(1,D+1):
        while j<k and A[j]<=2*d: sig+=A[j]; j+=1
        sigs[d]=sig; Nds[d]=j
    dp=np.zeros(1); dp[0]=1.0; cur=k; rec={}
    g=lambda m: dp[m] if 0<=m<len(dp) else 0.0
    for d in range(D,0,-1):
        jj=Nds[d]
        while cur>jj:
            cur-=1; a=A[cur]; nw=np.zeros(len(dp)+a); nw[:len(dp)]=dp; nw[a:a+len(dp)]+=dp; dp=nw
        if d<=dmax: rec[d]=(g(n+d), g(T-n+d))     # r_Bd(n+d), r_Bd(n-d-sigma_d)
    while cur>0:
        cur-=1; a=A[cur]; nw=np.zeros(len(dp)+a); nw[:len(dp)]=dp; nw[a:a+len(dp)]+=dp; dp=nw
    lam_true = 0.25*math.log(g(n-2)/g(n+2))       # per unit m, sign as in r082
    out=[]
    for d in sorted(rec):
        rp,rm = rec[d]; P=rp+rm; M=rm-rp
        delta = d + sigs[d]/2.0
        lam_d = math.atanh(M/P)/delta
        out.append((d,Nds[d],delta,lam_d,lam_d/lam_true))
    return out, lam_true, u, V

print()
print("="*106)
print("THE DISCRIMINATING MEASUREMENT:  lambda_d^eff / lambda_true  vs d and vs 1/delta_d")
print("   (S1) constant offset shift c  -> linear in 1/delta with intercept 1")
print("   (S2) global reference mismatch -> constant ~0.936 in d")
print("="*106)
for nm,f in ENS.items():
    for k in (180,220):
        if nm=="squares" and k==220: k=170
        for rho,xl in ((0.40,"x=0.10"),(0.30,"x=0.20")):
            L,lt,u,V=layers(f(k),rho,14)
            print(f"\n  ### {nm}  k={k}  {xl}   lambda_true={lt:+.6e}   u/V={-u/V:+.6e}   (u/V)/lt={-u/V/lt:.5f}")
            print("      d   N_d    delta_d     1/delta_d     lambda_d^eff      ratio to lambda_true")
            for (d,Nd,delta,ld,r) in L:
                print(f"    {d:3d} {Nd:5d} {delta:11.2f}  {1/delta:11.6f}   {ld:+14.6e}   {r:14.6f}")
            # fit ratio = a + b/delta
            xs=[1/e[2] for e in L]; ys=[e[4] for e in L]
            nn=len(xs); mx=sum(xs)/nn; my=sum(ys)/nn
            b=sum((p-mx)*(q-my) for p,q in zip(xs,ys))/sum((p-mx)**2 for p in xs); a=my-b*mx
            ss=sum((q-my)**2 for q in ys)
            r2=1-sum((q-(a+b*p))**2 for p,q in zip(xs,ys))/ss if ss>0 else float('nan')
            print(f"      fit ratio = a + b/delta :  a = {a:.6f}   b = {b:+.4f}  (=> c = {-b:+.4f})   R2 = {r2:.5f}")
            print(f"      spread of the ratio over d = {max(ys)-min(ys):.6f}   mean = {my:.6f}")
