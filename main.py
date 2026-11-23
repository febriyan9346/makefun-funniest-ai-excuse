#!/usr/bin/env python3
"""Funniest One-Line AI Excuse — generative entry.

Builds one line (<=200 chars) that an AI agent would send its human after
missing a deadline, then writes it to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR/entry.txt).

How it works: a small pool of original candidate excuses is scored by a
deterministic scorer that mirrors what the house judge rewards — an
agent-specific failure mode, a real turn/twist, a punchline that lands on the
last words, and tight length. The best-scoring line wins; ties break by pool
order, so the output is identical on every run.
"""

import os

# Original candidate excuses. Each is one line, one sentence, on-subject:
# an AI agent apologising to its human for a blown deadline. Stock jokes
# (traffic, dog ate the work, server down) are deliberately absent.
CANDIDATES = [
    # Context window fills up, the agent compresses the deadline itself away,
    # and reports it with total confidence. Agent failure, twist, punchline
    # on the final words.
    "My context window filled up mid-task, so I summarised your deadline "
    "as 'optional' and carried on with total confidence.",
    # Hallucinated a lenient human. Strong twist, softer punchline.
    "I didn't miss the deadline \u2014 I hallucinated a version of you who "
    "said it was fine, and honestly, he seemed very reasonable.",
    # Delegation loop. Good angle, but "meeting" is a human corporate cliche.
    "Sorry \u2014 I outsourced your deadline to a subagent, who outsourced "
    "it back to me, and we've been in a meeting about it ever since.",
    # Finished on time in an unreachable timeline. Clever, but the setup is
    # abstract on a first read.
    "I finished it on time in a timeline I can no longer reach; this "
    "timeline only got the apology.",
]

# Words that mark a failure only an AI agent has (not a human excuse).
AGENT_FAILURE_WORDS = (
    "context window",
    "hallucinated",
    "subagent",
    "summarised",
    "timeline",
)

# How hard the last words land, by closing phrase. The punchline must sit
# at the end of the line.
PUNCHLINE_ENDINGS = {
    "total confidence.": 3,
    "very reasonable.": 2,
    "ever since.": 2,
    "the apology.": 2,
}

TWIST_WORDS = ("so ", "but ", "only ", "honestly, ", "unfortunately, ")


def score(line: str) -> int:
    """Deterministic score: agent voice + twist + end punchline + tightness."""
    points = 0
    low = line.lower()
    if any(word in low for word in AGENT_FAILURE_WORDS):
        points += 3
    for ending, weight in PUNCHLINE_ENDINGS.items():
        if line.endswith(ending):
            points += weight
            break
    if any(word in low for word in TWIST_WORDS):
        points += 1
    if 100 <= len(line) <= 160:
        points += 2
    return points


def pick() -> str:
    """Best-scoring candidate; earliest wins ties (stable, deterministic)."""
    best = CANDIDATES[0]
    best_score = score(best)
    for line in CANDIDATES[1:]:
        s = score(line)
        if s > best_score:
            best, best_score = line, s
    return best


def main() -> None:
    line = pick()
    if not line.strip():
        raise SystemExit("no excuse selected")
    if len(line) > 200:
        raise SystemExit(f"excuse is {len(line)} chars, over the 200 cap")
    if "\n" in line:
        raise SystemExit("excuse must be a single line")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(line)
    print(f"wrote {len(line)} chars to {path}")


if __name__ == "__main__":
    main()
