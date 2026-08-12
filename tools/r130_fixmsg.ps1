$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'
$tmp = Join-Path $env:TEMP 'r130_msg2.txt'
& git log -1 --pretty=%B | Out-String | ForEach-Object { $_ -replace "^\uFEFF", '' } |
    ForEach-Object { [System.IO.File]::WriteAllText($tmp, $_, (New-Object System.Text.UTF8Encoding $false)) }
& git commit -q --amend -F $tmp
Remove-Item -Force $tmp
Write-Output '=== first bytes of the message ==='
$b = & git log -1 --pretty=%B
Write-Output ($b | Select-Object -First 1)
Write-Output '--- hexdump of first 6 bytes ---'
$raw = & git log -1 --pretty=%B | Out-String
[System.Text.Encoding]::UTF8.GetBytes($raw.Substring(0, 6)) | ForEach-Object { '{0:X2}' -f $_ }
