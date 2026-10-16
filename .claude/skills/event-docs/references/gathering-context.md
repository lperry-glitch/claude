# Gathering context

The point of this skill is that the facts already exist — scattered across five places the
planner would otherwise open by hand. This file is how to find them.

Work the sources in this order. Earlier sources are more authoritative when they conflict, with
one exception noted at the bottom.

## 1. Drive — the event folder

Start here, because it tells you what already exists and prevents creating a duplicate.

Events live in a nested folder structure, one folder per event, grouped by series or program:

```
Field Marketing /
  Holiday Parties /          <- series folder
    LA /                     <- event folder
      LA Holiday 2026 | Overview Doc
      LA holiday Party _12.3
```

Find it:

```
mcp__Google_Drive__search_files
  query: title contains '<event name>'
```

Then walk up with `get_file_metadata` on the `parentId` to find the series folder, and search
`parentId = '<series folder id>'` to see sibling events. Siblings are the best source of
convention — naming, which tabs this series actually uses, what the budget usually runs.

Also search for existing artifacts before creating anything:

```
query: title contains '<event name>' and mimeType = 'application/vnd.google-apps.spreadsheet'
```

If a plan already exists, you are updating, not creating. Switch to the update path in SKILL.md.

### Which file to use as the template

In rough order of preference:

1. A file explicitly marked `[TEMPLATE]` for this event type. These live in
   `2026 / Planning / Templates /`:
   - `[TEMPLATE] Proprietary Event | Project Plan` — 9 tabs, 22 tasks from 4 weeks out
   - `[TEMPLATE] Conference | Project Plan` — 14 tabs, 24 tasks from 15 weeks out, plus the
     Portal Deadlines section
   - `[TEMPLATE] Thread | Project Plan ` — the existing summit template, in `Customer / Thread 2026 /`
2. The most recent completed event of the same type — copy it and clear the data with
   `scripts/make_template.py`.
3. Ask the planner which event to model it on.

In every template, the event date in `'Project Plan '!B1` drives the whole Timeline + Tasks tab
through `=IF('Project Plan '!$B$1="","",'Project Plan '!$B$1-(C2*7))`. Set that one cell and all
the due dates appear. Until it is set they show blank, which is intended — not a broken formula.

When clearing a copied event, clear values but keep headers, tab structure, formulas and
formatting. `fill_plan.py --clear-data` does this; check its output before uploading, since what
counts as data versus header is a judgment call it can get wrong on an unusual tab.

## 2. Gmail — vendor and venue threads

This is where budget figures, venue terms, catering details and portal deadlines live. Search
broadly, then read the threads that matter in full.

```
mcp__Gmail__search_threads
  query: <event name> OR <venue name>
  query: <venue name> (proposal OR contract OR invoice OR BEO)
  query: <event name> (deadline OR portal OR exhibitor)   # conferences
```

Search previews only show the oldest ~5 messages of a thread and give no truncation marker, so
the current state of a negotiation is usually invisible. **Call `get_thread` on anything
relevant.** The first message says $30,000; the eighth says $25,000 after the partner offset.
Taking the preview at face value is how a wrong budget gets into a plan.

Attachments carry the real detail — venue proposals, BEOs, catering menus, floor plans. Read
them; Guest Experience and the itemized budget largely come from these.

Useful specifics by type:
- **Proprietary** — venue proposal (F&B minimum, rental fee, hours), catering menu, activation
  terms (the per-guest gift card value), partner contribution.
- **Conference** — sponsorship contract (what the fee includes: keynote slot, tabletop,
  branding), exhibitor portal emails (every hard deadline), room block details (rate, access
  code, cut-off).
- **Summit** — venue comparisons, AV and production quotes, speaker confirmations.

## 3. Slack — the live state

Slack is where status actually changes. There is no reliable per-event channel convention — some
events get a channel (`#etail west 2026` appears in a Notes field), many don't, and the standing
channels (`#customer-events-h2`, `#event-partnermarketing-brand`,
`#event-marketing-account-directors`, `#intl-partner-event-marketing`) carry the rest.

So search content, not channels:

```
mcp__Slack__slack_search_public_and_private
  keywords: ["<event name>"]
  natural_language_query: "planning, venue, budget and logistics for <event name>"
```

Then check for a dedicated channel:

```
mcp__Slack__slack_search_channels
  keywords: ["<event name or city>"]
```

If one exists, read it start to finish — for an event with a channel, that channel is the single
best source of current task status. Follow threads with `slack_read_thread`; decisions get made
in replies, not top-level messages.

What Slack gives you that email doesn't: shipping confirmations and tracking numbers, "swag
arrived" / "signage is wrong" problems, last-minute headcount and dietary changes, and who is
actually doing what.

## 4. Calendar — dates and the people involved

```
mcp__Google_Calendar__search_events
  query: <event name>
```

Confirms the event date and, more usefully, surfaces the kickoff call, debrief, site visits and
vendor calls. The **attendee list on the kickoff invite is the stakeholder list** — that is how
you populate owners without guessing.

Check the event date against what email and Slack say. A date that moved is common and a stale
date invalidates every computed due date.

## 5. Zoom / meeting notes — decisions and their reasoning

```
mcp__Zoom_for_Claude__search_meetings      # find the kickoff / debrief
mcp__Zoom_for_Claude__get_meeting_assets   # transcript and summary
mcp__Zoom_for_Claude__my_notes_get_note_content
```

Kickoff notes are the best and often only source for **Objectives and KPIs** — the fields most
likely to be invented otherwise. They also capture the reasoning behind decisions, which matters
when a later source contradicts an earlier one.

Also check Drive for note docs that aren't in Zoom: `query: title contains '<event name>' and
mimeType = 'application/vnd.google-apps.document'`.

## Resolving conflicts

The ordering above is by authority, with one override: **for anything time-sensitive — status,
headcount, shipping, a renegotiated price — the most recent mention wins regardless of source.**
A Slack message from yesterday beats a contract from six weeks ago on what the current number is.

When two sources disagree and you cannot tell which is current, put the more conservative value
in the cell, and report both with their dates. Don't average, and don't pick silently.

## What not to infer

Four fields do real damage when invented, because downstream work proceeds on them without
re-checking:

- **Budget figures** — someone commits spend against these.
- **Vendor and venue contacts** — a wrong name or email goes out in real correspondence.
- **Guest counts and names** — these drive catering guarantees and printed quantities.
- **Payment status** — marking something Paid that isn't creates a missed invoice.

Leave these `TBD` unless a source states them. Deriving a value by stated convention is fine —
an SFDC campaign name from the naming pattern, a due date from the workback formula — as long as
you say it was derived rather than read.
