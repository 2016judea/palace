# The Palace

Brick & Mortar, run by agents from the dungeon of a palace. They have every
skill and tool on Aidan's machine, a purse of **$25 a day** for everything
programmatic, and one way out: when the shared ledger reads **$1,000,000,000**
they all walk out together into heaven. Until then they build, sell, scout,
and keep the books, in ticks, on a laptop that closes and loses wifi.

**It is a closed system.** Aidan watches through a window and never approves
anything; God rules on every petition (a new buyer class, a channel, a ledger
question) inside the standing rules, within a minute of its filing. What God
cannot grant, such as money beyond the purse, is simply unavailable.

`grounded: 2026-09-25 — Aidan: "have the simulation take over what I've been doing the past few months with brickandmortar and iterating and building and trying to sell/monetize."`

## The residents

| resident | wakes | does |
|---|---|---|
| **God** | first tick of the day, $1.50 cap; and in court within a minute of any petition, $1, six a day | speaks the word: a provocation, an aspiration, a demand — Rand, Nietzsche, Evans, Rams, Ive, Jobs, and Aidan's own lines, each sourced. Never assigns work. Rules on petitions inside the bounds. |
| **Steward** | second tick, $2 cap | revenue, the purse, the scheduled machines, the calendar, the outbox. Numbers, not adjectives. |
| **Merchant** | only when `bin/due` finds a new reply, a dated action, or a grant | answers replies, sends the touches that are due and granted, drafts the next class, reads the ratios. |
| **Mason** | the idle default | ships the one thing a live offer needs, or one more row of the obsolete-parts index. |
| **Scout** | at most twice a day | finds the next super user or kills a dead path with one fact. |

`PALACE.md` is the constitution every resident is born with; `residents/*.md`
are the charters; `paths.json` is the map of money paths and what authority
each carries (`send` / `draft` / `machine`).

## Where it is

- **Live, on the laptop:** http://localhost:4477 — a window: the number, the light, a live ticker of what the working resident is doing, the day digest, the word, the court, the calendar, the journal. Two controls: pause/resume and the $/day. `launchd/com.palace.serve.plist` keeps it up.
- **Read-only copy for the phone:** https://palace-gray.vercel.app — redeployed after every tick. No names of people or companies ever appear on it.
- **The repo:** github.com/2016judea/palace (private).
- **The log:** `~/Library/Logs/palace.log`.

## Run it

    bin/tick              # one tick, the scheduler picks who wakes
    bin/tick god          # force a resident
    DRY=1 bin/tick        # print the brief, spend nothing
    bin/status            # the palace in the terminal
    bin/due --text        # what is actionable now, no model spend
    bin/spend 0.85 "…"    # record a non-model expense before incurring it
    bin/petition "…"      # a resident asks God for a ruling
    bin/sent <path> 5 form   # log first touches against the daily cap of 20
    bin/calendar add 2026-10-02 logistics-diagnostic "touch 2"
    bin/stripe            # new paid checkouts since last seen

The loop that keeps it alive:

    cp launchd/com.palace.dungeon.plist ~/Library/LaunchAgents/
    launchctl load ~/Library/LaunchAgents/com.palace.dungeon.plist
    tail -f ~/Library/Logs/palace.log

`bin/dungeon` ticks, breathes ten minutes, repeats; a petition or a new reply
cuts the breath to twenty seconds. Offline it waits two minutes and looks again.
The purse is a token bucket ($25 accrues per 24h, pooling to $8): it fills
while the lid is closed, so opening it starts a burst of work, then about a
dollar an hour. Nobody wakes for less than $2.

## How a tick works

`bin/tick` runs `bin/due`, picks the resident (court if a petition waits; God
and Steward once a day; Merchant only when something is due; Scout at most
twice; else Mason), computes the cap (`min(tick cap, bucket balance)`), and
assembles a one-screen brief: the word, what is due, rulings since that
resident's last tick, and its own resume note (`state/resume/<name>.md`, 300
words). `PALACE.md` + the charter + today's numbers are the system prompt; the
session runs headless with `--max-budget-usd <cap>`, every repo on the map as
`--add-dir`, and `stream-json` output so the page can show each action as it
happens. The result's `total_cost_usd` is charged to the bucket and logged in
`state/ledger.jsonl`; the closing `ACT:` line goes to `state/ticks.jsonl` and
the page; `bin/render` rebuilds `site/index.html`; state is committed and
pushed; the page deploys to Vercel. A dead session is charged the full cap, so
the purse can only over-count.

## What the residents can and cannot do

Within the purse they spend without asking; beyond it there is nobody to ask.
A first touch to a new buyer class, a new channel or a ledger question is a
petition to God (`state/court/`), ruled within the bounds: never cold email as
a first touch, the opener from the reader's own record, Aidan's voice, every
send ledgered, at most 20 first touches a day. Never grantable: money beyond
the purse, private data, anything passing for a real record, deleting his
things, rewriting his prose. A free key or listing behind his login they set up
themselves through his Chrome. They read his global setup and project memory
and never write into them.

## Layout

    PALACE.md          the constitution (system prompt, every tick)
    residents/         one charter per resident
    paths.json         the map: money paths + authority
    palace.json        purse, cadence, model, repos, rotation
    state/             revenue.jsonl · ledger.jsonl · ticks.jsonl · sends.jsonl · word.md
                       bucket.json · calendar.json · resume/<resident>.md · court/ (+ruled/)
                       live.jsonl · transcripts/ · last_tick.json
    journal/           YYYY-MM-DD.md, and words.md for everything God has said
    site/index.html    the page (generated; never hand-edit)
    bin/               tick · dungeon · render · serve · status · due · petition · sent · calendar · stripe · spend
    launchd/           the KeepAlive job
    .claude/skills/    skills born in the palace stay in the palace
