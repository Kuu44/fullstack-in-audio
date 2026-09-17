---
chapter: 34
title: "Test — Sequence the customer pilot"
slug: 34-scoping-and-sequencing
lesson: docs/lessons/34-scoping-and-sequencing.md
audio: media/34-scoping-and-sequencing.mp3
type: test
---

# Chapter 34 test — Sequence the customer pilot

This is a test, not a tutorial. It states the goal, the constraints, the state you start from, and the artifacts you must produce. It does not tell you how. Hints are at the very end, inverted so you do not read them by accident. Open them only after a genuine attempt, and only one at a time.

One demonstration in this test requires you to actually execute something against the running system: the rollback rehearsal. Do not write it up without performing it.

## Goal

Produce a delivery sequence for the FieldOps Copilot pilot that a customer sponsor would approve and that an engineer arriving cold could execute.

The sequence must be defensible on three grounds simultaneously:

1. It produces usable customer evidence before the whole system is deployed.
2. It retires your largest unknowns early rather than late.
3. It moves scope, speed, and polish without moving safety or operability.

## Starting state

FieldOps Copilot as built through chapter 32, plus the chapter 33 discovery outputs:

- Prioritised functional and nonfunctional requirements, each traced to a finding.
- Assumption log with load-bearing assumptions marked.
- Current-state workflow map with working time and waiting time separated.
- Volume profile: daily volume and hourly distribution, peak multiple, duplicate share, age tail.
- Revised charter with a three-way boundary (in first release / deferred with trigger / out of scope) and a subtraction statement.
- Acceptance criteria that name their instruments.

If any of those are missing or vague, go back. This test is not survivable on invented inputs — it will produce a plan that looks fine and encodes your guesses.

## Constraints

- **Slices, not layers.** Every slice must cross the full stack and end in a real user action. A slice consisting of only backend work, only schema work, or only infrastructure work is invalid.
- **Slice one stands alone.** It must be deployable and usable with every later slice absent.
- **No slice may depend on a later slice**, in any of the three dependency types. Circular dependencies between slices are an automatic fail.
- **The AI proposal capability may not be slice one or slice two** unless you can produce a written argument from your own discovery evidence that overrides the reliability-first ordering. If you make that argument, it must cite specific findings.
- **Every tradeoff is paired with a floor.** Any tradeoff recorded without an explicit statement of what quality property did not move is invalid.
- **Safety and operability are not tradeable.** Tenant isolation, authorisation on every operation, audit records, redaction, tracing, and rollback are floors for every slice including the first.
- **Deferrals need observable triggers.** A reconsideration condition expressed as a date, or as "later", or as "after the pilot", does not count.
- **The rollback rehearsal must be performed, timed, and performed by instructions someone else could follow.** A described rollback scores zero.
- **No new features.** This chapter plans and rehearses. It does not add capability to the system.

## Starting state you must not break

- The system builds, tests, passes its evaluation gate, and deploys exactly as it did at the end of chapter 32.
- After the rollback rehearsal, the system must be returned to its pre-rehearsal state, verified, not assumed.
- The chapter 33 artifacts are not edited to fit the plan. If planning reveals that a requirement was wrong, record it as a new finding with a date; do not rewrite history.

## Required artifacts

### A. Slice definitions

Six to eight slices covering the first release. Each slice states:

- The user-visible capability, in one sentence with a trigger, an actor, and a result.
- The named beneficiary role, and the sentence you want that person to say after using it.
- The evidence it produces: what you will know afterwards that you do not know now.
- Its acceptance criteria, referenced from the chapter 33 set.
- Which requirements it satisfies, by reference.
- What is deliberately absent from it.

### B. Dependency map

A single map with three visually distinct edge types:

- **Hard technical**: B cannot function without A.
- **Organisational**: B cannot proceed until a human institution acts. Each of these carries an owner, an estimated lead time, a required start date, and how you will know it is progressing.
- **Evidence**: B should not be finalised until A has taught you something. State what specifically must be learned.

Then mark the critical path, and state in one sentence whether it runs through work your team controls or work it does not.

### C. Decision register: unknowns and one-way doors

Per slice:

- Unknowns, each cross-referenced to the chapter 33 assumption log where applicable.
- Irreversible decisions, with: what makes it irreversible, the cost of reversing it, what evidence you want before taking it, and whether that evidence is affordable.

At minimum, the register must address: tenancy model, identity integration shape, the incident-to-asset join identifier, whether raw incident text is stored and for how long, and where customer procedure content is processed.

### D. Priority ranking, twice

Two rankings, both shown:

1. Ranked by customer impact and effort only.
2. Re-ranked by uncertainty retired per unit of effort.

Then the final chosen order, with a paragraph explaining every position where the two rankings disagreed and which one you followed.

Where a high-risk slice sits late, identify the cheap probe — a spike of a few days or a single conversation — that can retire its uncertainty early without moving the slice.

### E. First-two-slices defence

A written defence of slices one and two, in terms of customer value and risk retired, that explicitly does not appeal to technical interest, novelty, or demo impact. It must cite at least two specific discovery findings, including at least one number from the volume profile.

### F. Build / buy / configure / defer register

For at least six capabilities — including model access, retrieval storage, orchestration, observability backend, identity, and notification — record the choice with:

- Whether the capability is differentiating value or plumbing.
- Where the data must travel, and whether that is permitted.
- The reversal cost, and what interface keeps it reversible.
- Total cost including procurement and security review time, not just licence.
- Who operates it at 3 a.m.
- The sentence stating what would change the answer.

### G. Explicit tradeoff record

At least one tradeoff, written as: the decision; the option chosen from defer / simplify / buy / remove; who is affected; the cost in plain language; and the quality floor that did not move.

At least one of your tradeoffs must remove or defer something you already built.

### H. Milestone plan with evidence gates

Each milestone states: the slice, the organisational prerequisites that must be complete, the acceptance criteria that must pass, the instruments producing the evidence, the go / no-go decision it enables, and who makes that decision.

A milestone that cannot fail is invalid.

### I. RAID log

Risks, assumptions, issues, and dependencies, kept distinct. Each entry has an owner and a review date. Dependencies carry lead times.

### J. Rollback and contingency plan

Rollback at four levels, each with trigger conditions, the decision owner, the expected duration, and the communication step:

1. Turn the behaviour off.
2. Revert to the previous release manifest.
3. Data-shape reversal: what is forward compatible, what needs a migration, what would cost data.
4. Withdraw to the prior manual process.

Contingency, separately, for the top three organisational dependencies: trigger date, fallback, named decider.

## Required demonstrations

1. **Independence proof.** Deploy or run the system with only slice one's capabilities enabled — later slices switched off or absent — and show a real user action completing end to end. Record what an operator can and cannot do in that state.
2. **Circularity check.** Walk the dependency map and show that no slice pair depends on each other in both directions. Record the pass.
3. **Rollback rehearsal, level one and level two.** Execute both. Time them with a clock. Have someone other than the author follow your written steps, or if that is impossible, follow steps you wrote at least a day earlier without editing them during execution. Record: elapsed time per step, what was ambiguous, what you had to improvise, and the corrected instructions.
4. **Restore verification.** After rehearsal, verify the system is back to its prior state using an instrument, not an impression: the evaluation gate, a trace, or a test run.
5. **Three-sentence tradeoff.** Deliver your main tradeoff aloud in three sentences to someone playing the sponsor. One of the three must name the cost. Record their first question.
6. **Lead-time audit.** For every organisational dependency, state today's date, the required start date, and whether you are already late. Record any that are already late.

## Rubric

Grade each as pass or fail. Any fail means incomplete.

**Slicing**

- Slice one is independently deployable and usable, demonstrated, not asserted.
- Every slice has a named beneficiary and the sentence they would say.
- Every slice produces evidence that changes what you know.
- No slice is a pure layer. No milestone before the first user action.
- No circular dependencies.

**Risk discipline**

- Organisational dependencies appear on the dependency map with owners and lead times.
- The critical path is identified, and if it runs through work you do not control, that is stated.
- The top load-bearing assumption is retired in the first two slices or by a probe running in parallel.
- Every one-way door has a cost of reversal and a stated evidence requirement.

**Tradeoff honesty**

- Every tradeoff names a cost in plain language.
- Every tradeoff names the quality floor that did not move.
- No tradeoff moves tenant isolation, authorisation, audit, redaction, tracing, or rollback.
- At least one tradeoff removes or defers something already built.
- Every deferral has an observable reconsideration trigger a customer could independently evaluate.

**Executability**

- The rollback was performed and timed, not described.
- The written rollback steps survived being followed without editing, or the corrections are recorded.
- Restore was verified with an instrument.
- Each milestone has a failure condition and a named decider.

## Stop conditions

Stop and reconsider if any of these are true:

- Your first milestone contains no user.
- You are estimating durations before you have drawn the organisational dependencies.
- Every slice is roughly the same size, and that size matches your sprint length.
- The plan's order is the order in which you originally built the components.
- You cannot name a single thing that will not be in the first release.
- You are writing "we will add authorisation / observability / audit after the pilot."
- Your rollback plan's first step is to redeploy.
- The customer's existing process is being decommissioned before the pilot proves out.
- You are about to buy a component whose data path you have not checked against the security constraint.

## Carry forward

Chapter 35 turns this sequence into money and approvals. It needs the volume profile, the build/buy register with its cost columns, the milestone plan, and the organisational dependency list — because the security review, the data owner, and procurement are the same institutions that gate a business case. Chapter 36 needs your RAID log and your deferral list with triggers, because deferrals are what stakeholders will push back on. Chapter 38 will execute the rollback rehearsal again as part of release readiness, so keep the timed steps.

---

## Hints

Read these only after a real attempt. Each line is reversed. Reverse it to read it.

1. `.noitibma htiw reyal a si ti ;ecils a ton si gnissim era secils evif txen eht elihw yolped tonnac uoy ecils A`
2. `.tey seicnedneped lanoitasinagro eht nward ton evah uoy ,smrofrep maet nwo ruoy krow ylno sniatnoc htap lacitirc ruoy fI`
3. `.ecils ksir-tsehgih eht edisni gnidih eborp yad-owt eht rof kool neht ,syortsed ti tsil noitpmussa gniraeb-daol ruoy fo hcum woh yb ecils hcae knaR`
4. `.roolf a dedart uoy ,etirw ot drah si ecnetnes dnoces eht fI .evom ton did yllacificeps tahw dna ,rellams tog tahw :secnetnes owt sa ffoedart eht etirW`
5. `.rood yaw-eno a si niamod ruoy otni kael sreifitnedi esohw tnenopmoc thguob A .rodnev eht fo ton ,ecafretni eht fo ytreporp a si ytilibisreveR`
6. `.nwod rebmun eht etirw dna lasraeher eht emiT .ytilibapac ton ,noitatnemucod si rohtua sti naht rehto enoemos yb detucexe neeb reven sah taht kcablloR`
7. `.rediced deman a dna etad reggirt a eno hcae eviG .sevirra reven no dedneped ew gniht eht fi tahw tub ,dab si deppihs ew tahw fi tahw ton :kcabllor morf noitseuq tnereffid a srewsna ycnegnitnoC`
8. `.owt htnom gnimarf tnaw uoy nossel eht si taht rehtehw dna ,eno keew ni metsys eht tuoba nrael lliw noitasinagro eht tahw ksa ,redro ruoy ni tsrif si tnenopmoc evisserpmi eht fI`
