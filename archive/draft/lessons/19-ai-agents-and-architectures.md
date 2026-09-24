# Chapter 19 — AI agents and agent architectures

**Roadmap nodes covered:** AI Agents; Agent Architectures
**Part:** IV — Build AI behavior that can be controlled
**Companion test:** `docs/guides/19-ai-agents-and-architectures.md`
**Audio:** `media/19-ai-agents-and-architectures.mp3`

---

## Narration

Welcome to chapter nineteen.

At the end of last chapter you had a loop. The model could request an incident lookup, your executor authorized and ran it, the result went back, and generation continued. I walked you through one turn and counted nine control points, all of them in your code.

But that loop is implicit. It lives inside your adapter as a while statement. It has no name, no states, no record, and if I asked you to show a customer what the system does, you would have to describe code.

Today we make it explicit. We give it states, legal transitions, stop conditions, an approval gate, and durable persistence. And along the way I want to have an honest conversation about the word "agent," because it is doing a great deal of marketing work right now and not much engineering work, and an FDE who cannot separate those two things will build something expensive that a hundred lines of ordinary code would have done better.

The plan: what an agent actually is, stripped of mystique. The spectrum from workflow to autonomy and why you should sit as far down it as you can. The honest test for when you need an agent at all. Then the architectures worth knowing. Then our state machine, stop conditions, the approval gate, durability, and retries. Then pitfalls, verification, and the test project.

### What an agent actually is

Here is the whole thing.

A model produces output. Your code inspects that output. If it is a final answer, you stop. If it is a request for a tool, you execute the tool, append the result to the context, and call the model again. Repeat until something tells you to stop.

That is an agent. There is no other ingredient. Everything else that gets called agentic is a variation on where the loop's decisions come from and what the stop conditions are.

I labour this because the mystique causes real harm. Teams treat "build an agent" as adopting a new kind of system rather than as writing a loop, so they reach for a framework before they have specified behaviour, and they end up with a system whose control flow lives inside somebody else's abstraction and whose failure modes they cannot enumerate. Then a customer asks "what happens if it gets stuck," and the honest answer is "I am not sure."

So the reframe I want you to carry: the model is not the agent. The model is a function that maps context to a proposed next step. The agent is your loop, your transitions, and your stop conditions. Those are ordinary software, written by you, testable by you, and they are where essentially all of the engineering value lives.

A consequence worth stating plainly: agent quality is mostly not model quality. A better model makes better proposals. It does not give your loop a deadline, a budget, a resume path, or an approval gate. I have seen teams respond to an unreliable agent by upgrading the model, when the actual problem was that no stop condition existed and the thing ran for forty steps. The model was fine. The loop was missing.

### The spectrum, and where to sit on it

There is a spectrum of how much decision-making you hand to the model, and the right instinct is to sit as low on it as the problem allows.

At the bottom: a deterministic workflow with a model call in it. Your code runs the steps in a fixed order, and at one point it calls the model to do something models are good at — turning messy text into a structured value. The control flow is entirely yours. This is not usually called an agent, and it is the right answer far more often than it gets used.

One step up: routing and chaining. Your code asks the model to classify, then branches on the classification into a fixed set of paths. The model influences control flow but only through a small, enumerated choice. Still highly predictable, still fully testable.

Next: the tool loop, which is what we have. The model chooses whether to gather more information, from a fixed set of read-only capabilities, within your budget. The set of possible behaviours is larger but still bounded, and the worst case is bounded by what the tools can do.

Next: planner and executor. The model produces a multi-step plan, and then the steps are carried out — either by the same model, or by a separate cheaper one, or by deterministic code. Now the model is choosing the sequence, not just the next step.

At the top: open-ended autonomy. The model decides goals, sub-goals, and actions, potentially spawning work, with write access to real systems. This is where demonstrations are most impressive and where production deployments are rarest, for reasons that are not cowardice.

The key sentence for a forward deployed engineer: every step up this spectrum buys flexibility and pays for it in predictability, cost, latency, testability, and explainability. Those are all things your customer's operations team cares about more than they care about flexibility. So the design question is never "how agentic can we make this." It is "what is the least autonomous architecture that solves the customer's problem," and then you build that.

### Do you need an agent at all?

Let me give you the honest test, because I think the most valuable thing an experienced FDE does in an AI project is occasionally say "this does not need to be an agent."

Signs you do not need one. You can enumerate the steps in advance. The sequence does not depend on the content in any way you cannot express as a branch. You already drew a flowchart. That last one is the giveaway: if you have drawn a flowchart and you are now writing instructions telling a model to follow the flowchart, stop and run the flowchart. You will get a system that is faster, cheaper, deterministic, trivially testable, and explainable to a customer, and you will lose nothing except the ability to say the word agent in a meeting.

Signs you might need one. The number of steps genuinely varies with the input in ways you cannot predict. Deciding what to do next requires interpreting unstructured content that only arrives mid-flight. The branching factor is large enough that enumerating it is genuinely impractical rather than merely tedious. Or the task requires recovering from unexpected intermediate results in an open-ended way.

Apply the test to FieldOps triage honestly. Most of what we do is deterministic: validate the incident, check completeness against required fields, compute priority. One part genuinely benefits from a model — reading messy human language and proposing a category and urgency. One part is genuinely conditional — whether to look up a referenced incident depends on whether the text references one, which only a reader can determine.

So what we need is a mostly-deterministic workflow with a bounded tool loop in the middle. Not a planner. Not autonomy. And I want you to notice that this is a slightly disappointing answer, and that arriving at slightly disappointing answers deliberately, with reasons, is most of what good architecture is.

### Architectures worth knowing

Four patterns. Know what each is for.

The reason-act-observe loop. The model reasons about what it needs, requests an action, observes the result, and repeats. This is the classic agent shape and it is what we have. Strength: adaptive within a bounded capability set. Weakness: no global view, so it can wander, and it is entirely dependent on your stop conditions for termination.

Planner and executor. The model first produces a plan, and then the plan is executed. The advantage that matters most in field work is not efficiency — it is that the plan is an artifact. It exists before anything happens. You can show it to a human, you can validate it against a policy, you can reject it, you can approve it. Approving a plan is a much more meaningful act of oversight than approving a result, because the human is intervening before cost and consequence rather than after. If you ever do need to let a system take consequential actions for a customer, plan approval is the pattern I would reach for first.

Within it, one design choice: plan once and execute the whole thing, or re-plan after each step. Re-planning adapts better and costs a model call per step. Plan-once is cheaper and more predictable and handles surprises worse. For anything with a human gate, plan-once is usually right, because a plan that keeps changing is a plan nobody can approve.

The state machine. Explicit named states, explicit legal transitions, explicit terminal states. Some transitions are deterministic; some are decided by a model call. This is the architecture I would default to for any enterprise deployment, and here is why. It is inspectable — at any moment the system is in a named state, which you can log, display, and query. It is resumable — the state is data, so a process restart or an approval arriving three hours later is not a special case. It is testable — you can drive every transition directly without invoking a model. It is explainable — you can draw it on a whiteboard for a customer and they will understand it, which is worth more than it sounds. And illegal transitions are structurally impossible rather than merely unlikely.

Reflection, or the critic pattern. The model reviews its own output and revises. It helps sometimes. Be sceptical: a model's self-assessment shares the blind spots of the generation that produced it, so it catches format problems and obvious inconsistencies far better than it catches confident factual errors. It also doubles your cost and latency. Where a second opinion genuinely matters, a differently-scoped reviewer with different context is more likely to help, and that is chapter twenty-one.

### Frameworks, and whether to use one

A practical detour, because you will be asked this in the first week of any AI engagement and the wrong answer is expensive in both directions.

There are agent frameworks that give you the loop, the tool plumbing, state handling, and often a graph or workflow abstraction. There are also durable workflow engines, built originally for distributed systems, that give you persistence, retries, timers, and resumability, and into which you can put model calls as ordinary steps.

The case for a framework is real. Loop plumbing is tedious and easy to get subtly wrong. Persistence and resumability in particular are genuinely hard to build well, and a durable workflow engine has solved them properly, with years of production hardening you are not going to reproduce.

The case against is also real, and it is specific to field work. A framework's abstractions determine your failure modes, and you will be debugging those failure modes at a customer site at an awkward hour. If a run gets stuck and the state lives inside a framework's internals, your ability to explain it to a customer is bounded by your understanding of somebody else's control flow. Frameworks also tend to encourage the shape they were designed for, and most were designed for more autonomy than you want. And they move fast, which means version churn in a deployment that may need to be stable for a year.

My practical position, offered as a default rather than a rule. Write the loop yourself — it is genuinely small, perhaps a couple of hundred lines with all the control points, and owning it means you can explain every failure. Take the durability from something proven, whether that is a workflow engine or just your own database with an explicit state column and an event table. What you must not do is adopt a framework because it makes the project sound more serious, or avoid one because building things yourself feels more rigorous. Decide it against the customer's operational reality: who will maintain this after you leave, what they already run, and what they can debug.

And whichever way you go, the test is the same: can you name every way a run can terminate, and can you drive each one in a test. A framework that makes that easy is a good framework. A framework that makes it hard is a liability regardless of what it saves you.

### The FieldOps triage state machine

Let us design ours. I will name the states and the transitions, and I want you to notice how much happens before any model call.

Received. The workflow starts when an operator requests a suggestion for an incident. Entry does two deterministic things: authorize the operator for this incident, and load the record.

Screening. A deterministic completeness check against required fields — is there an affected service, is there a symptom, is the description above a minimum substance threshold. If the report fails screening, we transition directly to needs-more-information with a generated list of what is missing, and we never call the model at all. This is the single most valuable transition in the machine. It is free, it is instant, it is perfectly reliable, and it handles a meaningful fraction of real intake. Cheap deterministic filters before expensive probabilistic ones is a principle that applies far beyond this system.

Gathering context. If the description references another incident identifier, the tool loop from chapter eighteen runs here, with its budget and its duplicate guard. This state may be skipped entirely.

Proposing. The single model call that produces the structured suggestion. On return: schema validation, category membership check, confidence range check. A response that fails validation transitions to failed, not to proposing again — or at most one retry, counted.

Awaiting approval. The suggestion is persisted and presented to the operator. This state can last minutes or days. The workflow is not running; it is stored.

Then the terminal states. Approved: the operator accepted, possibly with edits, and the edits are recorded because they are your best quality signal. Rejected: the operator declined, with a reason. Needs more information: the operator has been given the list of gaps. Failed: something went wrong, with a category and a message the operator can act on. Abandoned: the approval window expired without a decision.

Five things I want you to notice about that design.

Two of the terminal states are reached without a model call. Screening handles the thin reports; failure handles the broken ones.

There is exactly one model call in the happy path, plus at most a small number of tool calls. This is not an elaborate system, and that is deliberate — every additional model call is latency, cost, and a new failure mode.

There is no transition into any state that modifies the incident. Not because a check prevents it, but because no such state exists. Chapter eighteen's principle again: absence beats restriction.

Every terminal state produces something useful for the operator. There is no state whose outcome is "nothing happened."

And awaiting-approval is a first-class state, not a user-interface detail. This matters enormously for implementation, because it forces the state to be durable, which forces you to build the thing that makes the system survive a restart.

### Stop conditions

Now the most important section, and the one most commonly under-specified.

An agent without stop conditions is not an agent, it is a leak — of time, of money, and of your customer's confidence. You need five, and each needs a defined outcome.

A step budget. A hard maximum on transitions or model calls per workflow run. Small — for our machine, something like three or four model calls is generous. When exceeded, terminate with a defined failure that tells the operator the system could not complete the analysis and they should triage manually.

A wall-clock deadline. The whole run has a deadline, separate from any individual call timeout, because several calls that each finish just under their timeout can still take far too long together. On expiry, terminate and return whatever partial result is useful.

A cost budget. Token spend per run, enforced by your adapter's accounting from chapter fifteen. This is the one teams skip and then discover through an invoice. It is also the one your customer will ask about specifically, because "how much can one incident cost us" is a question with a right answer and it should be a number.

A no-progress detector. Repeated identical tool calls, cycling between the same two states, or the same validation failure twice. A loop that is making no progress is worse than a loop that fails, because it consumes budget while looking alive. Detect it explicitly and terminate.

And terminal success. Worth naming, because it is easy to build a loop with three ways to fail and no explicit condition for being done, which produces a system that keeps going after it has the answer.

The rule that binds these: every stop condition produces a defined outcome that a human can act on. Never a hang. Never a spinner. Never a silent empty result. When the system gives up, the operator should see something like "automatic triage did not complete; here is what we found; please triage manually," and the incident should be sitting in their queue exactly as it would have been if the copilot did not exist. Graceful degradation to the pre-AI workflow is the safest fallback you have, and it is available to you precisely because you kept the AI as advice.

### Human approval, done properly

Three things about the approval gate, because it is easy to build the shape of oversight without the substance.

First, what a human needs in order to decide well. Not just the suggestion. They need the proposal itself, the evidence behind it — which after chapter twenty means cited sources, and today means which incidents were looked up — the stated reason, a coarse confidence, an explicit statement of what the system could not determine, and a clear sense of what accepting will do. A bare suggestion with an accept button does not produce a decision; it produces a click.

Second, approval fatigue, which is the failure mode that quietly destroys these systems. If every suggestion requires an approval, and ninety-five percent of them are obviously fine, the human becomes a rubber stamp within a fortnight. You now have the cost of a human in the loop and none of the benefit, plus a false sense of safety, plus — this is the bad part — the customer believes there is oversight when there is not.

The fix is not to remove the gate. It is to make approvals meaningful and rare. Design the system so it asks for a human decision only where a human decision has content. Auto-apply the cases where the suggestion is exactly what the deterministic policy would have produced anyway. Group the routine into a single reviewable batch. Reserve individual attention for the low-confidence, the ambiguous, and the ones that would change something material. And measure your rubber-stamp rate: if approvals are being granted in under two seconds, your gate is decorative, and you should either raise the bar for what needs approval or lower the volume that reaches it.

There is a related question worth deciding explicitly: what is the default when nobody decides? If a suggestion sits unapproved for two days, what happens? The tempting answer is to auto-apply after a timeout, because it feels efficient and it keeps the queue clean. Resist it. A timeout-based auto-apply is autonomy with extra steps — it means the system takes the action whenever a human is busy, which is precisely when you least want it to. The correct default for a pilot is expiry: the suggestion lapses, the incident remains untriaged in exactly the state it would have been without the copilot, and the lapse is counted. If your lapse rate is high, that is a finding about adoption or staffing, and it should reach a human as a finding rather than being silently absorbed by an automatic decision.

Third, rejection is your most valuable data. When an operator rejects a suggestion or edits it before accepting, capture what changed and why, with a small set of structured reasons plus optional free text. That is ground truth generated by domain experts, for free, in production. It is the seed of your evaluation set in chapter twenty-two, it is the evidence for your pilot readout in chapter thirty-five, and it is how you know whether the thing is actually working. A system that collects approvals but not rejection reasons is throwing away the most valuable signal it produces.

### Durability and state

Because awaiting-approval can last for days, workflow state cannot live in memory. It has to be persisted, and that changes the design in ways worth being explicit about.

Each run has a durable record: an identifier, the incident it belongs to, the current state, the timestamp of entry into that state, the accumulated context, a step count, a cost total, and the correlation identifier that ties everything together for chapter thirty-one's tracing.

Transitions are recorded as events, append-only, exactly like the audit events you built in chapter thirteen. Two payoffs. You can reconstruct the complete history of any run — which is what you will actually need when a customer asks about a specific bad suggestion. And you can compute the operational metrics your pilot readout depends on: how many runs reached each terminal state, how long approval takes, what the rejection rate is.

Transitions must be idempotent. In a distributed system with retries, the same transition will be attempted twice. Attempting to move from awaiting-approval to approved when the run is already approved should be a no-op, not an error and certainly not a duplicate.

And draw a hard line between workflow state and knowledge. Workflow state is ephemeral bookkeeping about one run — it is completed and discarded. Knowledge is durable information about the customer's world. Conflating them is the most common design mistake in the next chapter, so plant the distinction now: this run's accumulated context is not memory, it is a scratchpad with a lifetime.

### Retries at the right layer

A short but load-bearing section.

Retry as close to the failure as possible. A transient provider overload is retried inside the adapter, with backoff and jitter, and the workflow never knows. A tool timeout is retried, once, inside the executor. Only a failure that the lower layers could not resolve becomes a workflow-level event.

Never retry the whole workflow as a blunt instrument. It re-runs transitions that already happened, re-spends budget, re-issues tool calls, and if any step had a side effect, does it twice. If you need to resume, resume from the persisted state at the transition that failed. That is exactly what the durable state is for.

There is a subtlety about budgets and retries interacting that catches people. If your adapter retries a provider call three times internally, and your workflow counts model calls for its step budget, decide which number the budget counts. Counting attempts makes the budget a cost control, which is what you usually want, because three retries cost three calls. Counting logical steps makes it a progress control. You probably want both: a logical step budget so the workflow cannot wander, and a cost budget in tokens that captures retries. Pick deliberately rather than discovering the answer when a retry storm slips past a step limit that was only counting successes.

And distinguish transient failures from semantic ones. A network error is transient; retry it. A schema validation failure is semantic — the model produced something invalid, and calling it again with identical context will probably produce something invalid again. Retry a semantic failure at most once, and only with something actually changed, such as an added note about what was wrong. Otherwise you are paying for the same mistake repeatedly.

### What this looks like when it goes wrong

Let me describe two failures I want you to have imagined before you meet them, because both are mundane and both are the kind of thing that decides whether a pilot continues.

The first. Three weeks in, an operator reports that the copilot "just spins" on certain incidents. You look, and the pattern is reports that paste in a long monitoring alert containing several identifiers that look like incident references but are not. The model dutifully looks up each one, gets not-found for each, concludes it needs more context, and looks up the next. It is doing exactly what it was told. Your step budget catches it eventually, but the budget was set at a generous ten calls, so "eventually" is forty seconds of an operator staring at a screen during an outage.

Three fixes, and notice their order. Immediately, drop the budget to something honest — three calls — because a generous budget is not generosity, it is a slower failure. Then add the no-progress detector, because three consecutive not-found results is a signal, not a coincidence. Then fix the actual cause, which is upstream: the tool description should say what a valid identifier looks like, and the executor should reject anything that does not match the format before it ever reaches the data layer. The deepest fix is the cheapest and it is the one you find last, which is normal.

The second. A month in, the operations manager mentions in passing that the team "just accepts everything." You check the data: approval within two seconds on eighty percent of suggestions, and a rejection rate near zero. The system looks like a triumph in the metrics and is in fact doing nothing, because nobody is reading the suggestions. Worse, the customer's security reviewer signed off partly on the strength of the human approval gate, and that gate is now decorative.

This is not a technical failure and there is no bug to fix. It is a design failure about attention. The response is to reduce what reaches a human — auto-apply the suggestions that match what the deterministic policy would have produced anyway, batch the routine ones into a single review, and reserve individual approval for low confidence and material change. And then to say something uncomfortable to the customer: that the oversight they were promised was not happening, that you found it, and here is the change. That conversation is unpleasant and it is exactly the conversation that builds the trust an engagement runs on. An FDE who surfaces their own system's weakness before the customer finds it is worth considerably more than one whose dashboards are always green.

### Pitfalls

Eight.

Building an agent where a workflow would do. The most expensive mistake in the chapter, and the least visible, because the agent works.

No stop conditions, or only a step limit. You need step, time, cost, and no-progress, and every one of them needs a defined outcome.

Workflow state in memory, so an approval that arrives after a deploy is lost.

Approval fatigue, producing the appearance of oversight without the substance.

Discarding rejections. Throwing away your best quality signal.

Retrying the whole workflow instead of resuming from the failed transition.

Implicit states. The system is "in the middle of something" but cannot say what, so you cannot log it, display it, or test it.

Letting the model decide when to stop. Termination is a property of your loop. An instruction telling the model to stop when it has enough information is a suggestion, and a compromised or confused model will ignore it.

### How you verify this chapter

Six checks.

One. Draw your state machine on paper. Every state has at least one way in and one way out, every terminal state produces something an operator can act on, and there is no state whose exit depends on the model choosing to leave.

Two. Drive every transition in a test without calling a model at all. If you cannot, your states are entangled with your adapter.

Three. Force each of the four stop conditions independently and observe the operator-visible result for each. None may be a spinner.

Four. Start a run, take it to awaiting-approval, restart the process, and approve it. If that does not work, your state is not durable and you will discover it in production.

Five. Make the model return garbage — a valid response that violates your category set, then an unparseable one, then the same unhelpful tool call five times. Confirm each terminates cleanly with a distinct, informative outcome.

Six. Look at your approval interface and ask whether you could make a real decision from it in ten seconds, including the ability to disagree. If the only thing it affords is agreement, redesign it.

### The test project

The companion guide is a test. Attempt it before the hints.

Your goal is a bounded triage workflow with explicit states, enforced stop conditions, durable state, and a meaningful approval gate.

You will produce: a state diagram with named states and legal transitions; the first two transitions implemented deterministically, before any model call, including a screening check that can reach a terminal state with no model involvement; a proposing state that permits only a structured suggestion using the read-only tool; an approval state that is durable across process restart and captures accept, edit, and reject with reasons; four enforced stop conditions each with a defined operator-visible outcome; and a simulation showing what happens when the model is unhelpful, invalid, and looping.

The constraints: no write tool exists; no state modifies the incident; workflow state is persisted and transitions are idempotent and recorded as events; every terminal state gives the operator something actionable; and termination is decided by your code, never by the model.

You are done when you can drive every transition without a model, when a restart mid-flight loses nothing, when all four stop conditions produce clean useful outcomes, and when you can hand the state diagram to a customer and have them understand exactly what the system will and will not do.

### Recap

The decision from this chapter: you made the loop explicit, and you chose the least autonomous architecture that solves the problem.

The reframe: an agent is a loop plus stop conditions. The model proposes; your code decides. Agent quality is mostly loop quality, not model quality.

The spectrum: deterministic workflow, routing, tool loop, planner-executor, open autonomy. Sit as low as the problem allows. If you have drawn a flowchart, run the flowchart.

The architecture: a state machine, because it is inspectable, resumable, testable, and explainable — and because illegal transitions become impossible rather than unlikely. Cheap deterministic filters before expensive probabilistic ones.

The stop conditions: steps, time, cost, no-progress, and success — each with a defined outcome, and graceful degradation to the manual workflow the customer already has.

The approval gate: give the human what they need to disagree, keep approvals rare enough to stay meaningful, and treat every rejection as the ground truth it is.

Next chapter, the model gets something it has not had yet: your customer's own knowledge. Retrieval, embeddings, chunking, citations, tenant isolation, and the freshness problem. And we will keep the distinction we just drew — this run's scratchpad is not the customer's knowledge, and confusing the two is how grounded systems quietly become ungrounded.
