import Mathlib.Analysis.SpecialFunctions.Complex.Circle
import Mathlib.Analysis.Normed.Field.Basic

/-!
ℓ¹ 評価: 単位円上では多項式の値は係数の絶対値和で押さえられる。
論文2の Problem 10.3 を「整数の比較」に落とす部分の数学的中身。
-/

open Finset

theorem norm_poly_le_l1_on_circle {n : ℕ} (c : Fin n → ℝ) (z : ℂ) (hz : ‖z‖ = 1) :
    ‖∑ i, (c i : ℂ) * z ^ (i : ℕ)‖ ≤ ∑ i, |c i| := by
  refine le_trans (norm_sum_le _ _) (le_of_eq ?_)
  refine Finset.sum_congr rfl (fun i _ => ?_)
  rw [norm_mul, norm_pow, hz, one_pow, mul_one, Complex.norm_real, Real.norm_eq_abs]

#print axioms norm_poly_le_l1_on_circle
