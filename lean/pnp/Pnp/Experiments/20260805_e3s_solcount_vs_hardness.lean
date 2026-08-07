/-
  20260805_e3s_solcount_vs_hardness.lean  (作業ID: e3s)

  検討対象: 「SATの解は指数個あるから探索に指数時間かかる → P≠NP」という方向。
  この実験の狙い: 「解の個数」と「解きやすさ」が独立であることを具体例で示す。
    - taut n  : 解が 2^n 個(全割当が解)なのに、解は即座に書ける
    - chain n : 解が fib (n+2) ≈ 1.618^n 個ある 2-SAT 族(2-SAT は多項式時間で可解)
    - unitF n : 解がちょうど 1 個で、やはり即座に解ける
  さらに: 解の「個数」自体も、列挙せずに多項式時間で計算できる(フィボナッチ漸化式)。

  注意: 「多項式時間」という実行時間の主張は Lean の定理にしていない(計算モデル
  未形式化のため)。Lean で示すのは「解の個数」と「証拠(witness)の正しさ」。
-/

-- ==== 基本定義(references/lean-recipes.md §2.1 のひな形) ====

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

def countSat (n : Nat) (f : CNF) : Nat :=
  ((allAssignments n).filter (fun a => satisfies a f)).length

-- ==== 検討対象の CNF 族 ====

/-- `taut n` : n変数、節 (x_i ∨ ¬x_i)。全割当が解。 -/
def taut (n : Nat) : CNF :=
  (List.range n).map (fun i => [(i, true), (i, false)])

/-- `chain n` : n変数、節 (x_i ∨ x_{i+1}) (i = 0 .. n-2)。全節 2 リテラル = 2-SAT。 -/
def chain (n : Nat) : CNF :=
  (List.range (n - 1)).map (fun i => [(i, true), (i + 1, true)])

/-- `unitF n` : n変数、単位節 (x_i)。解は「全部 true」のただ 1 つ。 -/
def unitF (n : Nat) : CNF :=
  (List.range n).map (fun i => [(i, true)])

/-- フィボナッチ(反復版・線形時間)。 -/
def fibPair : Nat → Nat × Nat
  | 0 => (0, 1)
  | n + 1 =>
    let p := fibPair n
    (p.2, p.1 + p.2)

def fib (n : Nat) : Nat := (fibPair n).1

-- fib の検算(最初の 11 項)
example : (List.range 11).map fib = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55] := by decide

-- ==== 実験パート(#eval) ====

-- 実験1: taut n の解の個数 = 2^n。出力: (n, 実測, 2^n)
#eval (List.range 11).map (fun n => (n, countSat n (taut n), 2 ^ n))

-- 実験2: chain n の解の個数 = fib (n+2)。出力: (n, 実測, fib (n+2))
#eval (List.range 11).map (fun n => (n, countSat n (chain n), fib (n + 2)))

-- 実験2': もう少し大きい n(総当たり 2^16, 2^18 通り)
#eval (countSat 16 (chain 16), fib 18)
#eval (countSat 18 (chain 18), fib 20)

-- 実験3: unitF n の解の個数 = 1。出力: (n, 実測)
#eval (List.range 11).map (fun n => (n, countSat n (unitF n)))

-- 実験4: 解の「個数」は列挙せずに計算できる(chain n の個数 = fib (n+2))。
-- n = 100 の個数 fib 102 は巨大だが計算は一瞬。
#eval fib 102
#eval (toString (fib 102)).length   -- 10進での桁数
#eval (toString (fib 302)).length   -- n = 300 でも一瞬

-- ==== 形式証明パート ====

/-- 補題A: どんな割当も taut n を充足する。 -/
theorem satisfies_taut (a : List Bool) (n : Nat) :
    satisfies a (taut n) = true := by
  simp [satisfies, taut, List.all_eq_true]
  intro i _hi
  simp [evalLit]

/-- 補題B: 2分岐 flatMap は長さを 2 倍にする。 -/
theorem length_flatMap_pair (L : List (List Bool)) :
    (L.flatMap (fun a => [true :: a, false :: a])).length = 2 * L.length := by
  induction L with
  | nil => rfl
  | cons x xs ih =>
    simp only [List.flatMap_cons, List.length_append, List.length_cons,
      List.length_nil, ih]
    omega

/-- 補題C: n 変数の割当は全部で 2^n 個。 -/
theorem length_allAssignments (n : Nat) :
    (allAssignments n).length = 2 ^ n := by
  induction n with
  | zero => rfl
  | succ k ih =>
    simp only [allAssignments]
    rw [length_flatMap_pair, ih, Nat.pow_succ]
    omega

/-- 定理1: taut n の解の個数はちょうど 2^n(解が指数個ある易しい族の存在)。 -/
theorem countSat_taut (n : Nat) : countSat n (taut n) = 2 ^ n := by
  have h : (allAssignments n).filter (fun a => satisfies a (taut n))
      = allAssignments n := by
    apply List.filter_eq_self.mpr
    intro a _
    simp [satisfies_taut]
  unfold countSat
  rw [h]
  exact length_allAssignments n

/-- 定理2: taut n は充足可能(明示的な証拠: 全 true)。 -/
theorem taut_satisfiable (n : Nat) :
    ∃ a : List Bool, satisfies a (taut n) = true :=
  ⟨List.replicate n true, satisfies_taut _ n⟩

/-- 補題D: replicate n true の第 i 成分 (i < n) は some true。 -/
theorem getElem?_replicate_true (n i : Nat) (h : i < n) :
    (List.replicate n true)[i]? = some true := by
  induction n generalizing i with
  | zero => omega
  | succ k ih =>
    cases i with
    | zero => rfl
    | succ j =>
      rw [List.replicate_succ, List.getElem?_cons_succ]
      exact ih j (by omega)

/-- 定理3: 全 true 割当は chain n を充足する(解が指数個あっても発見は自明)。 -/
theorem allTrue_satisfies_chain (n : Nat) :
    satisfies (List.replicate n true) (chain n) = true := by
  simp [satisfies, chain, List.all_eq_true]
  intro i hi
  have h1 : (List.replicate n true)[i]? = some true :=
    getElem?_replicate_true n i (by omega)
  simp [evalLit, h1]

/-- 定理4: chain n は充足可能(明示的な証拠つき)。 -/
theorem chain_satisfiable (n : Nat) :
    ∃ a : List Bool, satisfies a (chain n) = true :=
  ⟨List.replicate n true, allTrue_satisfies_chain n⟩

/-- 定理5: 全 true 割当は unitF n も充足する(解が 1 個でも発見は自明)。 -/
theorem allTrue_satisfies_unitF (n : Nat) :
    satisfies (List.replicate n true) (unitF n) = true := by
  simp [satisfies, unitF, List.all_eq_true]
  intro i hi
  have h1 : (List.replicate n true)[i]? = some true :=
    getElem?_replicate_true n i hi
  simp [evalLit, h1]

/-- 定理6(有限範囲の機械検証): n ≤ 8 で chain n の解の個数 = fib (n+2)。 -/
theorem chain_count_eq_fib_upto8 :
    ((List.range 9).all (fun n => countSat n (chain n) == fib (n + 2))) = true := by
  decide

/-- 定理7(有限範囲の機械検証): n ≤ 8 で unitF n の解の個数 = 1。 -/
theorem unitF_count_eq_one_upto8 :
    ((List.range 9).all (fun n => countSat n (unitF n) == 1)) = true := by
  decide

-- ==== axioms 確認(sorry 残存チェック) ====

#print axioms satisfies_taut
#print axioms length_flatMap_pair
#print axioms length_allAssignments
#print axioms countSat_taut
#print axioms taut_satisfiable
#print axioms getElem?_replicate_true
#print axioms allTrue_satisfies_chain
#print axioms chain_satisfiable
#print axioms allTrue_satisfies_unitF
#print axioms chain_count_eq_fib_upto8
#print axioms unitF_count_eq_one_upto8
