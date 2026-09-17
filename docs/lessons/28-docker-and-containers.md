---
chapter: 28
title: "Docker and containers"
slug: 28-docker-and-containers
part: "Part VI — Ship and protect the production-shaped system"
roadmap_nodes: ["Docker", "Containers"]
voice: en-US-AndrewNeural
rate: "-18%"
audio: media/28-docker-and-containers.mp3
companion_guide: docs/guides/28-docker-and-containers.md
---

# Chapter 28 — Docker and containers

> Narration script. Headings, frontmatter, and blockquotes are stripped before rendering; only the prose below is spoken.

Welcome to chapter twenty-eight. Last chapter your pipeline learned to build an artifact once and deploy that exact artifact everywhere. Today we make the artifact a good one.

Here is the gap we are closing. Right now, "the artifact" is probably a bundle of application files, and running it requires a machine that already has the right runtime version, the right system libraries, the right environment variables, and a database reachable at the right address. That set of requirements exists, but it lives in a readme, in a pipeline configuration, and in your head. When you deploy into a customer's environment, every one of those unwritten assumptions becomes a potential half-day of debugging, usually conducted over a screen share with somebody watching.

A container image closes that gap by packaging the application together with its dependencies and its filesystem, so that the unit you ship is the unit that runs. That is the entire premise, and it is a good one. But I want to be careful here, because containers are surrounded by more confident nonsense than almost any other technology in this course. So we are going to be precise about what a container actually is, we are going to build an image that is genuinely fit to run inside a customer's network rather than one that merely starts, and we are going to talk honestly about the security difference between an image that passes a scan and a workload you would be comfortable deploying.

Let me start with what a container actually is, because the mental model people arrive with is usually a small virtual machine, and that model will mislead you at exactly the wrong moments.

A virtual machine virtualizes hardware. It runs its own kernel, boots its own operating system, and the isolation boundary is enforced by the hypervisor. It is heavy and the boundary is strong.

A container does not do that. A container is just a process, running on the host's kernel, with three kinds of restriction applied to it. First, namespaces, which change what the process can see: its own view of the filesystem, its own process identifiers, its own network interfaces, its own hostname. Second, control groups, which limit what it can consume: memory, processor share, input and output bandwidth. Third, a set of security restrictions that limit what it can do: which privileged operations are permitted, which system calls are allowed.

So a container is a normal process wearing a costume. This has three consequences that matter to you. It starts in milliseconds, because there is no operating system to boot. It shares the host kernel, which means a kernel vulnerability is a shared risk and the isolation boundary is meaningfully weaker than a virtual machine's. And most importantly, the restrictions are configurable, which means the strength of your isolation is a function of how you run the container, not a property you get automatically by using one. That last point is the reason for the security section later in this lesson.

Now, images. An image is the packaged filesystem and metadata that a container is created from. Images are built in layers: each build instruction produces a layer, and layers stack to form the final filesystem. Layers are content-addressed and shared, which is why pulling your second image from the same base is fast, and why a small change to your application does not require transferring the entire operating system again.

Layering has a consequence that catches people out and has real security implications, so let me be explicit. Layers are additive and permanent within an image. If one build step copies a credential file into the image and a later step deletes it, the file is gone from the final filesystem view but the layer containing it is still there, still part of the image, still extractable by anybody who has the image. Deleting a secret in a later layer does not remove it. The only safe approach is never to put it in a layer in the first place.

A registry is where images are stored and distributed. An image is referenced by a name and a tag, and here is a distinction that matters enormously for reproducibility: a tag is a moving label, while a digest is a content hash. If you reference a base image by a version tag, the content behind that tag can change. If you reference it by digest, you get exactly the bytes you tested. For anything you promote through environments, reference by digest. This is the same build-once principle from last chapter, applied one level down.

Next, the build. The single most useful technique in modern image building is the multi-stage build, and the idea is simple. You use one stage to build your application, with all the compilers, development dependencies, and tooling that requires. Then you start a fresh, minimal stage and copy only the finished output into it. The build tools never exist in the final image. The result is often five to ten times smaller and has a dramatically smaller attack surface, because a compiler, a package manager, and a shell full of utilities are all things an attacker would very much like to find waiting for them.

That leads to base image selection, which is a genuine engineering decision rather than a default. A full distribution base gives you a familiar environment, a package manager, and a shell, which makes debugging pleasant and makes the image large and full of software you never use. A slim variant trims the obvious excess. A minimal security-focused base gives you very little beyond the runtime. And a distroless-style base gives you effectively nothing: your application, its runtime, and certificates, with no shell at all.

The tradeoff is real and it cuts both ways. A smaller image has fewer vulnerabilities to report, which matters because your customer will scan it and somebody will read that report. But an image with no shell cannot be debugged by connecting to it and looking around, which is precisely what you want to do at two in the morning during a customer incident. My practical recommendation for a pilot is to use a slim official base for the runtime stage, keep the build tooling in a discarded build stage, and revisit the minimal-base question when the customer's scanning policy actually demands it. What I would push back on is a full distribution image in production, because you will be asked to justify every reported vulnerability in software you are not even using.

There is one more build property worth naming: reproducibility. Two builds of the same source should produce equivalent images. The enemies of this are unpinned dependency resolution, package installs that pull the latest available version at build time, and base images referenced by moving tags. Pin all three. You will care about this the first time an image that worked last week fails to build during a customer deployment window.

Now configuration. The rule is that an image is identical across environments and configuration is injected at run time. Concretely, your image must not contain the database address, the environment name, the provider endpoint, or anything else that differs between development, pilot, and production. Those arrive as environment variables or mounted configuration when the container starts. This is what makes promotion meaningful: the pilot and production containers are the same bytes, differing only in what they were told.

Secrets are configuration with an additional constraint. They must never be in the image, never in a build argument, and ideally not in an environment variable either, because environment variables have an unfortunate habit of appearing in process listings, crash dumps, and diagnostic output. The better pattern is to mount a secret as a file that the application reads at startup, or to fetch it from a secret manager using a workload identity. For a local development stack, a file that is excluded from version control is acceptable, as long as the production path is different and documented.

Then storage. Containers are ephemeral: when one is replaced, anything written inside its filesystem is gone. That is a feature, because it forces you to be explicit about what must persist. For FieldOps Copilot, what persists is the database, and the database's data belongs in a volume, which is storage managed outside the container's lifecycle. Your application container itself should ideally write nothing that matters, which incidentally makes it possible to run with a read-only root filesystem, a very effective hardening measure we will come back to.

Now networking. Containers on a shared network can reach each other by name. That is convenient and it hides a trap, which is that your application and your database are on the same network by default, and so is anything else you add. The principle to apply is that only what must be reachable is reachable. The database should be reachable by the service and by nothing else, and in particular should not publish a port to the host machine in anything resembling a production configuration. During local development people expose the database port for convenience, and that convenience quietly becomes the deployed configuration.

Finally, the concept that separates a container that runs from a workload that operates: health checks. The orchestrator, whatever it is, needs to know two different things, and conflating them causes outages.

The first question is whether the process is alive. If it is not, restart it. A liveness check should be extremely cheap and should not depend on anything external. If you make liveness depend on the database, then a brief database interruption causes every one of your containers to be declared dead and restarted simultaneously, which converts a recoverable blip into a full outage. This is a real and common mistake.

The second question is whether the process is ready to receive work. Readiness may depend on external things: has the database connection been established, have migrations been verified, is the model provider reachable. A container that is alive but not ready should be kept running and simply not sent traffic. That is exactly the behavior you want during startup and during a dependency interruption.

There is a third kind, a startup check, which gives slow-starting applications a longer grace period before liveness checking begins, so that a slow boot is not mistaken for a hang.

Now apply this to the chapter's requirement that a failed database connection becomes a visible unhealthy state. The right design is: liveness stays green because the process is fine; readiness goes red because the service cannot do its job; the container is removed from traffic rather than killed; and a health endpoint reports which dependency is failing. That last detail is what makes the difference during an incident. A health response that says the service is unhealthy tells you nothing you did not know from the alert. One that says the database connection is failing, the read model is stale by a stated amount, and the model provider is reachable, tells you where to look.

Let me ground all of this with a scenario, because the abstract case for containers is well known and the field case is more specific.

You have a pilot approved to deploy into the customer's environment. Your service runs beautifully on your machine. The customer's platform team gives you access on a Tuesday, and here is what you meet.

Their runtime nodes have a different processor architecture from your laptop, so an image built locally without thought simply refuses to start with an unhelpful error about executable format. Their registry is internal and mirrors only approved base images, and the base you chose is not among them. Their policy rejects any image whose configuration does not specify a non-root user, and rejects it at admission time, so your deployment does not fail slowly, it never starts. Their nodes have no outbound internet access, so the dependency your application fetches at startup, which you had forgotten it fetches, cannot be reached. And their scanner produces a report with four high-severity findings, all of them in packages that exist in your image only because your base includes a full distribution and none of which your application uses.

Every one of those is a Tuesday afternoon, and together they can be a fortnight. Now notice that all five are avoidable before you ever get access. Build for the target architecture, and know what it is by asking. Ask in the first week which base images are approved and build from one of those. Run as a non-root user, which you should be doing anyway. Bake every dependency into the image at build time and verify by running the container with networking disabled. And use a slim base and a multi-stage build so the scan report is short enough to read.

That list is why I keep pushing you to ask boring infrastructure questions early in a delivery. They are not interesting questions, and they determine your schedule. The general lesson for field work is that constraints discovered late cost ten times what they cost when discovered early, and the cheapest way to discover them is a thirty-minute conversation with the platform team in week one, with a written list of exactly what you intend to ship.

So, why does this matter more to a forward deployed engineer than to a product engineer?

The first reason is that you deploy into other people's infrastructure. A product team runs one environment shaped the way they chose. You might deploy into a customer's managed container service, their Kubernetes cluster, a virtual machine at a site with intermittent connectivity, or in more regulated settings an environment with no outbound internet access at all. An image is the most broadly accepted unit of deployment across all of those. It is, in practice, the lowest common denominator that enterprise platform teams already know how to run.

The second reason is that customers have image policies, and you should find out what they are in the first week rather than the last. Common ones: images must be built from an approved internal base; images must come from the customer's own registry, not a public one; images must not run as root; images must pass a vulnerability scan at a stated severity threshold; images must carry specific labels for ownership and support. None of these are hard if you know about them at the start. All of them are painful if you discover them during a security review with a launch date already committed.

The third reason is air-gapped and restricted environments. If the customer's runtime cannot reach the public internet, then everything your image needs must be inside it or inside their registry. A build that downloads a dependency at container startup works perfectly on your laptop and fails instantly there. Build-time dependency resolution with everything baked in is not just tidiness; in some environments it is the difference between deployable and not.

The fourth reason is handover, again. A documented local stack that starts the whole system with one command is the most effective onboarding artifact you can leave behind. A new engineer on the customer's team running the full system in ten minutes is worth more than a very good architecture document.

Let me now walk the actual build for FieldOps Copilot.

Start with the service image. Stage one takes a base with the full runtime and build tooling, installs dependencies strictly from the lock file so the build is reproducible, copies the source, and produces the compiled output. Stage two starts from a slim runtime base, creates a dedicated non-root user, copies only the production dependencies and the built output from stage one, sets the configuration expectations, declares the port, defines a health check, and sets the process to run as that non-root user.

A few details make the difference between a workable image and a good one. Order your build steps so that the things that change least often come first: dependency installation before source copying, so that a source change does not invalidate the cached dependency layer. Exclude everything from the build context that does not belong in the image, which means a proper ignore file covering version control metadata, local environment files, test fixtures, and build caches. This is a security control as well as a size optimization, because an overly broad copy instruction is one of the most common ways a local environment file ends up inside a published image.

Make the container handle termination signals properly. When an orchestrator stops a container, it sends a polite termination signal and then, after a grace period, kills it. Your application should catch the polite signal, stop accepting new requests, finish the ones in flight, close its database connections, and exit. If your process runs in a way that never receives that signal, every deployment truncates in-flight requests, which the operator experiences as random failures during releases.

For the frontend, you have a deliberate choice to make, and I want you to make it rather than default into it. You can serve the built interface files from the service itself, which is the fewest moving parts and is entirely reasonable for a pilot. Or you can build a separate image with a static file server, which separates concerns and lets the interface scale and cache independently. Either is defensible. What is not defensible is running a development server in production, which is slow, insecure, and reveals internals. Write down which you chose and why.

Then the local stack. Compose the service, PostgreSQL, and the optional cache into one definition with named configuration, a volume for the database, and a network where the database is not exposed to the host. Now the important part, which the chapter's mini-project calls out specifically: startup ordering must not hide a broken dependency. The naive approach is to make the service wait for the database before starting, and to consider the problem solved. It is not, because it only addresses the first thirty seconds of the system's life. The database can also disappear at hour six.

The robust design is the one we described with health checks. The service starts regardless. Its readiness reflects whether its dependencies are available. It retries connecting with a sensible backoff rather than crashing. And the health response names the failing dependency. Build it that way and the startup case is handled as a special case of the general one, which means you have tested the general one every single time you start the stack.

While we are here, a word about architecture, because it caused the first failure in my scenario and it catches people constantly now that development machines and server fleets frequently differ. An image built for one processor architecture will not run on another. If you develop on a machine with one architecture and the customer's nodes use another, a locally built image fails immediately, with an error message that does not obviously say what is wrong. There are two answers. The simple one is to let the pipeline build the image, on a runner matching the target architecture, and never deploy anything built on a laptop, which you should be doing anyway for the build-once reason. The more flexible one is a multi-architecture build, where one image reference resolves to the right variant for whichever platform pulls it. Build times roughly double. For a pilot with a single known target, the simple answer is usually correct; just make sure you know the target.

And a brief word on size, because it is easy to dismiss as vanity. Image size affects three concrete things. It affects how long a deployment takes, which matters more than you expect when a rollback is in progress and every second is being watched. It affects cold-start time when a node has never pulled the image, which in an autoscaling environment is a user-visible latency spike. And it affects the length of the vulnerability report somebody has to review, which is the difference between a scan result that gets read and one that gets rubber-stamped. Going from several hundred megabytes to under a hundred is usually straightforward with a multi-stage build and a slim base, and the return on that hour of work is high.

Now the security section, which is the part of this chapter I care about most, because it is where the gap between common practice and good practice is widest.

Here is the key idea. An image and a running workload are different things with different risk profiles. A scanner looks at an image and tells you about known vulnerabilities in the packages it contains. That is useful and it is not sufficient, because most container security incidents are not about a vulnerable package in the image. They are about how the container was run.

So consider the runtime posture, and treat each item as a decision.

Run as a non-root user. If a process is compromised, root inside a container is meaningfully more dangerous than an unprivileged user, particularly in combination with any misconfiguration. Create a user in the image and run as it. This is also the single most common item on a customer's container policy checklist.

Drop capabilities. A container process gets a default set of privileged capabilities, most of which your service will never use. Drop all of them and add back only what you need, which for a typical service is nothing at all.

Prevent privilege escalation. There is a flag that stops a process from gaining more privileges than it started with. Set it.

Use a read-only root filesystem. If your application writes nothing to its own filesystem, make it unable to. Where it needs scratch space, mount a small writable area explicitly. This defeats a whole class of attack that relies on writing a payload somewhere.

Set resource limits. A container without a memory limit can consume the host's memory and take down everything else on the node. This is more often an availability incident than an attack, and it is entirely preventable.

Never bake secrets into layers, for the reason we discussed earlier.

Pin the base image by digest so that what you scanned is what you run.

And keep the image small, because every package you do not ship is a vulnerability you never have to explain.

Two more topics before the pitfalls, and both come up in enterprise deployments.

The first is provenance, meaning the ability to prove where an image came from. An image is a file that anybody can build and push under any name. In an environment with an internal registry and multiple teams, the question of whether the image running in production is the one your pipeline built is not paranoia, it is basic hygiene. The mechanism is signing: your pipeline signs the image at build time, and the deployment environment verifies the signature before it will run it. Combine that with the component inventory from last chapter, attached to the image, and you can answer the two questions a security reviewer actually asks: what is in this, and who built it.

You do not need to implement a full supply-chain framework in a pilot. But you should know the vocabulary, you should reference images by digest rather than tag in your deployment definitions, and you should be able to say what your plan is for provenance if the customer requires it. Increasingly, large enterprises do.

The second topic is debugging a container you deliberately made hard to debug. If you took my advice and shipped a minimal image with no shell, then the familiar move of connecting to the container and looking around is unavailable. That is the intended tradeoff, and you need a replacement.

Your first replacement is that everything diagnostically interesting should be observable from outside: structured logs going to standard output, a health response that names failing dependencies, and the metrics and traces we build next chapter but one. If you need to get inside a container to understand it, that is usually a signal that your observability is insufficient, and the fix belongs there rather than in adding a shell to production.

Your second replacement is the debug sidecar approach, where you attach a temporary container that has diagnostic tooling and shares the target container's namespaces, letting you inspect its process and network without the production image containing anything extra. Most modern runtimes support some version of this. Know that it exists, and know that using it in a customer environment may need permission, because attaching to a running production workload is exactly the kind of action their controls are designed to notice.

Your third replacement is reproduction. If your image is genuinely reproducible and your configuration is genuinely injected, you can run the identical image locally with equivalent configuration and investigate there. This is the best option when it works, and the degree to which it works is a direct measure of how well you followed the rules earlier in this lesson.

Now the pitfalls.

The first is the single-stage build that ships compilers and package managers to production.

The second is running as root, which is the default if you do not act.

The third is the secret in a layer, or in a build argument, or in a broad copy instruction.

The fourth is the base image referenced by a moving tag, which quietly breaks reproducibility.

The fifth is liveness checks that depend on external dependencies, turning a blip into a restart storm.

The sixth is the container that ignores termination signals, making every deployment slightly lossy.

The seventh is the database port published to the host in a configuration that later becomes production.

The eighth is configuration baked into the image, which destroys promotion.

The ninth is the development server in production.

The tenth is treating a clean vulnerability scan as security. The scan is a package inventory check. It says nothing about whether you run as root, whether you dropped capabilities, whether your filesystem is writable, or whether your secrets are mounted sensibly.

The eleventh, and the one that bites during handover, is an image that requires undocumented environment variables to start. If a missing required variable causes a confusing crash three layers deep, validate configuration at startup and fail with a clear message naming exactly what is missing.

Now verification. Here is what you should demonstrate.

Build the image twice from the same source and show equivalent results.

Show the final image contains no compiler, no package manager, and no application source beyond what runs.

Show the container process running as a non-root user.

Search the image's layers for any secret-like content and show there is none.

Start the whole stack from images and documented configuration, with one command, on a clean machine.

Stop the database while the system is running, and show that the service stays alive, reports itself not ready, names the failing dependency in its health response, is removed from traffic, and recovers automatically when the database returns.

Send a termination signal during an in-flight request and show a graceful shutdown.

Show the image running with a read-only root filesystem, dropped capabilities, no privilege escalation, and memory limits.

Scan the image, then remove one unnecessary runtime dependency and show the difference.

And start the container with a required configuration value missing, and show a clear, immediate error naming it.

Your practice handoff is the test in the guide. Containerize the service with a multi-stage, non-root, reproducible build. Decide and document the frontend boundary. Compose the full local stack with a database volume and no exposed database port. Implement liveness, readiness, and a diagnostic health response. Apply the runtime hardening posture. Scan, then remove something unnecessary. And show that a failed database connection becomes a visible unhealthy state rather than a crash or a silent error.

To recap. A container is a process with restricted visibility, restricted resources, and restricted privileges, running on a shared kernel, which means your isolation is only as strong as how you run it. Build in multiple stages so the final image carries the runtime and nothing else. Pin the base by digest and install from a lock file so builds are reproducible. Keep configuration out of the image and secrets out of the layers entirely. Separate liveness from readiness, never make liveness depend on an external dependency, and make the health response name the failing dependency so an incident starts with information. Harden the runtime: non-root, dropped capabilities, no privilege escalation, read-only filesystem, resource limits. And remember that a clean scan is an inventory check, not a security posture. In the field, an image is the unit your customer's platform team already knows how to run, so making it a good one is one of the highest-leverage things you can do for the deployment.

Next chapter we decide where these containers actually go: cloud platforms, the real constraints that drive the choice between the major providers, and the landing zone your pilot will live in.
