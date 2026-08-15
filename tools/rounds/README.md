# One-round scripts and commit-message drafts

These are the disposable artefacts of individual rounds: the PowerShell used once to seed a
remote or replay the kernel, and the message files handed to `git commit -F`. They are kept
rather than deleted because a commit message that was drafted, edited and then used is part of
the record of how a claim reached the repository, and because the ledger cites some of them by
name.

Nothing here is part of the apparatus. The standing tools are one directory up:
`check.py` (checks C1-C20), `check_lean.ps1` (the import-closure check), `push_round.ps1`,
`publish_public.ps1`, `workshop_setup.ps1`, `workshop_verify.ps1`.
