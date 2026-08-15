# l5bscale_r26.py : L5b の有効半径。
#   包絡が使えるのは G のゼロを含まない区間だけ。最も近いゼロは theta = pi/max(B) 程度、
#   半径は約 pi/(2 max B)。一方ガウス包絡の減衰スケールは 1/sqrt(V0) = 2/sqrt(S2)。
#   両者の比 = 有効半径が何 sigma 分あるか。k とともに増えるかを見る。
import math
def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
ALLP=[p for p in primes_upto(2000) if p%2==1]
print("   k    b   max B    S2         1/sqrt(V0)     pi/(2 maxB)   有効半径 [sigma]   0.45*sqrt(k)")
for k in range(16,49,4):
    B=[a for a in ALLP[:k] if a>4]; b=len(B)
    S2=sum(a*a for a in B); V0=S2/4.0; am=max(B)
    sig=1/math.sqrt(V0); rad=math.pi/(2*am)
    print(f"  {k:3d}  {b:3d}  {am:5d}  {S2:9d}   {sig:.6f}     {rad:.6f}      {rad/sig:8.3f}       {0.45*math.sqrt(k):8.3f}")
print()
print("  ⇒ 有効半径(sigma 単位)が k とともに増えるなら、L5b の包絡は使い物になる。")
print("     理論: 有効半径/sigma = (pi/(2 a_max)) * sqrt(S2)/2 ~ (pi/4) sqrt(k/3) ~ 0.45 sqrt(k)")
