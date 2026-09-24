---
chapter: 11
title: "Backend services and Node.js"
roadmap_nodes: ["Backend Skills", "Backend", "Node.js"]
part: "III — Make the backend and data reliable"
audio: media/11-backend-services-nodejs.mp3
voice: en-US-AndrewNeural
rate: "-15%"
companion_guide: docs/guides/11-backend-services-nodejs.md
---

# Chapter 11 — Backend services and Node.js

[[Spoken narration begins below. Headers and this note are stripped before rendering.]]

## Orientation

Chapter eleven, and the start of Part Three. This is the chapter where FieldOps Copilot acquires an authority.

Here is where the build stands. You have a React operator workspace with two routes, a rebuilt intake form composed of typed components, deliberate empty and error states, an error boundary, and a keyboard path that survived the rewrite. All of its data comes from a mock service behind a seam, implementing a contract you wrote down. And the interface says so, out loud, because you put a marker on the screen.

Everything in that sentence is about to matter. In this chapter you build the real service: a typed Node process with a health endpoint, structured request logging, endpoints to create, list, and fetch an incident, server-side validation of every incoming record, and a domain service that owns the priority policy. Then you point the workspace at it and delete exactly the mock path that the service replaces — not the mock itself, which you keep, for reasons I will explain.

Records still live in memory in this chapter. That is deliberate. Restarting the service will lose every incident, and you will feel that as a defect, and that feeling is the motivation for chapter thirteen. Building persistence and a service at the same time means debugging both at once, and you will not know which layer lied to you.

By the end of this lesson you should be able to describe the lifecycle of a request through a layered service, explain what Node's execution model gives you and what it takes away, place a business rule where it can only exist once, produce error responses an interface can actually act on, and reason about what a customer's platform team will ask you before they let this process run near their systems.

## What a backend service is

Let me define it structurally, because the word backend covers everything from a single function to a data centre.

At its simplest, a service is a long-running process that listens on a network port, accepts requests, and returns responses. That is the whole mechanical description. Everything interesting is about what happens between accepting and returning, and about the properties the process maintains over time.

Walk one request through it. Something arrives on a socket. The process parses it into a method, a path, headers, and a body. It matches the path to a handler. It reads and size-limits the body, decodes it, and validates it against a schema. It establishes who is asking and whether they may — that is chapter twelve, and today you will leave a deliberate seam for it. It calls into application logic, which coordinates the work. That logic calls domain logic, which makes decisions. Decisions that need to be remembered go through a storage interface. Then a response is shaped, serialised, given a status, and written back. And throughout, one structured log line accumulates the facts of what happened.

The layering is the part worth spending real thought on, so let me name four layers and the rule that binds them.

The transport layer is the adapter to the outside world: routing, parsing, headers, status codes. It knows about the protocol and nothing about incidents.

The application layer coordinates a use case: create an incident means validate the input, ask the domain for a priority, persist the record, emit an audit event, return the created thing. It knows about the sequence and nothing about sockets.

The domain layer holds the rules: what makes an incident valid, how priority is computed, what a status transition is allowed to be. This is where your chapter three priority rule finally lands permanently. It knows nothing about the protocol, the database, or the framework, and it is ideally made of pure functions that you can test with no infrastructure at all.

The storage layer is an interface — a port, in the vocabulary from chapter six — with an implementation behind it. Today that implementation is a map in memory. In chapter thirteen it becomes PostgreSQL, and if you have drawn the boundary properly, nothing above it changes.

The rule that binds them is dependency direction: dependencies point inward, toward the domain. The domain does not import the framework. The domain does not import the database driver. It declares what it needs as an interface, and the outer layers supply it. This is the one architectural discipline I would insist on for a customer deployment, because it is what allows you to change the outside of the system — a new protocol, a new database, a new deployment target — without renegotiating the rules the customer agreed to.

One more property: statelessness. Each request should be understandable on its own, with no dependence on a previous request having landed on this same process. Not because purity is nice, but because in chapter twenty eight you will put this process in a container and in chapter thirty you may run several copies, and any state you kept in the process becomes a mystery when the second copy answers.

## What Node.js gives you, and what it takes

Now the runtime, because Node has specific properties that shape what a good service looks like.

Node runs your JavaScript on a single thread with an event loop — the same model you learned in chapter nine, which is a real advantage of choosing it here: one mental model for both sides. Input and output is non-blocking, handled by the platform underneath and delivered back to your loop as completions. The consequence is that Node handles many concurrent slow operations extremely well. A thousand requests all waiting on a database is exactly its strength.

The mirror image is the weakness, and it is sharp. Because there is one thread for your code, any computation that takes real time blocks every other request. Not slows — blocks. A synchronous loop over a large array, a big synchronous parse, an expensive hash, image work, or a giant serialisation, and every concurrent operator is waiting. For our service this is mostly fine: our work is validation, a rule evaluation, and a store operation. But you should know the escape routes exist — separate worker threads for genuinely heavy computation, or a different runtime for that one component — and you should know the diagnostic signature: latency that rises for everyone at once rather than for one endpoint.

Process lifecycle is the second Node topic that field work makes urgent. Your process starts, does some initialisation, and begins listening. It should distinguish being alive from being ready — it is alive as soon as it starts, ready only once its dependencies are reachable. It receives termination signals from the platform, and it must handle them: stop accepting new requests, let in-flight requests finish within a bounded grace period, close connections, then exit. Without that, every deployment in chapter thirty drops requests, and operators experience deploys as random failures. Graceful shutdown is fifteen lines and it is the difference between a deploy nobody notices and a deploy that generates tickets.

Related: decide what happens on an unhandled failure. An error that escapes all your handlers, or a rejected promise nobody was watching, leaves the process in an unknown state. The defensible policy is to log it with everything you know and exit, letting the platform restart you clean. Continuing to serve traffic from a process in an unknown state is how you get corrupt records, and a supervised restart is a second of unavailability against an unbounded correctness risk.

Configuration comes from the environment, not from files in your repository. The service address, the log level, the database location later, the model provider key much later. Nothing secret is ever committed, and nothing secret is ever printed — including in the startup line where people love to log their configuration for convenience.

Dependencies. Node's ecosystem is vast and that is a double-edged gift. Every package is code you are asking a customer to run inside their network, and in chapter thirty two somebody will ask you to account for it. So: pin versions with a lockfile, prefer a small number of well-maintained dependencies over many convenient ones, and be able to say what each one is for. For this service you need a web framework or the built-in server, a schema validator, a logger, and a test runner. That is a defensible list.

Finally, choose a runtime version that is a supported long-term release, and record the choice. Customers ask. Auditors ask. And a service pinned to an unsupported runtime becomes an urgent project at the worst time.

## The protocol is a contract you did not design

A short section on the transport, because engineers who learned frameworks before protocols tend to use one method and one status code for everything, and it costs them later.

Methods carry meaning that other software relies on. A read is safe: it must not change anything, and because it is safe, proxies, browsers, and monitoring tools feel free to repeat it. A creation is neither safe nor repeatable: sending it twice may create two things, which is exactly the ambiguity you met in chapter nine's timeout case. A full replacement is repeatable — sending it twice leaves the same result — and so is a deletion, in the sense that the end state is the same. Those properties are not decoration. A retrying proxy, a load balancer, or an impatient operator will exercise them, and a service that treats a read as a state change will eventually be surprised by infrastructure it does not control.

This is also why using one method for everything is a mistake even when it works. A tunnel where every operation is a creation and the real intent hides in the body throws away everything the ecosystem knows how to do for you: caching, retry safety, logging that distinguishes reads from writes, and the ability for a customer's platform team to reason about your traffic from the outside. In a customer environment, being legible from the outside is worth real money.

Status codes are the same story. A client should be able to make correct decisions from the status alone: retry, do not retry, fix the input, authenticate, escalate. If everything is a success with a nested error, or everything is a generic server error, then every client must parse prose to decide, and clients that parse prose break when you improve your wording.

Two more transport details worth deciding once. Content type: declare what you accept and reject what you do not, rather than guessing. And the response for a creation should tell the client where the new thing lives and what it looks like, so the interface does not have to immediately ask again.

You do not need to become a protocol scholar. You need enough to avoid the two mistakes that matter: pretending everything is the same kind of operation, and returning statuses that do not let a client act.

## Concurrency in one process

One more Node-specific hazard, because it feels impossible until it happens.

I said earlier that within a single task nothing interrupts you. That is true, and people over-generalise it into the belief that a Node service has no concurrency problems. It does. The interruption point is every await. Whenever your function suspends, another request's handler can run to its own suspension point, and the two interleave.

So consider a read-modify-write against your in-memory store: read the current list, decide something from it, then write. If anything between the read and the write suspends — a log flush, a validation that awaits, a lookup — a second request can slip in, read the same state, and both write, and one of the writes is lost. This is the classic lost update, and it exists in Node just as it does anywhere else.

Three defences, in order of preference. Prefer operations that do not require read-then-write at all — appending a record with a generated identifier does not, which is why creation is easy today. Where you must, keep the read and write in one synchronous stretch with no suspension between them, which is genuinely achievable with an in-memory store and worth doing deliberately. And where the operation is genuinely a transaction, push it into the storage layer and let a real database do it properly, which is what chapter thirteen gives you.

Why raise it now, when today's endpoints barely need it? Because chapter thirteen adds a status change, which is a read-modify-write, and chapter fourteen adds a counter, which is another. If you go in believing that a single-threaded runtime protects you, you will write both of them wrong and the failures will be intermittent, which is the worst kind. Learn the shape of the hazard here, where the code is small enough to reason about.

## Why a forward deployed engineer cares

Four arguments, and the first is the one that justifies this whole chapter.

The first is single ownership of policy. Right now the customer's triage rule exists in four places from earlier chapters — three language exercises and a Python command line tool — plus possibly a preview in the browser. That was fine as learning. It is not fine as a deployment. The moment two implementations of a rule exist, they will diverge, and the divergence will be discovered by a customer noticing that the screen and the report disagree. When they do, you will not be debugging code, you will be explaining to a manager why your system shows two different priorities for the same incident, which is a conversation that costs trust disproportionately. The service is where policy lives. One implementation, one owner, one place to change when the customer's definition of critical changes — which it will, in week three.

The second is that the service is the only place certain things can happen at all. Auditing that cannot be bypassed. Authorisation that cannot be edited by the person it restricts. Integration credentials that must not be visible. Rate limits. And — this is the one that matters most for the second half of this course — guardrails on the AI behaviour. In chapter nineteen you will build an agent that must never take an unapproved action. The only place that constraint can be enforced is behind an interface the model and the browser cannot reach around. A browser mock cannot enforce anything, and neither can a prompt.

The third is the customer's platform reality. A forward deployed engineer does not deploy into an empty field. You deploy into an environment with opinions: an approved runtime list, a proxy that inspects traffic, certificate interception, egress rules, a logging standard, a naming convention, a change window. Those constraints will affect your service more than any design preference you hold. So start asking early: what runtimes are approved here, what does the platform team need from a service to accept it, how does a service get a certificate, where do logs go, what is the health check contract. Chapters twenty seven through thirty one build the answers; chapter eleven is where you learn which questions to ask.

The fourth is that this process is the artifact that gets reviewed. When the security questionnaire arrives, it is about this. Input validation, error handling, dependency inventory, secret handling, logging content, authentication boundary, least privilege. Every one of those is cheaper to build now than to retrofit, and each one you skip becomes an item on somebody else's blocking list.

## How to do the work

The order I recommend, and why.

Start with the skeleton and the health endpoint. A process that starts, reads its configuration from the environment, listens on a configured port, answers a health request, logs one structured line per request, and shuts down gracefully on a termination signal. Nothing about incidents yet. This is perhaps forty lines and it gives you a deployable unit, which means chapter twenty eight has something to containerise and chapter thirty one has something to observe.

While you are there, be careful about what health means. A liveness check answers is this process running, and it should be trivial — no database, no outbound calls — because if it depends on a dependency, then a database blip causes the platform to kill and restart a perfectly healthy service, which is a genuinely spectacular failure mode. A readiness check answers should traffic be sent here, and that one may check dependencies. Keep them separate and note in your readme which is which, because the platform team will ask.

Then request logging. One line per request, structured as data rather than prose, containing method, path, status, duration, and a correlation identifier. Generate that identifier if the incoming request does not carry one, and return it in the response, because in chapter nine you promised the operator a reference they can quote and this is where that promise is kept. Never log the incident description, and be careful with anything the operator typed. Chapter thirty one goes deeper; today, establish the habit.

Then the contract, before the endpoints. You already wrote one in chapter nine. Read it again and decide whether it is still right now that you are on the other side of it. Three endpoints: create an incident, list incidents, get one incident. For each, the request shape, the success shape, the failure shapes, and the status codes.

On status codes, use them meaningfully and sparingly. A created resource is not merely fine, it is created, and saying so lets a client behave correctly. A validation rejection is a client error saying the request was understood but unacceptable, distinct from a request that was malformed at the protocol level. An unknown identifier is not found. An unexpected defect is a server error. That is most of what you need. And whatever you do, do not return success with an error field inside — every client in the world, including yours, will eventually forget to check it.

Then validation. Every incoming record gets parsed and checked at the boundary against a schema: required fields present, severity within the allowed set, impact within the allowed set, lengths bounded, unexpected fields either rejected or ignored by policy — decide which and write it down. Two design points. First, the rejection response should carry field-level detail, a list of which field failed and why, in exactly the shape your chapter nine interface already knows how to render, because you designed it. Second, and this is the important one: this validation is not a duplicate of the browser's, it is the real one. The browser's version exists to give fast feedback to a cooperating user. This one exists because the next request may come from a script.

Bound the request size too. An unbounded body is a trivial way to exhaust your process's memory, and the fix is one configuration value.

Then the domain service. Move the priority rule here as a pure function that takes the fields it needs and returns a priority, with no knowledge of transport or storage. Port it faithfully from your chapter three implementation and then, importantly, port the tests too — including the boundary cases and the ties. This is the moment to check that the rule you implemented three times actually agrees with itself, and I would not be surprised if you find a discrepancy. Finding it now is a good day.

While you are here, leave the seam for customer configuration that chapter six's decision record described: routing or weighting by business unit. Not implemented as a special case inside the rule, but as configuration the rule consumes. That distinction is the difference between a product and a fork.

Then the storage interface. Define what the application layer needs — save an incident, list incidents, fetch one by identifier — as an interface, and implement it with a map in memory. Two disciplines to observe even though it is temporary. Generate identifiers in a way that will still be valid in a database, and do not let anything above this interface know that storage is a map. If a route handler ever iterates the map directly, chapter thirteen becomes a rewrite.

Then wire the interface. In the React workspace, change the service seam's implementation from the mock to a real request, and change nothing else. If you have to touch a component, your seam was leaky and this is the lesson.

Keep the mock. Delete only the path the service replaces. You want the mock for tests that must run without a service, for interface work on a plane, and for demonstrating failure modes that a healthy service will not produce on demand. What you must remove is the ambiguity: the interface should be able to tell you which one it is talking to, and the visible simulated-service marker should appear only when the mock is in use.

Then confront the local networking detail that surprises everyone. Interface and service are now separate origins in development, and the browser will refuse cross-origin requests unless the server permits them. You have two options: configure permission explicitly for exactly your development origin, or run a development proxy so both appear to be one origin. The proxy is usually cleaner because it resembles production, where they will be behind one entry point. Whichever you choose, do not permit all origins as a shortcut, even in development, because that configuration always survives to production, and I have seen it survive to a security review.

Then integration tests. Start the application in-process and exercise it through its real routes: a valid creation returns the created incident with a priority you did not send; an invalid one returns field-level errors and creates nothing; listing returns what you created; fetching an unknown identifier returns not found. These are contract tests, and in chapter twelve they will be extended with authorisation cases, in chapter thirteen they will run against a real database, and in chapter twenty seven a pipeline will run them on every change. Write them so they read as statements about behaviour, not about implementation.

## Pitfalls, named

Business logic in route handlers. The single most common structural mistake. A handler that validates, computes priority, applies a customer rule, writes to storage, and formats a response cannot be tested without a server and cannot be reused by the background job you will need in chapter twenty four. Handlers should translate and delegate.

Trusting the client. Accepting a priority from the request body. Accepting a created timestamp. Accepting a status transition without checking it is legal. Accepting an identity claim without verifying it — that one is chapter twelve, and it is the one that becomes an incident report.

Leaking internals in errors. A stack trace, a database message, a file path, or a dependency version in a response body is reconnaissance handed to an attacker and confusion handed to an operator. Log the detail with a reference identifier; return the reference and a human sentence.

No request size limit and no outbound timeout. Both are one-line omissions with unbounded consequences. Anything you call — a database, an integration, a model provider — needs a deadline, or one slow dependency becomes your service's slowness, then your service's outage.

Blocking the loop. A synchronous operation over a large collection, or a heavy computation in a request path. Symptom: all endpoints slow together.

Treating console output as logging. Unstructured, unlevelled, unsearchable, and impossible to filter for sensitive content. Use a real logger from the first hour; retrofitting one across a codebase is tedious work nobody schedules.

Secrets in the repository. A configuration file with a real value, committed once, is committed forever in the history. Use environment variables, keep an example file with no real values, and add a secret scanner in chapter twenty seven.

Global mutable state. Convenient in a single process, wrong the moment there are two, and invisible until then. If it must be shared, it belongs behind the storage interface.

Swallowing errors. A catch that logs and returns success. The operator believes their incident was filed and it was not.

Async errors that escape the framework. Depending on your framework, an error thrown inside an asynchronous handler may not reach your error middleware, and the request hangs forever. Verify this deliberately by throwing on purpose, and confirm the client gets a response.

One health check that tests everything. Already covered, and worth repeating: a liveness check that depends on a database causes restart storms during a database blip.

Permissive cross-origin configuration. Wildcards in development that reach production.

Missing correlation identifiers. Without one, an operator's support ticket and your logs cannot be joined, and every investigation starts with guessing at timestamps.

And the big one: a second implementation of policy. If, at the end of this chapter, the browser still computes a priority that it displays as fact, you have not finished the chapter.

## Verifying your work

Seven checks, and I want you to actually do the fourth one.

Create an incident from the interface and confirm the returned record contains a priority the browser did not send, plus a server timestamp and an identifier.

Send an invalid record directly to the service, bypassing the interface entirely — empty required fields, a severity outside the allowed set, a description far too long, a priority you tried to inject. Confirm each is rejected with field-level detail and confirm that nothing was created.

List and fetch. Then fetch an identifier that does not exist and confirm you get a clean not-found rather than an empty success or a crash.

Restart the service with incidents in it. They are gone. Sit with that for a second. Write down what a customer would call this behaviour, and what you would have to promise them before this went anywhere real. That sentence is the brief for chapter thirteen.

Send a termination signal while a request is in flight. Confirm the request completes and the process exits without dropping it, within a bounded grace period.

Read your logs. Is there one structured line per request with a correlation identifier? Is the incident description absent? Is any secret absent, including from the startup line? Now imagine handing these logs to a customer's platform team, because in chapter thirty one you will.

Run the test suite from a clean checkout, including the ported domain rule tests. Note the command in the readme. In chapter twenty seven a machine runs exactly this, and if it needs a manual step today it will need a manual step then.

## Your practice test

The guide has the rubric. Spoken:

Your goal is a typed Node service that owns the FieldOps triage policy and serves create, list, and get for incidents, with the React workspace pointed at it and the corresponding mock path removed.

Your constraints: four layers with dependencies pointing inward, and a domain that imports neither the framework nor storage. Every incoming record validated on the server against a schema, with field-level rejection detail in the shape the interface already renders. The priority policy implemented once, here, ported with its tests from chapter three, with the business-unit rule expressed as configuration rather than a special case. Storage behind an interface, in memory, with nothing above the interface knowing that. Configuration from the environment, no secrets in code or logs. One structured log line per request with a correlation identifier returned to the caller. Separate liveness and readiness. Graceful shutdown with a bounded grace period. A request size limit and a deadline on anything outbound. No permissive cross-origin shortcut. And the mock kept but unambiguous, with the simulated marker appearing only when the mock is in use.

Your artifacts: the service; a layer map naming what each layer may and may not import; the contract document updated to what the service actually does, including status codes and error shapes; the ported domain rule with its test table and a note on any discrepancy you found between your earlier implementations; integration tests for valid creation, invalid rejection, list, and not found; a dependency inventory with one sentence per dependency; a note recording the restart-loses-data behaviour as the brief for chapter thirteen; and a short list of the questions you would ask a customer platform team before deploying this process.

You are done when the browser can create and retrieve a real incident through the service, when a direct invalid request cannot create one, when the priority policy exists in exactly one place, when the process starts and stops cleanly under signals, and when your logs are useful without containing anything you would not want to hand over.

## Recap

Five things.

First, a service is layers with dependencies pointing inward. Transport translates, application coordinates, domain decides, storage is an interface. That direction is what lets you change the outside without renegotiating the rules.

Second, Node's single-threaded loop is excellent at waiting and terrible at computing. Know the symptom of a blocked loop, and handle process lifecycle deliberately — ready is not the same as alive, and shutdown is a feature.

Third, server-side validation is not a duplicate of browser validation. It is the real one, and it is the only one that survives a client that is not yours.

Fourth, policy lives here, once. Every duplicated rule becomes a divergence, and every divergence becomes a conversation about trust.

Fifth, this process is the artifact that gets reviewed. Structured logs without sensitive content, no leaked internals, an inventory of dependencies, secrets from the environment, and a health contract the platform team recognises. All cheap now, all expensive later.

In chapter twelve we make this service safe to expose: roles and least privilege, an authentication boundary, authorisation on every operation, a published contract, and one honest decision about whether a graph query layer earns its place. Build the service first. Then meet me there.
