-- 算術地形理論 実験1 (2026-08-07, fable-5セッション)
-- {0,1}^k 部分和地形の不変量: gs(基底状態値)/ deg(縮退度)/ lm(厳密局所最小数)
-- 対象: 奇素数列 vs シード固定ランダム奇数列。出力: results_landscape_r1.csv

def isPrime (n : Nat) : Bool :=
  n ≥ 2 && ((List.range n).all fun d => d < 2 || n % d != 0)

def oddPrimes (k : Nat) : List Nat :=
  (((List.range 400).filter (fun n => isPrime n && n % 2 == 1)).take k)

def lcgNext (s : UInt64) : UInt64 :=
  s * 6364136223846793005 + 1442695040888963407

-- [3, maxV] の奇数から重複なしで k 個選ぶ(シード固定・再現可能)
def randOdds (k maxV : Nat) (seed : UInt64) : List Nat :=
  let cands := (List.range (maxV + 1)).filter (fun n => n ≥ 3 && n % 2 == 1)
  let rec go (s : UInt64) (cs : List Nat) (acc : List Nat) (m : Nat) : List Nat :=
    match m, cs with
    | 0, _ => acc.reverse
    | _, [] => acc.reverse
    | m + 1, cs =>
      let s' := lcgNext s
      let i := (s' >>> 33).toNat % cs.length
      go s' (cs.eraseIdx i) (cs[i]! :: acc) m
  go seed cands [] k

def dist (a b : Nat) : Nat := if a ≥ b then a - b else b - a

-- 全部分和(インデックスのビットiが第i項の採否に対応)
def subsetSums (a : Array Nat) : Array Nat := Id.run do
  let mut acc : Array Nat := #[0]
  for x in a do
    let mut nxt := Array.mkEmpty (acc.size * 2)
    for s in acc do nxt := nxt.push s
    for s in acc do nxt := nxt.push (s + x)
    acc := nxt
  return acc

-- 1つの目標 n について (gs, deg, lm) を全数計算
def invariants (a : Array Nat) (sums : Array Nat) (n : Nat) : Nat × Nat × Nat := Id.run do
  let k := a.size
  let mut gs := dist 0 n
  for s in sums do
    let e := dist s n
    if e < gs then gs := e
  let mut deg := 0
  let mut lm := 0
  for idx in [0:sums.size] do
    let s := sums[idx]!
    let e := dist s n
    if e == gs then deg := deg + 1
    let mut isMin := true
    for i in [0:k] do
      let ns := if (idx >>> i) &&& 1 == 1 then s - a[i]! else s + a[i]!
      if dist ns n ≤ e then isMin := false
    if isMin then lm := lm + 1
  return (gs, deg, lm)

def analyzeSeq (label : String) (l : List Nat) : List String := Id.run do
  let a := l.toArray
  let k := a.size
  let total := l.foldl (· + ·) 0
  let sums := subsetSums a
  let mut rows : List String := []
  -- 密度 ρ = n/total を 5%〜95% で走査
  for p in [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95] do
    let n := total * p / 100
    let (gs, deg, lm) := invariants a sums n
    rows := rows ++ [s!"{label},{k},{total},{p},{n},{gs},{deg},{lm}"]
  return rows

def main : IO Unit := do
  let mut out : List String := ["seq,k,total,rho_pct,n,gs,deg,lm"]
  for k in [8, 12, 16, 18, 20] do
    let primes := oddPrimes k
    let maxV := primes.getLast! -- 乱数列は同じ値域 [3, p_max] から取る
    let rands := randOdds k maxV 20260807
    out := out ++ analyzeSeq "primes" primes
    out := out ++ analyzeSeq "random" rands
    IO.println s!"k={k} primes={primes} rands={rands}"
  IO.FS.writeFile "results_landscape_r1.csv" (String.intercalate "\n" out ++ "\n")
  IO.println "WROTE results_landscape_r1.csv"
