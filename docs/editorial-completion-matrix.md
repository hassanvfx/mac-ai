# Editorial completion matrix

This is the working acceptance record for the canonical manuscript in
`book/chapters/`. The automated audit verifies baseline sections, citation-key
validity, and local links. This matrix records the human editorial work that a
structural check cannot prove: explanatory depth, evidence scope, runnable
companion material, and diagrams worth keeping in the print book.

Status is deliberately conservative. **Draft expanded** means a chapter has
been developed beyond its initial outline; it does not mean copyedited, print
ready, or final. A performance, memory, or framework claim is publishable only
when its linked record states the machine, versions, workload, method, and
limitation.

| Chapter | Current state | Runnable/evidence anchor | Needed before beta manuscript gate | Visual needed |
| --- | --- | --- | --- | --- |
| 00 Introduction | Draft expanded | `README.md`, setup commands | Fourth-pass installation walkthrough, final copyedit, source-of-truth visual | Repository source-of-truth map |
| 01 Tensors | Third-pass draft | `experiments/01-tensors/broadcasting.py` | Fourth-pass case studies, copyedit, full DOCX review | Complete: broadcasting diagram |
| 02 Gradients | Third-pass draft | `experiments/02-gradients/autograd.py`, Day 1 record | Fourth-pass worked update case, copyedit, full DOCX review | Complete: gradient-flow diagram |
| 03 PyTorch | Third-pass draft | `experiments/03-pytorch/train_tiny_network.py`, `benchmarks/01-day1/` | Fourth-pass validation-transition case, copyedit, full DOCX review | Complete: training-loop diagram |
| 04 Framework comparison | Third-pass draft | `experiments/04-tensorflow/train_keras_cnn.py`, `benchmarks/02-vision/` | Fourth-pass measured comparison case, copyedit, full DOCX review | Complete: matched pipeline comparison |
| 05 Vision | Third-pass draft | `experiments/05-vision/train_pytorch_cnn.py`, `benchmarks/02-vision/` | Fourth-pass error-analysis case, copyedit, full DOCX review | Complete: CNN feature-map flow |
| 06 Transformers | Third-pass draft | `experiments/06-transformers/inspect_sentiment.py`, `research/03-transformers/` | Fourth-pass inference case, copyedit, full DOCX review | Complete: tokenization and attention flow |
| 07 Apple Silicon | Third-pass draft | `experiments/07-mlx/run_local_model.py`, `benchmarks/04-mlx/` | Fourth-pass workload/capacity case, copyedit, full DOCX review | Unified-memory and inference path |
| 08 Embeddings | Third-pass draft | `experiments/08-embeddings/book_search.py`, `research/05-embeddings-and-rag/` | Fourth-pass retrieval evaluation case, copyedit, full DOCX review | Embedding-space/query flow |
| 09 RAG | Third-pass draft | `experiments/09-rag/grounded_answer.py`, `benchmarks/05-book-intelligence/` | Fourth-pass grounded-answer case, copyedit, full DOCX review | Retrieval-to-cited-answer flow |
| 10 AI systems | Third-pass draft | `experiments/10-systems/compare_structured_planning.py`, `benchmarks/06-structured-systems/` | Fourth-pass adapter comparison case, copyedit, full DOCX review | Evidence → plan → critic flow |
| 11 State machines | Third-pass draft | `experiments/11-langgraph/approval_workflow.py`, `benchmarks/07-workflow-graphs/` | Fourth-pass state trace case, copyedit, full DOCX review | Graph state-transition diagram |
| 12 Human control | Third-pass draft | `experiments/11-langgraph/approval_workflow.py`, `benchmarks/07-workflow-graphs/` | Fourth-pass approval/rejection case, copyedit, full DOCX review | Approval interrupt sequence |
| 13 Agent shapes | Third-pass draft | `experiments/13-workflows/compare_workflows.py`, `benchmarks/08-workflow-comparison/` | Fourth-pass comparison case, copyedit, full DOCX review | Complete: workflow-shape diagram |
| 14 Reliability | Third-pass draft | `evals/run_reliability.py`, `tests/test_reliability.py` | Fourth-pass release-gate case, copyedit, full DOCX review | Reliability/evaluation feedback loop |

## Per-chapter beta exit criteria

For every chapter, confirm all of the following during the final technical edit:

1. The chapter has intuition, problem, minimal and real implementation,
   experiment, failure analysis, alternatives, usage guidance, and takeaway.
2. Every code command resolves to a tracked runnable file and states required
   optional dependency groups when applicable.
3. Every research citation uses a key present in `research/references.bib`; each
   non-trivial performance or behavior claim links to a committed record or a
   source that supports it.
4. The chapter links to the relevant research note, experiment, and benchmark
   or evaluation record without duplicating raw code in print.
5. Examples use consistent vocabulary: *observation* for a measured result,
   *claim* for an interpretation, *fixture* for frozen test material, and
   *approval boundary* for a deliberate stop before a write or external action.
6. A diagram is added only when it explains a relationship that prose and a
   short code listing cannot make equally clear. Its editable, print-quality
   source remains under `book/assets/`.
7. The chapter is read in the generated DOCX after major expansion so headings,
   code listings, tables, and images are suitable for a 6×9 layout.

## Manuscript-wide gates

- `make audit-book` passes; word count is 45,000–55,000 before final layout
  work begins.
- Python tests, lint, site build, and relevant optional dependency groups pass
  from a clean environment.
- Every benchmark/result used in prose has a scope and limitation statement.
- A regenerated DOCX is rendered and inspected after the editorial pass; the
  Word-exported PDF, PDF preflight, and Lulu proof remain separate production
  gates.
