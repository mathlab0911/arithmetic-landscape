# w5smoke_r38.py (2026-08-08, opus-5 39周目) : fable-5 r37 作業3。
# W5 の領域分割ごとの寄与を数値積分し、表の上界内に収まるかを見る。
#   r_B(m) = (1/2pi) int F_B(theta) e^{-i m theta} dtheta なので、
#   各領域の寄与の大きさは (1/2pi) int_region |F_B| dtheta = (2^b/2pi) int |G| で上から押さえられる。
#   これを Main = 2^b/sqrt(2 pi V0) で割った相対値を見る。
import math
def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
P=[p for p in primes_upto(400) if p%2==1]

def run(k, d=2):
    A=P[:k]; B=[a for a in A if a>2*d]; b=len(B)
    S2=sum(a*a for a in B); V0=S2/4.0; sig=1.0/math.sqrt(V0)
    def G(th):
        v=0.0
        for a in B:
            c=abs(math.cos(a*th/2.0))
            if c<1e-300: return 0.0
            v+=math.log(c)
        return math.exp(v)
    # 領域: R0 = |theta| <= 8 sigma ; R6, R4 = 2pi/6, 2pi/4 の +-8 sigma ; RT2 = q=8,10,..,18 の +-8sigma ; R3 = 残り
    hw=8*sig
    centers={'R6':2*math.pi/6,'R4':2*math.pi/4}
    T2c={q:2*math.pi/q for q in (8,10,12,14,16,18,20)}
    N=200000
    tot={'R0':0.0,'R6':0.0,'R4':0.0,'RT2':0.0,'R3':0.0}
    dth=math.pi/N
    for i in range(N+1):
        th=math.pi*i/N
        g=G(th)
        if th<=hw: key='R0'
        elif any(abs(th-c)<=hw for c in centers.values()):
            key='R6' if abs(th-centers['R6'])<=hw else 'R4'
        elif any(abs(th-c)<=hw for c in T2c.values()): key='RT2'
        else: key='R3'
        tot[key]+=g*dth
    Main_rel = math.sqrt(2*math.pi*V0)          # (2^b/2pi)*X ÷ (2^b/sqrt(2piV0)) = X*sqrt(2piV0)/(2pi)
    out={kk: v*Main_rel/(2*math.pi) for kk,v in tot.items()}
    return b,S2,out

print("="*106)
print("[W5 スモーク] 各領域の ∫|G| dθ を Main で正規化した相対寄与(d=2、包絡半幅 8σ)")
print("="*106)
print("   k    b      R0        R6         R4         R_T2        R3      | 目安: (√3/2)^b  (1/2)^b")
for k in (24,32):
    b,S2,o=run(k)
    print(f" {k:3d} {b:4d}  {o['R0']:.4f}  {o['R6']:.3e}  {o['R4']:.3e}  {o['RT2']:.3e}  {o['R3']:.3e} |"
          f"  {(math.sqrt(3)/2)**b:.2e}  {0.5**b:.2e}")
print()
print("  判定基準(W5 の表):")
print("   ・R0 は 1 のオーダー(主要項)")
print("   ・R6 が副次項の主役。(√3/2)^b のオーダーであること")
print("   ・R4 / R_T2 / R3 はいずれも R6 より小さく、合計しても R6 を超えないこと")
