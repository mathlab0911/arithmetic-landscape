# r1remainder_r134.py -- Step 1, measured on the actual region rather than on an abstract box.
#
# r1theta0_r134 showed there is NO radius at accessible k with all phases <= 1 AND a negligible
# tail: the two requirements pull apart until k ~ 10^4-10^5.  So the requirement "every factor's
# phase is small" was MY invention, not the argument's.  What the Edgeworth argument on R1
# actually needs is that the SUMMED fourth-order Taylor error is small:
#
#   E(theta) = | log G~(theta) - [ i mu u - K2 u^2/2 - i K3 u^3/6 + K4 u^4/24 ] | ,  u = 2 pi theta
#
# small on |theta| <= theta_0.  That is one number and it can be measured exactly -- log G~ is
# an explicit finite product.  No abstraction, no box, no constant to guess.
#
# Predictions, written first:
#   (Q1) E(theta_0) is small (<< 1) even though individual phases reach 6-12
#   (Q2) E(theta_0) scales like the fifth-order term, (2 pi theta_0)^5 sum a^5 p q
#   (Q3) the ratio E(theta_0) / [(2 pi theta_0)^5 sum a^5 p q] is a bounded constant -- that
#        constant IS the explicit constant Step 1 is asked for.
import math, cmath
from r1budget_r133 import profile, solve_s, cumulants

def tilt(a, s): return 1.0 / (1.0 + math.exp(min(700.0, s * a)))

def logG(A, s, th):
    tot = 0j
    for a in A:
        p = tilt(a, s)
        tot += cmath.log(1 - p + p * cmath.exp(2j * math.pi * a * th))
    return tot

def setup(name, k, x):
    A = profile(name, k); T = sum(A); n = int((0.5 - x) * T)
    s = solve_s(A, n); B = [a for a in A if a > 2]
    mu, K2, K3, K4 = cumulants(B, s)
    S5 = sum(a**5 * tilt(a, s) * (1 - tilt(a, s)) for a in B)
    return A, B, s, mu, K2, K3, K4, S5

def E(B, s, mu, K2, K3, K4, th):
    u = 2 * math.pi * th
    poly = 1j*mu*u - K2*u*u/2 - 1j*K3*u**3/6 + K4*u**4/24
    return abs(logG(B, s, th) - poly)

print('E(theta) on R1, measured against the explicit product.  x = 0.20.')
print('  %8s %5s %11s %9s %12s %12s %10s'
      % ('profile', 'k', 'theta_0', 'max phase', 'E(theta_0)', '(2pi th)^5 S5', 'ratio C'))
for name in ('odds', 'primes', 'squares'):
    for k in (100, 200, 300, 450):
        try:
            A, B, s, mu, K2, K3, K4, S5 = setup(name, k, 0.20)
        except Exception:
            continue
        sg = math.sqrt(K2); th0 = math.log(k) / sg
        e = E(B, s, mu, K2, K3, K4, th0)
        fifth = (2 * math.pi * th0) ** 5 * S5
        print('  %8s %5d %11.4e %9.3f %12.4e %12.4e %10.5f'
              % (name, k, th0, 2*math.pi*A[-1]*th0, e, fifth, e / fifth))
    print()

print('is E small across the WHOLE of R1, not just at its edge?  (primes, k = 300)')
A, B, s, mu, K2, K3, K4, S5 = setup('primes', 300, 0.20)
sg = math.sqrt(K2); th0 = math.log(300) / sg
print('  %10s %9s %12s %12s' % ('theta/theta_0', 'phase', 'E', 'E/fifth(theta)'))
for frac in (0.1, 0.25, 0.5, 0.75, 1.0):
    th = frac * th0
    e = E(B, s, mu, K2, K3, K4, th)
    fifth = (2 * math.pi * th) ** 5 * S5
    print('  %10.2f %9.3f %12.4e %12.5f' % (frac, 2*math.pi*A[-1]*th, e, e / fifth))
print()

print('NEGATIVE CONTROL: drop the K4 term from the polynomial.  E must get WORSE,')
print('and must then scale like the FOURTH order, not the fifth.')
print('  %8s %5s %12s %12s %8s' % ('profile', 'k', 'with K4', 'without K4', 'ratio'))
for name in ('odds', 'primes'):
    for k in (200, 300, 450):
        A, B, s, mu, K2, K3, K4, S5 = setup(name, k, 0.20)
        sg = math.sqrt(K2); th0 = math.log(k) / sg
        e_with = E(B, s, mu, K2, K3, K4, th0)
        e_without = E(B, s, mu, K2, K3, 0.0, th0)
        print('  %8s %5d %12.4e %12.4e %8.1f  %s'
              % (name, k, e_with, e_without, e_without / e_with,
                 'OK' if e_without > e_with else '*** DID NOT FIRE ***'))
