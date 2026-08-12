$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r141.txt'
$body = @"
Region R1 written out: Appendix A, every constant proved

The one open problem the three conditional theorems of Part III shared is now a
written argument. Appendix A, four subsections, and the thing that had to change
first was the constant: the design of r133 carried the two-point Taylor remainder
with a MEASURED constant, and a measured constant is not a proof, so R1 would have
stayed open however much of the rest was assembled.

It is provable. K(t) = log(q + p e^t) is the cumulant generating function; its
nearest singularity needs Im t = pi mod 2pi, so K is analytic in |t| < pi for every
p. On |t| = 2, minimising the quadratic in u = p e^x gives |q + p e^t| >= q |sin 2|,
hence |K| <= 2 + pi, and Cauchy's estimate on that circle gives

   |log(1-p+p e^{iv}) - P_4(v)| <= 2(2+pi)/32 |v|^5 = 0.32136 |v|^5

for p <= 1/2 -- which is our case exactly, since s > 0 forces every p_a < 1/2. The
proved constant is 282 times the measured maximum. That costs nothing: only the
exponent enters the scaling, and the constant enters once, linearly.

The rest assembles r133-r137 with the estimate made under the integral rather than
uniformly -- the sup over R1 is of order 100 and does not decrease with k, while the
density-weighted remainder is 9e-5 at k=450 and falls like k^-3/2. The region cut at
sigma/N is what makes every phase at most 1, and beyond it no Taylor bound is needed;
that introduces a threshold k_0 which (H) supplies for every admissible profile, of
order a few thousand for the odd numbers and the primes. Printed rather than hidden.
Hermite inversion derived, three coefficients, and the budget eps*(Z) with the
suprema written out.

STATUS, and this is the point: proved, AWAITING INDEPENDENT VERIFICATION. The
standing rule of this project is that an argument written by one hand becomes
"proved on paper" only after a second, independent reading. So Theorems rigid and
transfer keep their conditional statements; what changed is the KIND of thing that
is missing -- a written argument to be checked, not a computation to be done. I am
not flipping the status of three theorems unilaterally, and the appendix says so at
its head.

Part III 32 -> 34 pp, Japanese edition 35 pp, both built clean. Six r1* scripts
moved into the tree with their logs, since the appendix cites them.

C1-C19 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
& git status --short
