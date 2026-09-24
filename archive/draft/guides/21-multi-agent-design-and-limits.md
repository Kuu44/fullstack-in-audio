# Test 21 — Add a specialist review without autonomous consensus

**Chapter:** 21 — Multi-agent design and delegation limits
**Format:** This is a test, not a tutorial. Hints are inverted at the end; read them only after a real attempt.
**Prerequisite state:** FieldOps Copilot at the end of chapter 20 — grounded triage with tenant-isolated retrieval, validated citations, calibrated insufficient-evidence threshold, and a recorded retrieval recall figure.

---

## Goal

Split the triage proposal into two bounded specialists with a **deterministic** coordinator, then **measure whether the split was worth doing** — and remove it if it was not.

Removing the split after measuring it is a passing outcome. Keeping it without measuring is a failing one.

---

## Constraints

- No role has write authority. No write tool exists for any role.
- **The coordinator is deterministic code, not a model.** It must never fabricate consensus, average two categories, or pick a winner on a confidence score.
- Disagreement is a first-class output, presented to the operator as a structured, decidable choice.
- Context is isolated per role. The evidence checker receives the classifier's **category** but not its **reasoning**.
- No role delegates further. Depth limit is one.
- Each role has its own budget, timeout, and defined partial-failure behaviour.
- Retrieved evidence is retrieved **once** and shared by reference, so both roles reason over identical evidence.

---

## Starting state you must not break

- Offline test suite green with no credentials.
- Chapter 20 adversarial cross-tenant retrieval test still passes.
- Chapter 19 stop conditions still terminate cleanly with operator-actionable outcomes.
- Citations still validated against what was actually retrieved.

---

## Required artifacts

### A. Two specialists with narrow contracts

| Role | Sees | Must not see | Produces |
|---|---|---|---|
| Incident classifier | Incident text, taxonomy with discriminators, urgency criteria | Runbook passages, other incidents, operator history | Category, urgency + rationale, missing-information list |
| Runbook evidence checker | Incident text, retrieved passages with identifiers, classifier's **category only** | Classifier's reasoning, incident-lookup tool | Whether a known procedure matches, which passages, and whether evidence contradicts the proposed category |

Each with a typed input, a typed schema-enforced output, no write authority, its own timeout and budget.

### B. Deterministic coordinator

Explicit rules for at least four cases:

1. **Agreement + strong evidence** → single confident suggestion with citations.
2. **No evidence above threshold** → classification presented with an explicit "no supporting procedure found" note.
3. **Contradiction flagged** → both positions presented side by side, marked contested.
4. **Either role failed or timed out** → whatever succeeded, clearly labelled partial.

The coordinator must contain **no model call**.

### C. Operator disagreement view

For the contested case, the operator must see, in this order: that the analysis is contested; the classification with its reason; the contradicting evidence **quoted specifically** (not summarized) with revision date, owner, and link; the implication of each position; and one-click options with a captured reason.

Resolving a disagreement must not be slower than accepting a confident answer.

### D. Shared evidence, correlation, and cancellation

- Retrieval runs once per run; both roles reference the same stored artifact.
- Every role invocation records: run ID, incident ID, role, model ID and version, prompt version and hash, tool calls, input/output tokens, latency, outcome.
- The coordinator records: which roles ran, which succeeded, whether they agreed, which rule fired, what was presented.
- Cancellation propagates into in-flight role calls when the run is abandoned or deadlined.

### E. Measurement table

Compare the split against the single-agent baseline on the **same** fixtures:

| Metric | Single agent | Split | Delta |
|---|---|---|---|
| Correct/useful results | | | |
| p95 latency | | | |
| Cost per triage (tokens, priced) | | | |
| Disagreement rate | n/a | | |

Ending with a **one-sentence decision**: the split stays, or the split goes, and why.

---

## Rubric

| Criterion | Fails | Meets | Strong |
|---|---|---|---|
| **Coordinator** | A model reconciles the two outputs | Deterministic rules for all four cases | A test proves no blended answer is producible |
| **Independence** | Checker sees classifier's reasoning | Checker sees category only | Disagreement rate is non-trivial, showing independence is real |
| **Disagreement surfacing** | Blended or hidden | Both positions shown, marked contested | Contradicting sentence quoted, one-click resolution, reason captured |
| **Least privilege** | Roles share one tool scope | Each role has only the tools it needs | No write capability exists for any role, structurally |
| **Partial failure** | A role timeout fails the run | Labelled partial result | Each role's timeout independently demonstrated |
| **Shared evidence** | Each role retrieves separately | Retrieved once, shared by reference | Disagreement provably reflects interpretation, not differing retrieval |
| **Correlation** | Cannot attribute a bad output to a role | Full per-role provenance recorded | Quality, latency, and cost can each be attributed to a role |
| **Cancellation** | Abandoned runs keep burning quota | Cancellation propagates | Verified by abandoning a run and checking the provider call stopped |
| **Measurement** | "It feels better" | Four numbers recorded against the baseline | A decision stated in one sentence, and acted on — including removal |

---

## Self-verification before you call it done

1. Construct a case designed to produce disagreement (text points one way, retrieved procedure points another). Confirm both positions reach the operator and nothing in your code can blend them.
2. Inspect each role's actual assembled context. Confirm the classifier sees no passages and the checker sees no classifier reasoning.
3. Time out each role independently. Confirm a clearly labelled partial result in each case.
4. Search for any write capability reachable by any role. There must be none, structurally.
5. Abandon a run mid-flight. Confirm the in-flight provider calls were cancelled, not merely ignored.
6. Read your measurement table. State what the split bought and what it cost, in numbers.
7. Ask whether you would keep this split if you were paying for it personally. Act on the honest answer.

---

## Stretch (optional)

- Route the classifier to a cheaper, faster model tier and re-measure. This is usually where a split starts to pay.
- Add a concurrency limit in front of the role calls and verify behaviour during a simulated burst against a low rate limit.
- Write the three-sentence answer you would give an executive who asks why you do not have more agents, and the three-sentence answer for a security lead who is worried that you have two.

---

## Common ways this goes wrong

- A model coordinator produces a fluent reconciliation, converting the most valuable signal in the system into false confidence.
- The checker is given the classifier's reasoning, so it agrees with everything and the disagreement rate is near zero.
- Voting across three roles is used as a quality mechanism, despite correlated errors.
- Roles exchange free-text messages instead of structured objects through the coordinator.
- Each role retrieves independently, so a "disagreement" is really a retrieval artifact.
- Resolving a disagreement takes longer than accepting a confident answer, so operators stop engaging with it.
- The split is kept because it was built, not because it measured well.

---

<details>
<summary>Hints — read only after attempting</summary>

**Hint 5 (last resort).** If your disagreement rate is near zero, the problem is almost always context leakage into the checker. Check what you are actually sending, not what you intended to send.

**Hint 4.** Make the coordinator a pure function from two role results to one presentation object. Pure means testable, and testable means you can prove it cannot blend.

**Hint 3.** For the contested view, quote the contradicting sentence verbatim from the retrieved passage. A summary asks the operator to trust the system about the very thing they are being asked to judge.

**Hint 2.** Retrieve once and pass a reference. If both roles retrieve, you cannot tell whether a disagreement is interpretation or retrieval variance, and that ambiguity makes the whole measurement worthless.

**Hint 1.** Do the measurement before you polish anything. If the numbers say remove it, you have saved yourself the polish — and "we measured and reverted" is a stronger result to report than a split you cannot justify.

</details>
