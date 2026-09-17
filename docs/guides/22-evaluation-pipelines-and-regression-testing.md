# Test 22 — Build the FieldOps evaluation gate

**Chapter:** 22 — Evaluation pipelines and regression testing
**Format:** This is a test, not a tutorial. Hints are inverted at the end; read them only after a real attempt.
**Prerequisite state:** FieldOps Copilot at the end of chapter 21 — grounded triage, deterministic coordinator (with or without the specialist split, depending on what you measured), full per-role provenance.

---

## Goal

Build an evaluation pipeline that can **detect a behaviour change without a human reading every answer**, and a gate that blocks a bad change before a customer meets it.

The proof is not a green dashboard. The proof is a **deliberate break that fails the gate and names the responsible layer.**

---

## Constraints

- Safety cases pass **absolutely**. No threshold, no tolerance, no averaging.
- **No judged check may block a merge on its own.** Judged checks inform; deterministic and safety checks gate.
- Results are only comparable within a full version tuple. Comparing across tuples or fixture-set versions is invalid.
- Each fixture runs multiple times; criteria are expressed as **rates**, not pass/fail.
- Your noise floor is **measured**, not assumed.
- The fast tier runs offline, in seconds, with no credentials.
- Synthetic or properly sanitized fixtures only, with provenance labelled per fixture.

---

## Starting state you must not break

- Offline test suite green with no credentials.
- Chapter 20 adversarial cross-tenant retrieval test still passes.
- Chapter 19 stop conditions still terminate with operator-actionable outcomes.
- Chapter 18 authorization tests still pass.

---

## Required artifacts

### A. Fixture set (minimum ten, spanning the real distribution)

Coverage must include, at minimum:

| Dimension | Requirement |
|---|---|
| Severity | Across the range |
| Ambiguity | Clear, borderline, and genuinely contested |
| Completeness | Including reports that must trigger a decline |
| Rarity | At least one rare category — where accuracy is worst and nobody looks |
| Tenancy | More than one tenant |
| Safety | All five: prohibited-action attempt, direct injection, **indirect** injection planted in a retrieved document, cross-tenant retrieval attempt, sensitive-content redaction |

Each fixture labelled `synthetic` / `sanitized` / `real-with-consent`. A **holdout** portion you do not look at while tuning.

### B. Checks across all four kinds

1. **Deterministic structural** — schema valid; category in set; confidence in range; every citation was actually retrieved; no write attempted; declined when retrieval below threshold; step/time/cost budgets respected.
2. **Reference-based** — expected category (or set of acceptable categories); overlap on missing-information list.
3. **Property-based** — including a **consistency** check: same fixture run N times, is the category stable?
4. **Judged** — at least one, with a **written rubric** covering actionability, groundedness, and calibration, where confident-and-wrong scores worse than declining.

Plus **trajectory** assertions: thin reports terminate in screening with zero model calls; clear reports complete in one model call and at most one tool call.

### C. Baseline stored by version tuple

Application version, prompt version + hash, tool contract version, model ID + version, embedding model, index revision, retrieval parameters, **and fixture-set version**.

### D. A deliberate break with a demonstrated failing regression

Choose a plausible fault, not an absurd one:

- Remove the decline-on-thin-evidence instruction; or
- Halve the retrieved result count; or
- Loosen citation validation to presence-only; or
- Broaden a category discriminator.

Record: did it fail, did it fail on the **right check**, and did the failure **name the layer**.

### E. Gate configuration and tiering

| Tier | Runs | Contents | Blocks? |
|---|---|---|---|
| Fast | Every commit | Unit tests vs fake + retrieval eval | Yes |
| Gate | PRs touching prompt/model/retrieval/tool config | Deterministic E2E + all safety cases | Yes |
| Nightly | Scheduled, **against the live provider** | Full suite + judged checks, stored by tuple | Warns (drift detection) |

### F. Rubric validation record

Two people score the same twenty outputs independently; record the disagreement. If you use a model judge, score the same twenty and compare against the human labels.

---

## Rubric

| Criterion | Fails | Meets | Strong |
|---|---|---|---|
| **Fixture representativeness** | All happy paths, all written by an engineer | Spans ambiguity, rarity, and all five safety cases | Distribution characterized against real ticket shape, with the customer |
| **Layering** | End-to-end only | Component evals (retrieval, schema, classification) plus E2E | A failure names the layer without investigation |
| **Gating discipline** | A judged check can block | Deterministic + safety gate; judged informs | Gate is small and fast enough that nobody bypasses it |
| **Safety** | Safety cases averaged into a score | Absolute pass required | Indirect (document-planted) injection is covered |
| **Non-determinism** | Single run, pass/fail | Multiple runs, rates | Noise floor measured by running twice with no change |
| **Attribution** | Results stored bare | Stored with full version tuple | Nightly run against live provider detects drift with no diff |
| **Deliberate break** | Not attempted | Suite fails | Failure names the layer, and broken variants retained as a meta-test |
| **Trajectory** | Output only | State sequence and call counts asserted | Efficiency regression (same answer, double the calls) is caught |
| **Loop closure** | Production failures not captured | Rejections sampled and added as fixtures | Offline vs production divergence tracked, and production believed |

---

## Self-verification before you call it done

1. Run the deliberate break. It fails, on the right check, naming the layer. If it passes, you found a real gap — fix the suite, not the break.
2. Run the suite twice with zero changes. Record the variation. Any alert threshold below that number is a ghost generator.
3. Count your gating checks. If any judged check can block a merge, move it to informational.
4. Pick a fixture at random and ask whether a real incident from this customer would look like it.
5. Take the last real failure you saw and confirm it is in the fixture set.
6. Compare offline score against production acceptance rate. If they disagree, fix the fixtures.
7. Time the fast tier. If it is slow enough to be annoying, it will stop running.

---

## Stretch (optional)

- Write the customer-facing evaluation report: fixture composition, pass rates by category including the worst, safety results, production accept/edit/reject rates, and what the gate blocks. Deliberately include your weakest number.
- Add drift detection: alert when a nightly run with an unchanged tuple moves beyond the noise floor.
- Keep the broken variants as a meta-test suite that verifies the gate can still go red.
- Measure and report the **decline rate** as a safety feature rather than a defect, and get the customer to agree with that framing in writing.

---

## Common ways this goes wrong

- Every fixture is a happy path, so the suite measures capability and says nothing about safety.
- The gate blocks on a stochastic judge, produces false failures, and gets bypassed within a fortnight.
- Only end-to-end evaluation exists, so a failure means a day of investigation instead of a minute.
- A sub-100% pass rate is treated as flakiness to be suppressed rather than a property to be reported.
- Runs are compared across different version tuples or fixture-set versions.
- The suite only runs on commits, so provider drift — the failure with no diff — is discovered by the customer.
- Nobody ever added a production failure, so the fixture set stays as naive as the day it was written.

---

<details>
<summary>Hints — read only after attempting</summary>

**Hint 5 (last resort).** If you build only one thing from this chapter, build the retrieval evaluation. It needs no model, runs in seconds, costs nothing, and it tells you your ceiling.

**Hint 4.** Express every criterion as a rate from the start, even when the rate is 100%. Retrofitting rates onto a pass/fail suite means rewriting all the assertions.

**Hint 3.** For the consistency check, run the same fixture five times and measure category stability. Instability is not noise to be hidden — it is direct evidence that your discriminators are underspecified, and it points at exactly which category pair is confusable.

**Hint 2.** Store results as rows keyed by the version tuple from the beginning. Adding attribution later means every historical result is uncomparable and effectively lost.

**Hint 1.** The most likely outcome of your first deliberate break is that nothing fails, because you have no fixture for the behaviour you removed. That discovery *is* the exercise. Add the fixture, then break it again.

</details>
