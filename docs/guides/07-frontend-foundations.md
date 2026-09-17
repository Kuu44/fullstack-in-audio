---
chapter: 7
title: "Project test: the incident intake page"
roadmap_nodes: ["Frontend Skills", "Frontend", "HTML"]
lesson: docs/lessons/07-frontend-foundations.md
format: test
---

# Chapter 7 project test — The incident intake page

This is a test, not a tutorial. It states what must be true when you are finished and how your result will be judged. It does not tell you which elements or attributes to use; deciding that is the assessment.

Listen to the chapter 7 lesson first. Then close it. Work from documentation and from your own reasoning.

## Starting state

You may begin only from what earlier chapters produced:

- The FieldOps Copilot delivery charter (chapter 1), including the target operator and the measurable outcome.
- The triage priority rule and its Python implementation (chapters 2–3).
- The repository, readme, and full-stack seam diagram (chapter 4).
- The architecture split of reusable core, customer configuration, and customer-specific adapter (chapter 6).

New in this chapter: one document file, created empty, and nothing else. No project scaffolding tool, no starter template, no copied form.

## Goal

Produce the incident intake page that a FieldOps Copilot operator will use to report an incident, and prove it is usable by someone who cannot use a mouse and cannot see the screen.

The page collects exactly five things: a short title, a severity, an affected service, a business impact, and a description. It reports back what it captured. It does not pretend to have filed anything anywhere.

## Constraints

Non-negotiable:

1. **No framework, no styling system.** No component library, no CSS framework, no build step. Scripting is permitted only to intercept submission and render feedback; it may not be required for the page to be readable and navigable.
2. **Every control has a visible label that is programmatically associated with it.** Placeholder text does not count as a label.
3. **Severity is a grouped set of visible options with a caption that states the question**, and each option carries a definition an operator can act on.
4. **Required fields are indicated in text**, not by colour or a lone symbol.
5. **Every validation failure produces two things**: a message tied to the control that failed, and a summary of all failures that receives focus.
6. **A complete keyboard-only path exists** from page load to a successful submission, with focus visible at every stop.
7. **The page states in plain words that submission is local**, and that no service has received the record.
8. **Reading order matches logical order** with styling disabled.
9. **The affected-service list is marked in your notes as customer configuration**, consistent with the chapter 6 split.
10. **Nothing invented.** Do not add fields, screens, accounts, or a persistence illusion. Five fields, one page.

Explicitly out of scope: visual design (chapter 8), typed asynchronous submission (chapter 9), components and routing (chapter 10), any server (chapter 11).

## Artifacts to produce

Commit these to the repository alongside the page:

| Artifact | Content |
| --- | --- |
| The intake page | One document, hand-written. |
| Field decision note | Each of the five fields: control type chosen, why that type, what the stored value looks like, and which later chapter consumes it. |
| Keyboard walkthrough note | Your actual tab path in order, plus anything that surprised you and what you changed. |
| Accessibility finding | One defect you found by inspecting the accessibility representation of the page, the evidence, and the fix. |
| Honest limits line | One sentence in the readme naming what this page cannot yet do. |

## Rubric

Score each row. You need every **Required** row at "meets" or better, and at least two **Distinguishing** rows at "meets", to pass.

| # | Criterion | Weight | Fails | Meets | Exceeds |
| --- | --- | --- | --- | --- | --- |
| 1 | Semantic structure | Required | Generic containers carry meaning; no heading outline | Landmarks, one heading outline that describes the page, a real form region | Outline alone is a usable table of contents for the task |
| 2 | Label association | Required | Any control without an associated visible label | All five controls named correctly and unambiguously | Names read correctly out of context, with attached help text |
| 3 | Severity as a decision | Required | Free text or an ambiguous numeric scale | Grouped closed set, captioned, all options visible | Each option defined in the customer's language, definitions attached programmatically |
| 4 | Error feedback | Required | Errors absent, generic, or colour-only | Per-control message plus a focused summary; text says what to do next | Errors clear as soon as input becomes valid; wording tested against a hurried reader |
| 5 | Keyboard path | Required | Any control unreachable, or focus lost at any stop | Full path completed with visible focus throughout | Error summary entries move focus to the failing control |
| 6 | Honesty about state | Required | Page implies a record was filed | Local-only stated in the interface and the readme | Confirmation shows interpreted values, not just a success message |
| 7 | Data-model fit | Distinguishing | Fields collect text the priority rule cannot use | Every field yields a value the chapter 3 rule or a later layer can consume | Note names the exact downstream consumer per field |
| 8 | Degradation | Distinguishing | Page unusable at 200% zoom or unreadable without styling | Both checks pass | Documented what breaks and at what threshold |
| 9 | Scope discipline | Distinguishing | Extra fields, screens, or fake persistence added | Exactly the specified surface | Deferred ideas captured with the chapter that will address them |
| 10 | Verification evidence | Distinguishing | "It looks fine" | Four verification passes recorded with findings | A finding you fixed and a finding you consciously deferred, with reasons |

## Self-check before you call it done

Answer out loud, without looking at the page:

- What is the accessible name of your submit control, and would a stranger know what it does from that name alone?
- Which of your five fields would produce unusable data if an operator rushed, and what did you do about it?
- If a screen reader user submitted an empty form, what would they hear, in what order?
- Which part of this page is customer configuration and which part is product?
- What can an operator do here that they should not be able to do once a server exists?

## Time and depth

Expect a focused sitting, not a day. If it takes much longer, you are probably designing visuals — stop, that is the next chapter. If it takes much less, you probably skipped a verification pass.

## Stuck hints

Read these only after a genuine attempt. They are printed upside down so you do not absorb them by accident; rotate your device or transcribe them.

˙ʎɥʍ ǝʇou puɐ pןǝᴉɟ ǝɥʇ ǝʇǝןǝp 'pןǝᴉɟ ɐ ɟo ɹǝɯnsuoɔ ɯɐǝɹʇsuʍop ǝɥʇ ǝɯɐu ʇouuɐɔ noʎ ɟI ˙9
˙sqoɾ ʇuǝɹǝɟɟᴉp ɥʇᴉʍ spןǝᴉɟ oʍʇ sɐ 'ɥʇoq spǝǝu ʎןqɐqoɹd ʇᴉ 'ǝɔuo ʇɐ ʇǝs pǝsoןɔ ɐ puɐ ʇxǝʇ ǝǝɹɟ pǝǝu oʇ sɯǝǝs pןǝᴉɟ ɐ ɟI ˙ϛ
˙sǝnןɐʌ ƃuᴉɹǝpɹo ʇᴉɔᴉןdxǝ ɹoɟ ɥɔɐǝɹ ʇou oᗡ ˙ƃuoɹʍ sᴉ ɹǝpɹo ʇuǝɯnɔop ǝɥʇ 'pǝᴉןddɐ ƃuᴉןʎʇs ou ɥʇᴉʍ ƃuoɹʍ sןǝǝɟ ɹǝpɹo qɐʇ ɹnoʎ ɟI ˙ㄣ
˙ןoɹʇuoɔ ɐ oʇ uoᴉʇdᴉɹɔsǝp ɐ ƃuᴉɥɔɐʇʇɐ sᴉ qoɾ ǝןoɥʍ ǝsoɥʍ ǝʇnqᴉɹʇʇɐ uɐ sᴉ ǝɹǝɥ⊥ ˙pǝɥɔɐʇʇɐ ʇou ʇnq pǝuoᴉʇᴉsod sᴉ ʇᴉ 'ǝɯᴉʇ ƃuoɹʍ ǝɥʇ ʇɐ pɐǝɹ sᴉ ʇxǝʇ dןǝɥ ɟI ˙Ɛ
˙uoᴉssᴉɯqns pǝןᴉɐɟ ɐ ɹǝʇɟɐ ʎɹɐɯɯns ǝɥʇ oʇ snɔoɟ ǝʌoɯ ʇsnɯ ƃuᴉɥʇǝɯos :dǝʇs ǝuo ƃuᴉssᴉɯ ǝɹɐ noʎ 'ʇnd sʎɐʇs snɔoɟ ʇnq pǝɔunouuɐ ǝɹɐ sɹoɹɹǝ ɹnoʎ ɟI ˙ᄅ
˙ƃuoɹʍ sᴉ ɯǝɥʇ ƃuᴉpᴉɥ 'sǝʎ ɟI ˙ƃuᴉpᴉɔǝp ǝןᴉɥʍ sǝnןɐʌ ןןɐ ǝɹɐdɯoɔ oʇ spǝǝu ɹoʇɐɹǝdo ǝɥʇ ɹǝɥʇǝɥʍ ʞsɐ 'ʎʇᴉɹǝʌǝs ɹoɟ suoᴉʇdo ǝןqᴉsᴉʌ puɐ uʍopdoɹp ɐ uǝǝʍʇǝq ǝpᴉɔǝp ʇouuɐɔ noʎ ɟI ˙Ɩ
