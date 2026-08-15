# step24_r70.py (2026-08-09, opus-5 70周目)
# §8 Step 2/4 の書き切りに先立つ【指数収支の検算】。V4: 目標の指数を先に紙で決め、それを数値で確かめる。
#  (1) Dirichlet 核の一様上界   |D_M(v)| = |Σ_{n≤M} cos 2πnv| ≤ 1/(4‖v‖) + 1/2
#  (2) 裾の Abel 評価           |Σ_{n>N0} cos(2πnv)/n| ≤ (1/(2‖v‖)+1)/N0
#  (3) 級数の符号の整合         log|2cos πu| = −Σ_{n≥1} cos(2πnv)/n,  v = u − 1/2
#  (4) 指数収支表を N ごとに数値化
import math, random
def frac_dist(v):           # ‖v‖ = 最寄りの整数までの距離
    return abs(v - round(v))
print("="*100); print("(1) Dirichlet 核 |D_M(v)| ≤ 1/(4‖v‖) + 1/2 —— 一様に成り立つか")
print("="*100)
worst=0.0; worstinfo=None
random.seed(11)
for _ in range(200000):
    v=random.uniform(-0.5,0.5); M=random.randint(1,400)
    nv=frac_dist(v)
    if nv<1e-6: continue
    D=sum(math.cos(2*math.pi*n*v) for n in range(1,M+1))
    K=1/(4*nv)+0.5
    r=abs(D)/K
    if r>worst: worst,worstinfo=r,(v,M,D,K)
print(f"   max |D_M|/K = {worst:.6f}   {'≤ 1 ✓ 成立' if worst<=1 else '★ 破れ'}")
print(f"   最悪点: v={worstinfo[0]:.5f}, M={worstinfo[1]}, D={worstinfo[2]:.4f}, K={worstinfo[3]:.4f}")
print()
print("="*100); print("(2) 裾 |Σ_{n>N0} cos(2πnv)/n| ≤ (1/(2‖v‖)+1)/N0  —— Abel 評価の妥当性")
print("="*100)
worst=0.0; wi=None
for N0 in (10,50,200):
    for _ in range(4000):
        v=random.uniform(-0.5,0.5); nv=frac_dist(v)
        if nv<1e-4: continue
        # 裾を十分先まで数値和(交代しないので大きめに取る)
        T=sum(math.cos(2*math.pi*n*v)/n for n in range(N0+1,N0+200001))
        B=(1/(2*nv)+1)/N0
        r=abs(T)/B
        if r>worst: worst,wi=r,(N0,v,T,B)
print(f"   max |tail|/bound = {worst:.6f}   {'≤ 1 ✓ 成立' if worst<=1 else '★ 破れ'}")
print(f"   最悪点: N0={wi[0]}, v={wi[1]:.5f}, tail={wi[2]:.5f}, bound={wi[3]:.5f}")
print()
print("="*100); print("(3) 符号の整合  log|2cos πu| =? −Σ_{n≥1} cos(2πnv)/n  (v=u−1/2)")
print("="*100)
for u in (0.10,0.23,0.37,0.44):
    v=u-0.5
    lhs=math.log(abs(2*math.cos(math.pi*u)))
    rhs=-sum(math.cos(2*math.pi*n*v)/n for n in range(1,400001))
    print(f"   u={u:.2f}:  lhs={lhs:+.6f}   rhs={rhs:+.6f}   差={lhs-rhs:+.2e}")
print()
print("="*100); print("(4) 指数収支表 (A=11, A'=12, δ₀=1/log b, N₀=(log N)^{A'}, b≍N/log N)")
print("="*100)
A,Ap=11,12
print("     N        b≈N/logN     S2b/b            |B_bad|/b      S4c/b(loglogN·|Bbad|/b)   合計/b")
for N in (10**6,10**12,10**24,10**60,10**200):
    L=math.log(N); LL=math.log(L); b=N/L; N0=L**Ap; d0=1/math.log(b)
    s2b = (L**(4-A/2))*LL                      # H(θ)/b
    bad = 4*d0 + 4*L**(-Ap) + (4/math.pi)*s2b  # |B_bad|/b
    s4a = 1/(2*N0*d0) + 1/N0                   # 各点の裾
    s4c = (Ap*LL+1)*bad                        # 悪い点が head に混ざる分 /b
    s4d = bad*math.log(2)
    tot = s4c + s2b + s4a + s4d
    print(f"   1e{int(math.log10(N)):>3d}  {b:9.3e}   {s2b:.4e}      {bad:.4e}      {s4c:.4e}            {tot:.4e}")
print()
print("  ⇒ 支配項は S4c = (log N₀)·|B_bad| ≍ 4A′·b·loglogN/logN。指数和ではなく【悪い点の head】が律速。")
print("  ⇒ 合計 = O(b·loglog N/log N) = o(b)。よって log|G_B| ≤ −b log2 + O(b loglogN/logN)。")
print()
print("  (参考) δ₀ は最適化していない。bδ₀·loglogN + b/(N₀δ₀) を釣り合わせると δ₀≍(N₀loglogN)^{-1/2}:")
for N in (10**12,10**24):
    L=math.log(N); LL=math.log(L); N0=L**Ap
    d_opt=1/math.sqrt(N0*LL)
    print(f"     N=1e{int(math.log10(N))}: 現行 δ₀={1/math.log(N/L):.4e} → 誤差 {(Ap*LL)*4/math.log(N/L):.3e}"
          f" / 最適 δ₀={d_opt:.4e} → 誤差 {2*math.sqrt(LL/N0)*Ap:.3e}")
