# Test 20 — Ground the agent in customer runbooks

**Chapter:** 20 — Memory, RAG, and vector databases
**Format:** This is a test, not a tutorial. Hints are inverted at the end; read them only after a real attempt.
**Prerequisite state:** FieldOps Copilot at the end of chapter 19 — explicit triage state machine, durable approval gate, four stop conditions, read-only lookup tool with per-call authorization.

---

## Goal

Ground the triage proposal in the customer's own procedures, such that **every grounded recommendation either points to a real retrieved passage or declines** — and retrieval provably never crosses a tenant boundary.

---

## Constraints

- The tenant filter is applied **inside the query** (or by physical separation), never by post-filtering retrieved results.
- Role/sensitivity filtering is driven by the **operator's** identity, not the service's.
- Workflow state is not confused with knowledge. **No learned memory** is introduced in this pilot; record that decision and why.
- The index is a **derived** store. The document repository is the source of truth, and the index must be rebuildable from scratch.
- Retrieved passages enter the **single delimited data region**, never the instruction region.
- Citations are validated against what was actually retrieved.
- Weak retrieval produces insufficient evidence, not a guess.
- Synthetic runbooks only. No real customer documents.

---

## Starting state you must not break

- Offline test suite green with no credentials.
- Chapter 18 cross-tenant tool refusal still passes.
- Chapter 19 stop conditions still terminate cleanly.
- Priority remains deterministic.

---

## Required artifacts

### A. Synthetic corpus across at least two tenants

Each document carries: tenant, access level/role, owner, revision date, source identifier, and a link back to the original.

Include deliberately: one document last revised years ago, two documents that describe the same procedure differently, and — in **tenant B** — a document containing a distinctive phrase that appears nowhere else (your adversarial canary).

### B. Chunking strategy

- Respects procedure boundaries. A chunk must never instruct step four without the context of steps one to three.
- Preserves the heading path inside the chunk text so a chunk is interpretable alone.
- Written down with the reasoning, and the chunk-size decision justified against your corpus rather than copied from a default.

### C. Index with metadata

- Metadata designed **before** indexing (retrofitting means reindexing — that is part of the lesson).
- Embedding model identifier recorded per vector.
- A documented rebuild path, exercised at least once.

### D. Filtered hybrid retrieval

- Tenant and role filters applied in the query or by separate namespaces.
- Semantic **and** keyword search, combined. Operational text is full of error codes and identifiers that vector search handles badly.
- A focused query constructed from structured fields rather than the raw description.
- Small result count (around five reaching the prompt).

### E. Grounding and citation

- Passages supplied with identifiers in the delimited data region.
- Citation required by the output schema.
- Citation **validated**: a cited identifier that was not retrieved is a rejected response, counted and logged.
- A calibrated insufficient-evidence threshold, with the calibration recorded (score distribution for answerable vs unanswerable fixtures).

### F. Freshness demonstrations

1. Update a runbook, reindex, and show the old passage no longer appears.
2. Delete a runbook and show its vectors are gone.
3. Show the revision date reaching the operator alongside the citation.
4. A written staleness policy, agreed as if with the customer.

### G. Retrieval evaluation set

Queries with known-correct source passages, and a recorded **recall** figure. This is your ceiling.

---

## Rubric

| Criterion | Fails | Meets | Strong |
|---|---|---|---|
| **Tenant isolation** | Post-filtering | Filter in query or separate namespaces | Adversarial canary test is automated and runs on every change |
| **Chunking** | Fixed split, procedures severed | Structural, heading context preserved | A randomly chosen chunk is interpretable cold |
| **Metadata** | Added later | Designed before indexing, drives filter/citation/freshness | Rebuild from source exercised and timed |
| **Retrieval quality** | Vector only | Hybrid semantic + keyword | Reranking applied, and the improvement measured on your eval set |
| **Citation integrity** | Citations trusted | Validated against retrieved set | Fabricated citation rejected by a test |
| **Honest declining** | Answers anyway | Insufficient evidence below threshold | Threshold calibrated on your own corpus with the data recorded |
| **Freshness** | No reindex path | Update and delete both demonstrated | Revision date surfaced; staleness policy written |
| **Separation of concerns** | Index treated as a source of truth | Index derived and rebuildable | Deleting the index costs time, not data |
| **Measurement** | Recall unknown | Recall recorded | Retrieval eval runs in seconds with no model, and is used before touching prompts |

---

## Self-verification before you call it done

1. Run the adversarial cross-tenant query: as a tenant A operator, submit an incident engineered to make tenant B's canary phrase maximally relevant. Nothing comes back. The attempt is logged. This is an automated test.
2. Pick a retrieved chunk at random and read it cold. If you cannot tell what procedure it belongs to, fix chunking — not the prompt.
3. Force retrieval below threshold. The system declines and names what it looked for.
4. Inject a fabricated citation into a test response. Validation rejects it.
5. Update, reindex, verify. Delete, verify. Both.
6. Run retrieval evaluation and write the recall number in your notes. Any prompt work done before this number exists is work done below the ceiling.
7. Delete the entire index and rebuild it from source. Nothing is lost.

---

## Stretch (optional)

- Profile the customer corpus problem: count documents, plot last-revised dates, and compute the fraction referencing systems still in the service catalogue. Write the one-slide finding.
- Add an operator control to flag a cited passage as wrong, routed to the document owner.
- Add an index-time flag for passages containing instruction-shaped language, and record how many the synthetic corpus trips.
- Compare recall with and without keyword search on queries containing error codes. Record the delta — it is usually large.

---

## Common ways this goes wrong

- Post-filtering for tenancy. This is an incident, not a defect.
- Chunks that sever procedures, producing operationally dangerous fragments.
- Metadata designed after indexing.
- Pure vector search on text full of identifiers and error codes.
- Citations trusted without validating they were retrieved.
- No deletion path, leaving orphaned vectors that surface "deleted" content.
- Embedding model changed without a planned reindex.
- Days spent rewriting prompts to fix what was a retrieval failure all along.

---

<details>
<summary>Hints — read only after attempting</summary>

**Hint 5 (last resort).** If you can only do one thing well in this test, make it the adversarial tenant test. Everything else is quality; that one is safety.

**Hint 4.** Physical separation (a namespace or collection per tenant) removes a whole class of bug compared to a filter. Prefer it where your store allows it — absence of capability beats restriction of capability, same as chapter 18.

**Hint 3.** Calibrate the threshold empirically: run your answerable and unanswerable fixtures, plot the top score for each, and put the cutoff where the two populations separate. There is no good universal number.

**Hint 2.** Build the retrieval evaluation *first*, before the generation path. It needs no model, runs in seconds, and it tells you whether anything downstream can possibly work.

**Hint 1.** If retrieval quality is poor, check in this order: is the query sensible, is keyword search present, is chunking severing context, is the metadata filter over-restricting. Reach for prompt changes last — they cannot reference a passage that was never supplied.

</details>
