#!/usr/bin/env python3
"""
r092 / audit of the section-6 axis.  alpha_r092 shows the (H) SERIES IS BOUNDED for cubes
(1.112e7, k-independent) -- so "cubes fail (H)" as (H) is written in spec_t3rigid_r087 is
not what the measurement says.  Question: does the cube residual follow c_A/k or not?
Falsifier for "cubes are fine after all": if k*R settles to a constant near
(2a+1)^2/(4a+1) = 49/13 = 3.769, the cube counterexample needs restating.
"""
import math, numpy as np
import importlib.util, sys
_s = open('alpha_r092.py').read().split("print('=' * 108)")[0]
_ns = {}
exec(compile(_s, 'alpha_r092.py', 'exec'), _ns)
globals().update(_ns)
for al, name in ((3.0, 'cubes a=3'), (2.0, 'squares a=2')):
    pr = (2*al+1)**2/(4*al+1)
    print(f"\n  {name}   prediction (2a+1)^2/(4a+1) = {pr:.4f}")
    print(f"    {'k':>4} {'N':>8} {'k*S4/S2^2':>11} {'k(s/lam-1)':>12} {'c_A=k*R':>10} {'(H)':>11}")
    for k in (16, 20, 24, 28, 32, 36, 40):
        A = sorted(pow_profile(k, al))
        if A[-1] > 70000: continue
        m = measured(A, [0.44, 0.40])
        r0, l0 = m[0.5]; p0 = Phi(A, l0)
        rm, lam = m[0.40]; lam = abs(lam)
        s = tilt(A, 0.40); pp = Phi(A, lam)
        cA = abs(((rm-pp)-(r0-p0))/(rm-r0))*k
        a = np.asarray(A, float)
        s4 = float((a**4).sum())/float((a**2).sum())**2
        H, W = Hstats(A)
        print(f"    {k:4d} {A[-1]:8d} {k*s4:11.4f} {k*(s/lam-1):12.4f} {cA:10.4f} {H:11.4g}")
