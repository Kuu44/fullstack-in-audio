# Chapter 4 project — Make FieldOps Copilot reviewable

**Format:** open-book test. No build steps. The chapter taught the standard; meeting it is your problem.
**Prerequisite:** chapter 4 audio, and the working intake program from chapter 3.

---

## Goal

A second engineer can clone your work, reproduce the current result on a machine you have never touched, and review the history without asking you a single question.

## Starting state

The chapter 3 intake program, the chapter 2 specification table, and the chapter 1 charter. If your work is already in a repository with a few vague commits, that is a realistic starting point — reshaping it is part of the test.

Imagine a specific reader: an engineer named Ana who takes over for three weeks, has never met your customer, and has no context beyond what is in the repository.

## Constraints

1. **Real history.** Commits made as the work happened, reshaped for clarity before publishing. A single squashed import fails. So does an invented history that describes work you did not do in that order.
2. **One logical change per commit.** Not one file, not one hour.
3. **Messages name behavior and motivation.** The diff shows *what*; your message must supply *why*.
4. **The README must work on a clean machine.** Not yours. One that has never run this project.
5. **Acceptance criteria before implementation.** The web intake issue is written before any interface exists, in observable terms, naming no technology.
6. **No secret anywhere in history.** Not just in the current state.
7. **Seam diagram names owners** for all four layers — browser, service, domain logic, data store — including the ones that do not exist yet.
8. **Documentation changes travel with the change** that invalidated them, in the same commit.

## Required artifacts

| Artifact | What it must contain |
| --- | --- |
| Repository with readable history | A commit sequence that tells the story of the work; every commit independently revertible |
| README | What this is and whose problem it solves; prerequisites with pinned versions; setup; how to run; what success looks like; common failures; where decisions are recorded |
| One issue with acceptance criteria | For the web intake experience: context, observable criteria a non-engineer could check, and an explicit out-of-scope list |
| One pull-request description | Behavior, risk, tests *including the gaps*, and rollback — with an honest statement of whether reverting is sufficient |
| Full-stack seam diagram | Four layers, and for each boundary: what crosses it, who is authoritative, what happens when the other side is unavailable |

## Self-grade rubric

**Pass bar — all seven must be true**

1. **Fresh-clone test passes.** A clone in a location you have never worked in, following only the README, produces a working program and a correct result.
2. **History reads as a story.** Top to bottom, a stranger can follow how the work developed.
3. **Single-revert test passes.** You can name a commit you could revert alone, without dragging unrelated changes with it.
4. **Motivation is recoverable.** For at least one non-obvious decision, the reason exists in the repository — commit message, decision record, or pull request.
5. **Criteria are checkable in thirty seconds** by someone who cannot read your code.
6. **Authority is decided at every seam.** You can state, without hesitating, who is authoritative for validity, for priority, and for what happened.
7. **No secret in any commit.** Verified across history, not just the working tree.

**Quality marks — aim for at least four**

8. Your pull-request description names a risk, and a test case you did *not* cover.
9. The rollback section says whether reverting is genuinely sufficient, and what else is needed if not.
10. The issue's out-of-scope list includes something the customer is likely to ask for.
11. The README's "what success looks like" is concrete enough that a reader knows whether it worked.
12. The seam diagram names an owner for a layer that does not exist yet, and you are honest where the owner is undecided.
13. At least one commit exists whose sole purpose is to record a decision or correct documentation, and it is not embarrassing.
14. You can point at where the customer's priority policy lives, and it is exactly one place.

**Automatic fail**

- The entire project arrives in one commit.
- The README works only because of something configured in your own environment.
- A credential appears anywhere in history, even if deleted in a later commit.
- Acceptance criteria were written after the work, or name a framework.
- Two layers are both authoritative for priority, or the browser is the only place validation happens.
- Commit messages are placeholders: "wip", "fixes", "updates".

## Stretch

- Reshape a genuinely messy branch into a publishable sequence, then write down — for yourself — what the original history would have cost Ana.
- Write the two-paragraph handover note you would send Ana on top of the repository, and then delete every sentence the repository already answers. What remains is the gap you should close in the repository itself.
- Add a decision record for the severity vocabulary, then check whether any of your four implementations disagrees with it.

## Verification you can run today

- Clone into a fresh directory on a fresh container. Follow only the README. Do not touch anything you remember.
- Read your commit list as a stranger and try to narrate the project's development out loud.
- Pick a commit and attempt the revert. Notice what comes along with it.
- Sweep the whole history for secrets.
- For each seam, say the three answers aloud. Hesitation marks your next bug.

---

<!-- tts:skip -->
## If stuck — inverted hints

Last on purpose, absent from the audio. One at a time, in order, after a real attempt.

1. History already a mess? You are allowed to reshape your own unpublished commits. What would the sequence be if you had known the destination when you started?
2. Cannot write a commit message? Finish this sentence: "Before this change, the system ______; after it, the system ______, because ______."
3. Unsure how small a commit should be? Ask whether you could revert it alone and have the project still make sense. If not, it is too big or too tangled.
4. README keeps working only for you? Do not debug it by reading. Run it somewhere hostile — a new container, a new user account — and let the failures write the missing lines.
5. Criteria feel vague? Put a person at the start of every criterion. If you cannot name who is observed doing what, it is not a criterion.
6. Cannot decide what is out of scope? List everything the customer has mentioned wanting. Everything not required by your one chapter-1 outcome is a candidate.
7. Pull request has no risk to name? Ask what a customer would notice first if this change were wrong, and how long it would take anyone to find out.
8. Rollback seems trivial? Ask whether the change touched data, configuration, or anything a person did by hand. Those are the reverts that are not reverts.
9. Seam diagram feels empty? For each boundary, try to break it: what if the other side is slow, down, or lying? Your answers are the diagram's real content.
10. Two places compute priority? Ask which one a customer's auditor would consider authoritative, then delete the authority of the other — not necessarily the code, but its right to decide.
<!-- /tts:skip -->
