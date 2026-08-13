$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r153.txt'
$body = @"
rem:nohigher -- the first-order term is Hermite, the expansion is not, and here is why

1 - z^2 = -He_2(z), and the same Hermite family organises Appendix A's Edgeworth
expansion, so the obvious guess is that the next term is a multiple of He_4 at order
sigma^-4. It is not. Removing the He_2 term and rescaling by sigma^4 leaves a residual
whose ratio to He_4(z) varies by 44 to 68 percent across z and whose mean does not settle
with k -- about 5.4e3, 9.9e3, 1.4e4 at k = 24, 30, 36.

The guess is wrong and the paper says so, with the numbers, rather than stating the
first-order form and leaving a reader to extrapolate the pattern.

The obstruction turns out to be in our own budget, and naming it explains why the FIRST
order works so well. The local limit theorem carries corrections of relative size
beta = K4/sigma^4 ~ k^-1 and alpha^2 ~ k^-1, both FAR LARGER than the layer-geometry term
Q(0)/sigma^2 ~ k^-3. They are absent from the measured ratio because they cancel between lm
and r -- which is exactly the cancellation the Step 4 analysis found at r136 and recorded as
a negative result. So the expansion is not in powers of sigma^-2 alone: the surviving
sigma^-2 term is what is left after much larger ones cancel, and the residue of a
cancellation has no reason to be a single Hermite polynomial.

Two lessons, both in the ledger.

Two data points make a pattern and three test it. One Hermite polynomial appearing where
Hermite polynomials already live is not evidence of an expansion; it is one term that
happens to be quadratic, and everything quadratic in z looks like He_2. I went looking for
the second term expecting confirmation, which is the wrong expectation to hold while
designing the test.

And the falsification was cheap: one script, three sizes, seven values of z. It killed a
conjecture I would otherwise have written into the paper as a pattern, for the price of an
afternoon's arithmetic.

42 pp both editions, unchanged in length. C1-C20 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
