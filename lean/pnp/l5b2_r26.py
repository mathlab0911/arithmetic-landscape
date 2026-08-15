# l5b2_r26.py : L5b の再検証。
# 前回 l5b_r26.py で「破れ」が出たが、原因は包絡の中心を 2pi/q に置いたこと。
# 2pi/q は局所最大ではない(h'(0) = -Delta/(2 sqrt3) != 0)。
# 真の局所最大 theta* を数値で求めてから包絡を張り直す。
import math
def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
ALLP=[p for p in primes_upto(400) if p%2==1]
k=24; A=ALLP[:k]; B=[a for a in A if a>4]
b=len(B); S2=sum(a*a for a in B); V0=S2/4.0
tau=lambda a: 1 if a%6==1 else (-1 if a%6==5 else 0)
Delta=sum(tau(a)*a for a in B)
def logG(th):
    v=0.0
    for a in B:
        c=abs(math.cos(a*th/2.0))
        if c<1e-300: return None
        v+=math.log(c)
    return v
def d1(th): return -sum((a/2.0)*math.tan(a*th/2.0) for a in B)
def d2(th): return -sum((a*a/4.0)/math.cos(a*th/2.0)**2 for a in B)

print(f"  b={b}, S2={S2}, V0={V0:.1f}, Delta={Delta}")
print()
print("[1] 真の局所最大 theta* を求める(Newton 法、2pi/q から出発)")
print("     q    2pi/q        theta*(真の極大)   ずれ       理論の目安 -h'(0)/h''(0)")
stars={}
for q in (6,4,8):
    th=2*math.pi/q
    for _ in range(60):
        g1=d1(th); g2=d2(th)
        th=th-g1/g2
    stars[q]=th
    th0=2*math.pi/q
    est=-d1(th0)/d2(th0)
    print(f"   {q:2d}  {th0:.9f}   {th:.9f}   {th-th0:+.3e}   {est:+.3e}")

print()
print("[2] 包絡 |G(th)| <= |G(th*)| exp(-V0 (th-th*)^2/2) を真の theta* で検証")
for q in (6,4,8):
    ts=stars[q]; L0=logG(ts)
    for half,tag in ((0.004,"±0.004"),(0.02,"±0.02"),(0.05,"±0.05")):
        worst=1e9; wth=None; n=0; N=6000
        for i in range(N+1):
            th=ts-half+2*half*i/N
            L=logG(th)
            if L is None: continue
            slack=(L0-V0*(th-ts)**2/2.0)-L
            n+=1
            if slack<worst: worst=slack; wth=th
        print(f"  q={q:2d} / {tag}: 判定点 {n}、(包絡−実測) の最小 = {worst:+.3e}  "
              f"{'OK' if worst>=-1e-9 else '★破れ'}")
print()
print("  ⇒ すべて OK なら L5b は成立。ただし『包絡の中心は 2pi/q ではなく真の極大』が必要条件。")
