# ripple_fit_r12.py (2026-08-08, opus-5 7周目)
# 設計文書 paper2_transfer_r11.md §6 の持ち越し 2, 3, 4 の数値照合。
#
# 予言(L3):  r_B(m)/Main(m) - 1 ~ 2 (sqrt3/2)^{b+1} cos(pi*m/3 - (pi/6)(c1-c5))
#   Main(m) = 2^b / sqrt(2 pi V0) * exp(-delta^2/(2 V0)),  delta = m - sum(B)/2, V0 = sum(a^2)/4
#   振幅の「+1」は幅因子 sqrt(V0/V6) = sqrt(3)/2 から来る(これが L3 の非自明な部分)
#   位相は arg F(zeta6) = (pi/6)(c1-c5),  c1=#{a=1 mod 6}, c5=#{a=5 mod 6}
#
# 抽出は窓上の離散フーリエ成分: C = (2/N) sum_m R(m) e^{-i pi m /3}
#   -> |C| = 振幅, arg(C) = -位相
import math, cmath, random

def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]

ALLP=[p for p in primes_upto(3000) if p%2==1]

def rep_counts(B):
    tot=sum(B); r=[0]*(tot+1); r[0]=1
    for a in B:
        for m in range(tot,a-1,-1): r[m]+=r[m-a]
    return r

def fourier_component(B, q, halfwidth=90):
    """r_B/Main - 1 の周期 q 成分。戻り値 (振幅, 位相phi) で ripple=Amp*cos(2pi m/q - phi)."""
    b=len(B); S=sum(B); V0=sum(a*a for a in B)/4.0
    r=rep_counts(B)
    c=S//2
    # 完全周期になるよう窓幅を q の倍数に丸める
    N=(2*halfwidth//q)*q
    ms=[c-N//2+t for t in range(N)]
    acc=0j; used=0
    for m in ms:
        if m<0 or m>=len(r) or r[m]==0: continue
        delta=m-S/2.0
        logmain=b*math.log(2)-0.5*math.log(2*math.pi*V0)-delta*delta/(2*V0)
        R=r[m]/math.exp(logmain)-1.0
        acc+=R*cmath.exp(-2j*math.pi*m/q); used+=1
    if used==0: return float('nan'), float('nan')
    C=(2.0/used)*acc
    return abs(C), -cmath.phase(C)

SQ = math.sqrt(3)/2

print("="*78)
print("[2] リップル公式の直接フィット  (B = 素数列の d=2 切断: 5 以上の素数)")
print("="*78)
print(" k    b   実測振幅      予言 2(√3/2)^(b+1)   比      実測位相    予言位相   差")
for k in range(14, 29, 2):
    A = ALLP[:k]
    B = [a for a in A if a > 4]                      # d = 2
    b = len(B)
    c1 = sum(1 for a in B if a % 6 == 1)
    c5 = sum(1 for a in B if a % 6 == 5)
    amp, phi = fourier_component(B, 6)
    pred_amp = 2*SQ**(b+1)
    pred_phi = (math.pi/6)*(c1-c5)
    # 位相は mod 2pi で比較
    dphi = (phi - pred_phi + math.pi) % (2*math.pi) - math.pi
    print(f"{k:3d} {b:4d}   {amp:.6e}   {pred_amp:.6e}   {amp/pred_amp:.4f}"
          f"   {phi:+.4f}   {pred_phi % (2*math.pi) - math.pi if False else pred_phi:+.4f}   {dphi:+.4f}")

print()
print("  参考: 「+1」なしの予言 2(√3/2)^b との比も出す(+1 が本当に要るかの判定)")
print(" k    b   実測/2(√3/2)^(b+1)   実測/2(√3/2)^b")
for k in range(14, 29, 2):
    A = ALLP[:k]; B=[a for a in A if a>4]; b=len(B)
    amp,_ = fourier_component(B, 6)
    print(f"{k:3d} {b:4d}      {amp/(2*SQ**(b+1)):.4f}              {amp/(2*SQ**b):.4f}")

print()
print("="*78)
print("[4] M(q) = (1/2)|Phi_q(-1)|^{1/phi(q)} の検証と順位表")
print("="*78)

def phi_euler(q): return sum(1 for r in range(1,q+1) if math.gcd(r,q)==1)

def M_direct(q):
    """幾何平均を直接計算: (prod_{r coprime q} |cos(pi r/q)|)^{1/phi(q)}"""
    vals=[abs(math.cos(math.pi*r/q)) for r in range(1,q+1) if math.gcd(r,q)==1]
    if any(v==0 for v in vals): return 0.0
    return math.exp(sum(math.log(v) for v in vals)/len(vals))

def phi_q_at_minus1(q):
    """古典値: q=1->0? / q=2->0 / q=2p^j -> p / q=2^j (j>=2) -> 2 / その他 q>=3 -> 1"""
    if q==2: return 0
    if q==1: return -2
    # q = 2^j
    t=q
    j=0
    while t%2==0: t//=2; j+=1
    if t==1: return 2 if j>=2 else 0
    # t は奇数部分
    ps=set()
    x=t; d=3
    while d*d<=x:
        while x%d==0: ps.add(d); x//=d
        d+=2
    if x>1: ps.add(x)
    if j==1 and len(ps)==1: return ps.pop()      # q = 2 p^i
    return 1

rows=[]
for q in range(3,41):
    md=M_direct(q)
    pc=abs(phi_q_at_minus1(q))
    mf=0.5*pc**(1.0/phi_euler(q)) if pc>0 else 0.0
    rows.append((q,md,mf,phi_euler(q),phi_q_at_minus1(q)))

print("  q  phi(q)  Phi_q(-1)   M(q)直接計算   M(q)閉形式    差")
for q,md,mf,ph,pc in rows[:18]:
    print(f" {q:3d}  {ph:5d}   {pc:6d}    {md:.8f}    {mf:.8f}   {abs(md-mf):.2e}")

print()
print("  --- M(q) の大きい順(q >= 3、上位8件)---")
for q,md,mf,ph,pc in sorted(rows,key=lambda t:-t[1])[:8]:
    tag = "  <- sqrt(3)/2" if abs(md-SQ)<1e-12 else ""
    print(f"   q={q:3d}   M(q) = {md:.8f}{tag}")
print(f"   (sqrt(3)/2 = {SQ:.8f},  5^(1/4)/2 = {5**0.25/2:.8f},  1/sqrt2 = {1/math.sqrt(2):.8f})")
print(f"   最大値の差 (M(6) - 第2位) = {SQ - sorted([r[1] for r in rows])[-2]:.8f}")

print()
print("="*78)
print("[3] 予想 R1/R2: mod-4 床  振幅 2(1/sqrt2)^{b+1}、レート 2^{-1/2}=0.70711")
print("="*78)
INV = 1/math.sqrt(2)

print(" R2: 素数の d=1 層(3 を含むので mod-6 が消え、mod-4 床が主項のはず)")
print(" k    b   周期4の実測振幅   予言 2(1/√2)^(b+1)    比      周期6の振幅")
for k in range(14, 27, 2):
    A = ALLP[:k]
    B = [a for a in A if a > 2]        # d = 1 : 3 が残る
    b = len(B)
    a4,_ = fourier_component(B, 4)
    a6,_ = fourier_component(B, 6)
    pred = 2*INV**(b+1)
    print(f"{k:3d} {b:4d}     {a4:.6e}    {pred:.6e}   {a4/pred:.4f}    {a6:.3e}")

print()
print(" R1: ランダム奇数列(20シードの中央値)")
print(" k    b   周期4の実測振幅   予言 2(1/√2)^(b+1)    比")
for k in range(14, 27, 2):
    maxV = ALLP[k-1]
    cands=[x for x in range(3,maxV+1,2)]
    rng=random.Random(20260808+k)
    vals=[]
    for _ in range(20):
        B=sorted(rng.sample(cands,k))
        a4,_=fourier_component(B,4)
        if a4==a4: vals.append(a4/(2*INV**(len(B)+1)))
    vals.sort()
    med=vals[len(vals)//2]
    b=k
    print(f"{k:3d} {b:4d}     {med*2*INV**(b+1):.6e}    {2*INV**(b+1):.6e}   {med:.4f}")

print()
print(" 減衰レート(周期4振幅の log 線形回帰、k>=18)")
def fit(ks, vs):
    ks=[k for k,v in zip(ks,vs) if v==v and v>0]; ys=[math.log(v) for v in vs if v==v and v>0]
    n=len(ks); mk=sum(ks)/n; my=sum(ys)/n
    sl=sum((k-mk)*(y-my) for k,y in zip(ks,ys))/sum((k-mk)**2 for k in ks)
    return math.exp(sl)
KS=[k for k in range(18,27,2)]
v_p=[fourier_component([a for a in ALLP[:k] if a>2],4)[0] for k in KS]
print(f"   素数 d=1: lambda = {fit(KS,v_p):.5f}   (予言 {INV:.5f})")
