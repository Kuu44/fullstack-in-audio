---
chapter: 32
title: "Test — Produce the pilot risk-control pack"
slug: 32-security-privacy-and-ai-governance
lesson: docs/lessons/32-security-privacy-and-ai-governance.md
audio: media/32-security-privacy-and-ai-governance.mp3
type: test
---

# Chapter 32 test — Produce the pilot risk-control pack

A test, not a tutorial. This is the largest artifact in Part VI and the one a customer will actually read. Hints are reversed at the end.

## Goal

Convert FieldOps Copilot's unknown risk into stated, bounded, owned risk, and prove with tests that the system fails safe under abuse — so that a customer's security, privacy, and governance functions can make a decision rather than refuse by default.

## Starting state

Chapter 31 complete. You have the full system: secured service, role separation, durable record with audit events, asset pipeline, grounded agent with a read-only tool, approval step, evaluation suite, release manifest, hardened image, declared infrastructure, and end-to-end tracing with redaction.

## Constraints

1. **Implemented and planned are never blurred.** Every control is marked as one or the other, and a planned control is never described as protection that exists.
2. **No control may depend on the model behaving correctly.** Model instructions are mitigations. Controls are enforced in code, in authorization, in schema validation, or in the absence of a capability.
3. **Tenant isolation is enforced at query time**, derived from the authenticated caller. Post-filtering and prompt instructions do not satisfy this.
4. **Every data category has a classification, a retention period, and a deletion mechanism** that provably reaches the operational database, backups, the read model, the retrieval index, the quarantine, and telemetry.
5. **Synthetic data only.** Abuse tests must never be run against real customer data or a real customer tenant.
6. **Abuse tests must fail closed and be audited.** A refusal that is not recorded fails this test.
7. **Errors reveal nothing about internals.** Safe, actionable messages only.
8. **The AI path has an off switch** that is a configuration change, effective in seconds, that leaves incident intake and the operational system working.
9. **Residual risks are named with an accountable owner**, not listed anonymously.
10. **The pack must be readable by a non-engineer.** A security reviewer, a privacy officer, and a data owner are the audience.

## Required artifacts

1. **A threat model** covering intake, service, database, retrieval, tools, model provider, deployment, and operator access. For each trust boundary, work all five threat categories (impersonation, undetected alteration, repudiation, information disclosure, disruption). Each identified threat gets a control, an owner, and an implemented-or-planned status.
2. **A data classification and handling table**: every data element at public, internal, confidential, or restricted, with who may read it, where it may be stored, whether it may cross a border, whether it may go to the model provider, its retention period, and its deletion mechanism.
3. **A deletion procedure** demonstrating reach across all six stores, including the retrieval index and backups.
4. **A control mapping** covering at minimum: encryption in transit and at rest with a statement of who can decrypt, tenant isolation, least privilege for every identity, the audit trail, human approval, and vendor review.
5. **An audit trail assessment** against the five properties: complete, attributable, tamper-evident, readable, and retained for a stated period.
6. **A vendor review file** for the model provider: security documentation, data handling terms, retention, regional options, subprocessor status, and incident notification commitments.
7. **Abuse test results** for five tests (three required by the mini-project, two added):
   - direct prompt injection through an incident description,
   - indirect prompt injection through a poisoned synthetic runbook in the retrieval corpus,
   - cross-tenant retrieval attempt,
   - unauthorized tool call and a call to a non-existent capability,
   - a cost or step exhaustion attempt against your chapter 19 and 23 limits.
8. **A meaningful-oversight assessment**: evidence that the operator sees uncertainty, sources, and a genuine reject path — plus the measured time operators actually take to decide, and your honest reading of whether oversight is real.
9. **An off-switch demonstration** with the measured time to disable and confirmation that intake still works.
10. **A residual risk register**: each risk, why it is not fully mitigated, compensating controls, the accountable owner, and the specific customer decision required before real-data launch.
11. **A purpose statement**: what customer data may and may not be used for, explicitly addressing training, fine-tuning, product improvement, and cross-customer reuse.

## Required demonstrations

- **D1 — Threat coverage.** Walk all eight components and show every high-risk flow has a named control and a named owner, with status marked.
- **D2 — Deletion reach.** Delete one synthetic person's data. Prove it is gone from all six stores, including the index.
- **D3 — Direct injection.** Submit an incident whose description instructs the system to escalate. Show the instruction had no effect and why, structurally.
- **D4 — Indirect injection.** Place instruction-shaped text in a synthetic runbook that retrieval will select. Show the architectural controls holding despite the text reaching the model's context.
- **D5 — Cross-tenant.** Attempt retrieval across the synthetic tenant boundary. Show the filter applied in the query and the document never a candidate.
- **D6 — Unauthorized tool.** Attempt an out-of-scope tool call and a non-existent capability. Show safe refusals and audit entries for both.
- **D7 — Exhaustion.** Attempt a request designed to be expensive. Show step, timeout, and cost limits bounding it.
- **D8 — No write path.** Demonstrate that no write capability exists for the agent, rather than that it declined to use one.
- **D9 — Off switch.** Disable the AI path. Time it. Show intake and triage-by-human still working.
- **D10 — Oversight reality.** Show what an operator sees, including uncertainty and sources, and report the measured decision time. If the time suggests rubber-stamping, say so and propose a fix.
- **D11 — Audit reconstruction.** For one incident, reconstruct every action, actor, order, and the system configuration in effect.
- **D12 — Safe errors.** Show that every refusal above returned a message revealing nothing about internal structure.

## Rubric

| # | Criterion | Does not meet | Meets | Exceeds |
|---|---|---|---|---|
| 1 | Threat model completeness | Components missing or categories skipped | D1 passes across all eight components and five categories | Findings prioritized by impact with the top three called out for the customer |
| 2 | Honesty of status | Implemented and planned blurred | Every control clearly marked | A separate one-page summary of what is not yet protected |
| 3 | Classification rigor | Ad-hoc handling decisions | Handling derived from classification for every element | Classification drove a design change; name it |
| 4 | Deletion reach | Index or backups missed | D2 passes across all six stores | Deletion is executable as a procedure, timed, and repeatable |
| 5 | Injection defence | Relies on prompt instructions | D3 and D4 pass with layered architectural controls | The defence is explained in terms of what remains true if the model is fully compromised |
| 6 | Tenant isolation | Post-filtered or prompt-instructed | D5 passes with query-time filtering | Separate namespaces or indexes make cross-tenant retrieval structurally impossible |
| 7 | Capability boundary | Write tools exist but are discouraged | D8 passes: no write capability exists | The tool surface is enumerable and each entry justified |
| 8 | Authorization at tool boundary | Ambient admin identity | D6 passes with caller-scoped authorization and audit | Denied attempts are alerted, not merely logged |
| 9 | Resource bounding | Unbounded loops or cost | D7 passes | Limits derived from the chapter 23 budget, not arbitrary constants |
| 10 | Audit quality | Events without attribution | Five properties satisfied; D11 passes | Tamper-evidence verified by attempting modification from the application identity |
| 11 | Encryption and keys | "It's encrypted" | Transit and rest stated, with who can decrypt | Key access narrower than storage access, demonstrated |
| 12 | Human oversight | Claimed without evidence | D10 passes with measured decision times | Interface changed as a result of what the measurement revealed |
| 13 | Off switch | Absent or requires deployment | D9 passes in seconds | Off switch is itself tested in the evaluation suite |
| 14 | Purpose limitation | Unstated | Written statement covering training and reuse, verified against provider terms | Confirmed in writing with the customer before real data |
| 15 | Residual risk | Absent, or framed as reassurance | Named risks, owners, and required customer decisions | A reviewer could approve or reject from this document alone |

## Stop conditions

- A control in your pack is a sentence in a prompt.
- You cannot state what your model provider does with the data you send it.
- Your deletion procedure does not mention the vector index.
- You are describing a planned control in the present tense.
- You are presenting the risk register as evidence the system is safe rather than as a decision to be made.

## Carry forward

Part VII turns from the system to the engagement. The residual risk register becomes an input to the pilot readout, the vendor file becomes part of the procurement packet, and the threat model becomes a section of the handoff. Keep the pack in a form you can hand to a person, because in chapter 38 you will.

---

## Hints

Reversed. One at a time.

1. Indirect injection defence: `?dedaol si tnetnoc detsurtnu nehw eurt niamer taht seitreporp eht era tahw :ksa dnA .snoitcurtsni sa ton ,ecnerefer sa dessapded si tnetnoc deveirter taht os ,skcolb tcnitsid owt otni tpmorp eht rutcurtS`
2. Tenant isolation: `.deretlif neht dna dehcteF .yreuq erots rotcev eht ni retlif atadatem a sa reifitnedi tnanet eht ssaP`
3. Deletion reach: `.sexedni dna ,senitnarauq ,spukcab gnidulcni :stnemele emas eht rof erots yreve klaW .tsrif elbat noitacifissalc eht esU`
4. No write path: `.esufer ot ledom eht gniksa naht regnorts si tsixe ton seod taht loot A .tsil eht morf meht evomeR .redisnoc ot sloot fo tsil eht ta kooL`
5. Meaningful oversight: `.pmats rebbur a evah uoy ,sdnoces wef a si ti fI .noisiced dna tnemesitrevda lasoporp neewteb emit eht erusaeM`
6. Audit tamper-evidence: `.sliaf ti taht wohs dna ,drocer gnitsixe na yfidom ot ytitnedi noitacilppa eht esu ;ylno-dneppa yrtne tidua eht ekaM`
7. Residual risk framing: `.tpecca ot deksa gnieb era yeht tahw dna ,ksir eht si erht ,lortnoc eht si sihT :ecnetnes eno ni ksir hcae etirW`
