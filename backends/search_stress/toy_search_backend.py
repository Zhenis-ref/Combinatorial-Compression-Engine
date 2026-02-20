from dataclasses import dataclass
from typing import Dict, Any, List
import numpy as np

from interfaces.backend_base import BackendBase
from core.norms import clamp01


@dataclass
class ToySearchParams:
    max_steps: int = 80
    base_branch: int = 14
    branch_min: int = 1
    branch_max: int = 20
    target_progress: float = 1.0


class ToySearchStressBackend(BackendBase):
    """
    Toy stress-test backend (domain-free).
    Emulates combinatorial explosion via a branching process.
    Baseline: fixed branching. DN: branching responds to Engine controls.
    """

    def __init__(self, params: ToySearchParams = ToySearchParams(), dn_control: bool = True):
        self.p = params
        self.dn_control = dn_control
        self.rng = np.random.default_rng(0)
        self.reset(0)

    def reset(self, seed: int = 0) -> None:
        self.rng = np.random.default_rng(seed)
        self.t = 0
        self.progress = 0.0
        self.branch = self.p.base_branch
        self.nodes_expanded = 0
        self.logs: List[Dict[str, Any]] = []

        self.internal_duality = 0.0

    def observe(self) -> Dict[str, Any]:
        dN = clamp01(1.0 - self.progress / max(self.p.target_progress, 1e-9))

        dD = clamp01(
            0.6 * (self.branch - self.p.branch_min) / max((self.p.branch_max - self.p.branch_min), 1)
            + 0.4 * self.internal_duality
        )

        return {"deltaN": dN, "deltaD": dD, "branch": self.branch, "progress": self.progress}

    def apply_controls(self, controls: Dict[str, Any]) -> None:
        if not self.dn_control:
            return

        explore = float(controls.get("explore", 0.0))
        exploit = float(controls.get("exploit", 0.0))

        delta = int(round(5 * explore - 4 * exploit))
        self.branch = int(np.clip(self.branch + delta, self.p.branch_min, self.p.branch_max))

    def step(self) -> Dict[str, Any]:
        obs = self.observe()

        self.nodes_expanded += self.branch

        explore_factor = (self.branch - self.p.branch_min) / max((self.p.branch_max - self.p.branch_min), 1)
        exploit_factor = 1.0 - explore_factor

        base = 0.01 + 0.03 * exploit_factor
        jump = 0.05 * explore_factor * (1.0 if self.rng.random() < 0.15 else 0.0)
        noise = 0.005 * self.rng.normal()

        dprog = max(0.0, base + jump + noise)
        self.progress = min(self.p.target_progress, self.progress + dprog)

        stagnation = 1.0 if dprog < 0.01 else 0.0
        self.internal_duality = clamp01(0.85 * self.internal_duality + 0.2 * explore_factor * stagnation)

        self.t += 1
        done = (self.progress >= self.p.target_progress) or (self.t >= self.p.max_steps)

        metrics = {
            "t": self.t,
            "done": done,
            "nodes_expanded": self.nodes_expanded,
            "progress": self.progress,
            "branch": self.branch,
            "deltaN": obs["deltaN"],
            "deltaD": obs["deltaD"],
        }
        self.logs.append(metrics)
        return metrics

    def get_logs(self) -> List[Dict[str, Any]]:
        return self.logs
