# c103_check_r12.py (2026-08-08, opus-5 7周目)
# 設計文書 paper2_transfer_r11.md §3 の持ち越し 1: Conjecture 10.3 の閉形式 Dev_d と
# 実測 (lm/deg − W_D) の照合。
#
# 予言:  lm/deg − W_D  ≈  Dev = Σ_d Dev_d,
#   Dev_d = 2^{−N_d} Re[ A_d e^{−i φ_d} ( e^{iπ(n+d)/3} + e^{iπ(n−d−σ_d)/3}
#                                          − 2 e^{iπn/3} P_d / 2^{N_d} ) ]
#   A_d = 2 (|F_{B_d}(ζ₆)|/2^{b_d}) √(V₀/V₆),  φ_d = arg F_{B_d}(ζ₆),
#   P_d = Π_{a∈I_d} (1 + e^{−iπa/3})     … 小要素部の部分集合平均の閉形式
# d=1 は 3∈B₁ ゆえ F(ζ₆)=0 → A₁=0(mod-6 リップル消滅)。
import math, cmath
from fractions import Fraction

def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]

ALLP=[p for p in primes_upto(2000) if p%2==1]
Z6=cmath.exp(2j*math.pi/6)

def rep_counts(B):
    tot=sum(B); r=[0]*(tot+1); r[0]=1
    for a in B:
        for m in range(tot,a-1,-1): r[m]+=r[m-a]
    return r
def rget(r,m): return r[m] if 0<=m<len(r) else 0

def analyze(A):
    A=sorted(A); k=len(A); T=sum(A); n=T//2
    deg=rep_counts(A)[n]
    if deg==0: return None
    D=(A[-1]-1)//2
    lm=deg; dev=0.0
    for d in range(1,D+1):
        Id=[a for a in A if a<=2*d]; Bd=[a for a in A if a>2*d]
        sig=sum(Id); Nd=len(Id); bd=len(Bd)
        rB=rep_counts(Bd)
        lm += rget(rB,n+d)+rget(rB,n-d-sig)
        # --- 予言側 ---
        F=1+0j
        for a in Bd: F*=(1+Z6**a)
        rel=abs(F)/2.0**bd
        if rel>1e-14:
            V0=sum(a*a for a in Bd)/4.0
            V6=sum(a*a/ (math.cos(math.pi*a/6)**2) for a in Bd)/4.0
            Ad=2.0*rel*math.sqrt(V0/V6)
            ph=cmath.phase(F)
            P=1+0j
            for a in Id: P*=(1+cmath.exp(-1j*math.pi*a/3))
            z=(cmath.exp(1j*math.pi*(n+d)/3)+cmath.exp(1j*math.pi*(n-d-sig)/3)
               -2*cmath.exp(1j*math.pi*n/3)*P/2.0**Nd)
            dev += 2.0**(-Nd)*(Ad*cmath.exp(-1j*ph)*z).real
    G=sum(Fraction(a,2**(j+1)) for j,a in enumerate(A))
    W=float(G+Fraction(A[-1],2**k))
    return dict(k=k,deg=deg,lm=lm,lmdeg=lm/deg,W=W,Q=(lm/deg)/W,dev=dev)

print("="*82)
print("[1] Conjecture 10.3: 閉形式 Dev と実測 (lm/deg − W_D) の照合(奇素数列)")
print("="*82)
print("  k   lm/deg      W_D      実測 lm/deg−W_D   予言 Dev      比      符号一致  T mod 6")
ok=0; tot=0
for k in range(8,27,2):
    A=ALLP[:k]
    r=analyze(A)
    if r is None: continue
    obs=r["lmdeg"]-r["W"]
    pred=r["dev"]
    same = (obs>0)==(pred>0)
    ok+= 1 if same else 0; tot+=1
    ratio = pred/obs if abs(obs)>1e-12 else float('nan')
    print(f" {k:3d} {r['lmdeg']:9.5f} {r['W']:9.5f}   {obs:+11.6f}   {pred:+11.6f}  {ratio:7.3f}"
          f"     {'YES' if same else 'no ':>3}      {sum(A)%6}")
print(f"\n  符号一致: {ok}/{tot}")

print()
print("="*82)
print("[1b] 層ごとの内訳(k=24)- どの d が Dev を支配しているか")
print("="*82)
A=ALLP[:24]; A=sorted(A); T=sum(A); n=T//2; D=(A[-1]-1)//2
print("  d   N_d   b_d   |F|/2^b       A_d        Dev_d          累積")
cum=0.0
for d in range(1,D+1):
    Id=[a for a in A if a<=2*d]; Bd=[a for a in A if a>2*d]
    sig=sum(Id); Nd=len(Id); bd=len(Bd)
    F=1+0j
    for a in Bd: F*=(1+Z6**a)
    rel=abs(F)/2.0**bd
    dv=0.0; Ad=0.0
    if rel>1e-14:
        V0=sum(a*a for a in Bd)/4.0
        V6=sum(a*a/(math.cos(math.pi*a/6)**2) for a in Bd)/4.0
        Ad=2.0*rel*math.sqrt(V0/V6); ph=cmath.phase(F)
        P=1+0j
        for a in Id: P*=(1+cmath.exp(-1j*math.pi*a/3))
        z=(cmath.exp(1j*math.pi*(n+d)/3)+cmath.exp(1j*math.pi*(n-d-sig)/3)
           -2*cmath.exp(1j*math.pi*n/3)*P/2.0**Nd)
        dv=2.0**(-Nd)*(Ad*cmath.exp(-1j*ph)*z).real
    cum+=dv
    if d<=10 or abs(dv)>1e-4:
        print(f" {d:3d}  {Nd:4d}  {bd:4d}   {rel:.3e}  {Ad:.3e}   {dv:+.6f}   {cum:+.6f}")
