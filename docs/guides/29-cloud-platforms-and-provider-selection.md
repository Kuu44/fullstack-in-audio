---
chapter: 29
title: "Test — Select the customer cloud landing zone"
slug: 29-cloud-platforms-and-provider-selection
lesson: docs/lessons/29-cloud-platforms-and-provider-selection.md
audio: media/29-cloud-platforms-and-provider-selection.mp3
type: test
---

# Chapter 29 test — Select the customer cloud landing zone

A test, not a tutorial. Hints are reversed at the end.

## Goal

Choose a pilot cloud for FieldOps Copilot on the basis of customer constraints rather than preference, and design a landing zone in which no workload holds an unlimited identity and every byte of data has a known location.

## Starting state

Chapter 28 complete: a hardened, reproducible container image built by your pipeline, a release manifest, a local stack, and a documented image-policy questionnaire.

You also have the customer charter from chapter 1 and, if you have reached it, the discovery work from later chapters. If your charter does not yet name a customer concretely enough to have cloud constraints, invent them explicitly and label them as assumptions.

## Constraints

1. **Constraints before scoring.** Eliminating constraints are identified and applied before any weighted comparison. A matrix that scores an option already eliminated fails this test.
2. **Weights agreed before scores.** Record the weights, then score. Adjusting weights after seeing scores must be disclosed if it happens.
3. **No unlimited identity.** Four distinct identities: deployment, service runtime, operator, break-glass. Each has explicit may and may-not statements.
4. **Workload identity over stored keys.** Any stored long-lived cloud credential requires written justification.
5. **The database has no public endpoint.**
6. **Every data location is enumerated**, including database, backups, object storage, logs, traces, registry, and the model provider endpoint, each checked against the residency requirement.
7. **Spending alerts and resource tagging exist from the start**, not as a follow-up.
8. **Two availability zones, one region**, unless you write a justification for something else.
9. **No unstated assumption of outbound internet access.**
10. **Spend nothing you do not have to.** A design plus an executable plan satisfies this test. If you do provision, use the smallest resources available and destroy them when the rehearsal ends.
11. **Your own familiarity is a tiebreaker at most**, and must be declared as such where it influenced anything.

## Required artifacts

1. **A constraint interview record**: at minimum, existing cloud agreements, workforce identity provider, data residency jurisdiction, approved landing zone patterns, approved service list, egress policy, post-handover operator and their skills, and new-vendor procurement timeline. Real answers where you have them, labelled assumptions where you do not.
2. **An eliminating-constraint analysis** naming which options were removed and by what.
3. **A weighted decision matrix** over the surviving options, with weights recorded before scoring, covering identity fit, residency and regional fit, approved-service coverage, procurement and agreement, customer operational skills, model service fit, and cost.
4. **A landing zone diagram** naming every component and its network placement: network boundary, public and private subnets across two zones, load balancer, container service, managed PostgreSQL, secret manager, object storage, image registry, scheduled job runner, and observability collection.
5. **An identity specification**: four identities, each with granted permissions and an explicit list of what it must not be able to do.
6. **A break-glass procedure**: how it is invoked, who may invoke it, what it alerts, and the post-use review step.
7. **A data location table**: every store, its region, its retention, and its residency verdict.
8. **A monthly cost estimate** with visible assumptions, itemized at least across compute, database, storage and backups, networking and egress, observability, model inference, and the nonproduction environment. Include a spending alert threshold.
9. **A portability boundary statement**: the single hardest component to move, what moving it would involve, and an honest estimate of the disruption.
10. **A cloud decision record**: chosen provider, the constraints that drove it, the runner-up, the role your familiarity played, and what would trigger reconsideration.

## Required demonstrations

- **D1 — Elimination works.** Show at least one option removed by a constraint before scoring, with the constraint named.
- **D2 — Weights precede scores.** Show the weights recorded and confirmed before the scoring step.
- **D3 — Identity separation.** For each of the four identities, state one action it can perform and one it must not. If you provisioned anything, attempt a denied action and show the refusal.
- **D4 — No public database.** Show the database's network placement and the absence of a public endpoint.
- **D5 — Residency completeness.** Walk your data location table and show that logs and backups were checked, not just the primary database.
- **D6 — Egress reality.** State whether the workload may reach the model provider, and show the architectural consequence of the answer either way.
- **D7 — Cost visibility.** Present the estimate with assumptions, and show where the alert threshold is set and who it notifies.
- **D8 — Break-glass.** Walk through invoking it, what alerts, and who reviews it afterwards.
- **D9 — Portability honesty.** State what a provider migration would actually cost. An answer of "it's containerized so it's portable" fails.
- **D10 — Teardown.** If you provisioned anything, show it destroyed and the final cost.

## Rubric

| # | Criterion | Does not meet | Meets | Exceeds |
|---|---|---|---|---|
| 1 | Decision order | Matrix built before constraints gathered | D1 passes; eliminating constraints applied first | Constraints gathered from a real or role-played customer conversation, with quotes |
| 2 | Matrix integrity | Weights chosen to justify a preferred answer | D2 passes | Customer or proxy confirmed weights in writing before scoring |
| 3 | Identity design | One identity, or roles undefined | Four identities with may and may-not; D3 passes | Denied actions verified empirically, not asserted |
| 4 | Break-glass | Absent, or just an admin account | D8 passes with alerting and review | Its existence allowed standing privileges to be removed elsewhere; show what was removed |
| 5 | Network placement | Database publicly reachable | D4 passes; private connectivity to managed services | Reachability verified by attempting connection from an unauthorized position |
| 6 | Residency rigor | Only the database considered | D5 passes; all stores enumerated | Model provider endpoint region confirmed, not assumed |
| 7 | Egress realism | Internet access assumed | D6 passes with the architectural consequence drawn | Both permitted and forbidden variants of the architecture are sketched |
| 8 | Cost estimate | A single number | D7 passes with itemization and assumptions | Identifies which lines are fixed versus usage-driven and what to cut first |
| 9 | Cost governance | No tags, no alerts | Tagging scheme and alert threshold defined | Attribution demonstrated: pilot cost separable from the rest of the account |
| 10 | Availability design | Unjustified single or multi-region | Two zones, one region, stated | Failure modes covered and not covered are both named |
| 11 | Operability after handover | Not considered | Customer skills scored in the matrix | Named the specific team and the gap to close before handover |
| 12 | Portability | Claimed as easy | D9 passes with an honest assessment | Quantified in effort and downtime, with the riskiest step named |
| 13 | Approved services | Not checked | Every component checked against the approved list | Exceptions identified with the approval path and timeline |
| 14 | Decision record | Absent or informal | Complete record including the runner-up and reconsideration trigger | Familiarity bias declared explicitly and its influence bounded |
| 15 | Shared responsibility | Provider certifications offered as the security answer | Configuration-side controls articulated | Mapped each component to which side of the line its risk falls on |

## Stop conditions

- You are comparing service catalogues before you know the customer's constraints.
- Your recommendation matches the cloud you personally know best and you have not examined why.
- You cannot say where your logs are stored.
- One identity is used for both deploying and running.
- You are designing multi-region failover for a pilot with no proven adoption.

## Carry forward

Chapter 30 expresses this landing zone as reviewable, rebuildable infrastructure code and confronts whether Kubernetes belongs in it. Your component list and identity specification are the input to that work, so make them precise enough to be translated directly.

---

## Hints

Reversed. One at a time.

1. Finding eliminating constraints: `.rewsna on evah yeht fi noitpmussa na sa ti kram dna ,esoht ksA .ecalp ni si tahw tuoba snoitseuq neves htiw dael ,gnisoohc erofeB`
2. Identity separation: `.ees ll'uoy tahw yb desirprus eb yam uoY .dnoces eht ni ti tup ,htob fi ;nur ro yolped ot dedeen si ti rehtehw ksa noissimrep hcae roF`
3. Residency completeness: `.rotcaf gnisirprus tsom eht si noitanitsed gol ehT .stsil dna ,tsil eht klaW .taht tsniaga kcehc dna ,sdnal atad erehw yreve tsil`
4. Cost estimate: `.suounitnoc si tahw ecuder ,tsoc ecuder oT .ylgnidrocca redro dna ,tseuqer rep segrahc tahw dna ylsuounitnoc snur tahw etarapeS`
5. Break-glass value: `.ylno sisirc a ni deniag eb nac hcihw ,laveirter esoht evomer neht dna ,emit eht fo tsom deriuqer ton era taht sessecca gnidnats eht tsiL`
6. Portability honesty: `.tnempolevd ton ,noitargim atad si trap drah eht taht ees ll'uoy ;yad rebotcO na no revo hctiws ot spets eht etirW`
7. Egress: `.yxorp a hguorht detsilwolla eb tsum ti rehtehw neht ,tenretni cilbup eht hcaer nac ecivres eht rehtehw tsrif ksA`
