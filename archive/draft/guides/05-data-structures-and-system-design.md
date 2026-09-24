# Chapter 5 project — Design the intake-to-triage flow

**Format:** open-book test. A design exercise with evidence. No build steps, no reference architecture.
**Prerequisite:** chapter 5 audio, the chapter 4 seam diagram, and the working intake program from chapter 3.

---

## Goal

A design for the path from intake to triage that states its capacity assumptions out loud, names what happens at every failure boundary, and survives its own worst case on paper — backed by evidence from breaking the small version you already have.

## Starting state

The chapter 3 command-line program, the chapter 4 seam diagram, and the chapter 1 charter. No service, no database, no queue exists yet, and you are not building them this chapter.

Your customer's storm is whatever their remembered worst day is. If you are using Harborline, it is eleven depots losing power and roughly three hundred reports in twenty minutes.

## Constraints

1. **Numbers before diagrams.** Typical volume, peak as a rate over a stated window, response time as a percentile, and retention. A diagram submitted without numbers fails.
2. **Every number is labelled** measured, derived, or assumed.
3. **No infinite scale.** No "it autoscales", no "the cloud handles it". Name the volume at which this design stops being appropriate.
4. **Every structure choice carries its reason** — the operation it makes cheap and the cost you accepted. "Standard choice" is not a reason.
5. **Every queue has a bound** and a stated behavior when the bound is reached.
6. **Every hop has a timeout** you chose, derived from your latency budget.
7. **You must break your own design** with a real batch run through the chapter 3 program before you defend it.
8. **No new components you cannot justify at pilot volume.** Complexity must be paid for with a number.

## Required artifacts

| Artifact | What it must contain |
| --- | --- |
| Load-assumption table | Typical volume, peak rate over a window, latency target as a percentile, retention, growth assumption, and the provenance label on every figure |
| Data-structure decision list | Each choice with the operation it optimizes, the cost accepted, and where in FieldOps it is used. Include your deduplication key and the reasoning behind it |
| Request-path diagram | Browser through service, durable record, queue, triage, and notification — with what crosses each boundary and who is authoritative |
| Failure-mode table | One failure mode and one graceful response per boundary, including the operator's attention as a boundary |
| Degradation statement | One sentence: what the system does when triage falls behind arrival |
| Batch-run findings | What you actually observed running hundreds of records through the chapter 3 program, ordered by which broke first |

## Self-grade rubric

**Pass bar — all eight must be true**

1. **Four numbers exist** and each is labelled measured, derived, or assumed.
2. **Peak is a rate over a window,** not a daily total.
3. **The design expiry is stated:** a volume at which you would redesign, with the component that fails first named.
4. **Fast and reliable are separated.** The operator's acknowledgment does not depend on the expensive work.
5. **Every queue is bounded** with a decided behavior at the bound.
6. **Every boundary has a failure mode and a graceful response,** and none of the responses is a confirmation the system cannot substantiate.
7. **Idempotency and deduplication are distinguished,** with different mechanisms and different keys.
8. **The batch was actually run** and the findings are observations, not predictions.

**Quality marks — aim for at least five**

9. Your capacity arithmetic appears on the page: a per-item cost multiplied by a peak rate, leading to a design decision.
10. Retention is multiplied out, and you named which query touches the growing thing.
11. The degradation statement uses your deterministic rule as the cheap reliable path, and marks expensive suggestions as pending.
12. Retries have a delay, a cap, and jitter — and you can say why jitter matters.
13. You identified at least one potential accidentally-quadratic behavior before it existed in code.
14. The design includes a way to switch off the expensive path and keep the workflow.
15. You can answer, in twenty seconds, what you are asking a platform team to run.
16. At least one batch-run finding surprised you, and it changed the design.

**Automatic fail**

- A diagram with no numbers.
- Capacity expressed only as a daily average.
- An unbounded queue anywhere.
- A hop with no timeout.
- The same key used for idempotency and deduplication.
- The design adds a component whose cost at pilot volume you cannot justify.
- The batch run was skipped, or "run" means five records.

## Stretch

- Write the five questions you expect a platform lead to ask, and your answers, in under twenty seconds each.
- Design the grouping behavior for the storm: a hundred and forty reports about eleven events. What key groups them, and what does a wrong grouping cost in each direction?
- Compute the arrival rate at which your customer's operators — not your software — become the bottleneck. That number is a product requirement, not an engineering one.

## Verification you can run today

- Read every figure aloud with its provenance label. Any unlabelled number is a defect.
- Walk the request path and ask at each hop: what is the time limit, and what happens when it is exceeded?
- Count your queues; check each has a bound and a behavior.
- Describe out loud what happens when the same submission arrives twice, then when two people report the same event. If the answers use the same mechanism, fix it.
- Run several hundred records through the chapter 3 program. Write down what broke, in the order it broke.

---

<!-- tts:skip -->
## If stuck — inverted hints

Last on purpose, absent from the audio. One at a time, in order, after a real attempt.

1. No numbers available? You are not allowed to give up here — the field never gives you numbers. What artifact already contains a count? A mailbox, a spreadsheet, a shift roster, a bill.
2. Cannot find the peak? Ask someone to describe their worst day in detail. People remember the worst day precisely, and their description is your burst figure.
3. Design feels like boxes with no substance? Multiply one per-item cost by your peak rate and see what the answer forces you to change. Arithmetic produces design decisions.
4. Unsure which parts must be fast? Ask which part a human is waiting on with their hand still on the keyboard. Everything else may be slow if it is visible.
5. Queue bound feels arbitrary? Ask what you would rather tell an operator: "we are not accepting reports right now", or nothing at all while the system quietly runs out of memory.
6. Cannot decide the deduplication key? Try to construct two reports that are the same event and two that look identical but are not. The key that separates those cases is your answer, and if no key separates them, that is a finding for the customer.
7. Confused about idempotency versus deduplication? Ask who is repeating themselves: the software, or two different humans.
8. Degradation statement keeps sounding like failure? Ask what your system can still do using only the deterministic rule and the database. That capability is your degraded mode, and it is genuinely useful.
9. Batch run produced nothing interesting? Increase the volume until something does, and include a malformed record in the middle.
10. Tempted to add a cache, a search index, and a worker fleet? For each one, state the number that justifies it at pilot volume. If you cannot produce the number, you have your answer.
<!-- /tts:skip -->
