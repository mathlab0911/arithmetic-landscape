$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

Write-Output '=== homepage commit ==='
Set-Location 'C:\Users\amake\Claude\Projects\homepage'
& git add -A
$h = Join-Path $env:TEMP 'hp2.txt'
$hb = @"
Attribute the identity: it is the Kubert distribution relation

The page described the coset identity as an exact identity of ours without saying
that it is the classical Kubert distribution relation for log|2 sin pi t|, shifted.
Corrected in both places it appears. What is new is the use, and the page now says
that instead.
"@
[System.IO.File]::WriteAllText($h, $hb, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $h
Remove-Item -Force $h
& git push origin main 2>&1
Write-Output ("homepage push exit=" + $LASTEXITCODE)

Set-Location 'C:\Users\amake\Claude\Projects\study'
& git add -A
$m = Join-Path $env:TEMP 'r139.txt'
$body = @"
Part III: attribute the distribution relation, and replace two computations with one reason

FIRST, A CORRECTION, and it is the pre-approved kind. The coset identity is the
classical Kubert distribution relation for log|2 sin pi t|, transported to the
cosine by t -> t + 1/2. Our first proof IS the multiplication formula, which is how
the classical relation is proved -- the mathematics was never in doubt. What was
wrong is that we advertised it as reaching outside the programme without saying
that it reaches outside because it IS outside. A number theorist recognises it in
one line and would have distrusted the section for not naming it.

Now named: in the abstract, at the lemma (with a status saying we claim no part of
it), in the terminology table, in the README and on the homepage, with Kubert-Lang
cited. What is ours is the corollary -- X >= 0, so the rational points are the
MINIMA of the coset average -- and the use made of it, and the text now says that
instead.

SECOND, A PROPOSITION, two lines, and it makes two of our theorems into one fact.

  (Z/q)^* is an additive coset of a subgroup of Z/q if and only if q is a power
  of 2.  Both 1 and -1 are units, so the coset modulus divides 2; modulus 2 forces
  every odd residue to be a unit.

The distribution relation averages over an ADDITIVE coset. An odd sequence's
residues are always one; a prime set's are the reduced residues, which are one only
at powers of two. Hence the floor pins the primes at q = 2^k -- maximal at q = 4,
giving 1/sqrt(2) -- and does not apply at q = 2m with m odd, where the odd residues
contain the zero of the cosine and the reduced residues do not. That is the
modulus-6 peak. So Theorem modfour and Part II's modulus-6 theorem are not two
coincidences but one property of q, and 6 is the smallest q where the two classes
part company.

Measured, and the measurement is how the proposition was found: testing the floor
as a stand-alone tool, it failed at exactly one cell of a six-by-two table -- the
primes at q = 6 -- and the failure was the phenomenon, not an error. At q = 4 and
q = 8 the odd primes below 4e4 sit ON the floor to five decimals.

Part III 31 -> 32 pp; the Japanese edition follows (C19 named the gap before I had
thought about it). tool_coset_r138 moved into the tree with its log, since a paper
now cites it.

C1-C19 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m
& git push origin main 2>&1
Write-Output ("study push exit=" + $LASTEXITCODE)
& git log --oneline -1
& git status --short
