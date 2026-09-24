# Chapter 2 project — Build a portable triage-priority rule

**Format:** open-book test. The chapter audio contains everything you need. No build steps are given.
**Prerequisite:** chapter 2 audio, plus the charter you produced in chapter 1.

---

## Goal

One priority rule, specified once and implemented three times, that behaves identically in all three runtimes — plus a defensible written choice of the single runtime you will use for the FieldOps service later in the course.

## Starting state

The charter and risk register from chapter 1. Nothing else. No repository yet, no service, no shared library.

Your charter supplies the inputs to the rule. If your customer's urgency is driven by different facts than the chapter's example, use yours — the exercise is about your customer, not about Harborline.

## Constraints

1. **The rule is pure.** Same inputs, same output, every time. No clock, no environment lookup, no file, no network, no logging side effect. Age is an input, not something the rule discovers.
2. **Three implementations, written by hand:** one in C++, one in Java *or* Scala, one in Go. No transpiling, no code generation, and no copying one implementation's structure line-for-line into another.
3. **One shared specification.** A single table of inputs and expected results drives all three. If the table and an implementation disagree, one of them is wrong and you must decide which.
4. **Ties are defined.** Two incidents that score equally must order deterministically, by a stated rule, in all three implementations.
5. **Invalid input is defined.** Every field must have stated behavior for missing, out-of-range, and wrong-shape values. Silent coercion to a default is a failure unless you deliberately chose it *and* wrote it down.
6. **Output serves a human and a machine.** A number for ordering and a band a coordinator can read.
7. **Performance is not the deciding argument.** If you benchmark, you must state whether the difference matters at your customer's actual volume.

## Required artifacts

| Artifact | What it must contain |
| --- | --- |
| Shared specification table | Input rows and expected priority plus band; must include at least one tie pair, one missing-field row, one out-of-range row, and one row whose expected result surprised you |
| Three implementations | C++, Java or Scala, and Go, each runnable and each checked against the full table |
| Runtime ADR | Context, decision, consequences, and the alternatives you rejected with the specific reason for each |
| Packaging note | For each runtime, what you would physically hand to the customer's platform team and what must already exist on the target machine |

## Self-grade rubric

**Pass bar — all six must be true**

1. **Agreement.** All three implementations produce identical numbers *and* identical bands for every row of the table.
2. **Purity.** None of the three reads a clock, an environment variable, a file, or the network. You can call any of them twice and get the same answer.
3. **Edges covered.** Missing, out-of-range, and wrong-type values each produce either a defined result or a clear refusal — never an unexplained number.
4. **Ties resolved identically.** Your tie pair orders the same way in all three, for the same stated reason.
5. **Hand-computable.** You can compute one table row on paper, out loud, without running anything.
6. **ADR names a rejected option and why.** A reader who was not in your head can tell you what you turned down and on what grounds.

**Quality marks — aim for at least four**

7. Confidence (or whatever you called your information-quality input) can lower a score but cannot inflate one, and you can explain the social reason that matters.
8. Your ADR separates technical fit from personal preference explicitly, including when they agree.
9. The ADR's reasoning is grounded in the customer's operating reality — who maintains it, where it runs — not in language aesthetics.
10. If you benchmarked, you stated plainly whether the difference is material at your volume. "Not a differentiator" is a valid and often correct finding.
11. The packaging note is concrete enough that a platform lead could react to it.
12. Your table contains a row you got wrong on the first attempt, and you kept it.

**Automatic fail**

- The three implementations disagree on any row, and you shipped anyway.
- The rule reads the current time internally.
- Tie ordering is left to whatever order the data happened to arrive in.
- An empty or unparseable severity silently becomes the lowest priority with no record.
- The ADR's central argument is performance, at a volume where performance is irrelevant.
- The ADR selects a runtime because you like it, with the customer reasoning reverse-engineered afterwards.

## Stretch

- Add a fourth implementation in a language you have never used, and time how long the specification table took to port. That number is a measure of how good your specification is, not of the language.
- Write the ten-minute conversation you would have with the platform lead about the runtime conflict between your velocity and their supportability. Include what you would concede.
- Extend the table with a row representing an incident class your charter does *not* cover, and decide whether the rule should refuse it or handle it.

## Verification you can run today

- Run the table against all three. Diff the outputs rather than eyeballing them.
- Boundary sweep: for each input, feed the lowest legal value, the highest legal value, one past each end, an empty value, and a value of an entirely wrong shape.
- Call one implementation twice with identical inputs and confirm byte-identical output.
- Hand the ADR to someone and ask them which option you rejected. If they cannot say, rewrite it.

---

<!-- tts:skip -->
## If stuck — inverted hints

Deliberately last, deliberately absent from the audio. Read one at a time, in order, after a real attempt.

1. Cannot start? Write the table first, with no implementation in mind. Five rows is enough to begin.
2. Cannot decide the weights? You do not have to get them right — you have to make them explicit. Pick something defensible, write down why, and let the table expose what feels wrong.
3. Rule keeps needing "now"? Ask what the caller already knows. If the caller knows when the incident arrived and what time it is, why is the rule discovering either of those?
4. Implementations disagree? Do not debug the code first. Reread the disagreeing row and ask whether your specification actually says what should happen. Most disagreements are underspecification, not bugs.
5. Rounding differences? Ask whether your specification says anything about precision or rounding direction. If it does not, that is the defect.
6. Stuck on invalid input? There are only two respectable answers. Which of them would an operator rather experience at three in the morning: a refusal with a reason, or a defined default that is recorded?
7. Ties feel rare? Construct one on purpose. What is the smallest change to two real incidents that makes them score identically?
8. Cannot tell which runtime to pick? Stop thinking about the language and ask who gets paged when it breaks at two in the morning, and what they already know.
9. ADR feels thin? For each rejected option, finish this sentence: "This would have been the right choice if ______ were true." If you cannot finish it, you have not understood the option well enough to reject it.
10. Suspect your choice is really a preference? Write the strongest one-paragraph argument *against* your choice. If that paragraph is better than your ADR, you have your answer.
<!-- /tts:skip -->
