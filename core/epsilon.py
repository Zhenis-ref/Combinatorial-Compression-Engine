from dataclasses import dataclass
import numpy as np


@dataclass
class EpsilonParams:
    eps: float = 1e-3
    enabled: bool = True
    mode: str = "white"  # "white" or "none"
    seed: int = 42


class EpsilonProcess:
    """
    ε-process: minimal fluctuation to avoid absorbing/stagnant states.
    For now: white noise. Later we can switch to OU-process if needed.
    """

    def __init__(self, params: EpsilonParams):
        self.params = params
        self.rng = np.random.default_rng(params.seed)

    def sample(self) -> float:
        if (not self.params.enabled) or (self.params.mode == "none"):
            return 0.0
        return float(self.params.eps * self.rng.normal(0.0, 1.0))
