#!/usr/bin/env python3
"""leeyang8b_r194 -- adjudication (fast form).  Falsifiers X-1..X-4 as in leeyang8_r194 header.
Scanning uses the closed form; X-4 validates the closed form against a literal transcription
of paper4's own displayed formula (line 1312) at spot points first."""
import mpmath as mp
mp.mp.dps = 30

def paper_gamma(k, q):                      # literal paper4 line 1312 (F23: independent route)
    s = mp.mpf(0)
    for j in range(1, k):
        s += (2*q)**j + (2*(1-q))**j
    return 3 + s/2

def f_lit(k, t): return mp.re(paper_gamma(k, mp.mpc(mp.mpf("0.5"), t)))
def f(k, t):                                # closed form: 2 + rho^k sin(k theta)/(2t)
    rho = mp.sqrt(1+4*t**2)
    return 2 + rho**k * mp.sin(k*mp.atan(2*t))/(2*t)

print("="*86)
print("leeyang8b_r194 -- paper4 rem:leeyanglacunary  vs  r194 algebra   (a_i = 2^i+1)")
print("="*86)
print("\n[X-4] literal paper formula vs r194 closed form")
worst = mp.mpf(0)
for k in (16,32,64,128,256):
    for t in (mp.mpf("0.003"), mp.mpf("0.02"), mp.pi/(2*k), 3*mp.pi/(2*k), mp.mpf(6)/k):
        a=f_lit(k,t); b=f(k,t)
        worst=max(worst, abs(a-b)/max(abs(a),mp.mpf(1)))
print(f"      worst relative discrepancy over 25 points : {mp.nstr(worst,5)}")
print(f"      X-4 (>1e-25) : {'FIRED -- closed form wrong' if worst>mp.mpf('1e-25') else 'not fired (forms agree)'}")

print("\n[X-1] is the paper's claimed FIRST-rung location t = 3pi/(2k) a zero?")
for k in (128,256,512,1024):
    t=3*mp.pi/(2*k); v=f(k,t)
    print(f"   k={k:5d}  t=3pi/2k={mp.nstr(t,8):>12}  Gamma^(q)={mp.nstr(v,8):>13}"
          f"   {'~zero' if abs(v)<mp.mpf('0.5') else 'NOT a zero'}")

def roots(k, n_wanted, npts=3000):
    out=[]; tmax=mp.mpf(11)/k
    pt=tmax/npts; pv=f(k,pt)
    for i in range(2,npts+1):
        t=tmax*i/npts; v=f(k,t)
        if mp.sign(v)!=mp.sign(pv) and v!=0:
            out.append(mp.findroot(lambda s: f(k,s),(pt,t),solver="bisect",tol=mp.mpf(10)**-25))
            if len(out)>=n_wanted: break
        pt,pv=t,v
    return out

print("\n[X-2 / X-3] the actual ladder: first three on-line zeros")
print(f"   {'k':>6} {'rung':>5} {'t_n':>16} {'k*t_n':>12} {'k*theta_n/pi':>13}   note")
for k in (128,256,512,1024):
    for n,t in enumerate(roots(k,3)):
        kt=k*t; kth=k*mp.atan(2*t)/mp.pi
        note = "paper's |q_1-1/2| is this one" if n==0 else ""
        if abs(kt-3*mp.pi/2)<mp.mpf("0.12"): note = "<== paper's k*Im q_1 = 4.77 is THIS one"
        print(f"   {k:6d} {n+1:5d} {mp.nstr(t,10):>16} {mp.nstr(kt,9):>12} {mp.nstr(kth,9):>13}   {note}")
print(f"\n   reference:  pi/2 = {mp.nstr(mp.pi/2,10)}    3pi/2 = {mp.nstr(3*mp.pi/2,10)}")

print("\n[paper's own |q_1-1/2| numbers, recomputed]")
for k,rep in ((32,"0.0520"),(64,"0.0253"),(96,"0.0167")):
    r=roots(k,1)[0]
    print(f"   k={k:4d}  first zero = {mp.nstr(r,8):>12}   paper reports {rep}"
          f"   {'MATCH' if abs(r-mp.mpf(rep))<mp.mpf('0.0001') else 'differ'}")

print("\n[paper's k*Im q_1 series, recomputed AT RUNG 3]")
for k,rep in ((128,"4.7736"),(256,"4.7457"),(512,"4.7299")):
    rr=roots(k,3)
    print(f"   k={k:5d}  rung3 k*t = {mp.nstr(k*rr[2],9):>12}   paper reports {rep} as k*Im q_1"
          f"   {'MATCH' if abs(k*rr[2]-mp.mpf(rep))<mp.mpf('0.01') else 'differ'}")
print("\ndone.")
