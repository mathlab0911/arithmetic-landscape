#!/usr/bin/env python3
"""
r096 / the fork opened by p3_r096: P3's derivation yields Phi's term times a
LAMBDA-INDEPENDENT Gaussian factor  c_d = exp(-delta_d^2 / (2 V_d))  that the printed Phi
omits.  How much of Table 1's residual is it?   Phi_g := 1 + SUM w_d c_d e^{-l^2 s_d/8} cosh(l de).
Conservative branch (per the completion protocol) is to keep Phi and account for c_d in E_k;
this measures what that costs.
"""
import math, numpy as np
_s = open('alpha_r092.py').read().split("print('=' * 108)")[0]
def odd_primes(k):
    out, n = [], 3
    while len(out) < k:
        if all(n % p for p in range(3, int(n ** .5) + 1, 2)): out.append(n)
        n += 2
    return out
_ns = {}; exec(compile(_s, 'alpha_r092.py', 'exec'), _ns); globals().update(_ns)

def Phi_g(A, lam, use_c):
    A = sorted(A); k = len(A); D = (A[-1]-1)//2
    S2 = sum(a*a for a in A)
    tot = 1.0; j = 0; sig = 0; s2s = 0
    for d in range(1, D+1):
        while j < k and A[j] <= 2*d:
            sig += A[j]; s2s += A[j]*A[j]; j += 1
        w = 2.0**(1-j)
        if w < 1e-18: break
        de = d + sig/2.0
        arg = lam*de
        if abs(arg) > 700: break
        Vd = (S2 - s2s)/4.0
        c = math.exp(-de*de/(2*Vd)) if use_c else 1.0
        tot += w*c*math.exp(-lam*lam*s2s/8.0)*math.cosh(arg)
    return tot

RH = [0.44, 0.40, 0.30, 0.20]
print("Table-1 residual (fraction of the centred signal): Phi as printed  vs  Phi with c_d")
print(f"  {'ens':>10} {'k':>5} {'variable':>12} " + "".join(f"   x={0.5-r:.2f}" for r in RH))
for nm, f, ks in (('odds', lambda k: [2*i+1 for i in range(k)], (180, 220)),
                  ('primes', odd_primes, (180, 220)),
                  ('a=3/2', lambda k: pow_profile(k, 1.5), (180, 220))):
    for k in ks:
        A = sorted(f(k)); m = measured(A, RH)
        for tag, uc in (('Phi', False), ('Phi with c_d', True)):
            r0, l0 = m[0.5]; p0 = Phi_g(A, l0, uc)
            cells = []
            for r in RH:
                rm, lam = m[r]; pp = Phi_g(A, lam, uc)
                cells.append(f"  {abs(((rm-pp)-(r0-p0))/(rm-r0))*100:6.3f}%")
            print(f"  {nm:>10} {k:5d} {tag:>12} " + "".join(cells))
    print()
