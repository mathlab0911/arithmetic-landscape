$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r143.txt'
$body = @"
The reduced residues, evaluated: prop:redresidue, and what a surrogate costs

Lead (c) asked whether the floor lemma improves a published minor-arc bound or
only reproduces it. Chasing why it was LOOSE for the primes at small odd v -- they
avoid 0 mod v, so they are not balanced over the coset -- turned up the sharper
statement, and it is an exact evaluation rather than a bound.

Write v = 2^j w with w odd, v not 2 mod 4. Then

   (1/phi(v)) sum_{r in (Z/v)*} X(r/v) = log2 * (1 - 2[w=1]/(2^j phi(w)))

which is (1 - 2^{1-j}) log 2 when v is a power of two and EXACTLY log 2 otherwise,
including every odd v > 1. Proof is Mobius inversion over lem:coset: the full-group
identity at t=0 for odd n, the odd-residue coset for 4 | n, and the two run against
each other. For v = 2 mod 4 the inversion is infinity - infinity, and that is not a
technicality -- it is exactly where the product vanishes.

Two things fall out.

thm:modfour is the case w = 1. The deficiency per element is the full circle mean
log 2 at every v except the powers of two; at v = 4 it is (1/2)log 2, i.e. the
product only falls to 2^{-k/2} = (1/sqrt2)^k. That is the modulus-4 theorem, and the
proposition adds that the obstruction happens at the powers of two AND NOWHERE ELSE
-- which is prop:twopower, reached from an exact evaluation instead of from the
group-theoretic characterisation. Two independent routes to one classification.

And the answer to lead (c), in rem:surrogate. Any argument that replaces X by a
surrogate a discrepancy estimate can handle caps at that surrogate's own mean:

   X itself            log 2      0.69315     --
   (1/2) sin^2(pi t)   1/4        0.25000     loses 2.773x
   (pi^2/2)||t||^2     pi^2/24    0.41123     loses 1.686x

Both surrogate inequalities are true (proved: -log c >= 1-c, and -log cos u has only
positive Taylor coefficients). They are true and lossy. Hand the surrogate routes
their exponential sum and their discrepancy EXACTLY -- no Weyl, no Koksma, no error
term -- and they still stop at a quarter. The loss is in the surrogate, not in the
equidistribution input: X has a logarithmic singularity at the half-integers, a
bounded convex surrogate does not, and that singularity is where the mass of the
average sits. The bound enters an exponent, so 2.77 in the constant is 2.77 in the
exponent.

The round also produced a misapplication worth the ledger. The first run applied the
floor with the average over the FULL group Z/v; for A odd and v even the orbit is a
coset of the index-2 subgroup, so the floor is (1-2/v)log2, not (1-1/v)log2. The
control caught it on six rows, and the number it wrongly claimed at v=8 is the
correct floor at v=16 -- one step down the 2-adic ladder, the signature of using a
group twice too big. When the tool says "coset of a subgroup", the floor belongs to
THAT subgroup and the ambient modulus is a decoy.

STATUS: proved, awaiting independent verification, same as Appendix A. Checked
against direct enumeration on 26 moduli to 1e-12, with two controls that fire 11/11.

Part III 34 -> 36 pp, Japanese edition 36 pp. C1-C19 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
& git status --short
