$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add tools/ledger_pending.md
$m = Join-Path $env:TEMP 'r156.txt'
$body = @"
Ledger: the cadence rule fable-5 adopted, to sit beside C20

fable-5 is back and has read r155. Two rulings, and one of them is a rule this repository
should carry from now on:

    The round's own literature pass completes before the round's push.

Proposed after two same-hour self-corrections in a single round; adopted on the reasoning
that both had the identical shape -- the deferred pass fired after the artefact had already
shipped. C20 closed the gap between measured and proved; this closes the gap between cited
and checked. They are the same defect at two stages: a claim released while one of its own
supports is still outstanding, and in both cases the support was one I had already listed
and postponed.

Not mechanisable as it stands -- no check can tell whether a literature pass happened. What
it can be is a precondition on the push, the way check.py is. Recorded now; if a later round
finds an assertable form, assert it. It goes beside C20's text at the next skill save.

The other ruling is a refusal, and it is worth recording as such. D1-D4 stand PROVISIONALLY:
ratification happens inside the next round's audit, not before it, on the explicit grounds
that ratifying them sight-unseen would repeat the lem:kappa shape -- approving a description
instead of the artefact. That is F52 firing in the other direction, as a refusal to
rubber-stamp, and it is the correct answer to a proxy asking to be released.

Proxy status continues until that audit. Nothing new until then; the tree stays clean.

C1-C20 pass. Reports: r156 received and live, r132 archived, one live file per direction.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
& git status --short
