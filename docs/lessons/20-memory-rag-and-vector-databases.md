# Chapter 20 — Memory, RAG, and vector databases

**Roadmap nodes covered:** Memory & State Management; RAGs; Vector DBs
**Part:** IV — Build AI behavior that can be controlled
**Companion test:** `docs/guides/20-memory-rag-and-vector-databases.md`
**Audio:** `media/20-memory-rag-and-vector-databases.mp3`

---

## Narration

Welcome to chapter twenty.

Your triage workflow is explicit now. It has named states, deterministic screening before any model call, a bounded tool loop, four stop conditions, a durable approval gate, and a record of every transition. It is a well-behaved system.

It is also ignorant. It knows what a generic model knows about incident management, plus the text of one incident, plus possibly one other incident it looked up. It knows nothing about how this customer actually works — their escalation procedure, their known issues, their workarounds, the fact that the warehouse scanner has a documented restart sequence that resolves seventy percent of its failures.

All of that exists. It is in their runbooks. Today we connect it.

And we do it the way an enterprise requires: grounded in sources the operator can check, filtered so a tenant can never see another tenant's material, honest when the evidence is weak, and with a plan for what happens when a document changes.

The plan for the next half hour. First, a distinction I flagged last chapter and now want to make properly: state versus memory versus knowledge. Second, why retrieval rather than the alternatives. Third, how retrieval actually works — embeddings, chunking, metadata, and search. Fourth, why pure vector search is not enough on operational text. Fifth, tenant isolation, which is the hard requirement. Sixth, grounding and citations. Seventh, freshness. Eighth, choosing a store. Ninth, evaluating retrieval separately, which is the thing almost nobody does and which explains most failures. Then pitfalls, verification, and your test project.

### State, memory, and knowledge

Three things get called memory and they have completely different properties. Conflating them is the most common design error in this area, so let us separate them cleanly.

Workflow state is the bookkeeping for one run. Which state the machine is in, the accumulated context, how many tool calls have been made, the running cost. It has a defined lifetime: it is created when the run starts and it is finished when the run terminates. You built this last chapter. It is not memory. It is a scratchpad.

Conversation or session memory is the context within one interaction. For a chat product this is the transcript. For us it barely exists, because triage is a single-shot operation rather than a dialogue — which is a simplification worth noticing and being grateful for.

Durable learned memory is the system writing down facts about a user, a tenant, or the world, and recalling them later. "This operator prefers terse rationales." "This customer treats the warehouse scanner as critical." This is the thing people usually mean when they say an AI system has memory, and I want you to be genuinely cautious about it.

Knowledge is the customer's authored content. Runbooks, procedures, policies, escalation matrices, service catalogues. The customer wrote it, the customer owns it, the customer maintains it, and — this is the key property — it has a source you can point at.

Now the rule I want you to carry into every enterprise AI deployment: prefer retrieved, cited knowledge over learned memory, every time you can.

Here is why, and it is worth spelling out because learned memory is seductive.

Learned memory is the system writing. Everything we have built has been careful about the model influencing writes, and durable memory is precisely that — the model's interpretation of something, persisted, and then fed back into future decisions. If the model misunderstands once, that misunderstanding can become a permanent input to every subsequent run. It is a hallucination with tenure.

Learned memory has no provenance you can show anyone. "The system believes the warehouse scanner is critical" — based on what? A retrieved runbook passage has an answer: this document, this section, revised on this date, owned by this person. A learned memory has a shrug.

Learned memory is a data retention and deletion problem. Your customer's privacy obligations apply to it. When an employee leaves and their data must be deleted, you need to find and remove whatever the system learned about them, and a pile of model-written notes is a genuinely hard thing to audit.

And learned memory is usually solving a problem that configuration solves better. If the warehouse scanner is critical, that belongs in the service catalogue as an attribute — reviewed, owned, visible, correctable — not inferred and stored by a model.

There is a place for durable memory, and I do not want to be absolute. Operator display preferences, a per-tenant terminology glossary, accumulated known-issue notes that a human curates. Notice what those have in common: they are small, human-reviewable, human-correctable, and they do not silently change a decision. If you introduce learned memory, keep it to that shape. What you must not build in a pilot is a system that quietly accumulates model-written beliefs and acts on them, because when it goes wrong you will not be able to explain why, and "I do not know why it thinks that" is a sentence that ends deployments.

So for FieldOps Copilot: knowledge, retrieved and cited. Workflow state, ephemeral. No learned memory in the pilot, and a note in the charter saying so and why.

### Why retrieval

Three ways to give a model knowledge it does not have. Let me compare them on the axes a customer cares about.

Fine-tuning. Train on the customer's documents so the knowledge is in the weights. It works for teaching style, format, and domain vocabulary. For facts it is a poor fit, for four reasons that are decisive in enterprise. It is stale the moment a document changes, and retraining is not something you do on a Tuesday afternoon. It cannot express access control — the weights do not know which user is asking, so a fine-tuned model that has seen restricted content can surface it to anyone. It cannot cite, so the operator has no way to verify. And it is expensive and slow to iterate. Fine-tuning has real uses; being the customer's knowledge base is not one of them.

Long context stuffing. Put all the runbooks in the prompt. The window is large, so why not. Because it does not scale — a real runbook corpus is far larger than any window. Because you pay for every token on every call, forever. Because latency scales with input. Because attention degrades across very long inputs, so burying the relevant paragraph in the middle of a hundred pages makes it less likely to be used, not more. And because it has the same access-control problem: everything in the prompt is available regardless of who is asking.

Retrieval. Find the small number of relevant passages, include those, cite them. It is fresh, because the index reflects the current documents. It is filterable, because retrieval is a query and a query can have access predicates. It is citable, because you know exactly which passage you supplied. It is cheap, because you send a few hundred tokens instead of a few hundred thousand. And it is inspectable — you can look at what was retrieved and see immediately whether the failure was retrieval or generation.

Retrieval wins on the axes enterprises actually score, and the citation and access-control properties are not nice-to-haves. They are usually the reason the deployment is approvable at all.

### How retrieval works

Now the mechanics, conceptually.

Embeddings. An embedding model converts a piece of text into a list of numbers — a vector, typically several hundred to a couple of thousand dimensions. The useful property is that texts with similar meaning land near each other in that space, so you can find related content by finding nearby vectors, usually measured by the cosine of the angle between them. That is the whole trick: semantic similarity becomes geometric proximity.

Two engineering consequences. The embedding model is a versioned dependency exactly like your language model — record which one produced each vector. And changing it invalidates your entire index, because vectors from different models are not comparable. Reindexing a large corpus is a real operation with a real cost, so treat an embedding model change as a migration, plan it, and never let it happen by accident through a floating version.

Chunking. You cannot embed a whole document usefully — a single vector for a fifty-page runbook averages everything into meaninglessness. So you split documents into chunks and embed each.

Chunk size is a genuine tradeoff. Too small and each chunk loses the context that makes it interpretable; a step that says "restart the service" is useless without knowing which service. Too large and the relevant sentence is diluted by surrounding material, so the vector drifts away from the query and you fail to retrieve it. Hundreds of words is a common working range, but the right answer depends on your documents.

Three strategies. Fixed-size chunks with overlap are the simple default; the overlap prevents a concept from being severed at a boundary. Structural chunking splits on the document's own structure — headings, sections, procedure steps. Semantic chunking tries to split where the topic shifts.

For runbooks, structural chunking is usually right, and the reason is specific: runbooks are already organized into procedures, and splitting a procedure in the middle produces a chunk that tells an operator to do step four without steps one through three. That is not merely unhelpful, it is potentially dangerous in an operational context. Respect the document's own boundaries, and keep the heading path as part of the chunk text so the chunk carries its own context.

Metadata. This is the part that gets the least attention and matters the most in enterprise, so I want to be emphatic. Every chunk carries, at minimum: the tenant it belongs to; the access level or role required; the owning team or person; the revision date; the source document identifier; the section or heading path; and a link that lets an operator open the original. Some of that drives filtering, some drives citation, some drives freshness decisions. Design it before you index anything, because retrofitting metadata means reindexing.

Retrieval itself. At query time you embed the query, apply your metadata filters, and ask the store for the nearest vectors, taking the top handful. Keep that number small — five or so for a focused task. More results mean more tokens, more dilution, and more opportunity for an irrelevant passage to mislead.

### Why pure vector search is not enough

An important practical point that trips up first implementations.

Vector search is good at meaning and bad at exact tokens. Operational text is full of exact tokens: error codes, service names, host names, ticket identifiers, product version strings. An operator searching for a specific error code wants the document containing that exact code, and semantic similarity will happily return three documents about similar-sounding problems and miss the one that names it.

So use hybrid retrieval: run a keyword search alongside the vector search and combine the results. Classical keyword scoring handles exact matches and rare terms precisely, which is exactly the vector model's weakness. Combining the two ranked lists — reciprocal rank fusion is a simple and effective method — reliably beats either alone on technical corpora. This is not an optimization for later; on operational documents it is often the difference between a system that works and one that does not.

Two refinements worth knowing. Reranking: retrieve a slightly wider set, perhaps twenty candidates, then score each one against the query with a model that looks at the pair together rather than at two independent vectors. That is more accurate and more expensive, and applied to twenty candidates it is affordable. It substantially improves what actually reaches the prompt.

Query construction: the incident description is not a good search query. It is long, it contains noise, and it may contain irrelevant detail. Constructing a focused query — from the structured fields you already have, or by a cheap model call that extracts the searchable essence — improves retrieval meaningfully. Start with the deterministic version using your structured fields, because it is free and it is often enough.

### Tenant isolation

Now the hard requirement, and the one where a mistake is not a quality problem but an incident.

The rule: the tenant filter is applied inside the query, in the store, before results are produced. Not afterwards.

Why post-filtering is unacceptable, in three parts. First, if you retrieve the top five across all tenants and then discard the ones that do not match, you may be left with one result or none, and now your system is silently degraded in a way that depends on other customers' data volume. Second, and worse, the other tenant's content was in your process memory, in your logs if you log retrieval results, and in your traces. You have handled data you were not entitled to handle, and in a regulated context that may be reportable regardless of whether it reached a user. Third, post-filtering invites the fix that makes it catastrophic: someone notices results are thin and widens the search before filtering, and one day the filter is skipped on an error path.

Better than filtering, where your store supports it: physical separation. A namespace, collection, or index per tenant. Then cross-tenant retrieval is not a filter that could be omitted, it is a query against a different container entirely. Same principle as chapter eighteen — absence of capability beats restriction of capability.

On top of the tenant boundary, role and sensitivity filtering within a tenant. Not every operator should retrieve every document; a security procedure or an HR-related runbook may be restricted. This filter also belongs in the query, driven by the same identity you propagated through the tool executor last chapter. And it must be the requesting operator's identity, not the service's — the confused deputy problem applies to retrieval exactly as it applies to tools, and it is easier to get wrong here because retrieval feels like reading public documentation rather than accessing a record.

Then test it adversarially. Write a synthetic runbook in tenant B containing a distinctive phrase that appears nowhere else. Then, as a tenant A operator, submit an incident engineered to make that phrase maximally relevant — quote it, describe the exact scenario it covers. Confirm you get nothing. Confirm the attempt is logged. Make that an automated test that runs on every change, because this is a property that breaks silently during a refactor and you will not notice by using the system normally.

### Grounding and citations

Retrieval gets the right passages nearby. Grounding is making the output actually depend on them, and making that dependency visible.

Four mechanisms.

Supply passages with identifiers, clearly delimited, in a dedicated region of the prompt — the same single untrusted region discipline from chapter sixteen, because a retrieved document is content someone else wrote and is an injection vector.

Require citation in the output schema. The suggestion's rationale references the identifiers of the passages it relied on. Structural requirement, not a request.

Validate the citations. This is the step people skip and it matters: models fabricate citations. A cited identifier that was not in the set you supplied is a validation failure, and you should treat it as one — reject the response, count it, and log it. Verifying that the cited passage exists and was actually retrieved is cheap and it catches a real failure mode.

And require an insufficient-evidence result when retrieval is weak. Which means you must define weak, concretely. Options: no result above a similarity threshold; fewer than two results above it; a reranker score below a cutoff. Whichever you choose, calibrate it against your own corpus, because similarity scores are not comparable across models or domains and there is no universal good number. Run your fixtures, look at the score distribution for cases you know are answerable and cases you know are not, and put the threshold where they separate. Then revisit it when the corpus grows.

One honest caveat to give your customer. Citation proves the passage was supplied and referenced. It does not prove the passage supports the claim. A model can cite a real, retrieved, relevant-looking passage and still draw a wrong conclusion from it. What citation buys is that a human can check in five seconds instead of not at all — which is a large, real benefit, and it is smaller than "the answer is verified." Say the accurate version. The overclaim will be discovered.

### Retrieved documents are an injection channel

A security point that deserves its own section, because retrieval quietly widens the attack surface we discussed in chapter sixteen and it is easy to miss.

Until now, the untrusted content in your prompt was the incident description, written by an employee reporting a problem. Now you are also inserting document passages. Those passages were written by someone, edited by someone, and are stored somewhere that may be more loosely controlled than you assume. A wiki that anyone in the company can edit. A document imported from a vendor. A runbook a contractor wrote three years ago.

This is indirect prompt injection: the attacker does not interact with your system at all. They put text into a document, and wait for retrieval to deliver it into your model's context on someone else's behalf. It is harder to detect than direct injection because the malicious content arrives through a channel everyone considers trustworthy, and because the person who triggers it is an innocent operator.

So apply the same discipline. Retrieved passages go into the delimited data region, never the instruction region. They are labelled as reference material to be used as evidence, not as instructions. The output remains schema-constrained, so the blast radius stays bounded by what your suggestion type can express. And the architectural answer still carries the weight: a fully compromised model can produce a bad suggestion that an operator reads, and nothing else, because there is nothing else available to it.

Two additions specific to retrieval. Consider where your corpus comes from and who can write to it, and say so in your threat model — "anyone in the company can edit these pages" is a materially different risk posture from "these are published by a controlled process." And if your indexing pipeline can cheaply flag passages containing instruction-shaped language, do it at index time rather than query time; it is a weak signal, but catching it once during ingestion is far cheaper than checking on every retrieval, and it gives you something to show when someone asks how you handle this.

### When the customer's corpus is bad

Now a field reality that no tutorial prepares you for, and that you will meet on almost every engagement.

You will ask for the runbooks, and what you get will be some combination of: a wiki with four hundred pages, half of them last edited years ago; three documents that describe the same procedure differently; procedures that reference systems that were decommissioned; a folder of screenshots; and one genuinely excellent document written by someone who has since left.

This is normal. It is not a sign the customer is disorganized; it is what operational documentation looks like everywhere, and the reason it looks like that is that maintaining it has never had an immediate payoff.

Three things to do, in order.

First, measure it rather than complain about it. Count the documents, the distribution of last-revised dates, and the fraction that reference systems still in the service catalogue. That takes an afternoon and produces a slide that is often the most valuable thing you deliver in the first month, because nobody has ever looked. It also reframes the conversation: you are not asking them to do homework for your feature, you are showing them a finding about their own operation.

Second, scope the corpus honestly. Do not index everything. Pick the subset that covers the incident types in your pilot scope, with the customer choosing what is authoritative. A small curated corpus with known provenance produces a system operators trust; a large uncurated one produces confident citations of obsolete procedures, which is worse than no retrieval at all because it launders bad information through a system that looks authoritative.

Third — and this is the part that separates an FDE from an implementer — recognize that you have just created an incentive that did not exist before. Once retrieval is live, a well-maintained runbook visibly makes the copilot better at a job the team does every day. Documentation maintenance now has an immediate, felt payoff. Several teams I have seen improved their runbooks more in the two months after a grounded assistant went live than in the previous five years, not because anyone mandated it, but because the feedback loop finally closed.

That is worth naming explicitly in your pilot readout, because it is a benefit the customer did not buy and will not otherwise notice, and because it changes how they think about the deployment — from a tool they are evaluating to a thing their own work now feeds.

One caution to pair with it. Do not let the copilot become the reason a wrong document is trusted. Show the revision date, show the owner, make the citation a real link that opens the source, and make it easy for an operator to flag a passage as wrong from the suggestion screen. That flag, routed to the document owner, is a small feature with a disproportionate effect: it turns every triage into a possible documentation review, performed by the person best placed to notice the error.

### Freshness

Documents change, and a retrieval system that does not handle change is a system that confidently quotes a procedure that was replaced last quarter.

Four things to get right.

Update means reindex. When a document changes, its chunks are re-embedded and replaced. The trigger can be a webhook, a scheduled scan, or manual, but it must exist and it must be reliable — stale retrieval is the failure mode your operators will notice first and trust least.

Deletion means removal. When a document is deleted or access is revoked, its vectors must go. Orphaned chunks in a vector store are a real and common bug, and in a privacy context they are worse than a bug: content the customer believes is deleted is still being surfaced. Test deletion explicitly.

Revision date travels with the result and is shown to the operator. A citation that says a runbook was last revised four years ago is doing useful work — it tells the operator to be sceptical without your system needing to judge.

And a staleness policy, agreed with the customer. What happens to a document not revised in two years — is it excluded, downweighted, or flagged? There is no universally right answer; there is only a decision, made with the customer, written down. Often the most valuable output of this conversation is not the policy but the discovery that their runbook corpus is largely unmaintained, which is a finding worth more to them than your triage feature.

One architectural note carried forward from chapter fourteen: the vector index is a derived store. The document repository is the source of truth. You must be able to rebuild the index from scratch, and losing it should cost you time, not data. If deleting your index would lose something, you have put authoritative data in the wrong place.

### Choosing a store

Briefly, because chapter fourteen already taught the discipline.

Three options. A dedicated vector database, purpose-built, with strong performance at scale and rich filtering. A vector extension on the relational database you already run. Or a managed search or vector service from your customer's cloud provider.

The forward deployed default: if you already operate PostgreSQL, and your corpus is in the thousands to low millions of chunks — which covers essentially every runbook corpus you will meet — use the extension. The reasons are the same ones from chapter fourteen. One fewer datastore to deploy, secure, back up, monitor, and explain in a security review. Metadata and vectors in one place, so your tenant filter is an ordinary predicate enforced by the same database that enforces every other predicate, and your index update can be transactional with the metadata update. And your customer's platform team already knows how to operate it.

A dedicated store earns its place when scale genuinely demands it, when you need filtering or index features the extension lacks, or when the customer already runs one. Write the decision as an ADR, name the volume at which you would revisit it, and resist adding a datastore for a corpus that would fit comfortably in a table.

### Evaluating retrieval separately

The last idea, and the one I most want you to remember, because it will save you weeks.

When a grounded system gives a bad answer, most of the time the retrieval failed, not the generation. The right passage was not in the top results, so the model was reasoning without it. And here is why that matters: the symptom looks identical to a generation problem. The output is fluent and wrong. So teams spend days rewriting prompts to fix a retrieval failure, and nothing improves, because no prompt can reference a passage that was never supplied.

So evaluate retrieval on its own. Build a small set of queries where you know which passage should be found, and measure whether it appears in the top results. That single number tells you where your ceiling is. If the correct chunk is in the top five for sixty percent of queries, then sixty percent is the best your generation can possibly do on grounded questions, and every hour spent on the prompt is an hour spent below the ceiling.

This also gives you a fast, cheap, deterministic test loop. Retrieval evaluation needs no language model, costs almost nothing, and runs in seconds, so you can iterate on chunking, hybrid weighting, and reranking properly. It is the highest-return evaluation in the whole system, and it is the seed of chapter twenty-two.

Build it as part of this chapter's work, not later.

### Pitfalls

Eight.

Post-filtering for tenancy instead of filtering in the query. The one that becomes an incident rather than a defect.

Chunking that severs procedures mid-step, producing instructions that are wrong out of context.

Skipping metadata design and discovering you must reindex to add a field.

Pure vector search on text full of error codes and identifiers. Add keyword search.

Trusting citations without validating that the cited passage was actually retrieved.

No reindex or deletion path, so the system quotes replaced procedures and surfaces removed documents.

Changing the embedding model without a planned reindex, silently corrupting similarity.

Debugging generation when the failure was retrieval. Measure retrieval separately before touching the prompt.

### How you verify this chapter

Six checks.

One. Run the cross-tenant adversarial query. Nothing comes back, the attempt is logged, and this is an automated test that runs on every change.

Two. Take a retrieved chunk at random and read it cold. Can you tell what it is about and which procedure it belongs to without the surrounding document? If not, fix chunking, not the prompt.

Three. Force retrieval to return nothing above threshold. Confirm the system returns insufficient evidence and names what it looked for, rather than answering anyway.

Four. Fabricate a citation in a test response. Confirm validation rejects it.

Five. Update a runbook, reindex, and confirm the old passage no longer appears. Then delete a runbook and confirm the same.

Six. Run your retrieval evaluation and write down the number. If you do not know your recall, you do not know your ceiling, and you cannot tell whether your next change helped.

### The test project

The companion guide is a test. Attempt it before the hints.

Your goal is to ground the triage proposal in customer runbooks, with tenant isolation, citations, and a freshness path.

You will produce: a small set of synthetic runbooks across at least two tenants, each with owner, revision date, tenant, and access metadata; a chunking strategy that respects procedure boundaries and preserves heading context; an index with metadata, built so it can be rebuilt from source; retrieval filtered by tenant and role inside the query, driven by the operator's identity; hybrid search combining semantic and keyword results; passages supplied with identifiers into a single delimited region; required and validated citations; a calibrated insufficient-evidence threshold; an update-and-reindex demonstration and a deletion demonstration; and a retrieval evaluation set with a recorded recall number.

The constraints: retrieval never crosses the tenant boundary, and an adversarial query proves it. Workflow state is not confused with knowledge, and no learned memory is introduced. The index is derived and rebuildable. Citations are validated against what was actually retrieved. And a weak-retrieval case declines rather than guessing.

You are done when every grounded recommendation either points to a real retrieved passage or declines, when your adversarial cross-tenant test is automated and passing, and when you can state your retrieval recall as a number.

### Recap

The decision from this chapter: you gave the system the customer's knowledge through retrieval with citations, rather than through learned memory or a larger prompt.

The distinction: workflow state is a scratchpad, knowledge is the customer's authored content with a source you can point at, and durable learned memory is a commitment to keep small, human-curated, and out of the pilot.

The mechanics: embeddings turn meaning into proximity; chunk along the document's own structure and keep the heading context; design metadata before indexing because it drives filtering, citation, and freshness; keep the result count small.

The corrections: hybrid search, because operational text is full of exact tokens that vectors handle badly; reranking for precision; and a query built from structure rather than the raw description.

The hard requirement: tenant filtering inside the query or, better, physical separation — with role filtering driven by the operator's identity, and an automated adversarial test.

The honesty: citations are validated, weak retrieval declines, revision dates are shown, and you tell the customer what citation does and does not prove.

And the habit that saves weeks: measure retrieval separately, because it is your ceiling and because most bad answers are retrieval failures wearing a generation costume.

Next chapter we look at whether splitting this work across multiple specialized agents is worth the latency, cost, and coordination — and how to make two agents disagree in front of a human rather than fabricate a consensus behind one.
