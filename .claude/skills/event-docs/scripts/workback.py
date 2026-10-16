#!/usr/bin/env python3
"""Build an event workback timeline from the event date.

Every due date in the existing Attentive event plans follows one rule, verified against
LA Holiday Party (Dec 3 2026), eTail West 2026 (Feb 23 2026) and Thread NYC 2026:

    due_date = event_date - (weeks_out * 7 days)

Negative weeks_out means after the event (-1 = the following week). Because the offset is a
whole number of weeks, every due date lands on the same weekday as the event, which is why the
convention holds in the real files.

Usage:
    python3 workback.py --date 2026-12-03 --type proprietary
    python3 workback.py --date 2026-02-23 --type conference --format csv
    python3 workback.py --date 2026-05-20 --type summit \
        --extra "Confirm keynote speaker:6" --extra "Ship gifting to venue:2"

Conference portal deadlines are deliberately NOT computed -- the show sets those dates, not the
workback. Pass --portal to emit them as rows with a blank due date for you to fill in from the
exhibitor portal.
"""

import argparse
import csv
import sys
from datetime import date, timedelta

# (weeks_out, task, notes)
PROPRIETARY = [
    (4, "Set Kickoff call with prelim stakeholders", ""),
    (4, "Venue Research", ""),
    (4, "Activations Research", ""),
    (4, "Create SFDC", ""),
    (4, "Create Slack Channel (if needed)", ""),
    (4, "Determine Meeting Strategy (if needed)", ""),
    (3, "Lock Venue", ""),
    (3, "Lock Activation", ""),
    (3, "Create Creative Brief and add to Monday for Brand", ""),
    (3, "Create Splash Page", ""),
    (3, "Add Event to the weekly Email", "Marketing Weekly Event Update for SDRs/AEs/CS"),
    (3, "Create Pre Event Email Copy and add to Outreach", ""),
    (3, "Determine swag needs", ""),
    (3, "Determine Printing Needs", ""),
    (3, "Place Printing Order", ""),
    (2, "Place Swag orders", ""),
    (2, "Track shipping on swag/printed assets", ""),
    (2, "Create Post Event Email Copy", ""),
    (1, "Set Debrief Call", ""),
    (-1, "Create Post Event Report", ""),
    (-1, "Share out Post Event Report", ""),
    (-1, "Finalize Budget Actuals", ""),
]

CONFERENCE = [
    (15, "Create Project Plan & Workback Timelines", ""),
    (15, "Venue Research", ""),
    (12, "Activations Research", ""),
    (10, "Create SFDC", ""),
    (10, "Create Slack Channel (if needed)", ""),
    (10, "Determine Meeting Strategy (if needed)", ""),
    (10, "Lock Offsite Venue", ""),
    (10, "Determine Ancillary Events", ""),
    (10, "Activation Research & Outreach", ""),
    (10, "Create Creative Brief and add to Monday for Brand", ""),
    (8, "Determine how many splash pages are needed", ""),
    (6, "Add Event to the weekly Email", "Marketing Weekly Event Update for SDRs/AEs/CS"),
    (6, "Create Pre Event Email Copy and add to Outreach", ""),
    (6, "Determine swag needs", ""),
    (6, "Determine Printing Needs", ""),
    (5, "Place Printing Order", ""),
    (5, "Place Swag orders", ""),
    (4, "Track shipping on swag/printed assets", ""),
    (2, "Create Post Event Email Copy", ""),
    (1, "Set Debrief Call", ""),
    (1, "List Upload Ticket & List Upload Template", "Post-Event List Upload Process Deck"),
    (-1, "Create Post Event Report", ""),
    (-1, "Share out Post Event Report & Email Follow Up Templates", ""),
    (-1, "Finalize Budget Actuals", ""),
]

# Set by the show, not by the workback formula. Weeks-out is indicative ordering only.
CONFERENCE_PORTAL = [
    (14, "Speaker Information, Headshot, Bio, presentation"),
    (6, "Tabletop / Booth Logo Deadline"),
    (6, "Company Logo, Description, Website, etc"),
    (5, "Staff Registration"),
    (4, "Hotel room block cut off date"),
    (1, "Tabletop / Booth Payment"),
    (1, "Exhibitor Orders Due (AV, Internet, Lead retrieval)"),
    (1, "Exhibition Activation"),
    (1, "Secondary hotel room block cut off date"),
]

# (phase, weeks_out, task, owner_role)
SUMMIT = [
    ("Foundation / Strategy", 16, "Build Project Plan", "Events"),
    ("Foundation / Strategy", 16, "Create Overview Document for all event note capture", "Events"),
    ("Foundation / Strategy", 16, "Fill in workback timeline", "Events"),
    ("Foundation / Strategy", 16, "Initial venue research", "Events"),
    ("Foundation / Strategy", 14, "Create SFDC", "Events"),
    ("Foundation / Strategy", 14, "Set kickoff call w/ stakeholders", "Events"),
    ("Foundation / Strategy", 14, "Activation research", "Events"),
    ("Foundation / Strategy", 14, "Agenda and session alignment", "Demand gen"),
    ("Infrastructure", 14, "Lock venue", "Events"),
    ("Infrastructure", 14, "Add event to the marketing calendar", "Events"),
    ("Infrastructure", 14, "Determine how many splash pages are needed and webpage strategy", "Events"),
    ("Infrastructure", 12, "Create Creative Brief and submit Monday ticket", "Events"),
    ("Foundation / Strategy", 12, "Determine ancillary events", "Events"),
    ("Infrastructure", 12, "Add event to wiki page", "Events"),
    ("Infrastructure", 12, "Monday ticket for marketing email calendar", "Comms"),
    ("Infrastructure", 12, "Create slack channel (if needed)", "Events"),
    ("Infrastructure", 12, "Draft hubspot emails and determine segmentation", "Demand gen"),
    ("Infrastructure", 12, "Create copy for internal comms", "Comms"),
    ("Marketing Launch", 12, "Publish registration pages", "Demand gen"),
    ("Marketing Launch", 12, "Calendar hold for execs", "Events"),
    ("Infrastructure", 10, "Determine A/V and production scope and lock", "Demand gen"),
    ("Infrastructure", 10, "Determine onsite meeting strategy (if needed)", "Events"),
    ("Infrastructure", 10, "Determine ancillary events and lock venues", "Events"),
    ("Marketing Launch", 10, "Create Outreach Templates for SDRs, AEs", "Comms"),
    ("Marketing Launch", 10, "Create Google doc templates for CS team", "Comms"),
    ("Marketing Launch", 10, "Send first promotional emails and launch internal comms", "Comms"),
    ("Promotion/Partner Activation", 10, "Check in with Partnerships Team on status of sales", "Partnerships"),
    ("Promotion/Partner Activation", 10, "Create RSVP list and share out with internal comms", "Comms"),
    ("Promotion/Partner Activation", 8, "Create promotional slide for CS and Rev", "Events"),
    ("Production & Logistics", 8, "Onsite activations locked", "Events"),
    ("Production & Logistics", 8, "Determine printing needs (directional signage, handouts, fabrication)", "Events"),
    ("Production & Logistics", 8, "Add printed items to design brief", "Events"),
    ("Marketing Launch", 8, "Add event to weekly email", "Comms"),
    ("Promotion/Partner Activation", 8, "Determine onsite branding", "Events"),
    ("Production & Logistics", 8, "Determine swag needs", "Events"),
    ("Marketing Launch", 8, "Ensure wiki page is updated", "Events"),
    ("Promotion/Partner Activation", 8, "Determine and schedule all splash email reminders", "Comms"),
    ("Promotion/Partner Activation", 6, "Lock partner participants & ensure vector file logo submission", "Partnerships"),
    ("Production & Logistics", 6, "Place swag orders", "Events"),
    ("Production & Logistics", 4, "Place printing order", "Events"),
    ("Final Event Prep", 4, "Track shipping on swag/printed assets", "Events"),
    ("Final Event Prep", 4, "Calendar hold for all internal attendees", "Events"),
    ("Final Event Prep", 3, "List Upload Ticket & List Upload Template", "Events"),
    ("Final Event Prep", 3, "Create copy for event reminder emails", "Comms"),
    ("Infrastructure", 2, "Create post event email copy for internal & external", "Comms"),
    ("Promotion/Partner Activation", 2, "Deploy reminder for ancillary & main events if not previously scheduled", "Comms"),
    ("Post Event", 1, "Set post event debrief call and add calendar holds", "Events"),
    ("Promotion/Partner Activation", 1, "Deploy second reminder email if not previously scheduled", "Comms"),
    ("Post Event", -1, "Create post event report Looker Dashboard", "Events"),
    ("Post Event", -1, "Share out post event report and follow up instructions", "Events"),
    ("Post Event", -1, "Finalize budget actuals", "Events"),
    ("Post Event", -1, "Add final budget to E&PM Budget", "Events"),
    ("Post Event", -1, "Add budget finals to Salesforce", "Events"),
]


def due_date(event_date, weeks_out):
    return event_date - timedelta(weeks=weeks_out)


def fmt(d):
    # Matches the existing sheets: "November 5, 2026"
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def parse_extra(values):
    out = []
    for raw in values or []:
        if ":" not in raw:
            sys.exit(f"--extra needs the form 'Task description:weeks_out', got: {raw!r}")
        task, _, weeks = raw.rpartition(":")
        try:
            out.append((int(weeks), task.strip(), "Added for this event"))
        except ValueError:
            sys.exit(f"--extra weeks_out must be an integer, got: {weeks!r} in {raw!r}")
    return out


def build_rows(event_date, kind, extra, include_portal):
    if kind == "summit":
        rows = [["Phase", "Description", "Status", "Weeks Out", "Due Date", "Owner"]]
        tasks = list(SUMMIT) + [("", w, t, "") for w, t, _ in extra]
        for phase, weeks, task, owner in sorted(tasks, key=lambda r: -r[1]):
            rows.append([phase, task, "Not Started", weeks, fmt(due_date(event_date, weeks)), owner])
        return rows

    source = PROPRIETARY if kind == "proprietary" else CONFERENCE
    tasks = sorted(list(source) + extra, key=lambda r: -r[0])
    rows = [["Description", "Status", "Weeks Out", "Due Date", "Notes"]]
    for weeks, task, notes in tasks:
        rows.append([task, "Not Started", weeks, fmt(due_date(event_date, weeks)), notes])

    if kind == "conference" and include_portal:
        rows.append(["", "", "", "", ""])
        rows.append(["Portal Deadlines", "Status", "Weeks Out", "Due Date", "Notes"])
        for weeks, task in CONFERENCE_PORTAL:
            # Blank due date on purpose: the show sets these, not the workback formula.
            rows.append([task, "Not Started", weeks, "TBD - confirm in exhibitor portal", ""])
    return rows


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--date", required=True, help="Event date, YYYY-MM-DD. First day for multi-day events.")
    p.add_argument("--type", required=True, choices=["proprietary", "conference", "summit"])
    p.add_argument("--extra", action="append", metavar="TASK:WEEKS",
                   help="Append an event-specific task, e.g. 'Confirm keynote:6'. Repeatable.")
    p.add_argument("--format", default="tsv", choices=["tsv", "csv"])
    p.add_argument("--portal", action="store_true",
                   help="Conference only: also emit the Portal Deadlines section.")
    args = p.parse_args()

    try:
        event_date = date.fromisoformat(args.date)
    except ValueError:
        sys.exit(f"--date must be YYYY-MM-DD, got: {args.date!r}")

    rows = build_rows(event_date, args.type, parse_extra(args.extra), args.portal)
    w = csv.writer(sys.stdout, delimiter="\t" if args.format == "tsv" else ",", lineterminator="\n")
    w.writerows(rows)

    first = max(r[1] if args.type == "summit" else r[0]
                for r in (SUMMIT if args.type == "summit" else
                          (PROPRIETARY if args.type == "proprietary" else CONFERENCE)))
    print(f"\n# {len(rows) - 1} tasks. Work starts {fmt(due_date(event_date, first))} "
          f"({first} weeks out); event {fmt(event_date)}.", file=sys.stderr)


if __name__ == "__main__":
    main()
