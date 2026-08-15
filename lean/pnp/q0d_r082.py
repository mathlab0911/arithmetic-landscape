# q0d_r082.py  Localise the residual: compare the EXACT layer term with the model term, per d.
#   exact term_d = [ r_{B_d}(n+d) + r_{B_d}(T-n+d) ] / r_B(n)
#   model term_d = 2^{-N_d} e^{-delta^2/2V} * 2 cosh(u*delta/V)
import numpy as np, math
from fractions import Fraction
def odd_primes(k):
    out=[]; n=3
    while len(out)<k:
        if all(n%p for p in range(3,int(n**0.5)+1,2)): out.append(n)
        n+=2
    return out
def layers(A, rho, dmax):
    A=sorted(A); k=len(A); T=sum(A); S2=sum(a*a for a in A); V=S2/4.0; D=(A[-1]-1)//2
    n=int(rho*T); u=T/2.0-n
    # build suffix DPs on the fly, from d=D down to 1, recording the terms we want
    dp=np.zeros(1); dp[0]=1.0; cur=k; rec={}
    g=lambda m: dp[m] if 0<=m<len(dp) else 0.0
    sigs={}; Nds={}
    j=0; sig=0
    for d in range(1,D+1):
        while j<k and A[j]<=2*d: sig+=A[j]; j+=1
        sigs[d]=sig; Nds[d]=j
    for d in range(D,0,-1):
        jj=Nds[d]
        while cur>jj:
            cur-=1; a=A[cur]; nw=np.zeros(len(dp)+a); nw[:len(dp)]=dp; nw[a:a+len(dp)]+=dp; dp=nw
        if d<=dmax: rec[d]=g(n+d)+g(T-n+d)
    while cur>0:
        cur-=1; a=A[cur]; nw=np.zeros(len(dp)+a); nw[:len(dp)]=dp; nw[a:a+len(dp)]+=dp; dp=nw
    rB=g(n)
    out=[]
    for d in sorted(rec):
        ex=rec[d]/rB
        delta=d+sigs[d]/2.0; w=2.0**(-Nds[d])
        mo=w*math.exp(-delta*delta/(2*V))*2*math.cosh(u*delta/V)
        out.append((d,Nds[d],sigs[d],delta,ex,mo,ex/mo))
    return out,u,V
print("="*104)
print("Per-layer comparison: EXACT term_d  vs  MODEL term_d   (odds, k=220)")
print("="*104)
for rho,lab in ((0.40,"x=0.10"),(0.20,"x=0.30")):
    L,u,V=layers([2*i+1 for i in range(220)], rho, 14)
    print(f"\n  {lab}   (u={u:.1f}, V={V:.4g})")
    print("     d   N_d  sigma_d   delta_d      exact term      model term     exact/model")
    for (d,Nd,sig,delta,ex,mo,r) in L:
        print(f"   {d:3d} {Nd:4d} {sig:8d} {delta:9.1f}   {ex:14.8f}  {mo:14.8f}   {r:10.6f}")
print()
print("="*104)
print("Same, primes k=220")
print("="*104)
for rho,lab in ((0.40,"x=0.10"),):
    L,u,V=layers(odd_primes(220), rho, 14)
    print(f"\n  {lab}")
    print("     d   N_d  sigma_d   delta_d      exact term      model term     exact/model")
    for (d,Nd,sig,delta,ex,mo,r) in L:
        print(f"   {d:3d} {Nd:4d} {sig:8d} {delta:9.1f}   {ex:14.8f}  {mo:14.8f}   {r:10.6f}")
