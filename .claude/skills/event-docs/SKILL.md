---
name: event-docs
description: Creates and updates the two standing event planning artifacts — the Overview Doc (Google Doc) and the Project Plan (multi-tab Google Sheet) — for Attentive field marketing events, filling them from event data already sitting in Gmail, Slack, Google Calendar, Drive and Zoom/meeting notes. Use this whenever the user mentions spinning up, kicking off, planning, prepping, or building docs for an event, a conference, a dinner, a party, an activation, a summit, a roadshow, or a Thread event — and also when they ask to refresh, update, or "catch up" an existing project plan, build a workback timeline, or figure out what's outstanding on an event. Trigger even if they don't say "overview doc" or "project plan" by name; "can you set up the docs for the Chicago dinner" or "what's left on eTail" is this skill.
---

# Event Docs

Build the Overview Doc and Project Plan for an event, filled from what already exists in
Gmail, Slack, Calendar, Drive and meeting notes.

The goal is to replace an hour of copy-paste-and-remember with a draft that is accurate about
what is known and honest about what is not. A planner can fix a wrong date in ten seconds; they
cannot recover from a confidently invented budget that nobody questioned until the invoice came.
So the bar here is not "complete" — it is **sourced**.

## The two artifacts

| Artifact | Format | Purpose |
| --- | --- | --- |
| **Overview Doc** | Google Doc | Outward-facing. Date, venue, key links table, description, guest experience. What you send someone who asks "what is this event?" |
| **Project Plan** | Google Sheet, many tabs | Working file. Objectives/KPIs/budget, the workback timeline, budget tracker, agenda, sessions, assets, shipping. What the team lives in. |

Naming convention, from existing files — match it exactly, trailing space and all:

```
<Event Name> <Year> | Overview Doc
<Event Name> <Year> | Project Plan
```

Regional field events use a variant: `<Event Name> Project Plan | <Region> <Quarter> Field Event`
(e.g. `The Curated Table Project Plan | VIP Dinner AU Q2`). Follow whichever pattern the sibling
events in the same Drive folder use.

## Workflow

### 1. Pin down the event and its type

You need three things before anything else: **event name**, **event date**, **event type**.

Ask for whatever is missing rather than guessing — the entire timeline is derived from the date,
so a wrong date silently corrupts all 24–54 rows.

The type determines the task list and tab structure. The three types and how to tell them apart:

| Type | You can tell because | Reference |
| --- | --- | --- |
| **Proprietary** | Attentive owns the venue and the guest list. Holiday parties, dinners, retail activations, customer happy hours. ~4 weeks of runway. | `references/proprietary.md` |
| **Conference** | Someone else's show; Attentive sponsors or exhibits. There is an exhibitor portal with deadlines you don't control. ~15 weeks. | `references/conference.md` |
| **Summit / roadshow** | Attentive-run, multi-session, with an agenda and speakers. The Thread series. ~16 weeks, phased, owner-assigned. | `references/summit.md` |

Read only the one reference file that matches. Each holds the task list, the tab structure, and
the Overview Doc shape for that type.

If an event genuinely straddles two types — a conference sponsorship with its own ancillary
dinner, like eTail West — use the conference list and fold the dinner in as extra rows. Say that
you did.

### 2. Gather context before writing anything

Read `references/gathering-context.md` and work through it. It has the specific searches per
source, the SFDC campaign naming convention, and how to resolve conflicts between sources.

The thing that makes this skill worth running is that it reads the five places the planner would
otherwise have to open by hand. Skipping this step and producing an empty template is worse than
useless — it looks finished.

Keep a note of **where each fact came from** as you go. You will report this in step 6, and you
cannot reconstruct it later.

### 3. Compute the workback timeline

Every due date in every existing plan follows one rule, verified across LA Holiday Party, eTail
West and Thread NYC:

```
due_date = event_date - (weeks_out x 7 days)
```

Negative weeks-out means after the event (`-1` = the week following). Dates land on the same
weekday as the event, which is why the convention holds.

Use the script rather than doing date math by hand:

```bash
python3 scripts/workback.py --date 2026-12-03 --type proprietary
```

It prints the timeline as TSV. `--type` takes `proprietary`, `conference`, or `summit`.
Add `--extra "Confirm keynote speaker:6"` to append event-specific tasks at a given weeks-out.

### 4. Build the Project Plan workbook

**There is no tool that writes cells into an existing Google Sheet.** `update_file` changes
metadata only — title, parent folder, description. So the two-step "copy the template, then fill
it" does not work, and attempting it leaves an empty copy sitting in the planner's Drive.

What works, and is verified to preserve all tabs, merged cells, fonts, fills and currency
formats: fill a local copy of the template with openpyxl, then upload it as xlsx and let Drive
convert it to a native Google Sheet.

```bash
# 1. Download the template workbook (see gathering-context.md for which file to use as template)
#    via mcp__Google_Drive__download_file_content with
#    exportMimeType application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
#    Large files land in a tool-results file rather than context — decode from there.

# 2. Fill it
python3 scripts/fill_plan.py \
  --template template.xlsx \
  --out "Chicago Dinner 2026 | Project Plan.xlsx" \
  --values values.json

# 3. Upload with mcp__Google_Drive__create_file:
#    base64Content = the xlsx, parentId = the event folder,
#    contentMimeType = application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
#    Leave disableConversionToGoogleType unset so it becomes a real Google Sheet.
```

`fill_plan.py --describe template.xlsx` prints the tab and cell map first, so you write to the
right cells instead of guessing. Pass values as JSON keyed by `"Tab Name!A1"`.

Two things to know about the conversion: Google-specific features that xlsx has no slot for —
cell notes, checkboxes, some conditional formatting — do not survive. And formulas are preserved
as formulas, so a budget tab keeps calculating. If a template leans heavily on checkboxes (the
Sponsors tab uses TRUE/FALSE, which is fine; real checkbox widgets are not), say so rather than
letting the planner discover it.

### 5. Build the Overview Doc

Upload HTML and let Drive convert it — `create_file` with `contentMimeType: text/html` produces
a Google Doc with a real table for the Key Links block. Plain text loses the table.

The structure per type is in the type reference file. The shared shape:

```
<Event Name>
Overview Document

Event Date: <date>
Venue: <venue>

[two-column table: Key Links | Description]

Guest Experience:
  - <bullets, nested where the source nests them>
```

### 6. Report what you filled and what you did not

This is the part that makes the output trustworthy. End with:

- **Filled from source** — each non-obvious value and where it came from, as a short list.
  "Budget $25,000 — from the Oct 8 thread with Goop events team." Link the thread or message
  where you can.
- **Left as TBD** — every field you could not source, so the planner knows the gap is real and
  not an oversight.
- **Conflicts** — where two sources disagreed, both values and which you used.

Put `TBD` in the cell itself, never a plausible-looking guess. A budget figure, a venue contact,
a guest count and a payment status are the four places an invented value does actual damage.

## When updating an existing plan rather than creating one

The same skill covers "what's outstanding on eTail?" and "refresh the Thread plan."

Download the existing workbook, read the Timeline + Tasks tab, and reconcile it against what the
sources now say: tasks whose evidence of completion you can find (a placed print order in email,
a shipped tracking number in Slack) move to Complete; tasks whose due date has passed and show
no evidence stay put and get surfaced.

Do not silently flip a status to Complete on weak evidence — "we should order the signage" is not
an order. Report the status changes you are proposing and let the planner confirm, unless they
have said to just apply them.

When the plan already exists, prefer updating the existing file over creating a second one. Since
cells cannot be written in place, that means download → fill → upload as a new version, then
confirm with the planner before trashing or superseding the old file. Never trash the old file
without asking; a project plan is the only record of what was agreed.
