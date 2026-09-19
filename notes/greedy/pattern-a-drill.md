# Pattern A — Interview Drill Plan

Goal: write Pattern A solutions from a blank editor, correctly, with a hand
trace, in interview time. Descriptions are done; this is about code.

## Exit criteria (when we move on)

- Writes Jump Game II from scratch, no hints, in under 10 minutes, with a
  correct trace on one example.
- Writes two variants never seen before (from the list below) with at most one
  hint each.
- Can say the exchange argument for each in one sentence.

## The description-to-code bridge (use this every time)

Every Pattern A solution answers five questions. Write the answers as comments
first, then fill in code under each.

1. **State.** What is the one (or two) running value(s)? Give it a name and an
   initial value. Ask: what is it before I have seen anything?
2. **Loop.** `for i, x in enumerate(arr):` Decide the bounds. Do I need the
   last element? (Jump Game II: no, you never jump from the end.)
3. **Order inside the loop.** Two lines: "use the state to update the answer"
   and "fold x into the state". Which comes first? Rule: if the answer at
   position i must not include x itself, update the answer first (Stock). If it
   may include x, fold x in first (Jump Game's farthest).
4. **Stop or fail condition.** Where does the loop bail out? (Jump Game: when
   i is beyond reach.)
5. **Edge cases.** Empty input, one element, all-equal values. Run the loop in
   your head on a one-element input before anything else.

Then trace on the smallest non-trivial example, writing the state after every
iteration in a small table. Do this even when confident; both slips so far
(add-vs-max, committing to a landing spot) would have shown up in a trace.

## Two correct shapes for Jump Game II

Both are O(n). The explicit-layer shape is the one the learner reached for; the
single-scan shape is its compression. Either is acceptable in an interview.
Verified equal on 5000 random arrays.

**Shape 1: explicit layers (matches the verbal description).**

```python
def jump(nums):
    n = len(nums)
    if n == 1:
        return 0
    jumps = 0
    lo, hi = 0, 0                     # current layer is indexes lo..hi
    while hi < n - 1:                 # last index not yet in a layer
        farthest = 0
        for i in range(lo, hi + 1):   # every launch point in this layer
            farthest = max(farthest, i + nums[i])
        jumps += 1
        lo, hi = hi + 1, farthest     # next layer
    return jumps
```

**Shape 2: single scan (same thing, layers tracked by one boundary).**

```python
def jump(nums):
    jumps = 0
    layer_end = 0
    farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == layer_end:
            jumps += 1
            layer_end = farthest
    return jumps
```

How Shape 1 becomes Shape 2: the inner loop visits indexes lo..hi in order and
the outer loop moves lo to hi+1, so across the whole run every index is visited
exactly once, in order. Replace the two loops with one loop over i and keep
only `hi` (renamed `layer_end`). The moment `i == hi` is the moment the inner
loop would have finished.

## Variants, in the order we will do them

| # | Problem | Difficulty | Running value | Why it is here | Verified |
|---|---------|------------|---------------|----------------|----------|
| 1 | Jump Game II, written cold | Medium | farthest + layer boundary | Retention check, code not description | yes |
| 2 | Best Time to Buy and Sell Stock II (LC 122) | Medium | none beyond previous price | Multiple buys/sells; answer is the sum of positive day-to-day gains. Exchange argument: any transaction spanning several days equals the sum of its daily steps, and dropping the negative steps never hurts. | vs DP on 3000 random inputs |
| 3 | Partition Labels (LC 763) | Medium | farthest last-occurrence + cut point | Jump Game II in disguise: cut when i reaches the farthest boundary. Tests whether the layer idea transfers. | example gives [9,7,8] |
| 4 | Gas Station (LC 134) | Medium | running tank + candidate start | Adds "reset the start" to the scan. Exchange argument: if the tank goes negative at i starting from s, no start in s..i can work either, so skip to i+1. | vs brute force on 3000 inputs |
| 5 | Video Stitching (LC 1024) | Medium | farthest per start point + layer boundary | Jump Game II on intervals; requires a preprocessing step first. Stretch goal. | example gives 3 |

Notes on tagging, for honesty: LeetCode tags Jump Game as both Dynamic
Programming and Greedy, and this repo's data does too (id 43). Maximum Subarray
(Kadane) has the same single-pass shape but is usually taught as DP, so it is
left out of this list to avoid muddying the label.

## Language

Code in these notes is Python for brevity. The repo's own solutions branch is
Java. Drill in whichever language the interviews will be in; the five bridge
questions are language-independent.
