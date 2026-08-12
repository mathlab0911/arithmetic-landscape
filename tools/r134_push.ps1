$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r134.txt'
$body = @"
Ledger: a bound that cannot work, and the control that said so

Step 1 of the R1 attack was to bound the fourth-order Taylor error of log G~
uniformly over region R1. Measured against the exact product, that supremum is
about 840 and does not decrease with k -- 817 / 846 / 843 / 816 at k = 100 / 200
/ 300 / 450. No choice of radius repairs it: at the radius where the integrand
has already fallen to k^-10 it is still 2.7 to 9.4.

Meanwhile the Edgeworth expansion predicts the same probabilities to a relative
3e-5 at k = 64, checked against exact dynamic programming.

Both are true. The integral is dominated by |theta| <~ 1/sigma, and the error at
the edge of the region is never integrated against anything. Weighted by the
density, the error is 9e-4 at k = 100 and 9e-5 at k = 450 -- six to seven orders
of magnitude below the supremum, decaying at k^-3/2, faster than the leading
terms of the budget it was supposed to be a remainder for.

A sup-norm bound over a region where the integrand is already negligible charges
the whole region at its worst point. When the estimate is going into an integral,
estimate it under the integral. Before bounding, ask what the bound is for.

How it was caught: the negative control -- drop the K4 term and the error must
get worse -- did not fire; removing the term improved the sup-norm by 30%. That
is a control reporting that the quantity being measured is not the quantity the
theory is about. Last round an inverted control said the labels were crossed;
this round a non-firing control said the estimate was.

The design and its execution record are gitignored working material
(lean/pnp/spec_r1_r133.md, scripts in study-private-lab). No paper text changed.

C1-C19 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
& git status --short
