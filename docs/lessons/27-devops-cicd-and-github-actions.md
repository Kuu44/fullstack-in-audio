---
chapter: 27
title: "DevOps, CI/CD, and GitHub Actions"
slug: 27-devops-cicd-and-github-actions
part: "Part VI — Ship and protect the production-shaped system"
roadmap_nodes: ["DevOps Skills", "DevOps & CI/CD", "GitHub Actions"]
voice: en-US-AndrewNeural
rate: "-18%"
audio: media/27-devops-cicd-and-github-actions.mp3
companion_guide: docs/guides/27-devops-cicd-and-github-actions.md
---

# Chapter 27 — DevOps, CI/CD, and GitHub Actions

> Narration script. Headings, frontmatter, and blockquotes are stripped before rendering; only the prose below is spoken.

Welcome to chapter twenty-seven, and to Part Six. The system you have built is, at this point, genuinely substantial. An operator workspace, a secured service, a durable record, a data pipeline with a schedule, a grounded and bounded agent, an evaluation suite, and a release manifest that pins every element of the AI configuration. There is one thing holding all of it together that we have not examined, and it is the weakest part of the whole deployment. That thing is you.

Right now, the checks run because you remember to run them. The artifact gets built because you build it. The evaluation gate passes because you looked at the results. The release manifest is accurate because you were careful. Every one of those is a human step, and human steps have a characteristic failure pattern: they work perfectly until the week that matters, when there is a customer deadline, three interruptions, and a fix that seems too small to need the full process.

Continuous integration and continuous delivery exist to move those steps from your memory into the system. That is the whole idea. Everything else in this chapter is detail.

Let me define the terms carefully, because they get used loosely and the distinctions matter in a customer conversation.

Continuous integration is the practice of merging work frequently into a shared line of development, with automated verification running on every change. The verification is the point. Continuous integration without automated checks is just frequent merging, which mostly means frequent conflicts.

Continuous delivery is the practice of keeping the software in a state where it could be released at any time, with the release process itself automated. Note the word could. Delivery means the button exists and works; a human decides when to press it.

Continuous deployment goes one step further: every change that passes the gates goes to production automatically, with no human decision. For a customer pilot involving artificial intelligence behavior and enterprise approval processes, continuous deployment is almost always the wrong choice, and being able to explain why you chose delivery over deployment is a mark of judgement rather than timidity. Your customer's change management process exists; automating past it does not eliminate it, it just means you are violating it faster.

Now the mechanics. A pipeline is a sequence of stages triggered by an event, usually a change being pushed or a merge request being opened. A stage contains one or more jobs, and a job runs on a runner, which is a machine, usually ephemeral, that is created for the job and destroyed afterwards. Ephemeral is a security property as much as a convenience: nothing persists between runs unless you deliberately persist it, so one run cannot contaminate the next.

An artifact is the built output you intend to deploy. The single most important rule in this entire chapter concerns artifacts, so let me state it plainly: build once, deploy many times. The thing you tested must be the identical thing you deploy. If your pipeline builds in continuous integration, then builds again during deployment, you have tested one artifact and shipped a different one, and the difference between them is exactly where the interesting bugs live. Build the artifact once, give it an identifier, store it, and have every subsequent stage refer to that identifier.

Caching is the mechanism for not redoing expensive setup work, typically dependency installation. It is valuable and it carries a specific trap: a cache is an input to your build that is not in your source control. If a corrupted or poisoned cache can change your output, your build is not reproducible. Key caches on something derived from your dependency lock file, and be prepared to invalidate them when diagnosing a build that behaves differently in the pipeline than on a clean machine.

A matrix build runs the same job across several variations, such as multiple runtime versions or operating systems. In field work this earns its keep when the customer's target environment differs from your development machine, which it usually does.

Branch protection and required checks are the enforcement layer. A required check means the platform will refuse to merge a change unless the named job succeeded. This is the mechanism that turns your evaluation suite from a thing people should run into a thing they cannot skip. Without it, your careful gate is a suggestion.

Environment protection rules attach requirements to a deployment target: which branches may deploy to it, who must approve, and whether there is a waiting period. This is where the human decision in continuous delivery actually lives, and it is the technical artifact you show a customer's change management reviewer.

Then secrets, which is where continuous integration gets genuinely dangerous, and where I want you to be more careful than the average tutorial suggests.

A secret is any credential the pipeline needs: a registry password, a cloud deployment identity, a model provider key. The platform gives you encrypted storage and injects them into jobs that need them. Three principles govern their use, and each one exists because of a real, repeated incident pattern.

The first is that secrets must not be available to untrusted code. Here is the attack. Your repository accepts contributions. Somebody opens a merge request that changes a build script to print the contents of an environment variable, or to send it somewhere. If your pipeline runs that submitted code with your secrets present, you have handed your credentials to a stranger. The defence is a split: the checks that run on untrusted proposed changes get no secrets, and anything requiring a secret runs only after a trusted merge, or under an explicit approval, or in a separate workflow that does not execute the submitted code. In a private customer repository the risk is lower but not zero, because a compromised dependency in your build can do exactly the same thing.

The second principle is that long-lived static credentials should be replaced with short-lived ones wherever the platform supports it. Modern continuous integration platforms can prove their identity to a cloud provider directly and receive a temporary credential scoped to the job. This removes the stored cloud key entirely. There is nothing to leak, nothing to rotate, and nothing sitting in a settings page that somebody copied into a chat message two years ago. When you are working with a customer's security team, this is one of the most persuasive things you can offer, because it eliminates a class of finding rather than mitigating it.

The third principle is least privilege for the pipeline itself. The deployment identity should be able to deploy and nothing else. Not read the database. Not manage other workloads. Not create new identities. A continuous integration system is an extremely attractive target precisely because it usually has powerful credentials and executes code that many people can influence.

Before the principles get too abstract, let me tell you how this goes wrong in the field, because the scenario is common enough to be a genre.

You are on site. It is the afternoon before a steering committee demonstration. An operator finds a real problem: a particular severity value causes the intake form to reject a valid incident. It is a five-character fix. You make it, you run the one test you think is relevant, it passes, and you deploy it by hand to the pilot environment because the full pipeline takes eleven minutes and you have a meeting in nine.

It works. The demonstration goes well. And you have just introduced three problems that will surface later. The first is that the artifact now running in the pilot environment does not correspond to any commit that passed the full gate, so your release manifest is now a work of fiction. The second is that the fix exists on the deployed machine and, if you are unlucky, not in version control at all, which means the next legitimate deployment silently reverts it and the bug returns with no explanation. The third is subtler and worse: you did not run the evaluation suite, and your change altered the set of accepted severity values, which is an input to the triage prompt's category mapping. Nobody will connect a drop in proposal quality three weeks later to an afternoon hotfix.

I am not telling you this to moralize about process. I am telling you because the pressure in that moment is completely real, and willpower is not the answer. The answer is design. If your tier-one pipeline runs in four minutes instead of eleven, you wait for it. If deployment is a single approved action rather than a manual sequence, doing it properly is faster than doing it by hand. If rollback is one operation, you are less afraid of shipping through the normal path. Every one of those is an engineering decision you make on a calm day so that the frantic day takes care of itself.

That is what people actually mean when they talk about DevOps as a culture rather than a toolset. The underlying claim is that the people who write software should be accountable for operating it, and that the way to make that accountability bearable is to automate the path between the two. For a forward deployed engineer this is not aspirational, it is simply your job description: you write it, you deploy it, you diagnose it at the customer site, and you hand it over in a state where somebody else can do the same. There is no separate operations team coming to rescue your deployment, and there is often no separate release manager to enforce discipline. The pipeline is the release manager.

Now let me spend a moment on why this matters more in forward deployed work than in a product team, because the emphasis genuinely differs.

The first reason is that you deploy into environments you do not control. A product team's pipeline deploys to infrastructure the team owns, configured the way they like. You may be deploying into a customer's cloud account, with their network restrictions, their approved base images, their identity provider, and their change windows. Automation is what makes that repeatable. Every manual step in a deployment is a step that must be performed correctly by somebody who may not be you, possibly under time pressure, possibly in a region you cannot reach.

The second reason is handover. Your pilot ends and somebody else maintains the system. The pipeline is the executable form of your deployment knowledge. If deploying requires seven commands in the right order with two judgement calls, then when you leave, the system effectively becomes unchangeable, and an unchangeable system decays. If deploying is a merge and an approval, the customer's own team can keep it alive.

The third reason is evidence. Enterprise customers ask how you know a change is safe. A pipeline definition in version control, with required checks and recorded runs, is a far stronger answer than a description of your team's habits. It is also durable: it answers the question in a security review nine months later when nobody involved is in the room.

The fourth reason is the specific difficulty of testing artificial intelligence behavior in a pipeline, which is worth solving properly because most teams get it wrong. Let me deal with that now, because it shapes the whole design.

Your evaluation suite has three awkward properties. It may call a paid provider, so running it on every push costs real money that grows with team activity. It is non-deterministic, so it can fail for reasons unrelated to the change. And it needs a provider credential, which we just said should not be available to untrusted proposed changes. If you ignore these, you end up with an expensive, flaky, insecure gate that people learn to re-run until it goes green, which is worse than no gate because it teaches the team that failures are noise.

The solution is tiering, and I want you to internalize this pattern. Split your verification into three tiers by cost and trust.

The first tier runs on every proposed change, with no secrets, in a minute or two. Dependency installation, linting, type checking, unit tests, and your evaluation suite running against the deterministic fake implementation of the model interface. That last point is why chapter fifteen insisted on the fake. Against the fake, your eval suite is free, instant, and completely deterministic, and it still catches an enormous amount: structural validity of outputs, prohibited actions, citation requirements, tool contract violations, and every piece of logic in your agent's state machine. Most regressions you will actually cause are caught here.

The second tier runs after merge, or on a schedule, with credentials, against a real provider using synthetic fixtures. This is where you measure genuine model quality against your recorded baseline, and where you measure latency and cost. It costs money, so it runs on a controlled trigger rather than on every push, and because it is non-deterministic you judge it against a tolerance rather than exact equality.

The third tier runs before promotion to the pilot or production environment. It is the full gate from chapter twenty-six: deterministic checks, quality within tolerance of baseline, budget met, and manifest completeness. This is the one attached to environment protection and human approval.

Handling non-determinism deserves one more sentence, because it is the thing that erodes trust in a gate. Do not assert exact outputs. Assert properties: the output parses against the schema, it contains a citation when retrieval was strong, it never proposes a write action, its category is within the allowed set, and its aggregate quality score across the suite is within tolerance of baseline. Properties are stable under the normal variation of a language model; exact strings are not. And when a tier-two run does fail, have it retain the actual outputs as an artifact, so a human can look at what happened rather than re-running blindly.

Now let us lay out the pipeline for FieldOps Copilot end to end.

On a proposed change, run tier one. Install dependencies from a lock file, so the build is reproducible. Lint and type check, because these are the cheapest bugs you will ever catch. Run unit tests for the priority policy, the validation rules, and the pipeline stages. Run service-level tests for the interface, including the authorization cases from chapter twelve: unauthenticated, unauthorized, valid, and malformed. Run the pipeline tests from chapter twenty-four, including idempotency and quarantine behavior. Run the evaluation suite against the fake. Verify the manifest can be generated and is complete. No secrets are present in any of this, which means it is safe to run on any proposed change, and it is fast enough that people will not route around it.

Then build the artifact, once. Tag it with the commit identifier. Retain it along with the test results and the generated manifest. From here on, every stage refers to that artifact by identity.

On merge to the main line, run tier two with credentials, against synthetic fixtures, recording quality, latency, and cost against the baseline. Update the release manifest with those results and attach them to the stored artifact.

On a promotion request to the pilot environment, evaluate the full gate, require the environment approval, and deploy the retained artifact. Not a rebuild. The same bytes.

There is one part of that sequence I skipped over, and it is the part that causes the most real-world deployment failures: database migrations. Your PostgreSQL schema from chapter thirteen evolves, and those changes have to happen somewhere in the pipeline. Three rules will keep you out of trouble.

First, migrations run as a distinct, observable step, not as a side effect of the application starting up. Migration-on-startup seems convenient until you run two instances and both try to migrate simultaneously, or until a migration fails and you now have a service that crash-loops while holding a partially applied schema. Make it a step with its own status and its own log.

Second, migrations must be forward-compatible with the currently running version for the duration of the deployment. During any rolling deployment there is a window where old and new code are both running against one database. If your migration drops a column the old code still reads, that window is an outage. The standard technique is to split a breaking change across releases: first add the new structure and write to both, then move readers over, then, in a later release, remove the old structure once nothing references it. It feels laborious and it is the difference between a deployment and an incident.

Third, and this follows directly: rollback of code does not roll back data. If you deploy release fifteen, it migrates the schema, and you roll back to release fourteen, the schema is still at fifteen. This is precisely why forward compatibility matters, and it is why your rollback rehearsal in chapter twenty-six must include a schema change to be honest. Test the rollback of a release that migrated, not just one that did not.

And keep one more thing in the pipeline that teams forget: the ability to deploy a previous artifact. Rollback should be a pipeline operation, ideally the same deployment job pointed at an earlier artifact identifier. If rollback is a different, rarely exercised code path, it will not work on the night you need it.

Let me also say something about running the same verification locally, because it matters for field velocity. A fresh checkout should be able to run the tier-one checks with one documented command, and get the same result the pipeline gets. When those diverge, engineers stop trusting the pipeline and start guessing. The usual cause of divergence is hidden state on the development machine: an installed tool, an environment variable, a database left in a convenient condition. Pin your versions, install from the lock file, and make the tests create their own fixtures. In a customer environment, where you may be working on a locked-down laptop or a jump host, the value of a build that does not depend on your personal setup goes up sharply.

Next, the supply chain, because a pipeline is the place where somebody else's code most easily becomes your code.

Consider what a typical workflow pulls in on every run. Third-party pipeline steps, often referenced by a friendly moving tag rather than a fixed revision. A base image. Your dependency tree, which for a typical service is hundreds of packages you never chose directly. Any of those can change between one run and the next without a single line of your code changing, and any of them executes with whatever access that job has.

Four practices address most of this, and they are cheap.

Pin third-party pipeline steps to an exact immutable revision rather than a moving version tag. A moving tag means the maintainer, or anybody who compromises the maintainer's account, can change what runs in your pipeline tomorrow. Pinning to a fixed revision means an update is a reviewed change in your repository. Yes, this means you must update them deliberately; that is the point.

Install dependencies from a lock file, with the installation mode that refuses to resolve anything not already pinned. A build that silently accepts a new patch version of a transitive dependency is a build whose output you cannot reproduce.

Produce a record of what went into each artifact: the dependency list with versions, the base image identity, and the source revision. This is often called a software bill of materials, and its value becomes obvious the first time a widely publicized vulnerability appears in a common library and somebody senior asks, within the hour, whether you are affected. With that record you answer in minutes. Without it you spend a day.

Scan dependencies for known vulnerabilities as part of the pipeline, and decide in advance what severity blocks a merge versus what raises a ticket. Be realistic: a policy that blocks on every advisory will be disabled within a fortnight. A policy that blocks on critical and high severity issues in code paths you actually ship tends to survive.

I want to connect this to the customer conversation, because it is one of the places where doing the work pays off visibly. Enterprise security questionnaires routinely ask how you manage third-party components, whether you can produce a component inventory, and how quickly you can respond to a disclosed vulnerability. If your pipeline already produces the inventory and already scans, those answers take one paragraph and a sample attachment. If it does not, those questions become a project, usually at the worst moment, usually right before a launch date somebody already promised.

One more field-specific note, on runners. The hosted runners provided by your platform live on the public internet. If your customer's environment is private, requires network-level allowlisting, or forbids outbound connections from their systems, a hosted runner cannot reach the deployment target. The answer is a self-hosted runner inside their network. It is a perfectly normal arrangement, and it comes with a responsibility: a self-hosted runner executes code from your repository inside the customer's network, so it must not run untrusted proposed changes, it should be ephemeral, and it should have a narrowly scoped identity. Raise this early in a deployment conversation, because discovering it late can delay a launch by weeks while network access is negotiated.

Let me step back and address what you are actually verifying, because a pipeline is only as good as the checks inside it, and FieldOps Copilot now has an unusual mix of things to check.

At the base are unit tests over pure logic: the priority rule, the contract validation, the normalization mapping, the retry classification, the state transitions in the agent's workflow. These are fast, deterministic, and numerous, and they should form the bulk of what runs. Every one of them is a test you can run ten thousand times for free.

Above those are integration tests that cross a real boundary. Your service against a real PostgreSQL instance, exercising transactions, constraints, and the idempotency key from chapter thirteen. Your pipeline stages against a real database and a real synthetic source file. These need infrastructure in the pipeline, which every major platform supports by running dependent services alongside the job. They are slower, so you want fewer of them, and they catch a different class of bug entirely: the ones where each unit is correct and the composition is not.

Then contract tests at the interface boundary. The workspace expects certain response shapes; your published interface contract from chapter twelve declares them. A test that validates real responses against that contract is worth more than a dozen assertions about individual fields, because it fails when the contract and the implementation diverge, which is the failure that breaks the customer's integration.

Then the authorization tests, which I want treated as a category of their own rather than as ordinary service tests. Unauthenticated, wrong role, correct role, malformed input, and cross-tenant access attempts. These are the tests a security reviewer will ask about by name, and they are the ones most likely to be quietly weakened during a refactor, because making authorization more permissive always makes something else easier.

Then the AI behavior checks against the fake, which I described earlier, plus the pipeline's own data quality tests from chapter twenty-four: idempotency, quarantine behavior, batch abort, and schema drift tolerance.

And finally, a very small number of end-to-end tests that drive the whole system through one realistic path. These are slow and the most likely to be flaky, so keep them few and make them count: one incident submitted through the interface, persisted, enriched, proposed, approved, and audited. If that single test passes, a great many things are true at once.

The thing I want you to take from this list is the shape of it. Many fast tests, fewer slow ones, a small number of whole-system ones, and a deliberate category for the things a customer's reviewer cares about. A pipeline whose distribution is inverted, with a handful of unit tests and a large suite of slow end-to-end tests, will be slow and flaky, and a slow flaky pipeline is one that gets bypassed.

Now the pitfalls.

The first is the gate that is not required. A check that runs and reports but does not block is decoration. Turn on the required-check enforcement.

The second is building twice. I have said it three times because it is the most common structural mistake in a pipeline.

The third is secrets available to untrusted code paths.

The fourth is a flaky gate nobody trusts. Fix the flakiness or downgrade the check to advisory, but do not leave a required check that people routinely re-run to get past.

The fifth is a pipeline that only runs on the main line. If verification happens after merge, you have made the shared line of development the place where breakage is discovered.

The sixth is the twenty-five-minute pipeline. Above roughly ten minutes, people stop waiting and start context switching, and the feedback loop that justifies the whole apparatus disappears. Parallelize, cache honestly, and move slow things to tier two.

The seventh is hard-coded configuration. Environment-specific values belong in environment configuration, and the artifact should be identical across environments. If your build produces different bytes for pilot and production, you cannot promote, you can only rebuild and hope.

The eighth is a deployment identity with broad permissions, usually granted during a frustrating debugging session and never narrowed afterwards.

The ninth is having no rollback path in the pipeline.

The tenth is pipeline definitions that are not reviewed like code. A change to the workflow file can disable a check, add a secret to an untrusted context, or alter the artifact. It deserves the same scrutiny as a change to the authorization logic, and in some ways more.

Now verification. Here is what you should be able to demonstrate at the end of the practice test.

A fresh checkout, on a clean machine, running the tier-one checks with one documented command and producing the same result as the pipeline.

A proposed change with a failing unit test being blocked from merging.

A proposed change that deliberately breaks a safety property, such as allowing a write action, being caught by the evaluation suite against the fake, with no credentials involved.

A proposed change that attempts to print a secret producing nothing useful, because no secret was present in that context.

A single artifact identifier flowing from build through tier two through deployment, provably the same artifact at each step.

A promotion attempt without the required evaluation evidence being refused by the environment protection rule.

A deployment of a previous artifact identifier as a rollback, using the same job.

And a timing figure for tier one, with a stated target, because a pipeline's speed is a feature.

Your practice handoff is the test in the companion guide. Define the stages, implement the tiered workflow, keep secrets out of untrusted contexts, produce and retain a versioned artifact with its evidence, wire the evaluation gate into required checks, add environment approval for promotion, demonstrate that a failing safety check blocks deployment, and show a rollback through the pipeline.

To recap. Continuous integration moves verification from your memory into the system, and continuous delivery makes release a decision rather than a procedure. Build the artifact once and deploy that exact artifact everywhere. Tier your verification: fast, secret-free, deterministic checks on every proposed change using the fake model implementation; credentialed quality, latency, and cost measurement after merge; and the full release gate before promotion. Assert properties rather than exact outputs so the gate is stable. Keep secrets away from untrusted code, prefer short-lived credentials over stored keys, and give the pipeline the narrowest identity that can do its job. Make required checks actually required, keep the fast tier fast, and make rollback an ordinary pipeline operation. And remember that in the field, the pipeline is the executable form of your deployment knowledge, which is what makes the system survivable after you leave.

Next chapter we package the service itself: images, layers, non-root runtimes, health checks, and the difference between an image that builds and a workload you would be willing to run inside a customer's network.
