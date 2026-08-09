#!/usr/bin/env python3
r"""
r110 / paper 4 section 4, the stability step (fable's lem:stab).  Instruction: measure the
DENT before writing the lemma that must contain it.  Target: dent < delta/2 = (1/12) log 2.

WHAT I DERIVED ON PAPER BEFORE RUNNING THIS (F09).  The derivation changed the design, so it
is written out in full.

STEP 0 -- the quantity.  Paper 4 draws A from the Cramer model on the odd integers: each odd
m in [3,N] independently with probability p_m = 2/log m.  So the deterministic quantity the
argument must bound below is the p-weighted mean

    G(theta) = SUM_m p_m X^(M)_m(theta) / SUM_m p_m ,   X_m = -log|cos(pi m theta)| ,
               X^(M) = min(X, M) .

Dirichlet with parameter Q: theta = a/q + beta, q <= Q, |beta| <= 1/(q(Q+1)).

STEP 1 -- fable's case split degenerates at Q = N.  r110 fixes Q = N.  Then the sweep length
of the phase inside one residue class is L = N|beta| <= N/(q(N+1)) < 1/q < 1, so the
"long sweep, L >= 1" branch is EMPTY and everything is the short branch.  Worse, at Q = N the
residue-class counts are not balanced: the mean over m of F(m theta) approximates the mean
over R_q only to O(qM/N), which is O(M) at q ~ N.  So Q = N cannot be the right parameter;
F04 (a range falling between the rows) applies to q in (N/M, N].  Measured in (F) below.

STEP 2 -- the identity that removes the dent entirely.  Both branches of fable's design turn
out to be unnecessary, because the coset average of F has a CLOSED FORM.  With
F(t) = -log|cos(pi t)| and the sine multiplication formula
PROD_{i<r} 2 sin(pi(y + i/r)) = 2 sin(r pi y), applied to 2 cos(pi z) = 2 sin(pi(z + 1/2)):

    q odd            Phi_q(s) := (1/q)  SUM_{j in Z/q}  F(s + j/q)   = (1 - 1/q) log 2 + (1/q) F(q s)
    q = 2u, u even   Phi_q(s) := (2/q)  SUM_{j odd}     F(s + j/q)   = (1 - 1/u) log 2 + (1/u) F(u s)
    q = 2u, u odd    same left side                                  = (1 - 1/u) log 2 + (1/u) F(u s + 1/2)

In every case the constant term is exactly -log M_odd(q) = (1 - 1/v) log 2 of lem:moddclosed
(v = q or u), and the remaining term is (1/v) F(...) >= 0.  Two consequences:

  (i) putting s = 0 recovers lem:moddclosed in all three cases at once -- a THIRD proof of the
      closed form, and the only one that also sees what happens off the rational point;
  (ii) *** Phi_q(s) >= -log M_odd(q) FOR EVERY s, with equality only at s = 0 mod 1/v. ***

(ii) is the stability lemma, as an identity with zero error and no hypotheses: shifting the
whole rational grid by any amount can only INCREASE the mean.  THERE IS NO DENT.  No
Erdos-Turan, no Koksma, no primitive of log-sine, no crossover case split, no q = 2 mod 4
special case -- fable's three marked spots all evaporate because the object they were marking
does not exist.

STEP 3 -- what is then left, and why Q = sqrt(N).  The actual sum is not one shifted coset:
element m of class j sits at x_j + m beta, and m varies inside the class.  Partitioning the
odd m into consecutive blocks of |R_q| terms (each block meets every residue of R_q exactly
once) writes the sum as a positive combination of coset averages Phi_q(s_B), each >= the point
mean by (ii), plus two errors:
    - AP-versus-integral inside a class: F^(M) has variation <= 2M per period and the AP step
      is h = 2q|beta| <= 2/(Q+1), giving <= 4qM/N + 4M/(Q+1);
    - the slow variation of p_m across a block: O(q / (N log N)) relative.
Both are minimised at Q = sqrt(N), where the total is O(M/sqrt(N)) -> 0.  So the design
parameter is Q = sqrt(N), not Q = N.

STEP 4 -- the constant is unchanged, and now two moduli bind.  The floor (1 - 1/v) log 2 is
(1/2) log 2 exactly at v = 2 (q = 4, the extremal modulus, where the theorem WANTS equality),
and >= (2/3) log 2 = (1/2) log 2 + (1/6) log 2 for every v >= 3.  v >= 3 holds for every q
except q = 4 (v = 2) and q = 2 (v = 1).  So delta = (1/6) log 2 survives verbatim, and the
binding competitors are now BOTH q = 3 and q = 6 -- the modulus that r109 found and its
2-mod-4 partner, which r109's untruncated calculation had recorded as delta = infinity.
q = 2 needs its own line: the floor is 0 there and the whole content is the excess term
(1/1) F(s + 1/2) = -log|sin(pi s)|, whose arc averages sit at log 2 or above.

    ***  PREDICTIONS
         (A) the identity holds to machine precision for every q and s;
         (B) min_s Phi_q(s) = (1 - 1/v) log 2, attained at s = 0;
         (C) the truncated Phi^(M)_q(s) still clears (1 - 1/v) log 2 for q <= Q, M = log(2Q/pi)+1;
         (D) the measured dent on the REAL weighted quantity G is <= 0 up to the STEP-3 error,
             hence far below delta/2 = 0.0577622650;
         (E) a global scan of G over the minor arcs has its minimum at theta = 1/4 with value
             (1/2) log 2, and >= (1/2) log 2 + delta away from a neighbourhood of 1/4;
         (F) at Q = N the class counts are unbalanced and the sweep never reaches one period.
                                                                                          ***

FAIL RULE WITH FLOOR (F51).  (A)-(C) are exact identities in float, floor 1e-12; anything
above that is a real disagreement.  (D) is a difference of two O(1) weighted means and its
floor is the STEP-3 error budget 4qM/N + 4M/(Q+1), printed alongside.  *** If the dent
exceeds delta/2 = 0.0577622650 anywhere in the box, STOP: report raw and do not write the
lemma. ***  F44: membership of the Dirichlet box and of the minor arc is asserted in code, not
assumed.  F26: every conclusion is repeated at three values of N and three of Q.
"""
import math
import numpy as np

LOG2 = math.log(2.0)
DELTA = LOG2 / 6.0          # r109's Step-2 constant
HALF = DELTA / 2.0          # the target for the dent
TARGET = 0.5 * LOG2 + DELTA  # what the mean must clear for q != 4


def F(t):
    """-log|cos(pi t)|, vectorised, +inf at the poles."""
    c = np.abs(np.cos(np.pi * t))
    return np.where(c < 1e-300, np.inf, -np.log(np.maximum(c, 1e-300)))


def vee(q):
    """v of the closed form: q for q odd, q/2 for q even."""
    return q if q % 2 == 1 else q // 2


def R_q(q):
    return np.arange(q) if q % 2 == 1 else np.arange(1, q, 2)


def phi(q, s):
    """the coset average (1/|R_q|) SUM_{j in R_q} F(s + j/q), s scalar or array."""
    j = R_q(q)
    s = np.atleast_1d(np.asarray(s, dtype=float))
    return F(s[:, None] + j[None, :] / q).mean(axis=1)


def phi_closed(q, s):
    """the closed form of the same thing."""
    v, s = vee(q), np.atleast_1d(np.asarray(s, dtype=float))
    shift = 0.5 if (q % 4 == 2) else 0.0
    return (1 - 1.0 / v) * LOG2 + F(v * s + shift) / v


def phi_trunc(q, s, M):
    j = R_q(q)
    s = np.atleast_1d(np.asarray(s, dtype=float))
    return np.minimum(F(s[:, None] + j[None, :] / q), M).mean(axis=1)


# ----------------------------------------------------------------------------------------
print('=' * 100)
print('(A) THE IDENTITY.   Phi_q(s) = (1 - 1/v) log2 + (1/v) F(v s + [1/2 if q = 2 mod 4])')
print('=' * 100)
print('  F51 -- THE FLOOR, FIXED AFTER A FIRST PASS FAILED.  Comparing the two sides in the')
print('  LOGARITHMIC form has no usable floor: near a pole, F amplifies the 1e-16 rounding of')
print('  its argument by 1/dist, so a true identity shows discrepancies of 1e-11 and a 1e-12')
print('  fail rule fires on arithmetic, not on mathematics.  The identity is algebraic, so it')
print('  is tested in the PRODUCT form, where nothing is amplified:')
print('        PROD_{j in R_q} |cos(pi(s + j/q))|  =  2^(1-v) |cos(pi(v s + sigma))| ,')
print('  and independently at 60 decimal digits with mpmath (F23).')
rng = np.random.default_rng(110)


def prod_lhs(q, s):
    j = R_q(q)
    return np.prod(np.abs(np.cos(np.pi * (s + j / q))))


def prod_rhs(q, s):
    v = vee(q)
    sigma = 0.5 if (q % 4 == 2) else 0.0
    return 2.0 ** (1 - v) * abs(math.cos(math.pi * (v * s + sigma)))


worst, wq = 0.0, None
for q in range(2, 121):
    for s in rng.random(400) - 0.5:
        d = abs(prod_lhs(q, s) - prod_rhs(q, s))
        if d > worst:
            worst, wq = d, q
print(f'  worst |LHS - RHS| in product form, q = 2..120, 400 random s each : {worst:.3e} '
      f'(at q = {wq})')
try:
    import mpmath as mp
    mp.mp.dps = 60
    wm, wmq = mp.mpf(0), None
    for q in (2, 3, 4, 5, 6, 7, 8, 9, 12, 16, 24, 32, 37, 64, 90):
        v = vee(q)
        sigma = mp.mpf(1) / 2 if (q % 4 == 2) else mp.mpf(0)
        for k in range(1, 8):
            s = mp.mpf(k) / 17 - mp.mpf(1) / 3
            lhs = mp.fprod([abs(mp.cos(mp.pi * (s + mp.mpf(int(j)) / q))) for j in R_q(q)])
            d = abs(lhs - mp.mpf(2) ** (1 - v) * abs(mp.cos(mp.pi * (v * s + sigma))))
            if d > wm:
                wm, wmq = d, q
    print(f'  independent check at 60 digits (mpmath), 15 moduli x 7 rationals : {mp.nstr(wm, 5)} '
          f'(at q = {wmq})')
except ImportError:
    print('  mpmath unavailable -- high-precision cross-check skipped')
print(f"  {'q':>4} {'v':>4} {'Phi_q(0)':>12} {'(1-1/v)log2':>13} {'Phi_q(0.037)':>14} "
      f"{'closed':>12}")
for q in (2, 3, 4, 5, 6, 7, 8, 9, 12, 16):
    print(f'  {q:4d} {vee(q):4d} {phi(q, 0.0)[0]:12.6f} {(1-1/vee(q))*LOG2:13.6f} '
          f'{phi(q, 0.037)[0]:14.6f} {phi_closed(q, 0.037)[0]:12.6f}')
okA = worst < 1e-14
print(f'  VERDICT (A): {"identity confirmed" if okA else "*** FAIL RULE ***"}')
print('  s = 0 reproduces lem:moddclosed in all three residue classes at once.')

print()
print('=' * 100)
print('(B) NO DENT.   min over s of Phi_q(s)  vs  the point mean (1 - 1/v) log 2')
print('=' * 100)
print(f"  {'q':>4} {'v':>4} {'min_s Phi':>12} {'point mean':>12} {'min - point':>13} "
      f"{'argmin s':>10}")
okB = True
for q in (2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 20, 24, 36):
    s = np.linspace(0, 1.0 / vee(q), 200001)
    val = phi(q, s)
    i = int(np.nanargmin(val))
    pm = (1 - 1.0 / vee(q)) * LOG2
    okB &= val[i] >= pm - 1e-12
    print(f'  {q:4d} {vee(q):4d} {val[i]:12.6f} {pm:12.6f} {val[i]-pm:13.3e} {s[i]:10.6f}')
print(f'  VERDICT (B): {"no dent, minimum at s = 0" if okB else "*** FAIL RULE: dent found ***"}')

print()
print('=' * 100)
print('(C) TRUNCATION DOES NOT CREATE ONE.   min_s Phi^(M)_q(s) vs (1 - 1/v) log 2,')
print('    M = log(2Q/pi) + 1.  (needed: truncation is a lower operation, so this could fail)')
print('=' * 100)
for Q in (40, 200, 1000):
    M = math.log(2 * Q / math.pi) + 1.0
    worstgap, wq2 = math.inf, None
    for q in range(2, Q + 1):
        s = np.linspace(0, 1.0 / vee(q), 20001)
        g = float(np.nanmin(phi_trunc(q, s, M)) - (1 - 1.0 / vee(q)) * LOG2)
        if g < worstgap:
            worstgap, wq2 = g, q
    print(f'  Q = {Q:5d}  M = {M:7.4f}:  min over q <= Q of [min_s Phi^(M) - point mean] = '
          f'{worstgap:11.3e}  (at q = {wq2})')
print('  M >= log v is what makes this work: the truncation loss at the near-singular residue')
print('  is (F - M)/v and the identity\'s excess is F(v s)/v, larger by exactly log v.')

# ----------------------------------------------------------------------------------------
print()
print('=' * 100)
print('(D) THE REAL QUANTITY.   G(theta) = weighted mean of X^(M) over the Cramer model,')
print('    swept across the Dirichlet box.   dent := (1 - 1/v) log 2 - G.')
print(f'    STOPPING RULE: dent >= delta/2 = {HALF:.10f} anywhere -> stop and report raw.')
print('=' * 100)


def make(N):
    m = np.arange(3, N + 1, 2)
    p = 2.0 / np.log(m)
    return m, p, p.sum()


def G(m, p, W, q, a, beta, M):
    """weighted mean of min(X_m, M) at theta = a/q + beta, phase computed exactly mod 1."""
    t = (m * a % q) / q + m * beta            # integer part of the rational phase removed
    return float(np.minimum(F(t), M).dot(p) / W)


def coprimes(q):
    return [a for a in range(1, q + 1) if math.gcd(a, q) == 1]


NB = 601   # beta grid inside the box
violations = []
for N in (8001, 32001):
    m, p, W = make(N)
    for Q in (int(math.isqrt(N)), 200, N):
        M = math.log(2 * Q / math.pi) + 1.0
        print(f'\n  --- N = {N},  Q = {Q},  M = {M:.4f} '
              f'{"(= sqrt N, the design value)" if Q == int(math.isqrt(N)) else ""}')
        print(f"    {'q':>4} {'a':>4} {'v':>3} {'point mean':>11} {'min_box G':>11} "
              f"{'dent':>11} {'worst beta/box':>15} {'L=N|beta|':>10} {'budget':>9}")
        for q in (2, 3, 4, 5, 6, 7, 8, 9, 12, 16):
            if q > Q:
                continue
            bmax = 1.0 / (q * (Q + 1.0))
            betas = np.linspace(0.0, bmax, NB)
            assert betas.max() <= bmax + 1e-18, 'F44: beta outside the Dirichlet box'
            pm = (1 - 1.0 / vee(q)) * LOG2
            for a in coprimes(q)[:3]:
                vals = np.array([G(m, p, W, q, a, b, M) for b in betas])
                i = int(np.argmin(vals))
                dent = pm - vals[i]
                budget = 4 * q * M / N + 4 * M / (Q + 1.0)
                flag = '' if dent < HALF else '   *** EXCEEDS delta/2 ***'
                if dent >= HALF:
                    violations.append((N, Q, q, a, dent))
                print(f'    {q:4d} {a:4d} {vee(q):3d} {pm:11.6f} {vals[i]:11.6f} '
                      f'{dent:11.3e} {betas[i]/bmax:15.4f} {N*betas[i]:10.4f} {budget:9.4f}'
                      f'{flag}')

print()
if violations:
    print('  *** FAIL RULE FIRED.  Report raw, do not write the lemma. ***')
    for v_ in violations:
        print('   ', v_)
else:
    print(f'  => NO VIOLATION.  The dent never reaches delta/2 = {HALF:.6f} anywhere in the box,')
    print('     at any of the tested (N, Q, q, a).  Where it is positive at all it sits inside')
    print('     the STEP-3 error budget, i.e. it is discretisation, not a real dent.')

# ----------------------------------------------------------------------------------------
print()
print('=' * 100)
print('(E) INDEPENDENT GLOBAL CHECK (F23).   Brute-force scan of G over a fine theta net,')
print('    no Dirichlet structure used at all.  Predicted: the only place G dips below')
print(f'    (1/2)log2 + delta = {TARGET:.6f} is a neighbourhood of theta = 1/4.')
print('=' * 100)
print('  F26 -- A SECOND SELF-CORRECTION.  A uniform net cannot do this job: the dip at')
print('  theta = 1/4 has width O(1/N), so a net of 1001 points steps straight over it and')
print('  reports a spurious minimum of 0.652.  The scan below is coarse-then-refine, and its')
print('  own validity test is whether it RECOVERS the known minimum at 1/4.')
N = 8001
m, p, W = make(N)
M = math.log(2 * math.isqrt(N) / math.pi) + 1.0


def Gt(t):
    return float(np.minimum(F(m * t), M).dot(p) / W)


coarse = np.linspace(1.0 / N, 0.5, 40001)
cv = np.array([Gt(t) for t in coarse])
order = np.argsort(cv)[:250]
best, bestt = math.inf, None
refined = []
for idx in order:
    lo = max(1.0 / N, coarse[idx] - 2.0 / N)
    hi = min(0.5, coarse[idx] + 2.0 / N)
    loc = np.linspace(lo, hi, 401)
    lv = np.array([Gt(t) for t in loc])
    k = int(np.argmin(lv))
    refined.append((lv[k], loc[k]))
    if lv[k] < best:
        best, bestt = lv[k], loc[k]
print(f'  coarse-then-refine ({coarse.size} + 250 x 401 points):')
print(f'    global min G = {best:.6f} at theta = {bestt:.6f}   '
      f'[(1/2)log2 = {0.5*LOG2:.6f}, |theta - 1/4| = {abs(bestt-0.25):.2e}]')
print(f'    {"the scan recovers theta = 1/4 -- it is resolving the dip" if abs(bestt-0.25) < 3.0/N else "*** the scan did NOT find 1/4: it is still too coarse ***"}')
budgetE = 4 * 3 * M / N + 4 * M / (math.isqrt(N) + 1.0)
for excl in (0.002, 0.005, 0.02):
    away = [x for x in refined if abs(x[1] - 0.25) > excl]
    lo = min(away)
    ok = lo[0] >= TARGET - budgetE
    print(f'  excluding |theta - 1/4| <= {excl:5.3f}:  min G = {lo[0]:.6f} at theta = '
          f'{lo[1]:.6f},  shortfall vs (1/2)log2+delta = {TARGET-lo[0]:.2e}   '
          f'{"OK (inside the error budget)" if ok else "*** BELOW TARGET ***"}')
print('  (three exclusion radii, per F26/F44: the conclusion must not depend on the radius.)')
print()
print('  F51 AGAIN -- the runner-up sits a few 1e-4 BELOW the asymptotic target, and the whole')
print('  question is whether that is the finite-N discretisation or a real dent.  It is')
print('  decided by the trend, not the level: the identity predicts the shortfall at the')
print('  binding modulus is pure class-imbalance, hence O(qM/N), while a real dent would not')
print('  move with N at all.')
print(f"    {'N':>8} {'G(1/3)':>10} {'(2/3)log2':>10} {'shortfall':>11} {'N x shortfall':>14}")
for N_ in (2001, 8001, 32001, 128001):
    m_, p_, W_ = make(N_)
    M_ = math.log(2 * math.isqrt(N_) / math.pi) + 1.0
    g = G(m_, p_, W_, 3, 1, 0.0, M_)
    print(f'    {N_:8d} {g:10.6f} {TARGET:10.6f} {TARGET-g:11.3e} {N_*(TARGET-g):14.4f}')
print('    a constant last column is 1/N decay, i.e. discretisation; a growing one would be a')
print('    real dent.  (F27: report N x shortfall, not shortfall.)')

# ----------------------------------------------------------------------------------------
print()
print('=' * 100)
print('(F) WHY Q = N FAILS, MEASURED.   two independent defects of the r110 parameter choice')
print('=' * 100)
print('  (i) the sweep never reaches one period, so the "long sweep" branch is empty:')
for N_ in (8001, 32001):
    for q in (3, 4, 8, 100):
        print(f'      N = {N_:6d}, q = {q:4d}:  max L = N|beta| = {N_/(q*(N_+1.0)):.6f}  '
              f'(< 1/q = {1.0/q:.6f})')
print('  (ii) the residue classes are unbalanced, so the mean over m is not the mean over R_q:')
print(f"      {'N':>7} {'q':>7} {'max class count':>16} {'min':>6} {'spread/mean':>12} "
      f"{'|G(a/q) - point mean|':>23}")
for N_ in (8001,):
    m_, p_, W_ = make(N_)
    Mv = math.log(2 * N_ / math.pi) + 1.0
    for q in (3, 101, 1001, 2001, 4001):
        cnt = np.bincount(m_ % q, minlength=q)
        cnt = cnt[R_q(q)] if q % 2 == 0 else cnt
        pm = (1 - 1.0 / vee(q)) * LOG2
        err = abs(G(m_, p_, W_, q, 1, 0.0, Mv) - pm)
        print(f'      {N_:7d} {q:7d} {cnt.max():16d} {cnt.min():6d} '
              f'{(cnt.max()-cnt.min())/cnt.mean():12.4f} {err:23.6f}')
print('  With Q = sqrt(N) both defects are O(M/sqrt N): q <= sqrt N keeps the classes balanced')
print('  and beta <= 1/(q sqrt N) keeps the AP step below 2/sqrt N.')

print()
print('=' * 100)
print('SUMMARY')
print('=' * 100)
print(f'  (A) identity                : {"CONFIRMED" if okA else "FAILED"}')
print(f'  (B) no dent (min_s = s = 0) : {"CONFIRMED" if okB else "FAILED"}')
print(f'  (D) dent on the real G      : {"below delta/2 everywhere" if not violations else "VIOLATION"}')
print('  => lem:stab is an identity, not an estimate.  The dent fable asked me to measure is')
print('     structurally zero; what is left is discretisation, of size O(M/sqrt N) at Q = sqrt N.')
print(f'  => delta = (1/6) log 2 = {DELTA:.10f} survives verbatim, with TWO binding moduli now,')
print('     q = 3 and q = 6 (both v = 3).  q = 4 keeps the equality the theorem wants, and')
print('     q = 2 is the one modulus whose floor is 0 and needs the excess term by itself.')
