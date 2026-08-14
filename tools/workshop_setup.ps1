# The WORKSHOP repository: a second git directory, living OUTSIDE the working tree, whose
# only remote is the private one, holding the working documents that the research
# repository deliberately ignores.
#
# Why it cannot leak, structurally rather than by convention:
#   - the workshop git-dir sits outside study\, so the research repo can never track it;
#   - the workshop repo has NO origin, so the public remote is not reachable from here;
#   - the research repo's .gitignore is untouched, so the working files stay out of it.
#
# The one thing that surprised us. A .gitignore lives in the WORKING TREE, so BOTH repos
# read it, and .gitignore outranks $GIT_DIR/info/exclude. So a whitelist in info/exclude
# cannot re-admit what .gitignore excludes. The workshop therefore adds its paths with
# --force, explicitly and by name.
#
# That leaves the failure mode pointing the safe way: a careless `git add -A` in the
# workshop repository adds NOTHING, because .gitignore blocks all of it. The dangerous
# direction is closed by the same rule that made the problem.
#
# Run with -Commit to actually commit and push; without it, this is a dry run.
param([switch]$Commit, [string]$Message)

$ErrorActionPreference = 'Continue'
$TREE = 'C:\Users\amake\Claude\Projects\study'
$GD   = 'C:\Users\amake\Claude\Projects\study-workshop.git'
$PRIV = 'https://github.com/mathlab0911/arithmetic-landscapes-private.git'
Set-Location $TREE

# the whitelist, and the only thing this repository is ever allowed to hold
$PATHS = @('reports', 'book', 'paper-ja', 'docs', 'outgoing')
$GLOBS = @('lean/pnp/spec_*.md', 'lean/pnp/paper2_*.md')

if (-not (Test-Path $GD)) {
    Write-Output "=== creating the workshop git directory (outside the tree) ==="
    & git init --bare $GD | Out-Null
    & git --git-dir=$GD config core.bare false
    & git --git-dir=$GD config core.worktree $TREE
    & git --git-dir=$GD config user.name  (& git -C $TREE config user.name)
    & git --git-dir=$GD config user.email (& git -C $TREE config user.email)
    & git --git-dir=$GD remote add private $PRIV
    Write-Output "created"
} else {
    Write-Output "=== workshop git directory already present ==="
}

# git escapes non-ASCII paths as \345\205\245... unless quotepath is off, and the
# whitelist guard then reads its own escaping as a path outside the whitelist. This is the
# second time this week that a checker written in English-shaped assumptions misread
# Japanese; the first was a line-wrapped exemption phrase (F69). Turn it off every run,
# not once at creation, because a setting that is only applied at setup is a setting that
# a fresh clone will not have.
& git --git-dir=$GD config core.quotepath false

Write-Output ""
Write-Output "=== GUARD 1: the workshop must not know the public remote ==="
$remotes = @(& git --git-dir=$GD remote)
Write-Output ("remotes: " + ($remotes -join ', '))
if ($remotes -contains 'origin') { Write-Output "REFUSED: workshop has an 'origin'."; exit 2 }
if (-not ($remotes -contains 'private')) { Write-Output "REFUSED: no 'private' remote."; exit 2 }
$url = (& git --git-dir=$GD remote get-url private)
if ($url -notmatch 'arithmetic-landscapes-private') { Write-Output "REFUSED: wrong private URL."; exit 2 }
Write-Output ("private -> " + $url + "   [passed]")

Write-Output ""
Write-Output "=== GUARD 2: the research repository must track none of this ==="
$leak = 0
foreach ($p in $PATHS) { if (& git -C $TREE ls-files $p) { Write-Output "LEAK: research repo tracks $p"; $leak++ } }
foreach ($g in $GLOBS) { if (& git -C $TREE ls-files $g) { Write-Output "LEAK: research repo tracks $g"; $leak++ } }
if ($leak -gt 0) { Write-Output "REFUSED."; exit 2 }
Write-Output "clean [passed]"

Write-Output ""
Write-Output "=== staging the whitelist, by name and with --force ==="
if ($Commit) {
    & git --git-dir=$GD --work-tree=$TREE checkout --orphan workshop 2>&1 | Out-Null
    foreach ($p in $PATHS) { & git --git-dir=$GD --work-tree=$TREE add --force -- $p 2>&1 | Out-Null }
    foreach ($g in $GLOBS) { & git --git-dir=$GD --work-tree=$TREE add --force -- $g 2>&1 | Out-Null }
    $staged = @(& git --git-dir=$GD --work-tree=$TREE diff --cached --name-only)
} else {
    $staged = @()
    foreach ($p in $PATHS) { $staged += @(& git --git-dir=$GD --work-tree=$TREE add --dry-run --force -- $p 2>&1) }
    foreach ($g in $GLOBS) { $staged += @(& git --git-dir=$GD --work-tree=$TREE add --dry-run --force -- $g 2>&1) }
    $staged = $staged | ForEach-Object { $_ -replace "^add '","" -replace "'$","" }
}

Write-Output "--- by top-level directory ---"
$staged | ForEach-Object { ($_ -split '/')[0] } | Group-Object | Sort-Object Count -Descending |
    ForEach-Object { Write-Output ("  {0,-12} {1}" -f $_.Name, $_.Count) }
Write-Output ("  TOTAL        " + $staged.Count)

Write-Output ""
Write-Output "=== GUARD 3: every staged path is inside the whitelist ==="
$staged = $staged | ForEach-Object { $_.Trim('"') }
$bad = @($staged | Where-Object {
    $f = $_
    -not (($PATHS | Where-Object { $f -like "$_/*" }) -or ($f -like 'lean/pnp/spec_*.md') -or ($f -like 'lean/pnp/paper2_*.md'))
})
if ($bad.Count -gt 0) {
    Write-Output ("REFUSED: " + $bad.Count + " path(s) outside the whitelist, first few:")
    $bad | Select-Object -First 10 | ForEach-Object { Write-Output ("  " + $_) }
    exit 2
}
Write-Output "all inside [passed]"

if (-not $Commit) {
    Write-Output ""
    Write-Output "DRY RUN. Nothing committed. Re-run with -Commit."
    exit 0
}

Write-Output ""
Write-Output "=== committing on an orphan branch ==="
$m = Join-Path $env:TEMP 'workshop.txt'
# The first commit's message described a first commit. Every later run reused it, so the
# second commit asserted "for the first time" about three changed files -- a false sentence
# in a permanent record, written by a default. A hardcoded message is a claim that stops
# being true; make it a parameter with a neutral default.
if ($Message) {
    $body = $Message
} else {
    $n = @(& git --git-dir=$GD --work-tree=$TREE diff --cached --name-only).Count
    $body = "Workshop: $n file(s) updated`n`nThe working documents that the research repository ignores: reports, book, paper-ja,`ndocs, outgoing and the design documents. Orphan branch of the private repository, tracked`nby a git directory outside the working tree with no origin remote."
}
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git --git-dir=$GD --work-tree=$TREE commit -q -F $m
Remove-Item -Force $m
& git --git-dir=$GD push -u private workshop 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git --git-dir=$GD log --oneline -1
Write-Output ""
Write-Output "=== branches now on the private remote ==="
& git --git-dir=$GD ls-remote --heads private
