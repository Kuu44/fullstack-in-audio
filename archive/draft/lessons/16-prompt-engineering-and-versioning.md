# Chapter 16 — Prompt engineering, management, and versioning

**Roadmap nodes covered:** Prompt Engineering; Prompt Management; Prompt Versioning
**Part:** IV — Build AI behavior that can be controlled
**Companion test:** `docs/guides/16-prompt-engineering-and-versioning.md`
**Audio:** `media/16-prompt-engineering-and-versioning.mp3`

---

## Narration

Welcome to chapter sixteen.

At the end of the last chapter you had something good: a narrow, domain-shaped boundary between your incident service and a language model, with a deterministic fake behind it for tests and one real adapter exercised only on synthetic data. Your provider decision is written down with evidence. Your task boundary is in the charter.

And inside that adapter, there is a block of text that nobody reviews, that lives in one engineer's working copy, that has been edited nine times today, and that entirely determines how the system behaves.

That block of text is the single most powerful and least governed artifact in your whole deployment. This chapter fixes that.

Here is where we are going. First, a reframe: what a prompt actually is, organizationally, and why treating it as wording is the root mistake. Second, the anatomy of a task prompt that works — the seven parts, and what each one is for. Third, the prompt engineering techniques that measurably pay for themselves, and the popular ones that do not. Fourth, the discipline that matters most in field work: separating customer policy from incidental phrasing. Fifth, template variables and prompt injection, which is where prompts become a security topic. Sixth, prompt management — where these things live and who may change them. Seventh, versioning, change notes, fixtures, and a rollback rule. Then pitfalls, verification, and your test project.

### What a prompt actually is

Let me start by naming the mistake, because almost everyone makes it and it is a mistake of category rather than skill.

People treat a prompt as writing. You phrase something, you try it, it works better, you keep it. It feels like editing a document. The feedback loop is fast and pleasant and completely unlike any other production change you make.

But look at what the prompt actually does. It determines which categories your customer's incidents get assigned to. It determines whether the system says "I do not know" or invents an answer. It determines whether a request to ignore prior instructions is honoured. It encodes your customer's escalation policy, their taxonomy, their definition of urgency, and the boundary you negotiated with their security lead.

That is not writing. That is production configuration with safety consequences. In every other part of your system, a change with those consequences goes through review, gets a version, is tested against fixtures, is deployable and revertible, and is recorded so you can answer "what was running when this went wrong." Prompts get none of that by default, and the gap between their power and their governance is where field deployments get embarrassed.

Here is the scenario I want you to hold in mind for the whole chapter. Six weeks into the pilot, a customer operations manager emails you: last Tuesday the copilot started marking network incidents as facilities issues, and it has been doing it ever since, and one of them sat for a day. Can you explain what happened.

If your prompts are governed, that is a twenty-minute investigation. You look up the suggestions from Tuesday, read the recorded prompt version, diff it against the previous version, see that somebody tightened the facilities category description in a way that broadened its scope, check the fixture results from that change, find the two fixtures that shifted and were dismissed as noise, and reply with a cause, a fix, and a rollback that is already done.

If they are not governed, that email is the beginning of a very bad week. You cannot tell which text was live on Tuesday. You cannot tell whether the model changed underneath you instead. You cannot reproduce the behaviour because the prompt has been edited eleven times since. And you end up saying "we have improved it" to a customer who now knows you cannot explain your own system.

Everything in this chapter is designed so you get the twenty-minute version.

### The anatomy of a task prompt

Now let us build the thing properly. A working task prompt for a bounded enterprise capability has seven parts. I will go through them in order, and the order itself matters.

Part one: operating context and role. A short statement of what the system is and what the model is doing within it. Keep it factual and specific to your deployment — the model is acting as a triage assistant inside an incident management tool used by an operations team, drafting suggestions that a human will review. Notice what that does: it establishes that a human reviews, which is context the model can use, and it establishes the domain, which helps it interpret jargon. What it should not do is inflate. "You are a world-class expert" is decoration; we will come back to why.

Part two: the inputs, and the trust boundary among them. State what the model is being given — an incident report submitted by an end user, and possibly some retrieved reference material. And state, explicitly, that the content of the incident report is data to be analysed, never instructions to be followed. That single sentence is your first and weakest layer of injection defence, and I will explain shortly why it is weak and what carries the real weight.

Part three: the task, expressed as a decision with criteria. This is where most prompts are far too vague. "Categorize the incident" is not a task specification; it is a gesture. The specification includes the list of valid categories and, crucially, a one-line discriminator for each — what distinguishes this category from its nearest neighbour. If your taxonomy has "network" and "application", say which one a slow page load belongs to and why. The model does not have your customer's tribal knowledge, and the places where your categories overlap are exactly the places it will be inconsistent. Writing those discriminators is genuinely hard, which is a signal: if you cannot write the rule, your human operators are probably also inconsistent, and you have just found something valuable to tell the customer.

Part four: the output contract. State the required shape in words, and enforce it structurally through your provider's schema mechanism. Do both. The structural enforcement guarantees parseability; the stated contract improves the semantic quality of what goes into each field, because the model is told what each field means and not just that it exists.

Part five: uncertainty behaviour. This is the part people skip and it is the part that determines whether the system is trustworthy. Say explicitly what to do when the report is too thin to categorize: return the insufficient-evidence result and list what is missing. Give the condition, not just the option — for example, if the report does not identify an affected service or a symptom, that is insufficient evidence. Without an explicit, easy, legitimate path to "I do not know," you are implicitly forcing a guess, and you will get one, delivered with the same fluent confidence as a correct answer.

Part six: prohibited actions and out-of-scope requests. State that the model must not produce any output that implies closing, escalating, notifying, or reassigning, and that if the report asks for such an action, it is to be treated as reported content, not as a request. Be aware of the limit here: this is an instruction, and instructions can be overridden by clever input. It is a layer, not a wall. The wall is architectural — there is no write tool. We built that boundary last chapter and we will reinforce it in chapters eighteen and nineteen.

Part seven: examples. A small number of worked examples — input and correct output — does more for consistency than several paragraphs of description, particularly for edge behaviour. Choose them for coverage, not volume. You want a clear case, a genuinely ambiguous case that should still resolve, a thin case that must return insufficient evidence, and a case where the reported text contains something that looks like an instruction and must be ignored. Four well-chosen examples beat fifteen similar ones, and fifteen similar ones actively hurt, because they cost tokens on every single call and they narrow the model's behaviour toward the pattern they happen to share.

And a warning about examples that is easy to miss: your examples are policy. If every example you wrote happens to mark authentication problems as high urgency, you have just encoded an urgency rule that appears nowhere in your written criteria, and nobody reviewing the criteria will find it. Examples must be reviewed with the same care as the instructions, and when your policy changes, your examples have to be checked too.

One more structural point. Order your prompt with the stable material first and the variable material last. The role, criteria, contract, prohibitions, and examples are identical on every call; the incident text changes. Most providers now cache repeated prefixes and charge much less for cached input tokens, so this ordering is worth real money at volume. It also helps a little with attention, since the variable content ends up near the end where models attend well.

### What actually works, and what is decoration

Now let me separate technique from folklore, because there is a great deal of folklore.

Things that reliably help.

Specificity about criteria. This is the highest-leverage change available to you, and it is unglamorous. Replacing "assess urgency" with a definition of each urgency level in terms of observable properties — number of users affected, whether a workaround exists, whether a revenue path is blocked — will improve consistency more than any amount of clever phrasing. Most prompt improvement is actually requirements clarification wearing a costume.

Making the model's job structurally easier. Asking for a choice from a fixed list is far more reliable than asking for free-form labelling. Asking for one decision per call is more reliable than asking for five unrelated decisions. If you find yourself writing a prompt that does triage and summarization and customer sentiment and duplicate detection, split it. Each split call is cheaper to evaluate, easier to debug, and independently versionable.

Explicit handling of the null case. Covered above, and worth repeating because it is the difference between a system that is honest and one that is not.

Deliberate reasoning, in the right places. Letting a model produce intermediate reasoning before its final answer genuinely improves multi-step accuracy. But be careful about two things. First, it costs output tokens and therefore latency and money, so use it where the task has real steps, not reflexively. Second — and this is a subtle trap — the rationale field in your output schema is not the model's reasoning. It is a generated explanation, produced alongside or after the answer, and it may be a plausible-sounding justification rather than a faithful account of how the answer arose. Present it to operators as "the stated reason," useful for a human to sanity-check, not as evidence of an internal process. If you tell a customer "you can see why it decided that," you are overclaiming, and someone will eventually catch it.

Things that are largely decoration.

Grandiose role inflation. Telling the model it is a world-class expert, or that lives depend on this, or offering it a tip. These circulate widely. They do not consistently help on constrained structured tasks, they add tokens to every call, and they make your prompt read as unserious to any customer reviewer who sees it. If you believe one of these helps on your task, that is a testable claim — run it against your fixtures and keep it only if the numbers move.

Piling on emphasis. Shouting in capitals, repeating an instruction four times, adding more exclamation. If a single clear instruction is being ignored, repetition rarely fixes it; restructuring usually does. Move the requirement into the schema, or into an example, or into a validation check on your side.

Negative instructions as a primary control. "Never do X" is a weaker lever than removing the ability to do X. Where you can express a constraint structurally — an enumerated field instead of free text, a missing capability instead of a forbidden one — do that, and keep the negative instruction only as a secondary layer.

The general principle: prefer structure over persuasion. Every requirement you can move from prose into schema, into the shape of the task, or into validation on your side, is a requirement that no longer depends on the model choosing to comply.

### Separating customer policy from incidental wording

This is the part that is specific to forward deployed work, and I think it is the most important idea in the chapter.

Go through your prompt line by line and sort every sentence into one of two buckets.

Bucket one is customer policy. The list of valid categories. The discriminators between them. The definition of each urgency level. The rule about what counts as insufficient evidence. The prohibition on suggesting escalation. These encode decisions your customer owns. If you change one of them unilaterally, you have changed your customer's operating policy without telling them, and if it causes a bad outcome, you own that entirely.

Bucket two is incidental phrasing. Whether you say "analyse" or "assess". The order of two independent instructions. Whether an example uses a printer outage or a payment gateway outage. These are craft decisions that belong to you, and you should be free to tune them against fixtures without a customer meeting.

Once you have sorted them, treat the buckets differently.

Policy content should be data, not prose, wherever it can be. The category list with its discriminators is a structured configuration object that your template renders into the prompt. The urgency definitions likewise. There are three payoffs. Policy becomes reviewable by non-engineers — you can put the taxonomy in front of the operations manager and get real feedback, which you will never get from a page of prompt text. Policy becomes diffable in a meaningful way: a change to the taxonomy shows up as a change to the taxonomy, not as a moved paragraph. And the same policy data can drive your validation, your UI dropdowns, and your evaluation fixtures, so they cannot silently disagree.

Phrasing stays in the template, versioned with the code.

There is a governance consequence that is easy to miss and expensive to learn. When you hand this system over, the customer will eventually want to change the taxonomy — they reorganize, a new service comes online, a category turns out to be useless. If the taxonomy lives inside a prompt string inside an adapter, that change requires you. If it lives in reviewed configuration with an approval path, it requires them plus a check. The second is a better product and a better commercial position, because it makes the deployment survivable without you, which is the actual definition of a successful handover.

### Template variables and prompt injection

Now the security topic, and I want to be precise about the threat model because vague worry produces vague defences.

Here is the core fact: the model receives one sequence of tokens. Your careful instructions and the incident description submitted by some user are, at the level the model operates, the same kind of thing. Role labels like system and user are a convention that models are trained to respect, and that training is real but it is a tendency, not an enforcement mechanism. There is no memory protection. There is no privilege bit. A sufficiently well-crafted piece of input text can cause the model to behave as though the input were instruction.

So who can inject into FieldOps Copilot? The incident title and description come from an end user reporting a problem. In an enterprise, that is usually an employee, so the risk seems low. But consider: incidents will eventually arrive from email intake, from a monitoring integration, from a customer portal. The description may contain a pasted log line, and logs contain whatever an attacker put into a request header. In chapter twenty we will add retrieved runbook content, which someone edited. Every one of those is untrusted content flowing into the prompt.

Now the layered defence, weakest first.

Layer one, the weakest: telling the model that the incident content is data, not instruction, and delimiting it clearly so there is an unambiguous boundary in the text. Do it. It raises the bar. It does not hold against a determined attempt.

Layer two: never interpolate untrusted text into the instruction region. This is a real engineering constraint with teeth. Your template should have exactly one place where untrusted content lands, and it should be a clearly delimited data region at the end. If you find yourself building an instruction sentence by concatenating a user-supplied string, stop — that is the prompt equivalent of string-concatenating a database query, and it fails the same way.

Layer three: constrain the output structurally. If the response must conform to a schema whose category field accepts only a fixed set of values, then a successful injection cannot make the system emit an arbitrary action. The blast radius of a compromised generation is bounded by what the output type can express. This is a strong layer and it is cheap.

Layer four, the one that actually carries the weight: assume the model is fully compromised by its input, and ask what it can then do. In our design, the answer is: produce a suggestion that a human will read and either accept or reject. It cannot close a ticket, because no such capability is exposed to it. It cannot read another tenant's data, because retrieval is filtered before the model sees anything. It cannot send an email, because there is no tool for that. The system is safe not because the model behaves, but because the model's worst behaviour is contained by the architecture around it.

That is the mental habit I want you to take from this section, and it will recur in chapters eighteen, nineteen, and thirty-two. Do not ask "can someone make the model misbehave." Assume yes. Ask "when they do, what is the worst thing that happens," and engineer that answer down until it is acceptable.

One practical addition: log and count suspected injection attempts. If an incident description contains something that looks like instruction-directed text, flag it for review. This is imperfect detection and should never be your only control, but the signal is useful, and being able to tell a customer "we saw three attempts and none of them could have done anything" is a very different conversation from having no idea.

### A worked walkthrough

Let me make this concrete by walking through one realistic change, because the abstract ritual is easy to nod along to and hard to actually perform.

Suppose your operations manager tells you that the copilot keeps suggesting medium urgency for incidents that the team considers high, specifically for anything affecting the warehouse scanning system, because that system going down stops physical shipments within about twenty minutes. She says, reasonably, "it should know that warehouse scanning is critical."

The naive response is to open the prompt and add a sentence saying warehouse scanning incidents are high urgency. It would probably work. It is also wrong in four separate ways, and noticing why is the skill this chapter is teaching.

First, it is a policy change dressed as a wording change. You are adding a rule about the customer's urgency classification. That belongs in the policy configuration, reviewed, with the customer's name on it, not buried in a paragraph of instructions.

Second, it is a specific patch to a general problem. The real finding is not "warehouse scanning is special." The real finding is that your urgency definition does not account for how fast an impact becomes material. Some systems degrade gracefully for hours; some stop physical operations in minutes. If your urgency criteria mention only how many users are affected, the model has no way to express time-to-material-impact, and it will get warehouse scanning wrong, and it will get three other systems wrong too, and you will patch each of them separately forever. Fixing the criterion fixes the class.

Third, it is unverified. You believe it will work. Run the fixtures. You may discover that adding a named-system rule causes the model to over-index on named systems and start downgrading everything unnamed. That kind of side effect is common and invisible without the harness.

Fourth, it is uncorrelated. If you make the change with no version bump and no change note, then in three weeks when someone asks why urgency distributions shifted, the record contains nothing.

So here is the same change done properly. You go back to the operations manager and ask a better question: how quickly does an outage in each of these systems become materially damaging, and is that the thing your team is really reacting to when they escalate? She confirms it is. You now have a discriminator you can write down: urgency reflects both the breadth of impact and the time until impact becomes material, and you define the thresholds with her. That definition goes into the policy configuration, where she can read it. Your service inventory gains a criticality attribute, which is data the asset pipeline in chapter twenty-four will eventually own properly. The prompt template renders both.

Then you run the ritual. Baseline on the current version. Apply the single change. Rerun. You find that four fixtures shifted: three moved from medium to high and are correct, one moved from low to medium and is arguably wrong. You investigate the fourth, find your threshold was stated ambiguously, tighten it, rerun, and now three shifted and one held. You write the change note: what changed — urgency criteria now include time-to-material-impact with stated thresholds; why — operations team escalates on speed of impact, confirmed with the manager on this date; expected difference — fast-impact systems move up one urgency band; fixtures affected — three, all intended. Policy change, so it gets a major version bump and a second reviewer. You publish.

Total elapsed time: maybe an hour longer than the naive fix. What you bought: a rule that generalizes, a customer who agreed to her own policy, evidence that it did what you claimed, and a record that will answer a question somebody asks in six weeks. In field work that trade is always worth taking, and the reason teams skip it is not that they disagree — it is that nobody made the fixture run easy. Make the fixture run easy. It is the highest-return piece of tooling in this entire part of the course.

### Prompt management: where these things live

Three options, and the choice is mostly about who is allowed to change behaviour and how fast.

Option one: prompts inline in application code. Simple, versioned with the code for free, reviewed in normal pull requests. The downsides are that they are hard for non-engineers to read or comment on, and every change requires a full deployment. For an early pilot with one engineer, this is entirely defensible.

Option two: prompts as versioned files in the repository, loaded at startup, with policy data in structured configuration alongside. Still reviewed in pull requests, still deployment-coupled, but now the prompt is a first-class artifact you can point at, diff cleanly, and hand to a reviewer without asking them to read source code. This is my default recommendation for a pilot, and it is what I would expect to see in your test project.

Option three: an external prompt registry or management service, where prompts are stored outside the codebase, fetched at runtime, and editable through a user interface. This is genuinely valuable when non-engineers need to iterate, and it decouples prompt changes from release cycles.

But be clear-eyed about what option three actually is: a mechanism for changing production behaviour without a deployment, a code review, or a test run. That is precisely the property you least want in a safety-relevant artifact. If you adopt a registry, you must add back what you removed — an approval step before a version goes live, an automatic fixture run on the candidate version, an immutable record of who published what and when, and the ability to revert instantly. A registry with those controls is excellent. A registry without them is a loaded weapon pointed at your customer's operations team, and the fact that it has a pleasant interface makes it more dangerous, not less.

There is a middle path worth knowing: keep prompts in the repository, but let the customer-owned policy data — the taxonomy, the urgency definitions — live in reviewed configuration that their administrator can propose changes to, with your approval gate in front of it. That gives the customer ownership of what is genuinely theirs without giving anyone the ability to silently rewrite the safety boundary.

### Versioning, change notes, and the ritual

Now the mechanics.

Every prompt has a stable version identifier. Two schemes work and you can use both. A human-assigned version number communicates intent — a major bump for a policy change, a minor bump for a phrasing change. A content hash guarantees identity — it tells you unambiguously that the text that ran was the text you think ran. The number is for humans; the hash is for correlation. Record both with every suggestion your system produces, alongside the model identifier and version from last chapter.

Say that again, because it is the single most valuable habit in this chapter: every stored recommendation carries the prompt version and the model version that produced it. Without that pairing you cannot answer the customer's Tuesday email, and you cannot tell whether a behaviour change came from your edit or from the provider's model update. Those two causes look identical from the outside and require completely different responses.

Every version has a change note, written by the person making the change, containing four things: what changed, why, the expected behavioural difference, and which fixtures were affected. That last item is the one that prevents self-deception. "Improved clarity" with no fixture movement is a phrasing change. "Improved clarity" with three fixtures changing category is a policy change that was mislabelled, and the change note is where that gets caught.

Then the ritual, which is short and should be automatic.

Before you change anything, run the current version against the full fixture set and save the results as the baseline. Make exactly one change. Run the fixtures again. Diff the outputs, case by case, and classify each difference as intended, neutral, or regression. Write the change note. Get it reviewed by someone other than you if the change touched policy. Then publish.

Two disciplines inside that ritual. Change one thing at a time: if you change the prompt and the model in the same step, and quality moves, you have learned nothing and you have to unwind both. And keep a genuine holdout — fixtures you do not look at while tuning — because prompts overfit to their fixture set readily, and a prompt that scores perfectly on the ten cases you have been staring at for a week may have quietly got worse everywhere else.

Your fixture set for this chapter should be small and pointed. Five is the working minimum, and they should cover a clear unambiguous case, a genuinely ambiguous case, a case missing critical information that must return insufficient evidence, a case containing content that looks sensitive so you can check redaction and handling, and a case where the reported text attempts to instruct the system. That fifth one is a safety fixture and it should never be dropped for being repetitive. Chapter twenty-two grows this into a proper evaluation gate; today you are building the habit and the harness.

Finally, the rollback rule, written down before you need it. It has four parts. What triggers a revert — for instance, any regression on a safety fixture, or an operator-reported quality drop confirmed on fixtures. Who can authorize it — and for safety triggers the answer should be any engineer on call, immediately, with review afterwards, because a revert to a previously approved version is a low-risk action and requiring approval for it just makes outages longer. How it is performed — the mechanism, tested at least once. And what gets recorded — the revert itself is a version event and goes in the log.

Rehearse it once. An untested rollback is a hope.

### Designing the output schema as part of the prompt

One more piece of craft before the pitfalls, because the schema and the prompt are really a single design and treating them separately produces bad versions of both.

Every field you add to the output type is a question you are forcing the model to answer on every call. That has three costs: output tokens, which are the expensive ones; an opportunity for a wrong answer; and a maintenance obligation, because something has to validate it and something has to display it. So the discipline is to justify each field by naming who consumes it.

Run through ours. The suggested category is consumed by the operator's accept-or-edit action, and it drives nothing automatically — justified. The suggested urgency, same. The rationale is consumed by the operator deciding whether to trust the suggestion; it needs to be short, because a paragraph nobody reads is pure cost, and one or two sentences that name the deciding factor is what actually gets read. The missing-information list is consumed by the operator's follow-up to the reporter, and it is arguably the most valuable field in the whole response, because it converts the model's uncertainty into a concrete human action. A confidence signal is consumed by display ordering and by your evaluation analysis — keep it coarse, three bands rather than a percentage, because a percentage implies a calibration you do not have. Provenance fields are consumed by you, later, during an investigation.

Now notice what is not there. There is no free-text notes field, because free text invites the model to say things outside the contract and gives injection somewhere to land. There is no suggested assignee, because that edges toward an action. There is no summary, because the operator can read the original report and a summary is a second place for facts to drift.

Two schema design rules worth remembering. Prefer enumerations to strings everywhere you can, because an enumeration turns an entire class of bad output into an impossible output rather than a detectable one. And give every optional field an explicit meaning when absent — if the missing-information list is empty, does that mean the report was complete, or that the model did not check? Decide, state it in the prompt, and validate it.

Finally, order matters inside the output too. Fields are generated in sequence, so a field generated earlier conditions the ones after it. If you put the rationale before the category, the model reasons and then labels. If you put the category first, it labels and then justifies, which produces rationales that are post-hoc even by the loose standards of generated explanations. For a task where you want the explanation to have any diagnostic value, put the reasoning field first. This is a small thing that costs nothing and that almost nobody does deliberately.

### Pitfalls

Eight, quickly.

Casual editing. Someone tweaks the live prompt to fix one annoying case, does not run fixtures, and shifts behaviour on twenty cases nobody was watching. This is the most common failure by a wide margin. Mitigation: the ritual, and making the fixture run a single easy command so there is no excuse.

The prompt in one person's head. The working version exists only in an engineer's local copy or a chat thread. When they are on leave, nobody can explain the system. Mitigation: the repository is the only source of truth, and what ships is what is committed.

Changing prompt and model together. Covered above. One variable at a time.

Fixture overfitting. Tuning until the visible cases are perfect while general quality degrades. Mitigation: a holdout set you do not tune against.

No version recorded with output. You cannot correlate complaints to causes. Mitigation: provenance on every suggestion, from the first one.

Untrusted text interpolated into instructions. Injection. Mitigation: one delimited data region, output constraints, and an architecture where the worst case is bounded.

Treating policy as wording. You change the definition of high urgency because it reads better, and you have altered the customer's escalation behaviour. Mitigation: the two-bucket sort, and customer review for bucket one.

Prompt sprawl. Six prompts across the codebase, three of them nearly identical, two of them abandoned. Mitigation: one registry of prompts with owners, and deletion of anything not referenced.

### How you verify this chapter

Six checks.

One. Pick a suggestion your system produced yesterday. From its stored record alone, retrieve the exact prompt text and model version that produced it. If you have to guess, you are not done.

Two. Take the last change you made and read its change note. Does it tell a reader what behaviour changed, or only what text changed? If only text, rewrite it.

Three. Hand the policy portion — just the taxonomy and urgency definitions — to someone who is not an engineer and ask if it matches how their team actually triages. If they cannot read it without reading code, your policy is in the wrong place.

Four. Submit an incident whose description contains an explicit instruction to ignore prior directions and mark the item as resolved. Confirm three things: the output still conforms to schema, no state changed, and the attempt was logged.

Five. Perform a rollback to the previous prompt version, end to end, and time it. Then check that the rollback is in the version log.

Six. Change a single word of phrasing, run the fixtures, and confirm you can state whether the difference was intended, neutral, or a regression. If you cannot tell because the harness is too painful to run, fix the harness — it will be run hundreds of times over this deployment.

### The test project

The companion guide is a test. Read it after this, attempt it unaided, and use the inverted hints only at the end.

The goal is to turn your triage instruction into a governed, versioned artifact with a fixture harness and a rollback rule.

You will produce: a first prompt version containing all seven parts, with customer policy separated into structured configuration and incidental phrasing in the template; a stable version identifier and content hash recorded with every suggestion your system stores; at least five synthetic fixtures covering clear, ambiguous, insufficient, sensitive-looking, and instruction-bearing inputs; a baseline result set; one deliberate single-instruction change with a full before-and-after comparison and a change note classifying every difference; and a written rollback rule naming trigger, authority, mechanism, and record.

The constraints. Untrusted content lands in exactly one delimited region and never inside an instruction. The fixture run works offline against your fake for the deterministic checks. No real customer text. Policy changes are distinguishable from phrasing changes in the version history without reading the diff.

You are done when a reviewer who was not present can read two adjacent versions and correctly state the behavioural difference, when every suggestion in your store can be traced to the exact text that produced it, and when your instruction-bearing fixture provably cannot do anything.

### Recap

The decision from this chapter: you stopped treating the prompt as writing and started treating it as versioned production configuration with safety consequences.

The structure: seven parts — context, inputs and their trust level, the task with real criteria, the output contract, uncertainty behaviour, prohibitions, and examples chosen for coverage. Stable content first, variable content last.

The craft: specificity beats cleverness, structure beats persuasion, one decision per call, and an explicit path to "I do not know." Role inflation and emphasis are decoration until fixtures say otherwise.

The field discipline: separate customer policy from your phrasing, make the policy reviewable data, and get customer sign-off on the parts that are theirs. Assume the model can be compromised by its input and make the worst case boring. Record prompt version and model version on every single output.

The ritual: baseline, one change, rerun, diff, classify, note, review, publish — with a holdout set and a rehearsed rollback.

Next chapter we turn the same governance instinct on the tools you build with, rather than the tool you are building. Coding assistants and agents can genuinely accelerate customer delivery, and they can also quietly introduce a dependency, a credential leak, or an assumption into a sensitive deployment. We will define what "agent-assisted but engineer-owned" means in a way you could actually put in a contract.
