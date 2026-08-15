# Launch the kernel replay detached and return immediately; poll the log afterwards.
# Written as a script FILE because -Command mangles $ variables (skill §9, and this round
# is the reminder: the first attempt was made with -Command and lost its own $log).
$ErrorActionPreference = 'Continue'
$root = 'C:\Users\amake\Claude\Projects\study'
$out  = Join-Path $root 'lean\pnp\checker_r160.log'
$err  = Join-Path $root 'lean\pnp\checker_r160.err'

if (Test-Path $out) { Remove-Item -Force $out }
if (Test-Path $err) { Remove-Item -Force $err }

$p = Start-Process -FilePath 'powershell' `
     -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File',(Join-Path $root 'tools\check_lean.ps1') `
     -RedirectStandardOutput $out -RedirectStandardError $err `
     -WorkingDirectory $root -PassThru -WindowStyle Hidden

Write-Output ("launched pid=" + $p.Id)
Write-Output ("stdout -> " + $out)
Write-Output ("stderr -> " + $err)
Start-Sleep -Seconds 20
Write-Output ""
Write-Output "=== first 20 seconds ==="
if (Test-Path $out) { Get-Content $out -Tail 20 } else { Write-Output "(no output yet)" }
Write-Output ("still running: " + (-not $p.HasExited))
