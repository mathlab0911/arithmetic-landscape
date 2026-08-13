$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r154.txt'
$body = @"
A witness that some hypothesis is necessary: the annealed prediction fails on 2^i + 1

prob:hrate asked whether (H) is about the phenomenon or about our proof. r150 settled the
clean power profiles affirmatively BY THE CORRECTION FORMULA. The same formula says where
to look for failure -- Q(0)/sigma^2 must be forced up, and that needs a family growing
faster than any power. So I looked there.

Take a_i = 2^i + 1: odd, distinct, and not super-increasing beyond i = 3, so the subset
sums genuinely overlap and r > 1 at many targets. Gamma = k + 2 grows linearly. lm/r does
not follow it:

    k          8      10      12      14      16      18
    Gamma     10      12      14      16      18      20
    lm/r    7.18    7.45    7.73    7.33    6.92    7.08
    ratio  0.718   0.621   0.552   0.458   0.385   0.354

lm/r stays near 7 while Gamma grows. a_i = 2^i - 1 does the same: 0.713, 0.583, 0.473,
0.379 at k = 8, 11, 14, 17.

Controls, because a spectacular result is where this project has been wrong before. The
dynamic programme agrees with BRUTE-FORCE ENUMERATION of all 2^k subsets at k = 8, 10, 12
with zero disagreements. The window occupancy is printed as a column, so the r150 support
trap is excluded. And Q(0)/sigma^2 is about 0.07 here while the shortfall is 65%, so the
first-order correction does not explain it either -- these families are outside the regime
prop:correction describes, which is exactly what makes them interesting.

So: SOME HYPOTHESIS IS NECESSARY. (H) is a sufficient but not a necessary form of it, and
the open problem is now to find the sharp condition rather than to decide whether one is
needed. Stated as a CONJECTURE, not a result, because k <= 18 is a range and not a limit --
the third of the three outs C20 allows, and the first time this project has used that out
for something it actually believes.

Method note, and it is the second time in three rounds. The naive implementation loops over
every offset d up to (max A - 1)/2, which for these families is exponential in k and does
not finish. But N_d is constant on blocks, so within a block the layer contributes a SLIDING
SUM of tail counts -- one prefix sum per block, O(T) instead of O(T) per d. Two timeouts
bought that observation; the same lesson as r152 in a different disguise: a quantity indexed
by something that only changes k times should be computed k times.

Part III 42 -> 43 pp, Japanese 43 pp. C1-C20 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
