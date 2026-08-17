# fable r218 second route: written from the model statement, not from opus's code.
# F = 1 + 2 Re G_k;  Re G_k(1+2it) = sum w_j rho^j cos(j th).
# v3 model: Hp(th) + T sin(k th) = -1/2, Hp = sum w_j cos(j th), T = w_{k-1} rho^k / (2t).
from mpmath import mp, mpf, sqrt, log, atan, cos, sin, tan, pi
mp.dps = 25

def F(w, t):
    rho, th = sqrt(1+4*t*t), atan(2*t)
    return 1 + 2*sum(wj * rho**j * cos(j*th) for j, wj in enumerate(w) if wj)

def model(w, k, t):
    rho, th = sqrt(1+4*t*t), atan(2*t)
    Hp = sum(wj * cos(j*th) for j, wj in enumerate(w) if wj)
    T = w[-1] * rho**k / (2*t)
    return Hp + T*sin(k*th) + mpf(1)/2

def first_root(f, thi, N=6000):
    prev_t, prev_v = None, None
    for i in range(1, N+1):
        t = thi * i / N
        v = f(t)
        if prev_v is not None and prev_v * v < 0:
            lo, hi = prev_t, t
            for _ in range(90):
                m = (lo+hi)/2
                if f(lo)*f(m) <= 0: hi = m
                else: lo = m
            return (lo+hi)/2
        prev_t, prev_v = t, v
    return None

print("s     k      t1            v3/t1        opus_v3/t1")
opus = {('1',256):'0.999777', ('2',512):'0.999825', ('4',1024):'0.999931'}
for s, k in [(1,256),(2,512),(4,1024)]:
    w = [mpf(1)/mpf(j+1)**s for j in range(k)]
    pred = sqrt(mpf(s)*log(k)/(2*k))
    t1 = first_root(lambda t: F(w,t), 3*pred)
    tv = first_root(lambda t: model(w,k,t), 3*pred)
    print(s, k, mp.nstr(t1,9), mp.nstr(tv/t1,6), " (opus:", opus[(str(s),k)]+")")

# N3: constant weights w0=0, w=1/2 -- Thm2(e): first zero exactly tan(pi/k)/2
print()
print("N3 constant weights k=256:")
k = 256
w = [mpf(0)] + [mpf(1)/2]*(k-1)
ref = tan(pi/k)/2
tv = first_root(lambda t: model(w,k,t), 4*ref)
print("  ref =", mp.nstr(ref,12), " v3 =", mp.nstr(tv,12), " rel =", mp.nstr(abs(tv-ref)/ref,5), "(opus: 0.0019382)")
