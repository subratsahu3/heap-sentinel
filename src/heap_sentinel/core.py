"""HeapSentinel: Differential Memory Velocity Tracer."""

from collections import deque
from typing import Dict, List, Optional


class DifferentialMemoryTracker:
    """
    Statistical memory leak sentinel.
    Computes first-order velocity and second-order acceleration of tracked object counts
    to identify compounding leaks without blocking production execution threads.
    """

    def __init__(self, window_size: int = 10):
        if window_size < 3:
            raise ValueError("Window size must be at least 3 for second-order analysis.")
        self.window_size = window_size
        self.history: deque[Dict[str, int]] = deque(maxlen=window_size)

    def record_sample(self, counts: Dict[str, int]) -> None:
        """Records a point-in-time dictionary of {type_or_key: count}."""
        self.history.append(dict(counts))

    def compute_velocity(self, key: str) -> Optional[float]:
        """
        Calculates average delta per step for a given key over the window.
        Returns: None if insufficient samples, otherwise float velocity.
        """
        if len(self.history) < 2:
            return None
        deltas = [
            self.history[i].get(key, 0) - self.history[i - 1].get(key, 0)
            for i in range(1, len(self.history))
        ]
        return sum(deltas) / len(deltas)

    def is_leaking(self, key: str, velocity_threshold: float = 5.0) -> bool:
        """
        Evaluates whether a monitored resource is exhibiting sustained positive accumulation.
        """
        vel = self.compute_velocity(key)
        if vel is None:
            return False
        return vel > velocity_threshold
