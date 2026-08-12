# r1step3_r136.py -- Step 3, corrected.
#
# The first form of the budget capped |He3| at 2, which is only right for z_max <= 2, and the
# test then failed at primes k=32 where z_max = 2.55.  Not a budget failure -- a test outside
# the budget's own stated condition -- but the condition must be IN the budget rather than
# beside it, or the next person will do what I just did.
#
# Tight-at-both-ends suprema on |z| <= Z (D2: no threshold, a factor that degrades gracefully):
#     sup |He3| <= min(3Z, 2 + Z^3)            He3(0) = 0   -> vanishes as Z -> 0
#     sup |He4| <=  3 + 6Z^2 + Z^4             He4(0) = 3
#     sup |He6| <= 15 + 45Z^2 + 15Z^4 + Z^6    He6(0) = -15
#
#   eps*(Z) = (|K3|/6s^3) min(3Z, 2+Z^3)
#           + (K4/24s^4)(3 + 6Z^2 + Z^4)
#           + (K3^2/72s^6)(15 + 45Z^2 + 15Z^4 + Z^6)
#           + (4/25) S5/s^5                      <- the Step 2 remainder
#
# Checked against the TRUE relative error of the Gaussian, from exact dynamic programming,
# over the whole window.  It must bound it at every k, including the ones where Z > 2.
import math
from r1budget_r133 import profile, solve_s, cumulants, window

def tilt(a, s): return 1.0/(1.0+math.exp(min(700.0, s*a)))

def exact_pmf(B, s):
    T = sum(B); f = [0.0]*(T+1); f[0] = 1.0
    for a in B:
        p = tilt(a, s); g = [0.0]*(T+1)
        for m in range(T+1):
            v = f[m]
            if v == 0.0: continue
            g[m] += v*(1-p)
            if m+a <= T: g[m+a] += v*p
        f = g
    return f

def eps_star(K2, K3, K4, S5, Z):
    sg = math.sqrt(K2)
    return (abs(K3)/(6*sg**3))*min(3*Z, 2+Z**3) \
         + (abs(K4)/(24*sg**4))*(3 + 6*Z*Z + Z**4) \
         + (K3*K3/(72*sg**6))*(15 + 45*Z*Z + 15*Z**4 + Z**6) \
         + (4.0/25.0)*S5/sg**5

print('eps*(Z) against the true relative error of the Gaussian, exact DP over the window.')
print('  %8s %5s %5s %8s %13s %13s %8s'
      % ('profile', 'k', 'x', 'z_max', 'true |rel err|', 'eps*', 'ratio'))
bad = 0
for name in ('odds', 'primes'):
    for x in (0.06, 0.20):
        for k in (32, 48, 64, 80):
            A = profile(name, k); T = sum(A); n = int((0.5-x)*T)
            s = solve_s(A, n); B = [a for a in A if a > 2]
            mu, K2, K3, K4 = cumulants(B, s); sg = math.sqrt(K2)
            S5 = sum(a**5*tilt(a,s)*(1-tilt(a,s)) for a in B)
            W = window(A, k); Z = W/sg
            eps = eps_star(K2, K3, K4, S5, Z)
            f = exact_pmf(B, s)
            worst = 0.0
            lo = max(0, int(mu - W)); hi = min(len(f)-1, int(mu + W))
            for m in range(lo, hi+1):
                if f[m] == 0: continue
                z = (m-mu)/sg
                gau = math.exp(-0.5*z*z)/(sg*math.sqrt(2*math.pi))
                worst = max(worst, abs(f[m]/gau - 1))
            ok = eps >= worst
            if not ok: bad += 1
            print('  %8s %5d %5.2f %8.4f %13.4e %13.4e %8.2f  %s'
                  % (name, k, x, Z, worst, eps, eps/worst,
                     'bounds' if ok else '*** FAILS ***'))
        print()
print('failures: %d' % bad)
print()
print('and how eps* scales once z_max has fallen below 1')
print('  %8s %5s %8s %13s %10s' % ('profile', 'k', 'z_max', 'eps*', 'k*eps*'))
for name in ('odds', 'primes'):
    for k in (100, 200, 300, 450):
        A = profile(name, k); T = sum(A); n = int(0.44*T)
        s = solve_s(A, n); B = [a for a in A if a > 2]
        mu, K2, K3, K4 = cumulants(B, s); sg = math.sqrt(K2)
        S5 = sum(a**5*tilt(a,s)*(1-tilt(a,s)) for a in B)
        W = window(A, k); Z = W/sg
        print('  %8s %5d %8.4f %13.4e %10.4f'
              % (name, k, Z, eps_star(K2, K3, K4, S5, Z),
                 k*eps_star(K2, K3, K4, S5, Z)))
    print()
