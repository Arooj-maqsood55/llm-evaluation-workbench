#!/usr/bin/env python3
"""CLI entry point for the LLM Evaluation Workbench."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .reports import write_csv_report, write_json_report
from .scoring import compare_pair


def main() -> None:
    parser = argparse.ArgumentParser(description="Score paired LLM answers with a rubric.")
    sub = parser.add_subparsers(dest="command", required=True)

    score = sub.add_parser("score", help="Score answer pairs")
    score.add_argument("--input", required=True, help="JSON file with answer pairs")
    score.add_argument("--rubric", required=True, help="Rubric JSON file")
    score.add_argument("--out", required=True, help="Output directory")

    args = parser.parse_args()
    if args.command == "score":
        pairs = json.loads(Path(args.input).read_text(encoding="utf-8"))
        rubric = json.loads(Path(args.rubric).read_text(encoding="utf-8"))
        results = [compare_pair(pair, rubric) for pair in pairs]
        out_dir = Path(args.out)
        write_json_report(results, out_dir / "scores.json")
        write_csv_report(results, out_dir / "scores.csv")
        print(f"Wrote {len(results)} comparisons to {out_dir}")


if __name__ == "__main__":
    main()
