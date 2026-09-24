# Test 19 — Assemble a bounded triage agent

**Chapter:** 19 — AI agents and agent architectures
**Format:** This is a test, not a tutorial. Hints are inverted at the end; read them only after a real attempt.
**Prerequisite state:** FieldOps Copilot at the end of chapter 18 — read-only incident lookup tool with per-call authorization, call budget, duplicate guard, and full audit.

---

## Goal

Turn the implicit loop inside your adapter into an explicit, durable, bounded workflow with named states, enforced stop conditions, and a meaningful approval gate.

The test of success: **you can hand the state diagram to a customer and they can state exactly what the system will and will not do**, and you can drive every transition in a test without calling a model.

---

## Constraints

- No write tool exists. No state modifies the incident.
- **Termination is decided by your code.** No stop condition may depend on the model choosing to stop.
- Workflow state is persisted. Transitions are idempotent and recorded as append-only events.
- Every terminal state produces something an operator can act on. No spinners, no silent empty results.
- At least one terminal state must be reachable **with no model call at all**.
- Retries happen at the layer nearest the failure. The workflow is never retried wholesale.
- No real customer data.

---

## Starting state you must not break

- Full offline test suite green with no credentials present.
- Chapter 16 fixture harness still matches baseline.
- Chapter 18 authorization tests still pass, including the cross-tenant refusal.
- Priority remains deterministic.

---

## Required artifacts

### A. State diagram

Named states, legal transitions, and terminal states. At minimum the machine must distinguish:

| State | Kind | Notes |
|---|---|---|
| Received | Entry | Authorize operator, load record |
| Screening | Deterministic | Completeness check; **no model call** |
| Gathering context | Conditional | Chapter 18 tool loop; may be skipped |
| Proposing | Model call | Exactly one structured suggestion |
| Awaiting approval | Durable wait | May last days |
| Approved / Rejected / Needs more information / Failed / Abandoned | Terminal | Each with an operator-actionable outcome |

Every state has at least one way in and one way out. No state's exit depends on the model.

### B. Deterministic transitions before any model call

The first two transitions must be deterministic. Screening must be able to reach a terminal state (needs-more-information) with a generated list of gaps and **zero** model involvement.

### C. Bounded proposing state

- One model call producing a structured suggestion, using only the read-only tool.
- Schema validation, category-membership check, confidence-range check on return.
- A validation failure transitions to `failed` (or at most one counted retry) — never silently back to proposing.

### D. Durable approval gate

- Survives process restart: start a run, reach awaiting-approval, restart, then approve.
- Captures **accept**, **accept-with-edits** (recording what changed), and **reject with a structured reason**.
- Presents to the operator: the proposal, the evidence, the stated reason, coarse confidence, and an explicit statement of what the system could not determine.
- Defines the no-decision default. **Expiry, not auto-apply.**

### E. Four enforced stop conditions

| Condition | Must have |
|---|---|
| Step budget | A small hard maximum, with a defined failure outcome |
| Wall-clock deadline | Separate from per-call timeouts |
| Cost budget | Token/cost ceiling per run, using chapter 15 accounting |
| No-progress detector | Repeated identical calls, state cycling, or a repeated validation failure |

Plus an explicit terminal success condition.

### F. Unhelpful-model simulation

Demonstrate and record the outcome for each of:

1. A syntactically valid response that violates your category set.
2. An unparseable response.
3. The same tool call repeated with no progress.
4. A provider timeout.
5. A model that never returns a final answer.

---

## Rubric

| Criterion | Fails | Meets | Strong |
|---|---|---|---|
| **Explicitness** | "In the middle of something" | Every moment is a named state, logged and queryable | The diagram is customer-presentable and was actually shown to someone |
| **Deterministic-first** | Model called on every run | Screening can terminate with no model call | Cheap filters measurably reduce model calls on a realistic fixture mix |
| **Testability** | Transitions require a model | Every transition drivable in a test with no model | Terminal-state coverage is asserted, not sampled |
| **Stop conditions** | Step limit only | All four enforced, each with a defined outcome | Each one demonstrated by a test, and none is a spinner |
| **Durability** | State in memory | Survives restart mid-flight | Transitions are idempotent and proven so by a repeated-transition test |
| **Approval quality** | Accept button on a bare suggestion | Evidence, reason, confidence, and unknowns presented | You measured time-to-approve and can argue the gate is not decorative |
| **Rejection capture** | Rejections discarded | Structured reason plus optional free text | Edits are diffed and stored as a quality signal for chapter 22 |
| **Retry placement** | Whole workflow retried | Retries at the nearest layer; resume from persisted state | Transient vs semantic failures handled differently, with semantic retries capped |
| **Degradation** | Failure leaves the operator stuck | Failure degrades to the manual workflow that existed before the copilot | The operator message names what was found and what to do next |

---

## Self-verification before you call it done

1. Draw the machine on paper. Find any state whose exit depends on the model. Remove that dependency.
2. Run the full transition set in tests with the model adapter deleted.
3. Trigger each of the four stop conditions independently. Screenshot the operator-visible result for each.
4. Start a run, reach awaiting-approval, restart the process, approve. Nothing is lost.
5. Apply the same transition twice. It is a no-op the second time, not an error and not a duplicate.
6. Run the five unhelpful-model simulations. Each terminates cleanly with a distinct, informative outcome.
7. Look at your approval screen. Could you make a real decision — including disagreeing — in ten seconds? If it only affords agreement, redesign it.

---

## Stretch (optional)

- Measure how many of a realistic fixture mix are resolved by screening alone. That number is your cheapest cost saving and it should be in your pilot readout.
- Instrument time-to-approve. If the median is under two seconds, propose a concrete change to make approvals rarer and more meaningful.
- Write the one-paragraph answer to "what happens if it gets stuck?" that you would give a customer's platform team.
- Decide, and write down, whether a framework or durable workflow engine is right for this customer — including who maintains it after you leave.

---

## Common ways this goes wrong

- An agent is built where a deterministic workflow would have been faster, cheaper, and explainable.
- Only a step limit exists, so a slow run or an expensive run is unbounded.
- Workflow state lives in memory, so an approval arriving after a deploy is lost.
- Approvals become a rubber stamp, producing the appearance of oversight without the substance.
- Rejections are discarded, throwing away the best quality signal the system produces.
- The whole workflow is retried, re-spending budget and repeating tool calls.
- Termination is delegated to an instruction in the prompt.

---

<details>
<summary>Hints — read only after attempting</summary>

**Hint 5 (last resort).** If the design feels too simple — one model call, a few deterministic checks, a wait state — that is the correct outcome. Complexity here is a cost you pay in debugging at a customer site.

**Hint 4.** Model the state as a column plus an append-only event table, exactly like the chapter 13 audit events. You already built the pattern; reuse it rather than introducing a second mechanism.

**Hint 3.** Make the state transition function total: it takes the current state and an event and returns the next state or an explicit rejection. Illegal transitions then become impossible rather than merely untested.

**Hint 2.** For the no-progress detector, the simplest useful signal is a hash of the last N actions. Two identical hashes in a row is enough to terminate, and it catches both repeated tool calls and state cycling with one mechanism.

**Hint 1.** Before implementing, write the operator-facing message for each terminal state. If you cannot write a useful message for a state, that state does not belong in the machine — or it is hiding a design decision you have not made yet.

</details>
