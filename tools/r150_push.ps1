$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r150.txt'
$body = @"
prop:correction -- the first correction term, and it was already in the paper

Applying the local limit theorem layer by layer at the centre and expanding to first
order in 1/sigma^2:

    lm/r = Gamma(A) * (1 - Q(0)/sigma^2) + o(sigma^-2),
    Q(0) = Gamma^-1 sum_d 2^{-N_d} (delta_d^2 - s_d/4).

Q(0) IS THE QUANTITY THE COUNTEREXAMPLE SECTION ALREADY TABULATES -- 20.3 for the odds,
50.4 for the primes, 916 for the squares, 3.8e5 for the cubes. It was put there to show
how far out of reach a profile is. It is, to first order, the error itself. We have had
the correction term printed in a table for dozens of rounds and read it as a difficulty
index; what made it legible was r147's reframing, because once the theorem is "the
annealed count is exact" the next question is "how exact", and the answer was on the page.

Verified against exact dynamic programming: measured/predicted = 0.98 at k = 90 on all
three profile families, including the one where (H) fails.

Three consequences, in rem:correctionH. The rate is explained rather than fitted (k^-3 for
the odds, k^-4 for i^{3/2}). (H) asks Q(0) = O(1) but the limit needs only Q(0) = o(sigma^2),
which is strictly weaker. And for power profiles distinctness forces sigma^2 ~ k^3 for
EVERY alpha while Q(0) ~ k^{3(1-alpha)}, so the ratio is k^{-3alpha} and every alpha > 0
works -- prob:hrate is settled affirmatively for clean powers by the formula rather than by
extrapolation, and stands for everything else.

It also corrects this project's own number from two commits ago. The fitted exponent 0.98
for alpha = 1/2 was contaminated by the smallest size, where the measured error changes
sign; the honest fit over the rest is 1.7 against a predicted 1.5. prob:hrate now says so
in its own text rather than quietly restating a better number.

A measurement bug that nearly became a discovery, and it is in the ledger. The translated
block {2m+1,...,2m+2k-1} returned a relative error of -3.7 -- lm/r nearly five times Gamma
-- which for ten minutes looked like the counterexample the open problem wants. It was the
measurement. Every subset sum of that family clusters near multiples of 2m, so a window of
41 consecutive targets is mostly EMPTY and the unweighted mean of ratios averages an
atypical subset. The r-weighted statistic sum lm / sum r -- the ratio at a typical ground
state, which is what the theorem is about -- makes it vanish. When a family produces a
spectacular result, check the support before checking the theory. The window occupancy is
now a printed column in the log.

Part III 40 -> 41 pp, Japanese 41 pp. C1-C20 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
