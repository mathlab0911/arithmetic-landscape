$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r147.txt'
$body = @"
Gamma IS the annealed prediction -- so the theorem is an annealed-exactness theorem

Kentaro asked whether there is anything here the mathematical community can actually
use. Two findings, and the first one changes what this programme is for.

1. THE READING WE HAD WAS BACKWARDS, AND THE TRUE ONE IS BETTER.

The classification of local minima says S is a strict local minimum for target n iff,
with D = sigma(S) - n, every a in S has a > 2D and every a outside S has a > -2D. Fix
the offset at D = d > 0 and that is just S contained in {a > 2d} -- and the number of
elements it forbids is exactly N_A(d). Apply the annealed (independence) heuristic:
pretend the subsets of a subfamily B hitting a prescribed target number about 2^|B|.
Layer d then contributes 2^{-N_A(d)}, the offsets +-d pair, d = 0 contributes 1, and the
sum is 1 + 2 sum_d 2^{-N_A(d)} = Gamma(A). On the nose.

So Gamma is not merely computed by an argument that AVOIDS the annealed approximation.
Gamma IS the annealed prediction, and the main theorem says

    the annealed count of metastable states is asymptotically exact for this model,

under a hypothesis (H) that is checked rather than assumed, with a profile in Part III
that violates it. That is the sentence to offer the statistical mechanics of disordered
systems, where the annealed approximation is in constant use and almost never
controlled: an NP-complete ground-state problem where it is provably right, plus the
condition delimiting it, plus an explicit counterexample to the condition.

The README said the theme was REPLACING the annealed approximation. Methodologically
true, and misleading about the result. Rewritten.

Verified: the local-minimum equivalence by brute force on 1952 (set, target) pairs, and
the two expressions for Gamma on five families.

2. THE FACTOR 1 - chi(2) IS THE DOUBLE-ANGLE FORMULA, AND THAT SETTLES THE ATTRIBUTION.

2 sin 2pi t = 2 * 2 sin pi t cos pi t, so log|2 cos pi t| = (T_2 - 1) log|2 sin pi t|
with T_2 f(t) = f(2t). On the chi-component T_2 acts by chi(2), since a -> 2a permutes
the units. So the factor 1 - chi(2) in prop:chardecomp IS the eigenvalue of 1 - T_2 and
nothing else, and the proposition is Dirichlet's classical evaluation of
sum chi(a) log|2 sin(pi a/f)| transported by the double-angle formula -- exactly as
lem:coset is the classical distribution relation transported the same way.

This is the third time the same lesson has arrived and I would rather write it down than
be told it: the coset identity was Kubert's, the class number corollary sits inside
Kubert-Sinnott, and now the character decomposition is Dirichlet's composed with a
trigonometric identity. rem:doubleangle says so at the proposition, and the proof stays
in because a reader should be able to see the transport rather than take it on trust.

What remains ours is unchanged and is now easier to state: the invariant, the theorem
that the metastable-to-ground-state ratio converges to it for every target, and the use
of an exact distribution relation where a minor-arc argument would spend an
equidistribution estimate.

Part III 38 -> 39 pp, Japanese 39 pp. C1-C20 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
