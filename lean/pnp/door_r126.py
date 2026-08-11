# r126: can the main theorem be stated using only objects an additive number theorist
# already has?  Dirk Zeindler declined the endorsement because the papers "make extensive
# use of non-standard terminology"; this tests whether the landscape vocabulary is load
# bearing or decorative.
#
# Claim to test: with r_B(m) = #{U subset of B : sum U = m}, I_d = {a in A : a <= 2d},
# B_d = A \ I_d,
#
#     lm_A(n)  =  r_A(n) + sum_{d>=1} [ r_{B_d}(n+d) + r_{B_d}(n - d - sigma(I_d)) ]
#
# i.e. the quantity the papers call "the number of valleys" is exactly a weighted sum of
# representation counts of the truncations.  If this holds, the landscape is motivation and
# not machinery, and the theorem can be stated without it.
from itertools import combinations
import random

def r(B, m):
    B = list(B); c = 0
    for k in range(len(B)+1):
        for S in combinations(B, k):
            if sum(S) == m: c += 1
    return c

def lm_direct(A, n):
    A = list(A); k = len(A)
    sums = [sum(a for i, a in enumerate(A) if S >> i & 1) for S in range(1 << k)]
    out = 0
    for S in range(1 << k):
        e = abs(sums[S] - n)
        if all(abs(sums[S ^ (1 << i)] - n) > e for i in range(k)):
            out += 1
    return out

def lm_via_reps(A, n):
    A = sorted(A); M = max(A)
    tot = r(A, n)                                   # the d = 0 stratum
    for d in range(1, (M - 1)//2 + 2):
        I = [a for a in A if a <= 2*d]
        B = [a for a in A if a > 2*d]
        tot += r(B, n + d) + r(B, n - d - sum(I))
    return tot

random.seed(7)
bad = 0; tested = 0
cases = [([3,5,7,11], n) for n in range(0, 27)] \
      + [([3,5,7,11,13,17], n) for n in range(0, 57)] \
      + [([1,5,9,15,21], n) for n in range(0, 52)]
for _ in range(40):
    k = random.randint(2, 7)
    A = sorted(random.sample(range(1, 40, 2), k))
    cases.append((A, random.randint(0, sum(A))))
for A, n in cases:
    tested += 1
    a, b = lm_direct(A, n), lm_via_reps(A, n)
    if a != b:
        bad += 1
        if bad <= 3: print(f"  MISMATCH A={A} n={n}: direct {a} vs reps {b}")
print(f"identity holds on {tested-bad}/{tested} cases, {bad} mismatches")

print()
print("So the main theorem reads, with no landscape vocabulary at all:")
print("  [ r_A(n) + sum_d ( r_{B_d}(n+d) + r_{B_d}(n-d-sigma(I_d)) ) ] / r_A(n)  ->  Gamma(A)")
A = [3,5,7,11,13,17,19,23,29,31,37,41,43,47]
n = sum(A)//2
print(f"  A = first 14 odd primes, n = {n}:  ratio = {lm_via_reps(A,n)/r(A,n):.4f}")
def Gamma(A):
    from fractions import Fraction as F
    A=sorted(A); M=A[-1]
    return 1+2*sum(F(1,2**sum(1 for a in A if a<=2*d)) for d in range(1,(M-1)//2+1))
print(f"  Gamma(A) = {float(Gamma(A)):.4f}")
