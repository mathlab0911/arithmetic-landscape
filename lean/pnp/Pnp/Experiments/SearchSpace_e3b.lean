/-
  SearchSpace_e3b.lean  (作業ID: e3b, 2026-08-05)

  「候補が指数個あるから、探索には指数時間かかる」という推論を
  Lean で検査する小さな実験ファイル(Mathlib 不使用、Lean 4 コアのみ)。

  機械検証するのは次の 2 点:

  (1) n 変数の真偽割当(候補空間)はちょうど 2^n 個ある。
      → 「候補は指数個」という前提そのものは正しい。

  (2) 候補が 2^n 個ある探索問題でも、「2^n 個ぜんぶ調べる全数探索」と
      まったく同じ答えを、リストを 1 回なめるだけの線形走査で返せる
      例が存在する(定理 fastScan_eq_bruteForce)。
      → 「候補が指数個 ⇒ 指数個調べる必要がある」という推論は、
        論理としては成立しない(反例がある)。

  注意: 「あらゆるアルゴリズムに対する時間下界」を主張するには、
  計算モデル(チューリング機械等)と時間計測の形式化が必要で、
  このファイルの範囲外。P≠NP の証明で埋めるべきギャップは
  まさにそこにある。
-/

namespace E3b

/-! ## (1) 候補空間のサイズは正確に 2^n -/

/-- n 変数のすべての真偽割当(候補空間)の列挙。 -/
def allAssignments : Nat → List (List Bool)
  | 0 => [[]]
  | n + 1 =>
      (allAssignments n).map (true :: ·) ++ (allAssignments n).map (false :: ·)

/-- 候補空間のサイズはちょうど 2^n。(「候補は指数個」は正しい) -/
theorem length_allAssignments (n : Nat) :
    (allAssignments n).length = 2 ^ n := by
  induction n with
  | zero => rfl
  | succ n ih =>
      simp only [allAssignments, List.length_append, List.length_map, ih,
                 Nat.pow_succ]
      omega

/-! ## (2) 候補は 2^n 個、しかし全数探索は不要という例

問題:「与えられた自然数のリストに、和が奇数になる部分集合は存在するか?」
部分集合は 2^n 個あるので、候補空間は SAT と同様に指数サイズである。 -/

/-- リスト l のすべての部分集合の和(候補は 2^(l.length) 個)。 -/
def subsetSums : List Nat → List Nat
  | [] => [0]
  | x :: xs => (subsetSums xs).map (x + ·) ++ subsetSums xs

/-- 候補(部分集合の和)は正確に 2^n 個ある。 -/
theorem length_subsetSums (l : List Nat) :
    (subsetSums l).length = 2 ^ l.length := by
  induction l with
  | nil => rfl
  | cons x xs ih =>
      simp only [subsetSums, List.length_append, List.length_map, ih,
                 List.length_cons, Nat.pow_succ]
      omega

/-- 全数探索: 2^n 個の候補をすべて生成して調べる(指数時間・指数領域)。 -/
def bruteForce (l : List Nat) : Bool :=
  (subsetSums l).any (fun s => s % 2 == 1)

/-- 線形走査: 奇数の要素が 1 つでもあるかを見るだけ(1 パス)。 -/
def fastScan (l : List Nat) : Bool :=
  l.any (fun x => x % 2 == 1)

/-- 空部分集合の和 0 は、つねに候補リストに含まれる。 -/
theorem zero_mem_subsetSums (l : List Nat) : 0 ∈ subsetSums l := by
  induction l with
  | nil => simp [subsetSums]
  | cons x xs ih =>
      simp only [subsetSums, List.mem_append]
      exact Or.inr ih

/-- 主定理: 線形走査は、2^n 個の候補に対する全数探索とつねに同じ答えを返す。

    すなわち「候補が指数個ある」ことは「指数個調べる必要がある」ことを
    含意しない。SAT で同じ短絡が起きない保証はどこにもなく、
    それを排除することこそが P≠NP の証明課題である。 -/
theorem fastScan_eq_bruteForce (l : List Nat) : fastScan l = bruteForce l := by
  induction l with
  | nil => rfl
  | cons x xs ih =>
      have hcons : subsetSums (x :: xs)
          = (subsetSums xs).map (x + ·) ++ subsetSums xs := rfl
      show (x :: xs).any (fun a => a % 2 == 1)
          = (subsetSums (x :: xs)).any (fun s => s % 2 == 1)
      rw [hcons, List.any_append, List.any_map, List.any_cons]
      rcases Nat.mod_two_eq_zero_or_one x with hx | hx
      · -- x が偶数のとき: x を足しても各候補の偶奇は変わらない
        have hpred : ((fun s => s % 2 == 1) ∘ (x + ·)) = (fun s : Nat => s % 2 == 1) := by
          funext s
          show ((x + s) % 2 == 1) = (s % 2 == 1)
          have h2 : (x + s) % 2 = s % 2 := by omega
          rw [h2]
        have hx' : (x % 2 == 1) = false := by simp [hx]
        rw [hpred, hx', Bool.false_or, Bool.or_self]
        exact ih
      · -- x が奇数のとき: 両辺とも true
        --   左辺: 先頭要素 x 自身が奇数
        --   右辺: 空部分集合の和 0 に x を足した候補 x + 0 が奇数
        have hx' : (x % 2 == 1) = true := by simp [hx]
        have hwit : (subsetSums xs).any ((fun s => s % 2 == 1) ∘ (x + ·)) = true := by
          rw [List.any_eq_true]
          exact ⟨0, zero_mem_subsetSums xs, by simp [Function.comp, hx]⟩
        rw [hx', hwit, Bool.true_or, Bool.true_or]

/-! ## 動作確認 -/

#eval (allAssignments 4).length          -- 16 = 2^4
#eval (subsetSums [1, 2, 3]).length      -- 8 = 2^3
#eval bruteForce [2, 4, 6]               -- false(奇数要素なし)
#eval fastScan  [2, 4, 6]                -- false
#eval bruteForce [2, 4, 7]               -- true
#eval fastScan  [2, 4, 7]                -- true

-- 全数探索が物理的に不可能な規模でも、線形走査は一瞬で終わる。
-- 以下のリストの部分集合(候補)は 2^100000 ≈ 10^30103 個ある:
#eval fastScan (List.range 100000)       -- true (奇数 1 を含む)

-- 証明が公理以外に依存していないことの確認
#print axioms length_allAssignments
#print axioms length_subsetSums
#print axioms fastScan_eq_bruteForce

end E3b
