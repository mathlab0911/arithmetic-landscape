#!/usr/bin/env python3
"""
leeyang7_r194 -- Track M rung 1b: the ladder, measured over MORE THAN ONE RUNG.

r194's rung-1a run found the recorded ladder "(2n+1)pi/(2k)" fits t_0 and NOT t_1
(k*t_1/pi came out ~1.00, not 1.5).  F27: a ladder is a claim about a range, and one
rung is not a range.  This script measures many rungs and tests the corrected law.

DERIVATION being tested (paper algebra, r194):
    z = 1+2it, rho=|z|, theta=arg z=atan(2t);  S_k = sum_{j=1}^{k-1} z^j = (z^k-z)/(2it)
    => Re S_k = rho^k sin(k theta)/(2t) - 1.
  family 2^i-1  (w_0=0, w_j=1/2): Gamma^(q)_k = 1 + Re S_k = rho^k sin(k theta)/(2t)
        => zeros EXACTLY at sin(k theta)=0, i.e. theta_n = n pi / k, all integers n>=1.
  family 2^i+1  (w_0=1, w_j=1/2): Gamma^(q)_k = 2 + rho^k sin(k theta)/(2t)
        => zeros at sin(k theta) = -4t/rho^k -> 0, so theta_n -> n pi / k too.
  family layer c=2 (w_j=1):       Gamma^(q)_k = 1 + 2 Re S_k = 2 rho^k sin(k theta)/(2t) - 1
        => sin(k theta) = t/rho^k -> 0, same limit ladder.

PRE-REGISTERED:
 Q1  For 2^i-1 the zeros are EXACT: k*theta_n/pi must equal integer n to 1e-20.
     FALSIFIER: any deviation > 1e-20  => the closed form is wrong.
 Q2  For the other two families k*theta_n/pi -> n, error shrinking with k.
     FALSIFIER: error does not shrink, or converges to n+1/2.
 Q3  The RECORDED law "t_n = (2n+1)pi/(2k), odd multiples only" is tested head-on:
     if the measured k*theta_n/pi hits BOTH parities, the recorded law is refuted.
 Q4  Off-line control at larger radius: does the arg-principle count keep matching
     2 * (on-line sign changes) as r grows?  Where it stops matching, off-line zeros begin,
     and that boundary is itself a measurement worth printing.
"""
import mpmath as mp
mp.mp.dps = 40

def weights(a):
    m = [mp.mpf(a[0]-1)/2] + [mp.mpf(a[j]-a[j-1])/2 for j in range(1, len(a))]
    return [m[j]/mp.mpf(2)**j for j in range(len(m))]
def lac_plus(k):  return [2**i+1 for i in range(1, k+1)]
def lac_minus(k): return [2**i-1 for i in range(1, k+1)]
def layer_c2(k):
    a=[3]
    for j in range(1,k): a.append(a[-1]+2*2**j)
    return a
def G(w,z):
    s=mp.mpf(0)
    for c in reversed(w): s=s*z+c
    return s
def gamma_q(w,q): return 1 + G(w,2*q) + G(w,2-2*q)
def f_line(w,t):  return mp.re(1 + 2*G(w, mp.mpc(1,2*t)))

def roots_on_line(w, tmax, npts=20000):
    out=[]; pt=mp.mpf(tmax)/npts; pv=f_line(w,pt)
    for i in range(2,npts+1):
        t=mp.mpf(tmax)*i/npts; v=f_line(w,t)
        if mp.sign(v)!=mp.sign(pv) and v!=0:
            out.append(mp.findroot(lambda s: f_line(w,s), (pt,t), solver="bisect",
                                   tol=mp.mpf(10)**-30))
        pt,pv=t,v
    return out

def zeros_in_disc(w,r,npts=3000):
    tot=mp.mpf(0); prev=None
    for i in range(npts+1):
        q=mp.mpf("0.5")+r*mp.exp(2j*mp.pi*mp.mpf(i)/npts)
        a=mp.arg(gamma_q(w,q))
        if prev is not None:
            d=a-prev
            while d> mp.pi: d-=2*mp.pi
            while d<-mp.pi: d+=2*mp.pi
            tot+=d
        prev=a
    return tot/(2*mp.pi)

print("="*84)
print("leeyang7_r194 -- the ladder, over many rungs.   theta = arctan(2t),  test k*theta/pi")
print("="*84)

FAM=[("2^i-1     (w0=0, w=1/2)  EXACT case", lac_minus),
     ("2^i+1     (w0=1, w=1/2)",             lac_plus),
     ("layer c=2 (w=1)",                     layer_c2)]

for name,prof in FAM:
    print("\n"+"-"*84); print(f"family: {name}")
    for k in (32,64,128):
        w=weights(prof(k))
        tmax=mp.tan(mp.mpf(6)*mp.pi/k)/2 if 6*mp.pi/k < mp.pi/2 else mp.mpf("0.4")
        rr=roots_on_line(w,tmax)
        vals=[k*mp.atan(2*t)/mp.pi for t in rr]
        print(f"  k={k:4d}  tmax={mp.nstr(tmax,5):>9}  rungs found: {len(rr)}")
        print(f"        k*theta_n/pi = " + ", ".join(mp.nstr(v,9) for v in vals[:8]))
        errs=[abs(v-mp.nint(v)) for v in vals[:8]]
        print(f"        |dev from nearest integer| max = {mp.nstr(max(errs),4) if errs else 'n/a'}"
              f"   nearest ints = {[int(mp.nint(v)) for v in vals[:8]]}")
        halferr=[abs(v-(mp.nint(v-mp.mpf('0.5'))+mp.mpf('0.5'))) for v in vals[:8]]
        print(f"        |dev from nearest HALF-odd|    = {mp.nstr(min(halferr),4) if halferr else 'n/a'}"
              f"   (recorded law predicted these)")

print("\n"+"-"*84)
print("[Q4] where do off-line zeros begin?  disc count vs 2*(on-line sign changes), k=64")
w=weights(lac_minus(64))
for rnum in (2,4,8,16,32,64):
    r=mp.mpf(rnum)/64
    if r>=mp.mpf("0.49"): continue
    nl=len(roots_on_line(w,r))
    nz=zeros_in_disc(w,r); nzr=int(mp.nint(nz))
    print(f"  r={mp.nstr(r,5):>9}  on-line(t>0): {nl:3d}   disc total: {nzr:3d}"
          f"   {'all on line' if nzr==2*nl else f'*** {nzr-2*nl} OFF-LINE ***'}")
print("\ndone.")
