$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'
Remove-Item -Force 'tools\_grep_dh.ps1' -ErrorAction SilentlyContinue

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r133b.txt'
$body = @"
Ledger: a negative control that fired 240x in the wrong direction

Checking the Edgeworth form the R1 attack design rests on, against exact dynamic
programming. The harness assigned the second-order coefficient twice and the
second assignment negated it, so the column labelled "true sign" carried the
corruption and the column labelled "flipped" carried the truth -- and the control
reported the fit improving 240x under corruption. That is how the bug was found.

A negative control that fires the wrong way is not a failed control. It is a
control reporting that the labels are crossed, and it is the only instrument that
can report that, because every other output looks the same either way.

Two operational rules: write the sign out once, in one assignment (the bug
survived reading because the second line looked like a refinement of the first);
and state the direction the control must move before running it -- "the fit must
get worse" is checkable, "the control fires" is not. Corrected harness: 12 of 12
fire, at 21x to 455x.

Without it the attack design would have shipped with an inverted sign and its
out-of-sample prediction fitted to the wrong quantity -- the failure mode where a
control matters most, because the surrounding numbers all look reasonable.

The design itself is gitignored working material (lean/pnp/spec_r1_r133.md,
scripts in study-private-lab). No paper text changed.

C1-C19 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
& git status --short
