---
chapter: 9
title: "Browser behavior with JavaScript and TypeScript"
roadmap_nodes: ["JavaScript / TypeScript", "JavaScript"]
part: "II — Build the customer-facing experience"
audio: media/09-javascript-typescript.mp3
voice: en-US-AndrewNeural
rate: "-15%"
companion_guide: docs/guides/09-javascript-typescript.md
---

# Chapter 9 — Browser behavior with JavaScript and TypeScript

[[Spoken narration begins below. Headers and this note are stripped before rendering.]]

## Orientation

Chapter nine. You have a page that means something and looks like something. Now it has to do something.

Here is the state of the build. The intake page collects five fields with real labels, real grouping, and real error messaging. It is keyboard operable. It has a token-based visual layer where every state has a text cue and a non-colour cue, and it survives greyscale and high zoom. And it still, honestly, does nothing: submitting shows the operator what they typed, and says so.

In this chapter you close that gap halfway. You will define one typed representation of an incident, replace the local confirmation with an asynchronous submission that talks to a mock service shaped exactly like the real one, and handle the four states every network request has. You will make it impossible to submit twice by accident. And you will establish a rule that governs everything from here to the end of the course: the browser is a courtesy layer, the server is the authority.

Two things this chapter is not. It is not a framework chapter — no components, no router, that is chapter ten. And it is not a real backend — the service is a mock you control, because building both sides at once means debugging both sides at once, and one of the more valuable habits in field work is refusing to do that.

By the end you will understand the browser's execution model well enough to reason about race conditions, know precisely what static types do and do not protect you from, be able to model asynchronous state so that impossible combinations cannot be represented, and have tests that survive your own refactoring.

## What JavaScript is, in the browser

Let me build this up properly, because the two or three concepts that engineers skip here are exactly the ones that produce the bugs that only appear at a customer site.

JavaScript in a browser runs on a single thread for your code. There is one call stack. When your code is running, nothing else of yours is running: no event handler fires in the middle of your function, no timer interrupts you. That property is a gift — you get no data races within a task — and it is also the source of the constraint that if you do something slow, the interface freezes, because rendering and input handling share that thread.

Work gets scheduled through an event loop. The loop takes a task, runs it to completion, then handles a queue of smaller follow-up jobs, then lets the browser render, then takes the next task. Events, timers, and completed network responses all arrive as tasks. The follow-up queue is where promise continuations run. The practical consequences: your code always runs to completion before the next handler, anything awaited resumes later even if the value was already available, and the interface can only repaint between tasks — so a long synchronous loop means a frozen page and an operator hammering a button.

Events. The document dispatches events, you register listeners, and the event travels down and back up the tree, which is why you can listen on a container and handle events from its children. Two behaviours matter for forms. A form submission event is cancellable, and cancelling it is how you take over submission yourself. And the same event carries a reference to the form, which is a much better source of values than reading each control individually.

Then asynchrony. A promise is a value that will exist later, or an explanation of why it will not. The comfortable syntax marks a function as asynchronous and lets you await promises inside it, so the code reads sequentially while actually suspending and resuming. Two things to internalise. First, an asynchronous function always returns a promise, so calling it without awaiting or otherwise handling it gives you a promise nobody is watching — a floating promise — and if it rejects, the failure surfaces as a global unhandled rejection at some unrelated moment, or nowhere at all. Second, awaiting suspends only the current function; the rest of the world keeps going, which is precisely how two overlapping submissions become possible.

Network requests. The browser gives you a request function that returns a promise for a response. Two traps worth knowing before you meet them. It does not reject for server error responses — a rejection means the request could not be completed at all, while a response saying the server refused your input is a perfectly successful request that you must inspect. And it does not time out on its own; if you want a deadline you attach a cancellation signal and abort it yourself, otherwise a customer with a flaky connection gets a spinner forever.

Modules. Modern browser code is organised as modules that explicitly export and import. Each module has its own scope, so you are not decorating a shared global object, and dependencies are visible in the file rather than implied by script ordering. Use them from the start. This is also what makes the chapter ten refactor tractable, because a module boundary is the natural seed of a component boundary.

And serialisation. What crosses the network is text. Objects get encoded on the way out and decoded on the way in, and the encoding is lossy in specific ways: a date becomes a string, an undefined value can vanish, a map or set becomes an empty object, and very large integers lose precision. Every one of those has bitten a real system. Decide the wire representation of each field deliberately — for our incident record, timestamps as an unambiguous text format, severity as a stable code rather than a display label — and convert at the boundary.

## What TypeScript is, and the one thing it is not

Now the typed layer, and I want to be precise here because the most consequential misunderstanding in this whole course lives in this paragraph.

TypeScript is JavaScript plus static type annotations, checked before your code runs and then erased. What ships to the browser has no types in it. Nothing about a type annotation inspects a value at runtime.

Which means: types do not validate data. If you declare that a response is an incident, and the server sends something else, your program will carry on with a value that violates its own declared type, and the failure will surface later, somewhere unrelated, as a confusing error. The type system protected the code you wrote against yourself. It did not protect you against the network.

So the rule at every boundary — network responses, form values, stored data, anything from outside your program — is: receive it as unknown, check its shape at runtime, and only then treat it as your domain type. This is often called parse, don't validate: rather than checking a value and continuing to treat it as loosely typed, you convert it once into a trusted shape and work with that. You can hand-write those checks, or use a schema library, and in chapter twelve you will generate types from the published contract instead of hand-maintaining both. For this chapter, hand-written is fine, and doing it by hand once is genuinely instructive.

What types are excellent at is the other half: making your own state impossible to get wrong.

TypeScript types are structural — compatibility is about shape, not about declared lineage. And the feature that matters most for us is the tagged union: a type that is one of several alternatives, each carrying a marker field, so that checking the marker tells the compiler exactly which other fields exist.

Use that for request state. The naive approach is a bag of booleans and optionals: a loading flag, an error string, a result object, a submitted flag. Count the combinations that bag can represent. Loading and error at once. Result present while loading. Error present with a result. Nothing set at all. Most of those are nonsense, but nothing stops you from creating them, and every one of them eventually renders as a spinner sitting on top of an error message, which is the single most common broken-looking state in enterprise web tools.

Model it instead as one value that is exactly one of: idle; submitting; succeeded with a created incident; rejected with a list of field errors; or failed with a message. Five named states, mutually exclusive, each carrying precisely the data that state needs and nothing more. The interface then renders one of five things, the compiler tells you if you forget one, and the impossible combinations no longer exist as values. This single technique removes more interface bugs than any framework choice you will make.

Turn on the strict settings, including the one that flags implicit loose typing and the one that treats null and undefined as distinct possibilities. And treat the loose escape-hatch type as a code smell that needs a comment justifying it. Every use of it is a place where you asked the compiler to stop helping.

## Rendering safely: the document as an API

One more piece of vocabulary before the field argument, because it is where the security failures of this chapter live.

Your script can read and modify the document at runtime. That capability comes in two flavours, and the difference matters enormously. You can create elements and set their text content, which treats whatever you provide as literal text. Or you can hand the browser a string of markup and ask it to parse and insert it, which treats whatever you provide as instructions.

The second one is how cross-site scripting happens. Consider your confirmation region echoing back the operator's description. Now consider a description containing something that looks like markup with a script in it. If you inserted that text as markup, you just executed a stranger's code inside your application, with your application's access. In a customer deployment, that is not defacement, it is a path to whatever the logged-in operator can reach, which after chapter twelve includes an authenticated session.

The rule is simple and absolute: content that came from a human or from a network response is set as text, never as markup. If you genuinely need rich formatting, you sanitise with a real library, and you write down why. And note that this threat does not go away when you move to a framework in chapter ten — frameworks escape by default, which is a big part of their value, but every one of them has an explicit escape hatch that reintroduces the hazard, and someone always reaches for it to render a formatted description.

While we are in the document: two behaviours from chapter seven need reconnecting now that content changes dynamically.

First, announcements. When you replace the confirmation region's content, a sighted user sees it immediately and a screen reader user may hear nothing, because nothing moved focus and nothing told the assistive layer that this region reports updates. Mark the region as one that announces its changes politely, so status text and result summaries are spoken. Use the assertive variant sparingly — it interrupts — and reserve it for something that genuinely must interrupt.

Second, focus on state change. When a submission fails, focus goes to the error summary, exactly as in chapter seven. When it succeeds and you swap the form for a confirmation, focus has to go somewhere sensible, because if you remove the element that had focus, focus falls to the document and a keyboard user is dumped at the top with no explanation. Decide where focus lands in each of your five states. This is a two-line decision that separates tools that feel finished from tools that do not.

Third, a smaller one: read your values from the form element rather than reaching for each control individually. It is less code, it stays correct when you add a field, and it forces you to have given every control a proper name — which, conveniently, is the same discipline the server will depend on in chapter eleven.

## Tooling: how typed code becomes browser code

A short practical note, because this is the first chapter where you need a build step and I do not want you to over-build.

Browsers do not execute type annotations. So something has to remove them. You have three reasonable options and I want you to choose consciously rather than by habit.

You can run the type checker purely as a checker and ship plain JavaScript modules that you wrote yourself, with types in separate declaration comments. This keeps the shipped code identical to the source, which is wonderful for debugging at a customer site, and it is awkward to maintain.

You can use a compiler to strip types and emit modules, with no bundling at all, and load those modules directly in the browser. This is my recommendation for this chapter. It is one command, the output maps almost line for line to your source, and there is no bundler configuration to explain to anyone.

Or you can adopt a full build tool with a development server, bundling, and hot reloading. That is where you will end up in chapter ten, and it is the right choice then, because a component framework effectively requires it. Today it is more moving parts than the problem needs.

Whichever you pick, two requirements. Generate source maps, so that an error in the browser points at the line you wrote rather than the line a tool produced — without them, diagnosing a problem on a customer's machine is guesswork. And make the type check a separate, explicitly runnable step, not something implied by the build, because in chapter twenty seven a pipeline needs to run it as its own gate and report its own failure.

One warning about dependencies, which chapter seventeen will revisit. Every package you add to browser code becomes part of what you ship, part of what a security reviewer examines, and part of what someone must update when a vulnerability is announced. For this chapter you need approximately nothing: a type compiler and a test runner. Resist the date library, the utility library, and the validation library until you can name the specific problem it solves better than twenty lines of your own code.

## Why a forward deployed engineer cares

Three reasons, all of which I have watched play out.

The first is where business rules live. Suppose you compute the priority in the browser, because you already have the rule from chapter three and it is right there. It works. It demos beautifully. Then chapter eleven arrives and the server computes priority too, and for a while both agree. Then the customer asks for a routing tweak — business unit A treats degraded service as critical — and somebody updates one of the two implementations. Now the operator sees one priority and the record stores another, and the audit trail in chapter thirteen disagrees with the screen. That is not a theoretical risk; it is the most common divergence bug in customer-facing systems. So the rule is: the browser may compute a hint, clearly labelled as a preview, but the displayed authoritative value is the one the service returned. One policy, one owner.

The second is what happens under real network conditions. Your development machine talks to a mock in under a millisecond. A customer's operator is on hotel wifi, a congested site network, or a mobile connection in a basement. On those connections, requests take seconds, arrive out of order, and sometimes never complete. Every state you did not model becomes visible: the double submission, the spinner that never stops, the stale response overwriting a newer one, the operator's twenty-line description lost because your error path re-rendered the form empty. Enterprise users are, in my experience, extremely tolerant of a slow tool and extremely intolerant of a tool that loses their work.

The third is trust in error messages. When a field tool fails, someone has to decide whether to retry, escalate, or work around it. That decision comes from your error text. Unexpected error tells them nothing and trains them to distrust every message you write. We will build an error taxonomy in a moment precisely so each failure produces a different, actionable sentence.

There is a fourth reason that is specific to working with a mock, and it is worth naming because it is a trap I have fallen into. A mock you invented is a contract you invented, and if you invent it casually, chapter eleven becomes a rewrite instead of a substitution. The way to avoid that is to write the contract down as a document before you write the mock — the success shape, the rejection shape, the failure shape, the status meanings — and treat the mock as an implementation of that document. Then, when the real service arrives, the question is whether the service matches the document, which is a testable question with a clear owner. Without the document, you get the classic field failure where the interface was built against an imagined server, and the integration week turns into an argument about who changed what.

Related: give the mock a visible marker in the interface. A small persistent label saying this build is using a simulated service costs nothing and prevents the demo disaster where a stakeholder concludes the backend exists. I have seen a customer report upward that a system was integrated because a screen looked like it was. Once that belief exists, correcting it costs you credibility you did not spend.

There is a security dimension too, which chapter thirty two will formalise but which starts here. Everything in the browser is visible to the user: your code, your configuration, every value you log. So no credentials in browser code, ever. No sensitive incident content written to the console. And no assumption that a check you performed in the browser was actually performed, because the person on the other side may not be cooperating.

## How to do the work

Here is the sequence, with the reasoning.

Start with the domain type. Write one representation of an incident and give it a home — its own module — because it is about to be imported by the submit function, the confirmation renderer, the tests, and later the components. Decide two shapes, not one: the draft that intake produces, and the created incident the service returns. They differ, and the difference is instructive: the created one has an identifier, a server timestamp, a status, and the authoritative priority. Keeping them distinct means the compiler stops you from displaying a priority you invented.

Also decide your severity representation now. A stable code that will not change when someone edits a label, plus a display label looked up separately. If you skip this, you will eventually have a customer who renames critical to priority one, and your data becomes a mixture of two vocabularies.

Second, define the mock service, and define it by its contract, not by convenience. Write down what a successful creation returns, what a validation rejection looks like — which should be a list of field-and-message pairs so the interface can attach each message to the right control — and what an unexpected failure looks like. Then implement the mock behind a function with the same signature the real one will have. This is the seam. In chapter eleven you replace the implementation and nothing else changes, and that is the whole reason for doing it this way.

Give your mock a deliberate delay of a few hundred milliseconds, and give it a way to produce each failure mode on demand — a particular title that triggers a rejection, another that triggers a server error, another that never resolves. You cannot test states you cannot produce, and building the fault injection into the mock takes minutes now versus contortions later.

Third, write the submit path. Take over the form's submission event, read the values from the form itself, build the draft, and hand it to the service function. Then handle the outcome by moving your one state value between the five states we discussed, and render from that state.

Guard against concurrency explicitly. If the state is submitting, ignore further submissions — do not merely disable the button visually, because a fast double press can land before the re-render and because keyboard activation can bypass your assumptions. And decide what happens if a response arrives for a request you no longer care about. The clean pattern is to keep a token or an abort controller for the current request and ignore anything that does not match, because on a slow connection an out-of-order response overwriting fresh state is a genuinely confusing bug to diagnose from a support ticket.

Attach a deadline. Pick something defensible — for an intake submission, perhaps ten seconds — and when it expires, abort and tell the operator what to do. Which brings us to the taxonomy.

Fourth, the error taxonomy. Give each of these a distinct, honest message.

A validation rejection is expected and is the service telling you the record is wrong. Attach each message to its field, focus the summary, and keep every value the operator typed. Nothing about this is an error in the engineering sense, and the wording should not alarm.

A transient network failure is a request that could not complete. The message should say the record was not saved and invite a retry. It is safe to retry because nothing was created.

A timeout is the one that requires care, because you genuinely do not know whether the server processed the request. Say so, honestly: the message should tell the operator to check the incident list before resubmitting. In chapter thirteen you will add an idempotency key so a retry cannot create a duplicate, and this is the moment you understand why that key exists.

An unexpected server failure is a defect. Tell the operator the system had a problem, that their input was preserved, and give them a reference identifier they can quote. Do not display internals. Do log it with enough context to find it later, which is the observability thread we pick up in chapter thirty one.

And offline is worth its own case, because the browser tells you about it and because the right message is different: you are not connected, your text is safe, try again when you have a signal.

Fifth, testing. Test three things, and skip the rest for now. Test the pure functions — the shape conversion, the validation, the runtime shape check — because they are cheap and total. Test the submit path with a fake service, once for success and once for a recoverable failure, asserting on what the operator would perceive rather than on internal variables. And test that a second submission during a pending one does not produce a second call, because that is the bug most likely to reappear during the chapter ten refactor.

Find things in your tests the way a person describes them: the control labelled severity, the button named submit, the region announcing the result. Those queries are stable across restyling and across the component rewrite, and they double as a check that the accessible names you built in chapter seven still exist. Tests bound to internal structure will all break in chapter ten and teach you nothing.

Finally, wire type checking into your verification. A type error should fail your check the same way a failing test does. In chapter twenty seven this becomes a pipeline stage; today it is a command you run before you claim to be done.

## Pitfalls, named

Types treated as validation. Already covered, and worth repeating because it is the one that produces the most baffling production failures. Any value from outside the program is unknown until you have checked it.

The loose escape-hatch type at the boundary. Declaring incoming data as loosely typed silences the compiler exactly where you needed it most. Receive as unknown, narrow deliberately.

Floating promises. An asynchronous call whose result nobody handles. It will fail silently one day, usually the day of the demo.

Stale captured state. A handler created earlier that closes over an old copy of your state and writes a decision based on it. This produces the classic bug where a retry uses the values from two submissions ago. Read state at the moment you act, and be suspicious of any handler that survives across state changes.

Out-of-order responses. Two overlapping requests, the slower one landing last and winning. Track the current request and discard the rest.

Losing the operator's input on failure. Never re-render the form empty on an error path. Their description is the most expensive thing on the screen.

Errors delivered through a browser dialog. Blocking, unstyled, unlocatable by assistive technology, impossible to include in a screenshot with context. Render errors in the page, in the region you designed in chapter seven.

Swallowed errors. A catch block that does nothing, or logs and continues as though it succeeded. If you cannot handle a failure, surface it.

Console logging sensitive content. Incident descriptions may contain customer names, addresses, account numbers. The console is a log the user can read, and screen sharing is common in field work. Do not put content there.

Secrets in browser code. There is no such thing as a secret in a browser bundle. If a value must be private, it lives on the server, and chapter twelve is where that boundary gets built properly.

Trusting the client clock. Machines are wrong, time zones lie, and users change their clocks. Timestamps of record come from the server.

Serialisation surprises. A date that becomes a string and is then treated as a date. Decide the wire format, convert at the boundary, and never let a parsed value wander into your domain unconverted.

Reaching for a state management library. You have one form and five states. A tagged union in a module is the right size. Adding a library now means a customer's engineer must learn it in order to fix a typo.

Validating on every keystroke. Now that you have scripting, the temptation returns. Same answer as chapter seven: validate on submission, re-check a field when it is left, clear errors as soon as they are resolved.

## Verifying your work

Six checks.

Throttle the network in your browser's developer tools to something slow, and use the tool. Watch what the operator sees for the two or three seconds when nothing has come back. Is there a visible pending state? Is it announced, not just drawn? Can they still read what they typed?

Exercise every failure mode through your mock. All five states must be reachable and each must produce distinct, actionable text. If you cannot reach one, your mock lacks the fault injection and that is itself a finding.

Double submit deliberately. Click twice fast, then press enter twice fast, then click while a keyboard activation is in flight. Count the calls. The answer must be one.

Go offline in developer tools and submit. Confirm the message names the connection as the problem and confirm no input was lost.

Inspect the request in the network panel. Is the payload exactly the shape your contract says? Are severity and impact stable codes rather than display strings? Is anything in there that should not be — a browser-computed priority, a stray internal field, anything sensitive?

Run the type check and the tests together, from a clean state, and note the command in your readme. In chapter twenty seven a machine will run exactly this.

One more, cheaper than all of them: read your own error messages aloud, imagining a tired operator at the end of a shift. If any of them would make you shrug, rewrite it.

## Your practice test

The guide has the rubric. Spoken version:

Your goal is to make the intake page's behaviour typed and asynchronous against a mock service, with all five request states handled and no possibility of an accidental double submission.

Your constraints: no user interface framework — that is next chapter. One shared typed representation of an incident, in its own module, with distinct draft and created shapes. All data crossing the boundary is checked at runtime before being treated as a domain value. Request state is modelled as a tagged union, not a collection of booleans. The displayed priority is the value the service returned; any browser-side calculation must be labelled a preview or removed. Every failure mode is reachable through fault injection in the mock, and each produces distinct actionable text. The operator's input survives every error path. A deadline exists on the request. And the chapter seven accessible names and error handling must still work — you are enhancing, not replacing.

Your artifacts: the typed domain module; the service seam with its mock and its fault injection; a short note documenting the contract you are coding against, including the rejection shape; a note listing each of the five states with the exact sentence the operator sees and why it is actionable; tests for one success, one recoverable failure, and the double-submit guard; and one paragraph recording which browser-side check is a courtesy and what will enforce it on the server.

You are done when a second submission during a pending request produces no second call, when all five states render correctly and are announced, when no input is lost on any error path, when the payload on the wire matches your documented contract, and when the type check and tests both pass from a clean run.

## Recap

Five things.

First, the browser runs your code on one thread through an event loop. Awaiting suspends your function, not the world, and that is why overlapping submissions and out-of-order responses are real rather than theoretical.

Second, types are erased. They protect your code from you; they do not protect you from the network. Parse at every boundary.

Third, model asynchronous state as one value with named alternatives. Impossible combinations should be unrepresentable, not merely unlikely.

Fourth, the server is the authority. The browser may hint, clearly labelled. One policy, one owner, no divergence.

Fifth, an error message has one job: tell the operator what to do next. And a timeout is the honest case where the right answer is check before you retry — which is why chapter thirteen gives us an idempotency key.

In chapter ten we take this working, typed, asynchronous page and break it into components with real boundaries, add an incident list and a detail route, and confront where state should live. Build this first. Then meet me there.
