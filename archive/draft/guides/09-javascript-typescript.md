---
chapter: 9
title: "Project test: typed asynchronous intake"
roadmap_nodes: ["JavaScript / TypeScript", "JavaScript"]
lesson: docs/lessons/09-javascript-typescript.md
format: test
---

# Chapter 9 project test — Typed asynchronous intake

A test. It states the finished condition and the scoring. It does not give you the state machine, the type definitions, or the request code.

Listen to the chapter 9 lesson, then close it.

## Starting state

- The chapter 7 intake page with its labels, grouping, error summary, and keyboard path.
- The chapter 8 token layer and state recipes.
- The chapter 3 priority rule, in Python, as the reference policy.
- No scripting beyond the minimal submission interception you may have added in chapter 7.

Everything typed in this chapter is new and hand-written.

## Goal

Give the intake page real asynchronous behaviour against a mock service that implements a contract you wrote down first, with every request state handled and accidental double submission impossible.

## Constraints

1. **No UI framework.** No React, no Vue, no Svelte. Modules and the document API only. Framework work is chapter 10.
2. **One shared incident representation**, in its own module, with **two distinct shapes**: the draft intake produces, and the created incident the service returns.
3. **All external data is parsed at runtime** before being treated as a domain value. A type annotation alone does not satisfy this row.
4. **Request state is a tagged union** with exactly one active alternative. Boolean-and-optional bags fail this test.
5. **The displayed priority is the service's value.** Any browser-side calculation is either removed or visibly labelled a preview.
6. **The mock implements a written contract** and can inject every failure mode on demand: validation rejection, transient failure, timeout, unexpected server failure.
7. **A deadline exists** on the request, and expiry produces its own distinct message.
8. **No input is lost on any error path.**
9. **Operator-supplied content is rendered as text, never as markup.**
10. **The interface visibly states that the service is simulated.**
11. **Chapter 7 behaviour survives**: accessible names intact, per-field errors intact, error summary still receives focus, and dynamic regions announce.
12. **Minimal dependencies.** A type compiler and a test runner. Justify anything else in writing.

Out of scope: components, routing, the incident list (chapter 10), any real server (chapter 11), authentication (chapter 12).

## Artifacts to produce

| Artifact | Content |
| --- | --- |
| Domain module | Draft and created incident shapes, severity and impact as stable codes. |
| Service seam | One function signature, a mock implementation behind it, fault injection documented. |
| Contract note | Success shape, rejection shape (field-and-message pairs), failure shape, and status meanings — written before the mock. |
| State table | Each of the five states: what the operator sees, what is announced, where focus goes, and why the text is actionable. |
| Tests | One success, one recoverable failure, one double-submit guard. |
| Authority note | One paragraph: which browser checks are courtesies, and what will enforce each on the server. |

## Rubric

Every **Required** row at "meets". At least three **Distinguishing** rows at "meets" to pass.

| # | Criterion | Weight | Fails | Meets | Exceeds |
| --- | --- | --- | --- | --- | --- |
| 1 | Boundary parsing | Required | External data trusted because it is annotated | Runtime shape check before domain use; rejects malformed responses | Failure to parse produces its own honest operator message |
| 2 | State modelling | Required | Booleans and optionals; impossible combinations representable | Tagged union, five mutually exclusive states, all rendered | Compiler enforces exhaustiveness |
| 3 | Double submission | Required | A fast double press or double keyboard activation produces two calls | Exactly one call under every activation pattern tried | Out-of-order responses discarded as well |
| 4 | Server authority | Required | Browser-computed priority displayed as fact | Displayed value is the service's | Browser preview, if kept, is labelled and visually distinct |
| 5 | Input preservation | Required | Any error path clears the form | All five paths preserve input | Long description survives repeated failures unchanged |
| 6 | Safe rendering | Required | Operator content inserted as markup anywhere | Text insertion throughout | A deliberate test proves markup in a description is not executed |
| 7 | Error usefulness | Distinguishing | Generic "something went wrong" | Five distinct messages, each naming a next action | Timeout message tells the operator to check before retrying |
| 8 | Contract discipline | Distinguishing | Mock invented ad hoc | Contract written first, mock implements it | Note predicts what chapter 11 must match, item by item |
| 9 | Announcement and focus | Distinguishing | State changes silent; focus lost on success | Dynamic regions announce; focus destination decided per state | Verified with the accessibility representation, not assumed |
| 10 | Test durability | Distinguishing | Tests query internal structure | Tests query by role and accessible name | Tests would survive the chapter 10 component rewrite |
| 11 | Verification | Distinguishing | Happy path only | Throttled network, offline, all fault injections, payload inspected | Findings recorded, including one thing you fixed as a result |

## Self-check before you call it done

- Press submit twice as fast as you can, then again with the keyboard. How many calls?
- Put markup with a script in the description and submit. What happens?
- Disconnect the network mid-request. What does the operator read, and is their text still there?
- If chapter 11's server returns a field you did not expect, what does your code do?
- Which value on this screen would be wrong if the customer's laptop clock were two days off?
- Name the one policy that must never be implemented twice.

## Time and depth

A focused sitting plus a verification pass. If you are building components or a router, stop — that is chapter 10.

## Stuck hints

Read only after a real attempt. Printed upside down on purpose.

˙sǝɯɐu ǝןqᴉssǝɔɔɐ ɹᴉǝɥʇ ʎq sןoɹʇuoɔ ɹoɟ ʞs∀ ˙ǝɹnʇɔnɹʇs oʇ punoq ǝɹɐ ʎǝɥʇ 'ǝpoɔ ǝʌoɯ noʎ ǝɯᴉʇ ʎɹǝʌǝ ʞɐǝɹq sʇsǝʇ ɹnoʎ ɟI ˙9
˙ʇuǝᴉןɔ ɹǝɹǝʌǝןɔ ɐ ʇou 'ɹǝʍsuɐ ǝɥʇ ǝɹɐ ʎǝʞ ʎɔuǝʇodɯǝpᴉ ɹǝʇɐן ǝɥʇ puɐ ǝƃɐssǝɯ ʇsǝuoɥ ǝɥ⊥ ˙snonƃᴉqɯɐ ʎןǝuᴉnuǝƃ sᴉ ʇᴉ — ʇɔǝɹɹoɔ sᴉ ʇɐɥʇ 'ǝןqɐʌןosǝɹun sןǝǝɟ ǝsɐɔ ʇnoǝɯᴉʇ ǝɥʇ ɟI ˙ϛ
˙pɐǝɹ noʎ spןǝᴉɟ ǝɥʇ ʎןuo ʞɔǝɥↃ ˙ǝsn ʇou op noʎ sƃuᴉɥʇ ƃuᴉʞɔǝɥɔ ʎןqɐqoɹd ǝɹɐ noʎ 'snoɯɹouǝ ןǝǝɟ sʞɔǝɥɔ ǝɯᴉʇunɹ ɹnoʎ ɟI ˙ㄣ
˙ʎɐʍʎuɐ ʇsᴉxǝ oʇ ʇɥƃno ʇɐɥʇ ʇuǝɯǝןǝ ʎɹɐɯɯns ɐ ɹo ƃuᴉpɐǝɥ ɐ ƃuᴉssᴉɯ sᴉ ǝʇɐʇs ǝɥʇ ןɐuƃᴉs ɐ sᴉ ʇɐɥʇ 'snɔoɟ ʇnd oʇ ǝןqᴉsuǝs ǝɹǝɥʍou sɐɥ ǝʇɐʇs ɐ ɟI ˙Ɛ
˙ʇןnsǝɹ ɐ ƃuᴉʎןddɐ ǝɹoɟǝq ʇᴉ ǝɹɐdɯoɔ puɐ ʇsǝnbǝɹ ʇuǝɹɹnɔ ǝɥʇ ɹoɟ uǝʞoʇ ɐ dǝǝʞ 'ǝʇɐʇs ɥsǝɹɟ ǝʇᴉɹʍɹǝʌo sǝsuodsǝɹ ɹǝpɹo-ɟo-ʇno ɟI ˙ᄅ
˙ןןɐɔ ǝɥʇ ǝɹoɟǝq 'ɟןǝsʇᴉ ǝnןɐʌ ǝʇɐʇs ǝɥʇ uo pɹɐn⅁ ˙ǝuoןɐ ǝʇnqᴉɹʇʇɐ pǝןqɐsᴉp ɐ ɥʇᴉʍ ƃuᴉpɹɐnƃ ʎןqɐqoɹd ǝɹɐ noʎ 'ǝןqᴉssodɯᴉ uoᴉssᴉɯqns ǝןqnop ǝʞɐɯ ʇouuɐɔ noʎ ɟI ˙Ɩ
