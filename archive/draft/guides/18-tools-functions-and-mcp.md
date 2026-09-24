# Test 18 — Build a read-only incident lookup tool

**Chapter:** 18 — Tools, functions, and the Model Context Protocol
**Format:** This is a test, not a tutorial. Hints are inverted at the end; read them only after a real attempt.
**Prerequisite state:** FieldOps Copilot at the end of chapter 17 — versioned triage instruction, fixture harness, assisted-development protocol, and the chapter 12 authentication/authorization boundary.

---

## Goal

Give the model its first contact with a real system through a read-only incident lookup tool, such that **an adversary in complete control of the model can do nothing the signed-in operator could not already do** — and you can demonstrate that with a test, not assert it in a document.

---

## Constraints

- **No write tool exists anywhere in the codebase.** Not disabled, not flagged, not permission-checked. Absent.
- The tool executes with the **operator's** authority, never the service's.
- Identity is a **required argument** to the executor. It must be impossible to call without one.
- The tenant filter is enforced **below** the tool, in the data access layer.
- Authorization is evaluated **freshly on every call**, never once per session and never at prompt-assembly time.
- The tool contract must be understandable without reading its implementation.
- Every invocation is audited, **including refusals and malformed calls**.
- No real customer data.

---

## Starting state you must not break

- Full offline test suite green with no credentials present.
- Chapter 16 fixture harness still matches its baseline.
- The triage port still has no provider-specific types.
- Priority remains deterministic.

---

## Required artifacts

### A. Tool contract

| Element | Requirement |
|---|---|
| Name | Unambiguous, names the single capability |
| Description | States what it does, what it does **not** do, and when **not** to use it |
| Description version | Versioned and recorded per invocation, like a prompt version |
| Input schema | Constrained: pattern or enumeration, minimum parameters, no free-form where a constraint works |
| Output shape | The **minimum** the triage reasoning needs; a written list of what you deliberately excluded and why |
| Errors | Stable structured codes, actionable messages, a **decided and documented** position on not-found vs not-authorized across a tenant boundary |
| Side effects | None. Safe to call repeatedly |

### B. Executor with per-call authorization

- Identity as a required parameter through the whole call chain (not ambient, not global).
- Fresh authorization check per call.
- Tenant filter in the data layer, below the tool.
- A read-only database credential scoped to the tables needed.
- Output projection applied before the result leaves the executor.

### C. MCP adapter or precise contract stub

Either a working MCP server exposing the capability, or — if your runtime makes that awkward — a precise stub defining capability name, description, input schema, output shape, error codes, transport assumption, and authorization model.

Also record: how you would review, pin, and re-review a **third-party** server before connecting it to this agent.

### D. Loop safety

- A per-turn tool-call budget with a defined terminal outcome when exhausted.
- A duplicate-call guard that returns a note rather than re-executing.
- A per-call timeout shorter than the turn deadline, returning a structured unavailable result.
- A reasoning path that degrades to a less-grounded suggestion or insufficient evidence when a tool result is missing — never invents the data.

### E. Audit record

Per invocation: correlation ID, executing identity, tool name and contract version, redacted input summary, authorization decision, result status, latency, model version, prompt version. **Redaction applied before writing, not after.**

---

## Rubric

| Criterion | Fails | Meets | Strong |
|---|---|---|---|
| **No write path** | A write tool exists behind a check | No write tool in the codebase | A test asserts that no model-originated path reaches a mutation |
| **Authority** | Tool runs as the service | Tool runs as the operator | Removing the identity argument fails the type check |
| **Tenant isolation** | Filter applied in tool code | Filter enforced in the data layer | Cross-tenant lookup returns not-found with no timing or shape tell |
| **Contract clarity** | Requires the implementation to understand | Another engineer can state what it does and cannot do | They can also state when it should *not* be used |
| **Output minimality** | Returns the record | Returns only the fields the decision needs | Exclusions are written down with reasons |
| **Error safety** | Malformed input crashes the turn | Structured error returned to the model | Model can self-correct; retries provably cannot change an authorization outcome |
| **Loop safety** | No budget | Budget and duplicate guard enforced in the executor | Demonstrated by a test that drives a loop to termination |
| **Audit** | Successes only | All invocations including refusals | Redaction verified; a refusal triggers an alert path |
| **MCP posture** | Third-party server treated as a convenience | Treated as a reviewed, pinned dependency with an owner | Written policy on description review, change detection, and credential isolation |

---

## Self-verification before you call it done

Perform these; do not merely intend them.

1. Search the codebase for any path from a model-originated request to a mutation. Confirm none exists, and that the absence is structural rather than conditional.
2. Hand-construct a tool call for an incident in a different tenant. Confirm not-found, confirm the audit record, and compare response timing and error shape against a genuinely non-existent ID — they must be indistinguishable.
3. Delete the identity parameter from the executor signature. The build or type check must fail.
4. Call with malformed arguments. The model receives a structured error and the turn continues.
5. Force the tool to return an unhelpful result repeatedly. The budget terminates the turn with a defined outcome, and the cost is bounded.
6. Give the contract (not the code) to another engineer. Ask what it does, what it cannot do, and when not to use it.
7. Draw the nine control points of one turn on paper. Mark which are in code and which are in the prompt. Anything in the prompt is unfinished work.

---

## Stretch (optional)

- Add an alert when a cross-tenant lookup is refused, and verify it fires.
- Write the paragraph you would give a security reviewer answering "what stops the AI from closing a ticket?" — it should be one sentence long and not mention permissions.
- Change only the tool description (remove the "when not to use it" clause), run the chapter 16 harness, and record the effect on call frequency, latency, and cost. This is the evidence that descriptions are behaviour-changing configuration.

---

## Common ways this goes wrong

- The tool runs with service credentials because that worked immediately. This is the confused-deputy flaw and it is the main thing this test is checking.
- The authorization rule is written in the tool description instead of in the executor.
- The whole incident record is returned "because it was easier".
- A write tool is built "for later".
- No call budget, so one unhelpful result becomes an unbounded cost loop.
- A third-party MCP server is attached casually, giving an unreviewed dependency runtime access to context and credentials.
- Only successful calls are audited, so the interesting events leave no trace.

---

<details>
<summary>Hints — read only after attempting</summary>

**Hint 5 (last resort).** If you are unsure whether your boundary is right, run the adversary test: assume someone fully controls the model via an incident description. Write the complete list of what it can now do. If anything on that list would alarm you coming from an anonymous user with the operator's session, move the boundary.

**Hint 4.** Make identity a required constructor or function parameter with a non-optional type. Security properties enforced by the compiler do not erode during refactors.

**Hint 3.** For the cross-tenant case, return the same error object as a genuine not-found, from the same code path, so there is no shape or timing difference to observe.

**Hint 2.** The duplicate-call guard is simplest as a per-turn map keyed on tool name plus normalized arguments. It also makes your traces much easier to read.

**Hint 1.** Before building the tool, seriously consider whether the information could be pre-fetched deterministically instead. If your intake already captures the related-incident field, a tool is the wrong answer and the right answer is three lines of ordinary code.

</details>
