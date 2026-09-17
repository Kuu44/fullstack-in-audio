# Chapter 6 project — Define the FieldOps Copilot architecture

**Format:** open-book test. Mostly design, with exactly one piece of code as evidence. No reference architecture is provided.
**Prerequisite:** chapter 6 audio, the chapter 5 design and batch-run findings, and the chapter 4 seam diagram.

---

## Goal

An architecture that separates the reusable FieldOps core from one customer's adaptation, so the second customer does not require a fork of the first — and one working interface boundary that proves the dependency arrow points the way you claim.

## Starting state

Everything from chapters 1 through 5: the charter, the specification table and four rule implementations, the intake program, the repository, the seam diagram, the intake-to-triage design, and the list of things that broke in your batch run.

Assume a second customer is arriving in six weeks with a different vocabulary, different weights, a different organizational structure, and a different notification vendor.

## Constraints

1. **Components, boundaries, and dependency direction only.** No framework selection, no ORM choice, no premature implementation — except the single interface boundary named below.
2. **The domain depends on nothing.** Your triage policy may not depend on a database, a web framework, a notification client, or a model provider.
3. **Customer-specific behavior is reachable by configuration or an adapter.** Editing core logic to serve one customer is a failure.
4. **No conditional keyed on a customer's name** anywhere in the design.
5. **Contracts in plain prose,** readable by a customer engineer, and testable with no real notification provider present.
6. **Lowest rung that works.** If a difference can be a value, it must be a value. Speculative extension points for variations you have not seen are a failure.
7. **Draw reality, not intention.** Where the current code violates your intended arrow direction, draw the real arrow and mark the intended change.

## Required artifacts

| Artifact | What it must contain |
| --- | --- |
| Component diagram (two levels) | The system in its environment (people and external systems), and the components inside it with arrow directions. Shaded into reusable core, customer configuration, and customer-specific adapter |
| Two interface contracts | Intake→triage and triage→notification, in prose: what crosses, what the receiver promises, what happens when the promise fails, who is authoritative, and whether the boundary is synchronous |
| Routing ADR | Business-unit (or equivalent) routing: context, decision, consequences, rejected alternatives. Must state what is data, what is core concept, and who can change the data |
| One exercised interface boundary | Working code: a port defined by your domain, a fake adapter behind it, and a test of the path through it with no real provider present |
| Second-customer classification | Six or more differences your imagined second customer brings, each classified as value, policy data, adapter, extension point, core capability, or escalation to a human decision |

## Self-grade rubric

**Pass bar — all seven must be true**

1. **The three groups are visible** on the diagram: reusable core, customer configuration, customer-specific adapter.
2. **Configuration is distinct from source code,** and you can name who at the customer can change it and whether a deployment is required.
3. **The no-provider test passes.** You can exercise intake → triage → routing → notification request with a fake adapter and no real provider.
4. **Dependency direction holds.** You can name everything your triage policy depends on, and the list contains no infrastructure.
5. **The reversal test passes.** If the second customer wanted the opposite routing rule, your design expresses it without new core code — or you can explain precisely why it is a genuine core capability change.
6. **Both contracts state the failure behavior** and who is authoritative, not just the payload.
7. **The ADR names a rejected alternative** and the specific reason it lost.

**Quality marks — aim for at least five**

8. Your second-customer classification includes at least one item you deliberately deferred rather than designing for, with the reason.
9. It also includes at least one item that is *not* an architecture question — a request that should go back to the sponsor or security reviewer.
10. For each bounded context you can say what "incident" means inside it, and the meanings differ.
11. No port's vocabulary is borrowed from a vendor's API.
12. Every configuration setting has a default that is correct for a typical customer.
13. Onboarding a new site or depot is a data change an administrator can make.
14. Your diagram stops at two levels and is still useful.
15. At least one finding from your chapter 5 batch run is visibly addressed by a boundary in this architecture.

**Automatic fail**

- A component named after a customer, or a conditional keyed on a customer's name.
- The severity vocabulary or priority weights are embedded in core source code.
- The triage policy imports a database, web framework, or provider client.
- Interface contracts describe only the payload.
- A general rules engine, plugin system, or dynamic schema built for a single customer.
- The diagram shows the architecture you intend rather than the one you have, without marking the difference.
- No code at all: the interface boundary was described but not exercised.

## Stretch

- Write the one-page answer to your own product organization's question: "how much of what you built here ships to everyone?" Use the shaded diagram as the evidence.
- Take the customer difference you were most tempted to fork for, and design the smallest boundary that avoids the fork. Then estimate what the fork would have cost over a year.
- Write the expiry conditions for a deliberate fork: if you ever did take that path, what date, what owner, what triggers its removal?

## Verification you can run today

- Second-customer test: classify every difference. Any core change needs a written justification as a genuine new capability.
- No-provider test: run the path with the fake adapter.
- Dependency check: list what the policy depends on, out loud.
- Vocabulary check: define "incident" inside each context.
- Administrator test: can the customer change routing data without an engineer?
- Ana test: hand the diagram to someone unfamiliar and ask which parts are reusable and where a customer-specific behavior would go.

---

<!-- tts:skip -->
## If stuck — inverted hints

Last on purpose, absent from the audio. One at a time, in order, after a real attempt.

1. Cannot find the boundaries? List the nouns your system deals with, then group them by which ones change together. Things that change together belong together.
2. Unsure whether something is core or customer-specific? Ask whether the *second* customer would want the concept, even with different values. Concept shared, values differ, equals core plus configuration.
3. Arrow direction confusing? Ask what you would have to start up in order to test your priority policy. Anything on that list is something your policy depends on.
4. Port keeps looking like the vendor's API? Write the port's method names using only words from your charter. If a word came from vendor documentation, it does not belong.
5. Cannot decide the customization rung? Try the cheapest rung first and see what breaks. Discovering that a value is insufficient takes ten minutes; undoing a plugin system takes a week.
6. Tempted by a general rules engine? Count your customers. Count the distinct rule shapes you have actually seen. If either number is one, you are designing from imagination.
7. Contract feels thin? Ask what the receiver is promising, and then ask what happens on the day it cannot keep that promise. The second answer is the half people omit.
8. Unsure if a boundary is real? Try to reach across it accidentally in code. If you can, it is decoration.
9. Diagram feels useless? Ask which question each level answers, and for whom. A level that serves nobody should be deleted.
10. Second-customer exercise feels fake? Use a real company you know of in a different industry. Their organizational structure will be genuinely different from your first customer's, which is the whole point of the test.
<!-- /tts:skip -->
