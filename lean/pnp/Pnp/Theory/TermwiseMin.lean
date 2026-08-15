/-
  Canon file 10.  Paper 4, Lemma 2.2 (termwise minimality) and Theorem 2.3 (the fair coin
  gives the flattest landscape).

  Statement.  For every integer N >= 2 and every q in [0,1],

        q ^ N + (1 - q) ^ N  >=  2 * (1/2) ^ N   ( = 2 ^ (1 - N) ),

  with equality if and only if q = 1/2.

  This is the engine of paper 4's section 2: since
        Gamma^{(q)}(A) = 1 + SUM_d [ q ^ N_d + (1 - q) ^ N_d ],
  the bound holds termwise, hence Gamma^{(q)}(A) >= Gamma(A) for EVERY sequence A, and
  strictly as soon as one stratum has N_d >= 2 -- which |A| >= 2 always supplies.

  Note (F48).  This replaces the Lean item as the spec stated it ("formalise Phi(0) = Gamma").
  That identity is misstated -- Phi(0) = W_D = Gamma + (2D+1) 2^{-k}, tail included -- and its
  correct form, windowSeries_eq_gapSeries, has been in the canon since paper 1.  See r100.

  Proof.  Convexity of x ^ N on [0, oo) at the midpoint of q and 1 - q, whose average is 1/2;
  strict convexity for N >= 2 gives the equality case.  The non-strict bound is proved a
  second time from Bernoulli's inequality, as an in-Lean cross-check of the statement itself.
-/
import Mathlib.Analysis.Convex.Mul
import Mathlib.Analysis.Convex.SpecificFunctions.Deriv

open Set

namespace Pnp

variable {N : ℕ} {q : ℝ}

/-- The two strata weights average to the fair-coin weight: the only arithmetic fact the
    convexity argument needs. -/
theorem half_smul_add_half_smul (q : ℝ) :
    (1 / 2 : ℝ) • q + (1 / 2 : ℝ) • (1 - q) = 1 / 2 := by
  simp only [smul_eq_mul]
  ring

/-- **Termwise minimality (paper 4, Lemma 2.2).**  For every `N` and every `q ∈ [0,1]`,
    `q ^ N + (1 - q) ^ N ≥ 2 * (1/2) ^ N`. -/
theorem termwise_min (hq0 : 0 ≤ q) (hq1 : q ≤ 1) (N : ℕ) :
    2 * (1 / 2 : ℝ) ^ N ≤ q ^ N + (1 - q) ^ N := by
  have hx : q ∈ Ici (0 : ℝ) := hq0
  have hy : (1 - q) ∈ Ici (0 : ℝ) := by
    simp only [mem_Ici, sub_nonneg]; exact hq1
  have h := (convexOn_pow (𝕜 := ℝ) N).2 hx hy (by norm_num : (0:ℝ) ≤ 1 / 2)
    (by norm_num : (0:ℝ) ≤ 1 / 2) (by norm_num)
  rw [half_smul_add_half_smul] at h
  simp only [smul_eq_mul] at h
  linarith

/-- The same bound again, from Bernoulli's inequality instead of convexity.  Two independent
    proofs of one statement is the cheapest check that the statement is the intended one. -/
theorem termwise_min' (hq0 : 0 ≤ q) (hq1 : q ≤ 1) (N : ℕ) :
    2 * (1 / 2 : ℝ) ^ N ≤ q ^ N + (1 - q) ^ N := by
  set t : ℝ := 2 * q - 1 with ht
  have h1 : (-2 : ℝ) ≤ t := by rw [ht]; linarith
  have h2 : (-2 : ℝ) ≤ -t := by rw [ht]; linarith
  have b1 := one_add_mul_le_pow h1 N
  have b2 := one_add_mul_le_pow h2 N
  have e1 : (1 : ℝ) + t = 2 * q := by rw [ht]; ring
  have e2 : (1 : ℝ) + -t = 2 * (1 - q) := by rw [ht]; ring
  rw [e1] at b1
  rw [e2] at b2
  have key : (2 : ℝ) ≤ (2 * q) ^ N + (2 * (1 - q)) ^ N := by nlinarith [b1, b2]
  have expand : ((2 : ℝ) * q) ^ N + (2 * (1 - q)) ^ N
      = 2 ^ N * (q ^ N + (1 - q) ^ N) := by
    rw [mul_pow, mul_pow]; ring
  rw [expand] at key
  have hp : (0 : ℝ) < 2 ^ N := by positivity
  have hc : 2 * (1 / 2 : ℝ) ^ N * 2 ^ N = 2 := by
    rw [mul_assoc, ← mul_pow]; norm_num
  nlinarith [key, hp, hc]

/-- **The equality case.** For `N ≥ 2` and `q ∈ [0,1]` with `q ≠ 1/2`, the inequality is
    strict. -/
theorem termwise_min_strict (hN : 2 ≤ N) (hq0 : 0 ≤ q) (hq1 : q ≤ 1) (hne : q ≠ 1 / 2) :
    2 * (1 / 2 : ℝ) ^ N < q ^ N + (1 - q) ^ N := by
  have hx : q ∈ Ici (0 : ℝ) := hq0
  have hy : (1 - q) ∈ Ici (0 : ℝ) := by
    simp only [mem_Ici, sub_nonneg]; exact hq1
  have hxy : q ≠ 1 - q := by
    intro h; apply hne; linarith
  have h := (strictConvexOn_pow hN).2 hx hy hxy (by norm_num : (0:ℝ) < 1 / 2)
    (by norm_num : (0:ℝ) < 1 / 2) (by norm_num)
  rw [half_smul_add_half_smul] at h
  simp only [smul_eq_mul] at h
  linarith

/-- The fair coin attains the bound. -/
theorem termwise_min_eq (N : ℕ) :
    (1 / 2 : ℝ) ^ N + (1 - 1 / 2 : ℝ) ^ N = 2 * (1 / 2 : ℝ) ^ N := by
  have h : (1 - 1 / 2 : ℝ) = 1 / 2 := by norm_num
  rw [h]; ring

/-- **Paper 4, Theorem 2.3.**  For `N ≥ 2` the map `q ↦ q ^ N + (1 - q) ^ N` on `[0,1]`
    attains its minimum `2 * (1/2) ^ N` exactly at `q = 1/2`. -/
theorem termwise_min_iff (hN : 2 ≤ N) (hq0 : 0 ≤ q) (hq1 : q ≤ 1) :
    q ^ N + (1 - q) ^ N = 2 * (1 / 2 : ℝ) ^ N ↔ q = 1 / 2 := by
  constructor
  · intro h
    by_contra hne
    exact absurd h (ne_of_gt (termwise_min_strict hN hq0 hq1 hne))
  · rintro rfl
    exact termwise_min_eq N

/-- `2 * (1/2) ^ N = 2 ^ (1 - N)`, so the statements above are the paper's, verbatim. -/
theorem two_mul_half_pow (N : ℕ) : 2 * (1 / 2 : ℝ) ^ N = (2 : ℝ) ^ (1 - (N : ℤ)) := by
  rw [zpow_sub₀ (by norm_num : (2:ℝ) ≠ 0), zpow_one, zpow_natCast]
  field_simp
  rw [← mul_pow]
  norm_num

end Pnp

-- Promoted from Experiments/ to Theory/ at r105, section 2 of paper 4 having stabilised.
-- Audit trail: no `sorry`, and no axioms beyond Lean's three.
#print axioms Pnp.termwise_min
#print axioms Pnp.termwise_min'
#print axioms Pnp.termwise_min_strict
#print axioms Pnp.termwise_min_iff
#print axioms Pnp.two_mul_half_pow
