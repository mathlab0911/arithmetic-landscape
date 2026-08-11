import Pnp.Theory.Bridge

/- ============ 極値定理: Γ の値域と、両端を実現する集合の一意性 ============

   r120。Γ の定義を「層の形」

       Γ(A) = 1 + 2 Σ_{d=1}^{(M-1)/2} 2^{−N_A(d)},   M = max A

   に変えたので、値域が定義から直接読める。各項 2^{−N_A(d)} は

       2^{−d} ≤ 2^{−N_A(d)} ≤ 1

   に挟まれる。上は N_A(d) ≥ 0 から。下は N_A(d) ≤ d から——2d 以下の奇数は
   1,3,…,2d−1 のちょうど d 個しかない。両端は両端の集合で実現される:
   上端は {M}(最も疎)、下端は {1,3,…,M}(最も密)。

   ここでは windowSeries A D をそのまま扱う。D = (M−1)/2 と置けば
   Bridge.lean の windowSeries_eq_gapSeries により Γ そのものになる。

   注意: 2026-08-11 のセッションでこれらの定理を一度書き上げたが、作業領域が
   リセットされて失われた。本ファイルは書き直しであり、証明は同じ骨格による。 -/

namespace ALT

open Finset

section Extremal

variable {A : List Nat}

/-- (1/2)^n は n について単調減少。 -/
theorem half_anti : Antitone (fun n : Nat => ((1 : ℚ) / 2) ^ n) :=
  (pow_right_strictAnti₀ (by norm_num) (by norm_num)).antitone

/-- 各項は 1 以下。 -/
theorem half_pow_le_one (n : Nat) : ((1 : ℚ) / 2) ^ n ≤ 1 := by
  simpa using half_anti (Nat.zero_le n)

/-- 幾何級数 Σ_{d=1}^{D} 2^{−d} = 1 − 2^{−D}。 -/
theorem half_geom (D : Nat) :
    ∑ d ∈ Finset.range D, ((1 : ℚ) / 2) ^ (d + 1) = 1 - ((1 : ℚ) / 2) ^ D := by
  induction D with
  | zero => simp
  | succ m ih =>
    rw [Finset.sum_range_succ, ih, pow_succ]
    ring

/-- 相異なる奇数のうち 2d 以下のものは高々 d 個。極値定理の下限はこの一行に尽きる。
    写像 a ↦ (a−1)/2 が {2d 以下の A の元} を {0,…,d−1} に単射で送る。 -/
theorem winCount_le (hlt : A.Pairwise (· < ·)) (hodd : ∀ a ∈ A, a % 2 = 1) (d : Nat) :
    winCount A d ≤ d := by
  classical
  unfold winCount
  rw [List.countP_eq_length_filter]
  have hnd : (A.filter (fun a => decide (a ≤ 2 * d))).Nodup := (hlt.filter _).nodup
  have hinj : ∀ a ∈ A.filter (fun a => decide (a ≤ 2 * d)),
      ∀ b ∈ A.filter (fun a => decide (a ≤ 2 * d)), (a - 1) / 2 = (b - 1) / 2 → a = b := by
    intro a ha b hb hab
    have h3 : a % 2 = 1 := hodd a (List.mem_of_mem_filter ha)
    have h4 : b % 2 = 1 := hodd b (List.mem_of_mem_filter hb)
    omega
  have hmnd : ((A.filter (fun a => decide (a ≤ 2 * d))).map (fun a => (a - 1) / 2)).Nodup :=
    hnd.map_on hinj
  have hsub : ((A.filter (fun a => decide (a ≤ 2 * d))).map
      (fun a => (a - 1) / 2)).toFinset ⊆ Finset.range d := by
    intro x hx
    rw [List.mem_toFinset, List.mem_map] at hx
    obtain ⟨a, ha, rfl⟩ := hx
    have h1 : a ∈ A := List.mem_of_mem_filter ha
    have h2 : a ≤ 2 * d := by
      have := List.of_mem_filter ha
      simpa using this
    have h3 : a % 2 = 1 := hodd a h1
    simp only [Finset.mem_range]
    omega
  calc (A.filter (fun a => decide (a ≤ 2 * d))).length
      = ((A.filter (fun a => decide (a ≤ 2 * d))).map (fun a => (a - 1) / 2)).length := by simp
    _ = (((A.filter (fun a => decide (a ≤ 2 * d))).map
            (fun a => (a - 1) / 2)).toFinset).card := (List.toFinset_card_of_nodup hmnd).symm
    _ ≤ (Finset.range d).card := Finset.card_le_card hsub
    _ = d := Finset.card_range d

/-- 逆向き。`A` が `2d` 以下の奇数をすべて含むなら `d ≤ winCount A d`。 -/
theorem le_winCount (hlt : A.Pairwise (· < ·)) {d : Nat}
    (hall : ∀ j, j < d → (2 * j + 1) ∈ A) : d ≤ winCount A d := by
  classical
  unfold winCount
  rw [List.countP_eq_length_filter]
  have hnd : (A.filter (fun a => decide (a ≤ 2 * d))).Nodup := (hlt.filter _).nodup
  have hOdds : ((List.range d).map (fun j => 2 * j + 1)).Nodup := by
    apply List.Nodup.map _ List.nodup_range
    intro x y hxy
    -- 仮定が β 簡約されていないと omega はラムダの中を見られない(既知の罠)。
    dsimp only at hxy
    omega
  have hsub : ((List.range d).map (fun j => 2 * j + 1)).toFinset ⊆
      (A.filter (fun a => decide (a ≤ 2 * d))).toFinset := by
    intro x hx
    rw [List.mem_toFinset, List.mem_map] at hx
    obtain ⟨j, hj, rfl⟩ := hx
    rw [List.mem_range] at hj
    rw [List.mem_toFinset, List.mem_filter]
    refine ⟨hall j hj, ?_⟩
    simp only [decide_eq_true_eq]
    omega
  calc d = ((List.range d).map (fun j => 2 * j + 1)).length := by simp
    _ = (((List.range d).map (fun j => 2 * j + 1)).toFinset).card :=
        (List.toFinset_card_of_nodup hOdds).symm
    _ ≤ ((A.filter (fun a => decide (a ≤ 2 * d))).toFinset).card := Finset.card_le_card hsub
    _ = (A.filter (fun a => decide (a ≤ 2 * d))).length := List.toFinset_card_of_nodup hnd

/-- **極値定理**。相異なる奇数の列 `A` の全要素が `2D+1` 以下なら
    `3 − 2·2^{−D} ≤ windowSeries A D ≤ 1 + 2D`。
    `D = (max A − 1)/2` と取れば左辺は `3 − 2^{1−D}`、右辺は `max A`。 -/
theorem windowSeries_bounds (hlt : A.Pairwise (· < ·)) (hodd : ∀ a ∈ A, a % 2 = 1) (D : Nat) :
    3 - 2 * ((1 : ℚ) / 2) ^ D ≤ windowSeries A D ∧ windowSeries A D ≤ 1 + 2 * D := by
  unfold windowSeries windowSum
  constructor
  · have hterm : ∀ d ∈ Finset.range D,
        ((1 : ℚ) / 2) ^ (d + 1) ≤ ((1 : ℚ) / 2) ^ (winCount A (d + 1)) :=
      fun d _ => half_anti (winCount_le hlt hodd (d + 1))
    have hs := Finset.sum_le_sum hterm
    rw [half_geom D] at hs
    linarith
  · have hterm : ∀ d ∈ Finset.range D, ((1 : ℚ) / 2) ^ (winCount A (d + 1)) ≤ 1 :=
      fun d _ => half_pow_le_one _
    have hs := Finset.sum_le_sum hterm
    simp only [Finset.sum_const, Finset.card_range, nsmul_eq_mul, mul_one] at hs
    linarith

/-- 上端の一意性。`windowSeries A D = 1 + 2D` は「`2D` 以下の元が無い」と同値。 -/
theorem windowSeries_eq_max_iff (D : Nat) :
    windowSeries A D = 1 + 2 * D ↔ ∀ d, 1 ≤ d → d ≤ D → winCount A d = 0 := by
  unfold windowSeries windowSum
  constructor
  · intro h d hd1 hdD
    by_contra hne
    have hlt1 : ((1 : ℚ) / 2) ^ (winCount A d) < 1 := by
      have h1 : 1 ≤ winCount A d := Nat.one_le_iff_ne_zero.mpr hne
      calc ((1 : ℚ) / 2) ^ (winCount A d) ≤ ((1 : ℚ) / 2) ^ 1 := half_anti h1
        _ < 1 := by norm_num
    have hmem : d - 1 ∈ Finset.range D := by simp only [Finset.mem_range]; omega
    have hrw : d - 1 + 1 = d := by omega
    have hstrict :
        ∑ e ∈ Finset.range D, ((1 : ℚ) / 2) ^ (winCount A (e + 1))
          < ∑ _e ∈ Finset.range D, (1 : ℚ) := by
      refine Finset.sum_lt_sum (fun e _ => half_pow_le_one _) ⟨d - 1, hmem, ?_⟩
      rw [hrw]; exact hlt1
    simp only [Finset.sum_const, Finset.card_range, nsmul_eq_mul, mul_one] at hstrict
    linarith
  · intro h
    have hone : ∀ e ∈ Finset.range D, ((1 : ℚ) / 2) ^ (winCount A (e + 1)) = 1 := by
      intro e he
      simp only [Finset.mem_range] at he
      rw [h (e + 1) (by omega) (by omega), pow_zero]
    have hsum : ∑ e ∈ Finset.range D, ((1 : ℚ) / 2) ^ (winCount A (e + 1)) = (D : ℚ) := by
      rw [Finset.sum_congr rfl hone]
      simp
    rw [hsum]

/-- 下端の一意性。`windowSeries A D = 3 − 2·2^{−D}` は
    「`A` が `2D` 以下の奇数をすべて含む」と同値。 -/
theorem windowSeries_min_iff_all_odds
    (hlt : A.Pairwise (· < ·)) (hodd : ∀ a ∈ A, a % 2 = 1) (D : Nat) :
    windowSeries A D = 3 - 2 * ((1 : ℚ) / 2) ^ D ↔ ∀ j, j < D → (2 * j + 1) ∈ A := by
  constructor
  · intro h j hj
    -- 等号なら各層で等号。まず winCount A (j+1) = j+1 を出す。
    have hall : ∀ d ∈ Finset.range D, winCount A (d + 1) = d + 1 := by
      intro d hd
      by_contra hne
      have hlt' : winCount A (d + 1) < d + 1 :=
        lt_of_le_of_ne (winCount_le hlt hodd (d + 1)) hne
      have hstrict : ((1 : ℚ) / 2) ^ (d + 1) < ((1 : ℚ) / 2) ^ (winCount A (d + 1)) :=
        pow_lt_pow_right_of_lt_one₀ (by norm_num) (by norm_num) hlt'
      have hsum :
          ∑ e ∈ Finset.range D, ((1 : ℚ) / 2) ^ (e + 1)
            < ∑ e ∈ Finset.range D, ((1 : ℚ) / 2) ^ (winCount A (e + 1)) :=
        Finset.sum_lt_sum (fun e _ => half_anti (winCount_le hlt hodd (e + 1))) ⟨d, hd, hstrict⟩
      rw [half_geom D] at hsum
      unfold windowSeries windowSum at h
      linarith
    -- winCount A (j+1) = j+1 かつ 2j+1 ∉ A は矛盾する。
    have hcount : winCount A (j + 1) = j + 1 := hall j (by simpa using hj)
    by_contra hnot
    have hbound : winCount A (j + 1) ≤ j := by
      classical
      unfold winCount
      rw [List.countP_eq_length_filter]
      have hnd : (A.filter (fun a => decide (a ≤ 2 * (j + 1)))).Nodup := (hlt.filter _).nodup
      have hinj : ∀ a ∈ A.filter (fun a => decide (a ≤ 2 * (j + 1))),
          ∀ b ∈ A.filter (fun a => decide (a ≤ 2 * (j + 1))),
          (a - 1) / 2 = (b - 1) / 2 → a = b := by
        intro a ha b hb hab
        have h3 : a % 2 = 1 := hodd a (List.mem_of_mem_filter ha)
        have h4 : b % 2 = 1 := hodd b (List.mem_of_mem_filter hb)
        omega
      have hmnd : ((A.filter (fun a => decide (a ≤ 2 * (j + 1)))).map
          (fun a => (a - 1) / 2)).Nodup := hnd.map_on hinj
      have hsub : ((A.filter (fun a => decide (a ≤ 2 * (j + 1)))).map
          (fun a => (a - 1) / 2)).toFinset ⊆ Finset.range j := by
        intro x hx
        rw [List.mem_toFinset, List.mem_map] at hx
        obtain ⟨a, ha, rfl⟩ := hx
        have h1 : a ∈ A := List.mem_of_mem_filter ha
        have h2 : a ≤ 2 * (j + 1) := by have := List.of_mem_filter ha; simpa using this
        have h3 : a % 2 = 1 := hodd a h1
        have h4 : a ≠ 2 * j + 1 := by rintro rfl; exact hnot h1
        simp only [Finset.mem_range]
        omega
      calc (A.filter (fun a => decide (a ≤ 2 * (j + 1)))).length
          = ((A.filter (fun a => decide (a ≤ 2 * (j + 1)))).map
              (fun a => (a - 1) / 2)).length := by simp
        _ = (((A.filter (fun a => decide (a ≤ 2 * (j + 1)))).map
                (fun a => (a - 1) / 2)).toFinset).card :=
              (List.toFinset_card_of_nodup hmnd).symm
        _ ≤ (Finset.range j).card := Finset.card_le_card hsub
        _ = j := Finset.card_range j
    omega
  · intro h
    have hall : ∀ d ∈ Finset.range D,
        ((1 : ℚ) / 2) ^ (winCount A (d + 1)) = ((1 : ℚ) / 2) ^ (d + 1) := by
      intro d hd
      simp only [Finset.mem_range] at hd
      have hge : d + 1 ≤ winCount A (d + 1) :=
        le_winCount hlt (fun j hj => h j (by omega))
      have hle : winCount A (d + 1) ≤ d + 1 := winCount_le hlt hodd (d + 1)
      rw [le_antisymm hle hge]
    unfold windowSeries windowSum
    rw [Finset.sum_congr rfl hall, half_geom D]
    ring

/-- **狭義単調性**。`max A` を変えずに元を足すと `windowSeries` は狭義に減る。
    「Γ は疎さを測る」という読みは、この定理が保証している。 -/
theorem windowSeries_insert_lt (A : List Nat) {b D : Nat} (hD : 1 ≤ D) (hb : b ≤ 2 * D) :
    windowSeries (b :: A) D < windowSeries A D := by
  unfold windowSeries windowSum
  have hmono : ∀ d ∈ Finset.range D,
      ((1 : ℚ) / 2) ^ (winCount (b :: A) (d + 1)) ≤ ((1 : ℚ) / 2) ^ (winCount A (d + 1)) := by
    intro d _
    apply half_anti
    unfold winCount
    rw [List.countP_cons]
    omega
  have hd0 : D - 1 ∈ Finset.range D := by simp only [Finset.mem_range]; omega
  have hstrict : ((1 : ℚ) / 2) ^ (winCount (b :: A) (D - 1 + 1))
      < ((1 : ℚ) / 2) ^ (winCount A (D - 1 + 1)) := by
    apply pow_lt_pow_right_of_lt_one₀ (by norm_num) (by norm_num)
    unfold winCount
    rw [List.countP_cons]
    have hone : (if decide (b ≤ 2 * (D - 1 + 1)) = true then 1 else 0) = 1 := by
      rw [if_pos]
      simp only [decide_eq_true_eq]
      omega
    omega
  have := Finset.sum_lt_sum hmono ⟨D - 1, hd0, hstrict⟩
  linarith

end Extremal

-- 評価による確認(証明ではない。定理は上で証明済み)。
section Eval

-- 上端: Γ({73}) = 73
#eval windowSeries [73] 36
-- 下端: Γ({1,3,…,73}) = 3 − 2^{−35} = 103079215103/34359738368
#eval windowSeries ((List.range 37).map (fun j => 2 * j + 1)) 36
-- 奇素数 20 個: Γ(P_20) = 1402281/262144
#eval windowSeries [3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73] 36
-- 単調性の実例: Γ({3,5,7}) < Γ({5,7})
#eval decide (windowSeries [3,5,7] 3 < windowSeries [5,7] 3)

end Eval

#print axioms ALT.winCount_le
#print axioms ALT.le_winCount
#print axioms ALT.windowSeries_bounds
#print axioms ALT.windowSeries_eq_max_iff
#print axioms ALT.windowSeries_min_iff_all_odds
#print axioms ALT.windowSeries_insert_lt

end ALT
