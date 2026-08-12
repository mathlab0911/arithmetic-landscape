# r1proof_r141.py -- can Lemma A.1's constant be PROVED rather than measured?
#
# The obstacle: spec_r1_r133 S2b gives |log(1-p+p e^{iv}) - P4(v)| <= (1/100) p q |v|^5 with the
# constant MEASURED (0.0093 over the actual range) and only the v->0 limit proved.  A measured
# constant is not a proof, so R1 would still be open.
#
# THE ROUTE.  K(t) = log(q + p e^t) is the cumulant generating function, and g(v) = K(iv).
# Its nearest singularity is at t = log(q/p) + i pi, at distance >= pi from 0.  So K is analytic
# in |t| < pi for EVERY p, and Cauchy's estimate on |t| = rho gives
#
#       |kappa_j| <= j! M_rho / rho^j ,      M_rho = max_{|t|=rho} |K(t)| ,
#
# whence, for |v| <= rho/2,
#
#       |g(v) - P4(v)| = |sum_{j>=5} kappa_j (iv)^j / j!| <= M_rho sum_{j>=5} (|v|/rho)^j
#                     <= 2 M_rho (|v|/rho)^5 .
#
# With rho = 2 and p <= 1/2 (which is our case exactly, since s > 0 forces p_a < 1/2):
#   upper:  |q + p e^t| <= q + p e^2 <= e^2, so log|.| <= 2
#   lower:  on |t| = 2, write t = x+iy with x^2+y^2 = 4, so cos y >= cos 2 = -0.41615, and
#           |q+pe^t|^2 = q^2 + 2 q p e^x cos y + p^2 e^{2x} >= q^2 + 2 q u cos2 + u^2  (u = p e^x)
#                     >= q^2 (1 - cos^2 2) = q^2 sin^2 2      [minimising the quadratic in u]
#           so |q+pe^t| >= q |sin 2| = 0.90930 q >= 0.45465 for q >= 1/2.
#   hence |K(t)| <= |log|q+pe^t|| + pi <= max(2, |log 0.45465|) + pi = 2 + pi < 5.1416.
#
#   ==>  |g(v) - P4(v)| <= 2 * 5.1416 * (|v|/2)^5 = 0.32135 |v|^5   for |v| <= 1, p <= 1/2.
#
# Every step is elementary.  CHECK ALL FOUR NUMERICALLY, including the two inequalities that
# were derived by hand, because a hand-derived inequality is a claim (F43).
import math, cmath
from mpmath import mp, mpf, mpc, log as mlog, exp as mexp
mp.dps = 40

print('(1) the singularity is at distance >= pi:  q + p e^t = 0 needs Im t = pi mod 2pi')
worst = None
for ip in range(1, 500):
    p = ip/1000.0                        # p <= 1/2
    q = 1-p
    d = abs(complex(math.log(q/p), math.pi))
    if worst is None or d < worst[0]: worst = (d, p)
print('    min over p in (0,1/2] of |log(q/p) + i pi| = %.6f   at p = %.3f   (pi = %.6f)'
      % (worst[0], worst[1], math.pi))
print('    %s' % ('OK: never closer than pi' if worst[0] >= math.pi - 1e-12 else '*** CLOSER THAN PI ***'))
print()

print('(2) lower bound on |q + p e^t| for |t| = 2 and p <= 1/2:  claim  >= q |sin 2| = 0.90930 q')
bad = 0; tight = 10.0
for ip in range(1, 501):
    p = ip/1000.0; q = 1-p
    for iph in range(0, 720):
        ph = 2*math.pi*iph/720
        t = complex(2*math.cos(ph), 2*math.sin(ph))
        val = abs(q + p*cmath.exp(t))
        claim = q*abs(math.sin(2))
        if val < claim - 1e-12: bad += 1
        tight = min(tight, val/claim)
print('    violations: %d      tightest ratio val/claim = %.6f' % (bad, tight))
print()

print('(3) M_2 = max_{|t|=2} |K(t)| for p <= 1/2:  claim  <= 2 + pi = %.5f' % (2+math.pi))
M = 0.0; wp = 0.0
for ip in range(1, 501):
    p = ip/1000.0; q = 1-p
    for iph in range(0, 720):
        ph = 2*math.pi*iph/720
        t = complex(2*math.cos(ph), 2*math.sin(ph))
        v = abs(cmath.log(q + p*cmath.exp(t)))
        if v > M: M, wp = v, p
print('    measured max = %.6f   at p = %.3f    claim %.5f    %s'
      % (M, wp, 2+math.pi, 'OK' if M <= 2+math.pi else '*** EXCEEDS CLAIM ***'))
print()

print('(4) the conclusion:  |g(v) - P4(v)| <= 0.32135 |v|^5  for |v| <= 1, p <= 1/2')
def ratio(p, v):
    P = mpf(p); Q = 1-P; V = mpf(v)
    k1=P; k2=P*Q; k3=P*Q*(1-2*P); k4=P*Q*(1-6*P+6*P*P)
    g = mlog(1 - P + P*mexp(mpc(0,1)*V))
    P4 = mpc(0,1)*k1*V - k2*V*V/2 - mpc(0,1)*k3*V**3/6 + k4*V**4/24
    return float(abs(g - P4) / V**5)
C = 2*(2+math.pi)/32
worst2 = 0.0; wpv = None
for ip in range(1, 501, 3):
    p = ip/1000.0
    for iv in range(1, 101):
        v = iv/100.0
        r = ratio(p, v)
        if r > worst2: worst2, wpv = r, (p, v)
print('    proved constant           = %.5f' % C)
print('    measured max of the ratio = %.5f   at p = %.3f, v = %.2f' % (worst2, wpv[0], wpv[1]))
print('    slack (proved / measured) = %.2f    %s'
      % (C/worst2, 'OK: the proof covers the truth' if C >= worst2 else '*** PROOF TOO WEAK ***'))
print()
print('    for reference, the measured form with the pq factor extracted:')
worst3 = 0.0
for ip in range(1, 501, 3):
    p = ip/1000.0; q = 1-p
    for iv in range(1, 101):
        v = iv/100.0
        worst3 = max(worst3, ratio(p, v)/(p*q))
print('      max |g-P4|/(pq|v|^5) = %.5f   (S2b measured 0.0093 over the applied range)' % worst3)
