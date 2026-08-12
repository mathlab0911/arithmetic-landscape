# r1hermite_r137.py -- the Hermite bookkeeping, and a check that can actually fail.
#
# THE DERIVATION.  With psi(u) = E[e^{iu(S-mu)}], t = sigma u, z = (m-mu)/sigma,
#
#   P[S=m] = (1/(2 pi sigma)) int psi(t/sigma) e^{-izt} dt
#
# On R1, with alpha = K3/sigma^3 and beta = K4/sigma^4 (both dimensionless),
#
#   log psi(t/sigma) = -t^2/2 - i alpha t^3/6 + beta t^4/24 + R5(t)
#   psi(t/sigma)     = e^{-t^2/2} [ 1 - i alpha t^3/6 + beta t^4/24 - alpha^2 t^6/72 + ... ] e^{R5}
#
# the third bracket term being (1/2)(-i alpha t^3/6)^2 = -alpha^2 t^6/72.
#
# THE INVERSION IDENTITY.  Differentiating (1/2 pi) int e^{-t^2/2} e^{-izt} dt = phi(z) j times
# in z brings down (-it)^j, and d^j phi/dz^j = (-1)^j He_j(z) phi(z).  Hence
#
#        (1/2 pi) int e^{-t^2/2} (it)^j e^{-izt} dt  =  He_j(z) phi(z) .          (*)
#
# Now  (it)^3 = -i t^3,  (it)^4 = t^4,  (it)^6 = -t^6, so the three bracket terms are
#   -i alpha t^3/6 = (alpha/6)(it)^3 ,  beta t^4/24 = (beta/24)(it)^4 ,
#   -alpha^2 t^6/72 = (alpha^2/72)(it)^6 ,
# and (*) turns them into (alpha/6)He3, (beta/24)He4, (alpha^2/72)He6.  That is the display.
#
# TWO CHECKS.  (1) the identity (*) itself, numerically.  (2) the assembled expansion against
# exact dynamic programming AT SEVERAL z -- the mean alone cannot test the He3 term, because
# He3(0) = 0.  This is the check the earlier rounds could not do.
import math, cmath
from r1budget_r133 import profile, solve_s, cumulants

def tilt(a, s): return 1.0/(1.0+math.exp(min(700.0, s*a)))
def He(n, z):
    return {3: z**3-3*z, 4: z**4-6*z*z+3, 6: z**6-15*z**4+45*z*z-15}[n]
def phi(z): return math.exp(-0.5*z*z)/math.sqrt(2*math.pi)

print('CHECK 1: (1/2pi) int e^{-t^2/2}(it)^j e^{-izt} dt  =  He_j(z) phi(z)')
print('  %3s %7s %15s %15s %10s' % ('j', 'z', 'numeric', 'He_j(z)phi(z)', 'rel err'))
bad1 = 0
for j in (3, 4, 6):
    for z in (0.0, 0.7, 1.5, -1.2):
        Tmax = 14.0; M = 40000; acc = 0j
        for i in range(M+1):
            t = -Tmax + 2*Tmax*i/M
            w = 1.0 if 0 < i < M else 0.5
            acc += w*math.exp(-0.5*t*t)*(1j*t)**j*cmath.exp(-1j*z*t)
        acc *= (2*Tmax/M)/(2*math.pi)
        pred = He(j, z)*phi(z)
        # He3(0) = 0 exactly, so a RELATIVE error there is 0/0 and prints garbage.  Report the
        # absolute error when the prediction vanishes -- a check must not manufacture its own
        # false alarms (F58).
        if abs(pred) < 1e-12:
            err = abs(acc); kind = 'abs'
        else:
            err = abs(acc - pred)/abs(pred); kind = 'rel'
        if err > 1e-6: bad1 += 1
        print('  %3d %7.2f %15.8e %15.8e %10.2e %-3s %s'
              % (j, z, acc.real, pred, err, kind, '' if err < 1e-6 else '*** MISMATCH ***'))
print('  identity failures: %d' % bad1)
print()

def exact_pmf(B, s):
    T = sum(B); f = [0.0]*(T+1); f[0] = 1.0
    for a in B:
        p = tilt(a, s); g = [0.0]*(T+1)
        for m in range(T+1):
            v = f[m]
            if v == 0.0: continue
            g[m] += v*(1-p)
            if m+a <= T: g[m+a] += v*p
        f = g
    return f

print('CHECK 2: the assembled expansion against exact DP, AT SEVERAL z.')
print('        He3 vanishes at the mean, so only z != 0 tests the third-cumulant term.')
for name in ('odds', 'primes'):
    for k in (48, 64, 80):
        A = profile(name, k); T = sum(A); n = int(0.44*T)
        s = solve_s(A, n); B = [a for a in A if a > 2]
        mu, K2, K3, K4 = cumulants(B, s); sg = math.sqrt(K2)
        al = K3/sg**3; be = K4/sg**4
        f = exact_pmf(B, s)
        print('  %s k=%d  alpha=%+.4e  beta=%+.4e' % (name, k, al, be))
        print('    %7s %6s %13s %13s %11s %11s %10s'
              % ('z', 'm', 'exact', 'Edgeworth', 'gauss err', 'edge err', 'k^1.5*err'))
        for zt in (-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0):
            m = int(round(mu + zt*sg))
            if m < 0 or m >= len(f) or f[m] == 0: continue
            z = (m-mu)/sg
            g0 = phi(z)/sg
            ed = g0*(1 + (al/6)*He(3,z) + (be/24)*He(4,z) + (al*al/72)*He(6,z))
            print('    %7.3f %6d %13.6e %13.6e %11.3e %11.3e %10.4f'
                  % (z, m, f[m], ed, f[m]/g0-1, f[m]/ed-1, k**1.5*abs(f[m]/ed-1)))
        print()

print('CHECK 2b: does the He3 term actually earn its place?  Drop it and compare, off the mean.')
print('  %8s %5s %7s %12s %12s %8s' % ('profile', 'k', 'z', 'with He3', 'without', 'ratio'))
bad2 = 0
for name in ('odds', 'primes'):
    for k in (48, 80):
        A = profile(name, k); T = sum(A); n = int(0.44*T)
        s = solve_s(A, n); B = [a for a in A if a > 2]
        mu, K2, K3, K4 = cumulants(B, s); sg = math.sqrt(K2)
        al = K3/sg**3; be = K4/sg**4
        f = exact_pmf(B, s)
        for zt in (-2.0, 2.0):
            m = int(round(mu + zt*sg))
            if m < 0 or m >= len(f) or f[m] == 0: continue
            z = (m-mu)/sg; g0 = phi(z)/sg
            e1 = g0*(1 + (al/6)*He(3,z) + (be/24)*He(4,z) + (al*al/72)*He(6,z))
            e0 = g0*(1 + (be/24)*He(4,z) + (al*al/72)*He(6,z))
            a1 = abs(f[m]/e1-1); a0 = abs(f[m]/e0-1)
            ok = a0 > a1
            if not ok: bad2 += 1
            print('  %8s %5d %7.2f %12.3e %12.3e %8.2f  %s'
                  % (name, k, z, a1, a0, a0/a1, 'OK' if ok else '*** DID NOT FIRE ***'))
print()
print('controls that failed to fire: %d' % bad2)
