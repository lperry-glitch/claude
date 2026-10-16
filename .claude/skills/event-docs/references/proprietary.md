# Proprietary / owned events

Attentive owns the venue and the guest list: holiday parties, VIP dinners, retail activations,
customer happy hours. Short runway — the task list starts 4 weeks out.

Reference event: **LA Holiday Party, Dec 3 2026, goop Brentwood, $25,000.**

## Project Plan tabs

| Tab | Contents |
| --- | --- |
| `Project Plan ` | Event Date, Venue, Budget, Objectives, KPIs, Description in A1:B6. Key Links block in C1:D3. |
| `Timeline + Tasks` | Description, Status, Weeks Out, Due Date, Notes. |
| `Budget Tracker ` | Total/Remaining/Contingency header, then Item, Estimated Cost, Description, Actual Cost, Payment Status, Notes. |
| `Agenda` | Time, Description, Owner. |
| `Sessions` | Session Title, Abstract, Speaker, Speaker Title, Time. Often thin or unused for a party. |
| `1:1 Meetings` | Company, Name, Title, Time requested, Time Assigned, CS Assigned. |
| `Printed Assets` | Asset, Description, Quantity, Payment Status. |
| `Digital Assets` | Item, Use Case. |
| `Shipping/Tracking` | Item, Qty, Tracking Link, Status. |

Note the trailing spaces in `Project Plan ` and `Budget Tracker ` — they are part of the real tab
names. `fill_plan.py --describe` prints them verbatim; copy from there.

## Timeline + Tasks

Status values in use: `Complete`, `In Progress`, `Not Started`, `Not Applicable`. Default a task
to `Not Started` unless a source shows otherwise. Use `Not Applicable` rather than deleting a row
— the row documents that the decision was made.

| Weeks Out | Task | Notes field convention |
| --- | --- | --- |
| 4 | Set Kickoff call with prelim stakeholders | |
| 4 | Venue Research | |
| 4 | Activations Research | |
| 4 | Create SFDC | SFDC campaign name (see below) |
| 4 | Create Slack Channel (if needed) | `#channel-name` once created |
| 4 | Determine Meeting Strategy (if needed) | |
| 3 | Lock Venue | |
| 3 | Lock Activation | |
| 3 | Create Creative Brief and add to Monday for Brand | Name of the creative brief doc |
| 3 | Create Splash Page | |
| 3 | Add Event to the weekly Email | `Marketing Weekly Event Update for SDRs/AEs/CS` |
| 3 | Create Pre Event Email Copy and add to Outreach | Name of the copy doc |
| 3 | Determine swag needs | |
| 3 | Determine Printing Needs | |
| 3 | Place Printing Order | |
| 2 | Place Swag orders | |
| 2 | Track shipping on swag/printed assets | |
| 2 | Create Post Event Email Copy | Name of the follow-up copy doc |
| 1 | Set Debrief Call | |
| -1 | Create Post Event Report | |
| -1 | Share out Post Event Report | |
| -1 | Finalize Budget Actuals | |

The SFDC campaign naming convention, from the LA plan's Notes field:

```
Event - Proprietary - <M.D.YY> - <Event Name>
```

e.g. `Event - Proprietary - 12.3.26 - LA Holiday Party`. Derive and propose it; note that you
derived it rather than read it.

## Objectives and KPIs

These recur nearly verbatim across proprietary events, so carry them forward unless a kickoff
note or email says otherwise:

**Objectives** — Strengthening Customer Relationships / Expand Customer Knowledge of Attentive /
Drive New Pipeline / Showcase Company Culture / Gain Feedback and Insights

**KPIs** — vary by event, and these are the ones worth sourcing rather than assuming. LA used
Executive Engagement and New Pipeline. If no source states them, put the objectives in and leave
KPIs as TBD rather than copying LA's.

## Overview Doc shape

```
<Event Name>
Overview Document

Event Date: <date>
Venue: <venue>

[table: Key Links | Description]
  Key Links cell, as a bulleted list of links:
    - SFDC
    - Drive Folder
    - Splash Page
    - Creative Brief
    - Project Plan
    - Venue Website
  Description cell: one or two sentences on the guest proposition — what the guest
  actually gets. LA: "A curated holiday shopping experience at goop in Brentwood! Each
  guest will receive a $100 gift card to shop the thoughtfully selected collection, with
  complimentary gift wrapping and personalization available to add an extra-special touch."

Guest Experience:
  - Arrival cocktails
      - Champagne, White Wine, Red Wine
  - <activation, with per-guest value if there is one>
  - <food and beverage>
```

Guest Experience is the heart of the doc for this type — it is what gets read aloud on a kickoff
call. Build it from the venue proposal or catering thread, nesting sub-items the way the source
does (drinks listed under "arrival cocktails"). If the proposal is a PDF attachment, read it.

A proprietary event's Overview Doc often has a second tab for a sibling event in the same series
(the LA doc has an empty "Tab 2"). If the series has other cities, set up the tab and leave it
for the planner.
