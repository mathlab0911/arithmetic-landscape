$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'
Write-Output '=== check.py on the final tree ==='
& python tools\check.py | Select-Object -Last 2
Write-Output ("check.py exit=" + $LASTEXITCODE)
Write-Output ''
Write-Output '=== git status ==='
& git status --short
Write-Output ''
Write-Output '=== unpushed commits ==='
& git log --oneline origin/main..HEAD
