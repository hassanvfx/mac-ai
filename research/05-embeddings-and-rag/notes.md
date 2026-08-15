# Embeddings and grounded retrieval notes

Chapters 8–9 use the repository itself as a small, inspectable corpus. The
implementation keeps a deterministic hashed-vector baseline for fast fixtures
and adds an optional learned local encoder, `sentence-transformers/all-MiniLM-L6-v2`,
for the live corpus. Both paths retain the same `Evidence` record: repository
path, corpus kind, chapter identifier when applicable, citation keys found in
the chunk, and lightweight experiment/benchmark grouping metadata.

The learned path encodes chunks and queries locally, L2-normalizes the vectors,
and ranks their dot products (cosine similarity after normalization). It emits
retrieved excerpts and paths only; it does not ask a language model to write an
answer. A score threshold is a conservative retrieval guard, not proof that
the returned excerpt answers the question.

The sentence-transformer approach follows the siamese BERT formulation in
[@reimers2019sentencebert]. The model identifier is a dependency choice, not a
claim that this compact model is universally best. Model weights download to a
developer-local Hugging Face cache and must not be committed.

Useful failure cases to retain in tests and prose:

- an empty corpus must produce an explicit missing-evidence response;
- weak neighbors must not be presented as an answer;
- chunk-level citations do not establish that every sentence in a chunk is
  supported by that citation;
- a source path is evidence only if it resolves within the checked-out corpus.
