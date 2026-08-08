# ripplediag_r60.py (2026-08-09, opus-5 60周目) : ripple100 で k≳52 から誤差が単調増した件の切り分け。
# 仮説A: K₂ 公式に高次項が欠けている(理論の不備)
# 仮説B: 参照 Main が Gauss のみで、Edgeworth 補正(1−S₄/4S₂²)などの滑らかな背景が
#        mod-6 の DFT ビンに漏れ込んでいる(測定の系統誤差)
# 判別: 参照に Edgeworth 補正を入れて再測定。消えれば B、残れば A。
import math, cmath, sys
def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
ALLP=[p for p in primes_upto(20000) if p%2==1]
SQ=math.sqrt(3)/2
def rep_counts(B):
    tot=sum(B); r=[0]*(tot+1); r[0]=1
    for a in B:
        for m in range(tot,a-1,-1):
            if r[m-a]: r[m]+=r[m-a]
    return r
def arith(B):
    tau=lambda a: 1 if a%6==1 else (-1 if a%6==5 else 0)
    return (sum(tau(a)*a for a in B), sum(tau(a)*a**3 for a in B), sum(B),
            sum(a*a for a in B), sum(a**4 for a in B),
            sum(1 for a in B if a%6==1), sum(1 for a in B if a%6==5))
def expoK2(B):
    D,D3,S1,S2,S4,c1,c5 = arith(B)
    return (D*D/(8.0*S2) - (3.0/8.0)*S4/S2**2 + D*D3/(4.0*S2**2)
            + (5.0/24.0)*D3*D3/S2**3 - 3.0*S4*D*D/(16.0*S2**3))
def dft(B,r,hw,edge):
    """edge=False: 参照は素の Gauss / edge=True: Edgeworth 補正 (1 − S₄/4S₂²·H) を入れる"""
    b=len(B); S=sum(B); S2=sum(a*a for a in B); S4=sum(a**4 for a in B); V0=S2/4.0
    center=S//2; N=(2*hw//6)*6; acc=0j; used=0
    for t in range(N):
        m=center-N//2+t
        if m<0 or m>=len(r) or r[m]==0: continue
        d=m-S/2.0; z=d/math.sqrt(V0)
        lg=b*math.log(2)-0.5*math.log(2*math.pi*V0)-z*z/2
        ref=math.exp(lg)
        if edge:
            # 4次 Edgeworth: (1 + (S4/(4 S2^2))·(z⁴−6z²+3)/... ) の主要形
            ref*= (1.0 + (S4/(4.0*S2*S2))*( (z**4-6*z*z+3)/8.0 ))
        acc+=(r[m]/ref-1.0)*cmath.exp(-2j*math.pi*m/6); used+=1
    C=(2.0/used)*acc
    return abs(C)
KS=[40,52,64,76,88,100]
print("="*104)
print("[切り分け] 参照に Edgeworth 補正を入れると k≳52 の誤差の増大は消えるか")
print("="*104)
print("   k    b   背景 S₄/S₂²  リップル 4(√3/2)^b   背景/信号   実測/K₂(素Gauss)  実測/K₂(Edgeworth)")
for k in KS:
    B=[a for a in ALLP[:k] if a>4]; b=len(B); r=rep_counts(B)
    D,D3,S1,S2,S4,c1,c5=arith(B)
    bg=S4/S2**2; sig=4*SQ**b
    v0=(dft(B,r,24,False)/(2*SQ**(b+1)))/math.exp(expoK2(B))
    v1=(dft(B,r,24,True )/(2*SQ**(b+1)))/math.exp(expoK2(B))
    print(f" {k:4d} {b:4d}   {bg:.6f}      {sig:.3e}      {bg/sig:9.1f}      {v0:8.4f}"
          f"          {v1:8.4f}")
    sys.stdout.flush()
print()
print("  ⇒ 背景/信号の比が k とともに急増している場合、素の Gauss 参照では漏れ込みが避けられない。")
print("     Edgeworth 補正で改善するなら【仮説B(測定の系統誤差)】、改善しないなら【仮説A(理論の欠落)】。")
