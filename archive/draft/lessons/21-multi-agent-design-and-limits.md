# Chapter 21 — Multi-agent design and delegation limits

**Roadmap nodes covered:** Multi-Agents
**Part:** IV — Build AI behavior that can be controlled
**Companion test:** `docs/guides/21-multi-agent-design-and-limits.md`
**Audio:** `media/21-multi-agent-design-and-limits.mp3`

---

## Narration

Welcome to chapter twenty-one.

FieldOps Copilot now has a single bounded agent. It screens deterministically, retrieves grounded evidence from the customer's runbooks with tenant isolation and validated citations, produces a structured suggestion with a reasoning path, declines when the evidence is thin, and waits for an operator to approve or reject.

The obvious next question, and the one you will be asked in a customer meeting within about a week of demonstrating it, is: should there be more than one of these?

This chapter answers that question honestly, which means the answer starts at no and has to be argued up. And then, if you do split, it shows you the one design decision that determines whether the split makes the system better or makes it confidently wrong.

The plan: what multi-agent actually means, since the term covers four quite different things. When a split genuinely helps — five real reasons. What it costs, stated numerically rather than vaguely. Our concrete split for FieldOps. Then the central idea of the chapter, which is about what a coordinator must never do. Then context isolation, correlation, delegation contracts, and measurement. Then anti-patterns, verification, and the test project.

### Four things called multi-agent

Let me separate these, because they have very different risk profiles and people argue past each other by mixing them.

The first is sequential decomposition: a pipeline where different steps have different instructions and different context. Extract, then classify, then summarize. Honestly, this is usually just a workflow with several model calls in it, and calling it multi-agent is mostly branding. It is also frequently good engineering, because a prompt doing one job is better at that job than a prompt doing four.

The second is parallel specialists: two or more roles look at the same problem from different angles at the same time, and their outputs are combined. This is what we will build.

The third is hierarchical delegation: a coordinator decomposes a task and assigns pieces to workers, possibly deciding at runtime how many workers and what they do. More powerful, considerably less predictable, and the coordinator's decisions are themselves model output.

The fourth is peer negotiation: agents exchange messages, argue, and converge. This is where most of the impressive demonstrations and most of the production disasters live. Free-text conversation between models is unbounded in length, unbounded in cost, difficult to evaluate, and produces agreement that looks like reasoning and frequently is not.

For enterprise field work: the first two are usable. The third needs a strong justification and hard limits. The fourth I would not deploy at a customer in a pilot, and I would be able to say why in one sentence — there is no stop condition you can trust and no way to evaluate the conversation.

### When a split genuinely helps

Five real reasons. If none of them applies, do not split.

Context isolation. This is the strongest reason and the most underrated. A single prompt asked to classify, assess urgency, check evidence, identify gaps, and detect duplicates is worse at every one of those than five focused prompts would be. The instructions compete for attention, the criteria for one task bleed into another, and the whole thing becomes impossible to change safely because every edit risks four other behaviours. Splitting by role is, more than anything else, a way of giving each job a clean, small context.

Different permission scopes. A role that reads runbooks does not need incident lookup. A role that classifies incident text does not need to touch the document store. If the roles are separate processes with separate tool sets, least privilege becomes structural rather than aspirational. This is the chapter eighteen principle applied at the agent level, and it is a genuinely good argument.

Genuine parallelism. If two independent pieces of work each take two seconds, doing them at once costs two seconds instead of four. This only helps when the work is truly independent — if the second role needs the first's output, you get the sum, not the maximum.

Different cost tiers. A cheap fast model can do a constrained classification perfectly well while a stronger model handles the harder judgment. Splitting lets you route each role to an appropriate tier instead of paying the top rate for everything. We will develop this properly next chapter.

Independent evaluation. This one is subtle and it is my favourite. If classification and evidence-checking are one call, you can only measure the combined output, and when quality drops you cannot tell which part regressed. Split them and each has its own fixtures, its own pass rate, and its own regression signal. That makes chapter twenty-two dramatically more useful.

Notice what is not on that list: "it seems more capable," "the demo is more impressive," or "agents are how this is done now." Those are not reasons.

### What it costs

Now the other side, stated concretely so you can weigh it.

Latency. Sequential roles add. Parallel roles cost the slowest plus coordination overhead. Either way you are adding, and for an operations tool used during an outage, seconds are not free.

Cost. Two roles is at least two calls. Worse, context is often duplicated — both roles need the incident text, so you pay for it twice. A naive two-role split can easily cost more than twice the single agent.

Failure modes multiply. With one agent you have success and failure. With two you have both succeed, either one fail, both fail, and the interesting case: both succeed but disagree. That last one is not an error and you must design for it.

Debuggability. A bad output now has two possible sources plus their combination. Without careful correlation you will not be able to say which.

Error compounding. If each role is independently right ninety percent of the time and you need both to be right, you are at eighty-one percent. Three roles, seventy-three. Decomposition does not automatically improve accuracy, and if the roles are dependent it can make it worse. This arithmetic is unforgiving and it is the reason long agent chains disappoint.

Coordination overhead. Something must combine the outputs. If that something is itself a model call, add its latency, its cost, and its failure modes to the total — and, as we are about to see, its own particular danger.

Let me make the arithmetic concrete, because "it costs more" is easy to wave away and a worked example is not.

Take the single agent. One call. Input: the instruction and criteria, perhaps eight hundred tokens; five retrieved passages, perhaps fifteen hundred; the incident text, three hundred. Call it twenty-six hundred input tokens. Output: a structured suggestion, maybe two hundred and fifty. One round trip, so latency is one time-to-first-token plus the generation of two hundred and fifty tokens.

Now the naive split. The classifier gets the instruction and criteria and the incident text: eleven hundred in, a hundred and fifty out. The evidence checker gets its own instruction, the passages, and the incident text: two thousand in, a hundred and fifty out. Total input has gone from twenty-six hundred to thirty-one hundred, because the incident text and a chunk of instruction are duplicated. Total output is slightly higher. If the roles run in parallel, latency is roughly the slower of the two rather than the sum, so you may come out even or slightly ahead there. If they run sequentially, you have roughly doubled it.

So the naive split costs perhaps twenty percent more in tokens, plus two sets of per-request overhead, for a latency outcome that depends entirely on whether you parallelized. That is the honest baseline before any quality benefit.

Now apply cost tiering, which is where splits start to pay. The classifier is a constrained choice from a fixed taxonomy — a small fast model handles it well. If the small model is several times cheaper per token, and it is handling eleven hundred of your thirty-one hundred input tokens, your blended cost can land below the single-agent baseline while latency improves, because small models also return faster. That is a real win, and notice it is a win that only exists because you split.

The point of the arithmetic is not the specific numbers, which will be different for your corpus and your provider. It is that the split's economics depend almost entirely on decisions you make after splitting — parallelism and model routing — and that a split made without those decisions is simply more expensive. Measure your own numbers; do not reason from mine.

### The FieldOps split

Here is what we will build, and I want you to notice how conservative it is.

Two specialists and a coordinator.

The incident classifier sees the incident text, the category taxonomy, and the urgency criteria. It does not see runbooks. It produces a suggested category, a suggested urgency with a rationale, and a list of missing information. This is essentially your existing triage prompt with the grounding removed — narrowed, not new.

The runbook evidence checker sees the incident text and the retrieved passages. It does not decide the category. It answers three questions: do the retrieved passages describe a known procedure that matches these symptoms; which specific passages; and does the evidence appear inconsistent with the classifier's proposed category. That third question is what makes this role worth its cost.

The coordinator is deterministic code. Not a model. It runs the two roles, applies its rules, and produces one object for the operator.

Its rules are simple. If both roles agree and the evidence is strong, present a single confident suggestion with citations. If the evidence checker found nothing above threshold, present the classification with an explicit note that no supporting procedure was found — which is useful information, not a failure. If the evidence checker flags an inconsistency, present both positions side by side and mark the suggestion as contested. If either role fails or times out, present whatever succeeded, clearly labelled as partial.

Notice what the coordinator never does: it never invents a resolution. It never averages two categories into a third. It never picks a winner based on a confidence number. When the specialists disagree, the disagreement is the output.

### Never fabricate consensus

This is the core of the chapter and I want to spend real time on it.

The tempting design is a model as coordinator. You give it both specialist outputs and ask it to reconcile them into a final answer. It works immediately. The output is smooth, single, confident, and easy to display.

It is also the worst thing you can build here, and here is exactly why.

A model asked to reconcile two positions will produce a reconciliation. That is what it does. It will produce one whether or not a genuine reconciliation exists, because producing fluent text that resolves a tension is precisely the capability it has. So when your two specialists genuinely disagree — when the classifier says network and the evidence checker found a facilities procedure matching the symptoms exactly — the model coordinator will write a confident paragraph that harmonizes them, and the operator will never learn that the system was uncertain.

Think about what that costs you. Disagreement between two independently-scoped specialists is an extremely valuable signal. It is the system telling you this case is hard. It is exactly the case where a human's judgment adds the most value, and it is exactly the case you most want surfaced. A model coordinator takes your highest-value signal and converts it into false confidence.

So state the rule as an architectural principle: disagreement is a first-class output, and it is routed to a human. The coordinator's job is to detect and present disagreement, not to resolve it.

There is a customer-trust argument here that I think is underappreciated, and it is worth making in a meeting.

A system that gives a confident answer and is wrong ten percent of the time trains operators to distrust all of its answers, because they cannot tell which ten percent. A system that gives a confident answer eighty percent of the time and says "these two analyses disagree, here is each one, you decide" the other twenty percent gets higher trust on the confident answers and provides genuine help on the hard ones. The second system is more useful even if its raw accuracy is identical, because calibrated uncertainty is what makes an assistant's confidence mean something.

Operations people understand this instinctively. They work with monitoring systems, and they know the difference between an alert that is usually right and an alert that is always confident. Tell them your system will say when it is unsure, and show them that it does, and you will get adoption that a more confident system would not earn.

One refinement. Presenting disagreement must not become presenting confusion. The operator should see a clear structure: here is the proposed classification, here is the evidence found, here is the specific point of tension, here is what each position implies, and here are your options. Not two paragraphs of competing prose. Structure the disagreement as carefully as you structure the agreement.

And a related trap: do not reach for voting. Three roles, majority wins, sounds robust. It is much weaker than it appears, because the errors are correlated — the same model family, similar prompts, and the same retrieved context produce the same mistakes together. Voting works when failures are independent, and here they are not. Three correlated opinions give you the same answer with more confidence and more cost, which is the opposite of what you want.

### Context isolation

A practical section on what each role sees, because this is where the benefit actually comes from.

The classifier gets: the incident text in its delimited data region, the taxonomy with discriminators, and the urgency criteria. It does not get runbook passages, other incidents, or operator history. Small, focused, cheap.

The evidence checker gets: the incident text, the retrieved passages with identifiers, and the classifier's proposed category — but only the category, as a value to test against, not the classifier's reasoning. Withholding the reasoning is deliberate: if you give the checker the classifier's argument, it will tend to agree with it, and you will have built two roles that produce one opinion. Independence is the entire value of the second role, and it is easy to destroy by being generous with context.

Neither role gets write tools. Neither gets the other's tool scope. The classifier has no document access; the checker has no incident lookup.

Three benefits, and the third is the one people miss. Cost: you are not paying to send runbook passages to the classifier that cannot use them. Quality: each prompt does one job. And blast radius: a prompt injection in the incident text reaches both roles, but the roles have structurally different jobs and different tools, so a manipulation that produces a plausible classification will not automatically produce fabricated evidence — the checker's output is constrained to passages that were actually retrieved and validated. Independent scoping gives you a second chance to notice.

### A disagreement, walked through

Let me make this concrete with one case, because "surface the disagreement" is easy to agree with and easy to implement badly.

An incident arrives: "Scanners in the east dock keep dropping connection, started around six this morning, staff are writing shipments on paper."

The classifier reads it. The word "connection" and the pattern of dropping suggest a network problem. It proposes category network, urgency high, rationale citing loss of connectivity affecting operations, and notes that the number of affected devices is missing.

Retrieval runs on the structured query and returns three passages. The top one is from a facilities runbook: a documented procedure for the east dock scanner cradles, which describes intermittent disconnection caused by a known power-delivery fault in that specific dock, with a restart sequence that resolves it, and a note that this presents as a network symptom but is not one.

The evidence checker reads the incident and those passages. It answers: yes, a known procedure matches these symptoms; the matching passage is the east dock cradle procedure; and yes, the evidence appears inconsistent with the proposed category, because the procedure explicitly says this symptom is not a network fault.

Now the coordinator. It sees agreement on nothing and an explicit inconsistency flag. Its rule fires: present both, mark contested.

What the operator sees should look like this. A clear statement that the analysis is contested, so they know before reading anything else that a judgment is required. Then the classification: network, high urgency, with its one-line reason. Then the evidence: a facilities procedure for the east dock, revised four months ago, owned by the facilities engineering team, with a link, and the specific sentence that contradicts the classification quoted. Then the implication of each: if network, it routes to the network team; if facilities, there is a documented restart sequence that has resolved it before. Then the actions: accept network, accept facilities, or neither, each one click, with a reason captured.

That screen takes an operator perhaps fifteen seconds and it is genuinely useful. Compare it to what a model coordinator would have produced — a confident paragraph concluding that this is a network issue with a possible facilities component, routed to the network team, who would have spent two hours on it before someone remembered the cradles.

Three things to notice about the design of that screen. The contested state is signalled first, not buried. The contradicting evidence is quoted specifically, not summarized, because the operator needs to judge the source rather than trust the summary. And every option is one click with a captured reason, because a disagreement that takes a minute to resolve will be skipped under pressure.

That last point generalizes. Surfacing uncertainty only helps if resolving it is cheap. If you make the honest path slower than the confident path, operators will learn to prefer the confident path, and your careful design will have made the system worse.

### Shared artifacts, queues, and cancellation

Three mechanics you need once there is more than one worker.

A shared artifact store. When two roles both need the retrieved passages, do not embed the passages in two separate messages passed around your system. Retrieve once, store the result against the run, and give each role a reference. Two reasons. Cost and consistency: both roles reason over exactly the same evidence, which matters, because if they reason over different retrievals then a disagreement might be an artifact of the retrieval rather than a real difference of interpretation. And traceability: the evidence that was used is stored once, immutably, against the run, so an investigation three weeks later sees what the roles saw.

Task queueing. For a pilot with two parallel roles, direct concurrent calls are fine and a queue is over-engineering. You need one when work becomes asynchronous — when a role might take minutes, when you must survive a restart mid-flight, or when you need to control concurrency against a provider rate limit. That last one arrives sooner than you expect: two roles per triage, fifty triages in a burst, and you are suddenly at a hundred concurrent calls against a quota that allows twenty. A queue with a concurrency limit is the right answer, and it is better to add it before the burst than during it.

Cancellation. This one is routinely forgotten. If the operator navigates away, or the run hits its deadline, or one role fails in a way that makes the other pointless, the outstanding work should be cancelled. Otherwise you are paying for results nobody will read, and under load those abandoned calls consume the quota that live requests need. Propagate a cancellation signal into every role call, and make sure your provider adapter actually honours it rather than merely ignoring the response. Test it by starting a run and abandoning it, then checking whether the provider call completed.

### Correlation and observability

With multiple roles, observability stops being nice and becomes the thing that makes debugging possible at all.

Every role invocation records: the run identifier from chapter nineteen, the incident identifier, which role, the model identifier and version, the prompt version and hash, any tool calls made, the input token count, the output token count, the latency, and the outcome.

The coordinator records: which roles ran, which succeeded, whether they agreed, what rule it applied, and what it presented.

Then the operator's decision records against the whole run: accepted, edited, or rejected, with a reason.

With that, you can answer the questions that actually arise. When a customer reports a bad suggestion, which role was wrong. When quality moves after a change, which role's pass rate moved. When latency goes up, which role got slower. When cost rises, which role is responsible. Without it, a multi-agent system is a black box with more surface area, and you will end up guessing in front of a customer.

This feeds directly into chapter thirty-one, where we make the whole path traceable. Emit the events now, in the shape you will want then.

### Delegation contracts

Each specialist gets a contract, and it looks a lot like the tool contract from chapter eighteen — deliberately, because the discipline is the same.

A narrow, typed input. Exactly the context this role needs, nothing more.

A narrow, typed output. Structured, schema-enforced, validated on return.

No write authority. Same principle: no write tool exists for any role.

Its own budget and timeout. A role that hangs must not hang the run. Give each one a deadline shorter than the coordinator's overall deadline, and make the coordinator handle a missing result as a normal case rather than an exception.

Defined partial-failure behaviour. If the evidence checker times out, the coordinator presents the classification with an explicit note that grounding was unavailable. It does not fail the run, and it does not pretend the check passed. Partial results, clearly labelled, are usually more useful than nothing — but only if the label is honest.

And a depth limit, if you ever allow a role to delegate further. Recursive delegation without a hard depth cap is an unbounded cost loop with extra steps. For a pilot, the right depth limit is one: specialists do not spawn specialists.

### Measure it, and be willing to delete it

Now the part that makes this chapter a real engineering exercise rather than an architecture discussion.

You have a single-agent baseline. You have an evaluation fixture set from chapter sixteen, and a retrieval evaluation from chapter twenty. Run both architectures against the same fixtures and record four numbers.

Quality: how many fixtures produce a correct, useful result. Latency: the ninety-fifth percentile, not the average, because that is what an operator feels. Cost per triage: total tokens across all roles, priced. And disagreement rate: how often the specialists diverge, which is a new number the single agent could not produce.

Then look honestly. The split might improve quality, in which case say by how much. It might not, in which case you have two extra calls, more latency, higher cost, and more failure modes, for nothing.

And if it is not better — delete it. Say so in your notes and revert to the single agent. That is a successful outcome for this chapter, not a failure. An FDE who can remove their own complexity after measuring it is considerably more valuable than one who ships every architecture they build, and "we tried the split, measured it, and it did not earn its cost" is a strong thing to be able to tell a customer.

The disagreement rate deserves a second look regardless. If it is very low, the second role is probably not independent enough — check whether you leaked the classifier's reasoning into its context. If it is very high, either your specialists are poorly specified or the task genuinely is ambiguous, and either way that is a finding worth taking to the customer, because it may mean their own operators disagree too.

### Explaining this to a customer

A short section on the conversation, because multi-agent is a term that arrives at your customer from the trade press before it arrives from you, and it carries expectations you will have to manage in both directions.

Some stakeholders will want it because it sounds advanced. An executive sponsor who has read three articles about agent teams may ask why your system has only one. The answer that works is not a lecture about correlated errors; it is a reframe. Tell them what the system does have: a deterministic screening step, a grounded analysis with citations from their own procedures, and a human decision point. Then say that you split work across specialists where it measurably helps, and that you measured it, and here is the table. Executives respond well to evidence of restraint when it is quantified. They respond badly to being told their question was naive.

Other stakeholders will be alarmed by it. A security lead hearing "multiple AI agents" will imagine a system with expanding, unclear authority. Here the reframe is about capability: each role has fewer permissions than the single agent did, not more, because you scoped them separately. That is true, it is checkable, and it turns the word from a worry into a control.

And the operations team will ask the only question that really matters: does it make the suggestions better, and does it make them slower. Have both numbers.

One more framing worth having ready. If you removed the split after measuring it, say so, and say what you measured. Teams sometimes hide a reverted experiment because it looks like failure. It is the opposite: it demonstrates that your architecture claims are backed by measurement rather than fashion, which is exactly the property a customer needs to believe about everything else you tell them. I have seen that one admission do more for credibility than a successful feature.

### Anti-patterns

Six, and they are all common.

Agent proliferation. One agent per noun in the domain. You end up with eleven roles, nine of which add a model call and no information, and a system nobody can reason about.

Role-play theatre. Giving agents job titles — a manager, a researcher, a critic — and letting them talk. The job titles do no work. What does work is different context and different tools, and you can have that without the costume.

Free-text inter-agent conversation. Unbounded, expensive, unevaluable, and it produces convergence that resembles agreement. Roles should exchange structured objects through your coordinator, not messages with each other.

Voting as a quality mechanism. Correlated errors mean the majority is often wrong together, and you have paid three times for it.

A model coordinator that resolves disagreement. The subject of this chapter's core section. It converts your best signal into false confidence.

Recursive delegation with no depth limit. An elegant way to build an unbounded loop.

### How you verify this chapter

Six checks.

One. Construct a case where you know the two roles should disagree — an incident whose text points one way and whose retrieved procedure points another. Confirm the operator sees both positions clearly, and that nothing in your code produced a blended answer.

Two. Check each role's context. Confirm the classifier receives no runbook passages and the evidence checker receives the classifier's category but not its reasoning.

Three. Force each role to time out independently. Confirm the run completes with a clearly labelled partial result in each case.

Four. Confirm no role has any write capability, and that this is structural.

Five. Read your measurement table. Can you state, with numbers, what the split bought and what it cost? If the answer is "it feels better," you have not done the chapter.

Six. Ask yourself whether you would keep this split if you were paying for it personally. If the honest answer is no, remove it and write down why.

### The test project

The companion guide is a test. Attempt it before the hints.

Your goal is to split the triage proposal into two bounded specialists with a deterministic coordinator, and then to measure whether that was worth doing.

You will produce: an incident classifier with a narrow contract and no document access; a runbook evidence checker with a narrow contract, no incident lookup, and the classifier's category but not its reasoning; a deterministic coordinator with explicit rules for agreement, weak evidence, disagreement, and partial failure; correlation of both role outputs to the run, the incident, and the model and prompt versions; per-role budgets, timeouts, and defined partial-failure behaviour; and a measurement table comparing the split against the single-agent baseline on quality, ninety-fifth-percentile latency, cost per triage, and disagreement rate.

The constraints: no role has write authority; the coordinator is deterministic and never fabricates consensus; disagreement is presented to the operator as a structured, decidable choice; context is isolated per role; and no role delegates further.

You are done when a genuine disagreement reaches a human intact, when a timeout in either role degrades gracefully, and when you can state in one sentence, backed by numbers, why this split stays or goes.

### Recap

The decision from this chapter: you split by role only where isolation, permissions, parallelism, cost tiering, or independent evaluation justified it — and you measured whether it paid.

The framing: multi-agent is a cost. Sequential decomposition is usually just good workflow design. Parallel specialists are usable. Hierarchical delegation needs hard limits. Peer negotiation does not belong in a pilot.

The arithmetic: roles multiply failure modes, duplicate context, add latency, and compound error. Ninety percent twice is eighty-one percent.

The core rule: the coordinator is deterministic and never fabricates consensus. Disagreement between independently-scoped specialists is your highest-value signal, and it goes to a human as a structured choice. Calibrated uncertainty earns more trust than uniform confidence.

The discipline: isolate context deliberately, including withholding one role's reasoning from another so independence survives. Correlate everything. Give each role a contract, a budget, and a defined partial-failure behaviour. And be willing to delete the whole thing if the numbers do not support it.

Next chapter we build the machinery that makes all of these judgments empirical rather than rhetorical: an evaluation pipeline with golden fixtures, measurable checks, safety cases, a baseline, and a regression gate that blocks a merge. Every "we think this is better" in part four becomes a number.
