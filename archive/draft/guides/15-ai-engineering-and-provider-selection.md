# Test 15 — AI triage recommendation seam and provider decision

**Chapter:** 15 — AI engineering, LLM fundamentals, and provider selection
**Format:** This is a test, not a tutorial. Work from the goal and constraints. Hints are at the end, inverted; read them only after a genuine attempt.
**Prerequisite state:** FieldOps Copilot at the end of chapter 14 — React operator workspace, typed Node API with authoritative priority policy, PostgreSQL incidents and audit events, one expiring cache behind an interface.

---

## Goal

Add an AI triage recommendation capability to FieldOps Copilot such that:

1. The capability is bounded to advice only — it can never change an incident.
2. The model provider can be replaced without editing the incident service.
3. The provider choice is justified by written evidence a customer security reviewer would accept.

---

## Constraints

- **No real customer data** leaves your environment. Synthetic incidents only.
- The incident domain and service layer must not import, reference, or name any provider SDK, model name, or prompt text.
- Priority remains computed by the existing deterministic policy. The AI does not compute, override, or influence stored priority.
- Every stored suggestion records the model identifier/version and the instruction version that produced it.
- A suggestion is a proposal attached to an incident. It must not mutate incident status, assignment, or any notification path.
- "Insufficient evidence" must be a first-class representable result, not an error and not a low-confidence guess.
- Automated tests must pass with no network access and no credentials present.

---

## Starting state you must not break

- Creating and retrieving an incident through the API still works with the AI path disabled.
- The existing test suite still passes.
- Restarting the service still retains incidents (chapter 13 behaviour).
- Duplicate intake retries still do not create duplicates (chapter 13 behaviour).

---

## Required artifacts

### A. Task boundary statement (in the charter)

A short section added to the delivery charter stating, in language a non-engineer would accept:

- The exact set of outputs the AI capability may produce.
- The explicit list of actions it may never take.
- What a human must do before anything changes.
- The reasoning, expressed as a reversibility argument, not as "we are being careful".

### B. Port, domain types, and deterministic fake

- A domain-shaped interface (not a generic chat interface) whose input is your existing incident type and whose output is a triage suggestion type.
- The suggestion type must be able to express: suggested category from a fixed set, suggested urgency with a plain-language rationale, a list of specific missing information items, a coarse confidence signal, provenance (model version, instruction version), and an insufficient-evidence result.
- A deterministic fake implementation that can be driven to produce, at minimum:
  1. a well-formed useful suggestion,
  2. an insufficient-evidence result,
  3. a schema-violating / unparseable response,
  4. a timeout,
  5. a hard provider failure.
- Tests covering all five paths, runnable offline.

### C. Provider scorecard

A comparison of **at least two** genuinely available candidate options across these eight dimensions:

| # | Dimension | Must contain |
|---|---|---|
| 1 | Data handling | Training use, retention, subprocessors, processing region, deletion, DPA availability — quoted with a retrieval date |
| 2 | Deployment surface | Direct vendor / hyperscaler-hosted / self-hosted, and fit with the customer's existing cloud and procurement |
| 3 | Task quality | Result on **your** fixture set, not a public leaderboard |
| 4 | Latency & throughput | A measured or documented figure and the rate/quota limits you could actually obtain |
| 5 | Cost | Input vs output token pricing, estimated cost per triage, estimated monthly cost at stated volume, with assumptions |
| 6 | Reliability | Status history, incident communication, deprecation notice period, support tier |
| 7 | Compliance | Certifications, contractual vs best-effort regional commitments |
| 8 | Fallback | What runs when this option is unavailable |

Weights for the dimensions must be recorded **before** any scoring. The scorecard ends with a stated decision and a named fallback.

### D. Real adapter, or a written abstention

Either:

- One real provider adapter, exercised **only** with synthetic incidents, with explicit timeout, bounded retry with backoff, and per-call usage recording (input tokens, output tokens, latency, model version, outcome); **or**
- A written statement of which approval is outstanding, who owns it, what you did instead, and what you will run the moment it lands.

---

## Rubric

Score each item. Anything below "meets" is unfinished work, not a stylistic preference.

| Criterion | Fails | Meets | Strong |
|---|---|---|---|
| **Replaceability** | Service code references a provider | Deleting the real adapter leaves a green test suite | You can name every file a provider switch touches, and it is only the adapter and its config |
| **Boundary** | AI output can reach a write path | Suggestions are proposals only; no write tool exists | The boundary is written in the charter in customer language and argued by reversibility |
| **Interface shape** | Generic messages-in/text-out port | Domain-shaped port over incident and suggestion types | "Insufficient evidence" is representable and tested |
| **Failure handling** | Provider failure surfaces as a stack trace or spinner | All five fake paths are tested; operator sees an actionable state | Timeout, bounded retry, and a defined fallback are all exercised |
| **Evidence quality** | Scorecard cells contain adjectives | Every cell contains a figure, a measurement, or a dated quotation | Weights were fixed before scoring and a reviewer could reach their own conclusion from the same evidence |
| **Data discipline** | Real or plausibly-real customer text was sent | Synthetic only, and you can demonstrate it | Prompt construction is treated as an egress boundary with redaction in place |
| **Provenance** | Suggestions stored without version info | Model and instruction version stored per suggestion | Token usage and latency recorded per call, ready for chapter 23 |
| **Operator clarity** | UI blends computed and suggested values | Workspace visually distinguishes computed priority from suggested triage | A non-engineer can state what the system may and may not do after 30 seconds of looking at it |

---

## Self-verification before you call it done

Run these as actions, not as intentions.

1. Delete the real adapter file. Run the full test suite. It is green.
2. Remove all provider credentials from the environment. Run the full test suite. It is green.
3. Force the fake into its timeout path with the workspace open. Screenshot what the operator sees.
4. Grep your service and domain directories for the provider's name, the model name, and any prompt string. Zero results outside the adapter.
5. Read your scorecard aloud to yourself as if you were the customer's security lead. Note every sentence you would have to defend with "trust me".
6. Explain the capability out loud in under 60 seconds without using the word "model". If you cannot, the boundary is not clear enough yet.

---

## Stretch (optional, only after the above)

- Run your fixture set against a second candidate model and record the actual switching cost in time.
- Add a coarse token estimator to the adapter and compare its estimate against reported usage; note the error on jargon-heavy inputs.
- Write the one-paragraph answer to "what happens when the provider is down?" that you would give in a customer meeting.

---

## Common ways this goes wrong

- The port is generic, so prompts leak into callers within two chapters.
- The fake only handles the happy path, so nothing tests degraded behaviour.
- The scorecard is written after the decision, so it reads as justification.
- Someone tests "just one real ticket" to check something quickly.
- Confidence from the model is treated as a calibrated probability and used to auto-accept suggestions.

---

<details>
<summary>Hints — read only after attempting</summary>

**Hint 5 (last resort).** The port has one method. It takes an incident and returns a suggestion result. That is the whole interface. If yours has more than two methods, you are probably modelling the provider rather than the capability.

**Hint 4.** The insufficient-evidence case is easiest to model as a variant of the result type rather than a null or a low confidence number. That forces every caller to handle it explicitly, which is the point.

**Hint 3.** For the fake's failure modes, drive them from the input rather than from global configuration — a synthetic incident whose title contains a known trigger phrase. This keeps tests independent and readable.

**Hint 2.** For the scorecard, build the fixture set first (a dozen synthetic incidents spanning clear, ambiguous, and under-specified). It doubles as the seed of your chapter 22 evaluation suite, so the effort is not spent twice.

**Hint 1.** If you are stuck on the boundary argument: list every action the system could conceivably take, sort them by how hard each is to undo, and draw the line above the first one that is hard to undo. Everything above the line is advice; everything below needs a human.

</details>
