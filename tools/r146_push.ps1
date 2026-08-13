$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r146.txt'
$body = @"
cor:classnumber -- the coset energy of a quadratic character is a class number

Door 1b of the future map, walked the same day it was drawn. Compose
prop:chardecomp with Dirichlet and the square roots cancel:

    sum_{a=1}^{p-1} (a/p) log|cos(pi a / p)|  =  0                  p = 1 mod 8
                                              =  4 h(p) log eps_p   p = 5 mod 8

Left side: a sum of logarithms of cosines at rational points -- the same energy X that
lem:coset governs and that section 8 sums over a set of integers. Right side: the class
number of a real quadratic field times its regulator. Nothing on the left knows it is
supposed to be four times an integer times a regulator, which is why the integrality is
reported as a check and not merely as a consequence.

Verified for all eighteen primes p = 5 mod 8 below 320. The ratio is a positive integer
in every case and equals the known class number in every case, h(229) = 3 included. The
fundamental unit is computed independently by solving x^2 - p y^2 = +-4, so no
L-function appears anywhere in that half of the check.

Attribution, and it matters more than the identity. X is an element of the universal
ordinary distribution; Kubert and Sinnott computed its {+-1}-cohomology and Sinnott's
index formula relates the cyclotomic units to the class number. AN IDENTITY CARRYING A
CLASS NUMBER OUT OF THAT THEORY IS THE EXPECTED KIND OF OUTPUT, NOT A SURPRISING ONE. I
could not consult those papers directly, so the paper says it does not know whether the
corollary appears there in this form, and says that rather than implying otherwise.
What is recorded is that this programme's energy function, arrived at from a subset-sum
landscape, lands there at all.

Two harness bugs on the way, both in the fundamental-unit routine, and both legible in
the answer. First every ratio was 1/6 or 1/2 -- 1.618^6 = 17.944 identified it in one
line, the routine was returning a POWER of the unit and the denominators were the
exponents. Then seventeen primes were right and p = 5 gave 1/2, because the Pell search
tried +4 before -4 and at p = 5 both solve at y = 1. A search for the least element must
enumerate in the order of the thing being minimised; mine took the first sign that
worked, which is not a minimisation. When a wrong answer is a clean function of the
right one, the discrepancy names the bug.

Part III 37 -> 38 pp, Japanese 38 pp. C1-C20 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
