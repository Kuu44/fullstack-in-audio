---
chapter: 7
title: "Frontend foundations: semantics and accessible intake"
roadmap_nodes: ["Frontend Skills", "Frontend", "HTML"]
part: "II — Build the customer-facing experience"
audio: media/07-frontend-foundations.mp3
voice: en-US-AndrewNeural
rate: "-15%"
companion_guide: docs/guides/07-frontend-foundations.md
---

# Chapter 7 — Frontend foundations: semantics and accessible intake

[[Spoken narration begins below. Headers and this note are stripped before rendering.]]

## Orientation

Welcome to chapter seven of FullStack in Audio. This is the first chapter of Part Two, where FieldOps Copilot stops being a thing you run in a terminal and becomes something a customer can actually look at and use.

Let me remind you where the build stands, because everything in this chapter attaches to work you have already done. You have a delivery charter that names a real customer team, the failure that costs them money, the operator who will use the system, and one measurable outcome. You have a priority rule, expressed as a small pure function, that turns severity, business impact, age, and confidence into a single triage priority. You wrote that rule three times in three different languages, then once more in Python, so you know it is portable and you know why you picked the runtime you picked. You have a command line intake tool that accepts one incident record, validates it, and prints a readable priority. You have a repository with a history a reviewer can follow, a readme another engineer can execute, and a diagram of the full stack seam: browser, interface layer, priority service, and a data store that does not exist yet. And you have an architecture split that marks which parts are reusable core, which parts are customer configuration, and which parts are customer specific adapters.

Now we open the browser. In this chapter you build the incident intake page: the first surface a customer operator will touch. There is no styling in this chapter, no JavaScript framework, no network call, and no server. That constraint is deliberate. The document itself, before any of those layers, either carries meaning or it does not, and almost every accessibility failure and data quality failure I have seen in a field deployment was already present in the document before anyone added a single line of style or script.

By the end of this lesson you will know what a browser document actually communicates to the machinery around it, how to build a form that produces trustworthy data, how to make a keyboard-only path through that form, how to give an operator error feedback they can act on, and how to verify all of that without guessing. Then you will build it yourself.

## What the frontend actually is

Let me start by narrowing the word frontend, because it is used to mean three different things and the ambiguity causes real design mistakes.

Sometimes frontend means a job description: the person who works on interfaces. Sometimes it means a technology set: documents, styling, scripting, build tools, component libraries. And sometimes, most usefully for us, it means a position in a system. The frontend is the boundary where a human intention gets converted into structured data, and where structured data gets converted back into something a human can perceive and act on. That is the definition I want you to hold, because it makes the frontend a data contract problem rather than a decoration problem.

Under that definition, the browser is not a canvas. The browser is a runtime with an opinionated document model, a security model, an input model, and an accessibility model, all of which you inherit whether you engage with them or not. Your job in this chapter is to engage with them on purpose.

Start with the document. A browser document is a tree of elements. Each element has a tag name, some attributes, and possibly children. That is the mechanical description. The important part is that the browser reads meaning out of those tag names. A heading element is not a big bold line of text; it is a declaration that a new section of content begins here, at a particular depth. A list element is not indentation with bullets; it is a declaration that these items are peers, and it tells assistive technology how many items there are before the user commits to walking through them. A button is not a rectangle you can click; it is a control that is reachable by keyboard, activatable by two different keys, exposed to automation, and announced by its role.

From that tree, the browser builds a second structure. It is usually called the accessibility tree. Think of it as the machine-readable summary of your interface. Every node in it has, at minimum, a role, an accessible name, sometimes an accessible description, and a set of states: is it required, is it invalid, is it disabled, is it expanded, is it checked. Screen readers read that tree. Voice control software targets that tree. Browser automation and many end to end test tools query that tree. Increasingly, so does anything trying to interpret a page programmatically.

Here is the sentence I would like you to carry out of this chapter: your accessible names and roles are an application programming interface. They are just as much a contract as the shape of a request body, and they are consumed by more clients than you expect. When you name a control badly, you are not making a cosmetic mistake, you are shipping a bad interface to every consumer of that tree, including the automated tests you will write in chapter nine and ten.

Now the form. A form is the part of a document whose entire purpose is to collect and submit a set of values. The browser gives you an enormous amount for free here, and most of what looks like sophisticated frontend engineering in an intake screen is really just the native form model used correctly.

Four pieces matter most.

First, the control types. Text inputs, multi-line text areas, checkboxes, radio buttons, selects, number inputs, date inputs. Each type carries its own keyboard behavior, its own mobile keyboard, its own validation semantics, and its own announced role. Choosing the right type is a design decision with real downstream consequences, and we will spend time on it.

Second, labels. A label is not text that happens to sit near a control. A label is an element that is programmatically associated with exactly one control, so that the browser can compute the control's accessible name, and so that clicking the label moves focus into the control. Association happens either by pointing the label at the control's identifier, or by wrapping the control inside the label. Both are fine. Text merely positioned above a box is not fine, and that is the single most common defect in enterprise intake forms.

Third, grouping. Some controls are only meaningful as a set. A severity choice made of four radio buttons is one question with four answers, not four independent questions. The document model has a grouping element for exactly this, with a caption element that names the group. Without it, a screen reader user hears four options with no idea what question they answer.

Fourth, validation feedback. The browser has a built-in constraint model: you can mark a field required, constrain its length, constrain its pattern, constrain a numeric range. When a constraint fails, the browser can block submission and surface a message. You can also take that over yourself and render your own messages, which is usually what a production tool ends up doing, because the built-in bubbles are terse, disappear, and are hard to style consistently. Either way, the requirement is the same: the error must be perceivable, it must be associated with the control that failed, and it must say what to do next.

There is one more concept to define before we move on, because it will come up in every later chapter of this part: progressive enhancement. Progressive enhancement means the document works at a baseline level with the simplest possible mechanism, and richer behavior is layered on top. In this chapter your form works with no scripting at all. In chapter nine you will add typed asynchronous submission on top of it. In chapter ten you will rebuild it as components. Each layer should be an improvement to something that already functioned, not a replacement for something that never did. That sequencing is not an academic preference. It is how you keep a field deployment debuggable, because when the rich layer breaks at a customer site, you want to know that the layer underneath was correct.

## Why a forward deployed engineer cares

Now let me connect this to the field, because if you learn semantics as a compliance chore you will do it badly.

Consider who uses an operational intake tool. A facilities dispatcher on a shared workstation with a browser two versions behind. A field technician on a narrow laptop in a truck, one handed, in a hurry, at the end of a shift. A night shift operator who was trained by the person who quit last month. A manager who opens the tool twice a month. A security reviewer who will open it once, adversarially. And, at some fraction of any real enterprise workforce, someone using a screen reader, someone using voice control, someone with low vision at high zoom, someone with a motor impairment who cannot reliably hit a small target.

That population has three consequences for you.

The first is data quality, and this is the one engineers underestimate. Everything you build in the rest of this course consumes what this form produces. In chapter eleven the server calculates priority from these fields. In chapter thirteen they become the durable record of what happened. In chapter twenty the retrieval layer decides which runbook applies based on the service and the impact. In chapter twenty two you evaluate whether the AI recommendation was good, using these fields as the input. If severity is an unconstrained text box, you will receive the word urgent in lower case, the same word shouted in capitals, the number one, the number five meaning the opposite of the other person's five, the phrase very bad, and an empty box. No prompt engineering fixes that. No model fixes that. The intake form is where your data model is either enforced or abandoned, and an ambiguous form is a permanent tax on every downstream layer.

The second consequence is trust, and trust is the currency of a pilot. An operator forms an opinion about your system in the first ninety seconds. If the form loses their typing when they hit an error, or if they cannot tell which field was wrong, or if tab moves focus somewhere absurd, they conclude the tool is unfinished. Once they conclude that, they route around it, and adoption numbers you will be asked about in chapter thirty five never materialize. The intelligence layer does not get a chance to be impressive, because nobody feeds it real work.

The third consequence is procurement. In any enterprise, public sector, healthcare, education, or financial customer, accessibility is not a nice to have, it is a document. You will be asked for a conformance statement. Somebody will run an audit tool and send you the report. If you built the form semantically from the start, that conversation costs you an afternoon. If you built it out of generic containers and click handlers, you are looking at a rewrite of the interface, at the worst possible moment, with the security review happening in parallel. I have watched a pilot slip a full quarter for exactly this reason, and the technical work required to have avoided it was perhaps two hours of care during the first week.

There is a fourth reason that is less often stated. Semantic markup is the cheapest testing affordance you will ever buy. When your controls have real roles and real accessible names, your tests can find them the way a human describes them: the button named submit incident, the group named severity, the field named affected service. Those tests survive restyling and refactoring, because they are bound to meaning instead of to structure. When you rebuild this same form as components in chapter ten, the tests you wrote against meaning will mostly still pass, and that is not luck.

## How to build it: the decisions that matter

Now the how. I am going to walk you through this as a sequence of decisions rather than a sequence of keystrokes, because the decisions are the transferable part.

Begin with the record, not the page. Open your charter and write down the fields you actually need for a first release. For FieldOps Copilot I would expect five: a short title, a severity, an affected service, a business impact, and a longer description. Resist adding more. Every optional field on an intake form is a small tax on every future submission and a source of missing data in every future analysis. If you cannot name who consumes a field and what decision it changes, it does not belong in release one.

For each field, decide four things: what type of control expresses it, whether it is required, what the failure message says, and what the value looks like when it reaches your code.

Take the title. It is a short free text field, it is required, and its purpose is to let an operator scan a list later and recognize this incident. That last part is a design constraint, and it means your label should not just say title. It should say something that hints at the expected content, and the field should carry a short piece of help text explaining that a good title names the symptom and the location. That help text should be programmatically attached to the control as its description, not floating nearby as unassociated prose, because a screen reader user needs to hear the guidance at the moment they focus the field, not five minutes earlier.

Take severity. This is the field that most rewards careful thought. It is a closed set of mutually exclusive values, and the number of values is small. A radio group is the right control. Not a text box, obviously, but also, in my judgment, not a dropdown. A dropdown hides its options until opened, which means the operator cannot see the full scale while deciding, and the difference between severity two and severity three is exactly the judgment you want them to make with the whole scale visible. A radio group shows all options, is fully keyboard operable with arrow keys, and announces itself as one question with a known number of answers. Wrap it in a group with a caption naming the question.

There is a second decision inside severity: the labels themselves. Numbers alone are ambiguous across organizations. Use the customer's words and attach a short definition to each option, so that critical means the service is down for many users with no workaround, and low means a single user with a workaround. That definition text is the difference between a scale and a coin flip, and it is the cheapest data quality intervention available to you.

Take the affected service. This is a closed set too, but a potentially large one, and it is owned by the customer, not by you. In release one you will hard code a handful of values, and you should mark in your notes that this list is customer configuration, not product code, which is exactly the distinction you drew in chapter six. In chapter twenty four you will feed the real list in from an asset inventory pipeline. For now, if the list is short, a select is fine. If it is long, a text input with a list of suggestions is kinder, because it lets an operator type three letters instead of scrolling. Whatever you choose, note the size at which your choice breaks. A select with three hundred options is not a user interface, it is a punishment, and you should know now that the pipeline chapter has to solve it.

Take business impact. Be careful here: it is tempting to make this free text, because impact is genuinely nuanced. But your priority rule needs a comparable value. The compromise I recommend is a closed set for the impact category, plus an optional free text field for the nuance. That way the rule has something to compute on, and the human context is not lost. Notice what just happened: a data modeling decision resolved a user experience tension. That is normal, and it is why the frontend is not downstream of the model, it is part of it.

Take the description. Multi-line, required in my view, and this is where you place your prompt for good input. Ask three explicit questions in the help text: what did you observe, what were you doing when it happened, and what have you already tried. That is the information your AI triage layer will beg for in chapter fifteen, and the cheapest place in the entire system to obtain it is right here, at the moment the human still remembers.

Now the structure of the page. Give the document one main landmark containing the form, a single top level heading naming the tool, a second level heading naming the task, and a form region with an accessible name. Landmarks let a keyboard or screen reader user jump straight to the work instead of walking through your header. Order the document so that the reading order matches the logical order, because in this chapter, with no styling, reading order is visual order, and in the next chapter, when you add layout, you must not break the correspondence.

Next, submission and feedback, which is where most of the engineering lives.

Decide first what submission means in this chapter. There is no server. You have two honest options. You can let the form submit to itself and re-render, which is the true baseline behavior and works with no scripting at all. Or you can intercept the submission with a small amount of scripting and render a confirmation region in place. Either is acceptable. What is not acceptable is a page that implies the incident has been filed, when in fact nothing left the browser. Say so, plainly, in text that the operator will read. Something like: this record has not been sent to a server yet, it is a local preview. That sentence costs you nothing and it prevents the single most damaging demo failure in field work, which is a stakeholder believing a capability exists because a screen said so.

Then design the error experience. Here is the pattern I recommend, and it is worth memorizing because it works in every framework you will ever use.

On a failed submission, do three things. Render a message next to each failing control, and associate that message with the control as its error description, and mark the control invalid so that state is exposed. Render a summary at the top of the form listing every failure, where each entry moves focus to the offending control when activated. And move focus to that summary, so a keyboard or screen reader user is told immediately that something went wrong, rather than being left at the bottom of the form wondering why nothing happened.

The message wording deserves attention. An error message has one job: tell the operator what to do next. Invalid input tells them nothing. This field is required tells them almost nothing. Choose a severity so the triage rule can rank this incident tells them what and why. When you write these messages, imagine the least confident person on the night shift reading them, and write for that person.

Do not validate aggressively while typing. Validating an email field on every keystroke means telling someone their address is invalid four times before they finish. Validate on submission, and optionally re-validate a single field when the operator leaves it, and always clear an error the moment the input becomes valid.

And do not disable the submit button to prevent invalid submissions. It is a popular pattern and it is a trap. A disabled button often cannot receive focus, so a keyboard user cannot reach it to discover why it is disabled, and the reason is usually not stated anywhere. Leave the button enabled, let the submission fail, and explain the failure. The operator learns more from a clear rejection than from a dead control.

Finally, the confirmation. When submission succeeds, show the record back to the operator, including the fields as they were interpreted, and announce it. Announcement matters because if you swap content in without moving focus or marking the region as one that reports updates, a screen reader user gets silence. Show the interpreted values, not just a success message, because that is how an operator catches a mis-selected severity in the two seconds when it is still cheap to fix.

## Five details that are easy to skip

Before the pitfalls, five small things that cost seconds and pay for themselves.

Declare the document's language. It is one attribute on the root element, and it tells a screen reader which pronunciation rules to use. Without it, an English page read by a synthesizer configured for another language is close to unintelligible. If your customer operates in more than one language, note now that this attribute is customer configuration, and that chapter ten is where a language choice would actually get wired in.

Give the page a real title. The title is the first thing announced, the text in the browser tab, the label in the window switcher, and the name in a bookmark. A title that names the tool and the task, in that order, orients a person who has six tabs open. A title that says index or untitled tells them nothing.

Declare the purpose of fields that have a standard purpose. Browsers can fill in a name, an email address, an organization, or a phone number when you tell them what the field is for. On an intake form used forty times a shift, that is minutes saved per person per day, and for someone with a motor impairment it is a meaningful reduction in effort. Our five incident fields mostly have no standard purpose, but if you add a reporter contact field, declare it.

Pick input types with the mobile keyboard in mind. A numeric field that summons a full alphabetic keyboard on a phone is a small daily insult. A field for a date should use a date control unless you have a specific reason not to. Field technicians are frequently on phones, and this course's charter almost certainly includes them.

Name the form region itself. A page with one form does not strictly need it, but a page that will grow to have a filter form and an intake form does, and giving the region a name now means the day you add the second form, a keyboard user can still tell them apart. Do the cheap thing early when you already know the page will grow.

## Pitfalls, named

Let me name the failures I expect you to hit, so you recognize them rather than debug them from scratch.

The placeholder as label. A placeholder is grey hint text inside a field. It disappears the moment typing starts, it is often too low contrast to read, and it is inconsistently exposed as an accessible name. If your only indication of what a field is disappears when the field is used, then anyone who is interrupted mid form has lost the plot. Use a visible label always. A placeholder may show an example format, and nothing more.

The generic container acting as a control. A clickable box that is not a button cannot be reached by tab, does not respond to space or enter, is not announced as actionable, and is invisible to your future tests. If it behaves like a button, make it a button. If it navigates to a different address, make it a link. This is the single highest value rule in frontend accessibility, and it is free.

Color as the only signal. If your required indicator is a red asterisk and your error is red text, then a person who does not perceive red perceives nothing. Every state needs at least two cues. We will do the visual half of this in chapter eight, but the textual half is here: the word required, and error text that reads as error text.

The error summary with no focus management. Teams often add a summary at the top of the form and then never move focus to it. The result, for a keyboard user, is a submission that appears to do nothing at all. If you take away one implementation detail from this lesson, take that focus move.

Broken tab order. Tab order follows document order, not visual order. In this chapter with no styling they are the same. Note that fact now, because in chapter eight it is possible to reorder things visually while document order stays put, and then focus jumps around the screen in a way that feels haunted. Also resist the urge to force tab order with explicit ordering values. Fixing document order is almost always the correct repair.

Ambiguous accessible names. Three buttons all named submit, or a link named click here, or an icon button with no name at all. Test the names by reading them out of context: if the name alone does not tell you what the control does, an assistive technology user who is listing controls does not know either.

Nested and pointless interactivity. A button inside a link, a control inside a label that also wraps another control, an entire row made clickable with a nested delete button. Each of these creates an unresolvable focus and activation puzzle. Keep interactive elements flat and singular.

The description that is nearby but not attached. Help text sitting under a field, visually associated, programmatically orphaned. Attach it. Same for error text.

And finally, the pitfall that matters most for your career in the field: treating browser validation as enforcement. Everything you do in this chapter is a courtesy to a cooperating user. Every constraint here can be removed by anyone with a browser and thirty seconds. In chapter eleven you will validate the same record on the server, and that will be the real enforcement. If you internalize this now, you will never build the class of system where a business rule exists only in the interface, which is the class of system that fails a security review in chapter thirty two.

## Verifying your work

Now, how do you know it is right? Not by looking at it. Run four passes, each of which takes a few minutes.

Pass one, keyboard only. Move your mouse out of reach. Load the page and, using only the tab key, arrow keys, space, and enter, reach every control, fill every field, trigger a failed submission, navigate from the error summary to the failing field, correct it, and submit successfully. At every single stop, you must be able to see where focus is. If focus disappears, even for one stop, you have found a defect. Write down what you had to do that a hurried operator would not figure out.

Pass two, the accessibility tree. Your browser's developer tools can show you the accessibility representation of the page. Walk it. For every control, confirm three things: the role is what you intended, the accessible name is the label you meant, and the required and invalid states appear when they should. Then, separately, list the headings and landmarks and ask whether that outline alone describes the page. If the outline reads as one heading called untitled document and one region called main, you have a document that is technically valid and practically opaque.

Pass three, degradation. Zoom the page to two hundred percent and confirm nothing becomes unreachable. Then disable styling entirely, which in this chapter changes almost nothing, and read the content top to bottom. It should read as a coherent sequence: what this tool is, what you are being asked for, each question, the submit action. If it reads as a scrambled pile, your document order is wrong and no amount of layout will fix it.

Pass four, the data pass. Submit a good record and look closely at the values your confirmation displays. Are they the values you expect, in the shape you expect, with the severity as a stable value rather than a display string? Then submit deliberately bad records: everything empty, only the title filled, a description of one character, a title of five hundred characters. For each, ask whether the response tells the operator what to do. This pass is where you discover that your data model and your interface disagree, and it is much cheaper to discover that now than in chapter thirteen when the disagreement is persisted in a database.

Record what you find. Two or three sentences per finding, in the delivery log you started in Part One. In field work, the record of what you checked is nearly as valuable as the fix, because in chapter thirty two somebody will ask you what accessibility verification you performed, and an honest specific answer is worth more than a claim of full compliance.

## Your practice test

Here is the work. The companion guide states it precisely, with a rubric; this is the spoken version.

Your goal is a single incident intake page for FieldOps Copilot, built from an empty file, that collects a title, a severity, an affected service, a business impact, and a description, and shows the operator what was captured.

Your constraints: no styling framework and no component framework in this chapter. Every control has a visible, programmatically associated label. The severity options are grouped with a caption that names the question. Required fields are indicated in text, not only visually. Every validation failure produces a message associated with its control, plus a summary that receives focus. The page states, in plain words, that submission is local until a later chapter connects a service. And there is a complete keyboard only path from page load to successful submission.

Your artifacts: the page itself, a short note listing each field with its control type and the reason you chose it, a keyboard walkthrough note recording your tab path and anything that surprised you, and one accessibility finding you discovered through inspection along with the change you made in response.

You are done when a person can complete the whole workflow without a mouse, when every field is labeled and every error is both announced and actionable, when the page does not imply that a record was filed on a server, and when you can explain, for each field, what downstream layer consumes it.

One more instruction that applies to every chapter of this course: write it yourself. Not because copying is morally wrong, but because the skill this chapter builds is the habit of asking, for each control, what does this mean to a machine and to a stranger. That habit only forms while your own hands are making the decisions.

## Recap

Let me close with the five things worth keeping.

First, the frontend is a boundary where human intention becomes structured data. Treat it as part of your data model, not as decoration.

Second, roles and accessible names are an interface consumed by assistive technology, automation, and your own tests. Name things as if a stranger will call them by name, because a stranger will.

Third, the browser's native form model gives you labels, grouping, constraint validation, and keyboard behavior for free. Most heroic frontend work on an intake screen is really that model, used correctly.

Fourth, error feedback has one job: tell the operator what to do next. Associate it, announce it, move focus to it, and write it for the least confident person on the shift.

Fifth, none of this is enforcement. The server is the authority, and we build that in chapter eleven.

In chapter eight we keep the same document and add the visual layer: layout, density, state affordances, and the design tokens that let an operator see a critical incident before they read a word. Build the page first. Then meet me there.
