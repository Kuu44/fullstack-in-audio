---
chapter: 10
title: "Project test: the React operator workspace"
roadmap_nodes: ["React", "Frontend Apps"]
lesson: docs/lessons/10-react-frontend-apps.md
format: test
---

# Chapter 10 project test — The React operator workspace

A test. It defines the finished condition, the constraints, and the scoring. It does not give you a component tree, a folder layout, or a routing configuration.

Listen to the chapter 10 lesson, then close it.

## Starting state

- The chapter 9 typed, asynchronous intake page: domain module, service seam with mock and fault injection, five-state request model, double-submit guard.
- The chapter 8 token layer and five state recipes.
- The chapter 7 accessibility properties: associated labels, grouped severity, error summary that receives focus.
- The chapter 6 split of reusable core, customer configuration, customer-specific adapter.

## Goal

Turn the single page into an operator workspace with an incident list and an incident detail route, with the intake form rebuilt as composed typed components, and with empty, loading, error, and not-found states that were designed rather than discovered.

## Constraints

1. **Rebuild the form from scratch as components.** Do not port the chapter 9 markup wholesale.
2. **Two routes**: a list, and a detail whose identity lives in the location. Both must survive a direct reload and open correctly in a new tab.
3. **No component library, no global state management library, no CSS framework.** Consume the chapter 8 tokens.
4. **Every component's props are typed.** No loosely typed props.
5. **State ownership is justified.** Every piece of state classified as server, location, interface, or form, with a named owner and a reason it is not held higher.
6. **All data access goes through the chapter 9 service seam**, still mocked, and the interface still visibly states that the service is simulated.
7. **Four states are implemented for each data view**: loading, populated, empty, failed — plus not-found on the detail route.
8. **An error boundary** prevents a rendering failure from producing a blank page.
9. **Route changes move focus and announce the new view.**
10. **Chapter 7 and chapter 9 properties survive, verified not assumed**: keyboard path, associated labels, focused error summary, five-state request model, impossible double submission, service-provided priority.
11. **Row navigation is a real link**, with an accessible name that identifies the incident.
12. **Files organised by feature**, with anything customer-specific identifiable as such.

Out of scope: a real server (chapter 11), authentication and roles enforcement (chapter 12), persistence (chapter 13), performance work (chapter 23).

## Artifacts to produce

| Artifact | Content |
| --- | --- |
| The application | Feature-organised, two routes, rebuilt form. |
| Component inventory | Each component: single responsibility, props, and whether it is core, configuration, or customer-specific. |
| State ownership table | Every piece of state: category, owner component, and why not higher. |
| Hostile seed data | Includes a critical incident, an overlong title, a description containing markup, and a record missing an optional field. |
| Tests | Critical incident renders fully; empty list renders its intended state; plus the surviving chapter 9 tests. |
| Test migration note | How many chapter 9 tests needed changes, and what that tells you about how they were written. |
| Re-verification note | Keyboard walk on both routes and an accessibility-representation check of the list. |
| Screenshot set | List, detail, empty, and one error state. |
| Framework decision record | Client-rendered versus server-rendered, decided against customer deployment constraints, with the conditions that would reverse it. |

## Rubric

Every **Required** row at "meets". At least three **Distinguishing** rows at "meets" to pass.

| # | Criterion | Weight | Fails | Meets | Exceeds |
| --- | --- | --- | --- | --- | --- |
| 1 | Routing as state | Required | Detail view only reachable by clicking | Direct reload and new tab both work | A shared link opens the exact incident with no extra steps |
| 2 | State placement | Required | Everything lifted to the top, or a global store introduced | Each piece justified in the four-category table | A piece deliberately kept local that a naive design would have lifted |
| 3 | Accessibility survival | Required | Any chapter 7 property lost | Full keyboard walk passes on both routes | Route change focus and announcement verified in the accessibility representation |
| 4 | Request model survival | Required | Five-state model collapsed into booleans, or double submission possible | Both intact after the rewrite | Guard proven by a test that would fail without it |
| 5 | Deliberate empty and error states | Required | Blank regions, or a spinner where empty should be | Loading, populated, empty, failed, and not-found all distinct | Empty state performs first-day onboarding |
| 6 | Error boundary | Required | A row-level error blanks the application | Boundary contains it with a usable fallback | Fallback offers a recovery action and reports enough to diagnose |
| 7 | Component boundaries | Distinguishing | One large page component doing everything | Small components with one responsibility each | A field wrapper that makes label, description, and error association impossible to forget |
| 8 | Server authority | Distinguishing | Returned priority copied into local state or recomputed | Displayed value comes from the service | No derived server value stored anywhere |
| 9 | Hostile data | Distinguishing | Flattering seed data only | All four hostile cases present and handled | Documented what broke first and what you changed |
| 10 | Test durability | Distinguishing | Most chapter 9 tests rewritten | Most survived unchanged | Migration note draws the right conclusion about query strategy |
| 11 | Effects discipline | Distinguishing | Effects deriving state or copying props | Effects only for genuinely external synchronisation | Development double-invocation causes no misbehaviour |
| 12 | Delivery evidence | Distinguishing | No screenshots or decision record | Both present | Framework decision names the customer constraint that drove it |

## Self-check before you call it done

- Paste your detail location into a fresh browser window. What happens?
- Empty the seed data. Read the screen as a first-day operator. Do you know what to do?
- Delete a row from the middle of the list. Does any state appear in the wrong row?
- Name three pieces of state and, for each, why it is not one level higher.
- Navigate between routes with the keyboard only. Where does focus go, and what is announced?
- Which of your components would a customer's engineer have to modify to add a sixth field, and how many?
- Which of your components is customer-specific, and would a stranger be able to tell?

## Time and depth

Longer than chapters 7 to 9 — this is a rebuild. If it is much longer, you are probably building a component library you do not need yet.

## Stuck hints

Read only after a real attempt. Printed upside down on purpose.

˙pɐǝʇsuᴉ ǝʞɐʇsᴉɯ ʇuǝɯǝɔɐןd ǝʇɐʇs ɐ sǝqᴉɹɔsǝp ǝɔuǝʇuǝs ǝɥʇ ʎןןɐns∩ ˙ʇsɹᴉɟ ǝɔuǝʇuǝs ǝuo uᴉ ɯǝןqoɹd ɔᴉɟᴉɔǝds ǝɥʇ uʍop ǝʇᴉɹʍ 'ʎɹɐɹqᴉן ʇuǝɯǝƃɐuɐɯ ǝʇɐʇs ɐ pɹɐʍoʇ ןןnd ǝɥʇ ןǝǝɟ noʎ ɟI ˙ㄥ
˙ǝɔᴉʍʇ ʇou 'ǝɔuo ʎɐʍ ǝןqɐɹnp ǝɥʇ ɯǝɥʇ ǝʇᴉɹʍǝᴚ ˙sǝɯɐu ǝןqᴉssǝɔɔɐ uɐɥʇ ɹǝɥʇɐɹ ǝɹnʇɔnɹʇs ƃuᴉʎɹǝnb ǝɹǝʍ ʎǝɥʇ 'ǝʞoɹq sʇsǝʇ 6 ɹǝʇdɐɥɔ ɹnoʎ ɟo ʇsoɯ ɟI ˙9
˙ʇsoן noʎ suoᴉʇɐᴉɔossɐ ǝɥʇ ɟo ןןɐ suʍo ʎןןɐnsn ʇuǝuodɯoɔ ǝuO ˙ɹǝddɐɹʍ pןǝᴉɟ ǝɥʇ ʇɐ ʇsɹᴉɟ ʞooן 'pǝssǝɹƃǝɹ ʎʇᴉןᴉqᴉssǝɔɔɐ ɟI ˙ϛ
˙ןɐʌᴉɹɹɐ uo ǝɔuɐʌǝןǝɹ ɹoɟ pǝʞɔǝɥɔ ʇou sᴉ ʇןnsǝɹ sʇᴉ ɹo pǝןןǝɔuɐɔ ʇou sᴉ ɥɔʇǝɟ ɹnoʎ 'ɐʇɐp s,ʇuǝpᴉɔuᴉ snoᴉʌǝɹd ǝɥʇ sʍoɥs uoᴉʇɐƃᴉʌɐu ʇsɐɟ ɐ ɟI ˙ㄣ
˙uoᴉʇɐɔoן ǝɥʇ ɯoɹɟ ʇᴉ ƃuᴉpɐǝɹ ɟo pɐǝʇsuᴉ ʎɹoɯǝɯ uᴉ ʇuǝpᴉɔuᴉ pǝʇɔǝןǝs ǝɥʇ ƃuᴉpןoɥ ǝɹɐ noʎ 'pɐoןǝɹ uo sʞɐǝɹq ǝʇnoɹ ןᴉɐʇǝp ɹnoʎ ɟI ˙Ɛ
˙pǝɯnssɐ noʎ uɐɥʇ ɹǝןןɐɯs sᴉ ʇᴉ uǝʇɟo puɐ 'ɹǝʍsuɐ ǝɥʇ sᴉ ʇǝs ʇɐɥʇ ɟo ɹoʇsǝɔuɐ uoɯɯoɔ ʇsǝɹɐǝu ǝɥ⊥ ˙ʇᴉ spɐǝɹ ʇɐɥʇ ʇuǝuodɯoɔ ʎɹǝʌǝ ǝɯɐu 'sƃuoןǝq ǝʇɐʇs ɟo ǝɔǝᴉd ɐ ǝɹǝɥʍ ǝpᴉɔǝp ʇouuɐɔ noʎ ɟI ˙ᄅ
˙ǝdʎʇ puɐ uoᴉʇᴉsod sʍoןןoɟ ǝʇɐʇS ˙ǝdʎʇ sʇᴉ ɹo ǝǝɹʇ ǝɥʇ uᴉ uoᴉʇᴉsod s,ʇuǝuodɯoɔ ʇɐɥʇ ʇnoqɐ pǝƃuɐɥɔ ʇɐɥʍ ʞsɐ 'oʇ ʇᴉ ʇɔǝdxǝ ʇou pᴉp noʎ uǝɥʍ sʇǝsǝɹ ɯɹoɟ ɐ ɟI ˙Ɩ
