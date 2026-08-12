$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'
& git add -A
& git commit -q --amend --no-edit
Write-Output '=== research repo: working tree ==='
& git status --short
Write-Output '=== research repo: commits waiting to be pushed ==='
& git log --oneline origin/main..HEAD
Write-Output ''
Set-Location 'C:\Users\amake\Claude\Projects\homepage'
Write-Output '=== homepage repo ==='
& git status --short
& git log --oneline origin/main..HEAD 2>&1
