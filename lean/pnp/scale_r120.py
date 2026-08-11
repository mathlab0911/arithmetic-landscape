# r120: paper 2, lem:cover / lem:annulus -- which scale does t live on?
#
# lem:cover's proof produces a bound on |theta/2pi - j/q|, but the lemma stated it for
# |theta - 2pi j/q|; and lem:annulus wrote theta = 2pi j/q + t and then summed e(p n t),
# which is only right if t is the offset INSIDE the 2pi.  A factor 2pi, absorbed everywhere
# downstream by the O(.) and by the e^{-c sqrt(log N)} saving, so nothing was wrong in the
# conclusion -- but the printed chain of inequalities did not hold as printed.
#
# This decides it numerically: the residue-class split
#     S_B(alpha_n) = sum_{r mod q} e(n r j/q) * sum_{p = r (q)} e(p n t)
# is an identity under exactly one of the two readings.
import cmath, math

def e(x): return cmath.exp(2j * math.pi * x)

def sieve(N):
    s = bytearray([1]) * (N + 1); s[0:2] = b'\x00\x00'
    for i in range(2, int(N ** .5) + 1):
        if s[i]: s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(3, N + 1) if s[i]]

B = sieve(200)
q, j, n, t = 6, 1, 3, 0.0137

def S(alpha): return sum(e(p * alpha) for p in B)
def split(t_):
    return sum(e(n * r * j / q) * sum(e(p * n * t_) for p in B if p % q == r)
               for r in range(q))

for name, theta in (("theta = 2*pi*(j/q + t)   [inside]", 2*math.pi*(j/q + t)),
                    ("theta = 2*pi*j/q + t     [outside]", 2*math.pi*j/q + t)):
    lhs = S(n * theta / (2 * math.pi))
    rhs = split(t)
    print(f"{name}:  |LHS - RHS| = {abs(lhs - rhs):.3e}"
          f"   {'IDENTITY' if abs(lhs - rhs) < 1e-8 else 'does NOT hold'}")

# and the covering lemma's reduction, on the scale the proof actually produces
from fractions import Fraction as F
import random
random.seed(3)
bad = 0
for _ in range(200000):
    Q = random.randint(2, 5000); jp = random.randint(0, Q - 1)
    f = F(jp, Q); qq = f.denominator
    # |x - j'/Q| <= 1/(Q tau)  ==>  |x - j/q| <= 1/(q tau), since q divides Q
    if not (qq <= Q and Q % qq == 0 and 1 / Q <= 1 / qq): bad += 1
print(f"reduction j'/Q -> j/q keeps the bound: {200000-bad}/200000 trials, {bad} failures")
