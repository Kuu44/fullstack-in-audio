---
chapter: 34
title: "Technical scoping, sequencing, and delivery tradeoffs"
part: "Part VII — Deliver value in the customer environment"
roadmap_nodes: "Technical Scoping & Sequencing; Tradeoffs: Scope, Speed, Quality"
narration_voice: en-US-AndrewNeural
narration_rate: "-10%"
audio: media/34-scoping-and-sequencing.mp3
guide: docs/guides/34-scoping-and-sequencing.md
---

# Chapter thirty four. Technical scoping, sequencing, and delivery tradeoffs.

Welcome to chapter thirty four of FullStack in Audio. In the last chapter you replaced an invented charter with evidence. You have a current state workflow map with waiting time on it, a volume profile with real shapes, a prioritized requirements set with numbers that have sources, an assumption log where the load bearing assumptions are marked, and a three way boundary that says what is in the first release, what is deferred with a trigger, and what is out of scope.

Now comes the part that separates a competent forward deployed engineer from an excellent one. Order.

Given everything you know, in what order do you deliver it. That question sounds like project management, and it is treated as project management in most organizations, which is exactly why it is done badly. Sequencing a customer delivery is a technical judgment. It depends on the dependency structure of the system, on which decisions are reversible, on where the uncertainty actually sits, and on what evidence each step can produce. Nobody who cannot read the dependency graph can make this call well, and in a field engagement, the person who can read the dependency graph is you.

There is a peculiarity in your situation that I want to use rather than apologize for. You have already built everything. Every slice you are about to sequence exists in some form on your machine. So what is left to sequence?

Everything that matters. Because built is not delivered. A component running on your laptop against synthetic data, with credentials you issued to yourself, in a cloud account you own, evaluated against fixtures you wrote, is not the same artifact as that component running in a customer environment, with credentials their security team approved, against their data, used by an operator whose shift depends on it, with a support path when it fails at two in the morning. The distance between those two states is where delivery lives, and that distance is what you are sequencing. Treat this chapter as sequencing the journey of an existing system into a customer's operations, and every principle transfers cleanly to the more common case where you are sequencing work not yet written.

## Part one. What technical scoping and sequencing actually mean.

Start with a distinction that prevents a specific and very common disaster.

Product scope is what the system does for the user. Technical scope is everything you must build, change, integrate, prove, secure, deploy, and operate in order for the product scope to be true in a specific environment. Technical scope always exceeds product scope, often by a large factor, and the excess is invisible to everyone but you.

Here is the concrete version. Product scope says: the operator sees the asset owner on the incident. Technical scope says: an identifier exists in both systems that can be joined; a credential exists that can read the asset inventory; someone is willing to issue that credential; the inventory refresh runs on a schedule that meets the freshness requirement; the join failure case is distinguishable from the not found case; the lookup is inside the latency budget at peak; and the whole path is traced so that when the owner is wrong you can tell whether the pipeline was stale or the inventory was wrong. One sentence of product scope, seven items of technical scope. When a customer sponsor says this seems simple, they are reading the first sentence honestly. Your job is not to contradict them. Your job is to make the other seven visible without sounding defensive.

Next, the unit of sequencing. The right unit is a thin vertical slice: a piece of work that crosses every layer of the system and ends with a real user doing a real thing and producing evidence. The wrong unit is a horizontal layer: all of the database, then all of the service, then all of the interface. Horizontal layering feels efficient because each layer is coherent, and it is a trap, because you learn nothing until the last layer lands, and by then every wrong assumption in the first layer has been built upon.

A good slice has four properties. It is independently deployable, meaning it can go live with the later slices absent. It is independently usable, meaning a real person gets real value from it alone. It is independently verifiable, meaning it has acceptance criteria that can pass or fail on their own. And it produces evidence, meaning after it ships you know something you did not know before.

That fourth property is the one people drop, and it is the most important in field work. A slice is not just a delivery increment. It is an experiment.

Now, dependencies. There are three kinds, and confusing them is why plans slip in ways that feel unfair.

A hard technical dependency means slice B cannot function without slice A. The audit record cannot exist before the durable record exists. These are the dependencies everyone draws.

An organizational dependency means slice B cannot proceed without something a human institution must do: a credential issued, a security review completed, a change window granted, a data processing agreement signed, an operator trained, a firewall rule approved. These have lead times you do not control, they are frequently measured in weeks, and they are the number one cause of a technically excellent plan arriving late. They belong on the same dependency map as the technical ones, drawn with the same weight.

An evidence dependency means slice B's design should not be finalized until slice A has taught you something. You could build the retrieval grounding before you learn whether operators trust the ownership lookup, but you would be designing on speculation. Evidence dependencies are soft, they are the ones an impatient plan violates first, and violating them is how you end up rebuilding.

Then, the two properties of a decision that govern how early you should make it. Reversibility, and cost of being wrong. A reversible decision with low cost should be made fast, by whoever is closest to it, and revisited if it turns out badly. An irreversible decision with high cost deserves delay, evidence, and a written record. In field delivery, the classic irreversible decisions are: which cloud and region, how identity is integrated, the tenancy model, whether raw customer text is stored at all, the retention default, and the shape of the data model that the customer's other systems begin to depend on. Each of those can be taken in an afternoon to save a week, and each of them can cost a quarter to reverse.

Finally the triangle, and the correction I want you to carry for the rest of your career. Scope, speed, and quality. Everyone learns that you can have two. The framing is useful and incomplete, because it treats quality as one dial, and quality is not one dial. It is at least five.

Correctness: does it produce right answers. Safety: does it prevent harmful outcomes, unauthorized access, and unapproved autonomy. Operability: can someone diagnose and recover it at three in the morning. Maintainability: can the next engineer change it without fear. Polish: does it feel finished.

Those five are not equally negotiable, and pretending they are is how pilots become disasters. In a customer pilot, polish is genuinely negotiable, and you should trade it away cheerfully. Maintainability can be consciously borrowed against for a short, named period, with the debt written down. Correctness can be narrowed, meaning you handle fewer cases well rather than all cases poorly. But safety and operability are floors, not dials. A pilot without an audit trail, without tenant isolation, without a rollback, and without a trace is not a fast pilot. It is an unbounded liability that happens to have a login page.

So the honest version of the triangle for field delivery is: you can trade scope, speed, polish, and consciously-borrowed maintainability. You cannot trade safety or operability, and when someone asks you to, the correct response is to trade scope instead and say so out loud.

## Part two. Why the sequence is a forward deployed engineer's highest leverage decision.

Let me make the case for why this chapter matters more than it looks.

First, customer urgency is real and legitimate. It is tempting to treat a sponsor's timeline as arbitrary pressure. Usually it is not. There is a budget cycle, a board commitment, a competitor, a regulatory date, a reorganization, or a person whose credibility is attached to this project. If you treat urgency as noise, you will lose the relationship. The FDE's move is not to resist urgency, it is to satisfy it with the smallest credible thing. Urgency is best answered by earlier evidence, not by faster promises.

Second, and this is the deep one: the sequence determines what you learn, and you cannot unlearn a bad first slice. If your first delivered slice is an AI triage proposal, then the first thing the organization learns about FieldOps Copilot is whether the model's suggestions are any good, and that becomes the frame for everything after. Every conversation for the next two months will be about model quality, which is the least stable and least controllable property of your system. If instead your first slice is reliable intake with a durable record and correct ownership lookup, the organization learns that the system is dependable, and the AI arrives later into a context of trust. Same components, same total work, radically different engagement. Sequencing is narrative control, and narrative control is not a marketing concern; it determines whether you get the access and patience to finish.

Third, the irreversible decisions cluster early, which is exactly when you know least. This is the fundamental awkwardness of delivery. You must choose the tenancy model and the identity integration before you have evidence about usage patterns. The mitigation is not to delay everything. It is to identify which early decisions are one way doors and buy information specifically about those, cheaply, before walking through them. A two day spike that answers whether the customer's identity provider can issue the token shape you need is worth more than two weeks of building around an assumption.

Fourth, you are the only person who can see both graphs. The customer's programme manager can see the political calendar. Your engineering colleagues can see the technical graph. Only the embedded FDE sees both, which means only you can notice that the security review has a four week queue and therefore must be started during slice one even though the thing it reviews does not ship until slice four. Nobody else will catch that. If you do not, the plan will be correct and late.

Fifth, tradeoff communication is a trust instrument. Every experienced enterprise buyer has been told yes by a vendor who then delivered something hollow. When you say, we can hit that date, and here is precisely what will not be in it, and here is the quality bar I will not move, you are doing something they may not have experienced from a supplier. The counterintuitive result is that visible, costed tradeoffs increase confidence rather than reducing it. Hidden tradeoffs feel like speed until they surface, and when they surface, you are no longer a partner, you are a risk.

Sixth, rollback is what makes yes possible. This is worth stating plainly because engineers underrate it. A customer's real fear is not that your system will be imperfect. It is that adopting it will be irreversible and they will be stuck. A rehearsed, documented, fast rollback converts a large decision into a small one. Half the objections you will hear in a go live meeting are not objections to your system, they are objections to being trapped, and rollback answers them.

## Part three. How to sequence the FieldOps Copilot pilot.

Eight moves. I will run them concretely against your system.

Move one: express the first release as slices, each with a named beneficiary and the sentence you want them to say afterwards. Here is a sequence I would defend for FieldOps Copilot, and I want you to notice its shape before I justify it.

Slice one: secure intake and durable record. An operator submits an incident through the workspace, authenticated with the customer's identity, and it persists with an audit trail and duplicate protection. The evidence: the system does not lose things and does not double count. The sentence you want: it is reliable.

Slice two: incident context without any AI. The workspace shows the affected service, the asset, its criticality, and the responsible owner, drawn from the ingested inventory, and it clearly distinguishes not found from stale data. The evidence: the ownership lookup is right often enough to be trusted, and the pipeline freshness holds. The sentence you want: it saves me the second and third system.

Slice three: read only AI proposal, behind a flag, for two volunteer operators. A structured triage proposal with a rationale and no ability to change anything, evaluated against your gate before exposure. The evidence: proposal usefulness and confirmation rate, measured, on real workload shapes. The sentence you want: it is usually right and it never surprises me.

Slice four: grounding in the customer's own procedures. Retrieval over their real runbooks with tenant isolation, citations shown, and an explicit insufficient evidence path. The evidence: proposals now cite the customer's own policy, and refusal behaves correctly when evidence is weak. The sentence you want: it quotes our procedure, not the internet.

Slice five: approval, audit, and notification. The operator's confirm action becomes the system of record event, and the downstream notification path exists. The evidence: an auditor can reconstruct who decided what and when. The sentence you want: we can explain any decision after the fact.

Slice six: rollout to the full shift, with the dashboard, the alerting, the runbook, and a named support path. The evidence: it operates without you in the room. The sentence you want: this is ours now.

Look at that ordering. The AI, the most impressive part and the reason the project probably got funded, is third. The retrieval, which is the technically most interesting work you did, is fourth. That is deliberate, and it is the single most important judgment in this chapter.

Move two: draw the dependency map with all three edge types. Hard technical edges are easy: slice five needs slice one's record and slice three's proposal. Slice two needs the asset pipeline. Evidence edges: slice four's design should follow slice three's data about where proposals go wrong, because if proposals fail on missing information rather than on policy knowledge, retrieval is not the fix and you would have built the wrong thing beautifully. Organizational edges are where you earn your keep. Slice one needs an identity integration, which needs a security review and a credential, which needs a queue position you must claim now. Slice four needs access to real runbooks, which needs a data classification decision and probably a legal conversation. Slice six needs operator training scheduled around shift patterns, and shift schedules are published weeks ahead.

Now find the critical path, and notice something: the critical path of a field engagement usually runs through the organizational edges, not the technical ones. Your engineering is rarely the bottleneck. Waiting for approval is.

Move three: annotate each slice with its unknowns and its one way doors. For slice one, the one way door is the identity integration shape and the tenancy model. For slice two, the one way door is the join identifier, because once other systems start relying on how you key assets to incidents, changing it is a migration. For slice three, the one way door is whether you store raw incident text sent to a provider, and for how long. For slice four, the one way door is where the customer's procedure content is processed and whether embeddings of it leave a boundary. Write these down separately from the general risk list, because they need a different treatment: they need evidence before you walk through them, and they need a written decision record.

Move four: score, then re rank by uncertainty retired. Start with the ordinary matrix: customer impact, effort, and risk if wrong. Then do the move that most plans skip. For each slice, ask how much uncertainty it removes per unit of effort. A slice that delivers modest value but retires a load bearing assumption may deserve to go first, or, better, may deserve to be split so that a small probe goes first.

That is the spike concept, and it is your main tool for reconciling risk first thinking with value first thinking. You do not need to deliver the whole integration to learn whether the credential can be issued. You need two days and a request. You do not need the full retrieval slice to learn whether legal will permit runbook content to be processed in your chosen region. You need one meeting and a written question. Put the cheap information purchases at the front, in parallel with slice one, and keep the value delivery order intact.

Move five: choose the first two slices and defend them out loud, in terms of value and risk, not novelty. For FieldOps, slice one first because it is the spine that everything attaches to and because it forces the identity and credential conversation to happen while there is still schedule to absorb it. Slice two second because your discovery volume profile said waiting for the right owner dominates working time, which means ownership context, not smarter categorization, is where the customer's money is. If your own discovery said something different, your order should be different, and that is the point: the sequence is derived from evidence, not from a template.

Move six: make one tradeoff explicitly, and record the quality floor that survives it. Let me walk a real one.

Notification into the customer's existing ticket system. Options: build a full bidirectional adapter now; use whatever webhook their platform already offers; configure a scheduled export that a human picks up; or defer notification entirely and have operators continue to work from the workspace. The full adapter is weeks of work against an integration owner who has already told you they dislike new load, and it depends on a change window you do not control. So the choice is to defer the adapter, ship a one directional notification through their existing webhook if it exists, and otherwise bridge manually for the pilot's duration.

Now the crucial second half, which most teams omit. State what does not move. Even with a manual bridge, every notification attempt is recorded as an audit event, nothing is silently dropped, and a failed bridge produces a visible operational alert rather than silence. The tradeoff reduced scope and speed of integration. It did not reduce auditability or observability. Write that sentence down, because in three weeks somebody will propose skipping the audit event to make the manual bridge simpler, and your written floor is what stops that.

Consider a second tradeoff that your own build invites. In chapter twenty one you added a specialist review role alongside the classifier, and the chapter told you honestly that you must be able to justify the split or remove it. In a first release, that split adds latency, cost, and a second failure mode in exchange for surfacing disagreement. Unless your evaluation evidence shows it materially improves outcomes, cut it from the first release, defer it with a trigger, and keep the code. That is what a deferral with a trigger looks like in practice: not deleted, not shipped, and reconsidered on a stated observable condition.

Move seven: shape the backlog as milestones with evidence gates rather than as a task list. Each milestone states the slice, the acceptance criteria it must satisfy from your chapter thirty three set, the instruments that will produce the evidence, the organizational prerequisites that must have completed, and the go or no go decision it enables. This is where the machinery you built becomes a project management asset. Your continuous integration gate is a milestone condition. Your evaluation suite baseline is a milestone condition. Your trace is how a criterion gets measured. A milestone that cannot fail is not a milestone, it is a date.

And keep a running risk, assumption, issue, and dependency log. The distinction matters: a risk might happen, an issue already has, an assumption is a belief you are relying on, a dependency is something outside your control that you need. Most teams keep only issues, which means they only track problems after they have become expensive.

Move eight: write the rollback and contingency plan, and then rehearse it. Rollback has levels, and naming them makes the conversation calm rather than dramatic.

Level one, turn the behavior off. The AI proposal is behind a flag; the flag goes off, the workspace continues to work, operators triage manually with full context. Seconds, no deployment.

Level two, revert the version. Your release manifest pins application version, prompt version, model, embedding model, and retrieval index revision. Rolling back means selecting the previous approved manifest, and you rehearsed that in chapter twenty six. Minutes.

Level three, revert the data shape. This is the expensive one, which is why the schema decisions were marked as one way doors. Have a stated position: what is forward compatible, what would require a migration, and what would require the customer to accept data loss.

Level four, withdraw to the prior process entirely. Operators return to the original tools. The requirement here is simple and often forgotten: the original process must still work. Do not let the customer decommission anything during a pilot.

Contingency is different from rollback and needs its own section. Rollback answers what if what we shipped is bad. Contingency answers what if something we depended on does not arrive. The credential is not issued in time. The security review slips past the change window. The runbooks turn out to be in a format nobody can export. The volunteer operators are pulled onto an outage for two weeks. For each of the top organizational dependencies, write the trigger date, the fallback, and who decides. A contingency without a named decider is a wish.

Then rehearse. An unrehearsed rollback does not exist. Time it. Write down the actual elapsed minutes and who performed each step. That number is one of the most persuasive things you will ever put in front of a nervous customer.

Move nine: decide build, buy, configure, or defer, capability by capability. I have left this until after the sequence because it is often taught first, as a procurement question, and that framing produces bad answers. Build versus buy is a sequencing decision. The same capability can be correctly bought in the pilot and correctly built in year two, or the reverse, and the deciding factor is usually where the uncertainty is, not where the cheapest line item is.

There are four options, not two, and forgetting the middle two is what makes these conversations feel binary and tense.

Build means you write and own it. You get exact fit and you inherit maintenance forever. Buy means a vendor or managed service owns it. You get speed and you inherit a dependency, a contract, a data path, and someone else's roadmap. Configure means the capability already exists somewhere in the customer's estate and you connect to it or turn it on. This is the option engineers systematically under-explore, and in enterprise environments it is very often the right answer, because large organizations already own more software than anyone in the room can enumerate. Defer means the capability is not in this release at all, and something simpler stands in for it.

Now the decision criteria I would actually apply, roughly in order of how often they turn out to be decisive.

Is this capability the differentiating value, or is it plumbing. Build the thing that is the reason the customer wants the system. Do not build the thing that is merely required for it to function. Your triage policy, your grounding behavior, your approval boundary, and your audit semantics are the value. An email delivery mechanism, a metrics backend, a queue, a login screen, an object store, and a document parser are plumbing. Every hour spent building plumbing is an hour not spent on the reason you are there, and plumbing is the part the customer will least forgive you for having built badly.

Where does the data have to go. This criterion frequently overrides everything else, and it is the one that catches teams late. A bought component that would require incident text to leave an approved boundary is not a cheaper option, it is a blocked option. Work this out before you get attached, because you will get attached.

What is the reversal cost. A bought component behind an interface of your own design is a two way door. A bought component whose data model, identifiers, and semantics leak into your domain is a one way door, and you have just given a third party a veto over your architecture. This is exactly the discipline you already practiced: your model provider sits behind a port, your cache sits behind an interface, your notification path is an adapter. Keep doing that, and buying becomes low risk.

What is the true total cost. Not the licence. The licence, plus the integration effort, plus the procurement and security review time, plus the annual review, plus the operational surface, plus the exit cost. In enterprise environments, the procurement and security review time for a new vendor is frequently the largest of those, and it is measured in months. A component you can build in four days may genuinely be cheaper than a component you can buy in one day, purely because buying triggers a vendor onboarding process. This is unintuitive to engineers and obvious to anyone who has sat through it once.

Who operates it at three in the morning. If the answer is the customer's platform team, then the choice must be something their platform team already knows how to operate. An excellent tool that nobody on site can run is a liability disguised as a capability, and it is one of the most common causes of a pilot that works and a handover that fails.

Then apply this to FieldOps Copilot honestly, and be prepared to be uncomfortable. Your model access is bought, correctly, and it sits behind a port, also correctly. Your vector store: ask whether the customer's existing database can serve the pilot's retrieval volume rather than introducing another datastore for the platform team to learn, and recall that your own chapter fourteen work told you to justify every additional datastore. Your orchestration: you built an Airflow shaped graph, and at pilot volume a scheduled job may be sufficient, so the honest question is whether the orchestration is carrying pilot weight or aspirational weight. Your observability backend: buy or use theirs, never build. Your identity: always configure, never build, and if you find yourself writing password handling in a customer engagement, stop and escalate. Your notification: configure into what they already run.

And write each of these as a decision record with an expiry. A build, buy, configure, or defer choice made for pilot scale should carry a sentence saying what would change the answer. That sentence protects you twice: it prevents a pilot expedient from silently becoming permanent architecture, and it prevents a future engineer from assuming the choice was made carelessly.

One last piece of craft that belongs here, because it is where sequencing meets the customer conversation: how to give an estimate you can live with. An honest estimate has three parts. A range, not a point. The assumptions the range depends on, stated in one line each. And a date by which you will replace the range with something narrower. It sounds like this: slice one lands in two to three weeks; that assumes the read credential is issued by the end of this week and that the identity integration uses the standard token flow rather than a custom one; I will confirm both on Friday and give you a tighter number then. Notice that this is not hedging. It names what you do not yet know, commits to when you will know it, and gives the sponsor something to act on, which is usually the credential. Estimates that are point values with hidden assumptions feel more confident and transfer all the risk onto you, which means they transfer it onto the customer's date, quietly.

## Part four. Pitfalls.

Horizontal slicing. All the data model, then all the service, then all the interface. It feels orderly and it delays every piece of learning to the end. Symptom: your first three milestones have no user in them.

Sequencing by demo appeal. The AI goes first because it is the exciting part and because someone senior wants to see it. The cost is that your entire engagement gets framed by the least controllable component while trust is still thin.

Value only prioritization. A ranked list by customer impact with no risk column produces a plan that does the easy valuable things first and hits the hard uncertain thing in month three, when there is no schedule left to absorb what it teaches you.

Silent quality erosion. It always sounds reasonable in the moment. We will add the authorization check after the pilot. We can put observability in later. Let us skip the audit event for now. Each one individually is defensible, and together they produce a system that cannot be deployed and cannot be diagnosed. The counter is the written floor from move six.

The unnamed organizational dependency. Somebody has to issue a credential, and nobody wrote down that it takes four weeks. This single pitfall causes more field delivery slippage than all technical estimation error combined.

Estimates presented as commitments. The honest form of an estimate names its uncertainty and its assumptions: two to three weeks if the credential arrives this week, and I will tell you on Friday which one it is. That is not hedging, it is forecasting with the error bars visible.

Deferral without a trigger. Later is not a plan, it is a way of ending an uncomfortable conversation. Every deferred item needs an observable condition for reconsideration, or the customer is right to hear it as never.

Casual one way doors. Choosing a region because it was the default in a console. Storing raw incident text because it was convenient for debugging. Keying a relationship on a display name because the identifier was awkward. Each takes an hour and costs a quarter.

Big bang rollout. Going from zero to the whole shift in one step gives you no controlled comparison, no way to isolate a problem, and no volunteers with a stake in success. Two operators first, always.

Unrehearsed rollback. See above. Also: rollback documented by the person who built it, never executed by anyone else, is a rollback that will fail under stress.

Slices sized to sprint boundaries. Sprints are a cadence for work, not a definition of evidence. Let the slice be the size that produces a decision, and let it span whatever number of weeks that takes.

And the ninety percent trap. Every part of the system works, so it feels nearly done, and the remaining work is integration, credentials, training, support paths, and operability, which is where most of the real duration lives. When you feel ninety percent done, look specifically at the list of things you have never done in the customer's environment.

## Part five. Verification.

How do you know your sequence is a good one.

The stakeholder sentence test. For every slice, name the person and the sentence they would say after it lands. If you cannot produce a person and a sentence, the slice is an engineering task masquerading as a delivery increment.

The independence test. Take slice one and confirm it deploys and is usable with slices two through six entirely absent. Then confirm no two slices depend on each other in both directions. Circular dependency between slices is proof that you sliced horizontally.

The uncertainty test. Look at your load bearing assumptions from chapter thirty three and confirm the top one or two are retired within the first two slices or by a cheap probe running in parallel. If your biggest unknown resolves in month three, reorder.

The floor test. For each tradeoff you made, point at the written sentence stating what quality property did not move. Every tradeoff without such a sentence is an undocumented degradation.

The trigger test. Every deferred item has an observable reconsideration condition. Read three of them aloud and check that a customer could independently tell whether the condition had been met.

The lead time test. Every organizational dependency has an owner, a lead time, and a start date that is early enough. Then check the corollary: is anything on your critical path something you cannot influence and did not start yet.

The rehearsal test. Rollback was executed, by someone other than its author, and you have the elapsed time written down.

The three sentence test. State your main tradeoff to an imagined sponsor in three sentences, and confirm that one of the three names the cost. If your explanation contains no cost, you are selling, not scoping.

## Part six. Your practice handoff.

The companion guide is a test. Its goal is a defensible delivery sequence for the FieldOps Copilot pilot: slices with beneficiaries and evidence, a dependency map with technical, organizational, and evidence edges, marked unknowns and one way doors, a re ranked priority with the first two slices defended, one explicit tradeoff with its surviving quality floor, a milestone plan with evidence gates, a risk assumption issue dependency log, and a rollback and contingency plan that you rehearsed and timed.

The rubric rewards independence and honesty over completeness. It checks whether slice one truly stands alone, whether the sequence retires your biggest unknown early, whether at least one deferral has a real trigger, whether your tradeoff names a cost, and whether the rollback was actually performed rather than described. It fails you for a plan whose first milestone has no user in it, and it fails you for any tradeoff that quietly moved safety or operability.

Hints are inverted at the end. Attempt first.

## Part seven. Recap.

Technical scope always exceeds product scope, and the excess is invisible to everyone but you. Sequence in thin vertical slices that are independently deployable, usable, verifiable, and evidence producing, never in horizontal layers.

Map three kinds of dependency: hard technical, organizational, and evidence. The critical path in a field engagement usually runs through the organizational ones, so start them absurdly early.

Separate reversible from irreversible decisions. Buy cheap information before walking through a one way door, and record the decision when you do.

Quality is not one dial. Correctness, safety, operability, maintainability, and polish are five different things. Polish is negotiable, maintainability is borrowable with the debt written down, correctness can be narrowed, and safety and operability are floors. When someone asks you to trade a floor, trade scope instead and say so.

Order by uncertainty retired as well as by value, use small probes to buy information without delaying delivery, put the impressive AI capability after the dependable foundation so the organization learns reliability first, and defer with observable triggers rather than with the word later.

Finally, write and rehearse rollback in four levels, keep contingency separate for the dependencies you do not control, and time the rehearsal, because that number is what turns a customer's large irreversible decision into a small reversible one.

In the next chapter you leave the technical plan and enter the part of delivery that engineers most often dismiss and most often lose to: the enterprise's own machinery. Business acumen, the approval workflow, and whether the value of this system can actually be demonstrated in money.
