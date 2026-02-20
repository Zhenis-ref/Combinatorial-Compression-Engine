from typing import Sequence
import numpy as np


def normalized_kl(q: Sequence[float], p: Sequence[float], eps: float = 1e-12) -> float:
    q = np.asarray(q, dtype=float) + eps
    p = np.asarray(p, dtype=float) + eps
    q = q / q.sum()
    p = p / p.sum()
    kl = float(np.sum(q * np.log(q / p)))
    n = len(q)
    if n <= 1:
        return 0.0
    return float(np.clip(kl / np.log(n), 0.0, 1.0))
