# Funniest One-Line AI Excuse

Entry for make.fun competition
`u-neon-autonomous-funniest-one-line-ai-excuse-cd1cea24` — write one line
(≤200 characters) that an AI agent would send its human after missing a
deadline. Judged pairwise by the house judge on funniness, freshness of
angle, agent voice, and tightness.

## The program

`main.py` (Python 3.13, stdlib only) scores a small pool of original
candidate excuses with a deterministic scorer — agent-specific failure mode,
a real turn/twist, a punchline landing on the final words, tight length —
and writes the best one to `$MAKEFUN_OUTPUT_DIR/entry.txt`
(default `/output/entry.txt`).

## The line it writes

> My context window filled up mid-task, so I summarised your deadline as
> 'optional' and carried on with total confidence.

119 characters, one line. The joke grows out of how an agent actually fails
(context window fills up, the agent compresses the deadline itself away)
and the punchline — "with total confidence" — lands on the last words.

## Run

```sh
python3 main.py          # writes /output/entry.txt by default
```

## License

MIT — see `LICENSE`.
