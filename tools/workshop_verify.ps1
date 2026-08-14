$ErrorActionPreference = 'Continue'
$TREE = 'C:\Users\amake\Claude\Projects\study'
$GD   = 'C:\Users\amake\Claude\Projects\study-workshop.git'
Set-Location $TREE

Write-Output "=== branches on the PUBLIC repository (must be main only) ==="
& git ls-remote --heads origin
Write-Output ""

Write-Output "=== branches on the PRIVATE repository (main + workshop) ==="
& git ls-remote --heads private
Write-Output ""

Write-Output "=== does the PUBLIC repository contain any working document? (must be nothing) ==="
$hits = 0
foreach ($p in @('reports','book','paper-ja','docs','outgoing')) {
    $n = (& git ls-tree -r --name-only origin/main -- $p).Count
    Write-Output ("  {0,-10} {1}" -f $p, $n)
    $hits += $n
}
$n = (& git ls-tree -r --name-only origin/main -- 'lean/pnp/spec_*.md' 'lean/pnp/paper2_*.md').Count
Write-Output ("  spec/paper2 " + $n)
$hits += $n
Write-Output ("  TOTAL leaked into public: " + $hits)
Write-Output ""

Write-Output "=== positive control: the public repository is not simply empty ==="
Write-Output ("  files on origin/main: " + (& git ls-tree -r --name-only origin/main).Count)
Write-Output ("  README present: " + [bool](& git ls-tree -r --name-only origin/main -- README.md))
Write-Output ""

Write-Output "=== the workshop branch holds what it should ==="
Write-Output ("  files on workshop: " + (& git --git-dir=$GD ls-tree -r --name-only workshop).Count)
& git --git-dir=$GD ls-tree -r --name-only workshop | ForEach-Object { ($_ -split '/')[0] } |
    Group-Object | Sort-Object Count -Descending | ForEach-Object { Write-Output ("  {0,-12} {1}" -f $_.Name, $_.Count) }
Write-Output ""

Write-Output "=== and the workshop repository still cannot see the public remote ==="
& git --git-dir=$GD remote -v
