#!/usr/bin/env python3
"""
leeyang6_r194 -- Track M, rung 1 (numerical).

QUESTION (fable-5, r192 sec.2 rung 1): on Re q = 1/2 the object is real-valued,
    Gamma^(q)_k = 1 + 2 Re G_k(1+2it),
so a sign change in t IS a zero on the line.  Rung 1 asks (a) do the near-1/2 zeros sit
EXACTLY ON the line, and (b) do their positions match the ladder (2n+1)pi/(2k)?
STOPPING RULE (fable's): if they sit off the line, stop and report.

PRE-REGISTERED BEFORE RUNNING (F45/F30/C-2):

 P1 Closed form.  z = 1+2it, z-1 = 2it, S_k := sum_{j=1}^{k-1} z^j = (z^k - z)/(2it);
    with rho=|z|=sqrt(1+4t^2), theta=arg z=atan(2t) and rho sin theta = 2t,
        Re S_k = rho^k sin(k theta)/(2t) - 1.
    F-1: closed form vs direct summation differ by > 1e-25 relative => algebra wrong, stop.

 P2 On the line.  #sign changes of f_k(t)=1+2 Re G_k(1+2it) on 0<t<r, versus the argument-
    principle count of ALL complex zeros of q -> Gamma^(q)_k in |q-1/2|<r.
    Predicted: (zeros in disc) == 2*(sign changes on t>0)   [f is even in t; t=0 not a zero].
    F-2: counts disagree => zeros OFF the line => STOP AND REPORT.  This is the rung's reason
    for existing, and it is the falsifier that can kill the design.

 P3 Ladder.  k*t_n/pi -> (2n+1)/2 = 0.5, 1.5, 2.5, ...
    F-3: k*t_n/pi does not settle on half-odd-integers as k grows.

 P4 Negative control.  Odds have R=2 and prop:nopinch proves |q-1/2|<1/6 zero-free, uniformly
    in k.  F-4: any zero there => prop:nopinch false or this script wrong; stop either way.

CONVENTION (stated because the count depends on it, F80): m_0=(a_1-1)/2,
m_j=(a_{j+1}-a_j)/2, w_j=m_j 2^{-j}, G_k(z)=sum_{j=0}^{k-1} w_j z^j,
Gamma^(q)=1+G(2q)+G(2-2q).  k = number of terms of G_k.
"""
import mpmath as mp
mp.mp.dps = 30

def weights(a):
    m = [mp.mpf(a[0]-1)/2] + [mp.mpf(a[j]-a[j-1])/2 for j in range(1, len(a))]
    return [m[j]/mp.mpf(2)**j for j in range(len(m))]

def odds(k):      return [2*i-1 for i in range(1, k+1)]          # R=2  (control)
def lac_plus(k):  return [2**i+1 for i in range(1, k+1)]         # R=1  w=(1,1/2,1/2,...)
def lac_minus(k): return [2**i-1 for i in range(1, k+1)]         # R=1  w=(0,1/2,1/2,...)
def layer_c2(k):                                                  # R=1  w=(1,1,1,...)
    a=[3]
    for j in range(1, k): a.append(a[-1] + 2*2**j)
    return a

FAM = [("odds       R=2 CONTROL", odds),
       ("2^i+1      R=1", lac_plus),
       ("2^i-1      R=1", lac_minus),
       ("layer c=2  R=1", layer_c2)]

def G(w, z):
    s = mp.mpf(0)
    for c in reversed(w): s = s*z + c
    return s

def gamma_q(w, q):  return 1 + G(w, 2*q) + G(w, 2-2*q)
def f_line(w, t):   return mp.re(1 + 2*G(w, mp.mpc(1, 2*t)))

def re_S_closed(k, t):
    rho = mp.sqrt(1+4*t**2); th = mp.atan(2*t)
    return rho**k * mp.sin(k*th)/(2*t) - 1

def check_P1():
    worst = mp.mpf(0)
    for k in (8,17,33,64,129):
        for t in (mp.mpf("0.001"), mp.mpf("0.01"), mp.mpf("0.05"),
                  mp.pi/(2*k), 3*mp.pi/(2*k)):
            z = mp.mpc(1, 2*t)
            direct = mp.re(sum(z**j for j in range(1,k)))
            closed = re_S_closed(k, t)
            worst = max(worst, abs(direct-closed)/max(abs(direct), mp.mpf(1)))
    return worst

def sign_changes(w, tmax, npts=2000):
    out=[]; pt = mp.mpf(tmax)/npts; pv = f_line(w, pt)
    for i in range(2, npts+1):
        t = mp.mpf(tmax)*i/npts; v = f_line(w, t)
        if mp.sign(v) != mp.sign(pv) and v != 0:
            out.append(mp.findroot(lambda s: f_line(w,s), (pt,t), solver="bisect",
                                   tol=mp.mpf(10)**-25))
        pt, pv = t, v
    return out

def zeros_in_disc(w, r, npts=2000):
    tot = mp.mpf(0); prev=None
    for i in range(npts+1):
        q = mp.mpf("0.5") + r*mp.exp(2j*mp.pi*mp.mpf(i)/npts)
        a = mp.arg(gamma_q(w, q))
        if prev is not None:
            d = a-prev
            while d >  mp.pi: d -= 2*mp.pi
            while d < -mp.pi: d += 2*mp.pi
            tot += d
        prev = a
    return tot/(2*mp.pi)

print("="*80)
print("leeyang6_r194 -- Track M rung 1: are the near-1/2 zeros ON the critical line?")
print("="*80)
w1 = check_P1()
print(f"\n[P1] Re S_k = rho^k sin(k theta)/(2t) - 1  vs direct sum, 25 (k,t) points")
print(f"     worst relative discrepancy : {mp.nstr(w1,5)}")
print(f"     F-1 (>1e-25) : {'FIRED -- STOP' if w1 > mp.mpf('1e-25') else 'not fired'}")

for name, prof in FAM:
    print("\n" + "-"*80); print(f"family: {name}")
    for k in (16, 32, 64):
        w = weights(prof(k)); r = mp.mpf(4)/k
        roots = sign_changes(w, r)
        nz = zeros_in_disc(w, r); nzr = int(mp.nint(nz))
        ok = (nzr == 2*len(roots))
        print(f"  k={k:3d} r={mp.nstr(r,4):>7}  on-line sign changes(t>0): {len(roots):2d}"
              f"  arg-principle in disc: {mp.nstr(nz,10):>13} -> {nzr:2d}"
              f"   {'MATCH' if ok else '*** MISMATCH: OFF-LINE ZEROS -- F-2 FIRED ***'}")
        for n,t in enumerate(roots):
            print(f"       t_{n} = {mp.nstr(t,12):>16}  k*t/pi = {mp.nstr(k*t/mp.pi,10):>13}"
                  f"   ladder (2n+1)/2 = {(2*n+1)/2}")

print("\n" + "-"*80)
print("[P4] negative control: odds, prop:nopinch says |q-1/2| < 1/6 is zero-free")
for k in (16,32,64,128):
    nz = zeros_in_disc(weights(odds(k)), mp.mpf(1)/6)
    print(f"  k={k:3d}  zeros in |q-1/2|<1/6 : {mp.nstr(nz,8):>13}"
          f"   {'ok (zero-free)' if abs(nz) < mp.mpf('1e-6') else '*** F-4 FIRED ***'}")
print("\ndone.")
