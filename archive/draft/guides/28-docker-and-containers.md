---
chapter: 28
title: "Test — Containerize the FieldOps service"
slug: 28-docker-and-containers
lesson: docs/lessons/28-docker-and-containers.md
audio: media/28-docker-and-containers.mp3
type: test
---

# Chapter 28 test — Containerize the FieldOps service

A test, not a tutorial. Hints are reversed at the end.

## Goal

Package FieldOps Copilot as an image a customer's platform team would accept: reproducible, minimal, non-root, hardened at runtime, configured from outside, and honest about its own health when a dependency fails.

## Starting state

Chapter 27 complete. You have a pipeline that builds an artifact once, a release manifest, an evaluation gate, a Node.js service, a React workspace, PostgreSQL, an optional cache, and an ingestion job.

## Constraints

1. **Multi-stage build.** The final image contains no compiler, no package manager, and no development dependency.
2. **Non-root by construction.** A dedicated user created in the image; the process runs as it.
3. **Base image pinned by digest**, not by a moving tag.
4. **Dependencies installed strictly from the lock file.** No resolution at build time, and nothing fetched at container start.
5. **Nothing environment-specific in the image.** The same image runs in every environment, differing only by injected configuration.
6. **No secret in any layer, build argument, or image history.** Secrets arrive as mounted files or from a secret manager.
7. **Liveness does not depend on any external dependency.** Readiness may.
8. **The database is not published to the host** in the stack definition you would deploy.
9. **Graceful shutdown.** Termination signals are handled; in-flight requests complete.
10. **Configuration is validated at startup** with a clear error naming any missing required value.
11. **Runtime hardening applied**: dropped capabilities, no privilege escalation, read-only root filesystem with explicit writable mounts, and memory and CPU limits.
12. **The image is built by the pipeline**, not by your laptop, and for the target architecture.

## Required artifacts

1. **A service image definition** meeting every constraint above, with a build-context ignore file that excludes version control metadata, local environment files, test fixtures, and caches.
2. **A frontend boundary decision note**: served by the service or a separate static image, with the reasoning and what would change it. A development server in production fails this test outright.
3. **A local stack definition** running service, PostgreSQL, and the optional cache, with a named volume for database data, a private network, and no database port on the host.
4. **Three health behaviors**: a cheap liveness check, a readiness check reflecting dependencies, and a diagnostic health response naming each dependency's state including read-model freshness.
5. **A runtime hardening specification**: the exact security settings applied, each with a one-line justification.
6. **A scan report before and after** removing at least one unnecessary runtime dependency, with the size and finding-count difference.
7. **A component inventory attached to the image**, continuing the chapter 27 artifact.
8. **A one-command local start procedure** in the readme, verified on a clean machine.
9. **A customer image-policy questionnaire**: the list of questions you would ask a platform team in week one (approved bases, registry, architecture, non-root policy, scan thresholds, required labels, egress restrictions, signing requirements), with your current answers marked as assumptions.

## Required demonstrations

- **D1 — Reproducible build.** Build twice from the same source; show equivalent images.
- **D2 — Minimal runtime.** Show no compiler, package manager, or source tree in the final image.
- **D3 — Non-root.** Show the running process's user is not root.
- **D4 — No secrets in layers.** Search image history and layer contents for secret-like content; show none.
- **D5 — Clean start.** One command on a clean machine brings up the full stack.
- **D6 — Dependency failure is visible.** Stop the database while running. Show: the container stays alive, readiness goes red, the health response names the database as the failing dependency, traffic is withheld, and recovery is automatic when the database returns.
- **D7 — No restart storm.** During D6, show the container was not killed and restarted.
- **D8 — Graceful shutdown.** Send a termination signal during an in-flight request; show it completing and the process exiting cleanly.
- **D9 — Hardened runtime.** Run with read-only root filesystem, dropped capabilities, no privilege escalation, and limits. Show the service still works.
- **D10 — Offline start.** Run the container with networking to the internet disabled. Show it starts, proving nothing is fetched at startup.
- **D11 — Missing configuration.** Start without a required value; show an immediate, clear error naming it.
- **D12 — Size and scan.** Show the before and after of removing an unnecessary runtime dependency.

## Rubric

| # | Criterion | Does not meet | Meets | Exceeds |
|---|---|---|---|---|
| 1 | Build structure | Single stage, or build tooling shipped | Multi-stage; D2 passes | Layer ordering optimized so a source change does not invalidate dependency layers |
| 2 | Reproducibility | Moving base tag or unpinned installs | Digest-pinned base, lock-file installs; D1 passes | Two builds produce byte-identical application layers |
| 3 | Identity | Runs as root | D3 passes with a purpose-created user | A non-numeric-root user is enforced by policy, not convention |
| 4 | Secret hygiene | Secret in a layer, argument, or broad copy | D4 passes; secrets mounted as files | Environment-variable secrets avoided entirely, with the reason documented |
| 5 | Configuration | Environment values baked in | Same image across environments; D11 passes | One image demonstrated running in two environments unchanged |
| 6 | Health semantics | One combined health check | Liveness, readiness, and diagnostic response distinct; D6 passes | Health response includes read-model freshness and release identifier |
| 7 | Failure containment | Dependency loss kills the container | D7 passes; backoff retry with no crash loop | Recovery time measured and stated |
| 8 | Shutdown | Signals ignored | D8 passes | Grace period is tuned to the measured longest normal request |
| 9 | Runtime hardening | Defaults accepted | D9 passes with all five settings justified | Hardening expressed in the deployment definition, not applied by hand |
| 10 | Network exposure | Database published to host | Private network; D5 passes without exposing the database | Only the service port is reachable, verified by attempting the others |
| 11 | Offline readiness | Fetches at startup | D10 passes | Verified against a registry mirror as well as a network block |
| 12 | Size and surface | Full distribution base | D12 shows measurable reduction | Under one hundred megabytes, or a written reason it cannot be |
| 13 | Frontend boundary | Development server, or undecided | Written decision with reasoning | Static assets served with correct caching and compression |
| 14 | Provenance | None | Component inventory attached; images referenced by digest in deployment | Images signed by the pipeline and verified before running |
| 15 | Customer fit | No policy questions asked | Questionnaire produced with assumptions marked | Answers confirmed with a real or role-played platform team, and the image adjusted |

## Stop conditions

- Your liveness check queries the database.
- You are adding a shell to a production image so you can debug it.
- You are building the deployable image on your own machine.
- Your local stack works only because a port is exposed that production would not expose.
- You treat a clean scan report as evidence the workload is secure.

## Carry forward

Chapter 29 chooses where these images run, and chapter 30 declares that placement as reviewable infrastructure. Keep the hardening specification: it becomes part of the deployment manifest rather than a set of flags you remember.

---

## Hints

Reversed. One at a time.

1. Multi-stage minimalism: `.sdliub eht morf tuptuo tliub eht dna seicnedneped noitcudorp eht ylno ypoc neht ,esab wen a htiw niaga trats dna ,gnihtyreve htiw dliub :segats owt etirW`
2. Readiness versus liveness: `.seicnedneped skcehc dnoces eht ;gninnur si ssecorp eht taht rewsna dna gnihton kcehc dluohs tsrif ehT .stniopdne etarapes owt esopxE`
3. No restart storm: `.ssenevil ton ,ssenidaer ot ylno kcehc ycnedneped eht erugifnoC`
4. Secrets: `.ffonaelc a etaerc ot dliub egats-itlum a esu dna ,yrotsih egami eht epsni ,dnif uoy fi ;gnihtyna deppac uoy erehw kcehC`
5. Offline verification: `.strats llits ti taht wohs dna ,dehcatta krowten on htiw reniatnoc eht nuR`
6. Read-only filesystem: `.emulov yraropmet llams a sa ti tnuom dna ,setirw noitacilppa ruoy hcihw ot htap eno eht yfitnedi tsriF`
7. Architecture: `.potpal ruoy no reven dna ,tegrat eht sehctam taht rennur a no egami eht dliub`
