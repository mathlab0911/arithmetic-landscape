# floor_r15.py — mod-4 床を「厳密に証明できる形」に固めて数値確認する。
#
# 主張(集約版・完全に初等):
#   B を奇数の有限列、b=|B|、r_B(m) を表現数とする。R_c = sum_{m = c mod 4} r_B(m) と置く。
#   F_B(z)=prod(1+z^a) を z=i で評価すると、奇数 a は a=1 or 3 mod 4 で
#     1+i^1 = 1+i,  1+i^3 = 1-i   いずれも絶対値 sqrt2
#   ⇒ |F_B(i)| = 2^{b/2}(剰余分布に依らず厳密、決してゼロにならない)
#   また F_B(-1) = 0(奇数だから)。よって
#     R_c = (1/4)[2^b + 2 Re(i^{-c} F_B(i))]
#   F_B(i) = 2^{b/2} e^{i phi} と書くと Re(i^{-c}F) は {±cos phi, ±sin phi} を走るので
#     max_c R_c - min_c R_c = 2^{b/2} * max(|cos phi|,|sin phi|) >= 2^{(b-1)/2}
#   平均は 2^{b-2} なので
#     (max-min)/平均 >= 2*sqrt2 * 2^{-b/2}
#   ⇒ どんな奇数列でも、mod 4 の表現数分布は 2^{-b/2} 以上ずれる(超えられない床)。
import math, cmath, random

def rep_counts(B):
    tot=sum(B); r=[0]*(tot+1); r[0]=1
    for a in B:
        for m in range(tot,a-1,-1): r[m]+=r[m-a]
    return r

def check(B):
    b=len(B); r=rep_counts(B)
    R=[0,0,0,0]
    for m,v in enumerate(r): R[m%4]+=v
    F=1+0j
    for a in B: F*=(1+1j**a)
    phi=cmath.phase(F)
    pred_spread=2.0**(b/2)*max(abs(math.cos(phi)),abs(math.sin(phi)))
    return R, abs(F), 2.0**(b/2), max(R)-min(R), pred_spread, b

print("="*88)
print("mod-4 床の厳密性チェック: |F_B(i)| = 2^(b/2) と max_c R_c - min_c R_c の予言")
print("="*88)
print("  列                          b   |F(i)|      2^(b/2)     一致  実測spread   予言spread  一致")
tests = [
    ("3,5,7,11",            [3,5,7,11]),
    ("奇素数 10 個",         [3,5,7,11,13,17,19,23,29,31]),
    ("奇素数 16 個",         [3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59]),
    ("1,3,5,...,29 (奇数)",  list(range(1,30,2))),
    ("全部 1 mod 4",         [1,5,9,13,17,21,25,29]),
    ("全部 3 mod 4",         [3,7,11,15,19,23,27,31]),
]
rng=random.Random(7)
tests.append(("ランダム奇数 14 個", sorted(rng.sample([x for x in range(1,80,2)],14))))
for name,B in tests:
    R,aF,pred,spread,pspread,b = check(B)
    ok1 = "OK" if abs(aF-pred)<1e-6*pred else "NG"
    ok2 = "OK" if abs(spread-pspread)<1e-6*max(1,pspread) else "NG"
    print(f" {name:<24} {b:3d} {aF:11.4f} {pred:11.4f}   {ok1}  {spread:11.1f} {pspread:11.1f}   {ok2}")

print()
print("  相対スプレッド (max-min)/平均 と、下界 2*sqrt2*2^(-b/2) の比較:")
print("  列                          b   実測相対      下界 2√2·2^(-b/2)   実測/下界")
for name,B in tests:
    R,aF,pred,spread,pspread,b = check(B)
    rel=spread/(2.0**b/4)
    lb=2*math.sqrt(2)*2.0**(-b/2)
    print(f" {name:<24} {b:3d} {rel:12.6e} {lb:16.6e}  {rel/lb:8.4f}")
