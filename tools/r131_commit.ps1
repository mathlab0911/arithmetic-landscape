$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'
& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)
& git add -A
$m = Join-Path $env:TEMP 'r131.txt'
$body = @"
Ledger: four blocks from the push round

Three scope lessons and one blind spot, written down while they are still
sharp: a reader-facing artefact is a scope and being inside the tree is not
being inside a check (F60); a push that reports success is not a reader seeing
the new state (F61); a region drawn too wide in an exemption forgives, where
the same region drawn too wide in a search only misses (F47); and the class of
things no tree can cover at all, because they are GitHub configuration rather
than content.

Reports rotated: r131 out, r129 archived.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m
& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
& git status --short
