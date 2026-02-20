from dataclasses import dataclass
from typing import Dict, Any, List
import numpy as np

from interfaces.backend_base import BackendBase
from core.norms import clamp01


@dataclass
class ToyDecodingParams:
    max_steps: int = 40
    k_min: int = 1
    k_max: int = 8
    k_init: int = 1
    target_score: float = 1.0


class ToyDecodingBackend(BackendBase):
    """
    Toy DN-regulated decoding backend (domain-free).
    Baseline: fixed k=1. DN: k responds to Engine controls.
    Metric: calls (proxy for model calls).
    """

    def __init__(self, params: ToyDecodingParams = ToyDecodingParams(), dn_control: bool = True):
        self.p = params
        self.dn_control = dn_control
        self.rng = np.random.default_rng(0)
        self.reset(0)

    def reset(self, seed: int = 0) -> None:
        self.rng = np.random.default_rng(seed)
        self.t = 0
        self.k = self.p.k_init
        self.calls = 0
        self.score = 0.0
        self.duality = 0.0
        self.logs: List[Dict[str, Any]] = []

    def observe(self) -> Dict[str, Any]:
        dN = clamp01(1.0 - self.score / max(self.p.target_score, 1e-9))
        dD = clamp01(
            0.7 * (self.k - self.p.k_min) / max((self.p.k_max - self.p.k_min), 1)
            + 0.3 * self.duality
        )
        return {"deltaN": dN, "deltaD": dD, "k": self.k, "score": self.score, "calls": self.calls}

    def apply_controls(self, controls: Dict[str, Any]) -> None:
        if not self.dn_control:
            return
        explore = float(controls.get("explore", 0.0))
        exploit = float(controls.get("exploit", 0.0))
        delta = int(round(3 * explore - 3 * exploit))
        self.k = int(np.clip(self.k + delta, self.p.k_min, self.p.k_max))

    def step(self) -> Dict[str, Any]:
        obs = self.observe()

        self.calls += self.k

        explore_factor = (self.k - self.p.k_min) / max((self.p.k_max - self.p.k_min), 1)
        base = 0.02 + 0.02 * (1.0 - explore_factor)
        jump = 0.07 * explore_factor * (1.0 if self.rng.random() < 0.20 else 0.0)
        noise = 0.005 * self.rng.normal()

        dscore = max(0.0, base + jump + noise)
        self.score = min(self.p.target_score, self.score + dscore)

        stagnation = 1.0 if dscore < 0.02 else 0.0
        self.duality = clamp01(0.9 * self.duality + 0.25 * explore_factor * stagnation)

        self.t += 1
        done = (self.score >= self.p.target_score) or (self.t >= self.p.max_steps)

        metrics = {
            "t": self.t,
            "done": done,
            "calls": self.calls,
            "score": self.score,
            "k": self.k,
            "deltaN": obs["deltaN"],
            "deltaD": obs["deltaD"],
        }
        self.logs.append(metrics)
        return metrics

    def get_logs(self) -> List[Dict[str, Any]]:
        return self.logs
