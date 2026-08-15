$ErrorActionPreference = 'Continue'
$TREE = 'C:\Users\amake\Claude\Projects\study'
$GD   = 'C:\Users\amake\Claude\Projects\study-workshop.git'
Set-Location $TREE

Write-Output "=== does the exclude file exist and what is in it? ==="
$ex = Join-Path $GD 'info\exclude'
Write-Output ("path: " + $ex + "   exists: " + (Test-Path $ex))
Get-Content $ex | Select-Object -First 25

Write-Output ""
Write-Output "=== config ==="
& git --git-dir=$GD config --list | Select-String 'core\.|remote\.'

Write-Output ""
Write-Output "=== do the directories actually exist on disk? ==="
foreach ($p in @('reports','book','paper-ja','docs','outgoing')) {
    $full = Join-Path $TREE $p
    $n = 0
    if (Test-Path $full) { $n = (Get-ChildItem $full -Recurse -File -ErrorAction SilentlyContinue).Count }
    Write-Output ("  {0,-10} exists={1,-5} files={2}" -f $p, (Test-Path $full), $n)
}
Write-Output ("  spec_*.md  " + (Get-ChildItem (Join-Path $TREE 'lean\pnp') -Filter 'spec_*.md' -ErrorAction SilentlyContinue).Count)
Write-Output ("  paper2_*.md " + (Get-ChildItem (Join-Path $TREE 'lean\pnp') -Filter 'paper2_*.md' -ErrorAction SilentlyContinue).Count)

Write-Output ""
Write-Output "=== check-ignore: why is a known file excluded? ==="
foreach ($f in @('reports/to-fable5/r155.md','paper-ja/paper1_ja.tex','lean/pnp/spec_future_r145.md')) {
    Write-Output ("--- " + $f)
    & git --git-dir=$GD --work-tree=$TREE check-ignore -v --no-index $f 2>&1
    Write-Output ("   (exit " + $LASTEXITCODE + ")")
}

Write-Output ""
Write-Output "=== status --porcelain, first 20 ==="
& git --git-dir=$GD --work-tree=$TREE status --porcelain 2>&1 | Select-Object -First 20
Write-Output ("status exit=" + $LASTEXITCODE)

Write-Output ""
Write-Output "=== add --dry-run on ONE explicit path ==="
& git --git-dir=$GD --work-tree=$TREE add --dry-run --force reports 2>&1 | Select-Object -First 5
