# Thread New York 2026 — Environment Reference

A 19-slide visual portfolio of the Thread World Tour New York stop, built for
reuse on future Thread environments and as a brand team reference.

Source of record: `Thread New York 2026 - Environment Reference.pptx`
Built on the canonical 2026 Attentive company deck template. Every slide is a
duplicated canonical template slide — no custom layouts.

## To get it into Google Slides

1. Upload the `.pptx` to the Thread NY 2026 Drive folder.
2. Right-click it → **Open with → Google Slides**.
3. Drive's converter keeps Inter and the exact positioning.

## To drop the photos in

Each photo frame currently holds a cream placeholder labelled with the file to
insert. In Slides: click the placeholder → **Insert → Image → Drive** → pick the
file → it fills the existing frame and keeps the template crop.

The photos live in `Photos/` alongside this deck. Filenames below are shortened —
each is `Attentive Thread Event – by @jennamurray-NNN.jpg`.

| Slide | Section | Frames | Photos to insert |
| --- | --- | --- | --- |
| 3 | The numbers | 1 | 845 |
| 4 | What Thread is | 1 (wide) | 829 |
| 6 | Hudson Yards | 1 | 800 |
| 8 | Arrival | 3 | 801, 802, 804 |
| 9 | The room | 4 | 807, 838, 885, 892 |
| 13 | The evening | 4 | 902, 905, 935, 940 |

14 frames, 14 photos.

**The photo-to-slide mapping is an assumption, not a fact.** Drive is blocked at
this environment's proxy and image reads came back empty, so the photos could not
be viewed. They were assigned by shot number on the assumption that the sequence
runs chronologically — low numbers early in the day, high numbers at the bash.
Check them against the actual images and swap any that land in the wrong section.
The captions on slides 8, 9, and 13 were written to the section, not to the frame,
so they may need adjusting once the real photos are in.

## Slide map

| # | Canonical | Content |
| --- | --- | --- |
| 1 | 16 | Cover |
| 2 | 30 | Breaker — The event |
| 3 | 80 | The numbers — 419 RSVPs, 211 customers, 106 prospects, 32 partners |
| 4 | 73 | What Thread is — launched 2022, four 2026 cities |
| 5 | 31 | Breaker — The space |
| 6 | 78 | Hudson Yards — one floor, short walks, three formats, a long day |
| 7 | 71 | The door — five check-in shifts, staffing per block |
| 8 | 86 | Arrival — check-in, lunch rounds, networking |
| 9 | 88 | The room — stage, screen, sightlines, breaks |
| 10 | 32 | Breaker — The activations |
| 11 | 70 | The morning — SoulCycle, Plaza M, Fellow Barber, Sunday Nails |
| 12 | 84 | What's in Store — Coach, TUMI, AG Jeans, Faherty |
| 13 | 87 | The evening — cocktail hour, food stations, Magnolia Bakery, Bash |
| 14 | 72 | Partners — Simon Data, Bazaarvoice, Recharge, Friendbuy, Shopify |
| 15 | 33 | Breaker — What to repeat |
| 16 | 60 | Closing statement |
| 17 | 159 | Run of show — five phases across the day |
| 18 | 150 | What to repeat — three takeaways |
| 19 | 128 | Closer |

## Where the content came from

All figures and details are drawn from existing event material, not invented:

- **Thread NYC 2026 - Internal Prep** (Slides) — RSVP breakdown, the morning
  activation list, What's in Store hosts, partner roster, full schedule,
  registration desk shifts.
- **Thread NY 2026 - Customer Follow Up** (Sheet) — confirmed the event date
  (May 20, 2026) and campaign name via the Salesforce campaign field.

Deliberately left out: attendee names, email addresses, CS/sales tiers, and
revenue-band data from the follow-up sheet. None of it belongs in a portfolio.

Also left out: the "~150 morning" and "~250 afternoon" attendance figures from
the prep deck, which are labelled estimates there. The 419/211/106/32
registration numbers are stated as actuals, so those are the ones used.

The prep deck's marquee guest speaker was still a placeholder (`XXX`), so no
speaker is named anywhere in this deck.

## Build

```bash
# python-pptx in an isolated venv (nothing installed into the system runtime)
uv venv pptxenv && uv pip install --python pptxenv/bin/python python-pptx

cd <skill>/attentive-slide-builder
python preflight_lint.py  plan.json          # CLEAN — 174 fields, 0 overflow, 0 unmatched
python build_from_plan.py plan.json out.pptx
python polish.py out.pptx
python verify_fills.py out.pptx              # no fill defects across 19 slides
```

`plan.json` is the editable source for the copy. `assets/` holds the 14
placeholder PNGs, generated at each frame's exact aspect ratio.

## QA status

Passed: preflight (no overflow, every placeholder key matched), post-build
structural verification, `verify_fills` (no leftover template copy, no duplicated
titles), and a custom audit — 19 slides at exactly 10 × 5.625in, all shape names
canonical, 14 images embedded on the intended slides, zero empty picture
placeholders, zero leftover placeholder strings.

**Not done: a visual render check.** `libreoffice-impress` is not installed in
this environment (the untouched template fails to convert too), so no slide was
rendered and eyeballed, and the skill's guidance is not to install system
software for a deck request. Two things that only a render catches are therefore
unverified: multi-line header line counts, and whether any title crowds a picture
frame. Worth a scroll-through after the Slides conversion, which is also when the
real fonts appear.
