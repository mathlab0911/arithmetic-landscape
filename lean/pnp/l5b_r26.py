# l5b_r26.py : fable-5 の L5b(ガウス包絡)を数値で確認する。
#   主張: log|G| の2階微分 = -sum (a^2/4) sec^2(a theta/2) <= -V0 (V0 = S2/4)
#         ⇒ G がゼロを持たない区間の内点最大 theta* から
#           |G(theta)| <= |G(theta*)| exp(-V0 (theta-theta*)^2 / 2)
# V3: 区間の取り方を2通り(峰の周りの狭い区間 / 隣接ゼロ点までの広い区間)で確認する。
import math
def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
ALLP=[p for p in primes_upto(400) if p%2==1]
k=24; A=ALLP[:k]; B=[a for a in A if a>4]      # d=2 の切断列
b=len(B); S2=sum(a*a for a in B); V0=S2/4.0
print(f"  k={k}, d=2 ⇒ b={b}, S2={S2}, V0={V0:.1f}, sqrt(2/V0)={math.sqrt(2/V0):.5f}")

def logG(th):
    v=0.0
    for a in B:
        c=abs(math.cos(a*th/2.0))
        if c<1e-300: return None
        v+=math.log(c)
    return v
def d2logG(th):
    return -sum((a*a/4.0)/math.cos(a*th/2.0)**2 for a in B)

print()
print("[1] 2階微分の実測が -V0 以下か(主張の核)")
print("     theta        d2 log|G|        -V0        d2/(-V0)")
for name,th in (("2pi/6",2*math.pi/6),("2pi/4",2*math.pi/4),("2pi/8",2*math.pi/8),
                ("0.01",0.01),("1.0",1.0)):
    print(f"  {name:8s} {th:.6f}   {d2logG(th):14.2f}   {-V0:10.1f}    {d2logG(th)/(-V0):8.4f}")
print("  ⇒ 比が 1 以上なら sec^2>=1 の主張どおり(2階微分は -V0 より下)")

print()
print("[2] 包絡の検証: |G(th)| <= |G(th*)| exp(-V0 (th-th*)^2/2) が全点で成り立つか")
for th_star,label in ((2*math.pi/6,"q=6 の峰"),(2*math.pi/4,"q=4 の峰")):
    L0=logG(th_star)
    for half,tag in ((0.004,"狭い区間 (±0.004)"),(0.02,"広い区間 (±0.02)")):
        worst=-1e9; worst_th=None; n=0
        N=4000
        for i in range(N+1):
            th=th_star-half+2*half*i/N
            L=logG(th)
            if L is None: continue
            slack=(L0-V0*(th-th_star)**2/2.0)-L      # >= 0 なら包絡が上
            n+=1
            if -slack>worst: worst=-slack; worst_th=th
        print(f"  {label} / {tag}: 判定点 {n}、包絡−実測 の最小値 = {-worst:+.6e}  "
              f"{'OK(包絡が上)' if worst<=1e-12 else '★破れ'}  @ th={worst_th:.6f}")

print()
print("[3] 峰が本当に局所最大か(内点最大の仮定の確認)")
for th_star,label in ((2*math.pi/6,"q=6"),(2*math.pi/4,"q=4")):
    L0=logG(th_star); ok=True
    for dd in (1e-5,1e-4,1e-3,1e-2):
        for s in (+1,-1):
            L=logG(th_star+s*dd)
            if L is not None and L>L0+1e-12: ok=False
    print(f"  {label}: {'局所最大である' if ok else '★局所最大でない'}")
