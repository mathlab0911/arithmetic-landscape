# Pending failure-ledger entries

Entries written mid-round, not yet folded into the `pnp-research` skill (§7).
`tools/check.py` (C6) prints this file on every run. Clear it at the next skill save.

Full text of entries already folded in lives in `tools/ledger_archive.md`.

---

(empty: emptied at the skill save in r131, which folded fourteen blocks covering r119–r131
into F18, F39, F47, F52, F60, F61, F62 and the three new entries F63, F64, F65)

---

## r132 (fable-5) — the verifier is not exempt from the cache (append to F61)

```
  claimed   : (draft r132) the README on main still writes deg_A(n); C18 passes over it
  actual    : fixed at a544f9b; the fetch of raw/main served the previous render from an
              edge cache.  The verifier's own evidence was one cache window old
  check     : verify at the immutable revision (raw/<sha>/…), never at the mutable path,
              whenever the claim is about the current state; keep the mutable-path fetch
              only as evidence about what SOME readers may still be seeing
  rule      : a mutable path inside its cache window can show any recent state, including
              one that resurrects fixed defects — and the verifier is not exempt.  Pin
              the revision first, then discuss the caches
```

This is the second half of the entry whose first half was written the round before, and the
symmetry is the point. At r130 the *author* was misled by a stale surface into thinking a
published page was clean when a reader saw otherwise. At r132 the *verifier* was misled by a
stale surface into nearly filing a defect that had already been fixed. Same mechanism, both
directions, one day apart.

> **Pin the revision, then discuss the caches.** The immutable path answers "is the published
> state correct?"; the mutable path answers "is that what a reader sees right now?". They are
> different questions and the second one has a time in its answer.

Recorded also because the draft report existed: a verifier who retracts before publishing has
still done the work of retracting, and the retraction is more informative than the finding
would have been. The post-TTL sweep (`lean/pnp/surfacesweep_r132.log`) is the other half of
the repair — all three surfaces caught up about twenty-two hours after the push.

## r132 — a tool that cries wolf on its own output (append to F58)

`python3 -W always tools/check.py` printed **230 ResourceWarnings** — twenty sites doing
`open(...).read()` without closing. Harmless: CPython closes them on collection, and the
checker has never misbehaved because of it.

That is exactly why it is worth fixing. A tool whose own diagnostic channel is full of noise
it generates itself trains its reader to skip that channel, and the next warning to appear
there will be a real one. Everything now goes through `_read` / `_lines`; the count is zero.

## r132 — a comment that asserted what the theorem below it denies

`Bridge.lean`'s section heading read "窓級数 = gapSeries 恒等式" and its body said the window
series "coincides exactly with Γ = gapSeries". The theorem underneath states
`windowSeries A D = gapSeries A + (2D+1)/2^{|A|}` — so the comment dropped the boundary term
— and, since r120, the canon's identifier `gapSeries` is the *enumeration* form while the
paper's Γ is the *layer* form, so "= Γ" also conflated two different objects. One sentence,
both mistakes.

> A comment is not checked by anything. C7 verifies that every Lean name a paper cites
> exists; nothing verifies that a sentence next to a theorem says what the theorem says.

Fixed by making the comment point at the theorem instead of paraphrasing it — the cheapest
form that cannot go stale in the same way. The naming collision itself is recorded at the
definition in `Landscape.lean`; renaming the canonical identifier is deferred until there is
another reason to redo the kernel replay.
