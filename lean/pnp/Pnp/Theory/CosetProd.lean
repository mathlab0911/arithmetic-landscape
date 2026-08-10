/-
  Canon file 14.  Paper 4, Lemma `lem:coset` (the coset identity) -- the REDUCTION.

  The identity is
      PROD_{k<v} |2 cos(pi (t + k/v))| = 2 |cos(pi (v t + tau_v))|,
      tau_v = 1/2 for v even, 0 for v odd,
  and it is the technical spine of paper 4: since |cos| >= 0 it makes the rational points the
  MINIMA of the coset average, which is what removes the equidistribution step from the
  minor-arc argument.  An external review (2026-08-10) named it as an unverified foundation.

  WHY THIS FILE PROVES A REDUCTION AND NOT THE WHOLE IDENTITY.  Mathlib has no product formula
  for sines or cosines -- searched the whole tree twice -- and the base case at an odd prime
  needs an evaluation over roots of unity.  But the identity is MULTIPLICATIVE in v, so:

      v = 2            double angle, elementary                     <- proved here
      v = a * b        multiplicativity, a reindexing               <- proved here
      v an odd prime   the only place roots of unity are needed     <- not here

  Steps 1 and 2 give the identity for every v built from the primes settled by step 3, and
  they are the steps with bookkeeping in them, hence the ones worth machine-checking.  The
  reduction was verified numerically first (`coset_mult_r116`), including a negative control
  on tau, before any Lean time was spent on it.

  THE REINDEXING NEEDS NO BIJECTION.  Writing k = i + a*j and inducting on b turns
  PROD_{k < a*b} into PROD_{i<a} PROD_{j<b} using only `Finset.prod_range_add`,
  `Finset.prod_range_succ` and `Finset.prod_mul_distrib`.  That is `prod_range_mul_index`
  below, which is stated for an arbitrary commutative monoid because nothing about it is
  analytic.
-/
import Mathlib

namespace Pnp

open Real Finset

/-- Splitting a product over `range (a*b)` as a double product via `k = i + a*j`.
    Pure algebra: no bijection, just induction on `b`. -/
theorem prod_range_mul_index {M : Type*} [CommMonoid M] (a b : ℕ) (g : ℕ → M) :
    ∏ k ∈ Finset.range (a * b), g k
      = ∏ i ∈ Finset.range a, ∏ j ∈ Finset.range b, g (i + a * j) := by
  induction b with
  | zero => simp
  | succ b ih =>
      have hab : a * (b + 1) = a * b + a := by ring
      have hstep : ∀ i ∈ Finset.range a,
          (∏ j ∈ Finset.range (b + 1), g (i + a * j))
            = (∏ j ∈ Finset.range b, g (i + a * j)) * g (i + a * b) :=
        fun i _ => Finset.prod_range_succ _ _
      rw [hab, Finset.prod_range_add, ih, Finset.prod_congr rfl hstep,
        Finset.prod_mul_distrib]
      congr 1
      exact Finset.prod_congr rfl (fun i _ => by rw [Nat.add_comm])

/-- The coset product of paper 4. -/
noncomputable def cprod (v : ℕ) (t : ℝ) : ℝ :=
  ∏ k ∈ Finset.range v, |2 * Real.cos (π * (t + (k : ℝ) / (v : ℝ)))|

/-- The offset of the closed form: `1/2` for `v` even, `0` for `v` odd. -/
noncomputable def tau (v : ℕ) : ℝ := if v % 2 = 0 then 1 / 2 else 0

/-- The identity, as a predicate on `v`, so that the reduction can be stated cleanly. -/
def CosetId (v : ℕ) : Prop :=
  ∀ t : ℝ, cprod v t = 2 * |Real.cos (π * ((v : ℝ) * t + tau v))|

/-- `|cos|` is unchanged by an integer multiple of `π`; the sign flips and the absolute
    value does not.  This is what makes the `tau` bookkeeping work mod 1. -/
theorem abs_cos_add_int_mul_pi (x : ℝ) : ∀ n : ℤ,
    |Real.cos (x + (n : ℝ) * π)| = |Real.cos x| := by
  intro n
  induction n using Int.induction_on with
  | zero => simp
  | succ k ih =>
      have h : x + (((k : ℤ) + 1 : ℤ) : ℝ) * π = (x + ((k : ℤ) : ℝ) * π) + π := by
        push_cast; ring
      rw [h, Real.cos_add_pi, abs_neg, ih]
  | pred k ih =>
      have h : x + ((-(k : ℤ) - 1 : ℤ) : ℝ) * π = (x + ((-(k : ℤ) : ℤ) : ℝ) * π) - π := by
        push_cast; ring
      rw [h, Real.cos_sub_pi, abs_neg, ih]

theorem cosetId_one : CosetId 1 := by
  intro t
  simp [cprod, tau, abs_mul]

/-- **Base case.**  `v = 2` is the double-angle formula and needs nothing else. -/
theorem cosetId_two : CosetId 2 := by
  intro t
  have h1 : π * (t + (1 : ℝ) / (2 : ℝ)) = π * t + π / 2 := by ring
  have h2 : π * ((2 : ℝ) * t + 1 / 2) = 2 * (π * t) + π / 2 := by ring
  simp only [cprod, tau, Finset.prod_range_succ, Finset.prod_range_zero, one_mul]
  norm_num
  rw [h1, h2, Real.cos_add_pi_div_two, Real.cos_add_pi_div_two, Real.sin_two_mul]
  simp only [abs_neg, abs_mul, abs_two]
  ring

/-- **Multiplicativity.**  If the identity holds at `a` and at `b` it holds at `a*b`.
    This is the step the whole reduction rests on. -/
theorem cosetId_mul {a b : ℕ} (ha : 0 < a) (hb : 0 < b)
    (Ha : CosetId a) (Hb : CosetId b) : CosetId (a * b) := by
  intro t
  have haR : (a : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr ha.ne'
  have hbR : (b : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hb.ne'
  -- (1) reindex k = i + a*j
  have hsplit : cprod (a * b) t
      = ∏ i ∈ Finset.range a, cprod b (t + (i : ℝ) / ((a : ℝ) * (b : ℝ))) := by
    unfold cprod
    rw [prod_range_mul_index a b]
    refine Finset.prod_congr rfl (fun i _ => Finset.prod_congr rfl (fun j _ => ?_))
    congr 2
    push_cast
    field_simp
    ring
  -- (2) apply the identity at b inside
  have hb2 : ∀ i ∈ Finset.range a,
      cprod b (t + (i : ℝ) / ((a : ℝ) * (b : ℝ)))
        = |2 * Real.cos (π * (((b : ℝ) * t + tau b) + (i : ℝ) / (a : ℝ)))| := by
    intro i _
    rw [Hb]
    have : (b : ℝ) * (t + (i : ℝ) / ((a : ℝ) * (b : ℝ))) + tau b
        = ((b : ℝ) * t + tau b) + (i : ℝ) / (a : ℝ) := by field_simp; ring
    rw [this, abs_mul]
    norm_num
  -- (3) that is cprod a at the shifted point, so apply the identity at a
  have hstep : cprod (a * b) t = cprod a ((b : ℝ) * t + tau b) := by
    rw [hsplit, Finset.prod_congr rfl hb2]
    rfl
  rw [hstep, Ha]
  -- (4) the tau bookkeeping
  congr 1
  have hexp : (a : ℝ) * ((b : ℝ) * t + tau b) + tau a
      = ((a : ℝ) * (b : ℝ) * t + tau (a * b)) + (((a : ℝ) * tau b + tau a - tau (a * b))) := by
    ring
  have hcast : ((a * b : ℕ) : ℝ) = (a : ℝ) * (b : ℝ) := by push_cast; ring
  rw [hcast]
  set D : ℝ := (a : ℝ) * tau b + tau a - tau (a * b) with hD
  have hint : ∃ n : ℤ, D = (n : ℝ) := by
    rcases Nat.even_or_odd a with hae | hao <;> rcases Nat.even_or_odd b with hbe | hbo
    · -- a even, b even:  D = a/2
      obtain ⟨m, hm⟩ := hae
      have ta : tau a = 1 / 2 := by simp [tau, Nat.even_iff.mp ⟨m, hm⟩]
      have tb : tau b = 1 / 2 := by simp [tau, Nat.even_iff.mp hbe]
      have tab : tau (a * b) = 1 / 2 := by
        simp [tau, Nat.even_iff.mp (Nat.even_mul.mpr (Or.inl ⟨m, hm⟩))]
      have hR : (a : ℝ) = (m : ℝ) + (m : ℝ) := by exact_mod_cast hm
      exact ⟨(m : ℤ), by rw [hD, ta, tb, tab, hR]; push_cast; ring⟩
    · -- a even, b odd:  D = 0
      obtain ⟨m, hm⟩ := hae
      have ta : tau a = 1 / 2 := by simp [tau, Nat.even_iff.mp ⟨m, hm⟩]
      have tb : tau b = 0 := by simp [tau, Nat.odd_iff.mp hbo]
      have tab : tau (a * b) = 1 / 2 := by
        simp [tau, Nat.even_iff.mp (Nat.even_mul.mpr (Or.inl ⟨m, hm⟩))]
      exact ⟨0, by rw [hD, ta, tb, tab]; push_cast; ring⟩
    · -- a odd, b even:  D = (a-1)/2
      obtain ⟨c, hc⟩ := hao
      obtain ⟨m, hm⟩ := hbe
      have ta : tau a = 0 := by simp [tau, Nat.odd_iff.mp ⟨c, hc⟩]
      have tb : tau b = 1 / 2 := by simp [tau, Nat.even_iff.mp ⟨m, hm⟩]
      have tab : tau (a * b) = 1 / 2 := by
        simp [tau, Nat.even_iff.mp (Nat.even_mul.mpr (Or.inr ⟨m, hm⟩))]
      have hR : (a : ℝ) = 2 * (c : ℝ) + 1 := by exact_mod_cast hc
      exact ⟨(c : ℤ), by rw [hD, ta, tb, tab, hR]; push_cast; ring⟩
    · -- a odd, b odd:  D = 0
      have ta : tau a = 0 := by simp [tau, Nat.odd_iff.mp hao]
      have tb : tau b = 0 := by simp [tau, Nat.odd_iff.mp hbo]
      have tab : tau (a * b) = 0 := by
        simp [tau, Nat.odd_iff.mp (Nat.odd_mul.mpr ⟨hao, hbo⟩)]
      exact ⟨0, by rw [hD, ta, tb, tab]; push_cast; ring⟩
  obtain ⟨n, hn⟩ := hint
  have : π * ((a : ℝ) * ((b : ℝ) * t + tau b) + tau a)
      = π * ((a : ℝ) * (b : ℝ) * t + tau (a * b)) + (n : ℝ) * π := by
    rw [hexp, hn]; ring
  rw [this, abs_cos_add_int_mul_pi]

end Pnp

-- Audit trail: no `sorry`, and no axioms beyond Lean's three.
#print axioms Pnp.prod_range_mul_index
#print axioms Pnp.abs_cos_add_int_mul_pi
#print axioms Pnp.cosetId_one
#print axioms Pnp.cosetId_two
#print axioms Pnp.cosetId_mul
