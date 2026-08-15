"""Run: uv run python experiments/01-tensors/broadcasting.py"""

import torch


def main() -> None:
    batch = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    bias = torch.tensor([0.1, 0.2, 0.3])
    print("batch shape:", tuple(batch.shape))
    print("bias shape:", tuple(bias.shape))
    print("broadcast sum:\n", batch + bias)


if __name__ == "__main__":
    main()
