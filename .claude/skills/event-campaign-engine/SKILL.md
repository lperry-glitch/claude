---
name: event-campaign-engine
description: Use when someone on Attentive's Events/Field Marketing team wants to plan a marketing event — sponsoring a retail/ecommerce conference, a regional field dinner for enterprise prospects, or a session/track at Attentive's own event (Thread). Runs a 3-step pipeline (research → plan → assets) and saves everything under /events/[event]/. Triggers on requests like "build an event campaign," "plan our presence at [conference]," "help me plan a Thread session," "field dinner for [account list]," or "event campaign engine."
user-invocable: true
disable-model-invocation: false
---

# Event Campaign Engine

A 3-step pipeline for turning a single event decision into a full campaign: research, plan, and customer-facing assets. Each step builds on the output of the last. This skill is process guidance, not canned copy — do real research and write real, specific content each time; never fill sections with placeholder text.

Context: the user runs Attentive's own events (e.g. Thread, Attentive's flagship customer conference) and field/industry events. Attentive is an AI-powered SMS + email marketing platform for retail and ecommerce brands.

## Step 0 — Pick the event

If the user hasn't named a specific event, suggest 2-3 concrete scenarios spanning the different shapes this takes, e.g.:
- Sponsoring/exhibiting at a named third-party retail/ecommerce conference (best when you need competitive intel — who else is sponsoring, what they're pitching).
- A regional field dinner or roundtable for enterprise retail/ecommerce prospects.
- A session/track at Attentive's own event (Thread) — different research angle: owned audience/agenda data rather than competitive intel.

Recommend which to start with and say why, then use `AskUserQuestion` (or just wait for a reply) to confirm before doing any research. If the user already named an event, skip straight to Step 1 — no need to re-confirm.

Slugify the event name for the output path, e.g. `/events/thread-2026/`, `/events/nrf-2027/`, `/events/nyc-enterprise-dinner-fall26/`.

## Step 1 — Event Research → `event_research.md`

Research the event and its audience:
- **Who attends**: roles, seniority, brand types/verticals.
- **What they care about**: pain points, priorities, what content/messaging resonates with this audience right now.
- **Agenda themes**: past and (if findable) upcoming themes, format, notable speakers/sessions.
- **Competitive landscape**: which competitors sponsor/exhibit/attend (for a third-party conference), or — for an owned event like Thread — what comparable competitor-run customer conferences exist and what they emphasize in their own content, since that's the mindshare Attentive is competing against even without a shared floor.
- **Best-practice formats/benchmarks**: what session/event formats and structures actually drive engagement for this kind of audience, and common mistakes to avoid.

Use WebSearch/WebFetch (directly or via a research subagent) rather than relying on memory — event details, dates, and competitor moves change often. Flag anywhere information is sparse or inferred rather than confirmed, and cite sources.

End the document with a section titled **"The wedge for standing out"** — the one or two angles that are genuinely hard for competitors to replicate, given everything above.

## Step 2 — Event Plan → `event_plan.md`

Using the research, produce:
- **Goals** for this specific event (pipeline, brand, retention/expansion, etc. — pick what actually fits).
- **Target-account / invite criteria** — who specifically should be invited or targeted, tied to the audience profile from Step 1.
- **Experience/session concept** — the specific format and topic, informed by the "wedge" and the format benchmarks from Step 1. If there's a real choice to make here (e.g. case-study fireside vs. interactive workshop), surface the tradeoff and get a quick confirm from the user before finalizing — this decision shapes Step 3.
- **Pre / during / post plan** — concrete timeline and activities for each phase.
- **Staffing** — who's needed and in what role.
- **Success metrics** — specific, measurable, tied back to the goals (avoid vanity metrics like booth traffic/swag counts unless directly justified).

## Step 3 — Event Assets → `event_assets.md`

Before writing any copy, load the `attentive-brand-artifacts` skill (or read its `references/voice-and-writing.md` directly if the skill isn't invocable in this context) to match Attentive's actual brand voice — do not invent a generic marketing voice.

Produce, using the plan from Step 2:
- **Invite email sequence**: save-the-date → invite → reminder.
- **2-3 LinkedIn promo posts.**
- **Booth/session talking points.**
- **Post-event follow-up sequence**, segmented by engagement level (e.g. attended + engaged, attended only, registered but no-show).

## Output conventions

- Save all three files under `/events/[event-slug]/` at the repo root: `event_research.md`, `event_plan.md`, `event_assets.md`.
- Each file should stand alone and be genuinely usable by the team (real recommendations, not hedged summaries), while still being clearly built on the prior step's specifics rather than generic event-marketing advice.
- This skill lives in the repo's local `.claude/skills/`, so it travels with the repo across Claude Code CLI, web, and any other environment where this project is checked out.
