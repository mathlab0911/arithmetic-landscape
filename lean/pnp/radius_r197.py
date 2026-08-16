#!/usr/bin/env python3
"""
radius_r197 -- does R >= 1 imply Gamma finite?  (paper4 prop:gqgen item 1, and rem:nopinchreading)

THE CLAIM UNDER TEST, quoted from a proposition carrying STATUS{proved}:
    "G(1) = (Gamma(A)-1)/2, so R >= 1 is exactly the statement that Gamma(A) is finite."

WHY IT IS SUSPECT.  R is the radius of convergence of G(z) = sum_j w_j z^j with w_j >= 0.
The radius says nothing about the boundary point z = 1:
    R > 1  =>  G(1) converges  (true)
    R < 1  =>  G(1) diverges   (true)
    R = 1  =>  either          (the case the claim absorbs into the wrong side)

FALSIFIER, registered before running (F45):
    The claim dies if a single pair exists with R = 1 for BOTH members and Gamma finite for one
    and divergent for the other.  If no such pair is found, the claim survives this test.

The two candidates are already in the paper and in r196:
    a_i = 2^i + 1     w = (1, 1/2, 1/2, ...)                 R = 1 ?   Gamma_k = k+2 ?
    family C          w_j = m_j 2^-j ~ (j+1)^-2              R = 1 ?   Gamma_k -> ~5.23 ?
"""
import mpmath as mp
mp.mp.dps = 30

def w_lacplus(k):  return [mp.mpf(1)]+[mp.mpf(1)/2]*(k-1)
def w_C(k):        return [max(1,int(round(2**j/(j+1)**2)))/mp.mpf(2)**j for j in range(k)]

print("="*84)
print("radius_r197 -- R >= 1 does NOT decide whether Gamma is finite")
print("="*84)
print(f"\n{'family':<26}{'k':>7}{'w_k^(1/k)  (R = 1/limsup)':>28}{'Gamma_k = 1+2*sum w':>22}")
res={}
for name, wf in (("a_i = 2^i+1", w_lacplus), ("family C  w_j~(j+1)^-2", w_C)):
    for k in (64,128,256,512,1024):
        w = wf(k)
        root = w[-1]**(mp.mpf(1)/(k-1))
        G = 1+2*sum(w)
        print(f"{name:<26}{k:>7}{mp.nstr(root,10):>28}{mp.nstr(G,10):>22}")
        res[(name,k)] = (root, G)
    print()

r1 = res[("a_i = 2^i+1",1024)]; r2 = res[("family C  w_j~(j+1)^-2",1024)]
print("VERDICT at k = 1024")
print(f"  2^i+1   : w_k^(1/k) = {mp.nstr(r1[0],8)}  -> R = 1 ;  Gamma_k = {mp.nstr(r1[1],8)}"
      f"  (= k+2 = {1024+2}, DIVERGES)")
print(f"  family C: w_k^(1/k) = {mp.nstr(r2[0],8)}  -> R = 1 ;  Gamma_k = {mp.nstr(r2[1],8)}"
      f"  (CONVERGES)")
same_R = abs(r1[0]-1) < mp.mpf("0.02") and abs(r2[0]-1) < mp.mpf("0.02")
split   = r1[1] > 1000 and r2[1] < 10
print()
print(f"  both have R = 1 : {same_R}")
print(f"  Gamma splits    : {split}")
print(f"  => 'R >= 1 is exactly the statement that Gamma is finite' is "
      f"{'REFUTED' if (same_R and split) else 'NOT refuted by this test'}")
print()
print("  The true statement:  R > 1  =>  Gamma finite;   Gamma finite  =>  R >= 1;")
print("                       R = 1  =>  undecided, and BOTH cases occur.")
print("  Note the surviving direction is the one prop:nopinch actually uses (R > 1),")
print("  so the proposition's own consequence (item 3, fair coin interior iff R>1) is untouched.")
