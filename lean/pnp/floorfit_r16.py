# floorfit_r16.py (2026-08-08, opus-5 11周目)
# 目的: 定理E の下界がどれくらい tight か、そして「大域(R_c)」と「窓(eps_d)」の
#       2つの量が実際どういう関係にあるかを数値で切り分ける。
#
#   量1(定理Eが厳密に押さえる量): S_glob = (max_c R_c - min_c R_c)/(平均 R_c)
#         下界 LB = 2*sqrt2*2^{-b/2}。比 S_glob/LB は必ず >= 1。1 に近いほど床に張り付き。
#   量2(定理D が必要とする量): eps_d = 窓 Win_d 上の r の max/min - 1。
#         定理E は直接これを押さえない。両者の大きさを並べて関係を見る。
import math, cmath, random

def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
ALLP=[p for p in primes_upto(5000) if p%2==1]

def rep_counts(B):
    tot=sum(B); r=[0]*(tot+1); r[0]=1
    for a in B:
        for m in range(tot,a-1,-1): r[m]+=r[m-a]
    return r
def rget(r,m): return r[m] if 0<=m<len(r) else 0

def glob_spread(B):
    """R_c の相対スプレッドと、定理E の下界との比"""
    b=len(B); r=rep_counts(B)
    R=[0,0,0,0]
    for m,v in enumerate(r): R[m%4]+=v
    mean=sum(R)/4
    S=(max(R)-min(R))/mean
    LB=2*math.sqrt(2)*2.0**(-b/2)
    # 予言(等号条件つき): 2^{b/2}*max(|cos phi|,|sin phi|)/2^{b-2}
    F=1+0j
    for a in B: F*=(1+1j**a)
    phi=cmath.phase(F)
    exact=2.0**(b/2)*max(abs(math.cos(phi)),abs(math.sin(phi)))/(2.0**b/4)
    return S, LB, S/LB, exact

def eps_window(A, d):
    """定理D が使う窓平坦性 eps_d"""
    A=sorted(A); T=sum(A); n=T//2
    Id=[a for a in A if a<=2*d]; Bd=[a for a in A if a>2*d]
    sig=sum(Id); rB=rep_counts(Bd)
    subs={0}
    for a in Id: subs |= {s+a for s in subs}
    targets=sorted({n-s for s in subs} | {n+d, n-d-sig})
    vals=[rget(rB,m) for m in targets]
    lo,hi=min(vals),max(vals)
    return (hi/lo-1) if lo>0 else float('inf'), len(Bd)

print("="*96)
print("[1] 大域量 S_glob = (max R_c - min R_c)/平均  と 定理E の下界 2√2·2^(-b/2)")
print("    (定理E が厳密に押さえるのはこの量。比は必ず 1 以上、1 に近いほど床に張り付き)")
print("="*96)
print("  列                     b    S_glob        下界 LB       S/LB    予言(等号形)  一致")
def show(name,B):
    S,LB,ratio,exact = glob_spread(B)
    ok="OK" if abs(S-exact)<1e-9*max(1,exact) else "NG"
    print(f" {name:<20} {len(B):3d} {S:.6e} {LB:.6e} {ratio:7.4f}  {exact:.6e}  {ok}")

for k in range(16,33,4):
    show(f"素数 d=2 (k={k})", [a for a in ALLP[:k] if a>4])
print()
rng=random.Random(20260808)
for k in (16,20,24,28,32):
    maxV=ALLP[k-1]; cands=[x for x in range(3,maxV+1,2)]
    rs=[]
    for _ in range(40):
        B=sorted(rng.sample(cands,k))
        S,LB,ratio,_=glob_spread(B); rs.append(ratio)
    rs.sort()
    print(f" ランダム奇数 k={k:2d}      {k:3d}   中央値 S/LB = {rs[20]:6.4f}   最小 {rs[0]:6.4f}   最大 {rs[-1]:6.4f}")
print()
print(" 奇数を全部並べた列(等号ケース):")
show("1,3,...,29", list(range(1,30,2)))
show("1,3,...,41", list(range(1,42,2)))

print()
print("="*96)
print("[2] 窓量 eps_d(定理D が使う量)と 大域量・床 の対比")
print("    定理E は eps_d を直接押さえない。両者の桁を並べて関係を見る。")
print("="*96)
print("  k    b_2   eps_2(素数)   S_glob(素数)  床 LB       eps_2/LB   S_glob/LB")
for k in range(16,33,2):
    A=ALLP[:k]
    e2,b = eps_window(A,2)
    B2=[a for a in A if a>4]
    S,LB,ratio,_ = glob_spread(B2)
    print(f" {k:3d} {b:5d}  {e2:.4e}  {S:.4e}  {LB:.4e}  {e2/LB:9.2f}  {ratio:9.4f}")

print()
print("  ランダム奇数列(20シード中央値)- 素数と違い mod-6 が消えるので床に近いはず:")
print("  k    b_2   eps_2(乱数)   S_glob(乱数)  床 LB       eps_2/LB   S_glob/LB")
for k in range(16,33,2):
    maxV=ALLP[k-1]; cands=[x for x in range(3,maxV+1,2)]
    rng2=random.Random(555+k)
    es=[]; ss=[]
    for _ in range(20):
        A=sorted(rng2.sample(cands,k))
        try:
            e2,b=eps_window(A,2)
        except Exception:
            continue
        B2=[a for a in A if a>4]
        if len(B2)==0: continue
        S,LB,ratio,_=glob_spread(B2)
        if e2==float('inf'): continue
        es.append(e2/LB); ss.append(ratio)
    if not es: continue
    es.sort(); ss.sort()
    A0=sorted(rng2.sample(cands,k)); B0=[a for a in A0 if a>4]
    _,LB0,_,_=glob_spread(B0)
    print(f" {k:3d} {len(B0):5d}  {'---':>11}  {'---':>11}  {LB0:.4e}  {es[len(es)//2]:9.2f}  {ss[len(ss)//2]:9.4f}")
