<!-- tts:skip -->
## TTS notes — chapter 1 (Mato Crafts rewrite)

- Voice: `en-US-AndrewNeural`, rate `-14%` (about 146 words per minute).
- Say "F D E" as three letters. The renderer substitutes this.
- "Mato" is Mah-toe. "Subhechha" is Soo-bhek-cha. "Niyalo" is Nee-yah-lo. "Patan Dhoka" is Pah-tahn Doe-kah.
- Do not speak this block. Do not speak the hints in the project guide.
- `[pause]` is a beat of silence at a turn, not mid-sentence.
<!-- /tts:skip -->

Welcome back to FullStack in Audio. This is chapter one again: entering the forward deployed engineering field. [pause]

If you already listened to the first version, set it aside. That version used a logistics company I invented, with depots and a vice president and a security team you have never met. You told me, correctly, that you are not inside an organization like that, and that asking you to invent one would not produce a useful charter. So this chapter has a real customer. One you already shipped for.

Before the scene, the same warning as last time, because the shape of the course did not change. This chapter is a full listen, and at the end there is a project. The project is an exam, not a tutorial. It gives you a goal, constraints, the artifacts you have to produce, and a rubric you grade yourself against. It does not give you steps. There is no finished charter to copy, including from this audio. I will show you how to think. I will not read you the page. If you get stuck, the written guide has hints at the very bottom, one question at a time. Try first. [pause]

## The customer is already yours

The customer is Mato Crafts. Patan. Handmade polymer-clay jewellery, especially earrings. The founder is Subhechha Singh. There is a shop at Patan Dhoka. The pieces are made by hand. You, through Niyalo, already built the store: catalog, custom orders, cart, sold-out states, payments, delivery, inventory, and the site itself. You also ran the Meta ads.

Hold that last pair of facts together, because they are the whole chapter.

The store can take an order. The ads can create more orders. The bench cannot magically absorb them. You already know the consequence, because it happened: the ads were paused when demand got ahead of what the makers could finish.

That pause is not a small marketing footnote. It is a founder choosing not to break promises. It is also growth turned off, on purpose, because the operation could not keep the promise the storefront was making. Dana, in the old version of this chapter, wanted refrigeration alarms to stop sitting in an inbox. Subhechha's version of that sentence is quieter and closer to you. She does not need another website. She has one. She needs the studio to be able to say yes to an order without the bench paying for that yes in missed dates, rushed clay, or ads that have to be switched off.

That is a forward deployed problem. And the awkward part is that you are already the person who built the surface customers buy through. [pause]

## What a forward deployed engineer actually is

A forward deployed engineer is an engineer who builds and delivers working software inside a customer's environment, accountable for the outcome the customer cares about rather than for a component in a backlog.

Three parts. Each one is load-bearing. I am going to say them in general, and then say what they mean at Mato, because the general version is how the role is defined and the Mato version is how you will practice it.

First: an engineer. You write the system. You read the logs. You decide what is stored, who can see it, and what happens when it fails. This is not a strategy role with a technical vocabulary. If you cannot build the thing, you cannot do the job. You already clear this bar. You have shipped stores, inventory, invoices, dashboards. Do not spend this course re-proving that you can make a page. Spend it on the parts a page does not cover.

Second: inside a customer's environment. Not in a clean repository with your favorite stack and your favorite assumptions. The environment is an input. At a large enterprise that means their identity provider, their cloud rules, their change window, their security review. At Mato it means something smaller and, for you, more dangerous, because it is familiar. The shop already has a live store that you built. Payments already exist. Sold-out already exists as a state on the site. Custom orders already exist as a path. The part you did not build is the bench: how a maker's day actually fills up, which designs are slow, which custom request is a polite no, who notices that a product should have been marked unavailable yesterday. That bench is the environment. If your design assumes the website is the business, you have already left the customer's environment and gone back to your own.

Third: accountable for the outcome. A correct feature that nobody uses is a failed delivery. Your unit of success is a change in how the studio works, measured in something the founder already recognizes. "The new screen looks better" is not that. "We stopped accepting orders the bench cannot start" might be. You will choose the measure in the project. I am not choosing it for you.

Now the boundary that makes this role confusing, because a forward deployed engineer sits between other jobs, and at a studio of this size those jobs are sometimes the same human wearing different hats. [pause]

## Who owns what, when the company is small

In a big delivery, four groups are easy to point at.

Product engineering owns the reusable core. They are right to refuse a one-customer fork.

Solutions and sales engineering own the promise made before you arrived. They demonstrated a future. You inherit it.

The platform team owns the substrate: accounts, networks, deploys, cost, on-call.

The customer's own people own the work. Operators do it. Administrators hold permissions. A security reviewer can veto. A sponsor holds the budget.

A forward deployed engineer produces the thing none of those four produce alone: one specific system, in that environment, for that outcome, that still runs after you leave.

After you leave. Say that again when you are tempted to be the permanent operator of Mato's queue. A desk that only works while you are in the Instagram thread, or while you are the one marking things sold out by hand, is not a deployment. It is you, rented as a feature.

At Mato, draw the same four groups honestly, even where the org chart is one room.

Product, for you, is Niyalo's ability to ship a store again for the next brand. You have done this shape of work more than once. ReFashion was orders moving off Instagram DMs onto a store with inventory. Mato is handmade jewellery with custom orders and a bench behind the catalog. If every Mato exception is hardcoded into a Mato-only pile, the next studio starts from zero and this one becomes unmaintainable. The reusable part and the Mato-only part have to be distinguishable. You will not draw that split in this chapter. You will refuse to pretend it does not matter.

Solutions, for you, is the proposal you already kept. The store shipped. Payments work. Ads ran. The dangerous misread is that "we built the store" was heard as "the studio can now accept whatever demand the ads create." Those are different sentences. A forward deployed engineer writes down which sentence was actually promised.

Platform, for you, is not a four-person team named Marcus. It is the accounts this shop already depends on: the store, the payment provider, the ad account, wherever product photos live. Some of those you administer. That is a risk, not a convenience. If the only person who can deploy, refund, or explain a sold-out flag is you, you are the platform team, and you are also the single point of failure. Write that down. Do not invent a platform department to make the charter look enterprise.

The customer is Subhechha, and the people who make the pieces, and whoever actually reads a new order on a given afternoon. Those might be the same person at different hours. A founder who sells in the shop, answers a custom request, and also makes jewellery is three stakeholders in one body. Your charter has to show the conflict inside that, not average it into "the client wants growth."

And the system you have not built yet, which this course will call Promise Desk, is a fifth party. It gets a row. It is not a feature. It is a participant with permissions and a prohibition.

What the role is not, still, because the title attracts the wrong story.

It is not a demo. You can make a model say "this order looks urgent" in an afternoon. The hard part is the promise, the stock, the maker's hours, and the person who is blamed when a customer in Kathmandu, or abroad, is told a date the clay cannot meet.

It is not a slide deck of recommendations. You are measured on a running change in the studio, not on a document that describes one. This chapter's document is the exception. It exists so the running system later has a boundary. It is not the delivery.

It is not a hero rewrite. You already have a store. Throwing it away to build a romantic new platform is how a small studio gets a second system and zero capacity.

It is not unpaid product management. You will do discovery because you cannot build the right limit without it. You will not substitute discovery for the system. Chapter one is the charter. The system starts after the charter exists. [pause]

## Coming from the work you already do

Most people enter this role from somewhere else. I am going to spend the time on your somewhere, and then name the others briefly so you can recognize them when a teammate, or a future you, shows up with a different bias.

You come from agency delivery and product engineering. Niyalo designs, brands, and ships. Sites, stores, inventory, invoices. Youanai is a product company where you own a large share of the engineering. That combination is rare and it is also the trap. You are used to a brief, a build, a launch, and a handoff of the website. The customer is happy when the site is live. Forward deployed work is happy when a number in the operation moves, and stays moved after the launch week.

So the transition, for you specifically, is this. Stop treating "the store is in production" as the end of the engagement. The store is the environment you landed in. The outcome is upstream of the store: what the bench can promise this week. Your old success habit is shipping the interface the proposal named. The new habit is noticing when that interface is making a promise the workshop cannot keep, and treating that as your problem even though nobody wrote it in the original scope.

If the scope is wrong, staying neatly inside the scope is a failure. That sentence is the whole career change. It will feel rude the first time you use it, because good agency work is partly the discipline of not rebuilding the client's entire company. You still need that discipline. The charter is how you aim it. You widen the problem on purpose, then you narrow the first release on purpose. Widen without narrowing and you have volunteered to run their operations. Narrow without widening and you have shipped another screen.

Other starting points, quickly, so the definition is not only autobiographical.

From backend work, people bring services and failure handling, and they usually wait too long for a product manager to resolve a fuzzy requirement. In the field, waiting is a decision.

From frontend work, people bring the rare instinct for whether a human can use the thing under pressure. They usually need the operational layer: durability, identity, deploy.

From data work, people see the stale table first. They usually need the path a human is waiting on.

From machine learning work, people know what a model cannot do. They usually need the boring release discipline that makes a model safe to trust.

From consulting, people can run a room. They need the credibility of having built the thing.

Your version of the missing piece is not syntax. You will get syntax later, in the chapters where you write the system, and those chapters will slow down and show the shape of a file, not only the idea. Not this chapter. This chapter is the aim. [pause]

## What the first two weeks look like when you already built the site

Here is the picture, and I want you to notice how little of it is a new framework.

You start by watching the making, not by interviewing the founder about the making. You already know how she talks about the brand. You do not yet know, unless you have stood there, what a Tuesday afternoon does to a custom request. Sit where the pieces are made, or where orders are accepted, and be quiet. You are looking for the second list. Every operation has an official path and a list that actually runs the day. At a studio this might be a notebook, a notes app, a stack of half-finished pairs, a message thread, a mental count of "we can do three of the hard ones." Nobody puts that list in the proposal. It is the system of record whether you like it or not.

Then you find the boundaries of the environment you think you already know. Where does a new order land, in practice, not in the sitemap? Who is allowed to mark something sold out, and how late do they notice? What leaves the shop when a customer pays: name, phone, address, a note about a custom design? Which of those would be unacceptable to paste into a model? You built the store, so you will be tempted to answer from memory of the schema. Memory of the schema is not the same as watching the afternoon. Label the difference. Observed means you saw it or you have a record from the delivery you can point at. Assumed means you are guessing, including educated guesses from having built the checkout.

Then you find the approval path. At Mato this is not a monthly governance board you have never heard of. It might still surprise you. Who can turn ads back on? Who can promise a date to a custom client? Who can refuse a design the studio does not want to make? Who can decide that your software is allowed to read order notes? A stakeholder has a wish. An approver can stop the work. Subhechha can stop the work. A maker who will not trust the queue can also stop it, by simply not using it, which is a veto with no meeting.

Only then do you write the charter. It should feel like notes from what you learned, compressed to a page. If it feels like a pitch, you started too early.

Somewhere in those two weeks you also produce one small piece of evidence, not the system. A count. How many orders arrived in a week you can actually reconstruct. How many were custom. How many were later delayed, remade, or refused. Even a rough count from a notebook is more useful than a mood. It does two things. It gives the outcome measure a baseline, and it stops you from designing for a volume you invented.

What is absent, still: picking a framework, drawing a schema, calling a model. Those are later chapters. Strong engineers start there because building is comfortable. What they build is often correct and beside the point. You are especially exposed to this, because you can build a store in your sleep. Do not build a second one. [pause]

## How a missing boundary actually breaks

Let me make the failure concrete, because "write down responsibilities" sounds like paperwork until you watch the meeting it prevents.

The store is live. A product can be ordered. Ads have, in the past, created more demand than the bench could finish, and the ads were paused. Imagine the next version of that mistake, because the paused ads are the symptom you already lived. The symptom is not yet the charter's costly failure. You have to decide what the failure underneath was. I will show you the shape. You will name it.

A customer orders a pair, or asks for a custom one. Someone says yes. The yes might be the checkout itself, which is a yes the website gives without asking the bench. Or the yes might be a human reply. The maker is already full. The date slips. The founder now has an angry customer, a half-made piece, and a reason to fear the next ad. So demand gets turned off. Revenue the studio wanted does not arrive. The website is "working." The outcome is not.

Whose failure is that, if nobody wrote it down?

If you never wrote it down, here is the argument. The founder believes the store was supposed to grow the studio, so the store failed. The maker believes they were buried by promises they did not make. You believe you shipped what was scoped: catalog, payment, delivery, inventory. Everyone is partly right, which means the engagement has no owner for the only sentence that matters: who is allowed to promise a date.

That is a boundary failure. It was available to prevent before any new code. An undocumented assumption is a liability with a delayed trigger. Yours, if you leave it unwritten, is this one: a live checkout is the same thing as a promise the bench can keep. It costs nothing on launch day. It costs the ads, later.

There is a second cost, and it is yours. Forward deployed engineers burn out from unbounded responsibility. If the charter says you are accountable for the brand, the clay, the ads, the refunds, and the code, you have accepted a job the founder did not give you and cannot pay you to finish. The page protects the studio and it protects you. Deciding and doing stay separate. You may build the desk. You do not get to decide which custom design the studio is willing to make. [pause]

## How to write this charter

The project is a one-page delivery charter for the first release of Promise Desk, for Mato Crafts. One page, because if it does not fit, you have not decided. Four readers have to recognize themselves: the founder, a maker, you as the engineer, and a future person who has to trust the limit when a recommendation is wrong. At this studio the fourth person might also be the founder. Write it so a skeptical friend can still find that concern on the page.

I am going to walk the parts. I will give you the standard for each part. I will not give you the finished paragraphs.

### The problem, before the solution

Write the current workflow as it actually happens, ugly parts included. You know some of it from the delivery. The studio sells handmade pieces through a live store. The store has a catalog, custom orders, a cart, payments, delivery, and a way to show that something is sold out. Makers produce the pieces by hand. Ads were paused because demand outran manufacturing.

You do not know, unless you have watched it, the exact afternoon path. Do not smooth that into a story about email inboxes borrowed from a logistics company. Write "unknown" where it is unknown. A charter that invents a warehouse process you have not seen is worse than a short one.

Then separate the symptom from the costly failure. "Ads were paused" is observed. It is a symptom. The costly failure is the thing that made pausing them rational. Candidates, and these are candidates, not your answer: a promised date the bench could not meet; a custom request accepted with no idea how long it takes; a product left orderable after the maker was already full; overtime and broken pieces from saying yes too often. Pick the one the founder would recognize as the reason, label it assumed if you did not see it, and demote the rest to friction. A charter that tries to fix ads, branding, and international expansion in release one has not chosen.

Every factual claim gets a label. Observed or assumed. "You shipped payments, delivery, and inventory" can be observed, because you did that work. "The bench can finish twenty pairs a day" is assumed unless someone showed you a count. Unlabelled claims are failures, not style issues. This is how you keep a public story about a real studio from drifting into fiction. If a number is not yours to publish, do not put it on the page. The charter can be specific without being a financial disclosure.

### The users, in the plural

There is no "the user."

Subhechha wants the studio to grow, and she has already shown she will turn demand off rather than break the work. She needs a way to say yes again without that fear. She can veto anything.

A maker wants a day that can be finished. A new tool that adds a form and removes nothing will be ignored. Ignoring it is a successful veto.

A customer wants a date they can trust, and a custom piece that matches what they asked for. They are not in the room. They still constrain the release. A faster checkout that lies about timing is a worse store.

You want a system you can leave behind. You also want a reusable core, because the next studio should not require a fork of Mato's exceptions.

Write the conflict. The founder can want ads back on in the same week a maker wants the queue frozen. The charter does not resolve that by cheerfulness. It states it, and the first release picks a side for now, with a reason.

### One outcome

One measure. The test: could the studio compute it this month, from something that already exists or could be counted by hand, and would the founder recognize it as the thing that matters?

Good shapes, still not your sentence: the share of accepted orders that meet the date someone actually promised; the number of orders accepted in a week that the bench cannot start; the time from a custom request to a human yes or no. Bad shapes: "improve efficiency," "grow the brand," "model accuracy." Accuracy is a trap here. There is no labelled ground truth for which handmade order "should" have been accepted. Two makers might disagree. You would spend the pilot scoring the model instead of protecting the promise. Measure the workflow. Leave model quality for the evaluation chapter, later.

If today's number is unknown, write that, and make establishing it task one. Do not invent a baseline to look rigorous.

### The release boundary

Three lists. What the first release does. What it does not do. What still requires a human.

The third list saves you. A honest direction, which you may reject if your problem statement demands it: Promise Desk may show that the bench is full, and may suggest whether a new order can be promised. A human accepts, changes, or refuses the promise before the customer is told. No automatic yes. No automatic refund. No automatic ad spend.

Non-goals are mandatory, and each one needs a reason from risk, evidence, or sequence. Not from what you feel like building. Likely non-goals, for you to accept or replace: replacing the current store; turning ads back on; designing new products; shipping abroad; letting a model reply to a customer. Someone will ask for each of these. A written non-goal turns the argument into a reference.

A non-goal is a schedule with a reason. It is not an insult to the founder.

### The responsibility matrix

Rows for: the founder, a maker, you, whoever administers the store and the ads if that is not already you, and Promise Desk itself.

For each row: what they decide, what they do, and where they escalate.

The system's row must contain a prohibition, not only a capability. Finish this thought in your own words: it may suggest a promise, and a person must confirm it before a customer is told. If you cannot write the prohibition, you are not ready to build.

Separate deciding from doing. The founder may decide that a design is in bounds. A maker does the making. You may build the check. You do not decide the brand's taste. Do not give yourself the business risk. It is flattering and it is how you end up accountable for a late pair you had no authority to refuse.

### The risks, with evidence

Three is enough. Each risk needs the evidence that would retire it.

I will give you the shape of one, so you can hear the difference between anxiety and a research task. Risk: makers will not trust the suggestion and will route around it with the notebook they already use. Evidence that retires it: in a week you actually watch, they accept or amend the suggestion on real orders, rather than ignoring it.

Your other two should come from this studio, not from a generic software list. Personal data in an order note. A checkout that still says yes while the desk says no. You being the only person who can change the system. Pick risks that, if they came true, would recreate the costly failure. A risk that would apply to any website is not a risk for this charter. [pause]

## What done sounds like, without handing you the page

A finished charter opens on the studio as it is. Handmade pieces, a live store you already shipped, a bench with a finite day, ads paused when orders outran making. Claims labelled. Unknowns left unknown.

It names one costly failure, not five, and it does not pretend the failure is "we need a better brand."

It names the conflict between growth and a finishable day.

It has one measure, and it admits if today's value is not on record.

It has three lists: does, does not, still needs a human.

It has a matrix whose system row can refuse. It has three risks with finish lines.

A founder can explain the first release in two minutes without saying a framework, a model, or a vendor. A maker can see they are not being automated out of the promise. You can see what you are not allowed to decide.

If your page is a transcript of this chapter, it fails. The reasoning is here. The sentences have to be yours, because you are the one who will have to defend them when the first awkward order arrives. [pause]

## How this goes wrong

The solution-shaped charter. The page describes a bot, a database, a dashboard. Delete every implementation noun. If the problem disappears with them, start again from the bench.

The everything charter. Ads, a new store, custom design tools, international shipping, a full factory planner. Ambition here is a narrow release that lands. The pause already taught you what happens when the surface gets ahead of the hands.

The unfalsifiable outcome. Satisfaction, "vibes," a usage count. If the number cannot go down, it cannot be trusted when it goes up.

The invisible human. The page implies the desk tells the customer yes. That is the failure mode you are here to make impossible.

The stakeholder you flattened. You wrote "the client" and never separated the founder who wants demand from the maker who has to meet it. Week three, the tool is unused, and you are surprised.

The model-shaped charter. Delete every sentence about intelligence and automation. If no problem remains, you brought a technology looking for a studio.

And one that is specific to you. The agency charter. It describes a successful relaunch of the website. That is the job you have already done. This course starts where that job stopped. [pause]

## How you check the page

The two-minute test. Explain the first release out loud as if to Subhechha. No service, no model, no stack. If you cannot, the charter is a build plan.

The disagreement test. Find two wants that do not fit. If you cannot, you wrote a brochure.

The veto test. Who can stop this? The founder, yes. Who else, including a maker who simply does not use it? Each of them needs a path to yes.

The measurement test. How would you compute today's value with what the studio already has, even if that is a notebook? If the answer is "we cannot yet," that sentence belongs on the page.

The prohibition test. Read the system's row. It needs a clear "may not."

The quiet test. Hand the page to someone who did not hear this chapter. Ask what the first release does, and who is accountable when a customer is told a date the bench cannot meet. Stay silent while they read. Whatever they miss is the document.

The fiction test, because this customer is real. Read every sentence and mark it observed or assumed. If a sentence would embarrass you when read back to the founder because you guessed their internals, it is assumed, or it comes off the page. Do not publish their finances. You do not need a revenue figure to name the operational problem. [pause]

## Your project

The written guide has the situation brief, the constraints, and the rubric. The brief is the input. You do not invent a company, and you do not switch customers. Mato Crafts is the customer for this course unless we deliberately change it later.

You will write three artifacts: a one-page charter, a responsibility matrix that includes Promise Desk and everyone who can block a decision, and a risk register where each risk has the evidence that would retire it. Put them in the chapter one folder of the field workspace. They are yours to commit when you want them in this repo. Do not commit customer personal data, payment details, or ad-account access.

Constraints, so you hear them before you open the guide. One page. No implementation detail. Every claim labelled. Non-goals required. One measure the studio could actually compute. The system gets a prohibition. You do not grade yourself generously.

There is no code in this chapter. There is no starter file with the answer hiding in it. The empty page is the starting state. That is still how the work begins. The difference from last time is that the studio is specified, so your effort goes into judgment, not into world-building. [pause]

## What you carry forward

A forward deployed engineer is accountable for an outcome inside the customer's environment, and the environment is an input. Yours, this time, is a handmade studio whose store you already shipped.

The role sits between a reusable core, the promise already made, the accounts the shop runs on, and the people who make and sell the work. At Mato those are not four departments. They are still four kinds of responsibility, and blurring them is how a checkout becomes a lie.

Coming from agency delivery, your specific shift is from "the site launched" to "the bench can keep the promise the site makes." Noticing a wrong scope is part of the job.

An unwritten assumption waits until it is expensive. Yours to kill on paper, today, is that a working store is the same thing as a keepable promise.

The charter is one page, four readers, one failure, one measure, three lists, a matrix with a prohibition, three risks with evidence.

Chapter two, when we retarget it, will take this charter as its input. You will implement one small promise rule, the same rule, in more than one language, and defend which runtime a studio like this would actually run. The audio that is in the repo tonight for chapter two is still the old logistics episode. Do not do that project against the old company. Finish this charter. We will rebuild chapter two on top of it.

That is chapter one. Go write the page.
