$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add tools/ledger_pending.md tools/ledger_archive.md
$m = Join-Path $env:TEMP 'r155.txt'
$body = @"
Consolidation: 26 blocks folded into the skill as F66-F76, case text to the archive

The skill's own rule says a consolidation pass every ten rounds. We were twenty-four past
it, and ledger_pending had grown to 26 blocks -- larger than it has ever been, and all of it
invisible to a cold session, because the skill is what gets auto-loaded and the skill had
not been saved since r130.

Folded into a new section 7.6, "Measurement, search, and reading your own result":

  F66  a hypothesis names a structure; the constant belongs to THAT structure. And a wrong
       answer that is a clean function of the right one names its own bug.
  F67  placing a result where it would actually be used is a check no suite can run.
  F68  a search restricted by a symmetry the object lacks succeeds on a subset.
  F69  a bilingual check needs a benign list per language and must unwrap line breaks.
  F70  measured-but-unproved blocks the push; three outs, the third is the open register.
  F71  remove a region by span, not by content -- a replace that misses does not raise.
  F72  one sample point can be noisier than the trend; check the support before the theory.
  F73  a result can be correctly proved, correctly stated, and pointed the wrong way.
  F74  a quantity computed to argue hopelessness can be the thing that measures it; and a
       correction term is a map of its own failure.
  F75  two data points make a pattern and three test it.
  F76  find the coarsest index on which the summand is constant, and loop on that.

Plus sharpenings folded into existing entries rather than added beside them: F27 gets the
contaminated-exponent case, F30 the degenerate-case corollary, F47 the Schur-concavity
resolution of the CV argument, F57 the observation that a checker's false positives land on
the text that says the most about its own limits, F58 the truncated-fetch diagnosis, F59
that a count must name which artefact it counts, F60 a sixth instance -- C19 catching its
own author ten rounds after it was written.

Two positive habits promoted to rules rather than entries: the cheapest falsification is a
sign at a stated place with no constant to fit; and three controls, the third being the one
that stops the result being over-read.

Also into the skill proper: C20 in the check list; the annealed-exactness statement of the
main theorem in section 1, so the next session inherits the right sentence; the standing
posture on novelty after three classical transports in a row; two scheduled questions in the
round loop that nothing else raises; and the LaTeX and git practice notes bought this week
(build in scratch and copy back, anchor patches on grepped strings, commit named paths
against line-ending churn).

The case text for all 26 blocks moved to ledger_archive.md, which is now 98 KB and is where
a rule gets traced back to the incident that bought it. ledger_pending is reset with the
fold recorded at the top; C6 reports the empty state as an empty state rather than as
silence.

C1-C20 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
