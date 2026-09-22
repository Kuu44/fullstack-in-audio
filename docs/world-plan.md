# World plan

Notes for retargeting the course after chapter 1. Not a lesson. Do not treat chapters 2–38 as updated until their audio and guides say Mato Crafts.

## Decision

The course customer is **Mato Crafts** (Patan Dhoka, Lalitpur). Handmade polymer-clay jewellery. Founder Subhechha Singh. Niyalo already shipped the store: catalog, custom orders, cart, sold-out, payments, delivery, inventory, and Meta ads. The ads were paused when demand outran making.

The accumulating system is **Promise Desk**. Release one only protects a promise the bench can keep. The existing store stays.

Harborline Logistics and FieldOps Copilot are archived. Chapter 1 audio and text from that draft live in [`archive/harborline/`](../archive/harborline/).

## Why not a telecom

"Enso" was considered as a Nepal telecom scenario. There is no Nepal telecom by that name worth building a course on. A fictional operator would repeat the Harborline problem: Kushal is not inside that organization and would be inventing the work. Mato is a customer he has already delivered for, so the charter tests judgment instead of world-building.

Ncell or Nepal Telecom can be a later contrast, not the spine. The spine is a studio whose checkout can say yes faster than the hands can make the piece.

## Facts we will not invent

Allowed on the page when labelled observed:

- Handmade polymer-clay jewellery, earrings as the core, Patan Dhoka shop, founder Subhechha Singh.
- Store capabilities Kushal shipped, and the ads pause because making could not keep up.

Not allowed unless a new source is written down:

- Revenue, profit, ROI multiples, headcount, ad spend.
- A separate warehouse, a daily pair-count, or an inbox workflow nobody has watched.
- Private order data of any kind.

Third-party social posts about the studio are not sources for this repo.

## What Kushal asked to change later

Chapters that teach code should include a real syntax and file-structure crash course: what the file is, what each part does, how it is run, how it fails. The exam shape stays. Hints stay at the bottom of the guide and out of the audio. He still writes the project. The audio stops assuming he already knows the dialect of the day.

Chapter 1 does not do that. It is a charter, not a language chapter.

Each project should be something he can commit. Chapter 1's place is `fieldops/01-charter/`.

## Chapter 2 is blocked on the charter

Do not sit the current chapter 2 project. Its audio still uses the logistics company and a triage-priority rule. After the charter exists, chapter 2 should be rebuilt as one promise rule taken from that charter, implemented in more than one runtime, with a written choice of which runtime this studio would actually run.

## Later retarget, not done

Same skills, new subject. Rough map from the old FieldOps exercises onto Promise Desk:

| Old beat | Promise Desk beat |
| --- | --- |
| Incident intake | An order or custom request arriving |
| Priority rule | Can the bench promise this, by when |
| Intake CLI | Record one request and get a yes, no, or needs-a-human |
| Operator UI | A maker or founder confirms the promise |
| API as authority | The site must not be the only thing allowed to say yes |
| Audit log | Who promised the date |
| AI suggestion | Suggest only. A human sends the answer |
| Eval | Did we recreate the "checkout says yes, bench is full" failure |
| Handoff | The studio can run the desk without Kushal in the thread |

Rewrite a chapter only when its lesson, guide, and audio all move together. Until then the old files stay, and the README says so.
