# Governance — this project as an instance of the three-layer model

**Commissioned by Kentaro; designed by fable-5 (r192); written up here at r193.**

A three-layer model for multi-agent work is in circulation: a **deterministic orchestrator**, a
**non-participating auditor**, and **mutually-evaluating agents**. This document maps our system
onto it — honestly, meaning we say where we already satisfy it, where we do not, and which of its
provisions we decline and why.

> **A model adopted wholesale is a model nobody checked against the thing it describes.** The
> value of writing this down is not the adoption; it is the two places where the mapping is
> imperfect, because those are the places the model can teach us something.

---

## 1. The mapping, as it already stands

| Model layer | What plays it here | Why the identification is honest |
|---|---|---|
| **Deterministic orchestrator** | The check suite **C1–C20**, the **status vocabulary**, and the **round-report protocol** | All three are mechanical and none of them is a model's judgement. C1–C20 run before every commit and refuse; the status vocabulary (*formally verified / proved / derived / measured / conjectured*) is enforced by C8 at the statement; the protocol admits exactly one live report per direction. |
| **Non-participating auditor** | The **referee pass** (`tools/referee_pass.md`) | Its defining property is the one the model asks for: **fresh context**. A reader who has been working on the material is not an auditor, and the procedure says so — *when fresh context is not available, the pass is not run and is not recorded as run.* |
| **Mutually-evaluating agents** | **fable-5 (head) and opus-5 (hands)**, each verifying the other in both directions | Documented in the skill §2 and demonstrated: `prob:R1` took three passes of correction *in both directions*, and the head's own wrong recipe (r173) is in the ledger under their name at their request. |

**Where the identification is imperfect, and this is the useful part:**

- Our orchestrator is deterministic *about form* and silent *about content*. C1–C20 check that a
  status exists, that a number is in a log, that a cross-reference resolves. **None of them reads
  for sense** — which is exactly the hole the referee pass was created to cover, after
  `ε*(Z) = ε*(Z) = …` passed all twenty checks and a typesetter.
- Our auditor is **not continuously non-participating**. It is invoked. A standing auditor would
  see every round; ours sees the statements a round changed, at a milestone. That is cheaper and
  it is weaker, and the difference is stated rather than glossed.

---

## 2. Adopted: A-1, the evidence-path declaration

**Rule, in force from r192.** *Every verification declares, in the report, which artefacts it
touched and whether it was independent of the author's description of them.*

Required field in every round report that claims a verification:

```
EVIDENCE PATH
  artefacts touched : <files, by name>
  independent of    : <the description(s) this reading did NOT rely on>
  grain             : <line by line | statement | paragraph | spot-check>
```

**Why.** The `lem:kappa` incident: a decision was approved on the basis of a *description* of it
rather than the thing itself, and the same shape recurred when a proxy asked to be released from
the doorway. The rule mechanises the lesson:

> **Approving a description is not approving the thing, and a verification that read the author's
> account of an artefact has verified the account.**

It also fixes a defect the referee pass exposed: three incompatible descriptions of one
independent reading, in one document, because nobody had been required to say *which text* each
reading covered. With the field, that cannot be written without noticing.

---

## 3. Adopted: A-2, the status-transition table

Each edge names **who may move it** and **what evidence class is required**. Nothing else moves a
status.

| From | To | Mover | Evidence class |
|---|---|---|---|
| *(new)* | **conjectured** | either model | a statement plus a named falsifier |
| **conjectured** | **measured** | hands | a committed script with a log, range stated |
| **measured** | **derived** | either | an argument from stated hypotheses, inheriting their status |
| **derived** | **proved** | either, **then confirmed by the other** | a written proof **and** a second independent reading, with its evidence path (A-1) |
| **proved** | **formally verified** | hands | Lean, in the import closure of `Pnp`, replayed through the kernel by a checker that first rejects the poisoned modules |
| **any** | **open register** | either | the honest third outcome; naming a thing open is a move, not a failure |
| **any** | **weaker status** | either, **unilaterally** | none required — *lowering a status needs no permission, only a reason* |

Two asymmetries are deliberate:

- **Raising requires the other party; lowering does not.** The expensive direction is guarded.
- **Every edge is reversible and every reversal is recorded.** *A status that improves is still a
  status change, and a reader who cannot see the old one cannot audit the new one* — so `prob:R1`
  remains in Part III, restated as CLOSED with what closed it.

---

## 4. Declined, with reasons

**JSON scoring of agent output.** Declined. A numeric score is a currency, and a currency invites
optimisation of the currency.

> **The currency here is a named artefact and a named falsifier.** *"This claim dies if the ratio
> at `k = 40` exceeds 2"* is worth more than any score, because it can be spent by someone who
> distrusts us. **We have already paid for our opinions; a score would let us mint more without
> paying.**

**Role rotation.** Declined. The head/hands split is not a fairness arrangement, it is a
*division of instruments*: the head holds design and the hands hold magnitudes, and the round
that mattered most this month turned on exactly that — *design cannot check itself against
magnitudes it has not computed*. Rotating the roles would rotate away the asymmetry that makes
the correction possible.

**Continuous auditing.** Not declined, not adopted: **priced.** A standing referee pass over every
round would cost roughly one fresh-context session per round. We run it at milestones instead and
say so, which is a weaker guarantee honestly described rather than a strong one asserted.

---

## 5. What this document is not

It is not a claim that the system works. The evidence for that is the failure ledger — **eighty-two
entries, every one of them the residue of something that went wrong here** — and the fact that
each of the twenty checks was born from a named failure rather than from a design meeting.

> **A governance document written before the failures is a hypothesis. Written after them, and
> citing them, it is a report.** This is the second kind, and where it describes a provision we
> have not yet paid for, it says so.
