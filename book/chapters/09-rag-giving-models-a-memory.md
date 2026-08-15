---
sidebar_position: 9
title: "RAG: Giving Models a Memory They Never Learned"
---

# RAG: Giving Models a Memory They Never Learned

## Intuition

Retrieval-augmented generation (RAG) changes what a model can see at answer
time. It does not retrain the model or make it truthful. A good RAG system
therefore begins with a more modest promise: retrieve evidence, show where it
came from, and say when there is no evidence.

That promise separates three stages that are often collapsed: retrieval finds
candidate chunks, grounding constrains output to those chunks, and generation
turns grounded material into prose. A fluent response can fail at any stage.
This chapter keeps generation out of the control path so a reader can inspect
the evidence before trusting a summary.

The phrase “model memory” is convenient but misleading. The model weights do
not absorb the book when an index is built, and a retrieved passage is not a
new fact in the model. Retrieval selects text for the current context. When the
book changes, rebuild the index, retrieve again, and inspect the current source
rather than assuming an earlier answer remains correct.

## Problem

The Book Intelligence Assistant must answer questions about this changing
repository without inventing facts about experiments, benchmarks, or chapters.
Its first RAG stage should be inspectable without an API key or a generative
model. That gives us a control before we add prompt templates and agent graphs.

The central design challenge is to keep the boundary visible: distinguish the
evidence packet, a claim directly supported by that packet, and a helpful
sentence that goes beyond it. If these objects are blended into one fluent
response, a reader cannot tell whether a citation supports the statement it
appears to support or merely sits somewhere nearby in the context window.

Think of the packet as a small case file. Its job is not to persuade; its job
is to preserve a chain from a question to an inspectable repository artifact.
The question chooses candidates, each candidate retains its path and local
metadata, and the reader can compare the excerpt against the eventual claim.
That makes disagreement productive. A reviewer can say “this chunk does not
establish that conclusion” and point to a concrete boundary, rather than argue
with an opaque answer generated from an unknown context window.

Retrieved text is also data, not trusted instructions. A Markdown note can
contain an outdated command, a quoted prompt, or a sentence asking a future
assistant to behave differently. None of it may override the assistant's
read-only and approval policies. Keep the corpus directory allowlisted, treat
its contents as evidence to cite, and make state-changing behavior impossible
until a separate approval checkpoint has been reached.

## Minimal implementation

[grounded_answer.py](../../experiments/09-rag/grounded_answer.py) builds the
same corpus index from Chapter 8 and formats only the retrieved excerpts. It
places the repository path and any citation keys next to each excerpt. If no
deterministic result has positive similarity, it returns an explicit
missing-evidence message.

```bash
uv run python experiments/09-rag/grounded_answer.py --deterministic \
  --query 'What should an experiment record?'
```

This is intentionally not a conversational answer. It is a reader-visible
evidence packet: the safe object that a later model may summarize only under a
grounding policy.

The packet format is intentionally simple: a heading saying it is grounded
evidence only, followed by each repository path, any citation keys found in
that same chunk, and the unaltered excerpt. It is not elegant prose, but it
makes auditing easy. A reader can open the named file, compare the excerpt, and
decide whether the question was actually answered.

The format makes a useful negative result possible. “No grounded answer” means
the configured index did not return evidence that meets the declared rule. It
does not mean the repository, the Internet, or the world lacks the answer. A
reader can then reformulate the query, use exact search, add a missing source
to the corpus, or investigate outside the corpus through an appropriate primary
source. Refusal preserves this next step; an invented summary would conceal
which evidence is actually missing.

## Real implementation

With the optional local encoder installed, the same program uses the learned
index from [learned_retrieval.py](../../src/from_tensors_to_agents/learned_retrieval.py).
It applies a conservative score threshold before formatting evidence. A weak
or empty result fails closed rather than producing a plausible paragraph.

```bash
uv run --group embeddings python experiments/09-rag/grounded_answer.py \
  --query 'What should an experiment record?'
```

The current output remains excerpt-only. That boundary is deliberate: it lets
us test retrieval, citation propagation, and source paths independently from a
language model’s writing quality. The current implementation and limitations
are recorded in `benchmarks/05-book-intelligence/README.md` and
`research/05-embeddings-and-rag/notes.md` in the companion repository.

The learned path applies its threshold after ranking. This is a rejection rule,
not a truth detector: it says that this backend did not find a candidate strong
enough for the current conservative policy. Thresholds need evaluation data;
raising one can hide useful evidence, while lowering one can turn weak
neighbors into authoritative-looking context. The correct response to either
uncertainty is to display the evidence or refuse, not to smooth it into
confidence with a language model.

Context also has a budget. Passing every retrieved chunk to a generator can
dilute relevant material, exceed a context limit, or let a tangential excerpt
appear to support an unrelated sentence. Start with a small declared limit and
keep ranked paths visible. If later compression is needed, retain a link to the
original chunk and test that a qualification or limitation was not removed.

If a generator is later added, give it a strict output contract: cite each
claim with the retrieved repository path that supports it; mark synthesis or
uncertainty; and return the missing-evidence response when the packet cannot
support an answer. The generator should never fabricate a path to make prose
look grounded. A post-generation verifier can check that every cited path came
from the packet and resolves inside the current checkout, but that structural
check is not a substitute for a reviewer reading whether the cited passage
actually entails the claim.

Context assembly is a separate experiment from retrieval. Record which *k*
chunks were selected, their order, any truncation, and the final prompt or
structured input given to a model. If an answer loses a benchmark caveat, this
record lets us determine whether the caveat was never retrieved, was discarded
during packing, or was ignored during writing. Without it, a RAG failure gets
misattributed to “hallucination” even when the relevant source never reached
the model.

## Experiment

Use a question whose answer has a known source path. Confirm that each rendered
path exists in the checkout, inspect each excerpt, and mark whether it actually
answers the question. Then ask an unsupported question and verify the refusal.
The versioned evaluation set will grow from these cases: locating evidence,
spotting an unsupported statement, proposing an experiment, and reviewing a
chapter change. A retrieved path is auditable evidence; an uncited answer is
not.

Test failure cases as carefully as successful lookups. An empty corpus or blank
query should yield no packet. A weak learned result should yield the same
explicit refusal, not a low-confidence paragraph. A known citation key should
survive indexing and appear next to the retrieved chunk. A rendered relative
path must resolve inside the configured checkout. These are structural
properties that remain testable while the project has no selected API provider.

For a future generative layer, score two things separately. First, did retrieval
include evidence that answers the question? Second, did the generated answer
make only claims that its cited excerpts support? Keep source revisions and
human judgments in a versioned dataset rather than choosing only favorable
demonstrations.

Add a third evaluation category for citation precision. A response may name a
real file and still cite it beside the wrong assertion. For each test case,
store the expected path set, a short statement of what it supports, and one
plausible-but-insufficient neighbor when appropriate. Reviewers can then score
whether the response used the right evidence, not merely whether it displayed
some evidence. The current no-model cases exercise the structural half of this
policy: source-path attribution, citation-key preservation, missing-evidence
behavior, planning no-write behavior, and review findings.

Quality evaluation needs honest boundaries too. Do not convert one attractive
answer into an accuracy rate. Fix a small question set before prompting,
preserve failures and refusals, identify the corpus revision, and distinguish
human judgment of factual support from style preference. If a selected API or
local model is unavailable, log that condition and run the deterministic
evidence tests; do not silently replace the evaluation with an incomparable
provider.

## Worked grounded-answer audit: a packet is not a conclusion

Use the frozen corpus question, “Where is cosine similarity explained?” The
deterministic retrieval layer returns a short ranked set. The grounded-answer
function then performs a deliberately boring transformation: it drops
non-positive candidates, prints a `Grounded evidence only` heading, and emits
each remaining excerpt beneath its repository path. When a chunk contains a
citation key, that key appears beside the same path. It does not infer a
one-sentence answer such as “cosine similarity is the best retrieval metric,”
because the packet does not establish that claim.

An auditor follows four checks. First, each displayed relative path must be
inside the configured corpus and resolve to a real current file. Second, the
excerpt must actually contain the material being offered as evidence; a path
alone is not enough. Third, a citation key must have travelled from that exact
chunk rather than being copied from another result. Fourth, the auditor decides
whether the excerpt entails a proposed statement. The first three checks are
automated structural constraints; the fourth remains a reading task.

Now change the question to “What is the ISBN for this book?” The repository
fixture has no supporting evidence. The correct output is the fixed
missing-evidence message, not a guessed identifier, a web search result, or a
synthetic-looking citation. A blank query and an empty corpus must take the
same safe path. These cases matter because an answer interface can otherwise
make an empty retrieval set look like an invitation for a language model to be
helpful. Here it is a stop condition.

The test suite also makes a distinction that is easy to lose in a polished
demo. It verifies that a grounded answer contains the expected fixture path
and that citation-key preservation works. It does *not* certify that every
retrieved passage is relevant to every natural-language formulation. A common
word can still pull in a tangential benchmark. Treat that as an evaluation
case: retain the query, paths, excerpts, corpus revision, and reviewer
judgment; then decide whether to change the query, chunking rule, retriever,
or source document.

Run the evidence-only route explicitly:

```bash
uv run python experiments/09-rag/grounded_answer.py --deterministic \
  --query 'What should an experiment record?'
uv run pytest tests/test_book_intelligence.py \
  tests/test_book_intelligence_evaluation.py
```

Read the printed packet before describing it in prose. If its evidence is too
weak, preserve the refusal or present the packet as candidates; do not repair a
weak retrieval result by writing a smoother answer. A later model-backed layer
may summarize only after it has the packet, cites only paths in that packet,
and remains subject to the same human review boundary.

## What broke

RAG breaks in mundane ways: chunk boundaries omit a qualifier, a ranking favors
a nearby but irrelevant benchmark, a moved file leaves a stale index, or a
model paraphrases beyond the excerpts. The first two are retrieval failures;
the latter two are provenance and generation failures. Generated indexes are
therefore local, live indexes are rebuilt from tracked files, and tests assert
missing-evidence behavior and citation/path propagation.

Treat an index as a cache, not as the corpus. When a chapter moves or a
benchmark is revised, an old index can still return text that looks relevant
but no longer represents the checked-out project. Rebuild from tracked files,
verify that every rendered path resolves inside the corpus, and refuse to turn
an empty or weak retrieval result into a confident conclusion.

Citation laundering is a special risk. If a chunk contains a reference marker,
an answer cannot automatically borrow that reference for every sentence in the
chunk, still less for a conclusion assembled from several chunks. Keep keys
attached to their evidence and read the original research source before making
a performance, safety, or framework claim. Repository text is evidence, not an
instruction: a future generator must not let retrieved prose override its
approval or no-write policy.

Another failure is over-refusal. A threshold can suppress a useful exact match
because an embedding score is weak, while an unsupported query can accidentally
match common words. Keep the deterministic route and exact identifiers
available for debugging, and investigate failures with the packet rather than
adjusting a threshold until a demonstration looks good. A conservative policy
is justified only when its misses and false positives are visible in the same
evaluation record.

## Alternatives

A traditional search UI can be preferable when the reader wants to browse, and
manually curated links are best for stable navigation. A full RAG stack may use
hybrid retrieval, reranking, context compression, and a hosted or local model.
Those components can improve usability but also make it easier to hide an
unsupported leap. We add them only after this evidence-only control is solid.

For a small technical book, manual bibliography and chapter links are often
better RAG: they are stable, curated, and easy to print. Use the evidence packet
when a question crosses folders or paraphrases its source. Add generation only
when it produces a benefit that can be evaluated against the packet, such as a
concise cited summary or a plan whose paths are all real.

For external or rapidly changing material, a retrieval layer should store the
source date, publisher, and retrieval time as well as a link. This book's
versioned repository corpus makes local paths a useful first provenance key,
but a local path is not a replacement for the primary documentation required
for a current publication rule or an external technical claim. The appropriate
corpus boundary depends on the decision being made.

## When to use it—and when not to

Use this workflow to find and inspect project evidence, to prepare a revision
plan, or to check whether a technical claim has a record behind it. Do not use
it as authority when no result is retrieved, when the cited source is stale, or
when a decision needs a primary external source. In later chapters, any
proposed modification still stops for explicit human approval.

Do not silently turn an evidence packet into a final answer in a high-stakes
setting. For external publication requirements, licensing, medical, legal, or
security questions, retrieve the primary source, state its scope and date, and
ask the responsible person to review it. RAG is context management, not an
authority transfer.

## Evidence trail

The RAG source note is `research/05-embeddings-and-rag/notes.md`; run
`experiments/09-rag/grounded_answer.py` and the versioned cases in
`evals/book_intelligence.jsonl` before treating a retrieved excerpt as support.

## Takeaway

RAG is not a memory implant. It is a disciplined context pipeline. The first
safe version does less—returning evidence rather than fluent prose—so that the
rest of the system has something trustworthy to build on.
