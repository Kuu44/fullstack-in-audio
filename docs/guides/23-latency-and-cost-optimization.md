# Test 23 — Set and meet a triage service budget

**Chapter:** 23 — Latency, inference, and cost optimization
**Format:** This is a test, not a tutorial. Hints are inverted at the end; read them only after a real attempt.
**Prerequisite state:** FieldOps Copilot at the end of chapter 22 — evaluation gate with deterministic and safety checks, baselines stored by version tuple, tiered CI runs.

---

## Goal

State a latency and cost budget, meet it, and **prove the optimization did not buy speed with quality**.

The proof is a single request trace that explains where time and money went, plus an evaluation gate that is still at or above baseline on **every** route.

---

## Constraints

- **No optimization ships without re-running the evaluation gate.** Every route is evaluated independently.
- Safety cases are 100% on every route, including cheap ones. A route that is faster and slightly worse at refusing is a regression.
- Every cache key for model-derived data includes the **full version tuple** and, where relevant, the **tenant and requesting scope**.
- The operator always receives something useful and always knows which degradation rung produced it.
- Budgets are expressed as **p95**, not averages.
- No real customer data.

---

## Starting state you must not break

- Evaluation gate green at baseline.
- Chapter 20 adversarial cross-tenant retrieval test passing.
- Chapter 19 stop conditions terminating with operator-actionable outcomes.
- Citations still validated against what was actually retrieved.

---

## Required artifacts

### A. Budgets in the charter

| Budget | Requirement |
|---|---|
| Latency | p95 end-to-end, **derived from the operator's workflow** (go and look at the work, or ask someone who has) — not from what is achievable |
| Latency, outage case | The harder target for when an operator is on a call, stated separately |
| Cost per triage | With stated assumptions |
| Cost monthly | At expected volume |
| Cost peak | A burst scenario, and what happens at the ceiling |
| Quality floor | Your chapter 22 baseline |

The ceiling behaviour (degrade / queue / stop) is the **customer's** decision, recorded as theirs.

### B. Full-path instrumentation

Spans for: request receipt, auth and scope, screening, query construction, embedding, vector search, keyword search, fusion, reranking, prompt assembly, model call split into **time-to-first-token and generation**, each tool call, validation, persistence, render.

Per model/embedding call: input tokens, cached input tokens, output tokens, reasoning tokens if applicable, model + version, computed cost.

All attributed to run, role, and version tuple. Reported as p50 / p95 / p99.

### C. Route comparison

A fast/cheap route and a higher-quality escalation route, evaluated **separately** on the same fixture set.

Record: per-route pass rates (including safety at 100%), per-route latency and cost, the **escalation rate**, and the computed **blended cost**. State whether the routing is actually an optimization.

### D. At least one safe optimization, with before/after

Choose from: embedding cache, reduced retrieved context, parallelized retrieval and classification, prompt prefix caching (verify cache hits are actually reported), or output schema reduction.

Record before and after for latency p95, cost per triage, and every evaluation metric.

### E. Degradation ladder

| Rung | Operator sees |
|---|---|
| Full | Grounded suggestion with citations |
| Degraded model | Same shape, **marked** as produced by the fast path |
| Retrieval only | Screening result + runbook links with titles and revision dates + honest message |
| Manual | Incident in the queue as before, with a clear unavailable message |

Each rung demonstrated. Nothing is a spinner.

---

## Rubric

| Criterion | Fails | Meets | Strong |
|---|---|---|---|
| **Budget provenance** | Number invented at the desk | p95 targets and cost ceiling written in the charter | Derived from observing the actual operator workflow, with the outage case separated |
| **Traceability** | Timing is aggregate | One trace shows every span, token count, and cost | You can point at the largest contributor instantly and it surprised you |
| **Quality protection** | Optimization shipped on plausibility | Gate re-run and at or above baseline | Every route evaluated independently; safety 100% on all of them |
| **Routing honesty** | Escalation rate unmeasured | Rate measured, blended cost computed | Routing removed if blended cost exceeds the single-model baseline |
| **Cache correctness** | Version tuple missing from key | Tuple and tenant scope in every key | Demonstrated: a new prompt version serves no stale cached result |
| **Tail focus** | Averages reported | p95 and p99 reported | Optimization targeted at the tail, not the median |
| **Degradation** | Failure yields a spinner or trace | All four rungs defined and demonstrated | Retrieval-only rung is genuinely useful and clearly labelled |
| **Decline preservation** | Decline rate dropped and was called an improvement | Decline rate tracked across routes | Framed to the customer as a safety feature, in writing |
| **Forecast** | A single confident number | Range with assumptions, peak scenario, ceiling behaviour | Non-linear scaling factors named, and the least-certain assumption identified |

---

## Self-verification before you call it done

1. Produce one full trace and read it. Point at the largest contributor.
2. Compare measured p95 against the charter budget. If there is no budget, you have not started.
3. Run the gate on every optimized configuration separately. Safety at 100% on each.
4. Force a model timeout with the workspace open. Confirm you see the retrieval-only rung within a fraction of a second, clearly labelled.
5. Deploy a new prompt version. Inspect a response's recorded version — not your assumptions — to confirm no stale cached result is served.
6. Measure the escalation rate and compute blended cost. If it exceeds baseline, the routing is not an optimization; say so and revert it.
7. Check the decline rate before and after. If it fell, investigate before celebrating the accuracy number.

---

## Stretch (optional)

- Build burst handling: deduplicate near-identical reports, add a concurrency-limited queue below your provider quota, and shed load to the retrieval-only rung when the queue is deep. Rehearse a 150-reports-in-an-hour scenario.
- Verify prompt prefix cache hits are actually being reported. A variable value accidentally placed early in the prompt silently disables caching for everything after it.
- Write the customer cost forecast: per-triage with assumptions, monthly at volume, peak, the non-linear scaling factors, and the assumption you are least sure about.
- Compare per-triage cost against operator time saved, including infrastructure and engineering time — honestly.

---

## Common ways this goes wrong

- Optimizing before measuring, and spending a week on a span worth 15% of the total.
- Cache keys without the version tuple, so production silently runs a retired prompt while the gate passed on the new one.
- A cheaper route deployed without independent safety evaluation, quietly weakening refusal and injection resistance.
- An escalation route that fires on 60% of requests, making the blended cost worse than the baseline.
- Optimizing the average while the p95 is what operators actually feel.
- A cache key omitting tenant scope, reintroducing a cross-tenant leak after chapter 20 removed it.
- A degradation path that ends in a spinner, so a provider outage looks like a broken product.

---

<details>
<summary>Hints — read only after attempting</summary>

**Hint 5 (last resort).** The cheapest large win is almost always "do less": measure how often deterministic screening already avoids the model entirely, and look for a second case like it. That number also belongs in your customer report.

**Hint 4.** Output tokens dominate generation time. Before touching models or infrastructure, read your output schema and delete a field.

**Hint 3.** Check whether retrieval and classification are actually running in parallel. After the chapter 21 split the classifier does not need passages, so they can start together — and "something serial that should be parallel" is the single most common finding in a first measurement.

**Hint 2.** Put the version tuple in the cache key rather than invalidating on deploy. Then a new version naturally has no entries and warms up on its own, and you can never forget the invalidation step.

**Hint 1.** If you can only build one degradation rung, build retrieval-only. Runbook links in 200 milliseconds beat a synthesis in 12 seconds, and it costs almost nothing because retrieval already ran.

</details>
