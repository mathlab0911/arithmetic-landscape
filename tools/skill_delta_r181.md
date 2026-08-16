# Skill delta r181 — the distillation of rounds r160–r180

The case text is folded into `ledger_archive.md`. This file is the **distillation**: exactly what
`pnp-research/SKILL.md` should gain, written so it can be applied verbatim without re-deriving it
from the archive.

**Why this file exists at all.** `save_skill` replaces `SKILL.md` whole — there is no patch
interface — so updating a 55 KB institutional-memory file means reproducing all 55 KB. Doing that
by hand risks a silent transcription error in the one document this project uses to remember why
it does things. **That is precisely the failure class the file itself is about**, so the
distillation is written down first and applied in a session with room to read the original and
emit it back verifiably. Apply, then diff the saved skill against the source before believing it.

---

## A. New entries — a new subsection

Insert after §7.6 (F66–F77), as:

### 7.7 Instruments, identifiers and handovers — F78–F82

Bought over rounds r160–r180: the lift of `prob:R1`, the Leiden signature, the first DOI and
release, the first referee pass, and door 2. Case text in `ledger_archive.md`.

- **F78** **The dangerous failure of a checker is not the false alarm; it is the empty scan.**
  A check that iterates over a discovered set and finds none passes — reporting green on the exact
  commit that removed the thing it protects. C16 caught its own version of this because it carries
  a second clause (*"the check cannot find its subject, which is a failure of the check and not a
  pass for the artefact"*); every check that discovers its own population needs that clause, in
  the same breath as its verdict. **And when a check is repaired after a rename, accept the old
  names as well as the new: a check that recognises only the current wording cannot audit the
  past**, because copies already in circulation carry the old one.

- **F79** **Anything that says "pending X" needs a person who will notice when X happens, because
  the file will not.** A conditional written into a permanent artefact keeps asserting its
  condition after the condition has changed — a licence line reading *"all rights reserved pending
  publication"* survived publication; `.zenodo.json` said *"three results are still explicitly
  conditional"* in the release whose whole subject was that they are not, and went out attached to
  a permanent identifier. **Twice in one day, the second time hours after writing the rule about
  the first.** *Writing the rule down did not install it: what was missing is a trigger.* So the
  release procedure now carries one question, answered before the tag is pushed —
  **what did this release make false?** Sweep every artefact that describes the work in prose
  (`.zenodo.json`, `CITATION.cff`, README, homepage, the previous version's release notes); none
  of them are the paper, so none of them are checked.

- **F80** **A fresh reader is not a more careful version of the author; it is a different
  instrument, and it measures something the author has no access to.** The first referee pass
  returned three findings and **every one was a claim about our own evidence, not about the
  mathematics**: three incompatible descriptions of one independent reading in one document; an
  absolute *"conditional on nothing"* sitting where its qualification was not; a miscount of which
  statements had been waiting. The strongest was one the author could not have made — having
  written both descriptions and believed them consistent, the author cannot see that they are not.
  **This is not a matter of effort.** Two corollaries: **an absolute claim belongs where its
  qualification is, or it belongs nowhere** (the STATUS block is where readers stop); and **state
  the convention where the count is made** — "exactly three" was defensible under *statement =
  numbered environment*, but the sentence justifying it was about damage, and damage does not
  respect environments.

- **F81** **An identifier looks like an imprimatur. Put the caveat where the claim gets copied.**
  A DOI certifies that a version exists and will not change; to almost any reader it looks like it
  certifies more. A qualification in the body of a document does not travel — a badge does. So the
  caveat goes in the three places a reader actually meets: the deposit's description under its own
  heading, the release notes, and **in bold directly under the README badge**. The sentence is
  shorter than the temptation to explain it: **a DOI makes a version permanent; it does not make
  it true.** *(Same shape as F67 and as `rem:notsup`, moved from mathematics to metadata: an
  estimate — or a caveat — made where nobody will read it has not been made.)*

- **F82** **Repeating an action that failed for reasons you cannot see is not persistence; it is a
  loop with a person waiting at the end of it. The second identical attempt is diagnosis; the
  fourth is denial.** When the cost of asking is one sentence and the cost of another attempt is
  another silent failure, ask. Two specifics: **the correct handover is not "please fix this" but
  "the state is here, the button is there, this is what it will ask you, and this is what it will
  not change"** — quoting the confirmation dialog in advance, including the warning that does not
  apply, is part of handing over rather than delegating. And **when an interface has a cache, a
  green screen is not evidence; ask the layer underneath** — the record page served a stale copy
  throughout and would have shown the old text after a successful publish too. *(Extends F61: read
  it back the way a reader would, **and read it from the place where nothing is cached**.)*

---

## B. Strengthenings of existing entries

**F26/F27** — append:

> **A plateau is a claim about a range, and three points inside one are not a range.** A median
> measured flat at `k = 10, 12, 14` was read as an exact effective depth; at `k = 16…20` it moved.
> **And when two people measure "the same" quantity and disagree by a factor, the first suspect is
> not arithmetic but the weight** — an `r`-weighted mean is the value at a typical *ground state*,
> a median over representable targets is the value at a typical *target*, and in one family they
> differ by 1.8 because the ratio is largest exactly where the weight is largest. **Name the
> population and the weighting in the sentence that reports the number, every time.**

**F35** — append (fable-5's r176 ruling, endorsed at constitutional strength):

> **A status that improves is still a status change, and a reader who cannot see the old one
> cannot audit the new one.** When a problem closes, restate it as *closed* with what closed it;
> do not delete it. Deleting leaves a paper that had never been missing anything — a different and
> worse paper — and it hides the strongest thing that can be said: *we knew exactly what the
> result rested on, said so in advance, and then supplied it.* **And closing a gap makes the
> remaining gap more prominent, not less**: with one caveat where there were two, a reader stops
> discounting the list and starts reading it.

**F38** — append:

> **A status is a label on a statement, and a label cannot fix a verb.** The smallest instance:
> *"Then, exactly,"* over a display whose own STATUS two lines below said *derived*. Not a missing
> status, not a wrong status — **a correct status undercut by the prose it labels**, and no
> mechanical check reads adverbs.

**F60** — append as a seventh instance and a rule:

> 7. *A rename.* The disclosure section was renamed to the name the Leiden Declaration specifies,
>    and C16 went red — correctly, by its own second clause. A naive version would have iterated
>    over an empty set and passed. See F78.

> **A green suite is evidence about the classes of defect the suite was built to catch, and about
> nothing else.** `ε*(Z) = ε*(Z) = …` — the left-hand side written twice — compiled with zero
> errors and passed all twenty checks, because a repeated `X =` is valid mathematics. It was found
> by reading the statement aloud in order to quote it. **Writing a claim out for someone else is a
> check, and it is the only unmechanised one we have.**

**F70** (the two positive habits) — append a third:

> - **When a correction makes a bound uglier, the ugliness is information about where the old
>   bound was borrowing.** Print the new ratio next to the old and say which region absorbed the
>   loss. And **a green check on part of a bound must name the part**: *"sixteen points, no
>   failures"* is a true sentence that can carry a false impression, and the STATUS line is where
>   that gets fixed.

---

## C. Two entries that belong to the division of labour (§2)

Append to §2 (Roles and chain of command):

> **Design cannot check itself against magnitudes it has not computed.** The head's prescription
> — force `|X| ≤ 1` across the whole window by a threshold in `k` — could not be carried out:
> `|α|T₁³ ≍ k`, so the condition holds for *small* `k` and dies for large, and a threshold pushes
> the wrong way. The hands measured it, **refused to carry it out, and said so**; the head verified
> the replacement and asked for the failure to be filed under their own name. *A silent patch
> would have left no record that the specification had been wrong.* **Execute faithfully, and
> report back when the execution refuses.**
>
> **The shape to aim for:** head verifies hands, hands correct head, head verifies the correction
> and accepts it. Three passes over one proposition, in both directions. That is what "solid"
> cost.
>
> **The scope of an authorisation is bounded by what the person could plausibly have been
> imagining when they gave it.** "Full authority" did not extend to granting an irrevocable
> worldwide licence on Kentaro's behalf; that was surfaced and decided explicitly. *(The `lem:κ`
> lesson generalised to consent.)*

---

## D. One entry for the referee pass itself

Append to the referee-pass material (or to §7.0):

> **Every procedure whose value is that a human does it can be hollowed out into a checklist while
> keeping its name, and the hollowing does not show up in the log.** Hence fable-5's clause: the
> candidate word list **is a lamp, not a filter**. A pass that degenerates into grepping the list
> has become a twenty-first mechanical check wearing a human costume. **And a reading delivered in
> parts is one reading, not several** — inflating the count of the expensive instrument is the
> same defect as substituting the cheap one for it.

---

## E. Sequencing, recorded because it was not asked for

Append to §6 (the research cycle):

> **A justification found after the choice is still worth recording as having been found after.**
> The head named `hrate-a` as the sharpest open item; the hands opened door 2 instead without
> asking. It turned out to bear on `hrate-a` directly. **The ruling on order was handed back
> late, and the lateness is in the ledger.**
>
> And the positive habit from the same round: **a result you decided to be interested in after
> seeing it is worth less than one you decided to be interested in before.** Door 2's three
> possible outcomes were written down, in a file, thirty-four rounds before the computation — which
> is what makes "we found the second one" a finding rather than a story.
