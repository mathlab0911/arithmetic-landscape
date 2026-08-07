-- 算術地形理論 実験2 (2026-08-07, opus-5セッション)
-- 100シードのランダム奇数列で lm / deg / Γ を per-seed 計測し、
-- P1(lm と Γ の相関)・P2(絶対公式)・lm/deg ≈ Γ を検証する。
-- 出力: results_landscape_r2.csv

def isPrime (n : Nat) : Bool :=
  n ≥ 2 && ((List.range n).all fun d => d < 2 || n % d != 0)

def oddPrimes (k : Nat) : List Nat :=
  (((List.range 400).filter (fun n => isPrime n && n % 2 == 1)).take k)

def lcgNext (s : UInt64) : UInt64 :=
  s * 6364136223846793005 + 1442695040888963407

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

-- Γ(A) = Σ_{j=1..k} a_j / 2^j (昇順に並べた列に対して評価する)
def gammaOf (l : List Nat) : Float := Id.run do
  let mut g : Float := 0.0
  let mut p : Float := 1.0
  for x in l do
    p := p / 2.0
    g := g + p * x.toFloat
  return g

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

def rowOf (label : String) (k : Nat) (seed : Nat) (l : List Nat) : String := Id.run do
  let ls := l.mergeSort (· ≤ ·)
  let a := ls.toArray
  let total := ls.foldl (· + ·) 0
  let sumsq := ls.foldl (fun acc x => acc + x * x) 0
  let sums := subsetSums a
  let n := total / 2
  let (gs, deg, lm) := invariants a sums n
  let g := gammaOf ls
  return s!"{label},{k},{seed},{total},{sumsq},{n},{gs},{deg},{lm},{g}"

def main (args : List String) : IO Unit := do
  let nseeds := (args.getD 0 "100").toNat!
  let mut out : List String :=
    ["seq,k,seed,total,sumsq,n,gs,deg,lm,gamma"]
  for k in [8, 12, 16, 18, 20] do
    let primes := oddPrimes k
    let maxV := primes.getLast!
    out := out ++ [rowOf "primes" k 0 primes]
    IO.println s!"k={k} primes done (maxV={maxV})"
    for i in [0:nseeds] do
      let seed : UInt64 := (20260807 + i * 2654435761).toUInt64
      let rands := randOdds k maxV seed
      out := out ++ [rowOf "random" k i rands]
    IO.println s!"k={k} {nseeds} seeds done"
    IO.FS.writeFile "results_landscape_r2.csv" (String.intercalate "\n" out ++ "\n")
  IO.println "WROTE results_landscape_r2.csv"
