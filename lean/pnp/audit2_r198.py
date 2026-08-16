#!/usr/bin/env python3
"""audit2_r198 -- ALL zeros of the odd-number Gamma^(q), exactly.
Gamma^(q)_k = 1 + sum_{j=1}^{k-1}[q^j+(1-q)^j] is a polynomial, so polyroots finds every zero:
'no zero here' becomes a statement about the whole set, not about where we looked (F60).
 A2 rem:leeyang  : endpoint rate must be 2pi/k, NOT pi/k (endpoint = single section,
                   fair coin = conjugate sum; the factor 2 is the r195 fingerprint).
 A3 prop:nopinch : no zero inside |q-1/2| < 1/6; paper's 0.5046 at k=64 and factor 3.03."""
import mpmath as mp
from math import comb
mp.mp.dps = 40

def coeffs(k):
    c=[mp.mpf(0)]*k; c[0]+=1
    for j in range(1,k):
        c[j]+=1
        for i in range(j+1): c[i]+=mp.mpf(comb(j,i))*(-1)**i
    c=list(reversed(c))
    while c and c[0]==0: c.pop(0)   # q<->1-q symmetry kills the top term for even k: true deg k-2
    return c

print("="*82); print("audit2_r198 -- ALL zeros of the odd-number Gamma^(q), exactly"); print("="*82)
print(f"\n{'k':>5}{'true deg':>10}{'|q| nearest 0':>18}{'k*|Im q|':>12}{'dist to 1/2':>14}")
R={}
for k in (16,24,32,48,64):
    c=coeffs(k); rts=mp.polyroots(c, maxsteps=300, extraprec=600); R[k]=rts
    n0=min(rts,key=lambda r:abs(r)); nh=min(rts,key=lambda r:abs(r-mp.mpf("0.5")))
    print(f"{k:>5}{len(c)-1:>10}{mp.nstr(abs(n0),9):>18}{mp.nstr(k*abs(mp.im(n0)),8):>12}"
          f"{mp.nstr(abs(nh-mp.mpf('0.5')),9):>14}")
print(f"\n[A2] endpoint rate.  paper claims 2*pi/k = {mp.nstr(2*mp.pi,9)}/k")
for k in (16,24,32,48,64):
    n0=min(R[k],key=lambda r:abs(r))
    print(f"   k={k:3d}  k*|Im q_1| = {mp.nstr(k*abs(mp.im(n0)),9):>13}"
          f"   /2pi = {mp.nstr(k*abs(mp.im(n0))/(2*mp.pi),7):>10}"
          f"   /pi = {mp.nstr(k*abs(mp.im(n0))/mp.pi,7):>10}")
print(f"\n[A3] prop:nopinch: |q-1/2| < 1/6 = {mp.nstr(mp.mpf(1)/6,8)} must be zero-free, uniformly in k")
for k in (16,24,32,48,64):
    d=min(abs(r-mp.mpf("0.5")) for r in R[k])
    print(f"   k={k:3d}  nearest zero to 1/2 = {mp.nstr(d,10):>13}"
          f"   {'ok' if d>mp.mpf(1)/6 else '*** FIRED ***'}   conservative by {mp.nstr(d/(mp.mpf(1)/6),5)}")
