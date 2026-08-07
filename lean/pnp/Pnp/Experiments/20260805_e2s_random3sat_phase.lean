/-
  ランダム3-SAT 相転移実験 (作業ID: e2s, 2026-08-05)

  モデル: n 変数, m = round(alpha * n) 節のランダム3-CNF。
  各節: 相異なる3変数を一様に選び、各リテラルの極性を一様ランダムに決める。
  充足判定: 全 2^n 割当の総当たり(節ごとに生存割当をフィルタ)。
  乱数: 決定的 LCG (seed 固定) のため全結果は再現可能。

  出力列:
    a1000      : alpha × 1000 (4270 は alpha = 4.27)
    m          : 節数 = round(alpha * n)
    sat        : 充足可能だった試行数 / 総試行数
    pct        : その百分率
    avgSolx100 : 充足割当数の標本平均 × 100
    thSolx100  : 理論期待値 E[#解] × 100 = 2^n (7/8)^m × 100
-/

-- ===== 乱数 (LCG) =====

def lcg (s : Nat) : Nat := (1664525 * s + 1013904223) % 4294967296

def mix (s : Nat) : Nat := lcg (lcg (lcg s))

/-- [0, k) の乱数 (上位ビット使用)。(値, 新状態) を返す。 -/
def randBelow (s k : Nat) : Nat × Nat :=
  let s' := lcg s
  ((s' / 65536) % k, s')

-- ===== ランダム節・式の生成 =====

/-- 節 = (正リテラル変数のビットマスク, 負リテラル変数のビットマスク)。
    相異なる3変数を一様に選ぶ(シフト法)。 -/
def randClause (n s : Nat) : (Nat × Nat) × Nat :=
  let (i1, s1) := randBelow s n
  let (i2, s2) := randBelow s1 (n - 1)
  let (i3, s3) := randBelow s2 (n - 2)
  let v1 := i1
  let v2 := if i2 < v1 then i2 else i2 + 1
  let a := min v1 v2
  let b := max v1 v2
  let t := if i3 < a then i3 else i3 + 1
  let v3 := if t < b then t else t + 1
  let (p1, s4) := randBelow s3 2
  let (p2, s5) := randBelow s4 2
  let (p3, s6) := randBelow s5 2
  let add := fun (pm : Nat × Nat) (v p : Nat) =>
    if p == 1 then (pm.1 ||| (1 <<< v), pm.2) else (pm.1, pm.2 ||| (1 <<< v))
  (add (add (add (0, 0) v1 p1) v2 p2) v3 p3, s6)

def randFormula (n m s : Nat) : List (Nat × Nat) × Nat :=
  go m s []
where
  go : Nat → Nat → List (Nat × Nat) → List (Nat × Nat) × Nat
  | 0, s, acc => (acc, s)
  | k + 1, s, acc =>
    let (c, s') := randClause n s
    go k s' (c :: acc)

-- ===== 充足判定 (総当たり) =====

/-- 割当 a (nビットのビットベクトル) が節 c を満たすか。full = 2^n - 1。 -/
def clauseSat (full a : Nat) (c : Nat × Nat) : Bool :=
  ((a &&& c.1) != 0) || (((a ^^^ full) &&& c.2) != 0)

/-- 充足割当の個数(全 2^n 割当を節ごとにフィルタして数える)。 -/
def satCount (n : Nat) (f : List (Nat × Nat)) : Nat :=
  let full := 2 ^ n - 1
  let init := (List.range (2 ^ n)).toArray
  (f.foldl (fun surv c => surv.filter (fun a => clauseSat full a c)) init).size

-- ===== 自己検査 =====

-- (x0 ∨ x1) ∧ (¬x1 ∨ x2) の充足割当は 8 個中ちょうど 4 個のはず
#eval satCount 3 [(3, 0), (4, 2)]

def popcountAux : Nat → Nat → Nat
  | 0, _ => 0
  | fuel + 1, x => if x == 0 then 0 else x % 2 + popcountAux fuel (x / 2)

def popcount (x : Nat) : Nat := popcountAux 64 x

/-- 生成器の検査: 節が常に「相異なる3変数・範囲内・正負の重複なし」か。 -/
def genCheck (n cnt s : Nat) : Bool :=
  go cnt (mix s)
where
  go : Nat → Nat → Bool
  | 0, _ => true
  | k + 1, s =>
    let (c, s') := randClause n s
    let u := c.1 ||| c.2
    if ((c.1 &&& c.2) == 0) && (popcount u == 3) && (u < 2 ^ n) then go k s' else false

#eval genCheck 8 1000 20260805
#eval genCheck 16 1000 20260805

-- ===== 試行ループ =====

/-- m = round(alpha * n)。alpha は 1000 倍整数で受ける。 -/
def mOf (n a1000 : Nat) : Nat := (n * a1000 + 500) / 1000

structure Res where
  nSat : Nat
  totalSol : Nat

def runTrials (n m trials seed : Nat) : Res :=
  go trials (mix seed) ⟨0, 0⟩
where
  go : Nat → Nat → Res → Res
  | 0, _, acc => acc
  | t + 1, s, acc =>
    let (f, s') := randFormula n m s
    let c := satCount n f
    go t s' ⟨acc.nSat + (if c > 0 then 1 else 0), acc.totalSol + c⟩

/-- E[#解] × 100 = 2^n (7/8)^m × 100 (切り捨て)。厳密な有理数計算。 -/
def thSolx100 (n m : Nat) : Nat := (100 * 2 ^ n * 7 ^ m) / 8 ^ m

def line (n a1000 trials seed : Nat) : String :=
  let m := mOf n a1000
  let r := runTrials n m trials (seed + 7919 * a1000 + 104729 * n)
  let pct := (100 * r.nSat) / trials
  s!"n={n} a1000={a1000} m={m} sat={r.nSat}/{trials} pct={pct} avgSolx100={(100 * r.totalSol) / trials} thSolx100={thSolx100 n m}"

def sweep (n trials seed : Nat) (alphas : List Nat) : String :=
  String.intercalate "\n" (alphas.map (fun a => line n a trials seed))

def seed0 : Nat := 20260805

-- ===== 証明用の具体例抽出 =====

def toLeanList (f : List (Nat × Nat)) : String :=
  "[" ++ String.intercalate ", " (f.map (fun c => s!"({c.1}, {c.2})")) ++ "]"

def findInstance (n m seed trials : Nat) (wantSat : Bool) : Option (List (Nat × Nat)) :=
  go trials (mix seed)
where
  go : Nat → Nat → Option (List (Nat × Nat))
  | 0, _ => none
  | t + 1, s =>
    let (f, s') := randFormula n m s
    if (satCount n f != 0) == wantSat then some f else go t s'

#eval do
  match findInstance 8 40 12345 200 false with
  | some f => IO.println ("UNSAT_EXAMPLE n=8 m=40: " ++ toLeanList f)
  | none => IO.println "no UNSAT instance found"

#eval do
  match findInstance 8 24 54321 200 true with
  | some f => IO.println ("SAT_EXAMPLE n=8 m=24: " ++ toLeanList f)
  | none => IO.println "no SAT instance found"

-- ===== 本実験: alpha 掃引 =====

#eval IO.println "=== random 3-SAT phase transition (e2s, seed=20260805) ==="

#eval IO.println (sweep 8 200 seed0 [3000, 4000, 4270, 4500, 5000, 5500, 6000, 6500, 7000])

#eval IO.println (sweep 10 150 seed0 [3000, 4000, 4270, 4500, 5000, 5500, 6000, 6500, 7000])

#eval IO.println (sweep 12 100 seed0 [3000, 4000, 4270, 4500, 5000, 5500, 6000, 6500])

#eval IO.println (sweep 14 60 seed0 [3500, 4270, 4500, 5000, 5500, 6000])

#eval IO.println (sweep 16 30 seed0 [4000, 4270, 5000, 5500, 6000])

#eval IO.println "=== done ==="
