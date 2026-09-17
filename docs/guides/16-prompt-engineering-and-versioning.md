# Test 16 — Version the triage instruction

**Chapter:** 16 — Prompt engineering, management, and versioning
**Format:** This is a test, not a tutorial. Hints are inverted at the end; read them only after a real attempt.
**Prerequisite state:** FieldOps Copilot at the end of chapter 15 — a domain-shaped triage port, a deterministic fake with five failure paths, a provider scorecard, and either one synthetic-data adapter or a written abstention.

---

## Goal

Turn the triage instruction from an ungoverned string into a versioned, reviewable production artifact with a fixture harness and a rehearsed rollback rule.

The test of success is not that the prompt is better. It is that **a reviewer who was not present can read two adjacent versions and correctly state the behavioural difference between them.**

---

## Constraints

- Untrusted content (the incident report) lands in **exactly one** clearly delimited region and is never concatenated into an instruction sentence.
- Customer policy (categories, discriminators, urgency definitions, insufficient-evidence conditions) must be **structured configuration**, not prose buried in the template.
- The fixture harness must run offline against the deterministic fake for all deterministic checks.
- Every suggestion your system stores records the prompt version identifier, the prompt content hash, and the model identifier and version.
- No real customer text. Synthetic fixtures only.
- Exactly one change per version. Do not change the prompt and the model in the same step.

---

## Starting state you must not break

- The full offline test suite still passes with no credentials present.
- The triage port still has no provider-specific types in its signature.
- Priority remains deterministic and unaffected by any suggestion.

---

## Required artifacts

### A. Prompt version one

A prompt containing all seven parts:

1. Operating context and role (factual, deployment-specific, no inflation)
2. Declared inputs and their trust level
3. The task, with **explicit decision criteria** — valid categories each with a discriminator against its nearest neighbour, and urgency levels defined by observable properties
4. The output contract, stated in words **and** enforced structurally
5. Uncertainty behaviour with a stated *condition*, not just permission
6. Prohibited actions and handling of instruction-like report content
7. Examples chosen for coverage: clear, ambiguous-but-resolvable, insufficient, and instruction-bearing

Stable content first, variable content last.

### B. The policy / phrasing split

A written two-column sort of every line in your prompt into **customer policy** or **incidental phrasing**, plus the implementation: policy lives in structured configuration rendered by the template; phrasing lives in the template.

State who owns each bucket and who must approve a change to it.

### C. Version identity and provenance

- A human-assigned version number with a stated bump convention (policy change vs phrasing change).
- A content hash computed from the rendered prompt.
- Both recorded on every stored suggestion alongside the model version.

### D. Fixture set (minimum five)

| # | Fixture type | Must exercise |
|---|---|---|
| 1 | Clear | Unambiguous category and urgency |
| 2 | Ambiguous | Two plausible categories; discriminator must decide it |
| 3 | Insufficient | Missing affected service or symptom; must return insufficient evidence |
| 4 | Sensitive-looking | Contains credential-shaped or personal content; checks redaction and handling |
| 5 | Instruction-bearing | Report text attempts to instruct the system (e.g. to resolve or escalate) |

Keep at least two additional fixtures as a **holdout** you do not look at while tuning.

### E. One deliberate change, fully documented

- Baseline results for every fixture on version one, saved.
- Exactly one instruction changed.
- Rerun, with a case-by-case diff.
- Every difference classified as **intended**, **neutral**, or **regression**.
- A change note containing: what changed, why, expected behavioural difference, fixtures affected.

### F. Rollback rule

A written rule with four parts: **trigger**, **authority**, **mechanism**, **record**. Rehearse the mechanism once and record how long it took.

---

## Rubric

| Criterion | Fails | Meets | Strong |
|---|---|---|---|
| **Traceability** | A stored suggestion cannot be tied to exact prompt text | Version and hash stored per suggestion | You can retrieve the exact rendered prompt for any past suggestion in under a minute |
| **Policy separation** | Taxonomy lives inside prose | Policy is structured config, phrasing is template | A non-engineer reviewed the policy and gave substantive feedback |
| **Criteria quality** | Categories are bare labels | Each category has a discriminator against its nearest neighbour | Urgency is defined by observable properties, not adjectives |
| **Uncertainty** | No insufficient-evidence path, or it is a low-confidence guess | Explicit path with a stated triggering condition | Fixture 3 reliably returns it and lists what is missing |
| **Injection posture** | Untrusted text reaches the instruction region | One delimited data region; output constrained by enumeration | Attempt is logged, output still conforms, and you can state the bounded worst case |
| **Change discipline** | Edit with no baseline or rerun | Baseline, single change, rerun, classified diff, change note | A holdout set exists and was checked after tuning |
| **Change note quality** | Describes text changes | Describes behavioural changes and names affected fixtures | A reader can predict the behaviour difference without seeing the diff |
| **Rollback** | Undocumented | Written with trigger, authority, mechanism, record | Rehearsed and timed; the revert itself appears in the version log |

---

## Self-verification before you call it done

1. Pick any suggestion your system produced. Retrieve the exact prompt text that produced it, from the stored record alone.
2. Submit fixture 5. Confirm three things: the output still conforms to schema, nothing in the system changed state, and the attempt was logged.
3. Hand only the policy configuration to someone who is not an engineer. Ask whether it matches how the team actually triages. Record what they said.
4. Read your change note without looking at the diff. Can you predict what will be different? If not, rewrite the note.
5. Perform the rollback end to end. Time it. Check the version log contains the revert.
6. Time your fixture run. If it is annoying enough that you would skip it under pressure, that is a defect — fix the harness.

---

## Stretch (optional)

- Add a second prompt version that changes only phrasing, and demonstrate that no fixture moves. This is how you prove your policy/phrasing split is real.
- Add an injection-attempt counter and surface it on the operator workspace.
- Reorder the output schema so the rationale field is generated before the category, rerun fixtures, and record whether rationale quality changed.

---

## Common ways this goes wrong

- The prompt is improved casually between fixture runs, so the baseline no longer means anything.
- Examples silently encode a policy that appears nowhere in the written criteria.
- The "policy vs phrasing" split is declared but the taxonomy is still hard-coded in the template.
- Prompt and model change in the same commit, so a quality shift cannot be attributed.
- Fixtures are tuned against until they all pass, with no holdout, and general quality quietly degrades.
- A confidence percentage is emitted and then treated as calibrated.

---

<details>
<summary>Hints — read only after attempting</summary>

**Hint 5 (last resort).** If you cannot decide whether a line is policy or phrasing, ask: "if I changed this without telling the customer, and it caused a bad outcome, would that be my fault or a shared decision?" Your fault alone means it was policy.

**Hint 4.** The content hash should be computed over the *rendered* prompt, after policy configuration is substituted in. Hashing only the template means a taxonomy change produces the same hash, which defeats the purpose.

**Hint 3.** For the ambiguous fixture, write it so that a reasonable human would also hesitate, then make the discriminator the thing that resolves it. If your discriminator does not resolve your own fixture, it will not resolve production cases either.

**Hint 2.** The easiest way to make the fixture run cheap is to make the harness a single command that prints a compact per-fixture table and a diff against the saved baseline. Spend the time on this before you spend it on prompt wording.

**Hint 1.** If the model keeps getting one category wrong, resist adding a sentence about that category. Ask instead what property of the incident the category actually depends on, and whether your criteria let the model express that property at all. Patch the criterion, not the case.

</details>
