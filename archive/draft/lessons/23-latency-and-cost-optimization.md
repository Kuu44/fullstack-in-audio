# Chapter 23 — Latency, inference, and cost optimization

**Roadmap nodes covered:** Latency and Cost Optimization; Inference Optimization
**Part:** IV — Build AI behavior that can be controlled
**Companion test:** `docs/guides/23-latency-and-cost-optimization.md`
**Audio:** `media/23-latency-and-cost-optimization.mp3`

---

## Narration

Welcome to chapter twenty-three, the last chapter of part four.

You have built something genuinely good. Bounded, grounded, cited, versioned, approval-gated, measured, and gated against regression. If you have followed the practice work, you have a system you could honestly put in front of an enterprise security reviewer.

Two questions remain, and they are the ones that decide whether it gets used.

Will an operator, standing in front of a screen during an outage with their manager asking for updates, wait for it? And can the customer afford to run it at the volume they actually have, including on their worst day?

If either answer is no, everything in the last eight chapters is a very well-engineered thing that nobody uses. Adoption dies on latency. Renewal dies on cost.

The plan: why you set budgets before you optimize. How to measure the whole path, and what your first measurement will probably tell you. The latency levers in order of return. The cost levers, including the one cache mistake that will bite you. Model routing done safely. Timeouts, the degradation ladder, and what the operator sees when you give up. The rule that protects quality. And forecasting for the customer. Then pitfalls, verification, the test project, and a look back across part four.

### Set the budget first

A budget is a requirement, not an outcome. If you do not state one, "fast enough" and "cheap enough" are opinions, and you will discover the real requirement when someone complains.

So write three numbers into the delivery charter, agreed with the customer.

A latency target, expressed as the ninety-fifth percentile, end to end, from the operator's click to a usable result on their screen. Not the model call — the whole thing, including your API, retrieval, validation, persistence, and rendering. The percentile matters because averages hide the tail, and the tail is what people remember. If the median is two seconds and one request in twenty takes fifteen, the system feels unreliable, not fast.

How do you choose the number? Not by asking what is achievable. By looking at the workflow. What is the operator doing before and after? If they are triaging a queue, and each item currently takes them forty seconds of reading, then a three-second suggestion that saves twenty seconds of reading is a clear win and nobody will mind. If they are on a call with a reporter, three seconds of silence is uncomfortable and you need either speed or something to show during the wait. Go and watch the work, or ask someone who has. The number comes from the job, not from the technology.

A cost ceiling per triage, and a monthly total at expected volume. Plus a peak scenario, because incidents arrive in bursts — a major outage generates a hundred reports in ten minutes, and that is precisely when the system is most valuable and most expensive. Then decide what happens at the ceiling: degrade, queue, or stop. That decision belongs to the customer, not to you, and asking them is a much better conversation than sending an unexpected invoice.

And a quality floor, which is the number people forget. Your evaluation baseline from last chapter. The optimization must not take quality below it. Without this, every optimization is technically successful, because you can always make something faster and cheaper by making it worse.

Three numbers. Latency at the ninety-fifth percentile, cost per triage with a monthly total, and the quality floor. Write them down before you touch anything.

Let me make the budget concrete with a worked example, because abstract advice about budgets produces abstract budgets.

Suppose you sit with the operations lead and watch the queue for an hour. Operators work through incidents one at a time. Reading and categorizing a typical report takes them thirty to fifty seconds. They are not usually on a call while doing it, but during a major outage they are, and that is when the queue is longest.

From that you can derive a budget rather than invent one. Normal triage: anything under about four seconds at the ninety-fifth percentile is invisible, because it is well under the reading time they were going to spend anyway. During an active outage with someone on the phone, the tolerance drops sharply — call it two seconds before silence becomes awkward, and note that you may not be able to meet it, in which case the answer is partial results rather than speed. So the budget becomes: four seconds at the ninety-fifth percentile, with something useful on screen within one second.

Now cost. They handle roughly four hundred incidents a week, with bursts to a hundred and fifty in an hour during a major outage. If a triage costs three cents, that is about twelve dollars a week, fifty a month — which nobody will notice. If it costs thirty cents because you routed everything to a large model with five thousand tokens of context, it is five hundred a month, which is a line item someone will ask about, and during a bad month with retries and bursts it could be twice that. So the ceiling gets set somewhere with room above the estimate but low enough to be a real constraint, and the peak scenario gets a per-tenant rate limit behind it.

Notice what that process did. It produced numbers from the work rather than from the technology, it made the outage case explicit as a separate and harder requirement, and it gave you a specific target to design against. Ninety minutes with a customer produces better requirements here than any amount of reasoning at your desk.

### Measure before you optimize

Now instrument the whole path, because you cannot optimize what you have not attributed.

Spans you need: request receipt, authentication and scope resolution, deterministic screening, query construction, embedding, vector search, keyword search, result fusion, reranking, prompt assembly, the model call broken into time-to-first-token and generation, each tool call, output validation, persistence, and response rendering.

Alongside timing, cost telemetry on every model and embedding call: input tokens, cached input tokens if your provider reports them separately, output tokens, reasoning tokens if applicable, the model and version, and the computed cost. You started recording some of this in chapter fifteen, which is why I told you to do it then.

And attribute everything to the run, the role, and the version tuple, so you can ask "which role got slower after which change."

Report percentiles — fiftieth, ninety-fifth, ninety-ninth — not averages. An average latency is a number that describes nobody's experience.

Now, what your first measurement will probably show you. I am going to predict, because these surprises are remarkably consistent.

The model call is not as dominant as you assumed. It is usually the largest single span, but often only half the total, with retrieval, validation, and your own serial code accounting for the rest. Teams that assume the model is everything spend weeks on prompt shortening and move the total by ten percent.

Your embedding call is a full network round trip you forgot about. Embedding the query is a separate provider call, and on a short query it can be a surprisingly large fraction of your latency because it is almost all round-trip overhead.

Your prompt is substantially larger than you think. The examples you added in chapter sixteen, the taxonomy with discriminators, the tool declarations, and five retrieved passages add up. Print the actual token count. It is usually two to three times the estimate.

Something you believed was parallel is serial. This is the most common finding and the cheapest fix.

And there are retries you did not know about, quietly doubling the cost of some fraction of requests.

Find these before you optimize anything. An afternoon of measurement routinely saves a week of work aimed at the wrong span.

### Latency levers, in order of return

Eight, roughly ordered by what they return for the effort.

First and best: do less. Every request that never reaches the model is instant and free. Your deterministic screening from chapter nineteen already does this — measure how often it fires. If a quarter of your intake is thin enough to be screened out, you have already cut a quarter of your cost and latency, and that number belongs in your customer report. Look for more of these. Does every incident need retrieval, or only those matching certain categories? Does a report that exactly duplicates one from five minutes ago need independent analysis?

Second: parallelize. Retrieval and classification are independent if your classifier does not see passages — which, after chapter twenty-one, it does not. Start them together. This is usually a small code change for a large win, and it is the fix for the "something serial that should not be" finding.

Third: reduce output tokens. Generation time is close to linear in output length, so this is the strongest lever on the model span itself. Look hard at your output schema. Is the rationale two sentences or a paragraph? Does the missing-information list need full sentences or short phrases? Is there a summary field nobody reads? Every field you remove is faster and cheaper on every single request, forever. And a shorter rationale is often a better rationale, because operators read short ones.

Fourth: reduce input tokens. Fewer retrieved passages, tighter chunks, trimmed examples. Be careful here — input reduction affects quality more readily than output reduction does, and dropping from five passages to three may cost you recall. Measure it against the evaluation set rather than assuming.

Fifth: route by model. A constrained classification from a fixed taxonomy does not need your most capable model. A small fast model is often several times faster and considerably cheaper, and on a well-specified constrained task the accuracy difference can be negligible. More on doing this safely in a moment.

Sixth: prompt caching. Most major providers now cache repeated input prefixes and charge much less for cached tokens, sometimes with a latency benefit as well. You get this nearly for free if your prompt is ordered stable-content-first, which is exactly how I asked you to build it in chapter sixteen. Check whether your provider reports cache hits, and check that you are actually getting them — a variable value accidentally placed early in the prompt will break caching for everything after it, and that is an easy and invisible mistake.

Seventh: perceived latency. Streaming helps conversational interfaces a lot and helps us less, because we want a validated structured object and you cannot validate half an object. But perceived latency has other levers. Show the retrieved runbook links as soon as retrieval completes, before the model finishes — they are useful on their own, and the operator has something to read. Show a specific progress indication rather than a generic spinner: "searching your runbooks," then "analysing." Both cost nothing and change the experience substantially.

Eighth: infrastructure. Run your service in a region close to your provider's endpoint. Reuse connections rather than establishing a new one per request. Avoid cold starts on a serverless runtime for a latency-sensitive path. These are small individually and they add up, and they are the ones to reach for after the others.

### Cost levers and the cache mistake

Tokens are cost, so most latency levers are also cost levers. Four additions.

Embedding caching. The same text gets embedded repeatedly — the same query shape, the same document chunk during a reindex that only changed one section. Embeddings are perfectly cacheable because the same text with the same model always produces the same vector. Key the cache on the text hash plus the embedding model identifier. This is cheap, safe, and often a meaningful saving during reindexing.

Retrieval result caching. Cache the retrieved passage identifiers for a normalized query, with a short expiry. Safe because it is derived data — chapter fourteen's discipline — and you can always rebuild it. Make sure the cache key includes the tenant and the requesting role's scope, or you will have built a cross-tenant leak in your cache, which is a genuinely embarrassing way to fail after all the care we took in chapter twenty.

Response caching. Tempting and mostly not useful, because free-text incident descriptions rarely repeat exactly. Where it does apply is duplicate intake — the same outage reported by six people in four minutes. But treat that as a deduplication feature at the incident level rather than a cache at the model level; it is more useful, more visible, and easier to reason about.

Batch processing. Providers often offer large discounts for asynchronous batch work with relaxed latency. Useless for interactive triage. Excellent for backfilling suggestions over historical incidents and for running your nightly evaluation suite, which after last chapter is a real recurring cost.

Now the cache mistake, and I want to be emphatic because it is subtle and the failure is silent.

Every cache key for anything derived from a model must include the full version tuple — prompt version, model version, embedding model, index revision. If it does not, then after you deploy a new prompt version, your cache will keep serving results produced by the old one. Your evaluation gate passed on the new version. Production is running the old one. And nothing is broken, nothing errors, nothing alerts — you simply are not running what you think you are running, and every conclusion you draw from production data is wrong until the cache expires.

I have seen this cost a team two weeks of confused investigation. Put the version tuple in the key. And on deploy, either invalidate or let the key change do it for you naturally, which is the elegant version: if the version is in the key, a new version simply has no cached entries and warms up on its own.

One more cost control: per-tenant rate limiting. It bounds your worst case, it protects other tenants from one tenant's burst, and it gives you a concrete answer to "what is the maximum this can cost us in a day," which is a question your customer's finance function will eventually ask.

### What is happening inside inference

A section on the machinery underneath, because the roadmap names inference optimization specifically, and because understanding it explains several provider behaviours that otherwise look arbitrary.

Generation has two phases with completely different performance characteristics. The prefill phase processes your entire input at once — it is highly parallel, it saturates the hardware well, and its time scales with input length. Then the decode phase produces output one token at a time, each token depending on the last, which is inherently sequential and leaves a lot of hardware idle. This is the structural reason output tokens cost more than input tokens almost everywhere: they are produced in the less efficient phase.

During decode, the model reuses the intermediate state computed for all preceding tokens rather than recomputing it. That stored state is what people mean by the attention cache, and it is large — it grows with context length and with concurrency, and it is usually the thing that limits how many requests a server can handle at once. Which explains something you may have wondered about: why long contexts degrade throughput so sharply on a busy service. It is not that the computation is much harder; it is that memory for cached state is the scarce resource and long contexts consume it greedily.

Providers extract efficiency through several techniques. Continuous batching interleaves many requests so that new ones can join a batch as others finish, rather than waiting for a whole batch to complete — this is why throughput at a provider is much better than what you would get running one request at a time yourself. Prefix caching stores the computed state for a repeated prompt prefix so it does not need recomputation, which is exactly the mechanism behind the discounted cached input tokens we discussed. Quantization reduces the numerical precision of the weights, cutting memory and increasing speed at some accuracy cost. And speculative decoding uses a small fast model to propose several tokens which the large model then verifies in one pass, accelerating decode when the small model guesses well.

Why does this matter if you are calling an API and never touching a GPU? Three reasons.

It explains the pricing. Output costs more than input because decode is less efficient. Cached input is cheap because prefill was skipped. Batch processing is discounted because relaxed latency lets the provider pack work efficiently. These are not arbitrary vendor choices; they reflect real costs, which means they are stable and worth designing around.

It explains the variability. Your latency depends on other people's load, because you share continuous batches with them. A ninety-ninth percentile much worse than your median is normal and is not your fault, which is worth knowing before you spend a day looking for a bug in your own code.

And it tells you what self-hosting would actually involve, which is the decision behind chapter twenty-six. Running open weights means owning batching configuration, memory management, quantization tradeoffs, capacity planning for peak concurrency, and GPU availability. At high sustained volume the economics can be compelling. At pilot volume they essentially never are, and the right answer is almost always to pay for someone else's saturated hardware. Knowing why lets you say so convincingly rather than defensively.

### Model routing done safely

Routing is the highest-value optimization available and also the easiest to do badly. Three rules.

Route by task shape, not by guess. A constrained choice from an enumerated taxonomy is a small-model task. Nuanced judgment over conflicting evidence is not. Split by the nature of the work, which is another argument for the role split from chapter twenty-one — once you have separate roles, routing them differently is trivial, and before you do, it is impossible.

Build an escalation route, and measure its rate. Run the cheap model first. If its output fails validation, or its confidence is low, or the case is flagged as ambiguous, escalate to the stronger model. This gives you cheap-model economics on the easy majority and strong-model quality where it matters. But the escalation rate determines your true blended cost, so measure it — if you escalate sixty percent of the time, you are paying for both models on most requests and you have made things worse. A route that escalates five percent of the time is a large win; one that escalates half the time is a loss dressed as a design.

Treat every route as a separate configuration with its own baseline. This is the rule people skip. The small model needs its own evaluation run, its own pass rates, and its own entry in the version tuple. Its prompt may need to differ — smaller models generally need more explicit instruction and benefit more from examples. And critically, check the safety cases on every route independently. Smaller models are often noticeably worse at declining when evidence is thin and worse at resisting injection attempts, which means a routing change can silently weaken exactly the properties you spent chapter eighteen and chapter twenty protecting. A route that is cheaper and faster and slightly worse at refusing is not an optimization, it is a regression you have not noticed yet.

### Timeouts, the ladder, and the fallback

Three nested deadlines. Each individual call gets a timeout. The whole run gets a deadline shorter than the sum of the call timeouts. And the operator's patience is the outer bound, which the run deadline must respect. If your run deadline is thirty seconds and your operator gives up at eight, the deadline is doing nothing.

Then a degradation ladder, defined explicitly rather than discovered under pressure. Four rungs.

Full path: retrieval, grounded analysis, citations, suggestion.

Degraded model: the cheaper route, with the result marked as produced by the fast path so nobody is misled about which configuration they are looking at.

Retrieval only: the model path failed or exceeded its budget, so show the screening result and the retrieved runbook links with their titles and revision dates, and say plainly that automatic analysis was unavailable. This rung is worth dwelling on, because it is genuinely useful and almost free. An operator handed three relevant runbook links in two hundred milliseconds is better off than an operator handed nothing, and arguably better off than one who waited twelve seconds for a synthesis. Many teams never build this rung and jump straight from full to nothing.

Manual: everything failed. The incident sits in the queue exactly as it would have without the copilot, with a clear message that automatic triage is unavailable. Nothing is lost, nothing is blocked. This rung is always available to you because you kept the AI as advice — which is the final dividend of the boundary we set in chapter fifteen.

And the rule for all of them: the operator always gets something, and they always know which rung they are on. A result that looks like a full analysis but came from the degraded route is worse than an honest degraded result, because it damages the calibration you worked to earn.

### Behaving well during a burst

One more operational case, because it is the one where all of this is tested at once.

A major outage produces a hundred and fifty reports in an hour, most of them describing the same thing. Three problems arrive together: your provider rate limit, your cost ceiling, and an operations team under maximum pressure.

Four responses, in the order I would build them.

Deduplicate before you analyse. Most of those reports are the same incident seen by different people. If you can group them — by affected service, by time window, by similarity — you analyse once and attach the result to the group. This is the biggest win by far, it reduces cost and latency together, and it is more useful to the operator than a hundred and fifty separate identical suggestions would be.

Queue with a concurrency limit rather than firing everything at the provider. Uncontrolled concurrency during a burst produces rate-limit rejections, which produce retries, which produce more rejections. A queue with a fixed concurrency below your quota converts a failure cascade into an orderly delay.

Shed load deliberately and visibly. When the queue is deep, drop to the retrieval-only rung rather than making people wait. An operator during a major outage would rather have runbook links immediately on everything than full analysis on the first twenty and nothing on the rest.

And degrade by policy, not by accident. Decide in advance what happens at the cost ceiling during a burst — continue at the cheap route, drop to retrieval-only, or stop and notify. Whichever it is, the operator should be told the system is in a degraded mode, because a system that quietly becomes less capable during the exact hour it is most needed is worse than one that says so.

The general principle: your worst hour is the hour your customer will judge the system by. Design for it explicitly, and rehearse it before it happens rather than discovering your behaviour during a real outage.

### The rule that protects quality

Say it plainly: no optimization ships without re-running the evaluation gate.

Every lever in this chapter is a quality risk. Fewer passages risks recall. A shorter rationale risks usefulness. A smaller model risks accuracy, calibration, and refusal behaviour. Aggressive caching risks staleness. Prompt trimming risks removing the instruction that was doing the work.

The optimization must not reduce the evaluation gate below its baseline. That is the acceptance criterion, and it is why chapter twenty-two came first. Without a gate, optimization is a series of plausible changes with no evidence, and the quality loss is invisible because it accumulates in small increments that each looked harmless.

Pay particular attention to two categories. The safety cases, because they are absolute and because cheap routes weaken them disproportionately. And the decline rate, because a system that stops saying "I do not know" has not got better, it has got bolder — and that shows up as improved apparent accuracy on some metrics while making the system less trustworthy in exactly the situations where trust matters.

### Forecasting for the customer

Finally, turning your measurements into something a customer can plan with.

Give them a per-triage cost with its assumptions stated: typical input size, typical output size, escalation rate, retry rate, retrieval cost. Then a monthly figure at their stated volume. Then a peak scenario.

Name the things that scale non-linearly, because these are what produce surprises. Retries during a provider degradation. Longer reports, since a customer that starts pasting full log excerpts can double input size overnight. More retrieved passages if someone tunes recall upward. Escalation rate drifting as the incident mix changes. Conversation length, if you ever add a follow-up interaction.

Present a range with its assumptions, not a single confident number, and say which assumption you are least sure about. And show the cost ceiling and what happens when it is reached, because the question behind the question is almost always "can this surprise us," and the reassuring answer is not a low number, it is a bounded one.

One framing worth offering. Compare the per-triage cost to the operator time it saves. If a triage costs a few cents of model spend and saves twenty seconds of a skilled operator's time, the ratio is not close, and putting it that way moves the conversation from cost to value. Be honest about the comparison — include your infrastructure and your ongoing engineering time, not just tokens — but make it, because a customer evaluating model spend in isolation has no frame of reference and will default to thinking it is expensive.

### Pitfalls

Eight.

Optimizing before measuring, and spending a week on a span that was fifteen percent of the total.

Omitting the version tuple from cache keys, and silently serving results from a retired prompt.

Routing to a cheaper model without evaluating that route independently, especially on the safety cases.

Building an escalation route and never measuring the escalation rate, so the blended cost is worse than the baseline.

Optimizing the average instead of the tail. The ninety-fifth percentile is what the operator experiences.

Removing the decline behaviour in pursuit of an accuracy metric, and mistaking boldness for improvement.

A degradation path that ends in a spinner or a stack trace instead of something useful.

A cache key that omits the tenant or the requesting scope, reintroducing a cross-tenant leak after all the care taken in chapter twenty.

### How you verify this chapter

Six checks.

One. Produce one request trace showing every span and its duration, plus tokens and cost per model call, and read it. You should be able to point at the largest contributor immediately.

Two. Compare your measured ninety-fifth percentile against the budget in the charter. If you have no budget, you have not started this chapter.

Three. Run the evaluation gate on every optimized configuration, separately, and confirm none is below baseline — with the safety cases at a hundred percent on every route.

Four. Force a model timeout with the workspace open and look at the screen. You should see the retrieval-only rung: screening result, runbook links, and an honest message.

Five. Deploy a new prompt version and confirm that no cached result from the previous version is served. Check by inspecting a response's recorded version, not by assuming.

Six. Measure the escalation rate on your routed configuration and compute the blended cost. If it is higher than the single-model baseline, the routing is not an optimization.

### The test project

The companion guide is a test. Attempt it before the hints.

Your goal is to set a latency and cost budget and meet it without dropping below your quality baseline.

You will produce: budgets in the charter — ninety-fifth percentile latency, cost per triage, monthly at expected volume, a peak scenario, and the quality floor. Instrumentation across the full path with per-span timing, token counts, and cost, attributed to run, role, and version. A comparison of a fast and cheap route against a higher-quality escalation route, evaluated separately on the same fixture set, with the escalation rate measured and the blended cost computed. At least one safe optimization implemented — embedding caching, reduced retrieved context, parallelized retrieval and classification, or prompt prefix caching — with before and after numbers. And a defined degradation ladder with the operator-visible result at each rung.

The constraints: a single trace shows where time and cost went. Every route is evaluated independently and no route falls below baseline, with safety cases absolute. Cache keys include the version tuple and the tenant scope. And the operator always receives something useful and always knows which rung produced it.

You are done when your trace explains your latency, when your optimized configuration passes the gate, and when an operator waiting on a failing provider gets runbook links in a fraction of a second rather than a spinner.

### Recap, and the end of part four

The decision from this chapter: you optimized against measured baselines and stated budgets, with an evaluation gate preventing you from buying speed with quality.

The order of operations: set the budget as a requirement, measure the whole path, then optimize the largest attributable span. Do less before you do it faster.

The levers: skip work entirely, parallelize, cut output tokens, cut input tokens carefully, route by task shape, exploit prefix caching through stable prompt ordering, improve perceived latency with partial results, and tune infrastructure last.

The traps: cache keys without a version tuple or a tenant scope, escalation rates that erase the saving, cheaper routes that quietly weaken refusal and injection resistance, and optimizing the average while the tail is what people feel.

And the ladder: full, degraded, retrieval-only, manual — each rung useful, each rung honest about what it is.

Now step back and look at what part four built. In chapter fifteen you put a narrow, reversible boundary around a probabilistic component and chose a provider on the customer's constraints. In sixteen you made the instruction a versioned, reviewable artifact with fixtures and a rollback rule. In seventeen you defined where assistance ends and ownership begins. In eighteen you gave the model its first contact with a real system as a request your code authorizes, executes, and audits. In nineteen you made the loop explicit, bounded, durable, and approval-gated. In twenty you grounded it in the customer's own knowledge with citations, tenant isolation, and an honest decline. In twenty-one you split by role only where it measured well, and kept disagreement visible to a human. In twenty-two you made every claim a number and put a gate in front of the ones that matter. And here you made it fast and affordable without giving any of that back.

The thread through all nine chapters is a single idea, and it is the one worth carrying into every AI system you ever deliver: the model is the least controllable part of your system, so every other part must be built to make its worst behaviour boring.

Part five moves the data and the model workflows — pipelines, orchestration, and the release discipline that ties a deployed recommendation to the exact configuration and evidence behind it. Your work here is what makes that possible, because a system you cannot version and cannot measure is a system you cannot responsibly promote.
