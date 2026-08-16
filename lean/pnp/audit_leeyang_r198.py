#!/usr/bin/env python3
"""
audit_leeyang_r198 -- systematic audit of EVERY quantitative claim in Part III's Lee-Yang section.

WHY.  Two errors were found there in two rounds, both by accident while doing something else
(r195: cos for sin; r197: R>=1 <=> Gamma finite).  F35: when one claim is found over-claiming,
that is evidence about the others -- check them the same hour.  This is not a referee pass
(that needs fresh context, which the author does not have); it is the mechanical check that
caught both errors, run over the whole section instead of opportunistically.

CLAIMS UNDER AUDIT, each with the falsifier stated:
 A1 cor:oddsclosed   For the odd numbers G(z)=z/(2-z) and Gamma^(q) = 1/(q(1-q)) - 1.
                     FALSIFIER: finite-k sum does not converge to that off the poles.
 A2 rem:leeyang      The odd numbers' zeros pinch the ENDPOINTS q=0,1 at rate 2 pi / k.
                     Paper algebra: q(1-q)Gamma^(q)_k = q^2-q+1-q^{k+1}-(1-q)^{k+1}, so with
                     q=u/k the condition is e^{-u}=1, giving u = 2 pi i n.  Spacing 2pi/k.
                     FALSIFIER: k*|Im q_1| near 0 does not approach 2 pi.
                     NOTE this is the number that must NOT be pi/k: the endpoint is a single
                     section (e^{ik theta}), the fair coin is a conjugate SUM (sin(k theta)),
                     and the factor 2 between them is the whole corrected fingerprint.  If the
                     endpoint also measured pi/k, the r195 correction would be wrong.
 A3 prop:nopinch     r = 1/6 proved for the odds; Gamma(A) >= 3 - 2^{2-k}.
                     FALSIFIER: a zero inside |q-1/2| < 1/6, or Gamma below the bound.
 A4 rem:pinchformula dist -> 1/c - 1/2 for layer gaps 2c^j; the k=70 table.
                     FALSIFIER: the published row is not reproduced.
 A5 rem:qcrit        Q(0) exists iff c < 2^{1/3} = 1.259921.  (constant only)
"""
import mpmath as mp
mp.mp.dps = 30

def G_odds(z, k):    # m_0 = 0, m_j = 1  =>  w_j = 2^-j
    s = mp.mpf(0)
    for j in range(k-1, 0, -1): s = (s + 1)*z/2
    return s
def gq_odds(q, k):   return 1 + G_odds(2*q, k) + G_odds(2-2*q, k)

print("="*84); print("audit_leeyang_r198"); print("="*84)

print("\n[A1] cor:oddsclosed : Gamma^(q)_k -> 1/(q(1-q)) - 1 ?")
worst = mp.mpf(0)
for q in (mp.mpf("0.5"), mp.mpf("0.3"), mp.mpc("0.5","0.1"), mp.mpc("0.4","-0.2")):
    lim = 1/(q*(1-q)) - 1
    v = gq_odds(q, 400)
    worst = max(worst, abs(v-lim))
    print(f"   q={str(q):>14}   limit={mp.nstr(lim,10):>20}   k=400 value={mp.nstr(v,10):>20}")
print(f"   worst |difference| = {mp.nstr(worst,5)}   "
      f"{'*** A1 FIRED ***' if worst > mp.mpf('1e-20') else 'closed form confirmed'}")
print(f"   and at q=1/2: 1/(1/4)-1 = 3 = Gamma(odds).  measured {mp.nstr(gq_odds(mp.mpf('0.5'),400),10)}")

print("\n[A2] rem:leeyang : endpoint pinch rate.  Must be 2*pi/k, NOT pi/k.")
def endpoint_eq(q, k):   # q^2 - q + 1 - q^{k+1} - (1-q)^{k+1}
    return q**2 - q + 1 - q**(k+1) - (1-q)**(k+1)
print(f"   {'k':>6}{'first zero q_1 near 0':>34}{'k*|Im q_1|':>14}   2pi={mp.nstr(2*mp.pi,8)}")
for k in (32,64,128,256):
    r = mp.findroot(lambda q: endpoint_eq(q,k), mp.mpc(0, 2*mp.pi/k))
    chk = abs(gq_odds(r,k)*r*(1-r))
    print(f"   {k:>6}{mp.nstr(r,10):>34}{mp.nstr(k*abs(mp.im(r)),9):>14}"
          f"   |q(1-q)Gamma^(q)| there = {mp.nstr(chk,3)}")
print("   -> endpoints 2pi/k (single section), fair coin pi/k (conjugate sum): factor 2 = the fold.")

print("\n[A3] prop:nopinch : Gamma(odds) >= 3 - 2^(2-k) ?")
for k in (8,16,32,64):
    G = gq_odds(mp.mpf("0.5"), k); bound = 3 - mp.mpf(2)**(2-k)
    print(f"   k={k:3d}  Gamma_k={mp.nstr(G,12):>16}  bound 3-2^(2-k)={mp.nstr(bound,12):>16}"
          f"   {'ok' if G >= bound - mp.mpf('1e-25') else '*** A3 FIRED ***'}")

print("\n[A4] rem:pinchformula : layer gaps 2c^j, dist -> 1/c - 1/2, published table at k=70")
def gq_layer(q, k, c):
    w = [mp.mpf(c)**j/mp.mpf(2)**j for j in range(k)]
    def G(z):
        s = mp.mpf(0)
        for a in reversed(w): s = s*z + a
        return s
    return 1 + G(2*q) + G(2-2*q)
def dist_layer(k, c, rmax=mp.mpf("0.95"), n=3000):
    pt = rmax/n; pv = mp.re(gq_layer(mp.mpf("0.5")+1j*pt, k, c))
    for i in range(2, n+1):
        t = rmax*i/n; v = mp.re(gq_layer(mp.mpf("0.5")+1j*t, k, c))
        if mp.sign(v) != mp.sign(pv) and v != 0:
            return mp.findroot(lambda u: mp.re(gq_layer(mp.mpf("0.5")+1j*u,k,c)), (pt,t),
                               solver="bisect", tol=mp.mpf(10)**-20)
        pt, pv = t, v
    return None
print(f"   {'c':>6}{'predicted 1/c-1/2':>20}{'measured k=70':>16}{'ratio':>10}   published")
pub = {"1.00":"0.503895","1.10":"0.413403","1.25":"0.305147","1.40":"0.220690",
       "1.60":"0.133982","1.80":"0.070741","2.00":"0.022306"}
for cs in ("1.00","1.10","1.25","1.40","1.60","1.80","2.00"):
    c = mp.mpf(cs); d = dist_layer(70, c); p = 1/c - mp.mpf("0.5")
    if d is None: print(f"   {cs:>6}{mp.nstr(p,7):>20}{'none':>16}{'--':>10}   {pub[cs]}"); continue
    ok = abs(d - mp.mpf(pub[cs])) < mp.mpf("1e-5")
    print(f"   {cs:>6}{mp.nstr(p,7):>20}{mp.nstr(d,7):>16}"
          f"{mp.nstr(d/p,6) if p!=0 else '--':>10}   {pub[cs]} {'MATCH' if ok else '*** DIFFERS ***'}")

print(f"\n[A5] rem:qcrit : 2^(1/3) = {mp.nstr(mp.mpf(2)**(mp.mpf(1)/3),10)}  (paper prints 1.259921)")
print("\ndone.")
