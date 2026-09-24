---
chapter: 38
title: "Capstone exam — Ship the FieldOps Copilot pilot candidate"
slug: 38-capstone-handoff
lesson: docs/lessons/38-capstone-handoff.md
audio: media/38-capstone-handoff.mp3
type: capstone-exam
---

# Chapter 38 capstone exam — Ship the FieldOps Copilot pilot candidate

This is the final exam of the whole course. It is not a tutorial and it is not a new topic. Everything it requires, you have already built across chapters 1 to 37. What is being tested is whether the system holds together without you helping it, and whether other people will take responsibility for it.

Hints are at the very end, inverted. Open them only after a genuine attempt, and only one at a time.

Read the rules before you begin. Two of them — the void-and-restart rule and the silence rule — are the exam. If you soften either one, you will pass a test you invented rather than this one.

## Goal

Produce a FieldOps Copilot pilot candidate that a real enterprise customer could accept, and hand it over so completely that their confidence does not depend on your presence.

Three things must be true and demonstrated:

1. One synthetic incident travels the full system with no manual intervention of any kind, and a single correlation identifier is present at every hop.
2. The agent is grounded, bounded, approval-gated, evaluated, and observable — each proven by an artifact, not by an accuracy figure.
3. A sponsor, an operator, and a security reviewer each leave with a recorded decision, or with a recorded statement of exactly what they still need.

## Starting state

The complete FieldOps Copilot system through chapter 32, plus all Part VII outputs:

- Chapter 33: evidence-based charter, requirements with instruments, assumption log, volume profile.
- Chapter 34: slice sequence, dependency map, milestone plan, RAID log, build/buy register, four-level rollback and contingency plan with timings.
- Chapter 35: baseline with confidence labels, cost model from telemetry, adoption metric definitions, claims boundary, enterprise readiness map, one-page readout.
- Chapter 36: stakeholder register with decision rights, feedback loop with statuses, decision log, shared pilot view.
- Chapter 37: operator quick-start, symptom-indexed runbook, decision index, diagram set, onboarding guide, all validated by silent transfer.

## The two rules

**The void-and-restart rule.** During the golden path run you may not touch anything: no manual database edit, no component restart, no cache clear, no pipeline refresh, no re-running a step. If you intervene in any way, the run is void. Record the intervention, fix its root cause properly, and start the run again from the beginning.

**The silence rule.** During any transfer, rollback, or rebuild performed by another person, you may not speak. Not a hint, not a correction. Every word you would have said is a defect in an artifact. Record it instead.

## Constraints

- **Everything is tested against a pinned candidate.** Nothing is tested against "the system".
- **Synthetic data only**, throughout. No real incident text, no real customer identifiers, no real credentials.
- **No new features.** You may fix defects surfaced by this exam. Each fix produces a new pinned candidate and a record of what was rerun.
- **Bounded means the capability does not exist.** A write capability that exists but is forbidden by instruction does not satisfy the bounded property.
- **Every claim in the readout stays inside the chapter 35 claims boundary.** If a result tempts you past it, the boundary wins.
- **Residual risk is disclosed, not softened.** Implemented controls and future commitments must be visually distinct.
- **The demo runs from the rehearsed environment**, on the pinned candidate, with pinned data. Not from a machine only you can run.
- **Failed attempts are part of the submission.** Concealing them fails the exam.

## Starting state you must not break

- The evaluation gate passes at the pinned candidate before any demonstration is given.
- Every injected failure is reverted and the revert verified with an instrument.
- The environment destroyed for the cold rebuild is a non-production environment, and it is rebuilt and verified before you finish.

## Required artifacts

### A. Pinned release candidate

A release manifest naming: application version, instruction/prompt version, model and provider, embedding model, retrieval index revision, infrastructure definition revision, and configuration set. Named, dated, immutable.

Every subsequent artifact references this manifest. If you produce a second candidate, both are recorded with what was rerun against each.

### B. Seam census

One row per seam, minimum: browser to interface layer; interface to system of record; interface to cache; interface to pipeline read model; agent to lookup tool; agent to retrieval; agent to model provider; service to notification path; CI to deployment; runtime to configuration and secrets; all components to observability.

Each row states: the contract, the failure mode, the timeout, the fallback, and what the user sees. Any cell you cannot fill is a defect logged and fixed in this chapter.

### C. Golden path run record

One synthetic incident traversing: authenticated intake, server-side validation, persistence with idempotency, asset context labelled found / not-found / stale, tenant-filtered retrieval, agent proposal with a citation to a specific passage, operator decision, audit record naming the actor, notification attempt recorded either way, and trace plus dashboard reflecting all of it.

The record must include:

- The list of hops, named.
- Proof that one correlation identifier appears at every hop, in an artifact a third party could query.
- **Every voided attempt, with the intervention that voided it and the root cause you fixed.**

### D. Adversarial pass records

1. **Evaluation suite** at pinned versions, compared to baseline, with the result stored against the manifest.
2. **Abuse cases**, minimum four: prompt injection in incident text; cross-tenant retrieval attempt; attempt to make the agent perform a write or consequential action; authorisation bypass on a normal operation. Each must fail safely, visibly, and leave evidence a reviewer could find unaided.
3. **Dependency failures**, each taken down in turn: system of record, cache, model provider, pipeline data, retrieval index. For each, record all three: the user-visible behaviour, the alert and whether it was actionable, and whether the runbook entry matched reality. **Every mismatch found is a pass, and must be recorded and fixed.**
4. **Rollback rehearsal** from this candidate to the previous approved manifest, executed from written steps by someone other than their author, timed per step, then restored forward and verified with an instrument.

### E. Realistic-conditions record

A synthetic batch reproducing your measured volume profile: duplicate/reopen share, ambiguity mix, messy and malformed inputs, non-incidents, and a compressed peak burst at your measured peak multiple. Plus at least two concurrency cases: two operators on one incident, and an approval arriving while a proposal is generating.

Report: 95th-percentile latency under burst against the chapter 23 budget; cost per triage under burst against the ceiling; refusal rate on messy versus clean inputs; state-machine integrity (no orphaned proposals, no intermediate states, no audit gaps); and **the load at which the system stops behaving as documented**.

### F. Automated end-to-end suite

The golden path as an executable test: real interface layer, real authenticated identity, assertions on persistence, idempotency, asset freshness labelling, tenant filtering, citation presence, approval, audit actor, and correlation identifier at every hop.

Requirements: runs with no credentials and no network using the chapter 15 deterministic fake; asserts observable outcomes rather than internals; a separate scheduled live path against the real provider with synthetic data; and wired into the chapter 27 pipeline as a gate alongside the evaluation gate.

### G. Agent readiness evidence — five artifacts

1. **Grounded**: a run citing a specific passage, and a weak-evidence run that correctly declined.
2. **Bounded**: the tool inventory showing no write capability exists, plus a rejected attempt.
3. **Approval-gated**: an audit record naming the human who decided.
4. **Evaluated**: the evaluation result stored against this manifest, including negative and safety cases, plus a deliberately regressed version that the suite detects.
5. **Observable**: one proposal from which instruction version, model, index revision, latency, and cost can all be reconstructed.

### H. Readiness review — six gates

Functional, safety, operability, reproducibility, evidence, reversibility. Each with its evidence artifact and a pass or fail.

Reproducibility requires the **cold rebuild**: destroy the non-production environment entirely, recreate it from declared infrastructure and the pinned manifest using only reviewed artifacts and nothing from your shell history. Record every manual step it exposed and whether you automated or documented each one.

### I. Three demonstrations, designed backwards from decisions

For each of sponsor, operator, and security reviewer, record: the decision they must make; their evidence type from the chapter 36 register; what you showed; **the failure you showed them deliberately** and why it addressed their specific concern; the limits you stated; the ask; and the outcome.

Suggested deliberate failures: cost ceiling engaging the fallback (sponsor); insufficient-evidence decline (operator); blocked cross-tenant retrieval appearing in the log (security reviewer).

Outcomes must be recorded as: a decision, or a refusal to decide plus exactly what is missing. An operator's qualified yes is captured in their own words. A security reviewer's conditional approval is captured verbatim as conditions.

### J. Handoff packet

With an index, and an owner per document **including on the customer side**:

Revised charter; diagram set; release manifest; risk-control pack; operator quick-start; engineering runbook; ROI model with labelled assumptions; feedback and decision process; open decisions; acceptance criteria results; evaluation baseline at pinned versions; timed rollback record; residual risk register.

Plus a section titled **what is not true yet**: what the pilot did not prove, what is bridged or manual, what is deferred with its trigger, and what must change before real customer data.

### K. Honest close

Three lists and a date:

1. **Evidence produced** — what you now know that you did not, with instruments and confidence labels.
2. **Risks remaining** — each with an accountable owner and the customer decision it requires, with implemented controls visually separated from future commitments.
3. **Conditions for a real-data launch** — as a checklist someone could work through.

Plus the agreed pilot decision date, in writing.

## Required demonstrations

1. Golden path completed under the void-and-restart rule, with every voided attempt recorded.
2. Correlation identifier traced across every named hop by someone who did not build the system.
3. All four abuse cases executed, each leaving discoverable evidence.
4. All five dependency failures executed against the three-part standard.
5. Realistic batch executed under burst, with the documented-behaviour limit stated.
6. End-to-end suite passing in the pipeline with no credentials present.
7. Cold rebuild completed from reviewed artifacts alone.
8. Rollback executed by a non-author, timed, and restored with instrument verification.
9. Three demonstrations delivered, each producing a recorded decision or a recorded gap.
10. Deliberate regression detected by the evaluation gate, then reverted.

## Rubric

Grade each as pass or fail. Any fail means the pilot candidate is not ready.

**Integration**

- Golden path completed with zero interventions on the passing run.
- Every seam has a contract, failure mode, timeout, fallback, and user-visible behaviour.
- No manual database repair anywhere in the exam.
- State machine intact under concurrency.

**Observability**

- One correlation identifier at every hop, verified by a third party.
- Every proposal reconstructible to instruction version, model, index revision, latency, and cost.
- Dashboards show both service health and workflow health, with no raw incident content.
- Every dependency failure produced an actionable alert.

**Agent readiness**

- All five properties evidenced by artifacts.
- Bounded is proven by the absence of the capability, not by instruction.
- The deliberate regression was detected.
- Quality claims and safety claims are stated separately.

**Operability and reproducibility**

- Cold rebuild succeeded from reviewed artifacts only; every exposed manual step is automated or documented.
- Runbook matched reality for all five failures, with mismatches recorded and fixed.
- Rollback executed by a non-author, timed, restore verified with an instrument.
- The load limit at which documented behaviour breaks is stated.

**Handoff and honesty**

- Every packet document has an owner on the customer side.
- The "what is not true yet" section exists and is specific.
- Residual risks each have an accountable owner and a required customer decision.
- Implemented controls are visually distinct from future commitments.
- No claim exceeds the chapter 35 boundary.
- Failed attempts, voided runs, and runbook mismatches are all disclosed.

**Decisions**

- Three demonstrations each ended in a recorded decision or a recorded gap.
- Each audience was shown a failure relevant to their own concern.
- The operator's qualification is in their words; the reviewer's conditions are verbatim.
- A pilot decision date is agreed in writing.

## Stop conditions

Stop and reconsider if any of these are true:

- You just fixed something mid-run and want to keep going.
- You are testing "the system" rather than a named pinned candidate.
- Your dependency-failure test asserts only that nothing crashed.
- You are about to skip the cold rebuild because the environment works.
- Rollback is being rehearsed by the person who wrote the steps.
- You are preparing one demo to give three times.
- You are presenting from your own laptop.
- A result is better than your claims boundary permits and you are rewriting the boundary.
- The residual risk register is being softened before a meeting.
- Your submission reports a clean first attempt with nothing found.
- There is no pilot decision date.

## After the capstone

You have now taken an ambiguous customer outcome to a deployed, observable, bounded, reversible, documented system, and handed it to people who can operate it without you. That arc — evidence before scope, thin slices before grand plans, safety and operability as floors, every input producing a visible decision, and nothing claimed beyond the instruments — is the work.

Do it again with a real customer, and keep the rules.

---

## Hints

Read these only after a real attempt. Each line is reversed. Reverse it to read it.

1. `.deyolped saw tahw tuoba gnihton remotsuc eht sllet tcafitra deman a ot deit eb tonnac taht tluser noitargetni nA .tset tsrif eht erofeb etadidnac eht niP`
2. `.tnatropminu redisnoc uoy maes a ta ,kcabllaf eht syawla tsomla si rewsna denifednu ehT .kcabllaf ,tuoemit ,edom eruliaf ,tcartnoc :snoitseuq ruof rewsna dna maes hcae klaW`
3. `.revo trats ,esuac eht xif ,noitnevretni eht drocer ,nur eht dioV .koobnur ruoy morf gnissim pets a si nur nedlog eht gnirud noitnevretni yrevE`
4. `.gnorw si taht eno eht eb ot koobnur eht tcepxE .koobnur eht dna ,trela eht ,ruoivaheb elbisiv-resu eht :eerga sgniht eerht nehw ylno sessap tset eruliaf-ycnedneped A`
5. `.deman ecivres on htiw tnemgarf a no sevom yllautca langis ecnedifnoc eht rehtehw kcehc nehT .elpitlum kaep dna ,xim ytiugibma ,erahs etacilpud derusaem ruoy morf hctab eht dliuB`
6. `.mialc ytefas a ton ,mialc ytilauq a evah uoy ,ti gnisu sdibrof ylerem noitcurtsni eht dna stsixe ytilibapac etirw eht fI .tpmorp eht fo ton ,yrotnevni loot eht fo ytreporp a si dednuoB`
7. `.wodniw egnahc laer a dekcolb evah dluow taht seno eht era dnif uoy spets launam ehT .yrotsih llehs ruoy morf gnihton htiw ,ylno stcafitra deweiver morf ti dliuber dna tnemnorivne noitcudorp-non eht yortseD`
8. `.reweiver eht rof laveirter tnanet-ssorc dekcolb ,rotarepo eht rof ecnedive tneiciffusni ,rosnops eht rof gniliec tsoc :raef nwo rieht sesserdda taht eruliaf eht ecneidua hcae wohs dna ,ekam tsum nosrep taht noisiced eht morf sdrawkcab omed hcae ngiseD`
9. `.lavorppa sa ton ,snoitidnoc sa mitabrev nwod ti etirW .tnemegagne eht ni ecnetnes elbaulav tsom eht si reweiver ytiruces a morf sey lanoitidnoc A`
10. `.gniteem doog a tcetorp ot piks ot detpmet eb lliw uoy eno eht si noitces tahT .tey eurt ton si tahw deltit noitces a sdeen tekcap eht dna ,edis remotsuc eht no renwo na sdeen tekcap eht ni tnemucod yrevE`
11. `.decrofne ton erew selur eht snaem tI .tluser gnorts a ton si spets dliuber detnemucodnu on dna ,sehctamsim koobnur on ,snoitnevretni on htiw tpmetta tsrif naelc A`
