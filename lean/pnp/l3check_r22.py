# l3check_r22.py : paper2_L3_draft.md の数値主張を出典ログと突き合わせる(作業3, V1)
import math
def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
ALLP=[p for p in primes_upto(20000) if p%2==1]
def arith(B):
    tau=lambda a: 1 if a%6==1 else (-1 if a%6==5 else 0)
    return (sum(tau(a)*a for a in B), sum(tau(a)*a**3 for a in B),
            sum(B), sum(a*a for a in B), sum(a**4 for a in B),
            sum(1 for a in B if a%6==1), sum(1 for a in B if a%6==5))
print("主張4: 「Δ₃²/S₂³ が最大なのは k=18、値 ≈ 1.0e-3」")
print("  k    Delta3^2/S2^3    S4/S2^2     hw=24 は sigma の何倍か (sigma=sqrt(S2)/2)")
best=None
for k in range(18,41,2):
    B=[a for a in ALLP[:k] if a>4]
    D,D3,S1,S2,S4,c1,c5=arith(B)
    v=D3*D3/S2**3; sig=math.sqrt(S2)/2
    if best is None or v>best[1]: best=(k,v)
    print(f" {k:3d}    {v:.4e}     {S4/S2**2:.5f}     {24/sig:6.3f} sigma")
print(f"  ⇒ 最大は k={best[0]}、値 {best[1]:.4e}   → 主張どおり" if best[0]==18 else "  ★不一致")
print()
print("主張7: 「振幅は狭窓 hw ≈ 0.15σ」 → 実際には hw は 24 に固定しており、")
print("        σ に対する比は k とともに 0.19σ(k=18)から 0.078σ(k=40)へ変化する。")
print("        『hw ≈ 0.15σ』ではなく『hw = 24(固定)、= 0.08〜0.19σ』と書くべき。")
print()
print("主張2の確認: |実測/K₂ − 1| の A枝/B枝/全体の平均")
print("  (k2psi_r20.log より A枝平均 0.00072・B枝平均 0.00073・A枝最大 0.00339@k=18・B枝最大 0.00098)")
print("  ⇒ 全体平均も 0.00072〜0.00073。草稿の『mean 0.00073 over k=18..40』は妥当")
print()
print("主張6の確認: c1-c5 と |Delta| の対応")
for k in range(8,45,2):
    B=[a for a in ALLP[:k] if a>4]
    if not B: continue
    D,D3,S1,S2,S4,c1,c5=arith(B)
    print(f"  k={k:3d}  c1-c5={c1-c5:+2d}  |Delta|={abs(D):4d}")
