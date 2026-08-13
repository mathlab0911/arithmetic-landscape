"""
r148b -- same question, with the finite-size noise averaged out and k pushed.

The single-target run wandered (0.93, 1.16, 0.94, 1.02, 1.01): lattice and parity effects
at one target are larger than the effect being measured.  Average |lm/r| over a window of
targets around the centre, and track the RELATIVE ERROR against Gamma as k grows.  If (H)
governs the phenomenon and not just the proof, the alpha = 1/2 error should refuse to
shrink while the alpha >= 1 errors do.
"""
import numpy as np

def subset_counts(A):
    T = sum(A); dp = np.zeros(T+1); dp[0] = 1.0
    for a in A: dp[a:] += dp[:-a]
    return dp

def lm_profile(A):
    """return arrays r(n) and lm(n) for all n"""
    A = sorted(A); T = sum(A); M = A[-1]
    r = subset_counts(A)
    lm = r.copy()
    cache = {}
    for d in range(1, (M-1)//2 + 1):
        j = sum(1 for a in A if a <= 2*d)
        if j not in cache:
            hi = A[j:]
            cache[j] = (subset_counts(hi) if hi else np.array([1.0]), sum(A[:j]))
        cnt, slow = cache[j]
        L = len(cnt)
        n = np.arange(T+1)
        t1 = n + d
        m1 = t1 < L
        lm[m1] += cnt[t1[m1]]
        t2 = n - d - slow
        m2 = (t2 >= 0) & (t2 < L)
        lm[m2] += cnt[t2[m2]]
    return r, lm

def gamma(A):
    A = sorted(A); M = A[-1]
    return 1 + 2*sum(2.0**(-sum(1 for a in A if a <= 2*d)) for d in range(1, (M-1)//2 + 1))

def profile(kind, k):
    if kind == 'odds':    return [2*i-1 for i in range(1, k+1)]
    if kind == 'sqrt32':
        A, last = [], -1
        for i in range(1, k+1):
            a = 2*int((i**1.5)/2)+1
            while a <= last: a += 2
            A.append(a); last = a
        return A
    if kind == 'alpha12':
        c = 4.0*np.sqrt(k); A, last = [], -1
        for i in range(1, k+1):
            a = 2*int(c*np.sqrt(i)/2)+1
            while a <= last: a += 2
            A.append(a); last = a
        return A

print("="*92)
print("relative error of the annealed prediction, averaged over 41 central targets")
print("="*92)
print(f"  {'profile':>9s} {'(H)':>6s} {'k':>4s} {'a_1':>5s} {'Gamma':>10s} {'mean lm/r':>11s}"
      f" {'rel err':>10s} {'k*relerr':>9s}")
for kind, Hok in (('odds','holds'), ('sqrt32','holds'), ('alpha12','FAILS')):
    for k in (20, 30, 40, 55, 70, 90):
        A = profile(kind, k)
        if sum(A) > 4_000_000: print(f"  {kind:>9s} k={k} skipped, T too large"); continue
        r, lm = lm_profile(A)
        T = sum(A); c = T//2
        w = slice(c-20, c+21)
        rr, ll = r[w], lm[w]
        m = rr > 0
        val = float((ll[m]/rr[m]).mean())
        g = gamma(A); rel = abs(val-g)/g
        print(f"  {kind:>9s} {Hok:>6s} {k:4d} {A[0]:5d} {g:10.5f} {val:11.5f}"
              f" {rel:10.5f} {k*rel:9.3f}")
    print()

print("="*92)
print("fitted decay exponents:  rel err ~ C k^{-p}")
print("="*92)
import numpy as _np
for kind, Hok in (('odds','holds'), ('sqrt32','holds'), ('alpha12','FAILS')):
    ks, es = [], []
    for k in (20, 30, 40, 55, 70, 90):
        A = profile(kind, k); r, lm = lm_profile(A)
        T = sum(A); c = T//2; w = slice(c-20, c+21)
        rr, ll = r[w], lm[w]; m = rr > 0
        g = gamma(A); rel = abs(float((ll[m]/rr[m]).mean())-g)/g
        ks.append(k); es.append(rel)
    p = _np.polyfit(_np.log(ks), _np.log(es), 1)[0]
    print(f"  {kind:>9s}  (H) {Hok:>6s}   exponent p = {-p:5.2f}")
print()
print("  (H) holding or failing does not decide WHETHER the annealed prediction is")
print("  correct over this range -- it decides HOW FAST the true ratio reaches it.")
