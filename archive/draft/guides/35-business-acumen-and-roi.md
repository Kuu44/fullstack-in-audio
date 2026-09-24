---
chapter: 35
title: "Test — Make the FieldOps business case"
slug: 35-business-acumen-and-roi
lesson: docs/lessons/35-business-acumen-and-roi.md
audio: media/35-business-acumen-and-roi.mp3
type: test
---

# Chapter 35 test — Make the FieldOps business case

This is a test, not a tutorial. It states the goal, the constraints, the state you start from, and the artifacts you must produce. It does not tell you how. Hints are at the very end, inverted so you do not read them by accident. Open them only after a genuine attempt, and only one at a time.

Two parts of this test require running the system: extracting real per-triage cost telemetry, and producing baseline measures from instruments rather than from memory.

## Goal

Produce a business case for the FieldOps Copilot pilot that survives a hostile finance review, and an enterprise readiness map that shows the pilot can actually clear the customer's own approval machinery in time to matter.

You must be able to answer four questions with artifacts:

1. What is the measured starting point, and how confident is each number?
2. What does the system cost to run, at peak, derived from your own telemetry?
3. What benefit can be claimed, under what adoption assumption, converted to money by what stated policy?
4. Which approvals gate a production commitment, who owns each, how long does each take, and what evidence does each want?

## Starting state

- Chapter 33 discovery outputs, including the volume profile and the assumption log.
- Chapter 34 slice sequence, milestone plan with evidence gates, build/buy/configure/defer register, RAID log, and the timed rollback rehearsal.
- The running system with chapter 23 latency and cost telemetry, chapter 31 tracing and dashboards, chapter 32 risk-control pack, chapter 26 release manifest.

## Constraints

- **Every number carries a confidence label**: measured, sampled, documented, or estimated — plus its source. An unlabelled number is an automatic fail on that artifact.
- **Run cost must be derived from your own telemetry**, not from a provider price page alone. If your telemetry cannot produce a per-triage cost, fix the telemetry first.
- **Adoption is applied before money.** Any benefit figure that multiplies the full incident volume rather than the assisted share is invalid.
- **The hours-to-money conversion must be a separate, visible, labelled step** with a stated conversion policy (reduce cost / absorb growth / redeploy) and a stated labour rate marked as a given assumption.
- **No claim without a mechanism.** For every asserted impact, you must be able to describe the causal path in one sentence.
- **Activity is not impact.** Proposal counts, token counts, call counts, and session counts may appear as adoption metrics but may never appear as benefits.
- **Synthetic and anonymised data only.** No real incident text, no real customer names, no real salary data for a real person.
- **The claims boundary is written and dated before you compute any result.** Do the two lists first.
- **The readout is one page.** Not one page plus appendices that carry the argument.

## Starting state you must not break

- No change to system behaviour. This chapter measures and models.
- Cost telemetry changes are permitted only if they add measurement; they may not alter the triage path, latency budget, or evaluation results.
- If you add instrumentation, the evaluation gate must still pass unchanged.

## Required artifacts

### A. Claims boundary (write this first, and date it)

Two lists, dated before any results exist:

- **Will claim** — with the mechanism for each, in one sentence.
- **Will not claim** — including at least: incident volume reduction, customer satisfaction, prevented outages, and any revenue effect, unless you can produce a mechanism and an instrument for one of them.

### B. Baseline

Four measures: time to triage, rework rate, escalation rate, and incident business impact. Each with:

- A definition precise enough that two people would compute it identically. For time to triage, the endpoints must be named explicitly.
- The instrument that produced it.
- Sample size and period.
- Confidence label.
- The distribution, not just a central value: at minimum median and a tail figure, with a note on which part of the distribution your system is expected to affect.

### C. Value hypotheses, per slice

One falsifiable sentence per slice from your chapter 34 sequence: if we do this, then this measure changes, measured by this instrument, by at least this much. At least one hypothesis must be about a non-AI slice.

### D. Cost model, five categories

Implementation, run, operational labour, change, and customer opportunity cost. Requirements:

- Run cost derived from telemetry, computed at median volume **and** at the peak from your volume profile.
- Explicit treatment of retries, growth, periodic re-indexing, longer contexts under difficulty, and the observability backend.
- Operational labour named with a role and an hours-per-month figure — including who tends instructions, reviews rejected proposals, and re-indexes procedures.
- The cost ceiling and fallback behaviour from chapter 23 stated as a control on the run-cost line.
- A three-year total cost of ownership figure with its horizon and assumptions stated.

### E. Adoption metric definitions

Coverage, confirmation rate split three ways (accepted unedited / accepted with edit / rejected), abandonment, and repeat use per operator. For each: the definition, the instrument that will produce it, and the target you would consider healthy.

Abandonment requires recording a non-event. State how you will capture it.

### F. Benefit model

- Gross time benefit, with the coverage multiplication shown as its own step.
- Conversion policy, obtained as an answer (role-played if necessary) from the sponsor, stated verbatim.
- The hours-to-money conversion as a separate labelled step, or an explicit refusal to monetise with the reason.
- Quality benefit modelled separately from time benefit.
- Risk and auditability benefit stated qualitatively and explicitly not priced.

### G. Sensitivity analysis

Three scenarios — pessimistic, expected, optimistic — driven by coverage and per-incident time saved. Must include the combined pessimistic case where both are halved, and a one-line statement of what you would do if only the optimistic case clears cost.

### H. Attribution design

- Which method you will use: staggered rollout, holdout, or before-and-after.
- How your chapter 34 slice sequence gives you a natural comparison between context-only and context-plus-proposal.
- The confounders you already know about, named.
- If a holdout was refused, the record of the refusal and a statement that attribution is consequently weaker.

### I. Enterprise readiness map

Every gate between here and a production commitment: executive sponsor, data owner, security review, privacy or data-protection assessment, legal and contracting, procurement and vendor onboarding, architecture review, change advisory board, operations/support acceptance, training and change management.

For each: the named owner, the lead time, the required start date, whether it is already late, what evidence it wants, and **the artifact you already have that satisfies it**.

Also: the sponsor succession answer — who else would care if your sponsor left — and the fiscal calendar date by which results must exist to be actionable.

### J. One-page pilot readout

Seven sections: what we set out to test; what we did; what we measured (labels visible); what we learned, including at least one negative finding; what we recommend, with all four options genuinely stated; what we need from you; risks and open decisions.

## Required demonstrations

1. **Telemetry extraction.** Produce a per-triage cost figure from a real run of your own system, showing the trace or metric it came from. Then produce the same figure under a deliberately harder input where retrieval is weak and retries occur. Record both.
2. **Peak-hour cost.** Compute the monthly run cost at your volume profile's peak multiple, not the median, and record the difference.
3. **Recomputation.** Hand your inputs and assumptions to someone who was not involved and have them reproduce your headline conclusion. Record any number they could not trace.
4. **Hostile question drill.** Have someone play a sceptical finance partner and ask, at minimum: where did that baseline come from; what happens if adoption is half; what is this costing us monthly at peak; what line in our budget changes; and how do you know it was your system. Record your answers and which one you answered worst.
5. **Budget line answer.** Obtain or role-play the sponsor's answer to "if this succeeds, what changes in your budget or commitments." Record it verbatim.
6. **Gate lead-time audit.** For every gate, state today's date against the required start date and list every gate that is already late.

## Rubric

Grade each as pass or fail.

**Honesty of numbers**

- Every number is labelled and sourced.
- Time to triage has explicitly named endpoints.
- The key measure is reported as a distribution, with the affected part identified.
- Coverage is applied before monetisation.
- The hours-to-money conversion is a separate visible step with a stated policy.
- No benefit is an activity metric.

**Cost realism**

- Run cost comes from telemetry, at peak as well as median.
- Retries, growth, re-indexing, and observability all appear as lines.
- Operational labour has a role and an hours figure.
- The customer's own effort is counted.
- A three-year total cost of ownership exists with stated assumptions.

**Claim discipline**

- The claims boundary is dated before results.
- The refusal list includes prevented outages and revenue.
- Every claim has a one-sentence mechanism.
- Confounders are named by you, not discovered by the reviewer.

**Process realism**

- Every gate has an owner, a lead time, and a required start date.
- Every gate is mapped to an existing artifact, or the gap is named as work.
- Already-late gates are identified.
- Sponsor succession is answered.
- The fiscal calendar date is stated and the plan works backwards from it.

**Communication**

- The readout is one page and self-sufficient.
- All four options are stated and the non-continue options are plausible as written.
- At least one negative finding appears.
- The "what we need from you" section contains a specific action for a specific person by a specific date.

## Stop conditions

Stop and reconsider if any of these are true:

- Your spreadsheet has two decimal places and four guesses.
- You are computing benefit against total incident volume.
- You cannot say what a single triage costs.
- Your only benefit is time saved and you have not asked what the organisation will do with it.
- You wrote the claims list after seeing a result you liked.
- Your enterprise readiness map has no dates.
- You are treating security review as a document exchange rather than a queue.
- Your readout recommends continuing and nothing else.
- The pilot has no agreed decision date.
- You are about to present a percentage improvement without stating the sample, the period, and the confounders.

## Carry forward

Chapter 36 runs the relationship around these documents: the stakeholder register that turns the enterprise readiness map into a cadence, the demo that produces feedback, and the decision log that closes the loop on requests you will refuse. Chapter 37 writes the runbook that most enterprise readiness maps show as the one missing artifact. Chapter 38 presents this readout to a mock sponsor, operator, and security reviewer as part of the final handoff.

---

## Hints

Read these only after a real attempt. Each line is reversed. Reverse it to read it.

1. `.rewsna elgnis taht drawot ledom tifeneb elohw eht dliuB .elpoep yolpeder ro ,htworg brosba ,tsoc ecuder :emit derevocer htiw od lliw yeht sgniht eerht fo hcihw rosnops eht ksA`
2. `.meht fo lla ot ton ,htap detsissa eht hguorht tnew yllautca taht stnedicni eht ot seilppa tifeneb ehT .retfa ton ,yenom ot trevnoc uoy erofeb egarevoc yb ylpitluM`
3. `.etamitse na si ti ,drow on sah rebmun a fI .detamitse ,detnemucod ,delpmas ,derusaem :dehcatta sdrow ruof fo eno sdeen rebmun yrevE`
4. `.tonnac retfa-dna-erofeb elgnis a nosirapmoc a uoy sevig ,lasoporp sulp txetnoc neht ,IA tuohtiw txetnoc :ngised noitubirtta na ydaerla si ecneuqes ecils ruoY`
5. `.egareva eht naht rehtar ruoh kaep eht ledom neht ,dnekcab ytilibavresbo eht dna ,ytluciffid rednu stxetnoc regnol ,gnixedni-er cidoirep ,htworg ,seirter ddA .ecnecil a ton si tsoc nuR`
6. `.noitpmussa eht gnitsujda naht rehtar os yaS .ksat gnireenigne ytiroirp-tsehgih ruoy emoceb tsuj sah krow noitpoda ,oiranecs citsimitpo eht ni skrow ylno esac eht fI`
7. `.noitasilanoitar a si ti sdrawretfA .ti etad dna ,tsixe stluser yna erofeb ekam ot esufer lliw uoy smialc fo tsil eht etirW`
8. `.koobnur eht yllausu si pag eht ;meht fo tsom revoc 43 dna 23 ,13 ,03 ,82 ,62 sretpahC .ti seifsitas taht tliub ydaerla uoy tcafitra eht eman ,etag esirpretne hcae roF`
9. `.meht naem dna snoitpo ruof lla etirW .tnemesitrevda na si eunitnoc si noitadnemmocer ylno esohw tuodaer A`
