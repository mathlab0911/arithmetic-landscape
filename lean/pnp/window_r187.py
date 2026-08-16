# window_r187.py -- the window experiment, pre-registered per fable-5's r186 Ruling B,
# with Ruling A applied: the CONTROL'S COMPUTATION is registered too, not only the prediction.
#
# ===================== PRE-REGISTRATION (nothing below the MEASUREMENT line changes it) =====
#
# THE WINDOW.  2^(1/3) = 1.2599 < c < 2, where Gamma is finite (R = 2/c > 1) but the constant
# Q(0) is not.  (H) fails throughout -- sigma/N is bounded there, so Appendix A's machinery does
# not start -- so this is Reading 2's most exposed point.
#
# fable-5's DERIVED LAW, checked below before it is used.  Layer gaps 2c^j give a_j ~ c^j, hence
# N_d ~ log_c d and 2^{-N_d} ~ d^{-lam} with lam = log2/log c.  With delta_d ~ d and s_d ~ d^2
# the Q-terms are ~ d^{2-lam}; truncated at the canonical cut d < a_k/2 ~ c^k,
#     Q_k ~ (c^k)^{3-lam} = c^{3k} 2^{-k}      (using c^lam = 2),
#     sigma_k^2 ~ c^{2k},
#     rho_k = Q_k/sigma_k^2 ~ (c/2)^k .
# The k-independent constant dies at lam = 3, i.e. c = 2^(1/3); the RUNNING correction does not.
#
# THE TWO HYPOTHESES, separated by functional form in k at fixed c:
#   LAYER   : e(k,c) = |lm/r - Gamma_k| tracks rho_k, i.e. decays exponentially at rate
#             log(2/c) -- a rate that MOVES WITH c in a named way.
#   ZEROS   : the distance 1/c - 1/2 is k-independent and cannot produce a c-tuned exponential
#             rate in k.
#
# PREDICTION : e(k,c)/rho_k(c) bounded above and below over k, at c in {1.4, 1.6}.
# FALSIFIER  : e decaying polynomially in k, or exponentially at a rate that does NOT move with
#              c as log(2/c).  Either kills the layer reading and re-opens the zeros' hearing.
# PRINTED    : e*(2/c)^k and the per-c fitted rates; every row carried, including the ones where
#              finite-k degradation shows.
#
# THE CONTROL'S COMPUTATION, REGISTERED (Ruling A, new this round):
#   * Q_k is summed over d = 1 .. floor((a_k - 1)/2) -- the last d with N_d < k.  This cut is
#     canonical and fixed here; it is NOT a tuning knob.  Convergence is tested in k, never in
#     the cap.
#   * sigma^2 = (1/4) sum_i a_i^2, the centre value; no tilt.
#   * Gamma_k is the finite grouped form 1 + 2 sum_j m_j 2^{-j}, dropping the degenerate N_d = k
#     tail, exactly as r183 defines it -- the same Gamma the error e is measured against.
#   * POSITIVE CONTROL of the pipeline: at c = 1 the same code must return Q(0) -> 61/3.
#   * lm/r is exact: no sampling, no asymptotics.
#
# WHAT A CONFIRMATION IS (C20, stated in advance).  Nothing here becomes proved.  A clean result
# registers as: EXPERIMENTALLY CONFIRMED ON THE WINDOW -- (H) is sufficient but not necessary,
# and the honest hypothesis for hrate-a is R > 1.
# ============================================================================================
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
    return 1.0 + 2.0*sum(m[j]*2.0**(-j) for j in range(k) if m[j])

def Qk_and_sigma2(A):
    """Q_k at the canonical cut d < a_k/2, and sigma^2 at the centre.  No free parameters."""
    k = len(A)
    sig2 = sum(a*a for a in A)/4.0
    dcap = max(1, (A[-1]-1)//2)
    G = gamma_of(A)
    tot = 0.0; idx = 0; n = 0; l = 0.0; s = 0.0
    for d in range(1, dcap+1):
        while idx < k and A[idx] <= 2*d:
            n += 1; l += A[idx]; s += A[idx]*A[idx]; idx += 1
        tot += 2.0**(-n)*((d + l/2.0)**2 - s/4.0)
    return tot/G, sig2, G

print('=== 0. CHECKING fable-5 s EXPONENTS BEFORE USING THEM (they asked) ===')
print('   claim: rho_k = Q_k/sigma^2 ~ (c/2)^k on 2^(1/3) < c < 2.')
print('   %6s %5s %16s %16s %16s %14s'
      % ('c','k','Q_k','sigma^2','rho_k','rho_k*(2/c)^k'))
ok = True
for c in (1.4, 1.6, 1.8):
    prev = None
    for k in (12, 16, 20, 24, 28):
        A = profile(k, c)
        Q, s2, G = Qk_and_sigma2(A)
        rho = Q/s2
        print('   %6.2f %5d %16.6e %16.6e %16.6e %14.6e'
              % (c, k, Q, s2, rho, rho*(2.0/c)**k))
    print()
print('   the last column is flat in k exactly when the derived law holds;')
print('   a trend in it is a defect in the derivation, not in the measurement.')

print()
print('=== 0b. POSITIVE CONTROL of the pipeline: Q(0) -> 61/3 at c = 1 ===')
for k in (16, 20, 24, 28):
    A = odds(k); Q, s2, G = Qk_and_sigma2(A)
    print('   k = %2d   Q(0) = %.6f   Gamma = %.8f   (61/3 = %.6f)' % (k, Q, G, 61/3))

print()
print('--- MEASUREMENT BEGINS ---')
print()

def lm_over_r(A):
    """Exact lm/r at the centre.  B_d takes only k distinct values as d runs, because B_d is the
    suffix {a > 2d}; so k subset-sum tables suffice, not a_k/2 of them."""
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
    # group d by the suffix it selects: for start index i, B = A[i:], valid while 2d >= a_{i-1}
    # and 2d < a_i, i.e. d in [ceil(a_{i-1}/2), ceil(a_i/2) - 1]; i = 0 means d < ceil(a_0/2)
    for i in range(k):
        B = A[i:]; sB = sum(B)
        lo = 0 if i == 0 else (A[i-1]+1)//2
        hi = (A[i]+1)//2 - 1
        if hi < lo: continue
        # any d in this group with sB < n + d contributes nothing and ends the scan
        if sB < n + lo: break
        g = [0]*(sB+1); g[0] = 1
        for a in B:
            for m in range(sB, a-1, -1):
                if g[m-a]: g[m] += g[m-a]
        for d in range(lo, hi+1):
            if sB < n + d: break
            if d == 0:
                tot += g[n] if n <= sB else 0
            else:
                if n+d <= sB: tot += g[n+d]
                t2 = n - d - (T - sB)
                if 0 <= t2 <= sB: tot += g[t2]
    return tot/r

print('=== 1. the window: does e track rho_k = Q_k/sigma^2 ? ===')
print('   %6s %5s %14s %14s %14s %14s %12s %14s'
      % ('c','k','lm/r','Gamma_k','e','rho_k','e/rho_k','e*(2/c)^k'))
res = {}
for c in (1.4, 1.6):
    for k in (10, 12, 14, 16, 18, 20):
        A = profile(k, c); T = sum(A)
        if T > 3_000_000:
            print('   %6.2f %5d   skipped, T = %.2e' % (c, k, T)); continue
        Q, s2, G = Qk_and_sigma2(A)
        rho = Q/s2
        v = lm_over_r(A)
        if v is None:
            print('   %6.2f %5d   skipped, odd total' % (c, k)); continue
        e = abs(v-G)
        res[(c,k)] = (e, rho)
        print('   %6.2f %5d %14.8f %14.8f %14.6e %14.6e %12.4f %14.6e'
              % (c, k, v, G, e, rho, e/rho if rho else float('nan'), e*(2.0/c)**k))
    print()

print('=== 2. the fitted decay rate of e, against log(2/c) ===')
print('   %6s %18s %18s %12s' % ('c','fitted rate of e','log(2/c)','ratio'))
for c in (1.4, 1.6):
    ks = sorted(kk for (cc,kk) in res if cc == c)
    if len(ks) < 3: print('   %6.2f   too few points' % c); continue
    xs = ks[-4:] if len(ks) >= 4 else ks
    ys = [math.log(res[(c,k)][0]) for k in xs]
    nn = len(xs); mx = sum(xs)/nn; my = sum(ys)/nn
    slope = sum((x-mx)*(y-my) for x, y in zip(xs, ys))/sum((x-mx)**2 for x in xs)
    rate = -slope
    print('   %6.2f %18.6f %18.6f %12.4f' % (c, rate, math.log(2.0/c), rate/math.log(2.0/c)))
print()
print('   PREDICTION: the ratio is 1 and e/rho_k is bounded above and below.')
print('   FALSIFIER : polynomial decay, or a rate that does not move with c as log(2/c).')
