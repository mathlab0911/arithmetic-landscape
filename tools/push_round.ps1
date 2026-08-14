# The everyday push: commit the round and send it to the PRIVATE workshop.
#
# Standing rule (Kentaro, 2026-08-14): private receives every round; public is updated
# only at verified milestones, and only through tools\publish_public.ps1.
#
#   .\tools\push_round.ps1 -MessageFile C:\path\to\message.txt
#   .\tools\push_round.ps1 -Message "one-line message"
#
# Pass -Paths to commit named paths instead of everything, which is the safe default when
# line-ending churn would otherwise stage files whose content did not change.
#
param(
    [string]$Message,
    [string]$MessageFile,
    [string[]]$Paths
)

$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

Write-Output "=== what actually differs (content, ignoring line endings) ==="
& git diff --stat --ignore-all-space
Write-Output "--- untracked ---"
& git ls-files --others --exclude-standard

Write-Output ""
Write-Output "=== C1-C20 ==="
& python tools\check.py | Select-Object -Last 2
if ($LASTEXITCODE -ne 0) {
    Write-Output "REFUSED: checks did not pass."
    exit 3
}

Write-Output ""
if ($Paths) { & git add -- $Paths } else { & git add -A }

if ($MessageFile) {
    & git commit -q -F $MessageFile
} elseif ($Message) {
    $m = Join-Path $env:TEMP 'round_msg.txt'
    [System.IO.File]::WriteAllText($m, $Message, (New-Object System.Text.UTF8Encoding $false))
    & git commit -q -F $m
    Remove-Item -Force $m
} else {
    Write-Output "REFUSED: give -Message or -MessageFile."
    exit 4
}

Write-Output "=== pushing to the PRIVATE workshop ==="
& git push private main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
& git status --short

Write-Output ""
Write-Output "public repository is NOT updated by this script; use tools\publish_public.ps1"
& git fetch origin main 2>&1 | Out-Null
Write-Output ("commits the public repository is behind: " + (& git rev-list --count origin/main..HEAD))
