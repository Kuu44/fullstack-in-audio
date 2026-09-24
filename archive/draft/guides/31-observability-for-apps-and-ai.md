---
chapter: 31
title: "Test — Trace one incident end to end"
slug: 31-observability-for-apps-and-ai
lesson: docs/lessons/31-observability-for-apps-and-ai.md
audio: media/31-observability-for-apps-and-ai.mp3
type: test
---

# Chapter 31 test — Trace one incident end to end

A test, not a tutorial. Hints are reversed at the end.

## Goal

Make one synthetic incident fully reconstructible from a single identifier, from the operator's submission through to their decision, and make the pilot observable in both dimensions that matter: service health and artificial intelligence workflow health — without exporting sensitive content.

## Starting state

Chapter 30 complete. You have a deployed, declared environment, a hardened image with health endpoints, a release manifest, a versioned prompt, a retrieval index, a read-only tool, an asset read model with freshness, an evaluation suite, and a cost and latency budget.

## Constraints

1. **One correlation identifier, every boundary.** Generated at submission, carried through intake, authorization, persistence, audit, asset lookup, retrieval, every tool call, the model request, the persisted proposal, and the operator's decision.
2. **Structured logging only.** Named fields, not sentences. Correlation identifier and release identifier on every entry.
3. **Vendor-neutral instrumentation.** Switching telemetry backends must be a configuration change, not a refactor.
4. **Redaction happens inside the service**, before data leaves the process. Destination-side filtering does not satisfy this.
5. **No raw incident content, personal data, or secret-shaped strings in logs, traces, metrics, or error reports.** This includes unhandled exception handlers.
6. **No unbounded cardinality in metrics.** Unique identifiers belong on traces and logs only.
7. **Sampling, if used, retains all errors, slow requests, refusals, fallbacks, weak-retrieval cases, and schema failures.**
8. **Every alert is a user-visible symptom and links to a runbook entry** written at the same time.
9. **Telemetry location, retention, and access are stated** for each signal type and checked against the chapter 29 residency requirement.
10. **Synthetic data only**, but the redaction controls must be written as though the data were real.

## Required artifacts

1. **A correlation design note**: where the identifier originates, how it propagates across each boundary, and how it is persisted.
2. **An instrumented triage span tree**: root span plus child spans for asset enrichment, retrieval, each tool call, and the model call, with the attributes named in the lesson (asset found, read model age, documents considered and selected with revisions, retrieval strength, tool name and status and duration, model and prompt versions, token counts, cost estimate, schema validity, refusal, fallback, proposal outcome, operator decision).
3. **A structured logging standard**: the required fields on every entry, the allowed levels, and how the level is changed at runtime without a deployment.
4. **A redaction implementation**: source-side, with a field policy (prefer allow-list), secret-pattern detection, and coverage of trace attributes and error reports.
5. **A sensitive-content access path**: if you retain any content for diagnosis, a narrow, access-controlled, short-retention channel with an audit trail — plus the written statement of what the customer is agreeing to.
6. **Two or three service level objectives** with indicators, targets, windows, and the resulting error budget. They must be about operator-visible behavior.
7. **Three dashboards**: operator, engineer, and sponsor, each small and each with a stated audience.
8. **An alert set with runbook entries**, covering at minimum: intake failing, read model stale beyond tolerance, retrieval strength collapse, model provider failure, and cost per triage over budget.
9. **A telemetry governance note**: per signal type, where it is stored, in which region, for how long, who can read it, and the estimated monthly cost.
10. **A sampling policy** if you sample, stating what is always retained.

## Required demonstrations

- **D1 — End-to-end reconstruction.** From one correlation identifier, produce the complete path of one synthetic incident including the operator's decision. Narrate it.
- **D2 — Time attribution.** Show a trace with duration attributed across intake, database, asset lookup, retrieval, tool calls, and the model call, and state where the majority went.
- **D3 — Redaction holds.** Submit an incident containing a person's name, a contact detail, and a credential-shaped string. Show none of them in logs, traces, metrics, or error output — while the identifier still links everything.
- **D4 — Exception safety.** Force an unhandled exception mid-request. Show no request body in the error report.
- **D5 — Both health families.** Show a dashboard containing availability, p95 triage time, failure rate, cost per triage, operator acceptance, refusal rate, retrieval strength, and read model freshness.
- **D6 — Actionable alert.** Trigger a synthetic dependency failure. Show an alert naming the user-visible symptom and linking to a runbook that resolves it.
- **D7 — Silent quality failure.** Degrade quality without producing any error: weaken retrieval so proposals become poorly grounded while every status code stays healthy. Show which signal catches it and how quickly.
- **D8 — Cardinality control.** Name a metric you were tempted to label with an incident identifier, and show what you did instead.
- **D9 — Retrospective attribution.** For a proposal produced earlier, recover its release identifier and prompt version from telemetry alone.
- **D10 — Stranger test.** Give a colleague a complaint in the form a manager would write it, with no identifiers, plus your documentation. Have them find the relevant trace unaided.

## Rubric

| # | Criterion | Does not meet | Meets | Exceeds |
|---|---|---|---|---|
| 1 | Correlation coverage | Identifier stops at a boundary | D1 passes across every boundary including the operator decision | Identifier survives the asynchronous pipeline path as well as the request path |
| 2 | AI span richness | Only the model call is traced | All attributes in the artifact list present | Retrieval span records rejected documents and why, not only selected ones |
| 3 | Time attribution | One total duration | D2 passes with per-phase breakdown | Breakdown reconciles with the chapter 23 budget, and overruns are flagged |
| 4 | Redaction correctness | Filtering at the destination | D3 and D4 pass, source-side | Allow-list rather than deny-list, so new fields fail safe |
| 5 | Sensitive access | Content logged freely, or diagnosis impossible | Narrow audited path with short retention and customer agreement | Access to that path is itself alerted and periodically reviewed |
| 6 | Objectives | Infrastructure metrics presented as SLOs | Two or three operator-visible objectives with error budgets | Error budget used in an actual prioritization decision |
| 7 | Dashboard fit | One dashboard for everyone | Three, each small, each with a named audience | Sponsor view ties to the charter's measurable outcome |
| 8 | Alert quality | Cause-based or runbook-free | D6 passes; every alert has a runbook entry | Alerts that fired without action taken were deleted, and you can say which |
| 9 | Silent failure detection | Only errors are detectable | D7 passes | Detection latency measured and stated in hours |
| 10 | Cardinality discipline | Unique values as metric dimensions | D8 passes | A guard prevents high-cardinality labels from being added accidentally |
| 11 | Sampling | Uniform random, or none considered | Policy retains all interesting cases | Tail-based decision made after the operation completes |
| 12 | Vendor neutrality | Backend library used throughout | Neutral instrumentation; backend is configuration | Demonstrated by switching backends |
| 13 | Governance | Location and retention unknown | Stated per signal type and checked against residency | Monthly telemetry cost estimated and compared against compute |
| 14 | Release linkage | Telemetry cannot identify configuration | D9 passes | Any signal can be sliced by release to compare versions |
| 15 | Handover readiness | Requires you to interpret | D10 passes | Colleague also identifies the likely cause, not just the trace |

## Stop conditions

- Your dashboard is green while the copilot is producing poor proposals and nothing would tell you.
- You are logging request bodies "temporarily".
- You cannot say where your telemetry is stored.
- An alert has fired more than twice with no action taken and still exists.
- You are attaching an incident identifier as a metric dimension.

## Carry forward

Chapter 32 turns these signals into controls and evidence: the audit trail, the abuse tests, and the residual risk statement all depend on what you instrumented here. In particular, your redaction policy and your sensitive-content access path become entries in the data classification and control mapping.

---

## Hints

Reversed. One at a time.

1. Propagation across boundaries: `.tnedi eht daer dna tcejni taht sreppartw yb dessap eb dluohs llac tuo yreve ;txetnoc tseuqer eht ni ti erots dna ,egde eht ta ecno reifitnedi eht etareneG`
2. Redaction that fails safe: `.dedda si dleif wen a nehw ylefas sliaf hcihw ,tsil-ynned a naht rehtar dettimrep si dleif hcihw fo tsil a peeK`
3. Detecting silent quality failure: `.slangis eseht hctaW .etar lasufer dna ,noitubirtsid htgnerts laveirter ,etar ecnatpecca rotarepo :srorre naht rehtar seussi ytilauq no tresA`
4. Cardinality: `.golgel ro ecart eht ot ti hcatta ;noisnemid cirtem a sa reifitnedi tnedicni na hcatta reveN .setubirtta detimil-eulav esU`
5. Tail-based sampling: `.deniater si tnemgduj taht dna ;peek ot rehtehw ediced neht ,sdne noitarepo eht litnu snaps reffuB`
6. Stranger test: `.txet tnialpmoc a morf ecart a ot htap eht elpmaxe na htiw ,noitatnemucod eht ni tsrif erudecorp hcraes eht etirW`
7. Exception safety: `.ereht ydob tseuqer eht redner reven dna ,gnihsilbup erofeb noitpecxe yreve sessap hcihw rezilaires tluafed eno etirW`
