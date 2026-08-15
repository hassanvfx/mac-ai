---
sidebar_position: 4
title: PyTorch vs TensorFlow
---

# PyTorch vs TensorFlow: Same Neural Network, Two Philosophies

## Intuition

The model is mathematical; the framework determines how directly we express,
inspect, and deploy that mathematics. A convolution, a cross-entropy loss, and
Adam do not become different ideas because their APIs differ. What does differ
is where the framework places its boundaries: explicit tensors and loops in
PyTorch, or composable layers and a training interface in Keras.

The useful comparison is therefore not a contest of short code samples. It is
one learning question implemented twice with the data split, seed, topology,
metric, and limits declared in advance.

That discipline protects against an appealing but weak comparison: placing two
unrelated tutorials side by side and judging whichever one has fewer lines. A
framework program includes data layout, initialization, batching, device
selection, defaults, and measurement boundaries as well as model layers. If
those differ, an observed difference may come from the experiment rather than
from the framework. The comparison here is intentionally narrow enough to
inspect, then clear about the questions it cannot answer.

Think of the comparison as a checklist of invariants. The class meaning,
fixture generator, split seeds, labels, topology, optimizer family, learning
rate, epoch budget, and evaluation outputs belong to the problem contract. The
tensor layout, loop API, initializer implementation, batching mechanism, device
visibility, and history object are framework or runtime choices. Separating
these categories is useful whenever results differ: inspect a violated
invariant before attributing the change to a framework philosophy.

## Problem

Train the same small convolutional classifier in PyTorch and TensorFlow/Keras
without changing the fixture, evaluation question, or model shape. The task is
to classify 16×16 synthetic images containing vertical, horizontal, or diagonal
strokes. It is intentionally a controlled teaching fixture, not an image
benchmark [@goodfellow2016deep].

## Minimal implementation

The two runnable implementations are:

```bash
uv run python experiments/05-vision/train_pytorch_cnn.py --device auto --epochs 30
uv sync --group tensorflow
uv run --group tensorflow python experiments/04-tensorflow/train_keras_cnn.py --epochs 30
```

Both use the deterministic fixture in `src/from_tensors_to_agents/vision.py`.
They train the same sequence of operations: two 3×3 convolutional layers with
8 then 16 channels, ReLU activations, pooling, global average pooling, and a
three-output classifier. Both use Adam with learning rate `0.01`, training seed
`17`, and 30 epochs. PyTorch keeps the optimization loop visible; Keras
encapsulates it in `model.fit` while keeping the model definition readable.

TensorFlow is an opt-in project group, not a requirement for the first three
chapters. The official TensorFlow installation guide is the authority for
supported platform details [@tensorflow2026install].

The two APIs make different trade-offs in visibility. In the PyTorch program,
the reader can see the forward call, loss, `backward()`, and optimizer update in
the source. This makes it easy to insert a diagnostic or change the training
rule. In the Keras program, `compile` declares the optimizer and loss, and
`fit` owns the standard loop. This removes routine code and collects a training
history, but custom behavior moves into callbacks or a custom training step.
Neither presentation changes the underlying objective; choose the boundary that
makes the current task easiest to verify.

Layout is a practical example. PyTorch convolution layers conventionally read
images as `(batch, channels, height, width)`. The Keras implementation receives
the same fixture after an explicit conversion to `(batch, height, width,
channels)`. The values and labels are shared; only their documented layout
changes. Omitting this conversion could produce an error, but worse, a shape
that happens to be accepted might make a different network from the one being
compared.

## Real implementation: compare the contract before the syntax

The comparison record at `benchmarks/02-vision/README.md` fixes the train,
validation, and test partitions at 32, 16, and 16 examples per class. It also
requires held-out accuracy, a three-by-three confusion matrix, and a list of
mistakes. Those checks matter more than matching a particular layer spelling:
they tell us whether each program has learned the same stated task.

Read the comparison table as a contract, not a leaderboard. The partitions are
fixed before either model is trained. Accuracy is evaluated separately, the
confusion matrix keeps per-class results visible, and the error list preserves
the examples behind a metric. For this separable fixture, zero test errors are
expected and still recorded explicitly. In a realistic vision problem, inspect
representative errors, class imbalance, ambiguous labels, and changes across
seeds before drawing conclusions from one score.

Fairness has limits even in this matched exercise. The PyTorch loop uses the
full training fixture as one batch while Keras uses batches of 32, and the
frameworks choose their own initial parameter values. These choices can affect
loss trajectories and elapsed time, so they are documented rather than hidden.
The educational question is whether both programs solve the declared held-out
task, not whether their internal states are bit-for-bit identical.

The confusion matrix is not decoration. Rows represent actual classes and
columns predicted classes in the shared helper. An identity matrix with sixteen
examples on each diagonal says every held-out stroke type was predicted as
itself in this fixture. The accompanying empty mistake list has meaning only
because its index space, labels, and split are fixed. On a harder task, save
representative mistakes and inspect whether they cluster around one class,
noise level, or preprocessing transformation.

The topology is equivalent at the level that matters to this lesson, not a
claim of identical parameter tensors. Both models apply same-padded 3×3
convolutions, ReLUs, pooling, global average pooling, and three final logits.
Different libraries initialize weights differently and may order or fuse
operations differently. Requiring bit-for-bit agreement would turn a lesson
about controlled task behavior into a fragile implementation test. Requiring
the declared fixture, held-out evaluation, and error report instead makes the
comparison useful and reproducible.

## Experiment

On the recorded Mac, PyTorch 2.13.0 completed the fixture with MPS selected and
also with CPU explicitly selected. TensorFlow/Keras 2.21.0 saw CPU as its only
visible device. Each recorded run reached 1.000 train, validation, and test
accuracy with an identity confusion matrix (16 held-out examples correct in
each class) and no mistakes. The raw results, versions, and elapsed values are
in `benchmarks/02-vision/README.md`.

That is task-level agreement, not a framework performance result. The runs use
different device paths and only one timing observation per configuration;
neither a loss value nor elapsed milliseconds establish that one framework is
faster. The final losses also differ because initializers and implementation
details differ. A proper speed comparison needs repeated runs, shared warmup,
equivalent device selection, and a declared timing boundary.

The MPS PyTorch run is slower than the recorded CPU run for this tiny workload.
That is not a contradiction of the idea that accelerators can help: setup,
dispatch, and synchronization can outweigh parallel computation when the work
is small. It is also not proof that CPU is generally faster. The only supported
statement is the one in the record: these wall-clock values were observed under
the declared, one-run conditions. Treat any broader conclusion as a hypothesis
requiring a larger, repeated, device-matched experiment.

Reproducibility also has levels. Fixed fixture generation and explicit seeds
make this CPU-friendly teaching task repeatable. They do not guarantee identical
floating-point traces across library versions, devices, or kernels. Record the
versions, selected device, data layout conversion, and observed final metrics;
then treat an unexpected divergence as an investigation prompt. A seed narrows
uncertainty; it is not a promise that every numerical detail is portable.

## What broke

Framework setup was the first practical difference. The core project does not
install TensorFlow, so the Keras experiment requires `uv sync --group
tensorflow`. On this Mac it ran on CPU only and emitted a non-fatal
`use_unbounded_threadpool` NodeDef compatibility warning; training and
evaluation still completed. Treat such a warning as an environment observation
to investigate, not as evidence that the result is invalid or portable.

A more subtle failure is false equivalence. Matching names such as `Conv2d` and
`Conv2D` is insufficient if layouts, padding, shuffling, splits, or metrics
change. The shared fixture converts PyTorch's channels-first tensor to Keras's
channels-last input explicitly, then verifies the same held-out labels.

Data leakage is another comparison failure. If generated images from the same
random pattern, augmentation lineage, or preprocessing cache cross the split
boundary, both frameworks may report excellent held-out accuracy while the
evaluation question has been compromised. The fixture uses distinct declared
seeds for its splits. When replacing it with a real dataset, preserve the split
manifest and fit normalization statistics only on the training partition.

## Alternatives and when to use them

Use PyTorch when an explicit training loop and immediate tensor inspection help
you learn or debug. Use Keras when a compact model-and-training declaration is
a better fit for the team and deployment path. JAX, higher-level PyTorch
trainers, and other ecosystems are valid alternatives, but should enter only
after the evaluation contract is stable.

Use a custom Keras `GradientTape` loop when the experiment requires the same
step-level control demonstrated in PyTorch; use PyTorch's module and optimizer
interfaces when an explicit loop remains clearest. Avoid choosing from
benchmark headlines when hardware, model size, precision, data pipeline, or
deployment target differs from the work at hand. A repeatable question and a
maintained test fixture are more durable assets than a short-lived ranking.

For a production comparison, expand the fixture before expanding the rhetoric.
Use a versioned real-data manifest or a more varied synthetic generator,
preserve train-only preprocessing, select a metric that reflects actual error
cost, and repeat across declared seeds. Only after correctness is fixed should
a separate performance protocol select matching devices, warm-ups, precision,
batch sizes, run counts, and timers. The two reports then answer different
questions without smuggling one conclusion into the other.

## Evidence trail

The shared framework note is `research/02-vision-and-frameworks/notes.md`.
Run `experiments/05-vision/train_pytorch_cnn.py` and
`experiments/04-tensorflow/train_keras_cnn.py`; compare their recorded contract
in `benchmarks/02-vision/README.md`, not elapsed values alone.

## Takeaway

Framework choice is an engineering trade-off, not a different theory of
learning. Start with a shared question and evidence contract; then let API
clarity, operational requirements, and measured constraints determine the
tool.
