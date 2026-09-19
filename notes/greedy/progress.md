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

## Skills checklist

- [x] Can state what a greedy algorithm is
- [x] Knows greedy can fail (coin counterexample)
- [x] Pattern A: identifies the single running value to track (stock)
- [x] Pattern A: applies it to reachability (Jump Game), with one hint
- [ ] Pattern A: applies it to counting steps (Jump Game II)
- [ ] Can state an exchange argument in one sentence without prompting
- [ ] Pattern B: sort-by-end interval sweep
- [ ] Pattern C: heap-driven scheduling
- [ ] Pattern D: deadline + regret heap

## Next session plan

- Jump Game II (LC 45): in progress, learner proposes the extra tracked value first.
- Then close out Pattern A and move to Pattern B.

## Recurring themes to watch

- Committing to a specific choice (a landing index) instead of tracking the best over everything seen. Greedy in Pattern A never commits; it keeps a running max. Reappeared once (Jump Game). Revisit in Jump Game II.
- Treating a reach value as a stockpile that accumulates (added fuel instead of taking the max). Jumps do not stack: landing on an index resets your reach to what that index offers, if that is better. Seen once (Jump Game trace).

## Observations

- 2026-09-19: Preferred plain chat over a narrated read-along page (browser
  voices were poor). Keep lessons in chat, short sections, one question at the
  end of each message.
