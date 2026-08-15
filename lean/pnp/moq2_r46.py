# moq2_r46.py (2026-08-08, opus-5) : MathOverflow に出す不等式の最終形と数値の裏取り。
#  sin3u/sinu = 3 - 4sin²u = 1 + 2cos 2u  なので、v=2u と置くと問題は
#     F(Y) := (1/Y)∫_0^Y log|1 + 2cos v| dv  ≤  log 3     (∀Y>0)
#  となる。1+2cos v = |1+z+z²| (z=e^{iv}) で Mahler 測度 1 ⟹ 円全体の平均は 0。
import numpy as np, math
print("="*100)
print("[最終形の確認] sin3u/sinu = 1 + 2cos 2u")
for u in (0.31,0.87,1.55,2.4):
    print(f"   u={u:.2f}:  sin3u/sinu = {math.sin(3*u)/math.sin(u):+.10f}   "
          f"1+2cos2u = {1+2*math.cos(2*u):+.10f}")
print()
print("="*100)
print("F(Y) = (1/Y)∫_0^Y log|1+2cos v| dv  を高精度で。log 3 = %.10f" % math.log(3))
print("="*100)
V=400.0; m=40_000_000
v=np.linspace(0.0,V,m+1)
f=np.log(np.abs(1+2*np.cos(v))+1e-320)
dv=v[1]-v[0]
cum=np.concatenate([[0.0],np.cumsum((f[1:]+f[:-1])/2*dv)])
Y=v[1:]; F=cum[1:]/Y
l3=math.log(3)
print(f"   sup_{{Y>0}} F(Y)          = {F.max():.10f}   (log 3 = {l3:.10f})")
print(f"   sup - log 3             = {F.max()-l3:+.3e}   ← 0 以下なら主張成立")
print(f"   argmax Y                = {Y[int(np.argmax(F))]:.6f}   (Y→0 で log 3 に収束するはず)")
for Y0 in (0.5,1.0,2.0,5.0):
    sel=Y>=Y0
    print(f"   sup_{{Y≥{Y0:>3}}} F(Y)        = {F[sel].max():.10f}    (log 3 との差 {F[sel].max()-l3:+.6f})")
print()
print("   Y の代表点での値:")
for Y0 in (0.01,0.1,0.5,1.0,2.0,2.4,3.0,6.0,12.0,50.0,200.0):
    i=int(Y0/dv)
    print(f"     Y={Y0:7.2f}   F(Y)={F[i-1]:+.8f}   (log3 - F = {l3-F[i-1]:+.8f})")
print()
print("   単調か: F の符号変化の回数(Y>0.01)…", int(np.sum(np.diff(np.sign(np.diff(F[1000::20000])))!=0)),
      "回の増減の切替 ⟹ 単調ではなく振動しながら 0 へ")
print()
print("="*100)
print("[一般形] (1/Y)∫_0^Y log|Φ_q(-e^{-iv})| dv ≤ log|Φ_q(-1)| は Φ_q(-1)=±1 のとき偽")
print("  (Jensen: 円全体の平均 = log(Mahler測度) = 0。出発点も 0 なら必ずどこかで正)")
print("  ⟹ MO では『Φ_q(-1)≠±1 のとき』を条件に付けるのが正しい。q=6 が最も厳しい。")
