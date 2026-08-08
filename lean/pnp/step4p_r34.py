# step4p_r34.py (2026-08-08, opus-5 35周目) : fable-5 r33 作業3。
# Step 4' の予算が守られるかを数値で確認する。
#
# 【重要な設計判断】fable-5 は k=24, 32 で確認せよと指示したが、
#   delta_0 = 1/log b は b=23 で 0.318、N_0 = b^{1/4} は 2.19 で、
#   漸近パラメータとして意味をなさない(N_0 delta_0 = 0.70 なので尾の上界 C/(N_0 delta_0) は 1 超)。
#   |G| の評価も S_B(n theta) も O(b) で計算できるので、**k を 2000 まで上げて漸近域で検証する**。
#   k=24, 32 も参考として併記する。
import math, random
from fractions import Fraction

def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
P=[p for p in primes_upto(300000) if p%2==1]

def star_discrepancy(xs):
    xs=sorted(xs); n=len(xs); d=0.0
    for i,x in enumerate(xs,1):
        d=max(d, abs(i/n - x), abs(x - (i-1)/n))
    return d

def analyse(B, th):
    b=len(B)
    us=[(a*th/(2*math.pi)) % 1.0 for a in B]         # u_p = p theta / 2pi mod 1
    D=star_discrepancy(us)
    d0=1.0/math.log(b)
    N0=max(2, int(round(b**0.25)))
    # 悪い点: ||u - 1/2|| < d0
    bad=[u for u in us if abs(((u-0.5+0.5)%1.0)-0.5)<d0]
    # 厳密な log|G| (= sum log|cos(pi u)| )
    ok=True; lg=0.0
    for u in us:
        c=abs(math.cos(math.pi*u))
        if c<1e-300: ok=False; break
        lg+=math.log(c)
    if not ok: return None
    # head: sum_{n<=N0} (1/n)|S_B(n theta)|
    head=0.0
    for n in range(1,N0+1):
        s=complex(0,0)
        for a in B: s+=complex(math.cos(2*math.pi*n*a*th/(2*math.pi)), math.sin(2*math.pi*n*a*th/(2*math.pi)))
        head+=abs(s)/n
    return dict(b=b,D=D,d0=d0,N0=N0,nbad=len(bad),
                bad_frac=len(bad)/b, bound=(D+2*d0),
                lgb=lg/b, excess=lg/b+math.log(2),
                head_frac=head/b, tail_bound=1.0/(N0*d0))

def deep_theta(seed, minq=40, maxq=100000):
    rnd=random.Random(seed)
    while True:
        th=rnd.uniform(0.05, math.pi-0.05)
        q=Fraction(th/(2*math.pi)).limit_denominator(maxq).denominator
        if q>minq: return th,q

print("="*118)
print("[Step 4'] 深い minor arc での予算チェック(delta_0 = 1/log b, N_0 = b^{1/4})")
print("="*118)
print("   k     b    delta_0   N_0   D_B      |B_bad|/b   上界 D+2d0   判定 |  -(1/b)log|G| - log2   head/b   尾の上界")
for k in (24,32,100,300,1000,2000):
    B=[a for a in P[:k] if a>4]
    th,q=deep_theta(1000+k)
    r=analyse(B,th)
    if r is None: print(f" {k:5d}  (cos がゼロに当たった。スキップ)"); continue
    ok = "OK" if r['bad_frac']<=r['bound'] else "★破れ"
    print(f" {k:5d} {r['b']:5d}  {r['d0']:7.4f} {r['N0']:4d}  {r['D']:7.4f}   {r['bad_frac']:8.4f}    {r['bound']:8.4f}   {ok:5s}|"
          f"    {r['excess']:+11.5f}       {r['head_frac']:7.4f}   {r['tail_bound']:8.3f}")
print()
print("  読み方:")
print("   ・|B_bad|/b <= D_B + 2 delta_0  が Step 4' の第1の予算(悪い点は o(b) 個)")
print("   ・-(1/b)log|G| - log2 が 0 に向かえば、目標 |G| <= (1/2+o(1))^b の向き")
print("   ・head/b が 0 に向かえば、指数和の頭の項が o(b)(Step 1-2 の帰結)")
print("   ・尾の上界 C/(N_0 delta_0) が 1 を切って初めて意味を持つ")
print()
print("="*118)
print("[比較] 同じ k で、複数の深い theta を取ったときのばらつき")
print("="*118)
print("   k     b   theta ごとの -(1/b)log|G| - log2")
for k in (100,300,1000,2000):
    B=[a for a in P[:k] if a>4]
    vals=[]
    for s in range(6):
        th,_=deep_theta(7000+100*k+s)
        r=analyse(B,th)
        if r: vals.append(r['excess'])
    print(f" {k:5d} {len(B):5d}   " + "  ".join(f"{v:+.5f}" for v in vals))
