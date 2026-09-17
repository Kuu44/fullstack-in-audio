<!-- tts:skip -->
## TTS notes — chapter 2

- Voice: `en-US-AndrewNeural`, rate `-14%` (about 146 words per minute).
- "C plus plus" is written out in prose so the voice says it correctly. Do not write the symbols.
- "Big oh" is written out; never write the mathematical notation.
- Say "F D E" as letters (handled by the renderer's substitution table).
- Recurring cast: Dana (sponsor), Sam (coordinator), Priya (security), Marcus (platform).
- `[pause]` becomes a beat of silence at segment turns.
- Nothing in this block is spoken.
<!-- /tts:skip -->

Welcome back to FullStack in Audio. This is chapter two: computer science, and the runtime choices a forward deployed engineer actually has to defend. [pause]

Last chapter you wrote a charter. Somewhere in it you promised that FieldOps Copilot would offer a suggested urgency for an incident. This chapter we take the first bite out of that promise, and it is a smaller bite than you might expect. We are going to build one rule that turns an incident's facts into a priority number. No service, no database, no model. One rule.

And then we are going to build it three times, in three different languages, and argue about which one belongs in a customer's environment.

If that sounds like busywork, let me tell you where this comes from. A forward deployed engineer's first serious technical conversation with a customer platform team is almost never about your clever architecture. It is a version of this question: "What is this thing going to be, and who here can keep it running?" Marcus, the platform lead at Harborline, has a team of four. They support a Java estate because the warehouse management system is Java. He has never deployed a Node service. He has heard of Go. If you arrive with a runtime nobody there can operate, you have handed him a problem and called it a solution.

So this chapter has two halves. First, the computer science that makes your code defensible — state, complexity, memory, concurrency, types, and compilation, taught as decisions rather than as trivia. Then the language comparison, done honestly, using the same tiny piece of logic implemented three ways.

## Why a priority rule is the right first piece of code

Before the theory, let me justify the exercise, because the choice of *what* to build first is itself a field skill.

The priority rule is the smallest piece of FieldOps Copilot that is genuinely customer-specific and genuinely valuable. Harborline's coordinators already do this in their heads: a refrigeration alarm at a depot with perishable inventory outranks a jammed dock door, which outranks a broken scanner on a slow afternoon. That judgment is the product. Everything else — the form, the database, the deployment — is plumbing around it.

It is also the piece you can get correct in a way you can prove. That matters more than it sounds. When you eventually add a model to this system, you will need a deterministic reference point: something that behaves the same way every time, that you can test exhaustively, that a customer can audit. If everything in your system is probabilistic, you have nothing to stand on when a recommendation is questioned.

So we start here. One function: facts in, priority out. [pause]

## The computer science that actually earns its keep

I am going to teach six ideas, and for each one I want you to hear the field consequence rather than the textbook definition.

### State

State is what your program remembers between one moment and the next. The most important question you can ask about any piece of code is: does this remember anything?

A function that remembers nothing — same inputs, same output, every single time, no clock, no network, no file, no counter — is called pure. Purity sounds academic until you notice what it buys you: you can test it exhaustively, you can reason about it in your head, you can run it in parallel without fear, and you can hand it to a customer's auditor and say "this is the whole rule."

Your priority function must be pure. If it reads the current time to compute how old an incident is, it is not pure, and it becomes untestable in a subtle way: your test passes today and fails at a month boundary or when someone runs it in a different time zone. The fix is not clever code. The fix is to pass the age in as an input and let the caller — the impure part of the system — decide what "now" means. That single habit, pushing time and randomness and input and output to the edges, will save you more debugging hours across your career than any framework you learn.

### Complexity

Complexity is how the cost of your work grows as the input grows. The vocabulary is big-oh notation, and for this chapter you need only the shape of it.

Constant cost means the input size does not matter. Linear means doubling the input doubles the work. Quadratic means doubling the input quadruples it. The reason a forward deployed engineer cares is not elegance; it is that customer volume is always larger than the demo, and it arrives in bursts.

Your priority rule is constant cost — it looks at a handful of fields. Good. But keep the number in mind: if the operations desk handles four hundred incidents on a peak day and the rule takes even a hundredth of a second, the whole day's triage arithmetic is four seconds. Nothing. This tells you that when triage feels slow later in the course, the rule will not be the reason, and you should not spend a day optimizing it. Knowing where the cost is *not* is as valuable as knowing where it is.

### Memory

Memory is where your data lives while the program runs, and who is responsible for cleaning up after it.

This is the dimension where our three languages differ most dramatically. In C plus plus, you are responsible. You decide what is allocated, when it is released, and who owns it. Get it wrong and you get a leak, or a crash, or — worst of all — a program that works in testing and corrupts data in production. In Java, Scala, and Go, a garbage collector handles reclamation for you. You trade control for safety, and you pay for it in occasional pauses and higher baseline memory use.

The field consequence: if you are deploying to a customer's constrained edge device in a depot, memory footprint and predictable pauses are real constraints. If you are deploying a service into a cloud container with a gigabyte of headroom, the garbage collector is a gift and worrying about it is a distraction. The correct answer depends on where the code lands, which is why this decision belongs in a document rather than in your habits.

### Concurrency

Concurrency is doing more than one thing at a time, or at least appearing to. Every one of our three languages offers it, and they offer genuinely different models.

C plus plus gives you threads and the full burden of coordination. Java gives you threads, a mature library of concurrency primitives, and, in recent versions, much lighter-weight virtual threads. Scala adds functional composition over futures and actor-style message passing. Go gives you goroutines and channels, which make concurrent code cheap to start and — this is the important part — cheap to *read*.

Here is the field consequence, and it is not about throughput. Concurrency bugs are the hardest class of defect to diagnose in someone else's environment. They are intermittent, they depend on timing you cannot reproduce, and they surface under load, which means they surface in front of the customer. When you are choosing a runtime for a system that a four-person platform team will maintain, the question is not "which is fastest" but "in which of these will a tired person writing a change at the end of a quarter be least likely to introduce a race."

Notice, too, that your priority rule sidesteps this entirely. Because it is pure, it is safe to call from a thousand concurrent requests. Purity is a concurrency strategy.

### Types

A type system is the set of promises the compiler will check for you before your program runs.

C plus plus, Java, Scala, and Go are all statically typed, which means those promises are checked at compile time. But they differ in how much they can express. Scala can encode quite a lot of your domain's rules in types — this thing is a severity, not merely an integer. Go deliberately keeps its type system simple, which makes code predictable and sometimes more repetitive. Java sits in between and has been steadily gaining expressiveness.

The field consequence is about change, not correctness. Customer requirements move. In week two, severity has three levels. In week seven, the customer adds a fourth and introduces a safety flag. In a language where your domain is encoded in types, the compiler becomes a checklist of everywhere you need to update. In a dynamically typed system, the same change becomes a search-and-hope exercise. Types are how you make a moving requirement safe to chase.

### Compilation and packaging

Finally, the least intellectually exciting and most operationally decisive property: what do you hand to the customer?

C plus plus produces a native binary, but one that is sensitive to the target system's libraries and architecture. Java and Scala produce bytecode that needs a virtual machine present, which is either trivial or a whole approval process depending on the environment. Go produces a single static native binary with no runtime dependency, which you can copy onto a machine and run.

The field consequence is enormous and routinely underestimated. "Copy one file and run it" versus "install and maintain a runtime" is the difference between a deployment you can do in a locked-down depot and one that requires a change request, a security scan of a new runtime, and a platform team meeting. I have seen a technically inferior choice win on exactly this ground, correctly. [pause]

## Why this is an FDE decision and not a preference

Let me be blunt about the professional stakes here, because this is the chapter where engineers most often behave badly.

Every engineer has a favorite language. This is fine, and in a product team it is mostly harmless: the team has a stack, you work in it. In the field, your favorite becomes a hazard, because you have unusual freedom and very little accountability for the years after you leave. You can absolutely choose the runtime you enjoy, ship a working pilot, and leave behind a component that the customer's team cannot debug. It will look like a success at handoff and become a quiet failure six months later. Nobody will write that down.

So here is the reframe. The runtime decision is a customer-fit decision with four inputs, in roughly this order of weight.

First, who operates it after you. If the customer's platform team can support one ecosystem and not another, that is not a tiebreaker; it is close to decisive. A system nobody can maintain is a liability regardless of its elegance.

Second, where it has to run and what it has to talk to. A component that must sit inside an existing Java application's process has effectively chosen Java. A component that must run on a depot machine with no runtime installed and no network at install time has effectively chosen a static binary.

Third, the shape of the work. Heavy numerical processing in a tight loop is genuinely a different problem from coordinating many concurrent network requests. Choose a runtime whose default answers match your dominant workload.

Fourth, and last, team velocity — including yours. This is real. A pilot that ships late is a failed pilot. But it is fourth, not first, and when it conflicts with the first input you have to say so out loud rather than quietly letting it win.

And there is a fifth consideration that is not a language property at all: how much of the system needs to make this choice. A great deal of field engineering skill is in keeping the polyglot surface small. If your priority rule is pure and its contract is written down, you can implement it in whatever the customer's environment wants without redesigning the rest of the system. That is what we are practicing this chapter: making the decision cheap by keeping the piece small. [pause]

## A runtime decision, narrated end to end

Let me walk one all the way through, so you can hear what a defensible decision sounds like when it is actually made.

Harborline needs two pieces of software eventually. One is the operations desk service: it receives incident reports, stores them, applies the priority rule, and serves the coordinators' screens. The other, later and smaller, is a depot-side agent that reads refrigeration telemetry from equipment on the local network and forwards summaries. Same customer, same system, two genuinely different runtime problems. Watch how the inputs land differently.

For the operations desk service, start with who operates it. Marcus has four people and a Java estate. That is a strong pull toward Java or Scala, because a defect at two in the morning gets diagnosed by someone who reads that language fluently and has the tooling already installed. Where does it run? In the customer's cloud account, in containers, with plenty of memory headroom, so garbage collection is a non-issue and startup time barely matters. What shape is the work? Coordinating network calls, database queries, and later model calls — concurrency-heavy but not compute-heavy. And what about team velocity? Here you have to be honest: if you personally are three times faster in one ecosystem, that is worth real money on a twelve-week pilot.

Now notice the tension. Inputs one and two point at the customer's existing ecosystem. Input four may point at yours. This is precisely the conflict I told you to say out loud rather than resolve quietly. The professional move is to name it to Marcus: "I would build this faster in a different runtime, and your team would support it worse. Which do you want to optimise, and can we get you training or shared ownership if we go my way?" That conversation takes ten minutes and it converts a future complaint into a joint decision.

For the depot-side agent, the inputs shift completely. It runs on a small machine in a warehouse, maybe an industrial computer that has been in place for years. Nobody is installing a virtual machine on it, and the change request to do so would take longer than the pilot. It must survive the network being down. It does very little work but must do it reliably and unattended. Here a single static binary with no runtime dependency is not a preference, it is nearly the whole answer, and that points at Go — or at C plus plus if you are integrating with a vendor library that only ships for it, which happens more than you would like in industrial environments.

Same customer. Two different correct answers. If you had a single favorite language and applied it to both, you would be wrong once, and the wrong one would be the deployment that fails quietly in a warehouse where nobody is watching.

One more thing this example teaches. Both of those components need the priority rule — or at least need to agree about urgency. Which is exactly why we built it as a small, pure, specified thing instead of as a method buried inside a service. The rule's portability is not an academic exercise; it is what lets you make two different runtime decisions without splitting your policy in two. [pause]

## How to design the rule before you write it in any language

Now the practical work. I am going to walk you through the thinking, not the code.

### Decide what goes in

From your charter you have a sense of what makes an incident urgent. At Harborline four things matter: how severe the operational impact is, how much business impact it carries — perishable inventory, a safety implication, a stopped production line — how long it has been waiting, and how confident we are in the information we have.

That last input deserves a comment, because it is the one people leave out. A report that says "fridge beeping, not sure which one" is not the same input as a report with a unit identifier and a temperature reading. If your rule treats them identically, you will get confident-looking priorities from unreliable facts, and coordinators will learn to distrust the number. Encoding confidence as an input is how you make the system honest about what it does not know.

### Decide what comes out

A number and a band. The number lets you order a queue. The band — critical, high, normal, low — is what a human reads.

Resist the urge to output only the number. Sam does not want to know that this incident scored sixty-seven; Sam wants to know it is high, and wants the ordering within high to be sensible. Design the output for the person, and keep the number for the machine.

### Decide the edges before the middle

This is the habit that separates code that survives a customer from code that does not. Before writing the ordinary path, decide what happens at every edge.

What happens when two incidents score identically? A tie must have a defined resolution — older first, or higher business impact first — because otherwise your queue ordering is at the mercy of whatever order the data arrived in, and that will look like a bug to an operator who sees two identical incidents swap places between refreshes.

What happens when severity is missing? When business impact is a value you have never seen, because a new depot started using a word nobody told you about? When age is negative, because a clock somewhere is wrong? When every field is empty?

There are only two respectable answers for a bad input: refuse it with a clear reason, or treat it as a defined default and record that you did. The unrespectable answer is the one most code takes by accident: produce a number anyway and say nothing. That is how a customer ends up with a critical incident sitting at normal priority because one field was blank.

Decide this once, in words, and then make all three implementations agree.

### Write the table before the code

Here is the single most useful technique in this chapter. Before implementing anything, write out the cases as a table of inputs and expected priorities. A refrigeration failure with perishable stock, fresh, well-described. The same failure with vague information. A scanner outage at low impact, three days old. Two incidents designed to tie. A record with a missing severity. A record with an impossible age.

That table is your specification. It is also your test suite, in all three languages. When you write the same table three times and get three matching sets of results, you have learned something real about all three languages, and you have a genuine artifact — a specification that outlives the implementations.

This technique is called table-driven testing, and it is the reason this project is possible at all. Without the table, "the same rule in three languages" is a matter of opinion. With it, it is a matter of evidence. [pause]

### A worked case, out loud

Let me do one case in words so you can hear the shape of the arithmetic without me reading code at you.

Suppose you decide severity contributes the most weight, business impact next, waiting time next, and confidence acts as a damper rather than a booster — it can reduce a score but never inflate it. That last design choice is worth pausing on. If confidence could raise a score, a well-written report about a trivial problem would outrank a vague report about a serious one, and coordinators would learn that writing lots of detail is how you jump the queue. Design decisions like this one have social consequences, and the social consequence is usually what determines whether the system survives contact with people.

So: a refrigeration alarm at a depot holding perishable stock. Severity is high, because product is at risk. Business impact is high, because there is inventory value and a customer commitment behind it. It arrived four minutes ago, so waiting time contributes almost nothing. The report includes the unit identifier and a temperature reading, so confidence is high and the damper does not reduce anything. It lands near the top of the critical band.

Now the same alarm, reported as "fridge beeping somewhere in the back." Severity is still high by category, business impact is still high, age is still small — but confidence is low, because you do not know which unit or whether it is even a refrigeration unit. The damper pulls the score down. Where should it land?

Here is the part I want you to actually think about, because it is a genuine design question with no obvious answer. If the damper drops it out of critical, you have built a system that de-prioritises badly-written reports about serious problems, which is exactly the report a stressed supervisor sends. If the damper does not move it at all, confidence is decorative. Most sensible designs do something in between: keep it high, but attach the missing information as the recommended next action, so the coordinator's first move is to ask which unit rather than to dispatch blindly.

That is the reasoning your rule should encode, and it is the reasoning you should be able to say out loud. Notice that I have not told you the weights, the scale, or the thresholds. Those are yours, and the rubric does not grade the numbers — it grades whether your edges are defined, your ties are resolved, and your three implementations agree.

Last thing on the table itself: include at least one row whose expected result you find surprising, and keep it. A specification that only contains cases confirming your intuition will not catch the bug that matters. [pause]

## Implementing it three times, and what you should notice

I am not going to narrate code. I am going to tell you what to pay attention to, because the learning is in the friction, and the friction is different in each one.

In C plus plus, notice how much of your attention goes to representation. How do you express a severity — an enumeration, an integer, a string? What happens when the input string does not match anything? You will find yourself making decisions about memory and ownership for a function that barely needs any, and you will notice that nothing stops you from reading a value that was never set. Notice how good the performance is and how little you needed it. Notice how much care the error path took.

In Java or Scala, notice the ceremony and the payoff. You will write more structure — a type for the incident, a type for the result. In exchange, the compiler will catch the case you forgot, especially in Scala if you model severity as a closed set of possibilities. Notice how the packaging conversation goes: you now have a build tool, a dependency graph, and an artifact that needs a virtual machine present. Notice whether that is a problem in your imagined customer environment or a non-issue.

In Go, notice the bluntness. You will probably write your validation by hand, check errors explicitly at each step, and find the code slightly repetitive and extremely easy to read. Notice how quickly you got to a runnable program, and notice what you hand over at the end: one binary, no runtime.

And across all three, notice the thing that actually matters for your ADR: how hard was it to make the invalid input behave correctly? Because that — not raw speed — is the property that determines whether a system degrades gracefully in a customer's environment, where the data is always worse than your test fixtures.

When all three agree with your table, do the comparison properly. For each language write down, in ordinary sentences: how errors are expressed and whether they can be ignored by accident; what you ship and what must already be present on the target; the concurrency model and how likely a maintainer is to misuse it; and whether the customer's team could support it. That is four short paragraphs and it is worth more than a benchmark.

Speaking of which: be careful with benchmarks here. Measuring a constant-time function three ways will produce a number, and that number will tempt you to conclude something. It is nearly meaningless for this decision. The honest sentence in your ADR is "all three are far faster than this workload requires, so performance is not a differentiator", and writing that sentence is a sign of maturity rather than laziness. [pause]

## What an architecture decision record is, and how to write one that is worth reading

Your artifact for this chapter is an ADR — an architecture decision record. It is a short document capturing one decision, at the time you made it, with the reasoning intact.

It has four parts and they are all short. The context: what situation forced a decision, including the constraints that were true at the time. The decision: what you chose, stated plainly. The consequences: what this makes easy and what it makes hard, including the things you now cannot do cheaply. And the alternatives: what else you considered and the specific reason each was not chosen.

That last part is where the value lives, and it is the part people skip. A record that says "we chose Go" is a note. A record that says "we chose Go because the component must run on depot machines where no runtime can be installed, accepting that the customer's Java-fluent platform team will need to learn a second ecosystem, which the customer's platform lead agreed to on this date" is an asset. Eighteen months later, when someone asks why this thing is not Java like everything else, the answer exists and nobody has to relitigate it from memory.

Two disciplines make ADRs useful rather than ceremonial.

Write them at decision time, not at documentation time. An ADR written afterwards is a justification, and it will quietly omit the constraint that actually drove the choice.

And separate technical fit from preference explicitly. If you wanted Go because you enjoy Go, and it also happens to fit, say both. The honesty costs you nothing and it tells a future reader how much weight to put on the reasoning. If you cannot find a customer-grounded reason at all, that is important information: it means the decision was preference, and preference decisions should be the ones that are easiest to reverse. [pause]

## The failure modes

Let me name how this chapter's work goes wrong.

The first failure is the impure rule. Time creeps in, or a configuration lookup, or a small piece of logging that writes a file. The function still works, and it is now untestable at the edges and unsafe to parallelize. The tell is a test that behaves differently on a Monday.

The second failure is three rules that merely resemble each other. You implement the same idea three times, each slightly differently — one rounds, one truncates, one treats a missing field as zero. Without the shared table you will never notice, and you will have learned the wrong lesson: that the languages behave differently, when in fact your specification was incomplete.

The third failure is undefined tie behavior. Ties will happen, more often than you expect, because real severity and impact values cluster. If ordering within a band is arbitrary, operators see items shuffle and conclude the system is unstable.

The fourth failure is silent coercion of bad input. An empty severity becomes zero, and a critical incident lands in the normal queue. This one is dangerous precisely because nothing looks broken.

The fifth failure is the benchmark conclusion. You measure, you find a difference of microseconds, and you write an ADR that justifies a runtime choice on performance grounds that are irrelevant at your workload. A platform team will spot this immediately, and it costs you credibility on the decisions where you *are* right.

The sixth failure is the preference dressed as analysis. You know it when you see it: a decision matrix with weights chosen after the answer. If your comparison has no line that is uncomfortable for your preferred option, you have not compared anything.

And the seventh, which is strategic rather than technical: spreading the polyglot surface. Choosing three languages is educational for you and a maintenance burden for a customer. Your ADR should end with exactly one runtime for the service you will build later, and the other two implementations should be understood as an exercise, not as an architecture. [pause]

## How you verify this chapter's work

Verification one: run your table against all three implementations and confirm the outputs match row for row. Not approximately. Exactly, including the bands and the tie ordering.

Verification two: take one case out of the table and hand-compute the expected priority on paper before running it. If you cannot compute your own rule by hand, it is too complicated to explain to a customer, and a rule you cannot explain is a rule that will not be trusted.

Verification three: the boundary sweep. For each input, feed the lowest legal value, the highest legal value, one beyond each end, an empty value, and a value of the wrong shape entirely. Every one of those must produce either a defined result or a clear refusal — never a surprise.

Verification four: the tie test. Construct two incidents that score identically and confirm all three implementations order them the same way for the same stated reason.

Verification five: the packaging test. For each implementation, write down literally what you would hand to Marcus, and what would already need to be present on his machines. Then ask yourself, honestly, which of those three sentences he would be happiest to receive.

Verification six: the ADR read-back. Give the ADR to someone who was not in your head. Ask them which option you rejected and why. If they cannot tell you, the record has failed at its only job. [pause]

## Your project

Here is the handoff. The project guide asks you to build a portable triage-priority rule: one specification, three implementations, one defensible runtime choice.

Your goal is a rule that behaves identically in C plus plus, in Java or Scala, and in Go, plus an architecture decision record selecting one runtime for the FieldOps service you will build in a later chapter. The constraints are that the rule must be pure — no clock, no network, no storage — that you write each implementation yourself rather than generating or translating one from another, that ties and invalid values must be defined behavior, and that the inputs come from the charter you wrote in chapter one rather than from my example.

The artifacts you owe are the three implementations, the shared table of inputs and expected priorities including boundary and invalid cases, and the ADR that separates technical fit from personal preference.

Grade yourself against the rubric before reading the hints. [pause]

## Recap

The ideas worth carrying forward.

Push state, time, randomness, and input-output to the edges, and keep your domain rules pure. Purity is what makes a rule testable, auditable, parallel-safe, and explainable to a customer.

Know where your cost is and where it is not. Constant-time work on hundreds of records a day is not your performance problem, and saying so plainly is part of the job.

Memory management, concurrency model, type expressiveness, and packaging are the four axes on which runtimes actually differ in the field, and packaging is the one that most often decides a deployment.

The runtime decision is a customer-fit decision: who operates it, where it must run, what shape the work is, and only then how fast your team moves in it.

Write the table before the code. A shared specification is what turns "three implementations" from an opinion into evidence.

Decide the edges before the middle. Refuse bad input or default it deliberately, and never silently coerce it.

And write the decision down while the reasoning is still true, including the alternative you rejected and the reason you rejected it.

In chapter three we leave the comfort of a pure function and step into the customer's actual machine: Linux, the shell, and Python. You will turn this rule into something a human can run, with input validation, failing behavior, and evidence left behind. Bring your table — chapter three's project checks the Python implementation against it.

That is chapter two. Go build the rule three times.
