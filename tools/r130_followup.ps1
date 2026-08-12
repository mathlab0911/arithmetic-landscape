$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

Write-Output '=== check.py with the homepage visible ==='
& python tools\check.py | Select-Object -Last 3
Write-Output ("exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r130b.txt'
$body = @"
Post-push verification: the push was green and the reader saw the old page

F61, fetched over the public internet rather than read in the tree.  Three of
the four observations were what they should be -- the README serves the
three-part table and the C18 row, Part III serves its corrected title, the
retired paper 3 is gone from main with a positive control from the same
directory proving the fetch works.

The fourth was not.  https://mathlab0911.github.io/ -- the bare URL, the one in
the author footnotes and in the mail that went to two mathematicians -- was
still serving the old page a minute after a successful push, while
/index.html served the new one: the enumeration definition, "order-sensitive
invariant", four papers, and 5.34920, the literal C11 has banned since r118.
Two green pushes and a green C18 over the local file, and the reader's URL
still had the retracted sentence on it.  Re-fetch queued for r131.

Also stripped a UTF-8 BOM from the README, found only by fetching the raw
bytes: PowerShell 5.1's Set-Content -Encoding UTF8 writes one, and I used it
for the log-count edit an hour earlier.  GitHub renders it away, so it was
visible nowhere except where a reader would curl it.  Second BOM this round;
the first was in the commit message.

Log: lean/pnp/pushverify_r130.log.  C1-C18 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

Write-Output ''
& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
Write-Output ''
& git log --oneline -1
& git status --short
