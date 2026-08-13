$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r144.txt'
$body = @"
Correction, second pass: rem:shift was wrong, and now it is proved both ways

I set out to PROVE the case the last commit left open -- 4 | v with odd part > 1,
reported there as "measured uniform, no proof". It is not uniform. It is false, and
the counterexample is not exotic: at v = 12, t = 1/5 the reduced-residue average is
0.4525 against log 2 = 0.6931 at t = 0.

The measurement that produced the wrong claim scanned t over [0, 1/v]. That interval
is the period of the FULL-GROUP average, where t -> t + 1/v permutes {k/v}. It is not
a period of the reduced-residue average: t -> t + 1/v carries r/v to (r+1)/v, and the
units are not closed under +1. The scan was blind to the region containing the
counterexample and returned a number rather than a warning.

  A search restricted by a symmetry the object does not have does not fail.
  It succeeds, on a subset.

Settling it properly needed the product form of lem:coset, and that answers both
directions at once. For 4 | n the odd residues are a coset, so

    O(n,t) = prod_{s<n odd} |2 cos pi(t + s/n)| = 2 |cos(pi (n/2) t)|,

and Mobius over the odd part of v = 2^j w gives

    Q(v,t) = prod_{r in (Z/v)*} |2 cos pi(t + r/v)|
           = 2^[w=1] prod_{d|w} |cos(pi (v/2d) t)|^{mu(d)}.

  w = 1 (v = 2^j):  Q = 2|cos(pi (v/2) t)| <= 2 = Q(v,0).  UNIFORM, PROVED --
                    as it must be, the reduced residues being one coset, so
                    cor:floor already covered it.
  w > 1:            Q is a RATIO, the mu(d) = -1 divisors in the denominator.
                    For w = 3 it is |cos 3u|/|cos u| = |4cos^2 u - 3|, above 1
                    whenever cos^2 u < 1/2.  FAILS.

So the evaluation becomes a bound on the surrounding arc if and only if v is a power
of two -- prop:twopower for the fourth time, and for the same reason each time: that
is exactly when the reduced residues form a coset. The trichotomy I pushed is a
dichotomy, and the middle row is gone.

The failed guess forced an exact computation that a successful measurement would have
left undone. That is the only good thing about it and it is worth recording.

rem:shift now carries its own history: a note at the end says what the earlier version
claimed and which scan produced it. Closed form checked against direct computation at
35 points, shift_r144. rem:modfourcorollary qualified to say "at the rational point
itself". 36 pp EN, 37 pp JA. C1-C19 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -3
& git status --short
