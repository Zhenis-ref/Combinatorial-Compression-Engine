from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BackendBase(ABC):
    """
    Backend must:
      - expose current ΔN and ΔD (domain-specific observation)
      - apply Engine controls to the domain process
      - step the process and return metrics for logging and CR calculations
    """

    @abstractmethod
    def reset(self, seed: int = 0) -> None:
        ...

    @abstractmethod
    def observe(self) -> Dict[str, Any]:
        """
        Must return at least:
          {"deltaN": float in [0,1], "deltaD": float in [0,1]}
        """
        ...

    @abstractmethod
    def apply_controls(self, controls: Dict[str, Any]) -> None:
        ...

    @abstractmethod
    def step(self) -> Dict[str, Any]:
        """
        Advances domain process by one tick.
        Returns metrics and 'done': bool.
        """
        ...

    @abstractmethod
    def get_logs(self) -> List[Dict[str, Any]]:
        ...
