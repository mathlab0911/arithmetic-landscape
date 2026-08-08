# p5check_r28.py (2026-08-08, opus-5 23周目) : fable-5 r27 作業2
#  (a) P5.1 閉形式のドリフト(0.997->0.980)の原因特定 —— 標本誤差か、公式の仮定か
#  (b) P5.2 超幾何裾 P(a_(J) <= delta N / k) <= (e(delta/2)/J)^J の検証
import math, random, statistics
def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
P=[p for p in primes_upto(200000) if p%2==1]
def gam(A):
    g=0.0; p=1.0
    for x in A: p/=2.0; g+=p*x
    return g
random.seed(20260810)

print("="*104)
print("[a] P5.1 閉形式 vs モンテカルロ —— 標本数を増やしてドリフトの正体を見る")
print("     E[Gamma] = (1-2^-k) + 2c(2-(k+2)2^-k),  c=(N+1)/(k+1)")
print("="*104)
print("     k     厳密公式    標本数    平均       標準誤差   (平均-公式)/SE    比")
for k,tr in ((100,20000),(400,20000),(800,20000)):
    pk=P[k-1]; N=(pk-3)//2+1; c=(N+1)/(k+1)
    exact=(1-2.0**-k)+2*c*(2-(k+2)*2.0**-k)
    cands=list(range(3,pk+1,2))
    vals=[gam(sorted(random.sample(cands,k))) for _ in range(tr)]
    m=statistics.mean(vals); se=statistics.stdev(vals)/math.sqrt(tr)
    print(f"  {k:4d}  {exact:10.4f}   {tr:6d}  {m:9.4f}   {se:8.4f}     {(m-exact)/se:+8.2f}     {m/exact:6.4f}")
print()
print("  |(平均-公式)/SE| が 2 程度以内なら、前回のドリフトは単なる標本誤差で、閉形式は厳密。")
print("  3 を大きく超えるなら公式の仮定(格子の端・N のパリティ)を疑う。")

print()
print("="*104)
print("[b] P5.2 超幾何裾: P(a_(J) <= delta*N/k を格子で言い換えた閾値) と上界 (e(delta/2)/J)^J")
print("    a_(J) は J 番目に小さい標本。格子 a=2i+1 なので a <= 2t+1 ⟺ i <= t。")
print("    閾値 t = delta * N / k(= 平均間隔の delta 倍のところまで)")
print("="*104)
print("      k     J   delta   実測 P        上界 (e(delta/2)/J)^J    判定")
TR=10000
for k in (100,400,1600,3200):
    pk=P[k-1]; N=(pk-3)//2+1
    cands=list(range(1,N+1))          # 格子インデックス
    for delta in (0.25,0.5,1.0):
        t=delta*N/k
        for J in (1,2,4,8):
            cnt=0
            for _ in range(TR):
                S=random.sample(cands,k)
                S.sort()
                if S[J-1]<=t: cnt+=1
            emp=cnt/TR
            ub=(math.e*(delta/2)/J)**J
            ok = "OK" if emp<=ub else "★破れ"
            print(f"   {k:5d}  {J:2d}   {delta:4.2f}   {emp:9.5f}      {ub:14.6f}      {ok}")
