$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r143b.txt'
$body = @"
Correction: prop:redresidue is an evaluation at the rational, not a bound near it

Found ten minutes after the previous push, by doing the literature pass I had
listed as a task and had not yet done.

The pass itself came out clean: rem:surrogate claims the standard minor-arc route
for these generating functions goes through a Weyl-sum bound, and the
partitions-into-prime-powers argument does exactly that -- it quotes an exponential
sum estimate for sum_p e(j p^k alpha) and saves a power of log X. The claim stands.

What did not stand was a sentence of mine two lines later. Putting the proposition
next to the shape of argument that would consume it exposed the gap: a minor arc is a
NEIGHBOURHOOD of a rational, and prop:redresidue evaluates AT the rational.
cor:floor makes a single coset's floor uniform in the shift; the reduced residues are
a Mobius-SIGNED combination of cosets, and a signed combination of lower bounds is
not a lower bound.

Measured, it is a trichotomy, and rem:shift now states all three:

  v = 2^j              uniform, and PROVED -- one coset, so cor:floor applies
  4 | v, odd part > 1  t=0 was minimal in every case tested; NO PROOF
  v odd                FALSE.  At v = 3 the average falls from log2 to (1/2)log2
                       at t = 1/3, since the shift carries a reduced residue onto
                       0, where X vanishes.

So the modulus-4 reading is exact at theta = h/v and, at odd v, is not by itself an
estimate on the arc around it. Only the powers of two turn the evaluation into a
bound -- which is the same 2-adic boundary as prop:twopower, for the third time.

Nothing in prop:redresidue changes; it was correct and remains correct. The prose
around it over-read it, and the check suite has no test for "is this evaluation also
a bound" and could not have: the defect was in the reading, not in the theorem.

Section 6 added to leadc_r143 with the shift scan and the counterexample.
36 pp both editions. C1-C19 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -2
& git status --short
