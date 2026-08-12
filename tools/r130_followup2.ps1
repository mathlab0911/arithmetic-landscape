$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r130c.txt'
$body = @"
The README was inside the tree and outside the checks

Read the rendered repository page in a browser after the push, the way a reader
meets it, and the first paragraph defined the ratio as lm_A(n)/deg_A(n).  deg_A
was purged from all four papers at r126 -- it was the first of the three
duplicate-name pairs the declined endorsement was about -- and it survived in
the first thing anyone sees.  The README also still said "papers 2-4" after the
series was renamed.

C9 counts this file's numbers and C14 guards one formula in it, so it has been
read by checks for rounds; neither has ever had an opinion about its
vocabulary.  Being inside the tree is not the same as being inside a check.

C18 now reads the README the same way it reads the homepage, with the r123
mention-versus-claim distinction, because the README has to be able to name
paper 3 in order to retire it.  Two of the five negative controls for that
exemption did not fire on the first attempt: a retirement note anywhere within
400 characters excused anything near it, including "four papers" reinstated
three lines away.  That is C17's region-too-wide failure moved into the
exemption, where it is worse -- a too-wide search only misses, a too-wide
excuse forgives.  The marker must now stand in the same sentence as the name it
retires.  All five controls fire.

Still open, and unreachable from here: the repository DESCRIPTION on GitHub is
the pre-series title of Part I.  It is in GitHub's settings, not in a file, so
no check in any tree can see it and no commit can fix it.

Log: lean/pnp/pushverify_r130.log.  C1-C18 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
& git status --short
