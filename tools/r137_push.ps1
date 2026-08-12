$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r137.txt'
$body = @"
Ledger: we did not name the family our own lemma belongs to

Part III's coset identity is the Kubert distribution relation for log|2 sin pi t|,
shifted by a half. Derived, and verified numerically to 1e-37 over v <= 40. The
distribution relation is the defining relation of the Kubert-Lang theory,
underlying cyclotomic units and the Kronecker limit formula; a number theorist
recognises it in one line.

Nothing is wrong with the mathematics -- our first proof IS the multiplication
formula, which is how the classical relation is proved. What is wrong is that we
advertised it as "the one result that reaches outside this programme" without
saying that it reaches outside because it IS outside.

F15 says: search whether the quantity you invented already has a name. We named
the object and not its family. A result can be correctly attributed at the level
of the proof and unattributed at the level of the literature, and only the second
is what a reader checks. The cost is not a lost claim -- the use is still ours,
and the corollary that the rational points are the minima, standing in for
Erdos-Turan, is the thing worth advertising. The cost is credibility with exactly
the audience that would recognise it.

Operational rule: when a lemma is proved by a classical mechanism -- a
multiplication formula, a reflection formula, a functional equation -- search for
the RELATION's name, not only for the statement's. The proof technique is the
pointer to the family.

Also this round, in gitignored working material: the Hermite bookkeeping derived
and checked (the inversion identity 12/12 to 1e-14; the assembled expansion
against exact DP at seven values of z, residual O(k^-3/2); dropping the He3 term
makes the fit 13x to 923x worse, 8/8 controls firing). R1 is bookkeeping-complete.
And an assessment of what the programme is for, with three leads and what would
kill each.

No paper text changed.

C1-C19 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
& git status --short
