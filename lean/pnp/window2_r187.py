# window2_r187.py -- the same pre-registered experiment, pushed to the largest k the exact
# computation reaches, with the diagnostics that decide whether the asymptotic regime has started
# at all.  The pre-registration is window_r187.py's and is not restated or amended here.
#
# WHY THIS FILE EXISTS.  window_r187 confirmed fable-5's control law (rho_k*(2/c)^k flat at
# c = 1.6, converging at c = 1.4) and returned a signal that swings by an order of magnitude
# between neighbouring k.  Two explanations, and they are distinguishable:
#   (a) the asymptotic regime has not started -- e/Gamma is O(1), not O(small), so there is no
#       correction being measured, only the raw disagreement of a small object;
#   (b) the regime has started and the scatter is granularity in lm/r, which moves in steps of
#       1/r(n).
# Print r(n) and e/Gamma and the answer is immediate.  ADDED, not substituted: no number from
# window_r187 is recomputed differently here.
import math

def cfamily(k, c):
    A = [1]
    for j in range(1, k):
        A.append(A[-1] + 2*max(1, int(round(c**j))))
    return A
def gamma_of(A):
    k = len(A)
    m = [(A[0]-1)//2] + [(A[j]-A[j-1])//2 for j in range(1, k)]
    return 1.0 + 2.0*sum(m[j]*2.0**(-j) for j in range(k) if m[j])
def Qk_and_sigma2(A):
    k = len(A); sig2 = sum(a*a for a in A)/4.0
    dcap = max(1, (A[-1]-1)//2); G = gamma_of(A)
    tot = 0.0; idx = 0; n = 0; l = 0.0; s = 0.0
    for d in range(1, dcap+1):
        while idx < k and A[idx] <= 2*d:
            n += 1; l += A[idx]; s += A[idx]*A[idx]; idx += 1
        tot += 2.0**(-n)*((d + l/2.0)**2 - s/4.0)
    return tot/G, sig2, G

def lm_r_and_r(A):
    k = len(A); T = sum(A)
    if T % 2: return None, None
    n = T//2
    f = [0]*(T+1); f[0] = 1
    for a in A:
        for m in range(T, a-1, -1):
            if f[m-a]: f[m] += f[m-a]
    r = f[n]
    if r == 0: return None, 0
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
            if d == 0:
                tot += g[n] if n <= sB else 0
            else:
                if n+d <= sB: tot += g[n+d]
                t2 = n - d - (T - sB)
                if 0 <= t2 <= sB: tot += g[t2]
    return tot/r, r

print('=== has the asymptotic regime started?  r(n) and e/Gamma at every reachable k ===')
print('   %6s %4s %12s %14s %14s %12s %12s %12s'
      % ('c','k','T','r(n)','lm/r','Gamma_k','e/Gamma','e/rho_k'))
data = {}
for c, KS in ((1.4, (14,16,18,20,22,24,26,28,30)), (1.6, (14,16,18,20,22,24))):
    for k in KS:
        A = cfamily(k, c); T = sum(A)
        if T > 1_500_000:
            print('   %6.2f %4d %12.2e   skipped (cost)' % (c, k, T)); continue
        v, r = lm_r_and_r(A)
        if v is None:
            print('   %6.2f %4d %12.2e   skipped (odd total)' % (c, k, T)); continue
        Q, s2, G = Qk_and_sigma2(A); rho = Q/s2
        e = abs(v-G); data[(c,k)] = (e, rho, G, r)
        print('   %6.2f %4d %12.2e %14d %14.6f %12.6f %12.4f %12.2f'
              % (c, k, T, r, v, G, e/G, e/rho))
    print()

print('=== the verdict this decides ===')
for c in (1.4, 1.6):
    ks = sorted(kk for (cc,kk) in data if cc == c)
    if not ks: continue
    rel = [data[(c,k)][0]/data[(c,k)][2] for k in ks]
    print('   c = %.1f : e/Gamma runs %s' % (c, ' '.join('%.3f' % x for x in rel)))
    print('             r(n) runs      %s' % ' '.join('%d' % data[(c,k)][3] for k in ks))
print()
print('   If e/Gamma is O(1) and not falling, the limit lm/r -> Gamma has not begun at these k')
print('   and NOTHING about its rate can be measured -- neither hypothesis is being tested.')
print('   If it is falling, fit the rate and compare with log(2/c).')
print()
for c in (1.4, 1.6):
    ks = sorted(kk for (cc,kk) in data if cc == c)
    if len(ks) < 4: continue
    xs = ks[-5:]; ys = [math.log(data[(c,k)][0]) for k in xs]
    nn=len(xs); mx=sum(xs)/nn; my=sum(ys)/nn
    slope = sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
    resid = [y - (my + slope*(x-mx)) for x,y in zip(xs,ys)]
    spread = max(resid)-min(resid)
    print('   c = %.1f : fitted rate %.4f against log(2/c) = %.4f ; residual spread in log e = %.2f'
          % (c, -slope, math.log(2.0/c), spread))
print()
print('   A residual spread of order 1 in log e means the fitted rate carries an uncertainty of')
print('   roughly spread/(k-range), and that number must be printed beside the rate or the')
print('   agreement is being asserted rather than measured.')
