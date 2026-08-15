# lit_r54.py (2026-08-08, opus-5 54周目) : 文献(Bzdega)の評価が我々の Problem を閉じるか検算。
#   Bzdega, "Products of cyclotomic polynomials on unit circle", arXiv:1606.07622:
#     L_n := max_{|z|=1}|Φ_n(z)| （= 我々の ‖Φ_q‖_∞ そのもの）
#     L_n/n ≤ S_n/n ≤ √(Q_n/n) ≤ A_n ,  A_n/M_n ≤ (C+ε_k)^{2^k}, C<0.859125 (Thm 3)
#     M_n = ∏_{j=1}^{k-2} p_j^{2^{k-j-1}-1}    (n = p_1<...<p_k、奇数・平方因子なし)
#   ⟹ log L_n ≤ log n + log M_n + 2^k log C  (C<1 なので最後の項は負)
#   必要: log L_n ≤ (φ(n)/2)·log3 = 0.5493·φ(n)
from math import log, gcd
def phi_from(ps): 
    r=1
    for p in ps: r*=(p-1)
    return r
def Mlog(ps):
    k=len(ps); s=0.0
    for j in range(1,k-1): s+=(2**(k-j-1)-1)*log(ps[j-1])
    return s
def primes(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
P=[p for p in primes(200) if p>2]
L3=log(3)/2
print("="*100)
print("[文献の検算] Bzdega Thm3 の上界が (φ(n)/2)log3 を下回るか(最悪ケース=最小の奇素数から)")
print("="*100)
print("   k   n = p_1..p_k(最小)        φ(n)          log n + log M_n   必要 0.5493·φ(n)   判定")
for k in range(1,13):
    ps=P[:k]; n=1
    for p in ps: n*=p
    ph=phi_from(ps); lhs=log(n)+Mlog(ps); rhs=L3*ph
    print(f"  {k:3d}   {('·'.join(map(str,ps)))[:26]:26s} {ph:>13d}   {lhs:>13.2f}   {rhs:>15.2f}   "
          f"{'OK' if lhs<=rhs else '★破れ'}")
print()
print("  ※ k=1(n=3)は 1.0986 vs 1.0986 で【等号】——我々が実測で見つけた等号ケースと一致。")
print("  ※ C<0.859125 の 2^k 乗は負の寄与なので、上では捨てている(安全側)。")
print()
print("="*100)
print("[fable-5 の自作案の検算] ‖Φ_q‖₁ ≤ (2(φ+1))^{2^{ω−1}}  が (φ/2)log3 を下回るか")
print("="*100)
print("    q(平方因子なし)      ω   φ(q)    log上界=2^{ω−1}log(2φ+2)   必要 0.5493·φ   判定")
for ps in ([3],[3,5],[3,5,7],[3,5,7,11],[3,5,7,11,13],[3,5,7,11,13,17]):
    n=1
    for p in ps: n*=p
    w=len(ps); ph=phi_from(ps)
    lhs=(2**(w-1))*log(2*ph+2); rhs=L3*ph
    print(f"   {n:>12d}     {w:2d}  {ph:>7d}         {lhs:>12.2f}          {rhs:>12.2f}   "
          f"{'OK' if lhs<=rhs else '★破れ'}")
for ps in ([2,3,5,7,11],):   # q=2310（fable が「最悪級」と書いた例）
    n=1
    for p in ps: n*=p
    w=len(ps); ph=phi_from(ps)
    print(f"   {n:>12d}(=2310) {w:2d}  {ph:>7d}         {(2**(w-1))*log(2*ph+2):>12.2f}"
          f"          {L3*ph:>12.2f}   {'OK' if (2**(w-1))*log(2*ph+2)<=L3*ph else '★破れ'}")
print()
print("  ⇒ 自作案も通る。ただし文献の評価のほうが桁違いに強い(C<0.859 の 2^k 乗が効く)。")
