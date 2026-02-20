from typing import Sequence
import numpy as np


def entropy_normalized(weights: Sequence[float], eps: float = 1e-12) -> float:
    w = np.asarray(weights, dtype=float) + eps
    w = w / w.sum()
    H = float(-np.sum(w * np.log(w)))
    K = len(w)
    if K <= 1:
        return 0.0
    return float(np.clip(H / np.log(K), 0.0, 1.0))
