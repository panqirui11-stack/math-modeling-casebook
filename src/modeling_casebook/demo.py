from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path

from .facility_location import solve_p_median
from .forecasting import linear_trend_forecast
from .topsis import topsis


def _load_decision_matrix(path: Path) -> tuple[list[str], list[list[float]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    names = [row["option"] for row in rows]
    matrix = [[float(row["quality"]), float(row["speed"]), float(row["cost"])] for row in rows]
    return names, matrix


def build_demo_report(data_path: Path) -> dict[str, object]:
    names, matrix = _load_decision_matrix(data_path)
    decision = topsis(matrix, weights=[0.45, 0.30, 0.25], impacts=["benefit", "benefit", "cost"])
    location = solve_p_median(
        demand_points=[(0, 0), (1, 2), (4, 1), (5, 4)],
        demand_weights=[4, 2, 3, 5],
        candidate_points=[(0, 1), (3, 1), (5, 3)],
        p=2,
    )
    trend = linear_trend_forecast([120, 128, 135, 149, 158, 171], horizon=3)
    return {
        "topsis": {
            "option_scores": {name: score for name, score in zip(names, decision.closeness)},
            "ranking": [names[index] for index in decision.ranking],
        },
        "facility_location": asdict(location),
        "trend_forecast": asdict(trend),
    }


def main() -> int:
    data_path = Path(__file__).resolve().parents[2] / "data" / "decision_matrix.csv"
    print(json.dumps(build_demo_report(data_path), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
