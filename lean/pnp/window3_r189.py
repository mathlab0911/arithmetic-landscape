# window3_r189.py -- the instrument round granted by fable-5's r188 Ruling D.
#
# ================================ PRE-REGISTRATION ================================
#
# WHAT IS NEW.  Not a new hypothesis: a new instrument for the same one.  In the window the
# representation counts are SMALL -- that is what sparsity means -- so exact arithmetic needs no
# big integers, and the binding constraint is table memory, not integer size.  Vectorised int64
# dynamic programming over the value range therefore reaches larger k than the pure-Python
# big-integer version, with the counts still exact by construction.
#
# OVERFLOW, RULED OUT BY A BOUND AND NOT BY OPTIMISM (Ruling A style).  Every entry of every
# table counts subsets of a set of at most k elements, so every entry is at most 2^k.  int64
# holds 2^63 - 1, so the computation is exact for every k <= 62.  This is asserted in code.
#
# VALIDATION RUNG, FIRST (Ruling D).  For k <= 28 at c = 1.4 the new instrument must reproduce
# the big-integer instrument's values IDENTICALLY -- the same integers lm and r, not close ones.
# If any pair differs the run aborts and reports the instrument as unfit.  Nothing downstream is
# believed until that passes.
#
# THE HYPOTHESIS UNDER TEST, at c = 1.4 only (fable-5's instruction, and its reason: at c = 1.6
# even k = 45 probably leaves e/Gamma at O(1), and spending the round there is how the thread
# dies of marginality).  ONE c CANNOT SEPARATE THE ZERO-HYPOTHESIS BY RATE-MOVEMENT, and this
# header says so: this round tests THE LAYER LAW.  The zeros get their hearing only if it fails.
#
#     LAYER LAW  :  e(k) = |lm/r - Gamma_k|  satisfies  e * (2/c)^k  bounded over the fitted
#                   range -- equivalently e decays like rho_k ~ (c/2)^k.
#     FALSIFIER  :  systematic drift in e*(2/c)^k over the fitted range, i.e. a trend that does
#                   not flatten as k grows.
#
# (C-2) THE REACHABLE RANGE, ESTABLISHED BEFORE ANY FIT, WITH THE CRITERION REGISTERED HERE:
#     the fit may use only k with e/Gamma < 0.1, and needs at least SIX such points spanning a
#     factor 2 in the predicted e.  Fewer than six, or less than a factor 2, and the run reports
#     "range not reached" and stops.  These numbers are fable-5's defaults, fixed before the data
#     exists.
#
# (C-1) EVERY FITTED RATE IS PRINTED WITH ITS RESIDUAL SPREAD, and a fit whose spread exceeds its
#     fitted value is reported as "no rate measurable", not as a rate.
#
# STOP RULE (Ruling D).  One round.  If the criterion column never opens a fittable range by the
# largest k this machine reaches, or the spread exceeds the rate, the verdict is
# "the window is analytically open and experimentally closed at current memory; parked".
# ==================================================================================
import math, sys
import numpy as np

C = 1.4

def cfamily(k, c=C):
    A = [1]
    for j in range(1, k):
        A.append(A[-1] + 2*max(1, int(round(c**j))))
    return A

def gamma_of(A):
    k = len(A)
    m = [(A[0]-1)//2] + [(A[j]-A[j-1])//2 for j in range(1, k)]
    return 1.0 + 2.0*sum(m[j]*2.0**(-j) for j in range(k) if m[j])

def rho_of(A):
    k = len(A); sig2 = sum(a*a for a in A)/4.0
    dcap = max(1, (A[-1]-1)//2); G = gamma_of(A)
    tot = 0.0; idx = 0; n = 0; l = 0.0; s = 0.0
    for d in range(1, dcap+1):
        while idx < k and A[idx] <= 2*d:
            n += 1; l += A[idx]; s += A[idx]*A[idx]; idx += 1
        tot += 2.0**(-n)*((d + l/2.0)**2 - s/4.0)
    return (tot/G)/sig2

# ---------------------------------------------------------------- reference: big integers
def lm_r_bigint(A):
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
    for i in range(k):
        B = A[i:]; sB = sum(B)
        lo = 0 if i == 0 else (A[i-1]+1)//2
        hi = (A[i]+1)//2 - 1
        if hi < lo: continue
        if sB < n + lo: break
        g = [0]*(sB+1); g[0] = 1
        for a in B:
            for m in range(sB, a-1, -1):
                if g[m-a]: g[m] += g[m-a]
        for d in range(lo, hi+1):
            if sB < n + d: break
            if d == 0: tot += g[n] if n <= sB else 0
            else:
                if n+d <= sB: tot += g[n+d]
                t2 = n - d - (T - sB)
                if 0 <= t2 <= sB: tot += g[t2]
    return tot, r

# ---------------------------------------------------------------- the instrument: int64 numpy
def lm_r_int64(A):
    k = len(A); T = sum(A)
    assert k <= 62, 'every table entry is at most 2^k; int64 needs k <= 62'
    if T % 2: return None
    n = T//2
    # one full table for r(n)
    f = np.zeros(T+1, dtype=np.int64); f[0] = 1
    for a in A:
        f[a:] += f[:T+1-a].copy()
    r = int(f[n])
    if r == 0: return None
    del f
    # suffix tables, built from the top element downward: B_i = A[i:], B_i = B_{i+1} + {a_i}
    g = np.zeros(T+1, dtype=np.int64); g[0] = 1
    sB = 0
    tot = 0
    contrib = [None]*k          # what each i contributes, filled as i descends
    for i in range(k-1, -1, -1):
        a = A[i]
        g[a:sB+a+1] += g[:sB+1].copy()
        sB += a
        lo = 0 if i == 0 else (A[i-1]+1)//2
        hi = (A[i]+1)//2 - 1
        if hi < lo or sB < n + lo:
            contrib[i] = 0
            continue
        sub = 0
        for d in range(lo, hi+1):
            if sB < n + d: break
            if d == 0:
                if n <= sB: sub += int(g[n])
            else:
                if n+d <= sB: sub += int(g[n+d])
                t2 = n - d - (T - sB)
                if 0 <= t2 <= sB: sub += int(g[t2])
        contrib[i] = sub
    # the big-integer version stops the i-loop at the first i (ascending) with sB < n+lo;
    # ascending i means descending sB, so the same rule is: take contributions only for i below
    # the first failure.  Reproduce it exactly.
    for i in range(k):
        B_sum = sum(A[i:])
        lo = 0 if i == 0 else (A[i-1]+1)//2
        hi = (A[i]+1)//2 - 1
        if hi < lo: continue
        if B_sum < n + lo: break
        tot += contrib[i]
    return tot, r

print('=== VALIDATION RUNG: int64 instrument against big integers, identical or nothing ===')
print('   %5s %14s %18s %18s %10s' % ('k','T','lm (bigint)','lm (int64)','identical'))
bad = 0
for k in (10, 12, 14, 16, 18, 20, 22, 24, 26, 28):
    A = cfamily(k)
    ref = lm_r_bigint(A); new = lm_r_int64(A)
    if ref is None and new is None:
        print('   %5d %14d   both skipped (odd total)' % (k, sum(A))); continue
    same = (ref == new)
    if not same: bad += 1
    print('   %5d %14d %18d %18d %10s'
          % (k, sum(A), ref[0], new[0], 'yes' if same else '*** NO ***'))
print('   r values too:', all(lm_r_bigint(cfamily(k))[1] == lm_r_int64(cfamily(k))[1]
                              for k in (10,14,18,22,26) if lm_r_bigint(cfamily(k))))
if bad:
    print('   INSTRUMENT UNFIT: %d disagreement(s).  Nothing below is believed.' % bad)
    sys.exit(1)
print('   passed: the instrument reproduces the reference exactly, so it may be used.')

print()
print('=== (C-2) THE REACHABLE RANGE, before any fit ===')
print('   criterion, registered above: fit only k with e/Gamma < 0.1; at least six such points')
print('   spanning a factor 2 in the predicted e.')
print()
print('   %5s %14s %10s %16s %14s %14s %12s'
      % ('k','T','mem GB','lm/r','Gamma_k','e/Gamma','e*(2/c)^k'))
rows = []
KS = [28, 30, 32, 34, 36, 38, 40, 42, 44, 46]
for k in KS:
    A = cfamily(k); T = sum(A)
    mem = T*8/2**30 * 2
    if mem > 2.2:
        print('   %5d %14d %10.2f   skipped: table would need more memory than the machine has'
              % (k, T, mem)); continue
    out = lm_r_int64(A)
    if out is None:
        print('   %5d %14d %10.2f   skipped: odd total' % (k, T, mem)); continue
    lm, r = out
    v = lm/r; G = gamma_of(A); e = abs(v-G)
    rows.append((k, e, G, e/G, e*(2.0/C)**k))
    print('   %5d %14d %10.2f %16.8f %14.8f %14.6f %12.4e'
          % (k, T, mem, v, G, e/G, e*(2.0/C)**k))

print()
print('=== the criterion, applied ===')
good = [(k, e, EG, s) for (k, e, G, EG, s) in rows if EG < 0.1]
print('   points with e/Gamma < 0.1 : %d  (need six)' % len(good))
if good:
    es = [e for (_, e, _, _) in good]
    span = max(es)/min(es) if min(es) > 0 else float('inf')
    print('   span in e over those points : factor %.2f  (need 2)' % span)
if len(good) < 6 or (good and max(e for _,e,_,_ in good)/min(e for _,e,_,_ in good) < 2):
    print()
    print('   RANGE NOT REACHED.  Per the registered criterion the fit is not performed, and the')
    print('   verdict is: THE WINDOW IS ANALYTICALLY OPEN AND EXPERIMENTALLY CLOSED AT CURRENT')
    print('   MEMORY; PARKED.  The gap keeps its name.')
else:
    ks = [k for (k, *_ ) in good]; ys = [math.log(e) for (_, e, _, _) in good]
    nn = len(ks); mx = sum(ks)/nn; my = sum(ys)/nn
    slope = sum((x-mx)*(y-my) for x, y in zip(ks, ys))/sum((x-mx)**2 for x in ks)
    resid = [y - (my + slope*(x-mx)) for x, y in zip(ks, ys)]
    spread = max(resid)-min(resid)
    rate = -slope; unc = spread/(max(ks)-min(ks))
    print()
    print('   (C-1) fitted rate %.4f  +- %.4f (residual spread %.2f over a k-range of %d)'
          % (rate, unc, spread, max(ks)-min(ks)))
    print('         against log(2/c) = %.4f' % math.log(2.0/C))
    if unc >= rate:
        print('         SPREAD EXCEEDS THE RATE: reported as NO RATE MEASURABLE, not as a rate.')
    else:
        flat = [s for (_, _, _, s) in good]
        print('         e*(2/c)^k over the fitted range: %s' % ' '.join('%.3e' % x for x in flat))
        print('         bounded over the range means the layer law survives this round.')
