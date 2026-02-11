"""Export evaluation results to JSON and CSV."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


def write_json_report(results: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(results, indent=2), encoding="utf-8")


def write_csv_report(results: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["pair_id", "preferred", "score_a", "score_b", "criteria_version"],
        )
        writer.writeheader()
        for item in results:
            writer.writerow(
                {
                    "pair_id": item["pair_id"],
                    "preferred": item["preferred"],
                    "score_a": item["A"]["total"],
                    "score_b": item["B"]["total"],
                    "criteria_version": item["criteria_version"],
                }
            )
