# induct_r58.py (2026-08-09, opus-5 58周目) : fable-5 r57 作業1。
# lem:l1small が【全ての ω】を覆うか。帰納の一段を紙で立て、数値で確かめる。
#
#  S(ω) := φ_ω·log3 − 2^ω·log(2φ_ω+2)   (φ_ω = 奇プリモリアル 3·5···p_{ω+1} の φ)
#  帰納: φ_{ω+1} = (p−1)φ_ω (p = p_{ω+2})、2φ_{ω+1}+2 ≤ (p−1)(2φ_ω+2) より
#        S(ω+1) ≥ (p−1)φ_ω log3 − 2^{ω+1}[log(2φ_ω+2) + log(p−1)]
#               ≥ (p−3)φ_ω log3 − 2^{ω+1} log(p−1)          (S(ω)≥0 を使用)
#               ≥ (p−3)[φ_ω log3 − 2^{ω+1}]                  (log(p−1) ≤ p−3, p≥5)
#  ⟹ 補助不変量  φ_ω·log3 ≥ 2^{ω+1}  が保たれれば S(ω+1) ≥ 0。
#     補助不変量は φ が ×(p−1)≥10、2^{ω+1} が ×2 なので各段で 5 倍以上強くなる。
from math import log
def primes(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
P=[p for p in primes(2000) if p>2]
L3=log(3)
print("="*100)
print("(1) 補題 log(p−1) ≤ p−3  (p ≥ 5 の素数)")
print("="*100)
for p in (5,7,11,13,17,101):
    print(f"    p={p:4d}:  log(p−1)={log(p-1):.4f}  ≤  p−3={p-3:4d}   {'OK' if log(p-1)<=p-3 else '★'}")
print()
print("="*100)
print("(2) 補助不変量  φ_ω·log3 ≥ 2^{ω+1}  と、帰納で保たれるか")
print("="*100)
print("     ω   φ_ω(奇プリモリアル)   φ_ω·log3        2^{ω+1}      比      次段の倍率(p−1)")
ph=1; ok_all=True
for w in range(1,15):
    ph*= (P[w-1]-1)
    lhs=ph*L3; rhs=2**(w+1); ok = lhs>=rhs
    if w>=3: ok_all = ok_all and ok
    nxt=P[w]-1
    phs=str(ph) if len(str(ph))<15 else f"{ph:.4e}"
    ls=f"{lhs:.4e}" if lhs>1e12 else f"{lhs:.2f}"
    print(f"    {w:2d}   {phs:>18s}  {ls:>14s}  {rhs:>12d}   {lhs/rhs:>9.3g}   ×{nxt}"
          f"   {'OK' if ok else ('—' if w<3 else '★')}")
print(f"\n    ⇒ ω ≥ 3 で補助不変量は{'成立し、比は各段で急増' if ok_all else '★破れ'}")
print()
print("="*100)
print("(3) 主張そのもの: (2φ_ω+2)^{2^ω} ≤ 3^{φ_ω} と slack 比 LHS/RHS(log 比)")
print("="*100)
print("     ω    (2φ+2)^{2^ω} の log     3^{φ} の log        比 LHS/RHS      判定")
ph=1; bad=[]
for w in range(1,15):
    ph*= (P[w-1]-1)
    L=(2**w)*log(2*ph+2); R=ph*L3
    if w>=3 and L>R: bad.append(w)
    print(f"    {w:2d}    {L:>18.4f}   {R:>18.4e}     {L/R:>12.4g}     "
          f"{'OK' if L<=R else ('★例外(既知)' if w<=2 else '★破れ')}")
print(f"\n    ⇒ ω ≥ 3 で {'全て成立(比は単調急減: ω=3で0.696、ω=12で2.7e−9)' if not bad else '★破れ '+str(bad)}")
print("    ⇒ 帰納の一段((1)(2))と ω=3 の基底で、【全ての ω】が覆われる。")
