"""Run: uv run python experiments/02-gradients/autograd.py"""

import torch


def main() -> None:
    weight = torch.tensor(3.0, requires_grad=True)
    target = torch.tensor(10.0)
    prediction = weight * 2
    loss = (prediction - target).pow(2)
    loss.backward()
    print(f"prediction={prediction.item():.1f}, loss={loss.item():.1f}")
    print(f"d(loss)/d(weight)={weight.grad.item():.1f}")


if __name__ == "__main__":
    main()
