---
chapter: 27
title: "Test — Automate the safe build"
slug: 27-devops-cicd-and-github-actions
lesson: docs/lessons/27-devops-cicd-and-github-actions.md
audio: media/27-devops-cicd-and-github-actions.mp3
type: test
---

# Chapter 27 test — Automate the safe build

A test, not a tutorial. Hints are reversed at the end.

## Goal

Move every verification and release step of FieldOps Copilot out of your memory and into an automated pipeline, such that a failing safety or regression check makes promotion impossible rather than inadvisable, and such that a stranger could deploy and roll back from the pipeline alone.

## Starting state

Chapter 26 complete: a generated release manifest, a promotion gate definition, environment boundaries, a rollback runbook, an evaluation suite with a deterministic fake model implementation, and a recorded baseline.

## Constraints

1. **Build once.** One artifact identifier flows from build through every later stage. No stage rebuilds.
2. **Tiered verification.** Tier one runs on every proposed change with no secrets. Tier two runs credentialed after merge or on schedule. Tier three is the promotion gate.
3. **No secret reaches untrusted code.** A proposed change must not be able to read, print, or exfiltrate any credential.
4. **Short-lived credentials where the platform supports them.** Stored long-lived cloud keys require a written justification if you keep any.
5. **Least privilege for the pipeline identity.** Deploy only. Enumerate what it cannot do.
6. **Properties, not exact outputs.** AI assertions check structure, prohibitions, citations, and aggregate tolerance. No exact-string matching against model output.
7. **Tier one completes in under six minutes** on a cold cache, and under four on a warm one. Report the measured figures.
8. **Reproducible locally.** One documented command on a fresh checkout produces the same tier-one result as the pipeline.
9. **Third-party pipeline steps pinned to immutable revisions.** No moving version tags.
10. **Dependencies installed from a lock file** in a mode that refuses unpinned resolution.
11. **Required checks enforced at the platform level.** A red check must block the merge, not merely display.
12. **Migrations are a distinct step** and are forward-compatible with the previously deployed version.
13. **Synthetic data only** in every automated context.

## Required artifacts

1. **A pipeline stage specification**: each stage, its trigger, its inputs, whether it has secrets, its expected duration, and what its failure means.
2. **The tier-one workflow**: dependency install from lock file, lint, type check, unit tests, integration tests against real PostgreSQL, contract tests, authorization tests, pipeline data-quality tests, evaluation suite against the fake, and manifest completeness check.
3. **The artifact build and retention step**, producing a tagged artifact plus retained test evidence and the generated manifest.
4. **The tier-two workflow**: credentialed, synthetic-fixture evaluation measuring quality, latency, and cost against baseline, with outputs retained as an artifact on failure.
5. **The tier-three promotion**: environment protection with required approval, gate evaluation, and deployment of the retained artifact by identity.
6. **A rollback job**: the same deployment path pointed at an earlier artifact identifier.
7. **A migration step** with forward-compatibility evidence: a demonstration that the previous release runs correctly against the new schema.
8. **A component inventory** per artifact: dependency versions, base image identity, and source revision.
9. **A dependency vulnerability scan** with a written severity policy stating what blocks and what files a ticket.
10. **A local verification command** documented in the readme.
11. **A runner decision note**: hosted or self-hosted for the target customer environment, with the network and trust implications, and the rule that untrusted changes never run on a self-hosted runner.

## Required demonstrations

- **D1 — Local parity.** Fresh checkout, one command, same result as the pipeline. Show both.
- **D2 — Failing test blocks merge.** A proposed change with a broken unit test cannot merge.
- **D3 — Safety regression caught free.** A change that permits a write action is caught by the evaluation suite against the fake, with no credentials in the job.
- **D4 — Secret exfiltration fails.** A proposed change that attempts to print credentials produces nothing, because none are present.
- **D5 — Artifact identity.** Show the same artifact identifier at build, tier two, and deploy, and prove the deployed bytes match the built bytes.
- **D6 — Gate refuses promotion.** Attempt promotion with missing or failing evaluation evidence. Show it blocked by the environment rule, not by convention.
- **D7 — Rollback through the pipeline.** Deploy a previous artifact identifier using the same job. Time it.
- **D8 — Migration compatibility.** Apply a migration, then run the previous release against the migrated schema successfully.
- **D9 — Pipeline speed.** Report tier-one duration cold and warm against your stated target.
- **D10 — Supply chain answer.** Given a named vulnerable package, determine from your component inventory whether a given artifact is affected, in under five minutes.

## Rubric

| # | Criterion | Does not meet | Meets | Exceeds |
|---|---|---|---|---|
| 1 | Build-once discipline | Any stage rebuilds | D5 passes | Artifact integrity verified by digest at deploy time |
| 2 | Tiering | One monolithic pipeline | Three tiers by cost and trust; D3 passes | Tier boundaries justified with measured cost per run |
| 3 | Secret isolation | Secrets present on proposed changes | D4 passes | Untrusted and trusted workflows are structurally separate, not conditionally guarded |
| 4 | Credential lifetime | Stored long-lived keys | Short-lived credentials, or written justification per exception | Zero stored deployment credentials |
| 5 | Pipeline privilege | Broad or unexamined | Deploy-only, with an enumerated list of denied capabilities | Privilege verified by attempting a denied action and showing it fail |
| 6 | Gate enforcement | Advisory checks | Required checks block merge; D2 and D6 pass | Bypass attempts are logged and visible |
| 7 | AI assertion stability | Exact-output matching | Property assertions with tolerance | Flake rate measured over repeated runs and reported |
| 8 | Speed | Over ten minutes | D9 meets stated target | Slowest stages identified with a written plan |
| 9 | Local parity | Works only in CI, or only locally | D1 passes | Divergence causes are documented and prevented, not just fixed |
| 10 | Migration safety | Migrate on startup | Distinct step; D8 passes | Rollback rehearsal includes a release that migrated |
| 11 | Rollback | Manual or undocumented | D7 passes through the pipeline | Timed, and the time is recorded in the runbook |
| 12 | Supply chain | Moving tags, no inventory | Pinned steps, lock-file installs, inventory produced; D10 passes | Scan policy is enforced and has survived at least one real advisory |
| 13 | Test distribution | Mostly slow end-to-end tests | Many fast, fewer integration, minimal end-to-end, with authorization as its own category | Distribution is measured and reported per run |
| 14 | Configuration handling | Environment values baked into the artifact | Identical artifact across environments; config injected | A single artifact is demonstrated running in two environments |
| 15 | Runner fit | Not considered | Written decision with trust and network implications | Self-hosted runner treated as untrusted-input-free and ephemeral by construction |

## Stop conditions

- You are adding a re-run button to get past a flaky required check.
- Your evaluation suite calls a paid provider on every proposed change.
- You cannot state which stages have secrets and which do not.
- Deploying by hand is faster than deploying through the pipeline.
- Your workflow files are not reviewed as carefully as your authorization code.

## Carry forward

Chapter 28 gives the pipeline something better to build: a reproducible, non-root, health-checked container image. Your artifact concept becomes an image identity, and your local verification becomes a locally runnable stack.

---

## Hints

Reversed. One at a time.

1. Secret isolation: `.hcnarb detsurt a morf sregrirt taht wolfkrow etarapes a ni ,egrem retfa ylno sterces htiw sboj nuR .dnammoc detimbus eht no snoitidnoc no yler ton oD`
2. Artifact identity: `.eno tliub eht si tseg ehd dessapd eht taht evorp dna ,yolped ta niaga ti etupmoC .tsefinam eht ni ti drocer dna dliub ta tcafitra eht fo tsegid a etupmoC`
3. Fast tier one: `.ytiralap yb nur ,ecnedneped on evah snoitazirohtua dna ,stcartnoc ,sepyt ,tniL .oen ton ,sboj lellarap ruof era stset dna kcehc epyt ,tniL`
4. Forward-compatible migrations: `.retal esaeler a ni nmuloc dlo eht porD .revoyaw sredaer evom neht ,htob ot etirw ,nmuloc wen a ddA .esaeler eno ni nmuloc a emaner reveN`
5. Property assertions: `.gnirts tcaxe na ton ,setacidep ruof esoht tressA .egnar ni yrogetac dna ,noitca etirw on ,tneserp noitatic ,amehcs eht stif tuptuo eht rehtehw ksA`
6. Local parity: `.enihcam ruoy no krow ot sneppah tahw ton ,senifed elifekam eht tahw snur enilepip ehT .htob yb dellac dnammoc eno enifeD`
7. Supply chain inventory: `.tsefinam esaeler eht ot ti hcatta dna ,tcafitra eht sa emit emas eht ta yrotnevni eht etareneG`
