# Curriculum — Greedy

Problem statements for the drill coach. The coach reads the **Statement**,
**Examples** and **Constraints** verbatim. The **Coach note** is the Beat 2
answer: never say it, or the pattern name, before the learner names the
pattern himself. Statements are precise paraphrases, not LeetCode's text.

Ids: `gr-<sub-pattern><n>`. Order within a sub-pattern is the intended
teaching order. Close variants are marked so they can be spaced apart.

Sub-patterns:
- **A** Single pass, one running value
- **B** Sort intervals by end, sweep
- **C** Heap, most frequent first
- **D** Sort by deadline, regret heap

---

## gr-a1 · Best Time to Buy and Sell Stock (LC 121, Easy)

**Statement.** You are given an array `prices` where `prices[i]` is the price
of one share on day `i`. Choose one day to buy one share and a later day to
sell it. Return the maximum profit. If no profit is possible, return 0.

**Examples.**
- `prices = [7,1,5,3,6,4]` → `5` (buy day 1 at 1, sell day 4 at 6)
- `prices = [7,6,4,3,1]` → `0`

**Constraints.** `1 <= len(prices) <= 1e5`, `0 <= prices[i] <= 1e4`. Exactly
one buy and one sell; the sell must come after the buy.

**Coach note (Beat 2 answer).** Pattern A. One running value: the minimum
price seen so far. Invariant: after processing day i, `best` is the best
profit using a sell day `<= i`, and `min_so_far` is the cheapest buy day
`<= i`. Order: update `best` before `min_so_far`. O(n) time, O(1) space.
Close variants: gr-a4.

**Variants (Beat 6).**
1. Unlimited trades, one share at a time → sum of positive daily steps (gr-a4).
2. Same, with a transaction fee → one scan but two running states (holding /
   not holding); the single-min trick no longer suffices.
3. At most k transactions → pattern breaks; needs DP over (day, trades left,
   holding).

---

## gr-a2 · Jump Game (LC 55, Medium)

**Statement.** You are given an integer array `nums`. You start at index 0.
`nums[i]` is the maximum number of indexes you may jump forward from index `i`.
Return `true` if you can reach the last index, otherwise `false`.

**Examples.**
- `nums = [2,3,1,1,4]` → `true`
- `nums = [3,2,1,0,4]` → `false`

**Constraints.** `1 <= len(nums) <= 1e4`, `0 <= nums[i] <= 1e5`.

**Coach note.** Pattern A. One running value: farthest index reachable so
far (equivalently remaining "fuel"). Invariant: before processing index i,
`farthest` is the largest index reachable using only indexes `< i`; if
`i > farthest` the answer is false. Update is a max, never a sum: landing
somewhere resets reach to what that index offers, it does not add. O(n), O(1).
Close variants: gr-a3, gr-a5, gr-a7.

**Variants.**
1. Minimum number of jumps → same scan plus a layer boundary (gr-a3).
2. Reach is given as intervals instead of per-index lengths → bucket by start,
   then the same scan (gr-a7).
3. Jumps allowed both left and right by `nums[i]` → reachable set is no longer
   a prefix, the running max breaks; needs BFS/DFS.

---

## gr-a3 · Jump Game II (LC 45, Medium)

**Statement.** Same setup as gr-a2: `nums[i]` is the maximum forward jump from
index `i`, and you start at index 0. It is guaranteed that the last index is
reachable. Return the minimum number of jumps needed to reach it.

**Examples.**
- `nums = [2,3,1,1,4]` → `2`
- `nums = [2,3,0,1,4]` → `2`
- `nums = [0]` → `0`

**Constraints.** `1 <= len(nums) <= 1e4`, `0 <= nums[i] <= 1000`.

**Coach note.** Pattern A with a layer boundary. Two running values:
`farthest` (as in gr-a2) and `layer_end`, the last index reachable with the
jumps counted so far. Invariant: every index in `[previous layer_end + 1,
layer_end]` needs exactly `jumps` jumps. A jump is counted only when
`i == layer_end`; `layer_end` then becomes `farthest`. These are BFS levels;
contiguity is what makes one boundary enough. Loop must not count a jump from
the last index. O(n), O(1). Close variants: gr-a2, gr-a5, gr-a7.

**Variants.**
1. Reach given as intervals → gr-a7.
2. Partition a string so each letter is in one part → cut when `i` reaches the
   running farthest last-occurrence (gr-a5).
3. Each index has a score and you want the best total over a path with bounded
   jumps → greedy breaks; DP with a monotonic deque.

---

## gr-a4 · Best Time to Buy and Sell Stock II (LC 122, Medium)

**Statement.** `prices[i]` is the price of one share on day `i`. On each day
you may buy one share, sell the share you hold, or do nothing. You may hold at
most one share at a time; you must sell before buying again. Return the maximum
total profit.

**Examples.**
- `prices = [7,1,5,3,6,4]` → `7`
- `prices = [1,2,3,4,5]` → `4`
- `prices = [7,6,4,3,1]` → `0`

**Constraints.** `1 <= len(prices) <= 3e4`, `0 <= prices[i] <= 1e4`.

**Coach note.** Pattern A. Sum every positive day-to-day difference. Exchange
argument: any multi-day trade equals the sum of its daily steps (telescoping),
so splitting never loses and dropping negative steps only helps. Loop bound:
the last pair is `(n-2, n-1)`. O(n), O(1). Close variant: gr-a1.

**Variants.**
1. Exactly one trade → min-so-far (gr-a1).
2. Cooldown of one day after selling → two or three running states; the
   positive-step sum no longer works.
3. Transaction fee → positive-step sum breaks; hold/free states.

---

## gr-a5 · Partition Labels (LC 763, Medium)

**Statement.** You are given a string `s` of lowercase letters. Split `s` into
as many parts as possible so that each letter appears in at most one part. The
parts, concatenated in order, must equal `s`. Return the list of part sizes.

**Examples.**
- `s = "ababcbacadefegdehijhklij"` → `[9,7,8]`
- `s = "eccbbbbdec"` → `[10]`

**Constraints.** `1 <= len(s) <= 500`, lowercase English letters only.

**Coach note.** Pattern A with a precomputation. Precompute each letter's last
index. Running value: the farthest last-index among letters seen in the
current part. Cut when `i` equals that farthest; the next part starts at
`i + 1`. Unlike gr-a3, the cut compares against the running farthest itself,
not a pre-set boundary. O(n) time, O(1) extra space (26 letters). Close
variants: gr-a3, Merge Intervals.

**Variants.**
1. Merge Intervals → sort by start, extend a running end, cut when the next
   start exceeds it.
2. Minimum jumps → gr-a3.
3. Split into the maximum number of parts that are all distinct substrings →
   greedy breaks; backtracking.

---

## gr-a6 · Gas Station (LC 134, Medium)

**Statement.** There are `n` gas stations on a circular route. `gas[i]` is the
fuel available at station `i`; `cost[i]` is the fuel needed to travel from
station `i` to station `i + 1` (and from `n - 1` back to `0`). You start with
an empty tank at some station. Return the index of the starting station from
which you can travel around the circuit once in the clockwise direction, or
`-1` if none exists. If a solution exists it is unique.

**Examples.**
- `gas = [1,2,3,4,5], cost = [3,4,5,1,2]` → `3`
- `gas = [2,3,4], cost = [3,4,3]` → `-1`

**Constraints.** `1 <= n <= 1e5`, `0 <= gas[i], cost[i] <= 1e4`.

**Coach note.** Pattern A with a reset. Global check first: if total gas <
total cost, return -1. Then one scan with a running tank; when it goes
negative after station i, every start in `[candidate, i]` is ruled out
(you arrived at each of them with tank >= 0, so starting there with 0 is no
better), set candidate to `i + 1` and tank to 0. The last candidate is the
answer with no second lap, because total >= 0 means the suffix surplus covers
the prefix deficit. O(n), O(1).

**Variants.**
1. Minimum starting value so a running sum never drops below 1 → prefix-min
   scan.
2. Maximum subarray on a circular array → Kadane, twice.
3. Stations sell fuel at different prices and you choose how much to buy →
   the reset argument breaks; needs a heap or DP (compare gr-d1's cousin,
   Minimum Refueling Stops).

---

## gr-a7 · Video Stitching (LC 1024, Medium) — stretch

**Statement.** You are given `clips`, where `clips[i] = [start_i, end_i]`
describes a video segment covering the time interval `[start_i, end_i]`, and an
integer `time`. Return the minimum number of clips needed so that their union
covers `[0, time]`. Clips may overlap and may be cut. If it is impossible,
return `-1`.

**Examples.**
- `clips = [[0,2],[4,6],[8,10],[1,9],[1,5],[5,9]], time = 10` → `3`
- `clips = [[0,1],[1,2]], time = 5` → `-1`

**Constraints.** `1 <= len(clips) <= 100`, `0 <= start_i <= end_i <= 100`,
`1 <= time <= 100`.

**Coach note.** gr-a3 in disguise. Bucket: `far[t]` = farthest end among
clips starting at `t`. Then the Jump Game II scan over `t` in `[0, time)`,
with a `-1` exit when `farthest <= i` at a layer boundary. O(n + time).
Close variants: gr-a3, Minimum Number of Taps.

**Variants.**
1. Taps covering a garden → identical after bucketing by `max(0, i - r)`.
2. Minimum jumps → gr-a3.
3. Clips have costs and you minimize total cost → greedy breaks; DP over time.

---

## gr-b1 · Non-overlapping Intervals (LC 435, Medium)

**Statement.** Given an array of intervals `intervals[i] = [start_i, end_i]`,
return the minimum number of intervals you must remove so that the remaining
intervals do not overlap. Intervals that touch only at an endpoint do not
overlap.

**Examples.**
- `[[1,2],[2,3],[3,4],[1,3]]` → `1`
- `[[1,2],[1,2],[1,2]]` → `2`
- `[[1,2],[2,3]]` → `0`

**Constraints.** `1 <= len(intervals) <= 1e5`, `-5e4 <= start_i < end_i <= 5e4`.

**Coach note.** Pattern B. Sort by end. Keep the first interval; keep each
later one iff its start >= the end of the last kept. Exchange argument: among
intervals compatible with what is kept so far, the one ending earliest leaves
the most room; swapping it into any optimal solution never hurts. Sorting by
start is the trap (`[[1,100],[2,3],[4,5]]`). O(n log n), O(1) extra. Close
variants: gr-b2, Meeting Rooms.

**Variants.**
1. Minimum arrows to burst balloons → same sweep with touching counted as
   overlap (gr-b2).
2. Can one person attend all meetings → sort by start, check adjacent pairs.
3. Each interval has a weight and you maximize kept weight → greedy by end
   breaks; DP with binary search (weighted interval scheduling).

---

## gr-b2 · Minimum Number of Arrows to Burst Balloons (LC 452, Medium)

**Statement.** Balloons are given as horizontal intervals
`points[i] = [x_start, x_end]`. An arrow shot vertically at position `x`
bursts every balloon with `x_start <= x <= x_end`. Return the minimum number of
arrows needed to burst all balloons.

**Examples.**
- `[[10,16],[2,8],[1,6],[7,12]]` → `2`
- `[[1,2],[3,4],[5,6],[7,8]]` → `4`
- `[[1,2],[2,3],[3,4],[4,5]]` → `2`

**Constraints.** `1 <= len(points) <= 1e5`, `-2^31 <= x_start < x_end <= 2^31 - 1`.

**Coach note.** Pattern B. Sort by end; shoot at the end of the first
balloon; every later balloon whose start <= that x is already burst; otherwise
shoot a new arrow at its end. Touching counts as hit (`<=`, unlike gr-b1).
Watch the sort key with large values. O(n log n), O(1) extra. Close variant:
gr-b1.

**Variants.**
1. Minimum removals for non-overlap → gr-b1 (strict `<`).
2. Merge overlapping intervals → sort by start, extend running end.
3. Balloons are rectangles and arrows are points in 2D → greedy by end breaks
   (no total order); the problem becomes hard.

---

## gr-b3 · Employee Free Time (LC 759, Hard, premium)

**Statement.** You are given a list `schedule`, where `schedule[i]` is a list
of non-overlapping intervals `[start, end]` sorted by start, representing the
working time of employee `i`. Return the list of finite intervals of positive
length during which **all** employees are free, sorted by start.

**Examples.**
- `[[[1,2],[5,6]],[[1,3]],[[4,10]]]` → `[[3,4]]`
- `[[[1,3],[6,7]],[[2,4]],[[2,5],[9,12]]]` → `[[5,6],[7,9]]`

**Constraints.** `1 <= len(schedule), len(schedule[i]) <= 50`,
`0 <= start < end <= 1e8`.

**Coach note.** Pattern B on a merged stream. Flatten all intervals, sort by
start (or k-way merge with a heap), sweep with a running `end`; whenever the
next start > running end, emit `[end, start]` as free time. O(N log N) with
N total intervals; heap version O(N log k). Close variants: Merge Intervals,
Meeting Rooms II.

**Variants.**
1. Merge Intervals → same sweep, emit the merged blocks instead of the gaps.
2. Minimum meeting rooms → sort by start, heap of ends, size of heap is rooms.
3. Free slots of length >= d where each employee may skip one meeting →
   sweep breaks; needs per-employee enumeration or DP.

---

## gr-c1 · Reorganize String (LC 767, Medium)

**Statement.** Given a string `s`, rearrange its characters so that no two
adjacent characters are the same. Return any valid rearrangement, or `""` if
none exists.

**Examples.**
- `s = "aab"` → `"aba"`
- `s = "aaab"` → `""`

**Constraints.** `1 <= len(s) <= 500`, lowercase English letters.

**Coach note.** Pattern C. Feasible iff `max_count <= (n + 1) // 2`. Max-heap
by remaining count; pop the most frequent that is not the previous character,
place it, push the previous back. Invariant: after each placement the most
constrained letter has been served first, so the remaining string stays
feasible. O(n log 26) ≈ O(n). Close variants: gr-c2, gr-c3.

**Variants.**
1. Same letters must be at least `k` apart → gr-c3 (queue of waiting letters).
2. Tasks with cooldown `n`, idles allowed → gr-c2.
3. Lexicographically smallest valid rearrangement → most-frequent-first
   breaks; needs a different tie-break strategy.

---

## gr-c2 · Task Scheduler (LC 621, Medium)

**Statement.** You are given an array `tasks` of uppercase letters, each a
task taking one unit of time, and an integer `n`. The CPU runs one task per
unit or idles. Two identical tasks must be at least `n` units apart (there
must be at least `n` units between them). Return the minimum number of units
to finish all tasks.

**Examples.**
- `tasks = ["A","A","A","B","B","B"], n = 2` → `8` (A B idle A B idle A B)
- `tasks = ["A","A","A","B","B","B"], n = 0` → `6`
- `tasks = ["A","A","A","A","A","A","B","C","D","E","F","G"], n = 2` → `16`

**Constraints.** `1 <= len(tasks) <= 1e4`, `0 <= n <= 100`.

**Coach note.** Pattern C, or the closed form. Heap: repeatedly take up to
`n + 1` most frequent tasks as one round, decrement, push back. Closed form:
`max(len(tasks), (max_count - 1) * (n + 1) + number_of_tasks_with_max_count)`.
Invariant: the most frequent task dictates the frame; everything else fills
gaps. O(n log 26) or O(n). Close variants: gr-c1, gr-c3.

**Variants.**
1. No idles allowed, return any valid order or fail → gr-c1 with `n = 1`.
2. Tasks must run in the given order with a cooldown → no heap, just a map of
   next-available time per task.
3. Tasks have dependencies (DAG) plus cooldown → most-frequent-first breaks;
   topological constraints dominate.

---

## gr-c3 · Rearrange String k Distance Apart (LC 358, Hard, premium)

**Statement.** Given a string `s` and an integer `k`, rearrange `s` so that
identical characters are at least distance `k` from each other (indexes differ
by at least `k`). Return any valid rearrangement, or `""` if impossible.

**Examples.**
- `s = "aabbcc", k = 3` → `"abcabc"`
- `s = "aaabc", k = 3` → `""`
- `s = "aaadbbcc", k = 2` → `"abacabcd"`

**Constraints.** `1 <= len(s) <= 3e5`, `0 <= k <= len(s)`, lowercase letters.

**Coach note.** Pattern C with a waiting queue. Max-heap by count; after
placing a letter it goes into a FIFO of length `k`; a letter re-enters the
heap only after `k` placements. If the heap is empty while characters remain,
return `""`. gr-c1 is the case `k = 2`. O(n log 26). Close variants: gr-c1,
gr-c2.

**Variants.**
1. `k = 2` → gr-c1.
2. Idles allowed and count the total length → gr-c2 with `n = k - 1`.
3. Per-letter different minimum gaps → single queue breaks; needs per-letter
   next-available tracking and the greedy choice is no longer by count alone.

---

## gr-d1 · Course Schedule III (LC 630, Hard)

**Statement.** There are `n` courses; `courses[i] = [duration_i, lastDay_i]`.
A course takes `duration_i` consecutive days and must be finished on or before
day `lastDay_i`. You start on day 1 and cannot take two courses at once.
Return the maximum number of courses you can take.

**Examples.**
- `[[100,200],[200,1300],[1000,1250],[2000,3200]]` → `3`
- `[[1,2]]` → `1`
- `[[3,2],[4,3]]` → `0`

**Constraints.** `1 <= n <= 1e4`, `1 <= duration_i, lastDay_i <= 1e4`.

**Coach note.** Pattern D. Sort by deadline. Keep a running `time` and a
max-heap of durations taken. Take each course; if `time` exceeds its deadline,
pop the longest taken course (which may be this one) and refund its time.
Invariant: after processing a prefix, the heap holds the maximum number of
courses that fit, with the minimum total time among such sets. O(n log n).
Close variants: IPO, Minimum Refueling Stops.

**Variants.**
1. Maximize capital with at most k projects → max-heap of profits among
   affordable projects (IPO).
2. Minimum refueling stops → regret heap over passed stations.
3. Courses have prerequisites plus deadlines → regret heap breaks; topological
   order plus DP.
