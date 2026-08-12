$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

Write-Output '=== check.py (homepage visible) ==='
& python tools\check.py | Select-Object -Last 2
Write-Output ("exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r131b.txt'
$body = @"
The Japanese edition of Part III, and a check that reads the skeleton

paper4_ja: 31 pages, the whole of Part III, same page count as its source.  92
labels of 92, 67 status declarations of 67, three TODOs of three, zero undefined
references.  C13 now has its third pair and stops reporting the absence.

Measuring that parity is what the round actually found.  C13 was written for the
Japanese editions and reads them on every run -- but it compares numbers, and
none of what was missing was a number: paper2_ja had lost SIX of its seven status
declarations, including the one on the main theorem, plus two whole remarks;
paper1_ja was missing the label its siblings cross-reference.  All of it was
content the English gained after the translation was made.

C13 was reading the file and not the property.  C19 compares the skeleton --
label set, count of each theorem-like environment, count of \STATUS -- with three
negative controls: delete a label, delete a remark, delete a status.  All three
fire.  A translation that drops the status labels is the overclaim C8 exists to
prevent, made invisible by being in the other language, and the Japanese editions
are the ones Kentaro approves from.

Repaired: the six statuses and two remarks in paper2_ja, the label in paper1_ja,
and a Hangul character sitting inside the word 検査 in the AI-disclosure paragraph
of both -- one bad keystroke, copied when the paragraph was, found by a scan no
check had ever run.

Also: the GitHub repository description was the pre-series title of Part I.  It
is in GitHub's settings, not in any file, so no check here could see it and no
commit could fix it; changed by hand with Kentaro's permission, and recorded in
the ledger as the class of thing this apparatus is structurally blind to.

C1-C19 pass.  paper-ja/README.md rewritten; it had said "残っている作業 なし。
三部作すべて完成" three lines under a row marking Part III as not started.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
& git status --short
