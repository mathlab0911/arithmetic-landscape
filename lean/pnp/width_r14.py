# width_r14.py (2026-08-08, opus-5 9周目)
# 持ち越し2: L3 の幅因子 sqrt(V0/Vq) を q=6 以外(q=4, 3)でも検証する。
#   予言:  振幅_q = 2 * (|F(zeta_q)|/2^b) * sqrt(V0/Vq),  Vq = (1/4) sum a^2 sec^2(pi a/q)
#   q=4 (奇数列): |cos(pi a/4)| = 1/sqrt2 一定 -> Vq = sum a^2 /2, sqrt(V0/V4) = 1/sqrt2
#   q=3 (3 を含まない素数列): |cos(pi a/3)| = 1/2 一定 -> V3 = sum a^2, sqrt(V0/V3) = 1/2
# 「幅因子あり」と「なし」の両方と比べ、どちらが 1 になるかで判定する。
# 抽出窓は狭窓(hw は sigma の 0.1〜0.15 倍)。8周目の教訓。
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

def comp(B, q, hw):
    """周期 q 成分の振幅(狭窓 DFT)"""
    b=len(B); S=sum(B); V0=sum(a*a for a in B)/4.0
    r=rep_counts(B); c=S//2
    N=(2*hw//q)*q
    acc=0j; used=0
    for t in range(N):
        m=c-N//2+t
        if m<0 or m>=len(r) or r[m]==0: continue
        d=m-S/2.0
        lg=b*math.log(2)-0.5*math.log(2*math.pi*V0)-d*d/(2*V0)
        acc+=(r[m]/math.exp(lg)-1.0)*cmath.exp(-2j*math.pi*m/q); used+=1
    return abs((2.0/used)*acc)

def predict(B, q):
    """(幅因子あり, 幅因子なし)"""
    b=len(B)
    Z=cmath.exp(2j*math.pi/q)
    F=1+0j
    for a in B: F*=(1+Z**a)
    rel=abs(F)/2.0**b
    V0=sum(a*a for a in B)/4.0
    Vq=sum(a*a/(math.cos(math.pi*a/q)**2) for a in B)/4.0
    return 2*rel*math.sqrt(V0/Vq), 2*rel

print("="*90)
print("[q=4] 素数の d=1 層(3 を含むので mod-6 が消え、mod-4 が主項)")
print("="*90)
print("  k   b   sigma    hw   実測振幅     幅因子あり    比      幅因子なし    比")
for k in range(16,29,2):
    B=[a for a in ALLP[:k] if a>2]; b=len(B)
    sg=math.sqrt(sum(a*a for a in B)/4.0); hw=max(12,int(0.12*sg))
    m=comp(B,4,hw); pw,pn=predict(B,4)
    print(f" {k:3d} {b:3d} {sg:7.1f} {hw:5d}  {m:.5e}  {pw:.5e} {m/pw:6.3f}  {pn:.5e} {m/pn:6.3f}")

print()
print("="*90)
print("[q=3] 素数の d=2 層(5以上の素数 -> 全て ±1 mod 3、|cos(pi a/3)|=1/2 一定)")
print("="*90)
print("  k   b   sigma    hw   実測振幅     幅因子あり    比      幅因子なし    比")
for k in range(10,23,2):
    B=[a for a in ALLP[:k] if a>4]; b=len(B)
    sg=math.sqrt(sum(a*a for a in B)/4.0); hw=max(12,int(0.12*sg))
    m=comp(B,3,hw); pw,pn=predict(B,3)
    print(f" {k:3d} {b:3d} {sg:7.1f} {hw:5d}  {m:.5e}  {pw:.5e} {m/pw:6.3f}  {pn:.5e} {m/pn:6.3f}")

print()
print("="*90)
print("[q=4] ランダム奇数列(20シード中央値、mod-6 は大半で消える)")
print("="*90)
print("  k   b   実測振幅     幅因子あり    比      幅因子なし    比")
for k in range(16,29,2):
    maxV=ALLP[k-1]; cands=[x for x in range(3,maxV+1,2)]
    rng=random.Random(20260808+k)
    rs_w=[]; rs_n=[]
    for _ in range(20):
        B=sorted(rng.sample(cands,k)); b=len(B)
        sg=math.sqrt(sum(a*a for a in B)/4.0); hw=max(12,int(0.12*sg))
        m=comp(B,4,hw); pw,pn=predict(B,4)
        rs_w.append(m/pw); rs_n.append(m/pn)
    rs_w.sort(); rs_n.sort()
    print(f" {k:3d} {k:3d}       ---        ---     {rs_w[10]:6.3f}       ---     {rs_n[10]:6.3f}")
