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

Question for the learner before the solution: which single number do you track
while scanning left to right, and what condition means "stuck"?

## Problem 3: Jump Game II (LC 45, Medium) — after that

Same setup, guaranteed reachable. Return the minimum number of jumps.
