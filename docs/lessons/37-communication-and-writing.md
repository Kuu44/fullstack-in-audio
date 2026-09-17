---
chapter: 37
title: "Communication and technical writing"
part: "Part VII — Deliver value in the customer environment"
roadmap_nodes: "Communication; Technical Writing"
narration_voice: en-US-AndrewNeural
narration_rate: "-10%"
audio: media/37-communication-and-writing.mp3
guide: docs/guides/37-communication-and-writing.md
---

# Chapter thirty seven. Communication and technical writing.

Welcome to chapter thirty seven of FullStack in Audio. This is the last chapter before the capstone, and it is the one that determines whether everything you have built belongs to the customer or belongs to you.

Here is the test I want you to hold in your head for the whole chapter. It is not, can the customer run this system after I leave. That framing is too comfortable, because leaving is a scheduled event you can prepare for. The real test is: can the customer run this system right now, at two in the morning their time, while you are on a plane and unreachable, when something has failed in a way nobody anticipated. If the answer is no, the system is not delivered. It is on loan.

That is what this chapter is about, and I want to name the genre precisely, because it is not the same thing as documentation.

Documentation, as most engineers imagine it, is written for a calm reader with time, who wants to understand a system. Field writing is written for someone who is stressed, interrupted, partially informed, working outside their expertise, and looking for one specific thing. They are not reading. They are scanning, under pressure, with a consequence attached. Design for that person and your writing works for the calm reader too. Design for the calm reader and your writing fails exactly when it matters.

And there is a second reason this chapter matters more than its position in the roadmap suggests. An FDE's influence travels through documents. You cannot be in two customer environments at once. Every hour you spend being the only person who knows something is an hour of your capacity permanently committed to one account. Writing is the only mechanism by which a field engineer scales, and it is also, not coincidentally, the mechanism by which the customer becomes willing to depend on the system in production.

## Part one. What we are actually writing.

There are four genres in field writing, they have four different jobs, and mixing them is the single most common defect I see in delivery documentation.

Explanatory writing answers why the system is the way it is. Architecture overviews, decision records. It is read once, carefully, usually by someone new or someone reviewing, and then referenced later when a decision is questioned. Its virtue is completeness of reasoning. Its unit is the argument.

Procedural writing tells someone what to do. Runbooks, quick starts, deployment steps. It is read under pressure by someone who wants to stop reading as soon as possible. Its virtue is unambiguous executability. Its unit is the verifiable step.

Reportorial writing says what is true right now. Status updates, incident notes, pilot readouts. It is read by people who have to decide something. Its virtue is the clean separation of what is known from what is guessed. Its unit is the labeled claim.

Reference writing describes what exists. Interface contracts, configuration indexes, error catalogues. It is looked up, never read front to back. Its virtue is findability and completeness. Its unit is the entry.

Now the failures that come from blending them. A runbook that explains the architecture is a runbook that nobody can execute at two in the morning, because the reader has to wade through reasoning to find an action. A decision record that reads like a status update loses the reasoning entirely, so in six months nobody can tell whether the decision was considered or accidental. A status update written as a chronology, Monday we did this and Tuesday we did that, forces the reader to reconstruct the situation themselves, which is exactly the work they were hoping you would do. And an interface contract that reads like a tutorial cannot be looked up.

So: choose the genre before you write the first sentence, and hold to it. If you find yourself wanting to explain inside a procedure, put one line saying why this matters and a pointer to the explanation, and continue with the steps.

Next, the audience model. For each document, know four things about the reader. What they already know. What they need to decide or do. What they will do immediately after reading. And what vocabulary they own.

That last one deserves attention, because it is where engineers reliably fail. In chapter thirty three you collected interview transcripts. Those transcripts contain the customer's actual words for things: what they call an incident, what they call a handoff, what they call the person who owns a service. Use their words, not yours. If your operators say job and your interface says incident, then your quick start is already generating friction on its first line. This is not a style preference; shared vocabulary is a functional requirement of a procedure.

Then the habit that I consider the highest value single thing in this chapter: epistemic labeling. In field writing, distinguish five kinds of statement, explicitly, so the reader never has to guess which one they are looking at.

A confirmed fact: something observed or measured, with its instrument. An assumption: something you are relying on that has not been verified. An inference: a conclusion you have drawn from facts, which may be wrong even though the facts are right. A decision: something that has been settled, by someone, on a date. And a request: something you need another person to do.

Here is why this matters more in field work than anywhere else. Your writing gets forwarded. The status update you send your sponsor will be pasted into an email to their director with your careful context removed. If your facts and your guesses look identical on the page, then in the forwarded version they are identical, and eventually one of your guesses will be quoted back to you as a commitment. Labeling is not pedantry. It is how you survive being forwarded.

Let me make it concrete. An unlabeled sentence: the slowdown was caused by the model provider and should be resolved by tomorrow. Now the labeled version. Confirmed: response times exceeded the budget for about forty minutes, measured from the traces. Inference: the provider's own status page reported degradation in the same window, so that is the most likely cause, though we have not proven it. Assumption: we are assuming this was not caused by our own change that morning, which we will verify today. Decision: the fallback response is enabled until we confirm the cause. Request: we need confirmation from your platform team that no network change occurred in that window, by end of day.

Same event. The second version is longer and enormously more useful, and notice that it can be forwarded without becoming a lie.

## Part two. Why this is a first-class engineering responsibility.

Five reasons.

First, the bus factor of one is a commercial problem, not a hygiene problem. A customer will not commit a system to production if operating it requires a specific person from a supplier. This is not distrust of you; it is basic institutional prudence. Every gate in chapter thirty five's enterprise readiness map is, in part, asking the question: can we run this without you. Your runbook is the answer to a procurement question.

Second, prose fails under pressure. This is a fact about human cognition, not a matter of taste. Under stress, working memory narrows and reading comprehension for continuous text degrades badly. People scan for imperatives, numbers, and names. Every paragraph you write in a runbook is a paragraph that will be skipped, and if the essential step is in the middle of it, it will be missed. Write procedures as short numbered actions with expected observations, and you are designing for the brain that will actually be reading.

Third, writing is how approvals happen. The security review wants a document. The change board wants a document. Procurement wants a completed questionnaire. Architecture review wants a diagram with ownership boundaries. In chapter thirty five you mapped each gate to an artifact you already had, and the one gap for most engagements is the runbook, which is exactly what this chapter produces.

Fourth, writing protects you. A decision record is the difference between a settled tradeoff and a blame conversation. When someone asks in month five why the system does not automatically assign incidents, an entry that names the two positions, the reasoning, the person who decided, the date, and the measurement that would revisit it ends the conversation in two minutes. Without it, you are defending a choice from memory, against someone's recollection of a meeting they may not have attended, and you will lose even when you were right.

Fifth, and this is the one engineers underestimate: writing surfaces your own confusion. If you cannot write the runbook step for a failure mode, you do not understand the failure mode. Trying to write down what an operator should do when the asset context is stale will force you to discover whether your system actually distinguishes stale from missing, or whether you only believe it does. I have found more design defects while writing procedures than while writing tests. The document is a test of your understanding, run against your own head.

## Part three. How to write the FieldOps handoff.

Eight moves.

Move one: write the purpose sentence before the document. Every document begins with one sentence in this shape: after reading this, a named kind of person can do a named thing without a named dependency. After reading this, a new operator can submit, review, and decide on an incident without asking a colleague. After reading this, an engineer on the customer's platform team can diagnose and recover the five known failures without contacting the supplier.

That sentence is not an introduction. It is the acceptance criterion for the document, and it is what you will test in move seven. Write it first, and delete anything in the document that does not serve it.

Move two: the operator quick start. Aim for something a person can read in five minutes and keep beside them. Five sections, and the fifth is the one everyone omits.

What this is, in two sentences, in their vocabulary, including what it explicitly does not do. Setting expectations here prevents the expectation mismatch class of feedback from chapter thirty six.

When to use it and when not to. Name the cases that do not belong in the system, because those cases exist and an operator meeting one for the first time should not have to guess.

The core workflow, as numbered actions with expected observations: submit an incident; read a proposal, including how to see the reason and the source it came from; approve, edit, or reject; and confirm the record is saved.

How to tell whether to trust it. This is the section that determines adoption. Explain what the confidence signal means in plain terms, what insufficient evidence means and why it is a good behavior rather than a failure, and what the operator should do in that case. If your system declines to answer and nobody explained why declining is a feature, operators will read it as brokenness.

And, what to do when it is wrong. The reporting path, exactly what information to include, where to find the identifier that lets an engineer trace it, and what happens next, meaning who will look at it and when they will hear back. That last part is the loop from chapter thirty six made visible to the person at the keyboard. A quick start without this section teaches operators that being wrong is their problem to absorb silently, and that is how you lose the feedback that a pilot exists to produce.

Move three: the engineering runbook, and there is one structural decision that matters more than everything else in it. Index it by symptom, not by component.

At two in the morning, the person reading has a symptom. Proposals are not appearing. The interface is slow. Operators say the owner shown is wrong. An alert fired about the pipeline. They do not have a diagnosis, and a runbook organized by component, with a section for the cache and a section for the retrieval index, requires them to already know the answer in order to find the answer. Organize by observable symptom, and let each symptom entry lead to the components.

Start with a health check section: how to establish in under a minute whether the system is broadly healthy. Then, for each known failure: the symptom as an operator or an alert would describe it; the first check, which should be a single action with a clear expected observation; a short decision tree; the remediation steps; how to verify recovery; and the escalation path.

Two rules about escalation. Name people and hours, not teams. Contact the platform on-call is not actionable at two in the morning. And state what information to bring, so the escalation arrives with the trace identifier and the timeline rather than with the word broken.

Your system already has at least five known failures, and you have met all of them. The database is unreachable, which you saw in chapter twenty eight when you added health checks. The cache is unavailable, which chapter fourteen required to be survivable. The model provider is timing out, or the cost ceiling has been reached and the fallback has engaged, from chapter twenty three. The asset pipeline is stale, so context is present but old, which chapter twenty four required to be distinguishable from missing. And the retrieval index does not match the current runbook revision, which chapter twenty made you verify. Write those five properly and your runbook is genuinely useful, because those are the failures that will actually happen.

Move four: the decision record index. You do not need to write new decision records; you have been writing them since chapter two. What is missing is an index, because a pile of records is not a navigable artifact. One line per decision: what was decided, why, in one clause each, plus its status, its date, and, in field work, the trigger that would revisit it. That revisit trigger is the same discipline as chapter thirty four's deferral triggers, and it turns a decision log into a live document rather than an archive.

Move five: write the same event twice, for two audiences. Take one incident, the model provider degrading for forty minutes, and produce a sponsor status note and an operator incident note.

The sponsor note leads with impact and the ask. The system was slower than target for about forty minutes this morning; operators could still triage manually throughout and no incident was lost; the most likely cause was our provider, which we are confirming; the fallback behaved as designed; we need your platform team to confirm no network change occurred in that window by end of day. Notice: impact first in their terms, causal detail compressed to one clause, and a specific request with a person and a deadline.

The operator note leads with what to do. Between these times this morning, proposals may have taken longer than usual or shown the fallback message; the incidents you triaged manually are recorded correctly and nothing needs redoing; if you see a proposal that looks stale from that window, reject it and triage manually; the system is back to normal and here is how to report anything that still looks wrong. Notice: no provider names, no architecture, no cause, because the operator cannot act on cause. But the impact is never omitted, and the reassurance is specific rather than general.

The rule that generalizes: adjust vocabulary, causal depth, and the ask to the audience. Never adjust the facts, and never omit the impact.

Move six: give every reportorial document a next-update time. In an incident note, this is the single most important line, and it is the one most often missing. What is happening, the impact in user terms, what we know, what we do not know, what we are doing, and when you will hear from us next. That last line converts anxiety into waiting. Without it, every stakeholder becomes a polling loop against you, at exactly the moment you have the least attention to spare.

Move seven: verify by transfer, and stay silent. This is the only verification that counts, and it is the move that makes this chapter a test rather than an essay.

Hand your runbook to a peer who did not build the system. Inject a synthetic failure. Then say nothing. Not a hint, not a clarification, not a well-what-I-meant-there. Watch where they stall, and write down every stall with its location in the document.

Every word you speak during that exercise is a step missing from your document. That is the whole lesson. Your instinct to help is the enemy of the artifact. Sit on your hands, let them struggle, record the struggle, then fix the document and run it again with a different failure.

Do the same for the quick start with someone who has never seen the system. Count the questions they ask. Each question is a defect with a location.

Move eight: plan for rot, because documents decay silently while code fails loudly. Attach each document to a change trigger rather than to a review date. The runbook is reviewed when the release manifest changes. The quick start is reviewed when the operator-visible workflow changes. The architecture overview is reviewed when a component or boundary changes. The decision index is updated when a decision is made, which means the update belongs in the same act as the decision.

Then put the documentation obligation into the release checklist from chapter twenty seven, so it is gated rather than remembered. And date every diagram and every screenshot, with the release they depict. An undated screenshot of an interface that has since changed is worse than no screenshot, because it teaches a new operator something false with an air of authority.

Move nine: make the diagrams answer questions rather than depict everything. You have been drawing diagrams since chapter four, and by now you probably have several: the full stack seam, the intake to triage flow, the component split with its reusable and customer specific boundaries, the landing zone, and the trace path. The temptation at handoff time is to merge them into one authoritative picture of the system. Resist it. A diagram that shows everything answers nothing, because the reader has to filter it themselves, and filtering is the work you were supposed to do for them.

So the rule is one diagram per question, with the question written as the title. Not FieldOps Copilot architecture, but: which components hold customer data. Not system overview, but: what happens to an incident from submission to audit record. Not deployment, but: what runs where, and who owns each boundary. When the title is a question, the diagram has an acceptance criterion, and you can tell whether it succeeded: does a reader who had that question now have an answer.

Three diagrams cover most handoff needs. A context diagram showing the system, the people, and the external systems it touches, which is what a security reviewer and an architecture board want first. A flow diagram following one incident through the components, which is what a new engineer needs to build a mental model and what an operator's escalation depends on. And a boundary diagram showing what is reusable core, what is customer configuration, and what is customer specific adapter, which is the diagram that prevents the next engineer from accidentally forking your product.

Then four rules that keep diagrams from becoming liabilities. Every diagram carries a date and the release it depicts, for the same reason screenshots do. Every diagram has a legend, because the meaning of a solid versus dashed line is obvious only to its author. Arrows must mean one thing consistently, and you must say which thing: either the direction data flows or the direction dependency points, never both in the same picture. And ownership belongs on the diagram. A box with no owner is a box that will be nobody's problem during an outage, and marking ownership on the picture is the cheapest way to surface the fact that one component has no owner at all, which you would much rather discover now than during an incident.

One more piece of craft. The most valuable annotation you can add to a flow diagram is the failure behavior at each boundary. A small note saying what happens here when this call fails turns a picture of the happy path into an operational document, and it costs you one line per boundary. It also, reliably, exposes a boundary where you do not know the answer.

Move ten: write the engineer onboarding guide, which is a different document from the runbook and is routinely conflated with it. The runbook answers what do I do when something is wrong. The onboarding guide answers how do I become someone who can change this system safely. Its reader is the customer's engineer, or your own colleague replacing you, and its purpose sentence is something like: after reading this and following it, an engineer new to FieldOps can make and ship a small change without supervision.

Five sections do the work.

What the system is for, in about a paragraph, aimed at the reason it exists rather than at the technology. Someone who does not know why the approval gate exists will eventually remove it to reduce friction, and they will be sincerely trying to help.

How to get it running locally, as executable steps with expected observations at each one, and with the prerequisites and access requirements stated at the top. Then the single most useful line in the document: how to tell that it is working. A new engineer's worst hour is the one where they cannot distinguish a broken environment from a broken understanding.

The map: which part of the code does what, in a handful of lines, oriented around the flow diagram rather than around the directory structure. Directory listings are reference material; a new engineer needs a narrative.

The rules that are not obvious from reading the code. This is the section that earns its keep. The AI path may only propose, never act. The priority policy has exactly one authoritative implementation and the interface must not reimplement it. Every suggestion records the instruction version that produced it. Tenant isolation is enforced at retrieval, and a change that makes retrieval convenient is a change that can break isolation. No real customer data in any development environment. Each rule gets one sentence of why and a pointer to the decision record. Without this section, every constraint you carefully built is a puzzle that the next engineer will solve by removing it.

And the first change: a specific, small, real task for their first day, with the verification steps and the review expectation. Give them something genuine, ideally something on your deferred list that is small and safe. A first change that they complete and ship teaches more than any amount of architecture prose, and it exercises your own documentation in the most honest way possible, because if the onboarding guide is wrong they will find out immediately and you will find out from them.

Notice the pattern shared by both of these moves and by everything else in this chapter. The document is not the deliverable. The reader's changed capability is the deliverable, and the document is only the instrument. That is why every verification in this chapter involves a person doing something while you watch, rather than you rereading your own prose and finding it clear.

## Part four. Pitfalls.

Writing for your future self. Your future self shares all of your context, so a document that satisfies them will fail a stranger. Write for the stranger.

Organizing the runbook by component. It requires the reader to have the diagnosis before finding the diagnosis.

Steps without expected observations. Restart the service is not a step. Restart the service; within about thirty seconds the health endpoint should report healthy; if it does not, go to the next section. That is a step.

Missing prerequisites and permissions. The reader gets to step four and discovers they need an access level nobody mentioned, at two in the morning, with no way to get it. Put required access, credentials, and tools at the top.

Undated diagrams and screenshots. They rot invisibly and then mislead confidently.

Explaining architecture inside a procedure. One line of why, a pointer, and move on.

Status updates as chronologies. Nobody wants your week. They want the current state, the change since last time, and the decision required.

Hedging that hides a fact, and confidence that hides an assumption. Both are failures of the same discipline: label the claim.

Incident notes without a next-update time.

The words simply, just, and obviously. Each one is a small insult to a reader who is struggling, and each one is usually covering a step you did not want to write out.

Documentation as a phase at the end. Write the runbook while you build the failure handling, because that is when you understand it, and because writing it is how you discover the handling is incomplete.

The demo standing in for the quick start. A demo is a performance you were present for. It transfers nothing to the person who joins next month.

Escalation paths that name teams instead of people and hours.

And never testing a document with a human. An untested runbook is a hypothesis about your own clarity, and that hypothesis is usually false.

## Part five. Verification.

The silent transfer test. A peer executes your runbook against an injected failure while you say nothing. Pass condition: they recover the system, and every stall is recorded and fixed. If you spoke, the test is void; fix the document and rerun.

The stranger test. Someone who has never seen FieldOps completes the core operator workflow using only the quick start. Count their questions. Zero questions is suspicious, one or two is realistic, five means the document has five defects and you know their locations.

The two-in-the-morning test. Give someone a symptom, not a diagnosis, and time how long it takes them to find the right runbook entry. If it is over a minute, your index is organized around your mental model rather than theirs.

The labeling test. Take a status update and ask a reader to separate the confirmed facts from the assumptions and inferences. If they cannot do it reliably, an unlabeled guess is going to be forwarded as a fact.

The why test. Pick a decision that was settled months ago and see whether the decision index answers why, and what would change it, in under a minute.

The freshness test. Every diagram and screenshot carries a date and a release. Any that do not are presumed wrong.

The ask test. Every status update contains a specific request naming a person and a date, or explicitly states that nothing is needed. Both are acceptable; ambiguity is not.

The vocabulary test. Read your quick start against your chapter thirty three transcripts and count the places where you used your word instead of theirs.

## Part six. Your practice handoff.

The companion guide is a test. You will produce an operator quick start, an engineering runbook indexed by symptom covering the five failures you have actually met, a decision record index with revisit triggers, a sponsor status update and an operator incident note for the same event, and operator-facing release notes. Then you will verify them by transfer, in silence, with someone else's hands on the keyboard.

The rubric is harsh in two specific places. First, any procedural step without an expected observation fails. Second, any spoken help during the transfer test voids that test. There is also a required negative demonstration: you must record at least one place where the exercise revealed that your system's behavior, not your writing, was the actual defect, because that is the most common and most valuable outcome of writing procedures properly.

Hints are inverted at the end. Attempt first.

## Part seven. Recap.

The test of your writing is whether the customer can operate the system at two in the morning while you are unreachable. Field writing is for a stressed, interrupted reader who is scanning, not reading.

Four genres with four jobs: explanatory for why, procedural for what to do, reportorial for what is true now, reference for what exists. Do not blend them.

Label your claims. Confirmed fact, assumption, inference, decision, request. Your documents get forwarded with your context removed, and labeling is what stops a guess becoming a commitment.

Write the purpose sentence first and treat it as the document's acceptance criterion. Give the operator quick start a section on how to tell whether to trust the system, and a section on what to do when it is wrong, including who will respond and when.

Index the runbook by symptom, never by component. Give every step an expected observation. Put prerequisites and access at the top. Name people and hours in escalation paths, and say what information to bring. Cover the five failures you have actually met: unreachable database, unavailable cache, model timeout or cost ceiling, stale pipeline, and mismatched retrieval index.

Write the same event twice for two audiences, changing vocabulary, causal depth, and the ask, never the facts and never the impact. Put a next-update time on every incident note.

Verify by transfer and stay silent, because every word you speak is a step missing from the document. Then attach each document to a change trigger and gate it in your release checklist, because documents rot quietly while code fails loudly.

In the next chapter, everything comes together. The capstone is the full FieldOps Copilot pilot candidate: the integrated system, an end-to-end synthetic scenario traced from intake to audit, the evaluation suite and abuse cases, a dependency-failure fallback, a rollback rehearsal, the complete handoff packet, and a demonstration to a sponsor, an operator, and a security reviewer, each of whom needs to leave with a decision.
