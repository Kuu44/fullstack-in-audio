---
chapter: 33
title: "Discovery, scoping, and requirements gathering"
part: "Part VII — Deliver value in the customer environment"
roadmap_nodes: "Discovery & Scoping; Requirements Gathering"
narration_voice: en-US-AndrewNeural
narration_rate: "-10%"
audio: media/33-discovery-and-scoping.mp3
guide: docs/guides/33-discovery-and-scoping.md
---

# Chapter thirty three. Discovery, scoping, and requirements gathering.

Welcome to chapter thirty three of FullStack in Audio, and welcome to Part Seven, the part of the course where the system you have built finally has to meet the people who are supposed to live with it.

Take stock of what you actually have right now. You have an accessible intake page, a React operator workspace, a typed and secured Node service, a PostgreSQL record with audit events and an idempotency key, an expiring cache behind an interface, a provider agnostic AI seam, a versioned prompt, a read only lookup tool, a bounded triage agent with explicit stop conditions, retrieval grounded in synthetic runbooks with tenant isolation, a second specialist role that surfaces disagreement instead of hiding it, an evaluation gate with negative cases, a latency and cost budget, a validated asset ingestion pipeline, an orchestrated refresh, a release manifest that pins every version, a continuous integration pipeline that blocks promotion on failed checks, container images that do not run as root, a cloud landing zone chosen against constraints, infrastructure declared as code, end to end tracing with redaction, and a risk control pack with abuse tests.

That is a serious system. And here is the uncomfortable thing about it. Every requirement it satisfies came from a charter that you invented in chapter one. You made up the customer. You made up the workflow. You made up the measurable outcome. That was exactly the right move as a teaching device, because you cannot learn to build under constraints that do not exist yet. But in real field work, it is the single largest risk in the engagement, and it is the risk that kills the most projects. A forward deployed engineer can absolutely build all of that. The question that decides whether the engagement succeeds is whether all of that was aimed at something real.

So this chapter does the work that a real engagement does first, and it does it deliberately late, so that you feel the cost of doing it late. You are going to run discovery against your own finished system. And I want to be honest about what that feels like. It feels like being told that some of your best work does not matter. That feeling is the lesson. An FDE who cannot revise a design in the face of evidence is not a field engineer. They are an author defending a manuscript.

## Part one. What discovery, scoping, and requirements gathering actually are.

Let me define the three activities precisely, because in customer conversations these words get used loosely, and the looseness is expensive.

Discovery is structured evidence gathering about how work happens today. It is descriptive. Its output is a picture of reality, including the parts of reality nobody is proud of. Discovery is not a sales conversation, it is not a design workshop, and it is not a requirements meeting. It is fieldwork. Its governing question is: what is actually true here.

Scoping is drawing a boundary. Given everything discovery revealed, scoping decides which part you will address first, which part you will address later, and which part you will not address at all. Its governing question is: what is the smallest thing we can build that produces real evidence about real value. Scoping is a decision, and decisions have owners and dates.

Requirements gathering is the translation step. It converts discovery findings into statements precise enough that somebody who was not in the room could test whether you delivered them. Its governing question is: how would we know.

Those three are sequential in logic and interleaved in practice. You will learn something in a requirements conversation that sends you back to discovery. That is normal. What is not normal, and what you must refuse, is skipping discovery and starting at requirements, because then your requirements simply encode your assumptions in more official looking language.

Now the vocabulary that makes the rest of this chapter work. There are four kinds of statement that must never be blended together, and blending them is the most common cause of a delivery that everyone agrees was completed and nobody agrees was successful.

A finding is an observation about the present. Someone did something, or a number was measured, or a document said something. A finding is attributable. You can say who said it or where you saw it. An example finding: the evening shift operator opens three separate systems before assigning any incident, and did so for every one of the six incidents observed.

A requirement is a statement about what the system must do. It is prescriptive, it is testable, and it belongs to the future. An example requirement: when an operator opens an incident, the workspace must show the affected service owner and the asset criticality without the operator opening another application.

An assumption is a belief you are relying on that you have not verified. Assumptions are not shameful. Undeclared assumptions are. An example assumption: the asset inventory is accurate enough that service owner lookup will be correct more often than the operator's own memory.

An acceptance criterion is a check that returns a plain yes or no when someone runs it against the delivered system. Not a goal. Not a direction. A check. An example acceptance criterion: for twenty sampled incidents in the pilot, the workspace displays a service owner, and in at least eighteen of them the operator confirms the owner is the person they would have contacted.

Finding, requirement, assumption, acceptance criterion. Four different things. Different lifetimes, different owners, different failure modes. Keep them in four separate places and half of the classic delivery disputes disappear.

Next, the split between functional and nonfunctional requirements, because this split is where field deployments actually die.

A functional requirement describes behavior. The system triages, the system notifies, the system records who approved. Functional requirements are the ones customers volunteer, because they are the ones people can picture.

A nonfunctional requirement describes the conditions under which that behavior must hold. How fast. How available. How long the data is kept. Which region it may live in. Who may see it. Whether it must work for a screen reader. Whether it may call the ticketing system during the nightly change window. Whether an auditor must be able to reconstruct a decision eleven months later.

Here is the pattern I want you to internalize. Functional requirements determine whether the demo works. Nonfunctional requirements determine whether the deployment happens. I have never seen an enterprise pilot blocked because the model's categories were slightly off. I have repeatedly seen pilots blocked because nobody asked which region the data could be processed in, or because retention was unspecified, or because the only integration credential available was a shared administrator account that security refused to issue. Those are not details. Those are the gate.

There is one more distinction that separates competent discovery from theatrical discovery: stated requirements versus revealed requirements. A stated requirement is what someone tells you they need. A revealed requirement is what their behavior proves they need. When an operator tells you the priority field is the most important thing on the screen, and then you watch six incidents and see them ignore priority entirely and sort by the age of the last update, you have found a revealed requirement that contradicts a stated one. Both are data. The revealed one is usually stronger, and the contradiction itself is often the most valuable thing you will learn all week.

## Part two. Why a forward deployed engineer cares about this more than anyone else on the team.

There is a version of this chapter that sounds like generic product management, and I want to draw the line clearly, because the FDE's stake in discovery is structurally different from a product manager's.

A product manager is usually optimizing across many customers. They can absorb being wrong about one account, because the portfolio protects them. An FDE is embedded in one customer environment, with their own name attached to a system that runs inside that customer's operations. If the scope is wrong, the FDE is the one sitting in the room when an operator says, politely, that they have gone back to the spreadsheet. There is no portfolio to hide in.

So here is why discovery is an engineering responsibility for you and not somebody else's upstream homework.

First, the most expensive failure in the field is solving an imagined problem perfectly. Every one of the previous thirty two chapters has increased the cost of being wrong about the problem. A misaimed prototype costs a week. A misaimed system with a data pipeline, an evaluation gate, a deployment definition, and a governance pack costs a quarter, and it costs credibility that you do not get back cheaply.

Second, the person who asked for the tool is very often not the person who has to use it, and their incentives diverge. An operations director may be measured on mean time to resolution and headcount efficiency. The operator on the evening shift is measured, informally and much more sharply, on not being the person who mishandled the outage. Those two people want different things from the same product. The director wants throughput and automation. The operator wants to not be blamed, which means they want control, visibility, and the ability to override. If you gather requirements only from the director, you will build something that increases the operator's exposure to blame while removing their control, and it will be quietly abandoned. Not loudly rejected. Quietly abandoned, which is worse, because you will not find out for two months.

Third, discovery is how you earn the right to say no. This is the part that surprises engineers new to field work. Saying no with nothing behind it sounds like laziness or vendor stubbornness. Saying no with evidence behind it sounds like expertise. When you can say, we observed eleven incidents, nine of them followed a path that this requested feature does not touch, and the two that would use it both require a data source your security team has not approved, you are not refusing. You are informing. Discovery converts your judgment from opinion into position.

Fourth, everything downstream in Part Seven depends on this chapter. The sequencing you will do in chapter thirty four needs a dependency map that only discovery can supply. The business case in chapter thirty five needs a baseline, and a baseline is a discovery artifact, not a spreadsheet you invent. The stakeholder loop in chapter thirty six needs to know who has decision authority, which is something you learn by asking, not guessing. The handoff writing in chapter thirty seven has to be aimed at named audiences with known workflows. And the capstone in chapter thirty eight is only a capstone if the thing you assembled matches something real.

Fifth, and practically: access is scarce and expensive. You will get a limited number of hours with the people who know the truth. An operator's time is operational capacity being withheld from operations. A security lead's time is a queue with a hundred other vendors in it. Treat interview access like a budget with a hard ceiling. Preparation is what converts that budget into evidence instead of into small talk.

## Part three. How to run discovery properly, applied to FieldOps Copilot.

Now the method. I will walk this as nine moves, and I will keep tying each one back to the system you already have, because your advantage in this exercise is that you can put a real working artifact in front of people, and a working artifact provokes far better correction than a slide does.

Move one: know before you ask. Every question you ask that could have been answered by reading is a question you have wasted, and it also signals that you did not prepare, which reduces how candid people are with you. Before any interview, get the artifacts. A ticket export from the last quarter. Screenshots of the current tool. The escalation policy document, however out of date. The org chart. And most valuable of all, the history of prior attempts. Almost every operations team has tried something before: a rules engine, a chatbot, a macro laden spreadsheet, a previous vendor. Ask what happened to it. The story of the last failed attempt tells you the political constraints, the technical constraints, and the trust deficit you are inheriting, all at once.

Move two: interview four roles, with four different question sets. The chapter mini project names them: an operator, a manager, a security lead, and an integration owner. Do not reuse one questionnaire. Each of these people holds a different kind of truth, and asking them the same questions wastes three of the four conversations.

With the operator, ask about the last real instance. Walk me through the most recent incident you handled. What did you do first. Where did you look second. What did you have to ask another person for, and how long did that take. What made this one slower than usual. When the current tool tells you something wrong, what do you do. What do you keep in a personal note or spreadsheet that is not in any system. That last question is gold, because personal spreadsheets are unmet requirements made visible.

With the manager, ask about measurement and consequence. What number do you get asked about, and by whom, and how often. Where does that number come from today, and do you trust it. Describe a bad week. What did it cost. How do you staff a peak. What would have to be true for you to change the process your team follows. Managers hold the definition of success, and critically, they hold the definition of failure, which is usually more concrete.

With the security lead, ask about classification and precedent. What class of data is in an incident description. Where may it be processed, and where may it not. What review gates exist before a system touches production data, and how long do they take. What have you refused before, and why. Do not ask a security lead to approve your architecture in a discovery interview. Ask them to teach you their constraints and their process. You are gathering the shape of the gate you will have to pass in chapter thirty five.

With the integration owner, ask about mechanics and pain. What is the system of record for tickets, for assets, for people. What integration surface actually exists, as opposed to what the vendor documentation claims. What are the rate limits, the change windows, the maintenance patterns. Who owns credentials and what does issuing one require. What breaks when someone calls your system too enthusiastically. Integration owners have usually been burned before, and their caution is data about your rollout plan.

Move three: use technique, not just curiosity. Three rules carry most of the weight.

Ask about past behavior, not future preference. What did you do last Tuesday produces evidence. What would you like the system to do produces speculation, and worse, it produces a feature list that you will feel obliged to honor. People are excellent witnesses to their own past and poor forecasters of their own future.

Ask for the exception. The main path is usually easy to learn and rarely where the cost is. Ask, when does this process not work. Ask, what was the weirdest one this month. In incident operations, a small minority of cases habitually consumes a large majority of the effort, and that minority is invisible in any summary a manager can give you.

Ask for artifacts, not opinions. Can you show me that ticket. Can I see the spreadsheet. Can you forward me the escalation email, redacted. An artifact anchors the conversation in something that actually happened and prevents the drift into how things are supposed to work.

And one discipline that is harder than it sounds: leave silence. When someone finishes a sentence and you wait three seconds instead of asking the next question, they very often add the caveat that matters. Engineers, especially engineers who are nervous about wasting a customer's time, fill silence. Do not.

Move four: observe the work. Interviews tell you what people believe about their work. Observation tells you what the work is. Sit with an operator through a real shift hour if you are permitted to, with synthetic or redacted data if you are not. Time the steps. Count the handoffs. Notice every moment they leave the system, because every exit to chat, phone, email, or spreadsheet is a seam where information is lost and where your system either helps or is irrelevant.

What you are producing here is a current state workflow map: the steps, who performs each, how long each takes, how long each waits, where decisions are made, and where the process leaves the tooling. Waiting time usually dwarfs working time, and that single realization reorders most delivery plans. If an incident spends four minutes being triaged and ninety minutes waiting for the right owner to notice it, then a smarter triage suggestion is worth far less than a reliable ownership lookup. Your existing asset pipeline may turn out to be more valuable than your agent. Let the map tell you.

Move five: synthesize before you conclude. Lay out findings by role, and specifically mark where they conflict. Do not resolve conflicts yet. The chapter mini project requires your scope to reflect at least two conflicting stakeholder needs, and that requirement is not a writing exercise. Real scopes contain real tension, and the FDE's job is to hold the tension visibly rather than average it into mush.

For FieldOps Copilot, the likely tensions are these. The manager wants automatic assignment because it removes a queue. The operator wants to keep the decision because they carry the blame. The security lead wants incident text never to leave a boundary, while the value of retrieval grounding depends on sending some of that text somewhere. The integration owner wants the fewest possible calls into the ticket system, while responsive suggestions want fresh data. Each tension has a real resolution, and none of the resolutions is a compromise in the middle. Automatic assignment becomes a pre filled decision with a one click confirm and a visible reason. The security constraint becomes a redaction boundary and a regional processing decision. The integration constraint becomes a cached read model with a stated staleness window, which, notice, you already built.

Move six: convert findings to requirements with a fixed shape. I want every functional requirement to name a trigger, an actor, an observable result, and a boundary. When an incident arrives with no recognized asset, the workspace shows the operator that asset context is unavailable, distinguishes unavailable from not found, and still allows manual assignment. That is testable. Compare it to: the system should handle missing assets gracefully. That second version cannot fail, which means it cannot pass either.

For nonfunctional requirements, insist on a number and the number's source. Not fast, but: the triage suggestion appears within six seconds at the ninety fifth percentile, because the operator's own tolerance in observation was roughly one screen refresh and the current tool takes eleven seconds. A number with a source can be negotiated. A number without a source will be negotiated away, because you will not be able to defend it.

Move seven: keep an assumption log with teeth. Every assumption gets five things: the claim, who or what it came from, why it matters, how it would be validated, and who owns validating it. Add one more column that most teams forget: what changes if this is false. That last column is what turns the assumption log into a planning instrument for chapter thirty four, because it tells you which assumptions are load bearing. An assumption that changes nothing if it is false does not need validating. An assumption that invalidates your architecture needs validating this week.

Move eight: write acceptance criteria that a pilot can actually run. This is where your existing engineering pays off, and where most requirements documents fail. An acceptance criterion needs three properties: someone can execute it, it produces a yes or a no, and the evidence it produces is recorded somewhere durable. You already have the machinery. Your evaluation suite can carry the deterministic criteria about structured output, citation presence, and refusal to take autonomous action. Your observability can carry the latency and failure rate criteria. Your audit table can carry the criteria about who approved what and when. Your operator acceptance rate is a metric your dashboard can hold. Write the criteria so they land on instruments you already own, and the pilot becomes measurable instead of anecdotal.

Move nine: rescope, and make the boundary hold. Discovery almost always produces more than the first release can carry. The discipline is to revise the charter without automatically expanding the release. Practically, that means writing three lists: what is in the first release, what is explicitly deferred with a trigger for reconsideration, and what is out of scope permanently with a reason. The word trigger matters. Deferred with a trigger sounds like: we will revisit automatic assignment when operator confirmation of the suggested owner exceeds ninety percent across two hundred incidents. That is a promise you can keep, and it protects you from the deferral being read as a refusal.

Move ten: capture the volume profile, because scope without volume is fiction. Back in chapter five you invented request volume, peak burst, response time, and retention in order to do a system design exercise. Now you replace those inventions with observed numbers, and you will find that the shape matters more than the average. Ask for the ticket export and look at four things. How many incidents per day, and how does that distribute across the hours. What fraction arrive in the worst hour of the worst day. What fraction are duplicates or reopens of the same underlying problem. And what is the tail of the age distribution, meaning how old is the oldest thing still open.

Those four numbers reshape design decisions you already made. If the peak hour carries eight times the median, your latency budget has to hold at the peak, not at the median, and your cost ceiling has to survive a bad afternoon. If a third of intake is duplicates, then deduplication is worth more than better categorization, and the idempotency work you did in chapter thirteen is closer to the core of the value than the agent is. If the age tail runs to weeks, then the real customer pain is abandonment, not triage speed, and a suggestion engine aimed at the first two minutes of an incident's life will not touch the problem the manager actually gets asked about. Notice how each of those findings would redirect the first release. That redirection is what discovery is for.

Move eleven: rehearse the translation on one sentence, completely. I want to walk this in full, because the gap between hearing a customer sentence and holding a testable requirement is where most requirements documents quietly fail, and the only way to close it is to do it slowly once.

The sentence is one you will hear in some form in almost every operations engagement. The manager says: we need the AI to handle the routine tickets so my team can focus on the real problems.

That sentence is not a requirement. It contains at least six unresolved questions, and every one of them is a place where you and the customer could shake hands while meaning different things.

Question one. What does routine mean, operationally. Not conceptually, operationally. Ask for examples: show me five from last week that you would call routine. Then ask what those five have in common that a system could detect at intake time. You will usually discover that routine means one of two very different things: either a recognizable category with a known procedure, or simply a low severity item that nobody minded losing. Those two definitions imply completely different systems.

Question two. What does handle mean. This is the dangerous one, because handle spans a spectrum from suggest a category, to pre fill the fields, to assign to an owner, to resolve and close without a human. Your entire architecture from chapter nineteen forward is built on the principle that the agent proposes and a human approves. If the manager means resolve and close, you have a fundamental conflict with the operator's need for control and with the governance boundary you established in chapter thirty two. Surface it now, not in month two.

Question three. Which team, and what do they actually do with the freed time. If the answer is a vague notion of higher value work, the benefit will be unmeasurable, and chapter thirty five's business case will collapse under scrutiny. If the answer is that two people currently spend their mornings on intake triage and would move to problem management, you have a measurable baseline and a measurable target.

Question four. What is the cost of being wrong on a routine item. Ask for the worst case. Sometimes a misrouted low severity request costs an hour of someone's patience. Sometimes an item that looked routine was the first symptom of a major outage, and the entire reason for human review is that the routine looking ones are occasionally not. That single answer determines whether your confidence threshold and your refusal behavior are conservative or relaxed.

Question five. Who decides that the system is allowed to handle a class of items, and can that decision be changed quickly. This is a configuration and governance question, and it belongs in the requirement. A system where the automation boundary can only be changed by redeploying is a system that will be turned off entirely the first time it misbehaves, because turning it off is the only control available.

Question six. What happens when it does not know. The most important behavior of a triage system is its behavior at the edge of its competence. Does it decline, does it guess, does it escalate, does it stay silent. Your retrieval work already gives you an insufficient evidence path. Make it a requirement so it cannot be dropped as an inconvenience later.

Now the translation. One customer sentence becomes a small family of statements. Functionally: when an incident matches a configured routine class and retrieval produces sufficient evidence, the workspace presents a complete pre filled triage proposal with its reason and sources, and the operator confirms with a single action or edits it. Also functionally: when the incident does not match a configured class, or evidence is insufficient, the workspace states that no proposal is available and why, and the operator triages manually with no loss of speed compared to today. Nonfunctionally: the proposal appears within six seconds at the ninety fifth percentile, and the routine class configuration can be changed by a named customer administrator without a deployment. As an assumption: two named operators currently spend a measurable share of each morning on intake triage, owned by the manager to validate from timesheets or observation. And as acceptance criteria: across the pilot's first two hundred incidents, at least seventy percent of proposals in configured classes are confirmed without edit, no proposal is applied without an operator action, and every applied proposal has an audit record naming the operator, the prompt version, and the sources.

Look at what happened there. One sentence, six questions, and now you have testable statements that connect directly to instruments you already own: your evaluation gate, your latency telemetry, your audit table, and your configuration boundary. That is the whole craft. The questions are not pedantry. Each one closes a gap where a delivery could have been declared complete and still failed.

## Part four. Pitfalls, named so you can catch yourself.

The feature interview. You ask what features they want, they tell you, and you have now converted your customer into a junior product designer and yourself into an order taker. Symptom: your notes are a list of nouns. Fix: for every feature they name, ask what happened that made them think of it, and record that instead.

The demo that ends discovery. You show FieldOps Copilot, people are impressed, and the room's energy tells you that you are done. Enthusiasm in a demo is a measure of your demo, not of your fit. Use the demo as an instrument of provocation: show it, then ask what is wrong with it, and keep asking until you get three real objections. If you cannot get three, you have not created enough safety for honesty.

The single source of truth. Every account has one talkative champion who is delightful to work with and will happily supply the entire picture. Their picture is one picture. Deliberately interview at least one person who does not like the project. Their objections are your risk register.

Requirements as adjectives. Intuitive, seamless, smart, robust, real time. These words feel like requirements and test like nothing. Every adjective must be converted into an observable behavior or dropped.

Silent scope inflation. It arrives in the phrase, and obviously it should also. It arrives most often from you, in a moment of wanting to be helpful. Say instead: that is worth doing, let me put it on the deferred list with a trigger, and let us decide it deliberately.

Skipping the exception path. If you only map the clean case, you will build for the minority of effort. Ask explicitly for the ugly ones and map at least two.

Nonfunctional later. Retention, residency, auditability, accessibility, and integration windows get labeled as hardening and pushed out. They are not hardening. They are the conditions of deployment, and discovering them in month three is how a pilot gets frozen.

Discovery without a decision date. There is always one more person to talk to. You owe the customer a scoping decision by a stated date, made on the evidence you have, with the gaps declared. An FDE who cannot decide under uncertainty is not being rigorous, they are being slow.

Recording opinion as fact. Notes that say the process takes twenty minutes, when what happened is that one person guessed twenty minutes, will be quoted back to you as a baseline in chapter thirty five. Attribute everything. Guessed, measured, and documented are three different confidence levels.

And the one specific to your situation right now: discovery to justify. Because you already built the system, there is enormous gravity pulling you toward hearing confirmation. You will unconsciously ask questions whose answers validate your agent, your retrieval, your pipeline. The counter measure is mechanical. Before you interview anyone, write down what you would have to hear in order to conclude that a major component you built is not needed in the first release. Write it down, in advance, specifically. Then listen for it.

## Part five. How you verify that your discovery was real.

Verification for a documentation heavy chapter is harder than for code, so here are the checks I trust.

The read back test. Read each requirement aloud to the person whose statements produced it and watch for correction. If they say yes, that is right, in a tone that means you have simply repeated their words, push harder. If they correct a detail, you have a real requirement now. Silent agreement is the weakest signal in field work.

The stranger test. Hand your requirements to a colleague who was not in any interview and ask them to describe how they would test three of them. If they cannot construct a test, the requirement is prose, not a requirement.

The conflict test. Point to the two conflicting stakeholder needs in your scope and to the sentence where you decided how to hold both. If you cannot find them, you either did not interview enough people or you averaged the conflict away.

The load bearing assumption test. Every assumption has an owner, a validation method, and a stated consequence if false. Any assumption whose consequence is severe and whose validation is unscheduled is a live risk that belongs in chapter thirty four's sequencing.

The subtraction test. This is the harshest and the most useful. Did discovery remove or reduce anything. If your first release boundary after discovery is the same size or larger than before, you did not scope, you collected. Name at least one thing you already built that will not be in the first release, or that will ship in a reduced form, and name why. If you genuinely cannot, then say so explicitly and record it as a finding that your invented charter was unusually lucky, which is possible but should be stated rather than assumed.

The testability test on success. Take your headline success measure and describe the exact procedure the pilot will use to produce it, with the sample size and the instrument. If the procedure requires data you do not collect, either change the measure or add the collection now.

## Part six. Your practice handoff.

The companion guide for this chapter is a test, not a tutorial, and it is deliberately not a checklist you can skim. Its goal is a revised FieldOps Copilot charter, a current state workflow map, a prioritized requirements set with functional and nonfunctional entries, an assumption log with owners and validation methods, and acceptance criteria that land on instruments you already built.

You will run four role play interviews with four distinct question sets. If you can recruit real people to play the roles, do that, and give them their role brief in advance without showing them your system. If you cannot, run them yourself as written interviews, but write them as transcripts with the awkward parts intact, not as summaries, because the awkward parts are where the conflicts live.

The rubric grades on evidence quality and boundary discipline, not on document length. Specifically, it looks for attribution on every finding, numbers with sources on nonfunctional requirements, at least two conflicting stakeholder needs held visibly rather than resolved by averaging, a deferral list where every item has a reconsideration trigger, and at least one honest subtraction from the first release.

Hints are at the end of the guide and inverted, so do not read them until you have produced a first draft. If you read them first you will write toward the hints instead of toward the evidence, and you will have practiced compliance instead of discovery.

## Part seven. Recap.

Discovery is evidence gathering about how work happens today, and it is descriptive. Scoping is a bounded decision about what you will build first, and it has an owner and a date. Requirements gathering is translation into statements someone else could test.

Keep four artifact types separate: findings, which are attributable observations, requirements, which are testable prescriptions, assumptions, which are declared and owned beliefs, and acceptance criteria, which return yes or no.

Functional requirements decide whether the demo works. Nonfunctional requirements decide whether the deployment happens. Get numbers, and get the source of each number.

Interview four different roles with four different question sets, ask about past behavior rather than future preference, demand the exception path, collect artifacts rather than opinions, and observe the work so you can see the revealed requirements that contradict the stated ones. Then synthesize, hold the conflicts visibly, and rescope without letting the first release grow by reflex.

For a forward deployed engineer, discovery is not upstream paperwork. It is the activity that determines whether thirty two chapters of engineering were aimed at anything, and it is the source of the evidence that lets you say no with authority. In the next chapter you will take these requirements and turn them into a sequence: which slice first, which risk retired earliest, which tradeoff made explicitly, and what happens when the first customer deployment goes wrong.
