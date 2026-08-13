"""
r144 -- settling rem:shift's middle row.  It settles the WRONG WAY, and it also
convicts the measurement that produced it.

Exponentiate lem:coset:  prod_{k<v} |2 cos pi(t + k/v)| = 2 |cos pi(v t + tau_v)|.
For n = 0 mod 4 the odd residues are the coset 1/n + (2/n)Z of size n/2, so

    O(n,t) := prod_{s<n, s odd} |2 cos pi(t + s/n)| = 2 |cos(pi (n/2) t)| .

Mobius over the odd part w of v = 2^j w (j >= 2), every v/d again 0 mod 4:

    Q(v,t) := prod_{r in (Z/v)*} |2 cos pi(t + r/v)|
            = 2^{[w=1]} prod_{d|w} |cos(pi (v/2d) t)|^{mu(d)} .

The average of X over the reduced residues is >= its value at t=0 exactly when
Q(v,t) <= Q(v,0).  Read off:

  w = 1  (v = 2^j):  Q = 2|cos(pi (v/2) t)| <= 2 = Q(v,0).  UNIFORM, proved.
  w > 1:             Q is a RATIO -- the mu(d) = -1 divisors sit in the
                     denominator -- and a ratio of cosines is not bounded by 1.
                     For w = 3: Q = |cos 3u| / |cos u| = |4cos^2 u - 3|, which
                     exceeds 1 whenever cos^2 u < 1/2.  So it FAILS.
"""
import numpy as np
from math import gcd, log, pi

def X(t): return -np.log(np.maximum(np.abs(np.cos(np.pi*np.asarray(t,dtype=np.float64))),1e-300))
L2 = log(2)

print("="*84)
print("1.  the scan that produced the wrong answer, and the scan that corrects it")
print("="*84)
print(f"  {'v':>5s} {'at t=0':>9s} {'min over [0,1/v]':>17s} {'min over [0,1]':>15s} {'argmin':>9s} {'verdict':>22s}")
for v in (4,8,16,32, 12,20,28,60, 3,5,9,15):
    R = np.array([r for r in range(1,v) if gcd(r,v)==1], dtype=np.float64)
    at0 = float(X(R/v).mean())
    t_short = np.linspace(0, 1.0/v, 40001); v_short = np.array([X(t+R/v).mean() for t in t_short])
    t_full  = np.linspace(0, 1.0,     40001); v_full  = np.array([X(t+R/v).mean() for t in t_full])
    i = int(np.argmin(v_full))
    ok_short = v_short.min() >= at0 - 1e-9
    ok_full  = v_full.min()  >= at0 - 1e-9
    verdict = "uniform" if ok_full else ("SHORT SCAN LIED" if ok_short else "fails, both scans")
    print(f"  {v:5d} {at0:9.6f} {v_short.min():17.6f} {v_full.min():15.6f} {t_full[i]:9.5f} {verdict:>22s}")
print()
print("  the short scan assumed period 1/v.  That is the period of the FULL-GROUP")
print("  average -- t -> t + 1/v permutes {k/v : k mod v}.  It is NOT a period of the")
print("  reduced-residue average, because t -> t + 1/v carries r/v to (r+1)/v and the")
print("  units are not closed under +1.  The symmetry used to shrink the search")
print("  belonged to a different object.")

print()
print("="*84)
print("2.  the closed form, checked, and the explicit counterexample")
print("="*84)
def Q_closed(v, t):
    f = {}; n = v
    while n % 2 == 0: f[2] = f.get(2,0)+1; n//=2
    j = f.get(2,0); w = v//2**j
    ds = [d for d in range(1, w+1) if w % d == 0]
    def mu(d):
        r, p, m = 1, 2, d
        while p*p <= m:
            if m % p == 0:
                m //= p
                if m % p == 0: return 0
                r = -r
            p += 1
        return -r if m > 1 else r
    out = 2.0**(1 if w == 1 else 0)
    for d in ds:
        e = mu(d)
        if e: out *= abs(np.cos(np.pi*(v/(2*d))*t))**e
    return out
print(f"  {'v':>5s} {'t':>8s} {'Q direct':>12s} {'Q closed':>12s} {'abs err':>10s}")
bad = 0
for v in (4,8,16,12,20,60,84):
    for t in (0.0, 0.07, 0.2, 0.33, 0.41):
        R = np.array([r for r in range(1,v) if gcd(r,v)==1], dtype=np.float64)
        direct = float(np.prod(np.abs(2*np.cos(np.pi*(t + R/v)))))
        closed = float(Q_closed(v, t)); e = abs(direct-closed)
        bad += e > 1e-9*max(1,abs(direct))
        print(f"  {v:5d} {t:8.2f} {direct:12.6f} {closed:12.6f} {e:10.2e}")
print(f"  mismatches: {bad}")

print()
v, t = 12, 0.2
R = np.array([r for r in range(1,v) if gcd(r,v)==1], dtype=np.float64)
print(f"  COUNTEREXAMPLE  v = {v}, t = {t}")
print(f"    reduced residues r/v      : {list(np.round(R/v,4))}")
print(f"    t + r/v                   : {list(np.round(t+R/v,4))}")
print(f"    X at those points         : {list(np.round(X(t+R/v),4))}")
print(f"    average                   : {float(X(t+R/v).mean()):.6f}")
print(f"    value at t = 0            : {float(X(R/v).mean()):.6f}  ( = log 2 )")
print(f"    so the average FALLS by     {float(X(R/v).mean()-X(t+R/v).mean()):.6f}")
print(f"    and w = 3 predicts it: Q = |cos 3u|/|cos u| = |4cos^2 u - 3| > 1 for")
print(f"    cos^2 u < 1/2, with u = pi (v/6) t = pi*{v/6*t:.4f}")

print()
print("="*84)
print("3.  so the trichotomy is a DICHOTOMY, and it is prop:twopower again")
print("="*84)
print("  the evaluation of prop:redresidue is a BOUND on the surrounding arc")
print("  if and only if v is a power of two -- i.e. exactly when the reduced")
print("  residues form a coset.  For every other v the average falls under a shift.")
print(f"  {'v':>5s} {'power of 2':>11s} {'min over [0,1]':>15s} {'value at 0':>11s} {'bound?':>8s}")
for v in (4,8,16,32,64, 3,5,7,9,12,15,20,21,28,60,84):
    R = np.array([r for r in range(1,v) if gcd(r,v)==1], dtype=np.float64)
    tt = np.linspace(0,1,40001); mn = min(float(X(t+R/v).mean()) for t in tt)
    at0 = float(X(R/v).mean()); p2 = (v & (v-1)) == 0
    print(f"  {v:5d} {str(p2):>11s} {mn:15.6f} {at0:11.6f} {str(mn >= at0-1e-9):>8s}")
