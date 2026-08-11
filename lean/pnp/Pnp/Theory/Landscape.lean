/- 算術地形理論(ALT)正典 第1号 (2026-08-07)
   部分和地形の基本定義と最初の定理群。
   実験側(Landscape.lean, exe)の gs と同じ定義をリストで形式化する。
   同日2周目の追加: gs補集合対称性の完全証明(定理4)、局所最小の分類定理
   (定理5〜7)、lm の正典化と数え上げ対応(定理8)、滑らかさ不変量 gapSeries(Γ)。 -/
import Mathlib.Tactic

namespace ALT

/-- 距離 |a - b|(Nat 版) -/
def ndist (a b : Nat) : Nat := if a ≥ b then a - b else b - a

/-- 列 A の全部分和 -/
def subsetSums : List Nat → List Nat
  | [] => [0]
  | x :: xs => subsetSums xs ++ (subsetSums xs).map (· + x)

/-- 基底状態値: 目標 n への最小距離 -/
def gs (A : List Nat) (n : Nat) : Nat :=
  (subsetSums A).foldl (fun m s => Nat.min m (ndist s n)) (ndist 0 n)

theorem ndist_zero_left (n : Nat) : ndist 0 n = n := by
  unfold ndist; split <;> omega

/-- 空選択 0 は常に部分和 -/
theorem zero_mem_subsetSums (A : List Nat) : 0 ∈ subsetSums A := by
  induction A with
  | nil => simp [subsetSums]
  | cons x xs ih => simp [subsetSums]; exact Or.inl ih

/-- 全選択 A.sum は常に部分和 -/
theorem sum_mem_subsetSums (A : List Nat) : A.sum ∈ subsetSums A := by
  induction A with
  | nil => simp [subsetSums]
  | cons x xs ih =>
    simp only [subsetSums, List.sum_cons, List.mem_append, List.mem_map]
    exact Or.inr ⟨xs.sum, ih, by omega⟩

/-- foldl-min は初期値を超えない -/
theorem foldl_min_le_init (l : List Nat) (f : Nat → Nat) (init : Nat) :
    l.foldl (fun m s => Nat.min m (f s)) init ≤ init := by
  induction l generalizing init with
  | nil => simp
  | cons a t ih =>
    calc t.foldl (fun m s => Nat.min m (f s)) (Nat.min init (f a))
        ≤ Nat.min init (f a) := ih _
      _ ≤ init := Nat.min_le_left _ _

/-- foldl-min はどの要素の値も超えない -/
theorem foldl_min_le_mem (l : List Nat) (f : Nat → Nat) (init : Nat)
    {s : Nat} (hs : s ∈ l) :
    l.foldl (fun m t => Nat.min m (f t)) init ≤ f s := by
  induction l generalizing init with
  | nil => cases hs
  | cons a t ih =>
    rcases List.mem_cons.mp hs with rfl | h
    · calc t.foldl (fun m u => Nat.min m (f u)) (Nat.min init (f s))
          ≤ Nat.min init (f s) := foldl_min_le_init _ _ _
        _ ≤ f s := Nat.min_le_right _ _
    · exact ih _ h

/-- 定理1: gs はどの部分和との距離も超えない -/
theorem gs_le_of_mem {A : List Nat} {s : Nat}
    (hs : s ∈ subsetSums A) (n : Nat) : gs A n ≤ ndist s n :=
  foldl_min_le_mem _ _ _ hs

/-- 定理2: gs A n ≤ n(何も選ばなければ誤差は n) -/
theorem gs_le_target (A : List Nat) (n : Nat) : gs A n ≤ n := by
  have h := foldl_min_le_init (subsetSums A) (fun s => ndist s n) (ndist 0 n)
  simpa [gs, ndist_zero_left] using h

/-- 定理3: gs A n ≤ |A.sum − n|(全部選んだときの誤差) -/
theorem gs_le_total_dist (A : List Nat) (n : Nat) :
    gs A n ≤ ndist A.sum n :=
  gs_le_of_mem (sum_mem_subsetSums A) n

/-- 部分和は総和を超えない -/
theorem subsetSums_le_sum {A : List Nat} {s : Nat}
    (hs : s ∈ subsetSums A) : s ≤ A.sum := by
  induction A generalizing s with
  | nil => simp [subsetSums] at hs; omega
  | cons x xs ih =>
    simp only [subsetSums, List.mem_append, List.mem_map] at hs
    rcases hs with h | ⟨t, ht, rfl⟩
    · have := ih h; simp [List.sum_cons]; omega
    · have := ih ht; simp [List.sum_cons]; omega

/-- 補集合対応: s が部分和なら A.sum − s も部分和 -/
theorem compl_mem_subsetSums {A : List Nat} {s : Nat}
    (hs : s ∈ subsetSums A) : A.sum - s ∈ subsetSums A := by
  induction A generalizing s with
  | nil => simp_all [subsetSums]
  | cons x xs ih =>
    simp only [subsetSums, List.mem_append, List.mem_map, List.sum_cons] at hs ⊢
    rcases hs with h | ⟨t, ht, rfl⟩
    · right
      refine ⟨xs.sum - s, ih h, ?_⟩
      have := subsetSums_le_sum h
      omega
    · left
      have := subsetSums_le_sum ht
      have h2 : x + xs.sum - (t + x) = xs.sum - t := by omega
      rw [h2]
      exact ih ht

/-- 距離の補集合対称性(範囲内で) -/
theorem ndist_compl {T s n : Nat} (hs : s ≤ T) (hn : n ≤ T) :
    ndist (T - s) (T - n) = ndist s n := by
  unfold ndist; split <;> split <;> omega

/- ============ 2周目: gs 補集合対称性の完全証明 ============ -/

/-- Nat.min の左決定(この版の omega は Nat.min を解釈しないための補助) -/
theorem nat_min_eq_left {a b : Nat} (h : a ≤ b) : Nat.min a b = a :=
  min_eq_left h

/-- Nat.min の右決定 -/
theorem nat_min_eq_right {a b : Nat} (h : b ≤ a) : Nat.min a b = b :=
  min_eq_right h

/-- foldl-min 達成補題: 結果は初期値か、リスト内のある要素の f 値に等しい -/
theorem foldl_min_attained (l : List Nat) (f : Nat → Nat) (init : Nat) :
    l.foldl (fun m s => Nat.min m (f s)) init = init ∨
    ∃ s ∈ l, l.foldl (fun m s => Nat.min m (f s)) init = f s := by
  induction l generalizing init with
  | nil => exact Or.inl rfl
  | cons a t ih =>
    show t.foldl (fun m s => Nat.min m (f s)) (Nat.min init (f a)) = init ∨
      ∃ s ∈ a :: t, t.foldl (fun m s => Nat.min m (f s)) (Nat.min init (f a)) = f s
    rcases ih (Nat.min init (f a)) with h | ⟨s, hs, h⟩
    · rcases Nat.le_total init (f a) with hle | hle
      · left; rw [h, nat_min_eq_left hle]
      · right; exact ⟨a, by simp, by rw [h, nat_min_eq_right hle]⟩
    · right; exact ⟨s, by simp [hs], h⟩

/-- gs はある部分和との距離として達成される -/
theorem gs_attained (A : List Nat) (n : Nat) :
    ∃ s ∈ subsetSums A, gs A n = ndist s n := by
  rcases foldl_min_attained (subsetSums A) (fun s => ndist s n) (ndist 0 n)
    with h | ⟨s, hs, h⟩
  · exact ⟨0, zero_mem_subsetSums A, h⟩
  · exact ⟨s, hs, h⟩

/-- 片側不等式: gs A (A.sum − n) ≤ gs A n -/
theorem gs_compl_le (A : List Nat) {n : Nat} (hn : n ≤ A.sum) :
    gs A (A.sum - n) ≤ gs A n := by
  obtain ⟨s, hs, hgs⟩ := gs_attained A n
  have h1 : gs A (A.sum - n) ≤ ndist (A.sum - s) (A.sum - n) :=
    gs_le_of_mem (compl_mem_subsetSums hs) (A.sum - n)
  rw [ndist_compl (subsetSums_le_sum hs) hn] at h1
  omega

/-- 定理4(gs補集合対称性): n ≤ A.sum のとき gs A (A.sum − n) = gs A n。
    1周目に実験で確認した対称性(random k=8/k=18 全19点で一致)の完全証明。 -/
theorem gs_compl (A : List Nat) {n : Nat} (hn : n ≤ A.sum) :
    gs A (A.sum - n) = gs A n := by
  have h1 := gs_compl_le A hn
  have h2 := gs_compl_le A (Nat.sub_le A.sum n)
  have heq : A.sum - (A.sum - n) = n := by omega
  rw [heq] at h2
  omega

/- ============ 2周目: 配位空間と局所最小の分類定理 ============
   配位 = 添字集合 S ⊆ Fin k。エネルギー E(S) = |Σ_{i∈S} A i − n|。
   近傍 = 1点フリップ(i を入れる/外す)。
   分類定理の内容: 誤差 d = |S.sum − n| とおくと
     過剰側(sum ≥ n): 厳密局所最小 ⟺ 選んだ最小要素 > 2d
     不足側(sum ≤ n): 厳密局所最小 ⟺ 選ばなかった最小要素 > 2d
   これにより地形量 lm は純算術的な(制限付き表現の)数え上げに帰着する。 -/

section LocalMin

variable {k : Nat}

/-- 配位 S のエネルギー(目標 n への到達誤差) -/
def energy (A : Fin k → Nat) (n : Nat) (S : Finset (Fin k)) : Nat :=
  ndist (S.sum A) n

/-- 1点フリップ: i ∈ S なら外し、i ∉ S なら入れる -/
def flip (S : Finset (Fin k)) (i : Fin k) : Finset (Fin k) :=
  if i ∈ S then S.erase i else insert i S

/-- 厳密局所最小: どの1点フリップでもエネルギーが真に増える -/
def IsStrictLocalMin (A : Fin k → Nat) (n : Nat) (S : Finset (Fin k)) : Prop :=
  ∀ i : Fin k, energy A n S < energy A n (flip S i)

instance (A : Fin k → Nat) (n : Nat) (S : Finset (Fin k)) :
    Decidable (IsStrictLocalMin A n S) :=
  decidable_of_iff (∀ i : Fin k, energy A n S < energy A n (flip S i)) Iff.rfl

/-- 消去和の分解: i ∈ S なら (S.erase i).sum + A i = S.sum -/
theorem sum_erase_add_of_mem (A : Fin k → Nat) {S : Finset (Fin k)} {i : Fin k}
    (hi : i ∈ S) : (S.erase i).sum A + A i = S.sum A :=
  Finset.sum_erase_add S A hi

/-- 定理5(分類定理・過剰側): 総和が目標以上の配位では、
    厳密局所最小 ⟺ 選んだどの要素 a_i も誤差の2倍を超える。
    (2*sum < A i + 2*n は a_i > 2(sum−n) を自然数で引き算なしに書いたもの) -/
theorem isStrictLocalMin_iff_of_ge {A : Fin k → Nat} (hA : ∀ i, 0 < A i)
    {n : Nat} {S : Finset (Fin k)} (hn : n ≤ S.sum A) :
    IsStrictLocalMin A n S ↔ ∀ i ∈ S, 2 * S.sum A < A i + 2 * n := by
  constructor
  · intro h i hi
    have hflip := h i
    have hsum := sum_erase_add_of_mem A hi
    unfold energy flip at hflip
    rw [if_pos hi] at hflip
    unfold ndist at hflip
    split at hflip <;> split at hflip <;> omega
  · intro hc i
    unfold energy flip
    by_cases hi : i ∈ S
    · rw [if_pos hi]
      have hsum := sum_erase_add_of_mem A hi
      have := hc i hi
      unfold ndist
      split <;> split <;> omega
    · rw [if_neg hi]
      have hsum : (insert i S).sum A = A i + S.sum A := Finset.sum_insert hi
      have := hA i
      unfold ndist
      split <;> split <;> omega

/-- 定理6(分類定理・不足側): 総和が目標以下の配位では、
    厳密局所最小 ⟺ 選ばなかったどの要素 a_i も不足の2倍を超える。 -/
theorem isStrictLocalMin_iff_of_le {A : Fin k → Nat} (hA : ∀ i, 0 < A i)
    {n : Nat} {S : Finset (Fin k)} (hn : S.sum A ≤ n) :
    IsStrictLocalMin A n S ↔ ∀ i ∉ S, 2 * n < A i + 2 * S.sum A := by
  constructor
  · intro h i hi
    have hflip := h i
    have hsum : (insert i S).sum A = A i + S.sum A := Finset.sum_insert hi
    unfold energy flip at hflip
    rw [if_neg hi] at hflip
    unfold ndist at hflip
    split at hflip <;> split at hflip <;> omega
  · intro hc i
    unfold energy flip
    by_cases hi : i ∈ S
    · rw [if_pos hi]
      have hsum := sum_erase_add_of_mem A hi
      have := hA i
      unfold ndist
      split <;> split <;> omega
    · rw [if_neg hi]
      have hsum : (insert i S).sum A = A i + S.sum A := Finset.sum_insert hi
      have := hc i hi
      unfold ndist
      split <;> split <;> omega

/-- 系: 誤差0の配位(基底状態)は常に厳密局所最小(要素が全て正のとき) -/
theorem isStrictLocalMin_of_exact {A : Fin k → Nat} (hA : ∀ i, 0 < A i)
    {n : Nat} {S : Finset (Fin k)} (h : S.sum A = n) :
    IsStrictLocalMin A n S := by
  rw [isStrictLocalMin_iff_of_ge hA (le_of_eq h.symm)]
  intro i _
  have := hA i
  omega

/-- 分類条件: 分類定理の右辺を1つの算術条件にまとめたもの -/
def ClassCond (A : Fin k → Nat) (n : Nat) (S : Finset (Fin k)) : Prop :=
  (n ≤ S.sum A → ∀ i ∈ S, 2 * S.sum A < A i + 2 * n) ∧
  (S.sum A ≤ n → ∀ i ∉ S, 2 * n < A i + 2 * S.sum A)

instance (A : Fin k → Nat) (n : Nat) (S : Finset (Fin k)) :
    Decidable (ClassCond A n S) :=
  decidable_of_iff ((n ≤ S.sum A → ∀ i ∈ S, 2 * S.sum A < A i + 2 * n) ∧
    (S.sum A ≤ n → ∀ i ∉ S, 2 * n < A i + 2 * S.sum A)) Iff.rfl

/-- 定理7(統合分類定理): 厳密局所最小 ⟺ 分類条件 -/
theorem isStrictLocalMin_iff_classCond {A : Fin k → Nat} (hA : ∀ i, 0 < A i)
    (n : Nat) (S : Finset (Fin k)) :
    IsStrictLocalMin A n S ↔ ClassCond A n S := by
  unfold ClassCond
  rcases Nat.le_total n (S.sum A) with h | h
  · rw [isStrictLocalMin_iff_of_ge hA h]
    constructor
    · intro hc
      refine ⟨fun _ => hc, fun hle i _ => ?_⟩
      have := hA i
      omega
    · rintro ⟨h1, _⟩
      exact h1 h
  · rw [isStrictLocalMin_iff_of_le hA h]
    constructor
    · intro hc
      refine ⟨fun hge i _ => ?_, fun _ => hc⟩
      have := hA i
      omega
    · rintro ⟨_, h2⟩
      exact h2 h

/-- 局所最小数 lm: 厳密局所最小の個数(定義自体が全数計算になっている) -/
def lm (A : Fin k → Nat) (n : Nat) : Nat :=
  ((Finset.univ : Finset (Finset (Fin k))).filter
    (fun S => IsStrictLocalMin A n S)).card

/-- 分類条件による数え上げ -/
def lmClassCount (A : Fin k → Nat) (n : Nat) : Nat :=
  ((Finset.univ : Finset (Finset (Fin k))).filter
    (fun S => ClassCond A n S)).card

/-- 定理8(数え上げ対応): lm は分類条件を満たす配位の数え上げに等しい。
    「地形の量 lm は純算術的な量である」ことの正当化。 -/
theorem lm_eq_lmClassCount (A : Fin k → Nat) (hA : ∀ i, 0 < A i) (n : Nat) :
    lm A n = lmClassCount A n := by
  unfold lm lmClassCount
  congr 1
  exact Finset.filter_congr (fun S _ => isStrictLocalMin_iff_classCond hA n S)

end LocalMin

/- ============ 2周目: 滑らかさ不変量 Γ(ギャップ級数) ============
   Γ(A) = Σ_{j=1}^{|A|} a_j / 2^j(有限リスト版)。
   増加奇数列では、誤差 d の配位が局所最小になる割合の総和
   1 + 2·Σ_{d≥1} 2^{−#{i : a_i ≤ 2d}} と厳密に一致する(望遠鏡和、証明は次周)。
   ギャップ形: Γ(A) = Σ_{j≥0} (a_{j+1} − a_j)/2^j(a_0 := 0)。
   つまり Γ は「列の初期ギャップ構造の2進重み付き和」であり、
   小さい初期ギャップ(素数なら双子素数など)が小さい Γ = 滑らかな地形を与える。
   主予想(P2): 中央目標 n = T/2 で lm_A(n,k)/2^k ≈ Γ(A)·√(2/(π·Σa_i²))。 -/

/-- 枚挙級数 Σ_{j=1}^{|A|} a_j / 2^j。

    **名前の注意(r121)**: この識別子は歴史的に `gapSeries` と呼ばれているが、
    r120 以降、論文でいう「間隙級数 Γ」は**層の形**
    `Γ(A) = 1 + 2 Σ_{d≤(M−1)/2} 2^{−N_A(d)}` のほうを指す。両者は `a_k/2^{|A|}` だけ
    異なり、極限は同じ。橋渡しは `windowSeries_eq_gapSeries`(境界項つきの恒等式)。
    つまり**同じ名前が正典と論文で別の対象を指している**。正典側の改名(`enumSeries`?)は
    カーネル再生をやり直す価値が出たときに行う。それまでは、この注記が対応表である。 -/
def gapSeries : List Nat → ℚ
  | [] => 0
  | a :: t => (a : ℚ) / 2 + gapSeries t / 2

theorem gapSeries_nonneg (A : List Nat) : 0 ≤ gapSeries A := by
  induction A with
  | nil => simp [gapSeries]
  | cons a t ih =>
    simp only [gapSeries]
    have h1 : (0 : ℚ) ≤ (a : ℚ) := Nat.cast_nonneg a
    linarith

/-- 一様上界: 全要素が M 以下なら Γ(A) ≤ M -/
theorem gapSeries_le_of_forall_le {M : Nat} {A : List Nat}
    (h : ∀ a ∈ A, a ≤ M) : gapSeries A ≤ (M : ℚ) := by
  revert h
  induction A with
  | nil =>
    intro _
    simp only [gapSeries]
    exact Nat.cast_nonneg M
  | cons a t ih =>
    intro h
    simp only [gapSeries]
    have h1 : (a : ℚ) ≤ (M : ℚ) := by exact_mod_cast h a (by simp)
    have h2 : gapSeries t ≤ (M : ℚ) := ih (fun b hb => h b (by simp [hb]))
    linarith

/- ---- Γ の例(品質ゲート: 例5つ) ---- -/

/-- 奇素数20項(1周目実験と同じ列) -/
def oddPrimes20 : List Nat :=
  [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73]

#eval gapSeries oddPrimes20                               -- 期待 ≈ 5.3492
#eval gapSeries ((List.range 20).map (· + 1))             -- 自然数: → 2 に収束
#eval gapSeries ((List.range 20).map (fun j => 2*j + 1))  -- 奇数: → 3 に収束
#eval gapSeries ((List.range 20).map (fun j => (j+1)^2))  -- 平方数: → 6 に収束
#eval gapSeries ((List.range 20).map (fun j => 2^(j+1)))  -- 2冪: 発散する非例(=項数)

/- ---- 分類定理・lm の実例と手計算クロスチェック ---- -/

/-- 例: A = (3,5,7,11) の Fin 4 版 -/
def A4 : Fin 4 → Nat := fun i => [3, 5, 7, 11].getD i.val 0

#eval lm A4 13            -- 手計算: {3,11} と {5,7} の2つ(期待 2)
#eval lmClassCount A4 13  -- 分類条件でも 2
#eval gs [3, 5, 7, 11] 13 -- 期待 1(13 は表現不能)
#eval [gs [3, 5, 7, 11] 6, gs [3, 5, 7, 11] 20]  -- 対称ペア(T=26): 両方 1

/-- 例: A = (3,5,7,11,13,17) の Fin 6 版 -/
def A6 : Fin 6 → Nat := fun i => [3, 5, 7, 11, 13, 17].getD i.val 0

-- lm(力ずく)と lmClassCount(分類条件)の全数一致チェック
#eval (List.range 31).all (fun n => lm A4 n == lmClassCount A4 n)  -- 期待 true
#eval (List.range 60).all (fun n => lm A6 n == lmClassCount A6 n)  -- 期待 true

/- ============ 予想の梯子(2周目版) ============
   【すぐ試せる予想(opus-5実験)】
   P1(相関予想): 100シードのランダム奇数列で、シードごとの lm(T/2) と Γ(R) は
     強く正相関する。1周目 k=18 の「最小要素9」標本は Γ が大きい側の点として
     予測どおり説明される(外れ値ではなく理論の検証点)。
     ※実験時は各シードの標本列そのものと Γ(R) も出力すること。
   P2(絶対公式): lm_A(T/2, k) ≈ 2^k · Γ(A) · √(2/(π·Σa_i²))。
     [実験的に確認 2026-08-07(素数列 ρ=50%, results_landscape_r1.csv):
      予測/実測 = k=8: 27.1/22, k=12: 218.0/214, k=16: 2160.9/2138,
      k=18: 7081.5/6706, k=20: 23809/22808(k≥12 で誤差2〜5%)。
      密度因子は deg でも独立確認(例 k=20: 予測4451/実測4344)。
      比 lm/deg ≈ Γ(A) が直接見える: k=8..20 で
      5.50, 5.63, 5.43, 5.20, 5.25 vs Γ_k = 5.22..5.35(誤差≤6%)。
      ランダム側の per-seed 検証(lm/deg から Γ(R) を逆算し標本列の Γ と比較、
      例 k=18: 13488/1178=11.45, k=20: 26156/4516=5.79)は opus-5 の100シード実験で。]
   【今期の目標予想】
   P3(滑らかさの普遍性): 増加奇数列の族で lm(T/2,k)/2^k · √(Σa_i²)/Γ(A) → √(2/π)。
   P4(lm対称性): lm_A(n) = lm_A(T−n)。分類条件の (n,S) ↔ (T−n, Sᶜ) 対応から
     従うはず(Lean証明は opus-5 へ)。
   P4'(平坦辺なし): 奇数列の地形では隣接配位のエネルギーは常に異なる
     (パリティ論法: d と d±a_i は a_i 奇数なら偶奇が違う)→ 厳密/非厳密の区別が消える。
   【夢の予想】
   P5: 素数地形の滑らかさ比 lm_P/lm_R は k→∞ で Γ(P)/E[Γ(R)] ≈ c/ln k → 0。
     「素数の初期ギャップの小ささ(双子素数の存在)が地形を漸近的に滑らかにする」。
   【ρ≠1/2 への拡張メモ】
   選択密度 ρ では因子 2^{−N} が (1−ρ)^N 型に変わり、Γ は評価点をずらした族
   Γ_x(A) = Σ a_j x^j に変形される(地形の温度パラメータ)。n/T が中央から
   離れた大偏差領域では lm/2^k に指数因子(レート関数)が掛かる。
   【橋(TODO)】
   List 版 gs と Fin k 版 energy の対応補題(subsetSums ↔ Finset.sum)は次周。 -/

end ALT

#print axioms ALT.gs_le_of_mem
#print axioms ALT.gs_le_target
#print axioms ALT.gs_le_total_dist
#print axioms ALT.compl_mem_subsetSums
#print axioms ALT.ndist_compl
#print axioms ALT.foldl_min_attained
#print axioms ALT.gs_attained
#print axioms ALT.gs_compl
#print axioms ALT.isStrictLocalMin_iff_of_ge
#print axioms ALT.isStrictLocalMin_iff_of_le
#print axioms ALT.isStrictLocalMin_of_exact
#print axioms ALT.isStrictLocalMin_iff_classCond
#print axioms ALT.lm_eq_lmClassCount
#print axioms ALT.gapSeries_nonneg
#print axioms ALT.gapSeries_le_of_forall_le
