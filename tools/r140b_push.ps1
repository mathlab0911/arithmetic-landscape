$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r140b.txt'
$body = @"
Ledger: the index had become a second copy of the thing it indexes

MEMORY.md is the index loaded at the start of every session: one line per memory
file, pointing at where the detail lives. It had reached 41 KB, of which a single
line was 19 KB -- the pointer to the research log had accumulated a full summary of
every round for forty rounds, and was approaching the size at which the file would
stop being readable at all.

Every word of it was already in the log. Verified before deleting, by sampling the
rounds the line cited and the lessons it quoted and confirming each appears in the
log, the failure ledger, or the skill. Compacted to 2.4 KB.

An index that grows becomes a copy, and a copy of the thing it indexes is worse
than no index: it is the artefact most likely to be read and least likely to be
maintained. The shape is F35's -- a summary drifting from what it summarises -- but
in the other direction: not over-claiming, over-INCLUDING, until the summary is the
document.

The rule is a size check rather than a judgement: the index gets one line per
entry, and a line that no longer fits on a screen belongs in the file it points at.
Where the current position genuinely needs to be in the index -- it does, because a
cold session reads the index first -- it gets one sentence naming the state, not a
history of how the state was reached.

Caught by tooling rather than by me: a write hook warned at 19.8 KB against a
24.4 KB read limit. Without it the next cold session would have found an index it
could not read.

C1-C19 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
& git status --short
