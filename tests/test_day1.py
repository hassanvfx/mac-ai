import torch

from from_tensors_to_agents.day1 import make_regression_data, mean_squared_error
from from_tensors_to_agents.device import preferred_device


def test_broadcasting_has_expected_values() -> None:
    batch = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    result = batch + torch.tensor([10.0, 20.0])
    assert torch.equal(result, torch.tensor([[11.0, 22.0], [13.0, 24.0]]))


def test_autograd_matches_analytic_gradient() -> None:
    weight = torch.tensor(3.0, requires_grad=True)
    loss = (2 * weight - 10).pow(2)
    loss.backward()
    assert weight.grad.item() == -16.0


def test_regression_data_is_deterministic() -> None:
    first = make_regression_data()
    second = make_regression_data()
    assert all(torch.equal(left, right) for left, right in zip(first, second))


def test_mse_is_zero_for_equal_values() -> None:
    values = torch.tensor([1.0, 2.0])
    assert mean_squared_error(values, values).item() == 0.0


def test_preferred_device_is_usable() -> None:
    assert preferred_device().type in {"cpu", "mps"}
