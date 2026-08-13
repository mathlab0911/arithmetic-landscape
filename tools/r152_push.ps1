$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r152.txt'
$body = @"
The crossing on the primes, Q(0) = 61/3 exactly, and which case the annealed answer likes

Kentaro asked for the z-dependence applied to the primes, which is the right place to ask:
Part II proves the theorem there at the centre with no hypothesis attached, so it is the
one family where a prediction is not resting on anything conditional.

The crossing appears exactly as predicted. At k = 90 the relative deviation runs
+3.24e-5 at z = 0, +7.0e-6 at z = 0.9, +9.8e-7 at z = 1, and -5.8e-6 at z = 1.1. Ratio of
measured to predicted deviation in [0.94, 1.00] away from the crossing, window fully
occupied at every point. For scale, Gamma computed from the first 65 odd primes already
agrees with Gamma(P) to 3e-15.

Two constants. The first is EXACT rather than measured: for the odd numbers N_d = d,
L_d = d^2, s_d = d(4d^2-1)/3, delta_d = d + d^2/2, and the series sums in closed form,

    sum_{d>=1} 2^-d (delta_d^2 - s_d/4) = 61      so   Q(0) = 61/3,

which with sigma^2 = k(4k^2-1)/12 makes the relative error at the centre asymptotically
61/k^3. For the odd primes Q(0) = 50.4369...

And then the comparison, which points the other way from the difficulty of the proofs.
Q(0) is only 2.5 times larger for the primes, while sigma^2 is far larger at the same k
because p_k ~ k log k against 2k. So THE ANNEALED PREDICTION IS MORE ACCURATE FOR THE
PRIMES THAN FOR THE ODD NUMBERS, by a factor growing like (log k)^2/4 -- measured, the
ratio of the two relative errors is 1.80 at k = 40 and 4.74 at k = 520.

The primes are the harder case to prove and the easier case to approximate, and both
follow from one fact: their elements are bigger. Big elements are what make the exponential
sums hard and what make the variance large. Difficulty of proof and quality of
approximation are pulled apart by the same cause.

Method note, in the ledger. The first run timed out because the tails A_{>2d} were rebuilt
from scratch at every threshold -- O(k) full dynamic programs. Building each distinct tail
once turned three minutes of nothing into thirty seconds of answer. A quantity indexed by a
shrinking set should be computed by shrinking the set, not by rebuilding it; obvious
afterwards, and the timeout was the only thing that made me look.

42 pp both editions. C1-C20 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
