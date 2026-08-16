#!/usr/bin/env python3
"""audit3_r198 -- A4: rem:pinchformula's k=70 table, by ALL roots rather than by scanning,
plus a stability check on the recomputation itself.
Gamma^(q)_k = 1 + sum_{j=0}^{k-1}[(cq)^j + (c(1-q))^j] for layer gaps 2c^j (m_j = c^j).
FALSIFIER: the published measured row is not reproduced.  It is not -- but see the stability
check: at c=1.80 the recomputation is itself unstable below 40 digits, so the disagreement is
about method, not about a wrong number."""
import mpmath as mp
def coeffs(k,c):
    c=mp.mpf(c); a=[mp.mpf(0)]*k
    for j in range(k):
        a[j]+=c**j; cj=c**j
        for i in range(j+1): a[i]+=cj*mp.binomial(j,i)*(-1)**i
    a[0]+=1; a=list(reversed(a))
    while a and a[0]==0: a.pop(0)
    return a
def dist(k,c,dps=40,ep=900):
    mp.mp.dps=dps
    r=mp.polyroots(coeffs(k,c),maxsteps=600,extraprec=ep)
    return min(abs(x-mp.mpf("0.5")) for x in r)
pub={"1.00":"0.503895","1.10":"0.413403","1.25":"0.305147","1.40":"0.220690",
     "1.60":"0.133982","1.80":"0.070741","2.00":"0.022306"}
mp.mp.dps=40
print("="*86); print("audit3_r198 -- rem:pinchformula, k=70, every root found (F60: not a scan)"); print("="*86)
print(f"\n{'c':>6}{'predicted 1/c-1/2':>20}{'recomputed':>15}{'published':>12}{'ratio':>9}  verdict")
bad=0
for cs in ("1.00","1.10","1.25","1.40","1.60","1.80","2.00"):
    c=mp.mpf(cs); d=dist(70,cs); mp.mp.dps=40; p=1/c-mp.mpf("0.5")
    ok=abs(d-mp.mpf(pub[cs]))<mp.mpf("5e-6"); bad+= (not ok)
    print(f"{cs:>6}{mp.nstr(p,7):>20}{mp.nstr(d,7):>15}{pub[cs]:>12}"
          f"{(mp.nstr(d/p,6) if p!=0 else '--'):>9}  {'MATCH' if ok else '*** DIFFERS ***'}")
print(f"\n  rows differing from the published table: {bad} of 7")
print("\nstability of the recomputation itself (is MY number the precision-limited one?)")
for cs in ("1.80","2.00","1.00"):
    vals=[dist(70,cs,d,e) for d,e in ((30,600),(40,900),(60,1500))]
    mp.mp.dps=40
    print(f"  c={cs}  dps30={mp.nstr(vals[0],10)}  dps40={mp.nstr(vals[1],10)}  dps60={mp.nstr(vals[2],10)}"
          f"   spread={mp.nstr(max(vals)-min(vals),4)}")
mp.mp.dps=40
print(f"\n  [A5] rem:qcrit constant 2^(1/3) = {mp.nstr(mp.mpf(2)**(mp.mpf(1)/3),10)}  (paper prints 1.259921)")
