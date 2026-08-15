# selfl1_r56.py (2026-08-09, opus-5 56周目) : fable-5 r55 作業1 の検算。
#  比較補題は 2^{ω−1}·log(2φ+2) ≤ (φ/2)·log3  ⟺  (2φ+2)^{2^ω} ≤ 3^φ   【完全な整数比較】
#  (a) 例外リストの独立再現(奇・平方因子なし q ≤ 30000 の全数)
#  (b) q=21 の margin を厳密整数で
#  (c) 各 ω の最小 φ(奇プリモリアル)と、固定 ω 内の単調性の閾値
from math import gcd, log
def phi(n):
    r=n; m=n; p=2
    while p*p<=m:
        if m%p==0:
            while m%p==0: m//=p
            r-=r//p
        p+=1
    if m>1: r-=r//m
    return r
def omega(n):
    c=0; m=n; p=2
    while p*p<=m:
        if m%p==0:
            c+=1
            while m%p==0: m//=p
        p+=1
    if m>1: c+=1
    return c
def squarefree(n):
    m=n; p=2
    while p*p<=m:
        if m%(p*p)==0: return False
        p+=1
    return True

print("="*100)
print("(a) 比較補題 (2φ+2)^{2^ω} ≤ 3^φ  の例外(奇・平方因子なし 3 ≤ q ≤ 30000 の全数)")
print("    ※ 整数どうしの厳密比較。浮動小数を一切使わない。")
print("="*100)
exc=[]
for q in range(3,30001,2):
    if not squarefree(q): continue
    ph=phi(q); w=omega(q)
    if (2*ph+2)**(2**w) > 3**ph: exc.append(q)
print(f"    例外: {exc}")
print(f"    ⇒ {'fable-5 の主張どおり {3,5,15} の3個だけ' if exc==[3,5,15] else '★主張と不一致'}")
print()
print("="*100)
print("(b) 小さい q の厳密整数比較(左辺 ≤ 右辺 なら補題が使える)")
print("="*100)
print("     q   ω   φ    (2φ+2)^{2^ω}                 3^φ                       判定")
for q in (3,5,7,9,11,15,21,33,35,105,1155,15015):
    if not squarefree(q) or q%2==0: 
        print(f"  {q:6d}   (平方因子ありまたは偶数のためスキップ)"); continue
    ph=phi(q); w=omega(q); L=(2*ph+2)**(2**w); R=3**ph
    Ls=str(L) if len(str(L))<26 else ("~10^"+str(len(str(L))-1))
    Rs=str(R) if len(str(R))<26 else ("~10^"+str(len(str(R))-1))
    print(f"  {q:6d}  {w:2d} {ph:4d}   {Ls:>26s}  {Rs:>26s}   {'OK' if L<=R else '★例外'}")
print()
print("    ※ q=21: 26^4 = 456976  ≤  3^12 = 531441   —— 厳密整数で成立(margin あり)")
print(f"       26^4 = {26**4}, 3^12 = {3**12}, 差 = {3**12-26**4}")
print()
print("="*100)
print("(c) 各 ω の最小 φ(奇プリモリアル)と、固定 ω 内の単調性の閾値 φ+1 > 2^ω/log3")
print("="*100)
def primes(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
OP=[p for p in primes(300) if p>2]
print("     ω   最小の q(奇プリモリアル)      最小 φ     閾値 2^ω/log3   単調性OK?   補題成立?")
for w in range(1,9):
    ps=OP[:w]; q=1
    for p in ps: q*=p
    ph=phi(q); thr=(2**w)/log(3)
    mono = (ph+1) > thr
    ok = (2*ph+2)**(2**w) <= 3**ph
    qs=str(q) if len(str(q))<22 else f"{q:.4e}"
    print(f"    {w:2d}   {qs:>22s}  {ph:>10d}   {thr:>12.2f}      {'YES' if mono else 'NO':>5s}"
          f"      {'OK' if ok else '★例外'}")
print()
print("  ⇒ 固定 ω 内では φ について margin が単調増(閾値を最小 φ が既に超えている)ので、")
print("     各 ω は最小 φ だけ確認すれば十分。ω=1,2 の最小(q=3,5,15)だけが例外。")
