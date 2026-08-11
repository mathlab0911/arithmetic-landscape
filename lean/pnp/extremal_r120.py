# r120: every number newly asserted in paper 1's extremal section, recomputed.
from fractions import Fraction as F
from math import log

def Gamma(A):                                   # Definition (layer form)
    A = sorted(A); M = A[-1]
    return 1 + 2*sum(F(1, 2**sum(1 for a in A if a <= 2*d)) for d in range(1, (M-1)//2 + 1))

def Enum(A):                                    # enumeration form  sum a_j 2^-j
    A = sorted(A)
    return sum(F(a, 2**(j+1)) for j, a in enumerate(A))

P = [3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73]
assert len(P) == 20 and P[-1] == 73
G = Gamma(P)
print("Gamma(P_20)          =", G, "=", float(G))
print("  claimed 1402281/262144 :", G == F(1402281, 262144), " 262144 = 2^18 :", 262144 == 2**18)
print("  Enum(P_20)         =", Enum(P), "=", float(Enum(P)))
print("  difference          =", G - Enum(P), " should equal a_k/2^k =", F(73, 2**20),
      G - Enum(P) == F(73, 2**20))

# limit of Gamma over the odd primes, to high precision, by extending the layer sum.
# Own sieve, so that the script needs nothing but the standard library.
def sieve_odd_primes(N):
    s = bytearray([1])*(N+1); s[0:2] = b'\x00\x00'
    for i in range(2, int(N**0.5)+1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(3, N+1) if s[i]]

def Gamma_layer_upto(D):
    pr = sieve_odd_primes(2*D+1)
    return 1 + 2*sum(F(1, 2**sum(1 for a in pr if a <= 2*d)) for d in range(1, D+1))
lim = Gamma_layer_upto(4000)
print("  limit  ~", float(lim))
print("  |Gamma(P_20) - limit| =", float(abs(G-lim)), "   |Enum(P_20)-limit| =", float(abs(Enum(P)-lim)))
print("  ratio                 =", float(abs(Enum(P)-lim)/abs(G-lim)))

# extremal bounds at M=73
M = 73; D = (M-1)//2
print()
print(f"M={M}, D={D}: lower bound 3-2^(1-D) = 3-2^-35 =", float(3 - F(1, 2**35)),
      "  upper bound =", M)
print("  Gamma({M}) =", Gamma([M]), "  Gamma(all odds <= M) =", Gamma(list(range(1, M+1, 2))),
      " = 3-2^-35 ?", Gamma(list(range(1, M+1, 2))) == 3 - F(1, 2**35))
pos = log(float(G)/3.0)/log(M/3.0)
print(f"  log-scale position of the primes in [3, {M}] = {pos:.4f}  -> {100*pos:.1f}%")

# monotonicity corollary, brute force
import itertools, random
random.seed(1)
bad = 0
for _ in range(20000):
    k = random.randint(1, 8)
    A = sorted(random.sample(range(1, 60, 2), k))
    cands = [b for b in range(1, A[-1], 2) if b not in A]
    if not cands: continue
    b = random.choice(cands)
    if not (Gamma(sorted(A + [b])) < Gamma(A)): bad += 1
print("  strict monotonicity counterexamples in 20000 random trials:", bad)

# negative control: adjoining b > max A must NOT decrease Gamma (it changes M)
ex = [3,5,7]
print("  control, adjoin above the max: Gamma(3,5,7) =", float(Gamma(ex)),
      "-> Gamma(3,5,7,9) =", float(Gamma(ex+[9])), "(increases, as it must)")
