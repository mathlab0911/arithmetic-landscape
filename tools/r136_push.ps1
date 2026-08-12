$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r136.txt'
$body = @"
Ledger: the hypothesis died, and its claim ceiling was the diagnostic

Three rounds ago an out-of-sample prediction held to +0.72%: the residual
constant c_A matched the first-order Edgeworth coefficient across four profiles.
The claim was capped at the time -- the profile dependence agrees to 0.7-2.4%
and the x dependence does not -- because the x dependence disagreed and there
was no reason for it to.

Checked by exact integer dynamic programming, the mechanism does not exist. The
Edgeworth corrections cancel between numerator and denominator: the layer B_d
differs from the whole set only in its N_d smallest elements, so the two have
nearly identical cumulant ratios and their corrections divide out. The measured
difference is two to three orders below the factor that actually explains the
residual, which the paper already names.

The agreement was real and its cause was mundane: K4/(8 sigma^4) is proportional
to S4/S2^2, with a constant universal to 0.6% across four profiles, and S4/S2^2
was already recorded as the shared driver. The same quantity appearing a third
time, not a new mechanism.

The part worth keeping is that the ceiling was the diagnostic. The x-dependence
disagreement was written down as a limitation three rounds before the explanation
was known, and it was exactly the fingerprint of the true cause -- a driver shared
at leading order and not beyond it. A hedge written honestly is not padding; it
is where the next finding comes from.

Corollary for the graveyard, applied: when an open question is answered, delete
the question and record the answer. This one had stood since r088 and would have
been rediscovered a fourth time.

Working material is gitignored. No paper text changed.

C1-C19 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
& git status --short
