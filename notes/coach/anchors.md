# Anchors — Greedy

One card per problem. For a **recall**, the coach says only the **Trigger**
line; the learner produces pattern, invariant and template from memory inside
90 seconds. Nothing else on the card is shown or paraphrased first.

**His phrase** is the learner's own sentence, verbatim from a session. Cards
without one have not yet been anchored in his words.

---

## gr-a1 · Best Time to Buy and Sell Stock
- **Trigger.** One buy, one later sell, maximize the difference.
- **Pattern.** A: single pass, one running value.
- **Invariant.** After day i, `best` is the best profit selling on or before i,
  and `min_so_far` is the cheapest day on or before i. Answer first, then min.
- **Template.** `min_so_far = inf; best = 0; for p: best = max(best, p - min_so_far); min_so_far = min(min_so_far, p)`
- **His phrase (2026-09-19).** "the lowest number that I've seen so far because
  that would be the time when I should have bought"

## gr-a2 · Jump Game
- **Trigger.** Each value is a maximum forward jump; can you reach the end.
- **Pattern.** A: single pass, running farthest reach (or remaining fuel).
- **Invariant.** Before index i, `farthest` is the largest index reachable from
  indexes before i. Stuck iff `i > farthest`. Update by max, never by sum.
- **Template.** `far = 0; for i: if i > far: return False; far = max(far, i + nums[i]); return True`
- **His phrase (2026-09-19, session 2).** "at the current idx, i can either take
  its value as fuel and keep moving or keep moving with what i already have,
  the way to decide is which one is greater"

## gr-a3 · Jump Game II
- **Trigger.** Same jumps, guaranteed reachable, fewest jumps.
- **Pattern.** A with a layer boundary (BFS levels on a line).
- **Invariant.** Every index up to `layer_end` needs `jumps` jumps. Count a
  jump only when `i == layer_end`; then `layer_end = farthest`.
- **Template.** `for i in range(n - 1): far = max(far, i + nums[i]); if i == layer_end: jumps += 1; layer_end = far`
- **His phrase (2026-09-19).** "if my idx reached the last possible one that i
  could have done in the current jumping capacity, then I need 1 more jump"

## gr-a4 · Best Time to Buy and Sell Stock II
- **Trigger.** Unlimited trades, one share at a time, maximize total.
- **Pattern.** A: sum of positive daily steps.
- **Invariant.** Any multi-day trade equals the sum of its daily steps;
  keeping only positive steps is optimal. Last pair is `(n-2, n-1)`.
- **Template.** `sum(max(0, p[i+1] - p[i]) for i in range(n - 1))`
- **His phrase.** none yet.

## gr-a5 · Partition Labels
- **Trigger.** Cut a string into the most parts with each letter in one part.
- **Pattern.** A with a precomputed last-occurrence; cut when i reaches the
  running farthest.
- **Invariant.** `far` is the farthest last-index among letters seen in the
  current part; the part is closed exactly when `i == far`; next start is
  `i + 1`.
- **Template.** `last = {c: i}; for i, c: far = max(far, last[c]); if i == far: out.append(i - start + 1); start = i + 1`
- **His phrase (2026-09-20).** "the number that matters is the last index where
  we see the instance of the letter in the array, as we partition at that idx,
  including idx"

## gr-a6 · Gas Station
- **Trigger.** Circular route, gas minus cost per stop, find the one valid start.
- **Pattern.** A with a reset, after a global feasibility check.
- **Invariant.** If total gas < total cost, -1. Otherwise the start after the
  last point where the running tank went negative is the answer; every start
  before it was ruled out by arriving with tank >= 0.
- **Template.** `if sum(gas) < sum(cost): return -1; tank = 0; start = 0; for i: tank += gas[i] - cost[i]; if tank < 0: start = i + 1; tank = 0; return start`
- **His phrase.** none yet (drill in progress 2026-09-22).

## gr-a7 · Video Stitching
- **Trigger.** Cover `[0, T]` with the fewest intervals.
- **Pattern.** gr-a3 after bucketing by start.
- **Invariant.** Same as gr-a3 over time points; -1 when a layer ends without
  the reach advancing.
- **Template.** `far[t] = max end of clips starting at t; then the gr-a3 scan over t in range(T)`
- **His phrase.** none yet.

## gr-b1 · Non-overlapping Intervals
- **Trigger.** Fewest removals so no two intervals overlap.
- **Pattern.** B: sort by end, keep greedily.
- **Invariant.** The kept set is a maximum compatible set of the prefix; the
  earliest-ending compatible interval is always safe to keep.
- **Template.** `sort by end; end = -inf; for s, e: if s >= end: keep += 1; end = e; return n - keep`
- **His phrase.** none yet.

## gr-b2 · Minimum Number of Arrows to Burst Balloons
- **Trigger.** Fewest vertical lines hitting every interval.
- **Pattern.** B: sort by end, shoot at ends.
- **Invariant.** An arrow at the earliest end hits every interval that
  overlaps it; touching counts.
- **Template.** `sort by end; x = -inf; for s, e: if s > x: arrows += 1; x = e`
- **His phrase.** none yet.

## gr-b3 · Employee Free Time
- **Trigger.** Gaps common to all of several sorted interval lists.
- **Pattern.** B on the merged stream.
- **Invariant.** With intervals in start order and a running `end`, a gap
  exists exactly when the next start exceeds `end`.
- **Template.** `flatten, sort by start; end = first.end; for s, e: if s > end: out.append([end, s]); end = max(end, e)`
- **His phrase.** none yet.

## gr-c1 · Reorganize String
- **Trigger.** Rearrange so no two adjacent characters match.
- **Pattern.** C: max-heap by count, serve the most constrained first.
- **Invariant.** Feasible iff `max_count <= (n + 1) // 2`; after each
  placement the remaining multiset is still feasible.
- **Template.** `heap of (-count, ch); pop best != prev; append; push prev back; prev = popped`
- **His phrase.** none yet.

## gr-c2 · Task Scheduler
- **Trigger.** Identical tasks need a cooldown; minimize total time with idles.
- **Pattern.** C, or the closed form.
- **Invariant.** The most frequent task fixes the frame
  `(max_count - 1) * (n + 1) + ties`; the answer is that or `len(tasks)`,
  whichever is larger.
- **Template.** `counts; m = max; ties = count of m; return max(len(tasks), (m - 1) * (n + 1) + ties)`
- **His phrase.** none yet.

## gr-c3 · Rearrange String k Distance Apart
- **Trigger.** Identical characters at least k apart.
- **Pattern.** C with a FIFO cooldown queue of length k.
- **Invariant.** A placed letter is unavailable for the next k - 1 placements;
  an empty heap with characters remaining means impossible.
- **Template.** `heap by count; queue; each step: pop, place, enqueue; if len(queue) == k: re-push front if count > 0`
- **His phrase.** none yet.

## gr-d1 · Course Schedule III
- **Trigger.** Durations and deadlines, maximize the count taken.
- **Pattern.** D: sort by deadline, regret heap of durations.
- **Invariant.** After each prefix, the heap holds the most courses that fit,
  with the smallest total time among such sets.
- **Template.** `sort by deadline; time = 0; heap; for d, last: time += d; push d; if time > last: time -= pop_max()`
- **His phrase.** none yet.
