<!-- tts:skip -->
## TTS notes — chapter 3

- Voice: `en-US-AndrewNeural`, rate `-14%` (about 146 words per minute).
- No commands, paths, or flags are written in this script. Everything is described in words on purpose.
- "standard out" and "standard error" are spelled out in prose; never write the abbreviations.
- Recurring cast: Dana (sponsor), Sam (coordinator), Priya (security), Marcus (platform).
- `[pause]` becomes a beat of silence at segment turns.
- Nothing in this block is spoken.
<!-- /tts:skip -->

Welcome back to FullStack in Audio. This is chapter three: Linux, the shell, and Python for field work. [pause]

Let me start with the moment this chapter prepares you for.

You are on a call with Marcus, the platform lead at Harborline. He has given you access to a single Linux machine inside their network — a jump host, as it is usually called, from which a few internal systems are reachable. You have this access for a pilot, it took two weeks to approve, and Priya in security signed off on a narrow scope. Marcus says: "You've got it. What do you need?"

Everything you do on that machine is now a professional statement. If you leave a credential in a file readable by everyone, you have undone Priya's approval. If you start a process and cannot tell anyone later what it did, you have created an unexplainable event in their environment. If you write a script that only works because of something you typed once and forgot, you have built a system with you as a dependency — the thing chapter one told you not to do.

This chapter is about being competent and trustworthy on someone else's computer. That is a genuine skill with a real reputation attached, and it is separate from your ability to write software.

By the end you will build the first thing in this course that another person can actually run: a command-line intake program that takes an incident, validates it, applies the priority rule you built in chapter two, and leaves behind evidence of what happened. Small, unglamorous, and the first piece of FieldOps Copilot that exists as software rather than as a document.

## What Linux actually is, for our purposes

Linux is the operating system almost every service you deploy will run on, and for field work you need a working mental model of five things: files, permissions, processes, environment, and ports. Not exhaustive knowledge — a model good enough to reason and to ask precise questions.

### Files, and the idea that everything is one

In Linux, an enormous amount of the system presents itself as files. Your configuration is a file. Your log is a file. The randomness source is a file. Information about running processes appears as files. This is not trivia; it is why the same small set of habits — look at it, follow it as it grows, search it, copy it — works on almost everything.

The practical field consequence is that when something is wrong, there is almost always a file that knows. Somebody's service will not start, and the answer is in a log file. A connection is refused, and the answer is in a configuration file that someone edited eight months ago. Your instinct should be to go find the file that knows, rather than to guess.

### Permissions, and the question "who can read this"

Every file has an owner, a group, and a set of permissions describing what the owner, the group, and everyone else may do with it: read, write, or execute.

Here is the only sentence about permissions that matters in the field: for every file you create on a customer's machine, you should be able to say who can read it and why that is acceptable.

Because the failure looks like this. You create a configuration file containing a database password. It is readable by everyone on the machine. On your laptop, "everyone" is you. On a customer's shared jump host, "everyone" includes contractors, automation accounts, and whoever else has been granted access over five years. You have not been compromised, and you have created an audit finding that will be discovered at the worst possible time, probably by Priya, probably in the week of the pilot review.

The habit is a boring one, and it separates professionals from talented amateurs: when you create anything holding a secret, restrict it to the account that needs it at the moment you create it, not later.

Related: least privilege. Do not run as the all-powerful administrative account because it is convenient. Not because a rule forbids it — because when something goes wrong, the scope of what could have gone wrong is determined by what your process was permitted to touch. A mistake made by a limited account is an incident. The same mistake made by an unrestricted account is an investigation.

### Processes, and knowing what you started

A process is a running program. It has an identifier, a parent, an owner, a working directory, an environment, open files, and a state.

The field skills here are simple and confidence-inspiring when you have them. You should be able to find out what is running, who started it, when, and what it has open. You should be able to stop something politely — asking it to shut down and letting it finish — and know the difference between that and killing it outright, which gives it no chance to flush its work. You should know that a process which does not release its resources on shutdown will eventually cause a problem someone else has to diagnose.

And you should know how to leave a machine as you found it. Starting something you cannot cleanly stop is one of the fastest ways to lose a platform team's trust.

### Environment, and why configuration does not belong in code

Every process has an environment: a set of named values handed to it when it starts. This is the conventional place to put the things that change between your laptop, the pilot machine, and production — a database location, a log level, a feature switch.

Two rules, and they are both about the boundary between configuration and secrets.

The first rule is that anything which differs between environments is configuration and must come from outside your code. If your program has a hard-coded address, it is not deployable; it is transcribable.

The second rule is subtler and trips people up. Environment variables are a fine way to *deliver* a secret to a process and a poor way to *store* one. They are visible in ways people forget: they are often inherited by child processes, they frequently show up in crash reports and process listings, and they get printed by the helpful diagnostic someone writes at two in the morning. Later in this course we will use a real secret store. For now, the discipline is that a secret is never committed, never printed, and never logged, and your example configuration file contains the shape of the values with obviously fake contents.

### Ports, and the boundary of a service

A port is the number a network service listens on. Two things cannot listen on the same one, and being unable to reach a service usually comes down to a small set of questions: is it running, is it listening on the address you think, is something else already using that port, is a firewall in the way, are you connecting from somewhere allowed to.

You do not need a port for this chapter's program, because it is a command-line tool. But learn the questions now, because in chapter eleven you will start a service and something will refuse to connect, and the difference between a confident engineer and a flailing one is having an ordered list of questions instead of a feeling. [pause]

## The shell, and why repeatability beats cleverness

The shell is the program that turns typed lines into work. Bash is the one you will meet most often. For field work, three properties of it matter more than any syntax.

The first is composition. Small programs connected by streams: the output of one becomes the input of the next. This is why you can do remarkable things with tiny tools, and why a Linux-literate engineer looks fast. Data flows through a chain.

The second is exit status. Every command ends with a number: zero means success, anything else means failure. This is the entire foundation of automation. A script that ignores exit status is a script that reports success while doing nothing, which is worse than a script that fails, because it is a lie you will believe.

I want to be emphatic here, because this is the single most common flaw I see in glue code written by strong engineers. A chain of commands where an early step failed and the later steps ran anyway will produce a confident-looking result built on nothing. In the field this shows up as a data load that "succeeded" with an empty file. Your automation must stop when something fails and must exit with a nonzero status so whatever called it knows.

The third is the difference between standard out and standard error. Results go to standard out. Diagnostics go to standard error. Keep them separate and you can pipe a program's results into something else while a human still sees the complaints. Mix them and you have a program that cannot be used in a pipeline and cannot be monitored cleanly.

Now, the judgment call about the shell: how much of your system should be shell?

My answer, having watched this go wrong: use the shell for orchestration — run this, check that it worked, capture the output, decide what to do next — and use a real language for logic. The moment a shell script contains arithmetic, string parsing, or branching more than about two levels deep, it has become software written in a language with no types, no tests, and terrifying quoting rules. Rewrite it in Python before somebody inherits it.

The corollary is the good part: a short, honest shell task is one of the most valuable things you can leave a customer. It is the executable version of "here is how you run this." When Marcus asks how to start the thing, a documented shell entry point is a better answer than a paragraph in a document, because it cannot drift out of date without breaking. [pause]

## Python, and why it wins in the field

Python is not the fastest language available to you, and for field integration work that is almost never the constraint. What Python offers is a better trade for this specific job.

It is readable by people who are not you. A customer's engineer who works mostly in Java can read and modify Python with confidence, which means your automation is not a black box you are leaving behind.

It has a library for almost every system you will be asked to talk to, which is what integration work actually consists of.

It is present or trivially installable nearly everywhere, which matters when an installation requires an approval.

And it is fast to write, which matters because field code is often written under time pressure with incomplete information, and needs to be changed the next day when the information improves.

Two habits make Python safe in a customer environment.

The first is isolation. Use a virtual environment so your dependencies belong to your project rather than to the machine. Installing packages into a customer's system-wide Python is a genuinely rude act: you are modifying shared state that other software depends on. It is also how you create the failure where your program works and something unrelated breaks a week later.

The second is pinning. Record exact dependency versions. "It worked on my machine" is usually a version story. In the field this is worse than annoying, because the machine that differs is often the one you cannot easily inspect.

Let me also say something about how to structure a small Python program, because most field code lives at exactly this size and it is where quality is cheapest to add.

Separate three things. First, the domain logic — your priority rule — which stays pure, exactly as in chapter two. Second, the boundary: reading input, writing output, exiting with a status. Third, validation, which sits between them and decides whether the input is even eligible to reach your logic.

Keeping those separate means you can test the rule without simulating a person typing, and test the validation without caring about the arithmetic. It also means that when the customer asks "what exactly are the rules for a valid incident", you have somewhere to point.

One more thing worth saying now: the Python implementation of the rule must agree with your chapter two table, row for row. This is the first moment in the course where you will feel the value of having written that table. You are not reimplementing from memory; you are implementing against a specification. [pause]

## How to design a command-line program someone else can trust

A command-line program is an interface, and it deserves the same care as a screen. Here is what makes one trustworthy.

### It tells you what it wants

When run with no useful input, it explains itself: what it does, what it needs, what it produces. The unhelpful version prints a usage line and exits. The helpful version tells you what a valid incident looks like in plain language.

### It validates before it acts

Validation is where you decide what your program will accept, and it deserves real thought rather than an afterthought.

For each field from your charter: is it required, what values are acceptable, what does the program do when it is missing or nonsense. And critically: does the program refuse everything at once, or one problem at a time? Refusing one problem at a time is a miserable experience — the operator fixes the severity, resubmits, and learns the depot is also wrong. Collect the problems and report them together.

An error message must do three things: say what is wrong, say where, and say what an acceptable value looks like. "Invalid input" does none of them. "Severity must be one of low, medium, high, or critical; you gave 'urgent'" does all three, and it teaches the operator the vocabulary rather than scolding them.

### It uses exit status honestly

Success exits zero. Invalid input exits nonzero. An internal failure exits nonzero, and ideally with a different status than invalid input, because "the human typed something wrong" and "the program is broken" deserve different responses from whatever is calling you.

This is the property that makes your program usable inside automation, which is what it will eventually be doing.

### It leaves evidence

Your program should record what happened: when it ran, what it was asked to do, what it decided, and how long it took. That is the primitive form of something we build properly in chapter thirty-one, and starting the habit now costs you nothing.

But — and this matters — evidence is not a dump of the input. Incident descriptions written by a stressed supervisor can contain names, phone numbers, customer references, and occasionally things you really do not want in a log file on a shared machine. So decide deliberately what you record. An identifier, the structured fields, the computed result, a timestamp: yes. The full free-text description: probably not, or not until Priya has told you where logs go and who can read them.

That decision, made early and written down, is the difference between an observable system and a data exposure with good intentions.

### It writes results to standard out, and complaints to standard error

So the result can be captured by a pipeline while a human still sees the diagnostics. Small thing, marks you instantly as someone who has done this before. [pause]

## Diagnosing a real machine safely

Let me give you the field method, because this is what the role looks like on a difficult day.

You will get a call: something is not working. You will have limited access, limited time, and an audience. The method that works is to reduce the space of possibilities in an order that costs least.

Start with the question "is it running at all". Then "is it running as who I think, from where I think". Then "what does it say" — find the log, read the end of it first, because the most recent complaint is usually the closest to the truth. Then "what does it have open" — files, connections. Then "can I reach it from where the user is", which is frequently a different answer from "can I reach it from here".

Three disciplines make this safe on someone else's system.

Change one thing at a time, and write down what you changed. An undocumented change during an incident is a gift to your future self's confusion, and when someone asks later whether anything was modified, "I think so, let me remember" is a bad sentence.

Prefer reading to writing. You can learn an enormous amount without modifying anything. Reserve modification for when you have a hypothesis you can state out loud.

And announce destructive actions before you take them, to whoever is accountable. Not for permission theatre — because a platform team needs to know what happened in their environment, and because a surprise is the one thing that makes a calm engineer look reckless.

The corresponding failure modes are worth naming. Guessing and fixing, where you change three things, it starts working, and nobody knows why — including you, which means it will happen again. Fixing without recording, so the knowledge dies with your session. And the most common one: diagnosing from your own assumptions rather than from the machine's evidence. The machine is telling you what is wrong. Go find the file that knows. [pause]

### A diagnosis, narrated

Let me make that concrete with the kind of problem you will actually get.

Marcus messages you: the nightly job that copies incident exports onto the jump host "isn't working." That is the entire report, and it is a realistic one.

You do not start by reading the job. You start by asking what "not working" means to the person who noticed. In this case, a folder that should have a file from last night does not have one. Good — now you have an observable symptom rather than an opinion.

First question: is it running at all? You look for the process, and it is not there, which is expected for a job that runs and exits. So you look at whatever scheduled it and find that it did run, at the time it should have, and finished quickly. Suspiciously quickly.

Second question: what did it say? You find its log, and you read the end first, because the last thing a program says before it stops is usually the closest thing to the truth. The end says nothing useful — it just stops mid-way. So you read a little further back and find a line about a directory, and then silence.

Third question: what was it allowed to do? You check the target directory, and here is the answer: the directory is owned by a different account, and the job's account can list it but not write to it. Somebody fixed a permissions finding last month — correctly, from a security standpoint — and the job has been failing silently every night since.

Now notice the two failures stacked on top of each other, because this is the real lesson. The permissions change is not the bug. The bug is that a job failed for three weeks without telling anyone. It exited, it produced no alarm, and its exit status was almost certainly zero, because someone wrote a chain of commands where a failed copy did not stop the script.

So what do you actually do? You do not fix the permissions yourself, because that directory belongs to someone else's decision and Priya may have made it deliberately. You write down what you found, in three sentences, with the evidence: the job ran, it could not write to the target, the target's ownership changed on this date. You take that to Marcus and let the person who owns the decision make it. And you point out the second problem — the silent failure — because that is the one that will bite them again in a different place next month.

That is the shape of a good field diagnosis. Observable symptom, ordered questions, evidence from the machine rather than from your assumptions, a clear statement of the two separate problems, and no unilateral change to something you do not own. It took twenty minutes and you modified nothing. [pause]

## What using your program should feel like

Let me describe the experience you are building toward, because it is easy to write a program that technically works and is miserable to use.

Sam starts the program. It tells Sam, in one short paragraph, what it does and what it needs: a title, how bad it is, which service or equipment is affected, what the business impact is, and a description. It does not make Sam guess the vocabulary — it says what the acceptable severity words are.

Sam types a real incident, in a hurry, the way people actually do: the title is fine, the severity is typed as "urgent", the depot is right, the impact field is left blank because Sam does not know yet.

The program comes back with two problems at once, not one. Severity must be one of low, medium, high, or critical, and "urgent" is not among them. Business impact is required, and here is what acceptable values look like. Sam fixes both and resubmits.

Now the program prints the result in a form Sam can read: the incident as it understood it, the priority band in plain words, the numeric score if Sam cares, and — this is the part that earns trust — the reason. Not a paragraph of prose. Just which factors pushed it up and which held it down. "High severity, high business impact, low information confidence" tells Sam something actionable, which is: go find out which unit it is.

And when Sam is done, something is recorded, somewhere Sam does not have to think about, that says an incident was assessed at a certain time with a certain outcome.

Notice what is missing from that description. No mention of storage, no mention of a service, no network call. Sam's experience is complete and honest at this size. That is the discipline of a first release: build a thing that is genuinely finished at a small scope rather than a scaffold that only makes sense once four more chapters exist.

Notice also that the reason is a design decision with consequences downstream. The moment your system shows its reasoning, people start arguing with the reasoning — which is exactly what you want, because their objections are the domain knowledge you have not captured yet. A system that shows only a number gets ignored. A system that shows why gets corrected, and corrections are free requirements. [pause]

## Leaving it behind: documentation as a deliverable

One more thing before failure modes, and it is the part engineers under time pressure skip.

Your program needs a short written run procedure: what must be installed, how to set up the isolated environment, how to run it, what a successful run looks like, and what the common failures mean. Five or six lines is plenty. The test of it is not whether it is elegant — it is whether someone can follow it on a machine that has never seen your project.

Write it as you go, not at the end. Documentation written afterwards suffers from a specific disease: you cannot see the steps you no longer notice yourself taking. The things that are obvious to you after two hours of work are precisely the things that will stop a new person, and you have already lost the ability to see them.

Two small habits make this much better. First, write down dependency versions as you install them, not from memory afterwards. Second, when you hit a confusing failure yourself during development, write the fix into the document immediately, in the operator's language. Your own confusion is the best available sample of your reader's confusion, and it has a short shelf life. [pause]

## The failure modes for this chapter's project

The first failure is the secret that escapes. A password in a committed file, a token printed in an error message, an example configuration file that contains a real value because it was easier. This is the failure with the longest tail: once a secret has been in a repository's history, removing it from the current version is not enough.

The second failure is the program that reports success while doing nothing. Validation that logs a complaint and continues. A shell task that ignores a failed step. An exit status of zero when the incident was rejected. Each one of these turns your program into an unreliable narrator.

The third failure is the drifting rule. The Python priority differs from your chapter two implementations by a rounding decision, a default, or a boundary. Now the system has two policies and no one knows which is authoritative. Run the table.

The fourth failure is the works-on-my-machine program: system-wide package installs, unpinned dependencies, a path that only exists in your home directory, a value you typed into your shell once and never wrote down. The test is brutal and simple — a clean shell, following only your documentation.

The fifth failure is log-everything. It feels responsible, and it puts free-text incident descriptions into a file on a shared machine where you do not control the readers. Observability without a data decision is a liability.

The sixth failure is the permission you did not think about. You created a directory, it inherited whatever the default was, and now your evidence file is world-readable. Decide, do not inherit.

And the seventh, which is about you rather than the code: the untidy exit. A process left running, a temporary file left behind, a port still held. Leave the machine as you found it, plus the thing you were asked to add and nothing else. [pause]

## How you verify this chapter's work

Verification one, and it is the one that matters most: the clean-shell test. Open a new terminal, in a new session, with none of your environment, and follow only your own written instructions. No remembered steps. Everything that fails is a documentation defect, and this test is the closest thing this chapter has to a grade.

Verification two: the table test. Run your chapter two specification table through the Python implementation and confirm every row matches, including bands, ties, and invalid cases.

Verification three: the rejection test. Feed it a malformed record and check three things — it refuses, it says what was wrong in a way a person could act on, and it exits nonzero. Then check that your shell task also exits nonzero, because that is where this usually breaks.

Verification four: the secret sweep. Search your project for anything resembling a credential, including the history if you have started committing. Then read your own log output and error messages and confirm no secret and no unnecessary free text is present.

Verification five: the permission read-back. For every file your program creates, state who can read it and why that is acceptable. If you cannot answer for one of them, that is your next task.

Verification six: the tidy test. Start the program, inspect its process, stop it cleanly, and confirm nothing is left behind — no stray process, no orphan file, nothing holding a resource.

Verification seven, optional and excellent: hand the documentation to another person and watch them try. Say nothing. Their first confused pause is the sentence you need to rewrite. [pause]

## Your project

Here is the handoff. The project guide asks you to turn the priority rule into a local intake command-line program.

The goal is that an operator can enter an incident on a Linux machine, get a priority back, and leave behind evidence you can inspect afterwards. The constraints: start from an empty directory, Python for the program and shell for the task wrapper, nothing secret committed or printed, malformed input fails loudly and exits nonzero, and the Python result agrees with your chapter two table on every row.

The artifacts you owe are the program, the shell task that runs it and propagates failure, a non-secret example configuration file, and a written note on the permissions you chose and the process and log evidence you inspected.

This is the first chapter whose output becomes input to the next one. Chapter four takes this working program and makes it reviewable — real history, a README another engineer can follow, and the first honest seam between a browser, a service, and data. So keep it. [pause]

## Recap

What to carry forward.

On a customer's machine, competence and trustworthiness are the same skill. For every file you create, know who can read it and why that is acceptable.

Run as a limited account. The scope of a mistake is determined by what the process was permitted to touch.

Configuration comes from outside your code. Secrets are delivered, never stored in your source, never printed, never logged.

Exit status is the foundation of automation. A script that ignores a failed step reports success while doing nothing, which is worse than failing.

Results to standard out, diagnostics to standard error. Shell for orchestration, a real language for logic.

Keep domain logic pure, put validation between the boundary and the logic, and collect all the input problems before reporting them.

Decide what you log. Evidence is deliberate, not a dump.

Diagnose by reducing possibilities in order — is it running, as whom, what does it say, what does it have open, can the user reach it — changing one thing at a time and writing it down.

And the clean-shell test is the only honest measure of whether your documentation works.

In chapter four we make all of this reviewable: commits that tell the truth, a README that survives a new machine, a pull request that names risk and rollback, and the full-stack seam that the rest of the course is built on.

That is chapter three. Go build the intake program.
