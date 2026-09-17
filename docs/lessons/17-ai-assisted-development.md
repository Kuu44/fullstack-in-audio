# Chapter 17 — AI-assisted development without surrendering engineering judgment

**Roadmap nodes covered:** Cursor; Claude Code; Codex; Gemini; Vibe Coding
**Part:** IV — Build AI behavior that can be controlled
**Companion test:** `docs/guides/17-ai-assisted-development.md`
**Audio:** `media/17-ai-assisted-development.mp3`

---

## Narration

Welcome to chapter seventeen.

For two chapters we have been careful about the model inside our product. We gave it a narrow port, a fixed output shape, an explicit uncertainty path, a versioned instruction, and no ability to change anything. We assumed it could be compromised by its input and we made sure the worst case was boring.

Now I want to turn that same scrutiny around, and point it at the models you are using to build with.

Because here is an uncomfortable asymmetry. The model inside FieldOps Copilot can, at absolute worst, produce a bad suggestion that an operator rejects. The coding assistant on your machine can write to your customer's repository, read your environment files, add a dependency, run a command against a database, and change the authorization check on an endpoint. It operates with your credentials and your permissions, and its output ships to production under your name.

The one we put behind a glass wall is the harmless one. That is worth sitting with for a moment.

This chapter is not anti-tool. These tools are genuinely excellent and I would not want to deliver without them. It is about the specific discipline that makes them safe in a customer environment, which is a harder environment than your own side project, and about a phrase you need a clear position on: vibe coding.

Here is the plan. First, what these tools actually are, arranged by how much autonomy they take. Second, an honest account of what they are good at and where they fail, including the failure mode nobody talks about. Third, the three risks that are specific to field work — data egress, supply chain, and assumption smuggling. Fourth, the review capacity problem, which I think is the real one. Fifth, the protocol: what "agent-assisted but engineer-owned" means concretely enough to put in a document. Then accountability, pitfalls, verification, and the test project.

### The spectrum of assistance

Let me lay out the landscape, because "AI coding tool" covers products with wildly different risk profiles and people talk about them as one thing.

At the low-autonomy end: inline completion. The editor suggests the rest of a line or a block, you accept or reject with a keystroke. The unit of review is small, you are looking at it as it appears, and the main risk is the quiet one — over time you accept suggestions that are plausible rather than correct, because rejecting requires more attention than accepting.

Next: chat in the editor, with awareness of your open files or your whole repository. You ask a question or request a change, you get a proposal, you apply it. The unit of review is a diff you chose to request. This is the sweet spot for most careful work.

Next: agentic coding in the editor or as a command-line tool. You state a goal, and the agent reads files, edits multiple files, runs the test suite, reads the failures, and iterates. Cursor's agent mode, Claude Code, Codex, and Gemini's command-line agent all live here, with different interfaces and different default permissions. The unit of review is now a completed multi-file change, possibly after dozens of intermediate steps you did not see, and often after the agent ran commands on your machine.

At the high-autonomy end: background and cloud agents that take an issue, work in their own environment, and open a pull request. The unit of review is a pull request from a contributor who cannot answer follow-up questions about its reasoning in any reliable way.

Notice what increases across that spectrum: not capability so much as the size of the thing you must review and the amount of activity you did not observe. That is the axis that matters. Your discipline has to tighten as you move along it, and the tools do not tighten it for you — their defaults generally move the other way, because frictionless feels better in a demo.

Now, vibe coding. The term was coined to describe a specific practice: building by describing what you want, accepting the generated code without really reading it, and steering by whether the result behaves correctly rather than by understanding the implementation. The important part of the original framing, which gets lost, is that it was described as suitable for throwaway weekend projects.

I want to give you a clear position, because you will be asked. Vibe coding is a legitimate technique with a legitimate domain. That domain is: code whose failure costs you nothing, that nobody else will maintain, that handles no sensitive data, and that you are willing to throw away entirely rather than debug. A script to reshape a file you will use once. A prototype to see whether an interaction feels right before you design it properly. Exploring an unfamiliar library by generating five variants and seeing which runs.

Outside that domain — and a customer deployment is very far outside it — accepting code you have not read is not a productivity technique, it is a transfer of risk from your attention to your customer's operations. The distinction is not about the tool. It is about whether anyone has read the code. You can use the most autonomous agent available and not be vibe coding, if you review every line before it lands. You can use plain inline completion and be vibe coding, if you accept on reflex.

So the rule for this course, and I would defend it in any customer conversation: in the FieldOps Copilot repository, no line ships that a human has not read and can explain. How it was produced is your business. Whether it was understood is the customer's.

### What they are good at, and where they fail

Let me be concrete, because generic advice here is useless.

Where these tools earn their cost, in roughly descending order of value for field work.

Explaining unfamiliar code. You land in a customer's codebase with four hundred thousand lines and two days to understand the part you must integrate with. Asking for an explanation of a module, a call path, or an unfamiliar framework convention is enormously faster than reading linearly, and the failure mode is mild — if the explanation is wrong, you find out when you read the code it pointed you to, and you have still been pointed somewhere useful.

Writing tests against a stated contract. You specify the behaviour, the assistant writes the cases. This is a good fit because tests are read carefully by definition, because a wrong test fails loudly rather than silently, and because the tedium of covering five failure paths is exactly the tedium that causes humans to cover two. Your chapter fifteen fake, with its five failure modes, is a good candidate.

Generating synthetic data and fixtures. We need a dozen realistic-but-fake incident reports with varied jargon density and messiness. That is a genuinely tedious writing task where variety matters more than precision, and there is no risk, because it is all synthetic by construction.

Mechanical refactors with a clear shape. Renaming a concept across a codebase, extracting an interface, converting a callback style to async. The correctness criterion is "behaviour unchanged," which your test suite can actually check.

Boilerplate at a boundary you have already designed. Once you have decided the adapter's shape, filling in the request construction and error mapping is not where your judgment adds value.

First drafts of documentation from code. Useful, always wrong in interesting ways, and the wrongness tells you where the code is unclear.

Now where they fail, and I want to be specific rather than gesturing at "hallucination."

They fail on decisions that depend on context they cannot have. Your customer's security lead said incident text may not leave the tenant region. That constraint lives in a meeting, not in the repository. An assistant designing a caching layer will happily propose something sensible and wrong. Every architectural decision in this course — the port shape, the autonomy boundary, the provider choice — is of this kind. These tools are not bad at them; they are structurally unable to do them, and the more fluent their proposal, the more likely you are to forget that.

They fail on code where "looks right" and "is right" diverge most. Concurrency. Authorization logic. Cryptographic use. Error handling paths that are rarely exercised. Retry and idempotency interactions. These are precisely the areas where plausible-looking code is most dangerous, because review by reading is weakest there for humans too.

They fail at knowing when they are wrong. This is the one that really matters and it is the deep reason for everything in this chapter. A junior engineer who does not understand your retry semantics will usually say so, or their uncertainty will show. A model produces the same confident, well-formatted, idiomatic output whether it is correct or invented. There is no tell. So your review cannot be risk-weighted by the tool's apparent confidence — it has to be weighted by the consequence of the code, every time.

And they fail at staying in scope. You ask for a small fix; you get the small fix plus a reorganized import block, a renamed variable, a "helpful" added null check, and a changed default. Most of it is harmless. One of them is not, and it is hiding in a diff that is six times larger than the change you asked for.

### Choosing and configuring the tool

A short practical section, because the roadmap names four specific products and you will be asked which to use.

Cursor is an editor with the assistance built into the editing surface. Its strengths are that the review loop is where you already work — proposed changes appear as diffs you accept or reject in the file, and the repository index gives it broad context. Its agent mode moves it up the autonomy spectrum, and its rules files are how you carry project instructions.

Claude Code is a command-line agent. It lives in the terminal, reads and edits files, runs commands, and iterates against your test suite. The command-line framing is honest about what it is doing: it is a process with your permissions in your working directory. It supports project instruction files and permission rules for which commands may run without asking.

Codex, as a product line, spans an in-editor assistant and a cloud agent that works in an isolated environment and produces a pull request. The cloud variant is the high-autonomy end of the spectrum, and it has an interesting property: because it runs in a sandbox with a defined network policy, the egress question is sharper and more controllable than on your laptop.

Gemini's command-line agent occupies similar ground to Claude Code, with its own context handling and tool permissions, and with a natural fit if your customer is already committed to Google's cloud and identity.

Now, the advice. The differences between these products are real, they change every few months, and they are far less important than four configuration decisions you should make identically regardless of which you pick.

First: what may run without asking. Every agentic tool has a permission model for shell commands. The default is usually more permissive than you want in a customer repository. Decide explicitly what is auto-approved — running tests, reading files, type checking — and what always requires a prompt: anything that writes outside the working tree, anything that touches the network, anything that installs, and anything that touches a database. Do not approve a package installer for automatic execution. That is the door the supply-chain risk walks through.

Second: what is excluded from context. Environment files, credential directories, any fixture directory that might contain customer-derived content, and anything under a path your customer told you not to transmit. Configure it, then verify it empirically.

Third: which account tier, with which data terms. For customer work, use a tier with no-training and defined retention, and know what the terms actually say rather than what the marketing page implies.

Fourth: where the project instructions live and whether they are committed. Commit them. They are part of how the system is built, they should be reviewed like anything else, and they should apply to every engineer on the engagement rather than living in one person's settings.

Get those four right and the choice between products is mostly a preference about interface. Get them wrong and no product choice saves you.

### Using an assistant as a reviewer

One inversion worth knowing, because it flips the risk profile in your favour.

Everything so far has treated the assistant as a producer of code that you review. But the same tools are useful as a reviewer of code that you wrote, and in that direction the failure mode is much more benign. If a reviewer is wrong, you get a false alarm and you spend two minutes dismissing it. If a producer is wrong, you get a defect that ships.

So ask for adversarial review rather than approval. Useful requests: what does this code do that the description does not mention; what inputs would make this fail; which error paths are unhandled; what assumptions does this make about ordering, concurrency, or the caller; and what would a security reviewer flag here. These are all questions where a broad, pattern-matching reader genuinely adds something, because it has seen an enormous number of failure shapes and does not get bored on the fourth read.

Two limits. Do not treat a clean review as evidence of correctness — absence of flagged issues is very weak evidence, and it will miss the context-dependent problems that matter most, exactly as it would if it had written the code. And do not paste customer code into a tool that is not permitted to receive it just because you are asking about it rather than generating from it. Transmission is transmission.

The most valuable single use of this inversion, in my experience, is on your own diff before you commit. Ask what the change does beyond its stated purpose. It catches scope creep — including the scope creep the assistant itself introduced earlier.

### The three field-specific risks

Now the risks that are different when you are working in or near a customer environment.

Risk one: data egress. These tools work by sending context to a provider. That context can include the file you are editing, files the agent decided to read, your repository index, terminal output the agent captured, and, with agentic tools, the results of commands it ran. Ask yourself what is in those places. Your environment file with a database password. A test fixture someone built from a real incident. A log excerpt with a customer's employee name in it. A customer's proprietary source code, which you may be contractually forbidden from disclosing to third parties.

That last one is not hypothetical and it is the one that gets people in trouble. Many customer engagements have confidentiality terms that cover their source code. Running a tool that transmits that source to a third-party provider may be a contract breach regardless of how good the provider's own privacy terms are, because the question is not whether the provider behaves well, it is whether you were permitted to send it at all.

So the controls. Know what your tool sends and when, including whether it indexes the whole repository. Use the ignore mechanisms to exclude environment files, secrets directories, and any customer data directory, and verify they work rather than trusting them. Prefer enterprise or business tiers, which typically offer no-training-on-your-data and retention controls, and get that in writing. And before you run any assistant inside a customer repository, find out whether you are allowed to. Ask. The answer is usually yes with conditions, and asking costs you five minutes and buys you the ability to say "we confirmed this with your security team" when it comes up later, which it will.

Risk two: the supply chain. Agents add dependencies. It is one of the most natural things for them to do, because the training data is full of code that imports things. Three problems follow.

The first is that a dependency is a permanent obligation that arrived through a two-second decision. Somebody now has to patch it, audit it, and explain it in the customer's security review.

The second is more specific and quite dangerous: models sometimes invent package names that do not exist, and attackers have noticed. They register the commonly-hallucinated names and put malicious code in them. So an agent suggests an import, the install succeeds because someone squatted the name, and you have executed hostile code in an environment that has credentials. The defence is straightforward but has to be a habit: every new dependency gets checked by a human — does this package exist, is this the real one, who maintains it, when was it last updated, how many transitive dependencies does it drag in, and what is its licence.

The third is licence contamination. A copyleft dependency in a component you are delivering to an enterprise customer can create obligations that your customer's legal team will be unhappy to discover after deployment.

Make the dependency diff a separate, explicit review step. Not part of reading the code change — a distinct look at the manifest and the lockfile, every time.

Risk three, and the subtlest: assumption smuggling. The generated code works. The tests pass. And embedded in it is an assumption that is not yours.

Examples I have genuinely seen. A permissive cross-origin setting, because the example the model learned from was a tutorial. An error handler that catches broadly and logs, turning a failure into a silent wrong answer. A retry loop with no bound, because unbounded retry is simpler to write. A database query built by string concatenation, because that is shorter. An overly broad cloud permission, because the narrow one requires knowing the exact resource. A default that disables validation in development and was never scoped to development. A timeout omitted entirely.

Every one of these looks completely ordinary in a diff. None of them announces itself. They pass review because reviewers read for "does this do what was asked" rather than "what does this also do." And in a customer deployment, several of them are findings in a security review, which means schedule slip and reputational cost at exactly the wrong moment.

The counter is to review against your own standards rather than against the request. Keep a short checklist of the assumptions your project has already decided — how errors propagate, what timeouts exist, how credentials are obtained, what is permitted at the network boundary — and check generated code against the checklist, not against whether it looks like reasonable code. It will always look like reasonable code.

### The review capacity problem

Now the structural issue, which I think is the actual problem and which no tool setting solves.

Generation has got dramatically faster. Review has not. Reading code with real understanding runs at roughly the speed it always did, and it is more tiring than writing, and it degrades fast with volume. So the bottleneck has moved, and when a bottleneck moves and the process does not change, the system finds a way to skip the bottleneck. In practice that means diffs get skimmed, and then they get scrolled, and then they get approved.

The consequence is not that bad code ships, at least not immediately. The consequence is that you accumulate code you do not understand, in a system you are accountable for. Then an incident happens at the customer site at eleven at night, and the thing you need is comprehension, and you do not have it. You are debugging your own repository as a stranger.

I want to put this plainly because it is the thing that separates sustainable use of these tools from the other kind: the limit on how much you should generate is not how much the tool can produce, and it is not how much you can verify by running tests. It is how much you can read and understand in the time you have. That is a much smaller number, and it does not grow when the model gets better.

Three practices follow.

Constrain the batch. Ask for changes that produce diffs you will actually read — one concern, tens of lines, not hundreds across a dozen files. If an agent proposes something large, it is usually better to take the plan and request it in pieces than to review the whole thing at once.

Keep generated changes separable. Commit assistant-produced work separately from your own edits, at least initially, so a reviewer can see what came from where and apply proportionate scrutiny. This is also enormously useful later when you are bisecting a bug.

Spend your review budget by consequence, not by size. A hundred lines of test fixtures deserve a skim. Ten lines touching the authorization check deserve line-by-line attention and probably a test written by hand. The tool has no idea which is which. You do.

There is a useful diagnostic for whether you are over your limit, and it is uncomfortable to run. Pick a file in your repository that was substantially generated a week or two ago. Without opening it, describe what it does, what its error behaviour is, and what would break if a dependency it uses started failing. Then open it. If the description was thin, you have been accumulating faster than you have been understanding, and the right response is not to try harder at review — it is to generate less per unit of time until the two rates match again.

And notice that this problem gets worse, not better, as the tools improve. A tool that produces mediocre code creates its own brake: you have to fix it, and fixing produces understanding. A tool that produces good code removes the brake entirely, because there is nothing to fix and the tests pass. The better the tool, the more deliberate the discipline has to be. That is counterintuitive and it is why teams get into trouble at the point where they start trusting the output.

One more structural support: put the things you cannot rely on yourself to check into automation. A test that fails when an endpoint lacks an authorization check. A lint rule that rejects a broad catch or a missing timeout. A pipeline step that fails when the dependency manifest changes without a corresponding note. Human review is where judgment goes; anything mechanical should be a machine's job, because that is the part of review that degrades first when you are tired and the customer is waiting. We build most of this in chapter twenty-seven, but the instinct belongs here: every assumption you keep having to catch by reading is a candidate for a check that never gets tired.

### The protocol

So here is "agent-assisted but engineer-owned," stated concretely enough that you could put it in a delivery document and a customer could audit against it. Five elements.

Element one: project instructions. Most of these tools read a project-level instructions file. Put the real constraints in it. What this system is and who uses it. The rule that no secret is ever written into code or into a prompt. That tests accompany behaviour changes. That dependencies require explicit human approval. What the assistant must never touch autonomously — for us, that is the authorization layer, the audit path, the priority policy, and anything involving credentials. And the autonomy boundary of the product itself, so a well-meaning agent does not add a convenient auto-close feature. This file is cheap to write and it changes behaviour meaningfully. It is also, incidentally, a good artifact to show a customer.

Element two: scoped requests. Ask for one thing with a stated contract. "Write tests for these five failure paths of the fake triage adapter, using the existing test conventions" is a good request. "Add AI triage to the app" is an invitation to review two thousand lines you did not design. The narrower the request, the more the tool's actual strength — filling in a shape you specified — is what you get.

Element three: understand before you keep. Read every changed line. For anything non-trivial, reimplement or substantially edit rather than accepting wholesale; the act of typing it is what produces the understanding you will need later. If you cannot explain why a line is there, it does not stay. This is the whole protocol in one sentence, honestly, and the other four elements exist to make it feasible.

Element four: verify with things that do not lie. Run the tests, including the ones you wrote by hand. Run the type checker and the linter. Review the dependency and configuration diff as a separate step. For anything touching the AI path, run your chapter sixteen fixture harness, because a subtle change to prompt assembly will not show up in a unit test but will show up there.

Element five: record it. A short review note per assisted change: what you asked for, what you accepted, what you rejected and why, what you verified. Three or four lines. This takes a minute and it does three things — it makes you articulate your review, which improves it; it gives the customer's security reviewer something real to look at; and it gives the next engineer context about which parts of the codebase were generated and how carefully they were checked.

Let me make it concrete for this chapter's work. Things I would happily hand to an assistant in FieldOps Copilot right now: generate fifteen additional synthetic incident fixtures with varied phrasing; write the test cases for the fake's five failure paths given the contract; explain an unfamiliar provider library's retry behaviour; draft the operator-facing error copy; turn my endpoint definitions into a first-draft contract document.

Things I would not delegate, and would only use assistance to critique after I had done them: the tool authorization boundary we build next chapter; the injection defence; anything touching the audit trail; the provider decision; the autonomy boundary. Not because an assistant would do them badly — it might do them fluently — but because these are the decisions the customer is actually paying for my judgment on, and because they are the ones where a plausible wrong answer is most expensive.

### Accountability

Three short points that matter more than they seem.

First: "the assistant generated it" is not a defence, anywhere. Not in a post-incident review, not in a security finding, not in a contract dispute. You committed it, your name is on it, your company delivered it. The tool has no liability and cannot be called as a witness. Internalize that and your review standards set themselves.

Second: many enterprise security questionnaires now ask directly whether AI coding tools were used in developing the delivered software, which tools, and under what data controls. You want a prepared, honest, specific answer: which tools, on which tier, with what retention terms, with what exclusions configured, and what the human review process was. "Yes, with these controls and this review protocol" is a fine answer. Being surprised by the question is not.

Third, on provenance: generated code can resemble training data. For most ordinary application code this is a minor concern, but if you are delivering something the customer will own outright, it is worth knowing your tool vendor's position on indemnity and whether they offer a duplication filter. Know it before someone asks rather than after.

### Pitfalls

Eight.

Reviewing for intent instead of for content — reading whether the code does what you asked, rather than what else it does.

Letting the diff grow past your attention span and approving anyway. If the diff is too big to read, it is too big to accept; ask for it in pieces.

Running an agent in a customer repository without permission. Ask first. Every time, for every customer.

Accepting a new dependency without checking that the package is real, maintained, and licensed acceptably.

Changing generated code and your own code in the same commit, so nobody can later tell which was which.

Trusting tests written by the same tool that wrote the code. Both can share the same misunderstanding, and then the green suite is evidence of consistency, not correctness. Hand-write the test for anything critical.

Letting the assistant broaden the product's autonomy. It has read a lot of code where systems act automatically, and it will helpfully suggest that yours does too. Your instructions file should forbid this explicitly.

Skipping the fixture harness because the unit tests passed. Prompt assembly changes do not show up in unit tests.

### How you verify this chapter

Five checks, all actions.

One. Open your project instructions file and read it as an adversary. Does it actually forbid the things that would hurt you, or does it contain generic encouragement?

Two. Take your most recent assisted change and, without looking at it, write down what it does. Then read it. The gap is your real review quality.

Three. Look at your dependency manifest and find the newest addition. Can you name what it does, who maintains it, why it beat the alternatives, and its licence? If not, that is the whole lesson in one line.

Four. Confirm what your tool is configured to exclude, then verify it empirically rather than by reading configuration — put a marker string in a file that should be excluded and check it never appears in context.

Five. Write the answer you would give to a customer asking which AI tools touched their codebase and under what controls. If writing it makes you uncomfortable, change the practice, not the wording.

### The test project

The companion guide is a test. Attempt it before the hints.

Your goal is to establish an assisted-development protocol for FieldOps Copilot and demonstrate it on one real, narrow change.

You will produce: a project instructions file stating the charter, the no-secret rule, the test expectation, the dependency-approval rule, the forbidden-autonomous-actions list, and the product's own autonomy boundary. One narrowly scoped assistant request — a test idea, a code explanation, or a small fixture generation task, not a feature. Evidence that you reimplemented or substantially edited the result after checking every line. Test and type-check output, plus a separate review of the dependency and configuration diff. And a short review note recording what you asked, accepted, rejected, and verified.

The constraints: no production customer data or credentials reach any tool by default, and you can demonstrate the exclusions work. The change is small enough that you genuinely read all of it. Generated work is separable from hand-written work in history. And the assistant does not touch authorization, audit, or the autonomy boundary.

You are done when someone else could follow your protocol without you explaining it, when your review note would satisfy a security reviewer, and when you can honestly say you understand every line that landed.

### Recap

The decision from this chapter: you defined a repeatable boundary between assistance and ownership, and wrote it down so it survives schedule pressure.

The shape of it: these tools are strong at explanation, test generation, fixtures, mechanical refactors, and boilerplate inside a design you specified. They are structurally weak at decisions requiring context they cannot have, at code where plausible and correct diverge, and at knowing when they are wrong.

The field-specific risks: data egress including customer source you may not be permitted to transmit; a supply chain where hallucinated package names are an active attack vector; and assumption smuggling, where ordinary-looking code carries a default you never chose.

The real constraint: review capacity, not generation capacity. Size your batches to what you can read and understand, spend attention by consequence, and remember that accumulating code you do not understand is a debt that comes due during an incident.

And the position on vibe coding: legitimate for throwaway work, malpractice in a customer deployment. The distinction is not the tool, it is whether a human read it.

Next chapter we go back to the product and give the model its first controlled contact with a real system — a read-only tool. We will define a tool contract, authorize it properly, expose it through a Model Context Protocol adapter, and make sure that a model failure or a malformed call can never route around the authorization boundary. The habits from this chapter apply directly: assume the caller is compromised, and bound the worst case.
