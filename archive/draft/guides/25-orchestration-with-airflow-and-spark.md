---
chapter: 25
title: "Test — Orchestrate the asset-context refresh"
slug: 25-orchestration-with-airflow-and-spark
lesson: docs/lessons/25-orchestration-with-airflow-and-spark.md
audio: media/25-orchestration-with-airflow-and-spark.mp3
type: test
---

# Chapter 25 test — Orchestrate the asset-context refresh

This is a test, not a tutorial. It gives you the goal, the constraints, the state you start from, the artifacts to produce, and the rubric you will be judged against. It does not give you the method. Hints are at the end, reversed, so you do not read them by accident.

## Goal

Turn the chapter 24 ingestion job into a scheduled, dependency-aware, recoverable workflow that a customer's operations team could run without you, and produce measured evidence about whether distributed processing belongs in this deployment.

## Starting state

Your chapter 24 result: a synthetic asset source generator, an asset contract, a four-stage ingestion job, a read model with lineage, a quarantine, a run record, batch-level assertions, and agent enrichment that reports freshness.

If your chapter 24 job reads the current clock anywhere, fix that first. Everything in this test depends on the target period being an input.

## Constraints

1. **Target date is a parameter.** No task may read the wall clock to decide which data it is processing. The same target date must always produce the same result.
2. **The quality gate precedes publication.** Batch assertions run against transformed data before anything becomes visible to readers.
3. **Load and publish are separate.** Readers see either the previous complete version or the new complete version. Never a partial one.
4. **Retry policy is per task and justified in writing.** A task that is unsafe to repeat gets no retries, and you must be able to say why each policy is what it is.
5. **Every wait has a deadline.** A task that waits for an external condition must fail when its deadline expires. No unbounded waiting.
6. **Catchup and concurrency are set explicitly.** Backfill must not be able to launch an unbounded number of simultaneous runs against the source.
7. **Synthetic data only.** No scheduled workflow points at any real system.
8. **Newer data is not overwritten by an older backfill.** State the rule and enforce it.
9. **Failure is visible without opening a log file.** A notification carries workflow, target date, task, counts, and the first line of the reason.
10. **Two severity levels exist.** Distinguish a routine failure from one that has breached the freshness tolerance, and route them differently.

## Required artifacts

1. **A dependency graph specification**: every task, its inputs, its outputs, its upstream dependencies, its retry policy with justification, and its timeout. This must be precise enough that another engineer could implement it in a different tool.
2. **A working implementation**, either in a local Airflow-compatible environment or in the simpler scheduled-invocation form described in the lesson. If you choose the simpler form, your specification document must state the trigger conditions under which you would graduate to a full orchestrator.
3. **Run history** showing, per execution: target date, per-task status, start and end times, attempt count, and final outcome.
4. **A notification implementation** with the two severity levels, delivered to somewhere observable (a file, a local channel, or a stub that records deliveries).
5. **A backfill procedure document**: how to run a historical date, how many may run at once, who is told before a large reprocess, and the ordering rule that protects newer data.
6. **A scale measurement report**: elapsed time and peak memory for your transform at pilot volume and at a volume one to two orders of magnitude larger, the same aggregation expressed in a distributed style, the comparison including startup overhead, and an explicit threshold at which you would revisit the decision.
7. **An operating decision note**: who runs the orchestrator in the target deployment (customer platform, your platform, or scheduled invocation), the reasoning, and the handover implications.

## Required demonstrations

- **D1 — Ordered success.** One clean run for a target date. Show that the order was enforced and each task's status and duration are visible.
- **D2 — Gate blocks publication.** Force a batch assertion to fail. Show load and publish were not attempted, the previously published data is still served, and a notification was produced.
- **D3 — Transient recovery.** Make extract fail once, then succeed. Show automatic recovery and an attempt count above one in the run history.
- **D4 — Deterministic failure does not retry.** Make validation fail on a contract breach. Show exactly one attempt.
- **D5 — Bounded waiting.** Withhold the source export past the deadline. Show the run failing at the deadline rather than hanging.
- **D6 — Reproducible backfill.** Run a historical target date. Run it again. Show the second run changed nothing.
- **D7 — Ordering protection.** Backfill an old date after a newer load. Show current data was not reverted.
- **D8 — Bounded catchup.** Deploy with a start date well in the past. Show the number of simultaneous historical runs was capped.
- **D9 — Graceful degradation.** Leave the workflow failing past the freshness tolerance. Show the agent qualifying its asset context with no new code, and show the escalated severity firing.
- **D10 — Scale evidence.** Present the timing comparison and your written threshold.

## Rubric

| # | Criterion | Does not meet | Meets | Exceeds |
|---|---|---|---|---|
| 1 | Reproducibility | A task reads the clock | Target date is a parameter throughout; D6 passes | Any historical date can be reproduced from the run history alone |
| 2 | Dependency correctness | Order enforced by comments or luck | Declared dependencies; D1 passes | Graph is documented independently of the tool that runs it |
| 3 | Gate placement | Assertions run after load | D2 passes | A failed gate leaves a diagnosable artifact of the rejected batch |
| 4 | Publish atomicity | Readers can see partial data | Load and publish separated; previous version remains served on failure | Rollback to the previous version is a single operation and is demonstrated |
| 5 | Retry judgement | One blanket retry setting | Per-task policy with written justification; D3 and D4 pass | Ambiguous-outcome failures are explicitly reasoned about against idempotency |
| 6 | Bounded waiting | Sensor or wait with no deadline | D5 passes | Deadline derived from the observed arrival distribution, not guessed |
| 7 | Backfill safety | Unbounded catchup, no ordering rule | D7 and D8 pass; procedure documented | Procedure includes notifying the source owner and an estimated load figure |
| 8 | Notification quality | "Task failed" | Workflow, date, task, counts, reason, and where to look | Includes the likely owner and a link to the relevant runbook step |
| 9 | Severity discrimination | Everything alerts the same | Two levels with different routing; D9 passes | Severity derives from the freshness tolerance number, not a hand-set constant |
| 10 | Task granularity | One giant task, or thirty trivial ones | One task per distinct failure mode or expensive step | Granularity justified against retry cost in writing |
| 11 | Data passing | Large payloads passed through the orchestrator | References, counts, dates, and identifiers only | Intermediate artifacts are addressable and retained for replay |
| 12 | Scale honesty | Cluster adopted or dismissed by assertion | D10 passes with real numbers and a stated threshold | Threshold expressed against a growth assumption from the charter |
| 13 | Operating model | No statement of who runs this | Written decision with reasoning and handover implications | Names the specific customer role and the skills required to keep it running |
| 14 | Source protection | Unbounded concurrency against the source | Concurrency capped; extraction still bounded and disableable | Measured peak request rate against the source, stated in the decision note |
| 15 | Continuity | Chapter 24 guarantees broken | Idempotency, lineage, quarantine, and freshness all still hold under orchestration | Run record and orchestrator history reconcile to each other |

## Stop conditions

Reconsider if:

- You are installing a cluster before you have measured anything.
- Your graph has a task whose failure has no consequence.
- You cannot state, for each task, whether running it twice is safe.
- Your backfill plan involves running everything and hoping.
- You have started building a general-purpose scheduling framework.

## Carry forward

Chapter 26 pins the intelligence side of this system to a release manifest: application version, prompt version, model and provider, embedding model, retrieval index revision, and evaluation result. Your run history and your published-version concept from this chapter are the data-side half of that manifest. Keep them addressable by version, not just by date.

---

## Hints

Reversed. Reverse to read. One at a time, after a genuine attempt.

1. Parameterizing the period: `.gnihtyna sdaer ti erofeb noitcnuf yreve otni etad tegrat eht ssaP .ksat hcae fo tnemugra tsrif eht ti ekam ,elbairav lanretni na sa etad tegrat eht gnitaert fo daetsnI`
2. Separating load from publish: `.hctiws remaner ro retniop a si hsilbup dna ;noisrev eht ni gnidaol yb devres si daer hcaE .noisrev dehsilbup tnerruc eht ot sretniop hcihw eulav elgnis a peeK`
3. Protecting newer data from a backfill: `.rewen si noisiver ecruos gnimocni eht fi ylno etirw ,daol nopU .wor yreve no dedrocer ydaerla noisiver ecruos eht erapmoC`
4. Retry classification: `.seirter on steg rehto eht ;seirter steg tsrif ehT .gnorw si atad eht esuaceb deliaf ti dna ,dednopser metsys rehtona esuaceb deliaf ti :sepyt roree owt otni eruliaf ksat yreve tros`
5. Bounded catchup: `.gnitiaw eht od rehcatapsid eht tel dna ,eno ot smur lacirotsih rof ycnerrucnoc timil ,ffo puhctac htiw yolpeD`
6. Two severity levels: `.tnegru si dnoces eht ,enituor si tsriF .ecnarelot ssenhserf eht deecxe hsilbup lufsseccus tsal eht ecnis sruoh eht rehtehw ksa ,gniliaf saw nur hcihw gniksa fo daetsnI`
7. Scale measurement: `.ecnereffid eht si daehrevo dna ,niaga nur neht ,daol on htiw boj detubirtsid eht trats :tsrif tsoc putrats eht erusaeM`
