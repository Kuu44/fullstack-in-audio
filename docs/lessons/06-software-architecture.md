<!-- tts:skip -->
## TTS notes — chapter 6

- Voice: `en-US-AndrewNeural`, rate `-14%` (about 146 words per minute).
- No code, no configuration syntax, no file paths. Architecture is described in words.
- Recurring cast: Dana (sponsor), Sam (coordinator), Priya (security), Marcus (platform), Ana (second engineer).
- New this chapter: Coastline, a second customer.
- `[pause]` becomes a beat of silence at segment turns.
- Nothing in this block is spoken.
<!-- /tts:skip -->

Welcome back to FullStack in Audio. This is chapter six: software architecture for customer-specific systems. It is the last chapter of part one, and it is the one that decides whether everything you build afterwards is an asset or a trap. [pause]

Let me start with the phone call that defines this chapter.

The Harborline pilot is going well enough that your own organization is excited. Someone in sales has been talking to a grocery distributor called Coastline — twelve distribution centres, a similar operations desk, a similar incident problem. They want the same thing. Can we deploy FieldOps Copilot for them in six weeks?

Now, here is the fork in the road, and it is both a metaphor and a literal version control operation.

Path one takes about three days. You copy the Harborline repository, rename things, change the severity vocabulary — because Coastline says "urgent" and "routine" instead of four levels — swap the notification integration, adjust the priority weights because perishability matters differently in grocery than in logistics, and ship it. It works. Everyone is delighted. You are a hero for approximately five months.

Then Harborline finds a bug in the priority rule. You fix it in the Harborline repository. Does anyone fix it at Coastline? Maybe, if someone remembers. Then Coastline asks for a feature that Harborline would also love, and now it exists in one place only. Then a security fix has to be applied in two places, by two different people, in two codebases that have drifted for five months. Then a third customer arrives, and someone copies whichever repository they happened to see first.

Path one is not a shortcut. It is a loan at a punitive interest rate, and the payments are made by whoever comes after you.

Path two takes maybe three weeks instead of three days, and it asks a different question: what is genuinely the same about these two customers, what is a setting, and what is truly specific to one of them?

This chapter is about how to answer that question without either extreme — without the copy-paste fork, and without the fantasy architecture that tries to make everything configurable and ends up understandable to nobody.

## What architecture actually is, at this size

Architecture is the set of decisions that are expensive to change later. That is the whole definition, and it is a useful one because it tells you what deserves the name and what does not.

Which library you use for parsing is not architecture; you can swap it in an afternoon. Where the customer's policy lives, what depends on what, and which boundaries have contracts — those are architecture, because changing them later means touching everything.

For a customer-specific system there are four architectural ideas you need, and I am going to teach them as decisions rather than as patterns.

### Modularity and bounded contexts

A module is a piece of the system with a name, a job, and a boundary. The question that makes modules real is: what does this module know about, and what is it deliberately ignorant of?

From chapter five's design, FieldOps has a natural set: intake, which receives and validates reports; triage policy, which decides urgency; the incident record, which is the durable truth; AI assistance, which produces suggestions; integrations, which talk to systems you do not own; and audit and observability, which record what happened.

A bounded context is the stronger version of that idea: inside this boundary, words have one specific meaning. This matters more than it sounds, because language is where customer-specific systems rot first. "Incident" means one thing to your intake module — a report from a human, possibly duplicated, possibly nonsense. It means something else in the triage context — a validated record with a priority. And it means something else again in the customer's maintenance system, where an incident might be a work order with a budget code attached.

If you let those three meanings share one concept, you will end up with a single sprawling object that has fields for everything, most of them empty most of the time, and nobody can tell you which fields are valid when. The discipline is to translate at the boundary and keep each context's language clean.

### Dependency direction

This is the most powerful idea in the chapter, and it takes a minute to see why.

Every dependency is an arrow: this thing needs that thing in order to work. Your architecture's health is largely determined by which way the arrows point.

The rule is that your domain — the customer's policy, your priority rule, the rules about what a valid incident is — should depend on nothing. Not on a database, not on a web framework, not on a notification provider, not on a model provider. Everything else depends on it. The arrows point inward, toward the policy.

Why does this matter in field work specifically? Three reasons, and they are all practical.

You can test the policy without infrastructure. Chapter one said the system must be explainable and auditable; chapter two made the rule pure. If your triage policy depends on a database connection, then testing your customer's business rules requires a database, and the tests get slow, flaky, and eventually skipped.

You can swap the infrastructure without touching the policy. Harborline is in one cloud with one notification system; Coastline may be in a different cloud with a different one. If the notification provider is a detail behind a boundary, that is a small change. If the policy calls the provider directly, it is a rewrite.

And you can deploy without the dependency. This is the one people miss. If your triage policy does not depend on the model provider, then the model provider being down does not stop triage. Chapter five's graceful degradation was not just an operational trick — it was made possible by the direction of an arrow.

The shorthand for this shape is ports and adapters. A port is a hole in your domain shaped like a need: "I need to notify somebody", "I need to store an incident", "I need a suggestion." An adapter is a specific thing that fills the hole: this notification service, that database, that model provider. The domain defines the shape of the hole; it does not know which adapter is plugged in.

That is the sentence to remember: the domain defines the shape of the hole.

### Configuration boundaries

Now the question that decides whether your second customer takes three days or three weeks: what varies between customers, and how is that variation expressed?

There is a ladder here, from cheapest to most expensive, and the skill is to always reach for the lowest rung that genuinely works.

The lowest rung is a configuration value. A severity vocabulary, a set of priority weights, a latency threshold, a depot list. Different data, same code. Changing it requires no deployment of new logic and, ideally, no deployment at all. If a customer difference can be a value, make it a value.

The second rung is declarative policy — a rule expressed as data rather than as code. "For this customer, any incident at a depot in the northern business unit routes to the regional team." That is a routing rule, and it can be a table of conditions and outcomes that your engine interprets. More powerful than a value, still not code.

The third rung is an adapter. The customer has a genuinely different external system, so you write a new implementation of an existing port. New code, but isolated code, and the core does not know it exists.

The fourth rung is an extension point in the core: a place where the core explicitly invites customer-specific behavior. Use this sparingly, and only when the shape of the variation is understood well enough to name.

And the fifth rung is the fork. This is not architecture; it is the absence of architecture. Sometimes it is genuinely the right call — a one-off proof of concept for a customer who may not proceed, with a written expiry date and a decision about who deletes it. But it should be a conscious, documented, dated decision, not something that happens because a Thursday was busy.

Here is the judgment that comes with experience: do not build rungs you do not need yet. An extension point designed for a variation you have not seen is almost always the wrong shape, and now you own it. Two customers is when patterns start to be visible. One customer is when you should keep the boundary clean and the machinery absent. [pause]

## Why this is an FDE problem and not a general architecture problem

Product engineers do this too, but the forward deployed engineer faces a specific and uncomfortable version of it, and the discomfort is structural.

You are rewarded on this engagement. Your customer needs this quarter's outcome, your sponsor is watching, and the fastest path to a working system is always to special-case whatever this customer needs. Meanwhile the cost of that choice lands on a different quarter, a different engineer, and often a different team — the product organization that has to absorb your customization, or the next field engineer who inherits a codebase with nine unexplained conditionals named after companies.

So the professional discipline is this: you are accountable for the outcome of this deployment and for the shape of what you leave behind. Both. Anyone can have one of the two.

Which gives you a concrete practice. Every time a customer-specific need arrives, ask three questions, out loud, in this order.

Is this a difference in data, or a difference in behavior? Most customer differences that look like behavior are actually data wearing a disguise. Severity vocabularies, weights, routing destinations, thresholds, escalation timings — all data.

If it is behavior, is it a variation on something the core already does, or something genuinely new? A variation belongs behind an existing port. Something new might belong in the core as a capability the core does not yet have — which is a product conversation, not a field hack.

And: if the next customer asks for the opposite, does my design break? This is the best test I know for a customer-specific decision. If Coastline wanted the inverse of Harborline's routing rule and your design cannot express it, you have not built a boundary; you have hard-coded one customer's answer in a nicer font.

There is a fourth question, and it is about honesty in the other direction, because over-abstraction is also a failure. Am I building this configurability because two customers need it, or because I imagine they will? One customer's need plus imagination equals speculative machinery. Two customers' needs equals evidence. Wait for the second customer whenever you can afford to. [pause]

## A worked example: routing by business unit

Let me walk the example your project asks you to record as a decision, because it is the archetypal customer-specific rule.

Harborline organizes its forty depots into three business units — northern, central, and port operations — and each unit has its own maintenance team and its own escalation manager. When an incident is triaged, it should be routed to the right unit's queue, and escalation should reach that unit's manager.

The tempting implementation is a conditional in the triage code: if the depot code starts with N, route to northern. It takes four minutes to write and it is wrong in five separate ways. It puts customer data in source code. It requires a deployment to onboard a new depot. It cannot be reviewed by the customer, who is the only party who actually knows the mapping. It is invisible to an auditor. And when Coastline arrives with regions instead of business units and a different escalation structure, the conditional multiplies.

The better shape starts by naming what varies. The mapping from a depot to a business unit is data — it is Harborline's organizational structure, and it changes when they reorganize, which they will. The mapping from a business unit to a destination is also data. The *idea* that incidents route somewhere based on where they came from is core behavior, shared by every customer of this kind.

So the core owns the concept: every triaged incident has a routing destination, determined by a routing policy. The policy is data the customer owns. And the actual delivery to a destination is a port, with adapters per customer — Harborline's notification system today, Coastline's something else later, and a fake one for tests.

Now notice three things this shape gives you for free.

Onboarding a depot is a data change, which means an administrator can do it and nobody deploys anything. That single property will save you more calendar time across a pilot than any performance work you will ever do.

The customer can review their own routing rules, because they are readable data rather than code. Dana can check them. That is the difference between a system the customer owns and a system they merely use.

And you can test the whole path — incident arrives, gets triaged, gets routed, notification is requested — with no notification provider anywhere in the test, because the port has a fake adapter. Your customer's most important behavior becomes testable in milliseconds.

One caution so you do not overshoot. Do not build a general rules engine on day one. Harborline's routing is "depot maps to unit, unit maps to destination." Two lookups. Implement the two lookups, keep them as data, and leave the general expression language alone until a second customer proves you need it. The architectural win here is not the sophistication of the mechanism; it is that the customer's organizational facts are not in your source code. [pause]

## Onboarding Coastline, item by item

Let me run the second-customer exercise properly, because it is the verification that makes this whole chapter concrete, and it is your project's hardest rubric line.

Coastline arrives with six differences. I will classify each one out loud, and I want you to notice that the classification is the architectural work — the code that follows is usually small.

Difference one: severity vocabulary. Harborline uses four levels; Coastline uses "urgent" and "routine". That is a value. A list of accepted terms, with a mapping onto the internal scale your rule uses. No new code, no deployment of logic. If your intake validation has the four Harborline words written into it, this difference costs you a code change and a release — which tells you the words were in the wrong place all along.

Difference two: priority weights. Perishability dominates in grocery distribution in a way it does not in general logistics. Also a value — the weights your chapter two rule multiplies. The rule's shape is the same; its coefficients belong to the customer. Notice how much this vindicates keeping the rule pure and parameterised rather than clever.

Difference three: organizational structure. Harborline has three business units; Coastline has regions, and a region can contain sites belonging to two different maintenance contracts. This one is policy data, and it is also the one where you must be careful: it is genuinely a different *shape*, not just different values. So the question becomes whether your routing concept — origin maps to group, group maps to destination — can express two hops with a contract dimension, or whether it assumed one hop. If it assumed one hop, this is where you learn it, and the honest answer might be that the core routing concept needs to become slightly more general. That is a legitimate core change, made on evidence from two customers, which is exactly the right reason to change a core.

Difference four: notification system. Different vendor entirely. That is a new adapter behind the existing port. Isolated code, no core change, and your fake adapter means you can build and test the rest of Coastline's deployment before that vendor's credentials are even approved.

Difference five: they want a field on intake that Harborline does not have — a temperature reading, because that is what matters for their refrigerated stock. This is the interesting one, and the tempting answer is a generic custom-fields mechanism. Resist it for now. Ask instead whether this is one customer's field or the beginning of a category. If Harborline would also record equipment readings given the chance, this is a core capability you are discovering, and it should be designed as one. If it is genuinely Coastline-only, an extension point or an adapter-supplied field is the smaller move. The wrong answer is a general dynamic schema built for a sample size of one.

Difference six: they want incidents automatically assigned, without operator approval. And here is the most important classification in the list: that is not an architecture question at all. That is a chapter-one question about human authority, and the answer may well be no — not because the system cannot do it, but because the risk boundary in your charter says a human disposes. Some customer differences are not configuration; they are requests to change a decision that exists for a reason. Recognizing which is which is senior work, and the honest response is to take it back to the sponsor and the security reviewer rather than to quietly add a setting.

Count the outcome: two values, one policy-data question that may generalise the core, one adapter, one deliberate deferral, and one escalation to a human decision. Zero forks. Six weeks is plausible. And nothing about Harborline's deployment changed while you did it. [pause]

## Drawing the diagram so it is actually used

Two words about the artifact itself, because most architecture diagrams are decorative and yours has to survive contact with Marcus, Priya, and Ana.

Draw at two levels, not one. The first level is the system in its environment: FieldOps Copilot, the people who use it, and the external systems it touches — the customer's identity provider, the notification system, the model provider, the asset source that arrives in chapter twenty-four. This is the picture Priya wants, because every line leaving your box is a place data crosses a boundary, and her entire job is those lines.

The second level is inside the box: your components — intake, triage policy, incident record, AI assistance, integrations, audit — and the direction of the arrows between them. This is the picture Ana wants, because it tells her where to put a change.

Resist the third level. A diagram showing every class is a diagram that is wrong within a week and that nobody reads.

Then do the thing that makes the diagram unusually useful: shade it into three groups. Reusable core. Customer configuration. Customer-specific adapter. That single visual distinction turns a picture of components into an argument about ownership, and it is the fastest way to answer the question your own product organization will eventually ask you — "how much of what you built at Harborline can we ship to everyone?"

And put the arrow directions on it honestly. If your triage policy really does import the database client today, draw that arrow, even though it is the arrow you are ashamed of. A diagram that shows the intended architecture instead of the actual one is worse than no diagram, because it is a map that will send someone the wrong way in a hurry. If intent and reality differ, draw reality and mark the intended change. That is an artifact people trust. [pause]

## Interface contracts, stated in plain language

Your project asks for two contracts in plain language: intake to triage, and triage to notification. Let me be precise about what a contract has to say, because most people write half of one.

A contract names what crosses the boundary, in domain language. Intake hands triage a validated incident: identity, the fields your charter promised, the arrival time, the reporter, and the idempotency key from chapter five. Not a database row and not a web request — a domain object with a defined meaning.

It names what the receiver promises. Triage promises to produce a priority and a band for every accepted incident, using the deterministic rule, with a recorded reason, within a stated time.

It names what happens when the promise cannot be kept. If triage cannot reach the model provider, it still produces the rule-based result and marks the suggestion pending. If it cannot record its result, the incident stays queued and is retried. Notice that this section is where chapter five's failure modes live — the contract is where a design decision becomes a commitment.

It names who is authoritative. Chapter four's question, now written down where both sides can see it.

And it says whether the boundary is synchronous or asynchronous, because that single property changes everything about error handling, retries, and duplicates. If triage is asynchronous, the contract must state that a message may be delivered more than once, which forces the receiver to be idempotent. If you leave that unstated, someone will assume exactly-once delivery, and they will be wrong in production.

Write these in prose a customer engineer can read. A contract that requires your codebase to understand is a comment, not a contract. [pause]

## The failure modes

The first failure is the fork, and I have already argued it. The tell is a repository named after a company.

The second failure is the customer conditional: a branch in your core logic keyed on a customer's name. It starts as one, and one is always defensible. Then there are nine, in six files, and no single person knows what any given customer's behavior actually is. The reliable warning sign is a condition that names an organization rather than a capability.

The third failure is the god configuration: everything is configurable, the configuration is enormous, nothing has a sensible default, and two settings can contradict each other. This is over-correction from the fork, and it fails a different way — your customer's behavior is now defined in a document nobody can reason about, and you have moved the complexity rather than reducing it. A useful discipline: every setting needs a default that is correct for a typical customer, and a stated consequence for changing it.

The fourth failure is the leaky boundary. You defined a port for notification, and its shape is exactly the shape of the first provider you integrated — its field names, its error codes, its quirks. The second adapter then has to pretend to be the first one. The tell is a port whose vocabulary comes from a vendor rather than from your domain.

The fifth failure is inverted dependencies: your domain logic imports the database library, or the model client, or the web framework. Now your customer's policy cannot be tested, deployed, or reasoned about without infrastructure. This one creeps in quietly, usually through a convenient type or a logging helper.

The sixth failure is architecture theatre — layers, interfaces, and indirection for a system with one customer and four hundred records a day. Every abstraction is a thing a new engineer must understand before they can change anything, and Ana has three weeks. Abstraction has a price and the price is paid in comprehension.

The seventh failure is the configuration that requires a deployment. If adding a depot means a code change, a review, a build, and a release window, then your "configuration" is source code with extra steps, and the customer cannot own their own data.

And the eighth, subtle and common: the boundary that exists in the diagram and not in the code. You drew intake, triage policy, and integrations as separate components, and in the codebase they are one file that touches all three. A boundary is only real if crossing it requires going through the contract. If you can reach across it accidentally, it is decoration. [pause]

## How you verify this chapter's work

Verification one, the second-customer test, and it is the strongest one available to you. Take your architecture and describe how you would deploy it for Coastline: a different severity vocabulary, different priority weights, different routing structure, different notification system. Then classify every change as a value, a policy data change, a new adapter, or a core change. If any of it is a core change, ask whether that is genuinely a new capability or whether your boundary is in the wrong place.

Verification two, the no-provider test: can you exercise intake through triage through routing to a notification request without any real notification provider present? If not, your port is not a port.

Verification three, the dependency direction check. Name what your triage policy depends on. If the list includes a database, a web framework, a model client, or a cloud service, the arrow is pointing the wrong way.

Verification four, the vocabulary check: for each bounded context, say what "incident" means inside it. If the answer is the same everywhere and includes fields that are empty most of the time, you have one sprawling concept rather than several clean ones.

Verification five, the reversal test: pick your customer-specific rule and imagine the next customer wants the opposite. Can your design express it without new code? If not, the boundary is a hard-coded answer.

Verification six, the administrator test: can the customer's own administrator change the routing data without an engineer, a build, and a release? If not, that is a real limitation and it belongs written down, with its cost.

Verification seven, the Ana test. Give the diagram to an engineer who has not seen the system and ask them two questions: which parts are reusable, and where would you add a customer-specific behavior? If they cannot answer from the diagram alone, the diagram is not doing its job — and the diagram is the artifact that outlives you. [pause]

## Your project

Here is the handoff. The project guide asks you to define the FieldOps Copilot architecture.

The goal is an architecture that separates the reusable core from one customer's adaptation, so that the second customer does not require a fork of the first. The constraints: components, boundaries, and dependency direction only — no framework selection, and no premature code beyond one interface boundary you actually exercise. Customer-specific behavior must be reachable through configuration or an adapter rather than by editing core logic. Your interface contracts must be in plain language and testable without a real notification provider.

The artifacts are a component diagram marking what is reusable core, what is customer configuration, and what is a customer-specific adapter; two plain-language interface contracts; an architecture decision record for business-unit routing; and one inward-pointing dependency demonstrated behind a small interface — which is the only code you need to write this chapter.

That last artifact matters. A diagram is a claim. One working interface boundary with a fake adapter behind it is evidence. [pause]

## Recap, and the end of part one

Architecture is the set of decisions that are expensive to change later. Everything else is just choices.

Bounded contexts keep language clean. "Incident" means different things in intake, in triage, and in the customer's maintenance system, and translating at the boundary is cheaper than one sprawling concept.

Dependency direction is the most powerful idea here. The domain depends on nothing; everything depends on the domain. The domain defines the shape of the hole, and adapters fill it. That is what lets you test policy without infrastructure, swap providers per customer, and keep working when a provider is down.

Reach for the lowest rung of the customization ladder that genuinely works: a value, then policy as data, then an adapter, then an extension point, and only then — consciously, with a date and an owner — a fork.

Ask of every customer-specific need: is it data or behavior; is it a variation or something new; and would the opposite request break my design?

Do not build rungs you do not need. One customer plus imagination is speculative machinery. Two customers is evidence.

Write contracts in plain prose: what crosses, what the receiver promises, what happens when the promise fails, who is authoritative, and whether the boundary is synchronous.

And a boundary is only real if crossing it requires going through the contract.

That closes part one. Look at what you have: a charter naming a customer outcome; a priority rule that is pure, specified, and implemented in four languages; a working command-line program an operator could use; a repository a second engineer could take over; a design with real numbers and named failure modes; and an architecture that can survive a second customer. Not one line of that is a framework tutorial, and all of it is the judgment the rest of the course is built on.

Part two puts a human in front of it. Chapter seven is frontend foundations — semantic markup, labels, keyboard paths, and an accessible intake page that a supervisor can complete under pressure, at three in the morning, on a laptop in a warehouse. Bring your architecture: the browser is about to become the first real adapter plugged into the seam you just drew.

That is chapter six. Go define the architecture.
