# Milestone 3 Transformer inference record

## Contract

The Chapter 6 experiment loads the public
`distilbert/distilbert-base-uncased-finetuned-sst-2-english` sequence
classifier at revision `714eb0fa89d2f80546fda750413ed43d93601a13`. It is a
small, fixed binary-sentiment demonstration chosen to make tokenization and
classification observable. It is not a sentiment benchmark, a safety test, or
a general language-model evaluation.

| Field | Value |
| --- | --- |
| Script | `experiments/06-transformers/inspect_sentiment.py` |
| Dependency group | `transformers` (`transformers` 5.15.0) |
| Runtime | Python 3.11.9; PyTorch 2.13.0 |
| Inputs | Two fixed English sentences: one clearly favorable, one clearly unfavorable |
| Tokenizer | The model's cached tokenizer; max length 64; truncation enabled |
| Direct path | `AutoTokenizer` → tensors/attention mask → `AutoModelForSequenceClassification` → logits → softmax |
| High-level path | `pipeline("text-classification")` with the same loaded model/tokenizer/device |
| Correctness check | Direct and pipeline top labels and scores agree for every fixed input |
| Download/cache | First use downloaded a local Hugging Face cache of approximately 256 MiB, outside this repository and Git |

## Recorded runs — 2026-08-14

The model was loaded before timing. Each elapsed value covers one manual,
two-sentence forward pass including tokenization and MPS synchronization when
applicable; it excludes model download, initial loading, and pipeline calls.

| Requested device | Selected device | Manual result vs pipeline | Manual elapsed time |
| --- | --- | --- | --- |
| `auto` | MPS | Same top label and score for both inputs | 380.206 ms |
| `cpu` | CPU | Same top label and score for both inputs | 120.787 ms |

The favorable sentence produced `POSITIVE` with score `0.999802`; the
unfavorable sentence produced `NEGATIVE` with score `0.999689`. The recorded
token sequences include `[CLS]`, ordinary WordPiece tokens, punctuation, and
`[SEP]`; their lengths were 10 and 11 respectively.

## Interpretation and limitations

The two interfaces agree for this declared model, revision, inputs, maximum
length, and device. That is evidence that the direct inspection and pipeline
are wired equivalently in this run. It is not evidence of classification
accuracy beyond two hand-selected examples.

The timing table is **not** an MPS-versus-CPU benchmark. It uses one tiny,
one-off workload, has no shared warmup or repeated samples, and includes very
different overhead proportions on the two devices. Its only purpose is to
record the actual observation and prevent a plausible-but-unsupported Apple
Silicon performance claim. A later benchmark must define repeated warmups,
sequence lengths, batch behavior, model loading, timing boundaries, and memory
sampling before comparing devices or frameworks.

The cache size is a local observation after downloading this one model, not a
general storage estimate for Transformer models. Check disk space before adding
models; the cache lives outside the project and is not committed.
