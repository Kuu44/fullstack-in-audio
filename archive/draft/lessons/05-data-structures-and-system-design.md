<!-- tts:skip -->
## TTS notes — chapter 5

- Voice: `en-US-AndrewNeural`, rate `-14%` (about 146 words per minute).
- "big oh" is spelled out in prose. No mathematical notation anywhere.
- "p ninety-five" is written as "the ninety-fifth percentile" so the voice reads it naturally.
- Recurring cast: Dana (sponsor), Sam (coordinator), Priya (security), Marcus (platform), Ana (second engineer).
- `[pause]` becomes a beat of silence at segment turns.
- Nothing in this block is spoken.
<!-- /tts:skip -->

Welcome back to FullStack in Audio. This is chapter five: data structures, algorithms, and system design — for one specific path through one specific customer's system. [pause]

Let me start with the day that ruins an unprepared design.

It is February. A storm takes out power across a region, and eleven of Harborline's forty depots lose it at once. Generators start in nine of them. Two do not. Within twenty minutes, the operations desk receives something like three hundred incident reports: refrigeration alarms, dock doors stuck in whatever position they were in, network outages, scanners offline, and a dozen reports that are really the same problem described by four different supervisors.

This is the moment your system either helps or becomes another thing that is broken. And notice something important about that burst: the daily total is not the problem. Four hundred incidents spread across a day is a trickle. Three hundred in twenty minutes, most of them describing eleven underlying events, is a completely different system.

That gap — between average volume and the shape of the peak — is where most designs fail, and it is why this chapter exists. We are going to design the path from intake to triage, and we are going to do it the way an engineer who has been burned does it: by writing down numbers first, choosing structures for stated reasons, naming a failure mode at every boundary, and then trying to break our own design on purpose.

## Why this chapter is not an interview drill

You will meet data structures and system design in forward deployed engineering interviews, and that is fine, but that is not why they matter here.

They matter because a customer's volume is not your demo's volume, and because your design has to survive the worst twenty minutes of their quarter. And they matter because you will be asked, by someone like Marcus, a question that sounds casual and is not: "What happens if we get a thousand of these at once?"

There are three possible answers to that question. The first is "it'll be fine", which is what an amateur says and which is almost never true. The second is "I don't know", which is honest and, said once, acceptable. The third is the professional answer: "Here is the volume I designed for, here is where it starts to degrade, here is how it degrades, and here is what it would take to handle ten times more." That answer is a design artifact, and producing it is this chapter's skill.

## Getting the numbers when nobody has the numbers

You need four numbers before you draw anything: typical volume, peak burst, acceptable response time, and retention.

And here is the field reality you already discovered in chapter one: nobody measures this. Harborline cannot tell you how many incidents they get. So you estimate, from artifacts rather than from opinions.

The mailbox knows. Count messages in the shared inbox for four weeks and you have a volume distribution rather than someone's guess. The shift pattern knows: three shifts, nine coordinators, and a known handover time tell you where the queue accumulates. The spreadsheet knows: it has rows with timestamps, and even bad timestamps give you shape. And the incident everyone remembers — the storm — gives you the worst case, because people remember the worst case vividly and will tell you about it in detail.

Three disciplines make an estimate honest.

Label every number as measured, derived, or assumed. Measured came from counting something. Derived came from arithmetic on something measured. Assumed came from a person's memory, and is the one that will be wrong.

State the peak as a rate over a window, not as a daily total. "Three hundred in twenty minutes" is designable. "Four hundred a day" tells you almost nothing about the design.

And write the growth assumption separately. If this succeeds at eleven depots, it goes to forty. If Harborline acquires a competitor, it goes to ninety. You are not designing for ninety today, and you should know the number at which today's design stops being appropriate. That number is the most useful thing in the document, because it converts "it'll scale" into a specific trigger.

Now response time. The useful discipline here is to state it as a percentile, not as an average, because averages hide the experience that people complain about. If the ninety-fifth percentile submission takes eight seconds, one in twenty operators has a bad time, and those are the ones who tell their colleagues the system is slow.

For FieldOps, sensible targets are: an operator's submission is acknowledged in under two seconds at the ninety-fifth percentile, because a form that takes longer feels broken, and a triage suggestion appears within about thirty seconds. Those two numbers are radically different, and the difference is a design instruction: the acknowledgment must be synchronous and cheap; the suggestion must be asynchronous and allowed to take time.

That single realization — which parts must be fast and which parts must merely be reliable — is what separates a design from a diagram. [pause]

### The arithmetic, done out loud

Let me do Harborline's numbers with you, because capacity math is much less intimidating than it sounds and almost nobody bothers.

Start with what we counted. Four weeks of the shared mailbox gives roughly two thousand four hundred messages, so about eighty-five a day on average, and a weekday peak around a hundred and forty. That is measured.

Now derive the rate. A hundred and forty reports across a twelve-hour operating window is about twelve an hour, or one every five minutes. At that rate, a system could be almost comically slow and nobody would notice. If that were the whole picture, your design would be a single process and a file.

Now the storm, which is assumed, because it comes from people's memory of February. Three hundred reports in twenty minutes. That is fifteen a minute, sustained, with bursts inside it — supervisors do not arrive evenly; they arrive in clumps as each depot works out what is wrong. Call the worst minute forty.

So the design has to hold two numbers that differ by a factor of about seventy-five: one every five minutes as the normal case, forty in a minute as the peak. And here is the thing worth internalizing: forty in a minute is still not a large number in absolute terms. This is not a scaling problem in the sense that a social network has scaling problems. A single modest service, writing to a single database, with a bounded queue in front of the expensive work, handles this without breathing hard.

What will break is not throughput. It is anything that takes a long time per item and runs synchronously. Suppose the model call in chapter fifteen takes four seconds. At one incident every five minutes, four seconds is irrelevant. At forty a minute, four seconds each means you need about three concurrent model calls running continuously just to keep up — and if the provider rate-limits you, or takes twelve seconds under load, you are now falling behind at a rate that compounds for the whole storm.

Do that arithmetic now, on paper, and notice what it tells you. It says: put the model behind a queue, make the operator's acknowledgment independent of it, and decide in advance what happens when the queue grows. You reached a design decision — arguably the most important one in the system — by multiplying two numbers. No diagram was involved.

One more piece. Retention, which is the number people forget entirely. If Harborline keeps incidents for two years, that is roughly sixty thousand records. Sixty thousand rows is nothing; every database on earth handles it. But sixty thousand rows with audit events at, say, four per incident, is a quarter of a million audit rows, and if your operator list query scans audit history to compute current status, you have built something that gets measurably slower every quarter and will feel fine for the entire pilot. That is the worst kind of defect: one whose arrival date is after your departure date.

So write the retention number down, multiply it out, and ask which of your queries touches the growing thing. [pause]

## Data structures as decisions

Now the structures. For each one I want the operation it makes cheap, the cost you accept, and the FieldOps place it belongs.

An array or list keeps order and gives you cheap access by position and cheap appending. Finding something by content means scanning it. Use it where order matters and lookup does not: the audit trail, the batch you are currently processing.

A map, or dictionary, gives you near-constant lookup by key, at the cost of memory and of losing order unless you pay extra for it. Use it wherever you have an identifier: active incidents by identifier, depots by code, a count of reports per depot during a burst.

A queue is order plus the discipline of handing work off. Its real value is not the data structure; it is the decoupling. The thing that accepts work and the thing that does work are no longer forced to run at the same speed. In FieldOps, the queue between intake and triage is what makes the storm survivable, because intake stays fast while triage falls behind — and falling behind visibly is completely different from timing out invisibly.

A priority queue, usually implemented as a heap, gives you cheap access to the most urgent item at the cost of not keeping a full ordering. This is the structure that matches your chapter two rule: the triage worker should always take the most urgent waiting incident, not the oldest.

But here is where I want to sharpen your judgment, because this is exactly the kind of decision that looks technical and is really about workload. If your queue holds forty items, sorting it every time is free and a heap is over-engineering. If it holds two hundred thousand, the heap earns its place. Choosing the sophisticated structure for a small workload is not a harmless flourish — it is code with more failure modes than the problem required, and you will maintain it.

A set gives you cheap membership testing, which is the foundation of deduplication. And deduplication, in the storm, is the single highest-value thing your design can do. Eleven power failures produce a hundred and forty reports. A coordinator who sees eleven grouped events instead of a hundred and forty rows can actually work.

But notice the hard part is not the set. It is the key. What makes two reports "the same"? Same depot plus same equipment identifier plus within a time window? Same depot plus same category? If your key is too loose you will merge two genuinely separate refrigeration failures and one of them will be invisible — which is the dangerous direction of that error. If it is too strict you deduplicate nothing. The structure is trivial; the domain decision is not, and it belongs in a document with your reasoning, not buried in a comparison.

An append-only log is a sequence you only ever add to. Use it for audit: who changed what, when. Its power is that it cannot be edited, which is exactly what an auditor wants and exactly what makes it a poor primary read model, because answering "what is this incident's status now" requires replaying it. Which brings us to the pattern worth naming: write facts to the log, and maintain a separate structure optimized for reading. You will meet that again in chapter fourteen.

And a graph, finally, where things point at other things: this incident affects that asset, which belongs to that depot, which depends on that power feed. You do not need graph machinery yet. You need to notice that the relationships exist, because in the storm the useful insight — "these hundred and forty reports are eleven power events" — is a graph traversal in disguise. Recognizing a graph you are not going to implement yet is a real skill, because it tells you which identifiers to record now so the traversal is possible later. [pause]

## Complexity, honestly

Two ideas and then I will stop.

The first: know where your cost actually is. For FieldOps, the priority rule is constant time and effectively free. The database query that lists an operator's open incidents is where your time goes, and the model call in chapter fifteen will take a thousand times longer than everything else combined. If you spend a day optimizing the rule, you optimized the cheapest thing in the system. Measure first, and the honest sentence "this is not where the time goes" is a real finding.

The second, and it is the one that catches good engineers: watch for accidentally quadratic work. It hides in innocent code. For each incoming report, scan all open incidents to check for a duplicate. With forty open incidents, invisible. With two thousand open incidents during a storm and three hundred arriving, that is six hundred thousand comparisons, which turns into a system that gets slower exactly when it is needed most.

That is the pattern to fear: not slowness, but slowness that increases with load. A map or a set turns that scan into a lookup and the problem disappears. The skill is noticing the nested loop in a description of behavior, before it exists in code. When you hear yourself say "for each of these, check all of those", stop and ask what the total is at peak. [pause]

## Designing the intake-to-triage path

Now let us design it, out loud, and I will narrate the reasoning rather than the boxes.

The path begins with an operator submitting a report from the browser. That request must do the least possible work: validate the input, assign an identifier, record it durably, and return. Nothing else. No model call, no notification, no enrichment, no clever lookup. Because everything you add here is added to the operator's waiting time and to your failure surface at the moment of highest load.

Ask a sharp question at this boundary: what does a successful response mean? It should mean "this is recorded and will be handled" — not "this has been triaged." Those are different promises, and only the first one can be kept quickly. A design that promises the second in the response is a design that will time out in the storm.

Then the report is queued for triage. The queue is the heart of the design, and it does three things: it absorbs the burst, it makes the backlog visible, and it lets you control how fast triage runs independently of how fast reports arrive.

Triage takes an incident, applies your priority rule, later adds a model suggestion and retrieval, and records the result. And here you must make a decision that will feel uncomfortable: what happens when triage is slower than arrival for a sustained period? Because in the storm, it will be.

There are only three honest answers, and all three are legitimate. You shed load — refuse new work with a clear message, which is brutal and safe. You degrade — skip the expensive part of triage, apply only the deterministic rule, and mark the incident as awaiting full triage, which keeps the system useful. Or you queue and wait, accepting a growing delay, which is fine if the delay is visible and bounded and disastrous if it is invisible.

For FieldOps, degrading is the right answer, and here is why it is a better answer than it first appears: your priority rule is deterministic, fast, and does not depend on a model provider. In a storm, a system that gives every incident a rule-based priority within seconds and flags the expensive suggestions as pending is genuinely more useful to Sam than one that would eventually produce beautiful recommendations. Graceful degradation is not a compromise; it is a designed behavior you chose because you knew which part of your system was cheap and reliable.

Then notification, which is the boundary where an external system you do not control enters your design. And external systems fail in the least convenient ways: they are slow, they succeed after your timeout, they accept a message twice, or they are down for an hour. Every one of those needs a decided answer. Which means retries with increasing delay and a cap, a dead-letter destination for messages you could not deliver, and — critically — the acceptance that a notification may be delivered twice, because a system that is retried is a system that duplicates.

Which brings us to the two ideas that make this whole path robust.

The first is idempotency. An operation is idempotent if performing it twice has the same effect as performing it once. This matters because retries are inevitable — the browser's connection drops after the write succeeded, so Sam presses submit again; a queue redelivers a message it was not sure was handled. Without idempotency, every one of those produces a duplicate incident, and during the storm you get a mess that looks like a bug in your customer's operation rather than in your retry logic.

The technique is an idempotency key: a value supplied by the caller that identifies this attempt, not this incident. Same key arriving twice means "this is the same attempt" and the second one returns the original result instead of creating something new. Note that this is a different mechanism from your deduplication key, and confusing them causes a subtle and painful bug. Idempotency asks "is this the same submission?" Deduplication asks "is this the same real-world problem?" Two supervisors reporting the same failed generator are not a retry; they are two submissions about one event, and they should both be recorded and then grouped.

The second is backpressure. Every queue must have a limit, and you must decide what happens when the limit is reached. Because an unbounded queue does not remove the failure — it relocates it. It converts a fast, visible rejection into a slow, invisible accumulation, and then into memory exhaustion at a moment of your system's choosing rather than yours. Bounded queues with a stated behavior at the boundary are one of the clearest markers of an engineer who has operated something in production.

And every boundary needs a timeout. Every single one. A call without a timeout is a call that can wait forever, and in a storm that means a worker occupied doing nothing while work piles up behind it. Default timeouts in libraries are frequently generous to the point of being useless. Choose them, from your latency budget, deliberately. [pause]

## Failure modes at each boundary

Let me go boundary by boundary, because your project requires exactly this.

Browser to service. The service is down, or slow, or the network drops mid-request. Graceful response: the operator is told it was not received, their typing is preserved, and retrying is safe because of the idempotency key. Never a confirmation you cannot substantiate.

Service to store. The database is unreachable or rejects the write. This one is important: if the write fails, the submission failed, and the operator must know. The tempting alternative — accept it into memory and write it later — turns a visible failure into silent data loss the moment the process restarts. Do not accept what you cannot durably record.

Service to queue. The queue is full or unavailable. If the incident is already durably recorded, you can recover by scanning for unqueued work, so this failure should degrade rather than reject — which is only true because you wrote the record first. Notice how the ordering of two steps determined whether a failure is recoverable.

Triage worker to model provider. Slow, rate-limited, or down. Degrade to the deterministic rule, mark the suggestion as pending, and retry with increasing delay. Never let this block the operator's view of the incident.

Triage to notification. Deliver at least once, accept possible duplicates, cap the retries, and dead-letter what you cannot deliver — with someone accountable for looking at the dead-letter destination, because an unwatched dead-letter queue is just a slower way to lose data.

And the boundary everyone forgets: the operator's own attention. If two hundred incidents arrive at once, your interface is a failure boundary too. Grouping, priority ordering, and an honest "triage is running behind" banner are design decisions, not decoration. A technically perfect backend fronted by an unreadable list of two hundred rows has failed the storm. [pause]

## The design review with the platform team

Let me tell you what this design has to survive socially, because a design that cannot be explained does not get deployed.

You will present this to Marcus and two of his engineers. They are not hostile, they are experienced, and they are going to carry whatever you leave behind. Here are the questions they will ask, in roughly this order, and what a good answer sounds like.

"What are you asking us to run?" A concrete list, with counts. One service, one database, one queue, one worker process. Not "a microservices architecture." If your answer to this question takes more than about twenty seconds, you have probably designed something too complex for a pilot.

"What happens when it breaks at two in the morning?" For each component: how a failure shows up, what the user sees, and whether the system recovers on its own or needs a person. The answer they are hoping for is that most failures degrade rather than stop, and that the ones requiring a person have a written procedure.

"Where does it get slow first?" This is the question that tells them whether you actually understand your own design. If you say "the model call, and here is the queue that contains the damage", you have passed. If you say "nowhere, it should be fine", they will stop believing the rest of the presentation.

"What happens at ten times the volume?" Not because they expect ten times — because they want to know whether you thought about it. The good answer names the first component that would need to change and roughly what change it needs.

"Who else can see this data?" That is Priya's question arriving through Marcus, and it belongs in a design review because data flow is a design property. Every hop your incident text takes is a place where someone could read it.

And the one that surprises people: "Can we turn part of it off?" Enterprises love a system with a switch. If the model path can be disabled and the system still records incidents and applies your deterministic rule, then they can deploy it during a change freeze, or during a provider outage, or during a security review, without losing the workflow. Designing that switch in from the start costs you almost nothing and it converts a risky deployment into an acceptable one.

Notice that not one of those questions is about your data structure choices. Those choices matter — they are why your answers are good — but the review is about operability. This is the recurring lesson of field engineering: the technical quality of a design is judged by how it behaves in the hands of people who did not build it. [pause]

## Breaking your own design

Your project asks you to run a large batch through the command-line program from chapter three and note where the current design fails. I want to explain why, because it is tempting to skip as busywork.

You have a working program. It handles one incident at a time, validates it, computes a priority, and records evidence. It is correct. It is also, right now, the entire system — which means it is the perfect thing to break, because breaking it teaches you what your design must solve rather than what you imagine it must solve.

So run hundreds of records through it, and pay attention to what actually goes wrong. Some of it will be predictable. Some of it will surprise you, and the surprises are the point. Does the evidence file become unreadable? Does anything deduplicate, or do you now have a hundred and forty rows about eleven events? Is there any notion of ordering — could you answer "what should Sam look at first"? What happens to a malformed record in the middle of a batch: does it stop everything, or get skipped silently, or get skipped visibly? Does anything at all tell you how far behind you are?

Then write down what you found, because that list is the requirements document for chapters eleven through fourteen, derived from evidence rather than from imagination. This is the difference between a designer and a person drawing boxes: the designer has broken a small version and knows which failure came first.

One more reason this matters. When Marcus asks his casual question — "what happens if we get a thousand at once?" — you will have an answer with a number in it, because you tried. That sentence earns more credibility than any diagram. [pause]

## The failure modes of this chapter's work

The first failure is the design with no numbers. Boxes and arrows, no volume, no latency target, no retention. It cannot be evaluated and it cannot be wrong, which means it is not a design.

The second failure is the daily average as a capacity plan. Four hundred a day sounds gentle and hides the twenty minutes that matter.

The third failure is the unbounded queue, which relocates a failure rather than handling it.

The fourth failure is the missing timeout. Somewhere in your design is a call with no time limit, and under load it will occupy a worker forever.

The fifth failure is the retry storm. Every client retries immediately, all at the same time, so the struggling dependency receives more load precisely when it is failing. Retries need increasing delays, a cap, and some jitter so they do not synchronize.

The sixth failure is confusing the deduplication key with the idempotency key, which produces either merged incidents that should have been separate or duplicate rows that should have been one. Two different questions, two different mechanisms.

The seventh failure is premature distribution. A queue system, a cache, and a worker fleet for a workload of four hundred records a day. Every component is a thing that fails, needs credentials, needs monitoring, and needs somebody at two in the morning. At pilot scale, the simplest design that degrades gracefully beats the scalable one that Marcus's four-person team cannot operate.

And the eighth, which is the one that costs a pilot: designing for the happy path and calling the failure modes "operational concerns." The storm is not an edge case. It is the week your customer decides whether this system is real. [pause]

## How you verify this chapter's work

Verification one: every number on your page is labelled measured, derived, or assumed. If nothing is assumed, you are not being honest; if everything is, you have not looked at the artifacts.

Verification two: state the peak as a rate over a window, and state the volume at which this design stops being appropriate. Both numbers, on the page.

Verification three: for every data structure, one sentence naming the operation it makes cheap and the cost you accepted. If your reason is "it is the standard choice", you have not made a decision.

Verification four: walk the request path aloud and ask at each hop, "what is the time limit here, and what happens when it is exceeded?" A hop with no answer is a hop with no timeout.

Verification five: count the queues and confirm each has a limit and a stated behavior at the limit.

Verification six: the double-submit test. Describe exactly what happens when the same submission arrives twice, and confirm it is a different mechanism from what happens when two people report the same real event.

Verification seven: the degradation statement. Write the single sentence describing what the system does when triage falls behind arrival — and confirm it does not include the word "queue" without a bound.

Verification eight: run the batch, write what broke, and keep the list. Then read your design and confirm it addresses at least the first two failures you actually observed. [pause]

## Your project

Here is the handoff. The project guide asks you to design the intake-to-triage flow.

The goal is a design that states its capacity assumptions out loud and survives its own worst case on paper. The constraints: numbers before diagrams, every number labelled; no appeal to infinite scale and no autoscaling hand-wave; every data-structure choice carries the operation it optimizes and its complexity; and you must break your own design with a real batch before you defend it.

The artifacts are a load-assumption table, a data-structure decision list with reasoning, a request-path diagram through queue, triage, and notification, one failure mode and graceful response per boundary, and the observed result of a large batch run with what it exposed.

Nothing here requires you to build the system. This is a design chapter, and the design is the deliverable — plus the evidence from breaking the small thing you already have. [pause]

## Recap

What to carry forward.

Get four numbers before you draw anything: typical volume, peak as a rate over a window, response time as a percentile, and retention. Estimate from artifacts, label each number's provenance, and state the volume at which the design expires.

Separate what must be fast from what must merely be reliable. Acknowledge the operator synchronously and cheaply; do the expensive thinking asynchronously.

Choose structures for stated operations: maps for identity, queues for decoupling, heaps when the queue is genuinely large, sets for deduplication where the hard part is the key, append-only logs for audit with a separate read model.

Fear work that grows with load, not work that is slow. "For each of these, check all of those" is the phrase to catch.

Idempotency answers "is this the same submission"; deduplication answers "is this the same real-world event." Different mechanisms, both required.

Every queue has a bound and a stated behavior at the bound. Every call has a timeout. Every retry has a delay, a cap, and jitter.

Degrade deliberately: your deterministic rule is the cheap, reliable part, so a storm should produce fast rule-based priorities with expensive suggestions marked pending.

And break the small version before you defend the big one. Your batch run is worth more than your diagram.

In chapter six we take this design and give it a shape that can survive a second customer: bounded contexts, dependency direction, and the boundary between a reusable core and one customer's adaptation. Bring the failure list from your batch run — chapter six's architecture has to account for it.

That is chapter five. Go design the path, then go break it.
