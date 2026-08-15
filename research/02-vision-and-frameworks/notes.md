# Vision and framework-comparison notes

The Milestone 2 comparison deliberately uses one synthetic, versioned fixture
so that framework code—not dataset download state—accounts for the observed
difference. The fixture and its exact split live in
`src/from_tensors_to_agents/vision.py`; the recorded runs and limits live in
`benchmarks/02-vision/README.md`.

Questions for the chapter drafts:

- Which aspects of the experiment are mathematical invariants, and which are
  framework choices?
- Do matching accuracy and topology justify a timing conclusion? No: only a
  shared, repeated, warmed-up timing protocol could support that claim.
- What should an error report say when the held-out fixture has no errors?
  State that result, inspect the confusion matrix, and explain why it does not
  establish real-world image performance.

The convolutional framing follows [@goodfellow2016deep]. TensorFlow's current
installation support is recorded from its official pip guide
[@tensorflow2026install].
