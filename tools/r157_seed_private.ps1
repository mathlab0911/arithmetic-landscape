$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

Write-Output "=== seeding the private workshop with the full history ==="
& git push private main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)

Write-Output ""
Write-Output "=== confirm both remotes now point at the same commit ==="
Write-Output "public  (origin):"
& git ls-remote --heads origin main
Write-Output "private:"
& git ls-remote --heads private main
Write-Output "local HEAD:"
& git rev-parse HEAD

Write-Output ""
Write-Output "=== set the default push target for the working branch to private ==="
& git branch --set-upstream-to=private/main main 2>&1
Write-Output ("upstream exit=" + $LASTEXITCODE)
& git rev-parse --abbrev-ref main@{upstream}
