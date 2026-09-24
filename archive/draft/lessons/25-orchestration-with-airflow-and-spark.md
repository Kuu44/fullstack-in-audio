---
chapter: 25
title: "Orchestration with Airflow and Spark"
slug: 25-orchestration-with-airflow-and-spark
part: "Part V — Move and operate the data and model workflows"
roadmap_nodes: ["Airflow", "Spark"]
voice: en-US-AndrewNeural
rate: "-18%"
audio: media/25-orchestration-with-airflow-and-spark.mp3
companion_guide: docs/guides/25-orchestration-with-airflow-and-spark.md
---

# Chapter 25 — Orchestration with Airflow and Spark

> Narration script. Headings, frontmatter, and blockquotes are stripped before rendering; only the prose below is spoken.

Welcome to chapter twenty-five. Last chapter you built an ingestion job for customer asset context: a contract, four separable stages, a quarantine, lineage on every row, and a run record. It works when you run it. Today we turn that job into something that runs without you, recovers from the failures that are normal in the field, and can be pointed at a historical date when somebody asks what the inventory looked like three weeks ago.

That is what orchestration means. It is not a technology category you adopt. It is the answer to four questions about work that happens on its own: when does it run, what must finish before it starts, what happens when it fails, and how do you know what happened. Every orchestration tool you will ever meet, from a scheduled task on a single machine to a cluster-scale workflow platform, is an opinion about those four questions.

We will use Apache Airflow as our vocabulary because it is the most widely deployed workflow orchestrator in enterprise data teams, and because there is a high chance your customer already runs it. Then we will look honestly at Apache Spark, which is a different kind of tool entirely, and which is frequently introduced into pilots that do not need it. By the end I want you to be able to design a dependable refresh workflow, and to be able to tell a customer, with evidence rather than opinion, whether distributed processing belongs in their deployment.

Let us build the vocabulary.

The central idea in Airflow is the directed acyclic graph, usually just called a DAG. Take that phrase apart. A graph is a set of units of work with connections between them. Directed means the connections have a direction: this finishes, then that starts. Acyclic means there are no loops, so the work always terminates rather than circling forever. In Airflow, a DAG is the whole workflow, defined in code, and each unit of work inside it is a task.

A task is one thing you want done: fetch the export, validate it, load it, run the assertions, send the notification. The connections between tasks are dependencies, and they are the entire point. When you declare that load depends on validate, you are making a promise that is enforced by the system rather than by a comment in a script: unsafe data cannot reach the destination because the loading task will not even be attempted unless validation succeeded.

An operator, in Airflow's language, is the type of a task: run this Python function, run this shell command, wait for this condition, call this service. Do not over-invest in operator taxonomy. The thing that matters is that each task is small, has a single responsibility, and reports success or failure honestly.

A sensor is a task that waits for something to become true before allowing the rest of the graph to proceed. In field work the most common use is waiting for an export file to appear. Sensors deserve a warning: a sensor that waits forever is a task that never fails, and a task that never fails will never alert anybody. Always give a waiting task a deadline, and make the expiry of that deadline a failure rather than a silent continuation.

The scheduler is the component that decides which tasks are eligible to run right now, based on the schedule you declared and on which dependencies have been satisfied. The executor is the component that actually runs them, locally, in separate processes, or on separate machines. For a pilot, the distinction rarely matters. For a customer deployment, it is a sizing conversation: how many tasks can run at once, and what happens when more are eligible than there is capacity for.

Now the concept that confuses almost everybody the first time, and which is central to doing this well: the difference between when a workflow runs and what data it is running for. Airflow calls the second thing the logical date, or in older language the execution date. Here is why they are different. Your nightly asset refresh runs at two in the morning, but it is processing the export produced for the previous day. If you write your job to use the current clock, then running it once, on time, gives the right answer, and running it again tomorrow to fix a bug gives a completely different answer, because the clock moved. If instead your job takes the target date as an input, then every run is reproducible: the run for a given date always produces the same result, whenever you execute it.

This is the single most valuable habit in orchestration, so let me state it as a rule. A task should be a pure function of its inputs, and the target time period should be one of those inputs, never read from the clock inside the task. When that rule holds, retries are safe, reruns are safe, and backfills are just ordinary runs with older inputs. When it does not hold, every one of those becomes an adventure.

Which brings us to retries. A retry is the system running a failed task again, automatically, after a delay. Retries exist because a meaningful fraction of failures in the field are transient: a network hiccup, a source system restarting, a brief authentication refresh, a lock held for a few seconds. Retrying those costs nothing and saves a human from being paged at three in the morning for something that fixed itself.

But retries are only safe for a class of failure, and confusing the classes causes real damage. Think of failures in three buckets. Transient failures should be retried, usually two or three times, with increasing delays between attempts. Deterministic failures should never be retried, because the second attempt will fail identically: a schema violation, a contract breach, a missing required field, a permission that was revoked. Retrying those just wastes time and buries the real signal under repeated noise. And then there is the dangerous middle bucket: failures where you do not know whether the work partially completed. A load that timed out may have written half its rows. This is exactly why we spent so long on idempotency last chapter. If your load is idempotent, the ambiguous bucket collapses into the transient bucket and retrying is safe. If it is not, a retry can double your data, which is worse than the original failure.

So the retry policy is not a number you set by habit. It is a decision per task: is this failure transient, and is this task safe to repeat? Write the answer down, especially for the task that writes.

Next, backfill. A backfill is running the workflow for a time period in the past. You will need this more than you expect. You will need it when you fix a transform bug and must reprocess a week. You will need it when a source system was down and its exports arrived late. You will need it when a customer asks for historical context that your pipeline was not yet collecting. A workflow designed around the logical-date rule can backfill by definition. One that reads the clock cannot, and retrofitting it under pressure is miserable.

There is a related setting worth understanding because it surprises people: catchup. If you deploy a scheduled workflow with a start date in the past, some orchestrators will immediately try to run every interval between then and now. That is occasionally what you want, and it is usually a stampede against a customer's source system at the exact moment you are trying to make a good impression. Know the default in whatever tool you use, set it deliberately, and always bound how many past runs may execute at once.

The last piece of Airflow vocabulary is the run history. For every execution of every task, you get a status, timings, and logs, retained and browsable. This is the operational evidence I keep asking you for, and in the field it earns its keep in a specific moment: the customer says the data was wrong last Thursday, and you can open Thursday's run, see that the validation task failed, see the reason, and see that the load task therefore never ran. That is a two-minute conversation instead of a two-day investigation.

Before we leave Airflow's vocabulary, there is one more concept that matters disproportionately in customer environments, and that is the service level expectation attached to a workflow. Most orchestrators let you declare how long a workflow or a task is expected to take, and alert when it exceeds that. This sounds like a nicety and it is actually one of your best early-warning signals, because the failure mode that hurts a pilot is rarely a workflow that crashes. A crash is loud. The dangerous one is the workflow that still succeeds but now takes four hours instead of twenty minutes, because the source system got slower or the data got bigger. It succeeds every night, right up until the night it does not finish before people start work. A duration expectation turns that slow slide into a warning weeks in advance.

Let me make the whole failure picture concrete with a scenario, because I want you to recognize the shape of it before you live through it.

A team deploys the asset refresh on a Friday. It is scheduled nightly. Over the weekend the customer's export host is rebooted for patching and, for two nights, the file arrives four hours late. The sensor waiting for that file has no deadline, so on both nights the workflow simply sits there waiting, and because it never fails, nobody is notified. On Monday, someone notices two workflow runs still in a running state, and cancels them. That looks like cleanup; it is actually data loss, because those two days are now simply missing and nothing in the system records that fact.

Then the well-intentioned part. The engineer redeploys the workflow with an earlier start date to pick up the missing days, catchup is on by default, and the orchestrator immediately launches fourteen historical runs at once, all of which hit the customer's export host simultaneously at nine fifteen on a Monday morning. The host, which serves other consumers, slows to a crawl. Within the hour there is a call with the platform team, and the pilot has acquired a reputation problem that has nothing to do with the copilot's quality.

Every part of that is preventable with decisions we have already named. The sensor gets a deadline, so a late file fails the run loudly on the night it happens. The failure notification names the workflow, the date, and the reason. The missing days are visible as failed runs rather than as absent ones, so nobody has to notice them by accident. Catchup is set explicitly, and concurrency for historical runs is bounded to one or two, so a backfill is a trickle rather than a flood. And before any large reprocess against a customer's system, you tell the person who owns that system what you are about to do and when.

I want you to notice the pattern. None of these are sophisticated engineering. They are defaults you chose deliberately instead of accepting, and in field work that is most of what reliability actually consists of.

Now let us turn to Spark, which people often mention in the same breath as Airflow, and which is a fundamentally different kind of thing. Airflow decides when work runs and in what order. Spark is a way of doing one piece of work across many machines. They solve different problems, and confusing them leads to some strange architectures.

The premise of Spark is that your data is too large to process on one machine, or would take too long. It splits a dataset into partitions, distributes them across a cluster, and runs your transformation on each partition in parallel. A driver program coordinates, and executors do the work. Two properties matter for our purposes.

The first is lazy evaluation. When you describe a chain of transformations, Spark does not immediately do them. It builds a plan, optimizes it as a whole, and only executes when you ask for a result. This is powerful and it also means your mental model of what runs when will be wrong until you learn to read the plan.

The second is the shuffle. Some operations can be done entirely within a partition: filtering rows, computing a value from fields in the same row. Those are cheap and parallelize beautifully. Other operations need data from different partitions to meet: grouping by a key, joining two datasets, sorting globally. To do those, Spark must move data across the network between machines, and that movement is called a shuffle. Shuffles dominate the cost of most Spark jobs. When somebody says a Spark job is slow, the answer is usually that it is shuffling more than it needs to, often because the data is partitioned by the wrong key.

Partitioning deserves a little more attention, because it is the lever that determines whether a distributed job is fast or embarrassing, and because the concept transfers even if you never run a cluster. A partition is a slice of the dataset that one worker handles independently. If you partition an incident history by month, then a query about one month touches one slice, and a transformation that operates within a month parallelizes perfectly across however many months you have. If instead you partition arbitrarily and then group by month, every worker holds fragments of every month, and the system must move data across the network until each month is gathered in one place. Same computation, wildly different cost.

The general principle is to partition by the dimension you filter and group on most often, and to keep partitions roughly even in size. Uneven partitions produce a condition called skew, where one worker holds most of the data and every other worker finishes early and waits. Skew is the reason a job that should take two minutes takes forty, and the usual culprit in operational data is a key with one dominant value: one site that generates most of the incidents, one default owner that thousands of unowned assets are assigned to, one category that everything falls into when nobody chose.

Here is the thing worth internalizing. Partitioning, skew, and the cost of moving data between workers are not exotic Spark trivia. They are the same considerations that make a database index useful, the same considerations that make your incident list query fast, and the same considerations that will make an analytical table pleasant or painful to query in two years. Learning them in the distributed setting just makes them impossible to ignore.

That gives you the honest criterion for whether Spark belongs in your deployment. Distributed processing pays for itself when the dataset genuinely does not fit comfortably in one machine's memory, or when the processing time on one machine exceeds the window you have. It costs you a cluster to run, a runtime to manage, a new failure vocabulary to learn, a much harder local development story, and a job that is slower than a simple script for small inputs, because coordination has a fixed overhead.

Let me put a number on the scale, with the caveat that the boundary moves as hardware improves. A single modern machine will happily process tens of millions of rows of tabular data in memory in seconds to minutes. An asset inventory for a large enterprise might be tens of thousands of rows. Two years of incident history for a busy operations team might be a few million rows. None of that is distributed-processing territory. If your pilot's data fits in memory on the machine you already have, a plain in-process transform is not a compromise: it is the correct engineering answer, it is faster, and it is enormously easier to operate.

So why does this chapter cover Spark at all? Three reasons, all of them real field reasons.

First, because your customer may already run it. If their data platform team has a Spark environment, established patterns, and people who know it, then writing your larger transform in their idiom may be the choice that gets your work supported after you leave. Fitting the customer's operating model is a legitimate reason to pick a heavier tool, as long as you say so out loud rather than pretending it was a performance decision.

Second, because pilots grow. The volume that fits in memory today may not in a year if the deployment expands from one site to two hundred. Knowing where that boundary is, and having measured where you sit relative to it, is what lets you answer a capacity question credibly instead of guessing.

Third, because you will be asked. Somebody senior will ask whether the solution is scalable, and they will often mean whether it uses the tools they associate with scale. Your answer should be a measurement and a threshold: here is the current volume, here is how long processing takes, here is the point at which a single machine stops being sufficient, and here is what we would do at that point. That answer builds far more confidence than adopting a cluster you cannot justify.

Now let us design the orchestrated asset refresh for FieldOps Copilot.

Start by naming the tasks. Wait for or fetch the source export for a target date. Validate the records against the contract. Transform and normalize the accepted records. Load them into the read model. Run the batch-level assertions. Publish the refresh, meaning update the freshness marker that the agent reads. And on failure, notify.

Now the dependencies, which is where the design decisions live. Validate depends on extract. Transform depends on validate. Load depends on transform. So far so obvious. The interesting question is where the assertions go. If you run the assertions after the load, then bad data reaches the read model and you detect it afterwards, which means your agent may serve it in the meantime. If you run them before the load, against the transformed set, then a failing assertion prevents publication entirely. I want you to do the second, and the lesson generalizes: put your quality gate before the thing you are trying to protect, not after it.

There is one more subtlety worth designing deliberately. Separate the load from the publish. Load writes the new data into a staging location or a new version. Publish is the small, fast, atomic act of making it the version readers see, and of updating the freshness marker. Splitting those gives you two benefits. A partially loaded dataset is never visible, and rolling back is just repointing to the previous version instead of re-running an ingestion.

Next, decide the retry policy per task. Extract talks to somebody else's system, so it is the most likely to fail transiently: give it a small number of retries with increasing delays. Validate and transform are pure computations over data you already have, so a retry will produce exactly the same failure: give them none, and let them fail fast and loudly. Load is a write, so its retry policy depends entirely on whether you made it idempotent, which you did, so a couple of retries are acceptable. Assertions are deterministic checks: no retries. And the notification task should be configured so that it runs when something upstream failed, which is the one case where you want work to happen precisely because the main path did not.

Now the failure path, which most people underspecify. When validation fails, what happens? Three things must be true. The downstream tasks must not run, which the dependency graph handles. A human must find out, through whatever channel the customer actually watches. And the state of the system must be unambiguous: the previous good data is still published, the freshness marker still reflects the last successful refresh, and therefore the agent already knows to qualify its answers as the data ages. Notice how the pieces we built last chapter compose: because freshness is a first-class value, a failed refresh degrades the system gracefully without any additional logic.

The notification itself deserves thought. An alert that says a task failed is nearly useless. An alert that says which workflow, which date, which task, how many records were involved, the first line of the reason, and where to look is actionable. And there should be an escalation distinction: a validation failure that quarantined twelve records is a working-hours issue, while a workflow that has not successfully published for longer than the freshness tolerance is a call-somebody issue. If everything alerts at the same severity, people stop reading the alerts, and then you have an alerting system that produces noise instead of safety.

Then the backfill. Make the target date an explicit parameter of the workflow, and make every task use it rather than the clock. Your synthetic source generator should be able to produce an export for any date you name, which is why I asked you to keep it. Then rehearse the backfill: pick a historical date, run the workflow for it, and confirm three things. The run completes. The read model ends in the state that date's data implies. And a second run of the same date changes nothing, because idempotency still holds when the input is old.

There is one genuinely hard question in backfilling a read model, and I want you to face it rather than avoid it. A read model normally holds current state. If you backfill an old date after today's data is already loaded, do you want the old data to overwrite the new? Almost always no. So either your backfill targets a separate historical store, or your load rule refuses to overwrite a row with data from an older source revision. The second is usually the right choice, it is a small amount of logic, and it prevents a whole category of accidents where a well-meaning reprocess silently reverts the system to last month.

Finally, the Spark comparison, which is a measurement exercise rather than a coding exercise. Take your transform, run it in process over your pilot-sized inventory, and record the elapsed time and peak memory. Then generate a synthetic batch that is one or two orders of magnitude larger, and run the same transform again. You will learn where the curve bends. Then express the same aggregation in a distributed style and compare, including the startup overhead, which for a small input will often make the distributed version slower by a wide margin. The deliverable is not a Spark job. The deliverable is a written statement: at our measured volume, in-process transformation takes this long, distributed processing is not justified, and the threshold at which we would revisit is this.

There is one question left, and in a customer deployment it is often the most consequential one: who runs the orchestrator, and where does it live?

You have three realistic options. The first is that the customer already operates a workflow platform, and your refresh becomes another workflow in it. This is frequently the best outcome, because it inherits their monitoring, their on-call rotation, their access controls, and their institutional familiarity. The cost is that you must fit their conventions, their deployment process, and their release cadence, and you will need a partner on their platform team.

The second is that you run a workflow platform as part of the deployment. This gives you control and speed during the pilot. It also means you have just added a database, a scheduler process, a worker pool, an interface with its own authentication, and an upgrade obligation to the set of things somebody must operate after you leave. That is a genuine cost and it should be a conscious choice rather than a side effect of following a tutorial.

The third, and the one I would most often recommend for a first pilot, is the boring option: a single scheduled invocation of your job on the platform you already have, with the target date as a parameter, retries handled in your own code, and the run record you already built as your history. If your workflow is one chain of five tasks with no branching and no cross-workflow dependencies, a full orchestrator is a substantial amount of operational machinery to gain a dependency arrow you could have expressed with an early return.

Be honest about the trigger for graduating. You need real orchestration when you have several workflows with dependencies between them, when backfills are routine rather than rare, when different people need to see run history without asking you, or when the number of scheduled things has grown past what anybody can hold in their head. Until then, the simpler thing is not technical debt. It is proportionality, and proportionality is a core field skill. What you must not do is skip the concepts. Retries, idempotency, target-period parameterization, quality gates before publication, bounded waiting, and actionable failure notification are required regardless of which of the three options you choose. The tool is optional. The discipline is not.

Let me cover the pitfalls.

The first is the workflow that reads the clock. It is the root of most orchestration pain. Parameterize the period.

The second is tasks that are too large. A single task that fetches, validates, transforms, and loads gives you one status for four different kinds of failure, and a retry that redoes everything including the expensive part. Split along the boundaries where failure means different things.

The third is tasks that are too small. Thirty tasks for a five-step pipeline gives you a beautiful diagram, slow scheduling, and thirty places to look. The right granularity is one task per meaningfully distinct failure or per meaningfully expensive step.

The fourth is passing large data between tasks through the orchestrator itself. Orchestrators are designed to pass small values: identifiers, counts, paths, dates. Pass a reference to the data, not the data.

The fifth is the sensor without a deadline. It looks like patience and behaves like a hang.

The sixth is retrying a deterministic failure. Watch your logs for the same error three times in a row with delays between them; that is the signature.

The seventh is hidden dependencies between workflows. Two independent schedules where one silently requires the other to have finished first will work for months and then fail on the morning the first one runs slowly. If a dependency exists, declare it.

The eighth is catchup surprising you on deployment day. Set it deliberately.

The ninth, and the most consequential in customer environments, is hammering the source. Your workflow that retries three times, with catchup enabled, across fourteen missed days, can generate a startling amount of load against a system whose owner never agreed to it. Bound concurrency, bound the number of backfill runs in flight, and tell the data owner before you run a large reprocess.

The tenth is adopting a cluster for a pilot because it sounds more serious. It adds cost, operational surface, and a skill dependency, and it makes local development harder, which slows down every future change you need to make in the field.

Now verification. Here is what I want you to be able to demonstrate.

Run the workflow end to end for a target date and show the dependency order was respected, with each task's status and duration visible.

Make validation fail and show that the load and publish tasks were not attempted, that the previously published data is still being served, and that a notification with actionable content was produced.

Retry a transient extract failure and show it recovering without human action, and show the run record reflecting that it took two attempts.

Cause a deterministic failure and show it did not retry.

Run a backfill for a historical date, then run it again, and show the second run changed nothing.

Backfill an old date after a newer load and show that current data was not overwritten.

Show a timing comparison between in-process and distributed processing at two data volumes, with a written threshold.

And finally, show that a run which has not published within the freshness tolerance results in the agent qualifying its asset context, without any extra code, because that behavior already exists from chapter twenty-four.

Your practice handoff is the test in the companion guide. You will express the asset refresh as a dependency graph with the quality gate before publication, implement it in a local Airflow-compatible setup or specify the graph precisely enough that somebody else could build it, set per-task retry policies with written justification, wire a notification and an escalation distinction, perform a controlled backfill, and produce measured evidence for or against distributed processing at your pilot's scale. As always, use synthetic data, and do not point any scheduled workflow at a real customer system.

To recap. Orchestration answers four questions: when work runs, what order it runs in, what happens when it fails, and how you know. Model your workflow as a graph of small, single-purpose tasks with declared dependencies, because the dependency is what makes an unsafe step impossible rather than merely discouraged. Parameterize by target period, never the clock, and reproducibility, retries, and backfills all follow from that one habit. Choose a retry policy per task based on whether the failure is transient and whether the task is safe to repeat. Put the quality gate before the publication step, and separate loading from publishing so that a failure never exposes partial data. Make alerts actionable and distinguish routine failures from urgent ones. And treat distributed processing as a decision you make with measurements: know your volume, know your processing time, know the threshold, and be able to say plainly why a cluster is or is not justified for this customer today.

Next chapter we move from data workflows to the release discipline around the intelligence itself: MLOps, model deployment, managed services, and the release manifest that lets a customer know exactly which configuration produced a recommendation and how to get back to the previous one.
