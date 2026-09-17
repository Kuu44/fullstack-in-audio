---
chapter: 12
title: "API design, identity, and secure integration surfaces"
roadmap_nodes: ["APIs Design / API Design", "API Security", "Authentication", "GraphQL"]
part: "III — Make the backend and data reliable"
audio: media/12-api-design-and-security.mp3
voice: en-US-AndrewNeural
rate: "-15%"
companion_guide: docs/guides/12-api-design-and-security.md
---

# Chapter 12 — API design, identity, and secure integration surfaces

[[Spoken narration begins below. Headers and this note are stripped before rendering.]]

## Orientation

Chapter twelve. This is, in my judgment, the highest-stakes chapter in Part Three, because it is where the system stops being a private toy and becomes a surface that other people and other software can reach.

Where we stand. You have a Node service that owns the triage policy, validates every incoming record, logs one structured line per request with a correlation identifier, separates liveness from readiness, and shuts down gracefully. The React workspace talks to it. And right now, anyone who can reach the port can create, list, and read every incident in the system, because there is no identity, no permission, and no boundary of any kind.

That is not a criticism of your work. It is the correct state after chapter eleven, and it is also precisely the state in which a great many pilots get deployed, because the demo works and the deadline is Thursday. I want to be blunt about the consequence: an unprotected internal endpoint containing customer operational data is not a rough edge, it is an incident waiting for its date. And the incident does not have to involve a malicious actor. It only takes one person discovering that a colleague's incidents are visible, and your pilot becomes an item in a compliance review.

So in this chapter you do four things. You design the interface properly, as a contract that can evolve. You add an authentication boundary that works locally without lying about how it will work in production. You enforce authorisation on every operation and every object, deny by default. And you publish the contract, then make one honest, documented decision about whether a graph query layer earns a place in this system.

Four topics, one lesson. They belong together because they are the same surface viewed from four angles: shape, identity, permission, and description.

## What API design actually decides

Start with design, because a well-shaped interface makes the security work simpler and a badly shaped one makes it nearly impossible.

An interface is a set of promises about what a client can ask for and what will come back. The promises you make now are expensive to break later, because breaking them breaks software you do not control — your own workspace, a customer's integration, the tool you build in chapter eighteen, and a script somebody wrote without telling you.

The first decision is resources versus actions. The dominant style organises the interface around things: a collection of incidents, one incident, that incident's status history. Operations on those things are expressed with the protocol's methods. The alternative organises around verbs: create incident, escalate incident, close incident. In practice, mature interfaces are mostly resources with a small number of explicit actions where a state transition genuinely is not a field edit. Approving an AI proposal in chapter nineteen is a good example: it is an event with meaning, not a field assignment, and modelling it as an action makes the audit trail obvious.

The second decision is granularity. Endpoints that are too fine make clients chatty — six requests to render one screen. Endpoints too coarse return everything to everyone, which is both wasteful and a security problem, because output that includes fields the caller should not see is a leak whether or not the interface displays them. Aim to serve a screen's needs in one or two requests, without inventing a bespoke endpoint per screen.

The third is collections, and this is where people under-design. A list endpoint needs filtering, sorting, and a bound on how much it returns. Decide the default page size and the maximum now, because an unbounded list works beautifully with your twelve seeded incidents and falls over at the customer's twelve thousand — and it does so in production, on the day adoption succeeds. Two pagination styles exist: offset-based, which is simple and drifts when records are inserted while paging, and cursor-based, which is stable and slightly more work. For an operator queue where new incidents arrive constantly, cursor-based is the correct answer, and you should be able to say why.

The fourth is evolution. You will change this interface. The rules that keep changes safe are simple and worth memorising. Adding an optional field is safe. Adding a new endpoint is safe. Removing a field, renaming a field, changing a type, making an optional field required, or changing the meaning of an existing value are all breaking. Never repurpose a field — a status value that used to mean one thing and now means another is undetectable by any client and produces the worst class of bug, the kind where everything runs and the data is wrong.

When you must break something, you need a versioning strategy. Put a version in the path, which is blunt but obvious and easy for a customer's team to reason about, or negotiate it in a header, which is more elegant and less legible from the outside. For a customer pilot I would take the blunt, legible option. And whatever you choose, write down your deprecation policy: how long an old version lives, how a client is told, and how you will know who is still using it. That last part requires logging the version per request, which is one field you add today and thank yourself for later.

The fifth decision is the error model, which you already started in chapter nine and chapter eleven. Keep one stable shape for every failure: a machine-readable code, a human-readable message, a correlation identifier, and, for validation failures, a list of field-and-reason pairs. The code is what clients branch on. The message is what a person reads. Do not let clients branch on the message text, because you will improve the wording and break them.

And the sixth, which becomes urgent in the next chapter: idempotency. A creation is not naturally repeatable, and chapter nine left you with an honest but unsatisfying answer to the timeout case. The interface-level solution is to let the client send a key it generates for a submission, and to promise that two requests with the same key produce one record and the same response. That promise is an interface design decision made now, implemented in chapter thirteen where the store can enforce uniqueness. Put it in the contract today.

## Identity: authentication versus authorisation

Now the part where precision of vocabulary genuinely prevents defects.

Identity is a claim about who is acting. Authentication is the process of establishing confidence in that claim. Authorisation is the decision about whether that actor may perform this operation on this object. Three separate things, and they fail separately. A system can authenticate perfectly and authorise catastrophically, which is in fact the most common serious flaw in real applications.

Two mechanisms carry authenticated identity. A session is server-side state referenced by an opaque identifier, usually in a cookie; the server can revoke it instantly by forgetting it. A token is a self-contained, signed statement of claims that the server validates cryptographically without a lookup; it scales beautifully and it cannot be revoked before it expires unless you add a revocation mechanism, which is state, which was the thing you were avoiding. That tradeoff is the whole conversation, and there is no free answer. For a browser-facing internal tool, sessions with an opaque cookie are frequently the safer and simpler choice; for service-to-service and for the tool you build in chapter eighteen, short-lived tokens fit better.

If you use tokens, three rules are not negotiable. Verify the signature, and verify it with the algorithm and key you expect rather than the one the token proposes. Enforce expiry, plus the audience and issuer claims, so a token minted for another system is not accepted by yours. And put nothing sensitive inside, because the contents are readable by anyone holding it — a token is signed, not secret.

Now, the enterprise reality, which is the part that separates a field engineer from someone who has only built greenfield products. Your customer already has an identity system. They have single sign-on. They have groups that already encode who is a dispatcher and who is a facilities manager. They have a joiner-mover-leaver process, and probably an automated provisioning mechanism. They have an authentication policy that includes a second factor. And they have an identity team who will be genuinely unhappy if you invent your own user table with your own passwords.

So the correct architecture is almost always: delegate authentication to the customer's identity provider through a standard protocol, receive a verified identity, and map the customer's existing group membership onto your application roles. You own authorisation; you do not own identity. There are three benefits and they are large. Leavers lose access automatically, because your system inherits their identity lifecycle. You never store a password, which removes an entire category of risk and an entire section of the security questionnaire. And the customer's existing second factor applies to your tool for free.

Which brings us to the local development problem, because you cannot make a pilot depend on a corporate identity integration in week one. The pattern that works is a pluggable authentication boundary: one component whose job is to turn an incoming request into a verified identity with a set of roles. In development it is satisfied by a local mechanism — a development identity issued by a local component, or a signed development credential — and in production it is satisfied by the customer's provider. Everything above that component sees only the verified identity, so nothing else changes when you swap.

Two disciplines make that safe. The development implementation must be selected by explicit configuration that is off by default, and the service should refuse to start in a non-development configuration if the development boundary is active. Fail loudly, at startup, rather than silently accepting a development credential in production — because that mistake has happened to real teams and it is indefensible in a review. And write the swap down as a decision record naming which protocol you expect to use and what you need from the customer to enable it, because that is a procurement conversation with a lead time, and starting it in month three is starting it late.

## Authorisation: the part that actually gets breached

Now the mechanics of permission, and I want to spend disproportionate time here because this is where real systems fail.

Start with roles. Your chapter one charter named an operator and an administrator. Define what each may do in terms of operations, not screens. An operator may create an incident, list incidents within their scope, read one, and later approve or reject an AI proposal. An administrator may additionally change configuration, view audit records, and manage the service catalogue. Write it as a matrix, because the matrix is both your implementation guide and your evidence for the security review.

Then the two rules.

The first rule is deny by default. Authorisation is not a list of things that are blocked; it is a list of things that are allowed, with everything else refused. The practical form is that a new endpoint is unreachable until someone explicitly grants access to it. This matters enormously in field work, because endpoints get added in a hurry between customer meetings, and the failure mode you want from haste is an endpoint nobody can reach, not an endpoint everybody can.

The second rule is that permission is about the object, not just the operation. This is the failure that appears at the top of every industry list of serious flaws, and it is worth stating slowly. Checking that the caller is an operator before allowing them to read an incident is not sufficient. You must check that this operator may read this incident. Otherwise any operator can read any record by changing an identifier in a request, and if your identifiers are sequential integers, they can read all of them by counting. FieldOps Copilot will have business units, and eventually multiple customers, and the isolation boundary between them is enforced exactly here, at the object level, on every operation, including read.

Two implementation notes that follow from that. Put the authorisation decision where it cannot be bypassed. A check in the route handler protects that route; a check in the application layer protects every caller of that use case, including the background job in chapter twenty four and the tool in chapter eighteen. And filter output as well as input: return only the fields this caller may see. It is not sufficient that the interface hides them, because the response is visible to anyone who opens the browser's network panel.

Also: use identifiers that cannot be guessed or enumerated. Random identifiers are not an access control mechanism and must never be your only defence, but sequential ones convert a single authorisation mistake into a complete data disclosure, and they leak business information — a customer can tell how many incidents you have processed, which they will notice.

## The rest of the security surface

Beyond identity and permission, there is a checklist, and I want to give it to you as a list you can actually work through.

Validate input on the server. Done in chapter eleven; keep it.

Guard against mass assignment. If you build a record by copying whatever fields arrived in the request body, then a client can set status, priority, owner, or an internal flag by including it. Accept an explicit set of fields and ignore or reject the rest. This is one of the most common ways a validated interface still gets subverted.

Rate limit. Per identity and per address, on write endpoints especially, and on anything expensive. Chapter fourteen gives you a natural place to store the counters. Without a limit, one misconfigured integration retrying in a loop becomes an outage, and that scenario is far more likely than an attack.

Manage secrets properly. Configuration from the environment now, a managed secret store when you reach a cloud in chapter twenty nine. Never in the repository, never in a log, never in a response, never in the contract document.

Insist on transport security. Encrypted transport everywhere it can be arranged, including inside the customer's network, and be aware that many enterprises inspect traffic with their own certificate authority, which will affect your outbound calls in chapter fifteen.

Be careful with outbound requests. If any endpoint ever takes a location from a caller and fetches it, you have handed the caller your service's network position, which inside a corporate network is a serious capability. Allow-list destinations rather than trusting input.

Do not leak information in error messages. This includes the subtle case: an authentication failure should not distinguish an unknown account from a wrong credential, because the difference tells an attacker which accounts exist.

Keep an audit trail for security-relevant events: authentication outcomes, authorisation denials, permission changes, administrative actions. Chapter thirteen makes it durable; today, log it.

And if you use cookies for sessions, understand cross-site request forgery and defend against it, with same-site cookie behaviour and, where needed, a token pattern. If you use bearer tokens in headers instead, you avoid that class and take on the storage problem — where the token lives in a browser is a genuine tradeoff, and browser storage readable by any script on the page is the weakest of the options.

## Machine callers and scoped credentials

One more design topic before the contract, because it is the part of the interface a browser-focused engineer forgets and a customer's integration team asks about immediately.

Not every caller is a person. Your own scheduled jobs will call this service in chapter twenty five. The read-only tool you build in chapter eighteen calls it on behalf of a model. And the customer will, sooner than you expect, want their existing ticket system to create incidents automatically. Those callers need identity too, and human identity is the wrong shape for them, because there is nobody to complete a login and nobody to notice a prompt.

So define a second kind of principal: a service identity. It authenticates with a credential the customer's platform team can rotate, it has a name that appears in your audit trail, and — this is the important part — it has a scope that is much narrower than any human role. The integration that files incidents from the ticket system should be able to create an incident and nothing else. Not list, not read, not update. If it can only create, then a leaked credential produces spam you can clean up rather than a data disclosure you must report.

Three rules for these credentials. Scope each one to the smallest set of operations that its job requires, and give each integration its own, so that revoking one does not break the others and so your audit trail tells you which integration acted. Make rotation possible without downtime, which means accepting two valid credentials during an overlap window — design that in now, because retrofitting it means a scheduled outage. And put an expiry on them, even if it is long, so that an abandoned integration eventually stops working instead of remaining a live key in somebody's script forever.

The same reasoning applies in the other direction, to calls your service makes outward. In chapter fifteen you will call a model provider, in chapter twenty four an asset source, and possibly a notification service. Each of those credentials is a separate secret with its own scope, and each outbound call needs a deadline and a failure behaviour. And when you send data outward, decide explicitly what you are sending, because an integration that forwards the whole incident record including the operator's free-text description may be sending customer-sensitive content to a third party. Chapter thirty two turns that into a data classification exercise; today, just notice that outbound is a boundary too.

There is a related design question worth deciding early: how does the customer's system learn that something happened in yours? Polling is simple, works through restrictive networks in the direction enterprises usually permit, and wastes requests. Outbound notifications are efficient and require your service to reach into their network, which is often the harder approval to obtain, and they bring their own requirements — retries, ordering, duplicate delivery, and a way for the receiver to verify the message came from you. You do not have to build either today. You do have to avoid designing something that makes both impossible, which mostly means keeping a reliable ordered record of what changed — which is exactly the audit trail chapter thirteen will make durable.

Finally, note what all of this does to your role matrix. It is no longer two rows. It is operator, administrator, and one row per service identity, each with an explicit list of permitted operations. Write it that way from the start. When a security reviewer asks what can create an incident in this system, the answer should be a table, not a conversation.

## Publishing the contract

Now the description, which is a deliverable in its own right.

A published interface description does four jobs. It lets a client team work without reading your source. It lets you generate types, so that chapter nine's hand-written incident shape can be replaced by a generated one and cannot drift. It gives the customer's security reviewer a precise object to review. And it becomes part of the handoff packet in chapter thirty seven.

Write it as a machine-readable specification. What must be in it: every endpoint, the request and response shapes, every error shape and status, the authentication scheme, and which role each operation requires. What must not be in it: real credentials, internal hostnames, database details, sample data containing real customer content. Documentation is published more widely than you expect, and I have seen a specification with a working credential in an example, sitting in a repository that was later shared with a partner.

Two practices raise this from documentation to engineering. Generate your client types from the specification rather than maintaining two truths — that is the moment your interface becomes a contract rather than a description. And test the service against the specification, so that a response shape that drifts from the document fails a test rather than surprising a client. In chapter twenty seven, both of those become pipeline stages.

## GraphQL: earn it or refuse it

Now the fourth topic, and the roadmap includes it for a reason: a forward deployed engineer is regularly asked about it, sometimes by a customer's architect who has an opinion.

Here is what it is. One endpoint, a typed schema describing all available data and their relationships, and clients send a query describing exactly the fields they want. The server resolves each field through a function. The client gets precisely the shape it asked for.

The real benefits. Clients stop over-fetching and under-fetching, which matters when you have many different clients with different needs. A screen assembling data from several sources gets one request instead of five. The schema is introspectable, so tooling is excellent. And evolution is by deprecation and addition rather than by versioned duplication, which is genuinely nicer for a long-lived interface with many consumers.

The real costs, and each one is concrete. Authorisation becomes per field, per object, because a client can traverse relationships you did not anticipate — if any path through your graph reaches an object without a check, the graph will find it. Query cost becomes unbounded unless you add depth limiting, complexity analysis, and cost budgets, because a deeply nested query is a denial of service that looks like a legitimate request. The naive resolver produces a query per item, and fixing that requires batching, which is real machinery. Response caching at the network layer largely stops working, because everything is one endpoint with a body. Introspection in production is a decision, not a default. And, most importantly for us, your customer's team has to be able to operate it after you leave.

So apply it to FieldOps Copilot. The write path — creating an incident, changing a status, approving a proposal — wants idempotency keys, precise validation, an audit event per operation, and dead-simple authorisation. All four are more straightforward over plain endpoints, and none of them benefits from client-specified shapes. Keep writes as they are.

The read path for a dashboard that wants incident counts by service and severity, plus the last few status changes, plus asset context from chapter twenty four, is a plausible case: several sources, one screen, varying shapes. So build one read-only query, by hand, typed, with authorisation applied per object and a depth limit, and use it to form an opinion from experience rather than from an article.

Then write the decision down, in either direction, and include the sentence I want you to be able to defend: whether the customer's team can operate this after handoff. If the honest answer is no, then a focused set of endpoints is the better engineering choice even if a graph layer is the more fashionable one. I have made that call both ways on real projects, and the deciding factor was never elegance.

## Why a forward deployed engineer cares

Three reasons, briefly, because I have been making the case throughout.

This is where value meets risk. The interface is simultaneously the thing that makes the system useful to other systems and the thing that makes customer data reachable. Every capability you add is also an exposure, and an FDE is the person who has to hold both thoughts at once, in a hurry, under a delivery deadline.

This is what gets reviewed. The security questionnaire, the penetration test, the architecture review board, and the procurement checklist all point at this chapter. Doing it now costs a few hours. Doing it after a review costs a delivery slip and, worse, spends the customer's confidence.

And this is where you either respect the customer's operating model or fight it. Their identity provider, their group structure, their token policies, their network controls. A pilot that inherits those is a pilot that can go to production. A pilot with its own user table and its own passwords is a pilot that will be asked to rebuild its foundation, at the exact moment everyone is excited about the results.

## Pitfalls, named

Authorisation checked on the route but not the object. Say it three times. Any operator reading any incident by changing an identifier is the defect.

Role enforcement in the interface only. Hiding the administrator button is a courtesy. The endpoint is the enforcement.

Administrator by default in development, and shipped that way. If your development identity has every role, you will never notice a missing check. Develop as an operator most of the time.

Tokens without verification, expiry, audience, or issuer checks. And secrets placed inside tokens, which are readable by design.

Long-lived credentials with no revocation path. A leaked token valid for a year is a year of exposure.

Returning whole objects. Internal notes, owner identifiers, provider metadata — filter output per caller.

Mass assignment. Building records from whatever arrived.

Sequential identifiers plus a missing check equals full disclosure.

No rate limit, so a retry loop becomes an outage.

Verbose authentication errors that reveal which accounts exist.

Permissive cross-origin configuration, again, because it survives from development.

A published specification containing a real credential or an internal hostname.

Breaking changes shipped in place. A renamed field, a repurposed status value, an optional field made required. All invisible to you and fatal to a client.

Unbounded graph queries, missing per-field authorisation, and production introspection.

And the quiet one: no record of who did what. Chapter thirteen makes the audit trail durable, but if you do not decide today which events matter, you will be reconstructing them from request logs during an investigation.

## Verifying your work

Build a matrix and run it. For every operation, four cases: no credential, a credential with the wrong role, a valid credential with the right role, and a malformed request from a valid caller. That is four times however many operations you have, and it is the single most valuable test suite in this course, because it is the one a reviewer will ask to see.

Then the object-level tests, which are the ones people skip. Create an incident as one operator in one business unit. Fetch it as a different operator in a different unit. You must be refused. Then try to change its status. Refused. Then list, and confirm the other unit's incident does not appear. If any of these succeed, stop everything and fix it, because that is the finding that ends pilots.

Then attempt an administrator-only operation as an operator, both through the interface and directly against the service, and confirm the direct attempt is refused too.

Then look for leaks. Read a full response body and account for every field: may this caller see this? Then read your error responses: any stack trace, driver message, internal hostname, or version string?

Then try enumeration. If identifiers are sequential, walk them and see what you get.

Then expiry and revocation. Use an expired credential. Then revoke access and confirm the next request fails — and note how long that takes, because that number is your answer when a customer asks how fast a departing employee loses access.

Then rate limiting. Send a burst and confirm you are throttled with a clear status rather than falling over.

Then validate the published specification: does it parse, does it describe every endpoint including errors and required roles, and can you generate client types from it that compile against your workspace? And search it for anything secret.

Finally, if you built the graph query, send a deliberately deep and expensive query and confirm it is refused, and attempt to traverse to an object you should not see.

## Your practice test

Guide has the rubric. Spoken:

Your goal is to make the FieldOps service safe to expose: two roles with least privilege, a pluggable authentication boundary, authorisation on every operation and every object, a published contract, and one documented decision about a graph query layer.

Your constraints: deny by default, so a new endpoint is unreachable until explicitly permitted. Authorisation decisions live where every caller passes through them, not only in route handlers. Object-level checks on every operation including reads and lists. Output filtered per caller. The development authentication mechanism must be off by default and the service must refuse to start with it enabled outside development. No user passwords stored by you — delegate authentication and map the customer's groups to your roles. Identifiers must not be guessable. Rate limits on writes. An idempotency key defined in the contract, to be enforced in chapter thirteen. And the published specification must contain no secret and no internal detail.

Your artifacts: the role and permission matrix, expressed as operations rather than screens; the authentication boundary with both implementations and the startup guard; the published interface specification including errors and required roles; generated client types replacing the hand-written ones from chapter nine; the four-case test matrix plus object-level isolation tests; one read-only graph query with per-object authorisation and a depth limit, or a written refusal with reasons; a decision record naming the identity protocol you expect in production and what you need from the customer to enable it; and a short security note listing which items on the checklist you implemented, which you deferred, and who owns each deferral.

You are done when an operator cannot perform an administrator action or read another unit's incident, when every operation refuses an unauthenticated caller, when the specification is publishable as-is, and when your graph decision has a reason attached that survives being questioned by a customer's architect.

## Recap

Five things.

First, interface design is a set of promises. Additive changes are safe, and repurposing a field is the one change that fails silently. Bound your lists, choose cursor pagination for a live queue, and define idempotency now.

Second, authentication and authorisation are different, and the customer already owns identity. Delegate it, map their groups to your roles, and never store a password.

Third, authorisation is per object, not per route, and deny by default. That single sentence covers the most common serious flaw in real systems.

Fourth, the published contract is an engineering artifact, not documentation. Generate types from it, test against it, and keep every secret out of it.

Fifth, GraphQL is a real tool with real costs — per-field authorisation, query cost control, batching, and operability after handoff. Decide, document, and be able to defend it either way.

In chapter thirteen the records stop disappearing. We model incidents, status changes, and immutable audit events in PostgreSQL, write migrations by hand, move the service's operations into transactions, enforce that idempotency key, and read a real query plan. Secure the service first. Then meet me there.
