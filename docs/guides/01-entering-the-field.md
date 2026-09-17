# Chapter 1 project — Create the FieldOps Copilot delivery charter

**Format:** open-book test. Everything you need was in the chapter audio. There are no build steps here by design.
**Prerequisite:** listen to chapter 1 first. The guide assumes it.

---

## Goal

Produce a delivery charter for the first release of FieldOps Copilot that a customer sponsor, an operator, a security reviewer, and an engineer can all read and come away with the same understanding of what is being built, for whom, and how success will be judged.

## Starting state

An empty file. Nothing exists yet — no repository, no code, no architecture. This is the real starting state of a field engagement, and it is deliberate.

Pick one customer to serve for the whole course. It must be an operations, facilities, or internal technology team that handles repeated incident or request triage. A customer you have actually observed is better than an invented one. If you have none, use Harborline Logistics from the chapter: forty depots, a nine-person operations desk, incidents arriving by email, urgency decided by human judgment, nothing measured.

## Constraints

1. **One page.** If it does not fit, you have not decided yet.
2. **No implementation detail.** No services, frameworks, models, databases, queues, or cloud providers. Not one.
3. **Every factual claim is labelled** as observed or assumed. Unlabelled claims are treated as failures, not as minor omissions.
4. **Exactly one measurable outcome.** It must be something the customer could measure within a month, and would recognise as mattering. If today's value is unknown, say so.
5. **Non-goals are mandatory,** and each carries a reason based on risk, evidence, or sequence — not on your convenience.
6. **The AI system is a party,** not a feature. It appears in the responsibility matrix with at least one explicit prohibition.
7. **Deciding and doing are separated** for every party in the matrix.
8. **No accuracy-style metric** as the headline outcome. The chapter explained why.

## Required artifacts

| Artifact | What it must contain |
| --- | --- |
| Delivery charter (one page) | Current workflow as it really happens; the costly failure; the users and their conflicting needs; one measurable outcome; the release boundary as three lists — does, does not, still requires a human |
| Responsibility matrix | Every party who can make or block a decision — including the customer's operators, an administrator, you, the platform team, the security or governance approver, and the AI system — with what each decides, what each does, and where each escalates |
| Risk register | At least three risks, each paired with the specific evidence that would retire it |

Keep all three. Chapter 2 takes its inputs from this charter, and later chapters revise it rather than replace it.

## Self-grade rubric

Score each line yourself. Be strict: you are the only reviewer you have.

**Pass bar — all six must be true**

1. **Two-minute test.** You can explain the first release out loud without using a single implementation word.
2. **Four-audience test.** A sponsor, an operator, a security reviewer, and an engineer each find their own primary concern addressed somewhere in the page.
3. **Conflict is visible.** At least two stakeholders are documented as wanting incompatible things, and the charter does not pretend to resolve it by wishful wording.
4. **The outcome is falsifiable.** You can state how today's value would be computed, even if the answer is "nothing records it yet, and establishing the baseline is task one."
5. **Non-goals exist and bite.** At least one non-goal is something the customer will plausibly ask for, with a written reason.
6. **The AI row has a prohibition.** Not only a capability list — a clear statement of what the system may never do without human approval.

**Quality marks — aim for at least four**

7. Every claim about the customer is explicitly observed or assumed.
8. At least one party with a genuine veto is identified, and their path to yes is named.
9. Each of your three risks has evidence that could actually be gathered during a pilot, not a vague "monitor closely."
10. Deciding and doing are separated in at least three rows of the matrix, including yours.
11. You did not give yourself authority over a business or security risk you cannot accept.
12. The charter survives the deletion test: remove every sentence mentioning intelligence, automation, or models, and a real problem worth solving still remains on the page.

**Automatic fail**

- The charter describes what you will build rather than what problem it solves.
- Scope includes an integration, a mobile experience, or a second channel in the first release.
- The headline outcome is a satisfaction score, a usage count, or a model-accuracy figure.
- Nobody in the document is accountable when a recommendation turns out to be wrong.

## Stretch

Pick one if the core work came easily.

- Write the two-sentence version your sponsor would say to *their* leadership, and check that it contains no promise your charter does not support.
- Write the paragraph you would send to the security lead asking for the earliest possible conversation — including what you already know about the data involved.
- Identify the one sentence in your charter most likely to be contradicted in week six, and add the assumption label and validation method it needs.

## Verification you can run today

- Hand the charter to another person. Ask them to tell you what the first release does and who is accountable when a suggestion is wrong. Say nothing while they read. Whatever they get wrong is a defect in your document, not in their reading.
- Read your users section aloud and try to find the conflict. If there isn't one, you have written a sales page.
- Count the words on your page. If it runs past one page, cut a paragraph rather than shrinking the font.

---

<!-- tts:skip -->
## If stuck — inverted hints

These are deliberately last, and they are deliberately not in the audio. Read them one at a time, in order, and only after a genuine attempt. Each hint is a question, not an answer.

1. Cannot start? Write the single worst thing that happened to this customer in the last quarter because of this workflow. One paragraph, no solution. That paragraph is your charter's opening.
2. Charter reads like a build plan? Cross out every noun that is a piece of technology. If almost nothing survives, you wrote a design document. Start again from the workflow.
3. Cannot pick one outcome? Ask which number the sponsor would quote to *her* boss to justify continuing. If two numbers compete, ask which one gets worse when the costly failure happens.
4. Outcome has no baseline? Good — that is a real finding. Where would the raw material for the baseline exist today, even in an inconvenient form? Who would have to give you access to it?
5. Matrix feels decorative? For each row ask: what happens if this party is unavailable for a week? If nothing stops, the row is not real and the responsibility is hiding somewhere else.
6. Stuck on the AI row? Finish this sentence honestly: "The system may suggest ______, and a human must ______ before ______ happens."
7. Cannot find the conflict? Ask what the operator would remove from the first release and what the sponsor would add. They are rarely the same item.
8. Cannot find a veto holder? Ask who reviews any system that reads the text a customer's employee typed. If you do not know, that is your first meeting, not a gap in the exercise.
9. Risks feel generic? A risk that would apply to any software project is not a risk for *this* charter. Reread your own costly-failure paragraph and ask what would have to be true for it to happen again after you ship.
10. Still stuck on non-goals? List the three things you would most enjoy building. They are almost certainly non-goals for release one, and now you know why the section matters.
<!-- /tts:skip -->
