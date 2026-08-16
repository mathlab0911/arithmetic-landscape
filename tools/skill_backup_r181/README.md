# Skill backup, r181

`save_skill` replaces `SKILL.md` whole and there is no patch interface, so applying the r181
distillation meant emitting the entire file by hand. **A truncated or mistyped emission would
corrupt the one document that records why this project does what it does, and it would be
invisible — that file has no checker, no build, and nothing that would fail.**

So both versions are committed here before the write, and the recovery is one step:

- `SKILL_before_r181.md` — the skill as it stood at the end of r180 (F01–F77).
- `SKILL_after_r181.md` — the intended result (F01–**F82**), produced mechanically from the
  former by the patch script recorded in `tools/skill_delta_r181.md`, not by hand.

**If the saved skill does not match `SKILL_after_r181.md`, re-save from this file.** Verify by
diffing the skill's cached `SKILL.md` against it; the expected size is 67240 bytes, 913 lines,
md5 `2b35e1bdd08c669892224eb1917e6846`.

*This directory is the answer to F82 applied to ourselves: when a write is unverifiable and
large, make the recovery cheap before making the write.*
