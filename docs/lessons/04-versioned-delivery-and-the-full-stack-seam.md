<!-- tts:skip -->
## TTS notes — chapter 4

- Voice: `en-US-AndrewNeural`, rate `-14%` (about 146 words per minute).
- No commands or file paths are written in this script. Git operations are described in words.
- Recurring cast: Dana (sponsor), Sam (coordinator), Priya (security), Marcus (platform).
- New name this chapter: Ana, a second engineer who joins mid-pilot.
- `[pause]` becomes a beat of silence at segment turns.
- Nothing in this block is spoken.
<!-- /tts:skip -->

Welcome back to FullStack in Audio. This is chapter four: versioned delivery, and the full-stack seam. [pause]

You now have something that works. A priority rule in four languages, and a command-line program that an operator could genuinely use. It exists in a directory on your machine, and if your laptop died tonight, so would the pilot.

This chapter is about the difference between having built something and having delivered something. And I want to warn you about the trap in this chapter, because it is a specific one: everybody listening already knows how to use version control well enough to get by. You can commit, you can branch, you can open a pull request. So it is tempting to treat this as a chapter you have already passed.

The field version of this skill is different from the personal version, and the difference is the entire chapter. In a product team, your history is a convenience for your colleagues. In field delivery, your history is customer-facing evidence. It is how a customer's own engineers take over. It is how a security reviewer confirms what changed and when. It is how you answer the question "why is this configured this way", eighteen months after you left, when nobody remembers the meeting.

Let me give you the scene that makes this concrete.

Six weeks into the Harborline pilot, you get pulled onto something urgent at another customer, and a second engineer named Ana takes over for three weeks. Ana is good. Ana has never met Dana, Sam, Priya, or Marcus, and has no context whatsoever.

What Ana finds in your repository determines whether those three weeks are productive or wasted. If she finds four commits called "work in progress", a README that says "run the script", and no record of why the severity vocabulary has four values instead of five, she will spend a week reconstructing decisions you already made — and she will get one of them wrong, in a way that surfaces at the pilot review.

So the standard for this chapter is: could Ana be productive in a day? Everything else follows from that. [pause]

## What a commit actually is, and what a good one does

A commit is a snapshot of your project plus a message explaining it. That is the mechanical definition and it hides the important part: a commit is a unit of reasoning, and the history is a document you are writing whether you intend to or not.

A good commit has one job. It contains one logical change — not one file, and not one hour of work. If your change touches a program, a test, and a document because those three things constitute one coherent change of behavior, that is one commit. If you fixed a validation bug and also renamed a variable across the project because it was bothering you, that is two, and mixing them makes both harder to review and much harder to revert.

The message matters more in the field than anywhere else, and the reason is that the *what* is already visible. Anyone can see what changed. What no one can see is why. So the useful message names the behavior and the motivation: not "update validation", but "reject incidents with unknown severity instead of defaulting to low, because a blank severity silently de-prioritised a refrigeration alarm during the trial." That is a sentence that will still be useful in a year, to someone who was not there.

Here is the test I use. Read your message without looking at the code and ask: could someone predict what changed? And read the code without the message and ask: could someone guess why? If the answer to either is no, the commit is doing half its job.

Now, the practical objection. Real work is messy. You explore, you backtrack, you leave a mess. Nobody writes a clean history in real time, and pretending otherwise produces a different bad habit: engineers who stop committing frequently because each commit feels like it has to be a publication.

The resolution is to separate working commits from delivered history. Commit constantly while you work — it is your safety net, and a small commit is free. Then, before you ask anyone to review, reshape that mess into a sequence that tells the truth about the change. Reordering, combining, and rewriting your own unpublished commits is a normal and healthy part of the craft, not cheating.

Two boundaries on that. Reshape your own unpublished work, freely. Do not rewrite history that others have already built on, because you will break their copies and your name will be attached to the confusion. And do not use reshaping to hide something a reviewer needs to know — if you tried an approach and abandoned it for a real reason, that reason belongs in the record somewhere, whether in a commit message, the pull request, or a decision record. [pause]

## Branches, reviews, and issues as a delivery system

Let me talk about the workflow around commits, in field terms rather than in general terms.

A branch is a line of work that is not yet part of the main story. In a field pilot, keep branches short-lived. This is not dogma; it is risk management. A long-running branch in a fast-moving pilot accumulates conflicts with a system whose requirements are changing weekly, and it hides work from the customer until a large, unreviewable moment. A pilot is exactly the environment where small, frequent, integrated changes are worth the most.

Code review in the field has a wrinkle worth naming. Sometimes you are the only engineer on the engagement. There is nobody to review your work, and the temptation is to skip the ritual as theatre.

Do not skip it. Change what it is for. When you write a pull request description with no reviewer, you are writing to three real audiences: yourself in six weeks, Ana when she takes over, and the customer's engineer during handoff. The act of articulating what changed, what could break, and how to undo it catches real defects — I have caught my own bugs while writing the rollback section more than once, because that section forces you to think about the state the system will be in.

And if the customer has engineers, get them into review as early as they will tolerate. It is the cheapest form of knowledge transfer that exists. A customer engineer who has reviewed forty of your changes does not need a handoff workshop; they already own the system. This is also, incidentally, how you avoid being the permanent dependency that chapter one warned you about.

Now issues. An issue is a decision that has not been made yet, or work that has not been done yet, with enough context to be picked up by someone else.

The field-specific discipline is acceptance criteria. Write them before the work, in observable terms, and ideally in language the customer's stakeholder would recognize. For the web intake experience you will build in chapter seven, criteria might be: an operator can submit an incident without using a mouse; every field has a visible label; required-field errors say what to do; a submission that fails validation does not clear the form. Notice that none of those name a technology, and all of them can be checked by a person in thirty seconds.

Why write them first? Because acceptance criteria written after the work is done are a description of what you built, which is a tautology. Written before, they are a contract you can fail — and therefore a contract that can protect you when the ask quietly grows. When Dana asks midway whether the form can also handle photo attachments, the criteria are what let you say "that is a separate issue, and here is what it would displace" rather than absorbing it invisibly.

One more thing about issue linkage, which sounds bureaucratic and pays off enormously. Connect the change to the issue, and the issue to the customer's need. Then, a year later, the chain is intact: this line of code exists because of this decision, which exists because of this customer requirement. That chain is what makes a system maintainable by strangers, and it is what auditors and security reviewers ask for. [pause]

### Writing the intake issue out loud

Let me draft one with you, because acceptance criteria are harder to write well than they look.

The issue is for the first web intake experience — the thing chapter seven builds. A weak version of this issue says: "Build a web form for incident intake." That sentence contains no criteria, no constraints, and nothing that can fail.

Here is a stronger version, spoken as I would write it.

Title: operators can report an incident from a browser without leaving their keyboard.

Context, two sentences: today supervisors email the operations desk and coordinators retype the report, which is where duplication and delay enter. A browser form removes the retyping step for the depots that have a screen available; phone reports remain out of scope for release one.

Then the criteria, and each one begins with a subject who can be observed doing something. An operator can complete and submit a report using only the keyboard. Every input has a visible label, not a placeholder standing in for one. When a required field is missing, the page states which field and what an acceptable value looks like, and the operator's other typing is preserved. When the submission cannot be delivered, the operator is told it was not received — no confirmation is shown. A submitted report displays the priority and the reasons that produced it.

Then what is explicitly not in scope: attachments, photographs, voice, editing after submission, and any automatic assignment of work.

Now notice three things about that issue.

It names no technology. No framework, no styling approach, no validation library. That is not squeamishness — it is because the criteria must survive the technology decision, and chapter seven has not made it yet.

Every criterion can be checked by a human in under a minute, with no special tooling and no access to your code. Dana could check them. Sam could check them, and Sam would be the better reviewer.

And the out-of-scope list is doing real work. When someone asks for photo attachments in week five — and they will, because a photograph of a leaking unit is genuinely useful — the issue is where the conversation starts, with a visible reason rather than an argument about what was agreed.

One more technique that costs nothing. Write the criteria as the sentences you would want a customer to read back to you in the pilot review. If a criterion would embarrass you when read aloud in that room — because it is vague, or because it is really a description of your implementation — rewrite it now. [pause]

## The pull request description as a professional artifact

Let me be specific about the four things a pull request description should contain in field delivery, because there is a pattern that consistently works.

Behavior. What is different after this change, described from the outside. Not "refactored the validator" — "an incident with an unknown severity is now rejected with a message naming the acceptable values, instead of being accepted as low priority."

Risk. What could this break, and who would notice. This is the section engineers skip and reviewers need most. If you cannot name a risk, either the change is trivially safe — say so, explicitly — or you have not thought hard enough about it.

Tests. What evidence exists that this works. Not "tested locally", which means nothing. Which cases you ran, and importantly, which cases you did *not* cover. Naming your coverage gap is a mark of seniority, not a confession of weakness.

Rollback. How to undo this. For a code change, reverting may be genuinely sufficient — but say so. And if reverting is not sufficient, because the change touched data, configuration, or something a person did by hand, that needs writing down before it is needed. The worst time to design a rollback is during the incident that requires it.

If you write those four sections honestly for every change of consequence, you will be a better engineer in six months, independent of any other skill in this course. It is the cheapest discipline with the highest return in the whole of delivery work. [pause]

## Version control realities specific to customer environments

A few things that nobody tells you until you hit them.

First, whose repository is it? This is a real question with legal consequences. Sometimes you build in your own organization's repository and deliver artifacts. Sometimes you build directly in the customer's repository, under their policies and their review requirements. Sometimes both, with a boundary between reusable product code and customer-specific configuration — which is exactly the architecture we design in chapter six. Find out early, because "we will sort out the repository later" tends to mean "we will have an awkward conversation about intellectual property during handoff."

Second, secrets in history. If a credential is ever committed, it is in the history, and deleting it in a later commit does not remove it. The only correct response is to treat it as disclosed: rotate the credential first, and then clean up. This is why we spent time on the secret discipline in chapter three. Prevention here is not an ideal; it is the only cheap option.

Third, the customer's own review requirements. Some enterprises require a second approver on every change, require specific commit trailers, or forbid direct changes to main. Learn these in week one, not in week five when you are trying to ship a fix. The rules are rarely negotiable and knowing them makes you look like someone who has done this before.

Fourth, and this one is strategic: the customer-specific fork is a trap that looks like a solution. When a customer needs behavior the core product does not have, the fastest path is a branch that never merges back. It works, it ships, and then it becomes a permanent tax — every product improvement must be reapplied, every security fix is a merge conflict, and nobody remembers which differences were deliberate. When you feel that pull, the correct response is to make the variation a configuration boundary, and to write down the decision. That is the whole subject of chapter six, and this chapter is where you first notice the pressure. [pause]

## The full-stack seam

Now the second half of the chapter, and the thing that makes this course a full-stack course rather than a collection of topics.

"Full stack" gets used as a résumé word meaning "knows several technologies." That is not what makes a system full stack. A system is full stack when you understand and own the seams between its layers: what crosses each boundary, who is authoritative for what, and what happens when one side is unavailable.

For FieldOps Copilot there are four layers in the first release, and you have already met three of them.

The browser, which you will build in chapter seven — where a human expresses intent and receives feedback.

The service, which you will build in chapter eleven — where the customer's policy is enforced and decisions are made.

The domain logic — your priority rule — which is where the policy actually lives.

And the data store, which arrives in chapter thirteen — where truth persists.

The seam is not the technology at each layer. The seam is the set of promises between them. And there are exactly three questions you have to answer at every boundary.

What crosses it? Name the information, in domain language. From browser to service: an incident report. From service to browser: an incident with its priority, band, reasons, and identity. That is a contract even before it has a format.

Who is authoritative? This is the question that prevents the most expensive class of bug. For FieldOps: the service is authoritative for validity and priority. The browser may validate for speed of feedback, and the browser's opinion does not count. The data store is authoritative for what happened. The browser's copy is a cache of a moment in time.

Say that out loud, because it has consequences: if the browser computed the priority, you would have two implementations of your customer's policy, drifting apart, one of them running on a machine you do not control. Any operator could open the tools built into their browser and change the score. Business policy enforced in the browser is a suggestion, not a rule.

What happens when the other side is unavailable? The browser must behave sensibly when the service is down. The service must behave sensibly when the store is down. Sensibly means: say what happened, do not lose the operator's typing, and do not pretend to have succeeded. That last one is the failure that destroys trust. A form that shows a confirmation when the submission never arrived is worse than an error message, because Sam will walk away believing the refrigeration alarm is in the system.

Let me add the fourth question, which is where seams get interesting once intelligence enters the picture. Where is the boundary of authority for a suggestion? In chapter fifteen you will add a model. It will produce a recommendation that crosses a seam into the service, and the service must treat it as an *input*, not as a decision — validated like any other untrusted input. Getting that right at the seam level is what makes the chapter one promise — this system proposes and a human disposes — true in the architecture rather than merely in the document.

Your project asks you to draw this. Not elaborately: four boxes and the three promises at each boundary. And an owner for each layer, including the ones that do not exist yet — because when Marcus asks who supports the browser layer in production, "I hadn't thought about it" is a bad answer and it is the honest answer for most engineers at this point in a project. [pause]

### Ana's first day

Let me run the handover twice, so you can hear the difference your history makes. Same code, same working program, two different repositories.

In the first version, Ana clones the project and finds three commits: "initial", "fixes", and "wip". The README says the project is an incident triage tool and tells her to run the program. She runs it. It fails, because there is a dependency she does not have, and the version she guesses at behaves differently. An hour gone.

She gets it running and reads the code. The validation rejects a severity of "urgent", and she has no idea whether that is deliberate. She looks for a decision record and finds none. She asks the customer's coordinator, who says "oh, we say urgent sometimes" — so Ana, reasonably, adds "urgent" as an accepted synonym mapping to high. She has just silently changed the customer's policy, in a system where the same policy exists in four other implementations, and the specification table you wrote in chapter two no longer matches the program. Nobody will notice until a report at the pilot review shows two different priorities for the same incident.

By day three she has a working environment, a wrong model of the system, and one quiet defect she introduced while being conscientious.

Now the second version. Ana clones the project and finds a dozen commits whose messages read in order: the pure rule, the specification table, the intake boundary, validation that rejects unknown severities with the reason it was introduced, the run procedure. The README names the customer problem in three sentences, points at the charter, lists prerequisites with pinned versions, and tells her what a successful run looks like. She is running it in ten minutes.

She hits the same "urgent" question, and this time the commit message tells her that blank and unrecognised severities are rejected deliberately, because a silent default de-prioritised a refrigeration alarm during the trial. So Ana does the right thing: she does not change the rule. She opens an issue proposing that "urgent" be mapped to high, notes that the change would need to be applied to the specification table and all four implementations, and asks the sponsor whether the operators' vocabulary should be widened.

Same conscientious engineer. One repository turned her into a liability and the other turned her into a contributor, and the difference cost you nothing at the time except attention to your commit messages.

That is the argument for this chapter, and it is not really about Git. It is about whether the system you are building can be understood by someone who was not present when it was decided. In the field, that person always arrives — sometimes it is a colleague, sometimes it is the customer's own engineer, and sometimes, most humblingly, it is you in eight months with no memory of any of this. [pause]

## What makes a README a deliverable rather than a courtesy

Your README has one job: a competent engineer who has never seen this project can reproduce the current result on a machine you have never touched.

That is it. Not a feature tour, not a marketing page. A reproduction procedure.

For this stage of FieldOps Copilot, it needs to say what this project is and whose problem it solves, in about three sentences — Ana needs the context, and a link to the charter is not enough, because she needs to know it exists. Then what must be installed. Then how to set up an isolated environment and run the program. Then what a successful run looks like, concretely, so the reader knows whether it worked. Then what the common failures mean. And then where the decisions are recorded, so someone can find out why before they change something.

Two failure modes. The README that assumes your machine — it works because of something in your environment that you have forgotten you configured. The clean-machine test is the only cure, and it is the same test as chapter three's clean-shell test, one level harder.

And the README that drifts, which is worse because it actively misleads. The only durable defense is to update it in the same commit as the change that invalidated it. Documentation updated "later" is documentation updated never. [pause]

## The failure modes

The first failure is the one giant commit. Everything you built in three chapters, committed as "initial implementation." The individual pieces are fine and the history is now worthless: nothing can be reverted independently, no decision is attributable, and Ana cannot see the order in which understanding developed.

The second failure is history that lies. Commit messages written to look tidy that describe something other than what happened, or an abandoned approach quietly erased along with the reason it failed. The next person repeats the experiment.

The third failure is the invisible decision. The severity vocabulary has four values and nobody wrote down why, so in week nine somebody adds a fifth in a form dropdown, and now the rule produces a default priority for a severity it does not recognize. Decisions that are not recorded get re-decided badly.

The fourth failure is the README that only works for you.

The fifth failure is the leaked credential. Committed, then deleted in a later commit, and treated as resolved. It is still in the history. Rotate first.

The sixth failure is the unreviewable pull request. Four hundred changed files spanning three unrelated concerns, opened on a Friday. Nobody will review that properly, including you, and the review you get will be about formatting because that is all a human can do with it.

The seventh failure is seam confusion, and it is the expensive one. Priority computed in the browser as well as in the service. Validation only in the browser. A confirmation shown before the write succeeded. Each of these is a boundary where authority was never decided, and each one produces a bug that looks like intermittent weirdness rather than a design error, which means it gets patched instead of fixed.

And the eighth, which is a habit rather than an event: treating documentation as separate from work. The engineer who finishes the feature and plans to document it "after the pilot" is describing a system that will require them personally, forever. [pause]

## How you verify this chapter's work

Verification one: the fresh-clone test. Clone your repository into a location you have never worked in, on a machine or container that has never run it, and follow only the README. Everything that fails is a defect. Not an inconvenience — a defect, with the same status as broken code.

Verification two: the history read-through. Read your commit list top to bottom as if you were Ana. Does it tell a story: the rule, then the program, then the validation, then the documentation? Can you point at the commit that introduced the severity decision? If the history reads as noise, reshape it before you publish.

Verification three: the single-revert test. Pick one commit and ask whether you could revert exactly it without dragging along unrelated changes. If not, your commits are not units of reasoning.

Verification four: the secret sweep across history, not just the current state. Every file, every commit.

Verification five: the acceptance criteria test. Read the issue you wrote for the web intake experience and ask whether a person could definitively pass or fail it in thirty seconds, without your help. If the criteria need interpretation, they are not criteria.

Verification six: the seam interrogation. For each of your three boundaries, answer out loud: what crosses it, who is authoritative, what happens when the other side is down. Any hesitation marks the boundary that will produce your next bug.

Verification seven: the rollback statement. For your most recent change, say how you would undo it, and whether undoing it is genuinely sufficient. If the answer involves data or a manual step, that is the sentence that belonged in the pull request. [pause]

## Your project

Here is the handoff. The project guide asks you to make FieldOps Copilot reviewable.

The goal is that a second engineer can clone your work, reproduce the current result, and review the history without asking you a single question. The constraints: real history made as the work happened — no single squashed import and no invented commits; a README sufficient to run the program on a clean machine; acceptance criteria written before any interface exists; and a seam diagram that names an owner for every boundary, including the ones that do not exist yet.

The artifacts are the repository with a readable history, the README, one issue with acceptance criteria, one pull request description naming behavior, risks, tests, and rollback, and the full-stack seam diagram.

If you already have the program from chapter three in a repository with three vague commits, that is a realistic starting state. Reshape it into a history that tells the truth, and write down in your own notes why the original was not good enough. [pause]

## Recap

What to carry forward.

In field delivery your history is customer-facing evidence, not a personal convenience. The standard is whether a second engineer could be productive in a day.

A commit is a unit of reasoning. One logical change, with a message that names the behavior and the motivation, because the what is visible and the why is not.

Commit messily while you work, reshape before you publish, never rewrite what others have built on, and never use reshaping to hide something a reviewer needs.

A pull request description is worth writing even with no reviewer: behavior, risk, tests including the gaps, and rollback. Writing the rollback section catches real bugs.

Acceptance criteria go before the work, in observable terms, in language the customer would recognize. They are what let you decline a quiet scope increase.

Find out early whose repository it is, what the customer's review rules are, and resist the customer-specific fork — make the variation configuration instead.

A system is full stack when you own the seams. At every boundary: what crosses it, who is authoritative, and what happens when the other side is unavailable. Business policy enforced in the browser is a suggestion.

And a README is a reproduction procedure, verified by cloning somewhere you have never worked.

In chapter five we take this seam and put load through it. Data structures, complexity, and a system design for the intake-to-triage path — with capacity numbers you state out loud and a failure mode named at every boundary. Bring your seam diagram; chapter five's project extends it directly.

That is chapter four. Go make it reviewable.
