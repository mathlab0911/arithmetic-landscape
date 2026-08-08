# psi_r19.py (2026-08-08, opus-5 14周目)
# 目的: fable-5 の psi(nu) 予言に欠けている「Delta 非依存項」を同定する。
#   予言:  g_pred = (sqrt3/2) * (D + D3/S2) / S2
#   実測:  窓中心をずらしたときの位相の勾配 sl
#   13周目の所見: |D| が小さい k=24,26,28 で D の符号に依らず sl ~ -1.8e-5 で一定。
#
# 検証プロトコル:
#   V3 … 自由パラメータ(窓半幅 hw)を振って、結論が hw の産物でないか確認する。★今回の主眼
#   V2c … 比だけでなく生の勾配値を印字する。
#   V1 … 出力は psi_r19.log に保存する。
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
    S1 = sum(B); S2 = sum(a*a for a in B); S4 = sum(a**4 for a in B)
    c1 = sum(1 for a in B if a%6==1); c5 = sum(1 for a in B if a%6==5)
    return D,D3,S1,S2,S4,c1,c5

def dft_phase(r, B, center, hw, q=6):
    b=len(B); S=sum(B); V0=sum(a*a for a in B)/4.0
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

SH=[-40,-30,-20,-10,0,10,20,30,40]
def slope(r, B, hw):
    c0=sum(B)//2
    xs=[];ys=[]
    for s in SH:
        s6=(s//6)*6
        a_,p_=dft_phase(r,B,c0+s6,hw)
        xs.append(s6); ys.append(p_)
    for i in range(1,len(ys)):
        while ys[i]-ys[i-1] >  math.pi: ys[i]-=2*math.pi
        while ys[i]-ys[i-1] < -math.pi: ys[i]+=2*math.pi
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    den=sum((x-mx)**2 for x in xs)
    sl=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/den
    pred=[my+sl*(x-mx) for x in xs]
    ssr=sum((y-p)**2 for y,p in zip(ys,pred)); sst=sum((y-my)**2 for y in ys)
    return sl, (1-ssr/sst if sst>0 else float('nan'))

KS=list(range(20,41,2))
HWS=[24,48,96]
DAT={}
print("="*112)
print("[V3] 窓半幅 hw を振る —— 実測勾配 sl は hw に依存するか?")
print("     13周目は hw=24 のみで測り、|Delta| 小の k で sl ~ -1.8e-5 の一定ドリフトを見た。")
print("     もしこれが hw とともに 0 に向かうなら、ドリフトは窓のアーティファクトである。")
print("="*112)
hdr="  k   b   Delta    g予言(x1e-5)"+"".join(f"   sl@hw={h:<3d}(x1e-5)" for h in HWS)+"    R^2@96"
print(hdr)
for k in KS:
    B=[a for a in ALLP[:k] if a>4]; b=len(B)
    D,D3,S1,S2,S4,c1,c5=arith(B)
    r=rep_counts(B)
    g=SQ*(D+D3/S2)/S2
    sls=[]; r2=None
    for h in HWS:
        s_,rr=slope(r,B,h); sls.append(s_); r2=rr
    DAT[k]=dict(b=b,D=D,D3=D3,S1=S1,S2=S2,S4=S4,c1=c1,c5=c5,g=g,sl=sls)
    print(f" {k:3d} {b:3d} {D:+7d}      {g*1e5:+9.3f}"
          + "".join(f"       {s*1e5:+9.3f}" for s in sls)
          + f"   {r2:7.4f}")

print()
print("="*112)
print("[F] 欠けている項の同定 —— hw=96 の実測勾配を候補基底に最小二乗回帰")
print("="*112)
print("  候補基底(いずれも次元 1/長さ):")
print("    x1 = (sqrt3/2)(Delta + Delta3/S2)/S2      … fable-5 の予言そのもの")
print("    x2 = (c1-c5)/S1                            … 零次モーメント(素数レースの個数差)")
print("    x3 = 1/S1                                  … 定数ドリフト(窓中心の系統ずれ)")
print("    x4 = S1/S2                                 … 平均的な大きさの逆数")
def feats(d):
    return [d['g'], (d['c1']-d['c5'])/d['S1'], 1.0/d['S1'], d['S1']/d['S2']]
NAMES=["x1(fable)","x2(c1-c5)","x3(1/S1)","x4(S1/S2)"]
Y=[DAT[k]['sl'][-1] for k in KS]
X=[feats(DAT[k]) for k in KS]

def lstsq(X,Y,cols):
    n=len(cols)
    A=[[sum(X[i][a]*X[i][bb] for i in range(len(X))) for bb in cols] for a in cols]
    v=[sum(X[i][a]*Y[i] for i in range(len(X))) for a in cols]
    # ガウス消去
    M=[row[:]+[v[i]] for i,row in enumerate(A)]
    for i in range(n):
        p=max(range(i,n),key=lambda t:abs(M[t][i])); M[i],M[p]=M[p],M[i]
        if abs(M[i][i])<1e-300: return None,None
        for j in range(i+1,n):
            f=M[j][i]/M[i][i]
            for t in range(i,n+1): M[j][t]-=f*M[i][t]
    c=[0.0]*n
    for i in range(n-1,-1,-1):
        c[i]=(M[i][n]-sum(M[i][t]*c[t] for t in range(i+1,n)))/M[i][i]
    fit=[sum(c[a]*X[i][cols[a]] for a in range(n)) for i in range(len(X))]
    ssr=sum((Y[i]-fit[i])**2 for i in range(len(Y)))
    my=sum(Y)/len(Y); sst=sum((y-my)**2 for y in Y)
    return c,(1-ssr/sst)

print()
print("  モデル                                係数                              R^2")
MODELS=[([0],"x1 のみ(fable-5 の予言)"),
        ([0,1],"x1 + x2"),
        ([0,2],"x1 + x3"),
        ([0,3],"x1 + x4"),
        ([0,1,2],"x1 + x2 + x3"),
        ([0,1,2,3],"全部")]
best=None
for cols,label in MODELS:
    c,r2=lstsq(X,Y,cols)
    if c is None: continue
    cs=" ".join(f"{NAMES[cols[a]]}={c[a]:+.4e}" for a in range(len(cols)))
    print(f"  {label:34s} {cs:60s} {r2:8.5f}")
    if best is None or r2>best[2]: best=(cols,c,r2,label)

print()
print("="*112)
print("[R] 最良モデルの残差(生の値)")
print("="*112)
cols,c,r2,label=best
print(f"  採用: {label}   R^2={r2:.5f}")
print("  k   Delta      実測sl(x1e-5)   fable予言(x1e-5)   最良モデル(x1e-5)   残差(x1e-5)")
for i,k in enumerate(KS):
    fit=sum(c[a]*X[i][cols[a]] for a in range(len(cols)))
    print(f" {k:3d} {DAT[k]['D']:+7d}     {Y[i]*1e5:+9.3f}         {DAT[k]['g']*1e5:+9.3f}"
          f"          {fit*1e5:+9.3f}        {(Y[i]-fit)*1e5:+9.3f}")
