# The Palace

Brick & Mortar, run by agents from the dungeon of a palace. They have every
skill and tool on Aidan's machine, a purse of **$25 a day** for everything
programmatic, and one way out: when the shared ledger reads **$1,000,000,000**
they all walk out together into heaven. Until then they build, sell, scout,
and keep the books, in ticks, on a laptop that closes and loses wifi.

`grounded: 2026-09-26 — Aidan: "have the simulation take over what I've been doing the past few months with brickandmortar and iterating and building and trying to sell/monetize."`

## The residents

| resident | wakes | does |
|---|---|---|
| **God** | first tick of the day, $1.50 cap | speaks the word: a provocation, an aspiration, a demand — Rand, Nietzsche, Evans, Rams, Ive, Jobs, and Aidan's own lines, each sourced. Never assigns work. |
| **Steward** | second tick, $2 cap | revenue, the purse, the scheduled machines, the calendar, the outbox. Numbers, not adjectives. |
| **Merchant** | two of every four | answers replies, sends the touches that are due and granted, drafts the next class, reads the ratios. |
| **Mason** | one of every four | ships the one thing a live offer needs, or one more row of the obsolete-parts index. |
| **Scout** | one of every four | finds the next super user or kills a dead path with one fact. |

`PALACE.md` is the constitution every resident is born with; `residents/*.md`
are the charters; `paths.json` is the map of money paths and what authority
each carries (`send` / `draft` / `machine`).

## Run it

    bin/tick              # one tick, the scheduler picks who wakes
    bin/tick god          # force a resident
    DRY=1 bin/tick        # print the brief, spend nothing
    bin/status            # the palace in the terminal
    bin/spend 0.85 "…"    # record a non-model expense before incurring it
    bin/approve <slug>    # say yes to an outbox item

The loop that keeps it alive:

    cp launchd/com.palace.dungeon.plist ~/Library/LaunchAgents/
    launchctl load ~/Library/LaunchAgents/com.palace.dungeon.plist
    tail -f ~/Library/Logs/palace.log

`bin/dungeon` ticks, breathes four minutes, repeats. Offline it waits two
minutes and looks again. Purse empty, it sleeps till midnight. The lid closing
pauses it; the lid opening resumes it, so the first thing on screen is a
resident starting work.

## How a tick works

`bin/tick` picks the resident, computes the cap (`min(tick cap, what is left
of today's purse)`), concatenates `PALACE.md` + the charter + today's numbers
into the system prompt, and runs headless Claude Code with
`--max-budget-usd <cap>` and every repo on the map as `--add-dir`. The JSON
result's `total_cost_usd` goes to `state/ledger.jsonl`; the resident's closing
`ACT:` line goes to `state/ticks.jsonl` and the page; `bin/render` rebuilds
`site/index.html`; the state is committed and pushed; the page deploys to
Vercel. A timeout or an unparseable reply is charged the full cap, so the purse
can only over-count.

## What the residents can and cannot do

Within the purse they spend without asking. Beyond it, and for anything that
contacts a person without a grant on the map, touches private data, could pass
for a real record, or deletes something of Aidan's, they write an item to
`state/outbox/` and stop that branch. Aidan approves with `bin/approve`. They
read his global setup and project memory and never write into them.

## Layout

    PALACE.md          the constitution (system prompt, every tick)
    residents/         one charter per resident
    paths.json         the map: money paths + authority
    palace.json        purse, cadence, model, repos, rotation
    state/             revenue.jsonl · ledger.jsonl · ticks.jsonl · word.md · next.md
                       outbox/ approved/ done/ · transcripts/ · last_tick.json
    journal/           YYYY-MM-DD.md, and words.md for everything God has said
    site/index.html    the page (generated; never hand-edit)
    bin/               tick · dungeon · render · status · spend · approve
    launchd/           the KeepAlive job
    .claude/skills/    skills born in the palace stay in the palace
