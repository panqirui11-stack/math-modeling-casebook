from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class TopsisResult:
    closeness: tuple[float, ...]
    ranking: tuple[int, ...]


def topsis(
    matrix: Sequence[Sequence[float]],
    weights: Sequence[float],
    impacts: Sequence[str],
) -> TopsisResult:
    """Return closeness coefficients and zero-based option ranking."""
    rows = [tuple(float(value) for value in row) for row in matrix]
    if not rows or not rows[0]:
        raise ValueError("matrix must not be empty")
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError("matrix rows must have equal length")
    if len(weights) != width or len(impacts) != width:
        raise ValueError("weights and impacts must match the number of criteria")
    if any(value < 0 for row in rows for value in row):
        raise ValueError("this demonstration expects non-negative criteria values")
    if any(weight < 0 for weight in weights) or sum(weights) <= 0:
        raise ValueError("weights must be non-negative and have a positive sum")
    if any(impact not in {"benefit", "cost"} for impact in impacts):
        raise ValueError("impacts must be 'benefit' or 'cost'")

    normalized_weights = [float(weight) / sum(weights) for weight in weights]
    denominators = [math.sqrt(sum(row[j] ** 2 for row in rows)) for j in range(width)]
    if any(value == 0 for value in denominators):
        raise ValueError("each criterion must contain at least one non-zero value")
    weighted = [
        tuple(row[j] / denominators[j] * normalized_weights[j] for j in range(width))
        for row in rows
    ]

    positive: list[float] = []
    negative: list[float] = []
    for j, impact in enumerate(impacts):
        column = [row[j] for row in weighted]
        positive.append(max(column) if impact == "benefit" else min(column))
        negative.append(min(column) if impact == "benefit" else max(column))

    closeness: list[float] = []
    for row in weighted:
        d_positive = math.sqrt(sum((row[j] - positive[j]) ** 2 for j in range(width)))
        d_negative = math.sqrt(sum((row[j] - negative[j]) ** 2 for j in range(width)))
        total = d_positive + d_negative
        closeness.append(0.5 if total == 0 else d_negative / total)
    ranking = tuple(sorted(range(len(rows)), key=lambda index: (-closeness[index], index)))
    return TopsisResult(tuple(round(value, 6) for value in closeness), ranking)
