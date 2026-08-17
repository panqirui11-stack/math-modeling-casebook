"""Small, auditable mathematical modeling examples."""

from .facility_location import FacilitySolution, solve_p_median
from .forecasting import TrendForecast, linear_trend_forecast
from .topsis import TopsisResult, topsis

__all__ = [
    "FacilitySolution",
    "TrendForecast",
    "TopsisResult",
    "linear_trend_forecast",
    "solve_p_median",
    "topsis",
]
