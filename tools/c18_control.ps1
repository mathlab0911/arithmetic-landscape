$ErrorActionPreference = 'Stop'
Set-Location 'C:\Users\amake\Claude\Projects\study'
$hp   = 'C:\Users\amake\Claude\Projects\homepage\index.html'
$rm   = 'C:\Users\amake\Claude\Projects\study\README.md'
$hpb  = "$env:TEMP\index_c18_backup.html"
$rmb  = "$env:TEMP\readme_c18_backup.md"
Copy-Item $hp $hpb -Force
Copy-Item $rm $rmb -Force

function Run-C18 { (& python tools\check.py 2>&1 | Select-String -Pattern 'C18') -join ' | ' }
function Patch($p, $from, $to) {
  $s = [System.IO.File]::ReadAllText($p)
  [System.IO.File]::WriteAllText($p, ($s -replace $from, $to), (New-Object System.Text.UTF8Encoding $false))
}

Write-Output '=== (0) baseline ==='
Write-Output (Run-C18)

Write-Output ''
Write-Output '=== (1) homepage: inject the banned literal 5.34920 ==='
Patch $hp '5\.3492879' '5.34920'; Write-Output (Run-C18); Copy-Item $hpb $hp -Force

Write-Output ''
Write-Output '=== (2) homepage: remove the disclosure heading ==='
Patch $hp 'Use of AI tools' 'Acknowledgements'; Write-Output (Run-C18); Copy-Item $hpb $hp -Force

Write-Output ''
Write-Output '=== (3) homepage: restore a retired name, with no retirement marker ==='
Patch $hp 'Three parts, in preparation' 'four papers, in preparation'; Write-Output (Run-C18); Copy-Item $hpb $hp -Force

Write-Output ''
Write-Output '=== (4) README: bring back deg_A ==='
Patch $rm 'lm_A\(n\)/r_A\(n\)' 'lm_A(n)/deg_A(n)'; Write-Output (Run-C18); Copy-Item $rmb $rm -Force

Write-Output ''
Write-Output '=== (5) README: strip every retirement marker from the paper-3 sentence ==='
Patch $rm 'The manuscript that was paper 3' 'Paper 3'
Patch $rm 'was absorbed into Part III at r130' 'appears in Part III at r130'
Write-Output (Run-C18); Copy-Item $rmb $rm -Force

Write-Output ''
Write-Output '=== (6) restored ==='
Write-Output (Run-C18)
Remove-Item $hpb, $rmb -Force
Write-Output ''
& python tools\check.py | Select-Object -Last 2
Write-Output ("exit=" + $LASTEXITCODE)
