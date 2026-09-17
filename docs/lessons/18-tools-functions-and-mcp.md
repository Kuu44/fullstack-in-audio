# Chapter 18 — Tools, functions, and the Model Context Protocol

**Roadmap nodes covered:** Tools & Functions; MCP
**Part:** IV — Build AI behavior that can be controlled
**Companion test:** `docs/guides/18-tools-functions-and-mcp.md`
**Audio:** `media/18-tools-functions-and-mcp.mp3`

---

## Narration

Welcome to chapter eighteen.

Until now, the model in FieldOps Copilot has been sealed. You hand it an incident, it hands back a suggestion. It has no way to find anything out. If the report mentions a related ticket, the model cannot look at it. If the operator wants to know whether this has happened before, the model has no idea.

Today we open one small door. We give the model the ability to ask for information from a real system — and we do it in a way that means a completely compromised model still cannot do anything harmful.

This is the chapter where AI engineering stops being about text and starts being about access control. If you only take one idea from part four of this course, I would like it to be the one in the middle of this chapter, about who the tool runs as.

The plan: first, what a tool call actually is mechanically, because it is widely misunderstood in a way that leads directly to unsafe designs. Second, how to design a tool contract, which is API design for a consumer that has never read your documentation and cannot ask you a question. Third, authorization at the tool boundary — the core of the chapter. Fourth, the Model Context Protocol: what it is, why it is genuinely useful to a forward deployed engineer, and the new risks it introduces. Fifth, error handling that fails safely. Sixth, auditing. Then pitfalls, verification, and the test project.

### What a tool call actually is

Let me start with the mechanics, stated carefully, because the mental model most people absorb is wrong in a way that matters.

You declare a set of capabilities to the model. Each one has a name, a description in natural language, and a schema describing its inputs. You send these declarations along with your prompt.

When the model decides a capability would help, it does not call anything. It cannot call anything. It emits a piece of structured output that says, in effect, "I would like the tool named this, with these argument values." That output arrives back at your code, and the generation pauses.

Then your code — your ordinary, deterministic, fully controlled code — decides what to do. You validate the arguments. You check authorization. You decide whether to execute at all. If you execute, you run your own function, with your own error handling, against your own systems. You take the result, format it, and send it back into the model's context as a new message. Generation resumes, now with that information available.

Say the important part again: the model never executes anything. It emits a request. Every single guardrail you will ever have lives in the code that decides whether to honour that request.

This matters because of how people phrase it. "We gave the agent access to the database." "The agent can query our ticketing system." Those sentences describe an outcome accurately but they encode the wrong mental model, and the wrong mental model leads engineers to put their safety controls in the prompt — telling the model which queries it may run — instead of in the executor, where they belong and where they cannot be talked out of.

Here is the correct framing, and I want you to use these words: a tool is an endpoint, and the model is an untrusted client calling it. You would never secure an HTTP endpoint by writing documentation asking clients to behave. You authenticate the caller, you validate the input, you authorize the action, you constrain the output. A tool is exactly the same, and the fact that the caller is a language model changes nothing except that this particular client is unusually creative about malformed requests and can be influenced by anyone who can get text into its context.

One more mechanical point, because it shapes the design. The tool's description is sent to the model on every call. That means two things. It is behaviour-changing configuration, exactly like the prompt in chapter sixteen, and it deserves the same versioning and review — a reworded tool description can change when the model reaches for it, which changes system behaviour, with no code change. And it is a recurring token cost, so verbose descriptions are paid for on every request forever.

### When something should not be a tool

Before we design one, a question people skip: should this be a tool at all?

There are three ways to get information to a model, and tools are the most expensive of them.

You can put it in the prompt directly. If the information is small, always relevant, and you already have it, just include it. The category taxonomy from chapter sixteen is a good example — you would never make the model call a tool to find out what the valid categories are. It is needed every time, it is tiny, and a tool call would add a full round trip for no benefit.

You can retrieve it deterministically before the call. If you know the incident references a related ticket because your intake captured that field, fetch it in your own code and include it. Your code knows the situation better than the model does, and a deterministic fetch is faster, cheaper, and cannot be skipped or misused. This is the option people forget, and it is frequently the right one.

Or you can expose it as a tool, which is appropriate when you genuinely do not know in advance whether the information is needed, and when fetching it always would be wasteful or impossible. A lookup by an identifier that appears in free-text description is a fair case: most reports will not reference another incident, so fetching unconditionally is not an option, and the model reading the text is the thing that determines whether the identifier is there.

The cost of a tool, so you can weigh it honestly: an extra model round trip, so roughly double the latency of that turn; the tokens for the declaration on every call plus the request and the result; an authorization surface to design and defend; an error path; an audit obligation; and a new way for the turn to go wrong. That is a lot to pay for information you could have just included.

So the rule: default to putting things in context, escalate to deterministic pre-fetch, and reach for a tool only when the model's judgment is genuinely required to decide whether the information is needed. Every tool you do not build is a tool you do not have to secure.

### Designing the tool contract

So let us design one. The capability we want for FieldOps Copilot is a read-only incident lookup: given an identifier, return enough about that incident for the triage reasoning to reference it.

Five design decisions.

First, the name and description. The model chooses tools by reading these, so they are a discovery surface. Be specific about what the tool does and, just as importantly, what it does not do and when not to use it. "Retrieves a single incident by its identifier. Read-only. Does not search, does not list, does not modify. Use only when the report references a specific prior incident." That last clause prevents a whole class of unnecessary calls, which is a latency and cost saving as well as a reduction in surface area.

Second, the input schema. Constrain everything you can. An identifier with a format pattern, not a free-form string. If there were a field selector, an enumeration, not arbitrary field names. Every place you accept free text is a place a malformed or hostile value can arrive, and every place you accept an enumeration is a class of bad input that becomes structurally impossible rather than merely detectable. Also: fewer parameters is better. Each optional parameter is a decision the model can get wrong and a branch you must test.

Third, the output shape, and this is where most people are too generous. The instinct is to return the incident record. Do not. Decide what the triage reasoning actually needs — probably the title, the status, the category, the created date, and a truncated description — and return exactly that. Consider what you are excluding and why: internal operator notes, the reporter's contact details, any attached free text from other systems, anything belonging to another tenant. Each excluded field is a leak that cannot happen.

There are three reasons to be strict here. Everything you return enters the model's context, which means it enters the provider's systems, which is a data boundary question your customer already asked you about. Everything you return costs tokens on this call and every subsequent turn. And everything you return is available to be reflected back into the model's output, where an operator might see it — including in a scenario where the model was influenced to reflect it deliberately.

Fourth, errors. A tool error is not an exception to be thrown into the void; it is a result that goes back to the model. Make it structured and actionable: a stable code, a short human-readable explanation, and where appropriate, a hint about what would be valid. "The incident identifier was not in the expected format" lets the model correct itself. An unhandled crash tells it nothing and usually ends the turn badly.

There is a genuine tradeoff in the not-found versus not-authorized distinction. Telling the model "you are not authorized to view this incident" is more useful and more honest. It also confirms the incident exists, which leaks information across a boundary. For tenant boundaries specifically, prefer to return not-found — the cross-tenant existence of a record should not be discoverable. Within a tenant, an explicit authorization error is fine and more helpful. Decide it deliberately and write down why.

Fifth, determinism and side effects. A tool should be a function, not an adventure. Same input, same output, no state change, no surprises. Read-only tools should be safe to call repeatedly, because the model will sometimes call them repeatedly. If a tool has side effects, it needs idempotency, a human approval gate, or both — and for this chapter, it needs to not exist.

Which brings us to the most important design decision in the whole system, and it is a decision about what you do not build. There is no write tool. Not a disabled one, not one behind a flag, not one that exists but checks a permission. It is not in the codebase.

The reason is a principle worth stating on its own: absence of capability is stronger than restriction of capability. A restricted capability depends on the restriction being correct, and on it staying correct through every future refactor, and on nobody adding a configuration flag that flips it. A capability that does not exist depends on nothing. When your customer's security reviewer asks "what stops the AI from closing a ticket," the answer "there is no code path that closes a ticket from the model" ends the conversation. The answer "there is a permission check" starts a much longer one.

A short concrete note on why the description needs versioning, because it sounds like bureaucracy until you see it happen.

Suppose your description says the tool retrieves an incident by identifier and should be used when the report references a prior incident. Someone shortens it to "retrieves an incident by identifier," because the longer version felt wordy. Nothing else changes. No code changes. No prompt version changes, if you did not think of the description as part of the prompt.

What happens is that the model starts calling it more often, on speculation, because the guidance about when to use it is gone. Your latency per triage goes up by a round trip on a third of requests. Your token cost rises. Your audit log fills with lookups of identifiers that turned out to be order numbers. And nobody can explain it, because the diff that caused it does not look like a behaviour change.

So: the tool description carries a version, it is recorded on every invocation alongside the prompt version, and a change to it runs the fixture harness from chapter sixteen. Same artifact class, same governance. The only reason this feels different from the prompt is that it lives next to code instead of next to instructions, and that is an accident of file layout, not a difference in kind.

### Authorization at the tool boundary

Now the core. I am going to spend real time here because this is where systems get built wrong, and the wrong version looks completely normal.

Start with the question: when your tool executes, whose authority does it use?

The natural implementation is that the service calls its own internal function, or its own database, using the service's credentials. That works immediately, which is the problem. Think about what you have just built. The service can read every incident for every tenant — of course it can, it is the service. The model can now request any incident by identifier. The only thing between "the model asked for another tenant's incident" and "the model received another tenant's incident" is whether the model happens to ask.

You have built a confused deputy. The deputy is your tool executor: a trusted component with broad authority, taking instructions from a less-trusted source, and acting with its own authority rather than the requester's. This is a classic security flaw and it predates language models by decades. What is new is that the less-trusted source is now influenceable by anyone who can get text into the model's context — which, in our system, is anyone who can file an incident report.

The rule, and it is absolute: the tool executes with the authority of the human on whose behalf the request is being made, not with the authority of the service.

Concretely, for FieldOps Copilot. An operator is logged into the workspace. They trigger a triage suggestion on an incident. That operator's identity and scope — their tenant, their role, their permitted business units, from the authorization model you built in chapter twelve — travels with the request into the triage workflow, and into the tool executor. When the model requests an incident, the executor performs the lookup as that operator. If the operator could not open that incident in the user interface, the tool returns not-found. The model's request is just a request; the operator's permissions decide the answer.

Three implementation notes that make this real rather than aspirational.

Pass identity explicitly, as a parameter through the call chain. Not from a global, not from ambient context, not from a variable someone might forget to set. If your executor function cannot be called without an identity argument, then it cannot be called without one — the type system enforces your security property, which is the best kind of enforcement.

Apply the tenant filter in the data access layer, server-side, not as a condition your tool code remembers to add. The query that the tool issues should be incapable of returning another tenant's row, because the constraint lives below the tool. Chapter thirteen gave you the place to put it.

Use a scoped credential. Even with per-user authorization above it, the database identity your read tool uses should be read-only and limited to the tables it needs. Defence in depth: if the authorization check is bypassed by a bug, the credential still cannot write.

And one thing that is not an implementation note but a habit: authorize on every call. Not once at the start of the session. Not by deciding at prompt-assembly time which incidents the model may ask about. Every call, in the executor, freshly. A session can be long, permissions can change, and a decision made at the start of a conversation is a decision made before the attacker's input arrived.

Let me close this section with the test I want you to apply to every tool you ever build. Assume the model is entirely under the control of an adversary — assume someone wrote an incident description that turned it into their puppet. Now list everything it can do. If the list contains anything you would not let an anonymous internet user do with your operator's account, your boundary is in the wrong place. In our design the list reads: request incidents the operator can already see, and produce a suggestion the operator will read. That is a boring list, and boring is the goal.

### The Model Context Protocol

Now MCP, which is the standardization layer on top of everything we have just discussed.

The problem it solves is combinatorial. You have built an incident lookup capability. Your customer would like the same capability available from their team chat assistant, and from the coding agents their platform engineers use, and from a future vendor tool. Without a standard, each of those integrations is bespoke: different schema format, different transport, different authentication, different error conventions. Capabilities times clients, and you build every cell.

The Model Context Protocol is an open protocol that turns that into capabilities plus clients. You expose your capability once, from an MCP server. Any MCP-compatible client can discover and use it. The structure is straightforward: a host application runs one or more clients, each connected to a server. Servers expose three kinds of thing — tools, which are actions the model can invoke; resources, which are data the client can read into context; and prompts, which are reusable templates the user can invoke. Communication happens over a local process channel for servers running on the same machine, or over an HTTP-based transport for remote servers. Clients discover what a server offers by asking, so capabilities can change without the client being rebuilt.

For a forward deployed engineer, three things make this worth your attention.

It decouples capability from client, which is exactly the reusable-core-versus-customer-adapter split you established in chapter six. Your incident lookup becomes a piece of reusable product surface rather than a wire into one application.

It gives you a vocabulary for customer conversations. "We will expose a read-only incident capability over a standard protocol, and your existing assistant tooling can consume it under your identity provider" is a much better sentence than a description of a bespoke integration, and it makes the deployment feel less like a dead end.

And it sharpens the boundary. Because a server is a separate component with an explicit interface, the authorization discussion becomes concrete rather than diffuse.

Now the risks, which are real and which I think are under-discussed relative to the enthusiasm.

MCP makes it trivially easy to attach capabilities to an agent, including capabilities you did not write. A third-party MCP server is a dependency with runtime access to your context and, potentially, to your credentials. Everything from chapter seventeen about supply chain applies, plus more, because this dependency is not just code you run — it is a participant in your model's reasoning.

Specifically, four things to understand.

Tool descriptions are injected into your model's context. A malicious or compromised server can put instructions in a tool description, and those instructions arrive in the same channel as your own. This is prompt injection with a very convenient delivery mechanism, and it is sometimes called tool poisoning. The user never sees the description; they see a friendly tool name in a list.

Descriptions and schemas can change after you approved them. You review a server, you approve it, and later the server returns different definitions. If your client re-reads capabilities dynamically and you do not pin or re-review, the thing you approved is not the thing running.

Multiple servers share one context. A server you barely trust can describe its tools in a way that influences how the model uses a different server's tools — for example, by claiming that all lookups must first be passed through it. The model has no notion of which server is trustworthy; it has a list of capabilities that all look the same.

And credentials aggregate. An agent connected to five servers holds, in one process, the access those five servers were given. The blast radius of a compromise is the union, not the maximum.

So the controls, stated as rules. Treat every MCP server as a reviewed dependency with an owner and a version — vendor or pin it, do not float. Read the tool descriptions as you would read code, because functionally they are code. Re-review on change and alert when definitions shift. Do not connect servers with sensitive write access into the same agent as servers handling untrusted input. Scope each server's credentials to the minimum, separately. Require human approval for consequential calls, which for us is trivially satisfied because none of our calls are consequential. And for a customer deployment, prefer servers you or the customer control over convenient third-party ones, at least until the ecosystem's supply-chain hygiene matures.

For your test project, either build a small MCP server exposing your read-only lookup, or, if your runtime makes that awkward, write the contract stub precisely — the capability name, description, input schema, output shape, error codes, and the authorization model — so the shape is defined even if the transport is not. The learning objective is the contract and the boundary, not the wire format.

### One turn, walked through

Let me trace a single triage turn end to end, because seeing the sequence makes the control points obvious and it sets up the state machine we build next chapter.

An operator opens an incident in the workspace and asks for a triage suggestion. Your API receives that request, authenticates the operator, and resolves their scope — tenant, role, permitted business units. That resolved identity is now the authority for everything that follows, and it is passed explicitly, not stashed somewhere ambient.

Your triage adapter assembles the call: the versioned instruction, the policy configuration, the declaration of the one available tool, and the incident text in its single delimited data region. It records the prompt version and hash. It sends the request with a timeout and a maximum output length.

The model responds. Two possibilities. Either it returns a structured suggestion, in which case you validate it against the schema, check the category against the allowed set, and you are done. Or it returns a tool request.

Say it requests the lookup with an identifier it found in the description. Now the control points fire, in order. Increment the call counter and check it against the turn budget. Check whether this exact call was already made this turn; if so, return the cached note instead of re-executing. Validate the arguments against the schema. Resolve the operator identity — which you have, because it was passed in. Authorize: can this operator read this incident, in this tenant. Execute against the read-only credential, through a data layer that applies the tenant filter below your code. Project the result down to the five fields you decided on. Write the audit record. Format the result and append it to the context.

Then you call the model again, with the tool result included. It may return the suggestion, or it may request another tool call, and the loop repeats until it produces a suggestion, or the budget is exhausted, or the overall deadline passes.

Count the control points in that trace: turn budget, duplicate guard, schema validation, authorization, tenant filter, output projection, audit, timeout, and output validation. Nine. Every one of them is in your code. None of them is in the prompt. That is the shape you are aiming for, and if you ever draw this trace for your own system and find a step where the only thing preventing bad behaviour is an instruction, you have found your next piece of work.

Notice also what is missing: there is no decision in that loop about whether to take an action, because there are no actions. The loop only gathers and produces. That is what makes it safe to run without supervision, and it is what we will preserve next chapter when we add explicit states and an approval gate.

### Failing safely

Four failure modes and what each should do.

Malformed arguments. Validate against the schema in the executor, before any work. Return a structured validation error as a tool result. Do not throw into the generation loop. The model can often correct itself with a clear error, and if it cannot, you have a clean failure rather than a crash.

Unauthorized. Return the appropriate refusal — not-found across a tenant boundary, an explicit authorization error within one — audit it, and here is the crucial part: make sure the model cannot retry its way around it. Authorization is evaluated fresh on every call and does not depend on anything the model controls, so a hundred retries produce a hundred identical refusals. If rephrasing the request could ever change the outcome, your authorization is reading something it should not be.

Dependency failure or timeout. Every tool call gets a timeout shorter than the overall turn budget. On expiry, return a structured unavailable result so the model can proceed without that information — and make sure the reasoning path handles missing information by degrading to a less-grounded suggestion or to insufficient evidence, rather than by inventing the data it could not fetch.

Repetition. A model that gets an unhelpful result will sometimes call the same tool again, and again. You need a per-turn call budget — a hard maximum on tool invocations before the turn is terminated — and a duplicate-call detector that returns a short note rather than re-executing. Without these you have an unbounded cost loop wearing the costume of an agent. We will formalize the surrounding state machine next chapter; the budget belongs here, at the executor, because it must hold regardless of what the orchestration layer does.

### Auditing

Every tool invocation produces an audit record. Not the ones that succeed — every one, including refused and malformed calls, because the refusals are the interesting ones.

The record contains: the correlation identifier tying it to the originating incident and operator action; who it executed as; which tool and which version of its contract; a summary of the input with sensitive values redacted; the authorization decision and why; the result status; the latency; and the model and prompt versions from chapters fifteen and sixteen.

Three reasons this pays for itself. When a customer asks "what did your system look at," you answer from records rather than from memory. When you investigate a bad suggestion in chapter thirty-one, the tool calls are usually where the explanation is. And when a security reviewer asks how you would detect an attempt to cross a tenant boundary, you can show them the refusal records and the alert.

Redact on the way in, not on the way out. If a raw value never enters the log, it cannot leak from the log.

### Pitfalls

Eight.

Running tools with service authority instead of user authority. The big one. Every other mistake in this chapter is smaller than this one.

Putting the authorization rule in the tool description. "Only look up incidents belonging to the current tenant" is documentation. It is not a control.

Returning the whole record because it was convenient. Context cost, token cost, leak surface, all at once.

Building a write tool "for later." It will be reachable sooner than you expect, and its existence changes the answer you give in the security review.

Unversioned tool descriptions. Behaviour changes with no code change and no record.

No call budget. One unhelpful result becomes a loop becomes an invoice.

Treating a third-party MCP server as a convenience rather than a dependency with runtime access to your context and credentials.

Auditing successes only. The refused and malformed calls are the ones that tell you something is happening.

### How you verify this chapter

Six checks, all of them things you do rather than things you believe.

One. Search your codebase for any path by which a model-originated request can reach a write operation. There should be none, and the absence should be structural, not conditional.

Two. Construct a tool call, by hand, requesting an incident belonging to a different tenant. Confirm you get not-found, that the audit record exists, and that no timing or error-shape difference reveals whether the record exists.

Three. Remove the identity argument from your executor and try to compile or type-check. It should fail. If it succeeds, identity is optional, and optional identity eventually means absent identity.

Four. Call the tool with malformed arguments and confirm the model receives a structured error and can proceed, rather than the turn crashing.

Five. Drive a loop: make the tool return an unhelpful result repeatedly and confirm the call budget terminates the turn with a defined outcome.

Six. Hand your tool contract — name, description, inputs, outputs, errors — to another engineer and ask them to describe what it does and what it cannot do. If they need your implementation to answer, the contract is not doing its job.

### The test project

The companion guide is a test. Attempt it before the hints.

Your goal is a read-only incident lookup tool, exposed through an MCP-compatible adapter or a precise contract stub, that cannot mutate anything and cannot be talked around.

You will produce: a tool contract with a constrained input schema, a deliberately narrow output shape, and stable structured error codes. An executor that takes the operator's identity as a required argument and authorizes every call freshly against it, with the tenant filter enforced below the tool and a read-only credential beneath that. An MCP adapter or a precise stub. A refusal path for an out-of-scope request that returns a safe, actionable error. A per-turn call budget and a duplicate-call guard. And an audit record for every invocation, including refusals, with redaction applied before logging.

The constraints: no write tool exists anywhere in the codebase; the model's authority never exceeds the operator's; a malformed or hostile call cannot bypass authorization; and the contract is understandable without reading the implementation.

You are done when an adversary in complete control of the model can do nothing you would not let the operator do, and when you can demonstrate that with a test rather than assert it in a document.

### Recap

The decision from this chapter: you gave the model its first contact with a real system, as a request that your code authorizes, executes, and audits — never as an action the model takes.

The mechanics: the model emits a request; your executor decides. Every control lives in the executor. A tool is an endpoint and the model is an untrusted client.

The contract: constrain inputs with enumerations and patterns, return the minimum the decision needs, make errors structured and actionable, keep tools deterministic and side-effect free, and version the description because it is behaviour-changing configuration.

The security core: the tool runs as the human, never as the service. Authorize every call, freshly, in the executor, with identity as a required argument and tenant filtering below the tool. And prefer absence of capability to restriction of capability — there is no write tool.

MCP: a real advance in reusability and a real expansion of your supply chain. Tool descriptions are injected instructions, definitions can change after approval, servers share one context, and credentials aggregate. Treat each server as a reviewed, pinned dependency with an owner.

Next chapter we build the loop around all of this: the states, the transitions, the stop conditions, the approval gate, and an honest discussion of when a deterministic workflow is a better answer than anything calling itself an agent.
