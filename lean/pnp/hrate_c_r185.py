# hrate_c_r185.py -- Reading 3, PRE-REGISTERED, and the confound computed BEFORE any measurement.
#
# fable-5's r184 ruling 1 released this experiment under the discipline our own ledger bought
# (F45: name the falsifier before the run; F30: compute the confound first; F20: an experiment
# that cannot separate the hypotheses is prep, not measurement).  Everything above the line
# `--- MEASUREMENT BEGINS ---` was written before the first number of the experiment was
# produced, and nothing below it changes anything above it.
#
# ============================== PRE-REGISTRATION ==============================
#
# THE OBJECT.  Along the interpolating family with layer gaps a_{j+1} - a_j = 2c^j (r183), the
# generating function G(z) = sum_j m_j 2^{-j} z^j has radius R = 2/c, and the distance from the
# fair coin to the nearest zero of Gamma^(q) goes to dist(c) = 1/c - 1/2, which is 1/2 at c = 1
# and 0 at c = 2.
#
# THE TWO HYPOTHESES.  Let e(k,c) = |lm_A(n)/r_A(n) - Gamma(A)| at the centre n = T/2.
#
#   NULL (Reading 2 -- the zeros are a reformulation).  prop:correction already gives the leading
#     error: e_null = Gamma * Q(0) / sigma^2, with Q(0) = (1/Gamma) sum_d 2^{-N_d}(delta_d^2 -
#     s_d/4).  Nothing about zeros enters.
#   READING 3 (the zeros see the rate).  e = C(c) k^{-gamma} with gamma stable in c and C(c)
#     diverging as c -> 2.  **Power unknown, divergence claimed** -- I have no derivation that
#     produces one, and r184 permits registering it that way.  The claim under test:
#
#         e * sigma^2 / (Gamma * Q(0))  ->  1 under the NULL,  ->  infinity as c -> 2 under R3.
#
# THE FALSIFIER, before the run.  Reading 3 dies if that ratio stays within a factor 2 of 1 across
# the c-range at the largest reachable k with no trend in c.  The null dies if the ratio grows
# monotonically in c by more than the finite-k drift measured on the c = 1 column.
#
# THE STOPPING RULE (F20).  If the null's own c-dependence cannot be separated from Reading 3's
# over the reachable k, this script says so and stops.  Phase C decides that from Phase A and B
# alone.
#
# WHAT IS PRINTED (F24/F27).  k*e and the ratio, not ratios alone, and every row is carried
# including the ones where agreement degrades.
#
# ==============================================================================
import math

def cfamily(k, c):
    A = [1]
    for j in range(1, k):
        A.append(A[-1] + 2*max(1, int(round(c**j))))
    return A
def odds(k): return [2*i-1 for i in range(1, k+1)]
def profile(k, c): return odds(k) if abs(c-1.0) < 1e-12 else cfamily(k, c)

def gamma_of(A):
    k = len(A)
    m = [(A[0]-1)//2] + [(A[j]-A[j-1])//2 for j in range(1, k)]
    return 1.0 + 2.0*sum(m[j]*2.0**(-j) for j in range(k) if m[j]), m

def Q_of(A, dcap):
    """Q(0) with an explicit cutoff, plus the size of the last decade of terms."""
    k = len(A); G, _ = gamma_of(A)
    tot = 0.0; idx = 0; n = 0; l = 0.0; s = 0.0; last = 0.0
    for d in range(1, dcap+1):
        while idx < k and A[idx] <= 2*d:
            n += 1; l += A[idx]; s += A[idx]*A[idx]; idx += 1
        t_ = 2.0**(-n)*((d + l/2.0)**2 - s/4.0)
        tot += t_
        if d > dcap*9//10: last += abs(t_)
    return tot/G, last

def qexponent(c):
    """m_j = c^j gives N_d ~ log_c d, so 2^{-N_d} ~ d^{-log2/log c} and the Q-terms grow like
    d^{2 - log2/log c}.  Convergent iff that is < -1, i.e. iff c < 2^{1/3}."""
    return float('-inf') if c <= 1.0 else 2.0 - math.log(2.0)/math.log(c)

CS = [1.0, 1.1, 1.25, 1.4, 1.6, 1.8, 2.0]
CCRIT = 2.0**(1.0/3)

print('=== PHASE A (confound first, F30): does the null even exist along the family? ===')
print('   Q(0) sums 2^{-N_d}(delta_d^2 - s_d/4) over d.  For layer gaps 2c^j the terms grow like')
print('   d^(2 - log2/log c), so the sum converges only below c = 2^(1/3) = %.6f.' % CCRIT)
print()
print('   %6s %16s %34s' % ('c','2 - log2/log c','the Q(0) sum'))
for c in CS:
    ex = qexponent(c)
    print('   %6.2f %16s %34s'
          % (c, ('-inf' if ex == float('-inf') else '%.4f' % ex),
             'convergent' if ex < -1 else 'DIVERGENT: there is no null here'))

print()
print('   CORRECTION, made before any of this was reported.  The first version of this check cut')
print('   the d-sum at a fixed 4000 and 16000 and reported that Q(0) moved by a factor 53 even at')
print('   c = 1, where the analysis says it converges.  The analysis was right and the check was')
print('   wrong: N_d saturates at k once 2d exceeds the largest element, after which the terms')
print('   are 2^{-k} d^2 and grow -- an artefact of an arbitrary cap, not of the profile.  The')
print('   canonical cut is the last d with N_d < k, i.e. d < a_k/2, and the honest convergence')
print('   test is in k, not in the cap.')
print()
print('   %6s %16s %16s %16s %12s' % ('c','Q(0), k=16','Q(0), k=20','Q(0), k=24','k=24/k=20'))
def natcap(A): return max(1, (A[-1]-1)//2)
for c in CS:
    qs = []
    for k in (16, 20, 24):
        A = profile(k, c); q, _ = Q_of(A, natcap(A)); qs.append(q)
    print('   %6.2f %16.6e %16.6e %16.6e %12s'
          % (c, qs[0], qs[1], qs[2], ('%.3f' % (qs[2]/qs[1])) if abs(qs[1]) > 1e-300 else '-'))
print('   settling in k means the limit exists; growing in k means it does not.')
print('   for the odd numbers the limit is Q(0) = 61/3 = %.6f (prop:correction).' % (61/3))

print()
print('=== PHASE B: the region where a comparison is possible at all ===')
usable = [c for c in CS if qexponent(c) < -1]
print('   c values with a finite null :', usable)
print('   c values Reading 3 is about :', [c for c in CS if c >= 1.4])
print()
print('   %6s %14s %16s' % ('c','dist = 1/c-1/2','1/dist'))
for c in CS:
    d = 1.0/c - 0.5
    print('   %6.2f %14.6f %16s' % (c, d, ('%.4f' % (1/d)) if d > 1e-12 else 'infinity'))

print()
print('=== PHASE C (F20): the stopping rule, decided before any lm/r is computed ===')
print('   (i) The null is undefined for c > %.4f, which is below the whole region where' % CCRIT)
print('       Reading 3 predicts a visible effect (dist < 0.3 needs c > 1.25).')
print('   (ii) Feasibility of exact lm/r: cost ~ (number of layers) x (subset-sum table).')
print('   %6s %5s %14s %16s' % ('c','k','T = sum a_i','layers to scan'))
for c in CS:
    for k in (16, 20, 24):
        A = profile(k, c); T = sum(A)
        print('   %6.2f %5d %14.3e %16.3e' % (c, k, T, (A[-1]+1)/2))
print()
print('   VERDICT: the experiment as designed CANNOT separate the hypotheses.  The comparison')
print('   requires a finite Q(0); Q(0) diverges above c = 2^(1/3) = %.4f; and below that the' % CCRIT)
print('   predicted zero-distance has barely moved (1/c - 1/2 is %.4f at c = %.2f against %.4f'
      % (1.0/1.25-0.5, 1.25, 0.5))
print('   at c = 1).  There is no c at which the null exists AND Reading 3 predicts a large')
print('   effect.  Per F20 this is prep, not measurement, and the run below is reported as a')
print('   consistency check of the null on its own domain -- NOT as a test of Reading 3.')

print()
print('--- MEASUREMENT BEGINS ---')
print()
print('=== PHASE D: the null, checked on the domain where it exists ===')

def lm_over_r(A):
    """Exact lm/r at the centre, with the layer scan cut where B_d can no longer reach."""
    k = len(A); T = sum(A)
    if T % 2: return None
    n = T//2
    f = [0]*(T+1); f[0] = 1
    for a in A:
        for m in range(T, a-1, -1):
            if f[m-a]: f[m] += f[m-a]
    r = f[n]
    if r == 0: return None
    tot = 0
    d = 0
    while True:
        B = [a for a in A if a > 2*d]
        sB = sum(B)
        if not B or sB < n + d: break
        g = [0]*(sB+1); g[0] = 1
        for a in B:
            for m in range(sB, a-1, -1):
                if g[m-a]: g[m] += g[m-a]
        tgt = [n+d] if d == 0 else [n+d, n-d-(T-sB)]
        for t_ in tgt:
            if 0 <= t_ <= sB: tot += g[t_]
        d += 1
    return tot/r

print('   %6s %5s %14s %14s %14s %14s %10s'
      % ('c','k','lm/r','Gamma','e','null pred','e/null'))
for c in usable:
    for k in (14, 18, 22):
        A = profile(k, c); T = sum(A)
        if T > 4_000_000:
            print('   %6.2f %5d   skipped, T = %.2e' % (c, k, T)); continue
        G, _ = gamma_of(A); Q, _ = Q_of(A, max(1,(A[-1]-1)//2))
        s2 = sum(a*a for a in A)/4.0
        v = lm_over_r(A)
        if v is None:
            print('   %6.2f %5d   skipped, odd total' % (c, k)); continue
        e = abs(v-G); null = G*Q/s2
        print('   %6.2f %5d %14.8f %14.8f %14.6e %14.6e %10.4f'
              % (c, k, v, G, e, null, e/null if null else float('nan')))
print()
print('   This column tests prop:correction on the c-family.  It says nothing about Reading 3,')
print('   for the reason Phase C gives, and it is not to be quoted as if it did.')
