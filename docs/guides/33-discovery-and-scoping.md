---
chapter: 33
title: "Test — Run a simulated FieldOps discovery"
slug: 33-discovery-and-scoping
lesson: docs/lessons/33-discovery-and-scoping.md
audio: media/33-discovery-and-scoping.mp3
type: test
---

# Chapter 33 test — Run a simulated FieldOps discovery

This is a test, not a tutorial. It states the goal, the constraints, the state you start from, and the artifacts you must produce. It does not tell you how. Work from the lesson, your own notes, and your judgement. Hints are at the very end, inverted so you do not read them by accident. Open them only after a genuine attempt, and only one at a time.

Unlike every previous chapter, almost nothing you produce here is code. That does not make it easier. The failure mode of this test is producing a plausible-looking document set that no one could act on, and that failure is very comfortable to commit.

## Goal

Replace the invented chapter 1 charter with an evidence-based one, and produce a first-release boundary for FieldOps Copilot that a customer could agree to and a pilot could measure.

Specifically, by the end you must be able to answer three questions with artifacts rather than opinions:

1. What is actually true about how incident triage happens for this customer today?
2. Which part of that will the first release address, and which part will it deliberately not address?
3. How will the pilot produce a yes-or-no answer about whether it worked?

## Starting state

FieldOps Copilot at the end of chapter 32:

- React operator workspace, secured typed API, PostgreSQL system of record with audit events and intake idempotency, expiring cache behind an interface.
- Provider-agnostic AI seam, versioned triage instruction, read-only lookup tool, bounded approval-gated agent, tenant-isolated retrieval over synthetic runbooks, specialist review split, evaluation gate, latency and cost budget.
- Asset ingestion pipeline, orchestrated refresh, AI release manifest.
- CI/CD with a blocking evaluation gate, non-root container images, chosen cloud landing zone, infrastructure as code, end-to-end tracing with redaction, risk-control pack with three passing abuse tests.
- The chapter 1 delivery charter, unchanged since you invented it.

Do not modify any running behaviour of the system in this chapter. This test changes documents and decisions only. Chapter 34 decides what changes next; chapter 38 assembles it.

## Constraints

- **Four roles, four distinct question sets.** Operator, operations manager, security lead, integration owner. No shared questionnaire. Each set must contain at least six questions the other three roles could not answer from their own job.
- **Transcripts, not summaries.** Each interview is recorded as a transcript with the hesitations, contradictions, and tangents intact. If you are role-playing all four yourself, you must still write them as transcripts.
- **Past behaviour only.** No question may ask what a role would like, prefer, or want in a future system. Questions ask what happened, when, how long it took, and what they did next.
- **Every finding is attributed.** A finding names its source and its confidence: observed, measured, documented, or stated.
- **Numbers carry sources.** Any nonfunctional requirement with a number must state where the number came from. Numbers you chose yourself belong in the assumption log, not the requirements list.
- **No new scope by reflex.** The first-release boundary may not grow simply because discovery revealed more. Growth requires a written justification naming what was removed to make room.
- **Synthetic data only.** If you use a ticket export, generate it; do not use real incident text from any real organisation.
- **No feature lists.** If an artifact contains a bulleted list of nouns with no trigger, actor, or observable result, it does not count as a requirement.

## Starting state you must not break

- The delivery charter's existing content is preserved as a dated prior revision. You revise; you do not overwrite history.
- Existing acceptance criteria that discovery invalidates must be marked invalidated with a reason, not deleted silently.
- The system still builds, tests, and deploys exactly as it did at the end of chapter 32.

## Required artifacts

### A. Four interview transcripts

One per role. Each transcript must contain:

- The role brief you gave (or held in mind), with the role's own incentives and what they are measured on.
- The questions asked, in order, with the answers as spoken.
- At least one moment where the answer contradicts something another role said, or contradicts something the same role said earlier.
- At least one exception-path answer: the ugliest or weirdest case that role handled recently.
- Three real objections from at least one of the four roles. Not concerns. Objections.

### B. Current-state workflow map

A map of how incident triage happens today, showing:

- Each step, who performs it, and which system it happens in.
- Working time and waiting time separately for each step.
- Every point where the work leaves tooling entirely (chat, phone, email, spreadsheet, memory).
- Decision points and who holds each decision.
- At least two exception paths drawn as branches, not footnotes.

### C. Volume profile

Four observed or generated-and-labelled numbers, each with its derivation:

- Incidents per day, and their distribution across the hours of a day.
- Peak-hour volume as a multiple of median-hour volume.
- Share of intake that is a duplicate or a reopen of an existing problem.
- Age distribution of open incidents, including the tail.

Then one paragraph per number stating what it changes about a design decision you already made in chapters 5, 13, 20, or 23.

### D. Requirements set

Two clearly separated lists.

**Functional requirements.** Each one names a trigger, an actor, an observable result, and a boundary where it stops applying. Each is traced to at least one finding by reference.

**Nonfunctional requirements.** Covering, at minimum: response time under peak, availability expectation, data retention period, data residency or processing-location constraint, auditability window, accessibility expectation, and any integration change-window or rate constraint. Each with a number and the number's source.

Both lists prioritised, with the prioritisation rule stated.

### E. Assumption log

Every unverified belief, with six columns: the claim; who or what it came from; why it matters; how it would be validated; who owns validating it; and what changes if it is false. Load-bearing assumptions — the ones whose falsity would change the architecture — must be marked as such.

### F. Acceptance criteria

Each criterion must:

- Return a plain yes or no when executed.
- Name the instrument that produces the evidence: the evaluation suite, a trace, the audit table, a dashboard metric, or a stated manual sampling procedure with a sample size.
- Include the sample size and the pass threshold where sampling is involved.

At least one criterion must be a negative criterion: something the system must never be observed doing during the pilot.

### G. Revised charter with a three-way boundary

The revised charter must contain three explicit lists:

- **In the first release**, with the customer outcome each item serves.
- **Deferred**, with a reconsideration trigger for each item, expressed as an observable condition rather than a date.
- **Out of scope**, with the reason.

Plus a subtraction statement: at least one thing that exists in the built system today and will not be in the first release, or will ship reduced, and why.

## Required demonstrations

1. **Read-back.** Take three requirements to the person (or role) whose statements produced them and record whether they corrected you. Record the correction. A requirement that survived read-back unchanged and unelaborated is suspect; note it as such.
2. **Stranger test.** Give the requirements set to someone who was in none of the interviews. Ask them to describe how they would test three requirements chosen at random. Record which ones they could not test, and fix those.
3. **Conflict demonstration.** Point at two conflicting stakeholder needs in your scope and at the specific sentence where you decided how to hold both. Show that the resolution is not an average of the two positions.
4. **Anti-confirmation check.** Show the note you wrote *before* interviewing, stating what you would have to hear in order to conclude that a major built component is unnecessary in the first release. Then state whether you heard it.
5. **Success-measure walkthrough.** Describe, step by step, the exact procedure the pilot will run to produce your headline success number, including who runs it, when, with what sample, and where the result is recorded.

## Rubric

Grade each item as pass or fail. Any fail means the test is not complete.

**Evidence quality**

- Every finding has a source and a confidence level.
- At least one revealed requirement contradicts a stated requirement, and the contradiction is recorded rather than resolved silently.
- The exception paths are mapped, and at least one of them carries more effort than the main path.
- No requirement rests solely on the champion's account.

**Requirement discipline**

- No adjective survives as a requirement.
- Every nonfunctional requirement has a number and a source for that number.
- Nonfunctional coverage includes retention, residency or processing location, and auditability. Absence of any of these three is an automatic fail.
- A stranger could construct a test for any requirement chosen at random.

**Boundary discipline**

- The first-release list did not grow without a stated removal.
- Every deferred item has an observable reconsideration trigger, not a vague later.
- The subtraction statement names something real that you built and are not shipping first, with a reason.
- At least two conflicting stakeholder needs are visible in the scope, with a stated resolution that is not a midpoint.

**Measurability**

- Every acceptance criterion returns yes or no and names its instrument.
- At least one criterion is negative.
- The headline success measure has an executable procedure with a sample size.
- No acceptance criterion depends on data the system does not currently collect, unless the collection gap is itself listed as a first-release item.

## Stop conditions

Stop and reconsider your approach if any of these are true:

- Your four transcripts read like one conversation with four names on it.
- You are writing requirements that describe features you already built, in the order you built them.
- Your workflow map has no waiting time on it.
- The assumption log is empty, or every assumption is owned by you.
- The revised charter's first-release list is longer than the chapter 1 version and nothing was removed.
- You have started designing a solution to something you learned two paragraphs ago, before finishing the map.
- You are about to ask a security lead to approve an architecture rather than to explain their constraints.
- Every acceptance criterion is a happy path.

## Carry forward

Chapter 34 turns this into a sequence. It needs three things from you in usable shape: the prioritised requirements set, the assumption log with load-bearing assumptions marked, and the three-way boundary. It will break the first release into independently testable slices, order them by risk retired rather than by novelty, make one tradeoff explicitly, and write the rollback plan for the first customer deployment. Keep the volume profile as well — chapter 34's sequencing and chapter 35's cost model both depend on it.

---

## Hints

Read these only after a real attempt. Each line is reversed. Reverse it to read it.

1. `.boj nwo rieht morf rewsna ton dluoc eerht rehto eht snoitseuq elor hcae eviG .semit ruof elor eno deweivretni uoy ,erutcip emas eht ecudorp stpircsnart weivretni ruof lla fI`
2. `.gniylppa spots ti erehw noitidnoc yradnuob eht dna ,tluser elbavresbo eht ,rotca eht ,reggirt eht eman :tneve na emoceb tsum evitcejda yrevE`
3. `.gol noitpmussa eht ot tsil stnemeriuqer eht morf ti evom ,uoy si ecruos eht fI .morf emac rebmun eht erehw etirw ,rebmun lanoitcnufnon hcae roF`
4. `.stseuqer laer eht ta gnikool ton era uoy ,gnihtyna sesol ydobon fI .rof deksa yeht tahw yltcaxe steg elor rehtona fi sesol elor hcae tahw gnitsil yb tcilfnoc eht dniF`
5. `.ti rof stpircsnart eht kcehc nehT .esaeler tsrif eht ni dedeen ton si reyal laveirter eht edulcnoc ot raeh ot evah dluow uoy tahw nwod etirw ,gniweivretni erofeB`
6. `.cirtem draobhsad a ro ,elbat tidua eht ,ecart a ,etius noitaulave eht :ecnedive eht secudorp taht tnemurtsni eht seman ti fi laer ylno si noiretirc ecnatpecca nA`
7. `.evom eht evivrus smeti hcihw ees dna tsil dedulcni eht erofeb tsil derrefed eht etirw ,knirhs ton did epocs fI`
8. `.pets yna esimitpo uoy erofeb spets neewteb spag eht erusaeM .pam wolfkrow eht no rebmun tsegral eht yllausu si ,emit gnikrow ton ,emit gnitiaW`
