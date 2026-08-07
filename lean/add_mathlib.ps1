# pnp プロジェクトへの Mathlib 導入(2026-08-05 賢太郎さん承認済み)
# 冪等。UTF-8 BOM付きで保存して実行すること(references/lean-recipes.md §7)。
$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$env:Path = "$env:USERPROFILE\.elan\bin;" + $env:Path
$Proj = "C:\Users\amake\Claude\Projects\study\lean\pnp"
Set-Location $Proj

Write-Host "[1/5] backup commit"
$ErrorActionPreference = "Continue"
git add -A | Out-Null
git commit -m "pre-mathlib snapshot" | Out-Null
$ErrorActionPreference = "Stop"
Write-Host "  ok (or nothing to commit)"

Write-Host "[2/5] lakefile.toml に mathlib require を追加"
$lf = Get-Content -Raw lakefile.toml
if ($lf -match "mathlib") {
  Write-Host "  already present"
} else {
  $req = "`n[[require]]`nname = `"mathlib`"`ngit = `"https://github.com/leanprover-community/mathlib4`"`nrev = `"v4.32.2`"`n"
  Add-Content -Path lakefile.toml -Value $req
  Write-Host "  added: mathlib rev v4.32.2 (toolchain一致確認済み)"
}

Write-Host "[3/5] lake update mathlib (mathlib本体+依存の取得、数分)"
lake update mathlib
if ($LASTEXITCODE -ne 0) { throw "lake update failed (exit $LASTEXITCODE)" }

Write-Host "[4/5] lake exe cache get (ビルド済みキャッシュ数GBのダウンロード)"
lake exe cache get
if ($LASTEXITCODE -ne 0) { throw "cache get failed (exit $LASTEXITCODE)" }

Write-Host "[5/5] Mathlib import スモークテスト"
$smoke = Join-Path $Proj "Pnp\Experiments\MathlibSmoke.lean"
$code = @'
import Mathlib.Tactic

theorem mlib_smoke1 : (2 : Rat) + 2 = 4 := by norm_num
theorem mlib_smoke2 (x : Real) (h : 0 < x) : 0 < 2 * x := by linarith
#print axioms mlib_smoke2
'@
[IO.File]::WriteAllText($smoke, $code, [Text.UTF8Encoding]::new($false))
lake env lean $smoke
if ($LASTEXITCODE -ne 0) { throw "mathlib smoke failed (exit $LASTEXITCODE)" }

Write-Host ""
Write-Host "=== MATHLIB READY ==="
lean --version
Write-Host "project: $Proj (mathlib v4.32.2 pinned)"
