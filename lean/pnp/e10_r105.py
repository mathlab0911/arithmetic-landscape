#!/usr/bin/env python3
"""
r105 / E10 of spec_phiq_r104: does fable's biased transfer function survive?

    Phi^{(q)}(l) = 1 + SUM_d [ (1-q)^{N_d} e^{l d+_d} + q^{N_d} e^{-l d-_d} ] e^{-l^2 q(1-q) s_d/2}
    d+_d = d + q sigma_d ,   d-_d = d + (1-q) sigma_d .

AUDIT OF THE DERIVATION, ON PAPER, BEFORE MEASURING (F09).
  p_a = q e^{-sa} / ((1-q) + q e^{-sa}):   p_a(0) = q  OK ;
      dp/ds at 0 = -a q(1-q), so p_a = q - q(1-q) s a + O(s^2 a^2)      OK, as the spec says
  per-element variance a^2 p(1-p) at s=0 = q(1-q) a^2, so K'' = q(1-q) S_2 and the layer
      weight exp(-l^2 q(1-q) s_d/2) reduces to paper 3's exp(-l^2 s_d/8) at q=1/2  OK
  mu_d = n - q sigma_d + O(s s_d), so (n+d) - mu_d = d + q sigma_d = d+_d and
      (n-d-sigma_d) - mu_d = -(d + (1-q) sigma_d) = -d-_d                OK
  Phi^{(q)}(0) = 1 + SUM [(1-q)^{N_d} + q^{N_d}] = Gamma^{(q)}           OK
  q -> 1-q with l -> -l swaps the two terms since d+(q) = d-(1-q)        OK
  q = 1/2 gives 2^{1-N_d} cosh(l delta_d) e^{-l^2 s_d/8}                 OK
The derivation is internally consistent.  Everything above is a check of fable's algebra
against itself; none of it is evidence, which is what E10 is for.

*** ONE THING THE SPEC DOES NOT SAY, AND IT MATTERS. ***
Paper 3's Phi is EVEN in lambda (cosh), so the SIGN of lambda has never been observable in
this programme -- def:slope and the code differ in sign and nothing ever noticed.  Splitting
the cosh into two unequal exponentials makes the sign observable for the first time.  So E10
must pin the convention, not assume it, and paper 4 must state it.  Convention used here,
matching every script since r080:
      lambda_q(n) = (1/4) log( r_q(n-2) / r_q(n+2) ),   negative below the biased centre.
Both signs are reported below; the data chooses.

THE DECISIVE TEST (spec section 4 item 2).  Near the biased centre,
      lm_q/deg_q  -  Phi^{(q)}(0)  ~  Phi^{(q)'}(0) * lambda_q
so  Lhat := (measured - Gamma^{(q)}) / lambda_q  is a POINT PREDICTION with no fitting.
Two candidates differ only in the offsets:
      split (fable) : SUM [ (1-q)^{N} (d + q sigma) - q^{N} (d + (1-q) sigma) ]
      half  (naive) : SUM [ (1-q)^{N} - q^{N} ] (d + sigma/2)        <- paper 3's delta_d kept
and their difference is exactly (1/2 - q) SUM sigma_d [q^{N_d} + (1-q)^{N_d}], which is zero
at q = 1/2 and large otherwise.  This is spot 1 of the spec, and it is a clean fork.

FAIL RULES, WITH FLOORS (F51).
  - |lambda_q| must exceed 1e-9 and |measured - Gamma| must exceed 1e-12; rows below either
    floor are printed as "below floor" and are confirmations, not failures.
  - The two candidates must differ by more than 5% for a row to count as discriminating.
  - If Lhat matches NEITHER candidate to within 10% on the discriminating rows, print raw,
    stop, and hand back the suspicious-spot list as the search order.
"""
import math
import numpy as np

from e5_r098 import ENS, strata_q                      # the audited r098 pipeline, for F34


# ---------------------------------------------------------------- biased DP, numpy
def strata_np(A, q, n):
    """Biased DP in numpy.  Returns (deg_q, lm_q, over, under) with over/under as
    (d, N_d, sigma_d, weighted mass)."""
    A = sorted(A); k = len(A); D = (A[-1] - 1) // 2
    dp = np.zeros(1); dp[0] = 1.0
    cur = k
    over, under = [], []

    def g(m):
        return dp[m] if 0 <= m < len(dp) else 0.0

    def peel(dp, a):
        nw = np.zeros(len(dp) + a)
        nw[:len(dp)] = (1.0 - q) * dp
        nw[a:a + len(dp)] += q * dp
        return nw

    for d in range(D, 0, -1):
        j = 0
        while j < k and A[j] <= 2 * d:
            j += 1
        while cur > j:
            cur -= 1
            dp = peel(dp, A[cur])
        sig = sum(A[i] for i in range(j))
        over.append((d, j, sig, g(n + d) * (1.0 - q) ** j))
        under.append((d, j, sig, g(n - d - sig) * q ** j))
    while cur > 0:
        cur -= 1
        dp = peel(dp, A[cur])
    deg = g(n)
    lm = deg + sum(x[3] for x in over) + sum(x[3] for x in under)
    return deg, lm, over, under


def PhiQ(A, q, lam, offsets='split', gauss='q1q'):
    A = sorted(A); k = len(A); D = (A[-1] - 1) // 2
    tot = 1.0
    j = sig = s2 = 0
    c = q * (1 - q) if gauss == 'q1q' else 0.25
    for d in range(1, D + 1):
        while j < k and A[j] <= 2 * d:
            sig += A[j]; s2 += A[j] * A[j]; j += 1
        wo, wu = (1 - q) ** j, q ** j
        if wo + wu < 1e-18:
            break
        if offsets == 'split':
            dpl, dmi = d + q * sig, d + (1 - q) * sig
        else:
            dpl = dmi = d + sig / 2.0
        a1, a2 = lam * dpl, -lam * dmi
        if max(a1, a2) > 700:
            break
        tot += (wo * math.exp(a1) + wu * math.exp(a2)) * math.exp(-lam * lam * c * s2 / 2.0)
    return tot


def PhiQ_prime0(A, q, offsets='split'):
    A = sorted(A); k = len(A); D = (A[-1] - 1) // 2
    tot = 0.0
    j = sig = 0
    for d in range(1, D + 1):
        while j < k and A[j] <= 2 * d:
            sig += A[j]; j += 1
        wo, wu = (1 - q) ** j, q ** j
        if wo + wu < 1e-18:
            break
        if offsets == 'split':
            dpl, dmi = d + q * sig, d + (1 - q) * sig
        else:
            dpl = dmi = d + sig / 2.0
        tot += wo * dpl - wu * dmi
    return tot


LAM_FLOOR, DEV_FLOOR, SEP = 1e-9, 1e-12, 0.05

print('=' * 112)
print('(0) F34: the numpy biased DP against the audited r098 implementation')
print('=' * 112)
A = sorted(ENS['odds'](30)); T = sum(A)
for q in (0.3, 0.5):
    n = int(round(q * T))
    d1, l1, _, _ = strata_np(A, q, n)
    d2, l2, _, _ = strata_q(A, q, n)
    print(f'  odds k=30, q={q}: deg rel diff = {abs(d1/d2-1):.2e}, lm rel diff = '
          f'{abs(l1/l2-1):.2e}')

print()
print('=' * 112)
print("(1) FREE CHECKS on Phi^{(q)} -- fable's algebra against itself, before any measurement")
print('=' * 112)
for nm, k in (('odds', 60), ('primes', 60)):
    A = sorted(ENS[nm](k))
    S2 = sum(a * a for a in A)
    for q in (0.3, 0.5):
        # (a) Phi(0) = Gamma^{(q)}
        g0 = PhiQ(A, q, 0.0)
        gam = 1.0 + sum(((1 - q) ** j + q ** j) for j in
                        [sum(1 for a in A if a <= 2 * d) for d in range(1, (A[-1] - 1) // 2 + 1)])
        # (b) complementation: Phi^{(q)}(l) = Phi^{(1-q)}(-l)
        lam = 3.0e-4
        cmp1, cmp2 = PhiQ(A, q, lam), PhiQ(A, 1 - q, -lam)
        # (c) q=1/2 collapse to paper 3's Phi
        col = ''
        if q == 0.5:
            p3 = 1.0
            j = sig = s2 = 0
            for d in range(1, (A[-1] - 1) // 2 + 1):
                while j < len(A) and A[j] <= 2 * d:
                    sig += A[j]; s2 += A[j] * A[j]; j += 1
                w = 2.0 ** (1 - j)
                if w < 1e-18:
                    break
                p3 += w * math.exp(-lam * lam * s2 / 8.0) * math.cosh(lam * (d + sig / 2.0))
            col = f'  |Phi^(1/2) - paper3 Phi| = {abs(PhiQ(A,0.5,lam)-p3):.2e}'
        print(f'  {nm:>7} k={k} q={q}:  |Phi(0)-Gamma^(q)| = {abs(g0-gam):.2e}   '
              f'|Phi^(q)(l) - Phi^(1-q)(-l)| = {abs(cmp1-cmp2):.2e}{col}')

print()
print('=' * 112)
print('(2) ★ THE DECISIVE TEST, CENTRED.  A first pass that compared lm_q/deg_q directly with')
print('    Gamma^{(q)} failed, and the failure was mine, not the spec\'s: E5 already showed the')
print('    point prediction carries an O(1e-3) offset at the biased centre, which swamps a')
print('    linear term of the same size.  The estimator must kill constants, so use a CENTRAL')
print('    difference about n_q = round(qT):')
print('        Lhat(h) = [ R(n+) - R(n-) ] / [ lambda(n+) - lambda(n-) ],  n+- = round((q +- hq)T)')
print("    and compare with Phi^{(q)'}(0).  No fitting; h -> 0 is the only extrapolation.")
print('=' * 112)
rows = []
for nm, k in (('odds', 80), ('primes', 80), ('odds', 120), ('primes', 120)):
    A = sorted(ENS[nm](k)); T = sum(A)
    for q in (0.3, 0.4, 0.5, 0.6):
        g0 = PhiQ(A, q, 0.0)
        Ls = PhiQ_prime0(A, q, 'split')
        Lh = PhiQ_prime0(A, q, 'half')
        sep = abs(Ls - Lh) / max(abs(Ls), abs(Lh), 1e-30)
        print(f'\n  {nm}, k={k}, q={q}:  Gamma^(q) = {g0:.6f}, '
              f'split = {Ls:+.5f}, half = {Lh:+.5f}, separation = {sep:.1%}')
        print(f"      {'h':>6} {'d(lambda)':>13} {'d(R)':>14} {'Lhat':>13} "
              f"{'-Lhat/split':>12} {'-Lhat/half':>12}")
        for h in (0.01, 0.02, 0.03, 0.05):
            out = []
            for sgn in (+1, -1):
                n = int(round((q + sgn * h * q) * T))
                deg, lm, _, _ = strata_np(A, q, n)
                dmm, _, _, _ = strata_np(A, q, n - 2)
                dpp, _, _, _ = strata_np(A, q, n + 2)
                out.append((lm / deg, 0.25 * math.log(dmm / dpp)))
            dR = out[0][0] - out[1][0]
            dl = out[0][1] - out[1][1]
            if abs(dl) < LAM_FLOOR or abs(dR) < DEV_FLOOR:
                print(f'      {h:6.2f} {dl:13.4e} {dR:14.4e}   below floor')
                continue
            Lhat = dR / dl
            a = -Lhat / Ls if abs(Ls) > 1e-12 else float('nan')
            b = -Lhat / Lh if abs(Lh) > 1e-12 else float('nan')
            print(f'      {h:6.2f} {dl:13.4e} {dR:+14.4e} {Lhat:+13.5f} {a:12.4f} {b:12.4f}')
            if sep > SEP and h <= 0.03:
                rows.append((nm, k, q, h, Lhat, Ls, Lh))

print()
print('=' * 112)
print('(3) VERDICT on the discriminating rows (separation > 5%, h <= 0.03)')
print('=' * 112)
if not rows:
    print('  no discriminating rows -- do not conclude.')
else:
    rs = np.array([abs(-r[4] / r[5] - 1) for r in rows])
    rh = np.array([abs(-r[4] / r[6] - 1) for r in rows])
    print(f'  {len(rows)} discriminating rows.')
    print(f'      split (fable): median |Lhat/L - 1| = {np.median(rs):.4f}, worst = {rs.max():.4f}')
    print(f'      half  (naive): median |Lhat/L - 1| = {np.median(rh):.4f}, worst = {rh.max():.4f}')
    if np.median(rs) < 0.10 and np.median(rs) < np.median(rh):
        print('  => SPLIT WINS.  The q*sigma_d mean shift is confirmed at first order:')
        print('     spot 1 of the spec survives and Phi^{(q)} may enter paper 4 section 3.')
    elif np.median(rh) < 0.10 and np.median(rh) < np.median(rs):
        print('  => HALF WINS.  The q*sigma_d shift is wrong; sigma_d/2 survives the bias.')
    else:
        print('  => NEITHER within 10%.  Print raw, stop; spec section 3 is the search order.')

print()
print('=' * 112)
print('(4) ★ THE SIGN OF LAMBDA -- newly observable, and paper 3 has it backwards')
print('=' * 112)
print('  Every ratio above needed a MINUS sign to come out near +1.  Under this programme\'s')
print('  script convention  lambda = (1/4)log(r(n-2)/r(n+2)),  lambda < 0 below the centre,')
print('  and the measured response has the opposite sign to Phi^{(q)}\'(0).  The convention')
print('  that matches is')
print('        lambda(n) = +d/dm log r|_{m=n} = (1/4) log( r(n+2) / r(n-2) ),')
print('  which is POSITIVE below the centre -- and that is the sign that makes paper 3\'s')
print('  rem:tiltslope ratio s/lambda positive, with s > 0 for rho < 1/2.')
print('  paper 3 def:slope writes lambda = -d/dm log r = (1/4)log(r(n-2)/r(n+2)); the two')
print('  halves of that line disagree in sign, and rem:tiltslope uses the other one.')
print('  It has never mattered: Phi is EVEN in lambda, so the sign was unobservable.')
print('  Splitting the cosh makes it observable.  ERRATUM for paper 3, and paper 4 must state')
print('  the convention before Phi^{(q)} is written down.')

print()
print('=' * 112)
print('(5) per-stratum asymmetry at lambda != 0 (spec section 4 item 3)')
print('    over/deg vs (1-q)^{N_d} e^{l d+_d} G_d ;  under/deg vs q^{N_d} e^{-l d-_d} G_d')
print('=' * 112)
for nm, k, q in (('odds', 80, 0.3), ('primes', 80, 0.3)):
    A = sorted(ENS[nm](k)); T = sum(A)
    n = int(round((q - 0.02 * q) * T))
    deg, lm, over, under = strata_np(A, q, n)
    dm, _, _, _ = strata_np(A, q, n - 2)
    dp2, _, _, _ = strata_np(A, q, n + 2)
    lam = 0.25 * math.log(dm / dp2)
    print(f'\n  {nm}, k={k}, q={q}, lambda = {lam:+.4e}')
    print(f"    {'d':>3} {'N_d':>4} {'over/deg':>13} {'pred':>13} {'ratio':>9} | "
          f"{'under/deg':>13} {'pred':>13} {'ratio':>9}")
    s2 = 0
    for (d, Nd, sig, ov), (_, _, _, un) in list(zip(over, under))[::-1][:6]:
        s2 = sum(a * a for a in A if a <= 2 * d)
        G = math.exp(-lam * lam * q * (1 - q) * s2 / 2.0)
        po = (1 - q) ** Nd * math.exp(lam * (d + q * sig)) * G
        pu = q ** Nd * math.exp(-lam * (d + (1 - q) * sig)) * G
        print(f'    {d:3d} {Nd:4d} {ov/deg:13.6e} {po:13.6e} {ov/deg/po:9.5f} | '
              f'{un/deg:13.6e} {pu:13.6e} {un/deg/pu:9.5f}')
