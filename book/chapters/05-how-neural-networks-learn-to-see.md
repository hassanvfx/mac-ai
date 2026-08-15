---
sidebar_position: 5
title: How Neural Networks Learn to See
---

# How Neural Networks Learn to See

## Intuition

Convolutions use local structure and repeated filters to turn pixels into useful
features. A filter that responds to a short vertical stroke can be useful at
many image positions, so a convolution shares the same learned weights across
the image. Pooling and later layers combine local responses into a decision
about the whole image [@goodfellow2016deep].

The important idea is *inductive bias*: a convolution assumes that nearby
pixels matter together and that a useful local pattern may appear in more than
one position. A fully connected layer can in principle learn such patterns,
but it assigns a separate weight to every input connection. A convolution uses
one small kernel repeatedly, which reduces parameters and expresses the useful
prior that a vertical edge is still a vertical edge when it shifts a few pixels.

![The tiny CNN changes channels and spatial resolution while preserving the batch.](../assets/vision/cnn-feature-flow.svg)

The receptive field grows as layers compose. A first 3×3 filter sees a small
patch; after pooling and a second convolution, a feature can depend on a wider
region of the original 16×16 image. Global average pooling then summarizes each
feature map across all remaining positions. This does not mean the network has
learned human concepts such as “line” or “object.” It means the architecture
offers a route from local pixel patterns to a translation-tolerant class score.

The phrase “feature map” names an intermediate tensor, not a verified picture
of what the network sees. One channel may respond strongly to a stroke-like
pattern in this fixture, but its values are the result of learned filters,
nonlinearities, and the data distribution—not a human-approved concept label.
Visualizing feature maps can help debug dimensions, dead channels, or saturated
activations. It cannot prove that a prediction was caused by a visual story a
reader prefers.

Receptive field has a boundary. A wider field lets a later unit combine more of
the image, but it does not restore detail a pooling step or crop removed. For
this 16×16 fixture, two convolutions and pooling make a compact teaching model.
For a high-resolution task, the same choices can discard thin objects or exact
positions. Begin with “what must remain distinguishable?” rather than layer
count.

## Problem

Train and inspect a small image classifier rather than treating a CNN as a black
box. We need more than a final accuracy: the split must be held out, the output
classes must be named, and errors must be inspectable.

## Minimal implementation

The companion fixture creates three balanced classes of 16×16 grayscale
images: a vertical, horizontal, or diagonal noisy stroke. It is generated from
fixed seeds and stored as code, so a reader does not depend on an external
download or an unstable train/test split.

Run the complete PyTorch implementation:

```bash
uv run python experiments/05-vision/train_pytorch_cnn.py --device auto --epochs 30
```

The model is deliberately small:

```text
image → Conv(8) → ReLU → max pool → Conv(16) → ReLU → global average pool → 3 logits
```

Logits are unnormalized class scores. Cross-entropy compares them to the known
class index, and Adam changes the filters to reduce that loss.

The actual tensor path is worth writing down. The fixture produces a
channels-first batch `(N, 1, 16, 16)`. The first padded 3×3 convolution keeps
the 16×16 spatial grid while changing one input channel into eight learned
feature maps. Max pooling halves height and width to `(N, 8, 8, 8)`. The next
convolution creates 16 feature maps, and adaptive global-average pooling turns
each entire map into one number. Flattening produces `(N, 16)`, then the final
linear layer emits `(N, 3)` logits—one score for each named class.

Pooling does not discover an object; it discards some exact location detail in
exchange for a compact local summary. On this fixture, that is a reasonable
choice because a stroke may be offset slightly. On a task where exact position
is the answer, aggressive pooling can remove the signal we need. Architecture
is therefore a hypothesis about the task, not a collection of default layers.

## Real implementation: an inspection-friendly evaluation

`src/from_tensors_to_agents/vision.py` owns the fixture, model, class names,
and confusion-matrix function. The training script reports train, validation,
and test accuracy separately; it also prints the confusion matrix with actual
classes in rows and predicted classes in columns, followed by every held-out
mistake. This output is intentionally simple enough to test in CPU CI.

Separate modes make evaluation meaningful. During training, `model.train()`
declares that train-time behavior should be active; before producing test
predictions, the script uses `model.eval()` and `torch.no_grad()`. The tiny
network has no dropout or batch normalization, so the numerical effect is small
here, but preserving the boundary establishes a habit needed for larger models.
`no_grad()` also says that prediction is not part of a later update, avoiding
unnecessary graph storage.

The confusion matrix answers a question accuracy hides: *which* cases are
wrong? Rows are actual classes and columns are predicted classes. If diagonal
strokes were repeatedly predicted as vertical, the corresponding off-diagonal
cell would identify a particular failure direction. The mistake list supplies
individual fixture indexes to inspect. A zero-error matrix is not empty
evidence; it documents that none of the declared error categories occurred on
the frozen held-out data.

The loss and metric answer different questions. Cross-entropy uses every logit
and known target to create a differentiable learning signal; accuracy discards
margin information and counts only whether the highest logit has the right
class. A model can improve cross-entropy while accuracy stays unchanged, or
reach the same accuracy with more or less decisive scores. Keep both when
debugging training, then inspect examples and the confusion matrix before
deciding whether either result is useful.

Validation data guides choices such as epoch budget, architecture, or noise
level. Test data estimates the final declared task after those choices are made.
Repeatedly using the test score to select a configuration turns it into another
validation set. This small fixture keeps all three splits because the habit is
more important than the difficulty of the current images.

### A decision rule for the three splits

Use training data to compute gradients. Use validation data to compare a small
number of predeclared alternatives: two learning rates, a pooling choice, or a
noise condition. Freeze the selected configuration, then evaluate the test
split once as the reported result. If a test result prompts another architecture
change, the old test set has become model selection and a new held-out split is
needed for an honest final estimate.

On a small fixture, record counts as well as percentages. Accuracy of 1.000 on
48 held-out examples means 48 declared predictions were correct; it does not
estimate a large-population error rate precisely. The identity matrix and empty
mistake list add detail, but do not make the sample larger.

### From an error to a hypothesis

If a harder follow-up makes diagonal strokes become vertical predictions, do
not immediately add layers. Open the named examples, compare their conditions
with correct diagonals, and check preprocessing and labels. Then state a
falsifiable hypothesis—perhaps pooling removes a displaced diagonal cue—and
test one intervention against the same fixed test condition. This connects an
off-diagonal cell to an experiment rather than an anecdote.

## Experiment

The recorded PyTorch MPS run used 32 training examples per class, 16 validation
examples per class, 16 held-out test examples per class, seed `17`, Adam at
`0.01`, and 30 epochs. It reached 1.000 accuracy on each split. Its held-out
matrix was the identity matrix: each of the 16 vertical, 16 horizontal, and 16
diagonal test examples was classified correctly. The explicit CPU run produced
the same accuracy and zero mistakes. See `benchmarks/02-vision/README.md` for
the complete record and timing limitations.

Zero mistakes are still an error-analysis result: there were no misclassified
examples to inspect under this controlled distribution. They do *not* mean the
network can see in the everyday sense. The images are highly separable, the
same generator supplies every split, and the test set is small. A next
experiment should make the boundary less clean—for example by varying stroke
position, contrast, or noise—and report which classes then confuse one another
before considering a real image dataset.

Use this result as a baseline, then make one change at a time. Increase noise
without changing split sizes and inspect whether errors first concentrate in
diagonal examples. Translate strokes farther from the center and ask whether
pooling helps enough. Reduce training examples per class and track the gap
between train and validation accuracy. Each variation tests a concrete
hypothesis about data, rather than asking a larger model to solve an undefined
problem. Commit the changed generator settings and result before describing a
robustness finding in prose.

To create a controlled-difficulty follow-up, change exactly one generator
condition: raise Gaussian noise, increase translation range, thin strokes, or
reduce training examples. Keep class balance, test seed, topology, and metrics
fixed. State the hypothesis before running—for example, “diagonal strokes will
be confused with vertical strokes under larger offsets”—then inspect the matrix
and saved mistakes. A harder score alone is not a finding until its error shape
and changed condition are recorded.

Keep a baseline record immutable. A controlled variant needs its own generator
settings, split seeds, model/optimizer settings, device, metrics, matrix,
mistakes, and limitations. Otherwise a later noisy run can overwrite the
perfect baseline and make it impossible to identify what changed. Benchmark
records preserve this history; prose should point to the executable condition.

### Worked error-analysis case: accuracy needs a direction

The current baseline has no held-out mistakes, so use the small confusion-matrix
unit test to practice reading a non-perfect result. Its actual labels are
`[vertical, horizontal, horizontal]`, while its predictions are
`[vertical, diagonal, horizontal]`. With actual classes as rows and predicted
classes as columns, the matrix is:

```text
                 predicted
actual       vertical  horizontal  diagonal
vertical          1         0          0
horizontal        0         1          1
diagonal          0         0          0
```

The single off-diagonal cell says more than “two out of three were correct.”
One horizontal example was predicted as diagonal. It does not say that every
horizontal image is hard, that diagonal filters are wrong, or that the network
needs another layer. It identifies a direction for inspection: open the named
fixture index, compare its stroke position, thickness, and noise with correct
horizontal examples, and verify the label and preprocessing before changing an
architecture.

Turn that observation into a narrow hypothesis. For example: “larger vertical
offsets make horizontal strokes resemble diagonals after pooling.” Create a new
fixture configuration that changes only the offset range, preserve the class
balance and split seeds, and run the same train/validation/test protocol. If
the horizontal-to-diagonal cell grows while other conditions stay fixed, the
result supports a specific robustness question. If it does not, the original
mistake may have been an isolated noisy example rather than evidence for a
design change.

The baseline's identity matrix remains valuable beside this hypothetical case.
It establishes that the declared easy distribution has no errors; the variant
would establish how one changed distribution behaves. Do not overwrite the
identity matrix or report only the worse aggregate accuracy. Versioned matrices
and mistake lists let a future reader distinguish a changed task from a
regression in the original one.

## What broke

The easy failure is to report training accuracy alone. A model can memorize a
tiny fixture while performing poorly on unseen data, so this experiment keeps
validation and test partitions separate. Another easy failure is a layout
mismatch: PyTorch convolution expects channels-first inputs while Keras uses a
channels-last version of the same fixture. The matched framework experiment
converts that layout explicitly rather than relying on an implicit transpose.

Finally, do not call this a general CNN benchmark. Its purpose is to make the
flow from pixels to logits inspectable and deterministic; it does not measure
augmentation, robustness, scale, or real-world generalization.

An incomplete error analysis is a failure too. A single accuracy value omits
whether one class was never recognized, whether errors repeat a visual pattern,
and whether mistakes came from training, validation, or test data. Keep class
names and matrix ordering with the recorded result. When a real dataset
replaces this fixture, examine labels as well as predictions: a model cannot
learn a distinction that annotators apply inconsistently.

Distribution shift is the larger version of the same problem. The fixture
assumes centered-ish strokes, clipped Gaussian noise, and three balanced named
classes. A camera image with texture, a new diagonal angle, or an unrepresented
class asks a different question. A confident output is still only one of the
original three logits. Before using a CNN in a new environment, collect
representative held-out data, decide how unknowns are handled, and evaluate the
error patterns that matter to users.

## Alternatives and when to use them

For image-like grids with local patterns, convolution gives a useful inductive
bias and often needs less data than a fully connected network. A small linear
classifier is a worthwhile baseline when the relationship may be simple. For
large-scale vision work, residual CNNs and vision transformers are common
alternatives, but they add capacity and evaluation requirements that would hide
this chapter's basic lesson.

Data augmentation is an alternative when the real deployment distribution
contains harmless rotations, crops, or illumination changes. Apply it only to
the training partition and state exactly which transformations are permitted;
augmenting held-out examples invalidates the evaluation boundary. Residual CNNs
can train deeper feature extractors, and vision transformers use patch tokens
and attention instead of convolution. Both are useful later, but neither makes
a tiny, perfectly separable fixture a proxy for real-world vision.

There is also a lesson in the fixture's construction. Train, validation, and
test images use separate random seeds, but share the same generating family.
That is appropriate for a controlled lesson about the learning loop, while also
limiting what the result establishes. A real deployment may have camera noise,
backgrounds, labels, and class proportions that this generator never models.
The correct response is not to claim robustness from a toy score; it is to
create a new versioned evaluation question with those conditions represented.

Segmentation, detection, and keypoint tasks are further alternatives when a
single class label discards information the product needs. Their outputs carry
spatial structure, so datasets, losses, metrics, and error review must do the
same. A classifier that calls a scene “diagonal” cannot replace a system that
must identify where a defect lies. Match output representation to the decision
the user must make before choosing an architecture family.

## Evidence trail

The fixture and CNN are defined in `src/from_tensors_to_agents/vision.py`; the
research note is `research/02-vision-and-frameworks/notes.md`. Run
`experiments/05-vision/train_pytorch_cnn.py` and inspect the evidence record in
`benchmarks/02-vision/README.md`.

## Takeaway

Neural networks learn to see by turning repeated local measurements into a
loss-driven decision. Trust the result only as far as its held-out data,
confusion matrix, error list, and stated limitations allow.
