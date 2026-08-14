$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

Write-Output "=== current remotes ==="
& git remote -v

Write-Output ""
Write-Output "=== current branch and head ==="
& git rev-parse --abbrev-ref HEAD
& git log --oneline -1
Write-Output ("commits on main: " + (& git rev-list --count HEAD))

Write-Output ""
Write-Output "=== adding the private remote (idempotent) ==="
$have = (& git remote) -contains 'private'
if (-not $have) {
  & git remote add private https://github.com/mathlab0911/arithmetic-landscapes-private.git
  Write-Output "added"
} else {
  & git remote set-url private https://github.com/mathlab0911/arithmetic-landscapes-private.git
  Write-Output "already present; url refreshed"
}

Write-Output ""
Write-Output "=== is the private repository reachable, and is it empty? ==="
& git ls-remote --heads private 2>&1 | Select-Object -First 10
Write-Output ("ls-remote exit=" + $LASTEXITCODE)

Write-Output ""
Write-Output "=== remotes after ==="
& git remote -v
