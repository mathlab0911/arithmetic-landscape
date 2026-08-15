# psi_hw_r19.py (2026-08-08, opus-5 14周目)
# V3 の追い込み: |Delta| が小さい k で見えた「一定ドリフト」は窓幅 hw のアーティファクトか?
# hw を 24 から 384 まで倍々に振り、勾配 sl(hw) が
#   (a) hw とともに 0 に向かう  → アーティファクト
#   (b) 一定値に収束する        → 本物の欠落項
# のどちらかを判定する。|Delta| が大きい k を対照群として同時に測る。
import math, cmath

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
        for m in range(tot,a-1,-1): r[m]+=r[m-a]
    return r

def arith(B):
    tau=lambda a: 1 if a%6==1 else (-1 if a%6==5 else 0)
    return (sum(tau(a)*a for a in B), sum(tau(a)*a**3 for a in B),
            sum(B), sum(a*a for a in B))

def dft_phase(r,B,center,hw,q=6):
    b=len(B); S=sum(B); V0=sum(a*a for a in B)/4.0
    N=(2*hw//q)*q; acc=0j; used=0
    for t in range(N):
        m=center-N//2+t
        if m<0 or m>=len(r) or r[m]==0: continue
        d=m-S/2.0
        lg=b*math.log(2)-0.5*math.log(2*math.pi*V0)-d*d/(2*V0)
        acc+=(r[m]/math.exp(lg)-1.0)*cmath.exp(-2j*math.pi*m/q); used+=1
    return -cmath.phase((2.0/used)*acc)

SH=[-40,-30,-20,-10,0,10,20,30,40]
def slope(r,B,hw):
    c0=sum(B)//2; xs=[];ys=[]
    for s in SH:
        s6=(s//6)*6
        xs.append(s6); ys.append(dft_phase(r,B,c0+s6,hw))
    for i in range(1,len(ys)):
        while ys[i]-ys[i-1] >  math.pi: ys[i]-=2*math.pi
        while ys[i]-ys[i-1] < -math.pi: ys[i]+=2*math.pi
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    den=sum((x-mx)**2 for x in xs)
    return sum((x-mx)*(y-my) for x,y in zip(xs,ys))/den

HWS=[24,48,96,192,384]
GROUPS=[("|Delta| 小(問題の3点)",[24,26,28]),
        ("|Delta| 中",[20,22,30,36,38]),
        ("|Delta| 大(対照群)",[32,34,40])]
for label,ks in GROUPS:
    print("="*104)
    print(f"[{label}]")
    print("="*104)
    print("  k   Delta   g予言(x1e-5) | " + " ".join(f"hw={h:<4d}" for h in HWS) + "   (すべて sl x1e-5)")
    for k in ks:
        B=[a for a in ALLP[:k] if a>4]
        D,D3,S1,S2=arith(B); g=SQ*(D+D3/S2)/S2
        r=rep_counts(B)
        sls=[slope(r,B,h) for h in HWS]
        print(f" {k:3d} {D:+7d}    {g*1e5:+9.3f} | " + " ".join(f"{s*1e5:+8.3f}" for s in sls))
    print()

print("="*104)
print("判定基準:")
print("  hw を倍にするたびに |sl| が単調に小さくなり 0 に向かう  → 窓のアーティファクト(欠落項ではない)")
print("  hw を倍にしても |sl| が動かない                        → 本物(fable-5 の式に欠落項がある)")
print("="*104)
