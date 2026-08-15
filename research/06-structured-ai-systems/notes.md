# Structured planning and adapter comparison notes

Chapter 10 compares two ways to ask an optional remote model for a plan or
review: the official OpenAI Python SDK directly, and LangChain’s `ChatOpenAI`
integration. The comparison intentionally fixes the retrieved `Evidence`
objects before either adapter receives a prompt. The adapters may format model
interaction differently, but neither is allowed to add a source path that was
not retrieved.

Both structured schemas use Pydantic. Their validation policy is stricter than
schema parsing alone: unsupported paths are removed and recorded as warnings;
an empty evidence set clears implementation steps; and `approval_required` is
forced to true. This makes a successfully parsed object a proposal, not an
authorized change.

The direct route uses the SDK's parsed structured response mechanism. The
LangChain route uses `with_structured_output(..., include_raw=True)` so parsing
failures are observable. Current LangChain documentation describes native JSON
schema support for OpenAI models and notes that `ChatOpenAI` targets official
OpenAI API specifications [@langchain2026chatopenai]. This repository keeps a
generic OpenAI-compatible endpoint option for controlled experiments, but it
does not claim that every compatible service supports every structured-output
mode.

No API key is stored in the repository. The adapter reads
`BOOK_INTELLIGENCE_API_KEY`, `BOOK_INTELLIGENCE_API_BASE`, and
`BOOK_INTELLIGENCE_MODEL` only when an API run is deliberately requested. A
missing value fails before a network call.
