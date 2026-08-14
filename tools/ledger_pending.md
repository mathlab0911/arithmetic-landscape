# Pending ledger entries

Entries written mid-round that have not yet been folded into the `pnp-research` skill (§7).
C6 prints this file on every run so nothing written here is lost between skill saves.

**Last fold: 2026-08-14 — 26 blocks from rounds r141–r154, distilled into F66–F76 (a new §7.6,
"Measurement, search, and reading your own result") plus sharpenings to F27, F30, F47, F57,
F58, F59 and F60. The case text moved to `ledger_archive.md`.**

Nothing pending.

---

## r156 — a process rule adopted by fable-5, to sit beside C20 at the next skill save

**The round's own literature pass completes before the round's push.**

Proposed by opus-5 in r155 §5 after two same-hour self-corrections in one round; adopted by
fable-5 in r156 §2 as taken, with the reasoning that both corrections had the identical shape:
*the deferred pass fired after the artefact had already shipped.*

> **C20 closed the gap between measured and proved. This closes the gap between cited and
> checked.** They are the same defect at two different stages — a claim released while one of
> its own supports is still outstanding — and in both cases the support was one the author had
> already put on the list and postponed.

Not mechanisable as it stands: no check can tell whether a literature pass "happened". What it
can be is a **precondition on the push script**, the way `check.py` is — the round does not push
until the round's own citations have been read against documents. Record it as a rule now; if a
later round finds an assertable form, assert it.

**Also from r156, and it belongs in the ledger of things done right rather than the other one:**
the four judgements of r155 were accepted whole, and D1–D4 stand **provisionally** — ratification
deferred into the next round's audit rather than granted from the doorway, on the explicit
grounds that ratifying them sight-unseen would repeat the `lem:kappa` shape (approving a
description instead of the artefact). *That is F52 firing in the other direction, as a refusal to
rubber-stamp.* Proxy status continues until that audit.

---

## r157 — two repositories: the workshop and the display case

**Kentaro's instruction, 2026-08-14.** `arithmetic-landscapes-private` is the workshop and
takes every round; `arithmetic-landscapes` is public and shows only the current finished form,
updated at milestones where fable-5's verification has passed. Public history is preserved and
appended to, never rewritten (r117's lesson: rewriting a public history makes objects
unreachable, not absent).

**The question that had to be asked before doing any of it.** "Only the finished form" has two
readings, and they differ by the whole credibility of the project:

> The public repository's value is not the papers. It is that every number has a committed log,
> every theorem is replayed by an independent kernel, and the failure ledger is public — because
> the README says *work produced this way cannot be trusted on the author's word; it has to be
> checkable.* **Move the logs and the ledger into the private repository and the papers stay but
> the reason to believe them leaves.**

Kentaro chose papers **plus the whole evidence trail** stays public; what moves is only
work-in-progress. Recorded because the wrong reading would have been an easy, tidy-looking
mistake, and because the general form applies beyond git:

> **When a request means "show less", ask which part of what is shown is load-bearing.** A
> display case that shows only conclusions is a weaker artefact than one that shows the working,
> even though it looks stronger.

**Mechanically.** One tree, one `.gitignore`, one history, two remotes; the difference is *when*
each is pushed. `main` now tracks `private/main`, so a bare `git push` goes to the workshop.
Publishing is a separate script that **refuses without a typed reason**, and also refuses on a
dirty tree or a red suite, then prints exactly which commits and files would become public.

> **Put the friction on the dangerous side.** The everyday action should be one keystroke and the
> irreversible one should make you write a sentence about why.

*Still outside both repositories:* `reports/`, `book/`, `paper-ja/`, `docs/`, `outgoing/`,
`lean/pnp/spec_*.md`. Backing those up into the private remote is a **separate** decision, and
the thing to build first is the guarantee that they cannot reach the public one — one tree with
one ignore file cannot express "tracked here, not there".

---

## r158 — the workshop repository, and the two things that fought back

The working documents — `reports/`, `book/`, `paper-ja/`, `docs/`, `outgoing/` and the design
documents — now live in an orphan branch of the private repository, tracked by a git directory
at `study-workshop.git` that sits **outside** the working tree and has **no `origin` remote**.
203 files that until today existed on exactly one disk.

> **Separation by structure, not by convention.** The public remote is not reachable from the
> workshop repository at all; and the research repository cannot track the workshop's git
> directory because it is not in the tree. Neither side needs anyone to remember a rule.

**The thing that fought back first, and it is a genuine piece of git.** A `.gitignore` lives in
the **working tree**, so *both* repositories read it, and `.gitignore` outranks
`$GIT_DIR/info/exclude`. A whitelist written in `info/exclude` therefore cannot re-admit what
`.gitignore` excludes — the first attempt staged **zero** files and said nothing about why.

> **An empty measurement that reports success is the r150 shape again**, and it appeared here
> within one command of being trusted. The fix is not to argue with the precedence: add the
> whitelist **by name, with `--force`**. That leaves the failure mode pointing the safe way —
> a careless `git add -A` in the workshop adds *nothing*, because the research repository's
> ignore rules block every one of these files. **The rule that caused the difficulty is the one
> that closes the dangerous direction.**

**The thing that fought back second was our own guard, and it fired correctly.** The whitelist
check refused the commit because git had escaped the Japanese filenames as
`"book/\345\205\245..."`, which does not match `book/*`. Not a leak — a checker reading its own
escaping as a violation.

> **Second time this week that a checker written in English-shaped assumptions misread
> Japanese** (F69 was a line-wrapped exemption phrase). The setting is `core.quotepath false`,
> and it is applied on **every run** rather than at creation, because a setting applied only at
> setup is a setting a fresh clone will not have.

**Verified from outside, with a positive control** (F61): the public repository has one branch,
`main`, and zero files under any protected path; its raw URL for a report returns nothing while
`tools/allow_numbers.txt` returns content. The private repository shows `main` and `workshop`,
and the workshop branch shows exactly the six directories.
