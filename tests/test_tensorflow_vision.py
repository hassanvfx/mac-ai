import importlib.util
import runpy
from pathlib import Path

import numpy as np
import pytest

SCRIPT = Path(__file__).parents[1] / "experiments/04-tensorflow/train_keras_cnn.py"


@pytest.mark.skipif(importlib.util.find_spec("tensorflow") is None, reason="optional tensorflow group")
def test_keras_nhwc_conversion_and_model_shape() -> None:
    module = runpy.run_path(str(SCRIPT))
    converted = module["to_nhwc"](np.zeros((2, 1, 16, 16), dtype=np.float32))
    assert converted.shape == (2, 16, 16, 1)
    assert module["make_model"]().output_shape == (None, 3)
