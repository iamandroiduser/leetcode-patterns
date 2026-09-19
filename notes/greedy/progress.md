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

## Skills checklist

- [x] Can state what a greedy algorithm is
- [x] Knows greedy can fail (coin counterexample)
- [x] Pattern A: identifies the single running value to track (stock)
- [x] Pattern A: applies it to reachability (Jump Game), with one hint
- [x] Pattern A: applies it to counting steps (Jump Game II), with the layer hint
- [ ] Can state an exchange argument in one sentence without prompting
- [ ] Pattern B: sort-by-end interval sweep
- [ ] Pattern C: heap-driven scheduling
- [ ] Pattern D: deadline + regret heap

## Next session plan

- Learner chose (2026-09-19) to stay on Pattern A until it is interview-ready
  in code, not just in description. Plan is in `pattern-a-drill.md`.
- Drill order: Jump Game II cold in code, Stock II, Partition Labels, Gas
  Station, Video Stitching (stretch).
- Pattern B (Non-overlapping Intervals first) starts once the drill exit
  criteria are met.

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
