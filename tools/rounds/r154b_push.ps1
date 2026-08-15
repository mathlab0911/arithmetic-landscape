$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add tools/ledger_pending.md
$m = Join-Path $env:TEMP 'r154b.txt'
$body = @"
Ledger: r154, and the general form of a lesson learned twice

The r154 block, plus the observation that ties it to r152.

A correction term is a map of its own failure. Once the size of the first error term is
known, the direction that makes it large is known too, and searching there is far cheaper
than guessing families. Two rounds ago prop:correction was only an accuracy statement; this
round it was a search strategy, and it found the witness on the first attempt.

Three controls on that witness, and the third is the one that stops it being over-read:
brute force against the DP at k = 8, 10, 12 with zero disagreements; window occupancy
printed; and Q(0)/sigma^2 = 0.07 against a 65% shortfall, which says the first-order term
does NOT explain the failure. It would have been easy and wrong to present this as "the
correction predicts the failure".

And the performance lesson, now stated in its general form. r152: a quantity indexed by a
shrinking set should be computed by shrinking the set. r154: a quantity indexed by an offset
that only changes the layer k times should be computed k times, by summing each block with
one prefix sum. Both are the same instruction --

    find the coarsest index on which the summand is constant, and loop on that.

Two timeouts bought the second half of it.

C1-C20 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
& git status --short
