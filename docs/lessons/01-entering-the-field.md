<!-- tts:skip -->
## TTS notes — chapter 1

- Voice: `en-US-AndrewNeural`, rate `-14%`.
- "F D E" is three letters. "Mato" is Mah-toe. "Subhechha" is Soo-bhek-cha. "Niyalo" is Nee-yah-lo. "Patan Dhoka" is Pah-tahn Doe-kah.
- Nothing in this block is spoken. The project guide's hints are not spoken.
- `[pause]` is a beat of silence between ideas.
<!-- /tts:skip -->

This is FullStack in Audio. Chapter one. Entering the forward deployed engineering field. [pause]

You are listening while you move, so here is the shape of the hour before any story. Six parts. First, the studio this course is about, which is a studio you already know. Second, what a forward deployed engineer is, said in plain language and then pinned to that studio. Third, who gets to decide what, when the company is small enough to fit in one room. Fourth, the shift this asks of you, specifically, because you already ship websites for a living. Fifth, one failure, told as a scene, so the paperwork has a reason. Sixth, how to write a one-page charter, and how you will know the page is finished.

By the end you should be able to explain the first release of a system called Promise Desk without naming a tool, and you should be able to sit down and write that page yourself. The audio teaches the judgment. It does not read you the finished page. The written guide, which you open after this, is the test. Hints live at the bottom of that guide. Leave them alone until you have tried. [pause]

## The studio

Part one. The studio. [pause]

Mato Crafts makes jewellery by hand in Patan. Polymer clay. Earrings, mostly. The founder is Subhechha Singh. There is a shop at Patan Dhoka. Someone shapes the clay, bakes it, and finishes a pair. That day has a size. It does not stretch because a webpage is confident.

You already built the store, through Niyalo. Catalog. Categories. Custom orders. A cart. A way to mark something sold out. Payments. Delivery. Inventory. And you ran the ads.

Hold the store and the ads together, because they are the reason this chapter exists.

The store can accept an order at any hour. The ads can bring more orders. The bench cannot absorb an infinite Tuesday. You have already seen what happens when those three disagree. The ads were paused, because demand got ahead of what the makers could finish.

Say that back, while you are still moving. The ads were paused. That is observed. It is also not yet the problem. It is the symptom. A founder turned demand off on purpose, rather than let the studio promise a pair the hands could not make. Growth stopped in order to protect the work. Subhechha does not need another website. She has one. She needs a way to say yes that does not end with the ads switched off, a customer waiting, or a maker staying late to rescue a date the checkout invented.

That is the job of Promise Desk. Not a second store. A limit on the promise. [pause]

Before the definition, one question. If you had to tell a friend why the ads were paused, in a single sentence that does not mention software, what would you say? Keep your answer. You will need a sharper version of it on the page. [pause]

## What the role actually is

Part two. The role. [pause]

A forward deployed engineer is an engineer who builds and delivers working software inside a customer's environment, and is accountable for the outcome the customer cares about, rather than for a piece of a backlog.

Three parts. Each one carries weight. I will say the general version, then the version that applies to you at this shop.

First, an engineer. You write the system. You read what it did. You decide what is stored, who can see an order, and what happens when a payment succeeds and the bench is already full. This is not a strategy title with technical words glued on. If you cannot build it, you cannot do the job. You already clear this bar. You have shipped stores, inventory, invoices, dashboards. Do not use this course to prove you can make a page. Use it for the part a page does not cover: the promise behind the page.

Second, inside a customer's environment. The environment is an input, not a nuisance. In a large company that means their login system, their cloud rules, their change window, their security review. At Mato the environment is smaller, and for you it is more dangerous, because it feels like yours. You built the store. Payments exist. Sold out exists. Custom orders exist. What you did not build is the bench. Which designs are slow. Which custom request is a polite no. Who notices, and how late, that a product should have been marked unavailable yesterday. If your design assumes the website is the business, you have left the customer's environment and gone back to your own.

Third, accountable for the outcome. A correct feature that nobody uses is a failed delivery. Your unit of success is a change in how the studio works, measured by something the founder already recognizes. A prettier screen is not that. Fewer accepted orders that the bench cannot start might be. You will choose the measure. I will not choose it for you.

There is a last clause that people skip. The system has to keep working after you leave. A queue that only functions while you are the person marking things sold out, or while you are in the message thread, is not a deployment. It is you, rented as a feature. [pause]

What the role is not, because the title attracts the wrong picture.

It is not a demo. You can make a model say "this order looks urgent" in an afternoon. The hard part is the date, the clay, and the person who is blamed when a customer is told the pair will be ready.

It is not a slide of recommendations. You are measured on a running change in the studio. This chapter's document is the exception. It exists so the running system has a boundary. The document is not the delivery.

It is not a rewrite of the store you already shipped. Throwing that away to build a grand new platform gives a small studio two systems and zero extra hours.

And it is not unpaid management of their whole brand. You will ask questions because you cannot set the right limit without them. You will not substitute questions for the system. This chapter is the charter. The system comes after the charter exists. [pause]

Question, before we move. In one sentence: what are you accountable for at Mato that a finished website does not already prove? [pause]

## Who decides, in one room

Part three. Who decides. [pause]

In a big delivery, four kinds of responsibility are easy to point at, because they wear different badges.

Product work owns the reusable core. The thing you could ship again for another studio, without forking the whole project for one customer's exceptions.

The promise made before the build owns the expectation. Someone, often you, already told the founder what the store would do. You inherit that sentence.

The platform owns the accounts the shop already depends on. The store, the payments, the ad account, the place the photos live. Whoever can change those is the platform, even if that person is you on a Sunday.

The customer's own people own the work. They make the pieces. They sell them. They can refuse a tool by simply not using it.

A forward deployed engineer produces the thing none of those four produce alone. One specific system, in that shop, for that outcome, that still runs when you are not in the room.

At Mato, draw those four honestly. Do not invent a department so the page looks like a big company.

Product, for you, is Niyalo's ability to ship a store again. You have done this shape of work more than once. If every Mato exception is hardcoded into a Mato-only pile, the next studio starts from zero, and this one becomes something only you can touch. You will not draw that split in this chapter. You will refuse to pretend it does not matter.

The promise already made is the store itself. It shipped. Payments work. Ads ran. The dangerous misreading is that "we built the store" was heard as "the studio can now accept whatever demand arrives." Those are different sentences. Write down which one was actually promised.

Platform, here, is not a team with a name. It is the accounts. Some of them you administer. That is a risk, not a convenience. If the only person who can explain a sold-out flag, or deploy a change, is you, then you are the platform, and you are also the single point of failure. Put that on the page.

The customer is Subhechha, and the people who make the pieces, and whoever actually reads a new order on a given afternoon. Those might be the same person at different hours. A founder who sells in the shop, answers a custom request, and also makes jewellery is three stakeholders in one body. Your charter has to show the conflict inside that. It must not average it into "the client wants growth."

And Promise Desk is a fifth party. It gets a row. It is not a feature. It is a participant with a permission and a prohibition. [pause]

Question. Who, in this shop, can stop the work without calling a meeting? Name at least two. One of them is the founder. The other might be a maker who ignores the tool. [pause]

## The shift this asks of you

Part four. Your shift. [pause]

You come from studio delivery and product engineering. Niyalo designs, brands, and ships. Sites, stores, inventory, invoices. Youanai is a product where you own a large share of the engineering. That combination is rare, and it is also the trap. You are used to a brief, a build, a launch, and a handoff of the website. The customer is happy when the site is live. This kind of work is happy when a number in the operation moves, and stays moved after launch week.

So the change, for you, is specific. Stop treating "the store is in production" as the end. The store is the environment you landed in. The outcome sits behind the store: what the bench can promise this week. Your old success habit is shipping the interface the work named. The new habit is noticing when that interface is making a promise the workshop cannot keep, and treating that as your problem even when nobody wrote it in the original scope.

If the scope is wrong, staying neatly inside the scope is a failure. That sentence is the career change. It will feel rude the first time you use it, because good client work includes the discipline of not rebuilding someone's entire company. You still need that discipline. The charter is how you aim it. You widen the problem on purpose, then you narrow the first release on purpose. Widen without narrowing, and you have volunteered to run their operations. Narrow without widening, and you have shipped another screen.

Other people arrive at this role from other places. I will name them briefly, so you can recognize the bias, including your own.

From backend work, people bring services and failure handling, and they often wait for someone else to resolve a fuzzy requirement. Waiting is itself a decision.

From interface work, people bring the rare sense of whether a human can use the thing under pressure. They usually still need durability, identity, and deploy.

From data work, people see a stale table first. They usually still need the path a human is waiting on.

From model work, people know what a model cannot do. They usually still need the dull release habits that make a suggestion safe to trust.

From consulting, people can run a room. They need the credibility of having built the thing.

Your missing piece is not syntax. When a later chapter asks you to write code, it will slow down and show what a file is, what each part does, and how it fails. This chapter is the aim. [pause]

Question. Complete this sentence out loud. The store launched, and the studio still had to pause the ads because... [pause]

## How a missing boundary breaks

Part five. The failure. [pause]

"Write down who decides" sounds like paperwork until you watch the afternoon it prevents.

The store is live. A product can be ordered. Ads have, in the past, created more demand than the bench could finish, and the ads were paused. Picture the next version of that mistake, because the pause is the symptom you already lived. The charter has to name the failure underneath. I will show you the shape. You will name it.

A customer orders a pair, or asks for a custom one. Someone says yes. The yes might be the checkout itself, which is a yes the website gives without asking the bench. Or the yes might be a human reply, sent because the shop was busy and the message felt small. The maker is already full. The date slips. The founder now has an unhappy customer, a half-finished piece, and a reason to fear the next ad. So demand gets turned off. The website is working. The outcome is not.

If nobody wrote down who may promise a date, here is the argument that follows. The founder believes the store was supposed to grow the studio, so the store failed. The maker believes they were buried by promises they did not make. You believe you shipped what was scoped: catalog, payment, delivery, inventory. Everyone is partly right. That means the engagement has no owner for the only sentence that matters.

That is a boundary failure. It can be prevented on paper, before any new code. An unwritten assumption waits until it is expensive. Yours, if you leave it unwritten, is this: a live checkout is the same thing as a promise the bench can keep. It costs nothing on launch day. It costs the ads, later.

There is a second cost, and it is yours. People in this role burn out from unbounded responsibility, not from hard work. If the charter says you own the brand, the clay, the ads, the refunds, and the code, you have accepted a job the founder did not give you. The page protects the studio and it protects you. Deciding and doing stay separate. You may build the desk. You do not get to decide which custom design the studio is willing to make. [pause]

## How to write the page

Part six. The page. [pause]

The project is a one-page delivery charter for the first release of Promise Desk, for Mato Crafts. One page, because if it does not fit, you have not decided. Four readers have to recognize themselves. The founder. A maker. You, as the engineer. And a future person who has to trust the limit when a suggestion is wrong. At this studio that fourth person might also be the founder. Write it so a skeptical friend can still find that concern.

A verbal map for the page, six rooms, so you can hold them while you run. The failure. The people. The measure. The boundary. The roles. The risks. Say those six once. Failure, people, measure, boundary, roles, risks. [pause]

The failure room comes first, and it is not a solution. Write the workflow as it actually happens, including the ugly parts and the parts you do not know. You know some of it because you built it. The studio sells handmade pieces through a live store. The store has a catalog, custom orders, a cart, payments, delivery, and a way to show that something is sold out. Makers produce the pieces by hand. Ads were paused because demand outran making.

You do not know, unless you have watched it, the exact afternoon path. Do not invent a process to sound thorough. Write unknown where it is unknown. A charter that fabricates the shop floor is worse than a short one.

Then separate the symptom from the costly failure. "Ads were paused" is observed. It is a symptom. The costly failure is the thing that made pausing them rational. Candidates, and these are candidates, not your answer: a promised date the bench could not meet. A custom request accepted with no idea how long it takes. A product left orderable after the maker was already full. Overtime and broken pieces from saying yes too often. Pick the one the founder would recognize, label it assumed if you did not see it, and demote the rest to friction. A charter that tries to fix ads, branding, and expansion in the first release has not chosen.

Every factual claim gets a label. Observed, or assumed. "You shipped payments, delivery, and inventory" can be observed, because you did that work. "The bench can finish twenty pairs a day" is assumed unless someone showed you a count. An unlabelled claim is a failure of the page, not a style nit. If a number is not yours to publish, do not put it on the page. You can be specific without disclosing the studio's finances.

The people room has no single user. Subhechha wants the studio to grow, and she has already shown she will turn demand off rather than break the work. She needs a way to say yes again without that fear. She can veto anything. A maker wants a day that can be finished. A new tool that adds a form and removes nothing will be ignored, and ignoring it is a real veto. A customer wants a date they can trust, and a custom piece that matches what they asked for. They are not in the room. They still constrain the release. A faster checkout that lies about timing is a worse store. You want a system you can leave behind. Write the conflict. The founder can want the ads back on in the same week a maker wants the queue frozen. The charter does not dissolve that with cheerful wording. It states it, and the first release picks a side for now, with a reason.

The measure room has exactly one number. The test for it is simple. Could the studio compute it this month, from something that already exists or could be counted by hand, and would the founder recognize it as the thing that matters? Good shapes, still not your sentence: the share of accepted orders that meet the date someone actually promised. The number of orders accepted in a week that the bench cannot start. The time from a custom request to a human yes or no. Bad shapes: improve efficiency, grow the brand, model accuracy. Accuracy is a trap. There is no labelled truth for which handmade order should have been accepted. Two makers might disagree. You would spend the work scoring a model instead of protecting the promise. Measure the workflow. If today's number is unknown, write that, and make establishing it the first task. Do not invent a baseline to look rigorous.

The boundary room is three lists. What the first release does. What it does not do. What still requires a human. The third list is the one that saves you. A honest direction, which you may reject if your failure statement demands it: Promise Desk may show that the bench is full, and may suggest whether a new order can be promised. A human accepts, changes, or refuses the promise before the customer is told. No automatic yes. No automatic refund. No automatic ad spend. Non-goals are mandatory, and each one needs a reason from risk, evidence, or sequence. Not from what you feel like building. Likely non-goals, for you to accept or replace: replacing the current store, turning the ads back on, designing new products, letting a model reply to a customer. Someone will ask for each of these. A written non-goal turns the argument into a reference. A non-goal is a schedule with a reason. It is not an insult to the founder.

The roles room is a matrix. Rows for the founder, a maker, you, whoever can stop a deploy or an ad change if that is not already you, and Promise Desk itself. For each row: what they decide, what they do, and where they escalate. The system's row must contain a prohibition, not only a capability. Finish this thought in your own words. It may suggest a promise, and a person must confirm it before a customer is told. If you cannot write the prohibition, you are not ready to build. Separate deciding from doing. The founder may decide that a design is in bounds. A maker does the making. You may build the check. You do not decide the brand's taste. Do not give yourself the business risk. It feels like ownership. It is how you end up accountable for a late pair you had no authority to refuse.

The risks room holds three risks. Each one needs the evidence that would retire it. Here is the shape of one, so you can hear the difference between anxiety and a research task. Risk: makers will not trust the suggestion, and will keep the notebook they already use. Evidence that retires it: in a week you actually watch, they accept or amend the suggestion on real orders, rather than ignoring it. Your other two should come from this studio. Personal data in an order note. A checkout that still says yes while the desk says no. You being the only person who can change the system. Pick risks that, if they came true, would recreate the costly failure. A risk that would apply to any website is not a risk for this charter.

Let me label three sentences the way the page has to label them, so the habit is in your ear before you write. First sentence: Mato Crafts sells handmade polymer-clay earrings from a shop at Patan Dhoka, and you shipped the store that takes payment and delivery. That one is observed. You did the work, and the shop is public. Second sentence: the ads were paused because orders got ahead of what the makers could finish. Also observed, from the delivery itself. It is still a symptom, not the failure underneath. Third sentence: the bench can finish twenty pairs on a normal day, and custom requests sit in a notebook by the oven. That one is assumed, unless you have stood there and counted. If you put it on the page without the label, you have started inventing the studio in order to sound precise. Precise and invented is worse than short and honest. Do this to every sentence you write. Observed, assumed, or unknown. [pause]

What finished sounds like, without handing you the sentences. The page opens on the studio as it is. Handmade pieces. A live store you already shipped. A bench with a finite day. Ads paused when orders outran making. Claims labelled. Unknowns left unknown. It names one costly failure. It names the conflict between growth and a finishable day. It has one measure, and it admits if today's value is not on record. It has three lists. It has a matrix whose system row can refuse. It has three risks with finish lines. A founder can explain the first release in two minutes without saying a framework, a model, or a vendor. A maker can see they are not being automated out of the promise. You can see what you are not allowed to decide.

If your page is a transcript of this chapter, it fails. The reasoning is here. The sentences have to be yours, because you are the one who will defend them when the first awkward order arrives. [pause]

## How the page goes wrong

Five ways this work fails. Listen for the one you are most likely to commit.

The solution-shaped charter. The page describes a bot, a database, a dashboard. Delete every implementation noun. If the problem disappears with them, start again from the bench.

The everything charter. Ads, a new store, custom design tools, international shipping, a full factory plan. Ambition here is a narrow release that lands. The pause already taught you what happens when the surface gets ahead of the hands.

The unfalsifiable outcome. Satisfaction, a mood, a usage count. If the number cannot go down, you cannot trust it when it goes up.

The invisible human. The page implies the desk tells the customer yes. That is the failure you are here to make impossible.

The flattened client. You wrote "the client" and never separated the founder who wants demand from the maker who has to meet it. Later, the tool is unused, and you are surprised.

And one that is specific to you. The launch charter. It describes a successful relaunch of the website. That is the job you have already done. This course starts where that job stopped. [pause]

## How you check it

This is a writing chapter, so the checks have to be things you can do out loud.

The two-minute test. Explain the first release as if to Subhechha. No service, no model, no stack. If you cannot, the charter is a build plan.

The disagreement test. Find two wants that do not fit. If you cannot, you wrote a brochure.

The veto test. Who can stop this? The founder, yes. Who else, including a maker who simply does not use it? Each of them needs a path to yes.

The measurement test. How would you compute today's value with what the studio already has, even if that is a notebook? If the answer is that nothing records it yet, that sentence belongs on the page.

The prohibition test. Read the system's row. It needs a clear may-not.

The quiet test. Hand the page to someone who has not heard this chapter. Ask what the first release refuses to do, and who is accountable when a customer is told a date the bench cannot meet. Stay silent while they read. Whatever they miss is the document.

The fiction test, because this customer is real. Read every sentence and mark it observed or assumed. If a sentence would embarrass you when read back in the shop, because you guessed their internals, it is assumed, or it comes off the page. Do not publish their finances. You do not need a revenue figure to name the operational problem. [pause]

## Your project

The written guide has the situation brief, the constraints, and the rubric. The brief is the input. You do not invent a company, and you do not switch customers. Mato Crafts is the customer.

You will write three things. A one-page charter. A responsibility matrix that includes Promise Desk and everyone who can block a decision. A risk register where each risk has the evidence that would retire it. Put them in the chapter one folder of the field workspace. They are yours to commit when you want them in the repo. Do not commit customer personal data, payment details, or ad-account access.

The constraints, so you hear them before you open the guide. One page. No implementation detail. Every claim labelled. Non-goals required. One measure the studio could actually compute. The system gets a prohibition. You do not grade yourself generously.

There is no code in this chapter. There is no starter file with the answer hiding in it. The empty page is the starting state. The studio is specified, so your effort goes into judgment. [pause]

## What you carry

You are still moving, so here is the hour again, in the order you can replay if a part slipped.

The studio. Handmade earrings in Patan. A store you already shipped. Ads paused because the bench could not keep up. That pause is a symptom. Promise Desk is the limit on the promise, not a second website.

The role. You build inside their environment, and you are accountable for an outcome. At this shop the environment you do not yet know is the bench, not the checkout. The system has to work after you leave.

Who decides. A reusable core. The promise the store already made. The accounts, which may be you. The founder and the makers, who can want opposite things on the same day. And Promise Desk, which may suggest and may not tell a customer yes.

Your shift. A launched site is not the end of the job. If the scope never mentioned a keepable date, noticing that is part of the work. Then you narrow the first release so you do not accidentally take over the studio.

The failure. A yes from the checkout, a full bench, a slipped date, demand turned off. The missing sentence is who is allowed to promise.

The page. Six rooms. Failure, people, measure, boundary, roles, risks. One page. Labels on every claim. One number the studio could count. A human between the suggestion and the customer.

Whatever you build next starts from this page. Go write it.
