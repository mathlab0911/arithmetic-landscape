$ErrorActionPreference = 'Continue'

Write-Output '=== homepage: commit ==='
Set-Location 'C:\Users\amake\Claude\Projects\homepage'
& git add -A
$m = Join-Path $env:TEMP 'hp_msg.txt'
$body = @"
Rewrite for the three-part series, with the disclosure

The page had drifted further than anything in the repository: it defined Gamma
by the enumeration form retired at r120, called it an order-sensitive invariant
(false under the layer definition), listed four papers, and printed 5.34920 --
the erratum banned in check.py since r118, and banned there over the paper trees
only, which is why it survived here for weeks.  It carried no AI disclosure
while every paper now does.

Rewritten: the research paragraph opens with r_A(n) and the truncations, so a
reader meets the objects before the vocabulary; three parts with their current
titles and statuses; a Use of AI tools section matching the papers word for
word.  C18 in the research repository now reads this file.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m
& git log --oneline -1

Write-Output ''
Write-Output '=== research repo: push ==='
Set-Location 'C:\Users\amake\Claude\Projects\study'
& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)

Write-Output ''
Write-Output '=== homepage: push ==='
Set-Location 'C:\Users\amake\Claude\Projects\homepage'
& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)

Write-Output ''
Write-Output '=== after ==='
Set-Location 'C:\Users\amake\Claude\Projects\study'
Write-Output 'research:'
& git log --oneline origin/main..HEAD
& git status --short
Set-Location 'C:\Users\amake\Claude\Projects\homepage'
Write-Output 'homepage:'
& git log --oneline origin/main..HEAD
& git status --short
