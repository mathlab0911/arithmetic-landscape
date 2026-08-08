# l5c_smoke_r32.py (2026-08-08, opus-5 33周目) : fable-5 r31 作業1・3
#
# (A) 構造的観察の検証: log|2 cos(pi u)| = sum_{n>=1} (-1)^{n+1} cos(2 pi n u)/n
#     ⇒ log|G_B(theta)| = -b log2 + sum_n ((-1)^{n+1}/n) * Re( sum_{a in B} e(n a theta / 2pi) )
#     すなわち **我々の積は、素数上の指数和の重ね合わせに厳密に分解できる**。
#     これが Vinogradov / Helfgott 型の入力が効く理由。
# (B) Helfgott Main Theorem の適用条件 x >= 2.16e20 を k に翻訳
# (C) L5c 手順3-4 のスモークテスト: 深い minor arc で |G|^{1/b} が 0.5 近傍か
import math
from fractions import Fraction

def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
ALLP=[p for p in primes_upto(400) if p%2==1]

print("="*104)
print("[A] log|2 cos(pi u)| = sum_{n>=1} (-1)^{n+1} cos(2 pi n u)/n の数値検証")
print("="*104)
print("     u        左辺 log|2cos(pi u)|     右辺(N=20000項)        差")
for u in (0.1,0.2,0.3,0.37,0.45,0.05):
    lhs=math.log(abs(2*math.cos(math.pi*u)))
    rhs=sum(((-1)**(n+1))*math.cos(2*math.pi*n*u)/n for n in range(1,20001))
    print(f"  {u:5.2f}      {lhs:+16.10f}     {rhs:+16.10f}    {lhs-rhs:+.2e}")
print()
print("  ⇒ 一致すれば、log|G_B(theta)| は素数上の指数和 sum_{a in B} e(n a theta/2pi) の")
print("     重み (-1)^{n+1}/n による重ね合わせとして厳密に書ける。")
print("     (u = a theta/(2pi) が cos のゼロに近いと収束は遅いが、恒等式自体は成立)")

print()
print("="*104)
print("[B] Helfgott arXiv:1205.5252 Main Theorem の適用条件 x >= x_0 = 2.16e20 を k に翻訳")
print("="*104)
x0=2.16e20
li = x0/math.log(x0)*(1+1/math.log(x0)+2/math.log(x0)**2)
print(f"  x_0 = {x0:.3e},  log x_0 = {math.log(x0):.3f}")
print(f"  k_0 = pi(x_0) ~ {li:.4e}")
print(f"  参考: 我々の数値実験の上限 k = 44、L5a の k_0(eta=0.05) は最大 14723")
print()
print("  ⇒ Helfgott の明示定数版は k ~ 4.6e18 以上でしか使えない。")
print("     L5c を『効果的版』に格上げすることはできない。漸近版のままとし、")
print("     効果性は T1(L5a: k_0 ~ 10^4)と T2(L5b: 算術入力ゼロ)に限る、と明記すべき。")

print()
print("="*104)
print("[C] L5c スモークテスト: 深い minor arc(連分数分母 q が大きい theta)で |G|^{1/b}")
print("="*104)
def Gnorm(B,th):
    v=0.0
    for a in B:
        c=abs(math.cos(a*th/2.0))
        if c<1e-300: return 0.0
        v+=math.log(c)
    return math.exp(v)
def cf_den(x, maxq=100000):
    """x に最も近い有理近似の分母(連分数)を返す。"""
    f=Fraction(x).limit_denominator(maxq)
    return f.denominator
import random
random.seed(20260811)
for k in (24,32):
    B=[a for a in ALLP[:k] if a>4]; b=len(B)
    print(f"\n  k={k} (b={b}) :")
    print("     theta        theta/(2pi) の分母 q    |G|^{1/b}     M(q=5..) の目安 0.5")
    cands=[]
    for _ in range(4000):
        th=random.uniform(0.05, math.pi-0.05)
        q=cf_den(th/(2*math.pi))
        if q>40: cands.append((q,th))
    cands.sort(reverse=True)
    for q,th in cands[:6]:
        g=Gnorm(B,th)
        r=g**(1.0/b) if g>0 else 0.0
        print(f"   {th:.6f}          q = {q:6d}          {r:.4f}")
print()
print("  判定: 深い minor(q が大きい)で |G|^{1/b} が 0.5 近傍に落ちていれば、")
print("        L5c の目標『(1/2+o(1))^b』の向きは合っている(証明ではなく向きの確認)。")
