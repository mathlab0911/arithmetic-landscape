"""
r143 -- the reduced-residue evaluation of the coset energy, and the head-to-head
against the surrogates a minor-arc argument would otherwise use.

Setting.  For A a finite set of odd positive integers,
    prod_{a in A} |1 + e(a theta)| = 2^{|A|} exp(-D(theta)),
    D(theta) = sum_{a in A} X(a theta),   X(t) = -log|cos pi t| >= 0.
Every minor-arc argument for a generating function of this shape needs a LOWER
bound on the deficiency D.

Claim (proved in Part III; this script is the check, not the proof).
Write v = 2^j w with w odd.  For v not congruent to 2 mod 4,

    (1/phi(v)) sum_{r in (Z/v)*} X(r/v) = log 2 * ( 1 - 2*[w=1] / (2^j phi(w)) )

    = (1 - 2^{1-j}) log 2   if v = 2^j is a power of two (j >= 2),
    = log 2   exactly       otherwise, including every odd v > 1.

For v = 2 mod 4 the residue w mod v gives cos = 0: the product vanishes outright.

Consequences checked here:
  (1) the evaluation, 26 moduli, against a case-split control;
  (2) thm:modfour is the w = 1 case: at v = 4 the value is (1/2)log 2, i.e. the
      product only falls to 2^{-k/2} = (1/sqrt 2)^k instead of 2^{-k};
  (3) the surrogate ceilings: any route replacing X by (1/2)sin^2 or by
      (pi^2/2)||.||^2 caps at 1/4 and pi^2/24 respectively, so it loses a factor
      2.77 or 1.69 in the exponent BEFORE any equidistribution input is invoked.
"""
import numpy as np
from math import log, gcd, pi
from sympy import totient, primerange, factorint

def X(t):
    return -np.log(np.maximum(np.abs(np.cos(np.pi*np.asarray(t, dtype=np.float64))), 1e-300))
def fd(t):
    t = np.asarray(t, dtype=np.float64) % 1.0
    return np.minimum(t, 1.0 - t)
def predicted(v):
    f = factorint(v); j = f.get(2, 0); w = v // 2**j
    if v % 4 == 2: return None
    return log(2) * (1 - 2*(w == 1)/(2**j * int(totient(w))))

L2 = log(2)
print("="*86)
print("1.  the evaluation")
print("="*86)
print(f"  {'v':>6s} {'2^j w':>9s} {'phi(v)':>7s} {'measured':>12s} {'predicted':>12s} {'abs err':>10s}  form")
worst = 0.0; n_ok = 0
for v in [3,5,7,9,11,15,21,25,33,45,105, 4,8,16,32,64,128,256, 12,20,24,40,48,80,96,144]:
    f = factorint(v); j = f.get(2,0); w = v//2**j
    r = np.array([x for x in range(1, v) if gcd(x, v) == 1], dtype=np.float64)
    meas = float(X(r/v).mean()); p = predicted(v); err = abs(meas - p)
    worst = max(worst, err); n_ok += err < 1e-12
    form = "log 2" if abs(p - L2) < 1e-15 else f"(1-2^(1-{j})) log 2"
    print(f"  {v:6d} {'2^%d*%d'%(j,w):>9s} {int(totient(v)):7d} {meas:12.6f} {p:12.6f} {err:10.2e}  {form}")
print(f"  agreed to 1e-12 on {n_ok}/26 moduli; worst absolute error {worst:.2e}")

print()
print("  the excluded class v = 2 mod 4, and why it is excluded:")
for v in (6, 10, 14, 22, 50):
    w = v//2
    r = np.array([x for x in range(1, v) if gcd(x, v) == 1], dtype=np.float64)
    print(f"    v = {v:3d} = 2*{w:<3d} mean {float(X(r/v).mean()):.6f};  a = {w} mod {v} gives"
          f"  a*h/v = 1/2 mod 1,  so 1 + e(a theta) = 0")

print()
print("="*86)
print("2.  controls")
print("="*86)
fired = 0
print("  (a) apply the 2-part rule to odd v too (drop the j=0 case):")
for v in (3,5,7,9,15,21):
    r = np.array([x for x in range(1,v) if gcd(x,v)==1], dtype=np.float64)
    meas = float(X(r/v).mean()); wrong = L2*(1 - 2/int(totient(v)))
    f = abs(meas-wrong) > 1e-9; fired += f
    print(f"      v={v:3d} measured {meas:.6f}  wrong {wrong:.6f}  differs {f}")
print("  (b) apply the floor with the AMBIENT modulus instead of the orbit's own")
print("      subgroup -- the r143a error: for A odd and v even the orbit is a coset")
print("      of the index-2 subgroup, so the floor is (1-2/v)log2, not (1-1/v)log2:")
A = np.arange(1, 200001, 2)
for v in (8, 16, 32, 64, 256):
    h = next(c for c in range(v//2, 0, -1) if gcd(c, v) == 1)
    truth = float(X(A*h/v).mean()); wrong = (1-1/v)*L2; right = (1-2/v)*L2
    f = wrong > truth + 1e-9; fired += f
    print(f"      v={v:5d} truth {truth:.6f}  ambient-group floor {wrong:.6f} (> truth: {f})"
          f"  orbit-subgroup floor {right:.6f}")
print(f"  controls fired {fired}/11")

print()
print("="*86)
print("3.  thm:modfour as the w = 1 case")
print("="*86)
print(f"  {'v=2^j':>7s} {'mean X':>10s} {'as a multiple of log2':>22s} {'|prod| <= 2^k * exp(-k*mean)':>30s}")
for j in range(2, 9):
    v = 2**j; p = predicted(v)
    print(f"  {v:7d} {p:10.6f} {p/L2:22.6f} {'2^{-k * %.4f}'%(p/L2):>30s}")
print(f"  the minimum over all v is at v = 4: (1/2)log 2, i.e. 2^(-k/2) = (1/sqrt2)^k"
      f" = {2**-0.5:.6f}^k")
print("  every other v (odd, or divisible by 4 with an odd part > 1) gives the full")
print("  log 2, i.e. 2^(-k).  The obstruction is at the powers of two and nowhere")
print("  else -- which is prop:twopower, reached from an exact evaluation instead of")
print("  from the group-theoretic characterisation.")

print()
print("="*86)
print("4.  the surrogate ceilings: what a bounded surrogate costs before any")
print("    equidistribution input is invoked")
print("="*86)
n = 4_000_000; tt = (np.arange(n) + 0.5)/n - 0.5
rows = [("X(t) itself",                X(tt).mean(),                       L2,      "log 2"),
        ("(1/2) sin^2(pi t)",          (0.5*np.sin(np.pi*tt)**2).mean(),   0.25,    "1/4"),
        ("(pi^2/2) ||t||^2",           ((pi**2/2)*fd(tt)**2).mean(),       pi**2/24,"pi^2/24")]
print(f"  {'mean over the circle of':28s} {'measured':>11s} {'exact':>11s} {'':>9s} {'factor lost':>12s}")
for lbl, meas, ex, sym in rows:
    print(f"  {lbl:28s} {meas:11.6f} {ex:11.6f} {sym:>9s} {L2/ex:11.3f}x")
print("  both surrogates are valid pointwise:")
t = np.linspace(-0.5, 0.5, 2_000_001)[1:-1]
for lbl, s in (("(1/2)sin^2", 0.5*np.sin(np.pi*t)**2), ("(pi^2/2)||t||^2", (pi**2/2)*fd(t)**2)):
    print(f"    X(t) >= {lbl:16s} violations {int(np.sum(s > X(t) + 1e-12)):8d}"
          f"   equality only at t = 0")
print("  they are valid and they are lossy: X has a logarithmic singularity at the")
print("  half-integers and the surrogates do not, and that singularity carries the")
print("  difference between 1/4 and log 2.")

print()
print("="*86)
print("5.  on a real minor arc: A = the odd primes up to 200000")
print("="*86)
P = np.array([p for p in primerange(3, 200001)], dtype=np.int64)
print(f"  |A| = {len(P)}")
print(f"  {'v':>7s} {'true D/k':>10s} {'evaluation':>11s} {'S1 best':>9s} {'S2 best':>9s} {'gain/S1':>8s} {'gain/S2':>8s}")
for v in (3,5,7,11,17,101,1009,10007, 4,8,16,32,256, 12,20,60):
    h = next(c for c in range(v//2, 0, -1) if gcd(c, v) == 1); th = h/v
    p = predicted(v)
    truth = float(X(P*th).mean())
    s1 = 0.5*float((np.sin(np.pi*P*th)**2).mean())
    s2 = (pi**2/2)*float((fd(P*th)**2).mean())
    print(f"  {v:7d} {truth:10.6f} {p:11.6f} {s1:9.5f} {s2:9.5f} {p/s1:8.2f} {p/s2:8.2f}")
print("  'S1 best' and 'S2 best' are the surrogates handed their exponential sum and")
print("  their discrepancy EXACTLY -- no Weyl, no Koksma, no error term.  They still")
print("  lose by the factors of section 4, because the loss is in the surrogate and")
print("  not in the equidistribution input.")

print()
print("="*86)
print("6.  does the evaluation survive a shift?  (it is a minor ARC, not a point)")
print("="*86)
print("  cor:floor makes a single coset's floor uniform in t.  The reduced residues")
print("  are a Mobius-SIGNED combination of cosets, and a signed combination of lower")
print("  bounds is not a lower bound.  So this has to be measured, not assumed.")
print(f"  {'v':>6s} {'v mod 4':>8s} {'at t=0':>10s} {'min over t':>11s} {'argmin':>9s} {'t=0 minimal':>12s}")
for v in (3,5,7,9,11,15,21,25, 4,8,16,32, 12,20,60):
    R = np.array([r for r in range(1,v) if gcd(r,v)==1], dtype=np.float64)
    ts = np.linspace(0, 1.0/v, 20001)
    vals = np.array([X(t + R/v).mean() for t in ts])
    i = int(np.argmin(vals)); at0 = float(X(R/v).mean()); mn = float(vals[i])
    print(f"  {v:6d} {v%4:8d} {at0:10.6f} {mn:11.6f} {ts[i]:9.6f} {str(mn >= at0-1e-9):>12s}")
print("  v odd: NOT minimal.  At v = 3 the average falls from log2 to (1/2)log2 at")
print("  t = 1/3, since the shift carries a reduced residue onto 0 where X = 0.")
print("  v = 0 mod 4: minimal in every case tested.  For v = 2^j that is proved --")
print("  the reduced residues are a single coset, so cor:floor applies -- and for")
print("  4m with m odd > 1 it is measured only.")
print()
print("  the single-coset floor, by contrast, is uniform in t and proved:")
for v in (3,5,8,16,32):
    ts = np.linspace(0,1.0/v,20001); K = np.arange(v)
    mn = min(float(X(t + K/v).mean()) for t in ts)
    print(f"    v={v:4d}  min over t {mn:.6f}   floor (1-1/v)log2 {(1-1/v)*L2:.6f}"
          f"   holds {mn >= (1-1/v)*L2 - 1e-9}")
