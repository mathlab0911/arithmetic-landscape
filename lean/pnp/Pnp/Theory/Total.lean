/- 算術地形理論(ALT)正典 第7号 (2026-08-08, opus-5 実務セッション・8周目)
   投稿前必須の残件: 定理19(和インデックス形)を d-インデックス形に書き換え、
   定理28(挟み撃ち)を lm 全体に接続する。

   定理29: lm A n = lmPartial A n D(D より上の層が消えていれば厳密に等しい)
   定理30: 消滅条件を「全要素 ≤ 2D+1」から自動的に供給する系
   これにより
     W_D/(1+ε) ≤ lm/deg ≤ (1+ε)·W_D,   W_D = Γ + (2D+1)/2^k
   が完成する。 -/
import Pnp.Theory.Sandwich

namespace ALT

section Total

variable {k : Nat}

/-- 打ち切り補題: P 以上で消える関数の range 和は range P までで尽きる -/
theorem sum_range_eq_of_vanish {f : Nat → Nat} {P M : Nat}
    (hf : ∀ d, P ≤ d → f d = 0) (hM : P ≤ M) :
    ∑ d ∈ Finset.range M, f d = ∑ d ∈ Finset.range P, f d := by
  refine (Finset.sum_subset (fun x hx => ?_) ?_).symm
  · simp only [Finset.mem_range] at hx ⊢; omega
  · intro x hx hxn
    simp only [Finset.mem_range] at hx hxn
    exact hf x (by omega)

/-- 打ち切り補題(両側版) -/
theorem sum_range_congr_of_vanish {f : Nat → Nat} {M N : Nat}
    (hf : ∀ d, min M N ≤ d → f d = 0) :
    ∑ d ∈ Finset.range M, f d = ∑ d ∈ Finset.range N, f d := by
  rw [sum_range_eq_of_vanish hf (Nat.min_le_left M N)]
  exact (sum_range_eq_of_vanish hf (Nat.min_le_right M N)).symm

/-- 消滅補題(過剰側・目標が総和を超える場合) -/
theorem overCount_eq_zero_of_sum_lt (A : Fin k → Nat) {n d : Nat}
    (h : Finset.univ.sum A < n + d) : overCount A n d = 0 := by
  unfold overCount
  rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
  intro S _
  rintro ⟨hsum, -⟩
  have hle : S.sum A ≤ Finset.univ.sum A :=
    Finset.sum_le_sum_of_subset (Finset.subset_univ S)
  omega

/-- 消滅補題(不足側・不足が目標を超える場合) -/
theorem underCount_eq_zero_of_lt (A : Fin k → Nat) {n d : Nat} (h : n < d) :
    underCount A n d = 0 := by
  unfold underCount
  rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
  intro S _
  rintro ⟨hsum, -⟩
  omega

/-- d = 0 の不足側層も基底状態の全体 -/
theorem underCount_zero_eq_degCount {A : Fin k → Nat} (hA : ∀ i, 0 < A i) (n : Nat) :
    underCount A n 0 = degCount A n := by
  unfold underCount degCount
  congr 1
  apply Finset.filter_congr
  intro S _
  constructor
  · rintro ⟨hsum, -⟩; omega
  · intro hsum
    exact ⟨by omega, fun i _ => by have := hA i; omega⟩

/-- 定理29(d-インデックス形): D より上の層が消えていれば lm は部分和 lmPartial に等しい。
    定理19(和インデックス形)の再インデックス。これで定理28 が lm 全体に接続する。 -/
theorem lm_eq_lmPartial (A : Fin k → Nat) (hA : ∀ i, 0 < A i) (n D : Nat)
    (hn : n ≤ Finset.univ.sum A)
    (hover : ∀ d, D < d → overCount A n d = 0)
    (hunder : ∀ d, D < d → underCount A n d = 0) :
    lm A n = lmPartial A n D := by
  classical
  set T := Finset.univ.sum A with hT
  rw [lm_eq_sum_strata A hA n]
  rw [← Finset.sum_filter_add_sum_filter_not (Finset.range (T + 1)) (fun s => n ≤ s)]
  -- 過剰側の添字集合
  have hIco : (Finset.range (T + 1)).filter (fun s => n ≤ s) = Finset.Ico n (T + 1) := by
    ext s
    simp only [Finset.mem_filter, Finset.mem_range, Finset.mem_Ico]
    omega
  have hRan : (Finset.range (T + 1)).filter (fun s => ¬ n ≤ s) = Finset.range n := by
    ext s
    simp only [Finset.mem_filter, Finset.mem_range]
    omega
  rw [hIco, hRan]
  -- 過剰側: s ↦ s − n で range に直す
  have hAsum : ∑ s ∈ Finset.Ico n (T + 1),
      (if n ≤ s then overCount A n (s - n) else underCount A n (n - s))
      = ∑ i ∈ Finset.range (T + 1 - n), overCount A n i := by
    rw [Finset.sum_Ico_eq_sum_range]
    apply Finset.sum_congr rfl
    intro i _
    rw [if_pos (by omega)]
    congr 1
    omega
  -- 不足側: s ↦ n − s(range_reflect)
  have hrefl : ∑ j ∈ Finset.range n, underCount A n (n - 1 - j + 1)
      = ∑ j ∈ Finset.range n, underCount A n (j + 1) :=
    Finset.sum_range_reflect (fun j => underCount A n (j + 1)) n
  have hBsum : ∑ s ∈ Finset.range n,
      (if n ≤ s then overCount A n (s - n) else underCount A n (n - s))
      = ∑ j ∈ Finset.range n, underCount A n (j + 1) := by
    rw [← hrefl]
    apply Finset.sum_congr rfl
    intro s hs
    simp only [Finset.mem_range] at hs
    rw [if_neg (by omega)]
    congr 1
    omega
  rw [hAsum, hBsum]
  -- 過剰側から d = 0 を取り出す
  have hT1 : T + 1 - n = (T - n) + 1 := by omega
  rw [hT1, Finset.sum_range_succ']
  rw [overCount_zero_eq_degCount hA n]
  -- 打ち切り
  have hovertrunc : ∑ i ∈ Finset.range (T - n), overCount A n (i + 1)
      = ∑ i ∈ Finset.range D, overCount A n (i + 1) := by
    apply sum_range_congr_of_vanish
    intro d hd
    rcases min_le_iff.mp hd with h | h
    · exact overCount_eq_zero_of_sum_lt A (by omega)
    · exact hover (d + 1) (by omega)
  have hundertrunc : ∑ j ∈ Finset.range n, underCount A n (j + 1)
      = ∑ j ∈ Finset.range D, underCount A n (j + 1) := by
    apply sum_range_congr_of_vanish
    intro d hd
    rcases min_le_iff.mp hd with h | h
    · exact underCount_eq_zero_of_lt A (by omega)
    · exact hunder (d + 1) (by omega)
  rw [hovertrunc, hundertrunc]
  unfold lmPartial
  rw [Finset.sum_add_distrib]
  omega

/-- 定理30(消滅条件の自動供給): 全要素が 2D+1 以下なら、D より上の層は自動的に消える。
    増加奇数列なら D = (a_k − 1)/2 が最小の選び方。 -/
theorem lm_eq_lmPartial_of_le (A : Fin k → Nat) (hA : ∀ i, 0 < A i) (n D : Nat)
    (hn : n ≤ Finset.univ.sum A) (hD : ∀ i, A i ≤ 2 * D + 1) :
    lm A n = lmPartial A n D := by
  refine lm_eq_lmPartial A hA n D hn (fun d hd => ?_) (fun d hd => ?_)
  · exact overCount_eq_zero A (fun i => by have := hD i; omega) (by omega)
  · exact underCount_eq_zero A (fun i => by have := hD i; omega) (by omega) hn

/-- 定理31(本論文の主定理): 平坦性 ε から lm/deg の上下界が出る。
    定理18(W_D = Γ + (2D+1)/2^k)と合わせると、右辺は Γ で書ける。
    近似は一切使っておらず、ε は各インスタンスで厳密に計算可能である。 -/
theorem sandwich_total (A : Fin k → Nat) (hA : ∀ i, 0 < A i) (n D : Nat) (ε : ℚ)
    (hε : 0 ≤ ε) (hn : n ≤ Finset.univ.sum A) (hD : ∀ i, A i ≤ 2 * D + 1)
    (hDg : 0 < (degCount A n : ℚ))
    (hup : ∀ d ∈ Finset.range D,
      ((overCount A n (d + 1) : ℚ) + (underCount A n (d + 1) : ℚ)) / (degCount A n : ℚ)
        ≤ 2 * (1 + ε) * ((1 : ℚ) / 2) ^ (winCountFin A (d + 1)))
    (hlo : ∀ d ∈ Finset.range D,
      2 * ((1 : ℚ) / 2) ^ (winCountFin A (d + 1)) / (1 + ε)
        ≤ ((overCount A n (d + 1) : ℚ) + (underCount A n (d + 1) : ℚ)) / (degCount A n : ℚ)) :
    winSeriesFin A D / (1 + ε) ≤ (lm A n : ℚ) / (degCount A n : ℚ) ∧
    (lm A n : ℚ) / (degCount A n : ℚ) ≤ (1 + ε) * winSeriesFin A D := by
  rw [lm_eq_lmPartial_of_le A hA n D hn hD]
  exact sandwich_partial A n D ε hε hDg hup hlo

end Total

/- ---- 数値クロスチェック: A6 = (3,5,7,11,13,17), 最大 17 = 2·8+1 なので D = 8 ---- -/

-- 定理29・30: lm = lmPartial を n ≤ 56 の全点で確認
#eval (List.range 57).all (fun n => lm A6 n == lmPartial A6 n 8)   -- 期待 true

-- 中央 n = 28 での各量
#eval [lm A6 28, lmPartial A6 28 8, degCount A6 28]
#eval winSeriesFin A6 8                       -- W_8
#eval (lm A6 28 : ℚ) / (degCount A6 28 : ℚ)   -- lm/deg

end ALT

#print axioms ALT.sum_range_eq_of_vanish
#print axioms ALT.sum_range_congr_of_vanish
#print axioms ALT.overCount_eq_zero_of_sum_lt
#print axioms ALT.underCount_eq_zero_of_lt
#print axioms ALT.underCount_zero_eq_degCount
#print axioms ALT.lm_eq_lmPartial
#print axioms ALT.lm_eq_lmPartial_of_le
#print axioms ALT.sandwich_total
