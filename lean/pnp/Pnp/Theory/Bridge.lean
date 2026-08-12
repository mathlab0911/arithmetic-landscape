/- 算術地形理論(ALT)正典 第3号 (2026-08-07, opus-5 実務セッション・4周目)
   3周目の持ち越し:
     定理14〜16  List 版 subsetSums と Finset (Fin k) 版配位空間の完全な橋
     定理17〜19  窓級数と gapSeries を結ぶ恒等式(増加奇数列・境界項つき)
   これで「実験のビットマスク列挙」「gs(List版)」「energy(Finset版)」が
   完全に同一の対象であることが形式的に確定し、窓級数が局所最小の窓の総和として
   純算術的に特徴づけられる。
   (r132: ここも「= gapSeries 恒等式」「Γ が」と書いていた。境界項があり、正典の
    `gapSeries` は論文の Γ とは別物である。下の該当節の注記を見よ。) -/
import Pnp.Theory.Symmetry

namespace ALT

/- ============ 定理14〜16: Finset (Fin k) 版との完全な橋 ============ -/

section FinBridge

variable {k : Nat}

/-- Fin (k+1) の Finset を「0 を含むか」と「1..k の部分」に分解する和の公式 -/
theorem sum_fin_succ (A : Fin (k + 1) → Nat) (S : Finset (Fin (k + 1))) :
    S.sum A =
      (Finset.univ.filter (fun j : Fin k => j.succ ∈ S)).sum (fun j => A j.succ)
      + (if (0 : Fin (k + 1)) ∈ S then A 0 else 0) := by
  classical
  set T := Finset.univ.filter (fun j : Fin k => j.succ ∈ S) with hT
  set M := T.map ⟨Fin.succ, Fin.succ_injective k⟩ with hM
  have hMmem : ∀ i : Fin (k + 1), i ∈ M ↔ (i ≠ 0 ∧ i ∈ S) := by
    intro i
    simp only [hM, hT, Finset.mem_map, Finset.mem_filter, Finset.mem_univ, true_and,
      Function.Embedding.coeFn_mk]
    constructor
    · rintro ⟨j, hj, rfl⟩; exact ⟨Fin.succ_ne_zero j, hj⟩
    · rintro ⟨hne, hi⟩
      rcases Fin.eq_zero_or_eq_succ i with rfl | ⟨j, rfl⟩
      · exact absurd rfl hne
      · exact ⟨j, hi, rfl⟩
  have hMsum : M.sum A = T.sum (fun j => A j.succ) := by
    rw [hM, Finset.sum_map]; rfl
  by_cases h0 : (0 : Fin (k + 1)) ∈ S
  · have hnot : (0 : Fin (k + 1)) ∉ M := by
      intro hc; exact ((hMmem 0).1 hc).1 rfl
    have hSeq : S = insert 0 M := by
      ext i
      simp only [Finset.mem_insert, hMmem i]
      constructor
      · intro hi
        by_cases hz : i = 0
        · exact Or.inl hz
        · exact Or.inr ⟨hz, hi⟩
      · rintro (rfl | ⟨-, hi⟩)
        · exact h0
        · exact hi
    rw [if_pos h0, hSeq, Finset.sum_insert hnot, hMsum]
    omega
  · have hSeq : S = M := by
      ext i
      simp only [hMmem i]
      constructor
      · intro hi
        refine ⟨?_, hi⟩
        rintro rfl; exact h0 hi
      · rintro ⟨-, hi⟩; exact hi
    rw [if_neg h0, hSeq, hMsum, Nat.add_zero]

/-- 定理14: 配位の和の集合は「0 を使わない/使う」の2択で再帰する -/
theorem exists_sum_succ_iff (A : Fin (k + 1) → Nat) (s : Nat) :
    (∃ S : Finset (Fin (k + 1)), S.sum A = s) ↔
    (∃ T : Finset (Fin k), T.sum (fun j => A j.succ) = s) ∨
    (∃ T : Finset (Fin k), T.sum (fun j => A j.succ) + A 0 = s) := by
  classical
  have hmap : ∀ T : Finset (Fin k),
      (T.map ⟨Fin.succ, Fin.succ_injective k⟩).sum A = T.sum (fun j => A j.succ) := by
    intro T; rw [Finset.sum_map]; rfl
  have hzero : ∀ T : Finset (Fin k),
      (0 : Fin (k + 1)) ∉ T.map ⟨Fin.succ, Fin.succ_injective k⟩ := by
    intro T hmem
    simp only [Finset.mem_map, Function.Embedding.coeFn_mk] at hmem
    obtain ⟨j, -, hj⟩ := hmem
    exact Fin.succ_ne_zero j hj
  constructor
  · rintro ⟨S, rfl⟩
    rw [sum_fin_succ A S]
    by_cases h : (0 : Fin (k + 1)) ∈ S
    · rw [if_pos h]; exact Or.inr ⟨_, rfl⟩
    · rw [if_neg h, Nat.add_zero]
      exact Or.inl ⟨_, rfl⟩
  · rintro (⟨T, rfl⟩ | ⟨T, rfl⟩)
    · exact ⟨T.map ⟨Fin.succ, Fin.succ_injective k⟩, hmap T⟩
    · refine ⟨insert 0 (T.map ⟨Fin.succ, Fin.succ_injective k⟩), ?_⟩
      rw [Finset.sum_insert (hzero T), hmap T]
      omega

/-- 定理15(完全な橋): List 版の部分和集合と Finset (Fin k) 版の配位和集合は一致する。
    実験側(ビットマスク列挙)と理論側(配位空間)が同じ対象であることの形式的保証。 -/
theorem mem_subsetSums_ofFn_iff :
    ∀ {k : Nat} (A : Fin k → Nat) (s : Nat),
      s ∈ subsetSums (List.ofFn A) ↔ ∃ S : Finset (Fin k), S.sum A = s := by
  intro k
  induction k with
  | zero =>
    intro A s
    simp only [List.ofFn_zero, subsetSums, List.mem_singleton]
    constructor
    · rintro rfl; exact ⟨∅, rfl⟩
    · rintro ⟨S, rfl⟩
      rw [Finset.eq_empty_of_isEmpty S, Finset.sum_empty]
  | succ k ih =>
    intro A s
    rw [List.ofFn_succ]
    simp only [subsetSums, List.mem_append, List.mem_map]
    rw [exists_sum_succ_iff A s]
    constructor
    · rintro (h | ⟨t, ht, rfl⟩)
      · exact Or.inl ((ih _ s).1 h)
      · obtain ⟨T, hT⟩ := (ih _ t).1 ht
        exact Or.inr ⟨T, by omega⟩
    · rintro (⟨T, rfl⟩ | ⟨T, rfl⟩)
      · exact Or.inl ((ih _ _).2 ⟨T, rfl⟩)
      · exact Or.inr ⟨T.sum (fun j => A j.succ), (ih _ _).2 ⟨T, rfl⟩, by omega⟩

/-- 定理16(gs = エネルギー最小): List 版の基底状態値は、Finset 版のエネルギーの
    配位全体にわたる最小値に一致する(達成配位つき)。 -/
theorem gs_ofFn_eq_energy_min (A : Fin k → Nat) (n : Nat) :
    ∃ S : Finset (Fin k),
      gs (List.ofFn A) n = energy A n S ∧
      ∀ T : Finset (Fin k), gs (List.ofFn A) n ≤ energy A n T := by
  obtain ⟨s, hs, hgs⟩ := gs_attained (List.ofFn A) n
  obtain ⟨S, hS⟩ := (mem_subsetSums_ofFn_iff A s).1 hs
  refine ⟨S, ?_, ?_⟩
  · unfold energy; rw [hS]; exact hgs
  · intro T
    exact gs_le_of_mem ((mem_subsetSums_ofFn_iff A (T.sum A)).2 ⟨T, rfl⟩) n

end FinBridge

/- 数値クロスチェック: Fin 版と List 版が同じ表現可能性を与える -/
#eval List.ofFn A4                                        -- 期待 [3, 5, 7, 11]
#eval (List.range 30).all (fun n =>
  (decide (gs (List.ofFn A4) n = 0)) ==
  (decide (∃ S : Finset (Fin 4), S.sum A4 = n)))          -- 期待 true

/- ============ 定理17〜18: 窓級数と gapSeries を結ぶ恒等式 ============
   分類定理(定理5・6)より、誤差 d の配位が厳密局所最小である条件は
   「小さい要素(a_i ≤ 2d)を選ばない/選ぶ」という制約だけで書ける。
   各要素を独立に見たときこの制約を満たす配位の割合は 2^{−#{i : a_i ≤ 2d}} であり、
   d を走らせて足し上げた量
       W_D(A) = 1 + 2 Σ_{d=1}^{D} 2^{−#{i : a_i ≤ 2d}}
   が「局所最小数 / 基底状態数 r_A(n)」の予測値になる。

   ★ 名前の注意(r132)。この節の見出しは長く「窓級数 = gapSeries 恒等式」で、本文は
   「W が Γ = gapSeries と厳密に一致する」と書いていた。どちらも、下の定理が実際に
   証明していることではない。二点:
     (1) 一致は厳密ではなく境界項がある: W_D(A) = gapSeries A + (2D+1)/2^{|A|}。
     (2) 正典の識別子 `gapSeries` は列挙形 Σ a_j 2^{−j} であり、r120 以降 論文が
         Γ と呼ぶ層の形 1 + 2 Σ_d 2^{−N_A(d)} とは a_k/2^{|A|} だけ異なる別物である
         (`Landscape.lean` の `gapSeries` の注記が対応表)。
   つまり「= Γ」と書いた瞬間に、同名異物と、落とした境界項の二つを同時に踏んでいた。
   定理の主張は下の `windowSeries_eq_gapSeries` が述べるとおりのものであり、この
   コメントはそれを言い換えるのではなく、それを指すだけにしてある。 -/

section WindowSeries

/-- 窓カウント N_A(d) = #{i : a_i ≤ 2d} -/
def winCount (A : List Nat) (d : Nat) : Nat := A.countP (fun a => decide (a ≤ 2 * d))

/-- 窓和 Σ_{d=1}^{D} 2^{−N_A(d)} -/
def windowSum (A : List Nat) (D : Nat) : ℚ :=
  ∑ d ∈ Finset.range D, ((1 : ℚ) / 2) ^ (winCount A (d + 1))

/-- 窓級数 W_D(A) = 1 + 2 Σ_{d=1}^{D} 2^{−N_A(d)} -/
def windowSeries (A : List Nat) (D : Nat) : ℚ := 1 + 2 * windowSum A D

/-- 定理17(項ごとの分解): 昇順・a が最小のとき、
    2^{−N_{a::t}(d)} = (2^{−N_t(d)} + [2d < a]) / 2 -/
theorem window_term_cons {a : Nat} {t : List Nat} (hmin : ∀ b ∈ t, a ≤ b) (d : Nat) :
    ((1 : ℚ) / 2) ^ (winCount (a :: t) d)
      = (((1 : ℚ) / 2) ^ (winCount t d) + (if 2 * d < a then 1 else 0)) / 2 := by
  unfold winCount
  rw [List.countP_cons]
  by_cases h : a ≤ 2 * d
  · have hif : (if 2 * d < a then (1 : ℚ) else 0) = 0 := by
      rw [if_neg (by omega)]
    rw [hif, if_pos (by simpa using h)]
    have : t.countP (fun b => decide (b ≤ 2 * d)) + 1
        = (t.countP (fun b => decide (b ≤ 2 * d))) + 1 := rfl
    rw [pow_succ]
    ring
  · have hzero : t.countP (fun b => decide (b ≤ 2 * d)) = 0 := by
      rw [List.countP_eq_zero]
      intro b hb
      have := hmin b hb
      simp only [decide_eq_true_eq]
      omega
    rw [hzero, if_neg (by simpa using h), if_pos (by omega)]
    norm_num

/-- 定理18(窓級数 = Γ の恒等式): A が昇順に並んだ奇数の列で、
    すべての要素が 2D+1 以下なら W_D(A) = Γ(A) + (2D+1)/2^{|A|}。
    Γ が「局所最小の窓の総和」という純算術的な意味をもつことの厳密形。 -/
theorem windowSeries_eq_gapSeries :
    ∀ (A : List Nat) (D : Nat), A.Pairwise (· ≤ ·) → (∀ a ∈ A, a % 2 = 1) →
      (∀ a ∈ A, a ≤ 2 * D + 1) →
      windowSeries A D = gapSeries A + (2 * (D : ℚ) + 1) / 2 ^ A.length := by
  intro A
  induction A with
  | nil =>
    intro D _ _ _
    unfold windowSeries windowSum gapSeries winCount
    simp only [List.countP_nil, pow_zero, Finset.sum_const, Finset.card_range,
      nsmul_eq_mul, mul_one, List.length_nil]
    ring
  | cons a t ih =>
    intro D hsorted hodd hle
    have hmin : ∀ b ∈ t, a ≤ b := (List.pairwise_cons.mp hsorted).1
    have ht : t.Pairwise (· ≤ ·) := (List.pairwise_cons.mp hsorted).2
    have ha : a % 2 = 1 := hodd a (by simp)
    have haD : a ≤ 2 * D + 1 := hle a (by simp)
    have hIH := ih D ht (fun b hb => hodd b (by simp [hb])) (fun b hb => hle b (by simp [hb]))
    -- 窓和の再帰: windowSum (a::t) D = (windowSum t D + a/2) / 2
    have hcnt : ∑ d ∈ Finset.range D, (if 2 * (d + 1) < a then (1 : ℚ) else 0)
        = ((a / 2 : Nat) : ℚ) := by
      have hfil : (Finset.range D).filter (fun d => 2 * (d + 1) < a)
          = Finset.range (a / 2) := by
        ext d
        simp only [Finset.mem_filter, Finset.mem_range]
        omega
      rw [← Finset.sum_filter, hfil, Finset.sum_const, Finset.card_range,
        nsmul_eq_mul, mul_one]
    have hws : windowSum (a :: t) D = (windowSum t D + ((a / 2 : Nat) : ℚ)) / 2 := by
      unfold windowSum
      rw [Finset.sum_congr rfl (fun d _ => window_term_cons hmin (d + 1)),
        ← Finset.sum_div, Finset.sum_add_distrib, hcnt]
    -- 奇数のキャスト: (a/2 : ℚ) = (a - 1)/2
    have hcast : ((a / 2 : Nat) : ℚ) = ((a : ℚ) - 1) / 2 := by
      have h2 : a = 2 * (a / 2) + 1 := by omega
      have h3 : (a : ℚ) = 2 * ((a / 2 : Nat) : ℚ) + 1 := by
        conv_lhs => rw [h2]
        push_cast
        ring
      linarith
    -- 代数
    have hP : ((2 : ℚ)) ^ t.length ≠ 0 := by positivity
    have hWt : windowSum t D
        = (gapSeries t + (2 * (D : ℚ) + 1) / 2 ^ t.length - 1) / 2 := by
      unfold windowSeries at hIH; linarith
    unfold windowSeries
    rw [hws, hWt, hcast]
    simp only [gapSeries, List.length_cons, pow_succ]
    field_simp
    ring

/- 数値クロスチェック: 恒等式が実際の素数列で成り立つこと -/

-- A4 = [3,5,7,11], D = 5(= 11/2)。W = Γ + 11/2^4 = 4.3125 + 0.6875 = 5
#eval windowSeries [3,5,7,11] 5
#eval gapSeries [3,5,7,11] + (2 * (5:ℚ) + 1) / 2 ^ 4
#eval decide (windowSeries [3,5,7,11] 5 = gapSeries [3,5,7,11] + (2 * (5:ℚ) + 1) / 2 ^ 4)

-- 奇素数20項, D = 36 (= 73/2)。Γ = 5609051/1048576 ≈ 5.3492
#eval windowSeries oddPrimes20 36
#eval gapSeries oddPrimes20 + (2 * (36:ℚ) + 1) / 2 ^ 20
#eval decide (windowSeries oddPrimes20 36
  = gapSeries oddPrimes20 + (2 * (36:ℚ) + 1) / 2 ^ 20)

-- D をさらに大きく取っても(尾部の項が (2D+1)/2^k に吸収されて)成立する
#eval decide (windowSeries oddPrimes20 200
  = gapSeries oddPrimes20 + (2 * (200:ℚ) + 1) / 2 ^ 20)

-- 昇順でないと崩れる(順序依存性の確認): [5,3] は D=2 で W=4 だが Γ+5/4=4.5
#eval windowSeries [5,3] 2
#eval gapSeries [5,3] + (2 * (2:ℚ) + 1) / 2 ^ 2

end WindowSeries

end ALT

#print axioms ALT.sum_fin_succ
#print axioms ALT.exists_sum_succ_iff
#print axioms ALT.mem_subsetSums_ofFn_iff
#print axioms ALT.gs_ofFn_eq_energy_min
#print axioms ALT.window_term_cons
#print axioms ALT.windowSeries_eq_gapSeries
