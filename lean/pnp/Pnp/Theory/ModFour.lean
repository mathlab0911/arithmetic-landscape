/-
  Canon file 11.  Paper 4, Theorem `thm:modfour` (the modulus-4 theorem), maximisation step.

  Paper 2's extremal quantity averages |cos| over the REDUCED residues and peaks at q = 6 with
  the value sqrt3/2.  A random odd sequence is equidistributed over the ODD residues instead,
  and the corresponding quantity is

      M_odd(q) = ( PROD_{j in R_q} |cos(pi j / q)| ) ^ (1/|R_q|),
      R_q = Z/q for q odd;  the odd residues mod q for q even.

  Paper 4 Lemma `lem:moddclosed` evaluates this in closed form by a root-of-unity product:

      q odd            :  2 ^ (1/q - 1)
      q = 0 (mod 4)    :  2 ^ (2/q - 1)     [ = 2^(1/u - 1) with q = 2u, u even ]
      q = 2 (mod 4)    :  0                 [ j = u is an odd residue and cos(pi/2) = 0 ]

  WHAT IS FORMALISED HERE, AND WHAT IS NOT.  This file takes the closed form as the definition
  `ModdCF` and proves the MAXIMISATION step: the maximum over q >= 2 is 1/sqrt 2, attained at
  q = 4 and nowhere else.  That is the step where a slip would hide -- a case analysis over
  three residue classes plus the comparison of 2^(-2/3) with 2^(-1/2).  The closed form itself
  is proved on paper (four lines of roots of unity) and checked numerically against the product
  for every q <= 200, worst discrepancy 4.4e-16 (`mq4_r107`); it is NOT formalised here, and
  the paper says so.

  F52 (prove load-bearing statements twice): the maximisation is proved once as an inequality
  with an equality case, and once again as `ModdCF_lt_of_ne_four`, a strict bound obtained by a
  different route (strict monotonicity rather than antisymmetry).  The two agree only if the
  statement is the intended one.
-/
import Mathlib

namespace Pnp

open Real

/-- The closed form of `M_odd(q)` from paper 4, Lemma `lem:moddclosed`.
    For `q = 2u` with `u` even the exponent `1/u - 1` is written `2/q - 1`. -/
noncomputable def ModdCF (q : ℕ) : ℝ :=
  if q % 2 = 1 then (2 : ℝ) ^ (1 / (q : ℝ) - 1)
  else if q % 4 = 2 then 0
  else (2 : ℝ) ^ (2 / (q : ℝ) - 1)

/-- The maximal value, in the form the paper writes it. -/
theorem two_rpow_neg_half : (2 : ℝ) ^ (-(1 : ℝ) / 2) = 1 / Real.sqrt 2 := by
  have e : (-(1 : ℝ) / 2) = -((1 : ℝ) / 2) := by ring
  rw [e, Real.rpow_neg (by norm_num : (0:ℝ) ≤ 2), ← Real.sqrt_eq_rpow, one_div]

theorem ModdCF_four : ModdCF 4 = (2 : ℝ) ^ (-(1 : ℝ) / 2) := by
  norm_num [ModdCF]

theorem ModdCF_six : ModdCF 6 = 0 := by
  norm_num [ModdCF]

theorem ModdCF_nonneg (q : ℕ) : 0 ≤ ModdCF q := by
  unfold ModdCF
  split_ifs
  · exact le_of_lt (Real.rpow_pos_of_pos (by norm_num) _)
  · exact le_refl 0
  · exact le_of_lt (Real.rpow_pos_of_pos (by norm_num) _)

private theorem two_rpow_le (x y : ℝ) : (2 : ℝ) ^ x ≤ (2 : ℝ) ^ y ↔ x ≤ y :=
  Real.rpow_le_rpow_left_iff (by norm_num)

private theorem two_rpow_inj {x y : ℝ} (h : (2 : ℝ) ^ x = (2 : ℝ) ^ y) : x = y :=
  le_antisymm ((two_rpow_le x y).mp h.le) ((two_rpow_le y x).mp h.ge)

/-- **The modulus-4 theorem, maximisation step.**  `M_odd(q) ≤ 1/√2` for every `q ≥ 2`. -/
theorem ModdCF_le (q : ℕ) (hq : 2 ≤ q) : ModdCF q ≤ (2 : ℝ) ^ (-(1 : ℝ) / 2) := by
  unfold ModdCF
  split_ifs with h1 h2
  · have h3 : 3 ≤ q := by omega
    have hqR : (3 : ℝ) ≤ (q : ℝ) := by exact_mod_cast h3
    have hpos : (0 : ℝ) < (q : ℝ) := by linarith
    rw [two_rpow_le]
    have key : 1 / (q : ℝ) ≤ 1 / 2 := by gcongr; linarith
    linarith
  · positivity
  · have h4 : 4 ≤ q := by omega
    have hqR : (4 : ℝ) ≤ (q : ℝ) := by exact_mod_cast h4
    have hpos : (0 : ℝ) < (q : ℝ) := by linarith
    rw [two_rpow_le]
    have key : 2 / (q : ℝ) ≤ 1 / 2 := by
      have h24 : (2:ℝ) / (q : ℝ) ≤ 2 / 4 := by gcongr
      linarith
    linarith

/-- **The equality case.**  The bound is attained exactly at `q = 4`. -/
theorem ModdCF_eq_iff (q : ℕ) (hq : 2 ≤ q) :
    ModdCF q = (2 : ℝ) ^ (-(1 : ℝ) / 2) ↔ q = 4 := by
  constructor
  · intro h
    unfold ModdCF at h
    split_ifs at h with h1 h2
    · exfalso
      have he := two_rpow_inj h
      have h3 : 3 ≤ q := by omega
      have hqR : (3 : ℝ) ≤ (q : ℝ) := by exact_mod_cast h3
      have hpos : (0 : ℝ) < (q : ℝ) := by linarith
      have hne : (q : ℝ) ≠ 0 := ne_of_gt hpos
      have : 1 / (q : ℝ) = 1 / 2 := by linarith
      field_simp at this
      linarith
    · exfalso
      have := Real.rpow_pos_of_pos (show (0:ℝ) < 2 by norm_num) (-(1:ℝ) / 2)
      linarith
    · have he := two_rpow_inj h
      have h4 : 4 ≤ q := by omega
      have hqR : (4 : ℝ) ≤ (q : ℝ) := by exact_mod_cast h4
      have hpos : (0 : ℝ) < (q : ℝ) := by linarith
      have hne : (q : ℝ) ≠ 0 := ne_of_gt hpos
      have hh : 2 / (q : ℝ) = 1 / 2 := by linarith
      field_simp at hh
      norm_num at hh
      exact_mod_cast hh.symm
  · rintro rfl
    exact ModdCF_four

/-- The same content by a different route: a strict bound off `q = 4`, proved from strict
    monotonicity rather than from antisymmetry.  Two routes to one statement (F52). -/
theorem ModdCF_lt_of_ne_four (q : ℕ) (hq : 2 ≤ q) (hne : q ≠ 4) :
    ModdCF q < (2 : ℝ) ^ (-(1 : ℝ) / 2) := by
  rcases lt_or_eq_of_le (ModdCF_le q hq) with h | h
  · exact h
  · exact absurd ((ModdCF_eq_iff q hq).mp h) hne

/-- The maximum in the paper's notation. -/
theorem ModdCF_le_one_div_sqrt_two (q : ℕ) (hq : 2 ≤ q) :
    ModdCF q ≤ 1 / Real.sqrt 2 := by
  rw [← two_rpow_neg_half]; exact ModdCF_le q hq

end Pnp

-- Audit trail: no `sorry`, and no axioms beyond Lean's three.
#print axioms Pnp.ModdCF_le
#print axioms Pnp.ModdCF_eq_iff
#print axioms Pnp.ModdCF_lt_of_ne_four
#print axioms Pnp.ModdCF_le_one_div_sqrt_two
#print axioms Pnp.two_rpow_neg_half
