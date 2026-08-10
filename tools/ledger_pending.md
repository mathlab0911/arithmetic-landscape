# Pending failure-ledger entries

Entries written mid-round, not yet folded into the `pnp-research` skill (§7).
`tools/check.py` (C6) prints this file on every run. Clear it at the next skill save.

Full text of entries already folded in lives in `tools/ledger_archive.md`.

---

## F35 — the summaries are a POPULATION, and they drift together (r117, pre-endorsement sweep)

```
claimed   : after r117 the papers were honest -- status inside every theorem, C8 enforcing it --
            so the over-claiming was fixed
actual    : three summaries still said more than the papers, and were found one at a time, each
            only because someone was about to read it.
              memory   -- paper 3 recorded as "finished" while its two theorems are skeletons
              README   -- papers 2 and 3 called "Complete"; every count stale
              homepage -- "Every theorem I state is formally verified in Lean 4 with Mathlib,
                          with no sorry and no additional axioms", which is true of the
                          structural results and false of papers 2, 3 and 4; paper 2 listed
                          under a title it had not carried for weeks; papers 3 and 4 absent
            The homepage is the one linked from the signature of every endorsement email sent.
check     : enumerate the artefacts that DESCRIBE the work -- memory, README, homepage, the
            abstracts, any profile or bio -- and check them against the papers as a set, in one
            pass. There were four; I fixed them in three separate rounds because I kept treating
            each as the last one.
rule      : *** F35's population is not "the abstract": it is every artefact that summarises the
            work, and they drift TOGETHER because they were all written from the same optimistic
            draft. *** When one summary is found over-claiming, that is evidence about the
            others, not an isolated defect -- go and check them the same hour. Asserted where the
            artefact is in the repository (C9 for the README's counts); the homepage lives in a
            different repository and is therefore the one most likely to rot next, so it now
            carries the same status vocabulary as the papers, which makes drift visible.
```
