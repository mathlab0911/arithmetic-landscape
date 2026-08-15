#!/usr/bin/env python3
"""r094 / the alpha = 3/2 row of Table 1, on the same x-grid as the other three."""
import math, numpy as np
_s = open('alpha_r092.py').read().split("print('=' * 108)")[0]
_ns = {}; exec(compile(_s, 'alpha_r092.py', 'exec'), _ns); globals().update(_ns)
RH = [0.44, 0.42, 0.40, 0.35, 0.30, 0.25, 0.20]
print("Table 1, residual as a fraction of the CENTRED signal")
print("     x = " + "".join(f"  {0.5-r:5.2f}" for r in RH))
for name, al, ks in (('a=3/2', 1.5, (140, 180, 220)),):
    for k in ks:
        A = sorted(pow_profile(k, al)); m = measured(A, RH)
        r0, l0 = m[0.5]; p0 = Phi(A, l0)
        cells, kr = [], []
        for r in RH:
            rm, lam = m[r]; pp = Phi(A, lam)
            v = abs(((rm-pp)-(r0-p0))/(rm-r0))*100
            cells.append(f"  {v:5.2f}%"); kr.append(v*k)
        print(f"  {name} k={k:3d} " + "".join(cells))
        print(f"     k*R    " + "".join(f"  {v:6.1f}" for v in kr))
    A = sorted(pow_profile(220, al))
    print(f"\n  a_1 = {A[0]}, N = a_k = {A[-1]}, |A| = {len(A)}, T = {sum(A)}")
    print(f"  Phi(0) = {Phi(A,0.0):.6f}   Gamma = {float(sum(a/2**(j+1) for j,a in enumerate(A))):.6f}")
