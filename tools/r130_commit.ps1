$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

Remove-Item -Force 'lean\pnp\_r130.err' -ErrorAction SilentlyContinue

& git add -A
Write-Output '=== staged ==='
& git status --short

$msg = @"
Retire paper 3 into Part III, and take the summary population with it

Paper 3 has been carried in full by Part III since the assembly (all 33
statements, MOVE 22 / CALIB 8 / OPEN 2 / SPLIT 1 / DROP 0), but the file was
still in the tree at 14 pp under its old title.  Pushing it would have published
the same content twice.

A file-level DROP_GUARD (lean/pnp/retire_r130.py) ran first, in two parts,
because the r123 lesson is that removal does not announce itself the way
addition does: a reader-facing scan over both trees and both READMEs, and a
functional run of every tool afterwards to see whether it survives the absence.
It refused twice.  What it caught was real -- Part III still cited paper 3 as a
sibling, which is a paper citing itself -- and the second refusal came from the
guard conflating a mention with a dependency, so the guard was rebuilt to
separate them.

Scopes updated in this same commit rather than after it (F60, applied in
advance): C9's series rows, C13's translation pairs, C15's sibling set, C17's
superseded-paper exclusion, which is now empty.

The homepage was the other half of the same population, and it was worse than
the README ever was: the enumeration definition of Gamma, "order-sensitive
invariant", four papers, no disclosure -- and 5.34920, the literal C11 has
banned since r118 and has been checking over paper/ and paper-ja/ only.  It is
rewritten, and C18 now reads it from this repository, with three negative
controls.  Third instance of the same shape and the first check that leaves the
tree to catch it.

Also: Part III's title still carried "(subtitle provisional until the Part-III
assembly is complete)", written before the assembly it describes -- F63 in the
week F63 was written -- and its author footnote had lost the address the other
two carry.

C1-C18 pass; canon replay PASS, 17 modules, three poisoned modules rejected.
"@

$tmp = Join-Path $env:TEMP 'r130_msg.txt'
Set-Content -Path $tmp -Value $msg -Encoding UTF8
& git commit -q -F $tmp
Remove-Item -Force $tmp
Write-Output ''
Write-Output '=== HEAD ==='
& git log --oneline -1
