---
chapter: 29
title: "Cloud platforms and provider selection"
slug: 29-cloud-platforms-and-provider-selection
part: "Part VI — Ship and protect the production-shaped system"
roadmap_nodes: ["Cloud Platforms", "AWS", "Azure", "GCP"]
voice: en-US-AndrewNeural
rate: "-18%"
audio: media/29-cloud-platforms-and-provider-selection.mp3
companion_guide: docs/guides/29-cloud-platforms-and-provider-selection.md
---

# Chapter 29 — Cloud platforms and provider selection

> Narration script. Headings, frontmatter, and blockquotes are stripped before rendering; only the prose below is spoken.

Welcome to chapter twenty-nine. You have an image, and you have a pipeline that builds it and would very much like to deploy it somewhere. Today we decide where somewhere is.

I want to set expectations about what this chapter is and is not. It is not a tour of three cloud providers' service catalogues. Those catalogues contain hundreds of services each, they change every quarter, and memorizing them is not a skill. What I am going to give you instead is a way of thinking that survives the catalogue changing: the small number of dimensions that actually differ between providers, the components every deployment needs regardless of provider, and a decision process that produces an answer you can defend to a customer's architecture review board.

And I want to start with the thing that makes this chapter different from the equivalent chapter in a product engineering course. In a product company, you choose your cloud once, probably years before you arrived, and everything afterwards is an implementation detail. In forward deployed work, the cloud is frequently chosen for you, by a customer, for reasons that have nothing to do with technology, and your job is to deploy well inside that choice.

Let me say that more strongly, because it is the central judgement of this chapter. The most common mistake I see is an engineer treating cloud selection as a technical comparison. They build a feature matrix, they conclude that one provider has a slightly better managed database or a more mature model service, and they recommend it. Then they discover that the customer has a seven-figure committed spend agreement with a different provider, that their identity system is already federated to that provider, that their security team has written and approved landing zone patterns for that provider and none for any other, and that procurement for a new vendor takes four months. The technical comparison was not wrong. It was irrelevant.

So the first thing I want to install is this: cloud selection is a constraint-satisfaction problem before it is an optimization problem. Find the eliminating constraints first. Then optimize within what remains.

Now let us build the vocabulary, organized around what your deployment actually needs rather than around any provider's marketing.

Start with compute, which is where your container runs. There is a spectrum here, and understanding it is more valuable than knowing the product names.

At one end is a virtual machine. You get an operating system and you are responsible for everything above it: patching, configuring a container runtime, restarting things when they die. Maximum control, maximum operational burden. For a pilot this is usually the wrong choice unless the customer's constraints force it, and sometimes they do.

Next is a managed container service where you supply a container image and the platform runs it, handles scaling and restarts, and you never see the underlying machines. This is what I would recommend for the great majority of pilots. Every major cloud has at least one of these, they cost very little at low volume, they are quick to deploy to, and they hand almost all the operational burden to the provider. The tradeoff is less control over networking details and startup behavior, and a scaling model you must work within rather than configure freely.

Next is a managed Kubernetes service, where the provider runs the cluster control plane and you run workloads on it. This is a large step up in capability and in obligation, and it is the subject of the next chapter, so I will not pre-empt it beyond saying: it is rarely the right first choice for a pilot, and it is frequently the right choice when the customer already runs one.

And at the far end are functions, where you supply code rather than a container and the platform runs it per request. Excellent for event handlers, such as the trigger that starts your ingestion job. Awkward for a long-lived service with model calls that take many seconds, because of execution duration limits and cold starts.

For FieldOps Copilot, a sensible default shape is a managed container service for the API, the same or a scheduled job runner for the ingestion pipeline, and static hosting with a content delivery network for the interface if you separated it.

Second component: networking. Three concepts matter and the rest is detail.

The first is the private network boundary, which every provider offers under a different name, and which is the virtual network your resources live in, subdivided into subnets, some reachable from the internet and some not. The rule for your deployment is simple: the database goes in a subnet with no route to the internet, and the service goes somewhere it can be reached by users but cannot be reached on its administrative interfaces.

The second is private connectivity to managed services. When your service talks to the managed database or a secret store, that traffic can traverse the provider's public endpoints or stay entirely within the private network. Enterprise security teams care about this a great deal, and the private option is usually available and usually worth taking. Expect to be asked.

The third is egress control, meaning what your workload is permitted to connect out to. This is the one that most often surprises people building AI systems, because your service needs to reach a model provider, which is an outbound connection to the public internet from inside a customer's controlled environment. Some customers forbid that outright, which is one of the strongest arguments for a model service inside their own cloud, exactly as we discussed in chapter twenty-six. Others permit it through a proxy with an allowlist. Find out early, because the answer can change your architecture.

Third component: identity, and this is the one I want you to take most seriously, because it is where the most damaging mistakes are made and where good practice is most visible to a customer.

Every cloud has a system for defining who can do what. The concepts are consistent even though the names differ. You have identities, which can be humans or workloads. You have permissions, grouped into roles. And you have policies that bind roles to identities, often scoped to particular resources.

Two ideas carry most of the value. The first is workload identity: your running service should have its own identity granted by the platform, not a stored key. When the service needs to read a secret or write to storage, it proves who it is by virtue of where it is running. No credential file, nothing to leak, nothing to rotate. This is the same principle as the short-lived pipeline credentials from chapter twenty-seven, and it is available in every major cloud.

The second is separation of identities by purpose. Your deployment automation needs one identity. Your running service needs a different one. Human operators need a third. And you need a break-glass path for emergency administrative access. These must not be the same thing, and the reason is not theoretical. If the deployment identity can also read the production database, then a compromised pipeline is a data breach rather than a deployment incident. If the service identity can modify infrastructure, then an application vulnerability becomes an infrastructure takeover.

Let me define break-glass properly, because people nod at the term without implementing it. Break-glass is a highly privileged access path that is normally unused, that requires deliberate action to invoke, that is loudly logged and alerts somebody when used, and that is reviewed after every use. It exists because emergencies happen and because the alternative is that somebody keeps administrative privileges permanently just in case. A well-designed break-glass path lets you take those permanent privileges away, which is the actual benefit.

Fourth component: managed data services. Your PostgreSQL database should be a managed service rather than a database you install on a machine. You get backups, patching, failover, and encryption without operating any of it. The things to decide are backup retention, whether you need a standby in another availability zone, and where backups are stored, because backup location is a data residency question and is easy to overlook.

Also in this category: a secret manager for credentials, object storage for artifacts and raw pipeline data, and a managed cache if you kept the one from chapter fourteen.

Fifth component: regions and availability zones. A region is a geographic location. An availability zone is an isolated datacenter within a region. Spreading across zones protects you from a single datacenter failure and is usually cheap. Spreading across regions protects you from a regional failure, costs substantially more, and adds latency and complexity. For a pilot, multiple zones in one region is almost always the right answer, and you should say so explicitly rather than leaving it unstated.

Region choice is more consequential than it looks, and for a customer it is often a legal question rather than a performance one. Data residency requirements may mandate that customer data never leaves a jurisdiction. Note that this applies to every place data lands: the database, the backups, the logs, the object storage, and, critically, the model provider's inference endpoint. It is entirely possible to deploy a compliant application that quietly violates residency because its logs ship to a different region by default.

Sixth: support and operations model. Enterprise customers buy support tiers with response-time commitments, and the tier they have is the tier you get during an incident. Worth knowing before you need it. Also worth knowing: who in the customer's organization can open a support case with the provider, because it may not be you.

Seventh: billing. Cloud billing is its own discipline, and for a pilot you need three things. You need to know the major cost drivers, you need spending alerts configured from day one, and you need resource tagging so costs can be attributed to the pilot rather than disappearing into a general account. That third one is unglamorous and it is what lets you answer the question that arrives at the end of every pilot: what did this actually cost?

Before we compare providers, there is one concept that underpins every conversation you will have with a customer's security team, and it is worth stating explicitly because engineers routinely get it half right. It is the shared responsibility model.

The provider is responsible for the security of the cloud: the physical datacenters, the hardware, the hypervisor, the managed service software, and the availability of the platform. You are responsible for security in the cloud: your network configuration, your identity and access policies, your data classification and encryption choices, your application, your images, your secrets, and who you granted access to.

The line moves depending on which service you use, and that movement is the part people miss. On a virtual machine, operating system patching is yours. On a managed container service, it is theirs, but your image contents are still yours. On a managed database, patching and backups are theirs, but who can reach the database and what data you put in it are yours. The general pattern is that the more managed the service, the more of the operational burden shifts to the provider, and the more the remaining risk concentrates in configuration and access.

That concentration is the important insight. When people talk about cloud breaches, the overwhelming majority are not provider failures. They are misconfigurations: storage left publicly readable, an over-permissive identity, a database exposed to the internet, a credential committed to a repository. Which means that the parts of this chapter that feel administrative, the identity separation and the network placement, are not administrative at all. They are the actual security work, and the provider cannot do them for you regardless of how much you pay.

There is a practical consequence for your delivery. When a customer's security reviewer asks how the system is secured, an answer that describes the provider's certifications is a weak answer, and they will recognize it as one. A strong answer describes your configuration: which identities exist, what each may do, what is reachable from where, where data lives, how secrets are delivered, and what is logged. Those are the things on your side of the line, and they are what the review is actually about.

Now, the three providers. Let me tell you where they genuinely differ, and where they do not.

Where they do not differ meaningfully: all three offer virtual machines, managed containers, managed Kubernetes, functions, managed PostgreSQL, object storage, secret management, private networking, identity and access management, logging, monitoring, and access to capable language models. At the level of what FieldOps Copilot needs, all three can do the job competently. Anybody who tells you a pilot of this shape is impossible on one of them is selling something.

Where they do differ, in ways that matter to a decision:

Identity integration is the big one. If the customer's workforce identity is already managed by a particular vendor's directory service, then that vendor's cloud offers the smoothest path for human access, single sign-on, and conditional access policies. This is frequently the single most influential technical factor, and it is genuinely a technical factor, not just a commercial one.

Existing commercial agreements come next. A committed spend agreement, negotiated discounts, or a marketplace arrangement can make one provider dramatically cheaper and dramatically faster to procure. The speed matters more than the money for a pilot.

Regional coverage differs, and specific services are not available in every region of any provider. If the customer requires a particular jurisdiction, check that the exact services you need exist there. This is a concrete, checkable thing and it occasionally eliminates an option outright.

Sovereignty and government-specific offerings differ, and if your customer is public sector or in a heavily regulated industry, this may be decisive.

Model service maturity and the specific models available differ, and they change constantly. Evaluate this at the time of the decision rather than from memory, and evaluate it against your actual task using your evaluation suite rather than against benchmark claims.

And finally, your customer's existing skills. If their platform team has operated one cloud for eight years, deploying into a different one means they cannot support what you build. That is a real operational risk and it belongs in the matrix.

Notice what is not on that list: which provider has the nicer console, which one you personally know best, and which one has the better documentation. Your preference is not a customer constraint. Your familiarity does matter a little, because a pilot has a schedule, but it should be a tiebreaker rather than a driver, and you should be honest about it when you write it down.

Let me show you how this goes when it is done in the wrong order, because I want the failure mode to be vivid.

A delivery team is three weeks into a pilot. They have built well. They picked a cloud on the first day, based on the fact that two of the three engineers knew it best, which felt like a reasonable schedule-driven decision and was never written down as a decision at all. They have a working deployment, a pipeline, and a demonstration scheduled with the customer's architecture review board.

At that meeting, four things emerge in about twenty minutes. The customer's workforce identity is federated to a different provider, so the operator sign-on the team built will need to be rebuilt. The customer has an approved landing zone pattern, with network topology, logging destinations, and tagging conventions already specified, for that same different provider, and no pattern at all for the one the team chose. Using a new provider requires a vendor security assessment that the security lead estimates at six to ten weeks. And the customer's committed spend agreement means the chosen provider's costs come out of a discretionary budget that requires separate approval, while the other provider's costs do not.

None of those are technical objections. Nobody in the room said the architecture was wrong. And yet the outcome is that several weeks of deployment work must be redone, the pilot's timeline slips past a quarter boundary, and, most damagingly, the team now looks to that review board like people who did not ask basic questions. That last cost is the one that lingers, because the board's job is to assess risk, and they have just been handed evidence.

Here is what the same team would have done with an hour in week one. A short conversation with the customer's platform lead and their security lead, asking the seven questions I am about to list. Written answers. A one-page decision record naming the chosen provider and the constraints that drove it, circulated for comment before any infrastructure existed. The engineering work would have been identical in volume and would have landed in the right place.

I labour this because the skill being tested is not cloud knowledge. It is the habit of finding the constraints before committing effort, and that habit generalizes to every part of forward deployed work.

So let me walk the decision process.

Step one, enumerate constraints and mark which are eliminating. Ask: is there an existing cloud agreement? Is workforce identity already federated somewhere? Is there a data residency requirement, and to which jurisdiction? Is there an approved landing zone pattern? Is there a list of approved services? Can workloads make outbound internet connections? Who operates this after handover, and what do they know? What is the procurement timeline for a new vendor? Any one of those can end the conversation, which is why you ask them before building a matrix.

Step two, build a weighted matrix for whatever survives. Criteria: identity fit, regional and residency fit, approved-service coverage, existing agreement and procurement speed, customer operational skills, model service fit, and estimated cost. Weight them according to the customer's stated priorities, not yours, and have the customer confirm the weights before you score. That last step is what converts your recommendation from an opinion into a shared conclusion, and it is worth a meeting.

Step three, design the landing zone. This is the named set of components your pilot will occupy, and I want you to be able to draw it from memory. A private network with public and private subnets across two availability zones. A managed container service running the API, reachable through a load balancer, with the containers themselves in private subnets. A managed PostgreSQL instance in a private subnet with no public endpoint, with backups and a stated retention. A secret manager holding the model provider credential and the database credential, reached over private connectivity. Object storage for raw pipeline data and retained artifacts. A registry holding your images. A scheduled job runner for the ingestion pipeline. Log and metric collection with a stated retention period and a stated region. And the four identities: deployment, service runtime, operator, and break-glass.

Step four, define the identities concretely. For each, write what it may do and, just as importantly, what it may not. The deployment identity may push images and update the service definition; it may not read the database or read secrets other than those needed to deploy. The service runtime identity may read its own secrets, connect to the database, write logs, and read pipeline objects; it may not modify infrastructure or create identities. The operator identity may read logs and dashboards and perform defined operational actions; it may not read raw incident content if your data classification says otherwise, which is a question chapter thirty-two will make you answer. And break-glass may do anything, is normally disabled, requires a deliberate action, and alerts on use.

Step five, estimate the cost drivers. For a pilot of this shape, the recurring costs are roughly: the container service, which at low volume is small; the managed database, which is often the largest fixed line item because it runs continuously; storage and backups, which are small; networking, where egress charges are the thing people forget; observability, where log ingestion and retention can become surprisingly significant if you log verbosely; and model inference, which is usage-based and which you have already budgeted in chapter twenty-three. Produce a monthly estimate with the assumptions visible, because a number without assumptions is not an estimate, it is a guess with a decimal point.

Let me make the cost estimate concrete, because "produce an estimate" is easy advice and the actual exercise teaches you something.

Take the FieldOps pilot: one small container service running continuously, one small managed PostgreSQL instance with a standby, modest object storage, a registry holding a handful of images, a nightly ingestion job, observability, and a couple of hundred model calls a day.

Go through the lines. The container service at this size is small, and if it scales to zero between requests it can be nearly nothing, though a service with a latency target usually keeps at least one instance warm. The managed database runs twenty-four hours a day regardless of whether anyone files an incident, which makes it typically the largest fixed cost in the whole deployment, and a high-availability standby roughly doubles it. That single fact often surprises people, and it is a useful one to surface early, because a pilot with ten users is paying primarily for a database that is idle most of the time. Storage and the registry are usually trivial. Networking is trivial except for egress, which is charged per gigabyte leaving the provider, and which is small for an application like this but can become significant if you ship verbose logs to an external system. Observability deserves attention precisely because of that: log ingestion and retention are priced per volume, and a service logging every request body at high verbosity can produce an observability bill that exceeds its compute bill. Model inference you have already budgeted, and at a couple of hundred calls a day it is likely modest.

Two lessons come out of that walk-through. The first is that the shape of a pilot's cost is dominated by things that run continuously, not by things that scale with usage, which means the way to reduce it is to remove or downsize idle resources rather than to optimize per-request efficiency. The second is that observability and egress are the two lines that most often surprise people, and both are controllable by decisions you make rather than by volume you cannot influence.

Then add the things people leave out of estimates and regret: backup storage, the cost of a nonproduction environment which is easy to forget and which runs all month, data transfer between zones if you spread across them, and the support tier if the pilot needs one. Finally, state the assumptions beside the number: request volume, retention periods, instance sizes, and whether high availability is included. An estimate whose assumptions are visible can be corrected. One without them gets quoted back to you as a commitment.

Step six, write the portability boundary. Identify the one service that would be hardest to replace if the customer changed cloud, and state what replacing it would involve. For most deployments of this shape the answer is either the managed database, which is portable in principle because PostgreSQL is PostgreSQL but painful in practice because of data movement and downtime, or the identity integration, which is genuinely deeply coupled. Being able to name this honestly is a mark of seniority. Claiming full portability is not credible, and customers who have been through a migration know it.

Now the pitfalls.

The first is optimizing before eliminating. You will waste a week scoring options that were never available.

The second is a single all-powerful identity used by everything, which is the default outcome of debugging permissions under time pressure and never narrowing them afterwards.

The third is a publicly reachable database, which happens more often than anyone would like, usually because it was convenient during setup.

The fourth is forgetting that logs and backups have a location, and therefore a residency implication.

The fifth is no cost alerting, discovered when somebody sees a bill.

The sixth is no resource tagging, which makes the pilot's cost unanswerable.

The seventh is designing for multi-region resilience in a pilot that has not yet proven it is useful. Solve the problem you have.

The eighth is assuming outbound internet access exists.

The ninth is choosing a provider your customer's team cannot operate, which produces a system that works until you leave.

The tenth is treating the customer's approved service list as a suggestion. If a service is not on it, using it means a security exception, which means a process and a delay. Ask first.

And the eleventh is designing a landing zone without talking to the customer's platform team. They have patterns, they have opinions, and they have been burned before. An hour with them early will change your design and save you weeks.

Now verification. Here is what you should be able to demonstrate.

A constraint list that identifies which constraints are eliminating and which are scoring, confirmed with the customer or your proxy for one.

A weighted matrix whose weights were agreed before scoring, producing a recommendation, with the weights and scores visible.

A landing zone diagram naming every component, its network placement, and its data residency.

Four distinct identities with explicit may and may-not statements for each.

Evidence that no workload uses an unlimited identity, ideally by attempting a denied action and showing it refused.

A monthly cost estimate with visible assumptions and a stated alerting threshold.

A statement of where every piece of data lands, including logs, backups, object storage, and the model provider's endpoint, checked against the residency requirement.

A named portability boundary with an honest description of what changing it would cost.

And a decision record that states the chosen provider, the constraints that drove it, the runner-up, and what would cause a reconsideration.

Your practice handoff is the test in the guide. You will create the weighted decision matrix, choose a pilot cloud, draw the landing zone, define the four identities with their limits, estimate the cost drivers, and write the portability boundary. You are not required to spend money. A design with a plan you could execute is the deliverable, and if you do provision anything, provision the smallest possible thing and destroy it when the rehearsal is over.

To recap. Cloud selection in field work is constraint satisfaction before optimization: find the eliminating constraints first, and the most common ones are existing agreements, workforce identity, data residency, approved service lists, egress policy, and who operates it after you leave. All three major providers can run this workload competently, so let the decision turn on fit rather than features. Design a landing zone you can draw: private network across two zones, managed containers, a private managed database, secrets, object storage, a registry, a job runner, and observability with stated retention and region. Separate deployment, runtime, operator, and break-glass identities, and prefer workload identity over stored keys. Estimate cost with visible assumptions, tag everything, and alert on spend from the first day. Know exactly where every byte lands, including logs and backups. And name your portability boundary honestly, because a claim of easy migration that has never been tested will not survive contact with a customer who has attempted one.

Next chapter we make all of this reviewable and rebuildable, with infrastructure as code in Terraform, and we confront the Kubernetes question directly: when a cluster is the right answer for a customer, when it is not, and what owning one actually costs.
