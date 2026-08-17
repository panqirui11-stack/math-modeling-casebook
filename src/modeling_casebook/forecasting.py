from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class TrendForecast:
    intercept: float
    slope: float
    fitted: tuple[float, ...]
    forecast: tuple[float, ...]
    r_squared: float


def linear_trend_forecast(values: Sequence[float], horizon: int) -> TrendForecast:
    """Fit y = intercept + slope*t by ordinary least squares."""
    series = [float(value) for value in values]
    if len(series) < 2:
        raise ValueError("at least two observations are required")
    if horizon < 1:
        raise ValueError("horizon must be positive")
    times = list(range(len(series)))
    mean_t = sum(times) / len(times)
    mean_y = sum(series) / len(series)
    denominator = sum((time - mean_t) ** 2 for time in times)
    slope = sum((time - mean_t) * (value - mean_y) for time, value in zip(times, series)) / denominator
    intercept = mean_y - slope * mean_t
    fitted = [intercept + slope * time for time in times]
    forecast = [intercept + slope * time for time in range(len(series), len(series) + horizon)]
    ss_res = sum((actual - predicted) ** 2 for actual, predicted in zip(series, fitted))
    ss_tot = sum((actual - mean_y) ** 2 for actual in series)
    r_squared = 1.0 if ss_tot == 0 and ss_res == 0 else (0.0 if ss_tot == 0 else 1 - ss_res / ss_tot)
    return TrendForecast(
        intercept=round(intercept, 6),
        slope=round(slope, 6),
        fitted=tuple(round(value, 6) for value in fitted),
        forecast=tuple(round(value, 6) for value in forecast),
        r_squared=round(r_squared, 6),
    )
