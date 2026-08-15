#!/usr/bin/env python3
"""
r110 / paper 3, rem:closing.  Can the Bernoulli-part-extraction literature be QUOTED for
prop:tiltlclt, as the external referee's item 1 suggested?  Answer: no, and for two reasons
that are structural rather than a matter of effort.

WHAT I READ.  Giuliano-Weber, "Approximate local limit theorems with effective rate and
application to random walks in random scenery", Bernoulli 23(4B) 3268-3310 (2017),
arXiv:1412.3980.  Read: the abstract, the definitions and Theorems 1.2, 1.4, 1.7 and
Corollary 1.8 with Remarks 1.3 and 1.9 (lines 85-190 of the arXiv text).  I did NOT read the
proofs or sections 3-7.  Their statement, verbatim in substance:

    vartheta_X = SUM_k  P{X = v_k} AND P{X = v_{k+1}}        (their (1.8); AND = min)
    Theta_n    = SUM_j vartheta_j ,   0 < vartheta_j <= vartheta_{X_j}
    Cor 1.8:  | P{S_n = kappa} - D e^{...}/(sqrt(2 pi) Var) |
                 <= C_2 { D (log Theta_n / (Var(S_n) Theta_n))^{1/2}
                          + (H_n + 1/Theta_n)/sqrt(Theta_n) }
    Rem 1.9 (their own applicability condition):
              ( Var(S_n)/Theta_n )^{1/2} ( H_n + 1/Theta_n )  ->  0
    where H_n is the Kolmogorov distance of the conditioned sum to the normal law.
Their Remark 1.3 states in as many words that vartheta can be identically 0, in which case
the theorem is empty.

OBSTRUCTION 1, EXACT AND ELEMENTARY.  Our summands are X_j = a_j * Bernoulli(p_j) with a_j an
odd integer >= 3.  Such a law charges exactly two integers, 0 and a_j, which are never
ADJACENT.  So every term of vartheta_{X_j} is min(P{X=k}, P{X=k+1}) = 0, hence
vartheta_{X_j} = 0 for every j, Theta_n = 0, and Corollary 1.8 reads "<= infinity".
The hypothesis is not hard to check for us; it is void.

THE OBVIOUS REPAIR, AND ITS PRICE.  Group A into blocks and apply the method to the block
sums, whose laws do charge adjacent integers once the block is big enough.  Measured below:
how big, and what Theta that buys.

OBSTRUCTION 2, WHICH THE REPAIR DOES NOT FIX.  Their Remark 1.9 requires
(Var/Theta)^{1/2}(H_n + 1/Theta_n) -> 0.  Our weights grow, a_j ~ j, so Var ~ S_2 ~ k^3 while
Theta <= k; and H_n is a Berry-Esseen distance, so H_n ~ SUM|a|^3/(SUM a^2)^{3/2} ~ k^{-1/2}.
Then (Var/Theta)^{1/2}(H_n + 1/Theta) ~ (k^2)^{1/2} k^{-1/2} = k^{1/2} -> INFINITY.
Their theorem is built for sums whose variance grows like the number of summands; ours grows
like its cube, because the summands are weighted.  Measured below at real k.

Fail rule with floor (F51): vartheta is a probability sum, so exact zeros are exact; the
Remark-1.9 quantity is a ratio of measured moments and only its GROWTH matters, so the test is
whether it increases with k, not its value at one k.
"""
import math
from fractions import Fraction


def odd_primes(k):
    out, n = [], 3
    while len(out) < k:
        if all(n % p for p in range(3, int(n ** .5) + 1, 2)):
            out.append(n)
        n += 2
    return out


ENS = {'odds': lambda k: [2 * i + 1 for i in range(k)], 'primes': odd_primes}


def block_law(block, p):
    """exact law of SUM_{a in block} a * Bernoulli(p), as a dict m -> probability."""
    law = {0: Fraction(1)}
    pp = Fraction(p).limit_denominator(10 ** 6)
    for a in block:
        nw = {}
        for m, v in law.items():
            nw[m] = nw.get(m, Fraction(0)) + (1 - pp) * v
            nw[m + a] = nw.get(m + a, Fraction(0)) + pp * v
        law = nw
    return law


def vartheta(law):
    """Giuliano-Weber (1.8): SUM_k min(P{X=k}, P{X=k+1}), on the integer lattice."""
    tot = Fraction(0)
    for m, v in law.items():
        w = law.get(m + 1, Fraction(0))
        tot += min(v, w)
    return tot


print('=' * 100)
print('(1) OBSTRUCTION 1: the Bernoulli part of a single summand a*Bernoulli(p)')
print('=' * 100)
print(f"  {'a':>5} {'p':>6} {'vartheta':>12}   (their Theorem 1.7 needs this > 0)")
for a in (3, 5, 7, 101):
    for p in (0.5, 0.3):
        print(f'  {a:5d} {p:6.2f} {float(vartheta(block_law([a], p))):12.6f}')
print('  Exactly zero, for every odd a >= 3 and every p: the law charges 0 and a only, and')
print('  those are never adjacent.  Theta_n = 0 and Corollary 1.8 is vacuous.  Their own')
print('  Remark 1.3 names this degenerate case.')

print()
print('=' * 100)
print('(2) THE REPAIR: block the sequence.  How large must a block be before vartheta > 0?')
print('=' * 100)
print(f"  {'sequence':>8} {'block':>26} {'m':>3} {'p':>5} {'vartheta':>12}")
for nm in ('odds', 'primes'):
    A = sorted(ENS[nm](12))
    for m in (1, 2, 3, 4, 5):
        blk = A[:m]
        for p in (0.5,):
            v = float(vartheta(block_law(blk, p)))
            print(f'  {nm:>8} {str(blk):>26} {m:3d} {p:5.2f} {v:12.6f}')
    print()

def block_law_f(block, p):
    """same law, in floats -- used where exact zeros are no longer the question."""
    law = {0: 1.0}
    for a in block:
        nw = {}
        for m, v in law.items():
            nw[m] = nw.get(m, 0.0) + (1 - p) * v
            nw[m + a] = nw.get(m + a, 0.0) + p * v
        law = nw
    return law


def vartheta_f(law):
    return sum(min(v, law.get(m + 1, 0.0)) for m, v in law.items())


print('=' * 100)
print('(3a) A CORRECTION TO MY OWN FIRST PASS.  Blocking by three gave a Theta that did not')
print('     grow with k at all -- 0.6250 for the odd numbers at every k -- and the reason is')
print('     that only the FIRST block contributes.  A block of three LARGE elements, say')
print('     {7,9,11}, has subset sums {0,7,9,11,16,18,20,27}: no two adjacent, vartheta = 0.')
print('     Adjacency needs the block to have more subset sums than its span, so the block')
print('     size must GROW.  vartheta by block position, m = 3:')
print('=' * 100)
print(f"  {'sequence':>8} {'block':>22} {'vartheta':>10}")
for nm in ('odds', 'primes'):
    A = sorted(ENS[nm](24))
    for i0 in (0, 3, 9, 21):
        blk = A[i0:i0 + 3]
        print(f'  {nm:>8} {str(blk):>22} {vartheta_f(block_law_f(blk, 0.5)):10.6f}')
    print()

print('=' * 100)
print('(3b) So: how large must the LAST block be before vartheta > 0?')
print('     Heuristic before measuring: a block of m elements has 2^m subset sums spread over')
print('     a span of about m * a_max, so adjacency needs 2^m >~ m * a_max, i.e. m >~ log2 k.')
print('=' * 100)
print(f"  {'sequence':>8} {'k':>5} {'a_max':>7} {'min m with last-block vartheta>0':>34} "
      f"{'log2(k)':>8}")
mstar = {}
for nm in ('odds', 'primes'):
    for k in (16, 32, 64, 128):
        A = sorted(ENS[nm](k))
        found = None
        for m in range(2, min(k, 20) + 1):
            if vartheta_f(block_law_f(A[k - m:], 0.5)) > 1e-12:
                found = m
                break
        mstar[(nm, k)] = found
        print(f'  {nm:>8} {k:5d} {A[-1]:7d} {str(found):>34} {math.log2(k):8.2f}')
    print()

print('=' * 100)
print('(3c) OBSTRUCTION 2, with blocks of the size (3b) forces.')
print("     Rem 1.9 quantity  R := (Var/Theta)^(1/2) * (H + 1/Theta),  H ~ Lyapunov ratio.")
print('     Their condition is R -> 0.  The test is the TREND in k.')
print('=' * 100)
print(f"  {'sequence':>8} {'k':>5} {'m':>4} {'#blocks':>8} {'Theta':>9} {'Var':>13} "
      f"{'H':>9} {'R':>12}")
for nm in ('odds', 'primes'):
    prev = None
    for k in (16, 32, 64, 128):
        A = sorted(ENS[nm](k))
        m = mstar[(nm, k)] or 20
        blocks = [A[i:i + m] for i in range(0, k - k % m, m)]
        Theta = sum(vartheta_f(block_law_f(b, 0.5)) for b in blocks)
        S2 = sum(a * a for a in A); S3 = sum(a ** 3 for a in A)
        Var = S2 / 4.0
        H = S3 / S2 ** 1.5
        R = math.sqrt(Var / Theta) * (H + 1.0 / Theta) if Theta > 0 else float('inf')
        arrow = '' if prev is None else ('  UP' if R > prev else '  down')
        print(f'  {nm:>8} {k:5d} {m:4d} {len(blocks):8d} {Theta:9.4f} {Var:13.1f} '
              f'{H:9.5f} {R:12.2f}{arrow}')
        prev = R
    print()

print('  R grows with k on both sequences, so Giuliano-Weber Remark 1.9 is violated, not')
print('  merely unverified.  The reason is structural: their Var grows like the NUMBER of')
print('  summands, ours like its cube, because our summands carry weights a_j ~ j.  Blocking')
print('  makes it worse, not better: it buys vartheta > 0 at the cost of Theta <~ k/log k.')
print()
print('  VERDICT for paper 3 rem:closing.  The Bernoulli-part-extraction route cannot be')
print('  quoted for prop:tiltlclt.  Obstruction 1 is repairable by blocking; obstruction 2 is')
print('  not, and it is the same feature -- large weights -- that makes our LCLT interesting.')
print('  The Edgeworth constants have to be derived, not imported.')
