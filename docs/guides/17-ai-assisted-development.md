# Test 17 — Establish an assisted-development protocol

**Chapter:** 17 — AI-assisted development without surrendering engineering judgment
**Format:** This is a test, not a tutorial. Hints are inverted at the end; read them only after a real attempt.
**Prerequisite state:** FieldOps Copilot at the end of chapter 16 — versioned triage instruction, policy/phrasing split, fixture harness, rollback rule.

---

## Goal

Define and then **demonstrate** a repeatable protocol for using coding assistants on a customer deployment, such that:

1. A second engineer could follow it without you explaining it.
2. A customer security reviewer could audit against it.
3. Every line that landed is understood by a human who can explain it.

This test is graded on the protocol and the evidence, **not** on how much code you produced. A one-file change with excellent evidence beats a feature with none.

---

## Constraints

- No production customer data, customer source you are not permitted to transmit, or credentials reach any assistant **by default** — and you must be able to demonstrate the exclusion empirically, not by pointing at configuration.
- The assistant does not touch: the authorization layer, the audit path, the deterministic priority policy, or the product's autonomy boundary.
- The change must be small enough that you genuinely read every line.
- Assistant-produced work must be separable from hand-written work in version history.
- No new dependency is added without an explicit, recorded human check.

---

## Starting state you must not break

- Full offline test suite green, no credentials present.
- Chapter 16 fixture harness still runs and still matches its saved baseline.
- The triage port still has no provider-specific types.

---

## Required artifacts

### A. Project instructions file (committed)

Must state, at minimum:

- What the system is, who uses it, and the delivery charter in two or three sentences.
- The no-secret rule: no credential in code, config, commit, prompt, or fixture.
- The test expectation: behaviour changes arrive with tests.
- The dependency rule: no new dependency without explicit human approval.
- The forbidden-autonomous-actions list (authorization, audit, priority policy, credentials, schema migrations).
- **The product's own autonomy boundary** — so the assistant does not helpfully propose auto-close or auto-escalate.

### B. Tool configuration record

A short written record of the four decisions, for whichever tool you use:

| Decision | Must record |
|---|---|
| Auto-approved commands | The exact allow-list, and confirmation that package installation is **not** on it |
| Context exclusions | Paths excluded, and how you verified the exclusion works |
| Account tier and data terms | Tier, training-use policy, retention period, retrieval date |
| Instruction file location | Path, and that it is committed rather than personal |

### C. One narrowly scoped assisted change

Choose **one**:

- Tests for the five failure paths of the chapter-15 deterministic fake, from a contract you state; or
- Additional synthetic incident fixtures with varied jargon density for the chapter-16 harness; or
- An explanation of an unfamiliar library's retry/timeout behaviour, used to correct your adapter.

Not a feature. Not the tool boundary. Not anything on the forbidden list.

### D. Verification evidence

- Test run output, including at least one test you wrote **by hand** covering the same behaviour.
- Type check and lint output.
- A **separate** review of the dependency and configuration diff, recorded as its own step.
- Chapter 16 fixture harness run if anything touched prompt assembly.

### E. Review note

Three to six lines: what you asked for, what you accepted, what you rejected and why, what you verified, and what you re-typed rather than accepted.

### F. Customer answer

A written paragraph answering: *"Which AI coding tools were used on our codebase, under what data controls, and what was the human review process?"*

---

## Rubric

| Criterion | Fails | Meets | Strong |
|---|---|---|---|
| **Instructions** | Generic encouragement | States the real constraints and forbidden actions | Includes the product's autonomy boundary and would change an agent's behaviour |
| **Egress control** | Exclusions assumed | Exclusions configured | Exclusion verified empirically with a marker string |
| **Scope** | Feature-sized request | One concern, readable diff | You can explain every line without re-reading |
| **Independence of verification** | Only assistant-written tests | At least one hand-written test for the same behaviour | Mechanical checks (lint/type/CI rule) added for an assumption you had to catch by reading |
| **Dependency discipline** | New dependency unexamined | Existence, maintainer, recency, transitive count, licence recorded | No new dependency was needed, and you can say why |
| **Separability** | Generated and hand edits in one commit | Separate commits | History makes the provenance obvious to a future bisect |
| **Review note** | Absent or "used AI to write tests" | Names accepted, rejected, verified | Names something you rejected and why — a note with no rejections is a note from someone who did not review |
| **Customer answer** | Vague or defensive | Specific tools, tier, terms, process | You would be comfortable if it were quoted back to you in a security review |

---

## Self-verification before you call it done

1. Read your instructions file as an adversary looking for a loophole. Note every gap.
2. Take the assisted change and, **without looking**, write down what it does. Then read it. The gap is your real review quality.
3. Find the newest dependency in your manifest. Name what it does, who maintains it, when it last shipped, and its licence. If you cannot, that is the lesson.
4. Put a unique marker string in a file you believe is excluded. Exercise the tool. Confirm the marker never appears in any context or log.
5. Pick a file generated more than a week ago (or the one from this test, in a week). Describe its error behaviour from memory, then check. Adjust your generation rate to match your comprehension rate.
6. Read your customer answer aloud. If any sentence needs "well, technically", rewrite the practice.

---

## Stretch (optional)

- Use the assistant in the **reviewer** direction on a diff you wrote by hand. Ask what it does beyond its stated purpose, what inputs break it, and what a security reviewer would flag. Record which findings were real.
- Add one automated check that would have caught an assumption you previously caught by reading (a missing timeout, a broad catch, an endpoint without an authorization check).
- Ask an assistant to add a convenience feature that would broaden the product's autonomy, and confirm your instructions file causes it to refuse or flag. If it does not, strengthen the file.

---

## Common ways this goes wrong

- Reviewing for "does it do what I asked" instead of "what else does it do".
- The diff grows beyond attention span and gets approved anyway.
- Tests and implementation written by the same tool, sharing the same misunderstanding.
- A hallucinated package name is installed because the install command was auto-approved.
- An agent is run inside a customer repository without asking whether that is permitted.
- The assistant quietly broadens autonomy, adds a permissive default, or removes a timeout, and it reads as ordinary code.

---

<details>
<summary>Hints — read only after attempting</summary>

**Hint 5 (last resort).** If your review note has no rejections, you did not review. Go back and find the thing you accepted without questioning — there is always one.

**Hint 4.** The empirical exclusion check is easier than it sounds: a distinctive nonsense string in an excluded file, then search every log, transcript, and cache the tool produces.

**Hint 3.** For the hand-written test, pick the failure path you understand least well. Writing it is how you come to understand it, which is the actual deliverable.

**Hint 2.** Package installation must not be on the auto-approve list. If your tool's default allow-list includes it, that single setting is the highest-value change in this whole test.

**Hint 1.** If you cannot think of a narrow enough request, invert the direction: ask for a critique of something you already wrote rather than a change to something you have not. The risk profile is far better and the value is often higher.

</details>
