import numpy as np
from mpmath import mp, mpf, sqrt, log, atan, cos, pi, zeta, gamma
mp.dps = 30
s_, k = mpf('0.5'), 4096
Cs = 2**(s_-1)*pi/(gamma(s_)*cos(pi*s_/2))
f = lambda t: k**(-s_)*(1+4*t*t)**(mpf(k)/2) - t*(1+2*zeta(s_)+Cs*t**(s_-1))
lo, hi = mpf('0.005'), mpf('0.05')
assert f(lo) < 0 and f(hi) > 0
for _ in range(80):
    m = (lo+hi)/2
    if f(m) > 0: hi = m
    else: lo = m
tpred = (lo+hi)/2
lam_pred = 2*k*tpred**2/log(k)
wnp = (np.arange(k)+1.0)**(-0.5)
def Fnp(ts):
    j = np.arange(k); rho = np.sqrt(1+4*ts*ts); th = np.arctan(2*ts)
    out = np.empty_like(ts)
    for a in range(0, len(ts), 500):
        b = min(a+500, len(ts))
        out[a:b] = 1 + 2*(wnp[None,:]*np.exp(np.log(rho[a:b])[:,None]*j[None,:])*np.cos(th[a:b][:,None]*j[None,:])).sum(axis=1)
    return out
ts = np.linspace(1e-6, 3*float(tpred), 3001)
v = Fnp(ts); idx = np.where(np.sign(v[:-1])*np.sign(v[1:])<0)[0]
def F_mp(t):
    rho, th = sqrt(1+4*t*t), atan(2*t)
    return 1 + 2*sum((mpf(1)/sqrt(mpf(j+1)))*rho**j*cos(j*th) for j in range(k))
lo, hi = mpf(float(ts[idx[0]])), mpf(float(ts[idx[0]+1]))
flo = F_mp(lo)
for _ in range(60):
    m = (lo+hi)/2
    if flo*F_mp(m) <= 0: hi = m
    else: lo, flo = m, F_mp(m)
t1 = (lo+hi)/2
lam_eff = 2*k*t1**2/log(k)
D = 4*pi*t1/log(k)
print("s=0.5 k=4096 (a point never printed by opus):")
print("  t_pred=%s t_1=%s" % (mp.nstr(tpred,8), mp.nstr(t1,8)))
print("  lam_pred=%s lam_eff=%s |resid|=%s D=%s -> %s" % (mp.nstr(lam_pred,6), mp.nstr(lam_eff,6),
      mp.nstr(abs(lam_pred-lam_eff),4), mp.nstr(D,4), "INSIDE" if abs(lam_pred-lam_eff)<=D else "OUTSIDE"))
print("  branch: |lam - s/2| = %s vs |lam - (s-1/2)| = %s" % (mp.nstr(abs(lam_eff-mpf('0.25')),4), mp.nstr(abs(lam_eff),4)))
