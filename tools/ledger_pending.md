# Pending ledger entries

Entries written mid-round that have not yet been folded into the `pnp-research` skill (§7).
C6 prints this file on every run so nothing written here is lost between skill saves.

**Last fold: 2026-08-15 — 3 blocks from rounds r156–r158.** The cadence rule adopted by fable-5 now sits
beside C20 inside F70, as instructed; the second Japanese-encoding instance joined F69; the
repository split became F77; and sections 9, 12 and 13 carry the practice changes. Case text in
`ledger_archive.md`.

Nothing pending.

---

## r160 — the canon replayed, and a rule I had and did not use

**Result.** `check_lean.ps1`: three poisoned modules rejected (exit 1 each), all 16 canon
source files inside the import closure of `Pnp`, ten `Pnp/Experiments` files deliberately
outside it, and **every constant of the 17-module canon replayed through the kernel in
179.8 s — PASS**. Nothing in the canon changed this session; this is the periodic confirmation
that it is still green after two days of heavy work on the papers around it.

**And the small thing worth one line.** The first attempt launched the replay with
`powershell -Command`, whose wrapper ate the `$log` variable and produced
`CommandNotFoundException` on a path. §9 of this skill has said *pass PowerShell work as a
script file, not `-Command`* since r116, and one round earlier this same session it gained the
sibling *pass long text as a file, not as an argument*.

> **A rule that exists and is not reached for is not yet a habit.** The ledger's value is in the
> reflex, not in the text; when the text is right and the hand does it anyway, the entry to make
> is not a new rule but a note that this one needs to be the default form. **Write the script
> file first, every time — there is no case where `-Command` with a variable is the right tool
> here.**
