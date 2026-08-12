$ErrorActionPreference = 'Continue'
Set-Location 'C:\Users\amake\Claude\Projects\study'

& python tools\check.py | Select-Object -Last 2
Write-Output ("check exit=" + $LASTEXITCODE)

& git add -A
$m = Join-Path $env:TEMP 'r138.txt'
$body = @"
Ledger: the hypothesis failed in exactly one place, and that place was the theorem

Testing the distribution-relation floor as a stand-alone tool, it failed at one
cell: the primes at q = 6, true average 0.1457 against a floor of 0.4621.

Not a bug. The lemma needs the residues to cover an ADDITIVE coset, and the
primes' residues mod 6 are {1,5} -- a multiplicative subgroup that is not one.
The failure is the modulus-6 phenomenon that Part II spends a section on.

Chasing why gave a two-line proposition: (Z/q)^* is an additive coset of a
subgroup of Z/q if and only if q is a power of 2. Both 1 and -1 are units, so the
coset modulus divides 2; modulus 2 forces every odd residue to be a unit. That one
fact explains why the extremal modulus is 4 for a random odd sequence and 6 for
the primes -- two theorems the papers currently prove separately.

When a lemma's hypothesis fails on real data, check whether the failure is a known
phenomenon before treating it as an error. A hypothesis that fails exactly where
the subject is exceptional has located the exception. And: run a new lemma against
the cases you already understand before the ones you do not -- the value of a
six-by-two table came entirely from the single cell where the answer was known and
the lemma disagreed.

Also this round, gitignored: the floor stated as a stand-alone lemma with no
vocabulary of ours, and measured head-to-head against Koksma. At every rational
with small denominator the Koksma bound is negative -- vacuous -- while the coset
floor is tight to four decimals; away from small rationals Koksma works and the
floor does not apply. Complementary, not competing, which is a smaller claim than
"improves on Erdos-Turan" and a true one.

No paper text changed.

C1-C19 pass.
"@
[System.IO.File]::WriteAllText($m, $body, (New-Object System.Text.UTF8Encoding $false))
& git commit -q -F $m
Remove-Item -Force $m

& git push origin main 2>&1
Write-Output ("push exit=" + $LASTEXITCODE)
& git log --oneline -1
& git status --short
