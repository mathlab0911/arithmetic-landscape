# const_r118.py -- the true value of every named constant the papers quote.
#
# This is the log behind check.py's C11 table and behind the r118 errata.  A correction
# whose evidence is not in the repository is the failure this project keeps recording
# (F20), so the constants that were fixed are recomputed here at 30 digits.
#
# Needs mpmath:  pip install mpmath --break-system-packages
from mpmath import mp, mpf, mpc, sqrt, log, exp, pi, polylog, im
from fractions import Fraction as F
mp.dps = 40
Cl2 = lambda t: im(polylog(2, exp(mpc(0, 1) * t)))

print("=== named constants, 30 digits ===")
C = [
    ("sqrt3/2",                sqrt(3) / 2),
    ("5^(1/4)/2",              mpf(5) ** mpf(0.25) / 2),
    ("1/sqrt2",                1 / sqrt(2)),
    ("7^(1/6)/2",              mpf(7) ** (mpf(1) / 6) / 2),
    ("3^(1/6)/2",              mpf(3) ** (mpf(1) / 6) / 2),
    ("log sqrt3",              log(sqrt(3))),
    ("e^(1/8) sqrt3/2",        exp(mpf(1) / 8) * sqrt(3) / 2),
    ("1 - e^(1/8) sqrt3/2",    1 - exp(mpf(1) / 8) * sqrt(3) / 2),
    ("delta = (1/6) log 2",    log(2) / 6),
    ("(1/2) log 2",            log(2) / 2),
    ("16 delta^2",             16 * (log(2) / 6) ** 2),
    ("Cl2(pi/3)",              Cl2(pi / 3)),
    ("Cl2(pi/3)/(2 pi)",       Cl2(pi / 3) / (2 * pi)),
    ("log2 - Cl2(pi/3)/(2pi)", log(2) - Cl2(pi / 3) / (2 * pi)),
    ("log2 - Cl2(pi/3)/pi",    log(2) - Cl2(pi / 3) / pi),
    ("1 - log(pi^2/4)",        1 - log(pi ** 2 / 4)),
    ("sqrt(3/2)",              sqrt(mpf(3) / 2)),
    ("sqrt(2/3)",              sqrt(mpf(2) / 3)),
]
for name, v in C:
    print(f"  {name:26s} {mp.nstr(v, 30)}")

print("\n=== Gamma(P), two independent routes ===")
def sieve(n):
    s = [True] * (n + 1); s[0] = s[1] = False
    for i in range(2, int(n ** .5) + 1):
        if s[i]:
            for j in range(i * i, n + 1, i): s[j] = False
    return [i for i in range(n + 1) if s[i]]
pr = sieve(20000)
odd = [p for p in pr if p % 2 == 1]
pi_of = lambda x: sum(1 for p in pr if p <= x)

g_terms = sum(mpf(p) / mpf(2) ** (j + 1) for j, p in enumerate(odd[:200]))
g_layer = 1 + 4 * sum(1 / mpf(2) ** pi_of(2 * d) for d in range(1, 1601))
print(f"  sum p_j 2^-j        (k=200)  {mp.nstr(g_terms, 30)}")
print(f"  1 + 4 sum 2^-pi(2d) (D=1600) {mp.nstr(g_layer, 30)}")
print(f"  agree to 30 digits: {mp.nstr(g_terms,30) == mp.nstr(g_layer,30)}")

print("\n=== the erratum: the finite value that was promoted to the limit ===")
P20 = odd[:20]
g20 = sum(F(p, 2 ** (j + 1)) for j, p in enumerate(P20))
print(f"  Gamma(3,...,{P20[-1]}) = {g20} = {float(g20):.10f}   <- paper 1, correct")
print(f"  Gamma(P)                              = {mp.nstr(g_layer, 12)}   <- the limit")
print(f"  they agree to 4 decimals, which is why 5.34920... survived in paper 2")

print("\n=== positive control: the odd numbers give exactly 3 ===")
print(f"  1 + 2 sum_{{d>=1}} 2^-d = {mp.nstr(1 + 2 * sum(1 / mpf(2) ** d for d in range(1, 300)), 30)}")
