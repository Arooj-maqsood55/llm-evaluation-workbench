#!/usr/bin/env python3
"""CLI workbench for rubric scoring of paired LLM answers."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


DEFAULT_RUBRIC = {
    "task_completion": 0.3,
    "factual_accuracy": 0.3,
    "instruction_adherence": 0.2,
    "clarity": 0.2,
}


def weighted_score(scores: dict[str, int], weights: dict[str, float]) -> float:
    total = 0.0
    for key, weight in weights.items():
        total += scores[key] * weight
    return round(total, 3)


def compare_pair(pair: dict[str, Any], weights: dict[str, float]) -> dict[str, Any]:
    a = weighted_score(pair["scores_a"], weights)
    b = weighted_score(pair["scores_b"], weights)
    if a > b:
        preferred = "response_a"
    elif b > a:
        preferred = "response_b"
    else:
        preferred = "tie"
    return {
        "id": pair["id"],
        "score_a": a,
        "score_b": b,
        "preferred": preferred,
        "notes": pair.get("notes", ""),
    }


def load_pairs(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else [data]


def write_json(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(json.dumps(rows, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Score paired LLM answers with a fixed rubric.")
    parser.add_argument("input", type=Path, help="JSON file with scored pairs")
    parser.add_argument("--out-json", type=Path, default=Path("report.json"))
    parser.add_argument("--out-csv", type=Path, default=Path("report.csv"))
    args = parser.parse_args()

    pairs = load_pairs(args.input)
    results = [compare_pair(pair, DEFAULT_RUBRIC) for pair in pairs]
    write_json(args.out_json, results)
    write_csv(args.out_csv, results)
    print(f"Wrote {args.out_json} and {args.out_csv} ({len(results)} pairs).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
