# Drill coach — repo side

The interview drill coach runs as a separate chat/voice project. It cannot
reach this repo. It reads three knowledge files that are snapshots of this
folder, and at the end of each session it prints a PREP-LOG JSON block that
gets filed back here.

## Files

| file | who writes it | what it is |
|---|---|---|
| `curriculum.md` | hand-edited here | problem statements, examples, constraints, coach notes, variants, ids |
| `anchors.md` | hand-edited here, his phrases added from logs | trigger line, pattern, invariant, template per problem |
| `status.md` | **generated**, never hand-edited | as-of date, due recalls, next new problem, per-problem status, error tags, slips, open items |
| `log/*.json` | appended by `ingest.py` | raw PREP-LOG blocks, one per session, append-only |
| `ingest.py` | | validates a block, files it, regenerates `status.md` |

## Loop

1. Upload `status.md`, `curriculum.md`, `anchors.md` to the coach project as
   knowledge files.
2. Run a session. At the end the coach prints one fenced `json` block.
3. Paste it into Claude Code and run one of:

   ```
   python3 notes/coach/ingest.py --paste        # then paste, then Ctrl-D
   python3 notes/coach/ingest.py block.json
   ```

   This files the block under `log/` and regenerates `status.md`.
4. Commit. Re-upload `status.md` (and `anchors.md` if a new phrase was
   logged) to the coach project. The coach's view is only as fresh as the
   last upload; it says the as-of date at the start of every session for
   this reason.

`python3 notes/coach/ingest.py --render` regenerates `status.md` without
filing anything, for example after editing a log by hand. `--today YYYY-MM-DD`
overrides the date used for the due calculation.

## Conventions

- Ids are `gr-<sub-pattern><n>` from `curriculum.md`. A problem not in the
  curriculum is keyed `"NEW: <title>"` in the block; add it to the curriculum
  afterwards and re-key the log entry.
- Error tags live in `ERROR_TAGS` in `ingest.py`. The coach reuses them from
  `status.md`; a tag it invents shows up as undefined in the table until it is
  added there.
- Spaced recall: a problem is due 1, 3, 7, 14, 30, 60 days after its 1st,
  2nd, ... distinct exposure day. Full solid needs five exposure days, so
  nothing becomes full solid in one session.
- Exposures from a session with a suspect turn carry `"verified": false`
  and show as `?` in the history column.

## Relationship to `notes/greedy/`

`notes/greedy/` is the narrative record from the chat sessions before the
coach existed: lessons, the drill protocol, and a prose progress log. The
first three blocks in `log/` were seeded from that prose log on 2026-10-02.
From here on, `log/` and `status.md` are the system of record for progress;
`notes/greedy/` keeps the lesson material.
