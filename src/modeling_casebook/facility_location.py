from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Sequence


Point = tuple[float, float]


@dataclass(frozen=True)
class FacilitySolution:
    selected_indices: tuple[int, ...]
    objective: float
    assignments: tuple[int, ...]


def solve_p_median(
    demand_points: Sequence[Point],
    demand_weights: Sequence[float],
    candidate_points: Sequence[Point],
    p: int,
) -> FacilitySolution:
    """Solve a small Euclidean p-median problem by exhaustive enumeration."""
    if not demand_points or not candidate_points:
        raise ValueError("demand and candidate points must not be empty")
    if len(demand_points) != len(demand_weights):
        raise ValueError("each demand point must have one weight")
    if any(weight < 0 for weight in demand_weights) or sum(demand_weights) <= 0:
        raise ValueError("demand weights must be non-negative and sum to a positive value")
    if not 1 <= p <= len(candidate_points):
        raise ValueError("p must be between 1 and the number of candidates")

    best: FacilitySolution | None = None
    for selected in itertools.combinations(range(len(candidate_points)), p):
        assignments: list[int] = []
        objective = 0.0
        for point, weight in zip(demand_points, demand_weights):
            assigned = min(
                selected,
                key=lambda index: (math.dist(point, candidate_points[index]), index),
            )
            assignments.append(assigned)
            objective += float(weight) * math.dist(point, candidate_points[assigned])
        candidate = FacilitySolution(selected, round(objective, 6), tuple(assignments))
        if best is None or (candidate.objective, candidate.selected_indices) < (
            best.objective,
            best.selected_indices,
        ):
            best = candidate
    assert best is not None
    return best
