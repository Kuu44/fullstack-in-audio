---
chapter: 36
title: "Stakeholder management and the product feedback loop"
part: "Part VII — Deliver value in the customer environment"
roadmap_nodes: "Stakeholder Management; Product Feedback Loop"
narration_voice: en-US-AndrewNeural
narration_rate: "-10%"
audio: media/36-stakeholders-and-feedback.mp3
guide: docs/guides/36-stakeholders-and-feedback.md
---

# Chapter thirty six. Stakeholder management and the product feedback loop.

Welcome to chapter thirty six of FullStack in Audio. You now have a plan and a business case, and both of them are documents. This chapter is about the fact that a customer delivery is not executed by documents. It is executed inside a continuous negotiation among people whose interests genuinely differ, and the thing that keeps that negotiation healthy is not charm, not enthusiasm, and not responsiveness. It is a loop with a memory.

Let me put the thesis of the chapter up front, because everything else follows from it.

Trust in a field engagement is not built by saying yes. It is built by making every input produce a visible decision. What destroys trust is not refusal. It is silence. When a person gives you feedback and nothing observable happens, they draw one of two conclusions: either you did not understand them, or you did not care. Both of those are considerably worse for you than a clear no with a reason. And here is the part that surprises engineers: a well delivered no, with the reasoning shown, frequently increases confidence in you. It demonstrates that you have a model of the system, that you are not merely agreeable, and that the yeses you do give mean something.

So this chapter is about building the machinery that guarantees no input disappears. That machinery has two halves. The stakeholder side, which is about who these people are, what they need, and whose yes actually counts. And the feedback side, which is about turning what people say into classified, owned, prioritized, decided, and communicated items.

## Part one. What we are actually talking about.

A stakeholder is anyone who can affect the deployment or is affected by it. That definition is deliberately wide, and the width matters, because the person who ends your pilot is frequently someone you did not have on a list.

There are four distinct stakeholder roles that get conflated constantly, and separating them will save you real pain.

The sponsor owns the outcome and usually the budget. They are the person whose credibility is attached to the project. They care about whether this was a good decision and whether they will be surprised.

The domain decision owner holds authority over one specific area. The data owner authorizes what data may be used. The security lead authorizes what boundaries may be crossed. The integration owner authorizes what may call their system. The platform lead authorizes what may run in their environment. Each of these people can stop you inside their domain, and their authority is usually narrow and absolute. Notice that the sponsor cannot simply overrule them, whatever the org chart implies, because these people are the organization's mechanism for not doing dangerous things.

The user is the operator. They cannot approve anything and they can kill everything, by not using it.

And the influencer, or informal blocker, is the person with veto by convention rather than by title. The most respected senior operator. The engineer everyone asks before trusting a new tool. The team lead whose opinion propagates through the break room. If that person says your system is rubbish, you will lose the pilot faster than any executive could take it from you, and no amount of dashboard evidence will save it. Find that person in week one and give them more of your attention than their title suggests.

Now the concept that separates competent stakeholder management from busy stakeholder management: decision rights.

For any given question, there is someone whose yes counts, people who must be consulted, and people who must be informed. The single most common failure in field delivery is obtaining an enthusiastic yes from someone who did not have the authority to give it, then proceeding, then discovering in month two that the actual authority never agreed. You did nothing dishonest. You simply did not know whose yes counted, and now you have built something on a permission that was never granted.

So for each decision area, write down who decides, who is consulted, and who is informed. Data usage. Access and authorization. Integration into a production system. Change to an operator's process. Model or provider choice. Retention. Go live. Each of those has a different decider, and in a large organization at least two of them will surprise you.

Next, cadence and preferred evidence. Different stakeholders need different frequency and, more importantly, different kinds of evidence.

Preferred evidence is a real and underused idea. Some people believe what they see working. Some believe numbers, and specifically numbers they can trace. Some believe a document with a name on it, because their world runs on accountability artifacts. And some believe only their own trusted colleague's opinion, which means the way to persuade them is to persuade that colleague. Sending a beautifully written document to someone who only believes demonstrations is wasted effort, and sending a demonstration to a security reviewer who needs an artifact for their file is also wasted effort. Match the evidence type to the person, and you will get more agreement with less work.

Now the feedback side. A piece of feedback is an observation about the system's behavior in use. And there is a critical distinction hiding inside almost every piece of feedback you will receive.

A request is a proposed solution. An observation is the underlying experience that produced it. When an operator says, I need a button to send this to the network team, that is a request. The observation behind it might be that the proposed owner was wrong for a specific class of incident, or that the notification path is manual right now, or that they do not trust the ownership lookup for one particular service. Those three observations imply three completely different pieces of work, and only one of them is a button.

So the discipline is: always capture the observation behind the request. The question that gets you there is simple and you should have it memorized. What happened that made you think of that. Ask it every time, gently, and you will find that roughly half of all feature requests dissolve into something smaller and more accurate.

Then the loop itself, which has six steps: capture, classify, prioritize, decide, communicate, and verify. Most teams do the first three well and stop. The last three are where trust is made.

Classification uses five classes, and I will add a sixth that field work demands. A defect: the system did not do what it was specified to do. A usability issue: the system did what it should but the person could not use it effectively. A missing requirement: discovery did not catch something real. An integration request: something must connect to another system. A training need: the system and the design are correct and the person did not know how to use them. And the sixth, expectation mismatch: the system behaved exactly as designed, and the person expected something different, usually because of how the capability was described to them.

Classification is not filing. Each class has a different owner, a different urgency, and a different response. A defect is yours and it is urgent. A usability issue is yours and it is often more valuable than the defect. A missing requirement goes back into your requirements set with a date, and it is the one that may legitimately change your scope. An integration request usually belongs to the integration owner's calendar as much as to your backlog. A training need belongs to the change management plan, not to your code. And an expectation mismatch is almost always a communication defect on your side, which is a useful and humbling thing to discover.

Finally, prioritization. Four axes from your syllabus: customer outcome, risk, effort, and strategic reuse. The first three are familiar. Strategic reuse is the FDE specific one, and it names your dual loyalty. You serve this customer and you serve the product. An item that only ever helps this one account is customer configuration or customer specific adapter work, and it should be built where chapter six said such work belongs. An item that would help many customers is product evidence, and it should travel back to the product team with the evidence attached rather than being quietly built into one deployment.

## Part two. Why this is the FDE's job specifically.

Six reasons.

First, you are a single point of trust. In most engagements, the customer's experience of your entire company is one person: you. Every process failure, every provider outage, every awkward scope conversation arrives through you. This is a heavy thing to carry and it is also enormous leverage, because a single trusted person can move an organization faster than a process can.

Second, the pilot's real product is learning. It is tempting to think the pilot's output is the system running. It is not; the system already runs. The pilot's output is a set of validated statements about what works, for whom, at what cost, with what risks. Feedback velocity is therefore the actual throughput metric of a pilot, and a pilot with a slow or lossy feedback loop is not a pilot, it is an unpaid deployment.

Third, unmanaged expectations produce scope creep by accretion, and accretion is much more dangerous than a single large request. Nobody ever asks you to double the project. They ask you for a small field, and a small filter, and a small export, and a small extra notification, and each one is individually reasonable, and each one is individually cheap, and eight weeks later your first release is unrecognizable and late. The defense is not toughness. It is a visible list with statuses, because a list makes accretion legible to everyone, including the people doing it.

Fourth, your dual loyalty is real and must be handled openly. You genuinely owe this customer a system that fits their operations, and you genuinely owe your product a codebase that does not fracture into per customer forks. The wrong resolution is to secretly build a fork because the customer is in front of you and the product team is not. That decision feels like service and it is a slow betrayal of both parties. The right resolution is the architectural boundary you already established: reusable core, customer configuration, customer specific adapter. Feedback gets routed to one of those three, explicitly, and when something does not fit any of them, that is a conversation to have rather than a fork to commit.

Fifth, informal authority is not visible in any document. The break room verdict, the group chat, the one person everyone asks. You will only learn this by paying attention to who gets deferred to in meetings and whose name comes up when others explain a decision.

Sixth, and most practically: the decision log is what stops you answering the same question every month. Without a written record of what was decided, by whom, on what basis, and when, every settled question will reopen, usually at the worst moment, usually because a new person joined. A decision log is not bureaucracy. It is the mechanism that lets an engagement accumulate rather than circle.

## Part three. How to run the loop for FieldOps Copilot.

Ten moves.

Move one: build the stakeholder register. For each person: their name and role; what they are measured on; what they need from you; their preferred evidence type; the cadence that suits them; their decision authority per area, expressed as decides, consulted, or informed; and their current disposition, from champion through supportive, neutral, skeptical, to blocker.

Two rules. Include at least one skeptic, deliberately, and give them real access. A register composed entirely of supporters is a comfort object. And keep the disposition column current, because disposition changes, and a champion drifting to neutral is the earliest warning signal you will ever get.

Move two: set the cadence and then honor it, especially when the news is bad. Operators want short, frequent, concrete contact, ideally inside the product they are using. The sponsor wants a predictable, brief, decision shaped update. Security and the data owner want event driven contact with artifacts, not regular updates they did not ask for. The integration owner wants advance notice of anything that will touch their system, and mostly wants to be left alone otherwise.

Now the discipline, and it is the single highest return habit in this chapter. Send the update on the bad week. Same day, same format, even if the content is that the credential did not arrive, the evaluation regressed, and there is nothing to show. Predictability is the trust mechanism. Sponsors do not lose confidence because a project has problems; they lose confidence when the rhythm of information breaks, because that is the pattern that has preceded every unpleasant surprise in their career.

Move three: run the demo as a research instrument rather than a performance. This is where most engineers waste their best opportunity.

Prepare three synthetic incidents deliberately. One clean case, where the system does its job well. One ambiguous case, where evidence is weak and the system correctly declines and says it has insufficient evidence. And one case where the system is wrong, or where it hits a boundary it cannot handle.

Yes, show the failure. On purpose. This feels like a terrible idea and it is the strongest trust building move available to you, for a specific reason: everyone in that room has been shown a flawless vendor demo before, and everyone in that room knows the flawless demo was a lie. When you show the boundary and explain what happens at it, you are giving them the thing they actually need, which is a calibrated sense of when to rely on the system. Frame it plainly: here is where it stops being useful, here is what it does instead, and here is why we made it behave that way rather than guess.

Then the technique. Do not narrate the interface. Give the operator the keyboard, give them a scenario, and be quiet. Watch where they hesitate. Hesitation is data with a location: it tells you exactly which label, which state, which control is unclear, in a way that no survey will. Write down the hesitations, not just the comments.

And one rule with no exceptions: do not promise anything in the room. It is enormously tempting, because someone raises something reasonable and you can see how to build it and you want to be helpful. Have a sentence ready. Let me capture that as an observation, and I will come back to you with a decision by Thursday. That sentence protects the customer from an unconsidered commitment, protects your sequence from accretion, and, counterintuitively, makes you look more reliable rather than less.

Move four: capture with structure. Each item records what happened, what the person expected instead, what they actually said in their words, the class, who raised it, when, and what evidence exists. Evidence means a trace identifier, a screenshot, an incident reference, or a recorded hesitation during the demo. An item without evidence is an anecdote, and anecdotes cannot be prioritized against each other honestly.

Move five: classify, and let the class drive the response. A worked pass over plausible FieldOps feedback. The proposal did not show a citation for a policy it referenced: defect, urgent, yours. The operator could not tell whether the asset context was missing or stale: usability issue, and by the way that distinction was a requirement, so check whether it is a defect. Operators need to triage a class of incident that arrives by phone and never enters the intake page at all: missing requirement, back to the requirements set with a date, and possibly a scope conversation. The team wants the confirmed triage to appear in their existing ticket system automatically: integration request, which chapter thirty four already deferred with a trigger, so the response is to restate the trigger. A new operator did not know that editing a proposal was allowed: training need, and also possibly an interface affordance problem, so check both. And someone believed the system would close incidents automatically: expectation mismatch, which means somebody described it that way, which means you need to find out who and fix the description.

Move six: separate the loud request from the validated one. Four tests. Frequency across independent sources, not repetition by one enthusiastic person. Behavioral corroboration: does your telemetry show the problem happening. Observation as well as report: did you see it yourself during a demo or a shift. And survival of the underlying question: when you asked what happened that made you think of that, did a real event appear, or did the request evaporate.

A request that passes all four is product evidence. A request that passes none is one person's preference, which is legitimate to hold and not a basis for changing a delivery. Say that respectfully, and say it with the tests visible, because then the refusal is about the evidence rather than about the person.

Move seven: prioritize with a published rubric. Score each item on customer outcome, risk, effort, and strategic reuse, and publish the rubric to the stakeholders. Publishing is the whole trick. When the rubric is visible, a low ranking is a rule applying to an item. When the rubric is invisible, a low ranking is a personal slight, and the requester's only available response is to escalate, which converts a small prioritization conversation into a political one.

Move eight: decide, and communicate the decision in a fixed shape. What we heard, in their words. What we are doing, with who and when. What we are not doing, and why, with the trigger for reconsideration if there is one. And what we need from you. Every item gets a status: accepted, deferred with a trigger, declined with a reason, reclassified, or needs more evidence.

Note that needs more evidence is a legitimate status and not a way of avoiding a decision, provided it names what evidence and who will gather it. Without those two, it is avoidance wearing a label.

Move nine: close the loop, and close it where the person lives. Going back to the person who raised something is the step that converts your process into their experience of being heard. Do it in the product where you can: the fix appears, and it says which observation it came from. Do it in release notes written for the operator, in their language, describing what changed in their workflow, not which component was refactored. And do it for the things you declined, not only for the things you did, because loop closure only on successes teaches people that raising something is a lottery.

Move ten: route to the right destination, honoring the architecture. Every accepted item lands in one of three places. Reusable core, if it is a general capability and you have product evidence. Customer configuration, if it is a legitimate local variation that the system was designed to absorb. Customer specific adapter, if it is genuinely local and needs code at a boundary that was built for that purpose. And if an item fits none of the three, that is your fork alarm. Escalate it, discuss it, and record the decision. Do not resolve a fork question privately at the end of a long week.

Move eleven: turn the pilot dashboard into a shared instrument rather than your private diagnostic. You built dashboards in chapter thirty one for service health and AI workflow health, and those are engineering instruments. A pilot dashboard is a different thing with a different audience, and building it is one of the highest leverage political acts available to you.

Here is the principle. When the customer and you look at the same numbers, on the same screen, updated on the same schedule, disagreements become factual rather than positional. Without a shared instrument, every conversation about whether the pilot is working is a contest between two impressions, and impressions are shaped by whoever had the worst experience most recently. One bad Tuesday afternoon, remembered vividly by a senior operator, will outweigh three good weeks that nobody measured.

So build a small pilot view with a handful of things, chosen for the audience rather than for completeness. The workflow outcome you agreed in chapter thirty five, shown as a distribution over time rather than as a single average. Coverage, meaning the share of eligible incidents that actually went through the assisted path. Confirmation split three ways: accepted unedited, accepted with edit, rejected. Availability and the ninety fifth percentile response time, because the operator's trust tracks responsiveness more tightly than it tracks accuracy. The running cost estimate, because the sponsor will be asked about it and should never be surprised. And the count of open feedback items by status, which is the loop made visible.

That last tile is the one people find surprising, and it is my favorite. Putting your own feedback backlog on the customer's dashboard is an act of deliberate exposure. It shows how many items are open, how long they have been open, and how many were declined. It makes you accountable in public, which is uncomfortable, and it makes the loop undeniable, which is exactly what you want. A stakeholder who can see that eleven items were raised, nine were resolved or decided, and two are waiting on their own security team, is a stakeholder who no longer needs to wonder whether they are being managed.

Two cautions. Do not put a metric on the shared dashboard that you would be tempted to explain away, because you will have to, repeatedly, in front of people. And do not show raw incident content, because the redaction discipline from chapter thirty one applies to dashboards shown in meeting rooms with a door open just as much as it applies to logs.

Move twelve: mediate a genuine conflict between two stakeholders without resolving it privately. This is the hardest interpersonal skill in the chapter and it is a technical skill, not a soft one, because the resolution is usually a design.

The conflict you will almost certainly get in FieldOps is this. The operations manager wants the system to assign incidents automatically, because assignment is the queue that creates the delay they are measured on. The senior operator does not want automatic assignment, because they carry the consequence of a wrong assignment and they have watched a previous tool make confident mistakes. Both positions are correct given what each person is accountable for. Neither is being difficult.

The wrong moves are all tempting. You can side with the manager, because they have the title and the budget, and lose the operator, and therefore lose adoption, and therefore lose the benefit that justified the budget. You can side with the operator, because you have been sitting with them and you like them, and lose the sponsor's confidence that you are working toward their outcome. Or you can average the two, and ship something half automatic and confusing that satisfies nobody and cannot be explained.

The right move has three steps. First, restate each position in terms of what the person is accountable for, out loud, in front of both of them, and get each to confirm you have it right. You are removing the interpretation that the other person is being obstructive. Second, name the shared constraint, which in this case is that a wrong assignment is expensive for both of them, and that speed with wrong assignments is worse than the current situation, not better. Third, propose a design that gives each of them the thing they are accountable for rather than the thing they asked for. Pre filled assignment with a visible reason and a single confirming action gives the manager most of the latency reduction, because confirming takes seconds while deciding takes minutes. Keeping the confirmation gives the operator the control they need. And an agreed measurement, that confirmation without edit exceeds a stated level across a stated number of incidents, gives them both a path to full automation later that is evidence based rather than authority based.

Notice what that resolution is. It is not a compromise on the axis they were arguing about. It is a move to a different axis, found by asking what each person is accountable for instead of what each person wants. That reframing is available in most stakeholder conflicts, and finding it is genuinely engineering work, because it requires knowing what the system can be made to do.

Then, and this matters, record it. The decision, the two positions, the reasoning, the measurement that would change it, and the date. Six months from now, one of those two people will have moved on, a new person will ask why the system does not assign automatically, and the record is the difference between a two minute answer and reopening a settled negotiation.

One more thing about conflict: escalate on process, not on personality. If a decision genuinely cannot be made at the level you are working at, the escalation is a factual note that says a decision is required between two documented positions, here is the tradeoff, here is what each option costs, and here is the date by which a choice is needed. It names no villain. An escalation that characterizes a person will be remembered long after the decision is forgotten, and it will be remembered as something you did.

## Part four. Pitfalls.

Saying yes in the room. The most natural error and the most expensive. Use the Thursday sentence.

Accepting the request instead of finding the observation. You build the button, the button works, and the underlying problem is untouched, so the same complaint returns wearing different clothes.

Registering only the friendly people. Your register should contain someone who does not want this to succeed. If it does not, you are managing your own comfort rather than the engagement.

Confusing the champion with the decision owner. Your most enthusiastic contact very often has no authority over data, security, or the integration, and their confident yes is worth nothing on those questions.

Cadence that stops when the news is bad. This single behavior does more damage than most technical failures. Silence during difficulty is how a recoverable problem becomes a lost account.

The feedback board as graveyard. Items with no status, no owner, and no date, growing steadily. Stakeholders learn quickly whether a board is a promise or a compost heap.

Prioritizing by seniority of requester. It feels politically safe and it teaches the organization that the way to get work done is to escalate, which guarantees that everything will be escalated.

Closing the loop only on wins. If people hear back only when you did what they asked, they learn that silence means no, and then they stop telling you things, and then your pilot loses its actual product.

The demo as performance. Rehearsed happy path, presenter driving, no failures shown. You will get applause and no information, and you will have burned the one hour where the operator's hands were on your system while you were watching.

Confusing training needs with defects in either direction. Dismissing a real usability problem as a training issue is the classic engineer's error. Rebuilding an interface because one person was never onboarded is the opposite error, and both come from skipping classification.

Silent forking. Building a customer specific behavior into the core because it was faster, and not telling anyone. This is the field engineer's original sin and it compounds quietly for years.

Release notes written for engineers. Nobody in operations wants to read about a refactor. Tell them what changed in their day.

And failing to record decisions, which guarantees you will relitigate every settled question, most likely in front of someone new.

## Part five. Verification.

The random five test. Pick five feedback items at random. Each must have an owner, a status, evidence, a decision date, and a record that the person who raised it was told the outcome. Any gap is a leak in the loop.

The stakeholder recall test. Ask a stakeholder, without prompting, to describe what happened to something they raised. If they cannot, your loop closure is happening on paper rather than in their experience.

The refusal test. Point to one request you declined or deferred, and check that the person who asked can restate your reasoning in their own words. If they can restate it, the refusal landed. If they can only restate that the answer was no, it did not.

The decision rights test. Take three pending decisions and name whose yes counts for each. Then verify with that person that they agree it is theirs. The verification step is the one that catches the expensive misunderstanding.

The loud versus validated test. Point to one loud request you did not act on, and show the four evidence tests you ran. Then point to one quiet observation you did act on because the telemetry corroborated it. Having both directions proves the process is doing work rather than rationalizing.

The demo quality test. Did you show a failure on purpose. Did the operator hold the keyboard. Can you list three hesitations by location. Three noes means you ran a presentation.

The bad week test. Look at your update history and find a week where things went badly. Confirm an update went out, on schedule, in the usual format. If updates are missing precisely where the trouble was, that is the pattern your sponsor will eventually notice.

The routing test. Every accepted item is labeled core, configuration, or adapter, and any item that fits none of them was escalated rather than quietly absorbed.

## Part six. Your practice handoff.

The companion guide is a test. You will produce a stakeholder register with decision rights and dispositions including a skeptic, a cadence plan with a defined bad news protocol, a demo plan with three deliberately chosen synthetic incidents including one failure, a structured feedback capture from running that demo, a classification of every item across the six classes, an evidence assessment separating loud from validated, a published prioritization rubric with scored items, a decision update in the fixed four part shape, operator facing release notes, and a decision log.

The rubric requires at least one correctly deferred request with a transparent rationale that the requester can restate, at least one item routed to configuration rather than core, evidence attached to every item, and a demonstration that you did not promise anything in the room.

Hints are inverted at the end. Attempt first.

## Part seven. Recap.

Trust comes from every input producing a visible decision. Silence, not refusal, is what destroys it.

Separate four stakeholder roles: the sponsor who owns the outcome, the domain decision owners whose narrow authority is absolute, the users who cannot approve anything and can end everything, and the informal influencer whose veto is by convention. Then write decision rights per area, because a yes from the wrong person is not a yes.

Match evidence to the person: demonstrations, traceable numbers, signed artifacts, or a trusted colleague's endorsement. Sending the wrong evidence type is wasted effort no matter how good it is.

Behind every request is an observation. Ask what happened that made you think of that, every time, and roughly half of the feature requests will turn into something smaller and truer.

Run the six step loop: capture with evidence, classify into defect, usability, missing requirement, integration, training, or expectation mismatch, prioritize with a published rubric across outcome, risk, effort, and strategic reuse, decide, communicate in a fixed shape with statuses and triggers, and verify by closing the loop where the person lives, including for the things you declined.

Run demos as research. Show a failure deliberately, give the operator the keyboard, record hesitations, and never promise in the room.

Honor your dual loyalty structurally rather than secretly: route every accepted item to reusable core, customer configuration, or customer specific adapter, and escalate anything that fits none of them instead of forking quietly.

In the next chapter, everything in this loop becomes writing. Runbooks, decision records, status updates, incident notes, and the operator quick start, which is the difference between a system that depends on you and a system the customer owns.
