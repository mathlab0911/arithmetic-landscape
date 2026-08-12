$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r135.txt'
$body = @"
Ledger: three controls in three rounds, three different messages

Measuring the constant in |log f - P4| <= C pq |v|^5 over the phases the tilt
produces, the first run reported C reaching 10^9, always at the smallest element
and v about 1e-4. Not a blow-up: the quantity there is 1e-20, double precision
has lost it, and dividing by v^5 = 1e-20 amplifies noise to O(1). That is F51's
own sentence -- identify the operation that amplifies rounding and restate the
comparison without it -- walked into while holding the ledger containing it.
Redone at 50 digits: C is 0.0053 to 0.0093, stable, and worst at the LARGE
elements, exactly where the naive fear said it would not be.

The sanity line then caught a second defect, in the prediction rather than the
code. I predicted the v -> 0 limit as |1 - 12pq + 24(pq)^2|/120 and it matched at
no p. The fifth Bernoulli cumulant is pq(1-2p)(1-12pq); against that the
measurement agrees to eight digits everywhere. The computation was right and my
formula was wrong.

Three rounds, three controls, three different places: r133 the harness labels
were crossed; r134 the estimate was not the quantity the theory is about; r135
the closed form being checked against was wrong. A control does not say what is
broken -- it says that two things you thought were the same are not, and which
two.

Operational note: put the analytic limit of a ratio in the harness as a sanity
line, not the ratio alone. The C table looked perfectly reasonable in both runs;
only the predicted limit separated them. The stale MISMATCH lines were also
removed from the log rather than left to be read as a real failure.

Working material is gitignored (lean/pnp/spec_r1_r133.md, study-private-lab).
No paper text changed.

C1-C19 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
& git status --short
