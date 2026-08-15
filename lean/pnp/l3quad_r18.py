# l3quad_r18.py (2026-08-08, opus-5 13周目)
# 設計文書 paper2_l3l5_r17.md §1 の照合レシピ 1〜3。
#   K   = exp[ D^2/(8 S2) - (3/8) S4/S2^2 + D*D3/(4 S2^2) + 45*D3^2/(24 S2^3) ]
#   psi(nu) = -(sqrt3/2) * nu * (D + D3/S2) / S2      … 窓中心をずらすと位相が線形ドリフト
#   D  = sum tau_a a,  D3 = sum tau_a a^3,  tau_a = +1 (a=1 mod 6) / -1 (a=5 mod 6)
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
    D  = sum(tau(a)*a for a in B)
    D3 = sum(tau(a)*a**3 for a in B)
    S2 = sum(a*a for a in B)
    S4 = sum(a**4 for a in B)
    c1 = sum(1 for a in B if a%6==1); c5 = sum(1 for a in B if a%6==5)
    return D,D3,S2,S4,c1,c5

def Kpred(B):
    D,D3,S2,S4,_,_ = arith(B)
    e = D*D/(8.0*S2) - (3.0/8.0)*S4/S2**2 + D*D3/(4.0*S2**2) + 45.0*D3*D3/(24.0*S2**3)
    return math.exp(e), e

def dft(B, center, hw=24, q=6):
    """窓中心 center での周期 q 成分。(振幅, 位相) を返す。"""
    b=len(B); S=sum(B); V0=sum(a*a for a in B)/4.0
    r=rep_counts(B)
    N=(2*hw//q)*q
    acc=0j; used=0
    for t in range(N):
        m=center-N//2+t
        if m<0 or m>=len(r) or r[m]==0: continue
        d=m-S/2.0
        lg=b*math.log(2)-0.5*math.log(2*math.pi*V0)-d*d/(2*V0)
        acc+=(r[m]/math.exp(lg)-1.0)*cmath.exp(-2j*math.pi*m/q); used+=1
    C=(2.0/used)*acc
    return abs(C), -cmath.phase(C)

print("="*104)
print("[1] K の照合: 実測振幅比 vs 予言 K (両枝が1本の式で再現されるか)")
print("="*104)
print("  k   b  c1-c5   Delta   Delta3/S2   S2        指数e      K予言    実測比    実測/K")
rows=[]
for k in range(18,41,2):
    B=[a for a in ALLP[:k] if a>4]; b=len(B)
    D,D3,S2,S4,c1,c5 = arith(B)
    K,e = Kpred(B)
    amp,ph = dft(B, sum(B)//2)
    meas = amp/(2*SQ**(b+1))
    rows.append((k,b,c1-c5,D,D3,S2,S4,K,meas,ph))
    print(f" {k:3d} {b:3d}  {c1-c5:+4d}  {D:+7d}  {D3/S2:+9.2f} {S2:9d}  {e:+9.5f}  {K:7.4f}  {meas:7.4f}  {meas/K:7.4f}")

print()
print("  判定: 『実測/K』が 1 に揃えば、2次補正 K が両枝を1本の式で説明できたことになる。")
print("        揃わなければ K の式は却下(あるいは高次が効いている)。")
ok=[abs(r[8]/r[7]-1) for r in rows]
print(f"        |実測/K − 1| の 最大 {max(ok):.4f} / 平均 {sum(ok)/len(ok):.4f}")
print(f"  参考:  K を使わない場合の |実測 − 1| の 最大 {max(abs(r[8]-1) for r in rows):.4f}")

print()
print("="*104)
print("[3] Delta(mod-6 符号付き素数和 = 重み付き素数レース)の k 依存")
print("="*104)
print("  k    Delta      Delta/S2      c1-c5   符号")
for k,b,cc,D,D3,S2,S4,K,meas,ph in rows:
    print(f" {k:3d}  {D:+8d}  {D/S2:+11.3e}   {cc:+4d}    {'負' if D<0 else '正'}")

print()
print("="*104)
print("[2] psi(nu) 位相ドリフト — 独立な第2の予言")
print("    予言: 窓中心を s だけずらすと位相が勾配 g = (sqrt3/2)(D + D3/S2)/S2 で線形にドリフト")
print("="*104)
print("  k   b     g予言        実測勾配      比      R^2      位相@中心")
SH=[-40,-30,-20,-10,0,10,20,30,40]
for k in range(20,41,2):
    B=[a for a in ALLP[:k] if a>4]; b=len(B)
    D,D3,S2,S4,c1,c5 = arith(B)
    g = SQ*(D + D3/S2)/S2
    c0=sum(B)//2
    xs=[];ys=[]
    for s in SH:
        # 窓中心を s ずらす。周期6を保つため s は 6 の倍数に丸める
        s6 = (s//6)*6
        a_,p_ = dft(B, c0+s6)
        xs.append(s6); ys.append(p_)
    # 位相のアンラップ
    for i in range(1,len(ys)):
        while ys[i]-ys[i-1] >  math.pi: ys[i]-=2*math.pi
        while ys[i]-ys[i-1] < -math.pi: ys[i]+=2*math.pi
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    den=sum((x-mx)**2 for x in xs)
    sl=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/den
    pred=[my+sl*(x-mx) for x in xs]
    ssr=sum((y-p)**2 for y,p in zip(ys,pred)); sst=sum((y-my)**2 for y in ys)
    r2=1-ssr/sst if sst>0 else float('nan')
    ratio = sl/g if abs(g)>1e-12 else float('nan')
    print(f" {k:3d} {b:3d}  {g:+.4e}  {sl:+.4e}  {ratio:7.3f}  {r2:7.4f}  {ys[4]:+8.4f}")
print()
print("  判定: 『比』が +1 か −1 の一方に揃えば予言成立(符号は規約の取り方)。")
print("        R^2 が 1 に近いことが線形性の確認。")
