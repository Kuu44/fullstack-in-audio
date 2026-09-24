---
chapter: 31
title: "Observability for applications and AI behavior"
slug: 31-observability-for-apps-and-ai
part: "Part VI — Ship and protect the production-shaped system"
roadmap_nodes: ["Observability"]
voice: en-US-AndrewNeural
rate: "-18%"
audio: media/31-observability-for-apps-and-ai.mp3
companion_guide: docs/guides/31-observability-for-apps-and-ai.md
---

# Chapter 31 — Observability for applications and AI behavior

> Narration script. Headings, frontmatter, and blockquotes are stripped before rendering; only the prose below is spoken.

Welcome to chapter thirty-one. Your system is now deployed on declared infrastructure, built from a reproducible image, promoted through gates, and fed by a pipeline that knows its own freshness. It works. And if you were asked today why it produced a particular triage proposal for a particular incident last Tuesday afternoon, you would not be able to answer.

That question is the subject of this chapter, and I want to be direct about why it deserves a full lesson. In a conventional application, when something goes wrong, the failure is usually a failure: an error, a timeout, a wrong status code. There is something to find. In a system with an artificial intelligence component, the most important failures are not errors at all. Everything returns successfully, every status code is in the healthy range, latency is normal, the dashboard is entirely green, and the answer is wrong. There is no exception to catch, no stack trace, no failed request. Just a human who has lost a bit of confidence in your system, and who will lose more if you cannot explain what happened.

So observability here has to do two jobs. It has to tell you whether the service is healthy, which is the traditional job. And it has to make the reasoning path of an individual request reconstructible, which is the new one. A customer escalation that begins with "the copilot was wrong about the chiller unit yesterday" should end with an engineering decision, not a shrug, and the distance between those two outcomes is entirely determined by what you instrumented before it happened.

Let us build the vocabulary.

Start with the distinction between monitoring and observability, which is not merely fashionable terminology. Monitoring is checking known things: is the service up, is latency below a threshold, is the error rate acceptable. You decide in advance what to watch, and you watch it. Observability is the property of being able to ask new questions of a running system without deploying new code to answer them. The difference matters because in a customer deployment the interesting questions are the ones you did not anticipate. Monitoring tells you that something is wrong. Observability lets you find out what.

Then the three traditional signals, and I want you to understand what each is actually good for rather than just listing them.

Logs are discrete records of events, with a timestamp and a body. They are best at recording something specific that happened, with rich context, at a moment in time. Their weakness is volume and cost: logs are the most expensive signal per unit of insight, and undisciplined logging is the most common cause of surprising observability bills.

Metrics are numeric measurements aggregated over time: counts, rates, durations, gauges. They are cheap, they compress beautifully, and they are what dashboards and alerts should be built from. Their weakness is that they lose individuality. A metric tells you that the ninety-fifth percentile latency rose; it cannot tell you which request was slow or why.

Traces record the path of a single operation through a distributed system, as a tree of timed spans. A span is one unit of work with a start, a duration, and attributes. Traces are what let you see that a request took nine seconds, of which one hundred milliseconds was your service, four hundred was the database, two seconds was retrieval, and six and a half seconds was waiting for the model. Traces are the signal most suited to the question this chapter is about, and they are the one teams most often skip.

Now the concept that ties them together: correlation. A correlation identifier, usually a trace identifier, is generated once at the start of an operation and carried through every subsequent step, appearing on every log line, every span, and every persisted record along the way. It is the thread that turns a pile of disconnected evidence into a story. Without it, you have logs from four services with adjacent timestamps and a hope that you are looking at the same request.

Let me be specific about where that identifier must travel in FieldOps Copilot, because the chapter's mini-project asks for exactly this. It starts when the operator submits an incident in the React workspace. It travels in the request to the service. It is attached to the database write. It is attached to the audit event. It flows into the asset lookup, including the read model query and its freshness. It flows into retrieval, including which documents were considered. It flows into every tool call the agent makes. It is attached to the model request and its response. It is recorded on the persisted triage proposal. And it is attached to the operator's eventual approval or rejection. When all of that is in place, one identifier retrieves the entire life of a decision.

Then structured logging, which is a small change with a large payoff. A structured log entry is a set of named fields rather than a sentence. The difference is that fields can be searched, filtered, and aggregated reliably, whereas sentences require pattern matching that breaks whenever somebody rewords a message. Adopt it everywhere, make the correlation identifier one of the fields, and include the release identifier from chapter twenty-six on every entry so that any log line can be traced back to the exact configuration that produced it.

Next, service level objectives. A service level indicator is a measurement of something users care about, such as the proportion of intake submissions that succeed within two seconds. A service level objective is a target for that indicator over a window, such as ninety-nine percent over thirty days. And the error budget is the amount of failure the objective permits, which is the part that makes this useful rather than ceremonial. An error budget converts an argument about whether reliability is good enough into arithmetic, and it gives you a principled way to answer a customer asking for more nines: more nines costs budget, here is what it would buy, here is what it would cost.

Two pieces of advice on objectives in a pilot. Pick very few, two or three at most, and make them about things the operator experiences rather than things your infrastructure experiences. Availability of the intake path matters; the availability of your cache does not, on its own, mean anything to anybody.

Then alerting, where the most common failure in our industry lives. The rule is to alert on symptoms that users feel, not on every cause. If you alert on high processor usage, you will be woken up for a condition that may be entirely harmless. If you alert on intake submissions failing, you will be woken up when it matters. Every alert should be actionable, should say what is wrong in user terms, and should link to a runbook. And if an alert fires regularly and the response is to acknowledge it and move on, delete it, because its real effect is to train people to ignore alerts, including the one that mattered.

Now the part specific to this course: observability for artificial intelligence behavior. The traditional signals will tell you your system is healthy while it is being confidently wrong, so you need a second family of signals.

Start with the trace. Your triage operation should produce a span tree that mirrors the decision. A root span for the triage request. A child span for asset enrichment, with attributes recording whether the asset was found and how stale the read model was. A child span for retrieval, recording the query, how many documents were considered, how many passed your relevance threshold, the identifiers and revisions of the ones selected, and the resulting retrieval strength. A span per tool call, with the tool name, an input summary, the result status, and the duration. A span for the model call, with the model identifier and version, the prompt version, the token counts for input and output, the estimated cost, and whether the response parsed against your schema. And attributes on the root recording the outcome: what was proposed, what confidence was expressed, whether the system declined for insufficient evidence, whether a fallback path was used, and later, what the operator decided.

Read that list again and notice something. Almost every element is a decision you made in an earlier chapter, now being recorded. The prompt version is from chapter sixteen. The tool audit is from chapter eighteen. Retrieval strength and citations are from chapter twenty. Token and cost accounting is from chapter twenty-three. The read model freshness is from chapter twenty-four. The release identifier is from chapter twenty-six. Observability is not a new subsystem; it is the act of making the decisions you already made visible.

Then the aggregate signals, which we touched on in chapter twenty-six and which belong on the pilot dashboard. Operator acceptance rate, which is your best available proxy for quality. Modification patterns, which tell you what to fix. Refusal and insufficient-evidence rate, which detects upstream breakage. Structural validity rate, which is an early indicator of a model change. Retrieval strength distribution, which tells you whether your grounding is degrading as the corpus grows. Fallback rate. And cost per triage, which the customer will ask about.

And one more that teams rarely instrument and should: the gap between proposal and decision. How long does an operator take to act on a proposal, and how often do proposals sit unactioned? A copilot whose suggestions are ignored is failing, and it will not show up in any error rate.

Let me walk an escalation, because the abstract case for tracing is much less persuasive than seeing one resolved.

The message arrives on a Thursday morning. The operations manager writes that the copilot was wrong about the chiller unit at the northern distribution site yesterday, that the operator followed its recommendation, and that it cost them several hours. There is no incident number in the message, no timestamp, and a slightly annoyed tone. This is what a real escalation looks like.

Step one is to find the interaction. With structured logs and an indexed identifier, you search for proposals concerning that asset within the previous two days and find three. You confirm with the operator which one they mean. Note that this step is only possible because the asset identifier was recorded as a field on the proposal, which is a decision from chapter twenty-four.

Step two is to open the trace for that correlation identifier, and here the entire decision unfolds in front of you. The asset enrichment span shows the asset was found, criticality low, read model age eleven hours, which is within tolerance. The retrieval span shows four documents considered, one passing the relevance threshold, retrieval strength marked weak. The model span shows the prompt version, the model version, the token counts, and a successful schema-valid response. The root span records that the proposal was routine priority, that confidence was expressed as moderate, and that the operator accepted it without modification eleven seconds after it appeared.

Step three is interpretation, and notice how different this is from speculation. Retrieval was weak, and the agent proposed anyway rather than declining for insufficient evidence. That is a behavioral question: was the threshold set too low, or was the instruction to decline too weak? Meanwhile the asset criticality was low, which sends you back to the pipeline to ask whether that value is correct in the source, which is a different investigation with a different owner. And the operator accepted in eleven seconds, which tells you something uncomfortable and important: the interface is not conveying uncertainty strongly enough for anyone to pause over it.

Step four is the response, and it is now a set of engineering decisions rather than an apology. Raise the retrieval strength threshold below which the agent must decline. Make weak grounding visible in the interface, not merely present in the response object. Open a data-quality item with the customer's asset owner about the criticality value. And add a fixture to the evaluation suite representing exactly this case, so the behavior cannot silently return.

Now compare this to the version without instrumentation. You would know that a wrong answer happened. You would not know whether retrieval fired, whether the asset data was stale, which prompt version was live, or whether the operator hesitated. You would probably adjust the prompt, because that is the only lever you can see, and you would have no way to know if it helped. The instrumented version took perhaps twenty minutes and produced four concrete actions, one of which was not even a software change. That difference is what this chapter buys.

There is one more thing I want you to notice about that escalation. Three of the four findings were not in the model. They were in the threshold, the interface, and the customer's data. This is typical, and it is why instrumenting only the model call is insufficient. The decision path is the unit of analysis, not the inference.

Now, redaction, which is a hard requirement rather than a nicety.

Incident text in a real deployment contains things you must not casually copy into a logging system: names, contact details, location details, account identifiers, occasionally health or safety information, and sometimes credentials that a user pasted into a description field because they were trying to be helpful. Your observability pipeline is, by default, an exfiltration path for all of it, and it typically sends that data to a third-party system, in a region you may not have checked, with a retention period nobody chose, accessible to everybody with a dashboard login.

So apply a few rules. Log identifiers, not content: record that an incident exists, its identifier, its category, its severity, and its priority, rather than its description text. Where you must capture content for debugging, redact it at the source, inside the service, before it leaves the process, not at the destination, because a filter at the destination means the data already travelled. Maintain a deny list of field names that are never logged, and prefer an allow list where you can, since an allow list fails safe when somebody adds a new field. Redact patterns that look like secrets, because users will paste them. And apply the same discipline to trace attributes and error reports, which people routinely forget: an exception handler that logs the full request body has just defeated every other control.

There is a tension here and I want to name it honestly, because pretending otherwise leads to bad practice. Redaction reduces diagnosability. If you never record what the operator typed, you cannot see why retrieval failed. The resolution is a documented, deliberate arrangement rather than an accident: identifiers and derived attributes in general telemetry, retained normally; a narrow, access-controlled path for content that is genuinely needed for diagnosis, with a short retention and an audit trail of who viewed it; and explicit customer agreement on where that line sits. That last part is the professional bit. The customer should know exactly what your telemetry captures, and should have agreed to it, ideally in writing before launch.

While we are here: observability has a location, and a retention, and a cost. The location is a data residency question, exactly as we discussed in chapter twenty-nine, and it is the one people most often get wrong because logging destinations default to somewhere convenient. Retention should be chosen, stated, and defensible, because both excessive retention and inadequate retention are findings in a review. And the cost is dominated by log volume, which means high-verbosity logging in a busy service can genuinely become one of your largest line items.

A word about dashboards, because most dashboards are built for nobody in particular and are therefore read by nobody in particular.

You have three audiences in a pilot, and they want different things. The operator or their supervisor wants to know whether the system is working for them right now: can incidents be filed, are proposals appearing, is anything degraded, and is the asset context current. Their view should be small, in plain language, and honest about degradation. A single line saying that asset context was last refreshed at a stated time is worth more to them than any chart.

The engineer wants diagnosis: latency broken down by phase, error rates by endpoint, dependency health, retrieval strength distribution, structural validity, fallback rate, and a path from any anomaly into the underlying traces. This view can be dense, because the person reading it is looking for something specific.

The sponsor wants evidence of value and control: adoption, volume, acceptance rate, time saved against the baseline from the charter, cost per triage against the budget, and availability against the objective. Notice that this view contains almost no infrastructure at all. A sponsor does not care about processor utilization, and showing it to them signals that you have confused activity with outcome.

Build all three, keep each one small, and know which you are presenting in which meeting. The most common mistake is showing the engineer's dashboard to the sponsor, which produces either alarm about numbers they cannot interpret or a polite loss of interest.

There is one number I would put on all three, and it is the one that ties this course together: whether the copilot's proposals are being accepted and acted on. It is the closest thing you have to a measure of whether any of this worked.

Let me also address the cost of observability directly, because it is a real budget line and because the way you control it is mostly design rather than negotiation.

Log volume is the dominant cost, and volume is driven by verbosity and by how much you log per request. So log at an appropriate level by default, make the level configurable at runtime so you can raise it temporarily during an investigation without a deployment, and resist logging both the entry and exit of every function. Metrics are cheap unless you attach high-cardinality dimensions, which we will come back to in the pitfalls. Traces are moderate, and the lever there is sampling.

Sampling deserves a moment because the naive approach undermines the whole chapter. If you keep a fixed small percentage of traces at random, then the one trace you need during an escalation is almost certainly one you discarded. The better approach is to decide whether to keep a trace after the operation completes, based on what happened: always keep errors, always keep unusually slow requests, always keep refusals and fallbacks, always keep anything where retrieval was weak or the schema validation failed, and sample the ordinary successes lightly. You get a small volume of traces that is heavily enriched with the interesting cases, which is exactly the inverse of what random sampling gives you.

Set a retention that matches how you use the data: traces for a short window because they are for live diagnosis, aggregated metrics for much longer because they are for trend and evidence, and logs somewhere in between. State those windows, because a customer will ask, and because an unbounded retention is both a cost and a liability.

Let me talk about instrumentation approach briefly. Use an open, vendor-neutral instrumentation standard for traces, metrics, and logs. The specific backend you send them to is a decision that may be made by the customer, may change, and may differ between the pilot and production environments. If your instrumentation is written against a neutral interface, switching backends is configuration. If it is written against a vendor's library, switching is a refactor of every file in your codebase. In field work, where the customer may already have a monitoring platform they insist on, this is not a hypothetical concern.

Also: automatic instrumentation gets you a surprising distance for free, typically covering incoming requests, outgoing requests, and database queries. Take that, and then spend your manual effort on the parts that matter here, which are the retrieval, tool, and model spans and their attributes. Those are the ones no library will add for you, and they are the ones that answer the question this chapter exists to answer.

One more thing belongs in this chapter, and it is the connection between observability and the runbook, because telemetry without a response procedure is just expensive curiosity.

For each alert you define, write the runbook entry at the same time. It needs four things. What this alert means in terms a person can act on, stated as a user-visible symptom rather than a metric name. What to check first, which should be a specific dashboard view or a specific query, not a general suggestion to investigate. What the known causes are, in rough order of likelihood, with the remedy for each. And when to escalate, to whom, and with what information.

Writing this at alert-definition time has a useful side effect: if you cannot write a sensible runbook entry, the alert is probably not actionable, and you have just discovered that before it wakes somebody.

For FieldOps Copilot, the runbook entries you will actually need are fairly predictable. Intake failing, which is the most urgent because it blocks the operator's primary job. The asset read model stale beyond tolerance, which points at the pipeline chapter. Retrieval strength collapsed across many requests, which usually means the index or the embedding path. Model provider failing or timing out, which should already be producing a labelled fallback and therefore is urgent only if the fallback is also failing. Cost per triage exceeding budget, which is a working-hours issue. And the quality signal, acceptance rate dropping, which is not an alert in the paging sense but should be a reviewed weekly signal with a defined owner.

Notice that these map almost one to one onto the chapters that preceded this one. That is not a coincidence. Each capability you added brought a failure mode with it, and this is where you finally write down what to do about each.

Now the pitfalls.

The first is logging everything at high verbosity, which produces cost, noise, and a privacy exposure all at once.

The second is missing correlation, where each component logs usefully and nothing connects.

The third is logging raw incident content, which is the single most common privacy failure in systems like this.

The fourth is alerting on causes rather than symptoms, which produces noise and trains people to ignore alerts.

The fifth is dashboards that show only service health. A green dashboard during a quality collapse is worse than no dashboard, because it provides false assurance.

The sixth is unbounded cardinality in metrics. Attaching a unique value such as an incident identifier as a metric dimension creates a separate time series for every incident, which breaks metrics backends and produces alarming bills. Unique identifiers belong on traces and logs, never as metric dimensions.

The seventh is sampling traces without keeping the interesting ones. If you sample, use a strategy that always retains errors, slow requests, refusals, and fallback cases.

The eighth is an alert with no runbook, which converts a page into a research project at the worst possible time.

The ninth is instrumenting the happy path only, so the fallback path, the refusal path, and the degraded path are invisible, which are exactly the paths you need to see.

The tenth is telemetry that leaves the jurisdiction without anybody checking.

And the eleventh is treating observability as something to add after the system works. It is much cheaper to instrument as you build, and a system that has been running uninstrumented has already destroyed the evidence for the questions you will be asked.

Now verification. Here is what you should be able to demonstrate.

Submit one synthetic incident and retrieve, from a single correlation identifier, the complete path: intake, authorization, persistence, audit, asset lookup with freshness, retrieval with document identifiers and strength, every tool call, the model request with its versions and token counts, the proposal, and the operator's decision.

Show a trace where the time is attributed across the phases, and state where the majority of it went.

Show the pilot dashboard containing both service health and workflow health: availability, ninety-fifth percentile triage time, failure rate, cost per triage, operator acceptance, refusal rate, retrieval strength, and read model freshness.

Cause a synthetic dependency failure and show an alert that names the user-visible symptom and links to a runbook that resolves it.

Demonstrate redaction: submit an incident containing a name, a contact detail, and something shaped like a credential, and show that none of them appear in logs, traces, or error reports, while the correlation identifier still connects everything.

Show that an unhandled exception does not log the request body.

Show a metric that would have had unbounded cardinality and how you avoided it.

State where your telemetry is stored, in which region, for how long, and who can read it.

And show the release identifier and prompt version present on a proposal produced a week ago, connecting this chapter's work back to chapter twenty-six.

Before the recap, one thought about handover, since it applies to everything in Part Six. The observability you build is not primarily for you. You will leave. The person who inherits this system will have none of your context, and the dashboards, alerts, traces, and runbooks are how you transmit it. So build them for a stranger: name things in the customer's vocabulary rather than your internal shorthand, make every alert self-explanatory, and make sure the path from a complaint to a trace is written down rather than known. A good test is whether somebody who has never seen the system can, given a complaint and your documentation, find the relevant trace unaided. If they can, you have built observability. If it requires you, you have built a set of tools that happen to work for you.

Your practice handoff is the test in the guide: trace one incident end to end, emit the structured events, redact before data leaves the service, build the dashboard with both health families, and trigger a synthetic failure to verify an actionable alert.

To recap. Monitoring answers questions you anticipated; observability lets you ask new ones. Logs carry specific events, metrics carry cheap aggregates, traces carry the path of a single operation, and a correlation identifier carried through every boundary is what makes the three into one story. For artificial intelligence behavior, instrument the decision: asset freshness, retrieval strength and sources, tool calls, model and prompt versions, token counts and cost, refusals, fallbacks, and the operator's eventual decision. Watch aggregate quality signals alongside service health, because a wrong answer produces no error. Alert on symptoms, always with a runbook, and delete alerts nobody acts on. Redact at the source, log identifiers rather than content, agree the boundary with the customer explicitly, and know where your telemetry lives and for how long. Instrument as you build, because you cannot retroactively observe last Tuesday.

Next chapter is the last of Part Six, and it gathers everything into the form a customer's risk function will actually assess: threat modeling, data classification, retention, least privilege, auditability, human oversight, abuse testing including prompt injection and cross-tenant retrieval, and the honest statement of residual risk that lets a customer decide whether to launch.
