---
chapter: 26
title: "Test — Create an AI release manifest"
slug: 26-mlops-and-model-deployment
lesson: docs/lessons/26-mlops-and-model-deployment.md
audio: media/26-mlops-and-model-deployment.mp3
type: test
---

# Chapter 26 test — Create an AI release manifest

A test, not a tutorial. Goal, constraints, starting state, artifacts, rubric. Method is yours. Hints are reversed at the end.

## Goal

Make every element of FieldOps Copilot's AI behavior versioned, pinned in a generated release manifest, gated on evaluation evidence, attributable from any individual triage proposal, and reversible by someone who is not you.

## Starting state

Chapter 25 complete. You have: a versioned triage prompt, a provider-agnostic model interface with a deterministic fake, a read-only lookup tool, a retrieval index over synthetic runbooks, an evaluation suite with a recorded baseline, a latency and cost budget, and an orchestrated asset pipeline with a published-version concept.

## Constraints

1. **The manifest is generated, never hand-written.** It is produced by the build or release process from the actual configuration in effect.
2. **Every element of the configuration surface is pinned.** If something can change behavior without a code change and is not in the manifest, the manifest is incomplete and the gate must fail.
3. **Versions are immutable and identifying.** Once assigned, content never changes. Two runs reporting the same version used the same thing. In-place editing of a versioned artifact is a failure of this test.
4. **Promotion moves the tested artifact.** No rebuilding between environments.
5. **Evidence travels with the release.** Evaluation results are attached to the manifest, not left in a transient log.
6. **The retrieval index is part of the release.** Rolling back the application rolls back the index revision too.
7. **Pin the model version.** Use the provider's specific version identifier, not a floating alias, wherever one is offered. If your provider offers no pinned version, document that as a stated risk with a detection plan.
8. **Synthetic data only**, throughout.
9. **Rollback is written down and executable by another person.** If it requires your memory, it does not count.

## Required artifacts

1. **A configuration surface inventory**: every element that can change behavior without changing code, with its owner and where its version comes from. Expect at least twelve entries.
2. **An environment boundary table**: development, pilot, and production-like, each defined by what data may exist there, who may change it, and what evidence promotion requires.
3. **A generated release manifest** pinning: application build, every prompt version, model identifier and provider and model version string, decoding settings, tool schema version, embedding model and version, retrieval index revision with document count and sources, chunking configuration, retrieval parameters, asset freshness tolerance, evaluation suite version, evaluation results, creator, timestamp, and approver.
4. **A release endpoint or equivalent**: an authorized way to ask the running system which release it is.
5. **A release stamp on every triage proposal**, persisted with the proposal.
6. **A promotion gate** enforcing: deterministic checks pass, quality within tolerance of baseline, cost and latency budget met, and manifest completeness.
7. **A drift detector**: a scheduled run of a small fixed fixture set against the production configuration, with results retained over time so a step change is visible on a day you did not deploy.
8. **A hosting decision matrix** scoring a provider interface against a managed service in the customer's cloud on data boundary, procurement, operational capacity, and economics, with a phased recommendation and a written trigger for moving.
9. **A rollback runbook**, executed at least once, covering application, prompt, index revision, and verification steps.
10. **A monitoring set**: operator acceptance rate, modification pattern, refusal rate, structural validity rate, and cost and latency, each attributable per release with an expected range.

## Required demonstrations

- **D1 — Self-identification.** Ask the running system its release; resolve the identifier to a complete manifest.
- **D2 — Retrospective attribution.** Take a proposal produced earlier; recover its full configuration from the proposal alone.
- **D3 — Gate refuses incomplete manifest.** Add a new prompt without versioning it. Show promotion blocked.
- **D4 — Gate refuses regression.** Degrade quality below the baseline tolerance. Show promotion blocked.
- **D5 — Clean promotion.** Change one prompt, evaluate, promote, and show a new manifest with new version and attached results, with the same artifact in both environments.
- **D6 — Full rollback.** Roll back to the previous manifest. Show the reported release, the observed behavior, and the index revision all reverting. Have someone else drive it from your runbook if possible.
- **D7 — Combination guard.** Attempt to deploy a prompt version and an index revision that have never been evaluated together. Show the gate catching it.
- **D8 — Provider failure.** Simulate an outage. Show a clearly labelled fallback rather than a silent degradation or a hang.
- **D9 — Drift signal.** Alter the fake provider's behavior to simulate a model change. Show the scheduled fixture run surfacing a step change with no deployment on your side.
- **D10 — Portability.** Run the evaluation suite against a second model or provider through the same interface, with no change to the incident service.

## Rubric

| # | Criterion | Does not meet | Meets | Exceeds |
|---|---|---|---|---|
| 1 | Surface completeness | Only the prompt is treated as configuration | Twelve or more elements inventoried with owners | Inventory review is part of the release process, catching new elements automatically |
| 2 | Version immutability | Versioned artifacts are edited in place | Content-addressed or write-once versions; D2 passes | A version can be resolved to exact content by someone who was not present |
| 3 | Manifest generation | Hand-maintained | Generated from effective configuration; D1 passes | Generation fails loudly when it encounters an unpinned element |
| 4 | Evidence binding | Results live in a build log | Attached to the manifest and retrievable months later | Evidence includes suite version and per-case results, not just a pass flag |
| 5 | Gate strength | Advisory or bypassable | D3 and D4 pass | D7 passes: the gate validates the combination, not just the parts |
| 6 | Promotion integrity | Rebuilt per environment | Same artifact promoted; D5 passes | Artifact identity is verified at deploy time, not assumed |
| 7 | Proposal attribution | Proposals carry no release | Release stamped and persisted on every proposal | Stamp is visible to an authorized operator in the interface |
| 8 | Rollback capability | Documented but never run | D6 passes including index revision | Executed by a second person from the runbook, timed, and the time recorded |
| 9 | Index as release member | Index rolls independently of the app | Index revision pinned and reverted together | Previous index revisions retained with a stated retention window |
| 10 | Provider version control | Floating alias in production | Pinned version, or documented risk with detection | D9 passes with a retained history a customer could be shown |
| 11 | Failure behavior | Silent degradation or hang | D8 passes with operator-visible labelling | Fallback path is itself evaluated, not just present |
| 12 | Hosting decision | Preference or unstated | Matrix across all four constraints with phased recommendation | Trigger for the phase change is objective and written into the plan |
| 13 | Portability claim | Asserted | D10 passes | Cost and latency differences between providers are measured and recorded |
| 14 | Monitoring | Service health only | Five AI signals, attributable per release, with expected ranges | A step change in any signal is detectable within one day |
| 15 | Environment discipline | Environments differ only in name | Table defines data, authority, and evidence per environment | A customer security reviewer could read the table unaided and understand the controls |

## Stop conditions

- You are adopting an MLOps platform before you have enumerated your configuration surface.
- Your manifest has a field you fill in manually each time.
- You cannot explain how to get back to last week's behavior.
- Your evaluation suite runs after promotion rather than before.
- The deterministic fake implementation no longer works.

## Carry forward

Chapter 27 makes the promotion gate mechanical: continuous integration runs the checks, the artifact is built once and retained, secrets stay out of untrusted code, and a failing evaluation blocks the merge rather than being a step somebody remembers to run. Your gate definition from this chapter is the specification for that pipeline.

---

## Hints

Reversed. One at a time, after a real attempt.

1. Manifest completeness: `.deggat ton si taht eno yreve rof liaf dna ,yrotnevni eht tsniaga tsefinam detareneg eht erapmoc ,gnissim si tahw rof gnikool fo daetsnI`
2. Immutable versions: `.eman noisrev eht sa tnetnoc eht fo hsah a esU .esuer ro tide ot elbissopmi ti sekam taht yaw a ni stcafitra erotS`
3. Combination guard: `.tsil taht ni si ti sselnu yolped ot esufer dna ,noitanibmoc noisiver-xedni-sulp-noisrev-tpmorp hcae drocer ,snur etius noitaulave eht nehW`
4. Index rollback: `.ssergorp ni srenetsil gnikaerb tuohtiw kcab dna drawrof htob spilf hcihw ,retniop eht evom ylnO .ecalp ni xedni na etirwrevo reveN`
5. Drift detection: `.htiw yalpsid dna erotS .tluser hcae fo mus a peek dna ,serutxif nezorf fo dnah llams a yad yreve nuR`
6. Release stamp: `.egnahc amehcs a si ti ;wor lasoporp eht no nmuloc a si ti :golatac etarapes a ton si pmats esaeler ehT`
7. Hosting matrix: `.hcae rof gnitar a naht lufesu erom si taht dna ,hcihw yfitnedi :rotanimilem na si tniartsnoc hcihw ksA .gnirocs erofeb retlif`
