#!/usr/bin/env python3
"""Fill an event Project Plan workbook locally, for upload to Drive as a Google Sheet.

Why this exists: the Drive connector has no tool that writes cells into an existing Google
Sheet -- update_file changes metadata only (title, parent, description). So "copy the template
then fill it" leaves an empty copy in the planner's Drive. Instead: download the template as
xlsx, fill it here, and upload with create_file so Drive converts it back to a native Sheet.

This round-trip is verified to preserve tabs, merged cells, fonts (Montserrat), fills, currency
number formats and formulas. It does not preserve cell notes, checkbox widgets, or some
conditional formatting -- xlsx has no slot for those.

Typical sequence:

    # 1. See what you are writing into. Tab names have trailing spaces; copy them from here.
    python3 fill_plan.py --describe template.xlsx

    # 2. Start from a template, or strip a past event's data to reuse its structure
    python3 fill_plan.py --template past-event.xlsx --out new.xlsx --clear-data

    # 3. Write the header block and the timeline
    python3 fill_plan.py --template new.xlsx --out "Chicago 2026 | Project Plan.xlsx" \
        --values values.json \
        --timeline timeline.tsv --timeline-tab "Timeline + Tasks"

values.json is keyed by "Tab Name!CellRef":

    {
      "Project Plan !B1": "December 3, 2026",
      "Project Plan !B2": "The Goop Brentwood",
      "Project Plan !B3": 25000,
      "Project Plan !B4": "Strengthening Customer Relationships\\nDrive New Pipeline"
    }

Numbers stay numbers so budget formulas keep working -- write 25000, not "$25,000.00". The
cell's existing currency format renders it. A newline inside a string makes a multi-line cell,
which is how Objectives and KPIs are stored in the real files.
"""

import argparse
import csv
import json
import sys

try:
    import openpyxl
except ImportError:
    sys.exit("openpyxl is required:  pip install openpyxl")


def describe(path, max_rows=6, max_cols=8):
    wb = openpyxl.load_workbook(path, data_only=False)
    print(f"{path}: {len(wb.sheetnames)} tabs\n")
    for name in wb.sheetnames:
        ws = wb[name]
        # repr() so trailing spaces in tab names are visible -- they are real and load-bearing
        print(f"=== {name!r}  ({ws.max_row} rows x {ws.max_column} cols)")
        if ws.merged_cells.ranges:
            print(f"    merged: {', '.join(str(r) for r in list(ws.merged_cells.ranges)[:6])}")
        for row in ws.iter_rows(min_row=1, max_row=min(max_rows, ws.max_row),
                                max_col=min(max_cols, ws.max_column)):
            cells = [f"{c.coordinate}={str(c.value)[:38]}" for c in row if c.value is not None]
            if cells:
                print("    " + "  ".join(cells))
        print()


def is_formula(value):
    return isinstance(value, str) and value.startswith("=")


def clear_data(ws, header_rows=1):
    """Blank out data values while keeping headers, formulas and formatting.

    Heuristic, and it can be wrong on tabs that don't start with a header row -- always check
    --describe output afterwards rather than trusting it blindly.
    """
    cleared = 0
    for row in ws.iter_rows(min_row=header_rows + 1):
        for cell in row:
            if cell.value is not None and not is_formula(cell.value):
                cell.value = None
                cleared += 1
    return cleared


def apply_values(wb, values):
    for key, value in values.items():
        if "!" not in key:
            sys.exit(f"values key must be 'Tab Name!A1', got: {key!r}")
        tab, _, ref = key.rpartition("!")
        if tab not in wb.sheetnames:
            sys.exit(f"no tab named {tab!r}. Tabs are: {[repr(n) for n in wb.sheetnames]}")
        wb[tab][ref] = value
        print(f"  {tab!r}!{ref} = {str(value)[:60]}", file=sys.stderr)


def apply_timeline(ws, rows, start_row, write_header):
    if not write_header:
        rows = rows[1:]
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            if val == "":
                continue
            # Weeks Out is numeric in the real sheets; keep it that way so it sorts and filters
            cell = ws.cell(row=start_row + i, column=j + 1)
            try:
                cell.value = int(val)
            except (TypeError, ValueError):
                cell.value = val
    return len(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--describe", metavar="FILE", help="Print the tab and cell map, then exit.")
    p.add_argument("--template", help="Source workbook to fill.")
    p.add_argument("--out", help="Where to write the filled workbook.")
    p.add_argument("--values", help="JSON file of {'Tab!A1': value} assignments.")
    p.add_argument("--clear-data", action="store_true",
                   help="Blank data rows on every tab, keeping headers, formulas and formatting.")
    p.add_argument("--clear-tabs", help="Comma-separated tabs to clear; default is all.")
    p.add_argument("--timeline", metavar="TSV", help="Timeline rows from workback.py.")
    p.add_argument("--timeline-tab", default="Timeline + Tasks")
    p.add_argument("--timeline-start-row", type=int, default=1)
    p.add_argument("--timeline-skip-header", action="store_true",
                   help="Don't write the header row (the template already has one).")
    args = p.parse_args()

    if args.describe:
        describe(args.describe)
        return
    if not (args.template and args.out):
        sys.exit("need --template and --out (or --describe)")

    wb = openpyxl.load_workbook(args.template, data_only=False)

    if args.clear_data:
        tabs = [t.strip() for t in args.clear_tabs.split(",")] if args.clear_tabs else wb.sheetnames
        for name in tabs:
            if name not in wb.sheetnames:
                sys.exit(f"no tab named {name!r}")
            n = clear_data(wb[name])
            print(f"  cleared {n} values from {name!r}", file=sys.stderr)

    if args.values:
        with open(args.values) as fh:
            apply_values(wb, json.load(fh))

    if args.timeline:
        if args.timeline_tab not in wb.sheetnames:
            sys.exit(f"no tab named {args.timeline_tab!r}. "
                     f"Tabs are: {[repr(n) for n in wb.sheetnames]}")
        with open(args.timeline, newline="") as fh:
            sample = fh.read(2048)
            fh.seek(0)
            delim = "\t" if "\t" in sample.splitlines()[0] else ","
            rows = [r for r in csv.reader(fh, delimiter=delim) if not (r and r[0].startswith("#"))]
        n = apply_timeline(wb[args.timeline_tab], rows, args.timeline_start_row,
                           not args.timeline_skip_header)
        print(f"  wrote {n} timeline rows to {args.timeline_tab!r} "
              f"from row {args.timeline_start_row}", file=sys.stderr)

    wb.save(args.out)
    print(f"\nwrote {args.out}", file=sys.stderr)
    print("Upload with mcp__Google_Drive__create_file: base64Content = this file, "
          "parentId = the event folder, contentMimeType = "
          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", file=sys.stderr)


if __name__ == "__main__":
    main()
