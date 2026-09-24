# Chapter 1 project — Charter Promise Desk for Mato Crafts

**Format:** open-book test. The thinking was in the chapter audio. There are no build steps here.
**Prerequisite:** listen to chapter 1 first. Do not start from this page.
**Customer:** Mato Crafts. Do not invent a replacement company.

---

## Goal

Write a one-page delivery charter for the first release of Promise Desk that Subhechha, a maker, you, and a skeptical reader can all use to answer the same three questions: what problem the first release exists to change, who decides, and how you will know it worked.

## Starting state

No code. No architecture. An empty page in [`fieldops/01-charter/`](../../fieldops/01-charter/README.md).

The situation brief below is the input. It is not the charter. Copying it into a document titled "charter" fails the test.

### Situation brief

Use these claims. Do not upgrade an assumed claim into an observed one. Do not add a financial figure.

**Observed**

- Mato Crafts is a handmade polymer-clay jewellery studio. Earrings are the core product. Founder: Subhechha Singh. Shop at Patan Dhoka, Lalitpur.
- Pieces are made by hand. You have described makers at the bench. You have not, in this course, documented a separate factory.
- Through Niyalo you shipped the live store: catalog, categories, custom orders, cart, sold-out states, payments, delivery, and inventory. You also ran Meta ads for the brand.
- The ads were later paused because demand got ahead of what the makers could finish. That pause is observed. The precise afternoon failure underneath it is not fully written down yet.

**Unknown — leave these unknown or go look. Do not invent them.**

- Whether making happens only at the Patan shop, in another work room, or both.
- Who reads a new order on a given day, and in what order (checkout, custom-request form, in-person, anything else).
- How many orders a week the bench can start. Any daily capacity number you write without a count is assumed.
- What today's promise-keeping rate is. Nothing in this brief is a baseline.
- Revenue, profit, headcount, and ad spend. They are not inputs to this charter.

**Already decided for the course**

- The system under charter is Promise Desk. Release one is about promises the bench can keep. It is not a new store.
- The store you already shipped stays. Replacing it is out of scope unless your charter explains why that would be reckless, as a non-goal.
- The next piece of work, when it exists, starts from this charter.

## Constraints

1. **One page** for the charter itself. The matrix and the risk register may sit on a second sheet. If the charter does not fit, you have not decided.
2. **No implementation detail.** No frameworks, vendors, models, databases, or "we will use AI." Not one.
3. **Every claim is labelled** observed or assumed. Unknown stays unknown.
4. **Exactly one measurable outcome.** The studio could compute it this month by hand if needed. The founder would recognize it. It is not a model-accuracy number, a satisfaction score, or a revenue target.
5. **Non-goals are mandatory,** each with a reason from risk, evidence, or sequence.
6. **Promise Desk has a row and a prohibition.** It may suggest. It may not tell a customer yes.
7. **Deciding and doing are separated.** You do not take the brand's taste, the maker's hours, or the founder's risk as your decision.
8. **Not a transcript.** If the page can be produced by rearranging this chapter's audio, rewrite it in your own sentences.
9. **Nothing private in the repo.** No customer names from real orders, phones, addresses, payment data, or ad-account access.

## Required artifacts

Write these yourself. Paths:

| Artifact | File | What it must contain |
| --- | --- | --- |
| Delivery charter | `fieldops/01-charter/charter.md` | The workflow as it is, including what you do not know; the costly failure, distinct from "ads were paused"; the people and the conflict; one outcome; three lists — does, does not, still requires a human |
| Responsibility matrix | `fieldops/01-charter/responsibility.md` | Founder, maker, you, whoever can stop a deploy or an ad change, and Promise Desk. For each: decides, does, escalates to |
| Risk register | `fieldops/01-charter/risks.md` | At least three risks. Each names the evidence that would retire it. At least one risk is about the checkout still saying yes while the bench is full |

## Self-grade rubric

Score each line. You are the only reviewer.

**Pass bar — all six must be true**

1. **Two-minute test.** You can explain the first release without an implementation word.
2. **Conflict is on the page.** Growth and a finishable making day are both present, and the release picks a side for now.
3. **The outcome is falsifiable.** You can say how today's value would be counted, even if the answer is "not recorded yet."
4. **The system row prohibits an unapproved yes** to a customer.
5. **You did not become the founder.** Taste, capacity, and commercial risk have a human owner who is not "the software."
6. **Labels survive a read-back.** A sentence the founder could contradict from the shop floor is marked assumed, or it is gone.

**Quality marks — aim for at least four**

7. "Ads were paused" is treated as a symptom, and the costly failure is a more specific operational event.
8. At least one unknown from the brief is still unknown, with the observation that would settle it.
9. A maker's refusal to use the tool is treated as a real veto.
10. Each risk's evidence could be gathered in the studio this month.
11. Deciding and doing are split in your row and in the founder's row.
12. Delete every sentence about software. A problem worth solving remains.

**Automatic fail**

- The customer is anyone other than Mato Crafts.
- The charter's subject is a new website.
- The headline outcome is revenue, ad ROI, or model accuracy.
- A capacity number, a headcount, or a revenue figure appears with no source you can point to.
- The page tells Promise Desk it may confirm an order on its own.

## Stretch

Pick one only after the pass bar is true.

- Write the two sentences Subhechha would say to a maker about why the queue is changing. Check that those sentences promise nothing your charter does not.
- Name the one claim you most need to verify by standing in the shop, and the question you would ask without pitching software.
- Cross out the non-goal you most want to build. If that was painful, the non-goal section is doing its job.

## Verification you can run today

- Read the charter aloud once, standing up. Any sentence you cannot say to the founder comes out or gets an assumed label.
- Ask someone who has not heard the audio what the first release refuses to do. If they cannot answer, the boundary is still in your head.

---

<!-- tts:skip -->
## If stuck — inverted hints

Last on purpose. Not in the audio. Read one at a time, only after a real attempt. Each item is a question.

1. Cannot start? Write one paragraph that begins "The store already works, and the studio still had to pause ads because..." Stop before you propose software.
2. The page is a build plan? Delete every noun a vendor would sell you. Read what remains out loud.
3. Two outcomes, cannot pick? Which number gets worse in the week a customer is promised a pair nobody can start?
4. No baseline? Where, in the shop, would the raw marks already exist: a notebook, the order list, a stack of unfinished pieces? Who would hand them to you?
5. Matrix feels like a form? For each row, what stops if that person is away for a week? If nothing stops, the row is fake.
6. System row is mush? Complete this and then make it stricter: "The desk may say the bench looks full. A person must still ______ before a customer hears ______."
7. No conflict? What would a maker remove from release one, and what would the founder add back the same day?
8. Looking for a security department? Ask instead who is harmed if an order note, a phone number, or a custom design is pasted into a tool you do not control. That person has the veto.
9. Risks are generic? Reread your costly-failure paragraph. What would have to be true for that same failure to happen after Promise Desk ships?
10. Non-goals are easy? List the three things you would enjoy building this month. They are probably not release one.
<!-- /tts:skip -->
