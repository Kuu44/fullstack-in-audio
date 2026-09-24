---
chapter: 14
title: "NoSQL and fit-for-purpose storage"
roadmap_nodes: ["NoSQL Databases"]
part: "III — Make the backend and data reliable"
audio: media/14-nosql-and-storage-fit.mp3
voice: en-US-AndrewNeural
rate: "-15%"
companion_guide: docs/guides/14-nosql-and-storage-fit.md
---

# Chapter 14 — NoSQL and fit-for-purpose storage

[[Spoken narration begins below. Headers and this note are stripped before rendering.]]

## Orientation

Chapter fourteen, the last chapter of Part Three. And this is a strange chapter, because the skill it teaches is mostly the skill of saying no.

Where we stand. PostgreSQL is the system of record. Incidents survive restarts. Status changes and audit events are append-only and the service cannot rewrite them. Idempotent creation is enforced by a unique constraint, so a retried submission produces one record. Concurrent status changes cannot silently lose one. You have one index chosen from a real query plan at realistic volume, hand-written migrations, and separated database privileges.

That is a solid foundation, and the temptation that arrives next is predictable. The dashboard needs counts and the query feels slow. The rate limiter from chapter twelve needs counters and putting them in the relational store feels wrong. Chapter twenty will need vector search. Chapter twenty four will bring integration payloads with irregular shapes. And somebody — possibly a customer's architect, possibly you at eleven at night — will propose a document database, a key-value store, a search engine, and a graph database, each with a genuine-sounding reason.

So this chapter has two jobs. Teach you the actual storage families well enough to choose between them competently. And teach you the decision discipline, because in field work every datastore you add becomes something the customer operates, patches, backs up, monitors, secures, and pays for, for years, possibly after you have left.

The practical work is small: add one expiring cache for one derived value, behind an interface, with defined behaviour when it is unavailable. The written work is the real deliverable: a storage decision record that states the cost of each additional datastore and why the ones you did not add are not needed yet.

## What NoSQL actually means

Let me dispose of the term first. NoSQL is not a technology. It is a historical label for several unrelated families of storage that share only the property of not being a traditional relational database. Treating them as one thing is how teams end up with the wrong one.

There are five families worth knowing, and I want you to hold each one as a data model plus an access pattern plus a sacrifice.

Key-value stores. The model is a dictionary: a key, an opaque value. The access pattern is get and set by exact key, extremely fast, often in memory. Many offer richer value types — counters, lists, sets, sorted sets — and expiry on individual keys, which is the feature we actually want today. What you give up is querying: you cannot ask for all the values matching a condition, because the store has no idea what is inside the values. Everything must be reachable by a key you can construct. Typical uses: caches, session state, rate-limit counters, distributed locks, lightweight queues and notification channels.

Document stores. The model is a collection of self-describing documents, usually nested, each independently retrievable and queryable by its contents. Good when the natural unit of work is one whole nested object, when shapes vary between records, and when you want to store an incoming payload as it arrived without designing a schema first. What you give up, and this is understated in the marketing: multi-record integrity guarantees are weaker and more manual, and the absence of a declared schema does not eliminate schema — it relocates it into every piece of code that reads the data, forever, including code that must still handle documents written two years ago.

Wide-column stores. The model is rows partitioned across many machines, with the partition key deciding placement. Extremely high write throughput, predictable performance at large scale, and queries essentially limited to the access patterns you designed the partitioning for. You give up query flexibility almost entirely: you design the table per query, and adding a new access pattern later can mean rewriting your data. Warranted at genuinely large scale with known patterns — telemetry, event streams, time series.

Graph databases. The model is nodes and edges with properties, and the access pattern is traversal: find things connected to this thing, several hops away, along particular relationship types. When your questions are genuinely about relationship paths — which assets depend on this service, which change touched anything upstream of this incident — a graph traversal is expressive in a way that repeated relational joins are not. What you give up is a smaller operational ecosystem, a query language your customer's team probably does not know, and, for shallow relationships, no real benefit at all, because a relational join two levels deep is perfectly fine.

And a fifth family worth naming because it will matter in chapter twenty: specialised search indexes, including vector stores. Text search engines are built for ranking and relevance rather than exact matching. Vector stores are built for nearest-neighbour search over embeddings. These are cases where the specialised tool genuinely does something a relational store does poorly — although note that PostgreSQL has capable extensions for both, which is a real option and one you should evaluate rather than dismiss.

## Consistency, said honestly

Now the property that separates these systems, and the one most often explained badly.

Every distributed store faces a choice when the network between its parts breaks. It can refuse to answer, preserving one consistent view, or it can answer from a part that may not know about recent writes elsewhere. That is the actual content of the famous trade-off theorem, and note the important qualifier: it describes behaviour during a network partition, not a general licence to say relational databases are consistent and everything else is fast.

The more useful everyday framing is what a client observes. Under a strongly consistent read, once a write succeeds, every subsequent read sees it. Under eventual consistency, reads may return older values for some window, converging later.

Now translate that into your operator's experience, because that is the only translation that matters. An operator changes an incident from open to acknowledged, and the list still shows open. They change it again. Now there are two status changes in the audit trail and the operator believes the tool is broken. That is what eventual consistency feels like at the human scale, and it is why the two guarantees you should care about have plain names: read-your-writes, meaning a person sees their own change immediately, and monotonic reads, meaning they never see time move backwards.

For anything an operator acts on, you want read-your-writes. That is one more argument for the relational store as the source of truth for state and for reading derived values carefully — and it is the argument that will determine your invalidation strategy in a moment.

## Caching: the concepts you need today

The practical work of this chapter is a cache, so let me define the patterns precisely.

Cache-aside is the pattern you will use. On a read, look in the cache; if it is there, return it; if not, read the source of truth, store it in the cache, and return it. Your application owns the logic, and the cache is a genuinely optional accelerator. Its great virtue is that removing the cache entirely leaves a correct, slower system.

Read-through and write-through push that logic into a layer that sits in front of the source. Write-behind acknowledges a write after storing it in the cache and persists it later — and I want you to notice what write-behind means: the cache is now holding data that exists nowhere durable, which makes it a system of record with no durability guarantees. That pattern has legitimate uses and this project is not one of them. Our rule, stated once and never broken: deleting the entire cache must not lose an incident, a status change, or an audit event.

Then expiry. A time-to-live on each entry bounds how stale a value can be, and it is your safety net for every invalidation you forget to write. Choose the duration from the product, not from a habit: how stale may a dashboard count be before an operator makes a wrong decision? For a count of open incidents by service, thirty to sixty seconds is often genuinely fine, and you should be able to defend the number to a customer. Write it in the interface if it matters — a small line saying counts update every minute converts a bug report into an understood behaviour.

Then invalidation, which is the hard half. Expiry alone means every value can be stale for its full window. Explicit invalidation on write makes changes visible immediately. The rule that reconciles them with what we said about consistency: invalidate the affected entries in the same operation that changes the data, and keep expiry as the backstop. And where a specific user has just made a change, prefer to serve them the authoritative value rather than a cached one, so read-your-writes holds for the person who acted.

Then two failure modes with memorable names. A stampede is what happens when a popular entry expires and a hundred concurrent requests all miss and all recompute it simultaneously, and your database absorbs a hundred copies of an expensive query at once. Defences: a short lock so one request recomputes while others wait or serve the stale value, or staggering expiry times so entries do not expire together. And negative results are worth caching too — remembering that a lookup found nothing prevents a repeated expensive miss, as long as you invalidate it when the thing is created.

Then the failure behaviour, which must be a decision rather than an accident. If the cache is unreachable, what happens? For a read-model cache, the answer is easy: fall through to the source of truth, log it, serve a slower correct answer. Never fail a request because an accelerator is missing.

For a rate-limit counter, the answer is genuinely hard and I want you to sit with it. If the counter store is down and you fail open, you have no rate limiting at exactly the moment your system is fragile. If you fail closed, you have just converted a cache outage into a total outage for all writes. Neither is obviously right. The defensible answers are a local in-process fallback limit — cruder, per-instance, better than nothing — or failing open while raising an alert and treating it as a genuine incident. What is not defensible is not knowing which one your system does. And this is exactly the type of question a customer's security reviewer asks in chapter thirty two, so decide it now and write it down.

Finally, cache key design, and this one is security-critical. A cache key must include every dimension that changes the correct answer, and that includes who is asking. If your dashboard summary is cached under a key that names only the time window, and your authorisation from chapter twelve scopes results by business unit, then the first operator's cached summary is served to the second operator from a different unit. You have just built a cross-tenant data leak, and you built it with a caching optimisation rather than a permission bug, which means none of your authorisation tests will catch it. Put the scope in the key. Test it. This is the single highest-severity mistake available in this chapter.

## The two candidates in FieldOps Copilot

Now apply all of that to our system. Two derived values are legitimate candidates, and the chapter asks you to implement one.

Candidate one: a read-model summary. Counts of open incidents by service and severity, for a dashboard. It is derived — recomputable from the relational store at any time. It is non-authoritative — nobody makes an irreversible decision from a count. It is comparatively expensive to compute as data grows, and it is requested repeatedly. It has an obvious invalidation trigger: an incident created, or a status changed, in the affected scope. And it has a defensible staleness window. That is a textbook fit.

Candidate two: a rate-limit counter, which chapter twelve required and which you may have implemented in memory. In-memory counters are wrong the moment there are two instances of your service, which chapter thirty makes likely, because each instance enforces its own separate limit. A shared counter store with per-key expiry is the standard solution, and the atomic increment operations these stores provide are exactly the primitive you need — remembering chapter eleven's lesson that read-then-write across a suspension point is a race, and that the fix is an atomic operation, not careful code.

Either is a good choice. The summary teaches invalidation; the counter teaches atomicity and the hard failure-mode question. Pick one, implement it properly, and note the other.

## The decision discipline

Now the part I actually care about most.

Before adding any datastore, cost it honestly. An additional datastore is not a dependency line in a manifest. It is: a deployment to define, a version to patch, a high-availability story, a backup and restore procedure someone must test, monitoring and alerts, a security review, capacity and cost, a network path and a set of firewall approvals, credentials to manage and rotate, a failure mode to document in a runbook, and knowledge that whoever is on call must have. In a customer environment, several of those require other people's approval and calendar time.

Then check whether you already have the capability. PostgreSQL is more capable than the reflex acknowledges. It stores and indexes semi-structured documents natively, which handles the irregular integration payloads chapter twenty four will bring. It has full-text search that is genuinely adequate for many products. It has a notification mechanism for lightweight publish and subscribe. It has extensions for vector similarity. It can hold counters — and yes, a high-write counter is a poor fit and a purpose-built store is better, but the honest comparison is against your actual volume, not against a hypothetical one. In a pilot serving a few hundred incidents a day, the relational store handles all of it, and the second datastore buys latency you cannot measure at a cost the customer can.

So the discipline: one datastore until a measured need justifies another. Measured, not anticipated. And when the need is real, say what specifically it is — this query at this volume exceeds this budget, or this data has a lifecycle the relational store would need a cleanup job for, or these counters are written thousands of times a second, or this is nearest-neighbour search over embeddings and a specialised index is a genuine capability difference.

Be equally willing to remove. If you add a cache and then measure that it saves four milliseconds on a query nobody complains about, delete it, and write down what you learned. Removing infrastructure is one of the most valuable things a forward deployed engineer does, and almost nobody gets credit for it, so give yourself the credit in the decision record.

One more thing about document stores specifically, because the flexibility argument is seductive and worth defusing. Storing a payload without designing a schema is genuinely useful at an ingestion boundary. But schemaless does not mean no schema; it means the schema now lives in every reader, and it accumulates historical variants forever. Three months in, some documents have a field, some do not, some have it with a different type, and every function that reads them must handle all three cases. Relational migrations are work, and they are the work of resolving that ambiguity once, in one place, with a review. When someone offers you flexibility, ask them where the schema went.

## Expiry is not retention

A quick distinction, because the two get conflated and one of them is a legal obligation.

Expiry is a performance and correctness setting: how long may this derived value be trusted before it must be recomputed. You choose it from the product, and its worst outcome is a slightly stale number.

Retention is a policy about how long you are permitted or required to keep information about people and their work. It is driven by the customer's obligations, sometimes by regulation, and it applies to your incidents, your status history, your audit trail, your logs, and — this is the part people miss — anything you copied into a cache or a secondary store.

Two consequences. First, if you cache anything derived from personal or sensitive content, that copy is now in scope for the customer's retention and deletion commitments. When someone asks you to delete a person's data, an expiry setting is not an answer, because expiry is not deletion on demand and because a value may be refreshed indefinitely. This is precisely why the rule to cache identifiers and aggregates rather than free-text content is worth following even when caching the content would be easier.

Second, your relational store needs a retention answer of its own, and audit records complicate it, because the same regulation that says delete personal data on request often coexists with a requirement to retain an audit trail. The resolution is usually to separate the identifying content from the event record, so that a deletion removes the former and leaves a non-identifying trace of the latter. You do not have to solve that today. You do have to notice, now, that every additional copy of data you create makes that eventual conversation harder — which is one more entry on the true cost of a second datastore.

## Queues: the other component people add

Worth a short section, because a queue is the second most commonly proposed addition after a cache, and you sketched one back in chapter five.

A queue decouples the moment work is accepted from the moment it is done. It lets you absorb a burst, retry a failing step without making the caller wait, and apply backpressure instead of collapsing. In chapter twenty four you will genuinely want its close relative — a place to put records that failed validation, so a bad row is quarantined rather than lost. And in chapter nineteen, a model call that takes fifteen seconds is a natural candidate for accepting the request and doing the work asynchronously.

The costs mirror the ones we have discussed. Something must run the broker, and something must run the workers. You now have asynchronous failure, which means a failure with no user attached to it, which means it needs its own alerting or it is invisible. You need to handle duplicate delivery, because most queues promise at-least-once rather than exactly-once — and note that you already built the defence for that in chapter thirteen, which is what an idempotency key is for. And you need to decide what a caller is told when the work has been accepted but not yet done, which is an interface design question, not an infrastructure one.

The honest assessment for our current state: intake is fast, triage is a rule evaluation and a database write, and nothing takes long enough to need deferring. So no queue today. Note the two places it becomes justified — the model call in Part Four and the pipeline in Part Five — and note that a relational table with a status column is a perfectly respectable queue at pilot volume, which is a genuinely underrated option and one you can operate with the components you already have.

Add that assessment to the same decision record. The record is not a cache document; it is the storage and infrastructure argument for this system, and it will be read by someone deciding whether to approve your deployment.

## Why a forward deployed engineer cares

Three arguments.

The first is that the operational surface you request is a negotiation you must win. Every component you ask a customer's platform team to run is a thing they must accept, secure, and support. Asking for one service and one database is a conversation. Asking for a service, a relational database, a cache, a document store, a search cluster, and a message broker is a project with a steering committee, and I have watched exactly that request delay a pilot past the window in which anyone was still enthusiastic. Your architecture is also a procurement document, whether or not you intended it to be.

The second is that the second half of this course is full of storage temptations, and they all arrive wearing the clothes of necessity. Conversation memory. Retrieved document chunks. Embeddings. Model responses to cache. Evaluation results. Trace data. Tool call logs. Each has a plausible specialised home. If you do not have a decision discipline before chapter fifteen, you will finish chapter twenty three with six datastores and no way to justify any of them to the person who has to run them.

The third is that caches are where correctness quietly dies. A cache is invisible when it works and mysterious when it does not. A stale value looks like a bug in your logic. A badly scoped key looks like an authorisation flaw. A cache that has become the only copy of something looks like data loss, because it is. So the rule bears one more repetition: authoritative data lives in the system of record, caches hold derived values, and deleting every cache must cost you nothing but speed.

## Pitfalls, named

Caching authoritative data. If losing the cache loses information, it is not a cache, it is an undurable database.

A cache key missing its scope. Cross-tenant leak, invisible to authorisation tests. The highest-severity mistake in this chapter.

No expiry. An entry cached once and never invalidated is wrong forever, and nothing in your system will tell you.

No invalidation, only expiry. Every value is stale for its full window, including immediately after the operator changed it.

Ignoring read-your-writes. The person who just acted must see their change. Serve them the authoritative value.

Unbounded memory. A key-value store with no expiry policy and no eviction policy eventually fills, and its failure mode when full is frequently to stop accepting writes — which, if you also put your rate-limit counters there, takes your write path down.

Stampede on expiry. A hundred concurrent recomputations of the same expensive query.

Undecided failure behaviour. Nobody knows what happens when the cache is down. Decide, implement, document, and for the rate-limiter case, be explicit about the open-versus-closed trade you accepted.

Sensitive content in a weakly controlled store. Incident descriptions may contain customer names and locations. A cache typically has weaker access control, weaker audit, weaker encryption configuration, and a different retention story than your database. Cache identifiers and aggregates, not free-text content, and if you must cache content, classify it and control it as such — chapter thirty two will ask.

Serialisation drift. The shape you cached last week is read by code you deployed today. Version your cached shapes, or namespace them with a version so a deployment simply misses and refills rather than misreading.

Reinventing locking. Distributed locks built on a cache are subtly wrong in more ways than fit in this lesson — expiry versus work duration, ownership, clock assumptions. If you need one, use a well-understood mechanism, and prefer the database's own locking, which chapter thirteen already gave you.

Adding a document store for flexibility, then reimplementing constraints, uniqueness, and joins in application code, badly.

Forgetting the new store in the backup story, the threat model, the runbook, and the cost estimate. If it is worth adding, it is worth adding to all four.

And the meta-pitfall: adopting a datastore because of an article, a conference talk, or an architect's preference, rather than because a measurement demanded it.

## Verifying your work

Eight checks, and the first two are the ones that matter most.

Delete the entire cache while the system is running. Confirm that nothing is lost, that every request still succeeds, and that the only difference is latency. If any incident, status change, or audit event is affected, you have violated the central rule of the chapter.

Make the cache unreachable — stop it entirely — and exercise every path that touches it. Confirm the behaviour matches what you wrote down: reads fall through, the failure is logged and visible, and whatever you decided for the rate limiter is what actually happens. Do not accept an unhandled failure surfacing to the operator.

Test the staleness window deliberately. Change the underlying data without invalidating, and confirm the cached value updates within the window you promised, and no later.

Test invalidation. Change the data through the real path, and confirm the affected entry is invalidated immediately, and confirm that the operator who made the change sees their change immediately.

Test scope isolation. Cache a summary as one operator in one business unit, then request it as an operator in another, and confirm you get their answer and not the first one. This is the test that catches the leak.

Test concurrency, if you built the counter. Fire many simultaneous requests and confirm the count is exact, which requires the store's atomic operation rather than read-then-write.

Measure the benefit. Before and after, at realistic volume, on the query that motivated this. Record the numbers. If the improvement is not worth the component, remove the component and record that instead — that outcome is a pass, not a failure.

And bound the memory. Confirm the store has an eviction policy and a maximum, and confirm you know what happens when it reaches it.

## Your practice test

The guide has the rubric. Spoken:

Your goal is to add exactly one expiring cache for one derived, non-authoritative value, behind an interface, with defined behaviour when it is unavailable — and to produce a storage decision record that justifies every datastore this system has and every one it does not.

Your constraints: the cached value must be derived and recomputable, and deleting the cache must lose nothing. The cache lives behind an interface with a no-op implementation so tests and local development can run without it. PostgreSQL remains the source of truth for every fact. Cache keys include every dimension that changes the answer, including the authorisation scope. Every entry has an expiry, and there is explicit invalidation in the same operation that changes the underlying data. Behaviour when the cache is unavailable is decided, implemented, and written down — including, if you chose the rate limiter, an explicit position on failing open versus failing closed. No free-text incident content is cached without a classification decision. Cached shapes are versioned so a deployment cannot misread an old shape. And the benefit is measured, with removal a legitimate outcome.

Your artifacts: the cache adapter and its interface, with the no-op implementation; a cache specification stating key structure, expiry, invalidation triggers, and unavailable-behaviour for each cached thing; a measurement pair showing the query before and after at realistic volume; a scope-isolation test proving one unit's cached value is never served to another; a resilience test showing the cache deleted and stopped with no data loss and defined degradation; and the storage decision record.

That decision record is the real deliverable, so let me be specific about what it must contain. For each datastore you now have, why it exists and what it costs to operate — deployment, patching, availability, backup, monitoring, security review, credentials, on-call knowledge, and money. For each family you did not adopt — document, wide-column, graph, search — one honest paragraph on what it would give you, what would have to become true for it to be justified, and what capability of your existing store makes it unnecessary today. And a note on chapter twenty, which will genuinely need vector similarity search, naming the two options you will compare when you get there.

You are done when deleting the cache cannot lose an incident or an audit event, when a stale result has an explicit acceptable window or is invalidated, when a second operator cannot receive the first operator's cached answer, when the unavailable behaviour is what you said it would be, and when the decision record names the cost of each additional datastore in terms a customer's platform team would recognise.

## Recap

Five things.

First, NoSQL is a label over several unrelated families. Key-value for exact-key speed and expiry, document for whole-object work and irregular shapes, wide-column for scale with fixed access patterns, graph for genuine traversal, specialised indexes for search and similarity. Each is a model plus an access pattern plus a sacrifice.

Second, consistency is best judged by what a person observes. For anything an operator acts on, you want them to see their own change immediately, and never to see time run backwards.

Third, a cache is an accelerator for derived values. Expiry as the backstop, invalidation in the same operation as the change, scope in the key, and defined behaviour when it is gone. Deleting it may cost speed and nothing else.

Fourth, the cost of a datastore is operational, and most of that cost lands on the customer, for years. One datastore until a measurement justifies another, and be willing to remove what you added.

Fifth, schemaless does not remove the schema. It moves it into every reader, permanently. When someone offers flexibility, ask where the schema went.

Part Three is complete. FieldOps Copilot now has a durable, secured, contract-published service with an authoritative record, an audit trail, enforced idempotency, and one justified accelerator. In chapter fifteen the AI layer begins — and it begins the same way this chapter ended, with a provider-agnostic seam, a deterministic fake, and a decision you can defend. Build the cache and write the record. Then meet me there.
