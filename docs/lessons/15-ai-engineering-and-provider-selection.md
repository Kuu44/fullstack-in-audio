# Chapter 15 — AI engineering, LLM fundamentals, and provider selection

**Roadmap nodes covered:** AI Engineering Skills; AI Engineering; LLM Fundamentals; Choosing your Model Provider
**Part:** IV — Build AI behavior that can be controlled
**Companion test:** `docs/guides/15-ai-engineering-and-provider-selection.md`
**Audio:** `media/15-ai-engineering-and-provider-selection.mp3`

---

## Narration

Welcome to chapter fifteen. This is the first chapter of part four, and it is the chapter where FieldOps Copilot finally earns the second half of its name.

Let me remind you where the build stands, because everything we do from here depends on it. You have a delivery charter that names a real customer problem, a measurable outcome, and a set of non-goals. You have a React operator workspace with an intake form and an incident list. You have a Node service that validates incoming incidents, applies a priority policy in one authoritative place, and returns stable success and error shapes. You have PostgreSQL holding incidents, status changes, and immutable audit events, with an idempotency key so a retried intake does not create a duplicate. And you have one small expiring cache in front of a derived read model, with the database still holding the truth.

That is a real system. It is boring in the best possible way. Nothing in it guesses.

Today we add something that guesses, and the entire discipline of this chapter is about adding it without letting the guessing spread into the parts of the system that must not guess.

Here is the shape of the next thirty-five minutes. First, what AI engineering actually is as a job, and how it differs from the machine learning work people assume it means. Second, the language model fundamentals you genuinely need to reason about the system — tokens, context, sampling, structured output, and latency. Third, the inference interface itself and what it means that every call is stateless. Fourth, how to choose a model provider for an enterprise customer, which is a procurement and risk decision at least as much as a quality decision. Fifth, how to build the seam in your code so the choice stays reversible. Then the pitfalls that catch competent engineers, how you verify you did this well, and the test project.

Let us start with the job.

### What AI engineering is, and what it is not

There is a persistent confusion about what the phrase "AI engineering" names, and it costs teams real money, so let us clear it out first.

Machine learning engineering is the discipline of producing a model. You gather and label data, you choose an architecture, you train, you measure against a held-out set, you tune, you retrain when the data drifts. The artifact you ship is weights. The hard parts are data quality, training infrastructure, and the statistics of generalization.

AI engineering, as the term is used in the roadmap you are working through and as the industry now uses it, is the discipline of building a reliable product on top of a model you did not train and cannot fully inspect. You do not own the weights. You own everything around them. The artifact you ship is a system: the instructions sent to the model, the context assembled for it, the tools it is allowed to call, the schema its output must satisfy, the validation that rejects bad output, the fallback when the provider is slow, the evaluation suite that catches regressions, the traces that let you explain a bad answer three weeks later, and the human approval step that keeps the whole thing inside the customer's risk appetite.

I want to put a number on that, roughly, because it reframes how you spend your time. In a working enterprise deployment, the call to the model is one small function. The retrieval, the schema enforcement, the guardrails, the audit trail, the evaluation harness, the cost controls, and the operator interface are the product. If you find yourself spending most of your delivery time fiddling with model choice and phrasing, and almost none on the surrounding system, you are building a demo, and a demo is exactly the thing that fails its first week in the field.

So here is the working definition I want you to carry: AI engineering is the practice of making a probabilistic component safe to depend on. Everything in part four of this course is an instance of that sentence.

And the forward deployed framing sharpens it further. You are not selling a model. You are not even really selling an AI feature. You are selling a measurable improvement to a customer workflow — in our case, faster and more consistent incident triage with a clear audit trail. If a deterministic rule achieves that, use the rule. The model is a tool you reach for when the task involves reading messy human language, when the rules would be unmanageably numerous, or when the useful answer is a judgment rather than a computation. Incident triage qualifies on all three counts, which is why it is a fair example — but notice that we had to argue for it rather than assume it.

### The fundamentals you actually need

Now the model itself. I am going to give you the mental model that makes the engineering decisions obvious, and skip the parts that are interesting but do not change what you build.

Start with tokens. A language model does not read characters and does not read words. It reads tokens, which are fragments of text produced by a tokenizer — often something like three quarters of an English word on average, so a rough conversion is that a hundred words is around a hundred and thirty tokens. That ratio is not a law. Common English prose tokenizes efficiently. Technical identifiers, long hostnames, stack traces, base sixty-four blobs, and non-English text tokenize much worse, sometimes at one token per character. This matters directly to you because your incident descriptions will contain log excerpts and service names, and your token estimate based on prose will be wrong by a large factor if you do not account for that.

Tokens are the unit of three things you care about: the limit, the cost, and the time. Every one of those scales with token count, so token discipline is not accounting hygiene, it is architecture.

Second concept: the context window. This is the maximum number of tokens the model can consider in a single call, and it is shared between everything you send and everything it generates. Your system instruction, the incident text, any retrieved runbook passages, any prior turns you chose to include, and the model's own response all live in that one budget. When you hear that a model has a very large context window, resist the instinct to fill it. There are three reasons. Cost scales with what you send. Latency scales with what you send. And attention quality is not uniform across a long context — models reliably attend better to material near the beginning and near the end of a long input than to material buried in the middle. If the decisive sentence for your triage is in the middle of forty pages of pasted runbook, you have made the model's job harder, not easier, and you have paid extra for the privilege.

The engineering consequence is one you will apply repeatedly in this part of the course: send the smallest sufficient context, deliberately ordered, rather than everything available. Chapter twenty, when we build retrieval, is essentially an entire chapter about earning the right to send less.

Third concept, and the one that trips up engineers coming from deterministic systems: what the model is actually doing. At each step it produces a probability distribution over possible next tokens, and then something samples from that distribution. The sampling parameters — temperature being the common one — control how much the sampler favours the highest-probability token versus exploring alternatives. Low temperature makes output more repetitive and more predictable. High temperature makes it more varied.

Two things follow that you must internalize.

The first is that low temperature is not determinism. Even at the lowest setting, you may see different outputs for identical inputs, because of floating point non-associativity in batched inference, because the provider routes you to different hardware, and because the model behind a friendly name can be silently updated. Any test you write that asserts an exact string from a live model is a test that will fail for reasons unrelated to your code. This is why chapter twenty-two exists, and it is why the fake implementation you build today is not a shortcut — it is the only way your unit tests stay meaningful.

The second is that hallucination is not a defect that better prompting eliminates. The model is producing plausible continuations. When the training data supports the continuation, plausible and true coincide. When you ask about your customer's internal escalation policy, which appeared nowhere in training, plausible and true come apart, and the model will still produce something fluent and confident. Fluency and confidence are properties of the generation process, not evidence about correctness. Every mitigation we build in this part of the course — retrieval with citations, structured output, schema validation, an explicit insufficient-evidence path, human approval — exists because of this one property.

Fourth: model families and what they are tuned for. A base model completes text. An instruction-tuned model has been further trained to follow directions and behave conversationally, and that is what you will almost always use. A reasoning model spends additional inference time generating intermediate deliberation before its final answer, which buys accuracy on multi-step problems at real cost in latency and tokens. Multimodal models accept images or audio alongside text. Smaller models in a family are dramatically cheaper and faster and are often entirely adequate for constrained classification-shaped tasks — which, if you look honestly at our triage task, is most of what we are asking for.

Hold that thought, because it becomes the core of chapter twenty-three: the biggest model is rarely the right default, and you will not know which is right without a task-specific comparison.

Fifth: structured output. Left alone, a model returns prose. Prose is unparseable in any way you would want to depend on. Every serious provider now offers some form of constrained generation — you supply a schema, and the decoder is restricted so the output conforms to it. Use it. Not because it makes the content correct, but because it converts "the model said something weird" from a parsing crash into a validation failure you can detect, count, log, and fall back from.

And then validate anyway, on your side, after the fact. Schema conformance guarantees shape, not sense. A response can be perfectly well-formed and name a category that does not exist in your customer's taxonomy. Your adapter checks that the category is a member of the allowed set, that the confidence value is in range, that required fields are non-empty. A response that fails your check is not a triage suggestion — it is an error, and it should be handled as one.

Sixth and last of the fundamentals: the shape of latency. Two numbers matter and they behave differently. Time to first token is how long you wait before anything comes back — it is dominated by queueing, by your input length, and by the provider's current load. Then there is generation speed, tokens per second, which is roughly linear in how much output you asked for. Total latency is therefore driven heavily by output length, which is a lever you control. Asking for a terse structured suggestion instead of a chatty explanation is not just a cost decision, it is a latency decision, and in an operations tool where someone is staring at a screen during an outage, latency is a usability decision too.

Streaming — delivering tokens as they are produced — improves perceived latency substantially for conversational interfaces. For our triage case it is less useful than you might think, because we want a validated structured object, and you cannot validate half an object. Know the option exists, and note that it interacts badly with strict schema validation.

That is the whole fundamentals set. Tokens, context, sampling, families, structured output, latency. Everything else you will learn as you need it.

### The inference interface and what stateless really means

Now, briefly, the interface you actually call, described in terms of behaviour rather than syntax, because I am not going to read request formats aloud.

You send a request containing a sequence of messages with roles. There is typically a system role carrying your standing instructions — who the model is acting as, what it may and may not do, what output shape is required. There are user roles carrying the actual task content. There may be assistant roles carrying prior model turns. You also send parameters: which model, the sampling temperature, a maximum output length, and often a schema or tool definitions. You get back generated content plus usage numbers telling you how many input and output tokens were consumed.

The single most important property of this interface: it is stateless. The provider remembers nothing between calls. Every apparent conversation is you resending the entire history each time. This has three consequences that engineers reliably discover the expensive way.

Cost grows superlinearly across a long conversation, because turn ten resends turns one through nine. A chat that feels cheap per message can be very expensive by the end.

Memory is your responsibility, entirely. There is no provider-side session to rely on. What the model "knows" in a given call is exactly what you put in that call. Chapter twenty is about building that deliberately.

And context contamination is a real failure mode. If turn three contained a wrong assumption, and you keep resending turn three, the model keeps conditioning on the wrong assumption. Long-running agent loops degrade this way and it looks mysterious until you remember the statelessness.

Alongside the shape of the call, three operational realities. Rate limits are usually enforced on two axes at once, requests per minute and tokens per minute, and the token axis is the one that surprises teams — a small number of very large requests can exhaust your quota while your request count looks fine. Failures are normal: transient overload responses are routine at scale, and you need retry with exponential backoff and jitter. And retries cost money, because a retried call is a fully billed call, so an unbounded retry loop against a struggling provider is a mechanism for converting an outage into an invoice.

One more, and it is the one that hurts most in a customer deployment: model lifecycle. Provider model names are frequently aliases that point at a moving target, and specific versions get deprecated and retired on published schedules that are shorter than enterprise procurement cycles. If your customer's system pins a friendly alias, the behaviour of your deployed product can change without any deployment on your part. Pin specific versions when the provider allows it, record the version with every recommendation, and put model deprecation on the operational risk list you hand to the customer. We will formalize that in chapter twenty-six when we build a release manifest.

### Why the forward deployed engineer cares

Let me now connect all of this to the field, because the fundamentals are common knowledge and the framing is what distinguishes an FDE.

You are going to sit in a room with an operations director, a security lead, and someone from the platform team. The operations director wants triage to be faster. The security lead wants to know where incident text goes and who can read it. The platform team wants to know what they will be operating at three in the morning and who they call when it breaks.

Nobody in that room cares which model you chose. They care about four things, and you should be able to answer all four in plain language.

Where does our data go, who processes it, in which country, for how long, and is it used to improve someone's model? That is the data boundary question and it is usually the one that decides the deal.

When it is wrong, what happens? That is the autonomy question. The answer that makes people comfortable is that a wrong answer produces a rejected suggestion and a log line, not a closed ticket or a page to an on-call engineer at two in the morning.

What does it cost to run, and can that cost surprise us? That is the budget question, and "it depends on usage" is not an acceptable answer without a per-unit estimate and a ceiling.

What happens when the provider is down? That is the continuity question, and the acceptable answer is that the queue keeps accepting incidents, operators triage manually as they do today, and nothing is lost.

Notice that three of the four are not about model quality. That is not because quality does not matter — it does, and we will measure it properly in chapter twenty-two. It is because quality is the dimension the customer can evaluate themselves once the other three are satisfied, and it is the dimension where your opinion carries the least weight compared to their own eyes on their own incidents.

There is a failure pattern I want to name because it is so common. An engineer arrives at a customer site excited about a capable new model, builds a compelling demo in two days, shows it, and gets enthusiastic buy-in from the operations team. Then security asks where the data goes, and the answer involves a vendor with no agreement in place and no regional processing guarantee. The pilot stalls for months, or dies. The technical work was fine. The sequencing was wrong. In the field, the data boundary question comes before the quality question, because the data boundary question can invalidate all the quality work and the quality work cannot rescue a failed data boundary.

### Choosing a provider: the dimensions that decide it

So let us build the scorecard properly. There are eight dimensions. I will go through each with what to actually look for.

Data handling. This is first for the reason I just gave. You need explicit answers on: whether inputs and outputs are used for training, what the retention period is for logged requests and whether zero-retention is available, which subprocessors are involved, in which regions processing physically occurs, what the deletion process is, and whether the vendor will sign the customer's data processing agreement. Get these from contractual documents, not from a marketing page and definitely not from the model itself. Write the answers into your scorecard as quotations with dates, because these terms change and your customer's security team will ask you to re-confirm.

Deployment surface. This is where FDE work diverges most from hobby work. The same model family is often available three ways: directly from the model vendor, hosted inside a hyperscaler's AI platform, or as open weights you run yourself. These are wildly different products from a procurement perspective even when the weights are identical. If your customer already has an enterprise agreement, an identity integration, a private network path, and a billing relationship with one cloud, then reaching the model through that cloud may turn a three-month vendor review into a one-week change request. That is often worth more to the delivery timeline than a modest quality advantage elsewhere. Self-hosting open weights buys you maximum data control and predictable cost at high volume, and costs you hardware, capacity planning, and an operational burden the customer's platform team must actually agree to carry. Do not propose self-hosting unless somebody has said yes to operating it.

Task quality. Not leaderboard quality. Public benchmarks measure aggregate performance on academic tasks and are contaminated by training data in ways nobody can fully audit. They are a weak prior for "can this model correctly categorize a terse, misspelt, jargon-dense incident report from this specific customer." Build a small comparison set — a dozen or two synthetic incidents that look like the real ones — and run every candidate against it. This is the seed of your evaluation suite in chapter twenty-two, so the work compounds. And measure the thing you actually need, which for us is structured field accuracy and calibration, not eloquence.

Latency and throughput. Measure from where the service will run, not from your laptop, and measure the percentile that matters rather than the average. An operator waiting during an outage notices the slow tail, not the median. Also check what quota you can actually get: published rate limits for a new account are often far below what a pilot needs at peak, and raising them can take days.

Cost model. Input and output tokens are priced differently, usually with output several times more expensive. Many providers now price cached input tokens at a steep discount, which rewards putting your stable instructions at the front of the prompt where they can be cached. Some offer large discounts for asynchronous batch processing, which is useless for interactive triage and excellent for bulk backfill. Build your estimate per triage: expected input tokens, expected output tokens, expected retry rate, multiplied by the customer's expected daily volume and peak. Then multiply by something like three, because first estimates are always low, and present a range with its assumptions rather than a single confident number.

Reliability and operational maturity. Look at the public status history, not just today's green dashboard. Look at how incidents are communicated. Look at the deprecation policy and typical notice period. Ask what support tier is available and what the response commitment is — for an enterprise pilot, being able to reach a human during an incident has real value.

Compliance and contracts. Which certifications exist, is there a data processing agreement, are regional processing commitments contractual or best-effort, and what are the terms on indemnity and acceptable use. Your customer's legal and procurement teams will ask. Having the answers in your pack before they ask is a meaningful part of how an FDE earns trust.

Fallback. Every one of the above assumes the provider works. Decide now what happens when it does not. Options in descending order of ambition: a second provider behind the same interface, a smaller model from the same provider, a deterministic rule-based suggestion, or a clean degradation to manual triage with a clear operator message. For a pilot, the last two are perfectly respectable, and writing the choice down is more important than which one you pick. What is not respectable is discovering the answer during a customer-visible outage.

One synthesis point before we move on. Weight these dimensions against the charter, not against your preferences, and write the weights down before you score. If you score after deciding, you will produce a matrix that justifies the decision you already made, and everyone in the room will be able to tell.

### Building the seam so the decision stays reversible

Now the code shape, described architecturally.

You are going to define a port — an interface — in your domain layer. And the critical design decision, the one this chapter really turns on, is what that interface is shaped like.

The tempting shape is a generic one: something that takes messages and returns text. It feels flexible. It is a trap, because it leaks the vocabulary of language models into your domain and makes every caller responsible for prompts, parsing, and validation. You will end up with prompt fragments scattered across your service.

The right shape is domain-shaped. Something named for what your product does: take an incident, return a triage suggestion. The input is your existing incident type — the one already shared by your API and your React workspace, from chapter nine. The output is a new domain type describing a suggestion: a suggested category drawn from a fixed set, a suggested urgency with a short rationale in plain language, a list of specific missing pieces of information an operator should collect, a confidence signal, and provenance fields recording which model version and which instruction version produced it. And, importantly, an explicit way to express insufficient evidence, so that "I do not know" is a valid, representable, first-class answer rather than something the model has to fake.

Everything language-model-specific lives behind that port, inside the adapter. Prompt construction, the provider call, retries, timeouts, schema handling, token accounting, mapping provider errors onto your domain errors. Nothing above the port knows a model exists.

That boundary is what makes your provider decision reversible, and reversibility is the actual deliverable of this chapter. You will not get the provider choice right the first time. The customer's security review will come back with a constraint. A price will change. A better-fitting model will ship. If swapping providers means touching your incident service, your controllers, and your tests, you will not swap, and you will quietly ship the wrong thing for the rest of the engagement.

Then build two implementations.

The first is a deterministic fake, and I want to be emphatic that this is not a stub you throw away. It is the implementation your automated tests run against, forever. It returns fixed, sensible suggestions for known inputs, and it can be told to return an insufficient-evidence response, a malformed response, a slow response, and a failing response, so you can test every branch of your handling. Writing the fake also forces you to specify the contract precisely before any provider-specific detail can muddy it. If you find the fake hard to write, your contract is underspecified — fix that before you write the real adapter.

The second is one real adapter, called only with synthetic incident data, or not called at all yet if credentials are not approved. And that constraint is not bureaucratic caution. Pasting one real customer ticket into an unapproved vendor endpoint is a data transfer to a third party that your customer has not agreed to. It is the kind of thing that ends engagements and, depending on jurisdiction and data type, the kind of thing that is reportable. Generate synthetic incidents that are structurally realistic — same field shapes, same jargon density, same messiness — and use those. You should be able to do essentially all of this chapter's work, and most of the next several chapters, on synthetic data alone.

Two more design notes on the adapter. Set an explicit timeout that is shorter than your operator's patience, and decide what happens when it fires — do not let a provider hang inherit your HTTP request's default timeout. And record usage on every call: input tokens, output tokens, model version, instruction version, latency, outcome. You will need all of that in chapter twenty-three, and retrofitting telemetry after the fact is much harder than emitting it from the first call.

### The bounded task, stated precisely

Let me now state the task boundary for FieldOps Copilot, because getting this sentence right is most of the safety work in part four.

The model may suggest a category from a fixed list. It may suggest an urgency level with a short rationale. It may list specific information that appears to be missing from the report. It may say it has insufficient evidence.

The model may not change an incident's status. It may not close, escalate, reassign, or notify. It may not create records. It may not decide priority — priority remains computed by the deterministic policy you wrote back in chapter two and made authoritative in chapter eleven. The suggestion sits alongside the record as a proposal, attributed and versioned, until a human accepts or rejects it.

Now, the reasoning behind that boundary, because you will have to defend it and "we are being careful" is not a defence.

Use the reversibility test. Sort every candidate action by how hard it is to undo. Displaying a suggestion is trivially reversible — the operator ignores it. Writing a suggested category into a draft field is reversible with an edit and an audit entry. Closing a ticket is poorly reversible; the customer's reporter has already been told their problem was handled. Paging an on-call engineer is completely irreversible; you cannot un-wake someone, and a few false pages will destroy trust in the whole system faster than any quality problem. Autonomy is appropriate in inverse proportion to irreversibility, and until you have evaluation evidence over a real period, the honest position is that only the trivially reversible actions are earned.

There is a second reason, and it is about how adoption actually works. An operations team that has been told a system will make decisions for them starts from suspicion. A team that has been told the system will draft a suggestion they can accept in one click starts from curiosity. The second framing gets you usage, usage gets you evaluation data, and evaluation data is the only honest basis for ever expanding autonomy later. Starting bounded is not just safer, it is the faster path to a system that is allowed to do more.

Write the boundary into the charter, in the customer's words, and get someone on the customer side to agree to it out loud. That sentence will be quoted back at you in the security review, and you want it to be a sentence you wrote deliberately.

### Pitfalls

Eight of them. These are the ones I have watched competent people walk into.

Benchmark shopping. Choosing on a leaderboard and discovering the model is mediocre on terse operational language full of internal acronyms. Mitigation: a small task-specific comparison set, built before you choose.

Silent lock-in through prompt tuning. You spend two weeks tuning instructions against one model's quirks, and now switching means redoing that work, so the "provider-agnostic interface" is agnostic in structure only. Mitigation: keep instructions as close to plain task description as you can, keep the fixture set portable, and periodically run a second model against it so you know your actual switching cost.

Testing against the live model. Flaky tests, slow suites, and a bill from continuous integration. Mitigation: the fake is the default in tests; live calls happen in a separate, explicitly invoked evaluation run.

Assuming the version is stable. An alias moves and behaviour changes with no deploy from you. Mitigation: pin versions, record the version on every recommendation, monitor deprecation notices, and tell the customer this risk exists.

Context stuffing. Sending everything available because the window allows it, then paying for it in cost, latency, and degraded attention. Mitigation: smallest sufficient context, measured.

Secrets and sensitive content in the prompt. Someone pastes a config file into an incident description and it goes straight to a third party. Mitigation: treat the prompt as an egress boundary. Redact before sending, not after logging. We will formalize this in chapters thirty-one and thirty-two, but start the habit now.

Unbounded retries. A provider degrades, your retry loop hammers it, and you get a large bill and no answers. Mitigation: bounded retries with backoff and jitter, a circuit breaker, and a defined fallback.

Confidence theatre. Asking the model for a confidence score and treating it as calibrated probability. Self-reported confidence from a language model is weakly correlated with correctness and is systematically overconfident. Use it as a coarse triage hint at best. Real confidence comes from evaluation over a fixture set, which is chapter twenty-two.

### How you verify this chapter

Five checks. These are behavioural, not aesthetic.

One. Delete your real adapter entirely and run the full test suite. Everything passes, because tests run against the fake. If anything fails, your abstraction leaked.

Two. Write, by hand, the list of files you would touch to switch providers. If that list includes anything outside the adapter and its configuration, the seam is in the wrong place.

Three. Read your scorecard and check that every cell contains evidence — a figure, a quoted contractual term with a date, a measured latency, a source — rather than an adjective. "Good quality" is not a scorecard entry. If someone else can reach a different conclusion from the same evidence, that is fine, but they should not be able to say the evidence is missing.

Four. Confirm the fallback is written down and that you have actually exercised it. Force the adapter to fail and watch what the operator sees. If they see a spinner or a stack trace, you have not finished.

Five. Search your own history for any real customer data that left the building. Not a policy statement — an actual check of what you ran. If the answer is not a confident no, say so now rather than later.

And one judgement check that is not a test: can you explain the model boundary to a non-engineer in under a minute, without using the word "model"? Something like: the system reads the report and drafts a suggested category and urgency with its reasoning, flags what information is missing, and an operator decides. It never changes the ticket or notifies anyone on its own. If you can say that cleanly, you understand your own design.

### The test project

Now the practice work. The companion guide is a test, not a tutorial — it states the goal, the constraints, the starting state, the artifacts, and the rubric, with hints only at the very end. Attempt it before you read the hints.

Your goal is to add an AI triage recommendation seam to FieldOps Copilot without any part of the existing system depending on a specific provider, and to produce a documented, evidence-backed provider decision.

Four artifacts. First, a written task boundary: the exact permitted outputs and the explicitly prohibited actions, in the charter, in language a customer stakeholder would accept. Second, the port and its domain types in your service, with a deterministic fake implementation that can produce a good suggestion, an insufficient-evidence suggestion, a malformed response, a timeout, and a hard failure — plus tests covering all five. Third, a provider scorecard comparing at least two real candidate options across the eight dimensions, with weights fixed before scoring, a stated decision, and a named fallback. Fourth, either one real adapter exercised only with synthetic incidents, or a written statement of what approval is outstanding and what you did instead.

Constraints. No real customer data leaves your environment. The incident service does not import anything provider-specific. Priority stays deterministic. The suggestion is stored as a proposal with model version and instruction version attached, and it never mutates incident state.

You are done when you can delete the real adapter and still have a green test suite, when your scorecard would survive a security reviewer reading it, and when an operator looking at the workspace can tell the difference between what the system computed and what it merely suggested.

### Recap

The one decision from this chapter is this: you added a probabilistic component to a deterministic system by putting a narrow, domain-shaped, reversible boundary around it, and you chose a provider against the customer's constraints rather than against a benchmark.

The fundamentals that justify the design: tokens drive limit, cost, and latency together. Context is a budget you should underspend, not fill. Sampling means output varies, so exact-match tests against a live model are worthless. Hallucination is structural, so grounding, schemas, validation, and human approval are architecture rather than polish. The interface is stateless, so all memory is yours to build. And model versions move underneath you, so pin and record them.

The field discipline: the data boundary question comes before the quality question. Bound autonomy by irreversibility. Keep the seam narrow so the decision stays reversible. Never send real customer data to an unapproved endpoint, not even once, not even to check something quickly.

What you can do now that you could not before: specify a bounded AI capability precisely enough to test it, justify a model provider to a security reviewer, and build the abstraction that keeps that choice from calcifying.

Next chapter, we take the instructions we are sending to that model and treat them the way they deserve to be treated — as versioned production configuration, with change review, fixtures, and a rollback rule. Because right now, your prompt is the least governed and most behaviour-changing artifact in the entire system, and that is about to become a problem.
