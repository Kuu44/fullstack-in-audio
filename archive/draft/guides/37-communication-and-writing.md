---
chapter: 37
title: "Test — Write the FieldOps operator and engineer handoff"
slug: 37-communication-and-writing
lesson: docs/lessons/37-communication-and-writing.md
audio: media/37-communication-and-writing.mp3
type: test
---

# Chapter 37 test — Write the FieldOps operator and engineer handoff

This is a test, not a tutorial. It states the goal, the constraints, the state you start from, and the artifacts you must produce. It does not tell you how. Hints are at the very end, inverted so you do not read them by accident. Open them only after a genuine attempt, and only one at a time.

This test cannot be completed alone. Two of its demonstrations require another person's hands on the keyboard while you stay silent. If you have nobody, the closest legitimate substitute is to write the documents, wait at least a full day, then execute them yourself without editing while recording every stall — but that is a weaker test and you must label it as such.

## Goal

Make FieldOps Copilot operable and changeable by people who did not build it.

Concretely, three purpose sentences must become true and be demonstrated:

1. A new operator can submit, review, and decide on an incident without asking a colleague.
2. An engineer who did not build the system can diagnose and recover each of the five known failures using the runbook and the traces.
3. An engineer new to the codebase can make and ship one small change without supervision.

## Starting state

- The running system through chapter 32, including health checks, tracing with redaction, dashboards, evaluation gate, release manifest, and rollback capability.
- Chapter 33 interview transcripts — the source of the customer's own vocabulary.
- Chapter 34 timed rollback rehearsal, deferral list with triggers, and RAID log.
- Chapter 35 enterprise readiness map, which almost certainly lists the runbook as your one missing gate artifact.
- Chapter 36 decision log, feedback statuses, and release-note practice.
- Decision records accumulated since chapter 2.
- Diagrams accumulated since chapter 4.

## Constraints

- **Every document opens with its purpose sentence**, in the form: after reading this, [who] can [do what] without [whom].
- **Every procedural step states its expected observation** and what to do if that observation does not occur. A step without one is invalid.
- **Prerequisites, access levels, and tools appear at the top** of every procedure.
- **The runbook is indexed by observable symptom**, not by component. A component-indexed runbook fails outright.
- **Escalation paths name people and hours**, plus what information to bring.
- **Every claim in reportorial writing is labelled**: confirmed fact, assumption, inference, decision, or request.
- **The customer's vocabulary, not yours.** Terms must be traceable to the chapter 33 transcripts.
- **Every diagram and screenshot carries a date and the release it depicts**, plus a legend, plus consistent arrow semantics stated explicitly.
- **No raw incident content, secrets, credentials, or real customer identifiers** in any document.
- **During transfer tests you may not speak.** Not a hint, not a clarification. Speaking voids the test.
- **No new features.** Fixes to system behaviour discovered while writing are permitted and must be recorded as findings, but the evaluation gate must still pass.

## Starting state you must not break

- The evaluation gate, tests, and deployment behave exactly as before, including after any behaviour fix you make.
- Injected failures used for the transfer test are reverted, and the revert is verified with an instrument, not an impression.
- Existing decision records are not rewritten. The index references them; it does not replace them.

## Required artifacts

### A. Operator quick-start

Five sections, in the customer's vocabulary, readable in about five minutes:

1. What this is, in two sentences, including what it explicitly does not do.
2. When to use it and when not to — including the incident types that do not belong in the system at all.
3. The core workflow as numbered actions with expected observations: submit; read a proposal including its reason and its source; approve, edit, or reject; confirm the record is saved.
4. How to tell whether to trust it: what the confidence signal means in plain terms, what insufficient evidence means, why declining is correct behaviour rather than a fault, and what to do in that case.
5. What to do when it is wrong: the reporting path, exactly what information to include, where to find the identifier an engineer needs, who will look at it, and when the operator will hear back.

Section 5 is not optional and is graded strictly.

### B. Engineering runbook

Opening with a health-check section: how to establish in under a minute whether the system is broadly healthy.

Then one entry per known failure, indexed by symptom. Minimum five entries, covering:

- The system of record is unreachable.
- The cache is unavailable.
- The model provider is timing out, or the cost ceiling has engaged the fallback.
- The asset pipeline is stale — context present but old.
- The retrieval index does not match the current procedure revision.

Each entry contains: the symptom as an operator or alert would state it; the first check as a single action with an expected observation; a short decision tree; remediation steps; how to verify recovery; and escalation with named people, hours, and the information to bring.

Plus a pointer to the chapter 34 rollback procedure with its rehearsed timings.

### C. Decision record index

One line per decision since chapter 2: what was decided, why in one clause, status, date, reference to the full record, and the trigger that would revisit it.

Every entry must have a revisit trigger or an explicit statement that the decision is permanent.

### D. Diagram set

At least three diagrams, each titled with the question it answers:

- Which people and external systems does this touch, and where are the trust boundaries?
- What happens to one incident from submission to audit record?
- Which parts are reusable core, customer configuration, and customer-specific adapter?

Each with a date, a release, a legend, one consistent arrow meaning stated on the diagram, ownership marked per component, and — on the flow diagram — the failure behaviour annotated at each boundary.

Any component with no owner must be flagged, not quietly left blank.

### E. Engineer onboarding guide

Five sections: what the system is for and why the constraints exist; how to run it locally with expected observations and how to tell it is working; a map of the code oriented around the flow diagram; the rules that are not obvious from reading the code, each with one sentence of why and a pointer to its decision record; and a specific small first change drawn from your deferred list, with verification steps and review expectations.

The non-obvious rules section must include, at minimum: the AI may propose but never act; the priority policy has exactly one authoritative implementation; every suggestion records its instruction version; tenant isolation is enforced at retrieval; and no real customer data in development.

### F. Same event, two audiences

For one real or synthetic incident — a provider degradation is the natural choice — produce:

- A sponsor status note: impact first in their terms, causal detail compressed, one specific request with a person and a date.
- An operator incident note: what to do, what needs redoing and what does not, no provider names, no architecture, impact never omitted.

Both fully labelled by claim type. Both containing a next-update time.

### G. Operator-facing release notes

Describing what changed in the operator's workflow. No component names. Including at least one deliberate non-change with its reason, consistent with your chapter 36 deferrals.

### H. Documentation maintenance plan

Each document attached to a change trigger, not a review date. Plus the specific addition to the chapter 27 release checklist that gates the obligation.

## Required demonstrations

1. **Silent runbook transfer.** A peer who did not build the system executes the runbook against a failure you inject without telling them which one. You say nothing. Record: which failure, elapsed time, every stall with its location in the document, and whether they recovered the system. Then fix the document and repeat with a different failure.
2. **Silent quick-start transfer.** Someone who has never seen FieldOps completes the core operator workflow using only the quick-start. Record every question they ask, with the section it belongs to. Each question is a defect; fix each one.
3. **Two-in-the-morning index test.** Give a reader a symptom, not a diagnosis, and time how long until they reach the correct runbook entry. Record the time. Over one minute means reorganise the index.
4. **Labelling test.** Give your sponsor status note to a reader and ask them to separate confirmed facts from assumptions and inferences. Record their accuracy.
5. **Onboarding first change.** Have someone follow the onboarding guide and complete the first change end to end, including verification. Record where they stalled and what they had to ask.
6. **Behaviour-defect record.** Record at least one instance where writing a procedure revealed that the system's behaviour — not the writing — was the actual defect. Then state what you did about it.
7. **Revert verification.** After all injected failures, verify the system is in its original state using the evaluation gate, a test run, or a trace. Record the instrument used.

## Rubric

Grade each as pass or fail.

**Structural**

- Every document has a purpose sentence in the required form.
- No procedural step lacks an expected observation and a not-observed branch.
- Prerequisites and access appear at the top of every procedure.
- The runbook is symptom-indexed and covers all five failures.
- Escalation names people and hours and states what to bring.

**Audience**

- Vocabulary is traceable to the chapter 33 transcripts.
- The quick-start's trust section explains insufficient evidence as correct behaviour.
- The quick-start's "when it is wrong" section names the reporting path, the identifier, the responder, and the response time.
- The two audience versions of one event differ in vocabulary, causal depth, and ask — and not in the facts.
- Neither version omits impact. Both carry a next-update time.

**Epistemic**

- Every reportorial claim is labelled.
- A reader could separate facts from assumptions unaided.
- Every status update contains a specific ask with a person and a date, or explicitly states nothing is needed.

**Durability**

- Every diagram has a date, release, legend, stated arrow semantics, and ownership per component.
- Unowned components are flagged.
- The decision index has a revisit trigger on every entry.
- Every document is attached to a change trigger and gated in the release checklist.

**Verified by transfer**

- The runbook transfer was executed and you did not speak. If you spoke, the test was rerun after fixing the document.
- Every stall and every question was recorded with a location and fixed.
- The onboarding first change was completed by someone else.
- At least one behaviour defect surfaced by writing is recorded with its resolution.
- Injected failures were reverted and the revert verified with an instrument.

## Stop conditions

Stop and reconsider if any of these are true:

- You are explaining architecture inside a procedure.
- Your runbook has a section per component.
- You have written the words simply, just, or obviously.
- You are about to clarify something out loud during a transfer test.
- Your status update is a chronology of the week.
- An incident note has no next-update time.
- A screenshot has no date.
- Your escalation path says "contact the on-call".
- You are writing documentation as a phase after the work rather than while you understand the failure.
- You are treating a demo as a substitute for the quick-start.

## Carry forward

Chapter 38 is the capstone and it consumes all of this directly. The handoff packet includes the quick-start, the runbook, the diagram set, the decision index, and the onboarding guide. The final demonstration is to a sponsor, an operator, and a security reviewer, each of whom must leave with a decision — and each of whom needs the evidence type you recorded in chapter 36. The rollback rehearsal will be run again as part of release readiness, using the written steps you validated here.

---

## Hints

Read these only after a real attempt. Each line is reversed. Reverse it to read it.

1. `.sisongaid a ton ,motpmys a evah yeht .m.a 2 tA .tluaf ta si tnenopmoc hcihw yb ton ,evresbo nac redaer eht tahw yb koobnur eht xednI`
2. `.ti evresbo ton od yeht fi od ot tahw dna ,sdrawretfa evresbo dluohs redaer eht tahw setats ti litnu pets a ton si pets A`
3. `.daetsni llats eht nwod etirw dna sdnah ruoy no tiS .tnemucod ruoy morf gnissim pets a si kaeps uoy drow yreve ,tset refsnart eht gniruD`
4. `.tuo deppirts txetnoc ruoy htiw dedrawrof eb lliw etadpu ruoY .tseuqer ro ,noisiced ,ecnerefni ,noitpmussa ,tcaf demrifnoc sa mialc hcae lebaL`
5. `.noissimrep a kcal uoy gnirevocsid dna ruof pets gnihcaer si tsniaga gningised era uoy eruliaf ehT .pot eht ta sloot dna ,slevel ssecca ,setisiuqererp tuP`
6. `.tcapmi eht stimo eno rehtien dna ,stcaf eht ni reffid reven yehT .ksa eht dna ,htped lasuac ,yralubacov ni reffid tnedicni emas eht tuoba stnemucod owT`
7. `.noiretirc ecnatpecca on sah margaid eht ,esarhp nuon a si eltit eht fI .srewsna ti noitseuq eht htiw margaid yreve eltiT`
8. `.pleh ot gniyrt ylerecnis elihw stniartsnoc ruoy evomer lliw yeht ,ti tuohtiW .yhw fo ecnetnes eno htiw hcae ,edoc eht morf suoivbo ton era taht selur fo tsil eht si reenigne txen eht sevas taht noitces ehT`
9. `.teg reve lliw ediug gnidraobno ruoy tset tsenoh tsom eht si yad tsrif riehT .tsil derrefed ruoy morf egnahc tsrif laer a reenigne wen eht eviG`
10. `.derebmemer naht rehtar decrofne si ti os tsilkcehc esaeler eht ni ti etag neht ,etad weiver a naht rehtar reggirt egnahc a ot tnemucod hcae hcattA`
