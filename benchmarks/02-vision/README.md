# Milestone 2 vision comparison record

## Shared task contract

Both implementations classify the versioned geometric-image fixture defined in
`src/from_tensors_to_agents/vision.py`. It contains three balanced classes:
vertical, horizontal, and diagonal strokes. The fixture is generated locally,
not downloaded, from a fixed seed. It is deliberately small enough for CPU CI
and does **not** establish real-image performance.

| Field | Shared value |
| --- | --- |
| Fixture | 16×16 grayscale synthetic strokes with clipped Gaussian noise (`σ=0.12`) |
| Classes | vertical, horizontal, diagonal |
| Split | train: 32/class; validation: 16/class; test: 16/class |
| Fixture seed | `41` (splits use 41, 42, and 43) |
| Training seed | `17` |
| Model topology | Conv(8, 3×3, same) → ReLU → max pool → Conv(16, 3×3, same) → ReLU → global average pool → dense(3) |
| Optimizer / learning rate | Adam / `0.01` |
| Epochs / batch rule | 30 / full fixture in PyTorch; batch size 32 in Keras |
| Evaluation | held-out test accuracy, 3×3 confusion matrix, and misclassification list |

## Recorded runs — 2026-08-14

| Framework | Runtime / device | Train / validation / test accuracy | Final train loss | Elapsed time | Error analysis |
| --- | --- | --- | --- | --- | --- |
| PyTorch 2.13.0 | Python 3.11.9; MPS available and selected | 1.000 / 1.000 / 1.000 | 0.275691 | 2323.301 ms | 0 mistakes; identity 16-per-class confusion matrix |
| PyTorch 2.13.0 | Python 3.11.9; CPU explicitly selected | 1.000 / 1.000 / 1.000 | 0.275690 | 404.449 ms | 0 mistakes; identity 16-per-class confusion matrix |
| TensorFlow/Keras 2.21.0 | Python 3.11.9; CPU was the only visible TensorFlow device | 1.000 / 1.000 / 1.000 | 0.001079 | 1015.773 ms | 0 mistakes; identity 16-per-class confusion matrix |

TensorFlow emitted a non-fatal `use_unbounded_threadpool` `NodeDef` compatibility warning during the recorded run. Training and evaluation completed successfully; the warning remains a documented environment observation.

## Interpretation and limitations

The measured equivalence is task-level: each implementation learned this
simple, held-out fixture under the declared conditions. Different loss values
are not directly comparable because initializers and framework implementations
differ. The PyTorch CPU observation aligns devices with TensorFlow, but its
one-run, no-shared-warmup measurement is still **not** a framework speed
comparison. It merely confirms that both implementations complete on CPU. Any
timing claim requires a later multi-run benchmark with equivalent warmup and
measurement rules.

The zero-error confusion matrices are expected for a deliberately separable
toy task. Here the error analysis is the explicit absence of errors, coupled
with the identity matrix and the stated reason it cannot generalize to natural
images. A later controlled-difficulty or real-data experiment is necessary
before making any broader vision claim.
