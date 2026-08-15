# leeyang3_r179.py -- the finding, isolated.
#
# leeyang2_r179 put the zeros of Gamma^(q) in three columns and one of them did not belong.
#
#   profiles satisfying (H) -- odds, primes, random odd sets:
#       the zeros pinch the real segment only at its ENDPOINTS q = 0 and q = 1, at rate
#       2*pi/k, and the nearest zero to the fair coin stays at distance ~1/2 forever.
#
#   the lacunary family a_i = 2^i + 1, which is the witness that BREAKS the annealed
#   prediction (prob:hrate):
#       the nearest zeros sit at Re q = 1/2 EXACTLY, and their distance to the real axis
#       goes to zero.  The fair coin is being pinched.
#
# That is the Lee-Yang dichotomy landing on the same partition of profiles that the main
# theorem does, from a completely different direction.  This file pins the second column down.
#
# WHY THE TWO COLUMNS DIFFER, IN ONE LINE.  With m_j = (a_{j+1}-a_j)/2 the layer multiplicities,
# Gamma^(q) = 1 + sum_j m_j [q^j + (1-q)^j].  For the odd numbers m_j = 1 and the sum is
# geometric with ratio q, so nothing grows.  For a_i = 2^i+1 we get m_j = 2^{j-1} exactly, and
#
#     Gamma^(q) = 3 + (1/2) sum_{j=1}^{k-1} [ (2q)^j + (2(1-q))^j ] ,
#
# two geometric series with ratios 2q and 2(1-q).  On Re q = 1/2 those ratios are complex
# conjugates of equal modulus, so the two terms can cancel -- and that is the whole mechanism.
# Writing q = 1/2 + i t, (1+2it)^k + (1-2it)^k = 2|1+2it|^k cos(k*arctan(2t)) vanishes when
# k*arctan(2t) = pi/2 mod pi, giving t ~ pi/(4k) for the first one.  The constant is measured
# below rather than asserted, because the constant term 3 and the truncation both move it.
import math
import mpmath as mp
mp.mp.dps = 40
TWOPI, PI = 2*math.pi, math.pi

def geometric(k): return [2**i + 1 for i in range(1, k+1)]
def odds(k):      return [2*i-1 for i in range(1, k+1)]

def G_geom(q, k):
    """Gamma^(q) for a_i = 2^i+1, in closed form: no cancellation, no huge coefficients."""
    a, b = 2*q, 2*(1-q)
    def S(r):
        return (r*(1-r**(k-1))/(1-r)) if r != 1 else mp.mpf(k-1)
    return 3 + (S(a) + S(b))/2

print('=== 0. the closed form is the polynomial ===')
def mult(A):
    k = len(A); m = [0]*k; m[0] = (A[0]-1)//2
    for j in range(1, k): m[j] = (A[j]-A[j-1])//2
    return m
def G_sum(m, q):
    s = mp.mpf(1); one = 1-q
    for j, mj in enumerate(m):
        if mj: s += mj*(q**j + one**j)
    return s
worst = 0
for k in (8, 12, 20):
    m = mult(geometric(k))
    for t in (mp.mpf('0.17'), mp.mpf('0.5'), mp.mpc('0.5','0.03'), mp.mpc('0.3','0.4')):
        worst = max(worst, abs(G_sum(m, t) - G_geom(t, k)))
print('   max | sum form - closed form | over 12 points = %.2e' % float(worst))
print('   Gamma^(1/2) = k+2 : ', [int(G_geom(mp.mpf('0.5'), k)) for k in (10, 20, 40)],
      ' against k+2 =', [k+2 for k in (10, 20, 40)])

print()
print('=== 1. the lacunary family: the zeros pinch the FAIR COIN ===')
print('   %6s %20s %16s %16s %14s' % ('k','t = Im of nearest','k*t','k*t/(pi/4)','Re'))
prev = None
for k in (32, 64, 128, 256, 512, 1024, 2048):
    # bisect on the real function t -> Re G(1/2 + it) along the symmetry line, then polish
    f = lambda t: mp.re(G_geom(mp.mpc(mp.mpf('0.5'), t), k))
    lo, hi = mp.mpf('1e-9'), mp.mpf(4)/k
    while f(hi) > 0 and hi < 1: hi *= 2
    if f(hi) > 0:
        print('   %6d   (no sign change found)' % k); continue
    for _ in range(200):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    t = (lo+hi)/2
    z = mp.mpc(mp.mpf('0.5'), t)
    print('   %6d %20.14f %16.8f %16.8f %14.10f'
          % (k, float(t), k*float(t), k*float(t)/(PI/4), float(mp.re(z))))
print('   pi/4 = %.8f ; the imaginary part is being measured on the line Re q = 1/2, where the'
      % (PI/4))
print('   two geometric ratios 2q and 2(1-q) are conjugate and can cancel')

print()
print('=== 2. the same measurement for the odd numbers: nothing on the fair-coin line ===')
print('   %6s %26s' % ('k','min |Re Gamma^(q)| on Re q = 1/2, |t| <= 2'))
for k in (32, 128, 512):
    m = mult(odds(k))
    vals = []
    for i in range(1, 400):
        t = mp.mpf(i)/200
        vals.append(abs(mp.re(G_sum(m, mp.mpc(mp.mpf('0.5'), t)))))
    print('   %6d %26.6f' % (k, float(min(vals))))
print('   no sign change, no zero: for (H)-profiles the symmetry line carries no zeros at all')

print()
print('=== 3. the endpoint pinch, for the lacunary family too? ===')
print('   %6s %22s %16s' % ('k','dist to [0,1] on the line','2*pi/k'))
for k in (32, 64, 128, 256):
    f = lambda t: mp.re(G_geom(mp.mpc(mp.mpf('0.5'), t), k))
    lo, hi = mp.mpf('1e-9'), mp.mpf(4)/k
    while f(hi) > 0 and hi < 1: hi *= 2
    for _ in range(200):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    print('   %6d %22.10f %16.10f' % (k, float((lo+hi)/2), TWOPI/k))
print('   for the lacunary family the nearest zero to the real axis is the one at Re q = 1/2,')
print('   and it is closer than 2*pi/k : the fair coin is the pinch point, not the endpoints')

print()
print('=== 4. what this says, stated so it can be attacked ===')
print('   The Lee-Yang zeros of Gamma^(q) separate the profiles on which the annealed count is')
print('   asymptotically exact from the one on which it is not, and they do it at the fair coin.')
print('   FALSIFIER 1: exhibit a profile satisfying (H) whose zeros approach q = 1/2.')
print('   FALSIFIER 2: exhibit a profile violating (H) whose zeros stay away from q = 1/2.')
print('   Neither is ruled out here.  Two families are two families.')
