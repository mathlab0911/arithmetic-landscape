$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

Write-Output "--- what actually differs (content, ignoring line endings) ---"
& git diff --stat --ignore-all-space
Write-Output "--- untracked ---"
& git ls-files --others --exclude-standard

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add tools/check.py tools/ledger_pending.md
$m = Join-Path $env:TEMP 'r145b.txt'
$body = @"
C20 housekeeping, and the rule bites its author the same day

Fixes the SyntaxWarning C20 introduced (a docstring containing \S needed to be raw),
and records two ledger entries.

The second one is the one worth reading. Door 2 of the future map was opened the same
afternoon: root G_q(A) = 1 + 2 sum_d q^{N_A(d)}, whose value at q = 1/2 is Gamma, and
watch the zeros. They pinch the real axis at q = 1, not at q = 1/2, with

    k * (distance to [0,1]) -> 6.2880 ... -> 2 pi     for the odds
                            -> 6.5652              for the primes

For the odds that 2 pi is provable in three lines -- 1 + 2 sum q^d = 0 rearranges to
q^{k+1} = (1+q)/2, and on the unit circle the nearest root sits at angle 2 pi/(k+1/2).
The primes give a different constant, and the reason is structural: writing
G_q = 1 + 2 sum_n g_n q^n, the coefficients g_n are EXACTLY the half-gaps of A. So this
is the gap generating function and its zero geometry is a statistic of the gap
sequence -- equal gaps give 2 pi, log-growing gaps give something else.

It also settles the Lee-Yang question in the direction that helps: the fair coin is not
a critical point. Gamma^(q) is analytic and non-vanishing in a neighbourhood of q = 1/2
with room about 1/2 at every k tested, so the smoothness Part III observes looks
provable rather than lucky.

None of that is in a paper, and that is the point. By C20 -- installed this morning --
a measured 2 pi and an unidentified 6.5652 are exactly the shape the rule bans, so they
went into a working note. A rule that has not yet cost you anything has not yet been
tested.

C1-C20 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
