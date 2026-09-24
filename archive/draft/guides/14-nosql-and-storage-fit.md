---
chapter: 14
title: "Project test: add an expiring triage cache — and defend your storage"
roadmap_nodes: ["NoSQL Databases"]
lesson: docs/lessons/14-nosql-and-storage-fit.md
format: test
---

# Chapter 14 project test — Add an expiring triage cache, and defend your storage

A test. The code is small; the written decision is the deliverable. It does not tell you which store to use or how to structure your keys.

Listen to the chapter 14 lesson, then close it.

## Starting state

- The chapter 13 PostgreSQL system of record: constraints, append-only history and audit, enforced idempotency, one evidence-backed index, separated database privileges.
- The chapter 12 authorisation model, including object-level and business-unit scoping.
- The chapter 11 storage interface, with everything above it unaware of the implementation.
- Whatever rate limiting you built in chapter 12, possibly in process memory.

## Goal

Add exactly one expiring cache for one derived, non-authoritative value — and produce a storage decision record that justifies every datastore this system has, and every one it does not.

Removing the cache after measuring it is a passing outcome if the record says why.

## Constraints

1. **One cached thing only.** Either the dashboard read-model summary or the shared rate-limit counter. Note the other; do not build both.
2. **The cached value is derived and recomputable.** Deleting the entire cache must not lose an incident, a status change, or an audit event.
3. **PostgreSQL remains the source of truth for every fact.**
4. **The cache sits behind an interface**, with a no-op implementation so tests and local development run without it.
5. **Cache keys include every dimension that changes the answer, including the authorisation scope.** A cross-scope leak fails this test outright.
6. **Every entry has an expiry**, chosen from the product and defensible to a customer.
7. **Explicit invalidation happens in the same operation that changes the underlying data**, with expiry as the backstop.
8. **The person who just made a change sees their change immediately.**
9. **Behaviour when the cache is unavailable is decided, implemented, and written down** — including, for the rate limiter, an explicit position on failing open versus failing closed.
10. **No free-text incident content is cached** without a written classification decision.
11. **Cached shapes are versioned or namespaced** so a deployment cannot misread an older shape.
12. **The store has an eviction policy and a maximum**, and you know what it does when full.
13. **Benefit is measured** before and after, at realistic volume.
14. **No second datastore beyond this one.** No document store, no search cluster, no queue, no graph.

Out of scope: vector storage and retrieval (chapter 20), pipelines and dead-letter handling (chapter 24), formal data classification (chapter 32).

## Artifacts to produce

| Artifact | Content |
| --- | --- |
| Cache adapter | Behind an interface, with a no-op implementation. |
| Cache specification | Key structure, expiry, invalidation triggers, and unavailable-behaviour, per cached thing. |
| Measurement pair | The motivating operation before and after, at realistic volume, with numbers. |
| Scope-isolation test | Proves one scope's cached value is never served to another. |
| Resilience test | Cache deleted and cache stopped: no data loss, degradation as specified. |
| Storage decision record | See below — this is the main deliverable. |

The storage decision record must contain: for each datastore you now run, why it exists and what it costs to operate (deployment, patching, availability, backup and restore, monitoring, security review, credentials and rotation, on-call knowledge, money); for each family you did not adopt — document, wide-column, graph, search — one honest paragraph on what it would give you, what would have to become true to justify it, and which capability of your existing store makes it unnecessary; the queue assessment, including where in Parts IV and V one becomes justified; and a note on chapter 20's genuine need for similarity search, naming the two options you will compare.

## Rubric

Every **Required** row at "meets". At least three **Distinguishing** rows at "meets" to pass.

| # | Criterion | Weight | Fails | Meets | Exceeds |
| --- | --- | --- | --- | --- | --- |
| 1 | Nothing authoritative cached | Required | Deleting the cache loses or corrupts any fact | Full deletion costs latency only | Proven by a test that wipes the cache mid-workload |
| 2 | Scope in the key | Required | One scope's value reachable by another | Keys include scope; isolation test passes | Test would fail loudly if a future key omitted scope |
| 3 | Expiry and invalidation | Required | Expiry only, or invalidation only | Both, with invalidation in the same operation as the change | Staleness window stated in the interface where operators see it |
| 4 | Read-your-writes | Required | Operator does not see their own change | Authoritative value served to the actor | Behaviour verified for both cached candidates conceptually |
| 5 | Unavailable behaviour | Required | Unhandled failure reaches the operator | Decided, implemented, documented | Rate-limiter position argued with the trade named honestly |
| 6 | Interface boundary | Required | Cache calls scattered through the application | One adapter behind an interface; no-op implementation works | Test suite runs identically with and without the cache |
| 7 | Measured benefit | Distinguishing | Assumed improvement | Before-and-after numbers at realistic volume | Willing conclusion to remove it, recorded |
| 8 | Operational bounds | Distinguishing | No eviction policy or maximum | Both set; full-store behaviour known | Full-store behaviour tested, not assumed |
| 9 | Shape versioning | Distinguishing | Old shapes misread after a deploy | Versioned or namespaced keys | Deploy simulated: miss and refill, never misread |
| 10 | Content discipline | Distinguishing | Free-text incident content cached without thought | Identifiers and aggregates only, or a written classification | Retention consequence of the copy acknowledged |
| 11 | Decision record quality | Distinguishing | A paragraph saying a cache is useful | Every store justified, every non-adopted family addressed | Costs expressed in terms a customer platform team would recognise |
| 12 | Restraint | Distinguishing | A second store added opportunistically | Exactly one accelerator | Something you were tempted by, named, with the trigger that would change your mind |

## Self-check before you call it done

- Delete every key in the cache during a live workload. What was lost?
- Stop the cache entirely. What does an operator experience on each affected path?
- Cache a summary as unit A, then request it as unit B. Whose numbers come back?
- How stale can the number on the dashboard be, and would you say that figure to the customer's operations manager?
- If the counter store is down, are you rate limited or not? Which did you choose, and why is it defensible?
- What is in your cache that a data deletion request would have to reach?
- Which datastore in this system would you remove today if the measurement said so?
- Which one will chapter 20 legitimately require, and what will you compare it against?

## Time and depth

Small implementation, real writing. If the code took longer than the decision record, you inverted the chapter.

## Stuck hints

Read only after a real attempt. Printed upside down on purpose.

˙pǝppɐ noʎ ɹǝʌǝʇɐɥʍ ʎq ƃuᴉuɹoɯ ǝɥʇ uᴉ ǝǝɹɥʇ ʇɐ pǝƃɐd ǝq ןןᴉʍ oɥʍ ɹǝǝuᴉƃuǝ ɯɹoɟʇɐןd ǝɥʇ oʇ ʇᴉ ƃuᴉpuɐɥ ǝuᴉƃɐɯᴉ 'ʞɹoʍʎsnq ǝʞᴉן sןǝǝɟ pɹoɔǝɹ uoᴉsᴉɔǝp ǝɥʇ ɟI ˙ㄥ
˙ssɐd ɐ sᴉ ʇɐɥ⊥ ˙uoᴉʇɐuɐןdxǝ uǝʇʇᴉɹʍ ɐ puɐ ןɐʌoɯǝɹ ɐ sᴉ ǝןqɐɹǝʌᴉןǝp ʇɔǝɹɹoɔ ǝɥʇ 'ʇᴉɟǝuǝq ou sʍoɥs ʇuǝɯǝɹnsɐǝɯ ǝɥʇ ɟI ˙9
˙ƃuᴉɥʇʎuɐ ƃuᴉppɐ ǝɹoɟǝq suɯnןoɔ pǝɹnʇɔnɹʇs-ᴉɯǝs ɥʇᴉʍ sǝop ʎpɐǝɹןɐ ǝɹoʇs ןɐuoᴉʇɐןǝɹ ɹnoʎ ʇɐɥʍ ʞɔǝɥɔ 'spɐoןʎɐd ɹɐןnƃǝɹɹᴉ ɹoɟ ǝɹoʇs ʇuǝɯnɔop ɐ ʎq pǝʇdɯǝʇ ǝɹɐ noʎ ɟI ˙ϛ
˙sǝʇɐsuǝdɯoɔ ʇɹǝןɐ ʇɐɥʍ ʎɐs puɐ 'ǝuo ǝsooɥɔ 'suoᴉʇdo ɥʇoq ǝɯɐN ˙ǝpɐɹʇ ɐ sᴉ ʎןǝuᴉnuǝƃ ʇᴉ ǝsnɐɔǝq sᴉ ʇɐɥʇ 'ƃuᴉʇᴉɯᴉן ǝʇɐɹ ɹoɟ ǝןqɐɹǝʍsuɐun sןǝǝɟ uoᴉʇsǝnb ɹnoᴉʌɐɥǝq-ǝןqɐןᴉɐʌɐun ǝɥʇ ɟI ˙ㄣ
˙uosɐǝɹ sᴉɥʇ ʎןʇɔɐxǝ ɹoɟ ʇuǝɯǝɹɔuᴉ ɔᴉɯoʇɐ uɐ ɹǝɟɟo sǝɹoʇs ǝsǝɥ⊥ ˙ƃuᴉʇᴉɹʍ uǝɥʇ puɐ ƃuᴉpɐǝɹ ǝɹɐ noʎ 'pɐoן ɹǝpun ƃuoɹʍ ɹǝʌǝ sᴉ ɹǝʇunoɔ ɐ ɟI ˙Ɛ
˙sʇɔǝɟɟɐ ʎןןɐnʇɔɐ ǝƃuɐɥɔ ǝɥʇ ǝdoɔs ǝɥʇ oʇ ʎǝʞ ǝɥʇ ʍoɹɹɐN ˙ǝsɹɐoɔ ooʇ sᴉ ʎǝʞ ɹnoʎ ןɐuƃᴉs ɐ sᴉ ʇɐɥʇ 'ʇɥƃᴉɹ ʇǝƃ oʇ ǝןqᴉssodɯᴉ sןǝǝɟ uoᴉʇɐpᴉןɐʌuᴉ ɟI ˙ᄅ
˙uǝʇɟo ʇsoɯ pǝʇsǝnbǝɹ sᴉ ʇɐɥʇ ǝuo ǝɥʇ ʞɔᴉd 'sǝᴉɟᴉןɐnb ǝuo uɐɥʇ ǝɹoɯ ɟI ˙ssoן ou ɥʇᴉʍ ǝsɐqɐʇɐp ǝɥʇ ɯoɹɟ ǝןqɐʇndɯoɔǝɹ sᴉ ǝuo ɥɔᴉɥʍ ʞsɐ 'ǝɥɔɐɔ oʇ ǝnןɐʌ ɥɔᴉɥʍ ǝpᴉɔǝp ʇouuɐɔ noʎ ɟI ˙Ɩ
