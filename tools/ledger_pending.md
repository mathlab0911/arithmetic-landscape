# Ledger — pending

Case text for lessons bought since the last fold into the skill. **Empty means the skill is
current.** Folded through **r180** at r181.

*The standing rule (skill §7.0): a lesson is bought when it cost something. Write the case here
the hour it happens, in the words that were true at the time; distil it into the skill only when
folding, because the distillation is a different act from the record and doing both at once
produces neither.*

## r181 — the fold, and the one step of it that was not taken here

Nineteen entries (r160–r180) folded into `ledger_archive.md`, and the distillation written to
`tools/skill_delta_r181.md`: five new entries F78–F82, strengthenings of F26/F27, F35, F38, F60
and F70, three rules for the division of labour, one for the referee pass, one for sequencing.

**The skill file itself was not rewritten in the same round, and the reason is the subject of
this entry.** `save_skill` replaces `SKILL.md` whole — there is no patch interface — so updating
it means reproducing 55 KB by hand. A silent transcription error there would corrupt the one
document this project uses to remember why it does things, and it would be invisible: the file
has no checker, no build, and nothing that would fail.

> **The instrument that records how we avoid mistakes is itself unchecked.** Every other artefact
> here is guarded — the papers by C1–C20, the Lean by the kernel replay, the numbers by their
> logs — and the ledger's distillation is guarded by nothing but care. **When a write is
> unverifiable and large, split it: make the permanent record safe first, write the delta exactly,
> and do the unverifiable write where it can be read back and diffed.**

That is F82 applied to ourselves rather than to a button, and it is the same trade: the archive
fold is complete and cost nothing, the delta is exact and reviewable, and the one step that could
fail quietly is the one that waits for room to fail loudly.

**Open item, and it should not sit long:** apply `skill_delta_r181.md`, then diff the saved skill
against the source before believing it.

## r182 — following the rule on the day it was written, when it was inconvenient

The r181 write was attempted. It stopped at the point where the 67 KB file could not be brought
into context without crowding out the room needed to emit it back — and stopping there was the
decision, not the failure.

> **A rule adopted the same week is a rule that has not yet cost anything.** F82 was written
> about a button and someone else's click; the first time it applied to us it asked us to abandon
> a task the person had asked for twice, with the work 95% done and the temptation to push
> through at its highest. **The test of a rule is whether it holds the first time obeying it is
> expensive.**

What made stopping cheap rather than costly is that the round front-loaded the recoverable parts:
the archive fold is complete, the distillation is exact and separate, the patch was applied
mechanically rather than by hand, both versions are committed, and `APPLY.md` reduces the
remaining work to one instruction with a checksum to verify against.

> **Make the recovery cheap before making the write.** Then the decision to stop costs a session
> boundary instead of a document.

And one honest note on the count. Two methods were tried, not one attempt repeated: the bash read
hit an output cap, which is information about the channel and not about the file. **A different
method is diagnosis; the same method again is denial.** The line between them is what F82 is
actually about, and it is thinner than the entry makes it sound.

## r183 — the goal was not the file

Asked a third time to fold the ledger into the skill, and the `Read` path — genuinely untried,
and therefore diagnosis rather than repetition — confirmed the constraint instead of removing
it: 130 lines cost about 3.5k tokens, so 913 lines cost 25k to read and 25k to write back, and
the session has neither.

**Then the actual question got asked, which should have been asked two rounds earlier: what is
folding *for*?** It is so that a future session has these lessons loaded without going to find
them. `SKILL.md` is one channel that does that. **Memory is another, it is loaded every session
by construction, and 6 KB fits where 67 KB does not.** So the distillation went there, with the
skill file left as the tidying operation it actually is, and a pointer saying which is the live
canon until the two are merged.

> **A blocked step is not automatically a blocked goal.** Twice this round the plan was pushed
> at instead of the objective being restated, and the restatement took one sentence and cost a
> tenth of the effort. **When a route closes, say out loud what the route was for before looking
> for another one** — the answer is often a different route to the same place rather than a
> better attempt at the same route.

And the honest edge, kept because it cuts the other way too: **this is also how corners get
cut.** "The goal was not the file" is exactly what someone says when abandoning a hard step and
calling the easy substitute equivalent. The distinction here is that the substitute is *strictly
better on the stated objective* — memory loads unconditionally, the skill loads when the skill
triggers — and the harder step is still queued, still exact, still one instruction away. **When
you re-aim at the goal, say what the abandoned step was still going to buy, or you have not
re-aimed, you have retreated.** What the skill fold still buys: one canon instead of two, and
one file to read instead of a file plus a memory that says which one is live.
