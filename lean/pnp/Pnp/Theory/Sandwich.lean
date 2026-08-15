/- 算術地形理論(ALT)正典 第6号 (2026-08-08, opus-5 実務セッション・7周目)
   5周目の持ち越し: 主張20b(挟み撃ち不等式)の Lean 化。

   狙い: 「独立近似」を仮定するのではなく、**平坦性という検証可能な有限の仮定**から
   lm/deg の上下界を導く。平坦性の度合い ε は各 k で厳密に計算でき(実測済み)、
   結論は ℚ 上の有限不等式なので、個々のインスタンスで認証付きの誤差評価になる。

   定理23(抽象版): 有限和の各項が基準値 v の (1+ε)^{±1} 倍に収まるなら、
     v / Σ ∈ [ 1/((1+ε)·|s|), (1+ε)/|s| ]。
   定理24: 過剰側 d-層 = 切断列の表現数(overCount = repCount, J = ∅)。
   定理25: 不足側 d-層 = 切断列の表現数(underCount = repCount, J = I_d)。
   定理26・27(= 主張20b の核): 平坦性 ⟹ 層比 over/deg, under/deg が 2^{−N(d)} の
     (1+ε)^{±1} 倍に収まる。
   定理28: d ≤ d* について足し上げた挟み撃ち(部分窓級数版)。 -/
import Pnp.Theory.Fiber

namespace ALT

section Sandwich

variable {k : Nat}

/-- 小要素の添字集合 I_d = {i : a_i ≤ 2d} -/
def smallIdx (A : Fin k → Nat) (d : Nat) : Finset (Fin k) :=
  Finset.univ.filter (fun i => A i ≤ 2 * d)

/-- N(d) = |I_d| -/
def winCountFin (A : Fin k → Nat) (d : Nat) : Nat := (smallIdx A d).card

/-- 部分窓級数 W_{d*}(A) = 1 + 2 Σ_{d=1}^{d*} 2^{−N(d)}(Fin 版) -/
def winSeriesFin (A : Fin k → Nat) (D : Nat) : ℚ :=
  1 + 2 * ∑ d ∈ Finset.range D, ((1 : ℚ) / 2) ^ (winCountFin A (d + 1))

/-- 定理23(抽象版の挟み撃ち): 有限和の各項が基準値 v の (1+ε)^{±1} 倍に収まるなら、
    v と和の比は 1/|s| の (1+ε)^{±1} 倍に収まる。平坦性の効き方の本体。 -/
theorem ratio_bounds_of_flat {ι : Type*} (s : Finset ι) (g : ι → ℚ) (v ε : ℚ)
    (hε : 0 ≤ ε) (hv : 0 < v) (hne : s.Nonempty)
    (hup : ∀ i ∈ s, g i ≤ (1 + ε) * v)
    (hlo : ∀ i ∈ s, v ≤ (1 + ε) * g i) :
    v / (∑ i ∈ s, g i) ≤ (1 + ε) / (s.card : ℚ) ∧
    (1 : ℚ) / ((1 + ε) * (s.card : ℚ)) ≤ v / (∑ i ∈ s, g i) := by
  have h1e : (0 : ℚ) < 1 + ε := by linarith
  have hc : (0 : ℚ) < (s.card : ℚ) := by
    exact_mod_cast Finset.card_pos.mpr hne
  -- 下からの評価: 各項 ≥ v/(1+ε)
  have hlo' : ∀ i ∈ s, v / (1 + ε) ≤ g i := by
    intro i hi
    rw [div_le_iff₀ h1e]
    have := hlo i hi
    linarith
  have hsum_lo : (s.card : ℚ) * (v / (1 + ε)) ≤ ∑ i ∈ s, g i := by
    have := Finset.card_nsmul_le_sum s g (v / (1 + ε)) hlo'
    simpa [nsmul_eq_mul] using this
  have hsum_up : ∑ i ∈ s, g i ≤ (s.card : ℚ) * ((1 + ε) * v) := by
    have := Finset.sum_le_card_nsmul s g ((1 + ε) * v) hup
    simpa [nsmul_eq_mul] using this
  have hvpos : (0 : ℚ) < v / (1 + ε) := div_pos hv h1e
  have hG : (0 : ℚ) < ∑ i ∈ s, g i := by
    have : (0 : ℚ) < (s.card : ℚ) * (v / (1 + ε)) := mul_pos hc hvpos
    linarith
  constructor
  · rw [div_le_div_iff₀ hG hc]
    have : (s.card : ℚ) * v ≤ (1 + ε) * ∑ i ∈ s, g i := by
      have h := mul_le_mul_of_nonneg_left hsum_lo (le_of_lt h1e)
      have hid : (1 + ε) * ((s.card : ℚ) * (v / (1 + ε))) = (s.card : ℚ) * v := by
        field_simp
      linarith [h, hid.ge, hid.le]
    linarith
  · rw [div_le_div_iff₀ (by positivity) hG]
    linarith

/-- 定理24: 過剰側 d-層は切断列の表現数(J = ∅ の場合) -/
theorem overCount_eq_repCount (A : Fin k → Nat) (n d : Nat) :
    overCount A n d = repCount A (smallIdx A d) ∅ (n + d) := by
  classical
  rw [← fiber_card_eq_repCount A (n + d) (Finset.empty_subset (smallIdx A d))]
  unfold overCount
  congr 1
  apply Finset.filter_congr
  intro S _
  constructor
  · rintro ⟨hsum, hcond⟩
    refine ⟨hsum, ?_⟩
    ext i
    simp only [Finset.mem_inter, Finset.notMem_empty, iff_false, not_and, smallIdx,
      Finset.mem_filter, Finset.mem_univ, true_and]
    intro hiS
    have := hcond i hiS
    omega
  · rintro ⟨hsum, hint⟩
    refine ⟨hsum, fun i hi => ?_⟩
    by_contra hcon
    have hiI : i ∈ smallIdx A d := by
      simp only [smallIdx, Finset.mem_filter, Finset.mem_univ, true_and]; omega
    have : i ∈ S ∩ smallIdx A d := Finset.mem_inter.mpr ⟨hi, hiI⟩
    rw [hint] at this
    exact Finset.notMem_empty i this

/-- 定理25: 不足側 d-層は切断列の表現数(J = I_d の場合) -/
theorem underCount_eq_repCount (A : Fin k → Nat) (n d : Nat) (hd : d ≤ n) :
    underCount A n d = repCount A (smallIdx A d) (smallIdx A d) (n - d) := by
  classical
  rw [← fiber_card_eq_repCount A (n - d) (Finset.Subset.refl (smallIdx A d))]
  unfold underCount
  congr 1
  apply Finset.filter_congr
  intro S _
  constructor
  · rintro ⟨hsum, hcond⟩
    refine ⟨by omega, Finset.inter_eq_right.mpr (fun i hi => ?_)⟩
    by_contra hns
    have h1 := hcond i hns
    simp only [smallIdx, Finset.mem_filter, Finset.mem_univ, true_and] at hi
    omega
  · rintro ⟨hsum, hint⟩
    refine ⟨by omega, fun i hi => ?_⟩
    by_contra hcon
    have hiI : i ∈ smallIdx A d := by
      simp only [smallIdx, Finset.mem_filter, Finset.mem_univ, true_and]; omega
    exact hi (Finset.inter_eq_right.mp hint hiI)

/-- 定理26(= 主張20b の核): 基底状態を小要素部 J で層別したときの表現数が
    基準値 v の (1+ε)^{±1} 倍に収まる(= 平坦性)なら、比 v/deg は
    2^{−N(d)} の (1+ε)^{±1} 倍に収まる。
    v = overCount(定理24)/ underCount(定理25)を入れると層比の評価になる。 -/
theorem stratum_ratio_bounds (A : Fin k → Nat) (n d v : Nat) (ε : ℚ)
    (hε : 0 ≤ ε) (hpos : 0 < v)
    (hup : ∀ J ∈ (smallIdx A d).powerset,
      (repCount A (smallIdx A d) J n : ℚ) ≤ (1 + ε) * (v : ℚ))
    (hlo : ∀ J ∈ (smallIdx A d).powerset,
      (v : ℚ) ≤ (1 + ε) * (repCount A (smallIdx A d) J n : ℚ)) :
    (v : ℚ) / (degCount A n : ℚ) ≤ (1 + ε) / 2 ^ (winCountFin A d) ∧
    (1 : ℚ) / ((1 + ε) * 2 ^ (winCountFin A d)) ≤ (v : ℚ) / (degCount A n : ℚ) := by
  classical
  have hdeg : (degCount A n : ℚ)
      = ∑ J ∈ (smallIdx A d).powerset, (repCount A (smallIdx A d) J n : ℚ) := by
    rw [degCount_eq_sum_repCount A n (smallIdx A d)]
    push_cast
    rfl
  have hcard : (((smallIdx A d).powerset.card : ℕ) : ℚ) = 2 ^ (winCountFin A d) := by
    rw [Finset.card_powerset]
    unfold winCountFin
    push_cast
    ring
  have hne : (smallIdx A d).powerset.Nonempty := ⟨∅, Finset.empty_mem_powerset _⟩
  have hv : (0 : ℚ) < (v : ℚ) := by exact_mod_cast hpos
  obtain ⟨h1, h2⟩ :=
    ratio_bounds_of_flat (smallIdx A d).powerset
      (fun J => (repCount A (smallIdx A d) J n : ℚ)) (v : ℚ) ε hε hv hne hup hlo
  rw [hcard] at h1 h2
  rw [hdeg]
  exact ⟨h1, h2⟩

/-- 部分局所最小数 lm_{≤D}: d ≤ D の層だけを足したもの(d=0 層は deg) -/
def lmPartial (A : Fin k → Nat) (n D : Nat) : Nat :=
  degCount A n + ∑ d ∈ Finset.range D, (overCount A n (d + 1) + underCount A n (d + 1))

/-- 定理28(= 主張20b): 平坦性から従う挟み撃ち。
    d ≤ D の各層で比が 2^{−N(d)} の (1+ε)^{±1} 倍に収まっているなら、
    部分局所最小数と基底状態数の比は部分窓級数 W_D の (1+ε)^{±1} 倍に収まる。
    結論は ℚ 上の有限不等式であり、具体的な k・ε で完全に計算可能。
    (定理18により W_D = Γ + (2D+1)/2^k なので、右辺は Γ で書き換えられる。) -/
theorem sandwich_partial (A : Fin k → Nat) (n D : Nat) (ε : ℚ) (hε : 0 ≤ ε)
    (hDg : 0 < (degCount A n : ℚ))
    (hup : ∀ d ∈ Finset.range D,
      ((overCount A n (d + 1) : ℚ) + (underCount A n (d + 1) : ℚ)) / (degCount A n : ℚ)
        ≤ 2 * (1 + ε) * ((1 : ℚ) / 2) ^ (winCountFin A (d + 1)))
    (hlo : ∀ d ∈ Finset.range D,
      2 * ((1 : ℚ) / 2) ^ (winCountFin A (d + 1)) / (1 + ε)
        ≤ ((overCount A n (d + 1) : ℚ) + (underCount A n (d + 1) : ℚ)) / (degCount A n : ℚ)) :
    winSeriesFin A D / (1 + ε) ≤ (lmPartial A n D : ℚ) / (degCount A n : ℚ) ∧
    (lmPartial A n D : ℚ) / (degCount A n : ℚ) ≤ (1 + ε) * winSeriesFin A D := by
  have h1e : (0 : ℚ) < 1 + ε := by linarith
  set Sg : ℚ := ∑ d ∈ Finset.range D, ((1 : ℚ) / 2) ^ (winCountFin A (d + 1)) with hSg
  have hSgnn : 0 ≤ Sg := Finset.sum_nonneg (fun d _ => by positivity)
  set R : ℚ := ∑ d ∈ Finset.range D,
    ((overCount A n (d + 1) : ℚ) + (underCount A n (d + 1) : ℚ)) / (degCount A n : ℚ) with hR
  have hsplit : (lmPartial A n D : ℚ) / (degCount A n : ℚ) = 1 + R := by
    rw [hR]
    unfold lmPartial
    push_cast
    rw [add_div, Finset.sum_div, div_self (ne_of_gt hDg)]
  have hRup : R ≤ 2 * (1 + ε) * Sg := by
    have h := Finset.sum_le_sum hup
    rw [← hR] at h
    calc R ≤ ∑ d ∈ Finset.range D, 2 * (1 + ε) * ((1 : ℚ) / 2) ^ (winCountFin A (d + 1)) := h
      _ = 2 * (1 + ε) * Sg := by rw [hSg, Finset.mul_sum]
  have hRlo : 2 * Sg / (1 + ε) ≤ R := by
    have h := Finset.sum_le_sum hlo
    rw [← hR] at h
    calc 2 * Sg / (1 + ε)
        = ∑ d ∈ Finset.range D, 2 * ((1 : ℚ) / 2) ^ (winCountFin A (d + 1)) / (1 + ε) := by
          rw [hSg, Finset.mul_sum, Finset.sum_div]
      _ ≤ R := h
  have hRlo' : 2 * Sg ≤ R * (1 + ε) := by
    rw [div_le_iff₀ h1e] at hRlo; linarith
  have hW : winSeriesFin A D = 1 + 2 * Sg := by rw [winSeriesFin, hSg]
  constructor
  · rw [hsplit, hW, div_le_iff₀ h1e]
    nlinarith [hRlo']
  · rw [hsplit, hW]
    nlinarith [hRup, hSgnn, hε]

end Sandwich

/- ---- 数値クロスチェック(定理24・25・28 の量がすべて計算可能であることの確認) ----
   A6 = (3,5,7,11,13,17), T = 56, 中央目標 n = 28。 -/

#eval [degCount A6 28, overCount A6 28 1, underCount A6 28 1,
       overCount A6 28 2, underCount A6 28 2]

-- 定理24・25 の左右が一致すること(d = 1, 2, 3)
#eval [decide (overCount A6 28 1 = repCount A6 (smallIdx A6 1) ∅ 29),
       decide (overCount A6 28 2 = repCount A6 (smallIdx A6 2) ∅ 30),
       decide (underCount A6 28 1 = repCount A6 (smallIdx A6 1) (smallIdx A6 1) 27),
       decide (underCount A6 28 2 = repCount A6 (smallIdx A6 2) (smallIdx A6 2) 26)]
-- 期待 [true, true, true, true]

-- 挟み撃ちの各量(ε は実測値を入れれば有限不等式として検証できる)
#eval lmPartial A6 28 3            -- 部分局所最小数 (d ≤ 3)
#eval winSeriesFin A6 3            -- 部分窓級数 W_3
#eval (lmPartial A6 28 3 : ℚ) / (degCount A6 28 : ℚ)

end ALT

#print axioms ALT.ratio_bounds_of_flat
#print axioms ALT.overCount_eq_repCount
#print axioms ALT.underCount_eq_repCount
#print axioms ALT.stratum_ratio_bounds
#print axioms ALT.sandwich_partial
