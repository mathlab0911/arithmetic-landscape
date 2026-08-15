# r1lift_r164.py -- fable-5's F-1 and F-2, assembled, plus the one place their recipe breaks.
#
# F-1 (accepted verbatim): the absolute-to-relative conversion carries e^{Z^2/2}.
#     relative residual = rho * sigma / phi(z),  sup over |z| <= Z is  rho*sigma*sqrt(2pi)*e^{Z^2/2}.
#     The bare 2/phi(0) is valid only for Z <= sqrt(2 ln 2) = 1.1774,
#     the bare 16 C_T S5/sigma^5 only for Z <= sqrt(ln(pi/2)) = 0.6720.   Both checked below.
#
# F-2 (accepted, with one correction): eps_hi must shed its O(.).  The moments and the cube
#     split are fable's and are verified below.  BUT their third ingredient does not work:
#
#     "restrict k so that |X| <= 1 on |t| <= T_1, factor e, folded into the same threshold"
#
#     |X(t)| <= |alpha||t|^3/6 + |beta|t^4/24, and at the edge t = T_1 = sigma/N this is
#     |alpha|T_1^3/6 ~ k^{-1/2} * k^{3/2} / 6 = k/6.  It DIVERGES.  A threshold in k makes it
#     worse, not better -- the condition holds for SMALL k and fails for large.  This is
#     rem:notsup's own lesson, one section later: a sup over a window where the integrand is
#     already negligible charges the whole window at its worst point.
#
#     The repair is to cut where the Taylor bounds are actually true and let the quadratic
#     estimate carry the rest:
#
#       T* = min{ T_1, (3/|alpha|)^{1/3}, (12/|beta|)^{1/4}, (sigma^5/(C_T S5))^{1/5} }
#
#     On |t| <= T*: |X| <= 1 and |R5| <= 1, so e^{|X|} <= e and |e^{R5}-1| <= 2|R5|.
#     On T* <= |t| <= T_1: every phase is <= 1, so |psi(t/sigma)| <= exp(-c t^2) with
#     c = 1 - cos(1) = 0.4597 (proved below), and the contribution is <= exp(-c T*^2) times a
#     constant.  T* ~ k^{1/6}, so this is exp(-c k^{1/3}): smaller than any power of k, which
#     is exactly the bucket rem:threshold already prints for the region beyond T_1.
#
# Then, with all integrals extended to R (which dominates), the residual on the probability
# scale is rho/sigma with
#
#   rho = (1/2pi) * INT e^{-t^2/2} [ 2e|R5| + (e/6)|X|^3 + |ab||t|^7/144 + b^2 t^8/1152 ] dt
#
# and the four Gaussian moments turn that into explicit constants.
import math

C_T = 2*(2+math.pi)/32
print('=== 1. fable-5\'s four Gaussian moments, verified ===')
def mom(j, n=4000001, L=40.0):          # trapezoid, |t|^j against e^{-t^2/2}
    h = 2*L/(n-1); s = 0.0
    for i in range(n):
        t = -L + i*h; w = 0.5 if (i == 0 or i == n-1) else 1.0
        s += w*math.exp(-0.5*t*t)*abs(t)**j
    return s*h
claim = {7: 96.0, 8: 105*math.sqrt(2*math.pi), 9: 768.0, 12: 10395*math.sqrt(2*math.pi),
         5: 16.0}
for j in sorted(claim):
    num = mom(j)
    print('  INT e^{-t^2/2}|t|^%-2d dt  claimed %14.6f   numeric %14.6f   rel %.2e'
          % (j, claim[j], num, abs(num/claim[j]-1)))

print()
print('=== 2. the cube split (a+b)^3 <= 4(a^3+b^3), and the two validity thresholds ===')
worst = 0.0
for i in range(1, 400):
    for jj in range(1, 400):
        a = i/50.0; b = jj/50.0
        worst = max(worst, (a+b)**3/(4*(a**3+b**3)))
print('  max (a+b)^3 / 4(a^3+b^3) over a,b in (0,8]  = %.6f   (must be <= 1; =1 at a=b)' % worst)
print('  2/phi(0) valid iff e^{Z^2/2} <= 2      -> Z <= %.4f' % math.sqrt(2*math.log(2)))
print('  bare 16C_T term valid iff sqrt(2/pi)e^{Z^2/2} <= 1 -> Z <= %.4f'
      % math.sqrt(math.log(math.pi/2)))

print()
print('=== 3. the quadratic estimate used beyond T*: |psi| <= exp(-(1-cos 1) t^2) ===')
c = 1-math.cos(1.0)
mn = min((1-math.cos(v/1000.0))/(v/1000.0)**2 for v in range(1, 1001))
print('  min_{0<|v|<=1} (1-cos v)/v^2 = %.6f   >= 1-cos(1) = %.6f  : %s'
      % (mn, c, 'OK' if mn >= c-1e-12 else 'FAILS'))
print('  so |psi(t/sigma)|^2 <= exp(-2c t^2) and |psi| <= exp(-c t^2), c = %.4f' % c)

print()
print('=== 4. the explicit constants of rho ===')
I5, I7, I8, I9, I12 = 16.0, 96.0, 105*math.sqrt(2*math.pi), 768.0, 10395*math.sqrt(2*math.pi)
e = math.e; tp = 2*math.pi
cR5 = (1/tp)*2*e*I5*C_T                      # 2e|R5| , |R5| <= C_T S5 |t|^5/sigma^5
cab = (1/tp)*I7/144.0                        # |alpha||beta||t|^7/144
cbb = (1/tp)*I8/1152.0                       # beta^2 t^8/1152
ca3 = (1/tp)*(e/6)*4*I9/216.0                # (e/6)|X|^3 , cube split, |alpha|^3 part
cb3 = (1/tp)*(e/6)*4*I12/13824.0             # (e/6)|X|^3 , |beta|^3 part
print('  rho = %.4f*S5/sigma^5 + %.4f*|alpha||beta| + %.5f*beta^2 + %.4f*|alpha|^3 + %.4f*|beta|^3'
      % (cR5, cab, cbb, ca3, cb3))
print('  (for comparison the old bare term was 16*C_T = %.4f, and it was a RELATIVE bound;'
      % (16*C_T))
print('   the new one is absolute and is multiplied by sqrt(2pi)e^{Z^2/2} = %.4f at Z=0)'
      % math.sqrt(2*math.pi))

print()
print('=== 5. does fable-5\'s "|X| <= 1 on the whole window" hold?  and does T* grow? ===')
from r1budget_r133 import profile, solve_s, cumulants, window
def tilt(a, s): return 1.0/(1.0+math.exp(min(700.0, s*a)))

def data(name, k, x):
    A = profile(name, k); T = sum(A); n = int((0.5-x)*T)
    s = solve_s(A, n); B = [a for a in A if a > 2]
    mu, K2, K3, K4 = cumulants(B, s); sg = math.sqrt(K2)
    S5 = sum(a**5 for a in B); N = max(B)
    al, be = K3/sg**3, K4/sg**4
    return A, B, s, mu, sg, al, be, S5, N, window(A, k)

print('  %8s %5s %5s %9s %9s %11s %9s %11s'
      % ('profile','k','x','T_1','|X|(T_1)','T*','T*/k^(1/6)','exp(-cT*^2)'))
for name in ('odds','primes'):
    for k in (32, 64, 128, 256):
        A,B,s,mu,sg,al,be,S5,N,W = data(name,k,0.20)
        T1 = sg/N
        XT1 = abs(al)*T1**3/6 + abs(be)*T1**4/24
        Ts = min(T1, (3/abs(al))**(1/3), (12/abs(be))**0.25, (sg**5/(C_T*S5))**0.2)
        print('  %8s %5d %5.2f %9.3f %9.2f %11.4f %9.4f %11.2e'
              % (name,k,0.20,T1,XT1,Ts,Ts/k**(1/6.0),math.exp(-c*Ts*Ts)))
print('  |X|(T_1) grows with k  -> fable-5\'s crude route fails exactly where it is needed.')
print('  T* grows like k^{1/6}  -> the outer piece is exp(-c k^{1/3}): beyond all orders.')

print()
print('=== 6. dominance: the assembled eps* against the true relative error, exact DP ===')
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

def eps_new(al, be, S5, sg, Z):
    herm = (abs(al)/6)*min(3*Z, 2+Z**3) \
         + (abs(be)/24)*(3 + 6*Z*Z + Z**4) \
         + (al*al/72)*(15 + 45*Z*Z + 15*Z**4 + Z**6)
    rho  = cR5*S5/sg**5 + cab*abs(al)*abs(be) + cbb*be*be + ca3*abs(al)**3 + cb3*abs(be)**3
    return herm + math.sqrt(2*math.pi)*math.exp(0.5*Z*Z)*rho

def eps_old(al, be, S5, sg, Z):
    return (abs(al)/6)*min(3*Z, 2+Z**3) + (abs(be)/24)*(3+6*Z*Z+Z**4) \
         + (al*al/72)*(15+45*Z*Z+15*Z**4+Z**6) + 16*C_T*S5/sg**5

print('  %8s %5s %5s %8s %12s %12s %8s %12s'
      % ('profile','k','x','Z','true |rel|','eps* (new)','ratio','eps* (old)'))
bad = 0
for name in ('odds','primes'):
    for x in (0.06, 0.20):
        for k in (32, 48, 64, 80):
            A,B,s,mu,sg,al,be,S5,N,W = data(name,k,x)
            Z = W/sg
            en = eps_new(al,be,S5,sg,Z); eo = eps_old(al,be,S5,sg,Z)
            f = exact_pmf(B, s); worst = 0.0
            lo = max(0, int(mu-W)); hi = min(len(f)-1, int(mu+W))
            for m in range(lo, hi+1):
                if f[m] == 0: continue
                z = (m-mu)/sg
                gau = math.exp(-0.5*z*z)/(sg*math.sqrt(2*math.pi))
                worst = max(worst, abs(f[m]/gau - 1))
            ok = en >= worst
            if not ok: bad += 1
            print('  %8s %5d %5.2f %8.4f %12.4e %12.4e %8.2f %12.4e  %s'
                  % (name,k,x,Z,worst,en,en/worst,eo,'bounds' if ok else '*** FAILS ***'))
        print()
print('  failures: %d / 16' % bad)
print()
print('=== 7. does the new eps* still go to zero, and at what rate? ===')
for name in ('odds','primes'):
    row = []
    for k in (100, 200, 300, 450):
        A,B,s,mu,sg,al,be,S5,N,W = data(name,k,0.20); Z = W/sg
        row.append(k*eps_new(al,be,S5,sg,Z))
    print('  %8s  k*eps* at k=100,200,300,450 : %s' % (name, ' '.join('%.3f' % v for v in row)))
