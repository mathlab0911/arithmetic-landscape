/-
  Canon file 12.  Paper 4, section 4: the two arithmetic facts that separate the primes from a
  random odd sequence.

  Section 4's headline -- "the primes are the harder case" -- rests on exactly two statements
  about the peak heights of PROD_{a in A} |cos(pi a / q)|:

    (1) THE MODULUS-4 FLOOR IS DETERMINISTIC.  |cos(pi a / 4)| = 1/sqrt 2 for EVERY odd a,
        so the product is (1/sqrt 2)^|A| for every odd sequence, with no arithmetic input at
        all.  It is a floor because it never vanishes, and it is universal because it does not
        depend on which odd numbers A contains.

    (2) THE MODULUS-6 PEAK DIES ON ONE ELEMENT.  If A contains a single a = 3 (mod 6) then
        cos(pi a / 6) = 0 and the whole product vanishes.  A set of primes contains exactly
        one such element, namely 3, and it leaves the layer B_d as soon as d >= 2; a random
        odd sequence contains about a third of them at every d.

  Put together: the primes keep the modulus-6 peak sqrt3/2 and a random odd sequence does not,
  so the random case converges at the strictly better rate 1/sqrt 2 -- which, by
  `ModFour.lean`, nothing else can beat.

  WHAT IS NOT HERE.  The general closed form of M_odd(q) for all q (two root-of-unity
  evaluations) is proved on paper and checked numerically for q <= 200; Mathlib has no
  off-the-shelf product over roots of unity, so formalising it is a separate job.  What is
  formalised here is the pair of special cases the paper's argument actually uses.
-/
import Mathlib

namespace Pnp

open Real

/-- **The modulus-4 floor, one element.**  For every odd `a`, `|cos(π a / 4)| = 1/√2`.
    No arithmetic beyond the parity of `a` enters. -/
theorem abs_cos_pi_mul_div_four (a : ℕ) (ha : a % 2 = 1) :
    |Real.cos (π * a / 4)| = 1 / Real.sqrt 2 := by
  have h2 : Real.sqrt 2 / 2 = 1 / Real.sqrt 2 := by
    rw [eq_div_iff (by positivity), div_mul_eq_mul_div, Real.mul_self_sqrt (by norm_num)]
    norm_num
  -- reduce `a` modulo 8; `cos (π a / 4)` has period 8 in `a`
  obtain ⟨t, r, hr, rfl⟩ : ∃ t r, r < 8 ∧ a = 8 * t + r :=
    ⟨a / 8, a % 8, Nat.mod_lt _ (by norm_num), by omega⟩
  have hx : π * ((8 * t + r : ℕ) : ℝ) / 4 = π * (r : ℝ) / 4 + (t : ℤ) * (2 * π) := by
    push_cast; ring
  rw [hx, Real.cos_add_int_mul_two_pi]
  -- `a` odd forces `r` odd, so only four residues survive
  have hrodd : r = 1 ∨ r = 3 ∨ r = 5 ∨ r = 7 := by omega
  rcases hrodd with rfl | rfl | rfl | rfl
  · -- r = 1
    rw [show π * ((1 : ℕ) : ℝ) / 4 = π / 4 by push_cast; ring, Real.cos_pi_div_four,
      abs_of_nonneg (by positivity), h2]
  · -- r = 3
    rw [show π * ((3 : ℕ) : ℝ) / 4 = π - π / 4 by push_cast; ring, Real.cos_pi_sub,
      Real.cos_pi_div_four, abs_neg, abs_of_nonneg (by positivity), h2]
  · -- r = 5:  5π/4 = -(π - π/4) + 2π,  so reuse the two lemmas already used above
    rw [show π * ((5 : ℕ) : ℝ) / 4 = -(π - π / 4) + (1 : ℤ) * (2 * π) by push_cast; ring]
    rw [Real.cos_add_int_mul_two_pi, Real.cos_neg, Real.cos_pi_sub, Real.cos_pi_div_four,
      abs_neg, abs_of_nonneg (by positivity), h2]
  · -- r = 7
    rw [show π * ((7 : ℕ) : ℝ) / 4 = 2 * π - π / 4 by push_cast; ring]
    rw [show (2 : ℝ) * π - π / 4 = -(π / 4) + (1 : ℤ) * (2 * π) by push_cast; ring]
    rw [Real.cos_add_int_mul_two_pi, Real.cos_neg, Real.cos_pi_div_four,
      abs_of_nonneg (by positivity), h2]

/-- **The modulus-4 floor, whole sequence.**  For an odd sequence the product is
    `(1/√2)^{|A|}` exactly: deterministic, and in particular never zero. -/
theorem prod_abs_cos_four (A : Finset ℕ) (hA : ∀ a ∈ A, a % 2 = 1) :
    ∏ a ∈ A, |Real.cos (π * a / 4)| = (1 / Real.sqrt 2) ^ A.card := by
  rw [Finset.prod_congr rfl (fun a ha => abs_cos_pi_mul_div_four a (hA a ha)),
    Finset.prod_const]

/-- **The modulus-6 peak dies on one element.**  If `a ≡ 3 (mod 6)` then `cos(π a / 6) = 0`. -/
theorem cos_pi_mul_div_six_eq_zero (a : ℕ) (ha : a % 6 = 3) :
    Real.cos (π * a / 6) = 0 := by
  obtain ⟨m, rfl⟩ : ∃ m, a = 6 * m + 3 := ⟨a / 6, by omega⟩
  rw [Real.cos_eq_zero_iff]
  refine ⟨(m : ℤ), ?_⟩
  push_cast
  ring

/-- **The modulus-6 peak dies on the whole sequence.**  One element `≡ 3 (mod 6)` is enough. -/
theorem prod_abs_cos_six_eq_zero {A : Finset ℕ} {a : ℕ} (ha : a ∈ A) (h : a % 6 = 3) :
    ∏ b ∈ A, |Real.cos (π * b / 6)| = 0 :=
  Finset.prod_eq_zero ha (by rw [cos_pi_mul_div_six_eq_zero a h, abs_zero])

/-- The separation, stated as paper 4 §4 uses it: an odd sequence containing an element
    `≡ 3 (mod 6)` has its modulus-6 peak at `0` while its modulus-4 peak is still exactly
    `(1/√2)^{|A|} > 0`.  A random odd sequence is in this case; a set of primes with `3`
    removed is not. -/
theorem six_dies_four_survives {A : Finset ℕ} (hA : ∀ a ∈ A, a % 2 = 1)
    {a : ℕ} (ha : a ∈ A) (h3 : a % 6 = 3) :
    ∏ b ∈ A, |Real.cos (π * b / 6)| = 0 ∧
      ∏ b ∈ A, |Real.cos (π * b / 4)| = (1 / Real.sqrt 2) ^ A.card ∧
      (0 : ℝ) < (1 / Real.sqrt 2) ^ A.card := by
  refine ⟨prod_abs_cos_six_eq_zero ha h3, prod_abs_cos_four A hA, ?_⟩
  have : (0 : ℝ) < 1 / Real.sqrt 2 := by positivity
  positivity

end Pnp

-- Audit trail: no `sorry`, and no axioms beyond Lean's three.
#print axioms Pnp.abs_cos_pi_mul_div_four
#print axioms Pnp.prod_abs_cos_four
#print axioms Pnp.cos_pi_mul_div_six_eq_zero
#print axioms Pnp.prod_abs_cos_six_eq_zero
#print axioms Pnp.six_dies_four_survives
