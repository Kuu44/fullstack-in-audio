---
chapter: 13
title: "Project test: persist incidents and audit events"
roadmap_nodes: ["SQL", "PostgreSQL"]
lesson: docs/lessons/13-sql-and-postgresql.md
format: test
---

# Chapter 13 project test — Persist incidents and audit events

A test. It states the finished condition and the scoring. It does not give you a schema, a migration, or a query.

Listen to the chapter 13 lesson, then close it.

## Starting state

- The chapter 12 secured service: roles, delegated authentication, object-level authorisation, published contract, idempotency key defined but not enforced.
- The chapter 11 storage interface, with an in-memory implementation behind it.
- The chapter 3 priority rule, now owned by the domain layer.
- An empty local PostgreSQL instance. Use a container if that is easiest; do not substitute a different engine.

## Goal

Make PostgreSQL the system of record. Incidents survive restarts, history is append-only, audit events cannot be rewritten by the service, duplicate submissions cannot create duplicate records, and one index decision is supported by two query plans.

## Constraints

1. **Model four things**: incidents, operators, status changes, audit events. The last two are append-only.
2. **Every fact that must be true is enforced by a constraint.** Not by your service alone. This is tested by issuing bad data directly to the database.
3. **Timestamps are instants with a time zone**, from a source you control, and recorded time is distinguished from occurrence time.
4. **Derived values record the policy version that produced them.**
5. **Severity and impact are represented in a way that reflects who owns the vocabulary**, with the choice justified against the chapter 6 split.
6. **Migrations are hand-written and ordered**, never edited after application, with any destructive change expressed as expand and contract.
7. **Multi-step operations are transactional and short.** No transaction spans an outbound call or a user's thinking time.
8. **Idempotency is enforced by a unique constraint**, resolved by returning the existing record. Check-then-insert fails this row outright.
9. **Concurrent status changes cannot silently lose one.** Choose optimistic versioning or explicit locking and justify it.
10. **The application's database role cannot alter the schema and cannot update or delete audit rows.** Migrations run as a different role.
11. **A statement timeout and a bounded connection pool** are configured, with the pool size reasoned about rather than guessed.
12. **Nothing above the chapter 11 storage interface changed.** If a route handler or a component needed edits, the boundary leaked.
13. **Chapter 12 authorisation still holds**, including object-level checks, now expressed in queries rather than in-memory filtering.
14. **Performance claims require plans.** No index without a before-and-after plan at realistic volume.

Out of scope: caching (chapter 14), analytical pipelines and read models (chapter 24), backups as an implemented capability (chapter 29) — a statement of intent is enough.

## Artifacts to produce

| Artifact | Content |
| --- | --- |
| Schema | With a one-line assertion per constraint: what does this make impossible? |
| Migrations | Hand-written, ordered, reviewable, with a stated rollback approach. |
| Transactional operations | Create, list, get, and status change. |
| Idempotency evidence | Two concurrent identical submissions, one resulting row, identical responses. |
| Concurrency evidence | Two simultaneous status changes; one wins, one is told, audit trail correct. |
| Plan pair | Before and after your index, at realistic volume, with timings and row estimates. |
| Seed script | Generates realistic volume and a realistic distribution, not twelve tidy rows. |
| Role and privilege note | What the application role may do, what the migration role may do, and why nothing is a superuser. |
| Retention and recovery statement | What you intend for backups, recovery, and how long data is kept. |
| Audit placement decision | Explicit application-layer writes or database triggers, with the actor-context problem addressed. |

## Rubric

Every **Required** row at "meets". At least four **Distinguishing** rows at "meets" to pass.

| # | Criterion | Weight | Fails | Meets | Exceeds |
| --- | --- | --- | --- | --- | --- |
| 1 | Durability | Required | Restart loses data | Records survive restart and reconnection | Reconnection after a database restart handled without a service restart |
| 2 | Constraint enforcement | Required | Bad data accepted when issued directly to the database | Every stated assertion refused by the database | Each constraint paired with the assertion it enforces, in writing |
| 3 | Append-only history | Required | Status changes updated or deleted | Insert-only, with actor and time on every row | Service role provably unable to modify them |
| 4 | Idempotency | Required | Two rows from two identical submissions, or a check-then-insert implementation | One row, same response, enforced by a constraint | Concurrent case tested, not just sequential |
| 5 | Transactional integrity | Required | Partial writes survive a failure | Deliberate rollback leaves nothing behind | No orphan status change or phantom audit row under any injected failure |
| 6 | Concurrency | Required | Lost update possible | Prevented, with the mechanism justified | Operator receives a useful "changed underneath you" outcome |
| 7 | Least privilege | Required | Service role can alter schema or modify audit rows | Privileges separated | Separation verified by attempting each forbidden action |
| 8 | Interface stability | Distinguishing | Layers above storage needed changes | Only the implementation behind the interface changed | Both implementations still satisfy the same tests |
| 9 | Evidence-based indexing | Distinguishing | Index added on instinct | Two plans at realistic volume, with the decision recorded | Partial or covering index justified by the actual query shape |
| 10 | Migration discipline | Distinguishing | An applied migration edited, or a destructive change in one step | Ordered, immutable, expand-and-contract where destructive | Notes which migrations take blocking locks |
| 11 | Time modelling | Distinguishing | Local time, text timestamps, or client-supplied times | Instants with zone, recorded versus occurred distinguished | Consequence for chapter 35 duration metrics stated |
| 12 | Policy versioning | Distinguishing | Derived priority stored bare | Policy version stored alongside | A historical decision reproducible from the stored version |
| 13 | Operational bounds | Distinguishing | No statement timeout or unbounded pool | Both configured and reasoned | Pool size derived from the database's own limits and expected concurrency |
| 14 | Query correctness | Distinguishing | Absence handled accidentally | Nullable columns handled explicitly in every query | A test that would fail if a nullable column silently excluded rows |

## Self-check before you call it done

- Read your schema aloud as assertions. Which sentences are hopes rather than constraints?
- Issue an incident with an invalid severity straight to the database. What happens?
- Update an audit row as the application role. What happens?
- Submit the same idempotency key twice at the same moment. How many rows?
- Change one incident's status from two sessions simultaneously. What does the second one learn?
- Run your operator list query at ten thousand rows. What does the plan say, and did you look before adding the index?
- If the customer redefined critical next week, which stored priorities would become unexplainable, and what saves you?
- What did you change above the storage interface? If the answer is anything, why?

## Time and depth

The heaviest chapter in Part III. Budget most of it for the schema and the two concurrency tests; those are where the learning is. If you are writing application features, you have drifted.

## Stuck hints

Read only after a real attempt. Printed upside down on purpose.

˙ǝuo ʇou 'suoᴉʇɐɹƃᴉɯ ɹnoɟ ǝɹɐ ǝʌoɯǝɹ puɐ 'ɥɔʇᴉʍs 'ןןᴉɟʞɔɐq 'pp∀ ˙ʇᴉ ʇᴉןds 'ƃuᴉuǝʇɥƃᴉɹɟ sᴉ uoᴉʇɐɹƃᴉɯ ɐ ɟI ˙8
˙ɐʇɐp sᴉ ʇᴉ 'ʇᴉ sʇᴉpǝ ɹǝɯoʇsnɔ ǝɥʇ ɟI ˙ʇsᴉן ǝɥʇ sʇᴉpǝ oɥʍ ʞsɐ 'ǝןqɐʇ dnʞooן ɐ puɐ ǝdʎʇ pǝʇɐɹǝɯnuǝ uɐ uǝǝʍʇǝq ǝpᴉɔǝp ʇouuɐɔ noʎ ɟI ˙ㄥ
˙pɹɐʍdn ʇdǝɔuoɔ ǝsɐqɐʇɐp ɐ pǝʞɐǝן ǝuo ʎןןɐnsn — sǝɹnʇɐuƃᴉs poɥʇǝɯ ,suoᴉʇɐʇuǝɯǝןdɯᴉ oʍʇ ǝɥʇ ǝɹɐdɯoɔ 'sǝƃuɐɥɔ pǝpǝǝu ǝƃɐɹoʇs ǝʌoqɐ sɹǝʎɐן ɟI ˙9
˙spɹɐʍɹǝʇɟɐ ƃuᴉɹǝʇןᴉɟ uɐɥʇ ɹǝɥʇɐɹ ʎɹǝnb ǝɥʇ ɟo ʇɹɐd sɐ uoᴉʇɐsᴉɹoɥʇnɐ ǝɥʇ ssǝɹdxǝ 'ǝǝs ʇou ʎɐɯ ɹǝןןɐɔ ǝɥʇ ɐʇɐp ƃuᴉɥɔnoʇ ʇnoɥʇᴉʍ ʇᴉun ʎq ɹǝʇןᴉɟ ʇouuɐɔ ʎɹǝnb ɐ ɟI ˙ϛ
˙uoᴉʇɔɐsuɐɹʇ ǝɯɐs ǝɥʇ uᴉ ʇou ǝɹɐ ʎǝɥʇ 'ǝǝɹƃɐsᴉp ɹǝʌǝ uɐɔ ǝƃuɐɥɔ ǝɥʇ puɐ ʍoɹ ʇᴉpnɐ ǝɥʇ ɟI ˙ㄣ
˙uoᴉsnןɔuoɔ ʎuɐ ƃuᴉʍɐɹp ǝɹoɟǝq uoᴉʇnqᴉɹʇsᴉp ɔᴉʇsᴉןɐǝɹ ɐ ɥʇᴉʍ sʍoɹ puɐsnoɥʇ uǝʇ ǝʇɐɹǝuǝ⅁ ˙ɐʇɐp ǝןʇʇᴉן ooʇ ǝʌɐɥ noʎ 'ǝɯɐs ǝɥʇ ʞooן ןןɐ suɐןd ɹnoʎ ɟI ˙Ɛ
˙pɐǝɹ noʎ uoᴉsɹǝʌ ɐ uo ǝʇɐpdn ןɐuoᴉʇᴉpuoɔ ɐ ɹo ʞɔoן ɐ ɹǝɥʇᴉǝ ʇnoɥʇᴉʍ ƃuᴉʇᴉɹʍ puɐ ƃuᴉpɐǝɹ ǝɹɐ noʎ 'pǝǝɔɔns ɥʇoq sǝƃuɐɥɔ snʇɐʇs snoǝuɐʇןnɯᴉs oʍʇ ɟI ˙ᄅ
˙uoᴉʇnןosǝɹ ʇɔᴉןɟuoɔ snןd ʇuᴉɐɹʇsuoɔ ǝnbᴉun ɐ sᴉ ǝןqɐןᴉɐʌɐ ɯsᴉuɐɥɔǝɯ ɔᴉɯoʇɐ ʎןuo ǝɥ⊥ ˙ɔᴉƃoן uoᴉʇɐɔᴉןddɐ ƃuᴉʇᴉɹʍ doʇs 'ʎɔɐɹ sןǝǝɟ ʎɔuǝʇodɯǝpᴉ ɟI ˙Ɩ
