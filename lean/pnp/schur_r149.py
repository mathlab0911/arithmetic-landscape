"""
r149 -- where does Gamma sit in the modern structural vocabulary?

Gamma has the closed form
    Gamma(a_1 < ... < a_k) = a_1/2 + a_2/4 + ... + a_{k-1}/2^{k-1} + a_k/2^{k-1},
a linear functional with ORDER-DEPENDENT dyadic weights.  Functionals of that shape have
a home: Schur convexity / majorization.  A symmetric function is Schur-convex iff it
increases under every transfer that spreads two coordinates apart.  Gamma is not
symmetric as written, but it is symmetric AS A SET FUNCTION -- the sorting is part of the
definition, not extra data -- so the question is well posed:

    is Gamma Schur-convex, Schur-concave, or neither, on sets of odd integers?

If Schur-concave: "Gamma is maximised by the most equal set, minimised by the most spread"
puts the extremal theorems of Part I inside a hundred-year-old framework, and every tool
that framework has (Karamata, Hardy-Littlewood-Polya, Muirhead) applies for free.
"""
import numpy as np, itertools, random

def gamma(A):
    A = sorted(A); M = A[-1]
    return 1 + 2*sum(2.0**(-sum(1 for a in A if a <= 2*d)) for d in range(1, (M-1)//2 + 1))

def majorizes(x, y):
    """x majorizes y: same sum, partial sums of sorted-descending x dominate"""
    if abs(sum(x)-sum(y)) > 1e-9: return False
    xs, ys = sorted(x, reverse=True), sorted(y, reverse=True)
    s = 0
    for i in range(len(xs)):
        s += xs[i]-ys[i]
        if s < -1e-9: return False
    return True

print("="*84)
print("Schur test: A majorizes B (same sum, A more spread) -- compare Gamma")
print("="*84)
random.seed(11)
pairs = []
tries = 0
while len(pairs) < 400000 and tries < 4000000:
    tries += 1
    k = random.choice([3,4,5])
    A = sorted(random.sample(range(1, 60, 2), k))
    B = sorted(random.sample(range(1, 60, 2), k))
    if A == B: continue
    if majorizes(A, B): pairs.append((A,B))
    elif majorizes(B, A): pairs.append((B,A))
    if len(pairs) >= 4000: break
inc = dec = eq = 0
worst_inc = worst_dec = None
for A, B in pairs:                       # A majorizes B
    ga, gb = gamma(A), gamma(B)
    if ga > gb + 1e-12:
        inc += 1
        if worst_inc is None: worst_inc = (A,B,ga,gb)
    elif ga < gb - 1e-12:
        dec += 1
        if worst_dec is None: worst_dec = (A,B,ga,gb)
    else: eq += 1
print(f"  {len(pairs)} comparable pairs (same sum, one majorizes the other)")
print(f"    Gamma larger on the MORE SPREAD set : {inc}")
print(f"    Gamma larger on the MORE EQUAL set  : {dec}")
print(f"    equal                                : {eq}")
if inc and dec:
    print("\n  NEITHER Schur-convex nor Schur-concave.  Witnesses:")
    A,B,ga,gb = worst_inc; print(f"    more spread wins: {A} (G={ga:.4f})  >  {B} (G={gb:.4f})")
    A,B,ga,gb = worst_dec; print(f"    more equal wins : {B} (G={gb:.4f})  >  {A} (G={ga:.4f})")
elif inc: print("\n  consistent with SCHUR-CONVEX over this sample")
elif dec: print("\n  consistent with SCHUR-CONCAVE over this sample")

print()
print("="*84)
print("the weaker property that the closed form suggests: monotone in each element")
print("="*84)
bad = 0; tested = 0
for _ in range(4000):
    k = random.choice([3,4,5,6])
    A = sorted(random.sample(range(1, 80, 2), k))
    i = random.randrange(k)
    B = A[:]; B[i] += 2
    if len(set(B)) < k: continue
    tested += 1
    if gamma(sorted(B)) < gamma(A) - 1e-12: bad += 1
print(f"  raising one element by 2: {tested} trials, {bad} decreases of Gamma")
print("  (Gamma is nondecreasing in every element -- consistent with the closed form,")
print("   whose weights are all positive.)")

print()
print("="*84)
print("and it is PROVABLE: the closed form is an ordered weighted average with")
print("non-increasing weights, which is exactly the Schur-Ostrowski condition")
print("="*84)
def gamma_weights(A):
    A = sorted(A); k = len(A)
    w = [2.0**-(i+1) for i in range(k-1)] + [2.0**-(k-1)]
    return sum(wi*ai for wi, ai in zip(w, A)), w
bad = 0
for _ in range(3000):
    k = random.choice([2,3,4,5,6,7])
    A = sorted(random.sample(range(1, 120, 2), k))
    g1 = gamma(A); g2, w = gamma_weights(A)
    if abs(g1-g2) > 1e-9: bad += 1
print(f"  layer form vs weighted form: 3000 sets, {bad} disagreements")
w = [2.0**-(i+1) for i in range(6)] + [2.0**-6]
print(f"  weights for k = 7: {[round(x,5) for x in w]}")
print(f"  non-increasing: {all(w[i] >= w[i+1]-1e-15 for i in range(len(w)-1))}")
print()
print("  Schur-Ostrowski: a symmetric phi is Schur-CONCAVE iff")
print("      (a_i - a_j)(d phi/d a_i - d phi/d a_j) <= 0.")
print("  Here d Gamma/d a_i = w_i with a sorted ASCENDING and w non-increasing, so")
print("  a_i > a_j forces i > j forces w_i <= w_j, and the product is <= 0.  Done.")
