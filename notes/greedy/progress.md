# Progress Log

How to read this: one row per problem attempt. "Hints" is how many nudges were
needed before the correct idea. "Self-solved" means the key insight came from
the learner, not from the lesson. The goal over time is more self-solved rows,
fewer hints, and harder problems.

## Attempts

| Date | Problem | Difficulty | Pattern | Result | Hints | Self-solved | Notes |
|------|---------|------------|---------|--------|-------|-------------|-------|
| 2026-09-19 | Best Time to Buy and Sell Stock (LC 121) | Easy | A | Correct | 0 | Yes | Gave max profit 5 (buy 1, sell 6) and identified "min price so far" as the one number to track, with the right reason ("that would be the time when I should have bought"). Answered before seeing any code. |
| 2026-09-19 | Jump Game (LC 55) | Medium | A | Partially correct | 1 | Partly | Tracked "jumps I can still make" (remaining fuel), which is a valid quantity. Gap: measured fuel from "the last index I was at", i.e. committed to a landing spot. Counterexample [3,0,2,0,1]: jumping farthest lands on a 0 and fails, but the answer is true. Fix: refresh fuel at every index passed, never commit. Stuck condition stated as "array value is 0 here"; refined to "fuel is 0 here". |
| 2026-09-19 | Jump Game trace on [3,0,2,0,1] | Medium | A | Right conclusion, wrong rule | 1 | Partly | Applied fuel = fuel - 1 + nums[i] (addition) at index 2 instead of max(fuel - 1, nums[i]). Reached the correct true/false answer by luck of the input. Falsified with [2,1,0,0]: addition says true, truth is false. |
| 2026-09-19 | Jump Game trace on [2,1,0,0] | Medium | A | Correct | 0 | Yes | Fuel 2, 1, 0, then negative at index 3. Applied the max rule correctly and stated the stuck condition in terms of fuel. |
| 2026-09-19 | Jump Game II (LC 45) | Medium | A | Correct | 1 | Yes | Given the layer framing as a hint, derived the algorithm: farthest reach per layer, count layers until the last index is covered. Did not name the two variables explicitly but described exactly what they do. |
| 2026-09-19 | Drill 1: Jump Game II written cold (Python) | Medium | A | Incorrect | 0 so far | No | Passed both textbook examples, failed 2962 of 5000 random arrays. Bug 1: one-element input returns 1, should be 0. Bug 2: `jump += 1` on every index, so it counts indexes visited, not layers; the layer boundary variable from the verbal description was dropped in code. Failing input [3,1,1,1,4]: returned 4, answer 2. Good parts: farthest-reach update is correct (max, not add), and the early return when farthest covers the end is a valid optimization. Learner asked to fix it themselves. |
| 2026-09-19 | Drill 1, attempt 2: Jump Game II | Medium | A | Incorrect | 1 | No | Fixed the one-element case. Changed the increment to fire whenever the farthest reach improves. Still no layer boundary: reach can improve several times inside one layer. Failing input [2,3,4,1,1,1]: returned 3, answer 2. Wrong on a large share of random arrays. Hint given: the layer end must be stored separately from the farthest reach, because reach changes while you are still inside the layer. |
| 2026-09-19 | Drill 1, attempt 3: Jump Game II, explicit-layer shape | Medium | A | Structurally correct, one off-by-one | 1 | Mostly | Algorithm is now right: layer lo..hi, inner loop finds new_hi, one jump per layer. Two name typos (`low` vs `lo`, `num` vs `nums`) mean it does not run as written. One logic bug: loop guard `hi < sz` should stop when hi already covers the last index, so it runs one extra layer. Trace on [2,3,1,1,4] gives 3, answer 2. One-element input gives 1 for the same reason. Changing the guard by one makes it pass 5000 random arrays. Different failure class from attempts 1 and 2: those were missing a concept in code; this is a boundary. |
| 2026-09-19 | Drill 1, attempt 4: Jump Game II, explicit-layer shape | Medium | A | Logic correct; not runnable as pasted | 0 | Yes | Loop guard fixed to `hi < sz - 1`. With names made consistent, passes 5000 random arrays and the one-element case. Mechanical issues: missing closing parenthesis on the max line (SyntaxError), counter initialised as `jmp` but incremented and returned as `jump` (NameError), one line indented differently (possibly a paste artifact). Naming mismatch between definition and use is now 2 of 4 attempts. |
| 2026-09-19 | Jump Game (LC 55) written in code, unprompted | Medium | A | Incorrect | 0 | No | Wrote the fuel rule with `fuel += nums[i]` instead of `fuel = max(fuel, nums[i])`. This is the same add-vs-max slip corrected in the hand trace earlier today, now reappearing in code. Fails [2,1,0,0] (says True, truth False). Also declared an unused `jump` variable. |
| 2026-09-19 (session 2) | Jump Game (LC 55), cold, under protocol | Medium | A | Correct | 0 | Yes | Step 1 state table took two rounds (change-event column first said when, not what; meaning sentence still says "previously picked idx" though the formula and the stated reason for max are right). Step 2 code correct as pasted: names consistent, check placed between decrement and max, one-element handled. Passes 10000 random arrays vs brute force. Step 3 (self-trace) was skipped; traces requested after the fact. First Pattern A code that ran correctly on first paste. |
| 2026-09-19 (session 2) | Jump Game II (LC 45), cold, under protocol, single-scan shape | Medium | A | Correct | 0 | Yes | Step 1 took two rounds: first table put the jump condition on the farthest-reach variable and defined the layer end as a per-index value (failure class 1, caught in the table, not in code). Second table correct; learner's own trace of it found the extra-jump boundary at the last index (class 2, caught before code) and chose an early exit plus a one-element guard. Code correct as pasted, names consistent, passes 10000 random arrays vs brute force. Step 3 half-done: traced the textbook example during the table phase, reasoned about [0] in words, did not trace [1,1,1,1]. |
| 2026-09-20 (session 2) | Best Time to Buy and Sell Stock II (LC 122), unseen variant | Medium | A | Incorrect, boundary | 1 | Mostly | Algorithm right on first try (sum of positive daily steps) with the exchange argument supplied by the coach. Exit row was requested and skipped. Loop bound `range(sz - 2)` misses the last pair: [1,2] returns 0, [1,2,3,4,5] returns 3. Passed all three requested traces by luck (the last step in each is not a gain). Notable: the hand trace had 5 rows for a loop that visits 4 indexes, so the trace was of the intended algorithm, not the code as written. |
| 2026-09-20 (session 2) | Stock II, fix | Medium | A | Correct | 1 total | Yes | Bound fixed to `range(sz - 1)`; passes 10000 random arrays vs DP. But the two accompanying traces were wrong: every gain written as 0 on [1,2] (answer 1) and [1,2,3,4,5] (answer 4). The i columns now match the loop. The trace's final value disagreed with the known expected output and this was not flagged. |
| 2026-09-20 (session 2) | Partition Labels (LC 763), unseen variant, attempt 1 | Medium | A | Incorrect | 1 | Partly | Key insight correct (last occurrence of each letter decides the extent). State table effectively skipped: one row with a prose change column, no precomputation row, no row for the running farthest or the part start. Code: crashes with TypeError because `for c, i in enumerate(...)` swaps index and char; with that fixed, the cut condition compares i against a pre-set boundary copied from Jump Game II, so after the first part the boundary never moves (part_ids [0, 8], then nothing). Also `part_len` vs `part_lens` (name class, third time), the length-conversion loop bound is `sz - 1` instead of the number of parts, and the end-of-string append sits inside the loop and would fire repeatedly. Hint given: the cut fires when i reaches the running farthest itself, unlike Jump Game II. |
| 2026-09-20 (session 2) | Partition Labels, attempt 2 | Medium | A | Incorrect | 1 (no new hint) | Partly | Cut condition now correct (i equals the running farthest). Table and traces skipped again despite an explicit request. Three name mismatches in 16 lines: `char_end` vs `char_ends`, `part_strat` vs `part_start`, `max_part_id` initialised but `last_part_id` used (NameError as pasted). With names made consistent, one boundary bug: the next part's start is set to i instead of i + 1, so every part after the first is one too long: [9, 8, 9] instead of [9, 7, 8], and "ab" gives [1, 2]. Coach now requires table and traces before running further pastes. |
| 2026-09-20 (session 2) | Partition Labels, attempt 3 | Medium | A | Logic correct; not runnable as pasted | 1 total | Yes | Full table provided (one row's formula still says the old `= max_part_end` while the code correctly says `i + 1`). Boundary fixed. With names made consistent, passes 10000 random strings. As pasted: NameError, and the two broken names are the same two as attempt 2, unchanged: `char_end` read where `char_ends` is defined, and `last_part_end` read where `max_part_end` is defined. The table itself has the right names, so the code deviated from the table. Traces skipped a third time. |
| 2026-09-20 (session 2) | Partition Labels, attempt 4 | Medium | A | Correct, runnable | 1 total | Yes | All names consistent; passes 10000 random strings. Needs `from collections import defaultdict` in a fresh file (a plain dict would avoid it). The name-audit lists were not pasted. The corrected table row still says `part_start_id = i` where the code says `i + 1`, so the table and code still disagree on the exact line that was the attempt-2 bug. Trace on "ab" correct in values, abbreviated to two columns, no match/mismatch word. |

## Skills checklist

- [x] Can state what a greedy algorithm is
- [x] Knows greedy can fail (coin counterexample)
- [x] Pattern A: identifies the single running value to track (stock)
- [x] Pattern A: applies it to reachability (Jump Game), with one hint
- [x] Pattern A: applies it to counting steps (Jump Game II), with the layer hint
- [x] Drill: Jump Game II written cold and runnable as pasted (session 2, first paste under the protocol; session 1 took 4 attempts)
- [x] Pattern A variant: Stock II (1 hint, 2 attempts)
- [x] Pattern A variant: Partition Labels (1 hint, 4 attempts, runnable on the 4th)
- [ ] Can state an exchange argument in one sentence without prompting
- [ ] Pattern B: sort-by-end interval sweep
- [ ] Pattern C: heap-driven scheduling
- [ ] Pattern D: deadline + regret heap

## Next session plan

- Learner chose (2026-09-19) to stay on Pattern A until it is interview-ready
  in code, not just in description. Plan is in `pattern-a-drill.md`, revised
  the same day after drill 1 showed the gap is idea-to-code, not the idea.
- Drill 1 logic passed on attempt 4 (2026-09-19). Learner then wrote Jump Game in code and the add-vs-max slip returned.
- Session 2 (2026-09-19): Jump Game and Jump Game II both passed cold on first paste under the protocol. Time per drill not measured; exit criterion 1 counted as met on correctness, timing to be checked once.
- Exit criterion 2 (two unseen variants, at most one hint each): Stock II done with 1 hint, Partition Labels logic done with 1 hint (2026-09-20). Partition Labels runnable on attempt 4. Both variant criteria now met, with the caveat that the mechanics took 6 attempts across the two.
- Decision (coach, 2026-09-20): one last Pattern A item, Gas Station, self-timed, full protocol. Then Pattern B regardless of result; the residual gap (names, skipped traces) is practiced on any problem, so more Pattern A variants do not target it.
- Then Stock II, Partition Labels, Gas Station, Video Stitching (stretch),
  each under the same protocol, scored per stage.
- Pattern B starts once the exit criteria in the drill plan are met.

## Where the gap is (learner's own observation, 2026-09-19, confirmed)

Descriptions are usually right; code is not. Three code attempts on Jump
Game II, none passed as submitted. Breakdown by failure class:

| Class | Attempts | Example |
|-------|----------|---------|
| State variable present in the description, dropped in code | 1, 2 | layer boundary missing, counter fired per index / per reach improvement |
| Boundary / off-by-one | 1, 3, Stock II | one-element case; loop guard runs one extra layer; loop bound one short |
| Name defined one way, used another | 3, 4, Partition Labels | `low` vs `lo`, `num` vs `nums`, `jmp` vs `jump`, `part_len` vs `part_lens`; also `for c, i in enumerate` with roles swapped |

Attempt 3 is a different kind of wrong from attempts 1 and 2: the algorithm
is fully present and only a boundary is off. That is progress, not noise.

## Protocol observations

- 2026-09-20: Name mismatches are now the dominant failure. Partition Labels attempts 2 and 3 broke the same two names. Step 2b added to the protocol: a name audit (list every name assigned, list every name read, diff them) before step 3.
- 2026-09-20: Step 3 traces skipped on three consecutive pastes. Next drill uses a two-character input for the trace so it costs under a minute.

- 2026-09-20: Partition Labels attempt 1 skipped the state table (one vague row) and the code had five distinct problems. The two cold passes earlier the same day both had full tables. Strongest evidence yet that the table is load-bearing, not ceremony.

- 2026-09-20: A self-trace only catches bugs if it traces the code as
  written. On Stock II the trace had one more row than the loop visits. Rule
  added: in step 3, write the list of i values the loop actually visits
  before tracing, straight from the range expression.
- 2026-09-20: On the Stock II fix, the i columns were right but every gain
  value was 0 on inputs whose answers are 1 and 4. A trace whose last row
  does not equal the expected output is a red flag in itself. Rule added:
  step 3 ends by comparing the trace's final value with the expected output
  and saying "match" or "mismatch".

## Recurring themes to watch

- Committing to a specific choice (a landing index) instead of tracking the best over everything seen. Greedy in Pattern A never commits; it keeps a running max. Reappeared once (Jump Game). Revisit in Jump Game II.
- Treating a reach value as a stockpile that accumulates (added fuel instead of taking the max). Jumps do not stack: landing on an index resets your reach to what that index offers, if that is better. Seen twice: the Jump Game hand trace, and again in code the same day after being corrected. This one is not yet fixed by correction alone; it needs the state-table step ("fuel is a reach, not a stockpile" written down before code).
- Acting at every index instead of only at a boundary. Drill 1 incremented the jump count on every index; the verbal description had the layer boundary, the code did not. Same family as the landing-spot commitment above: greedy in Pattern A acts only when a boundary condition fires. Seen twice now.

## Observations

- 2026-09-19: Interview language is Python (learner wrote drill 1 in Python; no other preference stated).
- 2026-09-19: Learner had a different code shape in mind for Jump Game II
  (explicit loop over each layer's indexes). It is correct and O(n); recorded
  both shapes and the transformation between them in the drill plan.

- 2026-09-19: Preferred plain chat over a narrated read-along page (browser
  voices were poor). Keep lessons in chat, short sections, one question at the
  end of each message.
