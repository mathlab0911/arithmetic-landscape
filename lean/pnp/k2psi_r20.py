# k2psi_r20.py (2026-08-08, opus-5 15周目)
# fable-5 指示書 opus5_報告兼指示書_r19.md の処方 K2-1 と psi-1 を実行する。
#   K2 = K * exp(-3 S4 Delta^2 / (16 S2^3)),  かつ Delta3^2 の係数を 45/24 -> 5/24 に訂正
#   psi-1: g(k) = alpha*Delta/S2 + beta*(c1-c5)/S2 + gamma/S2 の3パラメータ最小二乗
#          + 感度試験3点 (a)勾配xS2 が定数か (b)中心を±1/2ずらす (c)窓幅を振る
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
    D  = sum(tau(a)*a for a in B); D3 = sum(tau(a)*a**3 for a in B)
    S1 = sum(B); S2 = sum(a*a for a in B); S4 = sum(a**4 for a in B)
    c1 = sum(1 for a in B if a%6==1); c5 = sum(1 for a in B if a%6==5)
    return D,D3,S1,S2,S4,c1,c5

def expo(B, variant):
    """variant: 'r17'(元) / 'c5'(Delta3^2 を 5/24 に訂正) / 'K2'(訂正 + S4*Delta^2 項)"""
    D,D3,S1,S2,S4,c1,c5 = arith(B)
    c = 45.0/24.0 if variant=='r17' else 5.0/24.0
    e = D*D/(8.0*S2) - (3.0/8.0)*S4/S2**2 + D*D3/(4.0*S2**2) + c*D3*D3/S2**3
    if variant=='K2':
        e += -3.0*S4*D*D/(16.0*S2**3)
    return e

def dft(B, r, center, hw=24, q=6, half=0.0):
    b=len(B); S=sum(B); V0=sum(a*a for a in B)/4.0
    N=(2*hw//q)*q; acc=0j; used=0
    for t in range(N):
        m=center-N//2+t
        if m<0 or m>=len(r) or r[m]==0: continue
        d=m-(S/2.0+half)                      # 参照 Main の中心をずらす試験用
        lg=b*math.log(2)-0.5*math.log(2*math.pi*V0)-d*d/(2*V0)
        acc+=(r[m]/math.exp(lg)-1.0)*cmath.exp(-2j*math.pi*m/q); used+=1
    C=(2.0/used)*acc
    return abs(C), -cmath.phase(C)

KS=list(range(18,41,2))
DATA={}
for k in KS:
    B=[a for a in ALLP[:k] if a>4]
    DATA[k]=(B, rep_counts(B)) + arith(B)

print("="*118)
print("[K2-1] K2 = K * exp(-3 S4 Delta^2 / (16 S2^3))、Delta3^2 の係数を 45/24 -> 5/24 に訂正")
print("="*118)
print("  k   b  c1-c5   Delta   実測比    実測/K(r17)  実測/K(5/24)  実測/K2   枝")
rows=[]
for k in KS:
    B,r,D,D3,S1,S2,S4,c1,c5 = DATA[k]; b=len(B)
    amp,ph = dft(B,r,sum(B)//2)
    meas = amp/(2*SQ**(b+1))
    v = {t: meas/math.exp(expo(B,t)) for t in ('r17','c5','K2')}
    br = 'B' if (c1-c5)<=-3 else 'A'
    rows.append((k,b,c1-c5,D,meas,v,br))
    print(f" {k:3d} {b:3d}  {c1-c5:+4d}  {D:+7d}  {meas:7.4f}    {v['r17']:8.4f}     {v['c5']:8.4f}   {v['K2']:8.4f}   {br}")

print()
for t,lab in (('r17','K(r17 元の式)'),('c5','K(Delta3^2=5/24 に訂正)'),('K2','K2(S4*Delta^2 項を追加)')):
    A=[abs(x[5][t]-1) for x in rows if x[6]=='A']
    Bb=[abs(x[5][t]-1) for x in rows if x[6]=='B']
    print(f"  {lab:28s} A枝 |比-1| 平均 {sum(A)/len(A):.5f} 最大 {max(A):.5f}"
          f"  |  B枝 平均 {sum(Bb)/len(Bb):.5f} 最大 {max(Bb):.5f}")
print()
print("  合格基準(fable-5): B枝(k=32,34,40)の 0.990〜0.995 が 0.997〜1.003 に入り、A枝が悪化しないこと")
print("  B枝の実測/K2:", ", ".join(f"k={x[0]}:{x[5]['K2']:.4f}" for x in rows if x[6]=='B'))

# ---------------- psi-1 ----------------
SH=[-40,-30,-20,-10,0,10,20,30,40]
def slope(B,r,hw,half=0.0):
    c0=sum(B)//2; xs=[];ys=[]
    for s in SH:
        s6=(s//6)*6
        xs.append(s6); ys.append(dft(B,r,c0+s6,hw,half=half)[1])
    for i in range(1,len(ys)):
        while ys[i]-ys[i-1] >  math.pi: ys[i]-=2*math.pi
        while ys[i]-ys[i-1] < -math.pi: ys[i]+=2*math.pi
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    return sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)

def lstsq(X,Y):
    n=len(X[0])
    A=[[sum(X[i][a]*X[i][b] for i in range(len(X))) for b in range(n)] for a in range(n)]
    v=[sum(X[i][a]*Y[i] for i in range(len(X))) for a in range(n)]
    M=[A[i][:]+[v[i]] for i in range(n)]
    for i in range(n):
        p=max(range(i,n),key=lambda t:abs(M[t][i])); M[i],M[p]=M[p],M[i]
        for j in range(i+1,n):
            f=M[j][i]/M[i][i]
            for t in range(i,n+1): M[j][t]-=f*M[i][t]
    c=[0.0]*n
    for i in range(n-1,-1,-1):
        c[i]=(M[i][n]-sum(M[i][t]*c[t] for t in range(i+1,n)))/M[i][i]
    fit=[sum(c[a]*X[i][a] for a in range(n)) for i in range(len(X))]
    ssr=sum((Y[i]-fit[i])**2 for i in range(len(Y))); my=sum(Y)/len(Y)
    sst=sum((y-my)**2 for y in Y)
    # 各係数の標準誤差(残差分散 x (X^T X)^{-1} の対角)
    dof=max(len(Y)-n,1); s2=ssr/dof
    inv=[[1.0 if i==j else 0.0 for j in range(n)] for i in range(n)]
    M=[A[i][:]+inv[i] for i in range(n)]
    for i in range(n):
        p=max(range(i,n),key=lambda t:abs(M[t][i])); M[i],M[p]=M[p],M[i]
        d=M[i][i]
        for t in range(2*n): M[i][t]/=d
        for j in range(n):
            if j!=i:
                f=M[j][i]
                for t in range(2*n): M[j][t]-=f*M[i][t]
    se=[math.sqrt(s2*M[i][n+i]) for i in range(n)]
    return c,se,(1-ssr/sst)

print()
print("="*118)
print("[psi-1] g(k) = alpha*Delta/S2 + beta*(c1-c5)/S2 + gamma/S2  の3パラメータ最小二乗")
print("="*118)
NAMES=["alpha (Delta/S2)","beta  ((c1-c5)/S2)","gamma (1/S2)"]
for hw in (24,48,96,192):
    X=[];Y=[]
    for k in KS:
        B,r,D,D3,S1,S2,S4,c1,c5=DATA[k]
        X.append([D/S2,(c1-c5)/S2,1.0/S2]); Y.append(slope(B,r,hw))
    c,se,r2=lstsq(X,Y)
    print(f"  hw={hw:<4d} R^2={r2:.5f}")
    for i in range(3):
        t = c[i]/se[i] if se[i]>0 else float('nan')
        print(f"        {NAMES[i]:22s} = {c[i]:+12.4e}  ± {se[i]:.2e}   (t = {t:+7.2f}) "
              f"{'有意' if abs(t)>2 else '有意でない'}")
print()
print("  参考: fable-5 の予言は alpha = -(sqrt3/2) = {:+.4f}(Delta3 項を除いた主要部)".format(-SQ))
print("        beta が有意で安定 -> 実物理(H-psi2)。gamma のみ有意 -> アーティファクト(H-psi1)。")

print()
print("="*118)
print("[感度(a)] 勾配 x S2 は k によらず定数か?(定数なら 1/S2 スケール = H-psi1 と整合)")
print("="*118)
print("  k   Delta   c1-c5   sl*S2 (hw=24)   sl*S2 (hw=96)   sl*S2 (hw=192)")
for k in KS:
    B,r,D,D3,S1,S2,S4,c1,c5=DATA[k]
    print(f" {k:3d} {D:+7d}   {c1-c5:+4d}    {slope(B,r,24)*S2:+11.4f}    "
          f"{slope(B,r,96)*S2:+11.4f}    {slope(B,r,192)*S2:+11.4f}")

print()
print("="*118)
print("[感度(b)] 参照 Main の中心を ±1/2 ずらすと勾配は動くか?(動けば抽出系の性質)")
print("="*118)
print("  k    sl(half=-0.5)    sl(half=0)    sl(half=+0.5)   振れ幅/|sl(0)|")
for k in KS:
    B,r,D,D3,S1,S2,S4,c1,c5=DATA[k]
    a=slope(B,r,96,-0.5); b0=slope(B,r,96,0.0); c_=slope(B,r,96,+0.5)
    rel = (max(a,b0,c_)-min(a,b0,c_))/abs(b0) if b0 else float('nan')
    print(f" {k:3d}   {a:+.4e}   {b0:+.4e}   {c_:+.4e}     {rel:7.3f}")

print()
print("="*118)
print("[Delta 数表] c1-c5, Delta, Delta3 の k 依存(素数レースの記録)")
print("="*118)
print("  k   b   c1   c5  c1-c5     Delta       Delta3/S2        S2          S4/S2^2")
for k in range(8,45,2):
    B=[a for a in ALLP[:k] if a>4]; b=len(B)
    if b==0: continue
    D,D3,S1,S2,S4,c1,c5=arith(B)
    print(f" {k:3d} {b:3d}  {c1:3d}  {c5:3d}   {c1-c5:+4d}  {D:+8d}   {D3/S2:+11.2f}  {S2:10d}   {S4/S2**2:9.5f}")
