---
chapter: 10
title: "React and frontend application structure"
roadmap_nodes: ["React", "Frontend Apps"]
part: "II — Build the customer-facing experience"
audio: media/10-react-frontend-apps.mp3
voice: en-US-AndrewNeural
rate: "-15%"
companion_guide: docs/guides/10-react-frontend-apps.md
---

# Chapter 10 — React and frontend application structure

[[Spoken narration begins below. Headers and this note are stripped before rendering.]]

## Orientation

Chapter ten, and the last chapter of Part Two. This is where FieldOps Copilot stops being a page and becomes an application.

Where we stand. You have an intake page that is semantic, styled with a token layer, typed, and asynchronous against a mock service whose contract you wrote down. Five request states are modelled as one value. Double submission is impossible. Nothing is lost on an error path. That is a genuinely respectable piece of work, and it is also about to hit a wall, for a reason that has nothing to do with quality.

The wall is this: a pilot does not stay one screen. Within two weeks of a customer seeing an intake form, somebody asks to see the incidents that were submitted. Then somebody asks to open one and change its status. Then a manager asks for a filtered view of critical items. Then the security reviewer asks whether an operator can see another business unit's incidents. Each of those is a new surface that shares most of its logic with the ones before it, and hand-managing document updates across four screens is where handwritten frontends go to die.

So in this chapter you rebuild the intake experience as a React application with an incident list and an incident detail route, and you make the structural decisions that determine whether the next five screens are cheap or expensive. You will rebuild the form from scratch as components — not port it mechanically — because the exercise is learning where the boundaries belong.

Two constraints stay in force. The service is still the mock from chapter nine, behind the same seam. And everything you established in chapters seven, eight, and nine must survive: the accessible names, the error summary that receives focus, the redundant state encoding, the five-state request model, the impossibility of double submission. If a framework rewrite loses those, the framework was not the problem.

## What React is

Let me define it in a way that makes the rest of the chapter follow.

React is a library for describing an interface as a function of state. You write functions that take data and return a description of what should be on screen. When the data changes, you do not mutate the document; you let React call your functions again and work out the minimal set of changes to apply. That inversion is the entire idea. In chapter nine you told the document what to change. Here you describe what should be true, and something else figures out the changes.

The unit is a component: a function that receives a single object of inputs, conventionally called props, and returns a description of output. Props flow downward, they are read-only from the child's perspective, and that one-directional flow is what makes a large interface reasonable to think about — when something on screen is wrong, the cause is above it, not beside it.

State is data a component owns and can change, declared through a hook that gives you the current value and a function to replace it. Setting state schedules a re-render. Two consequences people trip over. Updates are batched and applied later, so reading the state variable immediately after setting it gives you the old value — if the next value depends on the current one, describe the update as a function of the previous value rather than reading and writing. And state is identified by its position in the component tree, which is why hooks must be called unconditionally in a stable order, and why conditional hook calls are forbidden rather than merely discouraged.

Effects are the escape hatch for synchronising with things outside React: a network request, a subscription, a timer, the document title. An effect runs after render, can declare what it depends on, and can return a cleanup function that runs before the next execution and on unmount. And here is the thing I most want you to take from this chapter: most effects that engineers write should not exist. If you are using an effect to compute a value from other values, that is not synchronisation, that is a calculation — do it during render. If you are using an effect to copy a prop into state, you have created two sources of truth that will drift. Effects are for reaching outside; everything else is a function of what you already have.

Keys. When you render a list, each item needs a stable identity so React can tell insertion from reordering from replacement. Use the incident's identifier. Do not use the array position — it is the single most common cause of the bug where you delete one row and the input state from a different row appears in the wrong place.

Controlled and uncontrolled inputs. A controlled input has its value driven by state, with every keystroke flowing through your code. An uncontrolled input keeps its own value and you read it when you need it. Controlled gives you live validation and derived behaviour at the cost of more re-rendering and more code; uncontrolled is simpler and works closer to how the platform behaves. For an intake form where you validate on submission — which is what you decided in chapter seven — uncontrolled is a perfectly professional choice, and it makes the form dramatically smaller. Choose deliberately and write down why.

Context. A mechanism for passing a value to a deep subtree without threading it through every level. It is the right tool for a small number of genuinely ambient things: the current user and their role, a theme, a service client. It is the wrong tool for application data that changes often, because every consumer re-renders when it changes, and because it makes data flow invisible — which is exactly the property that made props worth having.

Finally, error boundaries. A component that catches a rendering failure in its subtree and shows a fallback instead of a blank page. Without one, a single unexpected undefined value in one row of your incident list takes down the entire application and the operator sees white. In a customer deployment, white screens generate phone calls.

## What a frontend application is, structurally

Now the second half of this chapter's title, which is less glamorous and more consequential.

An application is not just more components. It has four structural concerns, and if you name them now you will not have to untangle them later.

The first is the shell. One layout that owns the frame: the identifying header, the primary navigation, the region where the current view renders, an error boundary, and any global announcement area. Everything else lives inside a slot in the shell. Building it explicitly means adding the fourth screen requires no layout thought at all.

The second is routing. A route maps a location to a view, and this is where I want to make a claim stronger than most tutorials make: the location bar is application state, and treating it as such is an operational feature, not a nicety. When an operator can send a colleague a link that opens exactly one incident, your tool joins their existing workflow — chat, email, the customer's own ticket system, the incident review meeting. When it cannot, every handoff becomes a spoken instruction to click three times. So: the incident detail route carries the incident's identifier in the location. Reloading it works. Opening it in a new tab works. The back button does what a person expects. Filters that a manager will want to share belong in the location too.

The third is the data layer, which for us is the service seam from chapter nine, now used by more than one view. Keep it as a module of functions that speak in domain types, with all parsing at the boundary. Views call those functions; views do not know about transport. That separation is why chapter eleven will be a substitution rather than a rewrite, and it is where chapter twelve's authorisation headers will be added exactly once.

The fourth is state ownership, and this is the decision that most determines whether your application ages well. Sort every piece of state into one of four categories and put it in the matching place.

Server state is data that lives authoritatively somewhere else and that you are holding a copy of: the incident list, one incident's detail. It is a cache, and it has properties caches have — it can be stale, it needs refreshing, it can fail to load. Own it in the view that displays it, at least until you have a reason not to.

Location state is anything that should survive a reload or be shareable: which incident is open, the active filter, the sort order, the page number.

Interface state is genuinely local and ephemeral: whether a disclosure is expanded, whether a menu is open, which field has an inline error showing.

Form state is the values being edited before submission, plus the five-state request model from chapter nine. It belongs to the form, and it should not be lifted anywhere unless something outside the form actually needs it.

Then apply the rule: put state in the narrowest scope that needs it. Lift only when a second component genuinely requires it, and lift to the nearest common ancestor, not to the top. The failure mode this rule prevents is the application where every value lives in one global store, every change re-renders everything, and no component can be understood or tested in isolation.

One more structural note: organise files by feature rather than by kind. A folder for intake, a folder for incidents, a folder for shared primitives beats a folder of all components, a folder of all hooks, and a folder of all types. Feature grouping means a change to intake touches one directory, and it means a customer-specific screen — remember the adapter category from chapter six — can live in its own folder and be identified as customer-specific at a glance.

## What actually happens when state changes

A short mechanical detour, because a handful of confusing behaviours all come from one process and it is easier to learn once than to be surprised by five times.

When state changes, React calls your component function again, and the functions of its children, producing a new description of the interface. It then compares that description with the previous one and applies only the differences to the document. Two words to keep separate: a re-render is your function running, and it is cheap; a document update is the browser changing what is on screen, and it is comparatively expensive. React re-renders liberally and updates minimally. This is why the instinct to prevent re-renders is usually misplaced — you are optimising the cheap half.

The comparison relies on identity. Within a list, identity comes from the key you supply, which is why a stable identifier matters. Across renders, a component keeps its state as long as it stays in the same position with the same type; move it to a different position or change its type and its state is discarded and rebuilt. This explains an otherwise baffling class of bug where switching between two views resets a form, or where conditionally wrapping a subtree wipes its state. If state disappears when you did not expect it to, ask what changed about that component's position or type.

Updates are batched. Several state changes inside one handler produce one render, not several. And because the new value is not visible until the next render, an update that depends on the current value must be expressed as a function of the previous value. Get this wrong and you get the classic bug where two rapid increments produce one.

In development, React may deliberately invoke your components and effects twice to surface impurity. This is not a bug and you should not work around it. It is telling you something true: a component function must be a pure calculation, and an effect must clean up after itself well enough that running it twice is harmless. If double invocation breaks your code, your code would also have broken under a real interruption in production — for example, two rapid navigations. Fix the impurity.

Finally, rendering is synchronous from your perspective but the browser only paints between tasks, which means an expensive render blocks input exactly as it did in chapter nine. A list of two hundred incidents rendering slowly is not a React problem, it is the same single-thread constraint, and the answers are the same: do less work, or do it less often.

## Choosing the frontend application shape

The roadmap names frontend applications as its own topic, and the reason is that React by itself is not an application architecture. You have to choose the shape around it, and for a customer deployment the criteria are different from the ones a public product would use.

Your two realistic options. A client-rendered application built with a modern build tool, producing static files that any web server can serve. Or a meta-framework that renders on a server, with routing, data loading, and server-side rendering built in.

For a public marketing site, the server-rendered option wins easily — search visibility, first-paint performance on unpredictable devices, sharing previews. For an internal operational tool behind authentication, almost none of those benefits apply. Search engines will never see it. The users are on a corporate network. Nothing is shared publicly.

Meanwhile the costs are real. A server-rendered application requires a running server process, which is one more thing to deploy, monitor, patch, and explain to a customer's platform team in chapter twenty nine. A client-rendered application is a directory of static files that can be served from almost anything, including a storage bucket, an existing internal web server, or the same container as your interface layer. In an environment with restrictive networking or an approval process for every new runtime — which describes a great many enterprises — that difference decides the project.

So for FieldOps Copilot I would choose the client-rendered build. Not because it is technically superior, but because it minimises what the customer's platform team must accept, and in field work the deployment surface you ask for is a negotiation you have to win. Write that reasoning down as a decision record. And note the conditions that would change the answer: if the customer needed the tool to load meaningfully on very slow devices, or wanted deep integration with server-side session handling, or already ran the relevant framework in production, server rendering becomes the better fit.

One thing you get for free from that choice, and should exploit: because the interface is static files, the interface and the service can be versioned and deployed separately. That means a styling fix does not require redeploying the service, which matters more than it sounds when a customer has a change-approval process measured in days. It also means you must think about compatibility between an older interface and a newer service, which is exactly what chapter twelve's versioned contract is for.

## Why a forward deployed engineer cares

Four arguments.

The first is the rate of change in a pilot. In the field, the interface is the part the customer sees, so it is the part they ask about, and the requests arrive weekly. A component model with clear state ownership means the fourth screen costs a fraction of the first. A hand-managed document means the fourth screen costs more than the first, because now four screens must be kept consistent. Adopting a component model is not fashion; it is a decision about the cost curve of the next three months of requests.

The second is duplication of the dangerous kind. Form logic is where duplication hurts most, because forms encode policy: which fields are required, what the severity vocabulary is, what an error says. When a second form appears — a status change form, a bulk update — the temptation is to copy the first. Then the customer renames a severity level, and one of the two forms still uses the old vocabulary, and now your data has two vocabularies. Extracting the field components and the vocabulary once, in this chapter, is what prevents that.

The third is the handoff, which is the argument most engineers underweight. At some point this system stops being yours. A customer's internal team, or a colleague who has never met the customer, will maintain it. That means your structural choices should be boring and legible: a widely used framework, conventional routing, state held close to where it is used, no clever abstraction with a private vocabulary. I would rather hand over a slightly repetitive application that a competent stranger can read than an elegant one that requires me on a call. Chapter thirty seven makes this explicit as a deliverable; chapter ten is where you either earn it or lose it.

The fourth is that the empty, loading, and error states are the product. In a demo, the incident list has six well-chosen incidents. On day one at the customer, it has zero, and the operator's first experience of your tool is an empty region. If it says nothing, they conclude it is broken. If it says no incidents have been reported yet, and here is how to report one, then the empty state has just done the onboarding that you were going to write a document for. Similarly, if the list fails to load and the screen is blank, the operator has no idea whether to retry, whether their data is gone, or whether to call someone. These states are not polish applied at the end; they are three of the four things the operator will see most often.

## How to do the work

The sequence I recommend, with the reasoning.

Start with the shell and the routes, before any components. Decide the two locations: a list of incidents, and one incident's detail identified in the location. Build the shell with a header, navigation, a content slot, and an error boundary around the slot. Get navigation working with placeholder views that say nothing but their own name. Ten minutes of work, and it means every subsequent decision has a home.

Then decide your component boundaries by looking at what repeats and what varies. For this stage I would expect a handful: a severity indicator that renders the state recipe from chapter eight; a status indicator; an incident row for the list; the intake form; a labelled field wrapper that owns the label, the help text, the error message and their programmatic associations; a page-level empty state; a page-level error state with a retry action.

That labelled field wrapper deserves a comment. It is the highest-value component in this chapter, because it is where chapter seven's accessibility work becomes reusable instead of repeated. One component that guarantees a label is associated, help text is attached as a description, an error is attached and the control is marked invalid — and then every future form in the system inherits correctness rather than re-deriving it. That is what a design system actually is, underneath the visual layer: correctness you cannot forget to apply.

Then rebuild the form. From scratch, as I said. Type its props. Decide controlled or uncontrolled and record the reason. Keep the five-state request model exactly as it was, now as state inside the form component, and keep the guard that makes double submission impossible. Keep the error summary and keep the focus move — in React, that focus move is a legitimate effect, one of the few, because it is synchronising with something outside React's model.

Then the list. Fetch through the service seam, model the fetch with the same discipline as the submission: loading, loaded with items, loaded but empty, failed. Note that loaded-but-empty is a distinct state from loading, and conflating them is how you get a spinner that looks like it is stuck. Render rows with the incident's identifier as the key. Make each row's primary action a real link to the detail location, not a click handler on a container — so that opening in a new tab works, so that the accessible name of the link describes the incident, and so the keyboard path is the platform's rather than yours.

Then the detail route. Read the identifier from the location, fetch that incident, and handle four cases: loading, found, not found, and failed to load. Not found is its own case and it needs its own honest message, because a link that used to work will eventually be followed after the record was removed.

Then seed data. Put several incidents into your mock, chosen deliberately to include a critical one, one with an unusually long title, one with a description containing markup, and one with a missing optional field. Your seed data is a test fixture, and the temptation is to make it flattering. Make it hostile instead, and the interface you build will be the one that survives a customer.

Then focus and announcement on navigation, which almost every React application gets wrong. When the location changes, the visual content changes but focus does not move and nothing is announced, so a screen reader user hears nothing and a keyboard user's next tab continues from wherever they were. The fix is to move focus to the new view's heading, or to a container that receives focus, and to announce the new view's name. It is a small effect in the shell, and it is the difference between a routed application that is accessible and one that merely contains accessible pages.

Then tests. Component tests for the two things named in the chapter's own success criteria: a critical incident renders with its full state treatment, and an empty list renders its intentional empty state. Then keep chapter nine's behavioural tests alive: one successful submission, one recoverable failure, the double-submit guard. Query by role and accessible name exactly as before — and notice, if you did chapter nine well, that most of those tests need no changes at all despite a complete rewrite of the implementation. That is the payoff for binding tests to meaning.

Finally, configuration. You now have something that needs a service address, and it will be a different address in every environment. Keep it as a build-time or run-time configuration value, never a hard-coded string in a component, and remember chapter nine's rule: nothing secret lives in browser code. This is also the moment to keep a single flag that says whether the mock or the real service is in use, and to keep the visible marker in the interface when it is the mock.

## Pitfalls, named

Effects doing calculations. If a value can be derived from props and state during render, derive it. An effect that sets state from other state creates an extra render, a moment of inconsistency, and a synchronisation bug waiting for a race.

Effects fetching without cleanup. Navigate to incident A, then quickly to incident B; the slower request for A lands last and you display A's data on B's page. Abort on cleanup, or check on arrival whether the response is still wanted. Same lesson as chapter nine, new packaging.

Array position as key. Delete a row and watch state migrate to a neighbour. Use identifiers.

A global store adopted on day one. You have two routes. Adding a state management library now means the customer's engineer must learn it to change a label, and the library will shape every subsequent decision. Wait until you can name the specific problem.

Context as a data bus. Ambient values only. If it changes frequently or belongs to one screen, it is not ambient.

Prop drilling misdiagnosed. Passing a value through three levels is fine and readable. Passing it through eight suggests your component boundaries are wrong, and the fix is usually composition — passing rendered content in — rather than reaching for context.

The two-hundred-line component. Usually a page that is simultaneously fetching, filtering, sorting, rendering, and managing a form. Split by responsibility, not by line count, and let the page coordinate rather than compute.

Premature abstraction. A configurable component with fourteen props, invented to serve two use cases that turn out not to be the same. Duplicate twice, extract on the third. Field work makes this worse, because each customer's variation looks like it wants a new prop, and after six customers you have a component nobody can reason about. That is exactly the fork chapter six warned about, wearing a component's clothes.

Blank screens. No error boundary, no empty state, no not-found state. Every one of these becomes a support call, and every one is ten minutes of work.

Losing accessibility in the rewrite. The most common regression: labels no longer associated because the field wrapper is doing it wrong, the error summary no longer receiving focus, route changes silent. Re-run chapter seven's keyboard walk after this chapter. It is not optional; it is the check that proves the framework did not cost you anything.

Storing derived server values in local state. Copying the returned priority into a state variable and then updating it locally. Now you have two priorities. Display what the service said.

Premature memoisation. Wrapping everything in caching helpers before measuring. It adds noise, it hides mistakes, and at this scale it buys nothing. Measure first, in chapter twenty three.

Snapshot tests of rendered markup. They pass until anything changes, then they all fail and everyone updates them without reading. Assert on what the operator can perceive.

## Verifying your work

Seven checks.

Reload every route directly, including the detail route with an identifier in the location. If the detail route only works when reached by clicking, your routing is not real and you have lost the shareable-link property that made routing worth having.

Open a detail link in a new tab and send it to yourself. That is the operational workflow. If it does not survive that, fix it.

Empty the mock's data and load the list. Read what appears. Does it tell a first-day operator what to do?

Make the list request fail, then make the detail request return not found. Two distinct, honest messages, each with a next action.

Throw an error deliberately inside one row's rendering. The error boundary should contain it. If the whole application goes white, add the boundary.

Do the full keyboard walk again, through both routes, including navigation. Focus visible at every stop, focus moves on route change, the new view is announced. Then walk the accessibility representation of the list: is each row's link name descriptive on its own, or are there fourteen links all named view?

Run the tests, including the chapter nine ones. Note how many needed changing and why. If the answer is all of them, your tests were bound to structure and this is your lesson; write that down, because it is worth more than the tests.

And one delivery step while you are here: capture screenshots of the list, the detail, the empty state, and one error state. Those four images are what a stakeholder will remember from this phase, and chapter thirty five will ask for them.

## Your practice test

Guide has the rubric. Spoken:

Your goal is a React operator workspace with two routes — an incident list and an incident detail — containing a rebuilt intake form composed of small typed components, with intentional empty, loading, error, and not-found states.

Your constraints: rebuild the form from scratch rather than porting it. Type every component's props. Keep request state in the narrowest component that needs it, and be able to justify the placement of each piece of state against the four categories: server, location, interface, and form. The detail route's identity lives in the location and survives a reload and a new tab. All data access goes through the chapter nine service seam, still mocked, still marked as mocked in the interface. No global state library and no component library — you are learning the model. Chapter seven's accessibility properties and chapter nine's five-state request model must both survive intact, verified rather than assumed. And route changes must move focus and announce the new view.

Your artifacts: the application, structured by feature; a component inventory naming each component's single responsibility and its props; a state ownership table listing every piece of state, its category, its owner, and why not higher; hostile seed data including a critical incident, an overlong title, and content containing markup; component tests for a critical incident and an empty list, plus the surviving chapter nine tests, with a note on how many needed changes; a keyboard and accessibility re-verification note; and screenshots of list, detail, empty, and error.

You are done when a detail location can be reloaded and shared, when the list, form, and indicators share no hidden state, when empty and error states are deliberate rather than blank, when the keyboard walk passes on both routes, and when the priority displayed is still the service's value and nothing else.

## Recap

Five things.

First, React lets you describe the interface as a function of state instead of instructing the document. The discipline that makes that pay off is putting each piece of state in the narrowest place that needs it, sorted into server, location, interface, and form.

Second, most effects you are tempted to write are calculations in disguise. Effects are for reaching outside React — including the one legitimate case in this chapter, moving focus.

Third, the location bar is an operational feature. A shareable incident link is how your tool joins the customer's existing workflow.

Fourth, empty, loading, error, and not-found are four of the states an operator sees most. Design them; do not discover them.

Fifth, a rewrite is where accessibility silently dies. Re-run the keyboard walk, and notice that tests bound to accessible names survived while tests bound to structure did not.

Part Two is complete. You have a customer-facing application with real structure and no server behind it. In chapter eleven we build the authoritative side: a typed Node service with validation, a domain service that owns the priority policy, stable response shapes, and the removal of exactly the mock path that the service replaces. Build the workspace first. Then meet me there.
