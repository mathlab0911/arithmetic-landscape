/-
  Canon file 16.  The two finite Abel identities the `s > 1` argument rests on (r226/r227).

  WHAT THIS IS FOR.  The argument for `lambda_infty(s) = s - 1/2` (door (a), fable-5's r224)
  bounds the head of the Abel sine series by two inequalities:

      (H1)  | HEAD - 2t * SUM_{j<=J} j D_j |  <=  2 e^2 t^2 * SUM_{j<=J} j^2 D_j
      (H2)  | 2 SUM_{j<=J} j D_j - 2 zeta(s) |  <=  2 J^{1-s} s/(s-1)

  where `D_j = w_{j-1} - w_j`.  Both are useless without closed forms for those two moments,
  and the closed forms are what make the bounds *computable* rather than merely asymptotic:

      SUM_{j=1}^{J} j   D_j  =  SUM_{i<J} w_i          -  J   w_J
      SUM_{j=1}^{J} j^2 D_j  =  SUM_{i<J} (2i+1) w_i   -  J^2 w_J

  Those are the two statements proved here.  They are finite, exact, and hold for EVERY real
  sequence `w` -- no monotonicity, no decay, no positivity.  Everything analytic in the
  argument (zeta, arctan, Dirichlet's test, the asymptotics) is deliberately NOT here; this
  file is the part that can be made certain, and it is separated out for exactly that reason.

  STATUS OF THE SURROUNDING ARGUMENT, so this file is not read as more than it is.  The
  `s > 1` branch is *derived, with every inequality checked numerically at 24 of 24 points*
  (`lean/pnp/debts_r226.py/.log`).  It is NOT proved: it has had no second reading, the `j^2`
  sum is handled case by case in `s` rather than by one closed form, and the analysis above
  is on paper only.  **These two lemmas being in Lean does not raise that status.**  They
  remove one class of error from it -- an algebra slip in the moments would be invisible in
  the numerics, because the same wrong formula would be used on both sides (F87).

  PROVENANCE.  The identities were derived by hand at r226 and checked against direct
  summation at 40 digits by `debts_r226.py` control M0a.  A numerical agreement between a
  formula and its own implementation is weak evidence (F52: two routes, and a spot check
  beside an exact comparison is decoration).  Induction is the second route.

  Proof.  Induction on `J` in both cases, with `(n+1) - n = 1` and `(n+1)^2 - n^2 = 2n+1`
  doing the work in the step.  Written by induction rather than by citing a Mathlib
  summation-by-parts lemma, per the project's standing preference.
-/
import Mathlib

namespace Pnp

/-- **First moment of the decrements (r226, identity behind (H2)).**

For every real sequence `w` and every `J`,
`∑_{j=1}^{J} j (w_{j-1} - w_j) = ∑_{i<J} w_i - J w_J`.

Indexed here from `0`: the `j`-th summand is `(j+1)(w_j - w_{j+1})`, so the sum over
`Finset.range J` is the sum over `j = 1 … J` in the paper's indexing. -/
theorem abel_moment_one (w : ℕ → ℝ) (J : ℕ) :
    ∑ j ∈ Finset.range J, ((j : ℝ) + 1) * (w j - w (j + 1))
      = (∑ i ∈ Finset.range J, w i) - (J : ℝ) * w J := by
  induction J with
  | zero => simp
  | succ n ih =>
    rw [Finset.sum_range_succ, ih, Finset.sum_range_succ]
    push_cast
    ring

/-- **Second moment of the decrements (r226, identity behind (H1)).**

For every real sequence `w` and every `J`,
`∑_{j=1}^{J} j^2 (w_{j-1} - w_j) = ∑_{i<J} (2i+1) w_i - J^2 w_J`.

The coefficient `2i+1` is exactly `(i+1)^2 - i^2`; that is the whole content of the step. -/
theorem abel_moment_two (w : ℕ → ℝ) (J : ℕ) :
    ∑ j ∈ Finset.range J, ((j : ℝ) + 1) ^ 2 * (w j - w (j + 1))
      = (∑ i ∈ Finset.range J, (2 * (i : ℝ) + 1) * w i) - (J : ℝ) ^ 2 * w J := by
  induction J with
  | zero => simp
  | succ n ih =>
    rw [Finset.sum_range_succ, ih, Finset.sum_range_succ]
    push_cast
    ring

/-- **The first moment is non-negative for a non-increasing sequence.**

`0 ≤ ∑_{i<J} w_i - J w_J` whenever `w` is non-increasing.  This is what makes (H2) a *tail*
bound: the truncated first moment approaches its limit from below, so the error is the tail
of a convergent series and nothing else. -/
theorem abel_moment_one_nonneg (w : ℕ → ℝ) (J : ℕ) (hmono : ∀ j, w (j + 1) ≤ w j) :
    0 ≤ (∑ i ∈ Finset.range J, w i) - (J : ℝ) * w J := by
  rw [← abel_moment_one w J]
  refine Finset.sum_nonneg fun j _ => ?_
  have h1 : (0 : ℝ) ≤ (j : ℝ) + 1 := by positivity
  have h2 : (0 : ℝ) ≤ w j - w (j + 1) := sub_nonneg.mpr (hmono j)
  exact mul_nonneg h1 h2

/-- **The skeleton of the two-line theorem (r220), named so that it can be cited.**

If every decrement `d j` and every factor `a j` is non-negative, the weighted sum is
non-negative.  This is immediate from `Finset.sum_nonneg` and is recorded not because it is
difficult but because it is the *shape* of the r220 result: with `d j` the weight decrements
of a non-increasing profile and `a j = ρ^j sin(jθ) ≥ 0` on `0 < θ ≤ π/k`, it gives `F_k ≥ 1`
and hence `t₁ > ½ tan(π/k)`.  The two hypotheses are where all the mathematics lives; naming
the trivial step keeps the paper's citation checkable (C7) and makes it visible that the
step itself assumes nothing else. -/
theorem sum_nonneg_of_nonneg_decrements (d a : ℕ → ℝ) (k : ℕ)
    (hd : ∀ j, 0 ≤ d j) (ha : ∀ j, 0 ≤ a j) :
    0 ≤ ∑ j ∈ Finset.range k, d j * a j :=
  Finset.sum_nonneg fun j _ => mul_nonneg (hd j) (ha j)

end Pnp
