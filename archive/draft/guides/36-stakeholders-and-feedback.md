---
chapter: 36
title: "Test — Operate a pilot feedback loop"
slug: 36-stakeholders-and-feedback
lesson: docs/lessons/36-stakeholders-and-feedback.md
audio: media/36-stakeholders-and-feedback.mp3
type: test
---

# Chapter 36 test — Operate a pilot feedback loop

This is a test, not a tutorial. It states the goal, the constraints, the state you start from, and the artifacts you must produce. It does not tell you how. Hints are at the very end, inverted so you do not read them by accident. Open them only after a genuine attempt, and only one at a time.

This test requires you to actually run a demo session with at least one other person. If nobody is available, you must run it against a written role-play with a recorded script — but a real person, even an untrained one, produces evidence a role-play cannot, so try hard first.

## Goal

Run one full turn of the FieldOps Copilot feedback loop, from stakeholder mapping through a live demo to a communicated decision, such that:

1. No piece of feedback is lost, and each one has an owner, a status, evidence, and a decision date.
2. Every person who raised something can describe what happened to it.
3. At least one request is correctly refused or deferred, and the requester can restate your reasoning.

## Starting state

- The running FieldOps Copilot system as built through chapter 32.
- Chapter 33 requirements, assumption log, and revised charter.
- Chapter 34 slice sequence, deferral list with triggers, and RAID log.
- Chapter 35 business case, adoption metric definitions, and enterprise readiness map with named gate owners.
- Chapter 6 architecture split: reusable core, customer configuration, customer-specific adapter.
- Chapter 31 dashboards and traces.

## Constraints

- **No commitments during the demo.** Not one. Every request is captured as an observation and answered afterwards.
- **Every feedback item carries evidence**: a trace identifier, a screenshot, an incident reference, or a recorded hesitation with its location in the interface. Items without evidence may be logged but may not be prioritised.
- **The register must contain at least one skeptic or blocker**, given real access.
- **Decision rights must be verified with the named person**, not assumed from the org chart.
- **Three demo incidents, and one of them must be a failure or boundary case** that you show on purpose.
- **The operator holds the keyboard.** You may not drive the interface during the demo.
- **The prioritisation rubric is published before any item is ranked.**
- **Every accepted item is routed** to reusable core, customer configuration, or customer-specific adapter. Anything fitting none of the three is escalated in writing, not absorbed.
- **No raw incident content on any shared dashboard or in any release note.** Redaction discipline from chapter 31 applies.
- **Deferrals need observable triggers**, consistent with chapter 34. "Later" is not a status.

## Starting state you must not break

- The system's behaviour is unchanged by this test except for fixes you deliberately choose to make and record as decisions.
- Any fix you do make must pass the existing evaluation gate before it is shown to anyone as resolved.
- The chapter 34 deferral list is not quietly edited to accommodate a demo request. Changes are recorded as decisions with dates.

## Required artifacts

### A. Stakeholder register

One row per stakeholder, with:

- Name and role, and which of the four role types they are: sponsor, domain decision owner, user, or informal influencer.
- What they are measured on.
- What they need from you.
- Preferred evidence type: working demonstration, traceable numbers, signed artifact, or trusted colleague's endorsement.
- Cadence and format.
- Disposition: champion, supportive, neutral, skeptical, or blocker.

Must include the informal influencer — the person others defer to — identified by observation, and at least one skeptic.

### B. Decision-rights table

For each decision area — data usage, access and authorisation, integration into a production system, change to an operator's process, model or provider choice, retention, go-live — record who decides, who is consulted, and who is informed.

Each "decides" entry must be confirmed with that person. Record the confirmation, and record any case where the person disagreed that the decision was theirs.

### C. Cadence plan with a bad-news protocol

Per stakeholder group: frequency, format, channel, and the specific evidence type.

Plus an explicit bad-news protocol: what you send when there is nothing good to report, who hears first, and how fast. State the rule in one sentence.

### D. Demo plan and script

Three synthetic incidents, chosen deliberately:

1. A clean case the system handles well.
2. An ambiguous case where evidence is weak and the system correctly declines with insufficient evidence.
3. A case where the system is wrong or hits a boundary.

For each: what you want to learn, not what you want to show. Plus the framing sentence you will use for the failure case, and the exact sentence you will use to decline making commitments in the room.

### E. Feedback capture log

One entry per item, recording: what happened; what the person expected instead; what they actually said, in their words; the class; who raised it; when; and the evidence.

Hesitations must be logged with their location in the interface — which control, label, or state — and at least three must be recorded.

### F. Classification

Every item classified as: defect, usability issue, missing requirement, integration request, training need, or expectation mismatch.

At minimum, your set must contain items in at least four classes. If real feedback did not produce that spread, state which classes are absent and why, rather than reclassifying to fill the table.

For each item, state the different response its class demands, and who owns it.

### G. Loud-versus-validated assessment

For each significant request, run and record four tests:

1. Frequency across independent sources.
2. Behavioural corroboration in telemetry — cite the trace or metric.
3. Observed as well as reported.
4. Survival of "what happened that made you think of that."

Then classify each as product evidence, local need, or single preference.

### H. Published rubric and scored backlog

The rubric across customer outcome, risk, effort, and strategic reuse — with the scoring scale written down — published to stakeholders before ranking. Then every item scored, with the resulting order.

### I. Decision update

In the fixed four-part shape: what we heard, in their words; what we are doing, with owner and date; what we are not doing and why, with reconsideration triggers; what we need from you.

Every item carries a status: accepted, deferred with trigger, declined with reason, reclassified, or needs more evidence. Any "needs more evidence" must name the evidence and who gathers it.

### J. Operator-facing release notes

Written for an operator, describing what changed in their workflow. No component names, no refactors, no internal terminology. Must include at least one entry about something that was decided not to change, with the reason.

### K. Shared pilot view

A small dashboard for the customer, not for you, containing at minimum: the agreed workflow outcome as a distribution over time, coverage, the three-way confirmation split, availability and 95th-percentile response time, running cost estimate, and open feedback items by status and age.

No raw incident content.

### L. Decision log

Every decision with: the decision, the positions considered, the reasoning, who decided, the date, and the measurement or condition that would change it.

Must include at least one entry resolving a genuine conflict between two stakeholders.

## Required demonstrations

1. **Live demo executed.** Run it. The operator holds the keyboard. Record what you did not say.
2. **Failure shown on purpose.** Record the framing you used and the reaction. Note whether trust appeared to rise or fall, and what was said.
3. **Conflict mediation.** Surface a real conflict between two stakeholder positions — the automatic-assignment conflict is the obvious one. Restate each position in terms of accountability, in front of both if possible, get confirmation, then propose a design that serves both accountabilities rather than splitting the difference. Record the design and the measurement that would revisit it.
4. **Refusal that lands.** Decline or defer one request. Then ask the requester to restate your reasoning in their own words. Record their restatement verbatim. If they can only restate that the answer was no, the refusal failed — revise and repeat.
5. **Loop-closure audit.** Pick five items at random. For each, show owner, status, evidence, decision date, and the record that the raiser was informed.
6. **Recall test.** Ask one stakeholder, unprompted, what happened to something they raised. Record their answer.
7. **Decision-rights verification.** For three decision areas, show the confirmation from the person you named as decider.

## Rubric

Grade each as pass or fail.

**Mapping**

- All four role types are represented, including the informal influencer, identified by observation not by title.
- At least one skeptic is in the register with real access.
- Every "decides" entry is confirmed with the named person.
- Dispositions are recorded and dated.

**Demo quality**

- A failure case was shown deliberately, with framing.
- The operator held the keyboard.
- At least three hesitations are logged with interface locations.
- No commitment was made in the room. If one slipped out, it is recorded as a slip and how you corrected it.

**Loop integrity**

- Every item has owner, status, evidence, and decision date.
- Items span at least four classes, or absences are explained.
- Every accepted item is routed to core, configuration, or adapter; anything else was escalated in writing.
- Loop closure happened for declined items as well as accepted ones.
- The random five audit passes with no gaps.

**Judgement**

- The rubric was published before ranking.
- At least one loud request was not acted on, with the four evidence tests shown.
- At least one quiet observation was acted on because telemetry corroborated it.
- The refused request's rationale was restated by the requester in their own words.
- The conflict resolution is on a different axis from the argument, not a midpoint.

**Communication**

- The update follows the four-part shape with statuses on every item.
- Release notes are in operator language and include a deliberate non-change.
- The shared dashboard contains the feedback backlog by status, and no raw incident content.
- The decision log entries state what would change each decision.

## Stop conditions

Stop and reconsider if any of these are true:

- Your register contains only supportive people.
- You are about to say "we can probably add that" out loud.
- You are driving the interface during the demo.
- Your demo shows only cases where the system succeeds.
- A feedback item has been open for a week with no owner.
- You are ranking items by who asked.
- You are building a customer-specific behaviour into the reusable core because it was faster.
- You have closed the loop only on the items you completed.
- You are writing release notes that mention a component name.
- You are resolving a stakeholder conflict privately, without both parties knowing the reasoning.

## Carry forward

Chapter 37 converts this into durable writing: the operator quick-start that replaces your demo, the engineering runbook, the ADR index that your decision log feeds, and the audience-specific status and incident notes. Chapter 38 uses the stakeholder register and the shared pilot view directly — the final handoff demonstration is to a sponsor, an operator, and a security reviewer, each of whom needs the evidence type you recorded here.

---

## Hints

Read these only after a real attempt. Each line is reversed. Reverse it to read it.

1. `.etarucca erom dna rellams gnihtemos otni nrut lliw stseuqer eht flah tuoba dna ,taht fo kniht uoy edam taht deneppah tahw ksA .tneve na si tseuqer erutaef yreve dniheB`
2. `.tneserp ecneidua na htiw ediced reveN .yad deman a yb noisiced a htiw uoy ot kcab emoc dna noitavresbo na sa taht erutpac em tel :moor omed eht rof ydaer ecnetnes eno evaH`
3. `.deman uoy nosrep eht htiw hcae yfirev neht ,aera noisiced rep ,demrofni si ohw dna ,detlusnoc si ohw ,sediced ohw nwod etirW .snoitseuq noitargetni dna ,ytiruces ,atad no sselhtrow si noipmahc ruoy morf sey A`
4. `.evah uoy evom tsurt tsegnorts eht si esoprup no yradnuob eht gniwohS .gnorw si ti erehw eno dna ,senilced yltcerroc metsys eht erehw eno ,naelc eno :stnedicni omed eerht esoohC`
5. `.raelcnu si etats ro lebal hcihw uoy sllet noitatiseh a ;stnemmoc tsuj ton ,noitacol yb snoitatiseh droceR .tnelis yats dna draobyek eht rotarepo eht eviG`
6. `.evom ylno s'retseuqer eht semoceb noitalacse dna ,thgils lanosrep a otni gniknar wol a snrut cirbur elbisivni nA .gnihtyna knar uoy erofeb cirbur noitasitiroirp eht hsilbuP`
7. `.sgniht uoy gnillet pots dna on snaem ecnelis taht nrael elpoep esiwrehtO .tliub uoy seno eht ylno ton ,denilced uoy smeti eht no pool eht esolC`
8. `.noitamrofni fo mhtyhr eht ni kaerb a etarelot ton od yeht ;smelborp etarelot srosnopS .tamrof emas ,yad emas ,keew dab eht no etadpu eht dneS`
9. `.tnemugra eht morf sixa tnereffid a no yllausu si noituloser ehT .seitilibatnuocca eht rof ngised neht ,stnaw hcae tahw naht rehtar rof elbatnuocca si hcae tahw etatser ,tcilfnoc sredlohekats owt nehW`
10. `.ylteiuq ti brosba reven ,ti etalacse :ksir krof a si eerht eht fo enon stif taht meti nA .retpada ro ,noitarugifnoc ,eroc si meti detpecca yrevE`
