# FullStack in Audio: Forward Deployed Engineer

## Listen-then-practice chapter list

This is a linear, audiobook-first rendering of the [Forward Deployed Engineer roadmap](https://roadmap.sh/forward-deployed-engineer). It covers all 20 live FDE topic/subtopic nodes and the distinct supporting topics in the roadmap's [source content](https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/forward-deployed-engineer/content). Some source records are aliases left by node renames (such as *APIs Design* / *API Design*); aliases are listed once, not taught twice.

The visual roadmap intentionally points to prerequisite tracks rather than prescribing one long sequence. The course is being retargeted onto one real customer: **Mato Crafts**, a handmade jewellery studio in Patan, and one system, **Promise Desk**. Chapter 1 matches that customer. Chapters 2–38 below still describe the earlier Harborline / FieldOps draft. Do not sit those projects until their audio is rewritten. The retarget notes are in [the world plan](world-plan.md).

**Practice rule for every chapter:** write the change yourself from an empty file or from the preceding Promise Desk state. Do not paste a finished solution. Use documentation and tests to resolve gaps, then retain the result for the next chapter. Chapters that still say FieldOps have not been rewritten.

**Every chapter project is a test, not a tutorial.** The chapter audio teaches everything you need to attempt it: the concepts, the tradeoffs, the failure modes, how to verify your own work, and the customer situation it belongs to. The project then gives you a goal, constraints, a starting state, the artifacts you must produce, and a pass bar you grade yourself against. It does not give you steps to follow. The companion project guide holds inverted hints at the very end for when you are genuinely stuck — they are deliberately absent from the audio.

**Listening time** is audio only: at least 30 minutes per chapter, usually 32 to 40, and up to 45 where the topic earns it. It excludes planning, building, and debugging. Project work is never time-boxed; it ends at demonstrated behavior.

---

## Part I — Enter the field and establish engineering judgment

### 1. Entering the Forward Deployed Engineer field
**Roadmap nodes covered:** Introduction; From X to FDE (including the source alias *What is an FDE*); Roles & Responsibilities (live-map label: *Roles & Responsabilities*)  
**Listen:** 35 minutes  
**What it covers:** The FDE role, its boundary with product, solutions, platform, and customer teams; delivery ownership; and the transition from an existing engineering specialty into field work.  
**Why an FDE cares:** An FDE succeeds by turning an ambiguous customer outcome into a maintainable deployed system—not by merely demonstrating a model or closing a ticket. Clear responsibility boundaries prevent promises the delivery team cannot keep.  
**Tools:** customer problem brief, stakeholder map, responsibility matrix, architecture decision record (ADR).

**Chapter project (test) — Charter Promise Desk for Mato Crafts**  
**Goal:** Subhechha, a maker, and you can read one page and agree what the first release will change, who decides, and how success will be judged.  
**Constraints:** The customer is Mato Crafts. The store already exists. No implementation detail. Every claim is labelled observed or assumed. Non-goals are mandatory. One outcome the studio could count this month. Promise Desk may suggest a promise and may not tell a customer yes.  
**Required artifacts:** a one-page delivery charter; a responsibility matrix including the founder, a maker, you, and Promise Desk; a risk register naming the evidence that would retire each risk.

**Pass bar**
- A one-page charter names a customer problem, users, measurable outcome, and non-goals.
- Responsibility for decisions and escalation is explicit.
- The first release can be explained in under two minutes without mentioning implementation details.

### 2. Computer science and polyglot implementation choices
**Roadmap nodes covered:** Computer Science; C++; Java / Scala; Go  
**Listen:** 36 minutes  
**What it covers:** Core computational thinking—state, complexity, memory, concurrency, types, compilation—and how C++, Java/Scala, and Go lead to different operational tradeoffs.  
**Why an FDE cares:** Customer environments and platform teams are rarely monocultures. An FDE must evaluate integration surfaces and choose a small, supportable component rather than force their favorite runtime everywhere.  
**Tools:** Big-O reasoning, type systems, compiler/toolchain docs, benchmarks, language interoperability boundaries.

**Chapter project (test) — Build a portable triage-priority rule**  
**Goal:** One priority rule, specified once, implemented in three runtimes, with a defensible choice of which runtime a customer service would actually use.  
**Constraints:** The rule is pure: same inputs, same output, no clock, no network, no storage. Write each implementation yourself in C++, Java or Scala, and Go — no code generation and no shared source between them. Ties and invalid values must be defined behavior, not accidents. The charter from chapter one supplies the inputs.  
**Required artifacts:** three implementations; one shared table of inputs and expected priorities including boundary and invalid cases; an ADR selecting one runtime that separates technical fit from personal preference.

**Pass bar**
- All three programs produce the same priorities for the same inputs.
- Tests expose at least one boundary case.
- The ADR distinguishes technical fit from personal preference.

### 3. Linux, shell, and Python for field work
**Roadmap nodes covered:** Linux Skills / Linux; Shell / Bash; Python  
**Listen:** 32 minutes  
**What it covers:** Files, processes, permissions, environment variables, ports, logs, repeatable shell work, and Python as an effective integration and automation language.  
**Why an FDE cares:** Deploying near customer systems means diagnosing a real runtime safely. Small, readable automation often removes more delivery friction than a large framework.  
**Tools:** Linux shell, Bash, Python, virtual environments, process inspection, structured local logs.

**Chapter project (test) — Turn the priority rule into a local intake CLI**  
**Goal:** An operator can enter an incident on a Linux machine, get a priority back, and leave behind evidence that you can inspect afterwards.  
**Constraints:** Start from an empty directory. Python for the program, shell for the task wrapper. Nothing secret is committed, printed, or logged. Malformed input fails loudly and exits nonzero. The Python priority result must agree with your chapter two implementations on every row of the shared input table.  
**Required artifacts:** the command-line program; a shell task that runs it and propagates failure; a non-secret example environment file; a written note on the permissions you chose and the process and log evidence you inspected.

**Pass bar**
- The CLI handles a valid record and rejects a malformed one.
- No secret is committed or printed.
- A new operator can run the documented local workflow from a clean shell.

### 4. Versioned delivery and the full-stack seam
**Roadmap nodes covered:** Git & GitHub; Full Stack  
**Listen:** 32 minutes  
**What it covers:** Commit design, branches, code review, issue linkage, reproducible handoff, and the frontend–backend–data boundary that makes a system truly full stack.  
**Why an FDE cares:** A customer pilot changes quickly. Traceable changes, a small integration contract, and a reviewable history make field adaptation safe to continue after the initial deployment.  
**Tools:** Git, GitHub, issue tracker, pull-request template, README, ADRs.

**Chapter project (test) — Make FieldOps Copilot reviewable**  
**Goal:** A second engineer can clone your work, reproduce the current result, and review the history without asking you a single question.  
**Constraints:** Real history made as the work happens — no single squashed import and no invented commits. The README must be sufficient to run the CLI on a clean machine. The first web-intake issue must state acceptance criteria before any interface exists. The seam diagram names an owner for every boundary, including the ones that do not exist yet.  
**Required artifacts:** the repository with a readable history; a README covering the charter and how to run the CLI; one issue with acceptance criteria; one pull-request description naming behavior, risks, tests, and rollback; a full-stack seam diagram.

**Pass bar**
- History tells the story of the initial implementation without one giant commit.
- The README lets another engineer reproduce the current CLI result.
- The interface diagram shows ownership of each boundary.

### 5. Data structures, algorithms, and system design
**Roadmap nodes covered:** DSA & System Design; Data Structures & Algorithms; System Design  
**Listen:** 34 minutes  
**What it covers:** Choosing arrays, maps, queues, heaps, and graphs; analyzing time and space; and translating a workload into a scalable system-design sketch.  
**Why an FDE cares:** FDE interview and production decisions both require explaining why an implementation remains responsive when customer volume or concurrency changes.  
**Tools:** complexity analysis, load assumptions, queues, caches, rate limits, architecture diagrams.

**Chapter project (test) — Design the intake-to-triage flow**  
**Goal:** A design for the path from intake to triage that states its capacity assumptions out loud and survives its own worst case on paper.  
**Constraints:** Numbers before diagrams: volume, peak burst, response-time target, retention — each labelled measured or assumed. No appeal to infinite scale and no autoscaling hand-wave. Every data-structure choice carries the operation it optimizes and its complexity. You must break your own design with a real batch before you defend it.  
**Required artifacts:** a load-assumption table; a data-structure decision list with complexity reasoning; a request-path diagram through queue, triage, and notification; one failure mode and graceful response per boundary; the observed result of a large batch run and what it exposed.

**Pass bar**
- Each data structure has a stated operation and complexity reason.
- The design names capacity assumptions rather than implying infinite scale.
- At least one queue, timeout, or backpressure decision is justified.

### 6. Software architecture for customer-specific systems
**Roadmap nodes covered:** Software Architecture  
**Listen:** 33 minutes  
**What it covers:** Modularity, bounded contexts, dependency direction, configuration boundaries, and how to separate customer adaptation from reusable product capabilities.  
**Why an FDE cares:** Field work goes wrong when one customer’s exception becomes an untestable fork. Architecture should preserve a reusable core while making approved customization explicit.  
**Tools:** C4-style diagrams, ADRs, ports-and-adapters, feature configuration, contract tests.

**Chapter project (test) — Define the FieldOps Copilot architecture**  
**Goal:** An architecture that separates the reusable FieldOps core from one customer's adaptation, so the second customer does not require a fork of the first.  
**Constraints:** Components, boundaries, and dependency direction only — no framework selection and no premature code beyond one interface boundary you actually exercise. Customer-specific behavior must be reachable through configuration or an adapter, never by editing core logic. Interface contracts are stated in plain language and must be testable without a real notification provider.  
**Required artifacts:** a component diagram marking reusable core, customer configuration, and customer-specific adapter; two plain-language interface contracts; an ADR for business-unit routing; one inward-pointing dependency demonstrated behind a small interface.

**Pass bar**
- A diagram makes the reusable/customer-specific split visible.
- Configuration is distinct from source-code changes.
- The chosen interface can be tested without a real notification provider.

---

## Part II — Build the customer-facing experience

### 7. Frontend foundations: semantics and accessible intake
**Roadmap nodes covered:** Frontend Skills; Frontend; HTML  
**Listen:** 33 minutes  
**What it covers:** Semantic documents, forms, labels, keyboard paths, validation feedback, and the browser’s role in a full-stack system.  
**Why an FDE cares:** Field tools are often used under pressure by varied roles. An inaccessible or ambiguous form creates bad data and makes the customer lose trust before the intelligence layer matters.  
**Tools:** HTML, browser developer tools, accessibility tree, form controls, client-side validation.

**Chapter project (test) — Build the incident intake page**  
**Goal:** An operator under time pressure can report an incident correctly on the first attempt, using only a keyboard.  
**Constraints:** Hand-written markup from an empty file. No framework, no component library, no styling work yet. The page must not imply that a submission reached a server. Accessibility is graded by inspection, not by intention.  
**Required artifacts:** the intake page covering title, severity, affected service, business impact, and description; a local confirmation view; a note recording one accessibility problem you found with browser tooling and how you fixed it.

**Pass bar**
- Every field is labeled and required fields announce errors clearly.
- The form is usable without a mouse.
- The page communicates that submission is local until the API chapter connects it.

### 8. CSS for trustworthy operational interfaces
**Roadmap nodes covered:** CSS  
**Listen:** 32 minutes  
**What it covers:** Layout, responsive behavior, visual hierarchy, state affordances, readable density, and design tokens.  
**Why an FDE cares:** Operations users must notice priority and status instantly. Visual polish here is not decoration; it reduces avoidable triage mistakes.  
**Tools:** CSS, responsive layout, custom properties, browser responsive mode, color-contrast checker.

**Chapter project (test) — Style the intake and priority confirmation**  
**Goal:** Severity and status are unmistakable at a glance, on a wide desktop and on a narrow field laptop, for an operator who cannot rely on color.  
**Constraints:** Your own stylesheet, no CSS framework. State must be carried by more than hue. No horizontal scrolling at a narrow viewport, and no focus state you cannot see. Contrast and high zoom are graded by measurement.  
**Required artifacts:** a small documented state vocabulary; the styled intake and confirmation views; before and after screenshots for the delivery record; the contrast and zoom checks you ran.

**Pass bar**
- The critical state has text, icon/shape, and color cues.
- No horizontal scrolling appears at a narrow viewport.
- Focus is always visible and contrast is checked.

### 9. Browser behavior with JavaScript and TypeScript
**Roadmap nodes covered:** JavaScript / TypeScript; JavaScript  
**Listen:** 36 minutes  
**What it covers:** Events, asynchronous work, modules, runtime errors, typed domain models, and the divide between browser validation and server authority.  
**Why an FDE cares:** Customer workflows need immediate feedback, but the browser must not become the only enforcement point for a business rule. Types make changing requirements safer.  
**Tools:** JavaScript, TypeScript, browser network panel, schema/type definitions, unit tests.

**Chapter project (test) — Make intake behavior typed and asynchronous**  
**Goal:** The intake page behaves correctly while a request is in flight, when it fails, and when the response is not what the browser expected.  
**Constraints:** One typed representation of an incident, shared by every code path. The browser may validate but may never be the authority on priority. Double submission must be impossible, not merely discouraged. The mock response is temporary and must be replaceable without rewriting the form.  
**Required artifacts:** the typed incident model; an asynchronous submit path with loading, success, rejected-validation, and unexpected-error states; tests for one valid submission and one recoverable failure; operator-readable error text.

**Pass bar**
- A user cannot accidentally submit twice while a request is pending.
- Error text tells an operator what to do next.
- The project has one shared representation of an incident rather than untyped field bags.

### 10. React and frontend application structure
**Roadmap nodes covered:** React; Frontend Apps  
**Listen:** 36 minutes  
**What it covers:** Component boundaries, state ownership, effects, routing, testable UI composition, and selecting a frontend-app structure that stays maintainable.  
**Why an FDE cares:** Pilots gain screens and roles rapidly. A component model lets an FDE ship the next customer workflow without duplicating fragile form logic.  
**Tools:** React, TypeScript, component tests, router, local mock service.

**Chapter project (test) — Convert the intake into a React operator workspace**  
**Goal:** An operator can move between a list of incidents and one incident's detail without losing their place, and the next screen you add will not require duplicating form logic.  
**Constraints:** Rebuild the form as components from scratch; do not port the old markup wholesale. State lives in the narrowest component that needs it. Components communicate through explicit typed interfaces, never hidden shared state. Empty and error views are deliverables, not afterthoughts.  
**Required artifacts:** the application shell with list and detail routes; reusable priority and status components; seeded local incidents; component tests for a critical incident and an empty list.

**Pass bar**
- Navigation preserves a stable URL for an incident detail.
- The form, status badge, and list do not depend on each other’s hidden state.
- Empty and error states are intentional, not blank screens.

---

## Part III — Make the backend and data reliable

### 11. Backend services and Node.js
**Roadmap nodes covered:** Backend Skills; Backend; Node.js  
**Listen:** 36 minutes  
**What it covers:** HTTP service structure, request lifecycle, validation, domain services, error boundaries, and Node.js runtime concerns.  
**Why an FDE cares:** A field deployment needs one authoritative place for customer policy, auditing, integrations, and AI guardrails. A browser mock is useful only until the first real user arrives.  
**Tools:** Node.js, TypeScript, HTTP framework, schema validator, unit/integration tests, environment configuration.

**Chapter project (test) — Create the FieldOps API**  
**Goal:** The service, not the browser, is the authority on what a valid incident is and what priority it receives.  
**Constraints:** A typed service written from scratch, honoring the chapter six interface contract. Every incoming incident is validated server-side; no field is trusted because the form produced it. Priority policy exists in exactly one place in the whole system. Remove only the mock path the service genuinely replaces.  
**Required artifacts:** the service with health, create, list, and get behavior; structured request logging; stable success and error response shapes; the workspace talking to the real service; evidence that invalid input cannot create an incident.

**Pass bar**
- The browser can create and retrieve a real in-memory incident through the service.
- Invalid server input cannot create an incident.
- The same priority policy is not independently maintained in the UI.

### 12. API design, identity, and secure integration surfaces
**Roadmap nodes covered:** APIs Design / API Design; API Security; Authentication; GraphQL  
**Listen:** 42 minutes  
**What it covers:** Resource and action API design, versioning, authorization versus authentication, input and output controls, least privilege, and when GraphQL is a better fit than a focused HTTP API.  
**Why an FDE cares:** Customer integrations are the boundary where valuable data and customer risk meet. A quick unprotected endpoint can turn a pilot into a security incident.  
**Tools:** OpenAPI, HTTP, OAuth/OIDC concepts, RBAC, secrets manager, GraphQL schema tooling, API security testing.

**Chapter project (test) — Secure operator access and publish the contract**  
**Goal:** A customer security reviewer could read your published contract and your tests and see exactly who can do what, and what happens when someone tries more.  
**Constraints:** Two roles with genuinely different privileges. Authorization is checked on every incident operation, including the ones you think are harmless. The published contract must leak no secret and no internal implementation detail. If you add a query language alongside the service, you must justify the second surface or remove it.  
**Required artifacts:** the role and privilege definition; an authentication boundary suitable for local development; the published API contract including errors and authorization requirements; one read-only query path with a written justification; tests covering unauthenticated, unauthorized, valid, and malformed requests.

**Pass bar**
- An operator cannot perform an administrator-only action.
- API documentation exposes no real secret or internal implementation detail.
- There is a concrete reason for using—or not using—GraphQL.

### 13. SQL and PostgreSQL as the system of record
**Roadmap nodes covered:** SQL; PostgreSQL  
**Listen:** 38 minutes  
**What it covers:** Relational modeling, keys, constraints, indexes, transactions, migrations, query plans, and safe access to a durable source of truth.  
**Why an FDE cares:** Customer operational history must remain correct when multiple people edit, integrations retry, and incident records are audited months later.  
**Tools:** PostgreSQL, SQL, migrations, query-plan inspection, transactions, database test fixture.

**Chapter project (test) — Persist incidents and audit events**  
**Goal:** Customer incident history survives a restart, a retry, and an audit six months later.  
**Constraints:** Migrations written by hand and applied to an empty database; no schema created by clicking. Constraints must make bad data impossible rather than unlikely. Duplicate intake retries may not create duplicate incidents. Audit records are immutable. Any index you add must be justified by a query plan you actually read.  
**Required artifacts:** the schema for incidents, operators, status changes, and audit events; the migrations; the service reading and writing inside transactions; a before-and-after query plan for one real operator query.

**Pass bar**
- Restarting the API retains the same incidents.
- Duplicate intake retries do not create duplicate incidents.
- An audit record identifies who changed a status and when.

### 14. NoSQL and fit-for-purpose storage
**Roadmap nodes covered:** NoSQL Databases  
**Listen:** 32 minutes  
**What it covers:** Document, key-value, wide-column, and graph storage tradeoffs; consistency; TTL; schema evolution; and deciding when not to add another datastore.  
**Why an FDE cares:** AI context, temporary rate limits, and integration payloads tempt teams to store everything everywhere. An FDE needs a defensible storage decision that limits operational cost.  
**Tools:** Redis-style key-value store, document-store concepts, TTLs, cache-aside pattern, load tests.

**Chapter project (test) — Add an expiring triage cache**  
**Goal:** One derived value gets faster without the system quietly acquiring a second source of truth.  
**Constraints:** Cache only something you can afford to lose and recompute. The relational store stays authoritative. Deleting the cache must be a survivable event, not an incident. Every additional datastore must be paid for in writing: operational cost, failure modes, and who runs it.  
**Required artifacts:** the cached value with a stated key, expiry, and invalidation trigger; the adapter behind an interface; observed behavior when the cache is stale and when it is unavailable; a storage decision record explaining what you did not add and why.

**Pass bar**
- Deleting the cache cannot lose an incident or audit event.
- A stale result has an explicit acceptable window or is invalidated.
- The storage ADR identifies the cost of each additional datastore.

---

## Part IV — Build AI behavior that can be controlled

### 15. AI engineering, LLM fundamentals, and provider selection
**Roadmap nodes covered:** AI Engineering Skills; AI Engineering; LLM Fundamentals; Choosing your Model Provider  
**Listen:** 42 minutes  
**What it covers:** Tokens, context windows, prompting boundaries, inference APIs, model capabilities, provider reliability, privacy, cost, and task-to-model fit.  
**Why an FDE cares:** An FDE sells an outcome, not a model name. Provider and model choice must reflect customer data boundaries, response quality, latency, budget, and fallback behavior.  
**Tools:** LLM provider SDKs, model scorecards, sandbox credentials, structured outputs, provider status pages.

**Chapter project (test) — Add an AI triage recommendation seam**  
**Goal:** The system can ask a model for a triage suggestion, and swapping that model changes nothing else about the system.  
**Constraints:** The model's job is bounded in writing before any call is made: suggest, never act. No real customer text leaves the machine, and no credential is used before it is approved. Tests must pass with a deterministic fake and no network. A provider comparison that names only one candidate is a fail.  
**Required artifacts:** the written bounded-task definition; a provider-agnostic interface with a deterministic fake; a two-option provider comparison judged against the charter, including a fallback; structured suggestions an operator must review before anything happens.

**Pass bar**
- The AI boundary can be replaced without changing the incident service.
- A documented model-selection decision includes a fallback.
- No real customer incident text is sent during unapproved experimentation.

### 16. Prompt engineering, management, and versioning
**Roadmap nodes covered:** Prompt Engineering; Prompt Management; Prompt Versioning  
**Listen:** 35 minutes  
**What it covers:** Task instructions, examples, schema constraints, prompt templates, version identity, change review, and separating policy from incidental wording.  
**Why an FDE cares:** A prompt is behavior-changing production configuration. Without versioning, an FDE cannot tell a customer which instruction caused a quality or safety change.  
**Tools:** prompt registry or versioned files, template variables, structured-output schema, evaluation fixture set, change log.

**Chapter project (test) — Version the triage instruction**  
**Goal:** You can tell a customer which exact instruction produced a given recommendation, and what changed when behavior changed.  
**Constraints:** Treat the instruction as production configuration: versioned, reviewable, and revertible. Variable content may never become instruction text. Every recommendation must carry the version that produced it. A behavior change you cannot demonstrate with fixtures does not count as evidence.  
**Required artifacts:** the versioned instruction with a human-readable change note; at least five synthetic fixtures including ambiguity, missing detail, and sensitive-looking content; a before-and-after comparison across one deliberate instruction change; a written rollback rule naming the approver.

**Pass bar**
- Every AI recommendation records the prompt version that produced it.
- Prompt variables cannot inject unreviewed instruction text.
- A reviewer can understand the behavioral difference between two versions.

### 17. AI-assisted development without surrendering engineering judgment
**Roadmap nodes covered:** Cursor; Claude Code; Codex; Gemini; Vibe Coding  
**Listen:** 32 minutes  
**What it covers:** Using coding agents and assistants for exploration, small changes, tests, review, and documentation while retaining ownership of requirements, security, and verification.  
**Why an FDE cares:** These tools can speed customer delivery, but unreviewed agent output can smuggle assumptions, secrets, dependencies, and unsafe integrations into a sensitive deployment.  
**Tools:** Cursor, Claude Code, Codex, Gemini, repository instructions, diff review, test runner, dependency scanner.

**Chapter project (test) — Establish an assisted-development protocol**  
**Goal:** Your team can say precisely what "agent-assisted but engineer-owned" means here, and prove it happened on one real change.  
**Constraints:** Narrow scope only — a test idea or an explanation, never a whole feature. Every changed line is read before it is kept. No tool receives customer data or credentials. Dependency and configuration changes are treated as security-relevant, not as noise.  
**Required artifacts:** written project instructions covering the charter, the no-secret rule, test expectations, and forbidden autonomous actions; one reviewed change with its diff and test evidence; a review note naming what you accepted, rejected, and verified.

**Pass bar**
- Assistant use leaves a human-reviewable diff and test evidence.
- No tool receives production customer data or credentials by default.
- The team has a repeatable definition of “agent-assisted but engineer-owned.”

### 18. Tools, functions, and the Model Context Protocol
**Roadmap nodes covered:** Tools & Functions; MCP  
**Listen:** 36 minutes  
**What it covers:** Tool schemas, deterministic functions, capability discovery, authorization at tool boundaries, Model Context Protocol concepts, and safe error handling.  
**Why an FDE cares:** The value of a customer copilot comes from carefully constrained actions over real systems. A model should request an allowed capability; it should never inherit an administrator’s unlimited access.  
**Tools:** JSON Schema, function calling, MCP server/client concepts, scoped credentials, audit logs, sandbox adapters.

**Chapter project (test) — Build a read-only incident lookup tool**  
**Goal:** A model can look up one incident through a capability that is incapable of changing anything, under an identity narrower than yours.  
**Constraints:** Read-only by construction, not by instruction — the write path must not exist. The tool runs under an operator-scoped identity; an administrator credential is a fail. Out-of-scope requests get a safe, actionable refusal. Every call is audited. The contract must be understandable without reading the implementation.  
**Required artifacts:** the tool contract with input validation and a narrow response shape; the implementation against your service; the capability exposed through a protocol adapter or a documented local stub; audit records with caller, input summary, result status, and latency.

**Pass bar**
- The tool cannot mutate an incident.
- Its contract can be understood without reading its implementation.
- A model failure or malformed call never bypasses authorization.

### 19. AI agents and agent architectures
**Roadmap nodes covered:** AI Agents; Agent Architectures  
**Listen:** 38 minutes  
**What it covers:** Agent loop boundaries, planner/executor patterns, state machines, human approval, retries, stop conditions, and when a deterministic workflow is better than an “agent.”  
**Why an FDE cares:** Customer trust is lost when a system silently loops, invents a task, or takes an unapproved action. The right architecture makes behavior inspectable.  
**Tools:** workflow/state-machine library, tool contracts, structured events, retry policy, human-in-the-loop queue.

**Chapter project (test) — Assemble a bounded triage agent**  
**Goal:** A workflow that proposes triage, stops on its own, and can explain every step it took.  
**Constraints:** States and transitions are explicit; an unbounded loop is a fail. Deterministic transitions come first, and the model is invited only where judgment is genuinely required. No external action without a recorded operator approval. A maximum step count and a timeout are mandatory, and you must watch them fire.  
**Required artifacts:** the state map with start, stop, and error states; the deterministic transitions; the model-produced structured proposal using only read-only capability; the approval gate; the observed behavior under an unhelpful or looping model response.

**Pass bar**
- The workflow has explicit start, stop, and error states.
- The agent cannot call a write tool because no write tool exists.
- The operator can see why the proposal was made and approve or reject it.

### 20. Memory, RAG, and vector databases
**Roadmap nodes covered:** Memory & State Management; RAGs; Vector DBs  
**Listen:** 40 minutes  
**What it covers:** Short-lived workflow state versus durable memory, retrieval-augmented generation, document chunking, embeddings, vector search, metadata filters, citations, and freshness.  
**Why an FDE cares:** A customer expects answers grounded in their procedures—not hallucinated policy. Retrieval needs tenant isolation, source visibility, and a plan for stale content.  
**Tools:** embedding model, vector database, document parser, metadata store, retrieval evaluation set, source citations.

**Chapter project (test) — Ground the agent in customer runbooks**  
**Goal:** Every recommendation either cites the customer's own procedure or declines to answer.  
**Constraints:** Synthetic runbooks only, each carrying owner, revision date, tenant, and access metadata. Retrieval must respect tenant and role boundaries — a cross-tenant result is an immediate fail. Weak retrieval must produce an explicit insufficient-evidence outcome, never a confident guess. Stale content must be provably removable.  
**Required artifacts:** the indexed runbook set with source references intact; tenant- and role-filtered retrieval; proposals carrying citations; the observed result of updating and reindexing one runbook; a written distinction between workflow state and durable customer knowledge.

**Pass bar**
- Every grounded recommendation can point to a source passage or declines to answer.
- Retrieval never crosses the synthetic tenant boundary.
- Workflow state is not confused with permanent customer knowledge.

### 21. Multi-agent design and delegation limits
**Roadmap nodes covered:** Multi-Agents  
**Listen:** 32 minutes  
**What it covers:** Delegating specialized work, shared versus isolated context, coordination costs, handoffs, conflicting advice, and observability across multiple workers.  
**Why an FDE cares:** Multiple agents add latency, cost, and failure modes. They are warranted only when specialization or parallelism beats a single bounded workflow.  
**Tools:** task queue, delegation contract, correlation IDs, shared artifact store, timeout/cancel controls.

**Chapter project (test) — Add a specialist review without autonomous consensus**  
**Goal:** Two specialists review a triage proposal, and their disagreement reaches a human instead of being averaged away.  
**Constraints:** Each role gets only the context and read-only capability it needs; shared omniscient context is a fail. The coordinator may not manufacture consensus. Both outputs are correlated to the incident and the instruction versions. You must measure the cost of the split and be willing to conclude it was not worth it.  
**Required artifacts:** two bounded role contracts; the coordinator behavior on agreement and on conflict; correlated outputs; a measured comparison of calls and latency against the single-workflow baseline; a keep-or-remove decision with its reason.

**Pass bar**
- Each specialist has a narrow contract and no write authority.
- Disagreement is visible to a human.
- You can state why this split is beneficial or remove it if it is not.

### 22. Evaluation pipelines and regression testing
**Roadmap nodes covered:** Building Eval Pipelines; Regression Testing  
**Listen:** 38 minutes  
**What it covers:** Representative fixtures, expected properties, automated and human evaluation, baselines, pass criteria, regression gates, and diagnosing non-deterministic failures.  
**Why an FDE cares:** “It looked good in a demo” does not establish production readiness. Evals make model, prompt, retrieval, and tool changes reviewable before a customer notices a regression.  
**Tools:** eval runner, golden fixtures, assertion library, rubric, CI workflow, result store.

**Chapter project (test) — Build the FieldOps evaluation gate**  
**Goal:** A behavior regression in the AI workflow is caught by your suite before a customer notices it.  
**Constraints:** At least ten synthetic cases spanning severity, ambiguity, missing information, and prohibited-action attempts. Negative and safety cases are mandatory. Checks must be measurable, not impressionistic; genuinely subjective quality goes to human review, not to a fake assertion. Results are stored against the versions that produced them.  
**Required artifacts:** the fixture set; the deterministic checks; a saved baseline run; a demonstrated failing regression from one deliberately harmful change; the gate that blocks promotion and names the responsible model, instruction, retrieval, or tool version.

**Pass bar**
- An evaluator can detect a behavior change without reading every answer.
- The suite includes negative and safety cases, not only happy paths.
- A failed gate names the relevant model, prompt, retrieval, or tool version.

### 23. Latency, inference, and cost optimization
**Roadmap nodes covered:** Latency and Cost Optimization; Inference Optimization  
**Listen:** 34 minutes  
**What it covers:** Latency budgets, token accounting, caching, batching, model routing, streaming, retries, timeouts, and quality-preserving optimization.  
**Why an FDE cares:** Customer adoption fails when an operational assistant is slow or has unbounded cost. Optimize against a measured baseline rather than degrading safety or answer quality blindly.  
**Tools:** tracing, token/cost telemetry, cache, queue, load test, provider usage dashboard.

**Chapter project (test) — Set and meet a triage service budget**  
**Goal:** The triage path meets a stated latency and cost budget, and you can prove the optimization did not cost you quality.  
**Constraints:** Budget first, measurement second, optimization last — tuning before a baseline is a fail. Every claimed improvement is re-checked against the evaluation gate. Safety and grounding may not be traded for speed. An operator who exceeds the budget gets a useful fallback, never an open-ended wait.  
**Required artifacts:** the latency target and per-triage cost ceiling; instrumented timings and token or cost estimates across service, retrieval, model, and tool; a measured comparison of two model routes; one optimization with before-and-after evidence; the timeout and fallback behavior.

**Pass bar**
- A single request trace shows where time and cost were spent.
- The optimization does not reduce the evaluation gate below its baseline.
- Operators receive a useful fallback rather than an infinite spinner.

---

## Part V — Move and operate the data and model workflows

### 24. Data engineering and data pipelines
**Roadmap nodes covered:** Data Engineering; Data Pipelines  
**Listen:** 36 minutes  
**What it covers:** Source systems, ingestion, schema contracts, transforms, quality checks, idempotency, lineage, and separating analytical data from the operational database.  
**Why an FDE cares:** Customer AI systems are only as reliable as their data path. A pipeline must expose missing, late, duplicated, and changed data before it corrupts recommendations.  
**Tools:** ETL/ELT patterns, CSV/API ingestors, schema validation, data-quality assertions, lineage metadata, dead-letter queue.

**Chapter project (test) — Ingest customer asset context safely**  
**Goal:** Asset context reaches the agent only when it is valid, current, and traceable to its source.  
**Constraints:** The ingestion job must be safe to run twice. Bad records are quarantined with an actionable reason, never silently dropped or coerced. Joins happen through a defined identifier, not fuzzy matching. The system must be able to say "the data is stale" as distinctly as it says "no asset found". You must break it yourself with an unexpected column and a duplicate row.  
**Required artifacts:** the source contract; the idempotent validated ingestion into a read model; recorded source revision, ingestion time, rejections, and correlation identifier; observed behavior on schema drift and duplicates.

**Pass bar**
- Bad records are quarantined with an actionable reason.
- Re-running the same source does not duplicate data.
- The agent can distinguish “no asset found” from “pipeline data is stale.”

### 25. Orchestration with Airflow and Spark
**Roadmap nodes covered:** Airflow; Spark  
**Listen:** 34 minutes  
**What it covers:** Scheduled and dependency-aware workflows, retries, backfills, run metadata, distributed processing, partitioning, and when local transforms are sufficient.  
**Why an FDE cares:** Customer imports often become larger and more frequent after a pilot. Orchestration makes dependencies visible; distributed compute should be justified by scale, not fashion.  
**Tools:** Apache Airflow, Apache Spark, DAGs, task logs, partitions, retry/backfill controls.

**Chapter project (test) — Orchestrate the asset-context refresh**  
**Goal:** The asset refresh runs on a schedule, refuses to load unsafe data, and can be re-run for a past date without corrupting the present.  
**Constraints:** Dependencies are explicit; a failed validation must make downstream loading impossible rather than unlikely. Retries are bounded and a failure notifies someone. Distributed compute must be justified by measured scale, not preference — if it is not needed at pilot size, say so in writing.  
**Required artifacts:** the dependency graph with observable run status and source date; the implemented workflow or a precisely documented equivalent; the same aggregation at small and larger scale; a controlled backfill for one historical date; written evidence for or against distributed processing.

**Pass bar**
- A failed validation task prevents unsafe downstream loading.
- Every refresh has an observable status and source date.
- There is written evidence for whether Spark is needed at the pilot scale.

### 26. MLOps, model deployment, and managed ML services
**Roadmap nodes covered:** MLOps; Model Deployment; Managed ML Services  
**Listen:** 36 minutes  
**What it covers:** Model/prompt/retrieval versions, deployment promotion, service reliability, rollback, hosted ML tradeoffs, and keeping inference behavior tied to evidence.  
**Why an FDE cares:** Even with an API model provider, deployed AI behavior needs release discipline. Customers need to know what changed, how it was evaluated, and how to revert it.  
**Tools:** model registry concepts, deployment environments, managed ML platforms, release manifests, canary strategy, rollback runbook.

**Chapter project (test) — Create an AI release manifest**  
**Goal:** Anyone can identify the exact AI configuration behind a past recommendation, and revert to the previous one without improvising.  
**Constraints:** A release is an immutable record, not a description of intent. Promotion requires evaluation evidence; a release without it may not advance. Rollback must be rehearsed, not assumed. The hosting decision is judged against the charter's operational constraints, including who is on call.  
**Required artifacts:** the environment boundaries; a release record pinning application, instruction, model and provider, embedding model, retrieval index revision, and evaluation result; a self-hosted versus managed comparison; one promotion and one rehearsed rollback.

**Pass bar**
- An operator can identify the exact AI configuration behind a recommendation.
- Promotion requires evaluation evidence.
- Rollback is a documented operation, not an emergency rewrite.

---

## Part VI — Ship and protect the production-shaped system

### 27. DevOps, CI/CD, and GitHub Actions
**Roadmap nodes covered:** DevOps Skills; DevOps & CI/CD; GitHub Actions  
**Listen:** 34 minutes  
**What it covers:** Build/test/deploy pipelines, environment promotion, immutable artifacts, secrets, approval gates, and feedback from CI failures.  
**Why an FDE cares:** A customer-specific fix must be repeatable in every environment. Hand-run deployment steps create irreproducible systems and make rollback slow.  
**Tools:** CI/CD, GitHub Actions, artifact registry, protected environments, secret store, test reports.

**Chapter project (test) — Automate the safe build**  
**Goal:** The same verification runs on a fresh checkout and in automation, and an unsafe change cannot reach an environment.  
**Constraints:** No credential in the repository and no secret reachable by untrusted contributor code. A failing safety or regression check must block promotion, not warn. The artifact is versioned and its test evidence is retained. Anything a human does by hand must be written down or automated.  
**Required artifacts:** the defined pipeline stages; the automated workflow running the non-secret stages on every change; environment-referenced configuration; a versioned artifact with retained evidence; the observed result of a deliberately failing check.

**Pass bar**
- A fresh checkout can run the same verification locally and in CI.
- A failed safety or regression check blocks promotion.
- Secrets are unavailable to untrusted pull-request code.

### 28. Docker and containers
**Roadmap nodes covered:** Docker; Containers  
**Listen:** 33 minutes  
**What it covers:** Images, layers, minimal runtime images, container networking, volumes, configuration, health checks, and the security difference between an image and a running workload.  
**Why an FDE cares:** A portable service makes customer-site and cloud deployment more predictable—provided images are reproducible, non-root, and observable.  
**Tools:** Docker, Dockerfile, Compose, image scanner, container registry, health probes.

**Chapter project (test) — Containerize the FieldOps service**  
**Goal:** The whole local system starts from images and documented configuration, and a broken dependency shows up as an unhealthy service rather than a mystery.  
**Constraints:** Non-root runtime, no secrets baked into images, and no build-time tooling left in the runtime image. Startup ordering may not paper over a failed dependency. The interface boundary between built assets and the service is a deliberate decision you must state.  
**Required artifacts:** the service image definition; the interface delivery boundary; local orchestration of service, database, and optional cache with named configuration; health checks; evidence from an image inspection and one removal it prompted.

**Pass bar**
- The full local service starts from images and documented configuration.
- Containers do not embed secrets or run as root by default.
- A failed database connection becomes a visible unhealthy state.

### 29. Cloud platforms and provider selection
**Roadmap nodes covered:** Cloud Platforms; AWS; Azure; GCP  
**Listen:** 38 minutes  
**What it covers:** Compute, networking, identity, managed data, regionality, support models, billing, and choosing AWS, Azure, or GCP for a customer constraint rather than a brand preference.  
**Why an FDE cares:** Enterprise customers may already have a cloud, identity system, regulatory region, or procurement agreement. The best deployment is often the one that fits their operating model.  
**Tools:** AWS, Azure, GCP, cloud architecture diagrams, IAM, cost estimator, regional service matrix.

**Chapter project (test) — Select the customer cloud landing zone**  
**Goal:** A cloud choice the customer's own constraints justify, with a landing zone drawn well enough to be reviewed by their platform team.  
**Constraints:** The decision must be driven by customer identity, region, approved services, staffing, cost, and support — brand preference is a fail. No workload gets an all-powerful identity. Data residency and recurring cost are stated, including model usage and observability. One irreplaceable dependency must be named honestly.  
**Required artifacts:** a weighted decision matrix across the three major clouds; the landing-zone diagram covering network, compute, database, secrets, logs, and backups; separate roles for automation, runtime, operators, and break-glass; a cost estimate; a portability boundary.

**Pass bar**
- The cloud choice follows stated customer constraints.
- No workload uses an all-powerful identity.
- The design names region, data residency, and cost assumptions.

### 30. Infrastructure as code and Kubernetes
**Roadmap nodes covered:** Terraform; Kubernetes  
**Listen:** 40 minutes  
**What it covers:** Declarative infrastructure, state, plan/review/apply workflow, Kubernetes workloads, services, configuration, secrets, scaling, and the operational cost of cluster ownership.  
**Why an FDE cares:** Infrastructure must be reviewable and rebuildable. Kubernetes is powerful but is not automatically the right answer for a small customer pilot.  
**Tools:** Terraform, Kubernetes, managed container service, Helm/Kustomize concepts, policy-as-code, infrastructure plan review.

**Chapter project (test) — Declare the pilot deployment**  
**Goal:** The pilot environment can be recreated from reviewed definitions, with no undocumented console clicks in the path.  
**Constraints:** Environment-specific values stay separate from reusable definitions. Every change is reviewed as a plan before it is applied. Container orchestration must be justified against a simpler managed alternative, including the operational burden of owning a cluster. Rehearsal environments are destroyed when you are done.  
**Required artifacts:** infrastructure definitions or a precise reviewed plan for network, service identity, database, and runtime; the workload definition with resource requests, health probes, and non-secret configuration; the orchestration decision with its alternative; evidence of plan review and teardown.

**Pass bar**
- Recreating the pilot does not require clicking through undocumented console steps.
- Deployment manifests specify health and resource behavior.
- The Kubernetes decision includes its operational burden and an alternative.

### 31. Observability for applications and AI behavior
**Roadmap nodes covered:** Observability  
**Listen:** 36 minutes  
**What it covers:** Logs, metrics, traces, correlation IDs, service-level objectives, alerts, dashboards, AI-specific quality signals, and observability without collecting unnecessary customer data.  
**Why an FDE cares:** “The copilot was wrong” is not diagnosable without a trace from user action to retrieval, tool calls, model response, and human outcome. Evidence turns a customer escalation into an engineering decision.  
**Tools:** OpenTelemetry, structured logging, metrics backend, tracing backend, dashboard, alerting, redaction filters.

**Chapter project (test) — Trace one incident end to end**  
**Goal:** When a customer says "the copilot was wrong", an authorized engineer can reconstruct exactly what happened without guessing.  
**Constraints:** One correlation identifier survives the whole path, from submission to operator decision. Logs must be useful without carrying raw sensitive content — redaction happens before anything leaves the service. Dashboards must show AI workflow health, not only service uptime. An alert that does not tell someone what to do is a fail.  
**Required artifacts:** the end-to-end correlated trace; structured events for latency, errors, retrieval strength, instruction and model version, approval outcome, and fallback use; redaction evidence; a pilot dashboard; one synthetic dependency failure with its actionable alert.

**Pass bar**
- An authorized engineer can follow one synthetic incident through the system.
- Dashboards show both service health and AI workflow health.
- Logs are useful without exposing raw sensitive content.

### 32. Security, data privacy, compliance, and AI governance
**Roadmap nodes covered:** Security; Data Privacy & Compliance; AI Governance  
**Listen:** 43 minutes  
**What it covers:** Threat modeling, access control, encryption, supply-chain risk, data classification, retention, auditability, human oversight, model risk, and customer governance controls.  
**Why an FDE cares:** Enterprise deployment requires more than a security checklist. The FDE must turn policy into enforceable technical boundaries and make residual risk visible to the customer.  
**Tools:** threat model, data inventory, DPIA/security questionnaire, IAM, encryption, secret scanner, audit logs, policy-as-code.

**Chapter project (test) — Produce the pilot risk-control pack**  
**Goal:** A customer security reviewer can see which controls exist today, which are promises, and what risk remains if they launch anyway.  
**Constraints:** Every high-risk data flow needs a named control and a named owner. Implemented controls must be distinguishable from intended ones — blurring that line is the failure this project exists to prevent. The system must survive three abuse attempts by failing safely, and you must run them rather than reason about them.  
**Required artifacts:** the threat model across intake, service, storage, retrieval, tools, provider, deployment, and operator access; a data classification with retention and deletion rules; the control map; results from injection, cross-tenant retrieval, and unauthorized capability attempts; a residual-risk statement with owners and the decision the customer must make.

**Pass bar**
- Each high-risk data flow has a named control and owner.
- The system fails safely on the three abuse tests.
- The customer can distinguish implemented controls from future commitments.

---

## Part VII — Deliver value in the customer environment

### 33. Discovery, scoping, and requirements gathering
**Roadmap nodes covered:** Discovery & Scoping; Requirements Gathering  
**Listen:** 36 minutes  
**What it covers:** Discovery interviews, workflow observation, functional and nonfunctional requirements, assumptions, acceptance criteria, and converting customer language into a testable pilot.  
**Why an FDE cares:** The most expensive failure is solving an imagined problem perfectly. Field delivery begins with evidence about work, incentives, constraints, and the customer’s definition of success.  
**Tools:** interview guide, workflow map, requirements document, acceptance criteria, assumption log, prototype/demo.

**Chapter project (test) — Run a simulated FieldOps discovery**  
**Goal:** Requirements grounded in how the work actually happens, including the parts of it that contradict each other.  
**Constraints:** Four different stakeholder perspectives with genuinely different question sets. Requirements state observable behavior; a vague feature label is a fail. Every unverified claim is marked as an assumption with an owner and a way to check it. Learning more may not automatically expand the first release.  
**Required artifacts:** the interview notes; the current-workflow map with handoffs, delays, and workarounds; prioritized functional and nonfunctional requirements; an assumption log; a revised charter and acceptance criteria that name at least two conflicting needs.

**Pass bar**
- Requirements state observable behavior, not vague feature labels.
- The scope reflects at least two conflicting stakeholder needs.
- The customer success measure can be tested during the pilot.

### 34. Technical scoping, sequencing, and delivery tradeoffs
**Roadmap nodes covered:** Technical Scoping & Sequencing; Tradeoffs: Scope, Speed, Quality  
**Listen:** 34 minutes  
**What it covers:** Dependency mapping, thin slices, risk-first sequencing, build-versus-buy, backlog shaping, quality thresholds, and communicating tradeoffs without hiding risk.  
**Why an FDE cares:** Customer urgency is real, but an FDE must choose the smallest credible sequence that produces evidence while protecting safety, operability, and future maintainability.  
**Tools:** dependency map, impact/effort/risk matrix, milestone plan, RAID log, ADR, release checklist.

**Chapter project (test) — Sequence the customer pilot**  
**Goal:** A sequence that produces usable customer evidence before the full system exists, with the tradeoffs stated rather than hidden.  
**Constraints:** Slices must be independently testable. Sequencing is driven by customer value and risk reduction, not by what is interesting to build. Irreversible decisions are flagged before they are made. Security, data boundaries, and observability are not deferrable polish. Every deferred item needs a reason and a trigger to revisit it.  
**Required artifacts:** the slice breakdown with prerequisites, unknowns, and irreversible decisions; the prioritized first two slices with their rationale; one explicit tradeoff naming the quality bar that stays non-negotiable; a rollback and contingency plan.

**Pass bar**
- The sequence creates usable evidence before the full system exists.
- Every deferred item has a reason and a trigger for reconsideration.
- Security, data boundaries, and observability are not treated as optional polish.

### 35. Business acumen, enterprise workflow, and AI ROI
**Roadmap nodes covered:** Business Acumen; Enterprise Workflow; ROI & AI Impact  
**Listen:** 38 minutes  
**What it covers:** Enterprise buying and change processes, procurement/security review, operating costs, benefit measurement, adoption, ROI models, and limits of AI-impact claims.  
**Why an FDE cares:** A technically sound pilot that cannot navigate approvals, prove economic value, or fit a real workflow will not become an adopted deployment.  
**Tools:** ROI model, value hypothesis, enterprise-readiness checklist, security/procurement packet, adoption metrics, executive readout.

**Chapter project (test) — Make the FieldOps business case**  
**Goal:** A sponsor can see what this is worth, what it costs to run, and which claims are supported by evidence rather than enthusiasm.  
**Constraints:** Every input is labelled and every uncertainty is exposed; a single confident number is a fail. Ongoing cost includes cloud, model usage, and the people who operate it. You must state plainly what the AI cannot be credited with. Success is measured in workflow outcomes, not model usage.  
**Required artifacts:** a labelled baseline for time-to-triage, rework, escalation rate, and business impact; a benefit and cost model with adoption sensitivity; an enterprise-readiness checklist naming every approver; a one-page readout offering continue, adjust, pause, or stop.

**Pass bar**
- The ROI calculation exposes inputs and uncertainty.
- Success is measured in workflow outcomes, not only model usage.
- The customer knows the approvals needed before a production commitment.

### 36. Stakeholder management and the product feedback loop
**Roadmap nodes covered:** Stakeholder Management; Product Feedback Loop  
**Listen:** 34 minutes  
**What it covers:** Stakeholder cadence, decision rights, demos, feedback capture, triage, prioritization, closing the loop, and separating a loud request from validated product evidence.  
**Why an FDE cares:** The field is a continuous negotiation between operators, executives, security, product, and engineering. Feedback must turn into a visible decision or trust erodes.  
**Tools:** stakeholder register, meeting decision log, feedback board, prioritization rubric, pilot dashboard, release notes.

**Chapter project (test) — Operate a pilot feedback loop**  
**Goal:** Feedback from a demo becomes a visible decision, including for the requests you decline.  
**Constraints:** Capture observations, not promises — agreeing to a feature in the room is a fail. Every item gets a type, an owner, a status, and a decision date. Prioritization weighs customer outcome, risk, effort, and reuse across customers. At least one request must be deferred transparently, with the reason given to the person who asked.  
**Required artifacts:** a stakeholder register with influence, needs, preferred evidence, cadence, and decision authority; demo notes from three synthetic incidents; the classified and prioritized feedback list; a written update stating what will happen, what will not, and why.

**Pass bar**
- Feedback has an owner, status, evidence, and decision date.
- A stakeholder can see how their input was handled.
- At least one requested feature is correctly deferred with a transparent rationale.

### 37. Communication and technical writing
**Roadmap nodes covered:** Communication; Technical Writing  
**Listen:** 33 minutes  
**What it covers:** Audience-aware explanation, concise status reporting, decision records, runbooks, handoff documentation, incident communication, and writing that is operational under pressure.  
**Why an FDE cares:** An FDE’s influence travels through documents. Clear writing lets the customer operate, approve, and troubleshoot the system without depending on a single embedded engineer.  
**Tools:** ADR template, runbook, architecture diagram, status update, release notes, onboarding guide, incident template.

**Chapter project (test) — Write the FieldOps operator and engineer handoff**  
**Goal:** The customer can run and troubleshoot this system without you in the room.  
**Constraints:** Documents are tested, not merely written: someone unfamiliar follows the runbook against a synthetic failure and the unclear step gets fixed. Audience shapes the writing — an executive update and an operator incident note may not be the same text. Confirmed facts, assumptions, decisions, and requests must be distinguishable.  
**Required artifacts:** an operator quick-start covering submit, review, approve or reject, find sources, and report a problem; an engineering runbook for health checks, common failures, rollback, and escalation; a decision-record index; one sponsor update and one operator incident note; the correction the runbook test produced.

**Pass bar**
- A new operator can complete the core workflow unaided.
- An engineer can diagnose a known failure from the runbook and traces.
- Status writing distinguishes confirmed facts, assumptions, decisions, and requests.

### 38. Capstone: complete applications, an observable agent, and customer handoff
**Roadmap nodes covered:** Complete Apps; Complete App with Observability; Build your Agent  
**Listen:** 45 minutes  
**What it covers:** Integrating the complete application, exercising the agent under realistic constraints, release-readiness review, demonstration design, and final customer handoff.  
**Why an FDE cares:** The role culminates in a system that works in a customer context: useful without unsafe autonomy, diagnosable under failure, deployed reproducibly, and accompanied by a credible adoption plan.  
**Tools:** end-to-end test suite, deployment checklist, observability dashboard, threat model, pilot readout, demo script, handoff packet.

**Chapter project (test) — Ship the FieldOps Copilot pilot candidate**  
**Goal:** One synthetic incident travels the entire system — intake to operator decision to audit record — and the resulting package is something a real customer could evaluate.  
**Constraints:** No manual database repair, no step performed by hand that is not documented, no capability the agent should not have. The evaluation suite, the abuse cases, a dependency-failure fallback, and a rollback rehearsal must all be run, not described. Remaining risks and open decisions are part of the deliverable, not omissions from it.  
**Required artifacts:** the integrated working slice; the end-to-end synthetic scenario evidence including citation, approval, audit, and trace; the run results for evaluation, abuse, fallback, and rollback; the customer handoff package; a demonstration record naming the next decision for the sponsor, the operator, and the security reviewer.

**Pass bar**
- A synthetic incident can be traced end to end without manual database repair.
- The agent is grounded, bounded, approval-gated, evaluated, and observable.
- The deployment can be reproduced from reviewed artifacts.
- The handoff clearly identifies pilot evidence, remaining risks, and the path to a real customer launch.

---

## Coverage audit

The 38 chapters cover the live map’s FDE nodes—**Introduction, From X to FDE, Roles & Responsabilities** (the live-map spelling; source heading: *Roles & Responsibilities*), **Linux Skills, Frontend Skills, Backend Skills, DSA & System Design, AI Engineering Skills, DevOps Skills, Discovery & Scoping, Requirements Gathering, Technical Scoping & Sequencing, Tradeoffs: Scope, Speed, Quality, Business Acumen, Enterprise Workflow, ROI & AI Impact, Stakeholder Management, Product Feedback Loop, Communication, and Technical Writing**—and the distinct supporting source topics:

- **Foundations and full stack:** Computer Science; C++; Java / Scala; Go; Python; Shell / Bash; Git & GitHub; Full Stack; Frontend; HTML; CSS; JavaScript; JavaScript / TypeScript; React; Frontend Apps; Backend; Node.js; APIs Design; API Security; Authentication; GraphQL; SQL; PostgreSQL; NoSQL Databases; System Design; Software Architecture.
- **AI application engineering:** AI Engineering; LLM Fundamentals; Choosing your Model Provider; Prompt Engineering; Prompt Management; Prompt Versioning; Cursor; Claude Code; Codex; Gemini; Vibe Coding; Tools & Functions; MCP; AI Agents; Agent Architectures; Memory & State Management; RAGs; Vector DBs; Multi-Agents; Building Eval Pipelines; Regression Testing; Latency and Cost Optimization; Inference Optimization; Build your Agent.
- **Data, ML, and operations:** Data Engineering; Data Pipelines; Airflow; Spark; MLOps; Model Deployment; Managed ML Services; DevOps & CI/CD; GitHub Actions; Docker; Containers; Cloud Platforms; AWS; Azure; GCP; Terraform; Kubernetes; Observability; Security; Data Privacy & Compliance; AI Governance.
- **Delivery and capstone:** Complete Apps; Complete App with Observability, plus all customer-delivery nodes named above.

Total listening time across the 38 chapters is about 23 hours, with no chapter under 30 minutes. Chapters 1 through 6 show their **measured** rendered durations; later chapters show the planned length their scripts are written to.

## Where each chapter's artifacts live

This document is the curriculum contract. Each chapter is shipped as three files, named with the same number and slug:

- `docs/lessons/NN-slug.md` — the full narration script, including a pronunciation and pause header that is not spoken.
- `docs/guides/NN-slug.md` — the test-style project guide: goal, starting state, constraints, required artifacts, self-grade rubric, and inverted hints at the very end.
- `media/NN-slug.mp3` — the rendered audio, verified against the 28-minute floor.

Audio is rendered with the course repository's edge-tts pipeline using a single consistent narration voice. See `docs/project-context.md` for the length policy, the guide rules, and the rendering contract.
