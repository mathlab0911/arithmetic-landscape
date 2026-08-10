# check_lean.ps1 -- independent kernel replay of the ALT canon.
#
# What this adds on top of `lake build`: `lake build` trusts the elaborator, the tactic
# framework and the environment as it was left by the .lean files.  lean4checker throws all
# of that away and replays every constant of the listed modules through the KERNEL from the
# imports up.  It catches proofs that were never really checked (unsafe, implemented_by,
# native_decide), axioms swapped after the fact, and environment tampering.
#
# What it does NOT add: it uses the same kernel implementation, so it does not protect
# against a kernel bug.  For that you want a second, independent checker (nanoda_bin, Rust);
# see references/lean-recipes.md.  And neither of them tells you the STATEMENT is the one you
# meant -- that is F52's job, and the two axes must not be confused (F54).
#
# Usage:   powershell -ExecutionPolicy Bypass -File tools\check_lean.ps1
# Cost:    about 160 s for the closure of Pnp on this machine.
# Fail rule: EXIT 0 with the negative control failing is a pass.  EXIT 0 with the negative
#            control ALSO passing means the harness is broken -- report, do not celebrate.
#
# Exit 4 = closure check failed.  See the block below: this was added in r117 after
# Pnp/Theory/Cyclotomic.lean was found sitting in the tree, counted as canon in the project
# memory, and imported by nothing -- so `lake build` never built it and lean4checker never
# saw it.  "The file exists" is not "the file is checked" (F55).

# NOTE, and it cost a run: this script deliberately invokes commands that MUST fail (the
# negative control).  With $ErrorActionPreference = 'Stop' PowerShell turns their stderr into
# a terminating error and the harness dies reporting its own success criterion as a crash.
# A harness that runs negative controls must not treat their failure as its own.
$ErrorActionPreference = 'Continue'
$env:Path = "$env:USERPROFILE\.elan\bin;" + $env:Path

$exe  = "C:\Users\amake\Claude\Projects\tools\lean4checker\.lake\build\bin\lean4checker.exe"
$proj = "C:\Users\amake\Claude\Projects\study\lean\pnp"

if (-not (Test-Path $exe)) {
  Write-Host "lean4checker not built.  Build it with:"
  Write-Host "  git clone https://github.com/leanprover/lean4checker C:\Users\amake\Claude\Projects\tools\lean4checker"
  Write-Host "  cd ...\lean4checker; Set-Content lean-toolchain 'leanprover/lean4:v4.32.2' -NoNewline; lake build"
  Write-Host "(a `leanchecker.exe` also ships inside the elan toolchain; the external build was"
  Write-Host " used here because it takes an explicit module list.)"
  exit 2
}

Write-Host "=== negative control: modules that MUST fail ==="
$ncOk = $true
Push-Location "C:\Users\amake\Claude\Projects\tools\lean4checker"
foreach ($m in @('Lean4CheckerTests.AddFalse','Lean4CheckerTests.ReplaceAxiom',
                 'Lean4CheckerTests.AddFalseConstructor')) {
  & { lake env $exe $m } 2>&1 | Out-Null
  if ($LASTEXITCODE -eq 0) { Write-Host "  !! $m PASSED -- the harness is not checking anything"; $ncOk = $false }
  else                     { Write-Host "  ok $m rejected (exit $LASTEXITCODE)" }
}
Pop-Location
if (-not $ncOk) { Write-Host "NEGATIVE CONTROL FAILED -- do not trust the run below."; exit 3 }

Write-Host "=== closure check: every CANON file must be reachable from the root module ==="
# lean4checker replays the import CLOSURE of `Pnp`, not the directory.  A .lean file that
# nothing imports is neither built nor replayed while still looking canonical in the tree.
#
# Scope, and it matters: the canon is Pnp/Theory + Pnp/Basic.  Pnp/Experiments is deliberately
# outside the closure -- scratch work, not claims -- so requiring the whole tree would make
# this check fail permanently, and a check that always fails is a check nobody reads.  The
# excluded count is printed rather than assumed, so the exclusion stays visible.
$srcRoot = Join-Path $proj 'Pnp'
$canonDirs = @('Theory')
$all = Get-ChildItem -Path $srcRoot -Recurse -Filter *.lean | ForEach-Object {
  $rel = $_.FullName.Substring($srcRoot.Length + 1)
  [pscustomobject]@{
    Module = 'Pnp.' + (($rel -replace '\\', '.') -replace '\.lean$', '')
    Canon  = ($rel -notmatch '\\') -or ($canonDirs -contains ($rel -split '\\')[0])
  }
}
$excluded = @($all | Where-Object { -not $_.Canon })
Write-Host "  (not canon, deliberately outside the closure: $($excluded.Count) file(s) under Pnp/Experiments)"
$all = @($all | Where-Object { $_.Canon } | ForEach-Object { $_.Module })
$closure = New-Object 'System.Collections.Generic.HashSet[string]'
$stack   = New-Object System.Collections.Stack
$stack.Push('Pnp')
while ($stack.Count -gt 0) {
  $m = $stack.Pop()
  if (-not $closure.Add($m)) { continue }
  $f = Join-Path $proj (($m -replace '\.', '\') + '.lean')
  if (-not (Test-Path $f)) { continue }
  foreach ($line in Get-Content $f) {
    if ($line -match '^\s*import\s+(Pnp[\w.]*)') { $stack.Push($Matches[1]) }
  }
}
$orphans = @($all | Where-Object { -not $closure.Contains($_) })
if ($orphans.Count -gt 0) {
  Write-Host "  !! outside the closure of Pnp -- NOT built, NOT replayed, but present:"
  $orphans | ForEach-Object { Write-Host "     $_" }
  Write-Host "  Fix: import it from Pnp.lean, or move it out of Pnp/ if it is not canon."
  exit 4
}
Write-Host "  ok all $($all.Count) source files are in the closure of Pnp"

Write-Host "=== canon: Pnp ==="
Push-Location $proj
$t0 = Get-Date
& { lake env $exe Pnp } 2>&1 | Write-Host
$code = $LASTEXITCODE
Pop-Location
$sec = [math]::Round(((Get-Date) - $t0).TotalSeconds, 1)

if ($code -eq 0) { Write-Host "PASS -- every constant of the canon replayed through the kernel ($sec s)" }
else             { Write-Host "FAIL -- lean4checker rejected the canon (exit $code, $sec s)" }
exit $code
