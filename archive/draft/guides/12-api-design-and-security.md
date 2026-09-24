---
chapter: 12
title: "Project test: secure operator access and publish the contract"
roadmap_nodes: ["APIs Design / API Design", "API Security", "Authentication", "GraphQL"]
lesson: docs/lessons/12-api-design-and-security.md
format: test
---

# Chapter 12 project test — Secure operator access and publish the contract

A test. It defines the finished condition and the scoring. It does not choose your identity mechanism, your framework, or your schema language.

Listen to the chapter 12 lesson, then close it. This is the chapter where a shortcut becomes a reportable finding, so read the constraints twice.

## Starting state

- The chapter 11 service: layered, validating, in-memory storage behind an interface, structured logging with correlation identifiers, health and shutdown handled.
- The chapter 10 React workspace pointed at that service.
- The chapter 9 contract document and hand-written incident types.
- The chapter 1 charter, which named an operator and an administrator.

Currently every endpoint is open to anyone who can reach the port. That is the defect this chapter closes.

## Goal

Make the FieldOps service safe to expose: two human roles plus service identities, a pluggable authentication boundary, authorisation enforced on every operation and every object, a published contract that a customer's security reviewer could read, and one defended decision about a graph query layer.

## Constraints

1. **Deny by default.** A newly added endpoint must be unreachable until access is explicitly granted. Demonstrate this by adding a throwaway endpoint and confirming it refuses everyone.
2. **Authorisation lives where every caller passes through it**, not only in route handlers.
3. **Object-level authorisation on every operation, including read and list.** Cross-unit access must be impossible, not merely hidden.
4. **Output is filtered per caller.** No field the caller may not see appears in any response body.
5. **You store no passwords.** Authentication is delegated; the customer's groups map to your roles.
6. **The development authentication path is off by default**, and the service refuses to start if it is enabled outside a development configuration.
7. **Identifiers are not guessable or enumerable.**
8. **Rate limits on write operations**, returning a clear status.
9. **An idempotency key is defined in the contract** for creation, with enforcement deferred to chapter 13 and that deferral written down.
10. **Service identities exist as their own principals**, each scoped to the minimum operations, each individually revocable, with rotation possible without downtime.
11. **The published specification contains no credential, no internal hostname, and no real customer content.**
12. **No permissive cross-origin configuration** in any environment.
13. **Client types are generated from the specification**, replacing the hand-written chapter 9 types.
14. **Errors reveal nothing.** No stack traces, driver messages, versions, or account-existence distinctions.

Out of scope: durable storage and audit tables (chapter 13), caching and counters (chapter 14), threat modelling as a formal artifact (chapter 32).

## Artifacts to produce

| Artifact | Content |
| --- | --- |
| Role and permission matrix | Operations, not screens. Rows for operator, administrator, and each service identity. |
| Authentication boundary | Both implementations behind one component, plus the startup guard that prevents the development path in production. |
| Published specification | Every endpoint, request and response shapes, all error shapes and statuses, the authentication scheme, and the role required per operation. |
| Generated client types | Produced from the specification and compiling against the workspace. |
| Test matrix | Four cases per operation: unauthenticated, wrong role, valid, malformed. |
| Isolation tests | Cross-unit read, list, and update attempts, all refused. |
| GraphQL decision | Either one read-only query with per-object authorisation and a depth limit, or a written refusal — both with reasons. |
| Identity decision record | The production protocol you expect, what you need from the customer to enable it, and the lead time you assume. |
| Security note | Checklist items implemented, items deferred, and the named owner of each deferral. |

## Rubric

Every **Required** row at "meets". At least four **Distinguishing** rows at "meets" to pass.

| # | Criterion | Weight | Fails | Meets | Exceeds |
| --- | --- | --- | --- | --- | --- |
| 1 | Object-level authorisation | Required | Any operator can reach another unit's incident by identifier | Every operation checks the object, including list filtering | An automated test would catch a regression on any single operation |
| 2 | Deny by default | Required | A new endpoint is reachable without explicit grant | Throwaway endpoint refuses everyone | Mechanism makes forgetting structurally difficult |
| 3 | Enforcement placement | Required | Checks only in route handlers | Checks where all callers pass, including future jobs and tools | A second caller path proven to inherit the checks |
| 4 | Output filtering | Required | Full objects returned | Per-caller field filtering | Every field in a sample response accounted for in writing |
| 5 | Development path safety | Required | Development identity usable in a production-shaped configuration | Off by default, startup refuses outside development | Failure message names exactly what is misconfigured |
| 6 | No stored passwords | Required | A local user table with credentials | Delegated authentication, groups mapped to roles | Mapping documented as customer configuration |
| 7 | Specification hygiene | Required | Any secret, internal host, or real content present | Publishable as-is | Reviewed as if by the customer's security team, with notes |
| 8 | Error discretion | Distinguishing | Stack traces, driver text, or account-existence hints | Reference identifier plus human sentence only | Verified by reading every error path's body |
| 9 | Service identities | Distinguishing | One shared credential for all machine callers | One per integration, minimally scoped, revocable | Rotation demonstrated with an overlap window |
| 10 | Contract evolution | Distinguishing | No versioning or deprecation thinking | Versioning strategy and deprecation policy written; version logged per request | Additive-change rules stated, with the repurposing trap called out |
| 11 | Collection design | Distinguishing | Unbounded list | Default and maximum page size, filtering, stable pagination | Cursor pagination justified against a live-queue workload |
| 12 | Type generation | Distinguishing | Hand-maintained types on both sides | Generated from the specification | Drift between service and specification fails a test |
| 13 | GraphQL judgement | Distinguishing | Adopted or dismissed without reasons | Concrete decision with named costs and benefits | Includes whether the customer's team can operate it after handoff |
| 14 | Rate limiting | Distinguishing | None | Write operations limited, clear status | Limit chosen from an assumed workload, not a guess |

## Self-check before you call it done

- As operator A, fetch an incident belonging to unit B. What happens, and is it the same for read, list, and update?
- Add an endpoint and grant it nothing. Can anyone reach it?
- Point your service at a production-shaped configuration with the development identity enabled. Does it start?
- Read one full response body. Justify every field.
- Revoke a credential. How many seconds until the next request fails? Would you say that number out loud to a customer?
- Which of your callers is not a person, and what exactly may it do?
- If you built the graph query, send a deeply nested query. What stops it?
- Search your published specification for anything that looks like a key. Anything?

## Time and depth

The longest chapter of Part III so far. The test matrix is most of the work, and it is the part a reviewer will ask to see, so do not compress it.

## Stuck hints

Read only after a real attempt. Printed upside down on purpose.

˙sɹǝןןɐɔ ǝuᴉɥɔɐɯ ǝɥʇ uǝʇʇoƃɹoɟ ǝʌɐɥ noʎ 'sʍoɹ oʍʇ ʎןuo sᴉ xᴉɹʇɐɯ ǝןoɹ ɹnoʎ ɟI ˙ㄥ
˙ǝɹǝɥ ʇᴉ ǝsnɟǝɹ oʇ uosɐǝɹ ǝʇɐɯᴉʇᴉƃǝן ɐ puɐ ʎƃoןouɥɔǝʇ ǝɥʇ ɟo ʇsoɔ ʇsǝuoɥ ǝɥʇ sᴉ ʇɐɥʇ 'pǝpunoqun sןǝǝɟ ɥdɐɹƃ ɐ uᴉ uoᴉʇɐsᴉɹoɥʇnɐ pןǝᴉɟ-ɹǝd ɟI ˙9
˙ɹoʇɐɹǝuǝƃ ǝɥʇ ʇou 'uᴉɐɯop ǝɥʇ ɹo ʇɔɐɹʇuoɔ ǝɥʇ xᴉℲ ˙pǝǝɹƃɐsᴉp uᴉɐɯop ǝɥʇ puɐ ʇɔɐɹʇuoɔ ǝɥʇ suɐǝɯ ʇᴉ :uoᴉʇɐɯɹoɟuᴉ ןnɟǝsn sᴉ ʇɐɥʇ 'sǝdʎʇ uᴉɐɯop ƃuᴉʇsᴉxǝ ɹnoʎ ɥʇᴉʍ ʇɔᴉןɟuoɔ sǝdʎʇ pǝʇɐɹǝuǝƃ ɟI ˙ϛ
˙pǝǝu ןןᴉʍ noʎ ʎɹǝnb ǝɥʇ ǝʇou puɐ ʍou ɹoɟ ɹǝʎɐן uoᴉʇɐɔᴉןddɐ ǝɥʇ uᴉ ɹǝʇןᴉℲ ˙ƃuᴉʞןɐʇ ƐƖ ɹǝʇdɐɥɔ sᴉ ʇɐɥʇ 'ʇǝʎ ǝʌɐɥ ʇou op noʎ uᴉoɾ ɐ ʇnoɥʇᴉʍ ʇᴉun ʎq ɹǝʇןᴉɟ ʇouuɐɔ ʇuᴉodpuǝ ʇsᴉן ɹnoʎ ɟI ˙ㄣ
˙pǝdɐɥs-uoᴉʇɔnpoɹd ƃuᴉɥʇʎuɐ ɥʇᴉʍ pǝuᴉqɯoɔ sᴉ ʇᴉ uǝɥʍ ʇɹɐʇs oʇ ǝsnɟǝɹ puɐ ƃɐןɟ ʇuǝɯdoןǝʌǝp ʇᴉɔᴉןdxǝ uɐ ǝɹᴉnbǝɹ :ʇןnɐɟǝp ǝɥʇ ʇɹǝʌuᴉ 'suoᴉʇɐɹnƃᴉɟuoɔ ɹǝɥʇo oʇuᴉ ƃuᴉʞɐǝן sdǝǝʞ ʎʇᴉʇuǝpᴉ ʇuǝɯdoןǝʌǝp ǝɥʇ ɟI ˙Ɛ
˙suǝʞoʇ pǝdoɔs oʇ uɐǝן sןooʇ pǝʌᴉן-ʇɹoɥs puɐ sǝuᴉɥɔɐɯ ؛suoᴉssǝs oʇ uɐǝן ʇuǝɯǝɹᴉnbǝɹ uoᴉʇɐɔoʌǝɹ ɐ ɥʇᴉʍ sɹǝsʍoɹ၁2 ˙sᴉ ɹǝןןɐɔ ǝɥʇ oɥʍ ʞsɐ 'suǝʞoʇ puɐ suoᴉssǝs uǝǝʍʇǝq ǝpᴉɔǝp ʇouuɐɔ noʎ ɟI ˙ᄅ
˙pǝddᴉʞs ǝq uɐɔ ɹǝɥʇᴉǝu puɐ ɹǝɥʇǝƃoʇ uǝddɐɥ uoᴉssᴉɯɹǝd puɐ ƃuᴉpɐoן os 'ʇɔǝɾqo ǝɥʇ spɐoן ʇɐɥʇ ǝsɐɔ ǝsn ǝɥʇ oʇuᴉ ʞɔǝɥɔ ǝɥʇ ǝʌoɯ oʇ ןɐuƃᴉs ɐ sᴉ ʇɐɥʇ 'ǝʌᴉʇᴉʇǝdǝɹ ןǝǝɟ sʞɔǝɥɔ ןǝʌǝן-ʇɔǝɾqo ɟI ˙Ɩ
