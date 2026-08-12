$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'
Remove-Item -Force .git\index.lock -ErrorAction SilentlyContinue
Write-Output '=== git rm the retired files (history keeps them) ==='
& git rm --quiet paper/paper3.tex paper/paper3.pdf
Write-Output ('rm paper/ exit=' + $LASTEXITCODE)
Write-Output '=== paper-ja is gitignored; remove from disk ==='
Remove-Item -Force paper-ja\paper3_ja.tex, paper-ja\paper3_ja.pdf, `
                   paper-ja\paper3_ja.aux, paper-ja\paper3_ja.log, paper-ja\paper3_ja.out `
                   -ErrorAction SilentlyContinue
Remove-Item -Force paper\paper3.aux, paper\paper3.log, paper\paper3.out -ErrorAction SilentlyContinue
Remove-Item -Force paper\.labels\paper3.txt -ErrorAction SilentlyContinue
Write-Output '=== what remains ==='
Get-ChildItem paper\paper*.tex, paper-ja\paper*.tex | Select-Object -ExpandProperty Name
