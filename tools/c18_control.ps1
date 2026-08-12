$ErrorActionPreference = 'Stop'
Set-Location 'C:\Users\amake\Claude\Projects\study'
$hp  = 'C:\Users\amake\Claude\Projects\homepage\index.html'
$bak = "$env:TEMP\index_c18_backup.html"
Copy-Item $hp $bak -Force

function Run-C18 {
  $out = & python tools\check.py 2>&1 | Select-String -Pattern 'C18'
  return ($out -join ' | ')
}

Write-Output '=== (0) baseline: the real homepage ==='
Write-Output (Run-C18)

Write-Output ''
Write-Output '=== (1) negative control: inject the banned literal 5.34920 ==='
$s = Get-Content $hp -Raw -Encoding UTF8
($s -replace '5\.3492879', '5.34920') | Set-Content $hp -NoNewline -Encoding UTF8
Write-Output (Run-C18)
Copy-Item $bak $hp -Force

Write-Output ''
Write-Output '=== (2) negative control: delete the AI disclosure heading ==='
$s = Get-Content $hp -Raw -Encoding UTF8
($s -replace 'Use of AI tools', 'Acknowledgements') | Set-Content $hp -NoNewline -Encoding UTF8
Write-Output (Run-C18)
Copy-Item $bak $hp -Force

Write-Output ''
Write-Output '=== (3) negative control: put back a retired name ==='
$s = Get-Content $hp -Raw -Encoding UTF8
($s -replace 'Three parts, in preparation', 'four papers, in preparation') | Set-Content $hp -NoNewline -Encoding UTF8
Write-Output (Run-C18)
Copy-Item $bak $hp -Force

Write-Output ''
Write-Output '=== (4) restored: baseline again ==='
Write-Output (Run-C18)
Remove-Item $bak -Force
Write-Output ''
Write-Output '=== full run on the restored tree ==='
& python tools\check.py | Select-Object -Last 3
Write-Output "exit=$LASTEXITCODE"
