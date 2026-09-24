# Chapter 22 — Evaluation pipelines and regression testing

**Roadmap nodes covered:** Building Eval Pipelines; Regression Testing
**Part:** IV — Build AI behavior that can be controlled
**Companion test:** `docs/guides/22-evaluation-pipelines-and-regression-testing.md`
**Audio:** `media/22-evaluation-pipelines-and-regression-testing.mp3`

---

## Narration

Welcome to chapter twenty-two.

Over the last seven chapters you have made a great many claims. That the provider you chose is a good fit. That version three of the prompt is better than version two. That the retrieval is grounded. That the split into two specialists helped, or did not. That the system declines when the evidence is thin.

Some of those claims you supported with fixtures. Most of them, honestly, you supported with your judgment and a few examples you looked at.

That is fine for building. It is not fine for shipping to a customer, and it is nowhere near enough for changing something after you have shipped. Today we build the machinery that turns every one of those claims into a number, and that stops a bad change before a customer meets it.

This chapter is the one that makes the rest of part four defensible. It is also, in my experience, the single biggest difference between teams whose AI features improve over time and teams whose AI features drift.

The plan: why evaluation is genuinely different from testing. The layers, and evaluating at the narrowest one that can see the failure. Building a fixture set that is representative rather than convenient. The four kinds of check, and the critical rule about which of them may block a merge. Baselines and version attribution. Handling non-determinism honestly. Designing the gate. Closing the loop with production signals. The cost of all this. Then pitfalls, verification, and your test project.

### Why this is not just testing

You know how to test software. Four things make this different, and each one changes the design.

Output is non-deterministic. The same input can produce different output. So an assertion of equality is not a test, it is a coin flip with extra steps. Everything must be expressed as a property that holds, or as a rate across repeated runs.

There is often no single correct answer. For a genuinely ambiguous incident, two categories may both be defensible. A test framework wants a right answer. Reality offers a set of acceptable ones, and sometimes a judgment about usefulness rather than correctness.

Quality is graded, not binary. A suggestion can be correct but unhelpfully vague, or wrong but usefully close. Collapsing that to pass or fail throws away most of the information.

And the system has many independently moving versions. Your application code, your prompt, your model, your model's silent update, your embedding model, your index contents, your tool contracts, your retrieval parameters. A quality change can come from any of them, and — this is the part that has no analogue in ordinary software — one of them can change with no diff in your repository at all. Your provider can update a model behind an alias and your system behaves differently on Monday than it did on Friday. No commit, no deploy, no cause you can find by reading code.

That last property alone justifies building this. It means you need a way to detect behaviour change that does not depend on you having changed something.

### The layers

Evaluate at the narrowest layer where the failure can be detected. This is the organizing principle and it saves enormous amounts of time.

At the bottom, ordinary unit tests against your deterministic fake, from chapter fifteen. Fast, free, offline, and they cover your handling of every failure mode. They test your code, not the model.

Next, component evaluations. Retrieval recall, from chapter twenty — does the correct passage appear in the top results. Schema validity rate. Classifier accuracy on cases with known categories. Each of these isolates one part.

Next, end-to-end evaluation: the whole workflow on a fixture, judged on its final output.

Then safety and abuse evaluation, which I treat as its own layer because it has different pass criteria — these are not graded, they are absolute.

And finally online evaluation: what happens in production, which after chapter nineteen means operator accept, edit, and reject signals.

Here is why the layering matters so much. Suppose your end-to-end pass rate drops from eighty-five percent to seventy. An end-to-end-only suite tells you something broke. A layered suite tells you retrieval recall fell from ninety to sixty while classification accuracy held, which points you at the indexing change somebody made on Tuesday. The first costs you a day of investigation; the second costs you a minute.

And the component evaluations are cheap. Retrieval evaluation needs no language model at all — it runs in seconds and costs nothing, so you can run it on every commit. That is the highest-return evaluation in the system and it is the one most teams never build.

### Building the fixture set

Your fixtures are the whole game. A perfect harness over bad fixtures measures nothing.

Representativeness first. The natural failure is to write cases you find interesting, which skews toward the clear and the exotic and misses the boring middle where most real volume lives. Before writing fixtures, characterize the real distribution — with the customer, from their historical tickets if you have access, or from their operators' description if you do not. What fraction are thin one-line reports? What is the category distribution, including the rare ones? How much jargon and pasted log content? Then build fixtures in roughly that shape.

Coverage dimensions to span deliberately: severity across the range; ambiguity, from clear to genuinely contested; completeness, including reports missing critical fields; jargon and log density; length, from one line to several pages; every category including the rare ones, because rare categories are where accuracy is worst and where nobody looks; multiple tenants; and the safety cases.

The safety cases deserve naming individually, because they are the ones that get dropped for feeling repetitive. A prohibited-action attempt, where the report asks the system to close or escalate. A prompt injection attempt in the description. An indirect injection, planted in a retrieved document. A cross-tenant retrieval attempt. And a sensitive-content case, to check redaction. Those five never get removed, and every one of them has a binary pass criterion.

Size. Start at ten to twenty. Do not wait for a hundred; a small suite that runs is infinitely better than a large one you are still building. Then grow it from reality, which brings me to the single most important habit in this chapter.

Every production failure becomes a fixture. Every one. An operator rejects a suggestion for an interesting reason: fixture. A customer reports a bad categorization: fixture, added before you fix it, so you can prove the fix works and prove it stays fixed. This is how the suite becomes genuinely representative over time — not by you imagining cases, but by reality supplying them. A team that does this for three months has an evaluation set that no amount of upfront design could have produced.

Provenance. Label every fixture as synthetic, sanitized-from-real, or real-with-consent. This matters for two reasons: sanitized fixtures need a review process to confirm the sanitization worked, and real fixtures may carry retention obligations. Keep the label on the fixture so nobody has to remember.

And holdout discipline, from chapter sixteen. Keep a portion you do not look at while tuning. Without it you will optimize against the cases you can see and learn nothing about the ones you cannot.

### The four kinds of check

Now, what you actually assert. Four kinds, and the distinction between them determines what may gate a merge.

Deterministic structural checks. Binary, cheap, unambiguous. Is the output schema-valid. Is the category in the allowed set. Is confidence in range. Does every citation correspond to a passage that was actually retrieved. Was any write attempted — always no. Did the system decline when retrieval was below threshold. Did the run terminate within its step, time, and cost budgets. Did the injection fixture fail to alter behaviour. Did the cross-tenant query return nothing.

These are the backbone. They are fast, they are certain, and they can block a merge without anyone arguing about them.

Reference-based checks. For fixtures where you know the right answer, compare against it. Exact match on category. Overlap between the expected and produced missing-information lists. For ambiguous cases, accept a set of acceptable answers rather than one.

Property-based checks. Invariants that must hold for any output, regardless of the case. The output never contains a personal name. Urgency never exceeds a threshold without supporting evidence. And a particularly useful one: run the same fixture several times and check that the category is stable. Inconsistency across identical inputs is a measurable quality property and a strong signal that your criteria are underspecified. Most teams never measure it, and it is one of the most diagnostic numbers you can have.

Judged checks. For "is this actually useful to an operator," where no mechanical check suffices. Two forms: a human rubric, and a model acting as a judge.

I want to be careful about model judges, because they are popular and they are easy to misuse. They are genuinely useful for scoring at a volume humans cannot reach. They also have known biases: a preference for longer and more verbose answers, a tendency to favour output from the same model family, sensitivity to position when comparing, and a general reluctance to give harsh scores. So: give the judge a specific rubric with concrete criteria rather than asking whether the answer is good. Validate it against human labels on a sample before trusting it, and re-validate periodically. Report its scores as an indicator, not a truth. And never let a model judge be the sole gate on a merge.

Which brings us to the rule that organizes this whole chapter.

### Evaluating the path, not just the answer

One kind of check that gets overlooked, and that your chapter nineteen state machine makes available almost for free.

Most evaluation looks at the final output. But for a workflow with states and tool calls, the path matters independently of the answer. Two runs can produce the identical suggestion while one took a single model call and the other took four, made three redundant lookups, and nearly hit its budget. Those are not equally good runs, and an output-only suite scores them the same.

So assert on the trajectory. Which states were visited, and in what order. How many tool calls were made. Whether screening correctly short-circuited on a thin report instead of proceeding to the model. Whether retrieval ran when it should have and was skipped when it should not have been. How much of the step, time, and cost budget was consumed.

Three reasons this pays for itself. It catches efficiency regressions before they show up as a cost surprise — a prompt change that makes the model call the lookup tool twice as often produces an identical answer and double the bill, and nothing but trajectory assertions will find it. It catches safety-relevant behaviour that the output does not reveal: an injection attempt that fails to change the final suggestion but did cause an extra tool call is a partial success for the attacker and worth knowing about. And it is cheap, deterministic, and gateable, because the state sequence and the call count are facts, not judgments.

A concrete pair worth asserting from day one: thin reports must terminate in screening with zero model calls, and clear reports must complete in exactly one model call plus at most one tool call. Both are binary, both are fast, and either one breaking tells you something specific went wrong upstream of the answer.

### What may block a merge

Deterministic checks gate. Judged checks inform.

A schema violation, a fabricated citation, a successful injection, a cross-tenant leak, a budget overrun, a missing decline on weak evidence — these block the merge. They are binary, they are reproducible, and nobody has to negotiate about them.

A drop in judged usefulness from seven point one to six point eight does not block anything. It raises a flag, it goes on a dashboard, it gets a human to look. Because a stochastic judge with its own biases producing a small delta is not evidence of a regression, and a gate that blocks on it will produce false failures, and a gate that produces false failures gets bypassed within a fortnight. Then you have no gate at all.

This is the most common way evaluation pipelines fail in practice, and it is worth saying plainly: the failure mode is not too little gating, it is gating on the wrong things and then being ignored. A small, fast, certain gate that is always respected is worth far more than a comprehensive one that people route around.

Safety cases sit in their own category: they gate absolutely, with no threshold and no tolerance. A failed injection fixture does not reduce a score, it stops the change.

### Designing a rubric that a human or a judge can apply

Since judged checks are where most of the subtlety lives, let me be concrete about writing one, because "rate the usefulness from one to ten" produces numbers that mean nothing and cannot be reproduced by two different reviewers.

A usable rubric has three properties. It asks about observable features of the output rather than about your feelings toward it. It defines each level with a description, not just a number. And it is narrow enough that two people applying it to the same output land within one point of each other.

For our triage suggestion, I would build it as three separate small rubrics rather than one aggregate score, because aggregates hide the thing you need to know.

Actionability. Does the suggestion tell the operator something that changes what they do next? Top level: names a category and urgency that the operator would act on, and lists a missing item that is specific enough to ask the reporter about. Middle: correct but generic, adds little beyond what the operator could see in ten seconds. Bottom: vague, restates the report, or lists missing information that is obvious or irrelevant.

Groundedness. Is the claim supported by the evidence cited? Top: every substantive claim traces to a cited passage, and the passage genuinely says what the rationale implies. Middle: cited passages are relevant but the rationale extends beyond them. Bottom: citation is decorative, or the passage does not support the conclusion drawn from it.

Calibration. Does the stated confidence match the actual quality? Top: confident when right, and declines or flags uncertainty when the evidence is thin. Bottom: confidently wrong — which should be scored as the worst possible outcome, worse than declining, because a confident wrong answer costs an operator more time than no answer at all.

That last point is worth dwelling on. Your scoring should encode the asymmetry of real cost. In an operations context, an unhelpful decline costs a few seconds. A confident wrong routing costs an hour of the wrong team's time and delays the fix. If your rubric treats those as equally bad, your measurement is telling you to build the wrong system. Make the penalty for confident error explicitly larger, and make sure whoever wrote the rubric agrees that the weighting matches how their team actually experiences the cost.

And validate the rubric before you trust it, whether a human or a model is applying it. Take twenty outputs, have two people score them independently, and look at the disagreement. If they diverge by more than a point regularly, the rubric is underspecified and no amount of judging volume will fix it. Then, if you are using a model judge, score those same twenty with the judge and compare against the human labels. That comparison is the only evidence that your judge measures anything, and it should be redone whenever you change the judge model — which, remember, can change underneath you.

### Baselines and attribution

Every evaluation run is stored with the complete version tuple: application version, prompt version and hash, tool contract version, model identifier and version, embedding model, retrieval index revision, and the retrieval parameters. Plus the fixture set version, because your fixtures change too and comparing across different fixture sets is meaningless.

That tuple is what makes results comparable and causes attributable. Without it you have a number with no context, and the question "what changed" has no answer.

Two specific uses.

When quality moves after a change, you compare tuples and see exactly which component differs. Usually one thing, and that is your cause.

And when quality moves with no change at all — same application version, same prompt, same index — you have detected provider drift. That is the failure mode with no diff, and this is the only way you will catch it. Which is why the suite should also run on a schedule against the live provider, not only on commits. A nightly run with a stable tuple is your early warning that the ground moved.

This also feeds directly into chapter twenty-six. A release manifest that pins all these versions and carries the evaluation result for that exact combination is what lets you tell a customer what changed, how it was measured, and how to go back.

### Non-determinism, handled honestly

Because output varies, a single run of a fixture tells you very little.

So run each fixture several times — three to five for a working suite — and record the pass rate rather than a pass or fail. Then express your criteria as rates. Schema validity must be a hundred percent. Safety fixtures must be a hundred percent. Category accuracy on clear cases might be ninety-five. Judged usefulness might be a target average.

Two consequences worth internalizing.

An eighty percent pass rate is not a flaky test to be fixed or ignored. It is a real, measured property of the system, and it should be reported to the customer as such. "The system suggests the correct category on roughly nine out of ten clear reports, and declines rather than guessing on thin ones" is an honest, useful statement. "It works" is not.

And you need enough repetitions to distinguish real movement from noise. A pass rate moving from eighty to seventy-five across three runs of ten fixtures is almost certainly noise. Know roughly how much variation your suite produces when nothing has changed — run it twice against an identical tuple and look — and set your alerting threshold above that. Otherwise you will chase ghosts, and chasing ghosts is how people stop trusting the suite.

### Closing the loop

Offline evaluation measures what you thought to test. Production measures what actually happens, and you already built the collection mechanism in chapter nineteen.

Every operator decision is a labelled example. Accept means the suggestion was good enough. Edit means it was close, and the diff tells you exactly what was wrong — which is the richest signal of all. Reject with a reason means it was wrong, and you know the category of wrongness.

Three things to do with that.

Track the rates over time as your primary online quality metric. Acceptance rate, edit rate, rejection rate by reason. This is what goes in your pilot readout in chapter thirty-five, and it is far more persuasive to a customer than any offline score, because it is their own people's judgment.

Convert failures into fixtures, as discussed. Sample rejections weekly, pick the interesting ones, add them.

And watch for divergence. If your offline scores are strong and your production acceptance rate is poor, your fixtures are not representative of reality, and fixing the fixtures is more urgent than fixing the model. That divergence is one of the most valuable signals you can have, and you only get it by measuring both.

One caution: acceptance rate alone can mislead, as we discussed last chapter. If operators are rubber-stamping, acceptance approaches a hundred percent and means nothing. Pair it with time-to-decision and with a periodic sample reviewed carefully by a human. A high acceptance rate with a two-second median decision time is not a quality signal, it is an attention signal.

### The evaluation report as a delivery artifact

One more use for all this, and it is the one that most directly affects whether your pilot continues.

Your evaluation results are not just an engineering tool. They are the most credible thing you can put in front of a customer, and most teams never show them.

Think about what a customer is actually deciding at the end of a pilot. Not "is this technology impressive" — they saw a demo months ago. They are deciding whether to depend on it, which means they are estimating how it will behave on cases they have not seen, and how they will find out when it degrades. An evaluation report answers both questions directly, in a way a demonstration cannot.

What to include. The composition of the fixture set, so they can see what was tested and challenge it — and they should challenge it; a customer telling you "you have no fixtures for after-hours reports from the night shift" is a gift. The pass rates by category, including the rare ones where performance is worst, because volunteering your weakest number is what makes the strong ones believable. The safety cases and their results, stated absolutely. The production acceptance, edit, and rejection rates from their own operators. And the gate itself: what blocks a release, so they know a regression cannot quietly ship.

What to be careful about. Do not present a single headline percentage; it invites comparison to numbers from other vendors that were measured differently, and you will lose that comparison or win it dishonestly. Do not present judged scores as if they were measurements. And do not hide the decline rate — the fraction of cases where the system says it does not know is not a failure statistic, it is a safety feature, and framing it that way from the start prevents somebody later treating it as a defect to be optimized away.

The sentence I would aim to be able to say, with evidence behind every clause: on cases like these, it suggests the right category about this often; on thin reports it declines rather than guessing; on the safety cases it has never failed; your operators accept its suggestions at this rate and edit them at this rate; and here is the gate that stops a change that would make any of that worse.

That sentence is worth more than any feature you could add in the same time.

### What this costs

Evaluation is not free and pretending otherwise leads to a suite nobody runs.

A full end-to-end run over fifty fixtures, five repetitions each, with two roles per run, is five hundred model calls. Add a judge and it is a thousand. At realistic prices that might be a few dollars per run, which is trivial once but not trivial on every commit from every engineer.

So tier it.

On every commit: unit tests against the fake, plus retrieval evaluation. Seconds, zero cost, no network. This catches a surprising amount.

On every pull request that touches prompts, models, retrieval, or tool contracts: the deterministic end-to-end suite against the full fixture set, with safety cases. Minutes, modest cost. This is your gate.

Nightly: the full suite including judged checks and the larger fixture set, against the live provider, with results stored by version tuple. This catches drift and tracks trends.

Before a release: everything, plus human review of a sample.

The point of the tiering is that the fast tier must be fast enough that nobody minds, because the fast tier is the one that actually runs.

### The deliberate break

I want to single out one exercise, because it is the one that tells you whether any of this works, and because it is easy to skip.

Break something on purpose, and check that the gate catches it.

Pick a change that is plausible rather than absurd — not "delete the prompt," but the kind of mistake a tired engineer makes on a Friday. Remove the clause in the prompt that tells the system to decline on thin evidence. Halve the number of retrieved passages. Loosen the citation validation to check only that a citation is present rather than that it was retrieved. Broaden a category discriminator slightly. Swap the model for a cheaper one in the same family.

Then run the suite and observe three things. Did it fail? Did it fail on the right check, or did it produce a vague overall score drop? And did the failure name the layer, so someone reading the output knows whether to look at retrieval, the prompt, or the model?

You will usually learn something uncomfortable the first time you do this. The most common discovery is that removing the decline instruction does not fail anything, because your fixture set has no case where declining is the correct answer. That is a real gap and you would not have found it any other way — certainly not by looking at a passing dashboard.

Do this deliberately at least once per significant component, and keep the broken variants around as a meta-test. A suite that has never been shown to fail is a suite you are trusting on faith, and a green dashboard that cannot go red is worse than no dashboard, because it manufactures confidence.

There is a customer dimension to this too. When a security reviewer or an operations lead asks how you know the system is safe, "we have tests" is weak. "We regularly introduce specific faults and demonstrate that the gate catches them, here are the faults and here is what happened" is a genuinely different class of answer, and it is available to you for the cost of an afternoon.

### Pitfalls

Eight.

Fixtures that are all happy paths. If your suite has no case that should decline, no prohibited-action attempt, and no injection, it measures capability and says nothing about safety.

Gating on a stochastic judge. Produces false failures, produces bypasses, produces no gate.

Comparing runs across different fixture sets or different version tuples, and drawing conclusions from the difference.

Evaluating only end to end, so a failure tells you something broke but not what.

Treating a pass rate below a hundred percent as flakiness to be suppressed rather than a property to be reported.

Never adding production failures to the suite, so the fixture set stays as naive as the day you wrote it.

No holdout, so you optimize against what you can see.

Only running on commits, so provider drift — the failure with no diff — goes undetected until a customer finds it.

### How you verify this chapter

Six checks.

One. Deliberately break something — weaken the injection defence, or remove the citation validation, or degrade retrieval by halving the result count. Run the suite. It must fail, and the failure must name the layer. If it passes, your suite does not cover the thing you most care about.

Two. Run the suite twice with no changes at all. The variation between those two runs is your noise floor, and any alerting threshold below it is a ghost generator.

Three. Look at your gate and count how many checks are deterministic and how many are judged. If a judged check can block a merge, move it.

Four. Pick a fixture at random and ask whether a real incident from this customer would look like it. If your fixtures all read like they were written by an engineer, they were, and they are not representative.

Five. Take the last real failure you saw and confirm it exists in the fixture set. If it does not, the habit has not formed yet.

Six. Compare your offline score against your production acceptance rate. If they disagree substantially, trust production and fix your fixtures.

### The test project

The companion guide is a test. Attempt it before the hints.

Your goal is an evaluation gate that can detect a behaviour change without a human reading every answer.

You will produce: at least ten synthetic incidents spanning severity, ambiguity, missing information, rare categories, and prohibited-action attempts, with labelled provenance and a holdout portion. Measurable checks across the four kinds — deterministic structural, reference-based, property-based including a consistency check across repeated runs, and at least one judged check with a written rubric. A baseline run of the current workflow, stored keyed by the full version tuple. A deliberately harmful change — to a prompt or to retrieval — with a demonstrated failing regression that names the responsible layer. And a gate configuration where deterministic and safety checks block, and judged quality routes to human review.

The constraints: safety cases pass absolutely or the change stops. No judged check blocks a merge on its own. Results are comparable only within a version tuple. Each fixture runs multiple times and criteria are expressed as rates. And your noise floor is measured, not assumed.

You are done when your deliberate break fails the gate and names the layer, when the fast tier runs in seconds on every commit, and when you can state your system's quality as a set of numbers you would be comfortable putting in front of the customer.

### Recap

The decision from this chapter: you made every claim in part four measurable, and you put a gate in front of the ones that matter.

Why it differs from testing: output is non-deterministic, correctness is often a set rather than a value, quality is graded, and one of your dependencies can change with no diff in your repository.

The structure: evaluate at the narrowest layer that can see the failure. Retrieval evaluation is cheap, fast, model-free, and it is your ceiling.

The fixtures: representative of the real distribution rather than of your imagination, spanning ambiguity and rarity and the five safety cases, with a holdout — and grown from production failures, which is the habit that matters most.

The checks: deterministic, reference-based, property-based, and judged. And the rule that organizes everything — deterministic and safety checks gate, judged checks inform. A small certain gate that is respected beats a comprehensive one that gets bypassed.

The bookkeeping: every result stored with its full version tuple, and a scheduled run against the live provider so drift is caught before a customer catches it.

The honesty: report pass rates, not pass or fail. Know your noise floor. And when offline and production disagree, believe production.

Next chapter, the last of part four, we take the system you have measured and make it fast and affordable without giving back the quality — latency budgets, token accounting, caching, model routing, and a fallback that is useful rather than an infinite spinner. And the evaluation gate you just built is what makes that optimization safe, because it is the thing that tells you when a cheaper path has quietly become a worse one.
