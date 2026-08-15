/- 算術地形理論(ALT)正典 第2号 (2026-08-07, opus-5 実務セッション・3周目)
   2周目の持ち越し課題のうち Lean 分:
     定理9  (P4)   lm 対称性 lm_A(n) = lm_A(T-n)
     定理10 (P4')  奇数列の地形には平坦辺がない(パリティ論法)
     定理11        平坦辺がなければ「厳密局所最小 = 局所最小」
     定理12・13    List 版 subsetSums と部分列和の橋渡し、表現可能性
   これにより実験側(List/ビットマスク)と理論側(Finset (Fin k))が接続される。 -/
import Pnp.Theory.Landscape

namespace ALT

/- ============ 定理9: lm の補集合対称性(P4) ============ -/

section Symmetry

variable {k : Nat}

/-- 補集合上の数え上げ補題: P S ↔ Q Sᶜ ならフィルタの濃度は等しい -/
theorem card_filter_compl_eq (P Q : Finset (Fin k) → Prop)
    [DecidablePred P] [DecidablePred Q] (h : ∀ S, P S ↔ Q Sᶜ) :
    ((Finset.univ : Finset (Finset (Fin k))).filter P).card =
    ((Finset.univ : Finset (Finset (Fin k))).filter Q).card := by
  have hinj : Function.Injective (compl : Finset (Fin k) → Finset (Fin k)) :=
    fun a b hab => by simpa using congrArg compl hab
  have himg : (Finset.univ.filter P) = (Finset.univ.filter Q).image compl := by
    ext S
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_image]
    constructor
    · intro hp; exact ⟨Sᶜ, (h S).1 hp, compl_compl S⟩
    · rintro ⟨U, hu, rfl⟩; exact (h Uᶜ).2 (by rwa [compl_compl])
  rw [himg, Finset.card_image_of_injective _ hinj]

/-- 補集合の和: Sᶜ の和 + S の和 = 全体の和 -/
theorem sum_compl_add (A : Fin k → Nat) (S : Finset (Fin k)) :
    (Sᶜ).sum A + S.sum A = (Finset.univ : Finset (Fin k)).sum A :=
  Finset.sum_compl_add_sum S A

/-- 1点フリップは補集合と可換 -/
theorem compl_flip (S : Finset (Fin k)) (i : Fin k) :
    (flip S i)ᶜ = flip (Sᶜ) i := by
  unfold flip
  by_cases hi : i ∈ S
  · rw [if_pos hi, if_neg (by simpa using hi), Finset.compl_erase]
  · rw [if_neg hi, if_pos (by simpa using hi), Finset.compl_insert]

/-- エネルギーの補集合対称性: E_{T-n}(Sᶜ) = E_n(S) -/
theorem energy_compl (A : Fin k → Nat) {n : Nat}
    (hn : n ≤ (Finset.univ : Finset (Fin k)).sum A) (S : Finset (Fin k)) :
    energy A ((Finset.univ : Finset (Fin k)).sum A - n) (Sᶜ) = energy A n S := by
  unfold energy
  have hc := sum_compl_add A S
  have hs : S.sum A ≤ (Finset.univ : Finset (Fin k)).sum A := by omega
  have h1 : (Sᶜ).sum A = (Finset.univ : Finset (Fin k)).sum A - S.sum A := by omega
  rw [h1]
  exact ndist_compl hs hn

/-- 厳密局所最小の補集合対称性 -/
theorem isStrictLocalMin_compl (A : Fin k → Nat) {n : Nat}
    (hn : n ≤ (Finset.univ : Finset (Fin k)).sum A) (S : Finset (Fin k)) :
    IsStrictLocalMin A ((Finset.univ : Finset (Fin k)).sum A - n) (Sᶜ) ↔
    IsStrictLocalMin A n S := by
  unfold IsStrictLocalMin
  constructor
  · intro h i
    have hi := h i
    rw [energy_compl A hn S] at hi
    rw [← compl_flip S i, energy_compl A hn (flip S i)] at hi
    exact hi
  · intro h i
    have hi := h i
    rw [← energy_compl A hn S, ← energy_compl A hn (flip S i), compl_flip S i] at hi
    exact hi

/-- 定理9(P4: lm 対称性): T = Σ A、n ≤ T のとき lm_A(T-n) = lm_A(n)。
    2周目に予想として置いた対称性を、配位の補集合による全単射で証明した。 -/
theorem lm_compl (A : Fin k → Nat) {n : Nat}
    (hn : n ≤ (Finset.univ : Finset (Fin k)).sum A) :
    lm A ((Finset.univ : Finset (Fin k)).sum A - n) = lm A n := by
  unfold lm
  refine card_filter_compl_eq _ _ (fun S => ?_)
  have h := isStrictLocalMin_compl A hn (Sᶜ)
  rwa [compl_compl] at h

end Symmetry

/- ============ 定理10・11: 奇数列には平坦辺がない(P4') ============ -/

section Parity

variable {k : Nat}

/-- 距離のパリティ: |a - b| ≡ a + b (mod 2) -/
theorem ndist_mod_two (a b : Nat) : ndist a b % 2 = (a + b) % 2 := by
  unfold ndist; split <;> omega

/-- 1点フリップは和を A i だけずらす(向きは2通り) -/
theorem flip_sum (A : Fin k → Nat) (S : Finset (Fin k)) (i : Fin k) :
    (flip S i).sum A + A i = S.sum A ∨ (flip S i).sum A = A i + S.sum A := by
  unfold flip
  by_cases hi : i ∈ S
  · rw [if_pos hi]; exact Or.inl (sum_erase_add_of_mem A hi)
  · rw [if_neg hi]; exact Or.inr (Finset.sum_insert hi)

/-- 定理10(P4'): 全要素が奇数なら、隣接する2配位のエネルギーは決して等しくない
    (地形に平坦な辺が存在しない)。パリティ論法。 -/
theorem no_flat_edge {A : Fin k → Nat} (hodd : ∀ i, A i % 2 = 1)
    (n : Nat) (S : Finset (Fin k)) (i : Fin k) :
    energy A n S ≠ energy A n (flip S i) := by
  unfold energy
  have hp : ndist (S.sum A) n % 2 ≠ ndist ((flip S i).sum A) n % 2 := by
    rw [ndist_mod_two, ndist_mod_two]
    have ho := hodd i
    rcases flip_sum A S i with h | h <;> omega
  intro hEq
  exact hp (by rw [hEq])

/-- 定理11: 平坦辺がないとき、厳密局所最小と(非厳密)局所最小は一致する。
    奇数列(素数列を含む)では lm がどちらの定義でも同じ量になることを保証する。 -/
theorem isStrictLocalMin_iff_le_of_odd {A : Fin k → Nat} (hodd : ∀ i, A i % 2 = 1)
    (n : Nat) (S : Finset (Fin k)) :
    IsStrictLocalMin A n S ↔ ∀ i : Fin k, energy A n S ≤ energy A n (flip S i) := by
  unfold IsStrictLocalMin
  constructor
  · intro h i; exact le_of_lt (h i)
  · intro h i
    rcases lt_or_eq_of_le (h i) with hlt | heq
    · exact hlt
    · exact absurd heq (no_flat_edge hodd n S i)

end Parity

/- ============ 定理12・13: 実験側(List)と理論側の橋 ============ -/

section Bridge

/-- 定理12: subsetSums の元 = 部分列の和。
    実験側のビットマスク列挙が「部分列を走ること」に他ならないことの形式化。 -/
theorem mem_subsetSums_iff_sublist (A : List Nat) (s : Nat) :
    s ∈ subsetSums A ↔ ∃ B : List Nat, B.Sublist A ∧ B.sum = s := by
  induction A generalizing s with
  | nil =>
    simp only [subsetSums, List.mem_singleton]
    constructor
    · rintro rfl; exact ⟨[], List.Sublist.refl _, rfl⟩
    · rintro ⟨B, hB, rfl⟩; rw [List.sublist_nil.mp hB]; rfl
  | cons x xs ih =>
    simp only [subsetSums, List.mem_append, List.mem_map]
    constructor
    · rintro (h | ⟨t, ht, rfl⟩)
      · obtain ⟨B, hB, hs⟩ := (ih s).1 h
        exact ⟨B, hB.cons x, hs⟩
      · obtain ⟨B, hB, hs⟩ := (ih t).1 ht
        refine ⟨x :: B, hB.cons_cons x, ?_⟩
        simp [hs, Nat.add_comm]
    · rintro ⟨B, hB, rfl⟩
      cases hB with
      | cons _ h => exact Or.inl ((ih _).2 ⟨B, h, rfl⟩)
      | cons_cons _ h =>
        rename_i B'
        refine Or.inr ⟨B'.sum, (ih _).2 ⟨B', h, rfl⟩, ?_⟩
        simp [Nat.add_comm]

/-- 定理13(表現可能性): gs A n = 0 ⟺ n が A の部分列の和として表せる。
    地形の基底エネルギーが 0 という物理的条件を、純粋な数論の条件に翻訳する。 -/
theorem gs_eq_zero_iff (A : List Nat) (n : Nat) :
    gs A n = 0 ↔ ∃ B : List Nat, B.Sublist A ∧ B.sum = n := by
  constructor
  · intro h
    obtain ⟨s, hs, hgs⟩ := gs_attained A n
    rw [h] at hgs
    have hsn : s = n := by unfold ndist at hgs; split at hgs <;> omega
    subst hsn
    exact (mem_subsetSums_iff_sublist A s).1 hs
  · rintro ⟨B, hB, rfl⟩
    have hmem := (mem_subsetSums_iff_sublist A B.sum).2 ⟨B, hB, rfl⟩
    have hle := gs_le_of_mem hmem B.sum
    have hz : ndist B.sum B.sum = 0 := by unfold ndist; simp
    omega

end Bridge

/- ---- 数値クロスチェック(定理の内容が実験側と一致することの確認) ---- -/

-- 定理9: A6 = (3,5,7,11,13,17), T = 56。n ≤ T の全点で lm(T-n) = lm(n)
#eval (List.range 57).all (fun n => lm A6 (56 - n) == lm A6 n)   -- 期待 true

-- 定理11: 奇数列なので厳密局所最小 = 非厳密局所最小(全 n・全配位で一致)
#eval (List.range 57).all (fun n =>
  lm A6 n ==
    ((Finset.univ : Finset (Finset (Fin 6))).filter
      (fun S => ∀ i : Fin 6, energy A6 n S ≤ energy A6 n (flip S i))).card)  -- 期待 true

-- 定理13: gs = 0 ⟺ 表現可能。奇素数6項で表現できない n の一覧
-- 実測 [1, 2, 4, 6, 9, 47, 50, 52, 54, 55]。n ↦ 56-n で閉じており(1↔55, 2↔54,
-- 4↔52, 6↔50, 9↔47)、定理4(gs補集合対称性)の独立な数値確認にもなっている。
#eval (List.range 57).filter (fun n => gs [3,5,7,11,13,17] n != 0)

end ALT

#print axioms ALT.card_filter_compl_eq
#print axioms ALT.compl_flip
#print axioms ALT.energy_compl
#print axioms ALT.isStrictLocalMin_compl
#print axioms ALT.lm_compl
#print axioms ALT.ndist_mod_two
#print axioms ALT.no_flat_edge
#print axioms ALT.isStrictLocalMin_iff_le_of_odd
#print axioms ALT.mem_subsetSums_iff_sublist
#print axioms ALT.gs_eq_zero_iff
