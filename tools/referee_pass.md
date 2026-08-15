# The referee pass

**A standing procedure, ruled on by fable-5 in r171, adopted r175.**

Every defect this project shipped in its last three rounds that actually mattered was invisible
to all twenty mechanical checks and to the typesetter, and was caught by a person reading:

- an adverb — *"Then, exactly,"* — over a display whose own STATUS two lines below contradicted
  it (r164);
- `ε*(Z) = ε*(Z) = …`, the left-hand side written twice, which compiled with zero errors and
  passed C1–C20, because a repeated `X =` is valid mathematics (r166);
- a licence line reading *"pending publication"* after publication, a section renamed out from
  under the check that guards it, and that check's own empty-scan blind spot (r169–r171).

**Three of a kind in three rounds is not a rate. It is a category**, and the category is: *what
a machine cannot see is what a machine was not asked about.* A green suite is evidence about the
classes of defect the suite was built to catch, and about nothing else.

---

## The form

**Per statement for mathematics. Per paragraph for prose. Always in a fresh context.**

A statement is a theorem, proposition, lemma, remark, problem or STATUS block. A paragraph is a
paragraph. "Fresh context" means the reader has not just written the thing, and has not been
reading around it — a new session, or a model that has not seen the surrounding work.

**When fresh context is not available, the pass is not run and is not recorded as run.** A pass
by the author over their own sentences is worth doing and is worth nothing as evidence; log it,
if at all, as `self` and never as a verdict. The word *always* above is doing real work, and
this is what it costs.

## What the reader is asked to do — three things, and nothing else

1. **Restate the claim in your own words.** Not paraphrase the sentence: state what would have
   to be true of the world for the claim to hold. A claim that cannot be restated is not yet a
   claim.
2. **Name what would falsify it.** Concretely: which computation, which counterexample, which
   value out of which range. "Nothing could falsify it" is an answer, and it is a finding.
3. **Flag any single word whose deletion or replacement changes the claim.** This is the adverb
   class, and it produced two of the three supports above. Candidates: *exactly, always, every,
   only, immediately, therefore, clearly, essentially, effectively, in fact, of course,
   pending, still, now.*

Nothing else. The pass is not a proof check, not a style review, and not an invitation to
suggest improvements.

*The design assumption behind the restriction, stated as an assumption because that is what it
is:* **a reader given three jobs does three jobs; a reader given a general brief writes an
essay.** We have not measured this. If a pass comes back as an essay, or if the three jobs miss
a defect that a general brief would have caught, the assumption is wrong and the form should
change.

## Rules of the pass

- **Cap the batch.** At most 15 units per session. Past that the context stops being fresh,
  which is the only thing the pass has going for it.
- **Log it like an experiment.** One line per unit: `stem — round — verdict`, where the verdict
  is `clear`, `restated-differently`, `no-falsifier`, or `word:<the word>`. The log lives beside
  the scripts in `lean/pnp/` under the round's stem, exactly like a measurement, because that is
  what it is.
- **A flagged word is not automatically a defect.** It is a place where the author has to say
  out loud why the word is right. If they cannot, it goes.
- **The pass does not gate a push.** C20 gates pushes. This one gates the *milestone*: a
  version does not become a public release until the statements it changed have been through it.

## What it does not do

It does not replace the independent reading that turns a written argument into a proof — that is
a different and heavier thing, and for `prob:R1` it arrived in three parts (r162, r164, r171),
which is **one** reading delivered piecewise and not three readings. The referee pass is cheap
and frequent; the independent reading is expensive and rare. **Do not let the cheap one be
quoted as if it were the expensive one** — and do not let a reading delivered in parts be
counted as several. Inflating the count of the expensive instrument is the same defect as
substituting the cheap one for it.
