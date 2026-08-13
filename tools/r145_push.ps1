$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r145.txt'
$body = @"
prop:chardecomp: the coset energy decomposes into L-values, and C20 stops the gap

Two things, and the second one is why the first was possible.

C20, Kentaro's ruling after r144. A claim of the form "measured but unproved" now
blocks the push. Twice in one round a defect lived in exactly that gap -- prose that
read as established, resting on a scan -- and neither was reachable by any other
check, because the theorem was correct and the reading was not. The gap is nameable
in advance, so it is now named. To pass, prove it, disprove it, or move it to the open
register: a problem environment, or a status that calls it a conjecture or an open
question. Naming it open is not a loophole, it is the third honest outcome, and it
puts the claim where a reader looks for what is missing. Five negative controls, all
five fire, including the exact r143 defect and its Japanese form. One benign class had
to be carved out and the adverb carries the whole distinction: "not proved HERE" means
proved elsewhere, in the literature, which is the opposite of "not proved".

Then the mathematics. prop:redresidue evaluated the mean over (Z/v)*. That is one
Fourier coefficient. The rest of them:

   sum_{a in (Z/f)*} conj(chi)(a) X(a/f)
      = phi(f) * (prop:redresidue)          chi trivial
      = 0                                   chi odd
      = -tau(conj chi) (1 - chi(2)) L(1,chi)   chi even, nontrivial

Three classical ingredients and a finite interchange: X is even so odd characters die
by pairing a with f-a; the Fourier series of log|2 cos pi t|; and
sum_a conj(chi)(a) e(na/f) = chi(n) tau(conj chi) for primitive chi. The sum over a is
finite, so nothing needs justifying to take it inside.

So the coset energy has a complete spectral decomposition in which THE TRIVIAL
COMPONENT IS EXACTLY log 2 WITH NO ERROR TERM and every other component is a Dirichlet
L-value at s = 1 times a Gauss sum. For a set A the main term of the deficiency is
exact and all of the error is carried by characters. When A is a set of primes those
twisted counts are what Siegel-Walfisz controls -- so Part II's single ineffective
constant enters there and nowhere else. That locates the ineffectivity rather than
removing it, and it opens the route: under GRH the twisted counts are explicit.

One corollary is clean enough to stand alone. For every prime p = 1 mod 8,

   sum_{a=1}^{p-1} (a/p) log|cos(pi a / p)| = 0,   exactly,

because the factor 1 - chi(2) vanishes for the Legendre symbol precisely when
(2/p) = 1. Verified to 1e-40 for every p < 200 with p = 1 mod 4; the p = 5 mod 8 half
is the control and is nonzero in all eleven cases. The parity control (odd characters
give zero) fires 8/8.

And the factor 1 - chi(2) is the fourth face of the same fact. prop:twopower says
which residues form a coset; thm:modfour gives the rate 1/sqrt2; rem:shift says when
the evaluation is a bound; and now the character group says which characters can see
the energy at all. Every one of them turns on the prime 2. The obstruction of this
theory is 2-adic and it has now been met from four independent directions.

Part III 36 -> 37 pp, Japanese 38 pp. C1-C20 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
& git status --short
