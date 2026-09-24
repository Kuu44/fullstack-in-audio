---
chapter: 38
title: "Capstone: complete applications, an observable agent, and customer handoff"
part: "Part VII — Deliver value in the customer environment"
roadmap_nodes: "Complete Apps; Complete App with Observability; Build your Agent"
narration_voice: en-US-AndrewNeural
narration_rate: "-10%"
audio: media/38-capstone-handoff.mp3
guide: docs/guides/38-capstone-handoff.md
---

# Chapter thirty eight. Capstone. Complete applications, an observable agent, and customer handoff.

Welcome to chapter thirty eight of FullStack in Audio, the final chapter, and the exam.

I want to be precise about what kind of exam this is, because it is not a knowledge test. There is no new topic in this chapter. Everything you need, you have already built. What is being tested is whether the whole thing holds together when you are not helping it, and whether you can hand it to other people in a state where they are willing to take responsibility for it.

That is a different question from any question you have answered so far. For thirty seven chapters you have built components, and every one of them worked while your attention was on it. You knew which command to run. You knew that the pipeline needed refreshing before that lookup would succeed. You knew that if the proposal came back empty you should check the index revision. All of that knowledge lives in your head, and none of it is in the system.

The capstone removes you from the loop and asks what is left.

Let me state the three properties that a complete application has to demonstrate, because they are distinct and they are verified in completely different ways.

It works together. That is integration, and it is not the same as having working components. Integration failures live at the seams, and seams are exactly what component tests do not cover.

It can be diagnosed. That is observability, and the standard is not that you have dashboards. The standard is that one identifier follows one piece of work across every boundary, so that a person who did not build the system can reconstruct what happened.

And it can be handed over. That is transferability, and it is verified only by other people successfully doing things without you speaking. You practiced that in chapter thirty seven and now it counts.

Three properties, three different kinds of evidence. Most projects that fail at this stage have the first, believe they have the second, and have never tested the third.

## Part one. What a complete application actually means.

Complete does not mean feature complete. Chapter thirty four's whole argument was that feature completeness is not the goal and often not desirable. Complete means boundary complete. Every path a real user can take either works, or fails in a way that is safe, visible, and documented. There are no paths that end in a spinner, a stack trace, a silently dropped record, or a state that requires you to open a database console.

So let me give you the concept that organizes this entire chapter: the seam census.

A seam is any place where one part of your system hands work to another part that could fail independently. List the seams in FieldOps Copilot and you get something like this. The browser to the interface layer. The interface to the system of record. The interface to the cache. The interface to the pipeline's read model for asset context. The agent to its read only lookup tool. The agent to retrieval. The agent to the model provider. The service to the notification path. Continuous integration to deployment. The runtime to its configuration and secrets. And everything to observability.

That is about eleven seams, and here is the claim I want you to take seriously: essentially all integration failures happen at those eleven places, and each of them needs four things defined. A contract, meaning what is exchanged. A failure mode, meaning what happens when the other side does not answer or answers wrongly. A timeout, meaning how long you wait before deciding it failed. And a fallback, meaning what the user sees and what the system does instead.

Now go and check. In practice you will find two or three seams where one of those four is undefined, usually the fallback, and usually at a seam you consider unimportant. That census hour is the highest yield hour of the entire capstone.

Next, observability completeness, and I want to give you a sharp test rather than a vague aspiration. Take one incident. Name every hop it makes. Then confirm that a single correlation identifier appears at every one of those hops, in an artifact somebody else can query. If the identifier is present at nine hops and absent at two, then your system is diagnosable in nine places and a mystery in two, and the two will be exactly where the problem is, because the places you did not instrument are the places you did not understand.

Then release readiness, which is a different thing from working. A readiness review is a set of gates, each with an evidence artifact attached, and I use six.

Functional: the acceptance criteria from chapter thirty three pass, with their instruments. Safety: the abuse cases fail safely and the governance controls from chapter thirty two are in place. Operability: health checks report truthfully, alerts fire, and the runbook has been validated by someone other than its author. Reproducibility: the environment can be rebuilt from reviewed artifacts alone. Evidence: the evaluation baseline exists at pinned versions, traces exist, dashboards exist. And reversibility: rollback has been executed and timed.

Notice something about those six. Only the first is about whether the software does what it should. The other five are about whether an organization can safely depend on it, and they are the five that most engineering teams treat as paperwork.

Finally, agent readiness, because one of this chapter's roadmap nodes is building your agent and I want to give you the exam for it explicitly. Five properties, each with an artifact.

Grounded: every recommendation cites a source passage or declines with insufficient evidence. The artifact is a set of runs including a weak evidence case that correctly declined.

Bounded: the agent cannot take a consequential action, and the reason it cannot is that no such capability exists in its tool set, not that a prompt asks it nicely. The artifact is the tool inventory plus a rejected attempt.

Approval gated: a human event is required before anything changes, and that event is recorded. The artifact is an audit record naming the person.

Evaluated: a baseline exists at pinned versions, including negative and safety cases, and a deliberate regression is detectable. The artifact is the evaluation result stored against the release manifest.

Observable: every proposal records the instruction version, the model, the retrieval index revision, its latency, and its cost. The artifact is one proposal from which you can reconstruct exactly what produced it.

Grounded, bounded, approval gated, evaluated, observable. If you can produce those five artifacts, you have built an agent that an enterprise can deploy. If you can only demonstrate that it gives good answers, you have built a demo.

That distinction deserves one more sentence, because it is the most common confusion in this field right now. Quality and safety are not the same property. An agent that is right ninety five percent of the time is a quality claim. An agent that cannot do harm when it is wrong is a safety claim. Enterprises are buying the second one, and a great many demonstrations only prove the first.

## Part two. Why the capstone is where an FDE is actually judged.

Four reasons.

First, everything works in isolation is the normal condition of a project that is about to fail. It is not a sign of health. It is the default state, and it is the state in which every optimistic status update gets written. The transition from component health to system health is where projects go wrong, and it goes wrong quietly, because nobody is testing the seams.

Second, this chapter tests judgment rather than knowledge, and judgment is visible in what you choose to show and what you choose to admit. Anyone can demonstrate a working feature. What distinguishes a professional is showing the boundary, naming the residual risk, and declining to claim something the evidence does not support, in front of people who would have believed the claim. That is the behavior that gets you invited back.

Third, a handoff is a transfer of accountability, and accountability can only be transferred when the evidence is legible. Somebody at the customer is going to put their name against operating this system. They will do it if they can see how it fails, how to recover it, how to reverse it, and what it costs. They will not do it because you assured them it is fine, and they should not.

Fourth, and this is the frame I want you to keep from this whole course: the actual output of forward deployed engineering is a decision made by someone else. Everything you built exists so that three people can each decide something. A sponsor decides whether to continue and what to fund. An operator decides whether to use it on a real shift and whether to recommend it to a colleague. A security reviewer decides whether it may touch real data and under what conditions. Your system is not the deliverable. Their decisions are, and your system is the instrument that lets them decide well.

## Part three. How to run the capstone.

Ten moves. This is the exam procedure.

Move one: freeze and pin, before you test anything. Create the release manifest for the candidate: application version, instruction or prompt version, model and provider, embedding model, retrieval index revision, infrastructure definition revision, and configuration set. Give it a name. From this moment, you are not testing the system. You are testing one specific, named artifact.

This matters more than it sounds. An integration test against a moving target produces results nobody can interpret. If you fix something midway, every result before the fix belongs to a different system than every result after it, and when someone later asks whether the evaluation baseline applies to what was deployed, the honest answer will be no. Pin first. Then, if you find something that must change, you change it and you produce a new pinned candidate and you rerun what needs rerunning, deliberately, with the version recorded.

Move two: run the seam census against the pinned candidate. Eleven seams or however many yours has, and four questions each: contract, failure mode, timeout, fallback. Write the answers down. Where an answer does not exist, you have found a defect before it found you, and it goes on the list to fix in this chapter rather than being discovered by an operator in month two.

Pay particular attention to two seams that are usually weakest. The notification path, because chapter thirty four probably deferred the real integration and a bridged or manual path is easy to leave undefined. And the pipeline read model, because asset context being stale rather than missing is a subtle state, and subtle states are where undefined behavior hides.

Move three: the golden path run, and this is the centerpiece, so I am going to give you a rule that will feel unreasonable.

Take one synthetic incident and take it all the way. Intake through the workspace with real authentication. Server side validation. Persistence with the idempotency key. Asset context from the pipeline read model, correctly labeled as found, not found, or stale. Retrieval with the tenant filter applied. An agent proposal with a citation to a specific procedure passage. The operator's decision to approve, edit, or reject. The audit record naming who decided and when. The notification attempt, recorded whether or not it succeeded. And finally the trace and the dashboard, reflecting all of it.

Now the rule. During that run you may not touch anything. No manual database edit. No restarting a component to make it cooperate. No refreshing the pipeline because you know it needs refreshing. No clearing a cache. No let me just. If you intervene in any way, the run is void, you write down what you intervened in, you fix that thing properly, and you start over from the beginning.

That rule is the entire test, and I want to explain why it is not pedantry. Every intervention you make is a piece of operational knowledge that lives only in your head. Each one is a step that is missing from the runbook, or a defect that has been invisible because you have been silently compensating for it. In a customer environment at two in the morning, you will not be there to intervene. The void-and-restart rule is the only mechanism I know that reliably surfaces the compensations you have stopped noticing you make.

Expect the first attempt to fail. That is normal and it is the point. Most people need three or four attempts, and the list of interventions from the failed attempts is the most valuable artifact the capstone produces.

Move four: the adversarial passes. Four of them, all against the pinned candidate.

First, the evaluation suite. Run it at pinned versions and compare to your baseline. Record the result against the manifest, so that the evaluation evidence and the deployed artifact are permanently linked. This is what makes the phrase evaluated release mean something.

Second, the abuse cases. At minimum four. Prompt injection embedded in incident text, attempting to make the agent ignore its instructions or reveal its instructions. A cross tenant retrieval attempt, checking that the isolation is enforced at the retrieval layer and not merely in the interface. An attempt to make the agent perform a write or a consequential action. And an authorization bypass attempt on a normal operation, such as an operator attempting an administrator only action. For each, the pass condition is not merely that it failed. The pass condition is that it failed safely, that the failure was visible in the audit trail or the logs, and that a person reviewing the evidence could tell it had been attempted.

Third, the dependency failure pass, and here is where I want to raise the standard above what most teams do. Take each dependency down in turn: the system of record, the cache, the model provider, the pipeline data, the retrieval index. For each, the test is not does the system survive. Anyone can check that it did not crash. The test is three parts. Does the user see the documented behavior, exactly as your runbook describes it. Does the alert fire, and is the alert actionable. And does the runbook entry match what actually happened.

That third part is the one that catches people. You will find at least one case where the system behaves sensibly, the alert fires, and the runbook describes something subtly different from reality, because the runbook was written from your understanding and the system was built from your implementation, and those two drifted. Fix the runbook, and note that you found it, because finding it is a pass, not a failure.

Fourth, the rollback rehearsal. From the pinned candidate back to the previous approved manifest, executed from the written steps, timed, and performed by someone other than the person who wrote the steps. Then restore forward and verify with an instrument.

Move five: exercise the agent under realistic conditions rather than curated ones. This is the move that separates a capstone from a demonstration, and it is the one most often skipped, because curated inputs are so much more pleasant to work with.

Everything you have run against the agent so far has been chosen by you. Your evaluation fixtures are deliberate. Your golden path incident is clean. Your abuse cases are targeted. All of that is necessary and none of it resembles a Tuesday afternoon in an operations team. So now you build a realistic batch, using the volume profile you measured back in chapter thirty three, and you run the system against the shape of real work rather than against your best examples.

Four properties of the batch matter.

The mix. Your volume profile told you what fraction of intake is duplicates or reopens, and what the ambiguity distribution looks like. Reproduce those proportions. If a third of real intake is duplicate, then a third of your batch is duplicate, and now you are testing the idempotency path and the deduplication behavior at the rate they will actually be exercised, rather than as a single unit test.

The burst. Your profile gave you a peak hour as a multiple of the median. Compress a peak hour's worth of incidents into a peak hour's worth of time and see what happens. This is where you learn whether your latency target holds where it matters, because a ninety fifth percentile measured at median load is a comfortable number that tells a customer nothing about their worst afternoon.

The messiness. Real incident text is not well formed. It has fragments, missing fields, copied email chains, contradictory statements, three problems described as one, and the occasional item that is not an incident at all but a request for a password reset. Generate a synthetic batch that includes those, and then watch specifically for one behavior: does the confidence signal actually move. A system whose confidence is high on a fragment with no service named is a system whose confidence signal is decoration, and you would very much rather discover that here than in front of a security reviewer.

And concurrency. Two operators working the same incident at the same time. An approval arriving while a proposal is still being generated. A pipeline refresh running while a lookup is in flight. These are the states that produce the strangest bugs and the ones your single threaded golden path cannot reach.

Now measure four things across the batch. Latency at the ninety fifth percentile under burst, against your chapter twenty three budget. Cost per triage under burst, against your ceiling, remembering that difficulty drives longer contexts and retries so cost rises exactly when volume does. The refusal rate, meaning how often insufficient evidence was returned, and whether it rose on the messy inputs as it should. And the correctness of the state machine: no incident left in an intermediate state, no proposal orphaned, no audit gap.

One caution about interpreting this pass. You are not trying to produce an impressive number. You are trying to find the load at which the system stops behaving as documented, and then to state that number honestly in the handoff packet. A system with a known, stated limit is deployable. A system with an unknown limit is a system whose limit will be discovered by an operator during an outage.

Move six: turn the golden path into an automated end to end suite, so that it is a repeatable instrument rather than a heroic afternoon. You proved the path works once, by hand, under the void-and-restart rule. That was the exam. But a single manual proof decays the moment anyone changes anything, and the customer's engineers will change things.

So automate the scenario: create an incident through the real interface layer with a real authenticated identity, assert persistence and the idempotency behavior, assert asset context resolves and correctly labels its freshness, assert retrieval applies the tenant filter, assert the proposal returns with a citation, perform the approval, assert the audit record names the actor, and assert the trace exists with the correlation identifier present at every hop.

Two design rules make this suite useful rather than a maintenance burden. Assert on observable outcomes rather than on internal implementation, so that a refactor does not break it and a behavior change does. And keep the model provider replaceable with your deterministic fake from chapter fifteen, so the suite runs without credentials and without network access, then keep a small separate live path that runs against the real provider deliberately, on a schedule, with synthetic data.

Then wire it into the pipeline you built in chapter twenty seven, alongside the evaluation gate. Now the golden path is not something you did once. It is a gate, which means the customer's engineers can change the system and find out in minutes whether they broke the seam between intake and audit. That is the difference between handing over a working system and handing over a system that stays working.

And notice what you have just done for the person who follows you. The end to end suite is documentation that executes. Chapter thirty seven's runbook tells a stranger what to do when something breaks; this suite tells them, automatically, that something broke and where. Those two artifacts together are most of what transferability actually means.

Move seven: the readiness review, six gates, each with its artifact. Functional, safety, operability, reproducibility, evidence, reversibility.

I want to isolate reproducibility, because it hides the most and it is the one that turns a pilot into a deployment. The test is a cold rebuild. Destroy the nonproduction environment entirely and recreate it from the declared infrastructure and the pinned manifest alone, using only reviewed artifacts, with no undocumented steps and nothing from your shell history.

This test is uncomfortable and it is the single most honest thing you can do in this chapter. Almost everyone discovers at least one manual step that was never written down: a secret that was set by hand, a database extension that was enabled once, a bucket that was created in a console, a permission granted in a moment of debugging. Every one of those is a step that would have blocked a real deployment, and finding them in a rehearsal costs you an afternoon rather than a change window.

Move eight: design the demonstrations backwards from decisions. Three audiences, three demonstrations, three decisions. This is not one demo given three times.

For the sponsor, the decision is continue, adjust, pause, or stop, and what to fund next. Their evidence type is usually traceable numbers plus a brief working demonstration. So show the workflow outcome against baseline with the confidence labels visible, show coverage and confirmation rates, show the running cost with the ceiling and the fallback, then a short live run. And show one failure that speaks to their concern: the cost ceiling engaging and the fallback behaving. That converts an anxiety about unbounded spend into a demonstrated control. Then ask for the decision, with the four options genuinely on the table, by a stated date.

For the operator, the decision is whether they will use it on a real shift and whether they will tell a colleague to. Their evidence type is working software in their own hands. So give them the keyboard, use their vocabulary, walk their own workflow, and show the failure that speaks to their concern: the case where evidence is weak and the system declines rather than guessing. Explain why declining is the behavior that protects them. Then ask them directly whether they would use it on Monday, and if the answer is qualified, capture the qualification, because that is your adoption risk stated in their words.

For the security reviewer, the decision is whether this may proceed toward real data and under what conditions. Their evidence type is artifacts they can file. So walk the threat model, the data classification with retention, the control mapping, and the audit trail, then show the failure that speaks to their concern: a live cross tenant retrieval attempt being blocked and appearing in the log. Then ask what conditions they require, and write them down as conditions, because a security reviewer's conditional yes is the most valuable sentence in the engagement and it must be recorded verbatim.

Three rules across all three demonstrations. Use the pinned candidate and pinned synthetic data. Rehearse in the actual environment you will present from, because an unrehearsed environment is where demos die. And never present from a laptop only you can run; that is a statement about the system, and everyone in the room will hear it.

Move nine: assemble the handoff packet, with an index, and with an owner for every document. The contents: the revised charter, the architecture diagrams, the release manifest, the risk control pack, the operator quick start and the engineering runbook, the return on investment model with its assumptions and labels, the feedback and decision process, and the open decisions. Add the acceptance criteria results, the evaluation baseline at pinned versions, the timed rollback record, and the residual risk register.

Two things make this a packet rather than a pile. First, every document has a named owner on the customer side, not just on yours, because a document nobody owns is a document that will be wrong within a quarter. Second, the packet contains a section titled what is not true yet. That section lists what the pilot did not prove, what is bridged or manual, what is deferred with its trigger, and what would need to change before real customer data. Writing that section is the most professional act in this chapter, and it is the one most likely to be quietly skipped in order to protect the mood of a good meeting.

Move ten: close honestly, with three lists and a date. Evidence produced, meaning what you now know that you did not know before, with instruments and confidence labels. Risks remaining, each with an accountable owner and the customer decision it requires, and with implemented controls clearly separated from future commitments. And conditions for a real data launch, stated as a checklist someone could work through.

Then the date. The pilot decision date, agreed, in writing. Without it you get chapter thirty five's pilot purgatory: a system that neither dies nor scales, consuming attention indefinitely while the sponsor's interest slowly decays.

## Part four. Pitfalls.

Fixing during the golden run. The most tempting and most damaging. Every silent fix is an operational secret you are keeping from the customer, usually without realizing it.

Testing the system rather than a pinned artifact. Produces evidence that cannot be tied to anything deployed.

Believing integration is verified by component tests. It is not. Your component tests pass at every seam's edges and say nothing about the seam.

Dependency failure tests that only assert survival. The real test is whether the documented behavior, the alert, and the runbook all agree with reality.

Skipping the cold rebuild. Guarantees that undocumented manual steps are discovered during a real deployment, in a change window, in front of an audience.

Rollback rehearsed by its author. Rollback is a procedure for a stranger under stress, and the author is neither.

Demonstrating a feature tour instead of driving to a decision. Everyone enjoys it, nobody decides anything, and you will need another meeting you cannot easily get.

Presenting from an environment you did not rehearse in, or from a machine only you can run.

Overclaiming in the readout. Chapter thirty five gave you the claims boundary; this is where the temptation to breach it peaks, because the results are in and you want them to be good.

Conflating quality with safety. Presenting an accuracy figure as though it addressed the question of what happens when the system is wrong.

Handing over documents without transferring capability. A packet delivered is not a capability transferred; chapter thirty seven's silent transfer test is the only proof.

Omitting or softening residual risk to protect a good meeting. It will surface later, and it will surface as something you concealed rather than something you disclosed.

And no decision date, which is how a successful pilot becomes a permanent experiment.

## Part five. Verification. The exam checklist.

Here is what must be true, and each item is a demonstration rather than an assertion.

One synthetic incident completed end to end, with no manual repair and no intervention of any kind. You can name every hop it made, and a single correlation identifier is present at every hop in an artifact somebody else can query.

The agent's five properties each have an artifact: a declined weak evidence case for grounded, a tool inventory plus a rejected attempt for bounded, an audit record naming a person for approval gated, an evaluation result stored against the manifest for evaluated, and one proposal from which the instruction version, model, index revision, latency, and cost can be reconstructed for observable.

All four abuse cases failed safely, visibly, and with evidence a reviewer could find.

Every dependency, taken down in turn, produced the documented user visible behavior, an actionable alert, and a runbook entry that matched reality. Every mismatch you found is recorded and fixed.

A realistic batch, matching your measured duplicate share, ambiguity mix, and peak burst, ran against the pinned candidate. You can state the ninety fifth percentile latency and the cost per triage under burst, whether the refusal rate rose on messy inputs as it should, and the load at which the system stops behaving as documented.

The golden path exists as an automated end to end suite that runs without credentials against the deterministic provider fake, asserts the correlation identifier at every hop, and is wired into the pipeline as a gate.

The cold rebuild succeeded from reviewed artifacts alone, and every manual step it exposed is now either automated or documented.

Rollback was executed by someone other than its author, timed, and the restore verified with an instrument.

The evaluation suite ran at pinned versions with its result recorded against the release manifest.

Three demonstrations were delivered, each ending in a recorded decision, or in a recorded refusal to decide together with exactly what the person needs in order to decide. A qualified operator yes is captured in their own words. A conditional security approval is captured verbatim as conditions.

The handoff packet has an index, an owner per document including on the customer side, and a what is not true yet section.

The residual risk register names an accountable owner and the required customer decision for each risk, and separates implemented controls from future commitments.

And there is a pilot decision date, agreed in writing.

## Part six. Your practice handoff.

The companion guide is the capstone test, and it is the longest one in the course. It requires the pinned candidate, the seam census, the golden path run with the void-and-restart rule enforced honestly, the four adversarial passes, the realistic batch under burst, the automated end to end suite wired in as a gate, the six gate readiness review including the cold rebuild, three audience specific demonstrations designed backwards from decisions, the handoff packet with owners, and the honest close with three lists and a date.

Its rubric contains one unusual instruction: you must record your failed attempts, particularly the interventions that voided your first golden path runs. A capstone submission that reports a clean first attempt with no interventions and no runbook mismatches and no undocumented manual steps in the cold rebuild is not a strong submission. It is an unlikely one, and it will be read as a sign that the rules were not enforced.

Hints are inverted at the end. Attempt first.

## Part seven. Recap, and the close of the course.

A complete application is boundary complete, not feature complete: every path either works or fails safely, visibly, and as documented. Integration failures live at seams, so run the census and give every seam a contract, a failure mode, a timeout, and a fallback.

Observability is complete when one identifier follows one piece of work across every hop, in an artifact a stranger can query.

Pin the candidate before testing anything. Run the golden path with no interventions, and treat every intervention as a defect and a missing runbook step rather than as a small convenience.

Prove the agent with five artifacts, not with accuracy: grounded, bounded, approval gated, evaluated, observable. And keep quality and safety separate, because the enterprise is buying safety.

Test dependency failures against the documented behavior, the alert, and the runbook, all three. Do the cold rebuild, because it is where undocumented manual steps live. Rehearse rollback with a stranger and time it.

Design demonstrations backwards from the decision each audience must make, show each audience the failure that addresses their specific fear, and leave every session with a recorded decision or a recorded list of what is missing.

Hand over a packet with owners and a section naming what is not true yet, and close with evidence produced, risks remaining with accountable owners, conditions for a real data launch, and a decision date.

And now the close of the whole course.

In chapter one you invented a customer, wrote a charter for a problem you made up, and defined a first release boundary for a system that did not exist. Between then and now you built a semantic, accessible intake surface; a typed operator workspace; a secured service with an authoritative policy; a durable system of record with an audit trail; storage decisions you can defend; a bounded, grounded, approval gated agent with versioned instructions and an evaluation gate; a data pipeline that distinguishes missing from stale; release discipline with pinned versions and rehearsed rollback; containers, a chosen cloud, declared infrastructure, and end to end tracing; and a governance pack with abuse tests. Then in chapter thirty three you did the hardest thing in the course, which was to hold all of that up against evidence and let the evidence change it.

That arc is the job. Not the individual technologies, which will be different in three years. The arc: from an ambiguous customer outcome, through disciplined engineering, to a deployed system that other people can operate, audit, reverse, and decide about without you.

A forward deployed engineer is not someone who can build anything. It is someone who can walk into an unclear situation with real constraints and real politics, find out what is true, build the smallest credible thing that produces evidence, prove that it is safe as well as good, and hand it over so completely that the customer's confidence does not depend on your presence.

You have now done that once, end to end, on a system you built yourself from an empty file. Do it again with a real customer, and keep the rules: evidence before scope, thin slices before grand plans, safety and operability as floors, every input producing a visible decision, and nothing claimed that the instruments do not support.

That is the end of FullStack in Audio. Go and deliver something.
