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

- Jump Game II (LC 45): variant, counts minimum jumps.
- Then close out Pattern A and move to Pattern B.

## Recurring themes to watch

- Committing to a specific choice (a landing index) instead of tracking the best over everything seen. Greedy in Pattern A never commits; it keeps a running max. Reappeared once (Jump Game). Revisit in Jump Game II.

## Observations

- 2026-09-19: Preferred plain chat over a narrated read-along page (browser
  voices were poor). Keep lessons in chat, short sections, one question at the
  end of each message.
