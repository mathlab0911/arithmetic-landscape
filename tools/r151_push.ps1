$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r151.txt'
$body = @"
cor:crossing -- the ratio crosses Gamma at exactly one standard deviation

The correction of the previous commit was stated at the centre. The theorem is about every
target, so redo the layer expansion at n with z = (n - mu)/sigma. The two offsets stop
being symmetric and combine into a cosh, and to first order

    lm/r = Gamma * (1 - (1 - z^2) Q(0)/sigma^2) + o(sigma^-2).

The correction carries a factor 1 - z^2. So the ratio sits BELOW the annealed value inside
one standard deviation of the centre and ABOVE it outside, crossing exactly at
|n - mu| = sigma.

Measured, odd numbers at k = 90: deviation +8.2e-5 at z = 0, +1.7e-5 at z = 0.9, +2.3e-6 at
z = 1, -1.5e-5 at z = 1.1. Three profile families, eight values of z, ratio of measured to
predicted deviation in [0.87, 1.10] away from the crossing where the prediction is zero and
the ratio is meaningless.

This is the first prediction this programme has made that it did not already believe.
Every previous check verified something we expected; the factor 1 - z^2 came out of the
algebra, nobody had looked at the off-centre ratio, and the sign change sits at a place the
theory names in advance. Nothing in the annealed picture suggests a crossing, and the main
theorem cannot see it -- the limit is Gamma at every target, so the whole phenomenon lives
inside the error term.

It is also the cheapest falsification the expansion admits: a SIGN, at a STATED PLACE, with
no constant to fit. A reader who wants to knock down prop:correction should aim at z = 1
and can do it in an afternoon without trusting any constant of ours. rem:crossing says so
in those words.

Worth recording about r147 through r151 as a sequence. The reframing came first -- the
theorem is an annealed-exactness theorem. That made a question audible: is (H) about the
phenomenon or the proof? Answering it produced a quantity, Q(0), which turned out to be
already printed in the paper for the opposite purpose. Generalising that produced a new
falsifiable prediction. NONE OF IT NEEDED A NEW TECHNIQUE. The local limit theorem has been
there since Part II. What changed each time was which question got asked, and every one of
those questions came from outside the derivation.

41 pp both editions. C1-C20 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
