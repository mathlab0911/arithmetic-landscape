# oeisseq_r30.py : OEIS 照会用に、本研究の中心的な数列を厳密に生成する。
#   もし誰かが同じ対象を研究していれば、これらの数列は OEIS に載っている可能性が高い。
#   載っていなければ「少なくとも数列としては未登録」という、かなり強い証拠になる。
#
# ★ このスクリプトは検査そのものではない。検査を「準備する」だけである(台帳 F20)。
#   照会は人間がブラウザで行う。その答えの置き場は lean/pnp/oeis_r119.log であり、
#   2026-08-11 に4本すべてを実施済み(陽性対照つき・全て該当なし)。
#   このファイルの .log は数列を印字するだけで、結果は含まない。結果は上のファイルにある。
import math
def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
P=[p for p in primes_upto(500) if p%2==1]     # 3,5,7,11,...

def lm_deg(B):
    """n = floor(T/2)。全数探索(2^k)。k<=22 まで。"""
    k=len(B); n=sum(B)//2
    sums=[0]
    for x in B: sums=sums+[s+x for s in sums]
    gs=min(abs(s-n) for s in sums)
    deg=sum(1 for s in sums if abs(s-n)==gs)
    lm=0
    for idx,s in enumerate(sums):
        e=abs(s-n); ok=True
        for i in range(k):
            ns=s-B[i] if (idx>>i)&1 else s+B[i]
            if abs(ns-n)<=e: ok=False; break
        if ok: lm+=1
    return lm,deg,gs

print("A: 先頭 k 個の奇素数(3,5,7,...)の部分和地形")
print("   k :  lm      deg     gs")
LM=[];DEG=[]
for k in range(1,23):
    B=P[:k]
    lm,deg,gs=lm_deg(B)
    LM.append(lm); DEG.append(deg)
    print(f"  {k:2d} : {lm:8d} {deg:7d} {gs:4d}")
print()
print("OEIS 照会用(カンマ区切り):")
print("  lm  =", ", ".join(map(str,LM)))
print("  deg =", ", ".join(map(str,DEG)))
print()
print("B: Gamma(A_k) = sum a_j/2^j の分子(分母 2^k)—— 有理数として厳密")
from fractions import Fraction
NUM=[]
for k in range(1,23):
    B=P[:k]
    g=Fraction(0)
    for j,x in enumerate(B,1): g+=Fraction(x,2**j)
    NUM.append(g.numerator*(2**k)//g.denominator if g.denominator<=2**k else None)
    print(f"  k={k:2d}  Gamma = {g}  = {float(g):.6f}")
print()
print("  Gamma の分子(分母を 2^k に揃えたときの分子):")
print("  ", ", ".join(str(n) for n in NUM))
