"""
r146b -- the same test with the fundamental unit computed correctly.

The first run returned h = 1/6 or h = 1/2 for every p.  Ratios that clean are never
a broken theorem; 1.618^6 = 17.944 and 12.083^2 = 146.0 identified it at once -- the
continued-fraction routine was returning a POWER of the unit, not the unit.  The
denominators 6 and 2 were the exponents.  Redone by solving x^2 - p y^2 = +-4 for the
smallest positive y, which is the fundamental unit of Z[(1+sqrt p)/2] by definition.
"""
import mpmath as mp
mp.mp.dps = 60
from sympy import legendre_symbol, primerange, integer_nthroot

def S(p):
    return mp.fsum([int(legendre_symbol(a, p))*mp.log(abs(mp.cos(mp.pi*mp.mpf(a)/p)))
                    for a in range(1, p)])

def eps(d, ymax=4*10**7):
    """fundamental unit of Q(sqrt d), d = 1 mod 4: least y>0 with x^2 - d y^2 = +-4.
       Try s = -4 BEFORE s = +4: at the same y both can solve, and the norm -4
       solution has the smaller x, hence the smaller unit.  Taking +4 first returned
       eps^2 at p = 5 -- the second harness bug of the round in the same function."""
    for y in range(1, ymax):
        for s in (-4, 4):
            t = d*y*y + s
            if t <= 0: continue
            x, ok = integer_nthroot(t, 2)
            if ok:
                return (mp.mpf(x) + mp.sqrt(mp.mpf(d))*y)/2, x, y, s
    return None

print("="*96)
print("prop:chardecomp composed with Dirichlet:  S(p) = 4 h(p) log eps_p  for p = 5 mod 8")
print("="*96)
print(f"  {'p':>5s} {'S(p)':>18s} {'x':>12s} {'y':>9s} {'eps':>16s} {'S/(4 log eps)':>20s} {'h':>4s}")
rows = bad = 0
known = {5:1, 13:1, 29:1, 37:1, 53:1, 61:1, 101:1, 109:1, 149:1, 157:1, 173:1, 181:1,
         197:1, 229:3, 269:1, 277:1, 293:1, 317:1}
for p in [q for q in primerange(5, 320) if q % 8 == 5]:
    s = S(p); e = eps(p)
    if e is None:
        print(f"  {p:5d}  unit search exhausted"); continue
    E, x, y, sg = e
    h = s/(4*mp.log(E)); near = int(mp.nint(h))
    ok = abs(h - near) < mp.mpf(10)**-25 and near >= 1
    agree = (known.get(p) == near)
    rows += 1; bad += not (ok and agree)
    flag = f"{near:4d}" if ok else " NO "
    print(f"  {p:5d} {mp.nstr(s,12):>18s} {x:12d} {y:9d} {mp.nstr(E,10):>16s}"
          f" {mp.nstr(h,16):>20s} {flag}"
          + ("" if agree else f"   <-- known h = {known.get(p)}"))
print(f"\n  {rows} primes; {bad} that are not a positive integer equal to the known class number")
print("  the left-hand side is a sum of logarithms of cosines.  Nothing in it knows that")
print("  it is supposed to be four times an integer times a regulator.")
