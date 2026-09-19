# Greedy Algorithms — Study Track

Personal study notes and progress log for the Greedy pattern. Lessons live in
this folder, one file per pattern. `progress.md` is the running record used to
plan the next session and to track improvement over time.

## Curriculum (order we are following)

| # | Pattern | The move | Problems (repo list unless noted) | Status |
|---|---------|----------|-----------------------------------|--------|
| A | Single pass, track one number | Scan once, keep a running "best so far" | Best Time to Buy and Sell Stock, Jump Game, Jump Game II (not in repo list) | In progress |
| B | Sort intervals, then sweep | Sort by end, keep the interval that ends earliest | Non-overlapping Intervals (not in repo list), Min Arrows to Burst Balloons, Employee Free Time | Not started |
| C | Heap, most frequent first | Always spend the item with the largest remaining count | Reorganize String, Task Scheduler, Rearrange String k Distance Apart | Not started |
| D | Sort by deadline, heap for regret | Take everything; when you overshoot, evict the worst earlier choice | Course Schedule III | Not started |

Extra variants to fold in: Gas Station, Partition Labels.

Source for "repo list": `src/data/questions.json` tags 8 problems with the
`Greedy` pattern (ids 31, 43, 80, 81, 83, 110, 111, 112).

## Core idea (one paragraph)

A greedy algorithm builds the answer one step at a time, takes the locally best
choice at each step, and never undoes a choice. It is only correct when you can
argue an **exchange argument**: if an optimal solution made a different choice
at this step, swapping in the greedy choice makes it no worse. If that argument
fails, the problem usually needs dynamic programming.

Counterexample to "always take the biggest": coins {1, 3, 4}, target 6.
Greedy gives 4+1+1 (3 coins); optimal is 3+3 (2 coins).

## Session format

1. Plain-English idea
2. The one-line exchange argument
3. Code
4. One variant the learner attempts first, before seeing the solution
