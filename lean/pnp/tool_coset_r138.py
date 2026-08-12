# tool_coset_r138.py -- why the floor failed at q=6 for the primes, and what that explains.
#
# The distribution relation averages over an ADDITIVE coset {r, r+m, r+2m, ...} of Z/q.
# A sequence whose residues cover such a coset evenly gets the floor exactly.
#
#   odd numbers mod q  : all residues (q odd) or all ODD residues (q even) -- an additive coset
#   primes mod q       : the REDUCED residues (Z/q)^*, a MULTIPLICATIVE subgroup
#
# Those coincide only sometimes.  Conjecture to test: (Z/q)^* is an additive coset of a
# subgroup of Z/q exactly when q is 1, 2, 4, a prime, or a power of 2 -- and q = 6 is the
# smallest q where they differ.
#
# If so, that is the STRUCTURAL reason the primes' extremal modulus is 6 while a random odd
# sequence's is 4: at q=4 the reduced residues ARE the odd residues, so the floor applies and
# pins the value at 1/sqrt(2); at q=6 they are not, the floor does not apply, and the peak
# sqrt(3)/2 survives.  The paper proves both facts separately; this says why they differ.
import math
from math import gcd

def reduced(q): return [j for j in range(q) if gcd(j, q) == 1]

def is_additive_coset(S, q):
    """is S = {r, r+m, ..., r+(q/m-1)m} for some divisor m of q?"""
    S = sorted(S)
    if not S: return False, None
    for m in range(1, q + 1):
        if q % m: continue
        if len(S) != q // m: continue
        r = S[0]
        if sorted((r + i * m) % q for i in range(q // m)) == S:
            return True, m
    return False, None

print('is (Z/q)^* an additive coset of a subgroup of Z/q ?')
print('  %4s %6s %-26s %-10s %s' % ('q', 'phi(q)', '(Z/q)^*', 'coset?', 'note'))
firstfail = None
for q in range(2, 33):
    R = reduced(q)
    ok, m = is_additive_coset(R, q)
    note = ''
    if not ok and firstfail is None: firstfail = q; note = '<-- smallest failure'
    print('  %4d %6d %-26s %-10s %s'
          % (q, len(R), str(R) if len(R) <= 10 else str(R[:8])[:-1] + ', ...]',
             ('yes, m=%d' % m) if ok else 'NO', note))
print()
print('  smallest q where the reduced residues are NOT an additive coset: %d' % firstfail)
print()

print('what that predicts, against the paper\'s two theorems')
print('  q=4 : reduced = odd residues = additive coset  -> the floor applies')
print('        M_odd(4) = 1/sqrt(2) = %.6f   and this is the extremal modulus for a' % (2**-0.5))
print('        random odd sequence (thm:modfour, proved).')
print('  q=6 : reduced = {1,5}, NOT an additive coset  -> the floor does not apply')
print('        M(6) = sqrt(3)/2 = %.6f  survives, and this is the extremal modulus for' % (3**0.5/2))
print('        the primes (Part II, proved).  M_odd(6) = 0 because the odd residue 3 is')
print('        present for an odd sequence and cos(pi/2) = 0 -- the vanishing lemma.')
print()

print('direct check: the coset average at q, for odd numbers versus primes')
def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
N = 40001
ODD = [a for a in range(3, N, 2)]
PRI = [p for p in primes_upto(N) if p % 2 == 1]
M = 8.0
def X(t):
    c = abs(math.cos(math.pi*t))
    return M if c <= 0 else min(-math.log(c), M)
print('  %4s %12s %12s %12s %8s' % ('q', 'floor', 'odds avg', 'primes avg', 'coset?'))
for q in (3, 4, 5, 6, 7, 8, 9, 10, 12):
    v = q if q % 2 else q // 2
    fl = (1 - 1.0/v) * math.log(2)
    ao = sum(X(a/q) for a in ODD)/len(ODD)
    ap = sum(X(p/q) for p in PRI)/len(PRI)
    ok, _ = is_additive_coset(reduced(q), q)
    print('  %4d %12.5f %12.5f %12.5f %8s  %s'
          % (q, fl, ao, ap, 'yes' if ok else 'NO',
             'primes below the floor' if ap < fl - 1e-6 else ''))
