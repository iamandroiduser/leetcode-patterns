#!/usr/bin/env python3
"""File a PREP-LOG block from the drill coach and regenerate status.md.

Usage:
  python3 notes/coach/ingest.py <file.json>     file one block, then render
  python3 notes/coach/ingest.py --paste          read a pasted block from stdin
                                                 (a ```json fence is fine)
  python3 notes/coach/ingest.py --render         regenerate status.md only
  python3 notes/coach/ingest.py --render --today 2026-10-02

Raw blocks are append-only under notes/coach/log/. status.md is derived from
them plus curriculum.md and is overwritten on every run. Edit the logs, not
status.md.
"""
import datetime as dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(HERE, "log")
CURRICULUM = os.path.join(HERE, "curriculum.md")
STATUS = os.path.join(HERE, "status.md")

# Spaced-recall intervals in days, indexed by the number of distinct days the
# problem has been exposed on. Five spaced exposures is the bar for full solid.
INTERVALS = [1, 3, 7, 14, 30, 60]

ERROR_TAGS = {
    "state-dropped": "a variable present in the verbal description has no line in the code",
    "boundary": "off-by-one: loop bound, loop guard, or the one-element input",
    "name-mismatch": "a name defined one way and read another (crashes as pasted)",
    "add-vs-max": "a reach value treated as a stockpile that accumulates",
    "commit-early": "committing to one choice (landing spot, boundary) instead of tracking the running best",
    "trace-skipped": "self-trace not done before the paste",
    "trace-not-code": "trace rows or values do not match the code as written, or a mismatch with the expected output went unflagged",
    "misread-input": "misread what an input number or a condition means",
    "polarity": "crossed two branches or flipped a comparison",
    "series-sum": "wrong complexity bound from summing a series by hand",
}

PROFILE = """Ajay. 5 to 10 years of experience, ML/AI in robotics and autonomous driving.
Targets: Waymo, Tesla, Nuro, Zoox, Aurora, NVIDIA, Anthropic, OpenAI, FAANG.
Codes in Python. Prefers plain chat over narrated pages. Learns best with
short sections and one question per message. His own diagnosis, confirmed by
the log: the idea is usually right, the translation to code is where it leaks."""

CLAIMS = """Stated in the coach prompt, not yet observed in this repo's log:
- misreading what the input numbers mean is his main loss point (one
  instance so far, gr-a6 on 2026-09-22)
- summing a series by hand has produced wrong complexity bounds
  (complexity has not been extracted in any session logged here)"""

PROTOCOL = """1. State table before code: name, meaning, initial value, exact update
   formula with the operator named. Exit row with the last iteration that runs.
2. Code translated row by row. 2b. Name audit: list names assigned, names
   read, diff.
3. Self-trace on the textbook example and a one-element input. Write the
   visited i values from the range expression first. End with match/mismatch.
4. Run."""


def load_curriculum():
    ids = []
    with open(CURRICULUM) as f:
        for line in f:
            m = re.match(r"^## (gr-\w+) · (.+?) \(LC (\d+), (\w+)", line)
            if m:
                ids.append((m.group(1), m.group(2), int(m.group(3)), m.group(4)))
    return ids


def load_logs():
    blocks = []
    for name in sorted(os.listdir(LOG_DIR)) if os.path.isdir(LOG_DIR) else []:
        if name.endswith(".json"):
            with open(os.path.join(LOG_DIR, name)) as f:
                b = json.load(f)
            b["_file"] = name
            blocks.append(b)
    return blocks


def validate(block):
    for k in ("source", "as_of", "problems", "errors", "anchors", "open_items", "suspect_turns"):
        if k not in block:
            raise SystemExit(f"PREP-LOG block is missing key: {k}")
    if block["source"] not in ("voice", "chat"):
        raise SystemExit("source must be 'voice' or 'chat'")
    dt.date.fromisoformat(block["as_of"])
    for pid, p in block["problems"].items():
        if p.get("status") not in ("shaky", "solid", "failed"):
            raise SystemExit(f"{pid}: status must be shaky, solid or failed")
        for e in p.get("exposures", []):
            dt.date.fromisoformat(e["date"])
            if e.get("kind") not in ("solve", "rep", "recall"):
                raise SystemExit(f"{pid}: exposure kind must be solve, rep or recall")
            if e.get("result") not in ("shaky", "solid", "failed"):
                raise SystemExit(f"{pid}: exposure result must be shaky, solid or failed")
    unknown = {e["tag"] for e in block["errors"]} - set(ERROR_TAGS)
    if unknown:
        print(f"note: new error tag(s) {sorted(unknown)}; add a definition to ERROR_TAGS in ingest.py")


def file_block(block):
    validate(block)
    os.makedirs(LOG_DIR, exist_ok=True)
    n = 1
    while True:
        name = f"{block['as_of']}-{block['source']}-{n}.json"
        path = os.path.join(LOG_DIR, name)
        if not os.path.exists(path):
            break
        n += 1
    with open(path, "w") as f:
        json.dump(block, f, indent=2)
        f.write("\n")
    print(f"filed {os.path.relpath(path)}")


def render(today):
    curriculum = load_curriculum()
    titles = {i: (t, lc, d) for i, t, lc, d in curriculum}
    order = [i for i, _, _, _ in curriculum]
    blocks = load_logs()
    as_of = max([b["as_of"] for b in blocks], default="never")

    # per-problem aggregation
    probs = {}
    for b in blocks:
        for pid, p in b["problems"].items():
            agg = probs.setdefault(pid, {"status": None, "status_date": "", "exposures": [], "slips": [], "self_ratings": []})
            agg["exposures"] += p.get("exposures", [])
            agg["slips"] += p.get("slips", [])
            if p.get("self_rating") and p["self_rating"] != "not asked":
                agg["self_ratings"].append((b["as_of"], p["self_rating"]))
            if b["as_of"] >= agg["status_date"]:
                agg["status"], agg["status_date"] = p["status"], b["as_of"]

    errors = [e for b in blocks for e in b["errors"]]
    anchors = {}
    for b in blocks:
        for a in b["anchors"]:
            anchors[a["id"]] = (a["phrase"], b["as_of"])
    open_items = [(b["as_of"], o) for b in blocks for o in b["open_items"]]
    suspect = [(b["as_of"], b["_file"], b["suspect_turns"]) for b in blocks if b["suspect_turns"] != "none"]

    def due_date(exps):
        days = sorted({e["date"] for e in exps})
        if not days:
            return None, 0
        n = len(days)
        gap = INTERVALS[min(n - 1, len(INTERVALS) - 1)]
        return dt.date.fromisoformat(days[-1]) + dt.timedelta(days=gap), n

    rows, due = [], []
    for pid in order + [p for p in probs if p not in order]:
        t = titles.get(pid, (pid, "", ""))
        agg = probs.get(pid)
        if not agg:
            rows.append((pid, t, "not started", 0, "", "", ""))
            continue
        d, n = due_date(agg["exposures"])
        last = max(e["date"] for e in agg["exposures"]) if agg["exposures"] else ""
        hist = " ".join(f"{e['date'][5:]}:{e['result'][0]}{'' if e.get('verified', True) else '?'}" for e in sorted(agg["exposures"], key=lambda e: e["date"]))
        due_s = d.isoformat() if d else ""
        flag = "DUE" if d and d <= today else ""
        rows.append((pid, t, agg["status"], n, last, due_s, flag, hist))
        if flag:
            due.append((d, pid))
    due.sort()
    next_new = next((pid for pid in order if pid not in probs), None)

    tag_counts = {}
    for e in errors:
        tag_counts[e["tag"]] = tag_counts.get(e["tag"], 0) + 1

    out = []
    w = out.append
    w(f"# Status — as of {as_of}")
    w("")
    w(f"Generated by `notes/coach/ingest.py` on {today.isoformat()} from {len(blocks)} log block(s) in `notes/coach/log/`. Do not edit by hand; file a PREP-LOG block instead.")
    w("")
    w("## Profile")
    w("")
    w(PROFILE)
    w("")
    w("## Due now")
    w("")
    if due:
        w(f"{len(due)} recall(s) due (spacing: {', '.join(map(str, INTERVALS))} days by distinct exposure days):")
        w("")
        for d, pid in due:
            w(f"- {pid} · {titles.get(pid, (pid,))[0]} (due {d.isoformat()})")
    else:
        w("No recalls due.")
    w("")
    if next_new:
        w(f"Next new problem: **{next_new} · {titles[next_new][0]}**")
    else:
        w("Next new problem: none left in the curriculum.")
    w("")
    w("## Problems")
    w("")
    w("Status is the latest block's call. `n` is distinct exposure days; full solid needs 5. History is `MM-DD:result`, with `?` for an unverified exposure (session with a suspect turn).")
    w("")
    w("| id | title | LC | status | n | last | due | history |")
    w("|---|---|---|---|---|---|---|---|")
    for r in rows:
        pid, t = r[0], r[1]
        if r[2] == "not started":
            w(f"| {pid} | {t[0]} | {t[1]} | not started | 0 | | | |")
        else:
            _, _, st, n, last, due_s, flag, hist = r
            w(f"| {pid} | {t[0]} | {t[1]} | {st}{' **DUE**' if flag else ''} | {n} | {last} | {due_s} | {hist} |")
    w("")
    w("## Error tags")
    w("")
    w("Reuse these tags exactly. Counts are across all logged sessions.")
    w("")
    w("| tag | count | meaning |")
    w("|---|---|---|")
    for tag, meaning in ERROR_TAGS.items():
        w(f"| {tag} | {tag_counts.get(tag, 0)} | {meaning} |")
    extra = sorted(set(tag_counts) - set(ERROR_TAGS))
    for tag in extra:
        w(f"| {tag} | {tag_counts[tag]} | (undefined, add to ingest.py) |")
    w("")
    w("### Recent errors")
    w("")
    for e in sorted(errors, key=lambda e: e["date"])[-15:]:
        w(f"- {e['date']} `{e['tag']}` {e['note']}")
    w("")
    w("## Slips by problem")
    w("")
    for pid in order:
        agg = probs.get(pid)
        if agg and agg["slips"]:
            w(f"**{pid} · {titles[pid][0]}**")
            for s in agg["slips"]:
                w(f"- {s}")
            w("")
    w("## His anchors (verbatim)")
    w("")
    for pid in order:
        if pid in anchors:
            ph, d = anchors[pid]
            w(f"- {pid} ({d}): \"{ph}\"")
    missing = [pid for pid in order if pid in probs and pid not in anchors]
    if missing:
        w(f"- no anchor phrase yet: {', '.join(missing)}")
    w("")
    w("## Open items")
    w("")
    for d, o in open_items:
        w(f"- {d} {('[' + o['id'] + '] ') if o.get('id') else ''}{o['note']}")
    w("")
    w("## Suspect turns")
    w("")
    if suspect:
        for d, f, s in suspect:
            w(f"- {d} ({f}): {s}")
    else:
        w("None logged.")
    w("")
    w("## Claims not yet evidenced here")
    w("")
    w(CLAIMS)
    w("")
    w("## Drill protocol in force")
    w("")
    w(PROTOCOL)
    w("")
    with open(STATUS, "w") as f:
        f.write("\n".join(out))
    print(f"rendered {os.path.relpath(STATUS)} (as of {as_of}, {len(due)} due, next new {next_new})")


def extract_json(text):
    m = re.search(r"```json\s*(\{.*\})\s*```", text, re.S)
    return json.loads(m.group(1) if m else text)


def main(argv):
    today = dt.date.today()
    if "--today" in argv:
        today = dt.date.fromisoformat(argv[argv.index("--today") + 1])
    if "--paste" in argv:
        file_block(extract_json(sys.stdin.read()))
    elif "--render" not in argv:
        paths = [a for a in argv if not a.startswith("--") and a.endswith(".json")]
        if not paths:
            print(__doc__)
            return
        for p in paths:
            with open(p) as f:
                file_block(extract_json(f.read()))
    render(today)


if __name__ == "__main__":
    main(sys.argv[1:])
