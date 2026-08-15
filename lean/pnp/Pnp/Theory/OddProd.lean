/-
  Canon file 13.  Paper 4, Lemma `lem:moddclosed`, the odd branch, by the DOUBLE-ANGLE route
  (paper 4, `rem:doubleangle`).

  The paper proves the closed form of M_odd from the coset identity `lem:coset`, whose proof
  runs through the multiplication formula PROD_i 2 sin(pi(y + i/r)) = 2 sin(r pi y) -- i.e.
  through the factorisation of x^r - 1.  Mathlib has no off-the-shelf product over roots of
  unity, so that route is not the one to formalise.  For q ODD there is a second proof using
  nothing but sin 2x = 2 sin x cos x and a bijection, and this file is that proof:

    PROD_{1<=j<q} |sin(2 pi j/q)| = 2^{q-1} PROD |sin(pi j/q)| PROD |cos(pi j/q)|  (double angle)
    j |-> 2j mod q is a bijection of {1,...,q-1} for q odd                          (q coprime 2)
    |sin(2 pi j/q)| = |sin(pi ((2j) mod q)/q)|                                      (period, up to sign)
    => S = 2^{q-1} S C  with S > 0  =>  C = 2^{1-q}.

  F52: the paper now carries two independent proofs of this identity (roots of unity, and the
  one below).  Two proofs check the STATEMENT; one proof checks only the tactic script.

  TRAP RECORDED (for lean-recipes): writing the statement as `|sin (pi * (2 * j % q) / q)|`
  elaborates `%` in the REALS -- Lean reads it as real modulo and the rewrites silently fail
  to fire.  The natural-number reduction has to be cast explicitly: `((2 * j % q : N) : R)`.
-/
import Mathlib

namespace Pnp

open Real Finset

/-- If `q` is odd and `q ∣ 2d` with `d < q`, then `d = 0`.  This is the only arithmetic input:
    it gives both that the doubling map avoids `0` and that it is injective. -/
private theorem odd_dvd_two {q d : ℕ} (hq : q % 2 = 1) (hd : q ∣ 2 * d) (hlt : d < q) :
    d = 0 := by
  obtain ⟨k, hk⟩ := hd
  match k, hk with
  | 0, hk => omega
  | 1, hk => omega
  | (k + 2), hk =>
      have h3 : q * 2 ≤ q * (k + 2) := Nat.mul_le_mul_left q (by omega)
      omega

/-- The doubling map sends `Ico 1 q` into itself. -/
private theorem dbl_mem {q j : ℕ} (hq : q % 2 = 1) (hj : j ∈ Finset.Ico 1 q) :
    2 * j % q ∈ Finset.Ico 1 q := by
  simp only [Finset.mem_Ico] at hj ⊢
  obtain ⟨h1, h2⟩ := hj
  have hq0 : 0 < q := by omega
  refine ⟨?_, Nat.mod_lt _ hq0⟩
  rcases Nat.eq_zero_or_pos (2 * j % q) with h | h
  · exact absurd (odd_dvd_two hq (Nat.dvd_of_mod_eq_zero h) h2) (by omega)
  · exact h

/-- The doubling map is injective on `Ico 1 q`. -/
private theorem dbl_inj {q : ℕ} (hq : q % 2 = 1) :
    Set.InjOn (fun j => 2 * j % q) (Finset.Ico 1 q : Finset ℕ) := by
  have main : ∀ a b : ℕ, a ∈ Finset.Ico 1 q → b ∈ Finset.Ico 1 q → a ≤ b →
      2 * a % q = 2 * b % q → a = b := by
    intro a b ha hb hab h
    simp only [Finset.mem_Ico] at ha hb
    have hmod : (2 * a) ≡ (2 * b) [MOD q] := h
    have hdvd : q ∣ 2 * b - 2 * a := (Nat.modEq_iff_dvd' (by omega)).mp hmod
    have hrw : 2 * b - 2 * a = 2 * (b - a) := by omega
    rw [hrw] at hdvd
    have := odd_dvd_two hq hdvd (by omega)
    omega
  intro a ha b hb h
  simp only [Finset.coe_Ico, Set.mem_Ico] at ha hb
  have ha' : a ∈ Finset.Ico 1 q := Finset.mem_Ico.mpr ha
  have hb' : b ∈ Finset.Ico 1 q := Finset.mem_Ico.mpr hb
  rcases le_total a b with hle | hle
  · exact main a b ha' hb' hle h
  · exact (main b a hb' ha' hle h.symm).symm

/-- Doubling the angle is, up to sign, reduction of the numerator mod `q`. -/
private theorem abs_sin_two {q j : ℕ} (hj : j ∈ Finset.Ico 1 q) :
    |Real.sin (2 * (π * j / q))| = |Real.sin (π * ((2 * j % q : ℕ) : ℝ) / q)| := by
  simp only [Finset.mem_Ico] at hj
  obtain ⟨h1, h2⟩ := hj
  have hq0 : 0 < q := by omega
  have hqR : (0 : ℝ) < q := by exact_mod_cast hq0
  rcases Nat.lt_or_ge (2 * j) q with h | h
  · rw [Nat.mod_eq_of_lt h]
    congr 1
    push_cast
    ring
  · have hr : 2 * j % q = 2 * j - q := by
      rw [Nat.mod_eq_sub_mod h, Nat.mod_eq_of_lt (by omega)]
    rw [hr]
    have hc : ((2 * j - q : ℕ) : ℝ) = 2 * (j : ℝ) - q := by
      rw [Nat.cast_sub h]; push_cast; try ring_nf
    have he : π * ((2 * j - q : ℕ) : ℝ) / q = 2 * (π * j / q) - π := by
      rw [hc]; field_simp; try ring_nf
    rw [he, Real.sin_sub_pi, abs_neg]

/-- **The odd closed form, by double angle.**  For odd `q`,
    `∏_{j=1}^{q-1} |cos(π j / q)| = (1/2)^{q-1}`. -/
theorem prod_abs_cos_odd (q : ℕ) (hq : q % 2 = 1) :
    ∏ j ∈ Finset.Ico 1 q, |Real.cos (π * j / q)| = (1 / 2 : ℝ) ^ (q - 1) := by
  have hq0 : 0 < q := by omega
  have hqR : (0 : ℝ) < q := by exact_mod_cast hq0
  -- every angle lies strictly inside (0, π), so the sine product is positive
  have hsinpos : ∀ j ∈ Finset.Ico 1 q, 0 < Real.sin (π * j / q) := by
    intro j hj
    simp only [Finset.mem_Ico] at hj
    have hj1 : (1 : ℝ) ≤ j := by exact_mod_cast hj.1
    have hj2 : (j : ℝ) < q := by exact_mod_cast hj.2
    refine Real.sin_pos_of_pos_of_lt_pi ?_ ?_
    · positivity
    · rw [div_lt_iff₀ hqR]
      nlinarith [Real.pi_pos]
  have hSpos : 0 < ∏ j ∈ Finset.Ico 1 q, |Real.sin (π * j / q)| :=
    Finset.prod_pos fun j hj => abs_pos.mpr (ne_of_gt (hsinpos j hj))
  -- the doubled product, computed two ways
  have hleft : ∏ j ∈ Finset.Ico 1 q, |Real.sin (2 * (π * j / q))|
      = ∏ j ∈ Finset.Ico 1 q, |Real.sin (π * j / q)| := by
    have h1 : ∏ j ∈ Finset.Ico 1 q, |Real.sin (2 * (π * j / q))|
        = ∏ j ∈ Finset.Ico 1 q, |Real.sin (π * ((2 * j % q : ℕ) : ℝ) / q)| :=
      Finset.prod_congr rfl fun j hj => abs_sin_two hj
    have himg : (Finset.Ico 1 q).image (fun j => 2 * j % q) = Finset.Ico 1 q := by
      apply Finset.eq_of_subset_of_card_le
      · intro x hx
        obtain ⟨j, hj, rfl⟩ := Finset.mem_image.mp hx
        exact dbl_mem hq hj
      · rw [Finset.card_image_of_injOn (dbl_inj hq)]
    have h2 : ∏ x ∈ (Finset.Ico 1 q).image (fun j => 2 * j % q),
            |Real.sin (π * (x : ℝ) / q)|
        = ∏ j ∈ Finset.Ico 1 q, |Real.sin (π * ((2 * j % q : ℕ) : ℝ) / q)| :=
      Finset.prod_image fun a ha b hb h =>
        dbl_inj hq (Finset.mem_coe.mpr ha) (Finset.mem_coe.mpr hb) h
    rw [h1, ← h2, himg]
  have hright : ∏ j ∈ Finset.Ico 1 q, |Real.sin (2 * (π * j / q))|
      = 2 ^ (q - 1) * ((∏ j ∈ Finset.Ico 1 q, |Real.sin (π * j / q)|)
          * ∏ j ∈ Finset.Ico 1 q, |Real.cos (π * j / q)|) := by
    have h1 : ∀ j ∈ Finset.Ico 1 q, |Real.sin (2 * (π * j / q))|
        = 2 * (|Real.sin (π * j / q)| * |Real.cos (π * j / q)|) := by
      intro j _
      rw [Real.sin_two_mul, abs_mul, abs_mul, abs_two]
      ring
    rw [Finset.prod_congr rfl h1, Finset.prod_mul_distrib, Finset.prod_mul_distrib,
      Finset.prod_const, Nat.card_Ico]
  -- abstract only now, so that no rewrite direction can go wrong
  set S := ∏ j ∈ Finset.Ico 1 q, |Real.sin (π * j / q)| with hS
  set C := ∏ j ∈ Finset.Ico 1 q, |Real.cos (π * j / q)| with hC
  -- `rw [← hleft]` would rewrite the S on BOTH sides; compose the two equalities instead
  have key : S = 2 ^ (q - 1) * (S * C) := hleft.symm.trans hright
  have hmul : S * 1 = S * (2 ^ (q - 1) * C) := by
    rw [mul_one]
    calc S = 2 ^ (q - 1) * (S * C) := key
      _ = S * (2 ^ (q - 1) * C) := by ring
  have hone : (1 : ℝ) = 2 ^ (q - 1) * C := mul_left_cancel₀ (ne_of_gt hSpos) hmul
  have h2ne : ((2 : ℝ) ^ (q - 1)) ≠ 0 := by positivity
  refine mul_left_cancel₀ h2ne ?_
  have hh : ((2 : ℝ) * (1 / 2)) ^ (q - 1) = 1 := by norm_num
  rw [← mul_pow, hh]
  exact hone.symm

end Pnp

-- Audit trail: no `sorry`, and no axioms beyond Lean's three.
#print axioms Pnp.prod_abs_cos_odd
