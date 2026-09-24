---
chapter: 30
title: "Test — Declare the pilot deployment"
slug: 30-infrastructure-as-code-and-kubernetes
lesson: docs/lessons/30-infrastructure-as-code-and-kubernetes.md
audio: media/30-infrastructure-as-code-and-kubernetes.mp3
type: test
---

# Chapter 30 test — Declare the pilot deployment

A test, not a tutorial. Hints are reversed at the end.

## Goal

Make the chapter 29 landing zone reviewable, rebuildable, and destroyable from definitions alone, and reach a defensible, evidenced decision about whether Kubernetes belongs in this deployment.

## Starting state

Chapter 29 complete: a chosen cloud, a landing zone diagram, four identity specifications, a data location table, a cost estimate, and a portability statement. Chapter 28 gave you a hardened image with health checks.

## Constraints

1. **No console clicking.** Every resource that constitutes the environment is declared. The only permitted manual step is the state-storage bootstrap, which must be documented as an explicit exception.
2. **State is remote, locked, encrypted, and access-controlled.** No local state for anything shared.
3. **Plan before apply, always.** For any production-like environment the plan is a reviewed artifact, not a scroll-past.
4. **Stateful resources carry deletion protection**, and removing it is its own reviewed change.
5. **Modules and environment values are separate.** The same modules produce pilot and production-like environments, differing only by inputs.
6. **No secret value in any definition, in version control, or in plan output.** Secret containers are declared; values are populated out of band.
7. **Policy checks enforce your chapter 29 rules**, at minimum: no public database endpoint, no public object storage, encryption enabled, and required tags present.
8. **Split by lifecycle.** A routine service change must produce a plan that does not touch network, identity, or database.
9. **Kubernetes workloads, if any, declare resource requests and limits and both readiness and liveness probes.**
10. **Destroy what you rehearse with.** The nonproduction environment is torn down at the end and the teardown is verified.
11. **Spend as little as possible.** Smallest viable resources; a local cluster is acceptable for the Kubernetes portion.
12. **If you would be applying into a real customer account, follow their change process**, even when you hold the credentials.

## Required artifacts

1. **Modules** for at least: network, identity, data, platform (registry, storage, secrets, observability), and service (runtime, load balancer, scheduled job).
2. **Environment configurations** for pilot and one other, composing the same modules with different values.
3. **A documented bootstrap procedure** for state storage and locking, marked as the one manual exception.
4. **A dependency and apply-order statement**: what each module outputs, what each consumes, and the order in which they apply, in one sentence.
5. **A reviewed plan artifact** for at least one change, with an annotation of anything that would be replaced rather than updated.
6. **A policy-as-code rule set** implementing your chapter 29 design rules, with at least one rule proven to reject a violating definition.
7. **A drift detection mechanism**: a scheduled plan with an alert when it is non-empty, plus a written reconciliation obligation with a time window.
8. **Kubernetes manifests** for the API: a Deployment with replicas, resource requests and limits, readiness and liveness probes wired to the chapter 28 endpoints, a Service, configuration injection, and a secret reference that does not store the value in the cluster. Plus your packaging choice (templating or overlays) with a one-line reason.
9. **A deployment target decision record**: managed container service or Kubernetes, the reasoning, the operational burden enumerated, the alternative, and the trigger that would change the decision.
10. **A rebuild-from-nothing record**: the destroy, the rebuild, the time taken, and confirmation that the application works afterwards.

## Required demonstrations

- **D1 — Rebuild from nothing.** Destroy the nonproduction environment and rebuild it from definitions with no console steps. Show the application working. Record the elapsed time.
- **D2 — Plan literacy.** Produce a plan and explain every line, explicitly identifying anything marked for replacement.
- **D3 — Destruction blocked.** Attempt a change that would destroy the database. Show protection preventing it.
- **D4 — Environment parity.** Show two environments built from the same modules with different inputs, and name every difference.
- **D5 — Secret absence.** Show a secret existing and usable, with its value absent from definitions, version control, and plan output.
- **D6 — Drift detected.** Make a manual change out of band. Show the scheduled plan reporting it and the reconciliation performed.
- **D7 — Policy rejection.** Submit a definition with a public database endpoint. Show the policy check rejecting it before apply.
- **D8 — Blast radius.** Make a routine service change. Show the plan touching only the service.
- **D9 — Kubernetes rolling update.** Deploy to a cluster, then roll out a new version while requests are in flight. Show zero dropped requests and probes behaving correctly.
- **D10 — Resource behavior.** Show requests and limits set, and demonstrate what happens when the limit is approached.
- **D11 — Teardown.** Destroy everything. Show nothing remains and report the final cost.

## Rubric

| # | Criterion | Does not meet | Meets | Exceeds |
|---|---|---|---|---|
| 1 | Rebuildability | Manual steps required | D1 passes with only the documented bootstrap exception | Rebuild time measured and the slowest step identified |
| 2 | State handling | Local or unlocked | Remote, locked, encrypted, access-controlled | Access to state is itself least-privilege and audited |
| 3 | Plan discipline | Apply without review | D2 passes; replacements identified | Plan generated in the pipeline and attached to the change for a second reviewer |
| 4 | Stateful safety | No protection | D3 passes | Backups verified by restoring one, not just enabled |
| 5 | Module design | Monolith or tangle | Five units; D8 passes; apply order stated in one sentence | Dependency direction is explicit and inverted nowhere |
| 6 | Environment separation | Values embedded in modules | D4 passes | Differences between environments are enumerable from configuration alone |
| 7 | Secret handling | Values in definitions or state | D5 passes | Workload identity used; no secret material transits the pipeline |
| 8 | Policy enforcement | Rules exist only as intentions | D7 passes for at least one rule | All four chapter 29 rules enforced, and a violation attempt is logged |
| 9 | Drift management | Undetected | D6 passes with a written reconciliation window | Drift rate tracked over time as an operational signal |
| 10 | Kubernetes competence | Manifests copied without understanding | D9 and D10 pass | In-cluster access control mapped to cloud identities, and the mapping documented |
| 11 | Probe correctness | Liveness depends on a dependency | Readiness and liveness distinct and correct | Rolling update verified under sustained load, not a single request |
| 12 | Packaging | Duplicated manifests per environment | One definition with injected values, choice justified | Environment differences reviewable as a small diff |
| 13 | Decision quality | Preference, or unexamined default | Decision record with burden enumerated and a trigger | Burden estimated concretely: upgrades, node management, access mapping, add-ons |
| 14 | Teardown | Environment left running | D11 passes with verification | A scheduled check confirms no orphaned resources remain |
| 15 | Customer process fit | Would apply using held credentials | Change process identified and followed | Plan shared with the platform team in advance of the first apply |

## Stop conditions

- You are applying from your laptop to something shared.
- Your plan output is too long to read and you are confirming anyway.
- You are adopting Kubernetes and cannot list five things you will now own.
- Your modules contain environment names.
- You are leaving the rehearsal environment up "just in case".

## Carry forward

Chapter 31 instruments what you have declared. Health probes become one signal among many, and the correlation identifier will need to survive every boundary you just created: load balancer, service, database, job runner, retrieval, and model call. Keep your resource tagging scheme, because it is how observability costs get attributed.

---

## Hints

Reversed. One at a time.

1. Finding replacements in a plan: `.gnidaer erofeb meht rof hcraes ;noitacifidom morf yltcnitsid tnemecalper skram tuptuo nalP`
2. Module boundaries: `.tinu etarapes a ni oG .yltneuqerfni segnahc taht gnihtynA ?egnahc siht seod netfo woH :ecruoser hcae ksA`
3. Secrets: `.reganam terces eht morf emitnur ta eulav eht daer dna ,ytitnedi daolkrow eht tnarg ,ytpme reniatnoc terces eht eralceD`
4. Drift detection: `.trela ,ytpme ton si ti fI .ylno nalp a nur ,gninrom yreve boj deludehcs A`
5. Policy checks: `.esle gnihtyna erofeb egats taht ni nur seluR .tsefinam elbadaer-enihcam a sa nalp eht tupO`
6. Probes: `.tniopdne ssenevil paehc eht ot etavil dna ,tniopdne ssenidaer eht ot eborp ssenidaer eht tnioP .82 retpahc ni tliub uoy sesnopser htlaeh owt eht esueR`
7. Rolling update with no drops: `.rehto hcae hctam tsum yehtc ;doirep ecarg noitanimret eht dna ,langis eht no ciffart gnitpecca gnippots ,yaled ssenidaer eht :eerht era sreveL`
