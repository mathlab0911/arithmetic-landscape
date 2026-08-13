$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r149.txt'
$body = @"
prop:schur -- Gamma is Schur-concave; and where this sits beside the local REM theorems

Kentaro asked what modern mathematics could be applied here. Two answers, one a theorem
and one a placement, and both came from asking the question rather than from working
harder on what we already had.

1. MAJORIZATION. prop:schur: Gamma is Schur-concave.

Abel summation on prop:gapform writes Gamma as an ordered weighted average

    Gamma(A) = sum_j w_j a_j,  a_1 < ... < a_k,
    (w_1,...,w_k) = (1/2, 1/4, ..., 2^{-(k-1)}, 2^{-(k-1)}),

positive and NON-INCREASING along the ascending order. Schur-Ostrowski then reads off
Schur-concavity in one line: a_i > a_j forces i > j forces w_i <= w_j, so
(a_i - a_j)(d_i Gamma - d_j Gamma) <= 0. Measured for confirmation on 4000
majorization-comparable pairs; Gamma was larger on the more equal set in every case that
was not a tie.

What it buys: Gamma is now inside Hardy-Littlewood-Polya, so Karamata and the standard
majorization toolkit apply without further work, and any "extremal on the most/least
spread set of a given sum" statement becomes a corollary. What it explains is better.
Schur-concavity says precisely that GAMMA REWARDS EQUALITY AND PUNISHES SPREAD -- the
exact version of the informal "Gamma is a bottom statistic" used throughout the series --
and it says why Gamma separates sets a second moment cannot: variance is Schur-CONVEX and
moves the other way. Not competing measures of one thing; opposite monotonicity under one
partial order.

2. PLACEMENT. rem:localrem, beside the rigorous number-partitioning literature.

Subset-sum at the centre is number partitioning. Borgs-Chayes-Pittel established its
phase transition and finite-size scaling; Bauke-Franz-Mertens conjectured local REM
statistics for the spectrum, and Borgs-Chayes-Mertens-Nair proved it. Ours is complement,
not overlap, and the difference is the whole novelty claim: their instances are RANDOM and
the statement is distributional about spectral spacings, converging to a Poisson process;
ours is a DETERMINISTIC instance -- the odd primes -- counting metastable states and
producing an EXACT CONSTANT. Neither implies the other so far as I can see. The remark
says outright that the papers are cited from abstracts and titles, that we have not worked
through them, and that after three classical transports in one paper the prior on novelty
should not be generous.

3. C20 CONVICTED THE MOST HONEST TEXT IN THE FILE, AGAIN, AND FOR A NEW REASON.

prop:schur's Japanese status was exempt by the phrase 確認のための測定 -- measurement for
confirmation only -- which the typesetter had split as 確認のための\n測定のみ. Japanese has
no inter-word spaces, so a hard line break falls mid-phrase; an English marker survives
\s+ because English breaks at spaces, and its Japanese counterpart does not survive at
all. The check now unwraps before matching: drop the newline between two non-ASCII
neighbours, otherwise make it a space.

The fix bred its own bug within the minute. Unwrapping broke the prose half, which blanked
statuses via prose.replace(block, ...) -- the unwrapped block no longer occurs verbatim, so
replace found nothing, failed silently, and handed every status back to the stricter rule.
A replace that finds nothing does not raise. Where the intent is "remove this region",
address it by span, not by content: content-based removal is a lookup that can miss, and
missing looks exactly like success. Now span-based.

Controls are seven: five defects fire, two escapes proved still open (the open register,
and a benign phrase split across a line break). c20control_r149 is committed.

Part I 25 pp both editions, Part III 40 pp both. C1-C20 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
