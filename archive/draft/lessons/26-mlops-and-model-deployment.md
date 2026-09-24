---
chapter: 26
title: "MLOps, model deployment, and managed ML services"
slug: 26-mlops-and-model-deployment
part: "Part V — Move and operate the data and model workflows"
roadmap_nodes: ["MLOps", "Model Deployment", "Managed ML Services"]
voice: en-US-AndrewNeural
rate: "-18%"
audio: media/26-mlops-and-model-deployment.mp3
companion_guide: docs/guides/26-mlops-and-model-deployment.md
---

# Chapter 26 — MLOps, model deployment, and managed ML services

> Narration script. Headings, frontmatter, and blockquotes are stripped before rendering; only the prose below is spoken.

Welcome to chapter twenty-six, the last chapter of Part Five. Over the previous two chapters you gave FieldOps Copilot a dependable data path: a contract, a pipeline, a schedule, retries, backfills, and a read model that knows how fresh it is. Today we apply the same discipline to the part of the system that has, so far, been changing with no discipline at all. The intelligence.

Let me be precise about what we are doing, because the term MLOps carries baggage. In its original setting, MLOps is the practice of operating machine learning systems you train: managing training data, experiments, model artifacts, a registry, deployment of those artifacts to serving infrastructure, and monitoring for drift. You are not training a model in FieldOps Copilot. You are calling somebody else's. A reasonable person might conclude that MLOps therefore does not apply to you.

That conclusion is wrong, and understanding why is the heart of this chapter. MLOps exists because machine learning systems have a property that ordinary software does not: their behavior is determined by things that are not source code. In a classical system, if the code did not change, the behavior did not change. In a machine learning system, behavior depends on the model artifact, the data it saw, and the configuration around it, and any of those can change while the code stays identical. Everything MLOps does is a response to that one fact.

Now look at your system. Your triage behavior depends on the application code, yes. But it also depends on the prompt version, the model you selected, the provider serving it, the decoding settings such as temperature, the tool schemas you exposed, the retrieval index and its contents, the embedding model that built that index, the chunking strategy, the number of results you retrieve, and the freshness of the asset read model. Not one of those is your application's source code. Every one of them changes what the copilot says. You have exactly the problem MLOps was invented for. You just do not have a training loop.

So today we build release discipline for AI behavior. The organizing artifact is a release manifest, and by the end of this chapter you should find it faintly alarming that anybody ships an AI feature without one.

Let us start with the vocabulary, mapped onto your system rather than onto a training pipeline.

The first idea is the configuration surface: the complete set of things that can change behavior without changing code. I just listed yours. Write your own version of that list, because the exercise is revealing. Most teams discover two or three items they had never considered configuration, and those are precisely the ones that will surprise them later. The commonest omission is the provider's model version, which we will come back to, because it is the one you do not control.

The second idea is versioning, which here means something stricter than usual. A version is useful only if it is immutable and identifying. Immutable means that once you have assigned a version, the thing it names can never change. Identifying means that if two runs report the same version, they used the same thing. If your prompt version is a file that people edit in place, it satisfies neither, and it is worse than having no version at all, because it provides false confidence. The same applies to your retrieval index: reindexing produces a new revision, and that revision must be nameable.

The third idea is the registry, which is simply the place where versioned artifacts live with their metadata, and where you can look up what a version contains. In classical MLOps this is a model registry holding trained artifacts. In your system it is more modest: versioned prompts, versioned tool schemas, versioned index revisions, and a record of which provider models you have qualified. The value is not the storage. It is that a version identifier can be resolved to the actual content by somebody who was not there when it was created.

The fourth idea is environments. You need at least three boundaries, and the word boundary matters more than the word environment. Development is where you work, where breaking things is free, and where only synthetic data exists. A pilot or staging environment is production-shaped: it runs the same artifacts, uses the same deployment path, and is where evaluation evidence is generated. Production is where real customer data lives and where changes require approval. The boundary is defined by three things: what data may exist there, who may change it, and what evidence is required to promote into it. If those three answers are the same for two of your environments, you have two names for one environment.

The fifth idea is promotion. A release moves through environments, and it moves as an immutable unit. This is worth emphasizing because it is where most teams cheat. Promotion does not mean rebuilding in the next environment. It means taking the exact artifact that passed the gate and running it somewhere else. If you rebuild, you have not promoted anything, you have created a new thing that you are hoping resembles the tested one.

The sixth idea is the deployment strategy, of which you should know three. A direct replacement swaps old for new everywhere at once; it is simple, and it makes every user your test group. A canary sends a small share of traffic to the new version, watches the signals, and expands if they hold. A shadow deployment runs the new version alongside the old on the same inputs, discards its output, and compares. Shadow is unusually well suited to AI changes: you can run a candidate prompt against real incoming incidents, never show its output to anybody, and compare its proposals against what the current version said and what the operator eventually decided. You get production-realistic evidence with zero user exposure. The cost is doubled inference spend for the duration, which is a budget conversation and usually a short one.

The seventh idea is rollback. Rollback is returning to a previously approved release. The test of whether you truly have rollback is uncomfortable but simple: can somebody who is not you, at two in the morning, restore the previous behavior in a few minutes using written instructions? If rollback requires editing a prompt back to what it used to be from memory, you do not have rollback. You have hope.

The eighth idea is drift, and in your system it has a particular flavor. Classical drift is the world changing so that a trained model's assumptions stop holding. You get that too: the customer reorganizes, their runbooks change, new equipment classes appear, and your prompt's examples slowly stop matching reality. But you also get a form that classical MLOps rarely has to handle, which is that the model underneath you can change without your involvement. A provider updates a model behind a stable name, deprecates a version, adjusts safety filters, or changes default behavior. Your code did not change. Your prompt did not change. Your outputs did. Any deployment where you cannot detect that is a deployment where a customer will discover it before you do.

Which brings us to managed machine learning services, because the mitigation for that risk is bound up with where inference happens.

Think of a spectrum. At one end you call a provider's public interface for a hosted model. You manage nothing, you get the newest capabilities quickly, you pay per use, and you accept that the model, its availability, its pricing, and its policies are outside your control. In the middle sit managed platform services from the major clouds: they host models for you, often including open-weight models, within your cloud account, your network boundary, and your identity system. You gain isolation, regional control, and a version you pin, and you pay for provisioned capacity rather than only for what you use. At the far end you host the model yourself on your own compute, which gives you maximum control and hands you every operational responsibility that comes with it, including hardware, scaling, and the fact that a model of meaningful capability is an expensive thing to keep running.

For a forward deployed engineer, the choice is rarely about which is technically best. It is about four customer-shaped constraints. The first is data boundary: may customer data leave their cloud tenancy or their region at all? For many regulated customers the answer is no, and that single answer eliminates most of the spectrum. The second is procurement: is there already a contract with this vendor? Adding a new vendor to an enterprise can take longer than building the entire pilot, whereas using a service under an existing cloud agreement can be a formality. The third is operational capacity: who will look after this after handover? A managed endpoint that scales itself is a very different obligation from a cluster of accelerators. The fourth is economics: usage-based pricing is efficient at low and spiky volume and becomes expensive at sustained high volume, while provisioned capacity is the reverse. Pilots are almost always low and spiky.

My general guidance for a pilot is to start at the hosted-provider end for speed, with a hard requirement: the abstraction boundary you built back in chapter fifteen must be real enough that moving to a managed service inside the customer's cloud is a configuration and adapter change, not a redesign. State that portability claim out loud, and then prove it at least once by running your evaluation suite against a second provider. A portability claim you have never exercised is marketing.

Let me put the risk in a scene, because this is the chapter where the abstract cost of poor release discipline becomes very concrete.

A pilot has been running for six weeks. Operator acceptance of the copilot's triage proposals is around seventy percent, which everybody is pleased with. On a Tuesday, acceptance drops to forty percent. The operations manager notices by Thursday and raises it in the weekly call. The delivery team is asked what changed.

Here is what actually happened, and notice that it takes three separate investigations to find out. Someone on the team improved the triage prompt on Monday, a small wording change to reduce verbosity. Separately, the runbook corpus was reindexed on Monday evening because the customer supplied twelve new documents. And separately again, the provider had shifted the default behind the model alias the service was configured with. Three changes, on two days, by two people and one vendor, none of them recorded anywhere that connects to an individual triage proposal.

Now consider the conversation on that Thursday call. Somebody asks whether the artificial intelligence got worse. The honest answer is that nobody knows, and the reason nobody knows is not that the problem is hard, it is that no evidence was retained. You cannot compare Tuesday's proposals to last week's because you do not know what produced either. You cannot roll back because there is no previous state to roll back to, only a series of edits. And you cannot even isolate the variables, because reverting the prompt does not revert the index and neither reverts the provider.

Now run the same scene with the discipline we are about to build. Every proposal carries a release identifier. You pull Tuesday's proposals, see release fourteen, pull last Tuesday's, see release eleven, and diff the two manifests. The diff shows prompt version changed, index revision changed, model version string changed. You roll back to release eleven in five minutes, confirm acceptance recovers over the next day, and then reintroduce the three changes one at a time through the pilot environment with evaluation evidence for each. By the following week you can tell the customer exactly which change caused what, and you have demonstrated something more valuable than a fix: that the system is under control.

The difference between those two scenes is not skill or effort. It is three artifacts: an immutable manifest, a release stamp on every output, and a rehearsed rollback.

Now, why does an FDE need this more than a product engineer?

Because you are accountable for explaining behavior to people who did not build it, sometimes months later, often in a meeting where trust is the actual subject. Three questions will be put to you. Why did the system say this? What changed? How do we go back? Without release discipline, your honest answers are: I am not sure, something in our configuration, and give me a day. With it, your answers are specific, and specificity is what converts a worried stakeholder into a collaborative one.

There is a second reason, and it is about the shape of enterprise approval. Customers do not approve software; they approve changes under a process. When your security reviewer asks how you control changes to the artificial intelligence behavior, the answer they need is procedural: changes are versioned, evaluated against a fixed suite, promoted only with evidence, recorded in a manifest, and reversible. That answer is frequently the difference between a pilot that reaches real data and one that stays in a sandbox forever. Notice that it is not a technical answer. The technical work is what makes the procedural answer true.

And a third reason, which is about your own leverage. A pilot that cannot be rolled back makes you cautious, and caution in the field means slow iteration, which means fewer improvements in front of the customer. Teams with real rollback ship more, because the cost of being wrong is small.

So let us build it. I will walk through the manifest, the environments, the gates, and the rehearsal.

The manifest first. A release manifest is a single record that pins every element of the configuration surface for one release, together with the evidence that justified it. Concretely, for FieldOps Copilot, it should name: the application version, meaning the exact commit or build identifier; the prompt version for every prompt in the system, not just the main one; the model identifier, the provider, and the specific model version string the provider exposes; the decoding settings; the tool schema version; the embedding model and its version; the retrieval index revision along with the count and source of documents in it; the chunking configuration; the retrieval parameters; the asset read model's expected freshness tolerance; the evaluation suite version; and the evaluation results that this release achieved. Finally, it needs provenance: who created it, when, and who approved promotion.

Two properties make this useful rather than decorative. It must be generated, not written by hand, because a hand-written manifest drifts from reality on the second release. And it must be reachable from a running system: an authorized engineer should be able to ask the deployed service which release it is, and get back the identifier that resolves to this record. Then take one more step, the one that pays off during an escalation. Record the release identifier on every triage proposal the system produces. When an operator says the copilot did something odd last Thursday, you open that proposal, read its release identifier, and you know the entire configuration that produced it. That is a five-minute investigation instead of a week of speculation.

Now environments. Define three for the pilot. Development holds synthetic data only, anybody on the delivery team may change anything, and no evidence is required. Pilot is production-shaped, holds synthetic or approved limited data, is changed only by promoting an artifact, and requires a passing evaluation gate. Production-like, or production when the customer gets there, holds real data, requires named approval, and requires both the evaluation gate and a rollback plan. Write those rules down in a table the customer can read, because this table is what your security reviewer wants and it costs you almost nothing to produce.

Then the gates. A promotion gate is a set of conditions that must be true before an artifact moves. For an AI release I want at least four. The deterministic checks from your evaluation suite must pass, meaning valid structured output, no prohibited actions, citations present where required. The quality metrics must not regress below the recorded baseline by more than a stated tolerance. The cost and latency budget from chapter twenty-three must still be met. And the manifest must be complete, meaning no element of the configuration surface is unpinned. That last gate catches the most common real-world failure, which is a release where somebody added a new prompt and nobody versioned it.

Now the provider-version problem, which deserves its own treatment. Wherever your provider offers a specific, pinned model version rather than a floating alias, use the pinned one. A floating alias means your behavior can change overnight. Then add a detector, because pinned versions get deprecated and aliases get updated regardless of your preferences. The detector is simpler than it sounds: run a small, fixed set of evaluation fixtures on a schedule against the production configuration and record the results over time. You are not looking for perfection. You are looking for a step change on a day when you did not deploy anything. That signal is worth a great deal during a customer escalation, because it lets you say, with evidence, that the behavior changed on a specific date without a change on your side, and here is what we are doing about it.

Then rehearsal. A rollback plan that has never been executed is a document, not a capability. So rehearse it. Deploy a release to the pilot environment, confirm the system reports the new release identifier, then roll back to the previous manifest, and confirm three things: the reported identifier reverts, the behavior reverts, and the retrieval index revision reverts too. That third one is where most rehearsals fail, because people version the prompt and forget that the index is also part of the release. If the new release reindexed your runbooks with a different embedding model, rolling back the application without rolling back the index gives you a combination that has never been evaluated, which is arguably worse than the problem you were fixing. So decide, before you need it, whether your index revisions are retained and switchable. For a pilot, retaining the previous index revision is cheap and it converts a frightening rollback into a boring one.

Let me also address monitoring, because deployment without it is just a more organized way of being surprised. In classical MLOps you monitor for data drift and prediction drift. The equivalents in your system are worth naming precisely, and they are mostly things you already have the ingredients for.

The first signal is operator acceptance rate: what fraction of triage proposals the human approves without modification. This is the closest thing you have to a ground-truth quality measure, it comes free from the approval step you built in chapter nineteen, and it is the number the customer will care about most. Track it over time and per release.

The second is the modification pattern. When an operator overrides a proposal, what do they change? If they consistently correct the same field in the same direction, that is a concrete instruction for your next prompt version, and it is far more useful than an aggregate score.

The third is refusal and insufficient-evidence rate. Your agent is supposed to decline when retrieval is weak. If that rate suddenly rises, something upstream broke, most likely the index or the asset read model, and you will find it faster here than anywhere else.

The fourth is structural validity: how often the model returns output your schema rejects. A rise here is often the first visible symptom of a model change underneath you.

The fifth is the cost and latency numbers from chapter twenty-three, which you are already collecting, now broken down per release so that a regression has an obvious suspect.

Two things make these useful rather than decorative. Every one of them must be attributable to a release, which is why the release stamp on each proposal matters so much. And each needs a rough expected range, so a change is visible without somebody staring at a chart. You do not need statistical sophistication in a pilot; you need to notice a step change within a day rather than a month.

One more design point. Promotion should carry the evidence with it. When a release moves to pilot, the evaluation results that justified the move should be attached to the manifest, not sitting in a build log that expires in thirty days. Customers ask for this at the worst possible moment, typically during a security review months later. Making the evidence part of the release record costs a few lines of automation and saves an afternoon of archaeology.

Let me work the managed-hosting decision as an example, because I want you to see how the four constraints actually resolve rather than just hear them listed.

Take a plausible FieldOps customer: a manufacturer with sites in two regions, an existing agreement with one major cloud provider, a security policy that requires customer operational data to remain within their tenancy, a small platform team of four people who already run several workloads, and a pilot volume of perhaps two hundred triage requests a day.

Score the data boundary first, because it is usually the constraint that eliminates options rather than merely penalizing them. The policy says data stays in tenancy. A public provider interface sends incident text outside that boundary. There are two legitimate ways forward: get a documented exception for the pilot on the basis that only synthetic data is used, which is often achievable and is exactly why we have been insisting on synthetic data, or use a managed model service inside their cloud account. Notice that the answer differs by phase. The pilot can run on the public interface with synthetic data under a written exception; real-data launch probably cannot.

Procurement comes next. They have an existing cloud agreement, so a managed service in that cloud is an expenditure under a contract that already exists. A new model vendor means a new vendor assessment, a security questionnaire, a data processing agreement, and a procurement cycle. If your pilot has three months and the vendor cycle takes four, that is not a preference, it is arithmetic.

Operational capacity third. Four people who already have jobs. A managed endpoint that scales itself and is patched by the provider is within their capability. Self-hosting a model on accelerators is not, and pretending otherwise produces a system that degrades the month after you leave.

Economics last, and this is where people usually start, which is why they often reach the wrong answer. Two hundred requests a day is a small number. Usage-based pricing at that volume is trivially cheap. Provisioned capacity in a managed service has a floor cost that runs whether you use it or not, and at pilot volume that floor may well exceed the usage-based cost by a wide margin. So economics argues for the public interface, and data boundary and procurement argue for the managed service, and your job is to make that tension visible rather than resolve it silently.

The recommendation that follows is a phased one, and this is the shape I want you to reach for generally. Run the pilot on the public provider interface, with synthetic data, under a written exception, because it is fastest and cheapest and the pilot's purpose is evidence. In parallel, prove portability once by running the evaluation suite against the managed service in their cloud, so the claim is tested rather than asserted. Then make the real-data launch conditional on the managed service, with the cost implication stated in advance so nobody is surprised by a bill. Write the trigger down: the move happens when real customer data enters the system, not when someone feels ready.

The reason I labour this is that the wrong version of this conversation is extremely common. An engineer picks the hosting model they find most interesting, and then constructs justifications. A customer asks for the cheapest option and gets one that violates their own data policy. Or a team defers the question entirely and discovers at the security review, two weeks before launch, that the architecture they built cannot be approved. The decision matrix takes an hour and it prevents all three.

Let me go through the pitfalls.

The first is versioning the prompt and nothing else. It is the most common partial adoption, and it leaves the majority of your configuration surface unmanaged.

The second is the mutable version. A prompt version that people edit, or an index revision name that gets reused, destroys the property that makes versions useful.

The third is rebuilding on promotion instead of moving the tested artifact.

The fourth is the floating model alias in production.

The fifth is evaluation evidence that is not attached to the release. If the evidence lives only in a transient log, you will eventually be unable to demonstrate that a production release ever passed anything.

The sixth is forgetting that the retrieval index is part of the release.

The seventh is a rollback that has never been rehearsed.

The eighth is treating the fake or deterministic implementation of your model interface as a second-class citizen. Keep it working. When a provider has an outage during a customer demonstration, the ability to switch to a deterministic path that produces sensible, clearly labelled placeholder proposals is the difference between a graceful five minutes and a lost meeting.

The ninth is adopting a heavyweight platform because it has the right name. A manifest can be a generated record in your own store, checked into version control, and it will serve a pilot perfectly. Adopt a platform when the number of releases, models, or people makes coordination the bottleneck, not before.

The tenth is promoting a configuration that no evaluation has ever seen. This happens through combination: prompt version four was evaluated with index revision seven, and index revision eight was evaluated with prompt version five, and somebody deploys four with eight. Gate on the combination, because the combination is what runs.

Now verification. Here is what you should be able to demonstrate.

Ask the running system what release it is, and resolve that identifier to a complete manifest with no unpinned elements.

Take a triage proposal produced last week and recover, from the proposal alone, the exact configuration that produced it.

Attempt to promote a release whose evaluation results are missing or below baseline, and show that the gate refuses.

Change one prompt, run the evaluation suite, and show a new manifest with a new prompt version and attached results.

Perform a rollback to the previous manifest and show the reported release, the behavior, and the index revision all reverting together.

Simulate a provider outage or failure and show the system falling back in a way that is clearly labelled to the operator rather than silently degraded.

And produce the comparison between hosting through a provider interface and using a managed service in the customer's cloud, scored against data boundary, procurement, operational capacity, and economics, with a recommendation and the trigger that would change it.

Your practice handoff is the test in the companion guide. You will define the three environment boundaries, generate a complete release manifest, attach evaluation evidence to promotion, make the running system report its release, stamp that release onto every proposal, compare self-managed against managed hosting against the charter's constraints, and rehearse a rollback including the retrieval index.

To recap. Machine learning systems change behavior without changing code, and that is the entire reason MLOps exists. Your system has a large configuration surface even though you train nothing: prompts, model, provider, decoding settings, tool schemas, embedding model, index revision, chunking, retrieval parameters, and data freshness. Enumerate it, version every element immutably, and pin all of it in a generated release manifest with evaluation evidence attached. Define environments by the data they hold, who may change them, and what evidence promotion requires. Promote artifacts rather than rebuilding them. Prefer pinned model versions and detect changes underneath you with a scheduled fixture run. Choose managed hosting against data boundary, procurement, operational capacity, and economics, not preference. And rehearse rollback, including the index, so that returning to a known-good state is an ordinary operation rather than an emergency.

Part Six begins next chapter, where we take all of this and make it repeatable: continuous integration and delivery, pipelines, artifacts, secrets, and the approval gates that turn your evaluation suite into something a merge cannot bypass.
