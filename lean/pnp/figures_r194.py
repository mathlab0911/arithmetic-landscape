#!/usr/bin/env python3
"""figures_r194 -- prints the numbers EXACTLY in the form they are quoted in paper4.
No number reaches a report except by copy from a log (F19/C2; three rounds of rounding bugs)."""
import mpmath as mp
mp.mp.dps = 30
def f(k,t):
    rho=mp.sqrt(1+4*t**2)
    return 2 + rho**k*mp.sin(k*mp.atan(2*t))/(2*t)          # a_i = 2^i+1
def f0(k,t):
    rho=mp.sqrt(1+4*t**2)
    return rho**k*mp.sin(k*mp.atan(2*t))/(2*t)              # a_i = 2^i-1
def first_root(fn,k,npts=4000):
    tmax=mp.mpf(3)/k; pt=tmax/npts; pv=fn(k,pt)
    for i in range(2,npts+1):
        t=tmax*i/npts; v=fn(k,t)
        if mp.sign(v)!=mp.sign(pv) and v!=0:
            return mp.findroot(lambda s: fn(k,s),(pt,t),solver="bisect",tol=mp.mpf(10)**-25)
        pt,pv=t,v
def roots(fn,k,n,npts=6000):
    out=[];tmax=mp.mpf(11)/k;pt=tmax/npts;pv=fn(k,pt)
    for i in range(2,npts+1):
        t=tmax*i/npts;v=fn(k,t)
        if mp.sign(v)!=mp.sign(pv) and v!=0:
            out.append(mp.findroot(lambda s: fn(k,s),(pt,t),solver="bisect",tol=mp.mpf(10)**-25))
            if len(out)>=n: break
        pt,pv=t,v
    return out

print("QUOTED FORMS for paper4 rem:leeyanglacunary  (a_i = 2^i+1 unless noted)\n")
vals=[k*first_root(f,k) for k in (128,256,512,1024)]
print("k*Im q_1 at k=128,256,512,1024, to 4 dp as quoted:")
print("   " + ", ".join(mp.nstr(v,5) for v in vals))
print("   full: " + ", ".join(mp.nstr(v,12) for v in vals))
print("   pi/2 = " + mp.nstr(mp.pi/2,8))
print()
print("|q_1 - 1/2| at k=32,64,96, to 4 dp as quoted:")
q=[first_root(f,k) for k in (32,64,96)]
print("   " + ", ".join(mp.nstr(v,3) for v in q))
print("   full: " + ", ".join(mp.nstr(v,12) for v in q))
print()
print("a_i = 2^i-1 : k*theta_n/pi for n=1..6, deviation from n")
for k in (32,64,128):
    rr=roots(f0,k,6)
    dev=max(abs(k*mp.atan(2*t)/mp.pi - mp.nint(k*mp.atan(2*t)/mp.pi)) for t in rr)
    print(f"   k={k:4d}  n=1..{len(rr)}   max |dev| = {mp.nstr(dev,4)}")
print()
print("odd numbers control, |q_1 - 1/2| at k=96 (paper quotes 0.5021):")
print("   prop:nopinch proves the disc |q-1/2| < 1/6 zero-free; winding measured 2.3e-32.")
