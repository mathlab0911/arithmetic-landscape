/-
  20260805_e1s_frozen_chain.lean(作業ID: e1s / 2026-08-05 / 初回研究セッション)

  問い: 物理由来の推論図式「解空間がクラスタ化し変数が凍結する(クラスタ間に
  大きなハミング・ギャップがある)⇒ その問題族はアルゴリズム的に困難」は正しいか。

  答え(本ファイルで確定): 偽。反例族 = 等価連鎖 2-CNF
      E_n = ⋀_{i=0}^{n-2} (x_i ↔ x_{i+1})
    - 解はちょうど2個 {全true, 全false}: 全変数が凍結・各クラスタは孤立点
    - 2解間のハミング距離は n(相対距離1 = 考えうる最大のギャップ)
    - しかし E_n は 2-CNF かつ XOR-SAT なので多項式時間で可解
      (2-SAT ∈ P: Krom 1967 / Aspvall–Plass–Tarjan 1979。この事実は文献による)

  主張レベルの区別(スキル準拠):
    - 「Leanで証明済み」: 一般 n の定理(§4)
    - 「decideによる有限証明」: n ≤ 8(§5)
    - 「実験的確認」: n ≤ 14(§3 の #eval)
-/

-- ========== §0 基本定義(lean-recipes.md §2.1 の型をそのまま使用) ==========

abbrev Lit := Nat × Bool
abbrev Clause := List Lit
abbrev CNF := List Clause

def evalLit (a : List Bool) (l : Lit) : Bool :=
  (a.getD l.1 false) == l.2

def satisfies (a : List Bool) (f : CNF) : Bool :=
  f.all (fun c => c.any (evalLit a))

def allAssignments : Nat → List (List Bool)
  | 0 => [[]]
  | n + 1 => (allAssignments n).flatMap (fun a => [true :: a, false :: a])

def solutions (n : Nat) (f : CNF) : List (List Bool) :=
  (allAssignments n).filter (fun a => satisfies a f)

def countSat (n : Nat) (f : CNF) : Nat := (solutions n f).length

-- ========== §1 等価連鎖 2-CNF と、その証明しやすい同値形 ==========

-- x_i ↔ x_{i+1} を節2つ (¬x_i ∨ x_{i+1}), (x_i ∨ ¬x_{i+1}) で表した 2-CNF
def chainCNF : Nat → CNF
  | 0 => []
  | 1 => []
  | n + 2 => [(n, false), (n + 1, true)] :: [(n, true), (n + 1, false)] :: chainCNF (n + 1)

-- 再帰版: 「隣接成分がすべて等しい」(証明しやすい形)
def chainOK : List Bool → Bool
  | [] => true
  | [_] => true
  | x :: y :: rest => (x == y) && chainOK (y :: rest)

-- ========== §2 実験用の道具 ==========

def hamming : List Bool → List Bool → Nat
  | x :: xs, y :: ys => (if x == y then 0 else 1) + hamming xs ys
  | _, _ => 0

def dedup (xs : List Nat) : List Nat :=
  xs.foldl (fun acc x => if acc.contains x then acc else acc ++ [x]) []

def insertSorted (x : Nat) : List Nat → List Nat
  | [] => [x]
  | y :: ys => if x ≤ y then x :: y :: ys else y :: insertSorted x ys

def sortNat (xs : List Nat) : List Nat := xs.foldr insertSorted []

-- 解集合のペア間ハミング距離の集合(昇順・重複なし)
def distSpectrum (sols : List (List Bool)) : List Nat :=
  sortNat (dedup (sols.flatMap (fun a => sols.map (fun b => hamming a b))))

-- 「距離 0 と n 以外が現れない」= クラスタ間ギャップが最大
def maxGap (n : Nat) (sols : List (List Bool)) : Bool :=
  (distSpectrum sols).all (fun d => d == 0 || d == n)

-- 凍結変数の個数(与えた解リストの全員が同じ値を取る座標の数)
-- 全解集合に適用すれば「大域の凍結」、クラスタに適用すれば「クラスタ内の凍結」
def frozenCount (n : Nat) (sols : List (List Bool)) : Nat :=
  ((List.range n).filter (fun i =>
    match sols with
    | [] => false
    | s :: _ => sols.all (fun t => t.getD i false == s.getD i false))).length

-- クラスタ分解: 隣接 = ハミング距離 1 として連結成分に分ける(物理のクラスタの標準定義)
def componentStep (all : List (List Bool)) (comp : List (List Bool)) : List (List Bool) :=
  all.filter (fun s => comp.contains s || comp.any (fun c => hamming c s == 1))

def componentOf (all : List (List Bool)) (seed : List Bool) : List (List Bool) :=
  (List.range all.length).foldl (fun comp _ => componentStep all comp) [seed]

def clustersAux : Nat → List (List Bool) → List (List (List Bool))
  | 0, _ => []
  | _ + 1, [] => []
  | k + 1, s :: rest =>
      let comp := componentOf (s :: rest) s
      comp :: clustersAux k ((s :: rest).filter (fun t => !comp.contains t))

def clusters (sols : List (List Bool)) : List (List (List Bool)) :=
  clustersAux sols.length sols

-- ========== §3 実験(#eval): 小さい n の全数チェック ==========

-- 3.1 解の個数(期待: n ≥ 1 で常に 2)
#eval (List.range 13).map (fun n => (n, countSat n (chainCNF n)))

-- 3.2 距離スペクトル(期待: [0, n] のみ = 2クラスタ・最大ギャップ)
#eval ((List.range 13).drop 1).map (fun n => (n, distSpectrum (solutions n (chainCNF n))))

-- 3.3 最大ギャップ判定(期待: true)
#eval ((List.range 13).drop 1).all (fun n => maxGap n (solutions n (chainCNF n)))

-- 3.4 大域の凍結変数(全解で値が共通の座標)。期待: 0(2つの解は互いに全ビット反転なので)
#eval ((List.range 13).drop 1).map (fun n => (n, frozenCount n (solutions n (chainCNF n))))

-- 3.4b クラスタ構造: (n, クラスタ数, 各サイズ, 各クラスタ内の凍結変数数)
--   期待: n ≥ 2 で (2, [1, 1], [n, n]) = 孤立クラスタ2個・クラスタ内では全変数凍結
--  (n = 1 は退化: 2解の距離が1なので単一クラスタになる)
#eval ((List.range 11).drop 1).map (fun n => let cs := clusters (solutions n (chainCNF n)); (n, cs.length, cs.map List.length, cs.map (frozenCount n)))

-- 3.4c 対照: 単一節 (x_0), n = 5。期待: (1, [16], [1]) = 1クラスタ・凍結は x_0 の1個だけ
#eval (let cs := clusters (solutions 5 [[(0, true)]]); (cs.length, cs.map List.length, cs.map (frozenCount 5)))

-- 3.5 対照実験: 単一節 (x_0) の族は解 2^(n-1) 個・距離が 0..n-1 の連続(ギャップなし)
#eval (countSat 5 [[(0, true)]], distSpectrum (solutions 5 [[(0, true)]]))
#eval maxGap 5 (solutions 5 [[(0, true)]])

-- 3.6 少し大きい n の追加確認(n = 14: 割当 16384 通り)
#eval (countSat 14 (chainCNF 14), distSpectrum (solutions 14 (chainCNF 14)))

-- ========== §4 一般 n の定理(Lean 証明) ==========

-- 4.1 核心補題: chainOK a ⟺ a は定数列(全 true または 全 false)
theorem chainOK_iff_const (a : List Bool) :
    chainOK a = (a.all (fun b => b) || a.all (fun b => !b)) := by
  induction a with
  | nil => rfl
  | cons x xs ih =>
    cases xs with
    | nil => cases x <;> rfl
    | cons y ys => cases x <;> cases y <;> simp [chainOK, List.all_cons, ih]

-- 4.2 存在側: 定数列は実際に解である(2つのクラスタが非空)
theorem chainOK_replicate (b : Bool) (n : Nat) :
    chainOK (List.replicate n b) = true := by
  induction n with
  | zero => rfl
  | succ k ih =>
    cases k with
    | zero => cases b <;> rfl
    | succ m =>
      show ((b == b) && chainOK (List.replicate (m + 1) b)) = true
      rw [ih]
      cases b <;> rfl

-- 4.3 2つの解は相異なる(n ≥ 1)
theorem replicate_true_ne_false (n : Nat) :
    List.replicate (n + 1) true ≠ List.replicate (n + 1) false := by
  intro h
  have h' : (true :: List.replicate n true) = (false :: List.replicate n false) := h
  injection h' with h1 _
  exact Bool.noConfusion h1

-- 4.4 距離定理: 2解間のハミング距離はちょうど n(相対距離1 = 最大ギャップ)
theorem hamming_replicate (n : Nat) :
    hamming (List.replicate n true) (List.replicate n false) = n := by
  induction n with
  | zero => rfl
  | succ k ih =>
    have h : hamming (List.replicate (k + 1) true) (List.replicate (k + 1) false)
        = 1 + hamming (List.replicate k true) (List.replicate k false) := rfl
    rw [h, ih]
    omega

-- 4.5 chainCNF は本当に 2-CNF(全節がちょうど 2 リテラル)
theorem chainCNF_is_2cnf (n : Nat) :
    (chainCNF n).all (fun c => c.length == 2) = true := by
  induction n with
  | zero => rfl
  | succ k ih =>
    cases k with
    | zero => rfl
    | succ m =>
      show ([(m, false), (m + 1, true)] :: [(m, true), (m + 1, false)]
              :: chainCNF (m + 1)).all (fun c => c.length == 2) = true
      simp [List.all_cons, ih]

-- 4.6 読みやすい Prop 版(4.1 の言い換え)
theorem chainOK_true_iff (a : List Bool) :
    chainOK a = true ↔ (∀ b ∈ a, b = true) ∨ (∀ b ∈ a, b = false) := by
  rw [chainOK_iff_const]
  simp

-- ========== §5 有限範囲の decide 証明(n ≤ 8) ==========

-- 5.1 CNF 意味論と chainOK の一致(ブリッジ): n ≤ 8 の全割当で一致
--(decide の評価が既定の再帰深度を超えるため maxRecDepth のみ引き上げ。公理は増えない)
set_option maxRecDepth 8192 in
theorem cnf_matches_chainOK_upto8 :
    ((List.range 9).all (fun n =>
      (allAssignments n).all (fun a => satisfies a (chainCNF n) == chainOK a))) = true := by
  decide

-- 5.2 解の個数はちょうど 2(n = 1..8)
theorem countSat_chain_two_upto8 :
    (((List.range 8).map (fun k => countSat (k + 1) (chainCNF (k + 1)))).all
      (fun c => c == 2)) = true := by
  decide

-- 5.3 距離スペクトルは {0, n} のみ(n = 1..8)
theorem maxGap_chain_upto8 :
    (((List.range 8).map (fun k => k + 1)).all
      (fun n => maxGap n (solutions n (chainCNF n)))) = true := by
  decide

-- ========== §6 公理確認(sorry 残存チェック) ==========

#print axioms chainOK_iff_const
#print axioms chainOK_replicate
#print axioms replicate_true_ne_false
#print axioms hamming_replicate
#print axioms chainCNF_is_2cnf
#print axioms chainOK_true_iff
#print axioms cnf_matches_chainOK_upto8
#print axioms countSat_chain_two_upto8
#print axioms maxGap_chain_upto8
