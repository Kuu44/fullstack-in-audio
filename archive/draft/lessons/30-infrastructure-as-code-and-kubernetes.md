---
chapter: 30
title: "Infrastructure as code and Kubernetes"
slug: 30-infrastructure-as-code-and-kubernetes
part: "Part VI — Ship and protect the production-shaped system"
roadmap_nodes: ["Terraform", "Kubernetes"]
voice: en-US-AndrewNeural
rate: "-18%"
audio: media/30-infrastructure-as-code-and-kubernetes.mp3
companion_guide: docs/guides/30-infrastructure-as-code-and-kubernetes.md
---

# Chapter 30 — Infrastructure as code and Kubernetes

> Narration script. Headings, frontmatter, and blockquotes are stripped before rendering; only the prose below is spoken.

Welcome to chapter thirty. Last chapter you designed a landing zone: a network, a container service, a private database, secrets, storage, a registry, a job runner, observability, and four separated identities. It exists as a diagram and a decision record. Today we make it exist as something a machine can build, a reviewer can read, and a successor can rebuild from nothing.

And then, in the second half, we confront the question this chapter is really about. Should your customer's pilot run on Kubernetes? I am going to give you a genuine framework for that rather than an answer, because the honest answer depends on facts about the customer, and because the two most common failures are equal and opposite. One team adopts a cluster for a system that could have run on a managed container service, and spends the pilot operating infrastructure instead of delivering outcomes. Another team refuses a cluster at a customer who already runs several, and produces a deployment their platform team cannot support. Both mistakes come from having a preference instead of a framework.

Let us start with infrastructure as code.

The idea is that your infrastructure is defined in files, kept in version control, reviewed like application code, and applied by a tool rather than by a human clicking through a console. The immediate benefits are obvious: repeatability, reviewability, and a written record of what exists. The deeper benefit takes longer to appreciate, and it is this: infrastructure as code turns infrastructure changes into a conversation that happens before the change, rather than an archaeology exercise afterwards.

Terraform is the tool we will use as our reference, because it works across providers and because it is the one you are most likely to find already in use at a customer. The concepts, though, transfer to every tool in this category.

The first concept is declarative desired state. You do not write instructions that create things. You write a description of what should exist, and the tool works out what actions are needed to make reality match. This is a genuinely different mental model from scripting, and it has a specific consequence: running it twice does nothing the second time, because reality already matches. That is idempotency again, the same property we demanded of your ingestion pipeline, now applied to infrastructure.

The second concept is state, and it is the one that causes the most operational grief, so let us be careful. The tool keeps a record of what it has created and how that maps to your configuration. It needs this because it must be able to tell the difference between something that does not exist yet and something that exists and needs modifying. That state file is therefore critical infrastructure in its own right. Three rules follow. It must be stored remotely and shared, not on somebody's laptop, or two engineers will produce conflicting realities. It must support locking, so two simultaneous applies cannot corrupt it. And it must be treated as sensitive, because it often contains resource identifiers and sometimes secret values, which means it needs encryption and access control like any other sensitive store.

The third concept is the plan, and this is the practice I want you to adopt most firmly. Before applying anything, the tool can compute and show you exactly what it intends to do: what will be created, what will be changed, and what will be destroyed. Reviewing that plan before applying is the single highest-value habit in this discipline. It is also the moment when you catch the change that would have replaced your database.

Let me dwell on that, because it is the specific danger. Some changes to a resource can be made in place. Others cannot, and the tool's only way to achieve your desired state is to destroy the existing resource and create a new one. For a load balancer that is an outage. For a database that is data loss. The plan tells you this in advance, in plain terms, and the discipline is to read it rather than scroll past it. Add a protection setting on your stateful resources so that destruction requires a deliberate override, and make plan review a required step for any change to a production-like environment.

The fourth concept is modules, which are reusable, parameterized groupings of resources. A module for your network, a module for the service, a module for the database. The value in field work is specific: a module lets you deploy the same shape into pilot and production, differing only by input values. That is the infrastructure equivalent of the build-once principle, and it is what makes environments genuinely comparable rather than merely similarly named.

Which brings to the fifth concept: separating definitions from environment values. The module says what a service looks like. The environment configuration says that pilot uses small instances, one zone for the database standby, a short log retention, and a particular network range, while production uses larger instances and longer retention. If those values are embedded in the module, you have two copies of your infrastructure that will drift apart. Keep them separate from the first day, because retrofitting it later is tedious.

The sixth concept is drift, which here means reality diverging from your definitions because somebody changed something by hand. It happens, usually during an incident, usually for a good reason. The problem is not that it happens; it is that it happens silently, and then the next apply either reverts the emergency fix or fails confusingly. Detect it by running a plan on a schedule and alerting when it is not empty. Then adopt a rule: an emergency manual change is acceptable, and it comes with an obligation to reconcile the definitions within an agreed window.

The seventh concept is secrets, and the rule is short. Secrets do not go in infrastructure definitions, because those are in version control. Create the secret container in code, populate its value out of band, and have the workload read it at runtime using its workload identity. Be aware that secret values referenced during an apply may be recorded in state, which is another reason state is sensitive.

The eighth concept is policy as code, which is automated checking of infrastructure definitions against rules before they are applied. Rules such as: no storage bucket may be public, every resource must carry the pilot's tags, no database may have a public endpoint, encryption must be enabled. This is the mechanism that turns your chapter twenty-nine design decisions into guarantees rather than intentions, and it is remarkably effective, because it catches the mistake in the plan stage rather than in a quarterly audit.

Let me make the module boundaries concrete for FieldOps Copilot, because deciding where to draw them is most of the design work and it is easy to get wrong in both directions.

A network module owns the private network boundary, the public and private subnets across two availability zones, the routing, and the private connectivity endpoints to managed services. It changes rarely and almost everything depends on it, so it gets its own unit with its own state.

An identity module owns the four identities from last chapter and their permission bindings. I would keep this separate from the workloads that use it, because permission changes deserve their own review and because a service redeployment should never be able to widen a permission by accident.

A data module owns the managed PostgreSQL instance, its subnet placement, its backup configuration and retention, its encryption settings, and its deletion protection. It is the most dangerous resource you manage, which argues for keeping it in its own unit so that routine changes elsewhere never generate a plan that touches it.

A platform module owns the pieces the application needs but does not change often: the image registry, the object storage buckets with their access policies and lifecycle rules, the secret containers, and the observability collection configuration with its retention.

And a service module owns the actual runtime: the container service definition, its scaling configuration, the load balancer and its certificate, the health check settings, and the scheduled job for the ingestion pipeline. This is the one that changes weekly.

The inputs and outputs between them are the interesting part. The network module outputs subnet identifiers. The identity module outputs identity references. The data module outputs a connection endpoint, and importantly not a password, which lives in the secret manager. The service module takes all of those as inputs. That dependency direction is deliberate and it is the same architectural instinct from chapter six applied to infrastructure: the frequently changing thing depends on the stable thing, never the reverse.

Now the two failure modes. Too few modules gives you one monolith where a service change plans against your database. Too many gives you a web of cross-unit dependencies where deploying anything requires applying five units in a specific order that exists only in your head. Five units for a pilot of this size is about right, and the test is simple: a routine service change should produce a small plan touching only the service, and a person should be able to state the apply order in one sentence.

One more consideration worth building in now: how an environment gets bootstrapped. Your state needs somewhere to live, which is itself infrastructure, which creates a small chicken-and-egg problem. The usual resolution is a tiny bootstrap step that creates the state storage and its locking mechanism, performed once per account and documented as a manual exception. Write that down rather than leaving it as tribal knowledge, because it is the very first thing a successor will hit when rebuilding from nothing.

Let me tell you about the plan you did not read, because every infrastructure engineer has a version of this story and I would rather you borrow mine.

A team needs to change a setting on their pilot database: a parameter group, a maintenance window, a minor version, something that sounds innocuous. They update the definition, run the tool, and it asks for confirmation. The output is ninety lines long. They have seen ninety-line outputs many times. They confirm.

Buried in the middle, in the tool's standard notation, was a line indicating that the resource would be destroyed and recreated, because the attribute they changed is one that cannot be modified in place for that resource type. The database is deleted. A new, empty one is created in its place, correctly configured, with none of the data.

Now, how bad this is depends entirely on preparation. If automated backups are enabled with a recent snapshot, this is an unpleasant hour and some data loss measured in minutes. If it is a pilot with synthetic data, it is embarrassing and educational. If it is production, with real customer incident history, and the backup retention was never configured because it was on the list of things to do after launch, it is the kind of event that ends engagements.

Three cheap controls prevent it entirely, and I want them to be reflexes. First, read the plan, specifically looking for anything that will be replaced rather than updated; most tools mark this distinctly and you can search for it. Second, put a deletion protection setting on every stateful resource, so that even a confirmed apply refuses, and removing that protection is its own reviewed change. Third, make the plan a reviewed artifact for any production-like environment: generate it in the pipeline, attach it to the change, and have a second person look at it. That third one feels bureaucratic in a two-person team and it is exactly what a customer's change process will require anyway, so you may as well adopt it early and get the benefit.

There is a broader point here about the nature of declarative tools. They are enormously powerful precisely because they will do whatever is necessary to reach the state you described. That power has no opinion about whether the necessary action is acceptable to you. The plan is where you supply that opinion, and skipping it is not a time saving, it is delegating a judgement you were supposed to make.

Now, why does this matter especially in field work?

The first reason is the one the chapter's done-when criterion names: recreating the pilot must not require clicking through undocumented console steps. At some point somebody will need to rebuild this environment. Maybe the pilot succeeds and moves to a production account. Maybe a region changes. Maybe somebody deletes something. If rebuilding requires you and two days of memory, the deployment is fragile in a way no test will reveal.

The second reason is review. A customer's platform team will want to see what you intend to create in their account before you create it. A plan output is exactly that artifact, and offering it unprompted changes the tenor of the relationship. It says you expect scrutiny rather than fearing it.

The third reason is teardown. Nonproduction environments are the largest source of unexplained cloud spend in most organizations. When your infrastructure is declared, destroying a rehearsal environment is one operation and is complete. When it was created by hand, teardown is a scavenger hunt, and the things you miss bill monthly forever.

The fourth reason is the handover, again. Infrastructure code is documentation that cannot go stale, because if it were wrong the environment would not exist.

Before we leave infrastructure code, let us talk about how it actually flows through a team, because the workflow matters as much as the syntax.

Organize the repository by lifecycle rather than by technology. One area holds shared modules: network, service, database, identity. Another holds environment configurations, one per environment, each composing those modules with its own values. And separate the pieces whose change frequency differs wildly. Your network, your identities, and your database are foundational; they change rarely and a mistake in them is expensive. Your service definition changes often. Putting them in the same unit means every routine service change generates a plan that touches foundations, which trains people to skim plans, which brings us back to the previous story.

Then wire it into the pipeline from chapter twenty-seven, with the same trust model. On a proposed change, run validation, formatting, a policy check, and a plan against the pilot environment, and publish the plan output where reviewers can read it. Note that generating a plan requires read access to the environment, so this job needs credentials, which means it must follow the untrusted-code rules we established: either the repository is trusted, or the plan runs only after review. On merge, apply to pilot automatically if you are comfortable. For production-like environments, require an explicit approval, exactly as with application promotion.

A note on who applies. There is a real temptation for each engineer to apply from their own machine, because it is faster. Resist it for anything shared. When applies happen from laptops, you get partial applies from interrupted sessions, applies from stale branches, and an audit trail that consists of people's memories. Applying from the pipeline gives you a log of who requested what, when, against which commit, with what plan.

And a note on the first apply into a customer's account, which is a moment worth treating carefully. Do it with their platform team present or at least informed, with the plan shared in advance, in a nonproduction context, and with an agreed teardown. You are asking for standing credentials in someone else's cloud; behaving as though that is a privilege rather than a given is how you keep it.

Now let us turn to the Kubernetes question.

First, what Kubernetes actually is, stated plainly. It is a system for running containers across a pool of machines, where you declare what should be running and the system continuously works to make that true. You say you want three copies of this container, reachable under this name, with these resources, and Kubernetes places them, restarts them when they die, replaces them when a machine fails, and updates them when you change the declaration.

The core objects are few, and you should know them. A Pod is one or more containers scheduled together, and it is the unit that gets placed on a machine. A Deployment declares how many copies of a Pod should exist and manages rolling updates between versions. A Service gives a stable name and address for reaching a set of Pods, since individual Pods come and go. An Ingress or gateway routes external traffic in. ConfigMaps hold non-secret configuration and Secrets hold sensitive configuration, both injected into Pods as environment values or mounted files. And namespaces divide a cluster into logical partitions.

For your deployment, the mapping is straightforward. The API becomes a Deployment with a few replicas and a Service in front of it. The health checks you built last chapter become the readiness and liveness probes, which is a nice confirmation that we did that work in the right order. Resource requests and limits express what each Pod needs and what it may not exceed. The ingestion job becomes a scheduled job object. Configuration comes from a ConfigMap, and secrets from the cluster's secret mechanism, ideally backed by the cloud's secret manager rather than stored in the cluster.

Two Kubernetes details deserve emphasis because they are where people get hurt.

The first is resource requests and limits. A request is what the scheduler reserves for your Pod, and it determines where your Pod can be placed. A limit is the ceiling it may not exceed. Set them deliberately. Omitting requests means the scheduler has no idea what your workload needs and will happily overcommit a machine. Setting a memory limit too low means your process is terminated abruptly under load, which appears as a mysterious restart. Setting processor limits too aggressively causes throttling, which appears as inexplicable latency. These are among the most common causes of confusing Kubernetes behavior, and they are configuration, not bugs.

The second is that rolling updates interact with your application's shutdown behavior. Kubernetes stops sending traffic to a Pod and signals it to terminate, then waits a grace period before killing it. If your application ignores that signal, every deployment drops in-flight requests. We covered this in chapter twenty-eight, and this is where it pays off.

A third detail, which matters in a customer environment more than in a personal project: access control inside the cluster is a separate system from access control in the cloud. Your cloud identity policies govern who can talk to the cluster's management interface. Once inside, a different permission system governs what they can do to workloads, namespaces, and secrets. These two must be deliberately mapped to each other, and if they are not, you commonly end up with a situation where a person's cloud permissions are carefully scoped and their in-cluster permissions are effectively unlimited, which makes all that careful scoping decorative. When you inherit a customer's cluster, ask how that mapping works before you assume your identity separation from chapter twenty-nine survives inside it.

Related: secrets in a cluster are, by default, less protected than people assume. They are namespaced and access-controlled, but in a basic configuration they are stored encoded rather than strongly encrypted, and anyone who can read them in a namespace can read all of them. The better pattern is to have the cluster pull secrets from the cloud's secret manager using a workload identity, so the cluster holds a reference rather than the value. If you are deploying into a customer's existing cluster, ask which pattern they use; it is a question that marks you as someone who has done this before.

And a word on packaging. Raw manifests are fine for a handful of objects, and they become unwieldy once you have several environments, because you end up with near-duplicate files that drift. The two common answers are a templating system, where you define a chart with parameters and render it per environment, or an overlay system, where you define a base and patch it per environment. Both work. The templating approach is more widely used and gives you packaging and release semantics; the overlay approach keeps the base readable as plain manifests. What matters for your purposes is the same principle as before: one definition, environment values injected, no copy-paste duplication. Pick either, and say why.

Now the decision. When is Kubernetes right?

It is right when the customer already runs it. If their platform team operates clusters, has established patterns, has monitoring and access control wired in, and knows how to debug it, then deploying your workload as a Deployment in their cluster is the path of least resistance and the best handover outcome. You inherit their operational maturity. This is, in my experience, the most common good reason.

It is right when you genuinely need what it provides: many services with complex interdependencies, sophisticated scaling behavior, node-level control, or portability across environments including a customer's own datacenter. That last one is real: if you must deploy to a cloud for one customer and to on-premises hardware for another, Kubernetes is one of the few substrates that plausibly spans both.

It is right when a mature ecosystem component solves a real problem for you, and the customer already runs the cluster to host it.

And when is it wrong? When it is your pilot's only workload, when nobody at the customer operates clusters, when a managed container service meets the requirement, and when adopting it means you spend delivery time on cluster concerns instead of customer outcomes.

Let me be concrete about the cost of ownership, because it is systematically underestimated. Even with a managed control plane, you own: node pools and their sizing, node operating system updates, cluster version upgrades on the provider's schedule which is not negotiable, the networking plugin and its behavior, ingress controllers and their certificates, in-cluster access control which is a separate system from your cloud's access control and must be mapped to it, resource quotas, and the accumulated configuration of whatever add-ons you install. Each is manageable. Together they are a part-time job, and in a pilot with one service, that job has no payoff.

There is also a subtler cost that I want to name because it is rarely discussed: cognitive load during incidents. When something is wrong in a managed container service, there are perhaps four places to look. When something is wrong in a Kubernetes cluster, there are twenty, and the failure can be in scheduling, networking, storage, admission control, resource pressure, or the application. During a customer incident, with people watching, that difference is substantial.

So here is my recommended posture for the FieldOps pilot. Default to a managed container service. Express the infrastructure in Terraform so that the deployment target is a module boundary rather than a hard assumption. Then, and this is the part I want you to actually do, package the API as a Kubernetes Deployment and Service as well, and run it in a local or small managed cluster once. Two reasons. You will genuinely understand the objects rather than having opinions about them. And you will have a working answer for the customer whose platform team says everything runs in our cluster, which is a sentence you will hear.

Then write the decision down with its burden stated. Something like: the pilot runs on a managed container service because it is a single service with no cluster-scale requirements and the customer's team does not currently operate Kubernetes; a Kubernetes packaging exists and has been validated; we would move if the deployment grows past a stated number of services, or if the customer's platform standard requires it. That is a decision a reviewer can accept or challenge on its merits.

Now the pitfalls.

The first is local state. The moment a second person is involved, local state produces conflicting realities.

The second is applying without reading the plan, which is how databases get replaced.

The third is no protection on stateful resources.

The fourth is secrets in infrastructure definitions or, equivalently, in the repository.

The fifth is one enormous configuration for everything, where a small change to a service requires a plan that touches the network and the database. Split by lifecycle: things that rarely change, like networking, should not be in the same blast radius as things that change weekly.

The sixth is unmanaged drift, where manual changes accumulate until the definitions are fiction.

The seventh is environment values baked into modules.

The eighth is adopting Kubernetes without pricing its ownership.

The ninth is Kubernetes workloads without resource requests and limits.

The tenth is a rehearsal environment that is never destroyed.

And the eleventh, which is specific to field work: applying infrastructure changes in a customer's account without their change process. Even if you have the access, using it outside their process is how you lose trust permanently. Ask what their process is, and follow it even when it is slower than you would like.

Now verification. Here is what you should be able to demonstrate.

Destroy a nonproduction environment completely and rebuild it from definitions alone, with no console steps, and confirm the application works afterwards.

Produce a plan for a change and explain every line of it, including anything that would be replaced rather than modified.

Attempt a change that would destroy the database and show the protection preventing it.

Show that pilot and production-like environments use the same modules with different input values.

Show a secret existing in the secret manager without its value appearing in any definition, in version control, or in the plan output.

Introduce a manual change out of band and show your drift detection reporting it.

Run a policy check that rejects a definition violating one of your chapter twenty-nine rules, such as a public database.

Deploy the API to a cluster with resource requests and limits and working readiness and liveness probes, then perform a rolling update with no dropped requests.

Show the state file stored remotely, locked during an operation, and access-controlled.

And present the deployment target decision with its operational burden and a named alternative.

Your practice handoff is the test in the guide. Write the modules for network, service identity, database, and container runtime. Separate environment values. Package the API for Kubernetes or justify the managed alternative, with probes and resource specifications either way. Review the plan before applying. And destroy the rehearsal environment when you are done, which is both good hygiene and a test of whether your definitions are complete.

To recap. Infrastructure as code makes your environment repeatable, reviewable, and rebuildable, and its most valuable habit is reading the plan before applying it. State is critical infrastructure: remote, locked, encrypted, access-controlled. Modules plus separate environment values give you comparable environments instead of similarly named ones. Keep secrets out of definitions, detect drift on a schedule, and enforce your design rules with policy checks so that decisions become guarantees. On Kubernetes: know the objects, map your health checks to probes, always set resource requests and limits, and choose the platform on customer fit rather than preference. Default to the simpler managed runtime for a single-service pilot, validate a Kubernetes packaging so you are ready when a platform team asks, and write the decision down with its operational burden and its trigger for change. And destroy what you were only rehearsing with, because an undeclared, unattended environment is a bill and a liability at the same time.

Next chapter we make the running system legible: logs, metrics, traces, correlation across the whole path from a click to a model response, and the observability signals specific to artificial intelligence behavior that let you answer the question a customer will eventually ask, which is why did it say that.
