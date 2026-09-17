# Chapter 3 project — Turn the priority rule into a local intake CLI

**Format:** open-book test. No build steps. The chapter audio taught the method; the route is yours.
**Prerequisite:** chapter 3 audio, the chapter 1 charter, and the chapter 2 specification table.

---

## Goal

An operator can enter an incident on a Linux machine, get a priority and a readable reason back, and leave behind evidence that you can inspect afterwards — with nothing secret written, printed, or logged.

## Starting state

An empty directory. Your chapter 1 charter defines the fields that matter. Your chapter 2 table defines what the rule must produce.

You are pretending to work on a customer's shared machine. Behave accordingly, even if you are on your own laptop: every permission and every log line should be one you could defend to a security reviewer.

## Constraints

1. **From scratch.** No scaffolding tool, no copied project, no framework. An empty directory and your own files.
2. **Python for the program, shell for the task wrapper.** Logic in Python; the shell only orchestrates and reports.
3. **Isolated, pinned dependencies.** No installs into the machine's system-wide Python. Versions recorded, not remembered.
4. **Nothing secret is committed, printed, or logged.** The example configuration file carries the *shape* of values with obviously fake contents.
5. **Malformed input fails loudly.** A clear, actionable message and a nonzero exit status — and the shell wrapper must propagate it.
6. **All input problems reported together**, not one per attempt.
7. **The rule stays pure.** Age is an input. The program, not the rule, decides what "now" means.
8. **Agreement with chapter 2.** Every row of the specification table produces the same number and band in Python as it does in your three earlier implementations.
9. **Logging is a deliberate decision.** You choose what is recorded and you can justify excluding the rest.

## Required artifacts

| Artifact | What it must contain |
| --- | --- |
| Intake program | Self-explaining when run without useful input; validates; applies the rule; prints a result a human can read, including which factors drove it |
| Shell task | Runs the program, captures its output, and exits nonzero when the program does |
| Example configuration | Non-secret, showing the shape of every value the program expects from its environment |
| Run procedure | Five or six lines: prerequisites, setup, how to run, what success looks like, what the common failures mean |
| Permissions and evidence note | Who can read each file your program creates and why that is acceptable; what you saw when you inspected the running process and its output |

## Self-grade rubric

**Pass bar — all seven must be true**

1. **Clean-shell test passes.** In a brand-new terminal with none of your environment, following *only* your written procedure, the program runs and produces a correct result.
2. **Valid record works.** A realistic incident produces a priority, a band, and a reason a coordinator could act on.
3. **Malformed record is refused** with a message naming what is wrong, where, and what an acceptable value looks like — and the process exits nonzero.
4. **The shell task fails when the program fails.** Verify this deliberately; it is the step most people get wrong.
5. **Table agreement.** Every specification row matches your chapter 2 results exactly.
6. **No secret anywhere.** Not in the files, not in the output, not in the logs, not in any history you have started.
7. **Permissions are chosen, not inherited.** You can state the reader of every file you created.

**Quality marks — aim for at least four**

8. Validation reports every problem in the input at once.
9. Results go to standard out and diagnostics go to standard error, so the program is usable in a pipeline.
10. The printed reason names which factors raised and lowered the priority, not just the number.
11. Your log records structured facts and deliberately omits free-text description, or records it only with a written justification for where the log lives and who can read it.
12. Different exit statuses distinguish "the human typed something wrong" from "the program is broken."
13. You inspected the running process and stopped it cleanly, leaving no stray process, file, or held resource.
14. Dependency versions were recorded as you installed them.

**Automatic fail**

- A credential, token, or password appears in any file, output line, or commit.
- The program exits zero after rejecting an incident.
- The shell task reports success when the program failed.
- The Python rule reads the current time internally.
- The Python priority disagrees with chapter 2 on any row.
- Packages were installed system-wide on the machine.

## Stretch

- Make the program accept a record on standard input as well as interactively, so it can be driven by automation, and verify both paths produce identical results.
- Add a batch mode that reads many records and reports how many were accepted and rejected — then run a few hundred and note how the experience changes.
- Write the three sentences you would send to a platform lead describing what your program writes to disk, where, and who can read it.

## Verification you can run today

- Clean shell, new session, documentation only. Everything that fails is a documentation defect.
- Run the full specification table and diff against chapter 2's output.
- Feed it garbage: empty input, missing fields, a severity that does not exist, an impossible age, a description of ten thousand characters.
- Search the whole project — including history — for anything resembling a secret.
- Start it, find the process, stop it politely, confirm nothing remains.

---

<!-- tts:skip -->
## If stuck — inverted hints

Last on purpose, and absent from the audio. One at a time, in order, after a genuine attempt.

1. Cannot start? Write the run procedure first, before any code. It tells you what the program has to be.
2. Unsure what the program should ask for? Open your charter. The fields you promised to collect are already written down.
3. Rule wants the current time? The rule needs an age, not a clock. Which part of your program knows both when the incident arrived and what time it is now?
4. Validation feels tangled with the logic? Ask which of your functions would still make sense if the input arrived from a web form instead of a keyboard. That boundary is where validation belongs.
5. Error messages feel unhelpful? Read one out loud as if you were the operator at three in the morning. Does it tell you what to type next?
6. Shell task reports success on failure? Investigate what a chain of commands does with a failed step in the middle, and what your script's exit status actually is.
7. Unsure what to log? Ask what you would need to answer the question "what did this program decide, and when?" a month from now — then ask which of those fields you would be uncomfortable showing a security reviewer.
8. Unsure about permissions? For each file, name the account that must read it. Anything broader than that list needs a reason.
9. Clean-shell test failing on a step you forgot? That is not a nuisance, that is the whole point of the test. Add it to the procedure and run the test again from scratch.
10. Table disagreement you cannot find? Compare band boundaries and rounding before anything else — they cause most cross-language mismatches.
<!-- /tts:skip -->
