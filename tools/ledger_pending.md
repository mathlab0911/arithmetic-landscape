# Pending failure-ledger entries

Entries written mid-round, not yet folded into the `pnp-research` skill (§7).
`tools/check.py` (C6) prints this file on every run. Clear it at the next skill save.

Full text of entries already folded in lives in `tools/ledger_archive.md`.

---

## r117: "force push" is not "deleted", and the identity in a commit is a published claim

```
claimed   : after git filter-repo and a force push, the design documents were gone -- every
            local check agreed: 0 tracked, 0 paths anywhere in history, 404 on main
actual    : GitHub keeps unreachable objects, and the OLD COMMIT SHA still served the full file.
            The local checks were all true and all irrelevant: they measured the repository I
            control, not the one the reader sees. Only deleting and recreating the repository
            actually removed it. The same thing then happened a second time with commit
            identity -- the visible history was clean and an orphaned SHA still showed the wrong
            account.
check     : fetch the artefact from OUTSIDE, by the route a reader would use, with a positive
            control alongside it -- an empty response means nothing until a URL you expect to
            work returns content. Then repeat for an old SHA, not just for the branch tip.
rule      : *** rewriting history changes what is REACHABLE, not what is STORED. *** For content
            that must actually be gone from a hosted repository, delete and recreate it; there
            is no client-side operation that does the job. And check from the outside: a
            verification run against your own working copy cannot see a hosting layer.
extra     : the second half of this entry is a plain mistake of mine. I committed with
            `-c user.email=<the account address from my environment>` instead of the address the
            repository was configured with, and GitHub attributes commits by email -- so ninety
            commits were credited to an unrelated account of the author's. **A commit identity
            is published metadata, not a local setting.** Read `git config user.email` in the
            repository and use that; never substitute an address from somewhere else.
```

## r118: a directory you create beside a mount is not inside it

```
claimed   : the r118 experiment scripts were "saved to study-private-lab", safe from the
            session ending -- I had made the directory with mkdir and written into it, and a
            listing showed all ten files
actual    : the sandbox exposes only the mounted folders. `mkdir ../study-private-lab` from
            inside the mount created a directory in the SANDBOX that merely sits beside the
            mount point and shares its name with a real folder on the user's machine. The two
            were different directories with different contents, and everything written to the
            sandbox one would have vanished when the session ended. Found only because a
            Windows-side listing showed two of the ten files instead of ten.
check     : list the directory from BOTH sides before trusting it, or write through a path
            that is known to be shared. The transfer route that works: sandbox -> the outputs
            folder (which is genuinely mounted) -> move on the Windows side.
rule      : *** persistence is a property of the path, not of the write succeeding. *** A
            successful write and a correct-looking listing prove only that some filesystem
            accepted the bytes. Before treating a file as saved, confirm it from the side that
            outlives the session -- the same shape as F55 (the control must be on the property
            you mean) and the same shape as "force push is not deletion" (a local check cannot
            see the other side of a boundary).
```

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
