$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r140.txt'
$body = @"
Ledger: the degenerate case was a theorem, and it nearly closed the lead

Testing whether Gamma says anything about numerical semigroups beyond what its
smallest generator says. The first control ruled out the obvious confounder: at
fixed smallest generator the correlation with the Frobenius number survives at
0.65 to 0.80 across ten cells, with a null control never above 0.17.

The second control was the one that mattered. Gamma has a closed form --
a1/2 + a2/4 + ... + a_{k-1}/2^{k-1} + a_k/2^{k-1}, verified against the sieve
definition and identical to Part I's gap form written in weights -- and from it,
at k=2 Gamma IS the mean, and at k=3 with a1 fixed it is affine in a2+a3 and so
perfectly correlated with the mean. Not approximately: provably. That is why the
measured correlations at k=3 matched the mean's to four decimals, and it means no
amount of data at small k could ever have shown Gamma carrying its own signal.

Where a closed form exists, the degenerate cases are theorems rather than data
points, and they are the cheapest place to discover that your statistic is
something else wearing a different name. Evaluate the closed form at the smallest
cases before running the correlation, not after.

Verdict on the lead: alive and weak. From k >= 5 Gamma beats the best one-line
statistic, but by 0.01 to 0.04 in correlation, not a separation. What would change
the answer is a formula or an inequality, not a better correlation -- two
quantities that both grow with the generators correlate at 0.85 for free. Recorded
with that as the next test, and not worth a paragraph in any paper until then.

No paper text changed this round; the r139 changes stand.

C1-C19 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
& git status --short
