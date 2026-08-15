# leeyang_r179.py -- Door 2 of spec_future_r145, opened.
#
# THE QUESTION.  Gamma^(q)(A) = 1 + sum_d [ q^{N_d} + (1-q)^{N_d} ] is, for finite A, a
# polynomial in q.  In statistical mechanics a phase transition IS the accumulation of
# partition-function zeros on the real axis (Lee-Yang), and Gamma^(q) plays the role of a free
# energy in the picture Part III already uses.  So: where do the zeros of Gamma^(q) go as
# |A| -> infinity, and do they pinch the real segment [0,1]?  Three outcomes, all publishable:
# stay away (no transition, and the smoothness Part III observes is a theorem); pinch at
# q = 1/2 (the fair coin is a CRITICAL point, not merely a minimiser); pinch elsewhere (a
# transition nobody has named, at a computable place).
#
# THE POLYNOMIAL.  Group the layers by their count.  With A = {a_1 < ... < a_k} odd,
# N_d = #{a <= 2d} equals j exactly for (a_{j+1}-a_j)/2 values of d, and equals 0 for
# (a_1-1)/2 of them.  Dropping the degenerate tail N_d = k (which contributes a constant
# multiple of q^k + (1-q)^k per layer and is the truncation term the paper already accounts
# for as (2D+1)2^{-k}),
#
#     G_A(q) = 1 + sum_{j=0}^{k-1} m_j [ q^j + (1-q)^j ],
#     m_0 = (a_1-1)/2,   m_j = (a_{j+1}-a_j)/2.
#
# G_A(1/2) = Gamma(A) up to O(2^{-k}); checked below.  G_A(q) = G_A(1-q) identically, so the
# zero set is symmetric about the line Re q = 1/2, and being real it is symmetric about the
# real axis too.
#
# THE ODD NUMBERS, IN CLOSED FORM.  There m_0 = 0 and m_j = 1 for j = 1..k-1, so the two
# geometric sums collapse and q(1-q)G(q) = F_k(q) with
#
#     F_k(q) = 1 - q + q^2 - q^{k+1} - (1-q)^{k+1} .
#
# That is worth staring at.  As k -> infinity the two power terms vanish wherever |q| < 1 AND
# |1-q| < 1, so the limit is 1 - q + q^2, whose roots are the primitive SIXTH ROOTS OF UNITY
# e^{+-i pi/3} = (1 +- i sqrt3)/2.  Those sit at Re q = 1/2 exactly -- directly above the fair
# coin -- at height +-sqrt(3)/2, which is nowhere near the real axis.  The rest of the k roots
# have to go somewhere, and that is what this script measures.
import math, cmath

# ---------------------------------------------------------------- profiles
def odds(k):  return [2*i-1 for i in range(1, k+1)]
def primes(k):
    out, n = [], 3
    while len(out) < k:
        if all(n % p for p in range(3, int(n**0.5)+1, 2)): out.append(n)
        n += 2
    return out
def randodd(k, seed):
    import random
    r = random.Random(seed); s = set()
    while len(s) < k: s.add(2*r.randrange(1, 6*k)+1)
    return sorted(s)

def multiplicities(A):
    k = len(A)
    m = [0]*k
    m[0] = (A[0]-1)//2
    for j in range(1, k):
        m[j] = (A[j]-A[j-1])//2
    return m                      # m[j] = #{d : N_d = j}, j = 0..k-1

def coeffs(A):
    """G_A(q) as a coefficient list, index = power of q.  Exact integers."""
    from math import comb
    m = multiplicities(A); k = len(A)
    c = [0]*k
    c[0] += 1
    for j in range(k):
        if m[j] == 0: continue
        c[j] += m[j]                                   # the q^j term
        for i in range(j+1):                           # the (1-q)^j term
            c[i] += m[j]*comb(j, i)*(-1 if i % 2 else 1)
    while len(c) > 1 and c[-1] == 0: c.pop()
    return c

def evalpoly(c, q):
    v = 0
    for a in reversed(c): v = v*q + a
    return v

def gamma_of(A):
    """Gamma(A) from the closed form of Part I, for the q = 1/2 cross-check."""
    k = len(A)
    return sum(A[i]/2**(i+1) for i in range(k-1)) + A[k-1]/2**(k-1)

print('=== 1. the polynomial is the invariant at q = 1/2 ===')
print('  %8s %4s %14s %14s %10s' % ('profile','k','G_A(1/2)','Gamma(A)','diff'))
for name, f in (('odds', odds), ('primes', primes)):
    for k in (10, 20, 30):
        A = f(k); c = coeffs(A)
        g = evalpoly(c, 0.5); G = gamma_of(A)
        print('  %8s %4d %14.10f %14.10f %10.2e' % (name, k, g, G, abs(g-G)))
print('  (they agree to O(2^-k), which is the truncation the paper already carries)')

print()
print('=== 2. the closed form for the odd numbers ===')
def F_odds(q, k): return 1 - q + q*q - q**(k+1) - (1-q)**(k+1)
worst = 0.0
for k in (6, 10, 16, 24):
    c = coeffs(odds(k))
    for t in (0.17, 0.33, 0.5, 0.71, 1.3, -0.4):
        lhs = t*(1-t)*evalpoly(c, t); rhs = F_odds(t, k)
        worst = max(worst, abs(lhs-rhs))
print('  max | q(1-q)G_odds(q) - [1 - q + q^2 - q^{k+1} - (1-q)^{k+1}] | = %.2e' % worst)
print('  roots of the limit 1 - q + q^2 : q = (1 +- i sqrt3)/2 = exp(+- i pi/3)')
print('    Re = %.6f   Im = %.6f   |q| = %.6f   |1-q| = %.6f'
      % (0.5, math.sqrt(3)/2, abs(complex(0.5, math.sqrt(3)/2)), abs(1-complex(0.5, math.sqrt(3)/2))))

print()
print('=== 3. where the zeros actually are ===')
try:
    import mpmath as mp
except ImportError:
    mp = None
    print('  mpmath unavailable; falling back to numpy')
    import numpy as np

def roots_of(c):
    if mp is not None:
        mp.mp.dps = 60
        return [complex(z) for z in mp.polyroots([mp.mpf(x) for x in reversed(c)],
                                                maxsteps=400, extraprec=400)]
    import numpy as np
    return list(np.roots(list(reversed(c))))

print('  %8s %4s %6s %10s %10s %12s %12s'
      % ('profile','k','#roots','min|Im|','dist to [0,1]','min|Re-0.5|','max|Re-0.5|'))
data = {}
for name, f in (('odds', odds), ('primes', primes),
                ('rand-7', lambda k: randodd(k, 7)), ('rand-11', lambda k: randodd(k, 11))):
    for k in (12, 20, 30, 40):
        A = f(k); c = coeffs(A)
        R = roots_of(c)
        if not R: continue
        # distance from each root to the real segment [0,1]
        def dseg(z):
            x = min(max(z.real, 0.0), 1.0)
            return abs(z - complex(x, 0.0))
        dmin = min(dseg(z) for z in R)
        imin = min(abs(z.imag) for z in R)
        remin = min(abs(z.real-0.5) for z in R)
        remax = max(abs(z.real-0.5) for z in R)
        data[(name,k)] = R
        print('  %8s %4d %6d %10.6f %14.6f %12.6f %12.6f'
              % (name, k, len(R), imin, dmin, remin, remax))

print()
print('=== 4. the closest approach to the real segment, as k grows (odds) ===')
print('  %4s %14s %14s %12s' % ('k','dist to [0,1]','nearest root','ratio to k-1'))
prev = None
for k in (10, 15, 20, 25, 30, 35, 40, 50):
    c = coeffs(odds(k)); R = roots_of(c)
    def dseg(z):
        x = min(max(z.real, 0.0), 1.0); return abs(z - complex(x, 0.0))
    z = min(R, key=dseg)
    d = dseg(z)
    print('  %4d %14.8f   %6.4f%+.4fi %12s'
          % (k, d, z.real, z.imag, ('%.4f' % (d/prev)) if prev else '-'))
    prev = d

print()
print('=== 5. do the roots lie on |q| = |1-q|, i.e. Re q = 1/2? ===')
for name in ('odds','primes','rand-7'):
    R = data.get((name,40)) or data.get((name,30))
    if not R: continue
    onhalf = sum(1 for z in R if abs(z.real-0.5) < 1e-6)
    print('  %8s : %d of %d roots have Re q = 1/2 to 1e-6; '
          'max |Re-1/2| over all roots = %.6f'
          % (name, onhalf, len(R), max(abs(z.real-0.5) for z in R)))

print()
print('=== 6. the accumulation point, tested directly (odds) ===')
w = complex(0.5, math.sqrt(3)/2)
print('  %4s %18s' % ('k','min |root - e^{i pi/3}|'))
for k in (10, 20, 30, 40, 60, 80):
    c = coeffs(odds(k)); R = roots_of(c)
    print('  %4d %18.10f' % (k, min(abs(z-w) for z in R)))
