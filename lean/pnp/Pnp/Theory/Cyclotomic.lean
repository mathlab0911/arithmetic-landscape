import Mathlib.Analysis.SpecialFunctions.Complex.Circle
import Mathlib.Analysis.Normed.Field.Basic

/-!
# 単位円上の ℓ¹ 評価

論文2の Problem 10.3 を「整数の比較」に落とす部分の数学的中身。

`lem:supnorm` により、環状領域の評価は `‖Φ_q‖_∞ ≤ 3^{φ(q)/2}` に帰着する。
本ファイルの補題により `‖Φ_q‖_∞ ≤ ‖Φ_q‖₁ = Σ|係数|` なので、
φ(q) が偶数(q ≥ 3)であることと合わせて、検証は【整数どうしの比較】になる。
-/

open Finset

/-- 単位円上では、多項式の値の絶対値は係数の絶対値和を超えない。 -/
theorem norm_poly_le_l1_on_circle {n : ℕ} (c : Fin n → ℝ) (z : ℂ) (hz : ‖z‖ = 1) :
    ‖∑ i, (c i : ℂ) * z ^ (i : ℕ)‖ ≤ ∑ i, |c i| := by
  refine le_trans (norm_sum_le _ _) (le_of_eq ?_)
  refine Finset.sum_congr rfl (fun i _ => ?_)
  rw [norm_mul, norm_pow, hz, one_pow, mul_one, Complex.norm_real, Real.norm_eq_abs]

/-- 系: 係数の絶対値和が `M` 以下なら、単位円上の値も `M` 以下。 -/
theorem norm_poly_le_of_l1_le {n : ℕ} (c : Fin n → ℝ) (M : ℝ)
    (hM : ∑ i, |c i| ≤ M) (z : ℂ) (hz : ‖z‖ = 1) :
    ‖∑ i, (c i : ℂ) * z ^ (i : ℕ)‖ ≤ M :=
  le_trans (norm_poly_le_l1_on_circle c z hz) hM

#print axioms norm_poly_le_l1_on_circle
#print axioms norm_poly_le_of_l1_le
