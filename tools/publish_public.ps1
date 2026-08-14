# Publish the current state to the PUBLIC repository.
#
# Standing rule (Kentaro, 2026-08-14): the private repository is the workshop and
# receives every round; the public one is the display case and shows only the current
# finished form. It is updated at milestones where fable-5's verification has passed.
#
# The dangerous action is the one that has to be typed out. This script refuses unless
# a reason is given, the working tree is clean, and C1-C20 are green.
#
#   .\tools\publish_public.ps1 -Reason "Appendix A verified by fable-5 (r158)"
#
param(
    [Parameter(Mandatory=$true)][string]$Reason,
    [switch]$DryRun
)

$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

Write-Output "=== reason given ==="
Write-Output $Reason
Write-Output ""

Write-Output "=== gate 1: working tree clean ==="
$dirty = & git status --porcelain
if ($dirty) {
    Write-Output $dirty
    Write-Output "REFUSED: the working tree is not clean. Commit or stash first."
    exit 2
}
Write-Output "clean"

Write-Output ""
Write-Output "=== gate 2: C1-C20 ==="
& python tools\check.py | Select-Object -Last 2
if ($LASTEXITCODE -ne 0) {
    Write-Output "REFUSED: checks did not pass."
    exit 3
}

Write-Output ""
Write-Output "=== gate 3: what would become public ==="
& git fetch origin main 2>&1 | Out-Null
$range = "origin/main..HEAD"
$n = (& git rev-list --count $range)
Write-Output ("commits the public repository does not have: " + $n)
if ($n -eq "0") {
    Write-Output "nothing to publish; the public repository is already at this state."
    exit 0
}
& git log --oneline $range
Write-Output ""
Write-Output "files touched:"
& git diff --stat --ignore-all-space origin/main..HEAD

if ($DryRun) {
    Write-Output ""
    Write-Output "DRY RUN: nothing pushed."
    exit 0
}

Write-Output ""
Write-Output "=== publishing ==="
& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)

Write-Output ""
Write-Output "=== post-push: read it back the way a reader would (F61) ==="
& git ls-remote --heads origin main
Write-Output "local HEAD:"
& git rev-parse HEAD
Write-Output ""
Write-Output "Now fetch the public URLs in a browser and confirm, with a positive control."
