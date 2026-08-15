# Workflow graph, persistence, and approval notes

Chapters 11–12 model a book-maintenance proposal as explicit graph state, not
as a loop of free-form model calls. The state stores objective, retrieved paths,
plan, critique, model/fallback status, approval decision, and terminal status.
The graph contains no node that writes prose, code, Git state, or external
services.

LangGraph persistence stores a checkpoint at graph super-step boundaries and
uses a `thread_id` to identify a resumable sequence. An `interrupt()` pauses the
approval node; resuming the same thread with `Command(resume=...)` supplies the
human response [@langgraph2026persistence; @langgraph2026interrupts]. The
project uses the separate SQLite checkpointer package for a local durable demo.
Its database lives below `.book-intelligence/` and is ignored.

The initial test revealed an operational detail worth preserving: the sync graph
can write checkpoints from a worker thread. A Python SQLite connection created
with its default thread guard then fails. Opening it with
`check_same_thread=False` lets LangGraph’s internally synchronized SQLite saver
use that connection. This is a local integration fix, not a claim that one
connection setup fits a multi-process production deployment.

The deterministic plan node is intentionally the fallback when a model is
unavailable or evidence is absent. That makes fallback behavior testable without
an API key and prevents an unavailable model from becoming permission to skip
the approval boundary.
