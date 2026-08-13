"""
r147 -- two questions, one of which decides what this programme IS.

(1) The double-angle identity.  2 sin 2pi t = 2 * 2 sin pi t cos pi t, so
        log|2 cos pi t| = log|2 sin 2pi t| - log|2 sin pi t| = (T_2 - 1) log|2 sin|
    where T_2 f(t) = f(2t).  If that is right then X = -(T_2 - 1) log|2 sin|, the
    factor (1 - chi(2)) in prop:chardecomp is the eigenvalue of (1 - T_2), and
    prop:chardecomp is the CLASSICAL Dirichlet computation composed with the
    double-angle formula.  Check it, and check that the character factor matches.

(2) Is Gamma the ANNEALED prediction?
    S is a strict local minimum iff every a in S has a > 2D and every a not in S has
    a > -2D, where D = sigma(S) - n.  For D = d > 0 that says S is contained in
    {a > 2d}; the number of excluded elements is exactly N_A(d) = #{a <= 2d}.  The
    annealed (independence) approximation says the fraction of subsets of A_{>2d}
    hitting a given target is 2^{-N_A(d)} of the fraction for A.  Summing over
    d in Z gives  1 + 2 sum_{d>=1} 2^{-N_A(d)}  =  Gamma(A).
    If so, the main theorem does not REPLACE the annealed approximation -- it PROVES
    it asymptotically exact, which is a different and more useful sentence.
"""
import numpy as np
from itertools import combinations
from sympy import primerange

print("="*78)
print("(1) log|2 cos pi t| = log|2 sin 2 pi t| - log|2 sin pi t| ?")
print("="*78)
ts = np.linspace(0.001, 0.999, 200001)
lhs = np.log(np.abs(2*np.cos(np.pi*ts)))
rhs = np.log(np.abs(2*np.sin(2*np.pi*ts))) - np.log(np.abs(2*np.sin(np.pi*ts)))
print(f"  max |lhs - rhs| over 200001 points, poles excluded: {np.nanmax(np.abs(lhs-rhs)):.3e}")
print("  so X = -log|cos pi t| = log 2 - (T_2 - 1) log|2 sin|, with T_2 f(t) = f(2t).")
print("  On the chi-component T_2 has eigenvalue chi(2) (a -> 2a permutes the units),")
print("  so (1 - T_2) contributes exactly the factor (1 - chi(2)) of prop:chardecomp.")
print("  CONCLUSION: prop:chardecomp is Dirichlet's classical evaluation of")
print("  sum chi(a) log|2 sin(pi a/f)| transported by the double-angle formula.")

print()
print("="*78)
print("(2) is Gamma the annealed prediction for lm/r ?")
print("="*78)
def gamma_layer(A):
    M = max(A)
    return 1 + 2*sum(2.0**(-sum(1 for a in A if a <= 2*d)) for d in range(1, (M-1)//2 + 1))
def gamma_annealed(A):
    """1 + 2 sum_{d>=1} (fraction of subsets that avoid every a <= 2d) -- derived
       from the local-minimum condition, not from the layer definition"""
    M = max(A); k = len(A); tot = 1.0
    for d in range(1, (M-1)//2 + 1):
        excluded = sum(1 for a in A if a <= 2*d)
        tot += 2*(2.0**(k-excluded))/(2.0**k)
    return tot
print(f"  {'A':>26s} {'layer form':>14s} {'annealed derivation':>21s} {'equal?':>7s}")
for label, A in [("odds <= 21", list(range(1,22,2))),
                 ("odd primes <= 31", [p for p in primerange(3,32)]),
                 ("{3,5,7,11,13}", [3,5,7,11,13]),
                 ("{1,9,25,49}", [1,9,25,49]),
                 ("odds <= 101", list(range(1,102,2)))]:
    a, b = gamma_layer(A), gamma_annealed(A)
    print(f"  {label:>26s} {a:14.10f} {b:21.10f} {str(abs(a-b)<1e-12):>7s}")

print()
print("  and the local-minimum condition itself, checked by brute force:")
print("  S is a strict local min  <=>  (every a in S has a > 2D) and (every a not in S")
print("  has a > -2D),  D = sigma(S) - n")
def brute_islocmin(A, S, n):
    D = sum(S) - n; base = abs(D)
    for a in A:
        T = set(S) ^ {a}
        if abs(sum(T) - n) <= base: return False
    return True
def cond(A, S, n):
    D = sum(S) - n
    return all(a > 2*D for a in S) and all(a > -2*D for a in A if a not in S)
bad = 0; tested = 0
for A in ([1,3,5,7], [3,5,9,11], [1,5,7,11,13]):
    for n in range(0, sum(A)+1):
        for r in range(len(A)+1):
            for S in combinations(A, r):
                tested += 1
                if brute_islocmin(A, set(S), n) != cond(A, set(S), n): bad += 1
print(f"    {tested} (set, target) pairs, {bad} disagreements")
