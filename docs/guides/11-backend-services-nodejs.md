---
chapter: 11
title: "Project test: the FieldOps API"
roadmap_nodes: ["Backend Skills", "Backend", "Node.js"]
lesson: docs/lessons/11-backend-services-nodejs.md
format: test
---

# Chapter 11 project test — The FieldOps API

A test. It states the finished condition and how it is scored. It does not give you a framework, a folder layout, a schema, or handler code.

Listen to the chapter 11 lesson, then close it.

## Starting state

- The chapter 10 React workspace: two routes, rebuilt form, service seam, mock behind it, simulated-service marker on screen.
- The chapter 9 contract document, and the five-state request model in the interface.
- The chapter 3 Python priority rule and its test table.
- The chapter 6 architecture split, including the business-unit routing decision record.

The service itself starts from an empty directory.

## Goal

Build the authoritative FieldOps service: create, list, and get incidents, with server-side validation, one implementation of the priority policy, structured request logging, a health contract, and graceful shutdown — then point the workspace at it and remove only the mock path it replaces.

Records live in memory this chapter. Losing them on restart is expected and is part of the test.

## Constraints

1. **Four layers with dependencies pointing inward.** The domain imports neither the web framework nor storage. Demonstrate this, do not assert it.
2. **Every incoming record is validated on the server** against a schema, with field-level rejection detail in the shape the chapter 9 interface already renders.
3. **The priority policy exists exactly once**, in the domain, ported from chapter 3 along with its tests. Any browser-side calculation is removed or visibly labelled a preview.
4. **The business-unit rule is configuration**, not a special case inside the rule.
5. **Storage is behind an interface.** Nothing above it knows the implementation is in memory.
6. **Configuration comes from the environment.** No secret in code, in the repository, or in any log line — including startup.
7. **One structured log line per request**, with a correlation identifier that is generated when absent and returned to the caller. No incident description in logs.
8. **Liveness and readiness are separate**, and liveness does not depend on any dependency.
9. **Graceful shutdown** on a termination signal, with a bounded grace period and no dropped in-flight request.
10. **A request size limit**, and a deadline on every outbound call you make.
11. **No permissive cross-origin configuration**, in any environment.
12. **The mock survives but is unambiguous.** The simulated marker appears only when the mock is in use.
13. **Status codes are meaningful.** No success response carrying an error inside it.
14. **Minimal dependencies**, each justified in one sentence.

Out of scope: authentication and authorisation (chapter 12), persistence and transactions (chapter 13), caching (chapter 14), containers (chapter 28).

## Artifacts to produce

| Artifact | Content |
| --- | --- |
| The service | Typed, layered, in-memory storage behind an interface. |
| Layer map | What each layer may and may not import, and how you enforce it. |
| Contract document | Updated from chapter 9 to what the service actually does: shapes, statuses, error bodies. |
| Ported domain rule | With its test table, and a note on any discrepancy found between your earlier implementations. |
| Integration tests | Valid creation, invalid rejection with no record created, list, and not-found. |
| Dependency inventory | Each dependency, one sentence on why it is there, version pinned. |
| Persistence brief | The restart-loses-data behaviour in customer language, as the brief for chapter 13. |
| Platform questions | The questions you would ask a customer platform team before running this process near their systems. |

## Rubric

Every **Required** row at "meets". At least three **Distinguishing** rows at "meets" to pass.

| # | Criterion | Weight | Fails | Meets | Exceeds |
| --- | --- | --- | --- | --- | --- |
| 1 | Single policy owner | Required | Priority computed in more than one place, or accepted from the client | Exactly one implementation, in the domain, exercised by both paths | Ported tests include the ties and invalid inputs from chapter 2 |
| 2 | Server-side validation | Required | A direct malformed request creates a record | All invalid cases rejected with field-level detail; nothing created | Rejection shape verified against the chapter 9 renderer without changes |
| 3 | Dependency direction | Required | Domain imports the framework or the store | Domain is pure and testable with no infrastructure | Direction enforced mechanically, not by convention |
| 4 | Storage boundary | Required | Any handler touches the in-memory structure | Interface only, above and below | Swapping the implementation would require no change above the interface |
| 5 | Error responses | Required | Stack traces, driver messages, or internal paths in a response | Human sentence plus a reference identifier; detail in logs | Reference identifier matches the correlation identifier the operator can quote |
| 6 | Process lifecycle | Required | Termination drops in-flight requests, or liveness depends on a dependency | Separate liveness and readiness; graceful shutdown within a bounded period | Unhandled failure policy stated and implemented |
| 7 | Logging hygiene | Required | Unstructured output, or operator content in logs | Structured line per request, correlation identifier, no sensitive content | Logs plausibly acceptable to a customer platform team as-is |
| 8 | Interface substitution | Distinguishing | Components changed to talk to the real service | Only the seam's implementation changed | Mock retained for offline work and fault injection, clearly signalled |
| 9 | Protocol use | Distinguishing | One method and one status for everything | Methods and statuses carry meaning; reads are safe | Creation response tells the client where the record lives |
| 10 | Concurrency awareness | Distinguishing | Read-modify-write across a suspension point | Hazard identified and avoided or contained | Written note predicting where chapters 13 and 14 will need a transaction |
| 11 | Configuration hygiene | Distinguishing | Values hard-coded, or an example file containing real values | Environment-sourced, example file inert | Startup logs configuration without revealing a single sensitive value |
| 12 | Evidence and handoff | Distinguishing | No inventory, no persistence brief | Both present and specific | Platform questions show awareness of approval, proxy, certificate, and logging constraints |

## Self-check before you call it done

- Send a request with a priority field you invented. What does the service do with it?
- Restart the service with three incidents in it. Write one sentence a customer would say about what just happened.
- Which file would you edit if the customer redefined critical tomorrow? Is the answer exactly one?
- Kill the process mid-request. Did the caller get an answer?
- Read your last twenty log lines aloud. Would you email them to the customer's platform team?
- If the database in chapter 13 is slower than you expect, which of your endpoints has no deadline?
- Where, precisely, will chapter 12 add the authorisation check, and how many places is that?

## Time and depth

Longer than the frontend chapters, because it is a new process with a lifecycle. If you are designing a database schema, stop — that is chapter 13.

## Stuck hints

Read only after a real attempt. Printed upside down on purpose.

˙ɹǝɟɟᴉp sʞɹoʍǝɯɐɹℲ ˙ʇᴉ sǝʌᴉǝɔǝɹ ƃuᴉןpuɐɥ ɹoɹɹǝ ɹnoʎ ɹǝɥʇǝɥʍ ǝǝs puɐ ɹǝןpuɐɥ snouoɹɥɔuʎsɐ uɐ ǝpᴉsuᴉ ʎןǝʇɐɹǝqᴉןǝp ɹoɹɹǝ uɐ ʍoɹɥʇ 'ǝsuodsǝɹ ou ɥʇᴉʍ sƃuɐɥ ʇsǝnbǝɹ ɐ ɟI ˙ㄥ
˙ɔᴉƃoן ƃuᴉɥɔuɐɹq sɐ uɐɥʇ ɹǝɥʇɐɹ sʇɥƃᴉǝʍ oʇ sʇnduᴉ ɟo ǝןqɐʇ ɐ sɐ ʇᴉ ǝqᴉɹɔsǝp 'uoᴉʇɐɹnƃᴉɟuoɔ sɐ ǝןnɹ ʇᴉun-ssǝuᴉsnq ǝɥʇ ssǝɹdxǝ ʇouuɐɔ noʎ ɟI ˙9
˙ʞɔǝɥɔ ƃuoɹʍ ǝɥʇ uᴉ ʎɔuǝpuǝdǝp ɐ ʇnd noʎ 'dᴉןq ʎɔuǝpuǝdǝp ɐ ƃuᴉɹnp sʇɹɐʇsǝɹ sǝsnɐɔ ʞɔǝɥɔ ɥʇןɐǝɥ ɐ ɟI ˙ϛ
˙ǝuᴉןpɐǝp ɐ ɥʇᴉʍ poᴉɹǝd ǝɔɐɹƃ ǝɥʇ ǝɔɹoɟuǝ puɐ 'pǝuǝdo noʎ ʇɐɥʍ ǝsoןↃ ˙uǝdo ɹǝɯᴉʇ ɐ ɹo uoᴉʇɔǝuuoɔ ɐ ƃuᴉpןoɥ ןןᴉʇs sᴉ ƃuᴉɥʇǝɯos 'sƃuɐɥ uʍopʇnɥs ןnɟǝɔɐɹƃ ɟI ˙ㄣ
˙sᴉ ʎʇᴉɹoᴉɹd sʇᴉ ʇɐɥʍ sʞsɐ ǝןnɹ ǝɥʇ 'pǝɯɹoɟ ןןǝʍ sᴉ pɹoɔǝɹ ǝɥʇ ɹǝɥʇǝɥʍ sʞsɐ uoᴉʇɐpᴉןɐʌ :suoᴉʇsǝnb ǝɥʇ ǝʇɐɹɐdǝs 'pǝʇɐɔᴉןdnp ןǝǝɟ ǝןnɹ uᴉɐɯop ǝɥʇ puɐ uoᴉʇɐpᴉןɐʌ ɟI ˙Ɛ
˙sǝɹnʇɐuƃᴉs ,suoᴉʇɐʇuǝɯǝןdɯᴉ oʍʇ ǝɥʇ ǝɹɐdɯoↃ ˙sןᴉɐʇǝp ʇɹodsuɐɹʇ ƃuᴉʞɐǝן sɐʍ ɯɐǝs ǝɥʇ 'ǝɔᴉʌɹǝs ןɐǝɹ ǝɥʇ oʇ ʞןɐʇ oʇ sǝƃuɐɥɔ pǝpǝǝu ǝɔɐɟɹǝʇuᴉ ǝɥʇ ɟI ˙ᄅ
˙sɹɐǝddɐsᴉp ʎɔuǝpuǝdǝp ǝɥʇ puɐ pɐǝʇsuᴉ sǝnןɐʌ uᴉɐɯop uᴉɐןd ssɐԀ ˙pɹɐʍuᴉ sʇɔǝɾqo ʇsǝnbǝɹ ƃuᴉssɐd ǝɹɐ noʎ 'sǝdʎʇ ʞɹoʍǝɯɐɹɟ ƃuᴉpǝǝu sdǝǝʞ uᴉɐɯop ɹnoʎ ɟI ˙Ɩ
