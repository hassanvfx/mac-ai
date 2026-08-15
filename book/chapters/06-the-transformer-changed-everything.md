---
sidebar_position: 6
title: The Transformer Changed Everything
---

# The Transformer Changed Everything

## Intuition

Attention lets each token select useful context rather than receiving a fixed
summary of a sequence. Self-attention compares each token with other tokens in
the same sequence, then mixes their value representations according to those
comparisons. Stacking that operation lets a Transformer form context-dependent
representations without a recurrent step-by-step state [@vaswani2017attention].

That description can sound abstract until we inspect the actual inputs. A
pretrained Transformer does not receive words directly. It receives token IDs,
special boundary markers, and an attention mask; it returns scores whose
meaning comes from the model's trained label mapping.

## Problem

Move from tokenization to a pretrained model inference path we can inspect. We
will classify two fixed sentences with a compact binary sentiment model. This
is a demonstration of the mechanics of pretrained inference, not proof that a
model understands sentiment, evaluates quality, or makes a trustworthy
recommendation.

## Minimal implementation

Install the optional dependency group and run the complete inspection:

```bash
uv sync --group transformers
uv run --group transformers python experiments/06-transformers/inspect_sentiment.py --device auto
```

The script loads
`distilbert/distilbert-base-uncased-finetuned-sst-2-english` at its recorded
revision. For the sentence `This small experiment is clear and useful.`, its
WordPiece tokenizer emits:

```text
[CLS] this small experiment is clear and useful . [SEP]
```

The corresponding integer IDs and all-ones attention mask are printed by the
script. `[CLS]` and `[SEP]` delimit the sequence for this model family; they
are not words from the sentence. An attention mask marks which positions are
real input rather than padding when a batch contains sequences of unequal
length.

## Real implementation: reveal the path hidden by a convenience API

The manual path in `experiments/06-transformers/inspect_sentiment.py` is:

```text
text → tokenizer → input IDs + attention mask → model logits → softmax → labels
```

It uses `AutoTokenizer` and `AutoModelForSequenceClassification`, moves tensors
and the model to MPS when available (otherwise CPU), runs under
`torch.inference_mode()`, and applies softmax explicitly. The high-level
`pipeline("text-classification")` path then uses the same model, tokenizer,
device, inputs, and maximum length. Transformers provides both styles because
one optimizes inspection and the other reduces application boilerplate
[@wolf2020transformers; @huggingface2026transformers].

## Experiment

The recorded run used Python 3.11.9, PyTorch 2.13.0, Transformers 5.15.0, a
maximum sequence length of 64, and model revision
`714eb0fa89d2f80546fda750413ed43d93601a13`. On MPS, the first sentence was
classified `POSITIVE` at `0.999802` and the second, explicitly unfavorable
sentence was classified `NEGATIVE` at `0.999689`. The direct path and pipeline
matched in top label and score for both fixed inputs. CPU produced the same
two results. See `benchmarks/03-transformers/README.md` for the full record.

The direct two-sentence pass took 380.206 ms in the recorded MPS run and
120.787 ms on the recorded CPU run. This surprising-looking pair is not a speed
comparison: it is a single tiny workload without repeated warmups or equal
overhead boundaries. It is included precisely to demonstrate why a number
without a benchmark design should not become a hardware claim.

## What broke

The first practical surprise is storage. Loading a pretrained model downloads
and caches files outside the repository; this particular cache occupied about
256 MiB after the run, but model sizes vary enormously. Check disk space before
selecting a model and never commit the cache.

The second surprise is that a label is not an explanation. The fixed favorable
and unfavorable sentences were selected to make the control flow easy to read,
not to evaluate the model. Inputs near a decision boundary, different domains,
long contexts, sarcasm, and unfamiliar language can behave very differently.

Finally, context length is an input contract. The experiment enables truncation
at 64 tokens. In a real system, silently discarding the tail of a document can
change the result; record the limit, inspect the tokenized sequence, and choose
a chunking strategy rather than assuming the model saw everything.

## Alternatives and when to use them

Use a direct model call when you need to inspect preprocessing, logits, labels,
or device placement. Use a pipeline for a well-understood inference task after
the low-level path has been verified. Recurrent models remain useful where
streaming state or very small deployments dominate; task-specific classifiers
can be simpler and more predictable than a general generative model.

## Takeaway

Transformers trade recurrent sequence processing for flexible context mixing,
but they still execute a precise input-to-output contract. Inspect the tokens,
mask, logits, label mapping, model revision, device, and limitations before
turning a convenient prediction into an engineering conclusion.
