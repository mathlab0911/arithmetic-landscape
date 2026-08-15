# leeyang2_r179.py -- the law behind what leeyang_r179 saw.
#
# leeyang_r179 found that the zeros of Gamma^(q) do approach the real segment [0,1], but not at
# the fair coin: the nearest roots have real part going to 0 or to 1, and k times their distance
# settled near 6.26.  That is 2*pi to two places, and there is a reason.
#
# THE MECHANISM.  For the odd numbers, q(1-q)Gamma^(q) = F_k(q) = 1 - q + q^2 - q^{k+1} -
# (1-q)^{k+1}.  Put q = w/(k+1).  Then q^{k+1} -> 0, (1-q)^{k+1} -> e^{-w} and 1 - q + q^2 -> 1,
# so F_k -> 1 - e^{-w}, whose zeros are w = 2*pi*i*n.  Keeping the first correction,
# e^{-w} = 1 - q + q^2 gives -w = log(1 - w/(k+1)) + 2*pi*i*n = -w/(k+1) + 2*pi*i*n + ..., so
# w = 2*pi*i*n*(1 + 1/k + ...) and
#
#     Im q_{+-1}  =  +- 2*pi/k  +  O(k^{-2}) .
#
# The pinch is therefore at the ENDPOINTS of the parameter interval -- the degenerate measures,
# every element absent (q=0) or present (q=1) -- at the rate 2*pi/k, with no constant to fit.
#
# A note on method, because the first attempt at this file got it wrong.  Seeding a root-finder
# at 2*pi*i/k and running Newton on Gamma^(q) does not work: the seed sits close to the root but
# the iteration walks away to the sixth-root family at height sqrt(3)/2.  Rooting the whole
# polynomial is slower and does not care where the answer is.  That is the honest trade and the
# reason the ks below stop where they do.
import math
import mpmath as mp
mp.mp.dps = 35

TWOPI = 2*math.pi

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

def mult(A):
    k = len(A); m = [0]*k
    m[0] = (A[0]-1)//2
    for j in range(1, k): m[j] = (A[j]-A[j-1])//2
    return m

def coeffs(A):
    from math import comb
    m = mult(A); k = len(A)
    c = [0]*k; c[0] += 1
    for j in range(k):
        if m[j] == 0: continue
        c[j] += m[j]
        for i in range(j+1):
            c[i] += m[j]*comb(j, i)*(-1 if i % 2 else 1)
    while len(c) > 1 and c[-1] == 0: c.pop()
    return c

def roots_of(A):
    c = coeffs(A)
    return [complex(z) for z in mp.polyroots([mp.mpf(x) for x in reversed(c)],
                                             maxsteps=400, extraprec=500)]

def dseg(z):
    x = min(max(z.real, 0.0), 1.0); return abs(z - complex(x, 0.0))

def Gval(m, q):
    s = mp.mpf(1); one = 1 - q
    for j, mj in enumerate(m):
        if mj: s += mj*(q**j + one**j)
    return s

print('=== 1. the rate: k * (distance to [0,1]) against 2*pi, odd numbers ===')
print('   %5s %18s %14s %14s %12s' % ('k','dist to [0,1]','k*dist','k*dist/2pi','Re of it'))
for k in (16, 24, 32, 48, 64, 80, 96):
    R = roots_of(odds(k))
    z = min(R, key=dseg); d = dseg(z)
    print('   %5d %18.12f %14.6f %14.6f %12.6f' % (k, d, k*d, k*d/TWOPI, z.real))
print('   2*pi = %.6f ; the approach is from below and the gap closes like 1/k' % TWOPI)

print()
print('=== 2. is the rate universal across profiles? ===')
print('   %10s %6s %16s %14s %12s' % ('profile','k','k*dist','k*dist/2pi','Re'))
for name, f in (('odds', odds), ('primes', primes),
                ('rand-7', lambda k: randodd(k, 7)),
                ('rand-11', lambda k: randodd(k, 11)),
                ('geometric', geometric)):
    for k in (32, 64, 96):
        R = roots_of(f(k))
        z = min(R, key=dseg); d = dseg(z)
        print('   %10s %6d %16.6f %14.6f %12.6f' % (name, k, k*d, k*d/TWOPI, z.real))
print('   the mechanism counts elements; it does not read them')

print()
print('=== 3. the fair coin: no zero approaches it ===')
print('   %10s %6s %18s %16s' % ('profile','k','min |z - 1/2|','min over (0,1)'))
for name, f in (('odds', odds), ('primes', primes), ('geometric', geometric)):
    for k in (32, 64, 96):
        R = roots_of(f(k)); m = mult(f(k))
        dhalf = min(abs(z - 0.5) for z in R)
        best = min(float(Gval(m, mp.mpf(i)/1000)) for i in range(1, 1000))
        print('   %10s %6d %18.10f %16.8f' % (name, k, dhalf, best))
print('   Gamma^(q) is real and >= 3 on (0,1) by thm:fair, so no real zero is possible at all;')
print('   the column above says the complex zeros do not approach q = 1/2 either')

print()
print('=== 4. the other accumulation point: the primitive sixth roots of unity ===')
w6 = complex(0.5, math.sqrt(3)/2)
print('   %5s %22s %14s %14s' % ('k','min |z - e^{i pi/3}|','|z|','|1-z|'))
for k in (24, 48, 72, 96):
    R = roots_of(odds(k))
    z = min(R, key=lambda z: abs(z-w6))
    print('   %5d %22.12f %14.8f %14.8f' % (k, abs(z-w6), abs(z), abs(1-z)))
print('   1 - q + q^2 vanishes exactly where |q| = |1-q| = 1, on the boundary of both discs,')
print('   which is why the k-dependent terms never become negligible there')

print()
print('=== 5. the ten zeros nearest the real axis, odd numbers, k = 96 ===')
R = roots_of(odds(96)); R.sort(key=lambda z: abs(z.imag))
print('   %14s %16s %12s %12s' % ('Re','Im','|q|','|1-q|'))
for z in R[:10]:
    print('   %14.9f %+16.9f %12.6f %12.6f' % (z.real, z.imag, abs(z), abs(1-z)))
print('   they come in conjugate pairs and in q <-> 1-q pairs, as the symmetry requires')
