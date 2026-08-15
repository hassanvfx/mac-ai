# Transformer and tokenization notes

Chapter 6 begins with a deliberately narrow inference contract: inspect a
fixed, pretrained binary sentiment classifier both through direct PyTorch calls
and the Hugging Face `pipeline` API. The full result and its limitations are
in `benchmarks/03-transformers/README.md`; the implementation is
`experiments/06-transformers/inspect_sentiment.py`.

Questions to preserve in the prose:

- The tokenizer emits special boundary tokens, integer IDs, and an attention
  mask. Those are model inputs, not a transparent representation of meaning.
- The manual path exposes tokenization, logits, softmax, and label mapping.
  The pipeline hides those operations for convenience. The two paths should
  agree only when they use the same model, tokenizer, device, and parameters.
- A positive or negative output is a model prediction on a fixed label space,
  not a trustworthy judgment about a person, product, or project.
- A one-off MPS/CPU timing on two short sequences cannot establish accelerator
  performance. Keep the counterintuitive result as a limitation rather than
  explaining it away.

Background: [@vaswani2017attention; @wolf2020transformers]. Installation and
cache behavior are documented by Hugging Face [@huggingface2026transformers].
