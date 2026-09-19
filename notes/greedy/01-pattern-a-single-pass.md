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
