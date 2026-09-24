---
chapter: 8
title: "Project test: style the intake and priority confirmation"
roadmap_nodes: ["CSS"]
lesson: docs/lessons/08-css-operational-interfaces.md
format: test
---

# Chapter 8 project test — Style the intake and priority confirmation

A test, not a walkthrough. It defines the finished condition and the scoring. It does not name properties, values, or layout techniques; choosing those is the assessment.

Listen to the chapter 8 lesson, then close it and work from documentation.

## Starting state

- The chapter 7 intake page: semantic, labelled, keyboard operable, honest that submission is local.
- The chapter 6 split of reusable core, customer configuration, and customer-specific adapter.
- No stylesheet yet, or only browser defaults.

Start the stylesheet from an empty file. No framework, no starter theme, no copied token set.

## Goal

Make the intake page and its confirmation readable and correctly prioritised at a glance, on a wide dispatch monitor and on a narrow field laptop, for an operator who may not perceive colour, may be at high zoom, and may be in a hurry.

The chapter 7 document must survive unchanged in structure. This is a layer on top, not a rebuild.

## Constraints

1. **No CSS framework, no component library, no build step.**
2. **Two token layers.** A small set of raw values, and semantic roles named for meaning. Rules reference semantic roles only — no raw value and no literal colour appears in a component rule.
3. **Five complete state recipes** — normal, warning, critical, success, disabled — each specifying background, foreground, border, text cue, and a non-colour visual cue.
4. **Redundant encoding.** No state is distinguishable by colour alone. This is verified in greyscale, not by argument.
5. **Document order is unchanged**, and no visual reordering diverges from it.
6. **Focus is visible on every interactive element against every surface it can appear on.**
7. **No horizontal scrolling** at a narrow viewport, and the page remains usable at 400% zoom.
8. **Native controls stay native.** You may restyle them; you may not hide one and rebuild its behaviour.
9. **User preferences honoured** for reduced motion and colour scheme, or not claimed at all.
10. **No component library and no second screen.** One form, one confirmation region.

Out of scope: behaviour and async states (chapter 9), components and the incident queue (chapter 10), anything server-side.

## Artifacts to produce

| Artifact | Content |
| --- | --- |
| Stylesheet | Hand-written, organised so a stranger can predict where a rule lives. |
| Token note | Every semantic role, the raw value behind it, and its measured contrast ratio against the surfaces it is used on. |
| Screenshot set | Before, after, greyscale, and 400% zoom — each at a stated width and zoom level, dated. |
| Configuration boundary note | One paragraph: which tokens a customer may override for branding, which are product decisions, and why. |
| Breakpoint log | Each width where you changed the layout, and the specific problem that width solved. |

## Rubric

Every **Required** row must reach "meets". At least two **Distinguishing** rows must reach "meets" to pass.

| # | Criterion | Weight | Fails | Meets | Exceeds |
| --- | --- | --- | --- | --- | --- |
| 1 | Redundant state encoding | Required | Any state readable only by colour | All five states survive the greyscale test | Non-colour cue is meaningful, not merely present |
| 2 | Contrast | Required | Unmeasured, or any body text under roughly 4.5 to 1 | Every pair measured and recorded, including disabled and focus indicator | Contrast holds in both themes if a second theme exists |
| 3 | Focus visibility | Required | Outline removed, or invisible on any surface | Deliberate indicator, visible everywhere, distinguishes keyboard navigation | Indicator designed as a token, reused consistently |
| 4 | Order integrity | Required | Visual order diverges from document order anywhere | Tab order still matches visual order after styling | Verified by a repeated keyboard walk, recorded |
| 5 | Responsive behaviour | Required | Horizontal scroll at narrow width, or unusable at 400% zoom | Both pass; narrow layout is the default | Layout adapts intrinsically rather than by enumerated device widths |
| 6 | Token discipline | Required | Literal values scattered through rules | Two layers, semantic references only | A brand palette could be applied by overriding raw values alone |
| 7 | Hierarchy | Distinguishing | Everything emphasised, or nothing is | The two-second glance returns the element you intended | Strongest signal reserved for the state that requires action |
| 8 | Native control integrity | Distinguishing | A control hidden and reimplemented | Controls restyled, behaviour untouched | Styled visuals driven by the control's own states |
| 9 | Content robustness | Distinguishing | Breaks on a long title, long service name, or all errors visible | Survives the hostile-content pass | Documented the threshold at which each element degrades |
| 10 | Delivery evidence | Distinguishing | No screenshots | Full screenshot set, dated, at stated conditions | Note explaining what a stakeholder should conclude from the pair |

## Self-check before you call it done

- Look away, look back for two seconds, look away. What did you see? Is it what you intended to win?
- Desaturate a screenshot. Can you still tell critical from normal?
- If a customer sent you three brand colours tomorrow, how many rules would you edit?
- Where does your layout break, and did you find that width or guess it?
- Which of your colours is the strongest signal, and is it reserved for something that genuinely needs action?

## Time and depth

A focused sitting. If you are building buttons you do not yet have a use for, you have drifted into chapter 10.

## Stuck hints

Read only after a real attempt. Printed upside down on purpose.

˙sǝuo ǝןqɐɹnƃᴉɟuoɔ ǝɥʇ ǝɹɐ ǝsoɥ⊥ ˙ןᴉɐɯǝ uɐ uᴉ ǝɯɐu pןnoʍ ɯɐǝʇ puɐɹq ɐ ǝuo ɥɔᴉɥʍ ʞsɐ 'ǝןqɐɹnƃᴉɟuoɔ-ɹǝɯoʇsnɔ sᴉ uǝʞoʇ ɥɔᴉɥʍ ǝpᴉɔǝp ʇouuɐɔ noʎ ɟI ˙9
˙ʎɹɐssǝɔǝuun ɯǝɥʇ ɟo ʇsoɯ ǝʞɐɯ pןnoʍ ʇnoʎɐן ƃuᴉddɐɹʍ ɐ ɹǝɥʇǝɥʍ ʞsɐ 'sǝןnɹ ɔᴉɟᴉɔǝds-ɥʇpᴉʍ ʎuɐɯ ƃuᴉʇᴉɹʍ ǝɹɐ noʎ ɟI ˙ϛ
˙sǝsɐɔ oʍʇ ǝsoɥʇ sǝɥsᴉnƃuᴉʇsᴉp ʇɐɥʇ ɹoʇɔǝןǝs ǝʇɐʇs ǝɥʇ ʇuɐʍ noʎ 'ƃuᴉqqɐʇ ɹǝʇɟɐ ʇɥƃᴉɹ ʇnq ʞɔᴉןɔ ɐ ɹǝʇɟɐ ƃuoɹʍ sʞooן snɔoɟ ɟI ˙ㄣ
˙ʍoןɟɹǝʌo ǝɥʇ ƃuᴉpᴉɥ uɐɥʇ ɹǝɥʇɐɹ ʇuǝɯǝןǝ ʇɐɥʇ puᴉℲ ˙ɹnouoɥ ʇouuɐɔ ʇᴉ ɥʇpᴉʍ ɯnɯᴉuᴉɯ ɐ sɐɥ ʇuǝɯǝןǝ ǝuo 'sʎɐʍǝpᴉs sןןoɹɔs ɥʇpᴉʍ ʍoɹɹɐu ǝɥʇ ɟI ˙Ɛ
˙ɹnoןoɔ ʇxǝʇ ǝɥʇ ƃuᴉʇɥƃᴉɟ uɐɥʇ ɹǝɥʇɐɹ ǝɔɐɟɹns ǝɥʇ uǝʇɥƃᴉן ɹo uǝʞɹɐᗡ ˙pǝʇɐɹnʇɐs ooʇ ʎןqɐqoɹd sᴉ punoɹƃʞɔɐq ɹnoʎ 'ƃuᴉןᴉɐɟ sdǝǝʞ ʇsɐɹʇuoɔ ɟI ˙ᄅ
˙uoᴉʇɐɹnʇɐsǝp ǝʌᴉʌɹns ɹnoɟ ןןɐ puɐ dɐǝɥɔ ǝɹɐ ɹnoɟ ןן∀ ˙pɹoʍ ʇᴉɔᴉןdxǝ uɐ ɹo 'ssǝuʞɔᴉɥʇ ɹǝpɹoq ɐ 'ǝdɐɥs ɐ 'ʇɥƃᴉǝʍ ʎɹʇ 'puᴉɯ oʇ sǝɯoɔ ƃuᴉɥʇou puɐ ǝnɔ puoɔǝs ɐ spǝǝu ǝʇɐʇs ɐ ɟI ˙Ɩ
