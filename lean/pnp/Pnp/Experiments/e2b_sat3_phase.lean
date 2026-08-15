/-
  e2b_sat3_phase.lean — ランダム3-SAT相転移実験 (作業ID: e2b)

  モデル(標準的 random 3-SAT):
    n 変数, m = round(α·n) 節。各節は相異なる3変数を一様に選び,
    各リテラルの極性(肯定/否定)を確率 1/2 で独立に決める。
  ソルバ: 単位伝播つき DPLL(探索の分岐ノード数も計測)。
  検証: n=8 で全数探索(2^n 通り)と突き合わせる selftest 付き。

  使い方 (プロジェクト直下 lean/pnp から):
    lean --run .\Pnp\Experiments\e2b_sat3_phase.lean selftest
    lean --run .\Pnp\Experiments\e2b_sat3_phase.lean <n> <trials> <seed>
  出力: CSV
    alpha_pct,m,alpha_eff_pct,trials,sat,sat_pct,median_nodes,p90_nodes,max_nodes,ms
-/

-- ========== 乱数 (xorshift64*) ==========
structure Rng where
  state : UInt64

instance : Inhabited Rng := ⟨⟨0x9E3779B97F4A7C15⟩⟩

namespace Rng

def next (r : Rng) : UInt64 × Rng :=
  let x := r.state
  let x := x ^^^ (x <<< 13)
  let x := x ^^^ (x >>> 7)
  let x := x ^^^ (x <<< 17)
  (x * 2685821657736338717, ⟨x⟩)

/-- [0, bound) の一様乱数 (bound は 2^31 以下を想定; 剰余バイアスは無視できる大きさ) -/
def natLt (r : Rng) (bound : Nat) : Nat × Rng :=
  let (x, r') := r.next
  ((x >>> 33).toNat % bound, r')

/-- 公平なコイン投げ -/
def coin (r : Rng) : Bool × Rng :=
  let (x, r') := r.next
  (((x >>> 62) &&& 1) == 1, r')

end Rng

def mkRng (seed : Nat) : Rng :=
  let s := UInt64.ofNat seed * 6364136223846793005 + 1442695040888963407
  ⟨if s == 0 then 0x9E3779B97F4A7C15 else s⟩

-- ========== 3-SAT インスタンス生成 ==========
/-- リテラル: 正の Int は変数(1..n)の肯定, 負は否定 -/
abbrev Clause := List Int
abbrev Formula := List Clause

/-- 相異なる3変数 + ランダム極性の節を1つ生成(重複時はやり直しの棄却法) -/
partial def genClause (n : Nat) (r : Rng) : Clause × Rng :=
  let (a, r) := r.natLt n
  let (b, r) := r.natLt n
  let (c, r) := r.natLt n
  if a == b || b == c || a == c then
    genClause n r
  else
    let (sa, r) := r.coin
    let (sb, r) := r.coin
    let (sc, r) := r.coin
    let mk := fun (v : Nat) (s : Bool) =>
      if s then Int.ofNat (v + 1) else -(Int.ofNat (v + 1))
    ([mk a sa, mk b sb, mk c sc], r)

def genFormula (n m : Nat) (r0 : Rng) : Formula × Rng := Id.run do
  let mut r := r0
  let mut f : Formula := []
  for _ in [0:m] do
    let (c, r') := genClause n r
    r := r'
    f := c :: f
  return (f, r)

-- ========== DPLL ソルバ ==========
/-- リテラル l を真にして式を簡約。空節が生じたら none (矛盾)。 -/
def assignLit (l : Int) : Formula → Option Formula
  | [] => some []
  | c :: rest =>
    if c.contains l then
      assignLit l rest
    else
      let c' := c.filter (fun x => x != -l)
      if c'.isEmpty then none
      else
        match assignLit l rest with
        | none => none
        | some f' => some (c' :: f')

/-- 単位節 (長さ1の節) を探す -/
def findUnit : Formula → Option Int
  | [] => none
  | [l] :: _ => some l
  | _ :: rest => findUnit rest

/-- 分岐用リテラル: 最短の節の先頭リテラル -/
def chooseLit (f : Formula) : Int :=
  match f with
  | [] => 0
  | c :: rest =>
    let best := rest.foldl (fun b cc => if cc.length < b.length then cc else b) c
    best.head!

/-- DPLL 本体。戻り値は (充足可能か, 分岐ノード数)。 -/
partial def dpll (f : Formula) (nodes : Nat) : Bool × Nat :=
  match f with
  | [] => (true, nodes)
  | _ =>
    match findUnit f with
    | some l =>
      match assignLit l f with
      | none => (false, nodes)
      | some f' => dpll f' nodes
    | none =>
      let l := chooseLit f
      let nodes := nodes + 1
      match assignLit l f with
      | none =>
        match assignLit (-l) f with
        | none => (false, nodes)
        | some f2 => dpll f2 nodes
      | some f1 =>
        match dpll f1 nodes with
        | (true, nodes') => (true, nodes')
        | (false, nodes') =>
          match assignLit (-l) f with
          | none => (false, nodes')
          | some f2 => dpll f2 nodes'

-- ========== 全数探索 (検証用, n は 12 以下を想定) ==========
def litSat (asn : Nat) (l : Int) : Bool :=
  let v := l.natAbs - 1
  let bit := ((asn >>> v) &&& 1) == 1
  if l > 0 then bit else !bit

def bruteSat (n : Nat) (f : Formula) : Bool :=
  (List.range (2 ^ n)).any (fun asn => f.all (fun c => c.any (litSat asn)))

/-- DPLL と全数探索の突き合わせ + 固定ケースの検査 -/
def selftest : IO Unit := do
  let n := 8
  let total := 300
  let mut r := mkRng 20260805
  let mut bad := 0
  let mut satCnt := 0
  for i in [0:total] do
    let (dm, r') := r.natLt 51
    let m := 6 + dm      -- m ∈ [6,56] → α ∈ [0.75, 7.0]
    let (f, r'') := genFormula n m r'
    r := r''
    let (d, _) := dpll f 0
    let b := bruteSat n f
    if d != b then
      bad := bad + 1
      IO.println s!"MISMATCH i={i} m={m} dpll={d} brute={b} f={f}"
    if b then satCnt := satCnt + 1
  IO.println s!"selftest: n={n}, {total} random instances, mismatches={bad}, sat={satCnt}"
  let (u1, _) := dpll [[1], [-1]] 0
  let (u2, _) := dpll [[1, 2], [1, -2], [-1, 2], [-1, -2]] 0
  let (s1, _) := dpll ([] : Formula) 0
  let (s2, _) := dpll [[1, 2, 3], [-1, -2, -3]] 0
  IO.println s!"fixed cases (expect false false true true): {u1} {u2} {s1} {s2}"
  if bad == 0 && u1 == false && u2 == false && s1 == true && s2 == true then
    IO.println "SELFTEST PASSED"
  else
    IO.println "SELFTEST FAILED"

-- ========== 実験本体 ==========
/-- 調べる α の一覧 (百分率表記: 427 = α 4.27)。閾値予想 4.27 付近を密に。 -/
def alphaListPct : List Nat :=
  [300, 340, 370, 390, 400, 410, 420, 427, 435, 445, 460, 480, 500, 550]

def runExperiment (n trials seed : Nat) : IO Unit := do
  let stdout ← IO.getStdout
  IO.println s!"# e2b random 3-SAT: n={n} trials={trials} seed={seed}"
  IO.println "alpha_pct,m,alpha_eff_pct,trials,sat,sat_pct,median_nodes,p90_nodes,max_nodes,ms"
  let mut r := mkRng (seed + 1000003 * n)
  for apct in alphaListPct do
    let m := (apct * n + 50) / 100          -- m = round(α·n)
    let t0 ← IO.monoMsNow
    let mut sat := 0
    let mut nodesArr : Array Nat := #[]
    for _ in [0:trials] do
      let (f, r') := genFormula n m r
      r := r'
      let (ok, nd) := dpll f 0
      if ok then sat := sat + 1
      nodesArr := nodesArr.push nd
    let t1 ← IO.monoMsNow
    let sorted := nodesArr.qsort Nat.blt
    let med := sorted[trials / 2]!
    let p90 := sorted[(trials * 9) / 10]!
    let mx := sorted[trials - 1]!
    let aeff := (m * 100 + n / 2) / n       -- 実効 α = round(100·m/n)
    IO.println s!"{apct},{m},{aeff},{trials},{sat},{(100 * sat + trials / 2) / trials},{med},{p90},{mx},{t1 - t0}"
    stdout.flush

def main (args : List String) : IO Unit := do
  match args with
  | ["selftest"] => selftest
  | _ =>
    let n := ((args[0]?).bind String.toNat?).getD 20
    let trials := Nat.max 1 (((args[1]?).bind String.toNat?).getD 100)
    let seed := ((args[2]?).bind String.toNat?).getD 1
    if n < 3 then
      IO.println "error: n must be >= 3"
    else
      runExperiment n trials seed
