# P≠NP研究用 Lean 4 セットアップ(Windows)
# 賢太郎さんの承認を得てから、desktop-commander で実行する:
#   powershell -ExecutionPolicy Bypass -File <このファイル>
# 冪等: 導入済みの手順は自動でスキップされる。管理者権限は不要。

$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$LeanRoot   = "C:\Users\amake\Claude\Projects\study\lean"
$ProjectDir = Join-Path $LeanRoot "pnp"
$ElanBin    = "$env:USERPROFILE\.elan\bin"
$env:Path   = "$ElanBin;" + $env:Path

# --- 1/4: elan(Leanツールチェーン管理) ---
if (Get-Command elan -ErrorAction SilentlyContinue) {
  Write-Host "[1/4] elan は導入済み: $(elan --version)"
} else {
  Write-Host "[1/4] elan をインストールします(初回のみ)..."
  $tmp = Join-Path $env:TEMP "elan-setup"
  New-Item -ItemType Directory -Force -Path $tmp | Out-Null
  $zip = Join-Path $tmp "elan.zip"
  Invoke-WebRequest -UseBasicParsing -Uri "https://github.com/leanprover/elan/releases/latest/download/elan-x86_64-pc-windows-msvc.zip" -OutFile $zip
  Expand-Archive -Path $zip -DestinationPath $tmp -Force
  & (Join-Path $tmp "elan-init.exe") -y --default-toolchain stable
  if ($LASTEXITCODE -ne 0) { throw "elan-init が失敗しました (exit $LASTEXITCODE)" }
  $env:Path = "$ElanBin;" + $env:Path
  Write-Host "  導入完了: $(elan --version)"
}

# --- 2/4: Lean ツールチェーン(stable) ---
Write-Host "[2/4] Lean stable を確認します(未取得なら数百MBのダウンロードが走ります)..."
elan default stable
lean --version
lake --version

# --- 3/4: 検証用プロジェクト pnp ---
if ((Test-Path (Join-Path $ProjectDir "lakefile.toml")) -or (Test-Path (Join-Path $ProjectDir "lakefile.lean"))) {
  Write-Host "[3/4] プロジェクトは作成済み: $ProjectDir"
} else {
  Write-Host "[3/4] Lean プロジェクトを作成します: $ProjectDir"
  New-Item -ItemType Directory -Force -Path $LeanRoot | Out-Null
  Push-Location $LeanRoot
  lake new pnp lib
  Pop-Location
}
New-Item -ItemType Directory -Force -Path (Join-Path $ProjectDir "Pnp\Experiments") | Out-Null
# --- 4/4: 動作確認(スモークテスト) ---
Write-Host "[4/4] スモークテストを実行します..."
$smoke = Join-Path $ProjectDir "Pnp\Experiments\Smoke.lean"
$code = @'
def hello := "P≠NP lab ready"
#eval hello

theorem smoke : 2 + 2 = 4 := by decide
#print axioms smoke
'@
[IO.File]::WriteAllText($smoke, $code, [Text.UTF8Encoding]::new($false))
Push-Location $ProjectDir
lake env lean .\Pnp\Experiments\Smoke.lean
$ok = $LASTEXITCODE
Pop-Location
if ($ok -ne 0) { throw "スモークテスト失敗 (exit $ok)" }

Write-Host ""
Write-Host "=== SETUP COMPLETE ==="
Write-Host "プロジェクト: $ProjectDir"
Write-Host "実験ファイル置き場: $ProjectDir\Pnp\Experiments"
