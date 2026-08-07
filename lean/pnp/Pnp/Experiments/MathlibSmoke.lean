import Mathlib.Tactic

theorem mlib_smoke1 : (2 : Rat) + 2 = 4 := by norm_num
theorem mlib_smoke2 (x : Real) (h : 0 < x) : 0 < 2 * x := by linarith
#print axioms mlib_smoke2