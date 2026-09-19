# Pattern A — Single pass, track one number

## Idea

Walk the array once, left to right. Keep exactly one summary of everything you
have already seen. At each element, first use the summary to update the answer,
then fold the current element into the summary.

The skill is choosing *which* single number is enough.

## Problem 1: Best Time to Buy and Sell Stock (LC 121, Easy)

Buy once, sell once later, maximize profit.

**Learner's answer (2026-09-19, correct, no hints):** profit 5 by buying at 1 and
selling at 6; track the minimum price seen so far, because that is the day you
would have wanted to buy.

**Exchange argument:** for any sell day, the best buy day is the cheapest day
before it. If an optimal solution bought on a more expensive earlier day, swap
that buy for the minimum-so-far and profit does not drop. So one number, the
running minimum, is enough.

**Code (Python):**

```python
def max_profit(prices):
    min_so_far = float("inf")
    best = 0
    for p in prices:
        best = max(best, p - min_so_far)   # sell today against the cheapest past day
        min_so_far = min(min_so_far, p)    # then let today become a candidate buy day
    return best
```

Order of the two lines matters: update the answer *before* updating the minimum,
otherwise you could "buy and sell on the same day" for profit 0, which is
harmless here but the wrong habit for variants.

Time O(n), space O(1).

Trace on `[7, 1, 5, 3, 6, 4]`:

| price | min_so_far after | best after |
|-------|------------------|------------|
| 7 | 7 | 0 |
| 1 | 1 | 0 |
| 5 | 1 | 4 |
| 3 | 1 | 4 |
| 6 | 1 | 5 |
| 4 | 1 | 5 |

## Problem 2: Jump Game (LC 55, Medium) — next

`nums[i]` is the maximum jump length from index `i`. Start at index 0. Can you
reach the last index?

Examples: `[2,3,1,1,4]` -> true. `[3,2,1,0,4]` -> false.

**Learner's answer (2026-09-19, partially correct, 1 hint):** track "how many
jumps I can still make", measured from the last index landed on; stuck when
standing on a 0 that is not the last index.

**What was right:** remaining reach ("fuel") is a valid single number to track.

**The gap:** "from the last index I was at" commits to a landing spot. Greedy
never commits. Counterexample: `[3,0,2,0,1]`. Jumping as far as possible from
index 0 lands on index 3 (value 0) and fails, yet the answer is true via index 2.

**The fix:** refresh fuel at every index you pass, not only where you land.
Fuel at index i = max(fuel from before minus 1, nums[i]). Stuck when fuel would
go negative before the last index. That always happens while standing on a 0,
so the learner's zero intuition was right, but the test is on fuel, not on the
array value.

**Exchange argument:** whatever landing spots an optimal path uses, the fuel
rule at every index is at least as large as that path's remaining reach, so
the fuel rule never gets stuck when a real path exists.

**Code (Python), fuel version:**

```python
def can_jump(nums):
    fuel = nums[0]
    for i in range(1, len(nums)):
        fuel -= 1                      # one step costs one unit
        if fuel < 0:
            return False               # could not even reach index i
        fuel = max(fuel, nums[i])      # refuel if this index offers more
    return True
```

**Equivalent "farthest index" version** (what most write-ups show):

```python
def can_jump(nums):
    farthest = 0
    for i, n in enumerate(nums):
        if i > farthest:
            return False
        farthest = max(farthest, i + n)
    return True
```

Trace of the fuel rule on `[3,0,2,0,1]`:

| i | nums[i] | fuel after |
|---|---------|------------|
| 0 | 3 | 3 |
| 1 | 0 | 2 |
| 2 | 2 | 2 |
| 3 | 0 | 1 |
| 4 | 1 | 1 (reached) |

Time O(n), space O(1).

## Problem 3: Jump Game II (LC 45, Medium) — after that

Same setup, guaranteed reachable. Return the minimum number of jumps.

### Jump Game II — solution

**Learner's answer (2026-09-19, correct idea, layer framing supplied as a hint):**
start at index 0, find the farthest index reachable with one jump; every index
up to there is the next set of launch points; scan them to find the farthest
reachable with two jumps; repeat until the farthest reaches the last index; the
number of layers is the answer. (One verbal slip: said "equal to or less than the
last index" where "equal to or greater than" was meant; the follow-up sentence
had it right.)

**The two numbers:** `layer_end`, the last index of the current layer, and
`farthest`, the best reach seen from any index in the current layer. When the
scan index reaches `layer_end`, one jump is counted and `layer_end` becomes
`farthest`.

**Why this is the minimum:** the layers are exactly breadth-first search levels
on the "can jump to" graph, and BFS level equals shortest path length. Because
each layer is a contiguous range of indexes, one boundary number is enough to
represent it, which is what makes this O(n) instead of a real BFS with a queue.

**Code (Python):**

```python
def jump(nums):
    jumps = 0
    layer_end = 0      # last index of the current layer
    farthest = 0       # farthest index anyone in this layer can reach
    for i in range(len(nums) - 1):        # never jump FROM the last index
        farthest = max(farthest, i + nums[i])
        if i == layer_end:                # layer finished: a jump must have happened
            jumps += 1
            layer_end = farthest
    return jumps
```

Verified against a brute-force shortest-path solver on 3000 random arrays.

Trace on `[2,3,1,1,4]`:

| i | nums[i] | farthest | layer_end after | jumps |
|---|---------|----------|-----------------|-------|
| 0 | 2 | 2 | 2 | 1 |
| 1 | 3 | 4 | 2 | 1 |
| 2 | 1 | 4 | 4 | 2 |
| 3 | 1 | 4 | 4 | 2 |

Two edge cases the loop bound handles: a one-element array returns 0, and the
scan stops before the last index so it never counts a jump from the end.

## Pattern A summary

- Stock: track the minimum so far.
- Jump Game: track the farthest reach so far (or remaining fuel). Never commit
  to a landing spot. Take the max, do not add.
- Jump Game II: same scan, plus a layer boundary that tells you when a jump
  must have happened.
