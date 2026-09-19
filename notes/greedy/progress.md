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

## Skills checklist

- [x] Can state what a greedy algorithm is
- [x] Knows greedy can fail (coin counterexample)
- [x] Pattern A: identifies the single running value to track (stock)
- [x] Pattern A: applies it to reachability (Jump Game), with one hint
- [x] Pattern A: applies it to counting steps (Jump Game II), with the layer hint
- [ ] Drill: Jump Game II written cold and runnable as pasted (logic passed 2026-09-19 after 4 attempts; mechanics not yet clean)
- [ ] Can state an exchange argument in one sentence without prompting
- [ ] Pattern B: sort-by-end interval sweep
- [ ] Pattern C: heap-driven scheduling
- [ ] Pattern D: deadline + regret heap

## Next session plan

- Learner chose (2026-09-19) to stay on Pattern A until it is interview-ready
  in code, not just in description. Plan is in `pattern-a-drill.md`, revised
  the same day after drill 1 showed the gap is idea-to-code, not the idea.
- Drill 1 logic passed on attempt 4 (2026-09-19). Session ended there.
- Next session opens with a cold rewrite of Jump Game II under the four-step
  protocol (state table, code, self-trace on two inputs, then run).
- Then Stock II, Partition Labels, Gas Station, Video Stitching (stretch),
  each under the same protocol, scored per stage.
- Pattern B starts once the exit criteria in the drill plan are met.

## Where the gap is (learner's own observation, 2026-09-19, confirmed)

Descriptions are usually right; code is not. Three code attempts on Jump
Game II, none passed as submitted. Breakdown by failure class:

| Class | Attempts | Example |
|-------|----------|---------|
| State variable present in the description, dropped in code | 1, 2 | layer boundary missing, counter fired per index / per reach improvement |
| Boundary / off-by-one | 1, 3 | one-element case; loop guard runs one extra layer |
| Name defined one way, used another | 3, 4 | `low` vs `lo`, `num` vs `nums`, then `jmp` vs `jump` |

Attempt 3 is a different kind of wrong from attempts 1 and 2: the algorithm
is fully present and only a boundary is off. That is progress, not noise.

## Recurring themes to watch

- Committing to a specific choice (a landing index) instead of tracking the best over everything seen. Greedy in Pattern A never commits; it keeps a running max. Reappeared once (Jump Game). Revisit in Jump Game II.
- Treating a reach value as a stockpile that accumulates (added fuel instead of taking the max). Jumps do not stack: landing on an index resets your reach to what that index offers, if that is better. Seen once (Jump Game trace).
- Acting at every index instead of only at a boundary. Drill 1 incremented the jump count on every index; the verbal description had the layer boundary, the code did not. Same family as the landing-spot commitment above: greedy in Pattern A acts only when a boundary condition fires. Seen twice now.

## Observations

- 2026-09-19: Interview language is Python (learner wrote drill 1 in Python; no other preference stated).
- 2026-09-19: Learner had a different code shape in mind for Jump Game II
  (explicit loop over each layer's indexes). It is correct and O(n); recorded
  both shapes and the transformation between them in the drill plan.

- 2026-09-19: Preferred plain chat over a narrated read-along page (browser
  voices were poor). Keep lessons in chat, short sections, one question at the
  end of each message.
