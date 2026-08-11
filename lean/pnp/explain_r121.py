# r121: every number used in the explanatory PDF (docs/status_20260812_ja.pdf), computed here
# so that it has a log, like every other number in this project.
from fractions import Fraction as F
import itertools, statistics

def Gamma(A):
    A = sorted(A); M = A[-1]
    return 1 + 2*sum(F(1, 2**sum(1 for a in A if a <= 2*d)) for d in range(1, (M-1)//2 + 1))

def N(A, d): return sum(1 for a in A if a <= 2*d)

A = [3,5,7,11]
print("=== worked example A = {3,5,7,11} ===")
print("  d      2d   N_A(d)   2^-N")
for d in range(1, (max(A)-1)//2 + 1):
    print(f"  {d:<6} {2*d:<5} {N(A,d):<7} {F(1,2**N(A,d))}")
print("  Gamma =", Gamma(A), "=", float(Gamma(A)))

print()
print("=== the landscape of A at every target ===")
k=len(A); tot=sum(A)
sums=[sum(a for i,a in enumerate(A) if s>>i&1) for s in range(1<<k)]
print("  n   deg  lm   lm/deg")
rows=[]
for n in range(0, tot+1):
    E=[abs(s-n) for s in sums]; g=min(E)
    deg=sum(1 for e in E if e==g)
    lm=0
    for S in range(1<<k):
        e=E[S]
        if all(E[S^(1<<i)] > e for i in range(k)): lm+=1
    if deg and n%2==tot%2 or True:
        rows.append((n,deg,lm,lm/deg))
for n,deg,lm,r in rows:
    if n in (13, tot//2): print(f"  {n:<3} {deg:<4} {lm:<4} {r:.3f}")
print("  median lm/deg over all targets:", round(statistics.median(r for *_,r in rows),3))

print()
print("=== the two extremes at M = 11 ===")
print("  sparsest {11}      Gamma =", Gamma([11]))
print("  densest  {1,3,5,7,9,11} Gamma =", Gamma([1,3,5,7,9,11]), "= 3 - 2^-4 =", 3-F(1,16))

print()
print("=== the odd primes ===")
def sieve(Nn):
    s=bytearray([1])*(Nn+1); s[0:2]=b'\x00\x00'
    for i in range(2,int(Nn**.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(3,Nn+1) if s[i]]
P20 = sieve(73)
print("  P_20 =", P20)
print("  Gamma(P_20) =", Gamma(P20), "=", float(Gamma(P20)))
lim = 1 + 2*sum(F(1,2**sum(1 for p in sieve(8001) if p<=2*d)) for d in range(1,4000))
print("  limit ~", float(lim))
print("  range available to a set with M=73: [3 - 2^-35, 73] =",
      f"[{float(3-F(1,2**35)):.10f}, 73]")
import math
print("  the primes sit at", f"{100*math.log(float(Gamma(P20))/3)/math.log(73/3):.1f}%",
      "of that interval on a log scale")

print()
print("=== why the primes are small: the first gaps ===")
print("  gap form  Gamma = a_1 + sum (a_{j+1}-a_j)/2^j")
A2 = P20
terms = [(A2[0], F(A2[0]))] + [(A2[j+1]-A2[j], F(A2[j+1]-A2[j], 2**(j+1))) for j in range(6)]
for g,t in terms: print(f"    gap {g:<3} contributes {t} = {float(t):.4f}")
