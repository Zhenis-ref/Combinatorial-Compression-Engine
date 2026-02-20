from dataclasses import dataclass


@dataclass
class BifurcationParams:
    deltaN_crit: float = 0.6
    deltaD_bif: float = 0.25
    hysteresis: float = 0.05  # prevents flicker


class BifurcationGate:
    """
    Bifurcation as a regime switch:
      ON  if ΔN high and ΔD still low.
      OFF with hysteresis.
    """

    def __init__(self, params: BifurcationParams):
        self.p = params
        self._on = False

    def update(self, deltaN: float, deltaD: float) -> bool:
        if not self._on:
            if (deltaN >= self.p.deltaN_crit) and (deltaD <= self.p.deltaD_bif):
                self._on = True
        else:
            if (deltaN < (self.p.deltaN_crit - self.p.hysteresis)) or (deltaD > (self.p.deltaD_bif + self.p.hysteresis)):
                self._on = False
        return self._on
