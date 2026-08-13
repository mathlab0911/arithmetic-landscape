"""
r145 -- is prop:redresidue the trivial-character component of something bigger?

X is even, so only even characters see it.  Using
    log|2 cos pi t| = sum_{n>=1} (-1)^{n+1} cos(2 pi n t)/n
and, for chi primitive mod f,  sum_a conj(chi)(a) e(na/f) = chi(n) tau(conj chi),

    sum_{a in (Z/f)*} conj(chi)(a) X(a/f)
      = - tau(conj chi) * sum_n (-1)^{n+1} chi(n)/n
      = - tau(conj chi) * (1 - chi(2)) * L(1, chi)          [chi even, nontrivial]

Note the factor (1 - chi(2)): the component VANISHES when chi(2) = 1.  If that is
right, the 2-adic boundary that runs through prop:twopower shows up a fifth time,
now inside the character group.
"""
import mpmath as mp
mp.mp.dps = 40
from sympy import primerange
from math import gcd

def X(t): return -mp.log(abs(mp.cos(mp.pi*mp.mpf(t))))

def characters(f):
    """all Dirichlet characters mod f, as dicts, via the group structure (brute force)"""
    units = [a for a in range(1, f) if gcd(a, f) == 1]
    n = len(units)
    # brute force: find characters as homomorphisms using the cyclic decomposition
    # via discrete logs against generators found greedily
    gens, orders, seen = [], [], {1}
    for g in units:
        if g in seen: continue
        # order of g
        o, x = 1, g
        while x != 1: x = x*g % f; o += 1
        new = set()
        for s in seen:
            y = s
            for _ in range(o):
                new.add(y); y = y*g % f
        if len(new) > len(seen):
            gens.append(g); orders.append(len(new)//len(seen)); seen = new
        if len(seen) == n: break
    # index every unit by its exponent vector
    idx = {}
    def rec(i, val, vec):
        if i == len(gens):
            idx[val] = tuple(vec); return
        x = val
        for e in range(orders[i]):
            rec(i+1, x, vec+[e]); x = x*gens[i] % f
    rec(0, 1, [])
    assert len(idx) == n, (len(idx), n)
    chars = []
    def build(i, vec):
        if i == len(gens):
            k = tuple(vec)
            chars.append({u: mp.e**(2j*mp.pi*sum(mp.mpf(k[t])*idx[u][t]/orders[t]
                                                 for t in range(len(gens))))
                          for u in units})
            return
        for e in range(orders[i]): build(i+1, vec+[e])
    build(0, [])
    return units, chars

def is_even(ch, f):  return abs(ch[(f-1) % f] - 1) < 1e-20
def is_trivial(ch):  return all(abs(v-1) < 1e-20 for v in ch.values())
def is_primitive(ch, f):
    for d in range(1, f):
        if f % d == 0 and d < f:
            if all(abs(ch[u]-1) < 1e-20 for u in ch if (u-1) % d == 0): 
                # induced from modulus d?
                if all(abs(ch[u]-ch[v]) < 1e-20 for u in ch for v in ch if (u-v) % d == 0):
                    return False
    return True

def tau(ch, f):
    return mp.fsum([ch[a]*mp.e**(2j*mp.pi*mp.mpf(a)/f) for a in ch])

def Lval(ch, f):
    # L(1, chi) = -(1/f) sum_a chi(a) psi(a/f)   for chi nontrivial
    return -mp.fsum([ch[a]*mp.digamma(mp.mpf(a)/f) for a in ch])/f

print("="*94)
print("the character decomposition of the coset energy")
print(f"  {'f':>4s} {'chi':>4s} {'even':>5s} {'prim':>5s} {'chi(2)':>16s} {'measured':>22s} {'predicted':>22s} {'err':>9s}")
worst = 0.0; n = 0; vanish = []
for f in (5, 7, 8, 12, 13, 15, 16):
    units, chars = characters(f)
    for ci, ch in enumerate(chars):
        if is_trivial(ch) or not is_even(ch, f) or not is_primitive(ch, f): continue
        conj = {a: mp.conj(v) for a, v in ch.items()}
        meas = mp.fsum([conj[a]*X(mp.mpf(a)/f) for a in units])
        c2 = ch.get(2 % f, mp.mpf(0)) if gcd(2, f) == 1 else mp.mpf(0)
        pred = -tau(conj, f)*(1 - c2)*Lval(ch, f)
        e = abs(meas - pred); worst = max(worst, float(e)); n += 1
        if gcd(2, f) == 1 and abs(c2 - 1) < 1e-20: vanish.append((f, ci))
        print(f"  {f:4d} {ci:4d} {'yes':>5s} {'yes':>5s} {mp.nstr(c2,6):>16s}"
              f" {mp.nstr(meas,8):>22s} {mp.nstr(pred,8):>22s} {float(e):9.1e}")
print(f"\n  {n} even primitive nontrivial characters, worst error {worst:.2e}")
if vanish:
    print(f"  characters with chi(2) = 1 (component must vanish): {vanish}")
"""
r145b -- the prediction with teeth: the component VANISHES when chi(2) = 1.

For p = 1 mod 8 the Legendre symbol mod p is even (p = 1 mod 4) and has
(2/p) = +1 (p = +-1 mod 8), so the formula predicts, EXACTLY,

    sum_{a=1}^{p-1} (a/p) * log|cos(pi a / p)| = 0 .

For p = 5 mod 8 the symbol is still even but (2/p) = -1, so the same sum is
-2 tau(chi) L(1,chi) and is nonzero.  That pair is the control: one class must
vanish and the neighbouring class must not.
"""
import mpmath as mp
mp.mp.dps = 50
from sympy import legendre_symbol, primerange

def S(p):
    return mp.fsum([legendre_symbol(a, p)*mp.log(abs(mp.cos(mp.pi*mp.mpf(a)/p)))
                    for a in range(1, p)])

print("="*74)
print("quadratic characters: p = 1 mod 8 must vanish, p = 5 mod 8 must not")
print(f"  {'p':>5s} {'p mod 8':>8s} {'(2/p)':>6s} {'sum (a/p) log|cos(pi a/p)|':>32s} {'verdict':>12s}")
bad = 0
for p in [q for q in primerange(5, 200) if q % 4 == 1]:
    s = S(p); two = legendre_symbol(2, p)
    should_vanish = (two == 1)
    v = abs(s) < mp.mpf(10)**(-40)
    ok = (v == should_vanish); bad += not ok
    print(f"  {p:5d} {p%8:8d} {int(two):6d} {mp.nstr(s, 12):>32s}"
          f" {('vanishes' if v else 'nonzero') + ('' if ok else '  <-- BUG'):>12s}")
print(f"\n  disagreements with the prediction: {bad}")

print()
print("="*74)
print("control: the same sum for p = 3 mod 4, where the symbol is ODD")
print("X is even, so every odd character must give 0 regardless of chi(2)")
print("if this does NOT vanish, the parity argument is wrong")
for p in [q for q in primerange(5, 60) if q % 4 == 3]:
    print(f"  p={p:4d}  (2/p)={int(legendre_symbol(2,p)):+d}  sum = {mp.nstr(S(p), 10)}")

print()
print("="*74)
print("and the trivial character reproduces prop:redresidue")
for f in (5, 7, 9, 12, 16, 20, 4, 8):
    from math import gcd
    U = [a for a in range(1, f) if gcd(a, f) == 1]
    m = mp.fsum([-mp.log(abs(mp.cos(mp.pi*mp.mpf(a)/f))) for a in U])/len(U)
    j = 0; w = f
    while w % 2 == 0: w //= 2; j += 1
    from sympy import totient
    pred = mp.log(2)*(1 - 2*(w == 1)/(2**j*int(totient(w)))) if f % 4 != 2 else None
    print(f"  f={f:4d}  mean {mp.nstr(m,12):>18s}   prop:redresidue {mp.nstr(pred,12):>18s}"
          f"   err {float(abs(m-pred)):.1e}")
