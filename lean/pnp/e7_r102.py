#!/usr/bin/env python3
"""
r102 / E7 of spec_paper4_concept_r097:  M = 20 random odd instances through the full
paper-3 pipeline.  This is the empirical floor under paper 4 section 4's intended
zero-ineffective-constant theorem.

MODEL (Cramer, on the odd integers).  Each odd m in [3,N] is included independently with
probability p_m = 2/log m, and N is fixed so that E|A| = k_target.  Nothing is conditioned,
so |A| fluctuates from instance to instance.  That is deliberate: k*R is the k-invariant
quantity, so an ensemble of genuinely different sizes tests the 1/k law for free.

MEASURED per instance, exactly as paper 3 measures the primes:
  (1) (H): SUM_d 2^{-N_d} delta_d^2 and the window W(k).  Section 4 is unconditional only
      if (H) holds for the random instances THEMSELVES, so this is a precondition, not a
      result.  Measured first, and it can stop the run.
  (2) Phi-agreement at the centre: measured lm/deg vs Phi(0) = W_D.
  (3) The Table-1 residual R(x) in paper 3's signal-fraction language, x = 0.06..0.30, with
      each instance's OWN N_d, sigma_d.
  (4) k*R(x): the c_A/k law across instances.  Cross-instance concentration is the claim.
  (5) The peak spectrum h(q) = max_{(r,q)=1} (PROD_a |cos(pi r a / q)|)^{1/|A|}, q <= 60.

*** AUDIT OF THE BRIEF, BEFORE RUNNING IT (F18/F46). ***
The spec says "the modulus-4 floor of papers 1-2, which is universal for odd sequences, is
then the exact leading ripple".  Checking that against the papers rather than the spec:
  - paper 2 abstract: the modulus-4 floor is (1/sqrt2)^{|B|} and NEVER vanishes.  Indeed
    |cos(pi a/4)| = 1/sqrt2 for EVERY odd a, so h(4) = 1/sqrt2 identically -- deterministic,
    not just universal.
  - paper 2 lem:vanish: the peak at modulus 2m (m odd) is exactly 0 as soon as a = 3 mod 6
    occurs in A.  A random odd sequence contains such an element almost surely (density
    1/3); a set of primes contains at most one (namely 3).
  So the statement under test is SHARPER than the brief: for the RANDOM model the
  modulus-6 peak sqrt3/2 is identically zero and the modulus-4 floor is the leading peak,
  whereas for the PRIMES it is not -- the primes' modulus-6 ripple is a structural feature
  that the Cramer model on the odd integers destroys.  Both are measured in (5).

FAIL RULE.  Any instance failing (H) (series not O(1), or W(k) growing like a power), or any
q <= 60 with h(q) > 1/sqrt2 in the random ensemble, or any residual outside [0, 10]% ->
print the raw numbers and stop, do not average.
"""
import math
import numpy as np

# reuse the audited paper-3 pipeline: measured(), Phi(), Hstats(), pow_profile()
_s = open('alpha_r092.py').read().split("print('=' * 108)")[0]
_ns = {}
exec(compile(_s, 'alpha_r092.py', 'exec'), _ns)
globals().update(_ns)


def odd_primes(k):
    out, n = [], 3
    while len(out) < k:
        if all(n % p for p in range(3, int(n ** .5) + 1, 2)):
            out.append(n)
        n += 2
    return out


def cramer_N(ktarget):
    """smallest odd N with SUM_{odd m in [3,N]} 2/log m >= ktarget."""
    tot, m = 0.0, 3
    while tot < ktarget:
        tot += 2.0 / math.log(m)
        m += 2
    return m - 2


def cramer_instance(N, rng):
    """each odd m in [3,N] independently included with probability min(1, 2/log m)."""
    ms = np.arange(3, N + 1, 2)
    p = np.minimum(1.0, 2.0 / np.log(ms))
    return [int(m) for m in ms[rng.random(len(ms)) < p]]


def peak_spectrum(A, qmax=60):
    """h(q) = max_{(r,q)=1} (PROD_a |cos(pi r a / q)|)^{1/|A|}.  Returns dict q -> h."""
    a = np.asarray(A, float)
    k = len(A)
    out = {}
    for q in range(2, qmax + 1):
        best = 0.0
        for r in range(1, q):
            if math.gcd(r, q) != 1:
                continue
            c = np.abs(np.cos(np.pi * r * a / q))
            if c.min() < 1e-12:
                h = 0.0
            else:
                h = math.exp(float(np.log(c).sum()) / k)
            best = max(best, h)
        out[q] = best
    return out


RH = [0.44, 0.40, 0.30, 0.20]           # x = 0.5 - rho = 0.06, 0.10, 0.20, 0.30
XS = [0.5 - r for r in RH]
FLOOR = 1.0 / math.sqrt(2.0)
SEED = 102
M = 20

print('=' * 104)
print('E7 / r102 -- M = 20 random odd instances (Cramer model), full paper-3 pipeline')
print(f'  seed = {SEED};  x = 0.5 - rho in {XS}')
print('=' * 104)


def run_one(A):
    """returns (k, Gamma, meas0, Rpct[x], lam[x], Hser, W)."""
    A = sorted(A)
    k = len(A)
    m = measured(A, RH)
    r0, l0 = m[0.5]
    p0 = Phi(A, l0)
    Rs, lams = [], []
    for r in RH:
        rm, lam = m[r]
        pp = Phi(A, lam)
        Rs.append(abs(((rm - pp) - (r0 - p0)) / (rm - r0)) * 100.0)
        lams.append(lam)
    hs, W = Hstats(A)
    return k, p0, r0, Rs, lams, hs, W


for KT in (120, 180):
    N = cramer_N(KT)
    rng = np.random.default_rng(SEED + KT)
    print()
    print('-' * 104)
    print(f'  target E|A| = {KT}   (Cramer cut-off N = {N};  for comparison the {KT}th odd '
          f'prime is {odd_primes(KT)[-1]})')
    print('-' * 104)
    print(f"  {'inst':>5} {'k':>5} {'a_1':>5} {'Gamma=Phi(0)':>13} {'meas/Gamma-1':>13} "
          f"{'(H) series':>11} {'W':>8} " + ''.join(f'  R(x={x:.2f})' for x in XS))
    rows, bad = [], []
    for i in range(M):
        A = cramer_instance(N, rng)
        k, gam, r0, Rs, lams, hs, W = run_one(A)
        rows.append((A, k, gam, r0, Rs, lams, hs, W))
        flag = ''
        if hs > 1e4 or any(not (0.0 <= v <= 10.0) for v in Rs):
            flag = '  <-- FAIL RULE'
            bad.append(i)
        print(f'  {i:5d} {k:5d} {A[0]:5d} {gam:13.6f} {r0/gam-1:13.3e} '
              f'{hs:11.2f} {W:8.1f} ' + ''.join(f'  {v:8.3f}%' for v in Rs) + flag)
    if bad:
        print(f'  *** FAIL RULE fired on instances {bad}: raw rows above, no averaging. ***')

    ks = np.array([r[1] for r in rows], float)
    Rm = np.array([r[4] for r in rows], float)          # M x 4
    kR = Rm * ks[:, None]
    print()
    print(f'  cross-instance concentration ({M} instances, k in '
          f'[{int(ks.min())},{int(ks.max())}]):')
    print(f"      {'x':>6} {'mean R%':>10} {'sd R%':>9} {'mean k*R':>10} {'sd k*R':>9} "
          f"{'sd/mean':>9} {'min k*R':>9} {'max k*R':>9}")
    for j, x in enumerate(XS):
        print(f'      {x:6.2f} {Rm[:,j].mean():10.3f} {Rm[:,j].std(ddof=1):9.3f} '
              f'{kR[:,j].mean():10.2f} {kR[:,j].std(ddof=1):9.2f} '
              f'{kR[:,j].std(ddof=1)/kR[:,j].mean():9.4f} {kR[:,j].min():9.2f} '
              f'{kR[:,j].max():9.2f}')

    # reference rows: the two named sequences at the same k
    kref = int(round(ks.mean()))
    print()
    print(f'  reference, same k = {kref}:')
    for nm, f in (('primes', odd_primes), ('odds', lambda kk: [2 * i + 1 for i in range(kk)])):
        A = sorted(f(kref))
        k, gam, r0, Rs, lams, hs, W = run_one(A)
        print(f'      {nm:>8} {k:5d} {A[0]:5d} {gam:13.6f} {r0/gam-1:13.3e} '
              f'{hs:11.2f} {W:8.1f} ' + ''.join(f'  {v:8.3f}%' for v in Rs)
              + f'   k*R = ' + ' '.join(f'{k*v:7.2f}' for v in Rs))

# ------------------------------------------------------------------ (5) peaks
print()
print('=' * 104)
print('(5) peak spectrum.  CORRECTION TO MY OWN FIRST PASS: the set that carries the minor')
print('    arcs is B_d = {a in A : a > 2d}, not A.  Measured over A the modulus-6 peak dies')
print('    for the PRIMES too, because 3 = 3 (mod 6) is in A; but 3 leaves B_d at d >= 2.')
print('    h_d(q) = max_{(r,q)=1} (PROD_{a in B_d} |cos(pi r a/q)|)^{1/|B_d|},  q <= 120')
print(f'    modulus-4 floor 1/sqrt2 = {FLOOR:.6f};  modulus-6 peak sqrt3/2 = '
      f'{math.sqrt(3)/2:.6f}')
print('=' * 104)
rng = np.random.default_rng(SEED)
N = cramer_N(180)
cases = [('random #%d' % i, sorted(cramer_instance(N, rng))) for i in range(5)]
cases += [('primes', odd_primes(180)), ('odds', [2 * i + 1 for i in range(180)])]
print(f"  {'sequence':>10} {'d':>3} {'|B_d|':>6} {'h(4)':>10} {'h(6)':>10} "
      f"{'max h(q) q>=3':>14} {'argmax':>7} {'#(=3 mod 6) in B_d':>19}")
viol = []
for nm, A in cases:
    A = sorted(A)
    for d in (1, 2, 5):
        B = [a for a in A if a > 2 * d]
        h = peak_spectrum(B, qmax=120)
        top = max(((v, q) for q, v in h.items() if q >= 3))
        n3 = sum(1 for x in B if x % 6 == 3)
        if nm.startswith('random') and top[0] > FLOOR + 1e-9:
            viol.append((nm, d, top))
        print(f'  {nm:>10} {d:3d} {len(B):6d} {h[4]:10.6f} {h[6]:10.6f} {top[0]:14.6f} '
              f'{top[1]:7d} {n3:19d}')
if viol:
    print(f'  *** FAIL RULE: a random instance beats the modulus-4 floor: {viol} ***')
else:
    print('  No random instance beats the modulus-4 floor at any of d = 1,2,5, q <= 120.')
    print('  h(4) = 1/sqrt2 EXACTLY for every odd set (|cos(pi a/4)| = 1/sqrt2 for odd a):')
    print('  the floor is deterministic, not merely universal.  h(6) = sqrt3/2 for the primes')
    print('  once d >= 2 removes 3, and 0 for a random odd set at every d, because such a set')
    print('  contains ~|B_d|/3 elements = 3 (mod 6).')
    print('  CONSEQUENCE for section 4: the geometric rate for a random odd sequence is the')
    print('  modulus-4 floor 1/sqrt2 = 0.7071 per element, STRICTLY BETTER than the primes\'')
    print('  sqrt3/2 = 0.8660 of papers 1-2.  The primes are the harder case, not the easier.')

# ------------------------------------------------------------------ (6) z-scores
print()
print('=' * 104)
print('(6) do the primes look like a random odd sequence in this statistic?')
print('    z = (value - ensemble mean) / ensemble sd,  on c_A := k*R/100,  k ~ 180 ensemble')
print('=' * 104)
rng = np.random.default_rng(SEED + 180)
N = cramer_N(180)
ens = []
for i in range(M):
    A = cramer_instance(N, rng)
    k, gam, r0, Rs, lams, hs, W = run_one(A)
    ens.append([k * v / 100.0 for v in Rs])
ens = np.array(ens)
print(f"      {'x':>6} {'ens mean':>10} {'ens sd':>9} | {'primes':>9} {'z':>7} "
      f"| {'odds':>9} {'z':>7}")
for j, x in enumerate(XS):
    mu, sd = ens[:, j].mean(), ens[:, j].std(ddof=1)
    out = [f'      {x:6.2f} {mu:10.4f} {sd:9.4f} |']
    for f in (odd_primes, lambda kk: [2 * i + 1 for i in range(kk)]):
        A = sorted(f(175))
        _, _, _, Rs, _, _, _ = run_one(A)
        v = 175 * Rs[j] / 100.0
        out.append(f' {v:9.4f} {(v-mu)/sd:7.2f} |')
    print(''.join(out))
print('  (Table 1 of paper 3 reports the same quantity for the odd numbers as c_A -> 1.8,')
print('   the value (2a+1)^2/(4a+1) predicted at a = 1.)')
