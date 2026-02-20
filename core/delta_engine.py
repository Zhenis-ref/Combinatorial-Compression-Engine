from dataclasses import dataclass
from typing import Dict, Any
import numpy as np

from .norms import clamp01
from .bifurcation import BifurcationGate, BifurcationParams
from .epsilon import EpsilonProcess, EpsilonParams


@dataclass
class DeltaParams:
    # Canonical α-shape
    A: float = 1.0
    k: float = 10.0
    deltaN_crit: float = 0.6
    p: float = 1.0
    eps_floor: float = 1e-3
    beta: float = 0.1

    # Regime boost in bifurcation
    A_bif: float = 2.0
    beta_bif: float = 0.15

    # Control target
    dsdt_target: float = 1.0


@dataclass
class EngineOutput:
    deltaN: float
    deltaD: float
    alpha: float
    dsdt: float
    bifurcation: bool
    noise: float
    controls: Dict[str, Any]


class DeltaEngine:
    """
    Universal DN Engine (domain-agnostic):

      dS/dt = α(ΔN,ΔD)*ΔN + β*ΔD + ε*ξ(t)

      α(ΔN,ΔD) = A / [(1+exp(-k(ΔN-ΔNcrit))) * (ΔD^p + eps_floor)]
    """

    def __init__(
        self,
        params: DeltaParams = DeltaParams(),
        bif_params: BifurcationParams = BifurcationParams(),
        eps_params: EpsilonParams = EpsilonParams(),
    ):
        self.p = params
        # ensure bif gate uses same deltaN_crit as engine params
        bif_params.deltaN_crit = self.p.deltaN_crit
        self.bif = BifurcationGate(bif_params)
        self.eps_proc = EpsilonProcess(eps_params)

    def alpha(self, deltaN: float, deltaD: float, A: float) -> float:
        dN = clamp01(deltaN)
        dD = clamp01(deltaD)
        gate = 1.0 + np.exp(-self.p.k * (dN - self.p.deltaN_crit))
        denom = gate * ((dD ** self.p.p) + self.p.eps_floor)
        return float(A / max(denom, 1e-12))

    def step(self, deltaN: float, deltaD: float) -> EngineOutput:
        dN = clamp01(deltaN)
        dD = clamp01(deltaD)

        is_bif = self.bif.update(dN, dD)
        A = self.p.A_bif if is_bif else self.p.A
        beta = self.p.beta_bif if is_bif else self.p.beta

        a = self.alpha(dN, dD, A=A)
        noise = self.eps_proc.sample()
        dsdt = float(a * dN + beta * dD + noise)

        # Universal control signals (backend decides how to use them)
        err = dsdt - self.p.dsdt_target
        controls = {
            "mode": "bifurcation" if is_bif else "normal",
            "explore": float(np.clip(-err, 0.0, 1.0)),  # dsdt below target => explore
            "exploit": float(np.clip(err, 0.0, 1.0)),   # dsdt above target => exploit
            "dsdt_target": self.p.dsdt_target,
        }

        return EngineOutput(
            deltaN=dN,
            deltaD=dD,
            alpha=a,
            dsdt=dsdt,
            bifurcation=is_bif,
            noise=noise,
            controls=controls,
        )
