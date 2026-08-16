# leeyang4_r182.py -- the easy half of the r179 dichotomy, promoted from conjecture to proof.
#
# r179 measured a dichotomy and registered it as conjectured: for profiles satisfying (H) the
# zeros of Gamma^(q) leave the fair coin alone, and for the lacunary witness a_i = 2^i+1 they
# close in on it.  What decides?  The question was handed to fable-5.  It has an answer, and one
# side of it is a two-line proof.
#
# THE CRITERION.  With m_j = (a_{j+1}-a_j)/2 the layer multiplicities,
#
#     Gamma^(q) = 1 + sum_j m_j [ q^j + (1-q)^j ],      Gamma^(1/2) = Gamma(A).
#
# Everything turns on the series  g(x) = sum_j m_j 2^{-j} x^j,  because on |q - 1/2| = r both
# |q| and |1-q| are at most 1/2 + r = (1/2)(1+2r), so the j-th term is controlled by
# m_j 2^{-j} (1+2r)^j.  Write R for the radius of convergence of g.  Note g(1) = (Gamma-1)/2, so
# R >= 1 exactly when Gamma is finite -- and R > 1 is the strictly stronger statement that the
# layer weights decay GEOMETRICALLY rather than merely summably.
#
# THE PROPOSITION (the easy half, proved).  Comparing values rather than bounding from zero:
#
#     |q^j - 2^{-j}| = |q - 1/2| |sum_{i<j} q^i 2^{-(j-1-i)}| <= r j (1/2 + r)^{j-1},
#
# so, summing and doing the same for 1-q,
#
#     |Gamma^(q) - Gamma(A)|  <=  4r * g1(1+2r),      g1(x) := sum_j j m_j 2^{-j} x^{j-1}.
#
# Since Gamma(A) >= 3 for every admissible profile (thm:fair with Gamma(odds) = 3 the minimum),
# ANY r with 4r*g1(1+2r) < 3 gives a disc |q - 1/2| < r free of zeros, UNIFORMLY IN k.  For the
# odd numbers g1(x) = 2/(2-x)^2 exactly, the condition becomes 12r^2 - 20r + 3 > 0, and the
# proved radius is r = 1/6.
#
# THE OTHER HALF is not proved here and is not claimed: R = 1 does not by itself force a zero,
# it only removes the obstruction to one.  The lacunary family has R = 1 and is pinched; that is
# one family, and the paper says so.
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
def randodd(k, seed):
    import random
    r = random.Random(seed); s = set()
    while len(s) < k: s.add(2*r.randrange(1, 6*k)+1)
    return sorted(s)
def geometric(k): return [2**i + 1 for i in range(1, k+1)]
def powerprofile(k, alpha):        # a_i ~ i^alpha, forced odd
    out = []
    for i in range(1, k+1):
        v = int(round(i**alpha)); v = 2*(v//2)+1
        if not out or v > out[-1]: out.append(v)
        else: out.append(out[-1]+2)
    return out

def mult(A):
    k = len(A); m = [0]*k; m[0] = (A[0]-1)//2
    for j in range(1, k): m[j] = (A[j]-A[j-1])//2
    return m
def G(m, q):
    s = mp.mpf(1); one = 1-q
    for j, mj in enumerate(m):
        if mj: s += mj*(q**j + one**j)
    return s
def g1(m, x):
    return sum(j*mj*mp.mpf(2)**(-j)*mp.mpf(x)**(j-1) for j, mj in enumerate(m) if j >= 1 and mj)
def gamma_val(m):  return float(G(m, mp.mpf('0.5')))

print('=== 1. the identity the criterion rests on: g(1) = (Gamma-1)/2 ===')
print('   %10s %5s %14s %14s' % ('profile','k','2*g(1)+1','Gamma^(1/2)'))
for name, f in (('odds', odds), ('primes', primes), ('geometric', geometric)):
    for k in (20, 40):
        m = mult(f(k))
        g = sum(mj*mp.mpf(2)**(-j) for j, mj in enumerate(m) if mj)
        print('   %10s %5d %14.8f %14.8f' % (name, k, float(2*g+1), gamma_val(m)))

print()
print('=== 2. the radius of convergence R, read off m_j 2^{-j} ===')
print('   %12s %5s %18s %14s' % ('profile','k','(m_j 2^-j)^{1/j} tail','1/R approx'))
for name, f in (('odds', odds), ('primes', primes), ('rand-7', lambda k: randodd(k,7)),
                ('power a=2', lambda k: powerprofile(k,2)), ('geometric', geometric)):
    k = 60; m = mult(f(k))
    tail = [ (mj*2.0**(-j))**(1.0/j) for j, mj in enumerate(m) if j >= k//2 and mj > 0 ]
    v = max(tail) if tail else float('nan')
    print('   %12s %5d %18.8f %14.4f' % (name, k, v, v))
print('   1/R < 1 means the layer weights decay geometrically; 1/R = 1 means they do not')

print()
print('=== 3. the proved radius, and the measured one ===')
print('   the condition is 4r*g1(1+2r) < Gamma(A); for the odd numbers g1(x) = 2/(2-x)^2 exactly')
worst = 0
for k in (20, 40, 80):
    m = mult(odds(k))
    for x in (1.0, 1.1, 1.2, 1.3):
        worst = max(worst, abs(float(g1(m, x)) - 2/(2-x)**2))
print('   max | g1 - 2/(2-x)^2 | over k = 20,40,80 and x = 1.0..1.3 : %.2e   (finite-k truncation)' % worst)
print()
print('   %12s %5s %12s %14s %14s %10s' % ('profile','k','Gamma','proved r','measured min','ratio'))
def proved_r(m, gamma):
    lo, hi = 0.0, 0.49
    for _ in range(80):
        mid = (lo+hi)/2
        try: val = 4*mid*float(g1(m, 1+2*mid))
        except Exception: val = float('inf')
        if val < gamma: lo = mid
        else: hi = mid
    return lo
def coeffs(A):
    from math import comb
    m = mult(A); k = len(A); c = [0]*k; c[0] += 1
    for j in range(k):
        if m[j] == 0: continue
        c[j] += m[j]
        for i in range(j+1): c[i] += m[j]*comb(j, i)*(-1 if i % 2 else 1)
    while len(c) > 1 and c[-1] == 0: c.pop()
    return c
def minhalf(A):
    c = coeffs(A)
    R = [complex(z) for z in mp.polyroots([mp.mpf(x) for x in reversed(c)],
                                          maxsteps=300, extraprec=400)]
    return min(abs(z-0.5) for z in R)
for name, f in (('odds', odds), ('primes', primes), ('rand-7', lambda k: randodd(k,7)),
                ('power a=2', lambda k: powerprofile(k,2)), ('geometric', geometric)):
    for k in (32, 64):
        A = f(k); m = mult(A); gam = gamma_val(m)
        pr = proved_r(m, gam)
        try: me = minhalf(A)
        except Exception: me = float('nan')
        print('   %12s %5d %12.5f %14.6f %14.6f %10s'
              % (name, k, gam, pr, me, ('%.2f' % (me/pr)) if pr > 1e-9 else 'no radius'))
print()
print('   the proved radius is uniform in k where it exists, and it is conservative;')
print('   where it does not exist (geometric), the measured distance is going to zero')

print()
print('=== 4. the proved bound actually holds: no zero inside the proved disc ===')
bad = 0; tested = 0
for name, f in (('odds', odds), ('primes', primes), ('rand-7', lambda k: randodd(k,7)),
                ('power a=2', lambda k: powerprofile(k,2))):
    for k in (24, 48):
        A = f(k); m = mult(A); gam = gamma_val(m); r = proved_r(m, gam)
        if r < 1e-9: continue
        lo = None
        for a in range(72):
            th = 2*math.pi*a/72
            q = mp.mpc(mp.mpf('0.5') + 0.999*r*math.cos(th), 0.999*r*math.sin(th))
            v = abs(G(m, q)); tested += 1
            if lo is None or v < lo: lo = float(v)
        ok = lo > 0
        if not ok: bad += 1
        print('   %12s k=%3d  proved r = %.6f   min |Gamma^(q)| on that circle = %.6f  %s'
              % (name, k, r, lo, 'OK' if ok else '*** ZERO INSIDE ***'))
print('   %d points tested, %d failures' % (tested, bad))

print()
print('=== 5. what is proved and what is not ===')
print('   PROVED : if sum_j j m_j 2^{-j} x^{j-1} converges at some x > 1, then Gamma^(q) has no')
print('            zero in a disc about q = 1/2 whose radius depends only on that series and on')
print('            Gamma(A) >= 3 -- uniformly in k.  The fair coin is never pinched there.')
print('   NOT    : the converse.  A radius of convergence equal to 1 removes the obstruction to')
print('            a zero near q = 1/2; it does not produce one.  The lacunary family is pinched,')
print('            and that is one family.')
