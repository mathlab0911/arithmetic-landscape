# character_check_r10.py — 論文2の出発点になる予測の検証。
# 主張: r_B の周期6リップルは、生成多項式 F_B(z)=prod(1+z^a) を 1 の原始6乗根で
#       評価した値で決まる。素数(>=5)は mod 6 で ±1 に限られるので各因子の絶対値は
#       |1+zeta6^{±1}| = sqrt(3)。よって相対振幅は (sqrt(3)/2)^{|B|}。
# 決定的な検証点: 3 は 3 mod 6 なので 1+zeta6^3 = 0。つまり 3 を含む B では
#       リップルが完全に消える。d=1 では B_1 が 3 を含み、d>=2 では含まない。
#       ⇒ eps_1 だけ極端に小さいはず(実測 eps_1=0.0003 vs eps_2=0.057, k=24)。
import cmath, math

def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]

ALLP=[p for p in primes_upto(2000) if p%2==1]

def F(B, j, Q=6):
    z = cmath.exp(2j*cmath.pi*j/Q)
    v = 1+0j
    for a in B: v *= (1 + z**a)
    return v

print("=== 1 の原始6乗根での各因子の絶対値 ===")
z6 = cmath.exp(2j*cmath.pi/6)
for r in range(6):
    print(f"  a = {r} mod 6 : |1 + zeta6^a| = {abs(1+z6**r):.6f}")
print(f"  (sqrt(3) = {math.sqrt(3):.6f})")

print()
print("=== |F_B(zeta6^j)| / 2^|B|  (B = 素数列の切断, k=24) ===")
A = ALLP[:24]
print(" d  |B_d|  3を含む?   j=1        j=2        j=3      予測(sqrt3/2)^|B|")
for d in (1,2,3,4):
    B = [a for a in A if a > 2*d]
    tot = 2.0**len(B)
    r1 = abs(F(B,1))/tot; r2 = abs(F(B,2))/tot; r3 = abs(F(B,3))/tot
    pred = (math.sqrt(3)/2)**len(B)
    print(f" {d}   {len(B):3d}   {'yes' if 3 in B else 'no ':>3}    "
          f"{r1:.3e}  {r2:.3e}  {r3:.3e}   {pred:.3e}")

print()
print("=== |B_d| に対する減衰(d=2 固定、k を動かす)===")
print("  k  |B_2|   |F(zeta6)|/2^|B|      (sqrt3/2)^|B_2|      比")
for k in range(14, 25, 2):
    A = ALLP[:k]
    B = [a for a in A if a > 4]
    tot = 2.0**len(B)
    got = abs(F(B,1))/tot
    pred = (math.sqrt(3)/2)**len(B)
    print(f" {k:3d}  {len(B):4d}    {got:.6e}    {pred:.6e}    {got/pred:.6f}")
