# leeyang5_r183.py -- the dichotomy becomes a formula.
#
# WHERE THIS CAME FROM.  r182 proved one half of the r179 dichotomy and noticed that the proved
# radius stayed proportional to the measured distance even where the hypothesis failed --- which
# said the certificate was really the mechanism.  Rewriting Gamma^(q) in the obvious way makes
# the mechanism visible:
#
#     Gamma^(q)  =  1 + G(2q) + G(2-2q),      G(z) = sum_j m_j 2^{-j} z^j .
#
# (Because m_j q^j = m_j (2q)^j 2^{-j}.)  For the odd numbers m_j = 1, G(z) = z/(2-z), and this
# is 1 + q/(1-q) + (1-q)/q = 1/(q(1-q)) - 1, which is cor:oddsclosed.
#
# THE PREDICTION.  Let R be the radius of convergence of G.  Then Gamma^(q) is analytic exactly
# on the lens |q| < R/2 AND |1-q| < R/2.  The fair coin q = 1/2 sits at distance R/2 - 1/2 from
# each boundary circle, and the zeros of the finite-k polynomials cannot accumulate strictly
# inside a region where the limit is analytic and non-vanishing.  So
#
#     dist( q = 1/2 , nearest zero )  ->  R/2 - 1/2      as k -> infinity,
#
# provided the limit has no zero closer than that.  For the odd numbers R = 2 and the prediction
# is 1/2; for the lacunary family a_i = 2^i+1 we have m_j = 2^{j-1}, so m_j 2^{-j} = 1/2, R = 1,
# and the prediction is ZERO -- the fair coin is ON the boundary of analyticity.  That is the
# dichotomy of r179, restated as a distance, with no families and no cases.
#
# THE TEST.  Build a one-parameter family that interpolates: layer gaps a_{j+1} - a_j = 2c^j, so
# m_j = c^j, w_j = (c/2)^j, R = 2/c, and the prediction is
#
#     dist -> 1/c - 1/2 ,
#
# which is 1/2 at c = 1 (the odd numbers) and 0 at c = 2 (the lacunary family), with everything
# in between.  A formula with no fitted constant, tested at seven values of c.
import math
import mpmath as mp
mp.mp.dps = 30

def odds(k):  return [2*i-1 for i in range(1, k+1)]
def primes(k):
    out, n = [], 3
    while len(out) < k:
        if all(n % p for p in range(3, int(n**0.5)+1, 2)): out.append(n)
        n += 2
    return out
def geometric(k): return [2**i + 1 for i in range(1, k+1)]

def cfamily(k, c):
    """a_1 = 1 and a_{j+1} - a_j = 2*round(c^j), so m_j = round(c^j) and w_j ~ (c/2)^j."""
    A = [1]
    for j in range(1, k):
        A.append(A[-1] + 2*max(1, int(round(c**j))))
    return A

def mult(A):
    k = len(A); m = [0]*k; m[0] = (A[0]-1)//2
    for j in range(1, k): m[j] = (A[j]-A[j-1])//2
    return m
def coeffs(A):
    from math import comb
    m = mult(A); k = len(A); c = [0]*k; c[0] += 1
    for j in range(k):
        if m[j] == 0: continue
        c[j] += m[j]
        for i in range(j+1): c[i] += m[j]*comb(j, i)*(-1 if i % 2 else 1)
    while len(c) > 1 and c[-1] == 0: c.pop()
    return c
def roots_of(A):
    cc = coeffs(A)
    return [complex(z) for z in mp.polyroots([mp.mpf(x) for x in reversed(cc)],
                                             maxsteps=400, extraprec=600)]
def minhalf(A): return min(abs(z-0.5) for z in roots_of(A))

print('=== 1. the rewriting is exact: Gamma^(q) = 1 + G(2q) + G(2-2q) ===')
def Gser(m, z):
    return sum(mj*mp.mpf(2)**(-j)*z**j for j, mj in enumerate(m) if mj)
def Gdirect(m, q):
    s = mp.mpf(1); one = 1-q
    for j, mj in enumerate(m):
        if mj: s += mj*(q**j + one**j)
    return s
worst = 0
for A in (odds(20), primes(20), geometric(16), cfamily(18, 1.4)):
    m = mult(A)
    for q in (mp.mpf('0.3'), mp.mpc('0.5','0.2'), mp.mpc('0.7','-0.35')):
        worst = max(worst, abs(Gdirect(m, q) - (1 + Gser(m, 2*q) + Gser(m, 2-2*q))))
print('   max discrepancy over 12 points, 4 profiles : %.2e' % float(worst))
print('   and for the odd numbers G(z) = z/(2-z) gives 1/(q(1-q)) - 1, which is cor:oddsclosed:')
for q in (0.3, 0.42):
    m = mult(odds(40))
    print('     q = %.2f :  series %.10f   closed form %.10f'
          % (q, float(Gdirect(m, mp.mpf(q))), 1/(q*(1-q)) - 1))

print()
print('=== 2. the formula: dist(1/2, nearest zero) -> 1/c - 1/2 ===')
print('   %6s %8s %14s %14s %14s %10s'
      % ('c', 'R = 2/c', 'predicted', 'k = 40', 'k = 70', 'k=70/pred'))
for c in (1.0, 1.1, 1.25, 1.4, 1.6, 1.8, 2.0):
    pred = 1.0/c - 0.5
    row = []
    for k in (40, 70):
        A = cfamily(k, c) if c > 1.0 else odds(k)
        try: row.append(minhalf(A))
        except Exception: row.append(float('nan'))
    rat = (row[1]/pred) if pred > 1e-9 else float('nan')
    print('   %6.2f %8.4f %14.6f %14.6f %14.6f %10s'
          % (c, 2.0/c, pred, row[0], row[1],
             ('%.4f' % rat) if pred > 1e-9 else 'pred = 0'))
print('   at c = 2 the prediction is exactly 0 and the measurement must go to 0 with k')

print()
print('=== 3. c = 2 is the boundary: the distance goes to zero, and how fast ===')
print('   %6s %16s %14s' % ('k','dist to 1/2','k * dist'))
for k in (24, 40, 56, 72, 88):
    A = cfamily(k, 2.0)
    d = minhalf(A)
    print('   %6d %16.10f %14.6f' % (k, d, k*d))
print('   compare rem:leeyanglacunary: Im q_1 = 3*pi/(2k), so k*dist -> 3*pi/2 = %.6f'
      % (1.5*math.pi))

print()
print('=== 4. the named profiles, against the same formula ===')
print('   %12s %6s %14s %14s %12s' % ('profile','k','1/R measured','predicted','measured dist'))
for name, f in (('odds', odds), ('primes', primes), ('geometric', geometric)):
    k = 70
    A = f(k); m = mult(A)
    tail = [ (mj*2.0**(-j))**(1.0/j) for j, mj in enumerate(m) if j >= k//2 and mj > 0 ]
    invR = max(tail)
    pred = 1.0/(2*invR) - 0.5 if invR > 0 else float('nan')
    try: d = minhalf(A)
    except Exception: d = float('nan')
    print('   %12s %6d %14.6f %14.6f %12.6f' % (name, k, invR, pred, d))
print('   1/R read off a finite tail converges slowly from above, so the predicted column is')
print('   an underestimate at these k; the odd numbers and the primes both have R = 2 exactly')

print()
print('=== 5. what the rewriting proves, and what it does not ===')
print('   PROVED  : Gamma^(q) = 1 + G(2q) + G(2-2q) identically, so the limit is analytic exactly')
print('             on |q| < R/2 and |1-q| < R/2, and the fair coin is interior iff R > 1.')
print('             R >= 1 is equivalent to Gamma(A) < infinity, since G(1) = (Gamma-1)/2.')
print('   MEASURED: dist(1/2, nearest zero) -> 1/c - 1/2 on the interpolating family.')
print('   OPEN    : that the zeros accumulate ON the boundary rather than merely not inside it.')
print('             Hurwitz gives one direction on compact subsets of the analytic region; the')
print('             other needs the limit to be non-vanishing there, which for these profiles is')
print('             a statement about G and is not proved here.')
