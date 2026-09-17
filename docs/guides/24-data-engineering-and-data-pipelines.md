---
chapter: 24
title: "Test — Ingest customer asset context safely"
slug: 24-data-engineering-and-data-pipelines
lesson: docs/lessons/24-data-engineering-and-data-pipelines.md
audio: media/24-data-engineering-and-data-pipelines.mp3
type: test
---

# Chapter 24 test — Ingest customer asset context safely

This is a test, not a tutorial. It states the goal, the constraints, the state you start from, and the artifacts you must produce. It does not tell you how. Work from the lesson, the official documentation for whatever runtime you chose in earlier chapters, and your own judgement. Hints are at the very end, inverted so you do not read them by accident. Open them only after you are genuinely stuck on a specific decision, and only one at a time.

## Goal

FieldOps Copilot must be able to enrich an incident with context about the physical or logical asset it concerns, and must be able to tell the difference between an asset it does not know about and an asset inventory that is out of date.

Build a pipeline that ingests a synthetic customer asset inventory into a read model inside your system, safely and repeatably, and wire it into the incident flow through a single defined identifier.

## Starting state

You begin from your chapter 23 state: a React operator workspace, a secured Node.js API, PostgreSQL as the system of record for incidents and audit events, an optional cache, a bounded triage agent with a read-only lookup tool, retrieval over synthetic runbooks, an evaluation gate, and a latency and cost budget.

You add to that state. Do not restructure what already works, and do not modify the incident table's role as the operational system of record.

## Constraints

1. **Synthetic data only.** Generate the asset inventory yourself. It must be realistic in shape, including messy values, and entirely invented in content. No real customer data, and no real customer system is contacted.
2. **The source is external.** Treat your synthetic inventory as a system you do not control: read it, never write to it, and never assume it is correct.
3. **Four separable stages.** Extract, validate, transform, and load must be distinguishable units with a clear boundary between them. Extract performs no validation and no reshaping.
4. **Idempotent by construction.** Running the same source twice must produce the same read model state, including the same row count.
5. **Records are rejected individually, batches are rejected collectively.** One invalid record must not discard the batch. A batch whose failure rate exceeds a threshold you choose and document must abort the run without loading.
6. **Nothing is silently dropped or silently defaulted.** Every rejected record is retained with a reason. Every defaulted value is marked as defaulted.
7. **The read model is read-only to the application.** No application code path may write to it. It must be safe to drop and rebuild entirely from the source.
8. **The join is by identifier only.** No fuzzy or name-based matching between incidents and assets anywhere in the system.
9. **Extraction is bounded.** A row limit, a time bound, and a timeout. The job must be disableable by configuration without a code change.
10. **Unknown extra fields are tolerated. Missing required fields are not.**
11. **No secret or connection credential appears in source control, logs, or the run record.**

## Required artifacts

Produce all of these. They are what you will be assessed on and what carries forward into chapter 25.

1. **An asset contract document.** Required fields, optional fields, types, allowed values, the identity field, the rule for each violation, the duplicate-within-batch rule, the deletion signal, the batch failure threshold, and the freshness tolerance stated as a number with the reasoning behind it.
2. **A synthetic source** containing at least 40 asset records, of which at least 6 are deliberately problematic across at least 4 distinct defect classes.
3. **The ingestion job**, with the four stages separable and independently exercisable.
4. **A read model table** carrying lineage on every row: source name, source revision or export identifier, ingestion timestamp, and job run identifier.
5. **A run record** per execution: start and end time, counts for extracted, accepted, rejected, inserted, updated, and marked-absent, the result of each batch assertion, and a final status.
6. **A quarantine store** holding rejected records with a reason and the offending field, readable by a non-engineer.
7. **At least three batch-level assertions**, one of which must detect a source that has stopped changing.
8. **Asset enrichment in the incident flow**, exposed through the agent's read-only lookup path, returning asset context together with the freshness of the read model.
9. **A staleness behavior**: a documented threshold, a visible last-refreshed indicator for the operator, and agent output that qualifies its asset context when the read model is stale.
10. **A short decision note** recording your cadence choice and its justification, and one paragraph on what would have to change before this pipeline touched real customer data.

## Required demonstrations

Capture evidence for each. A terminal transcript, a test output, or a short screen capture is sufficient.

- **D1 — Repeat run.** Run the unchanged source twice. Show identical read model state and row count after each.
- **D2 — Single bad record.** Introduce one record with an unrecognized criticality value. Show it quarantined with a readable reason and show every other record loaded.
- **D3 — Unexpected column.** Add a field the contract does not know about. Show the run succeeding and the field ignored.
- **D4 — Duplicate identity.** Place two records with the same identity key in one batch. Show your documented rule applied and exactly one row resulting.
- **D5 — Deletion.** Remove a record from the source. Show it marked absent rather than silently retained or hard deleted.
- **D6 — Frozen feed.** Present the same unchanged source repeatedly past your freshness tolerance. Show the assertion firing.
- **D7 — Batch abort.** Corrupt enough records to exceed your threshold. Show the run aborting with nothing loaded.
- **D8 — Unknown versus stale.** Query an identifier that does not exist, and query a valid identifier while the read model is stale. Show that the agent's output distinguishes the two cases in language an operator would understand.
- **D9 — Degraded fallback.** Make the read model unavailable. Show that incident intake and triage still work, with asset context marked unavailable.

## Rubric

Score each line. Anything below *Meets* means the artifact is not finished.

| # | Criterion | Does not meet | Meets | Exceeds |
|---|---|---|---|---|
| 1 | Contract completeness | Validation exists only in code | Every required field, allowed value, violation rule, and threshold is written down before the code | Contract is versioned and a change to it is reviewable as a diff |
| 2 | Stage separation | Fetch, clean, and load are interleaved | Four stages with clear boundaries; transform can be replayed against retained raw output | Raw extract output is retained with its own lineage and a replay is demonstrated |
| 3 | Idempotency | Second run changes row count | D1 passes | Load is a verified swap or transactional upsert, and a partial failure leaves no half-loaded state |
| 4 | Record-level handling | Bad rows crash the run or vanish | D2 passes with a readable reason | Quarantine reasons are grouped by class with counts and first-seen dates |
| 5 | Batch-level assertions | None, or only row counts | Three assertions including frozen-feed detection (D6) | Thresholds derived from observed history rather than guessed constants |
| 6 | Schema drift tolerance | Unknown column breaks the run | D3 passes and a missing required field is rejected | Unknown columns are logged once as a change signal rather than ignored entirely |
| 7 | Lineage and run record | Rows cannot be traced to a run | Every row carries source, revision, ingestion time, and run id; every run produces a record | A single query answers "which run produced this value and what else did it change" |
| 8 | Deletion handling | Removed assets persist invisibly | D5 passes | Absence is distinguishable from never-seen, with the date first absent |
| 9 | Join discipline | Any name or fuzzy matching exists | Join is by identifier only; intake resolves free text to an identifier with operator confirmation | Unresolvable references are surfaced to the operator rather than guessed or dropped |
| 10 | Freshness semantics | Agent cannot distinguish unknown from stale | D8 passes | Freshness is a first-class field on every enrichment response and appears in the operator interface |
| 11 | Failure containment | Broken feed blocks intake | D9 passes | Degradation is explicit in the agent output and recorded as an event, not just absent |
| 12 | Operational safety | Unbounded query, no off switch | Row limit, time bound, timeout, and configuration-level disable | A dry-run mode reports what would change without writing |
| 13 | Separation of concerns | Application writes to the read model | Read model is read-only and rebuildable from source | Rebuild from empty is demonstrated and timed |
| 14 | Cadence reasoning | Schedule chosen by habit | Freshness tolerance stated as a number with justification; cadence follows from it | Tolerance is traced to a specific operator decision it protects |
| 15 | Customer readiness | No statement about real data | Written paragraph on what must change before real data flows | Names the data owner role, the approval required, and the access scope requested |

## Stop conditions

Stop and reconsider your approach if any of these are true:

- You are building a generic pipeline framework rather than one pipeline.
- You have added a second datastore that the contract does not require.
- Your validation rules live only inside database constraints.
- You are tempted to match assets to incidents by name because the identifiers are inconvenient.
- Your job catches every exception and always exits successfully.

## Carry forward

Chapter 25 orchestrates exactly what you build here: it will add scheduling, dependency ordering, bounded retries, failure notification, and a controlled backfill over a historical source date. Keep the four stages separable, keep the run record, and keep the synthetic source generator, because you will need to produce several historical source dates from it.

---

## Hints

Read these only after a real attempt. Each line is reversed. Reverse it to read it.

1. Identity and repeat runs: `.tresni no gnihton od dna yek ytitnedi eht no tcilfnoc :puorg eno sa hctab elohw eht taert ,wor yb wor gnigrem fo daetsnI`
2. Frozen feed detection: `.eulav tsetal eht ,tsap eht ni raf oot si pmatsemit deifidom nwo s'ecruos eht fo mumixam eht rehtehw kcehc ,dedaol swor gnirapmoc fo daetsnI`
3. Deletion signal: `.swor eteled reven ;nur tahs ni nees ton saw ti fi etad-tnesba-tsrif a tes dna ,tohspans lluf a retfa nur dnoces a sa ecnesba tekraM`
4. Unknown versus stale: `.egaugnal gnitfard erofeb tsrif epahs esnopser eht xiF .gnissim si dna ,ssenhserf ,dnuof-ton neewteb hsiugnitsid taht sdleif eerht nruter dluohs esnopser pukool ehT`
5. Batch abort: `.dedaol si gnihton os ,noitcasnart a nihtiw daol eht nur dna ,egats daol eht erofeb dlohserht eht kcehC`
6. Quarantine readability: `.dleif eht eman dna ,eulav gnidneffo eht etouq ,elur tcartnoc eht etats :secnetnes hsilgnE sa snosaer etirW`
7. Degraded fallback: `.dedivorp ton saw txetnoc tessa taht gnitats dleif a htiw esnopser a nruter ,worht ton od :eruliaf no tluafed sti dna ,tuoemit nwo sti htiw ,ecafretni na dniheb pukool tessa eht ecalP`
