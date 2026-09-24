# FullStack in Audio — Forward Deployed Engineer Course Context

## Goal

Turn the Forward Deployed Engineer (FDE) roadmap into an audiobook-first course that reliably converts listening into applied skill. The course is not a generic full-stack survey: its learning sequence follows the FDE roadmap's technical, operational, and customer-delivery topics, and all practice work accumulates into one customer-deployable system.

The learner's running build is **Promise Desk** for **Mato Crafts**, a handmade jewellery studio in Patan whose store Niyalo already shipped. The operational problem is a promise the bench cannot keep. Chapter 1 is the live course. A later chapter is written when asked, and it extends this charter rather than starting from a blank company.

## Source boundary and coverage policy

- Primary map: [roadmap.sh Forward Deployed Engineer](https://roadmap.sh/forward-deployed-engineer), retrieved through its public roadmap API on 2026-09-17.
- Source content cross-check: [`nilbuild/developer-roadmap`](https://github.com/nilbuild/developer-roadmap), `roadmaps/forward-deployed-engineer/content/`.
- The live map contains 20 curricular topic/subtopic nodes, plus explicit links to the Frontend, Backend, Linux, DSA, System Design, AI Engineer, and DevOps roadmaps. The chapter list includes every live FDE node and linearizes the named linked tracks only where the FDE source supplies the supporting topic content.
- The source directory contains 99 content records. It includes several renamed or duplicate records (for example, two API-design file names share one node ID). These are treated as aliases, not as extra learning requirements. The course names the distinct source topics once and preserves exact roadmap names in each chapter's “Roadmap nodes covered” line.
- Topic order is pedagogical, not a claim that the visual map is a single prerequisite chain. The course moves from foundations to building, then operating, governing, and delivering the same system.

## Delivery model: listen, then practice

Every chapter is shipped as a paired unit:

1. **Listen:** a full audio lesson teaches everything needed to *attempt* the chapter project unaided — concepts, tradeoffs, failure modes, verification method, and the customer context an FDE is working inside. It is a taught chapter, not a topic survey.
2. **Pause and plan:** the learner names the change they will make to Promise Desk before opening tools.
3. **Sit the project:** the learner opens the chapter's project guide, which is written as a test. It states the goal, constraints, starting state, required artifacts, and a self-grade rubric. It contains no implementation recipe.
4. **Self-grade:** the learner scores their own result against the rubric and records one short decision note or artifact.
5. **Carry forward:** the next chapter starts from the working state just built.

### Chapter length policy (locked)

- Every chapter's audio runs **at least 30 minutes**. The target band is **32–40 minutes**, and a chapter may run up to **45 minutes** when the topic genuinely needs it.
- Narration is measured at **~145 words per minute**, so a chapter script is **about 4,400–5,800 spoken words**. Scripts are sized to the low end only when the topic is narrow.
- A render below **28 minutes** is treated as a defect: expand the script and re-render. Under-length audio is not shipped.
- The chapter list's **Listen** figure is the audio duration only. It excludes planning, building, and debugging time. Practice is never time-boxed; it ends at demonstrated behavior.

### Depth bar for a chapter script

A chapter is long enough only when a learner who has *only* listened could reasonably start the project. That means the script must carry:

- the concept and its vocabulary, defined in plain language;
- at least one worked example narrated as reasoning, not as code;
- the tradeoff space: what the alternatives are and what each one costs;
- the common failure modes and what they look like from the outside;
- how to verify the result — what evidence proves the work is correct;
- the FDE customer situation the topic shows up in, including who gets hurt when it is done badly.

## Audio lesson expansion rules

The chapter list is an outline, not lesson prose. Each chapter is expanded into an audio-safe lesson script at `docs/lessons/NN-slug.md` with this structure:

| Segment | Purpose |
| --- | --- |
| TTS header (not spoken) | Pronunciation and pause notes for the renderer, inside a skip block. |
| Cold open | Name the customer situation this chapter exists to survive. |
| What | Define the concept, boundaries, and vocabulary in plain language. |
| Why | Connect it to a concrete FDE decision, customer risk, or delivery outcome. |
| How | Walk a decision process, an architecture, or an implementation approach in spoken description, including a worked example. |
| Failure modes | Narrate what going wrong looks like and how it is detected. |
| Verification | State what evidence proves the work is correct. |
| Project handoff | Point at the project guide and state the goal and constraints only. |
| Recap | Restate the key decisions and what the learner can now do. |

Do **not** read raw source code, long commands, URLs, file paths, JSON, stack traces, tables, or punctuation-heavy configuration aloud. Audio should explain intent and decision-making; the project guide carries exact artifact names. Avoid inflated claims, vendor-specific guarantees, and examples that suggest production safety without tests, review, observability, and security controls.

## Project guides are tests, not tutorials

Each chapter ships a companion guide at `docs/guides/NN-slug.md`. It is written as an exam paper for a working engineer, and it has a fixed shape:

| Section | Contents |
| --- | --- |
| Goal | One sentence naming the outcome, in the customer's terms. |
| Starting state | What must already exist from earlier chapters, and what may be assumed. |
| Constraints | Hard rules: what may not be used, what must remain true, what is out of scope. |
| Required artifacts | The named deliverables that will be graded. |
| Self-grade rubric | Observable criteria with a pass bar, written so a learner can score honestly. |
| Stretch | Optional extra difficulty for a learner who finished comfortably. |
| If stuck | Inverted hints, at the very end, clearly fenced off. |

Rules that hold for every guide:

- **No implementation recipe.** No numbered build steps, no code, no command sequences, no library choices made on the learner's behalf. State the required outcome and let the learner find the route.
- **From scratch or from prior state.** Practice is typed and decided, never pasted. A chapter either starts from an empty file or from the Promise Desk state the previous chapter left behind.
- **Hints are inverted and last.** The "If stuck" section is printed upside-down in spirit: it is a list of questions and nudges, ordered from gentlest to most specific, and it is explicitly *not* part of the audio. A learner who listened to the chapter should never hear the hints.
- **Grading is observable.** A rubric line must describe something the learner can see, run, or show another engineer — not a feeling of completeness.
- **Mock is allowed; pretending is not.** A guide may permit a local or mock integration, but it must require the learner to name what would have to change before a real customer deployment.

## TTS pipeline (edge-tts is the default renderer)

The renderer lives in the course repository at `tts/render_lesson.py`; the repository README explains setup and per-chapter rendering. The contract:

1. **Voice and pace.** `edge-tts` with `en-US-AndrewNeural` at `-14%` rate. Measured on this pipeline, that is ~146 words per minute, which matches the curriculum's listen-time math.
2. **The script is the source of truth.** The renderer strips frontmatter, the pronunciation header (a `tts:skip` block), headings, tables, code fences, link targets, list markers, and emphasis. `[pause]` becomes a beat of silence. A small substitution table spells out forms the voice mangles.
3. **Render per chapter.** Long scripts are split at paragraph and sentence boundaries, rendered with retries, and concatenated.
4. **Verify every render.** The file must be a real mp3 stream, and its duration must clear the 28-minute floor. The renderer exits nonzero on a short or malformed render.
5. **Name audio stably.** `media/NN-slug.mp3`, matching the lesson file name exactly, so lesson, guide, and audio line up by number and slug.
6. **Spot-listen.** Check the opening, one transition, any abbreviation-heavy passage, and the final minute of every render. Re-render only after fixing the script or the pronunciation notes.

**Optional later renderers**

- **ElevenLabs:** use only after a voice, licensing, privacy, and cost decision; keep the same approved narration script and manifest contract.
- **NotebookLM:** use as an optional research or alternate-summary workflow, not as the canonical source of curriculum truth and not as a substitute for the approved narration script.

## Phases

1. **Extract** — snapshot the FDE map and reconcile its topic/content records. *(Done.)*
2. **Sequence** — one customer, one accumulating build. Chapter 1 is live. Later chapters are written when asked.
3. **Expand for audio** — write full What/Why/How narration scripts and test-style project guides. *(In progress, chapter by chapter.)*
4. **Render** — generate per-chapter audio with the edge-tts pipeline, verify duration, and run listening QA. *(In progress, chapter by chapter.)*
5. **Listen then practice** — release the paired lesson, project guide, and rubric in chapter order.
6. **Improve** — use learner completion notes and project failures to clarify future scripts without silently changing roadmap coverage.

## Standing constraints

- Live curriculum is the chapters that have been written. Right now that is chapter 1.
- Every shipped chapter needs all three artifacts: a lesson script, a project guide, and a verified audio file of at least 30 minutes.
- Audio is spoken prose only. No code, JSON, URLs, file paths, or long commands are read aloud.
- Project guides are tests. No implementation recipe, and hints only at the very end where the audio never reaches them.
- No web application or course platform is scaffolded. The repository holds the live chapter, the archived draft, and the Promise Desk work.
- A project may use a local or mock integration at first, but must require the learner to identify what would need to change before a real customer deployment.
