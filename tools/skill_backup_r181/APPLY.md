# How to finish the r181 fold — one step, from a fresh session

**Do this first, before anything else in the session.** It needs room to read ~67 KB and emit
~67 KB, and nothing else should be competing for that room.

1. `Read` (or `cat`) `tools/skill_backup_r181/SKILL_after_r181.md`.
2. Call `save_skill` with `name: "pnp-research"`, `overwrite: true`, the description **exactly**
   as it appears in that file's YAML front matter, and `content` = the file's body.
3. **Verify before believing it.** Re-read the skill's cached `SKILL.md` and diff it against
   `SKILL_after_r181.md`. Expected: **67240 bytes, 913 lines,
   md5 `2b35e1bdd08c669892224eb1917e6846`**, and `F01` through `F82` all present
   (`grep -o '\*\*F[0-9][0-9]\*\*' | sort -u | wc -l` = 82).
4. If the diff is not empty, re-save from `SKILL_after_r181.md`. If it is empty, delete nothing:
   leave this directory as the record of how the write was made safe.

## Why it was not done in the round that prepared it

The attempt was made and stopped at the point where the file could not be brought into context
without crowding out the room needed to write it back. **That is the condition F82 describes**,
and the rule was written the same day: *the second identical attempt is diagnosis, the fourth is
denial; when a write is unverifiable and large, split it.*

So the round did the parts that cannot fail quietly — the archive fold, the exact distillation
in `tools/skill_delta_r181.md`, the mechanical patch, and both versions committed here — and
left the single atomic write for a session with room to read it back and diff it.

**Nothing is lost and nothing needs re-deriving.** The intended result already exists as a file;
this step only moves it into the skill store.
